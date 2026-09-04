#!/usr/bin/env python3
"""Sync: bring the latest approved copy into this checkout, tidy up, and say
where you are and what is waiting on you. The first thing to say in a
session and the way to look again while a proposal is checking. Never
pushes, never merges a proposal, never touches the approved copy on GitHub.

Run from the repo root, or say /sync:
    python3 scripts/sync.py                  # sync, then the status paragraph
    python3 scripts/sync.py --status         # the status paragraph only
    python3 scripts/sync.py --dry-run        # say what a sync would do
    python3 scripts/sync.py --keep-conflicts # leave a conflicted merge for the agent to resolve

On the approved copy it brings in what landed. On a proposal's branch it
brings in the gate's tidy-up and the approved copy; a clash between the two
is reported by file name and undone unless --keep-conflicts. Then it turns on
the pre-push hook, refreshes the skill links, removes branches whose proposal
landed, and prints your open proposals with their state. Exit 1 only when
the folder is not connected to GitHub or GitHub cannot be reached.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import doctor  # noqa: E402
import sync_skills  # noqa: E402
from _common import CommandError, gh_ready  # noqa: E402
from _lifecycle import NO_GH, NOT_CONNECTED, OFFLINE, Checkout, describe, proposal_for, proposals  # noqa: E402
from review_gate import self_merge_allowed  # noqa: E402


def bring_in(co, say, dry_run, keep_conflicts):
    """Steps 3 and 4: the approved copy forward, then the branch forward. Returns a list of notes."""
    base, branch = co.base, co.branch()
    if not branch:
        say("You are between branches. Ask me to get back to the approved copy.")
        return
    if branch == base:
        behind = co.count(f"HEAD..origin/{base}")
        ahead = co.count(f"origin/{base}..HEAD")
        if behind:
            if dry_run:
                say(f"Would bring in {behind} changes from the approved copy.")
            elif co.run("merge", "--ff-only", f"origin/{base}").returncode == 0:
                log = co.git("log", "--oneline", f"-{min(behind, 5)}", "HEAD").strip()
                say(f"Brought in {behind} changes from the approved copy:\n  " + log.replace("\n", "\n  "))
            else:
                say("The approved copy moved and your copy has changes of its own. Say /propose to send them as a proposal.")
        else:
            say("The approved copy is up to date.")
        if ahead:
            say(f"Your copy has {ahead} changes GitHub does not. Say /propose to send them as a proposal.")
        return

    # On a proposal's branch: keep the local approved copy fresh without switching to it.
    co.run("fetch", "-q", "origin", f"{base}:{base}")
    if co.has_ref(f"origin/{branch}") and co.count(f"HEAD..origin/{branch}"):
        if dry_run:
            say("Would bring in the check's tidy-up of your proposal.")
        elif co.run("merge", "--ff-only", f"origin/{branch}").returncode == 0:
            say("The check tidied your proposal; brought that in.")
        else:
            say("Your proposal and its copy on GitHub have drifted apart. Ask me to sort it out.")
    behind = co.count(f"HEAD..origin/{base}")
    if not behind:
        say("Your proposal already has everything from the approved copy.")
        return
    dirty = co.dirty()
    if dirty:
        say(f"You have unsaved edits to {', '.join(dirty[:5])}; propose or discard them, then sync again.")
        return
    if dry_run:
        say(f"Would bring the approved copy ({behind} changes) into your proposal.")
        return
    if co.run("merge", "--no-edit", f"origin/{base}").returncode == 0:
        say("Brought the approved copy into your proposal.")
        return
    clashes = co.conflicted()
    if not keep_conflicts:
        co.run("merge", "--abort")
    say(f"Your proposal and the approved copy changed the same lines in {', '.join(clashes) or 'some files'}. "
        + ("The clash is left in place for me to resolve." if keep_conflicts else "Ask me to resolve it."))


def housekeeping(co, say, dry_run):
    """Step 5: hook on, skill links fresh, landed proposals' branches gone."""
    if co.run("config", "core.hooksPath").stdout.strip() != "scripts/hooks" and (co.root / "scripts" / "hooks").is_dir():
        if not dry_run:
            co.git("config", "core.hooksPath", "scripts/hooks")
        say("Turned on the safety check that runs before anything leaves this computer.")
    if not dry_run and (co.root / ".agents" / "skills").is_dir() and co.root == Path(sync_skills.ROOT):
        sync_skills.main([])
    co.run("remote", "prune", "origin")
    if dry_run or not gh_ready(co.root):
        return
    current, base = co.branch(), co.base
    for line in co.git("branch", "--format=%(refname:short)").splitlines():
        name = line.strip()
        if not name or name in (current, base):
            continue
        landed = proposal_for(co, name, state="merged")
        if landed:
            co.run("branch", "-D", name)
            say(f"Proposal #{landed['number']} landed; removed its branch.")


