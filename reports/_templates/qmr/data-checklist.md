# QMR data checklist: [year]-q[n]

Every snapshot this QMR needs. The `qmr` skill works down this list: pulls
what integrations can provide, and turns the rest into one batched export
request. Check items off with the actual snapshot path. Delete rows that
don't apply to your stack; add rows for what your QMR additionally tracks.

Snapshot naming: `YYYY-MM-DD-<source>-<what>.csv`, dated the day of the
pull, saved in the listed folder.

## CRM (`data/crm/snapshots/`)

- [ ] **Pipeline by stage**: deals with stage, amount, created/closed dates
      for the quarter. Via HubSpot MCP, or export: CRM → Deals → filter
      created/closed in quarter → export CSV.
      Expected: `<date>-hubspot-pipeline.csv`
- [ ] **New contacts / signups**: contacts created in the quarter with
      source and lifecycle stage.
      Expected: `<date>-hubspot-new-contacts.csv`
- [ ] **MQLs/SQLs for the quarter**: per the definitions in
      `data/ontology/metrics.md` (if computable from the two exports above,
      skip this row).
- [ ] **Email performance**: sends, opens, clicks, unsubscribes per
      campaign. Expected: `<date>-hubspot-email-performance.csv`
- [ ] **Event attendees**: one file per event held this quarter (webinars,
      conferences). Expected: `<date>-<source>-<event>-attendees.csv`

## Analytics (`data/analytics/snapshots/`)

- [ ] **Traffic by source/channel** for the quarter, weekly or monthly
      granularity. Via PostHog/GA4 MCP, or export from the analytics UI.
      Expected: `<date>-<posthog|ga4>-traffic-by-source.csv`
- [ ] **Conversions / key events**: the events named in
      `data/ontology/events.md`, counts for the quarter.
      Expected: `<date>-<source>-conversions.csv`
- [ ] **Top content**: pageviews for `content/` pieces published this and
      last quarter. Expected: `<date>-<source>-top-content.csv`

## SEO (`data/seo/snapshots/`)

- [ ] **Ranking snapshot**: current rank for every keyword in
      `data/seo/keywords.csv`. Via DataForSEO MCP.
      Expected: `<date>-dataforseo-rankings.csv`
- [ ] The comparable snapshot from last quarter's QMR exists (for deltas). If
      not, note "baseline quarter" in the report.

## From the repo itself (no export needed: the skill computes these)

- [ ] Content shipped: `content/` frontmatter, `status: published` in
      quarter
- [ ] Projects closed / in flight: `projects/*/status.md` + `_archive/`
- [ ] Decisions made: `memory/decision-log.md` entries in quarter
