<!-- source: https://raw.githubusercontent.com/seranking/seo-skills/main/skills/seo-plan/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Plan structure: pillars, phases, metrics, critical path

Condensed from SE Ranking's seo-plan skill.

## Inputs, and what to do when one is missing

The plan composes specialist outputs; it does not replace them. Treat an
output older than 30 days as missing. For each missing input list the
skill, its rough cost, and ask once whether to run it now; the default is
no, and the missing items open the plan as Phase 0: discovery. Never
bypass a specialist's own cost check.

## Four pillar scores (0 to 100)

| Pillar | From |
| --- | --- |
| Technical health | severity-weighted issue count in the audit |
| Content quality | average page quality across audited pages (experience, expertise, sourcing, freshness) |
| Topical authority | cluster coverage relative to the top three competitors: pillars with a page, spokes published |
| AI-search readiness | citation share against competitors on the prompt set |

The lowest pillar is the lead theme of the first phase.

## Business-type templates (what the work items default to)

- SaaS and B2B: product-led pillars, integration pages, comparison and
  alternatives pages, jobs-to-be-done content, decision-stage pages.
- Publisher: topical clusters, author expertise, freshness cadence,
  AI-search citations.
- Ecommerce and local: category hygiene, product schema, faceted
  navigation rules, location pages (not this repo's usual case).

## Three phases, always three

| Phase | Weeks | Content |
| --- | --- | --- |
| Foundations | 1 to 4 | technical fixes that unblock everything, a baseline snapshot, one or two quick refreshes from the decay list |
| Build | 5 to 8 | one pillar and three to seven spokes from the cluster map, schema fixes, a comparison page if the competitive frame supports it |
| Compound and measure | 9 to 12 | AI-readiness pass on top pages, the backlink outreach batch, the second decay or drift comparison, retro and adjust |

A 30-day plan compresses the phases; a year repeats build and compound
with refreshed inputs and a quarterly retro.

## Work item row

Number, item, skill or source that produces it, owner role, effort
(S, M, L), phase-end metric. Phase exit criteria in one line.

## Metrics

Lagging (quarterly): organic traffic, keywords ranking top 10, organic
conversions. Leading (weekly or monthly): technical issue count, pages
passing the quality bar, AI-search citation count, referring domains.
One leading and one lagging per phase, each with a current value and a
target the base rate supports; say when the math does not support the
target the team wanted.

## Critical path

The ordered list of work items that block later ones ("rewrite the
pillar" depends on "fix noindex on the blog template" depends on "run the
audit"). This is the deliverable most teams lack; everything not on it is
movable.

## Constraints

Repeat the team's constraints (engineering capacity, no template changes,
content budget) and drop items that violate them, however high their
leverage. A plan that will not ship is worse than a smaller one that
does.

## Cadence

Re-run at the end of the horizon with the drift or decay comparison as
input; the "where you are" section updates and everything follows.
