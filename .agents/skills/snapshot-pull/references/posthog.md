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

| `<what>` | HogQL |
| --- | --- |
| traffic-by-source | `SELECT toDate(timestamp) AS date, properties.$referring_domain AS source, properties.utm_medium AS medium, properties.utm_campaign AS campaign, count(DISTINCT $session_id) AS sessions, count(DISTINCT person_id) AS users FROM events WHERE event = '$pageview' AND timestamp >= '<start>' AND timestamp < '<end>' GROUP BY 1,2,3,4` |
| conversions | `SELECT toDate(timestamp) AS date, event, properties.utm_source, properties.utm_medium, properties.utm_campaign, count() FROM events WHERE event IN (<ontology conversion events>) AND timestamp >= '<start>' GROUP BY 1,2,3,4,5` |
| landing-pages | `$pageview` events where `properties.$entry_pathname` (or the session's first pathname) is the page, grouped by date, page, source, medium |
| funnel | a funnel insight over the ontology's steps, or `funnel` via the insights tool; one row per step |

Session-level source needs the `sessions` table on newer projects
(`SELECT $entry_referring_domain, $entry_utm_source ... FROM sessions`);
use it when the project has it, the events table otherwise, and say which.

## Mapping to the snapshot columns

`source` = `utm_source` when set, else the referring domain; `medium` and
`campaign` = the UTM properties (empty, not `(not set)`); `users` = distinct
persons; `new_users` = persons whose first event is in the row's day
(`person.created_at`); `conversions` = the count of the ontology's primary
conversion event in the same source group.

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
