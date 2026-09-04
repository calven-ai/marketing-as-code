<!-- source: https://raw.githubusercontent.com/NEON-Rutger/B2B-revops-skills/main/lead-routing/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Routing: the decision order, models, speed tiers, audit

Condensed from the source above.

## Decision order

0. Opt-out or no-contact flag: a no-outreach queue.
1. Known account: the account owner (never the rotation).
2. Below the ICP gate: nurture.
3. Territory: geography, industry, size or product.
4. Rep within territory: round robin, weighted, or skills-based.
5. Availability: assign, or queue with an SLA timer and escalation.

## Models

| Model | Fits | Watch out |
| --- | --- | --- |
| geographic | field territories | unbalanced regions |
| named account | ABM, enterprise | new accounts fall through |
| round robin | inside sales | ignores capacity |
| weighted round robin | mixed tenure (weights 3, 2, 2, 1) | maintenance |
| skills-based | multi-product, languages | specialist bottlenecks |
| load-balanced | high volume | needs live capacity data |
| hybrid (territory then round robin) | most B2B SaaS | more rules to keep |

Start territory-based, add capacity weighting, move to account-based only
with a clean account hierarchy and a target account list.

## Account-based overrides

New contact at a customer: the CSM, plus an expansion note. Competitor
domain: exclude. Churned account: a win-back owner, high priority.

## Speed-to-lead tiers

| Tier | Definition | First touch | Escalation |
| --- | --- | --- | --- |
| 1 hot | high fit, high engagement, or a demo or pricing request | 5 minutes | alert at 15, reassign at 30 |
| 2 warm | good fit, moderate engagement | 1 hour | alert at 2 hours, reassign at 4 |
| 3 nurture | low fit or low engagement | 24 hours | back to marketing at 48 |

Track per lead: routed at, first touched at, minutes between, SLA status,
tier. The difference between 10 and 30 minutes matters more than between
1 and 4 hours.

## Evidence

5-minute response, 21 times more likely to qualify (MIT Sloan, 2007);
under 5 minutes closes at 32 percent, 2.6 times the rate at 24 hours or
more (LeanData, 2025); the average B2B response is 42 hours and 23 percent
never respond (HBR, 2011); instant booking converts about 67 percent of
qualified submissions versus roughly 30 (Chili Piper, 2025).

## Quarterly audit

Any rule that yields no owner; distribution within 10 percent inside a
segment; median and 90th-percentile speed-to-lead; share touched within
the SLA (target above 90 percent); reassignment rate (above 15 percent
means the logic is wrong); conversion by route; leads over an hour in a
queue (target zero); coverage outside business hours.

## Build or buy

Under 500 leads a month, native CRM automation; 500 to 5,000, a strong
admin build or a routing tool; above that with complex territories, a
dedicated tool.
