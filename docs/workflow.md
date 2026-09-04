# The review workflow: how work ships

One ritual keeps a human in charge of everything user-visible. Written for
GitHub Desktop users, no terminal required. New to GitHub? Start with
[new-to-github.md](new-to-github.md).

## The shape of every change

1. **A branch, not main.** Your agent proposes work on a branch. Main is
   what the team has approved.
2. **A pull request a human can read.** The description (the template fills
   itself in) says what changed and why, linking the brief or decision
   behind it.
3. **A human reads the diff.** The actual changed lines, not just the
   summary. The PR template's checklist is the reviewer's list: on-strategy,
   on-voice, numbers traceable, no credentials, decisions logged.
4. **The human merges.** Merging is the approval. Agents never merge,
   publish or send. The one exception is bookkeeping, below.

## What must always take this path

- Published content (`status: published` is set in a PR, never directly)
- Anything sent to the outside world: emails, social posts, website changes
- Strategy, brand and ontology changes, because they cascade everywhere
- Anything running in GitHub Actions, script or agent. It opens proposals;
  only the gate merges, and only bookkeeping ones
  ([operating-model.md](operating-model.md))

## Two kinds of proposals, one path

Every change is a branch and a pull request, which this repo calls a
proposal. The check (`.github/workflows/check.yml`) tests it. The gate
(`.github/workflows/gate.yml`, run from the approved copy so a proposal
cannot change the rules it is judged by) sorts it into one of two kinds:

- **Bookkeeping.** It touches only files the agents maintain: project
  `status.md` entries, decision-log appends, data snapshots, transcripts
  moving through the inbox, recurring reports. The list is `bookkeeping`
  in `docs/schema.json`. Once the check is green, the gate merges it.
  Nobody has to merge a snapshot.
- **Needs review.** Everything else: content, strategy, brand, ontology,
  skills, scripts, workflows, docs. A person who is not the author reads
  the diff and approves. Anything touching the machinery (`.github/`,
  `scripts/`, `docs/schema.json`, the agent settings, the skills, the
  integrations) is needs-review no matter what else is in the proposal.

When in doubt the gate decides, and it errs toward review. On GitHub Team
or Pro the checks are enforced; on Free they advise
([github-settings.md](github-settings.md)).

One maintainer? GitHub never lets an author approve their own proposal,
so set `review.self_merge` to `true` in `docs/schema.json`. The gate then
passes a needs-review proposal and your merge is the approval. Nothing
merges on its own, and you still read the diff. Set it back to `false`
the day a second person joins.

## Review rhythm

Treat PR review like inbox: daily, briefly. A stalled PR is usually a
missing decision. Name it, decide it, log it in `memory/decision-log.md`,
and merge or close. Closed without merge is a fine outcome; the history
keeps the thinking.
