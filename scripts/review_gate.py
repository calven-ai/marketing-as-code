#!/usr/bin/env python3
"""The review gate: run from main by gate.yml after every check run,
never from the proposal. Classifies a proposal as bookkeeping
(agent-maintained files only, per docs/schema.json plus the hard-coded
never-bookkeeping list in scripts/lint.py) or needs-review, applies the
safe fixes as a Tidy commit, labels it, publishes the `review-gate` check
on its head commit, and merges a bookkeeping proposal itself once the
health check succeeded on that exact commit. A needs-review proposal
passes only when someone other than the author has approved it, unless
docs/schema.json sets review.self_merge (one maintainer): then the
author's own merge is the approval.

Usage, from a checkout of main (gate.yml calls it):
    python3 scripts/review_gate.py --pr 12 --head-sha <sha> --doctor success
    python3 scripts/review_gate.py --pr 12 --dry-run     # classify and say what would happen

Exit 0 means "this proposal may land" (or has landed). Exit 1 means it
waits: for a green health check, a Tidy commit's re-run, or a person. The
check it publishes needs an Actions token (checks: write); locally, use
--dry-run.
"""

import argparse
import fnmatch
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint  # noqa: E402
from _common import CommandError, find_gh, gh, git  # noqa: E402

ROOT = lint.ROOT
LABELS = {"bookkeeping": "bookkeeping", "needs-review": "needs-review"}
CHECK = "review-gate"
BOT_NAME, BOT_EMAIL = "github-actions[bot]", "41898282+github-actions[bot]@users.noreply.github.com"


def codeowners_for(paths):
    """Owners whose CODEOWNERS pattern matches any of the paths (last match wins per path)."""
    rel = ROOT / ".github" / "CODEOWNERS"
    if not rel.is_file():
        return []
    rules = []
    for line in rel.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        pattern, *owners = line.split()
        rules.append((pattern.strip("/"), owners))
    found = []
    for path in paths:
        owners = []
        for pattern, rule_owners in rules:
            if path == pattern or path.startswith(pattern + "/") or fnmatch.fnmatch(path, pattern) \
                    or fnmatch.fnmatch(path, pattern + "/*") or fnmatch.fnmatch(path, pattern + "/**"):
                owners = rule_owners
        for o in owners:
            if o not in found and not o.endswith("owner-placeholder"):
                found.append(o)
    return found


def approvals(pr):
    data = json.loads(gh("pr", "view", str(pr), "--json", "author,reviews,latestReviews"))
    author = data.get("author", {}).get("login", "")
    latest = data.get("latestReviews") or data.get("reviews") or []
    approved = sorted({r["author"]["login"] for r in latest
                       if r.get("state") == "APPROVED" and r.get("author", {}).get("login") != author})
    return author, approved


def self_merge_allowed(schema):
    """review.self_merge in docs/schema.json, or the repository variable REVIEW_SELF_MERGE=true (gate.yml passes
    it through): the author's merge counts as the approval."""
    if os.environ.get("REVIEW_SELF_MERGE", "").strip().lower() == "true":
        return True
    return bool((schema.get("review") or {}).get("self_merge"))


def needs_review_verdict(schema, author, approved, owners):
    """What the gate publishes for a needs-review proposal: (conclusion, title, summary).
    Approved by someone else: passes. Nobody yet: passes only under self_merge."""
    if approved:
        return ("success", f"Approved by {', '.join(approved)}",
                "A person who is not the author read the diff and approved it; this proposal may land.")
    if self_merge_allowed(schema):
        return ("success", "Needs review: a person reads the diff, then merges",
                "Self-merge is on for this repository (review.self_merge in docs/schema.json, or the "
                "REVIEW_SELF_MERGE variable), so the author's own merge is the approval. Nothing merges on its "
                "own: read the diff, then merge.")
    ask = ", ".join(owners) if owners else "a teammate who is not the author"
    return ("action_required", f"Waiting for approval from {ask}",
            f"This proposal needs a person to read the diff and approve it (the author, {author or 'unknown'}, "
            "cannot approve their own). Nothing is wrong with the files.")


def publish(repo, sha, conclusion, title, summary, url=""):
    """One completed `review-gate` check run on the commit; the ruleset requires it."""
    args = ["api", "-X", "POST", f"repos/{repo}/check-runs", "-f", f"name={CHECK}", "-f", f"head_sha={sha}",
            "-f", "status=completed", "-f", f"conclusion={conclusion}",
            "-f", f"output[title]={title}", "-f", f"output[summary]={summary}"]
    if url:
        args += ["-f", f"details_url={url}"]
    gh(*args)
    print(f"{CHECK}: {conclusion}. {title}")


