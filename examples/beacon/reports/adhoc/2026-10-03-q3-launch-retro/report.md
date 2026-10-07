# Q3 launch retro: audience segments

- **Date:** 2026-10-03 · **Prepared by:** `program-retro` with Ana Ruiz
- **Question:** "How did the Q3 launch do, and what do we change for the next one?"

## Answer

A close miss: 37 launch-attributed MQLs against a goal of 40, out of 118
in the quarter. The comparison page was the best asset of the launch: 10
MQLs in its first nine days, 6 from people who found it and 4 from paid
social. Paid social before it existed made 2 MQLs for 6,200 USD; after,
4 for 1,800. The next launch ships its comparison page before any paid
traffic.

This is one week after the campaign closed, so pipeline is immature:
launch SQLs and deal amounts are re-checked on 2026-11-21.

## Evidence

**Tier 1, activity.** The launch post drew 1,240 sessions in September and
ranks 4 for "customer communication during outage". The LinkedIn post
reached 18,400 impressions with 212 reactions and 31 comments. The
announcement email: 4,820 delivered, 41.2 percent opened, 6.3 percent
clicked.

**Tier 2, outcomes.** Launch MQLs by first-touch asset, 2026-07-07 to
2026-09-30:

| Asset | Landing page | Sessions | Signups | MQLs |
| --- | --- | --- | --- | --- |
| Launch post | /blog/what-customers-want-during-an-outage | 1,470 | 41 | 9 |
| Announcement email | /product/audience-segments | 380 | 21 | 8 |
| LinkedIn post | /blog/what-customers-want-during-an-outage | 290 | 7 | 3 |
| Product page, unpaid | /product/audience-segments | 940 | 24 | 5 |
| Comparison page, unpaid | /compare/northstar | 270 | 9 | 6 |
| Paid phase 1 | /product/audience-segments | 1,100 | 9 | 2 |
| Paid phase 2 | /compare/northstar | 420 | 14 | 4 |
| **Total** | | **4,870** | **125** | **37** |

**Tier 3, cost.** Paid social is the only line with spend:

| Phase | Dates | Spend | Signup rate | Cost per MQL |
| --- | --- | --- | --- | --- |
| 1, product page | 2026-07-21 → 2026-08-20 | 6,200 USD | 0.8% | 3,100 USD |
| 2, comparison page | 2026-09-23 → 2026-09-30 | 1,800 USD | 3.3% | 450 USD |

Same audience (Tier 1 accounts), a different landing
page. 2,000 USD of the 10,000 budget was left unspent.

## What worked, what did not

- **Worked:** the comparison page. A visitor weighing us against Northstar
  had something to read. It ranks 9 for "northstar alternative" after
  eight days.
- **Worked:** the email to the existing list, 8 MQLs from one send.
- **Did not:** phase 1 ran entirely before the feature shipped on
  2026-08-25 (it was due 2026-08-11), so it sent buyers to a page about a
  feature they could not try. Inference, from the dates; forty percent of
  the spend went to visits under ten seconds
  (`projects/q3-launch/paid-social/status.md`).
- **Did not:** the slip itself. On 2026-09-01 the launch had 14 MQLs; 23
  of the 37 came in September.

## Keep, change, stop

- **Keep:** a problem-first post as the launch's main asset; one email to
  the list.
- **Change:** the comparison page ships before any paid traffic, and paid
  lands only on it (logged 2026-10-03).
- **Stop:** starting paid spend on a date the feature might miss; tie it
  to the ship date instead.

Proposed playbook rules for `memory/knowledge/launch-playbook.md`: the
two lines under Change and Stop, each citing this retro.

## Caveats and gaps

- Attribution is first touch (`data/ontology/funnel.md`); a buyer who read
  the post and then clicked an ad counts for the post.
- Phase 2 ran eight days. Four MQLs is a small number; the cost gap is
  large enough to act on, not to forecast from.
- Launch SQLs and pipeline: not computed yet; re-check 2026-11-21.

## Data used

| Used for | Snapshot |
| --- | --- |
| Launch MQLs, sessions and signups by asset | `data/crm/snapshots/2026-09-30-repo-launch-attribution.csv` |
| Quarter MQLs | `data/crm/snapshots/2026-09-30-hubspot-lifecycle-by-quarter.csv` |
| Paid spend and dates | `data/ads/snapshots/2026-09-30-linkedinads-campaigns.csv` |
| Email | `data/email/snapshots/2026-09-30-hubspot-sends.csv` |
| LinkedIn post | `data/social/snapshots/2026-09-30-linkedin-posts.csv` |
| Launch post sessions | `data/analytics/snapshots/2026-09-30-posthog-top-content.csv` |
| Rankings | `data/seo/snapshots/2026-09-30-dataforseo-rankings.csv` |
