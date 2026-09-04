---
name: propose
description: Turn what changed into a proposal (a pull request) and hand back the link. Use when asked to "propose", "send this for review", "ship it", "open a proposal", "save this to GitHub", or when a piece of work is done and should land.
metadata:
  kind: workflow
  needs: nothing; the GitHub CLI to open the proposal itself
---

# Propose

The ship-it word. Saying it is the consent: the proposal opens in the
same turn, with no second question. The script does the deterministic part
(check, fix, commit, push, open); this skill does the judgment (scope, the
title, the description, the fixes the script cannot make).

## Procedure

1. **Look first**: `python3 scripts/propose.py --check --json`. It lists
   the files, the findings and the kind (bookkeeping or needs review).
2. **Scope**: if the files include something the person did not work on
   in this session, say so and ask whether it belongs in this proposal.
   `--paths` leaves things out. Otherwise proceed without asking.
3. **Fix what the script cannot**: for each remaining finding, fix it in
   the file (a frontmatter value, a broken link, a misplaced file moved
   with `git mv`), then run `--check` again. A finding about something
   shaped like a key: stop, say so, and point at `docs/secrets.md`.
4. **Write the title and the description.** Title in sentence case, under
   80 characters, "Subject: what changed"; it becomes the commit title on
   the approved copy. Description: two short paragraphs, what changed and
   why, in plain words, naming the brief or decision behind it when there
   is one. Save the description to a temporary file.
5. **Run it**: `python3 scripts/propose.py --title "..." --body-file <file>`.
6. **Relay**: the link, the outcome sentence (merges itself, you are the
   reviewer, or waiting for someone), and that the check takes about a
   minute. If the script printed a "Create pull request" link instead, say
   to open it and click the button.
7. **If it refused**: relay the reason in the script's words and the one
   action it names. Nothing was sent.

## Rules

- Never run `git push --force`, `gh pr merge`, `gh pr review`, or push to
  `main`. The script does not either.
- Content goes through `/review` before it is proposed as `in-review` or
  `published`; suggest it when the proposal holds a draft. A draft that
  flips to `published` in this proposal must carry `published` (the date)
  and `published_url`; confirm both before running.
- Never include credentials or a customer's personal data.