def status(co, say):
    """Step 6: where you are, your open proposals, what awaits your review, the doctor's three lines."""
    base, branch = co.base, co.branch()
    self_merge = self_merge_allowed(co.schema())
    mine = proposals(co, "--author", "@me")
    if branch == base:
        say("You are on: the approved copy.")
    elif branch:
        pr = next((p for p in mine or [] if p.get("headRefName") == branch), None) or proposal_for(co, branch)
        say(f"You are on: your proposal \"{pr['title']}\" (#{pr['number']})." if pr
            else f"You are on: a change not yet proposed ({branch}). Say /propose when it is ready.")
    dirty = co.dirty()
    if dirty:
        say(f"Unsaved edits: {', '.join(dirty[:8])}" + (f" and {len(dirty) - 8} more" if len(dirty) > 8 else "") + ".")
    if mine is None:
        say(NO_GH)
    elif mine:
        say("Your open proposals:")
        for pr in mine:
            say(f"  #{pr['number']} {pr['title']}: {describe(pr, self_merge)}. {pr['url']}")
        awaiting = proposals(co, "--search", "review-requested:@me") or []
        awaiting = [p for p in awaiting if p["number"] not in {m["number"] for m in mine}]
        if awaiting:
            say("Waiting for your review:")
            for pr in awaiting:
                say(f"  #{pr['number']} {pr['title']}: {pr['url']}")
    else:
        say("No open proposals of yours.")
        awaiting = proposals(co, "--search", "review-requested:@me") or []
        for pr in awaiting:
            say(f"Waiting for your review: #{pr['number']} {pr['title']}: {pr['url']}")
    for line in doctor.brief(co.ctx()):
        say(line)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Bring in the approved copy, tidy up, say what is waiting.")
    ap.add_argument("--status", action="store_true", help="only say where you are and what is waiting")
    ap.add_argument("--dry-run", action="store_true", help="say what a sync would do, change nothing")
    ap.add_argument("--keep-conflicts", action="store_true", help="leave a clashing merge in place to resolve by hand")
    ap.add_argument("--json", action="store_true", help="the same lines as JSON, for skills")
    ap.add_argument("--root", help="the checkout to sync (default: the one this script lives in)")
    args = ap.parse_args(argv)

    co = Checkout(args.root)
    lines = []

    def say(text):
        lines.append(text)
        if not args.json:
            print(text)

    def finish(code):
        if args.json:
            print(json.dumps({"ok": code == 0, "lines": lines}, indent=2))
        return code

    if not co.connected:
        say(NOT_CONNECTED)
        return finish(1)
    if co.run("fetch", "-q", "origin").returncode != 0:
        say(OFFLINE)
        return finish(1)
    try:
        if not args.status:
            bring_in(co, say, args.dry_run, args.keep_conflicts)
            housekeeping(co, say, args.dry_run)
        status(co, say)
    except CommandError as err:
        say(f"Something went wrong underneath: {err}. Run /doctor.")
        return finish(1)
    return finish(0)


if __name__ == "__main__":
    sys.exit(main())
