<!-- source: https://raw.githubusercontent.com/NEON-Rutger/B2B-revops-skills/main/abm-engagement-scoring/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Engagement scoring: weights, decay, coverage, the hand-off gate

Condensed from the source above. These are starting weights; the team's
own rules, once `lead-lifecycle-spec` writes them into `data/ontology/`,
override every number here.

## Signal weights

| Signal | Points | Decay |
| --- | --- | --- |
| website visit | 1 | weekly, keep 50 percent |
| pricing or ROI page view | 10 | monthly, keep 75 percent |
| demo request | 15 | none |
| meeting accepted | 20 | none |
| case study or whitepaper download | 5 | weekly, keep 60 percent |
| webinar attended | 5 | weekly, keep 60 percent |
| email open | 0 | not counted |
| email click | 2 | weekly, keep 60 percent |
| email reply or inbound message | 10 | none |
| ad click | 1 | weekly, keep 50 percent |
| LinkedIn post engagement | 2 | weekly, keep 60 percent |
| intent spike from a third party | 5 | monthly, keep 80 percent |

Persistent signals (demo, meeting, reply) never decay. Use a trailing
90-day window; anything older drops out.

## Score bands

| Score | Stage | Action |
| --- | --- | --- |
| 0 to 25 | watchlist | nurture |
| 26 to 50 | aware | monitor |
| 51 to 100 | engaged | warm; incomplete buying group; tell the owner |
| 101 to 150 | hot | hand off if coverage is 50 percent or more |
| above 150 | in market | hand off |

Recycle rule: a score under 40 for 30 days returns the account to aware.

## Buying-group coverage

Roles a deal needs (define per product in `strategy/personas.md`):
economic buyer (every deal), technical buyer (complex products), end-user
champion, security or compliance (regulated buyers), procurement.

Coverage = roles seen / roles needed. 50 percent escalates, 75 percent
prioritises. Two named contacts per required role is the depth target in a
private repo; in a public one, count roles, not people.

## The hand-off gate

Both conditions, never one: score above 100 and coverage at or above 50
percent (at least two roles, or the economic buyer confirmed). A score of
120 from one person is not readiness.

Critical events bypass the score but not the coverage gate: demo request
from a qualified contact (24 hours), meeting request from the economic
buyer, RFP or proposal request (immediate), intent spike with two or more
roles engaged (48 hours), trial activation with a power user (7 days).

## Triggers to report every week

| Trigger | Action |
| --- | --- |
| score crosses 100 for the first time | review coverage; prepare the hand-off |
| critical event | hand-off within 24 hours |
| score down more than 50 percent in two weeks | at-risk line in the report |
| coverage reaches 50 percent | flag for the next hand-off batch |
| sales rejected the same account three times | joint review, not another hand-off |

## What the hand-off note carries

Company, tier, score with its breakdown, roles seen and coverage, the
critical event and its date, the content and activity history, whether the
CRM records exist, and a suggested first touch with discovery questions.
Sales accepts or rejects with a reason; 60 to 75 percent acceptance is
healthy, higher means the gate is too loose, lower means it is too tight.
