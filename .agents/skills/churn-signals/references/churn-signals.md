<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/churn-prevention/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Churn signals, health scoring and saves

Condensed from the source above (a self-serve and SaaS churn guide); the
parts a weekly at-risk list uses. Thresholds are the source's, not this
team's; the ontology wins where it defines them.

## Early signals, two to four weeks before a cancel

- Login frequency down 50 percent or more.
- A key feature stops being used.
- Support tickets spike, then go quiet.
- Visits to the billing or plan page spike.
- Seats removed from the team.
- A data export started.

## A health score, if the team wants one

| Component | Weight |
| --- | --- |
| login frequency | 30 |
| feature usage | 25 |
| support sentiment | 15 |
| billing health | 15 |
| engagement (email, community, events) | 15 |

80 to 100 healthy; 60 to 79 needs a check-in; 40 to 59 at risk; below
40 critical, personal outreach. Only compute it when
`data/ontology/metrics.md` adopts a definition; otherwise report the raw
signals.

## Two kinds of churn

Voluntary (the customer decides; half to two thirds of churn) and
involuntary (a payment fails; the rest). Involuntary churn is the cheaper
fix: card-expiry alerts at 30, 15 and 7 days, a backup payment method,
smart retries on days 1, 3, 5 and 7, and a four-step dunning sequence
over ten days. A past-due subscription on the weekly list is an
involuntary signal; route it to whoever owns billing, not to a CSM
conversation.

## Match the save to the reason

| Reason | Offer |
| --- | --- |
| too expensive | a modest time-boxed discount (20 to 30 percent for two or three months) or a downgrade framed as right-sizing |
| not using it enough | a pause of one to three months, or onboarding again |
| missing feature | a roadmap preview with a date |
| switching | a comparison and a conversation, not a blanket discount |
| technical trouble | immediate escalation |
| temporary need | a pause |
| business closing | a graceful exit, no offer |

The top slice of accounts by revenue gets a person, not an offer.
Discounts above 50 percent train cancel-and-return behaviour; pauses
beyond three months rarely reactivate.

## Benchmarks the source gives

Cancel-flow save rate 25 to 35 percent average, above 35 good; pause
reactivation 60 to 80 percent; payment recovery 40 to 50 percent average.
External figures; the team's own come from comparing the weekly lists
over a quarter with the churn snapshot.

## Mistakes to name in Caveats

No cancel flow at all; a hidden cancel path; one offer for every reason;
silent payment failures; guilt-trip messaging; no way back after a cancel.
