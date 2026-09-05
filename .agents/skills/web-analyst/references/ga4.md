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

## The three weekly reports

| Snapshot | Dimensions | Metrics |
| --- | --- | --- |
| traffic-by-source | `sessionSource`, `sessionMedium`, `sessionDefaultChannelGroup` | `sessions`, `totalUsers`, `newUsers`, `engagedSessions`, `conversions` |
| conversions | `eventName`, `sessionDefaultChannelGroup` | `eventCount`, `totalUsers` |
| landing-pages | `landingPage` | `sessions`, `engagedSessions`, `conversions` |

Filter the conversions report to the event names listed in
`data/ontology/events.md`; GA4's `conversions` metric counts whatever
the property marks as a key event, which may not be the ontology's
definition.

## Monthly additions

- pages: `pagePath` with `screenPageViews`, `totalUsers`,
  `userEngagementDuration` (divide by users for the average),
  `conversions`.
- utm-campaigns: `sessionSource`, `sessionMedium`,
  `sessionCampaignName`, `sessionManualAdContent` with `sessions`. The
  `conforms` and `reason` columns are computed here against
  `data/ontology/naming.md`, not pulled.

Other dimensions the source lists that you may need: `firstUserSource`
for first-touch questions, `pageTitle`, `exitPage`, `country`,
`deviceCategory`, `date` for a daily series. Metrics: `activeUsers`,
`sessionsPerUser`, `averageSessionDuration`, `bounceRate`,
`engagementRate`, `screenPageViewsPerSession`.

## Field to column mapping

| Column | GA4 field |
| --- | --- |
| `source`, `medium` | `sessionSource`, `sessionMedium` |
| `channel_group` | `sessionDefaultChannelGroup` |
| `sessions`, `users`, `new_users` | `sessions`, `totalUsers`, `newUsers` |
| `engaged_sessions` | `engagedSessions` |
| `conversions` | `eventCount` of the ontology's events, or `conversions` when they agree |
| `event`, `count` | `eventName`, `eventCount` |
| `landing_page` | `landingPage` |
| `page_path`, `views` | `pagePath`, `screenPageViews` |

## Cost and limits

The Data API is free within Google's quota (tokens per property per
hour; a weekly run uses a fraction). Report the number of `run_report`
calls; three for a weekly run, five for a monthly one.

## Without the MCP

Reports > Acquisition > Traffic acquisition (by session source /
medium), Engagement > Conversions (by event), Engagement > Landing page;
Share > Download CSV; drop into `data/analytics/snapshots/` with the
names in the skill, and rename the columns to the ones above.
