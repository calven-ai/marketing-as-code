# PostHog (source token `posthog`; category `web-analytics`)

Routes (from `integrations/catalog/web-analytics.json`): the remote MCP
server `posthog` with `?readonly=true` in the URL (OAuth for a person, a
personal API key `POSTHOG_API_KEY` with the "MCP Server" preset for
unattended runs), or `posthog-cli api` in a workflow step. Run
`posthog-cli api --agent-help` before the first CLI call and follow what it
prints. Keep the read-only switch on; this skill only reads.

## Calls per snapshot

The server exposes insight and HogQL query tools; check the tool list in
the session. HogQL is the contract, and the same queries run through the
CLI (`posthog-cli api` against the query endpoint).

The weekly web set (`traffic-by-source`, `landing-pages`,
`page-by-source`, `engine-fetches`, `conversions`, `site-funnel`,
`tracking-quality`) comes from `scripts/web_snapshot.py`: run it with the
key, or `--print-sql` for the MCP and `--from-results` to save. Its
queries, columns and the session-entry rule (never the per-event
`$referring_domain`) are in
`.agents/skills/web-analyst/references/posthog.md`.

| `<what>` | HogQL |
| --- | --- |
| funnel | a funnel insight over the ontology's steps, or `funnel` via the insights tool; one row per step |
| other | from the `sessions` table for anything per session (`$entry_utm_source`, `$entry_referring_domain`, `$entry_pathname`), from `events` per event; always a date window and a `LIMIT` |

## Limits and cost

- Query API calls are rate-limited per key (on the order of 240 per
  minute for analytics endpoints) and a single HogQL query is capped in
  execution time; group by day rather than pulling raw events.
- Results are limited per query (thousands of rows); add a date filter
  and page by date range for long periods.
- Personal API keys are scoped by the preset; a query that fails with 403
  needs the `query:read` scope, not a wider key.
- Cost: query usage counts toward the plan's data allowance; a daily
  aggregate over a quarter is small.

## Export fallback

Open the insight (Trends, grouped by the properties above) > Export > CSV,
or Data management > Export. Drop at
`data/analytics/snapshots/YYYY-MM-DD-posthog-<what>.csv` and rename the
columns to the snapshot set.
