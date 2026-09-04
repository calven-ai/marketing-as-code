<!-- source: https://raw.githubusercontent.com/thatrebeccarae/claude-marketing/main/skills/cross-platform-audit/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Benchmarks and decision rules for the weekly paid report

Condensed from the cross-platform audit above and, for the platform
tables, thatrebeccarae's Google Ads and LinkedIn Ads skills and
coreyhaines31's Google Search and LinkedIn B2B playbooks (all MIT). Use
these to label a number as unusual, never as a target: the target is in
`projects/<campaign>/campaign.md`, and the narrowest comparison wins
(this campaign last week, then this account, then a peer cohort, then an
industry range).

## Pause and scale rules

- **Kill list**: a campaign at more than 3x its target CPA or CPL, for two
  consecutive weeks, with enough clicks to judge (below). Recommend pause;
  never pause a campaign in its learning phase or inside the first week
  after a bid or budget change.
- **Scale list**: a campaign under target CPL that is budget-constrained
  (Google: search lost impression share due to budget; LinkedIn: daily
  budget exhausted early, audience penetration under 25%). Recommend +20%
  at a time and 3 to 5 days between steps; a 30% jump resets learning.
- **Minimum clicks before a verdict**: brand search 50, non-brand search
  25, display 15, LinkedIn sponsored content 20, Lead Gen Form campaigns
  20. Fewer is "wait", with the click count in the report.
- **Attribution sanity**: if platform-reported conversions exceed the
  neutral source (GA4, CRM) by more than 20%, say so and do not reallocate
  budget on the platform numbers alone. Never add conversions across
  platforms with different attribution windows without normalising.
- **Broken tracking halts everything else**: if the primary conversion
  action received nothing in 30 days, the first recommendation is to fix
  tracking, not to move budget.
- **Platform minimums**: do not recommend moving 500 a month to a platform
  whose useful minimum is 3,000 a month.

## Google Ads (B2B search)

| Metric | Good | Excellent | Alert |
| --- | --- | --- | --- |
| Search CTR | 4 to 6% | 8%+ | under 3% |
| Search conversion rate | 3 to 5% | 7%+ | under 2% |
| Quality score | 7 to 8 | 9 to 10 | under 6 |
| Brand impression share | 90%+ | 95%+ | under 80% |
| Non-brand impression share | 40 to 60% | 70%+ | under 30% |
| Display CTR | 0.5 to 1% | 1.5%+ | under 0.3% |

Wide B2B SaaS ranges: brand CTR 8 to 20% and CVR 15 to 40%; non-brand
high-intent CTR 2 to 6%, CVR 3 to 10%, CPC 8 to 40+, CPL 80 to 400+.
Competitor terms run higher CPC and lower CVR than non-brand. Smart
bidding needs about 30 conversions in 30 days per campaign; campaigns
under 15 conversions a month should merge or run manual CPC. Lost
impression share (budget) is a money problem; lost impression share
(rank) is an ad-quality problem.

## LinkedIn Ads (B2B)

| Metric | Good | Average | Poor |
| --- | --- | --- | --- |
| CTR, sponsored content | over 0.8% | 0.4 to 0.8% | under 0.4% |
| CTR, message ads | over 3% | 1 to 3% | under 1% |
| CPC | under 5 | 5 to 10 | over 10 |
| CPM | under 30 | 30 to 60 | over 60 |
| Cost per lead | under 50 | 50 to 150 | over 150 |
| Lead form completion | over 15% | 10 to 15% | under 10% |

Funnel view from the B2B playbook: click-through to landing page 0.30 to
0.55% cold, 0.55 to 0.80% mid-funnel, 0.80 to 1.30% retargeting; CPM 33 to
65; cost per Lead Gen Form 50 to 200; cost per website form 200 to 500;
lead form fill rate over 8%. Scale on audience penetration, not spend:
under 25% raise the budget, 25 to 35% hold, over 35% add audiences
instead. Rising spend with flat reach means competitors outbid you or the
creative is weak. Refresh creative every 4 to 6 weeks.

## The weekly scorecard

Spend, leads, CPL, lead to SQL rate (from the CRM), SQLs, cost per SQL,
search impression share, top wasted search terms. In-platform conversions
are form fills; the CRM decides what became pipeline, and B2B cycles run
60 to 180 days, so reconcile monthly and let the CRM win.
