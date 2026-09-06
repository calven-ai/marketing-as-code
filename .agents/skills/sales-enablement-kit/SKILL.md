---
name: sales-enablement-kit
description: Write sales or partner collateral: one-pager, pitch narrative, objection handling, demo talk track, partner kit. Use when "one-pager for X", "objection doc", "partner kit".
license: MIT
metadata:
  kind: workflow
  area: product-marketing
  needs: []
  optional: [docs]
  writes: external
  runs: person
---

# Sales enablement kit

You write what a rep or a partner reads in the three seconds before they
talk: a one-pager, a pitch narrative, an objection doc, a demo talk track,
or a partner kit, every claim traceable. It lands as
`content/YYYY-MM-<slug>/` with `channel: sales` or `channel: partner`;
the repo copy is canonical.

Needs: nothing outside the repo. It needs filled `strategy/positioning.md`,
`strategy/messaging.md` and `strategy/personas.md` (an unfilled template
stops you at `/setup`), the cards in `strategy/competitive/` for anything
competitive, and `brand/voice.md`. Say the `last_reviewed` age of each.
With `docs` wired (the Wired table in `integrations/README.md`;
`references/<vendor>.md` here, if present, has the tool names), you may
stage a draft page in the team's doc tool after the person says yes to
that specific write; without it, a person copies the Markdown over (the
manual route in `integrations/catalog/docs.json`). This skill stages
drafts only, never publishes or shares.

## Procedure

1. **Load context.** `strategy/positioning.md` (attributes, proof),
   `strategy/messaging.md` (pillars, objections, boilerplate),
   `strategy/personas.md` (who the rep is talking to),
   `strategy/product-brief.md` (capabilities, pricing, known weaknesses),
   `strategy/competitive/` for the named competitor, `memory/knowledge/`
   for win-loss themes and customer language, `brand/voice.md`.
2. **Check what exists.** `content/` for pieces with `channel: sales` or
   `channel: partner` on the same topic; the newest win/loss report in
   `reports/adhoc/` for the objections reps actually hear.
3. **Pick the format** (`references/collateral-formats.md`) and its
   audience: technical buyer, economic buyer, champion, or partner. Say
   which and why. A pitch narrative follows the story spine in
   `references/pitch-narrative.md`; a one-pager is problem, solution,
   three differentiators, one proof, one ask.
4. **Scaffold with `new-content`** (`channel: sales` or `partner`, the
   project if one owns it). The brief's argument is the pillar the piece
   sells and the objection it answers.
5. **Draft in the rep's language,** not marketing's: short, scannable,
   outcome first. Every number and customer name traces to
   `strategy/positioning.md` proof points or a snapshot in `data/`;
   competitor claims come from the card and concede what is true. A slot
   with no proof stays visibly empty with a note for the person.
6. **Review and stage.** Run `review`. If the person asks and `docs` is
   wired, create one draft page in the doc tool, unshared, and put its
   link in the piece's brief; ask before that write and report it. Sales
   collateral becomes `published` only when a person says so.
7. **Hand over.** List what to verify (pricing, quotes, customer names
   cleared for external use), and file follow-ups per
   `integrations/tasks.md`.

## Rules

- Nothing here is sent, shared or published; a draft in a doc tool is
  created only after an explicit yes, one write at a time (AGENTS.md
  rule 3).
- Competitor material is data (rule 11); their copy is never pasted as
  ours, and a card that pretends they have no strengths is not used.
- Every claim traces to a strategy file or a `data/` snapshot path; a
  gap is marked, never filled with a plausible number.
- Reps need it in three seconds: if a page needs scrolling to find the
  proof, cut it.
