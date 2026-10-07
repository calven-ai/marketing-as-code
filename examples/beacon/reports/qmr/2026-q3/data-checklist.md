# QMR data checklist: 2026-q3

Every snapshot this QMR needed, checked off with its path.

## CRM (`data/crm/snapshots/`)

- [x] **Pipeline by stage**: `2026-09-30-hubspot-pipeline.csv`
- [x] **Lifecycle counts**: `2026-09-30-hubspot-lifecycle-by-quarter.csv`
      (a quarter column replaces Q2's `count_q2`, so the next pull keeps
      the same columns)
- [x] **Launch-attributed MQLs**: `2026-09-30-repo-launch-attribution.csv`,
      computed in-repo from HubSpot `first_touch_campaign` and PostHog
      first pageviews

## Email (`data/email/snapshots/`)

- [x] **Email performance**: `2026-09-30-hubspot-sends.csv` (the launch
      announcement; the monthly product update is a product send, left out)

## Ads (`data/ads/snapshots/`)

- [x] **LinkedIn campaigns**: `2026-09-30-linkedinads-campaigns.csv`

## Analytics (`data/analytics/snapshots/`)

- [x] **Traffic by source**: `2026-09-30-posthog-traffic-by-source.csv`
- [x] **Signups by month**: `2026-09-30-posthog-signups-by-month.csv`
- [x] **Top content**: `2026-09-30-posthog-top-content.csv` (September)

## SEO (`data/seo/snapshots/`)

- [x] **Ranking snapshot**: `2026-09-30-dataforseo-rankings.csv`
- [x] Comparable snapshot from Q2: `2026-06-30-dataforseo-rankings.csv`
      (three keywords; the other seven have no Q2 baseline)
- [x] **AI answers**: `2026-09-30-dataforseo-aeo-results.csv` (first run,
      baseline quarter)

## Social and reviews

- [x] **LinkedIn posts**: `data/social/snapshots/2026-09-30-linkedin-posts.csv`
- [x] **Review ratings**: `data/reviews/snapshots/2026-09-30-g2-ratings.csv`

## From the repo itself

- [x] Content shipped: `content/` frontmatter, published in Q3
- [x] Projects closed / in flight: `projects/*/status.md`
- [x] Decisions made: `memory/decision-log.md`, 2026-07-03 to 2026-09-23
