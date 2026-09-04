# Google Ads: what to pull and how it maps

Vendor id `google-ads`, source token `googleads` (from
`integrations/catalog/ads.json`). The default route is Google's official
read-only MCP server (`googleads` in `.mcp.json`): tools `search` (GAQL),
`list_accessible_customers`, and `get_resource_metadata`. It cannot write,
so nothing in it needs denying. Check the server's tool list in the session
before calling; names can move between commits.

## The campaign report

One `search` call per period against the `campaign` resource:

```
SELECT campaign.id, campaign.name, campaign.status,
       campaign.advertising_channel_type,
       metrics.cost_micros, metrics.impressions, metrics.clicks,
       metrics.conversions, metrics.conversions_value,
       metrics.search_impression_share,
       metrics.search_budget_lost_impression_share
FROM campaign
WHERE segments.date BETWEEN '2026-08-31' AND '2026-09-06'
  AND campaign.status != 'REMOVED'
```

`segments.date` in the SELECT gives one row per day; leave it out for a
period total. Pass the customer id the team uses (`list_accessible_customers`
lists them); a manager account needs `login-customer-id` set in the server
environment.

## Column mapping

| Snapshot column | GAQL field | Note |
| --- | --- | --- |
| `campaign` | `campaign.name` | must carry the slug from `data/ontology/naming.md` |
| `platform` | constant `googleads` | |
| `period_start`, `period_end` | the WHERE dates | |
| `spend` | `metrics.cost_micros / 1e6` | account currency |
| `impressions` | `metrics.impressions` | |
| `clicks` | `metrics.clicks` | |
| `conversions` | `metrics.conversions` | the account's primary actions only |
| `cost_per_conversion` | `spend / conversions` | blank when conversions is 0 |
| `currency` | `customer.currency_code` | one extra `search` on `customer` |

Only primary conversion actions count in `metrics.conversions`; secondary
ones sit in `metrics.all_conversions`. Which action is "a lead" is
`data/ontology/events.md`, and the conversion window is the account's, so
name it in the report's caveats.

## Other useful resources

- `search_term_view` (search terms, for wasted spend): `search_term_view.search_term`,
  `metrics.cost_micros`, `metrics.conversions`, `campaign.name`.
- `ad_group_criterion` with `ad_group_criterion.quality_info.quality_score`
  for keyword quality scores.
- `campaign_budget` for `campaign_budget.amount_micros` (daily budget) in
  pacing.

## Manual export

Google Ads > Campaigns > the date range > Download > CSV. Keep the columns
Campaign, Cost, Impr., Clicks, Conversions, and rename them to the
snapshot columns above. Drop the file at
`data/ads/snapshots/YYYY-MM-DD-googleads-campaigns.csv`.

## Limits

The API is quota-based (basic access is 15,000 operations a day), not
billed; a weekly pull is a handful of operations. Metrics for the current
day lag by a few hours; pull yesterday as the last full day. Pull
mechanics beyond this live with the `snapshot-pull` skill.
