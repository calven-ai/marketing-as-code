<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/product-marketing/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Completeness checklist for the strategy context

Condensed from the product-marketing context skill in marketingskills. That
skill keeps one product-marketing document that every other skill reads;
this repo spreads the same content across `strategy/` and `brand/`. Use the
list to find what a positioning refresh should check for, and where each
item lives here.

| Section in the source | Lives here |
| --- | --- |
| Product overview: one-liner, category, type, business model | `strategy/positioning.md`, `strategy/product-brief.md` |
| Target audience: company type, decision makers, primary use case, jobs to be done | `strategy/icp.md` |
| Personas: user, champion, decision maker, financial buyer, technical influencer | `strategy/personas.md` |
| Problems and pain points: core challenge, why alternatives fail, the cost, the emotional tension | positioning (alternatives), personas (pains) |
| Competitive landscape: direct, secondary, indirect, and their shortcomings | positioning (alternatives table), `strategy/competitive/` |
| Differentiation: what is different, and why that is better | positioning (unique attributes, value themes) |
| Objections and anti-personas | `strategy/messaging.md` (objections), `strategy/icp.md` (disqualifiers) |
| Switching dynamics (the four forces: push, pull, habit, anxiety) | positioning (why now), personas (objections) |
| Customer language: verbatim problem and solution descriptions, words to use and avoid | `memory/knowledge/` (customer language), `brand/voice.md` (banned list) |
| Brand voice | `brand/voice.md` |
| Proof points: metrics, named customers, testimonials, one per value theme | positioning (proof points), backed by `data/` snapshots |
| Goals: business goal, conversion action, current metrics | `projects/`, `data/ontology/metrics.md` |

## How the source keeps it current, and the equivalent here

- Auto-draft from what exists (README, landing pages, docs), then ask "what
  needs correcting, what is missing" and iterate. Here: draft the diff from
  the decision log, reports and knowledge, then ask the same two questions
  in the PR.
- A changelog at the bottom, one line per substantive revision with the
  date and the why; typo fixes get no entry. Here: `memory/decision-log.md`
  through `log-decision`, plus Git history.
- Specific questions beat broad ones: "what is the number one frustration"
  rather than "describe your customers". Ask for an example whenever an
  answer is abstract.
- Verbatim customer language outranks polished description in every
  section; if a section reads like copy, it needs a quote.
- Skip sections that do not apply (a B2C product has no buying committee)
  rather than filling them with placeholders.
