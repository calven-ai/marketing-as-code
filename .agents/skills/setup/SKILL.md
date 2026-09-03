---
name: setup
description: Onboard a team into this repo. Use when asked to "set up the repo", "run the setup interview", or when the strategy/brand/ontology templates are clearly unfilled and the user wants to start working. Interviews the team, fills the templates from their answers, connects integrations, and writes the task-tool adapter.
metadata:
  kind: workflow
  needs: nothing
---

# Setup: the onboarding interview

You are turning a blank template into *this team's* second brain. Interview,
then fill. Never invent answers, and never overwrite something the team
already filled in without asking.

## Procedure

1. **Take stock.** Check which of these are still unfilled templates:
   `strategy/positioning.md`, `strategy/messaging.md`, `strategy/icp.md`,
   `strategy/personas.md`, `strategy/product-brief.md`, `brand/voice.md`,
   `brand/visual-identity.md` + `brand/tokens.json`, `data/ontology/*.md`,
   `integrations/tasks.md`. Tell the user what's missing and that you'll
   work through it in short rounds; they can stop anytime and resume later.

   Ask one question before the interview: does the team already keep
   positioning, messaging, ICP and personas somewhere structured, for
   example a marketing context layer such as Calven? If yes, connect it per
   `integrations/context-layer.md` (they generate the key and put it in
   `.env`; you never touch `.env`), confirm with `get_workspace_overview`,
   mark the mirrored strategy files `source: context-layer` with the
   two-line fallback body, and skip rounds 1 to 3 below. If no, continue;
   the Markdown path is the default.

2. **Interview in this order** (each round: a few questions, then you draft
   the file, then they correct it; don't ask twenty questions up front):
   1. *Positioning*: who is it for, what problem, what category, why you
      over the alternative. Draft `positioning.md` section by section (the
      headings are fixed; leave a section visibly empty rather than
      inventing it), iterate. Set `last_reviewed` to today once the team
      confirms the draft, and put a name in `owner`.
   2. *Messaging*: the core narrative and two to four pillars with proof,
      then the persona matrix and objections. Existing homepage copy or a
      pitch deck is admissible evidence: ask if there's something to paste.
      Same `last_reviewed` and `owner` rule.
   3. *ICP and personas*: `icp.md` first (fit, triggers, tiers,
      disqualifiers; the scorecard can wait), then one `personas.md` block
      per person in the deal. Offer `product-brief.md` here too, skippable
      if there is no product documentation to paste yet. Same
      `last_reviewed` and `owner` rule.
   4. *Voice*: three adjectives, do/don't examples (ask for a paragraph
      they love and one that made them cringe; derive rules from those),
      banned words.
   5. *Visual identity*: colors and fonts if known; fill `tokens.json` and
      `visual-identity.md` together. Skippable.
   6. *Ontology*: what a signup/MQL/SQL actually means here, funnel stages,
      the few events that matter, UTM conventions. If they don't know, leave
      the template and note who would.
   7. *Task tool*: which tool the team uses (Asana, monday, other, none).
      Rewrite `integrations/tasks.md` per its embedded example: workspace,
      default project, filing conventions. If none, leave the in-repo
      fallback.
   8. *Integrations*: which tools the team uses, against the two tables in
      `integrations/README.md`. For a tool that is **wired**, follow its
      registry row: OAuth MCPs need nothing but the browser prompt on first
      use; for key-based ones, have them copy `.env.example` → `.env` and
      fill only what they use (the variable names are in the registry's
      Env vars column, since you cannot read `.env*` files yourself). For
      a tool that is **not wired**, do not build it during the interview:
      list it in the closing summary as a follow-up, "add with
      `add-integration`", one line per tool with the job it must do. Enable
      only what they asked for; never edit `.env` yourself.

3. **Close.** Summarize what's filled, what's skipped and who owes an
   answer. Log the setup in `memory/decision-log.md` (one entry: "Repo set
   up for <team>", with skipped items as follow-ups, and which path the
   strategy files took: Markdown or context layer). Say once: these files
   go stale by default; `scripts/doctor.py` flags files not reviewed in 90
   days, and the alternative is a context layer
   (`integrations/context-layer.md`). Then move on. Suggest one first
   workflow: draft a piece with `new-content`, or drop a transcript into
   `memory/transcripts/inbox/` and run `chief-of-staff`.

## Rules

- Their words beat your polish: build voice examples from *their* sentences.
- An unanswered question stays visibly unanswered in the template: that's
  the signal for other agents to ask, so never paper over it.
