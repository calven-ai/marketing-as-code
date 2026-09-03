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
- Automated pipelines: anything running in GitHub Actions, script or agent,
  opens proposals; only the check merges, and only bookkeeping ones
  ([operating-model.md](operating-model.md))

## Two kinds of proposals, one path

Every change travels the same way: a branch and a pull request, which this
repo calls a proposal. The check (`.github/workflows/check.yml`) then sorts
it into one of two kinds:

- **Bookkeeping.** It touches only files the agents maintain: project
  `status.md` entries, decision-log appends, data snapshots, transcripts
  moving through the inbox, recurring reports (the list is `bookkeeping` in
  `docs/schema.json`). Once the checks are green it approves itself and
  lands. Nobody has to merge a snapshot.
- **Needs review.** Everything else: content, strategy, brand, ontology,
  skills, scripts, docs. A person who is not the author reads the diff and
  approves; the `review-gate` check says whose approval it is waiting for.

When in doubt the check decides, not the author, and it always errs toward
review. On GitHub Team or Pro the two checks are enforced; on Free they
advise ([github-settings.md](github-settings.md)).

## Review rhythm

Treat PR review like inbox: daily, briefly. A stalled PR is usually a
missing decision: name it, decide it, log it in `memory/decision-log.md`,
and merge or close. Closed-without-merge is a fine outcome; the history
keeps the thinking.
