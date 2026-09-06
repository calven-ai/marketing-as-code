# The review workflow: how work ships

One ritual keeps a human in charge of everything user-visible. Written for
GitHub Desktop users: one command, once, then none. New to GitHub? Start
with [new-to-github.md](new-to-github.md).

## The shape of every change

Five words: **Sync. Work. Propose. Review. Merge.** Doctor is the repair
word beside them. Say the word to your coding agent; it runs the
machinery. GitHub Desktop users click through the same loop
([new-to-github.md](new-to-github.md)).

<p align="center">
  <img src="assets/lifecycle.svg" alt="The lifecycle as pixel-art panels: Sync (get the latest), Work (ask the agent), Propose (open the proposal), Review (read the diff), Merge (click merge), and a red Doctor panel below: the repair word when something is red" width="720">
</p>

1. **Sync.** Say `/sync`. The agent brings the latest approved copy into
   your checkout and tells you what is waiting on you.
2. **Work.** Ask for what you need. The agent works on a branch. Main is
   what the team has approved.
3. **Propose.** Say `/propose`. The agent checks the files, fixes what is
   safe, writes the description from the template, and hands you the
   link. It also says which kind of proposal it is (below).
4. **Review.** A human reads the diff. The actual changed lines, not just
   the summary. The PR template's checklist is the reviewer's list:
   on-strategy, on-voice, numbers traceable, no credentials, decisions
   logged.
5. **Merge.** Merging is the approval. Agents never merge, publish or
   send. The one exception is bookkeeping, below.

Something red, or a message you do not understand? Say `/doctor`.
[troubleshooting.md](troubleshooting.md) lists every message.

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
  the diff and approves; a bot's approval never counts. Anything touching
  the machinery (`.github/`, `scripts/`, `docs/schema.json`, the agent
  settings, the skills, the integrations) is needs-review no matter what
  else is in the proposal, and so is any proposal from a fork or from an
  agent that ran with nobody watching (`transcripts-process.yml`,
  `role-run.yml`), even when every file it touched is bookkeeping: the
  agent read text nobody vetted, so a person reads the diff before it
  becomes context every later agent trusts. A proposal that touches
  `scripts/`, `.github/` or `docs/schema.json` gets no Tidy commit from
  the gate: the tidy step runs main's lint against the proposal's files,
  and a proposal's own machinery takes no part in that.

When in doubt the gate decides, and it errs toward review. On a public
repository, and on a private one under GitHub Team or Pro, the checks are
enforced; on a private repository under Free they advise
([github-settings.md](github-settings.md)).

One maintainer? GitHub never lets an author approve their own proposal,
so set `review.self_merge` to `true` in `docs/schema.json` (`/setup` asks
how many people merge and sets it). The gate then passes a needs-review
proposal and your merge is the approval. Nothing merges on its own, and
you still read the diff. The template ships `false`; set it back to
`false` the day a second person joins. A repository that must keep the
file as shipped (the template itself) sets the Actions variable
`REVIEW_SELF_MERGE` to `true` instead, which has the same effect.

## Review rhythm

Treat PR review like inbox: daily, briefly. A stalled PR is usually a
missing decision. Name it, decide it, log it in `memory/decision-log.md`,
and merge or close. Closed without merge is a fine outcome; the history
keeps the thinking.
