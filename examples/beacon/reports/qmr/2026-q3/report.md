# Quarterly Marketing Review: 2026 Q3

- **Prepared:** 2026-10-05 · **Owner:** Ana Ruiz
- **Status:** ready for review

> How to read this: every number traces to a snapshot listed in **Data
> used**. Claims marked *[confirm]* are drafted from the data and await the
> team's judgment. Gaps are stated as gaps.

## Headline: the quarter in five numbers

| Metric | Target | Actual | vs last Q | Verdict |
| --- | --- | --- | --- | --- |
| MQLs | 110 | 118 | +23% | hit |
| Open pipeline | 450k | 501k | +22% | hit |
| Signups | 900 | 910 | +17% | hit |
| Sessions | 34,000 | 36,800 | +17% | hit |
| Launch-attributed MQLs | 40 | 37 | new | miss |

Every quarterly target was hit; the launch missed by three MQLs. Most of
the gap is a feature that shipped two weeks late and a month of paid
social sent to a product page for a feature that was not live yet.

## Funnel

| Stage | This Q | Last Q | Conversion from prior stage |
| --- | --- | --- | --- |
| Visitors | 36,800 | 31,400 | |
| Signups | 910 | 779 | 2.5% |
| Activated | 512 | 430 | 56% |
| MQLs | 118 | 96 | 23% |
| SQLs | 49 | 41 | 42% |
| Customers | 15 | 12 | 31% |

Conversion held at every stage; the growth is volume. Signups rose each
month (280, 297, 333), and September carried the launch. SQL conversion
went from 43 to 42 percent, one deal at this size, not a trend.

## Channels

| Source | Sessions | Signups | Signup rate | Q2 sessions |
| --- | --- | --- | --- | --- |
| Organic | 16,900 | 470 | 2.8% | 14,200 |
| Direct | 8,300 | 196 | 2.4% | 7,900 |
| Referral | 4,600 | 104 | 2.3% | 4,100 |
| Social | 3,900 | 62 | 1.6% | 2,600 |
| Email | 3,100 | 78 | 2.5% | 2,600 |

Organic is 46 percent of sessions and half of signups. Social converted
worst again; it includes LinkedIn Ads (the roll-up in
`data/ontology/naming.md`). Paid phase 1 sent 1,100 sessions to the
product page for 9 signups and 2 MQLs at 6,200 USD; phase 2 sent 420 to
the comparison page for 14 signups and 4 MQLs at 1,800 USD.

The launch announcement reached 4,820 inboxes: 41.2 percent opened, 6.3
percent clicked, 21 signups.

Rankings against 2026-06-30: "status page software" 11 → 8, "incident
communication template" 4 → 3, "status page for saas" 17 → 12. New this
quarter: "customer communication during outage" at 4 and "northstar
alternative" at 9, eight days after the comparison page went live.

AI answers, first check: of 12 buyer prompts, Beacon is named in 3,
Northstar in 9, Pagewise in 6. Baseline quarter, no delta.

Reviews: 4.7 on 34 reviews, 9 new this quarter. Northstar 4.3 on 412,
Pagewise 4.6 on 131.

## Content shipped

Seven pieces published against a target of seven. The four launch pieces:

| Piece | Channel | Published | Early signal |
| --- | --- | --- | --- |
| What customers want during an outage | blog | 2026-08-28 | 1,240 sessions in September, ranks 4, 9 launch MQLs |
| LinkedIn launch post | linkedin | 2026-09-02 | 18,400 impressions, 212 reactions, 31 comments, 3 launch MQLs |
| Audience segments announcement | email | 2026-09-08 | 21 signups, 8 launch MQLs |
| Beacon vs Northstar | web | 2026-09-22 | 690 sessions in 9 days, ranks 9, 10 launch MQLs |

The other three are not included in this example.

## Projects and campaigns

- **Q3 launch** (`projects/q3-launch/campaign.md`): 40 launch MQLs → 37.
  Done 2026-10-03. Retro in
  `reports/adhoc/2026-10-03-q3-launch-retro/report.md`, lesson logged
  2026-10-03.
- **Customer stories** (`projects/customer-stories/brief.md`): in flight,
  the Fernhill case study due 2026-11-05.
- **Q4 pipeline** (`projects/q4-pipeline/campaign.md`): kicked off
  2026-10-01.

Decided this quarter: paid social paused (2026-08-20) and resumed on the
comparison page only (2026-09-23); a per-workspace plan for teams over
ten seats from 2026-10-01 (2026-09-15).

## Wins, misses, lessons

- **Win:** the comparison page made 10 launch MQLs in nine days, more than
  any other launch asset over the whole window. *[confirm]*
- **Miss:** 37 launch MQLs against 40. Phase 1 paid social cost 3,100 USD
  per MQL; phase 2 cost 450.
- **Lesson → change:** the comparison page ships before any paid traffic,
  and Q4 retargeting lands on it (decision log, 2026-10-03).

## Decisions needed

| Question | Context | Owner |
| --- | --- | --- |
| Archive `projects/q3-launch/` | Waits for this QMR to be final | Ana Ruiz |
| A Pagewise comparison page in Q4? | Pagewise is named in 6 of 12 AI answers; no page answers "pagewise alternative" | Ana Ruiz |

## Next quarter

Decided on 2026-10-01: 130 MQLs, 1,000 signups and 550k open pipeline at
quarter end, carried by the webinar with Fernhill on 2026-11-12 and Tier 1
ABM on 30 accounts. Logged in the decision log.

## Data used

| Number(s) | Snapshot |
| --- | --- |
| Funnel counts, MQLs | `data/crm/snapshots/2026-09-30-hubspot-lifecycle-by-quarter.csv` |
| Q2 funnel counts | `data/crm/snapshots/2026-06-30-hubspot-lifecycle.csv` |
| Open pipeline | `data/crm/snapshots/2026-09-30-hubspot-pipeline.csv` |
| Launch MQLs by asset | `data/crm/snapshots/2026-09-30-repo-launch-attribution.csv` |
| Sessions, signups by source | `data/analytics/snapshots/2026-09-30-posthog-traffic-by-source.csv` |
| Q2 sessions by source | `data/analytics/snapshots/2026-06-30-posthog-traffic-by-source.csv` |
| Signups by month | `data/analytics/snapshots/2026-09-30-posthog-signups-by-month.csv` |
| Content sessions | `data/analytics/snapshots/2026-09-30-posthog-top-content.csv` |
| Paid spend | `data/ads/snapshots/2026-09-30-linkedinads-campaigns.csv` |
| Email | `data/email/snapshots/2026-09-30-hubspot-sends.csv` |
| LinkedIn post | `data/social/snapshots/2026-09-30-linkedin-posts.csv` |
| Rankings | `data/seo/snapshots/2026-09-30-dataforseo-rankings.csv`, `data/seo/snapshots/2026-06-30-dataforseo-rankings.csv` |
| AI answers | `data/seo/snapshots/2026-09-30-dataforseo-aeo-results.csv` |
| Reviews | `data/reviews/snapshots/2026-09-30-g2-ratings.csv` |

Gaps: launch-attributed SQLs and pipeline are not computed; the launch's
deals are too young. The retro re-checks them on 2026-11-21.
