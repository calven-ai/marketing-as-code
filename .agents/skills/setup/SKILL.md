---
name: setup
description: Onboard a team into this repo. Use when asked to "set up the repo", "run the setup interview", or when the strategy/brand/ontology templates are clearly unfilled and the user wants to start working. Interviews the team, fills the templates from their answers, connects integrations, and writes the task-tool adapter.
---

# Setup: the onboarding interview

You are turning a blank template into *this team's* second brain. Interview,
then fill — never invent answers, and never overwrite something the team
already filled in without asking.

## Procedure

1. **Take stock.** Check which of these are still unfilled templates:
   `strategy/positioning.md`, `strategy/messaging.md`,
   `strategy/icp-personas.md`, `brand/voice.md`, `brand/visual-identity.md`
   + `brand/tokens.json`, `data/ontology/*.md`, `integrations/tasks.md`.
   Tell the user what's missing and that you'll work through it in short
   rounds — they can stop anytime and resume later.

2. **Interview in this order** (each round: a few questions, then you draft
   the file, then they correct it — don't ask twenty questions up front):
   1. *Positioning* — who is it for, what problem, what category, why you
      over the alternative. Draft `positioning.md`, iterate.
   2. *Messaging* — the narrative and 2–4 pillars with proof. Existing
      homepage copy or a pitch deck is admissible evidence: ask if there's
      something to paste.
   3. *ICP & personas* — great fit / poor fit, the people in the deal.
   4. *Voice* — three adjectives, do/don't examples (ask for a paragraph
      they love and one that made them cringe; derive rules from those),
      banned words.
   5. *Visual identity* — colors and fonts if known; fill `tokens.json` and
      `visual-identity.md` together. Skippable.
   6. *Ontology* — what a signup/MQL/SQL actually means here, funnel stages,
      the few events that matter, UTM conventions. If they don't know, leave
      the template and note who would.
   7. *Task tool* — which tool the team uses (Asana, monday, other, none).
      Rewrite `integrations/tasks.md` per its embedded example: workspace,
      default project, filing conventions. If none, leave the in-repo
      fallback.
   8. *Integrations* — which of the tools in `integrations/README.md` the
      team uses. For OAuth MCPs, point them at the setup doc in
      `integrations/` (or at the registry row while the doc doesn't exist
      yet); for key-based ones, have them copy `.env.example` → `.env` and
      fill only what they use — the variable names are in the registry's
      Env vars column, since you cannot read `.env*` files yourself. Enable only what they asked for; never edit `.env` yourself.

3. **Close.** Summarize what's filled, what's skipped and who owes an
   answer. Log the setup in `memory/decision-log.md` (one entry: "Repo set
   up for <team>", with skipped items as follow-ups). Suggest one first
   workflow: draft a piece with `new-content`, or drop a transcript into
   `memory/transcripts/inbox/` and run `chief-of-staff`.

## Rules

- Their words beat your polish: build voice examples from *their* sentences.
- An unanswered question stays visibly unanswered in the template — that's
  the signal for other agents to ask, so never paper over it.
