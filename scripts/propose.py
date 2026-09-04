#!/usr/bin/env python3
"""Propose: turn what changed in this checkout into a proposal (a pull request)
and hand back the link. Checks the files first and fixes what is safe,
refuses on real problems with nothing committed, commits, pushes the
branch, opens or updates the proposal from the template, and says what
happens next: bookkeeping merges itself, needs-review waits for a person.
Never pushes to the approved copy, never force-pushes, never merges.

Run from the repo root, or say /propose:
    python3 scripts/propose.py --title "Positioning: sharper claim" [--body-file what-and-why.md]
    python3 scripts/propose.py --check      # the files, the findings and the outcome; changes nothing
    python3 scripts/propose.py --dry-run    # everything --check says, plus what would happen
    python3 scripts/propose.py --title T --paths content/2026-09-post  # only these paths

Options: --branch NAME (default proposal/<date>-<slug of title>), --wait (stay
until the check finishes), --json (the result as JSON, for skills), --root.
Without the GitHub CLI it still commits and pushes and prints the link to
open the proposal in the browser. Exit 1 when the files have problems, the
push failed, or the folder is not connected to GitHub.
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint  # noqa: E402
from _common import CommandError, find_gh, gh, gh_ready  # noqa: E402
from _lifecycle import NOT_CONNECTED, OFFLINE, Checkout, outcome, proposal_for  # noqa: E402
from review_gate import codeowners_for, self_merge_allowed  # noqa: E402

TEMPLATE = ".github/PULL_REQUEST_TEMPLATE.md"
CHECKLIST = ("## Review checklist\n\n"
             "- [ ] I read the actual diff (not just the summary above)\n"
             "- [ ] Anything user-visible (published content, sent email) matches `strategy/` and `brand/voice.md`\n"
             "- [ ] Numbers trace back to `data/` snapshots and use `data/ontology/` definitions\n"
             "- [ ] No credentials, no customer PII\n"
             "- [ ] Decisions this work resolved are in `memory/decision-log.md`\n")
NOTHING = "Nothing has changed since the approved copy."
NO_IDENTITY = "Git does not know your name yet. Run /doctor to set it."
LANDED = "That proposal already landed. Say /sync, then propose again."
AUTH = "GitHub did not accept your login. Run /doctor."
SECRET = ("GitHub refused this because it contains something shaped like a key. Remove it, rotate it "
          "(docs/secrets.md), then propose again.")
SAVED_LOCALLY = ("Your change is saved on this computer. In GitHub Desktop click Push origin, then Create pull "
                 "request. To let me do this next time, install the GitHub CLI (docs/troubleshooting.md).")


def branch_name(title, co):
    base = f"proposal/{date.today().isoformat()}-{lint.slug(title) or 'change'}"
    name, n = base, 1
    while co.has_ref(name) or co.has_ref(f"origin/{name}"):
        n += 1
        name = f"{base}-{n}"
    return name


def build_body(co, prose):
    """The proposal description: the template's sections with PROSE under What and Why, the checklist always."""
    text = (co.root / TEMPLATE).read_text(encoding="utf-8") if (co.root / TEMPLATE).is_file() else ""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    checklist = re.search(r"^## Review checklist.*", text, flags=re.S | re.M)
    checklist = checklist.group(0).strip() + "\n" if checklist else CHECKLIST
    prose = (prose or "").strip()
    if re.search(r"^## ", prose, flags=re.M):
        body = prose  # the skill wrote its own sections
    else:
        parts = re.split(r"\n\s*\n", prose, maxsplit=1) if prose else ["", ""]
        what = parts[0].strip() or "See the changed files."
        why = parts[1].strip() if len(parts) > 1 and parts[1].strip() else "Not stated."
        body = f"## What this changes\n\n{what}\n\n## Why\n\n{why}"
    return body.rstrip() + "\n\n" + checklist


def commit_message(title, body):
    prose = re.split(r"^## Review checklist", body, flags=re.M)[0]
    prose = re.sub(r"\n{3,}", "\n\n", re.sub(r"^## .*\n", "", prose, flags=re.M)).strip()
    return f"{title}\n\n{prose}\n" if prose else f"{title}\n"


