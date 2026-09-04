<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/ads/references/payback-period.md | license: MIT | fetched: 2026-09-04 -->

# Payback period: what a lead may cost

Condensed from the payback-period reference above. Use it to set the
target CPL or CPA a brief is judged against, and to say when a channel
cannot pay for itself no matter how good the copy is.

## Formulas

- Payback (months) = CAC / monthly ARPU. Healthy range 3 to 12 months.
- Discounted payback = CAC / (monthly ARPU x annual retention), with
  retention as a fraction (0.70 for 70%). This is the number to plan on;
  most churn happens in the first three months, so raw payback flatters.
- CAC is all-in: media, creative, tooling and the people who run it,
  divided by customers won, not leads.
- Target CPL = affordable CAC x lead-to-customer rate (from the CRM,
  through `data/ontology/funnel.md`). No funnel rate means no CPL target;
  say so.

## Why LTV:CAC misleads

It assumes every customer eventually churns at a uniform rate, hides
plan-level variance under a blended average, and ignores the gap between
spending and collecting. A 3:1 ratio can sit on a channel that runs out
of cash. Payback shows the timing.

## Worked numbers from the source

CAC 300 across three plans:

| Plan | Monthly ARPU | Payback |
| --- | --- | --- |
| Starter | 9 | 33 months, unaffordable |
| Pro | 99 | 3.0 months, scalable |
| Enterprise | 999 | 0.3 months |

Discounted: CAC 300, ARPU 99, 70% annual retention gives 4.3 months,
still viable.

## Decision rules

1. Compute all-in CAC per channel from `data/ads/snapshots/` and the CRM.
2. Compute discounted payback per plan or segment the campaign targets.
3. Run paid only where discounted payback is 12 months or under; route
   segments above that to organic or product-led motions.
4. Recompute monthly; CAC drifts as spend scales.
5. In the brief, state the plan the persona buys, the affordable CAC, the
   funnel rate used, and the resulting target CPL, each with its source.

Under 3 months usually means the team is under-investing; over 12 means
the channel is being subsidised. Story-driven copy outperforms
feature-first copy in the source's experience; test it, one variable at
a time.
