<!-- source: https://raw.githubusercontent.com/NEON-Rutger/B2B-revops-skills/main/revops-metrics/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Funnel and revenue metrics: formulas and ranges

Ranges are published B2B SaaS medians, for orientation only. A report
compares the team against its own previous periods; it cites a range only
to say whether a number is unusual, never as a target the team did not set.

## Funnel conversion (definitions from `data/ontology/metrics.md`)

| Step | Typical range |
| --- | --- |
| Lead to MQL | 20 to 25% |
| MQL to SQL | 15 to 21%; top performers around 40% |
| SQL to opportunity | 60 to 80% |
| Opportunity to win | 15 to 30%; enterprise 15 to 20%, SMB 25 to 35% |
| Lead to win | 1 to 3% |

## Pipeline velocity

```
velocity = opportunities * win rate * average deal size / sales cycle days
```

Four levers: volume, win rate, deal size, cycle length. Report each lever's
delta against the previous period so the team sees which one moved. A
short cycle matters: deals closed under about 50 days win far more often
than deals that run longer.

## Unit economics (when spend is in the repo)

| Metric | Formula | Range |
| --- | --- | --- |
| CAC | sales and marketing spend / new customers, by segment and by inbound vs outbound | outbound often 2 to 5x inbound |
| CAC payback | CAC / (ARPA * gross margin), in months | under 12 excellent, 12 to 18 strong, over 24 concerning |
| LTV | ARPA * gross margin * (1 / annual churn) | LTV to CAC 3:1 to 5:1; above 5:1 suggests under-investing |
| NRR | (starting ARR + expansion - contraction - churn) / starting ARR | 100 to 110% stable, 110 to 120% strong |
| GRR | (starting ARR - contraction - churn) / starting ARR | 90 to 95% strong; always at or under 100% |

Spend comes from `data/ads/snapshots/YYYY-MM-DD-finance-invoices.csv` and
the ads snapshots; a CAC without a spend snapshot is a gap.

## Diagnostic when the number is off

1. Volume: enough leads, MQLs, SQLs, opportunities entering?
2. Conversion: which step dropped?
3. Deal size: ACV down, discounting up?
4. Velocity: cycle longer, deals stalled?
5. Retention: GRR or NRR moved?

Slice each by owner, product, segment, source and cohort to separate a
systemic change from an individual one. Segment win rates that diverge
widely point at ICP drift or inconsistent stage definitions before they
point at a rep.

## Deal health (when the CRM records activity and contacts)

Six dimensions scored 0 to 3: next steps quality, activity velocity,
multi-threading, access to the economic buyer, review cadence, methodology
fields complete. 13 to 18 healthy, 10 to 12 watch, 9 or under at risk.
Report the count in each band, not the per-deal scores, in a public repo.
