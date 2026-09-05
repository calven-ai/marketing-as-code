# data/social/

Organic social stats, listening pulls and community threads. Fed by three
integration categories: `social` (the team's own accounts),
`scraping-search` (mentions across the open web) and `community` (the forum
or chat the team hosts). See `integrations/README.md`.

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable, named per
`data/README.md`. Typical:

- `2026-08-31-linkedin-posts.csv`: impressions, engagement and clicks per
  post
- `2026-08-31-apify-mentions.csv`: scraped mentions of the brand and its
  competitors
- `2026-08-31-discourse-threads.csv`: community threads, reply counts and
  the questions nobody answered

The `social-performance`, `social-listening` and `community-digest` skills
write here.

## Rules

- Load `data/ontology/` first. Engagement is not a lead;
  `data/ontology/funnel.md` says what is.
- The PII rule from `data/`: mentions and threads name people. Handles,
  profile URLs and quoted text from individuals stay out of a public copy.
