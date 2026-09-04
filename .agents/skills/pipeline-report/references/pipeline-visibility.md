<!-- source: https://raw.githubusercontent.com/NEON-Rutger/B2B-revops-skills/main/pipeline-visibility/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Pipeline metrics: formulas, thresholds, signals

Condensed for the weekly report. Every stage name and probability below is
an example; the team's own are in `data/ontology/funnel.md` and its closed
deals.

## Formulas

| Metric | Formula | Notes |
| --- | --- | --- |
| Coverage | open pipeline / remaining target | required coverage = 1 / historical win rate; a 25% win rate needs 4x |
| Stage conversion | deals that reached the next stage / deals that entered this stage, over a closed cohort (won and lost) from the trailing 12 months | recompute quarterly; never from open deals only |
| Velocity (days per stage) | median of (exit date - entry date) per stage over the closed cohort | the baseline for "stalled" |
| Days in current stage | today - entry date | flag when above the stage baseline by more than 25% |
| Stale deal | open, no logged activity past the stage threshold | dashboard metric: % of pipeline stale, target under 15% |
| Overdue close date | open deals with close date before today / open deals | target under 5%; count pushes per deal |
| Win rate | won / (won + lost) over the same period | rolling 3 months; segment by size band and source |
| Pipeline created | deals with created date in the period | the leading indicator; report against a weekly target |
| Forecast accuracy | 1 - abs(actual - commit) / target | 80 to 85% acceptable, 85 to 95% good, above 95% rare |

## Thresholds used as defaults until the team sets its own

| Item | Default |
| --- | --- |
| Coverage RAG | green at or above 3.5x, amber 2.5x to 3.4x, red under 2.5x; industry range 3x to 5x |
| Stale after (by stage) | early stages 7 to 14 days; proposal 7 days; negotiation 5 days |
| Stage count | 5 to 8 stages, each with a verifiable exit criterion tied to a buyer action |

## Weekly waterfall

```
starting pipeline (last snapshot)
  + created this week
  + advanced (amount now in a later stage)
  - pushed (close date moved to a later period)
  - closed lost
  - closed won
= ending pipeline (this snapshot)
```

Compute it by diffing this week's `pipeline` snapshot against last week's
on `deal_id`; deals present last week and absent now are in
`closed-deals` or were deleted (say which).

## Deal risk signals

| Signal | Reads as |
| --- | --- |
| no activity over 7 days at proposal or later | at risk; ask the owner |
| close date pushed 3 or more times | timeline not real |
| one contact on the deal | fragile; multi-threading wanted (3+ contacts close markedly more often) |
| amount decreased | scope or competitive pressure |
| stage moved backwards | re-qualify |
| activity spike from the buyer | evaluation accelerating |

## Minimum report set

Pipeline by stage; pipeline by close month (next two quarters); win rate
(this quarter); sales cycle length (won this quarter); conversion funnel
by cohort; stale deals; loss reasons (90 days); coverage; pipeline created
by week. The executive view is six widgets: pipeline by forecast category,
coverage with RAG, win rate trend, average deal size trend, forecast vs
actual for three periods, top ten deals with stage, next step and days in
stage. Marketing's additions: sourced and influenced pipeline by source,
against `data/ontology/naming.md`.
