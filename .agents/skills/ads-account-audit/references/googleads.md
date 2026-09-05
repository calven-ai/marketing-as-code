# Google Ads: the resources an audit reads

Vendor id `google-ads`, source token `googleads`. The official read-only
MCP server (`googleads` in `.mcp.json`) exposes `search` (GAQL),
`list_accessible_customers` and `get_resource_metadata`; use the last one
when a field name below has moved. Check the server's tool list in the
session. The shapes of the weekly campaign pull are in the sibling
`ads-performance` skill's reference of the same name; the pull mechanics
live with `snapshot-pull`.

## One snapshot per resource, last 30 days

| Snapshot `<what>` | GAQL resource | Fields |
| --- | --- | --- |
| `campaigns` | `campaign` | `campaign.name`, `campaign.status`, `campaign.advertising_channel_type`, `campaign.bidding_strategy_type`, `campaign_budget.amount_micros`, `metrics.cost_micros`, `metrics.clicks`, `metrics.conversions`, `metrics.search_impression_share`, `metrics.search_budget_lost_impression_share`, `metrics.search_rank_lost_impression_share` |
| `search-terms` | `search_term_view` | `search_term_view.search_term`, `search_term_view.status`, `campaign.name`, `ad_group.name`, `metrics.cost_micros`, `metrics.clicks`, `metrics.conversions` |
| `keywords` | `keyword_view` | `ad_group_criterion.keyword.text`, `ad_group_criterion.keyword.match_type`, `ad_group_criterion.quality_info.quality_score`, `...creative_quality_score`, `...post_click_quality_score`, `...search_predicted_ctr`, `metrics.impressions`, `metrics.clicks`, `metrics.cost_micros`, `metrics.conversions` |
| `ads` | `ad_group_ad` | `ad_group_ad.ad.responsive_search_ad.headlines`, `...descriptions`, `ad_group_ad.ad_strength`, `ad_group_ad.status`, `ad_group.name`, `metrics.ctr`, `metrics.clicks` |
| `negatives` | `campaign_criterion` and `shared_set` | `campaign_criterion.negative`, `campaign_criterion.keyword.text`, `shared_set.name`, `shared_set.type` |
| `assets` | `campaign_asset` | `asset.type`, `campaign.name` (sitelinks, callouts, snippets, images) |
| `settings` | `campaign` | `campaign.network_settings.target_search_network`, `...target_content_network`, `campaign.geo_target_type_setting.positive_geo_target_type`, `campaign.ad_serving_optimization_status` |
| `conversions` | `conversion_action` | `conversion_action.name`, `conversion_action.primary_for_goal`, `conversion_action.status`, `conversion_action.click_through_lookback_window_days`, `conversion_action.attribution_model_settings.attribution_model`, `metrics.all_conversions` |
| `pmax-assets` | `asset_group` and `asset_group_asset` | asset group count, asset counts by type, `asset_group.ad_strength` |

Divide `cost_micros` by 1e6. Filter `segments.date DURING LAST_30_DAYS`.
The learning-phase state is not a GAQL field; read
`campaign.bidding_strategy_system_status` where present, else mark the
learning checks unknown.

## Manual exports when nothing is wired

Google Ads > Campaigns > Download; Keywords > Search terms > Download;
Keywords > Download (add Quality Score columns first); Ads & assets >
Download; Goals > Conversions (screenshot or export). Name each file
`data/ads/snapshots/YYYY-MM-DD-googleads-<what>.csv` with the `<what>`
values above.

## What the audit cannot see through the API

Consent Mode status, GA4 link health, server-side tagging and the tag's
firing on every page need a person in the UI or Tag Manager; score them
unknown and list them under "verify by hand".
