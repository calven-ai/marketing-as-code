# LinkedIn Ads: the exports an audit reads

Vendor id `linkedin-ads`, source token `linkedinads`. No official MCP
server exists; the catalog's default route is the Campaign Manager
export, and a community server, if wired, is used read-only after checking
its tool list in the session. Pull mechanics live with `snapshot-pull`.

## Exports, last 30 days

| Snapshot `<what>` | Where in Campaign Manager | Columns to keep |
| --- | --- | --- |
| `campaigns` | Campaigns > Export (campaign level) | Campaign Name, Campaign Group, Objective, Status, Daily Budget, Bid Type, Total Spent, Impressions, Clicks, Average CPM, Average CPC, Conversions, Leads, Frequency if shown |
| `ads` | Ads > Export | Ad Name, Campaign Name, Format, Created date, Impressions, Clicks, CTR, Conversions |
| `audiences` | Plan > Audiences (Matched Audiences) | Audience Name, Type (website, list, engagement), Size, Status, Created date |
| `demographics` | Campaign > Demographics > Export | Campaign Name, Job Title or Function, Seniority, Company Size, Impressions, Clicks, Conversions |
| `settings` | per campaign, by hand | Audience Expansion on or off, LinkedIn Audience Network on or off, audience size, forecast reach |

Name each `data/ads/snapshots/YYYY-MM-DD-linkedinads-<what>.csv`. The
settings snapshot is a small CSV a person fills from the campaign setup
screen (`campaign,audience_expansion,audience_network,audience_size,active_ads`).

## The API, if a script exists

`adAnalytics` with `pivot=CAMPAIGN` for the campaigns table and
`pivot=CREATIVE` for ads; `adCampaigns` for status, budget, bid type and
`audienceExpansionEnabled` and `offsiteDeliveryEnabled` (the two settings
the audit cares most about); `adSegments` for matched audiences. Spend is
`costInLocalCurrency`. Partner approval is needed before any token works.

## What only a person can check

Insight Tag installation and the conversion events it feeds, the
attribution window per conversion, and whether lead-form leads were ever
reconciled against the CRM. Ask, and score unknown until answered.
