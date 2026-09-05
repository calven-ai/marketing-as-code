# Google Analytics 4 (source token `ga4`; category `web-analytics`)

Routes (from `integrations/catalog/web-analytics.json`): the local stdio
server `ga4` (`analytics-mcp`, Application Default Credentials; a service
account JSON at `GOOGLE_APPLICATION_CREDENTIALS` makes it headless), or a
stdlib script calling the Analytics Data API `runReport` (copy
`scripts/seo_snapshot.py`). `gcloud` does auth only. The server is
read-only by design.

## Calls per snapshot

Tools: `run_report`, `run_funnel_report`, `run_realtime_report`,
`get_account_summaries`, `get_property_details`, `list_google_ads_links`
(names from the vendor README; confirm in the session). Every report needs
the property id and a date range.

| `<what>` | Dimensions | Metrics |
| --- | --- | --- |
| traffic-by-source | `date, sessionSource, sessionMedium, sessionCampaignName` | `sessions, totalUsers, newUsers, conversions` (or `keyEvents:<event>` for one event) |
| conversions | `date, eventName, sessionSource, sessionMedium, sessionCampaignName` | `eventCount`, filtered to the events `data/ontology/events.md` marks as conversions |
| landing-pages | `date, landingPagePlusQueryString, sessionSource, sessionMedium` | `sessions, conversions` |
| funnel | `run_funnel_report` with the steps as event filters | `activeUsers` per step |

Use `sessionDefaultChannelGroup` as an extra dimension when the report
wants GA4's channel labels; keep raw source and medium in the snapshot so
`data/ontology/naming.md` can be applied later.

## Mapping to the snapshot columns

`source,medium,campaign` = the three session dimensions as returned
(`(direct)`, `(not set)` kept verbatim); `conversions` = the key-event
count for the ontology's primary conversion; `conversion_rate` computed in
the snapshot only when both inputs are in the same row.

## Limits and cost

- Data API quotas per property: on the order of 200,000 tokens per day and
  10 concurrent requests; a daily report over a quarter is one request per
  dimension set, so a snapshot costs a handful of tokens.
- `limit` is at most 100,000 rows per request; page with `offset`.
- Data for the last 24 to 48 hours is still being processed; a weekly
  pull ending yesterday is stable, ending today is not.
- Sampling and thresholding can hide rows on small properties; say so when
  a row count looks low.
- Cost: free within quota.

## Export fallback

Reports > the standard Traffic acquisition or an Explore report with the
dimensions above > Share > Download file (CSV), date range set. Drop at
`data/analytics/snapshots/YYYY-MM-DD-ga4-<what>.csv` and rename the
columns to the snapshot set.
