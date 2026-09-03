# data/analytics/

Website and product analytics pulls (GA4, PostHog, or whatever the team
tracks with). See `integrations/README.md`.

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable. Typical:

- `2026-08-31-posthog-traffic-by-source.csv`
- `2026-08-31-ga4-conversions.csv`
- `2026-09-30-posthog-signup-funnel.csv`

Keep columns stable per `<what>` so snapshots diff cleanly across months.

## For agents

- Interpret event and conversion names through `data/ontology/events.md`.
  Never assume what `signed_up` means.
- Analyses go to `reports/recurring/analytics/` (or `reports/adhoc/` for
  one-off questions), not here.
