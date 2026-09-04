---
name: doctor
description: Say what is wrong with this checkout in plain words and fix what is safe. Use when asked for the "doctor", "something is red", "the check failed", "is everything set up", or when sync or propose report a problem.
license: MIT
metadata:
  kind: workflow
  area: core
  needs: []
  writes: repo
  runs: person
---

# Doctor

The repair word beside the lifecycle. `scripts/doctor.py` finds the
problems; this skill explains them and fixes the ones that need judgment.

## Procedure

1. Run `python3 scripts/doctor.py --fix` (add `--github` when the GitHub
   CLI is logged in, to check the repository settings too).
2. **For each remaining finding**, say what it means for the person, then
   either fix it (a frontmatter value, a broken link, a misplaced file
   moved with `git mv`, a naming slip) or name the one action only they
   can take. A stale review date is theirs: ask the owner whether the
   content still holds before touching the date.
3. **"Your machine" lines**: relay the action as written. When it is a
   terminal command (`gh auth login --web`), tell the person to run it in
   their own terminal or the desktop app's terminal, and what they will
   see: a code, then the browser.
4. **When clean**, say so in one line. If files changed, `/propose` sends
   the fixes.

## Rules

- Never read `.env` or ask for a key value; say where the key lives
  (`docs/secrets.md`).
- Unfilled templates are `/setup`'s job; say so and stop.
- The check on GitHub runs the same lint, so green here means green there.
