<!-- source: https://raw.githubusercontent.com/NEON-Rutger/B2B-revops-skills/main/revops-forecasting/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Forecasting: the month-end section

Three views, computed from the same snapshots, presented side by side.
Where they converge the number is trustworthy; where they diverge, the
divergence is the finding.

## View 1: forecast categories (what the reps say)

Deals carry a category in the CRM (HubSpot `hs_forecast_category`,
Salesforce `ForecastCategoryName`). Expected close rates by category, as
a sanity range, not a rule:

| Category | Meaning | Typical close rate |
| --- | --- | --- |
| Commit | buyer confirmed, terms agreed, procurement or legal started, closes this period | 85 to 95% |
| Best case | well progressed, one or more risks left | 40 to 60% |
| Upside | could close if everything aligns; usually timing risk | 15 to 30% |
| Pipeline | active, discovery ongoing | 5 to 15% |

```
conservative = commit * 0.9
expected     = commit * 0.9 + best case * 0.5
optimistic   = expected + upside * 0.2
```

Slippage runs high (around a third of deals slip a period in recent
benchmarks); apply the team's own measured slip rate to best case and
upside, and say what it is.

Commit checklist a manager applies: buyer confirmed intent this period;
economic buyer engaged; commercial terms agreed; a documented close plan;
procurement or legal started; close date inside the period; the owner can
explain it in two minutes. A commit missing two of these is best case.

## View 2: stage-weighted pipeline (what history says)

```
weighted pipeline = sum over open deals of amount * P(close | current stage)
```

`P(close | stage)` is the team's stage-to-close rate from the trailing 12
months of closed deals, segmented when the volume allows (size band,
inbound or outbound, new or expansion). The CRM's default stage
probabilities are a placeholder until replaced; say which you used.

## View 3: run rate (what the trend says)

Average closed-won per period over the trailing periods, times periods
left, optionally adjusted by the trailing growth slope and the same period
last year. Reliable for renewals and expansion, weak for lumpy new
business.

## Coverage and the gap

```
coverage = open pipeline / remaining target
required = 1 / win rate
gap      = remaining target - expected
```

Reps starting a quarter above roughly 3.2x weighted coverage hit quota far
more often than those under 2.8x; treat 3x as the floor, 3.5x healthy, 4x
strong, higher when win rates are low. State what pipeline must be created
by when to close the gap, given the median cycle length.

## Accuracy, tracked over time

```
accuracy = 1 - abs(actual - forecast) / actual
```

Within 10% is strong, 15 to 20% average, 25% or more a structural
problem. Consistent over-forecasting points at loose commit criteria and
optimistic close dates; consistent under-forecasting at sandbagging or
late-attributed inbound. Keep every month-end forecast in the report so
the next run can score it.
