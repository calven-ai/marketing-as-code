# The review workflow: how work actually ships

The one ritual that keeps a human in charge of everything user-visible.
Written for GitHub Desktop users, no terminal required. (New to GitHub
entirely? Start with [new-to-github.md](new-to-github.md).)

## The shape of every change

1. **A branch, not main.** Your agent proposes work on a branch (ask it to:
   "make this a branch and open a PR"). Main is what the team has approved.
2. **A pull request a human can read.** The PR description (the template
   fills itself in) says what changed and why, in plain language, linking
   the project brief or decision behind it.
3. **A human reads the diff.** Not just the summary but the actual changed
   lines. The PR template's checklist is the reviewer's list: on-strategy,
   on-voice, numbers traceable, no credentials, decisions logged.
4. **The human merges.** Merging *is* the approval. Agents never merge,
   publish, or send.

## What must always take this path

- Published content (`status: published` is set in a PR, never directly)
- Anything sent to the outside world: emails, social posts, website changes
- Strategy, brand, and ontology changes: these cascade everywhere
- Automated pipelines: the transcript cron (wave 2) opens PRs, never merges

## What may skip it

Low-stakes internal bookkeeping an agent does in place: project `status.md`
updates, decision-log appends dictated in conversation, data snapshots,
moving a processed transcript. When in doubt, it's a PR.

## Review rhythm

Treat PR review like inbox: daily, briefly. A stalled PR is usually a
missing decision: name it, decide it, log it in `memory/decision-log.md`,
and merge or close. Closed-without-merge is a fine outcome; the history
keeps the thinking.
