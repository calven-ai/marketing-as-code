# strategy/

**Kind:** context, what the team knows.

Market truth: who we serve, what we claim, and against whom. This is what an
agent loads before doing any marketing *thinking*. (How we sound and look
lives in [`brand/`](../brand/), loaded at *making* time.)

## What is authoritative here

| File | Owns |
| --- | --- |
| [positioning.md](positioning.md) | Positioning statement, category, alternatives, unique attributes, value themes, proof |
| [messaging.md](messaging.md) | Core narrative, value pillars, value props and matrix by persona, objections, boilerplate |
| [icp.md](icp.md) | Ideal customer profile: firmographic, technographic and behavioral fit, triggers, tiers, verticals, disqualifiers, scorecard |
| [personas.md](personas.md) | The people in the deal: goals, pains, gains, jobs to be done, objections, watering holes |
| [product-brief.md](product-brief.md) | What the product is: capabilities, use cases, integrations, architecture, pricing, differentiators and weaknesses |
| [competitive/](competitive/) | Competitor notes and battlecards, one file per competitor |

Every file carries frontmatter: `source` (`repo` or `context-layer`),
`last_reviewed` (the date the team last confirmed the content is true), and
`owner`. The four documents with an MCP twin also carry `document`.

## Rules

- Everything downstream (content, campaigns, prototypes) inherits from these
  files. When positioning changes, it changes here first, then everything
  that inherits from it gets reviewed.
- If a file is still an unfilled template, agents ask the team rather than
  inventing strategy. `/setup` fills these from an interview.
- Log strategy changes in `memory/decision-log.md` with the reasoning.

## Keeping this current

These files go stale by default. Nobody owns the update, every agent keeps
reading last quarter's positioning, and when positioning does change,
messaging, personas, battlecards and published content all have to be walked
through by hand. Two ways to handle it:

1. **Maintain the Markdown.** Every file here carries `last_reviewed` in its
   frontmatter. `python3 scripts/doctor.py` lists files not reviewed in 90
   days, and CI prints the same list on every pull request. When positioning
   changes, change it here first, then review everything that inherits from
   it.
2. **Connect a marketing context layer.** A service that holds positioning,
   messaging, ICP, personas and competitive intelligence, keeps them current
   from research and customer signals, and serves them to every agent over
   MCP. The files in this folder become the fallback and the MCP becomes the
   truth. Calven, which maintains this repo, makes one, and it is the example
   the repo is wired for. See
   [integrations/context-layer.md](../integrations/context-layer.md).

The templates here mirror the documents Calven serves (same document set,
same section headings), so a team can start in Markdown and switch later
without restructuring anything.