def push_failure(stderr):
    """The push's stderr as one plain sentence, or None when it was a plain non-fast-forward."""
    low = stderr.lower()
    if "gh013" in low or "push protection" in low or "secret" in low:
        return SECRET
    if "pre-push:" in low:
        return next((line.strip() for line in stderr.splitlines() if "pre-push:" in line), stderr.strip())
    if any(k in low for k in ("authentication failed", "could not read username", "permission denied",
                              "403", "invalid username or token", "terminal prompts disabled")):
        return AUTH
    if any(k in low for k in ("non-fast-forward", "fetch first", "rejected")):
        return None
    if any(k in low for k in ("could not resolve host", "could not read from remote", "network")):
        return OFFLINE
    return stderr.strip() or "The push failed."


def compare_url(repo, base, branch, title, body):
    return (f"https://github.com/{repo}/compare/{base}...{branch}?quick_pull=1"
            f"&title={quote(title)}&body={quote(body)}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Turn what changed into a proposal and hand back the link.")
    ap.add_argument("--title", help="the proposal's title (becomes the commit title on the approved copy)")
    ap.add_argument("--body-file", help="a file with what this changes and why, in plain language")
    ap.add_argument("--branch", help="the branch name to create when starting from the approved copy")
    ap.add_argument("--paths", nargs="*", default=[], help="only propose these paths")
    ap.add_argument("--check", action="store_true", help="report files, findings and outcome; change nothing")
    ap.add_argument("--dry-run", action="store_true", help="like --check, plus what would happen next")
    ap.add_argument("--wait", action="store_true", help="stay until the check on the proposal finishes")
    ap.add_argument("--json", action="store_true", help="the result as JSON, for skills")
    ap.add_argument("--root", help="the checkout to propose from (default: the one this script lives in)")
    args = ap.parse_args(argv)
    look_only = args.check or args.dry_run
    if not look_only and not args.title:
        ap.error("--title is required (or use --check / --dry-run)")

    co = Checkout(args.root)
    result = {"ok": False, "lines": [], "files": [], "findings": [], "kind": None, "branch": None,
              "url": None, "outcome": None}

    def say(text):
        result["lines"].append(text)
        if not args.json:
            print(text)

    def finish(code):
        result["ok"] = code == 0
        if args.json:
            print(json.dumps(result, indent=2))
        return code

    # 1. Preflight.
    if not co.connected:
        say(NOT_CONNECTED)
        return finish(1)
    name, email = co.identity()
    if not (name and email):
        say(NO_IDENTITY)
        return finish(1)
    base, branch = co.base, co.branch()
    repo = co.repo
    with_gh = gh_ready(co.root)
    self_merge = self_merge_allowed(co.schema())
    online = co.run("fetch", "-q", "origin").returncode == 0

    # 2. Anything to propose?
    dirty = co.dirty(args.paths)
    unpushed = 0
    if branch and branch != base:
        unpushed = co.count(f"origin/{branch}..HEAD") if co.has_ref(f"origin/{branch}") else co.count(f"origin/{base}..HEAD")
    elif branch == base:
        unpushed = co.count(f"origin/{base}..HEAD")
    existing = proposal_for(co, branch) if (with_gh and branch and branch != base) else None
    if not dirty and not unpushed and not co.merging():
        if existing:
            say(f"Your proposal is up to date: {existing['url']}")
            result["url"] = existing["url"]
            return finish(0)
        say(NOTHING)
        return finish(0)

    # 4. A branch whose proposal already landed cannot carry a new one.
    if with_gh and branch and branch != base and not existing:
        if proposal_for(co, branch, "merged") or proposal_for(co, branch, "closed"):
            say(LANDED)
            return finish(1)

    # 5. Stage and check, fixing what is safe.
    if not look_only:
        co.git("add", "-A", "--", *args.paths) if args.paths else co.git("add", "-A")
    ctx = co.ctx()
    findings = lint.run_checks(ctx)
    if not look_only:
        fixed = lint.apply_fixes(ctx, findings)
        if fixed:
            co.git("add", "-A", "--", *args.paths) if args.paths else co.git("add", "-A")
            findings = lint.run_checks(ctx)
            say(f"Fixed {len(fixed)} small things on the way.")
    errors = [f for f in findings if f.level == lint.ERROR]
    result["findings"] = [f.as_dict() for f in findings if f.level != lint.INFO]
    changed = sorted(set(co.dirty(args.paths)) | set(
        p for p in co.run("diff", "--name-only", f"origin/{base}...HEAD").stdout.splitlines() if p))
    result["files"] = changed
    kind = lint.classify_paths(co.schema(), changed)
    result["kind"] = kind
    if look_only:
        say(f"{len(changed)} files would be proposed as {kind}:")
        for p in changed:
            say(f"  {p}")
        if errors:
            say(f"{len(errors)} problems to fix before this can be proposed"
                + (", some of them automatically" if any(f.fixable for f in errors) else "") + ":")
            say(lint.format_text(errors))
        else:
            say("No problems in the files.")
        target = args.branch or (branch if branch and branch != base else branch_name(args.title or "change", co))
        result["branch"] = target
        if args.dry_run:
            if with_gh:
                say(f"Would commit on {target}, push it, and "
                    + ("update the open proposal." if existing else "open a proposal."))
            else:
                say(f"Would commit on {target}, push it, and print the link to open the proposal in the browser.")
            say(outcome(kind, self_merge, codeowners_for(changed), "<the proposal's link>"))
        return finish(1 if errors else 0)
    if errors:
        say(f"{len(errors)} problems to fix before this can be proposed:")
        say(lint.format_text(errors))
        say("Nothing was sent. Fix these (ask me), then propose again.")
        return finish(1)

    # 3. From the approved copy: move the edits onto a new branch.
    if branch == base or not branch:
        target = args.branch or branch_name(args.title, co)
        co.run("merge", "--ff-only", f"origin/{base}")  # best effort; the edits stay staged
        co.git("switch", "-c", target)
        branch = target
    result["branch"] = branch

    # 6. Commit.
    body = build_body(co, Path(args.body_file).read_text(encoding="utf-8") if args.body_file else "")
    if co.dirty(args.paths) or co.merging():
        proc = co.run("commit", "-q", "-m", commit_message(args.title, body))
        if proc.returncode != 0:
            say(f"Could not save the change: {proc.stderr.strip()}")
            return finish(1)

    # 7. Reconcile with the pushed copy, then push.
    if not online:
        say(OFFLINE)
        say("Your change is saved on this computer; propose again when you are back online.")
        return finish(1)
    if co.has_ref(f"origin/{branch}") and co.count(f"HEAD..origin/{branch}"):
        if co.run("merge", "--no-edit", f"origin/{branch}").returncode != 0:
            co.run("merge", "--abort")
            say("Your proposal and its copy on GitHub have drifted apart. Say /sync and ask me to sort it out.")
            return finish(1)
    proc = co.run("push", "-u", "origin", branch)
    if proc.returncode != 0:
        reason = push_failure(proc.stderr)
        if reason is None:  # someone pushed to this branch meanwhile: bring it in once and retry
            co.run("fetch", "-q", "origin")
            if co.run("merge", "--no-edit", f"origin/{branch}").returncode == 0:
                proc = co.run("push", "-u", "origin", branch)
                reason = push_failure(proc.stderr) if proc.returncode != 0 else ""
            else:
                co.run("merge", "--abort")
                reason = "Your proposal and its copy on GitHub have drifted apart. Say /sync and ask me to sort it out."
        if proc.returncode != 0:
            say(reason if reason != AUTH or with_gh else SAVED_LOCALLY)
            return finish(1)

    # 8. The proposal itself.
    if with_gh:
        existing = proposal_for(co, branch)
        if existing:
            url = existing["url"]
            say(f"Updated your proposal: {url}")
        else:
            body_path = co.root / ".git" / "PROPOSAL_BODY.md"
            body_path.write_text(body, encoding="utf-8")
            try:
                url = gh("pr", "create", "-R", repo, "--base", base, "--head", branch, "--title", args.title,
                         "--body-file", str(body_path), cwd=co.root).strip().splitlines()[-1]
            except CommandError as err:
                say(f"Pushed, but could not open the proposal: {err.stderr.strip() or err}")
                say(f"Open it here instead: {compare_url(repo, base, branch, args.title, body)}")
                return finish(1)
            finally:
                body_path.unlink(missing_ok=True)
            say(f"Opened your proposal: {url}")
    else:
        url = compare_url(repo, base, branch, args.title, body)
        say(f"Open this link and click Create pull request: {url}")
    result["url"] = url

    # 9. What happens next.
    verdict = outcome(kind, self_merge, codeowners_for(changed), url)
    result["outcome"] = verdict
    say(verdict)
    say("The check takes about a minute; the proposal page shows it.")
    if args.wait and with_gh:
        gh("pr", "checks", "-R", repo, branch, "--watch", cwd=co.root, check=False)
        say("The check finished. Say /sync to see where it stands.")
    return finish(0)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CommandError as err:
        sys.exit(f"Something went wrong underneath: {err}. Run /doctor.")
