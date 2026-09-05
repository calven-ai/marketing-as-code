<!-- source: https://raw.githubusercontent.com/NEON-Rutger/B2B-revops-skills/main/marketing-operations/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Dual-axis scoring, decay, calibration and the written SLA

Condensed from the source above.

## Dual-axis model

Fit score (account level, 0 to 100): size, geography, industry, tech stack,
growth stage. Engagement score (behaviour, 0 to 100): visits with weekly
decay, clicks (not opens), content depth, events, trial activation.

MQL threshold example: fit at least 40 and engagement at least 30 in the
last 30 days. Teams moving from one axis to two report acceptance gains of
5 to 15 points.

Decay: half-life 30 days (50 percent of peak after 30 days of silence, 25
percent after 60).

## Stages

subscriber (email captured), lead (validated), MQL (meets both scores),
SAL (sales accepted), SQL (open opportunity with discovery scheduled).

## The written SLA

| Marketing commits | Sales commits |
| --- | --- |
| X MQLs a month meeting the definition | review each MQL within 24 hours |
| name, email, company, title, both scores, source on every MQL | accept or reject with a categorised reason |
| MQL delivered within 1 hour in business hours | follow up an accepted lead within 4 hours |
| weekly rejection-trend report | weekly pipeline visibility |
| attribution closed within 5 days of month end | quarterly win and loss feedback |

Reason codes: bad fit, low intent, wrong timing, duplicate, wrong role.

Healthy acceptance: 60 to 80 percent. Under 50 means the scoring or the
definition is broken; over 85 means the threshold is too low. Rejection
above 70 percent triggers a model audit.

Escalation: marketing misses volume, discuss the cause; sales ignores MQLs,
leads recycle and budget moves; either side misses twice, a joint review.

## Speed targets

| Metric | Target |
| --- | --- |
| first response, tier 1 | under 5 minutes |
| first response, general | under 10 minutes |
| MQL to SAL | under 24 hours |
| SAL to SQL | under 7 days |
| capture to first contact, median | under 4 hours |

## Recycling

Disqualify (remove): no budget for 12 months or more, happy with a
competitor, not involved in buying, 18-month-plus timeline. Recycle
(nurture hold): "not now"; re-score after 60 days; reactivate on a trigger.
Reactivation runs 8 to 15 percent within six months.

## Quarterly calibration

1. Pull last quarter's MQLs with outcomes (accepted, rejected, recycled,
   SQL, won).
2. Which dimensions predicted wins; which produced false positives.
3. Holdout: 10 to 15 percent of inbound on a challenger model for 30 days.
4. Re-weight; keep at least 100 MQLs per tier before trusting a change.
5. Version the model (v1, v2), date each change, never edit the live one.
   Roll back if acceptance drops more than 10 points.

## Shared definitions, written once

What is an MQL, what is pipeline (stage, close window, minimum value),
what is sourced (SAL created from an MQL), what is influenced (any
marketing touch before close). No shared definitions, no trust.

## Compliance notes for EU teams

B2B scoring usually rests on legitimate interest: record the purpose, the
balancing test, an easy opt-out, and the scoring date and model per
record. Disclose AI-assisted qualification in the first outreach. Enrich
MQLs, not every lead.
