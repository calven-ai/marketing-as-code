---
name: sync
description: Bring in the latest approved copy and say what is waiting on you. Use at the start of a session, when asked to "sync", "get the latest", "where am I", "what's waiting on me", or to look again while a proposal is checking.
license: MIT
metadata:
  kind: workflow
  area: core
  needs: []
  writes: repo
  runs: person
---

# Sync

The first word of the lifecycle: Sync. Work. Propose. Review. Merge. It
brings the approved copy into this checkout, tidies up, and ends with
where the person stands and what is waiting on them. It never pushes,
never merges, never touches the approved copy on GitHub.

## Procedure

1. Run `python3 scripts/sync.py` (`--status` when the person only wants
   to look). Every line it prints is written for the person; relay them
   as they are, shortest first.
2. **A clash** ("changed the same lines in X"): run
   `python3 scripts/sync.py --keep-conflicts`, open each named file, and
   resolve the conflict markers so both intents survive. If the two
   versions genuinely disagree, show the person both and ask which holds.
   Then say the files are reconciled and that `/propose` saves it.
3. **Not connected, or GitHub unreachable**: relay the one action the
   script names; `docs/troubleshooting.md` has the longer version.
4. **Unsaved edits** the person did not mention: say what they are and ask
   whether to propose or discard them before syncing again.

## Rules

- No git vocabulary in what the person reads: proposal, the approved copy,
  the check, the gate. Branch, commit and pull request are allowed.
- Never push, force-push, merge, or check out `main` with unsaved edits.
- When the person then wants to work, help them; when the work is done,
  `/propose`.
