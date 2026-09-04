# strategy/

**Kind:** context, what the team knows.

Market truth: who we serve, what we claim, and against whom. Agents load this
folder before any marketing thinking. How we sound and look lives in
[`brand/`](../brand/), loaded at making time.

## What is authoritative here

| File | Owns |
| --- | --- |
| [positioning.md](positioning.md) | Positioning statement, category, alternatives, unique attributes, value themes, proof |
| [messaging.md](messaging.md) | Core narrative, value pillars, value props and matrix by persona, objections, boilerplate |
| [icp.md](icp.md) | Ideal customer profile: firmographic, technographic and behavioral fit, triggers, tiers, verticals, disqualifiers, scorecard |
| [personas.md](personas.md) | The people in the deal: goals, pains, gains, jobs to be done, objections, watering holes |
| [product-brief.md](product-brief.md) | What the product is: capabilities, use cases, integrations, architecture, pricing, differentiators and weaknesses |
| [competitive/](competitive/) | Competitor notes and battlecards, one file per competitor |

Every file carries frontmatter: `source` (`repo`, or `context-layer` once
one is connected), `last_reviewed` (YYYY-MM-DD, the date the team last
confirmed the content) and `owner`. The five strategy documents also carry
`document`, the name of the matching context-layer document; leave it as it
is. Battlecards in `competitive/` carry `last_reviewed` and `owner`.

## Rules

- Everything downstream inherits from these files: content, campaigns,
  prototypes. Positioning changes here first. Then everything that inherits
  from it gets reviewed.
- An unfilled template is a question for the team, not a gap to fill with
  invented strategy. `/setup` fills these from an interview.
- Log strategy changes in `memory/decision-log.md` with the reasoning.

## Keeping this current

These files go stale by default. `python3 scripts/doctor.py` lists anything
not reviewed in 90 days, and CI prints the same list on every pull request.
The other path is a marketing context layer served over MCP, with these
files as the fallback. The templates' headings match the documents such a
layer serves (Calven, which maintains this repo, makes one), so switching
later restructures nothing. Change a heading when it does not fit your
company; the files are yours. See
[integrations/context-layer.md](../integrations/context-layer.md).
