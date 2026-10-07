<!-- source: https://raw.githubusercontent.com/thatrebeccarae/claude-marketing/main/skills/google-analytics/REFERENCE.md | license: MIT | fetched: 2026-09-04 -->

# GA4 for the web analyst

Field names condensed from the source above; the mapping and the
mechanics are this repo's. The wired route is the official
`analytics-mcp` stdio server (catalog id `ga4`, source token `ga4`);
check the server's tool list in the session, and expect `run_report`,
`run_funnel_report`, `run_realtime_report`, `get_account_summaries` and
`get_property_details`. `snapshot-pull` does the pull; this file says
what to ask for.

## Property and dates

`get_account_summaries` lists the properties; the team's property id
belongs in `data/analytics/README.md`, not in a skill. Ask for full
days ending yesterday: GA4 finishes processing 24 to 48 hours after the
fact, so "today" is never complete. Check the response's sampling
metadata; a sampled report is a caveat in the report.

## The weekly reports

The snapshot names and columns are the ones in `references/posthog.md`,
so a GA4 week diffs against a PostHog week. GA4 aggregates before you see
the data, which changes three things:

- **Channel.** `sessionDefaultChannelGroup` is GA4's grouping, not the
  model in `data/ontology/naming.md`. Pull `sessionSource`,
  `sessionMedium` and `sessionCampaignName` and compute `channel` here by
  the model's rules in order, or build a custom channel group in GA4
  Admin with the same order and pull that.
- **Session class.** GA4 drops known bots and offers no per-session
  duration, so every row is `human` unless the property exports to
  BigQuery (then run the session fragment's rule there). An engine-fetch
  proxy: sessions whose source is an answer engine with
  `engagedSessions` 0 and `averageSessionDuration` under 5 s, labelled a
  proxy in Data caveats.
- **No scroll per session.** `scroll_p50` and the tracking-quality
  coverage columns stay empty unless the property sends them as events.

| Snapshot | Dimensions | Metrics |
| --- | --- | --- |
| traffic-by-source | `sessionSource`, `sessionMedium` | `sessions`, `engagedSessions`, `screenPageViews`, `averageSessionDuration`, `eventCount` filtered to the CTA and conversion events |
| landing-pages | `landingPage` | `sessions`, `engagedSessions`, `bounceRate`, `averageSessionDuration`, `screenPageViewsPerSession`, `eventCount` of the CTA and conversion events |
| page-by-source | `landingPage`, `sessionSource`, `sessionMedium` (7 and 28 days, two calls) | `sessions`, `engagedSessions` |
| conversions | `eventName`, `pagePath`, `sessionSource`, `sessionMedium` | `eventCount`, `sessions` |
| site-funnel | none (one row) | `sessions`, `engagedSessions`; decision page, CTA and conversion via `run_funnel_report` |

Filter conversion counts to the event names in
`data/ontology/events.md`; GA4's `conversions` metric counts whatever the
property marks as a key event, which may not be the ontology's
definition. GA4 counts events, not sessions with the event: name that
difference in Data caveats, or use `run_funnel_report` for session
counts.

## Monthly additions

- pages: `pagePath` with `screenPageViews`, `totalUsers`,
  `userEngagementDuration` (divide by users for the average),
  `conversions`.
- utm-campaigns: `sessionSource`, `sessionMedium`,
  `sessionCampaignName`, `sessionManualAdContent` with `sessions`. The
  `conforms` and `reason` columns are computed here against
  `data/ontology/naming.md`, not pulled.

## Cost and limits

The Data API is free within Google's quota (tokens per property per
hour; a weekly run uses a fraction). Report the number of `run_report`
calls; six for a weekly run, eight for a monthly one.

## Without the MCP

Reports > Acquisition > Traffic acquisition (by session source /
medium), Engagement > Events, Engagement > Landing page; Share > Download
CSV; drop into `data/analytics/snapshots/` with the names in
`references/posthog.md`, and rename the columns to match.
