# LinkedIn Ads: what to pull and how it maps

Vendor id `linkedin-ads`, source token `linkedinads` (from
`integrations/catalog/ads.json`). LinkedIn has no official MCP server. The
catalog's default route is the manual export from Campaign Manager; the
community server `mcp-linkedin-ads` (read and write, unverified tool
names) is judged as a script and its write tools stay denied. If it is
wired, check the server's tool list in the session and use only the
analytics read.

## Manual export (the default)

Campaign Manager > the account > Campaigns > set the date range > Export.
Choose the campaign-level report, CSV. LinkedIn's columns are named for
people; map them:

| Snapshot column | Campaign Manager column | Note |
| --- | --- | --- |
| `campaign` | Campaign Name | must carry the slug from `data/ontology/naming.md` |
| `platform` | constant `linkedinads` | |
| `period_start`, `period_end` | the export's date range | |
| `spend` | Total Spent | account currency |
| `impressions` | Impressions | |
| `clicks` | Clicks | for Lead Gen Forms use Clicks to Landing Page only if the objective is website visits |
| `conversions` | Conversions, or Leads for Lead Gen Form campaigns | say which in the report |
| `cost_per_conversion` | `spend / conversions` | blank when 0 |
| `currency` | the account currency | |

Drop the file at `data/ads/snapshots/YYYY-MM-DD-linkedinads-campaigns.csv`.
The demographics export (job title, company, seniority per campaign) is a
second file, `YYYY-MM-DD-linkedinads-demographics.csv`; it is aggregate,
so the PII rule in `data/ads/README.md` allows it.

## The API, if a script is written

`GET /rest/adAnalytics?q=analytics&pivot=CAMPAIGN&timeGranularity=ALL`
with `dateRange`, `accounts`, and `fields=costInLocalCurrency,impressions,clicks,externalWebsiteConversions,oneClickLeads,landingPageClicks`.
`costInLocalCurrency` is the spend, `oneClickLeads` the Lead Gen Form
count, `externalWebsiteConversions` the Insight Tag conversions. The
Marketing API needs partner approval for the app before any token works
(catalog caveat), and the version header changes quarterly. Model the
script on `scripts/seo_snapshot.py`; the pull mechanics live with the
`snapshot-pull` skill.

## Reading the numbers

- LinkedIn attributes conversions on a 30-day click and 7-day view window
  by default; Google Ads defaults differ. Never add the two columns
  without naming the windows.
- Frequency (impressions per member) is not in the campaign export; read
  it in the campaign's Performance chart when creative fatigue is the
  question.
- Audience size and penetration (reached members divided by audience
  size) are in the campaign's Demographics and forecast panels, not in the
  CSV; note them by hand when scaling is on the table.
