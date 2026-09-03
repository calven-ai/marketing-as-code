#!/usr/bin/env python3
"""The review gate CI runs on every proposal: classifies it as bookkeeping
(agent-maintained files only, per docs/schema.json) or needs-review, labels
it, and either merges a green bookkeeping proposal itself or, for
needs-review, passes only once someone other than the author has approved.
Needs gh with a token that can write pull requests. --dry-run prints
what it would do.

Usage, from the repo root (check.yml calls it):
    python3 scripts/review_gate.py --pr 12 --base main
    python3 scripts/review_gate.py --pr 12 --base main --dry-run

Exit 0 means "this proposal may land" (or has landed). Exit 1 means it is
waiting for a person, with the names to ask printed in plain words. On a
GitHub plan where the check is required, that blocks the merge button; on
GitHub Free it is advisory (docs/github-settings.md).
"""

import argparse
import fnmatch
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint  # noqa: E402

ROOT = lint.ROOT
LABELS = {"bookkeeping": "bookkeeping", "needs-review": "needs-review"}


def gh(*args, check=True):
    run = subprocess.run(["gh", *args], capture_output=True, text=True, cwd=str(ROOT))
    if check and run.returncode != 0:
        sys.exit(f"gh {' '.join(args[:2])} failed: {run.stderr.strip()}")
    return run.stdout


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


def main(argv=None):
    ap = argparse.ArgumentParser(description="Classify, label and gate a proposal.")
    ap.add_argument("--pr", required=True, type=int)
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    ctx = lint.Ctx()
    kind, paths = lint.classify(ctx, args.base)
    print(f"proposal #{args.pr}: {kind} ({len(paths)} files)")
    for p in paths:
        print(f"  {p}")

    if args.dry_run:
        print("dry run: would " + ("merge it once the checks are green." if kind == "bookkeeping"
                                    else f"wait for an approval from {', '.join(codeowners_for(paths)) or 'a teammate'}."))
        return 0
    other = [v for k, v in LABELS.items() if k != kind][0]
    gh("pr", "edit", str(args.pr), "--add-label", LABELS[kind], "--remove-label", other, check=False)

    if kind == "bookkeeping":
        print("bookkeeping only: the checks are green, so this proposal approves itself.")
        # --auto waits for every required check (including this one) on plans
        # that enforce rulesets; where auto-merge is unavailable, merge now.
        if subprocess.run(["gh", "pr", "merge", str(args.pr), "--auto", "--squash", "--delete-branch"],
                          capture_output=True, text=True, cwd=str(ROOT)).returncode != 0:
            gh("pr", "merge", str(args.pr), "--squash", "--delete-branch")
        return 0

    author, approved = approvals(args.pr)
    if approved:
        print(f"approved by {', '.join(approved)}; this proposal may land.")
        return 0
    owners = codeowners_for(paths)
    ask = ", ".join(owners) if owners else "a teammate who is not the author"
    print(f"waiting for approval from {ask} (the author, {author or 'unknown'}, cannot approve their own proposal).")
    print("Nothing is wrong with the files; a person reads the diff, then approves or requests changes.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
