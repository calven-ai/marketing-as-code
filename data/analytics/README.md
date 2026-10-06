# data/analytics/

Website and product analytics pulls (GA4, PostHog, or whatever the team
tracks with). See `integrations/README.md`.

## The site

Filled by the team; the `web-analyst` role reads it before every pull.

| Setting | Value |
| --- | --- |
| Site domain (links between its pages count as Direct) | [example.com] |
| Analytics project or property id (not a secret) | [ ] |
| CTA event (the click that hands a visitor to the conversion) | [`cta_clicked`, per `data/ontology/events.md`] |
| Conversion event, and the system that records it | [ ] |
| Decision page | [/pricing] |

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable. The weekly web set
is `traffic-by-source`, `landing-pages`, `page-by-source`,
`engine-fetches`, `conversions`, `site-funnel` and `tracking-quality`;
their columns are in
`.agents/skills/web-analyst/references/posthog.md`, and
`scripts/web_snapshot.py` writes all seven from PostHog.

Keep columns stable per `<what>` so snapshots diff cleanly across months.

## For agents

- Interpret event and conversion names through `data/ontology/events.md`.
  Never assume what `signed_up` means.
- Channels and sources follow `data/ontology/naming.md`; sessions, never
  visitors; bots never in a rate (`data/ontology/metrics.md`).
- Analyses go to `reports/recurring/analytics/`, or `reports/adhoc/` for
  one-off questions. Never here.
