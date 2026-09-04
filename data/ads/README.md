# data/ads/

Paid campaign pulls from the ad platforms (Google Ads, LinkedIn Ads, or
whatever the team buys on), plus the finance export that budget pacing
reconciles spend against. Fed by the `ads` integration category
(`integrations/catalog/ads.json`). See `integrations/README.md`.

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable, named per
`data/README.md`. Typical:

- `2026-08-31-googleads-campaigns.csv`: spend, clicks and conversions by
  campaign
- `2026-08-31-linkedinads-campaigns.csv`
- `2026-08-31-finance-invoices.csv`: the finance export (`finance` is the
  source token for it) that `budget-pacing` reconciles platform spend
  against

The `ads-performance`, `budget-pacing` and `ads-account-audit` skills write
here. `attribution-analysis` and `qmr` read.

## Rules

- Load `data/ontology/` first. A conversion means what
  `data/ontology/events.md` says, and campaign names follow
  `data/ontology/naming.md`.
- The PII rule from `data/`: campaign-level aggregates only. Audience lists
  and per-person click data never land here.