def tidy(pr, head_branch, head_sha):
    """Apply the safe fixes from main's lint to the proposal's files; push them as one Tidy commit.
    Returns True when a commit was pushed (the new commit gets its own check and gate run)."""
    with tempfile.TemporaryDirectory(prefix="gate-tidy-") as tmp:
        wt = Path(tmp) / "proposal"
        git("worktree", "add", "--detach", str(wt), head_sha)
        try:
            subprocess.run([sys.executable, str(ROOT / "scripts" / "lint.py"), "--fix", "--quiet", "--root", str(wt)],
                           capture_output=True, text=True, cwd=str(ROOT))
            if not git("status", "--porcelain", cwd=wt).strip():
                return False
            git("-c", f"user.name={BOT_NAME}", "-c", f"user.email={BOT_EMAIL}", "add", "-A", cwd=wt)
            git("-c", f"user.name={BOT_NAME}", "-c", f"user.email={BOT_EMAIL}", "commit", "-q", "-m",
                "Tidy: apply the safe fixes from scripts/lint.py", cwd=wt)
            git("push", "origin", f"HEAD:refs/heads/{head_branch}", cwd=wt)
            print(f"pushed a Tidy commit to {head_branch}; the check and the gate run again on it")
            gh("workflow", "run", "check.yml", "--ref", head_branch, check=False)
            return True
        finally:
            git("worktree", "remove", "--force", str(wt), check=False)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Classify, tidy, label and gate a proposal from main.")
    ap.add_argument("--pr", required=True, type=int)
    ap.add_argument("--head-sha", default="", help="the commit the triggering check ran on")
    ap.add_argument("--doctor", default="none", choices=["success", "failure", "none"],
                    help="how the check's doctor job concluded on that commit")
    ap.add_argument("--no-tidy", action="store_true", help="do not push safe fixes to the proposal")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    view = json.loads(gh("pr", "view", str(args.pr), "--json",
                         "number,state,url,isCrossRepository,headRefName,headRefOid,baseRefName"))
    if view.get("state") != "OPEN":
        print(f"proposal #{args.pr} is {view.get('state', 'unknown').lower()}; nothing to do")
        return 0
    head_sha, head_branch = view["headRefOid"], view["headRefName"]
    base = view.get("baseRefName") or "main"
    fork = bool(view.get("isCrossRepository"))
    if args.head_sha and args.head_sha != head_sha:
        print(f"proposal #{args.pr} moved on since this check ran ({args.head_sha[:7]} -> {head_sha[:7]}); "
              "the run on the newer commit decides")
        return 0
    repo = os.environ.get("GITHUB_REPOSITORY") or json.loads(gh("repo", "view", "--json", "nameWithOwner"))["nameWithOwner"]

    if not fork:
        git("fetch", "-q", "origin", base, head_branch)
    else:
        git("fetch", "-q", "origin", base, f"pull/{args.pr}/head")  # a fork's commits, without its remote
    ctx = lint.Ctx()  # main's schema and checks, whatever the proposal did to its own copies
    kind, paths = lint.classify(ctx, f"origin/{base}", head_sha)
    if fork:
        kind = "needs-review"
    print(f"proposal #{args.pr}: {kind} ({len(paths)} files{', from a fork' if fork else ''})")
    for p in paths:
        print(f"  {p}")

    if args.dry_run:
        if kind == "bookkeeping":
            print("dry run: would merge it once the health check is green on this commit.")
        elif self_merge_allowed(ctx.schema):
            print("dry run: would pass the review-gate check (review.self_merge is on); a person reads the diff and merges.")
        else:
            print("dry run: would wait for an approval from "
                  f"{', '.join(codeowners_for(paths)) or 'a teammate who is not the author'}.")
        return 0

    if not fork and not args.no_tidy and tidy(args.pr, head_branch, head_sha):
        return 1  # the Tidy commit's own run decides

    other = [v for k, v in LABELS.items() if k != kind][0]
    gh("pr", "edit", str(args.pr), "--add-label", LABELS[kind], "--remove-label", other, check=False)

    if kind == "bookkeeping":
        if args.doctor != "success":
            publish(repo, head_sha, "failure", "Waiting for a green health check",
                    "This proposal only touches files the agents maintain (bookkeeping), so it merges itself, "
                    "but only once the health check passes on this exact commit. Fix what the check names, or "
                    "run `python3 scripts/doctor.py --fix`.", view["url"])
            return 1
        publish(repo, head_sha, "success", "Bookkeeping: merging",
                "Only agent-maintained files changed and the health check passed on this commit, so the gate on "
                "main merges this proposal itself (docs/workflow.md).", view["url"])
        run = subprocess.run([find_gh() or "gh", "pr", "merge", str(args.pr), "--squash", "--delete-branch",
                              "--match-head-commit", head_sha], capture_output=True, text=True, cwd=str(ROOT))
        if run.returncode != 0:
            print(f"merge refused: {run.stderr.strip()}")
            print("The proposal stays open; a person can merge it, or the next gate run retries.")
            return 1
        print("merged.")
        return 0

    author, approved = approvals(args.pr)
    conclusion, title, summary = needs_review_verdict(ctx.schema, author, approved, codeowners_for(paths))
    publish(repo, head_sha, conclusion, title, summary, view["url"])
    return 0 if conclusion == "success" else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CommandError as err:
        sys.exit(str(err))
