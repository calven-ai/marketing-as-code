# data/reviews/

Review-site, NPS and survey exports (G2, Capterra, Typeform, or whatever the
team collects feedback with). Fed by the `surveys-reviews` integration
category. See `integrations/README.md`.

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable, named per
`data/README.md`. Typical:

- `2026-08-31-g2-reviews.csv`: reviews with rating, date, role and text
- `2026-08-31-typeform-nps.csv`: NPS responses with score and verbatim

The `review-monitor` skill writes here. `voice-of-customer` and
`advocacy-program` read.

## Rules

- Load `data/ontology/` first. A promoter is not a customer advocate until
  `data/ontology/metrics.md` says what one is.
- The PII rule from `data/`: a review or NPS response names a person. Keep
  reviewer names and emails out of a public copy, and quote verbatims by
  role and company only.
