<!-- source: https://raw.githubusercontent.com/NEON-Rutger/B2B-revops-skills/main/icp-builder/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# ICP validation: dimensions, thresholds, tiers

Condensed from the ICP builder in the B2B RevOps skills. The validation
mode is what this skill runs; the build and expand modes are summarised so
you can name them when the team needs more than a refresh.

## Seven dimensions to rate (strong, adequate, weak, missing)

| Dimension | Strong looks like | Red flag |
| --- | --- | --- |
| Specificity | Named industry, revenue band, headcount, geography, stack, stage | "Everyone"; criteria that describe 50,000 companies |
| Pain clarity | Problems in customer language, per persona | Vendor jargon; "better visibility" |
| Buying signals | Triggers that say in-market now (board pressure, missed target, migration) | No difference between active market and total universe |
| Evidence base | Enough comparable great customers (see thresholds) | Defined in an offsite without customer input; CRM-only sample |
| Segmentation | Segments split by motion, buying process, committee, value prop | One definition for very different customers |
| CRM operationalisation | Criteria filterable in the CRM; fit score is a field; reports by segment | ICP lives in a slide deck; tiers by intuition |
| Feedback loop | Quarterly review fed by win/loss and CS health | Written once, never revisited |

Deliverables of a validation: the score table with one sentence per
dimension, the single highest-leverage fix, three prioritised
recommendations with an owner, three to five probing questions, and
whether to refine or rebuild.

## Customer count thresholds by motion

| Motion | Customers needed | Confidence |
| --- | --- | --- |
| No touch, product-led | about 160 | 95 percent |
| Low touch, one stage | about 80 | 90 percent |
| Medium touch, two stage | about 40 | 85 percent |
| High touch, field sales | about 27 | 80 percent |
| Dedicated, named accounts | about 20 | 75 percent |

Below the threshold, call it an early customer profile and iterate
quarterly; calling it an ICP distorts the forecast.

## Tiers with a 0 to 100 fit score

Five to eight weighted attributes across firmographic, technographic and
behavioral pillars; one weight set per segment; computable from enrichment
data alone, no discovery call needed.

| Tier | Score | Expected win rate |
| --- | --- | --- |
| T1, perfect fit | 80 to 100 | 60 to 80 percent |
| T2, good fit | 50 to 79 | 30 to 50 percent |
| T3, opportunistic | below 50 | 10 to 30 percent; do not chase |

Validate monthly against cycle times (MQL to SQL, SQL to win, win to
onboarded, time to first impact). When a tier loses a column, change one
weight and test it for a quarter.

## Goldilocks checks before finalising

Sustainable ACV for the motion (about 20k for medium touch, 50k for high
touch); deals closing in two to four months (six or more means the ICP is
too big); five or more reference customers; cost to serve at most 30
percent of ACV; at least 100 addressable targets.

## The build path (GAP), when a refresh is not enough

Gather (CRM history, market data, enrichment, conversations; interviews are
the highest-value source), Analyse (industry, size, stack, revenue model,
pain patterns, usage, signals, pipeline behavior), Profile (definition with
explicit exclusions, tiers, personas, informational needs per buying
phase). A full build is four to six weeks; a validation is one or two days.

## Expansion triggers

Win-rate plateau, pipeline saturation, NRR signals, competitive pressure,
TAM exhaustion, new product capability. Expand by geography first, then
vertical, then account size.

## Definition of good

Any company scores from data alone; tier 1 is a four-figure list from a
six-figure universe (fifty accounts at an early stage, not five thousand);
the score is a CRM field that drives routing and reports; the evidence
base includes companies never contacted; the list is re-scored quarterly.
