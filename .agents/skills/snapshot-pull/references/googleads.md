# Google Ads (source token `googleads`; category `ads`)

Routes (from `integrations/catalog/ads.json`): the local stdio server
`googleads` (`google-ads-mcp`, pinned to a commit; Application Default
Credentials plus `GOOGLE_ADS_DEVELOPER_TOKEN`; a service-account JSON makes
it headless), or a stdlib script posting GAQL to
`googleads.googleapis.com/v19/customers/<id>/googleAds:searchStream` (copy
`scripts/seo_snapshot.py`). The server is read-only by design: `search`
(GAQL), `list_accessible_customers`, `get_resource_metadata`.

## Calls per snapshot

Start with `list_accessible_customers` when the customer id is not in the
request; a manager account needs `login-customer-id` set to the manager
and the query run against the child account.

| `<what>` | GAQL |
| --- | --- |
| campaigns | `SELECT segments.date, campaign.name, campaign.status, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions, metrics.conversions_value FROM campaign WHERE segments.date BETWEEN '<start>' AND '<end>' ORDER BY segments.date` |
| campaigns by network | add `segments.ad_network_type` to the select and group in the report, not in the snapshot |
| keywords (ad hoc) | `SELECT segments.date, ad_group_criterion.keyword.text, metrics.clicks, metrics.cost_micros, metrics.conversions FROM keyword_view WHERE segments.date BETWEEN ...` saved as `<what>` = keywords |

`get_resource_metadata` lists selectable fields when a metric name is in
doubt; do not guess field names.

## Mapping to the snapshot columns

`cost` = `metrics.cost_micros / 1,000,000` in the account currency;
`conversions` = `metrics.conversions` (the account's conversion actions;
which ones count is `data/ontology/events.md`); `conversion_value` =
`metrics.conversions_value`; `status` = `campaign.status` as returned
(ENABLED, PAUSED, REMOVED). Aggregates only; no audience or per-person
rows ever land in `data/ads/`.

## Limits and cost

- `searchStream` returns the whole result without paging; `search` pages
  10,000 rows at a time. A campaign-by-day query over a quarter is one
  call.
- Basic API access allows on the order of 15,000 operations per day; a
  weekly snapshot is a handful.
- Data for today is partial; end the range yesterday.
- Cost: the API is free; the developer token needs approval once.

## Export fallback

Campaigns > the date range > segment by Day > Download (CSV). Drop at
`data/ads/snapshots/YYYY-MM-DD-googleads-campaigns.csv`, convert cost to
plain currency units, and rename the columns to the snapshot set.
