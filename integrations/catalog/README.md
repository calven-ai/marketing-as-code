# integrations/catalog/

**Kind:** agents, the workforce as instructions in English.

Every integration category this repo's skills know, and every vendor route
the catalog holds for it: the official MCP server where one exists, the CLI
or script where that is the headless path, and always a by-hand export.
One JSON file per category (`crm.json`, `web-analytics.json`, and so on);
this page is rendered from them by `python3 scripts/lint.py --fix`. Edit
the JSON, never this table.

Skills name a category in their `needs`, never a vendor. Which vendor is
wired for each category in this repo is the Wired table in
[integrations/README.md](../README.md); `python3 scripts/wire_integration.py
--list` prints the same from the terminal, and
`python3 scripts/wire_integration.py <vendor>` wires one.

How to read a row: **Mechanism** is the default route (`http` a remote
server, `stdio` a local package pinned to a version, then the CLI or script
if the vendor has one). **Auth** is the model and the variables a person
puts in `.env`. **Writes** says whether the server can create, change or
send anything; write tools are denied in `.claude/settings.json` when wired,
unless the team allows them. **Headless** says whether it can run in GitHub
Actions (key-based servers and scripts can; OAuth cannot). **Verified** is
`vendor` when the entry was read on the vendor's own docs or repo,
`listing` when only a directory said so, `unverified` when nobody checked;
the wire script refuses an unverified entry without `--force`. **Checked**
is the date; the check warns after 180 days.

<!-- generated:catalog -->
### crm

**CRM**: pipeline, contacts, companies, deals, lifecycle stages. Data lands in `data/crm/`.
By hand: Export the deals or contacts view as CSV from the CRM's list page (HubSpot: Contacts/Deals > Export; Salesforce: a report > Export) and drop the file into the snapshots folder. Drop: `data/crm/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| HubSpot | http `hubspot`: https://mcp.hubspot.com; CLI `hs` | oauth | yes, 5 tools recorded | no | vendor | 2026-09-04 |
| Salesforce | http `salesforce`: https://api.salesforce.com/platform/mcp/v1/platform/ (+1 variant); CLI `sf` | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Pipedrive | http `pipedrive`: https://mcp.pipedrive.ai/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Close | http `close`: https://mcp.close.com/mcp (+1 variant) | header: `CLOSE_API_KEY` | yes, tools unrecorded; read-only switch | yes | vendor | 2026-09-04 |
| Attio | http `attio`: https://mcp.attio.com/mcp | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| Zoho CRM | none | manual export | yes, tools unrecorded | no | unverified | 2026-09-04 |
| Microsoft Dynamics 365 | http `dynamics-dataverse`: https://${DYNAMICS_ORG_HOST}/api/mcp; CLI `pac` | oauth: `DYNAMICS_ORG_HOST` | yes, tools unrecorded | no | vendor | 2026-09-04 |

### marketing-automation

**Marketing automation and email**: campaigns, flows and journeys, audiences and segments, email performance. Data lands in `data/email/`.
By hand: Open the campaign or email performance report in the tool, export it as CSV (most tools have Export on the report or campaign list page) and drop the file into the snapshots folder. Drop: `data/email/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| HubSpot Marketing Hub | http `hubspot`: https://mcp.hubspot.com; CLI `hs` | oauth | yes, 5 tools recorded | no | vendor | 2026-09-04 |
| Marketo (Adobe) | http `marketo`: https://marketo-mcp.adobe.io/mcp | header: `MARKETO_CLIENT_ID`, `MARKETO_CLIENT_SECRET`, `MARKETO_MUNCHKIN_ID` | yes, tools unrecorded | yes | vendor | 2026-09-04 |
| Customer.io | http `customerio`: https://mcp.customer.io/mcp (+1 variant) | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Braze | http `braze`: https://mcp.braze.com/mcp (+1 variant) | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| Klaviyo | http `klaviyo`: https://mcp.klaviyo.com/mcp (+1 variant) | oauth | yes, tools unrecorded; read-only switch | no | vendor | 2026-09-04 |
| Mailchimp | http `mandrill`: https://mandrillapp.com/mcp | bearer: `MANDRILL_API_KEY` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| ActiveCampaign | none | manual export | yes, tools unrecorded | no | listing | 2026-09-04 |
| Brevo | http `brevo`: https://mcp.brevo.com/v1/brevo/mcp | bearer: `BREVO_MCP_TOKEN` | yes, tools unrecorded | yes | vendor | 2026-09-04 |
| Iterable | stdio `iterable`: npx -y @iterable/mcp@1.8.1 | env: `ITERABLE_API_KEY` | yes, tools unrecorded | yes | vendor | 2026-09-04 |
| Intercom | http `intercom`: https://mcp.intercom.com/mcp | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| Resend | http `resend`: https://mcp.resend.com/mcp (+2 variants) | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |

### transcripts

**Meeting transcripts and conversation intelligence**: meeting transcripts, call summaries, action items into memory/transcripts/inbox/. Data lands in `memory/transcripts/`.
By hand: Open the meeting in the tool, copy or download the transcript as text, and save it as one Markdown file per meeting in the inbox contract (memory/transcripts/README.md) with the date and a slug in the filename. Drop: `memory/transcripts/inbox/YYYY-MM-DD-<slug>.md`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Granola | http `granola`: https://mcp.granola.ai/mcp; script `scripts/pull_transcripts.py` | oauth: `GRANOLA_API_KEY` | no | script | vendor | 2026-09-04 |
| Gong | http `gong`: https://mcp.gong.io/mcp | oauth | no | no | vendor | 2026-09-04 |
| Fireflies.ai | http `fireflies`: https://api.fireflies.ai/mcp | oauth | no | no | vendor | 2026-09-04 |
| Fathom | http `fathom`: https://api.fathom.ai/mcp | oauth | no | no | vendor | 2026-09-04 |
| Otter.ai | http `otter`: https://mcp.otter.ai/mcp | oauth | no | no | listing | 2026-09-04 |
| Grain | http `grain`: https://api.grain.com/_/mcp | oauth | no | no | vendor | 2026-09-04 |
| Avoma | none | manual export | yes, tools unrecorded | no | listing | 2026-09-04 |
| tl;dv | none | manual export | no | no | vendor | 2026-09-04 |
| Zoom | http `zoom`: https://mcp.zoom.us/mcp/meeting/streamable (+1 variant) | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| Google Meet (Gemini notes via Workspace MCP) | http `google-workspace`: https://workspacemcp.googleapis.com/mcp/v1 | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |

### web-analytics

**Web and product analytics**: traffic, sessions, conversions, funnels, retention, session replay. Data lands in `data/analytics/`.
By hand: Open the report in the analytics tool (GA4: Reports > Explore or a standard report; PostHog and Mixpanel: the insight), export it as CSV from the report's share or export menu, and drop the file into the snapshots folder. Drop: `data/analytics/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Google Analytics 4 | stdio `ga4`: pipx run analytics-mcp==0.7.0; CLI `gcloud` | env: `GOOGLE_APPLICATION_CREDENTIALS`, `GOOGLE_PROJECT_ID` | no | yes | vendor | 2026-09-04 |
| PostHog | http `posthog`: https://mcp.posthog.com/mcp?readonly=true (+1 variant); CLI `posthog-cli` | oauth | yes, tools unrecorded; read-only switch | no | vendor | 2026-09-04 |
| Mixpanel | http `mixpanel`: https://mcp.mixpanel.com/mcp (+1 variant) | oauth | no | no | vendor | 2026-09-04 |
| Amplitude | http `amplitude`: https://mcp.amplitude.com/mcp (+1 variant) | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| Plausible | http `plausible`: https://plausible-mcp.sentry.dev/mcp | bearer: `PLAUSIBLE_API_KEY` | no | yes | listing | 2026-09-04 |
| Matomo | none | manual export | no | no | listing | 2026-09-04 |
| Adobe Analytics / Customer Journey Analytics | none | manual export | yes, tools unrecorded | no | unverified | 2026-09-04 |
| Microsoft Clarity | stdio `clarity`: npx -y @microsoft/clarity-mcp-server@2.0.1 --clarity_api_token=${CLARITY_API_TOKEN} | env: `CLARITY_API_TOKEN` | no | yes | vendor | 2026-09-04 |
| Heap and Hotjar (Contentsquare) | none | manual export | no | no | unverified | 2026-09-04 |

### seo-data

**SEO and search data**: keyword volumes and difficulty, rankings, SERP features, backlinks, site audits, Search Console performance. Data lands in `data/seo/`.
By hand: Export the keyword, ranking or backlink report as CSV from the tool (Search Console: Performance > Export; Ahrefs and Semrush: the Export button on any report) and drop the file into the snapshots folder; data/seo/keywords.csv stays the canonical table. Drop: `data/seo/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| DataForSEO | stdio `dataforseo`: npx -y dataforseo-mcp-server@3.1.1; script `scripts/seo_snapshot.py` | env: `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | no | yes | vendor | 2026-09-04 |
| Ahrefs | http `ahrefs`: https://api.ahrefs.com/mcp/mcp | oauth | no | no | vendor | 2026-09-04 |
| Semrush | http `semrush`: https://mcp.semrush.com/v2/mcp (+1 variant) | oauth | no | no | vendor | 2026-09-04 |
| Moz | none | manual export | no | no | vendor | 2026-09-04 |
| Google Search Console | stdio `gsc`: uvx mcp-search-console==0.3.3 | env: `GSC_CREDENTIALS_PATH` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| Similarweb | http `similarweb`: https://mcp.similarweb.com | header: `SIMILARWEB_API_KEY` | no | yes | vendor | 2026-09-04 |
| Screaming Frog SEO Spider | CLI `screamingfrogseospider` | manual export | no | no | vendor | 2026-09-04 |
| Bing Webmaster Tools | none | manual export | yes, tools unrecorded | no | listing | 2026-09-04 |

### ai-visibility

**AI visibility (AEO / GEO)**: how AI answer engines mention and cite us and competitors against the prompt set in data/seo/prompts.csv. Data lands in `data/seo/`.
By hand: Run the prompt set by hand in ChatGPT, Perplexity and Google AI Overviews, record which brands are mentioned and which pages are cited in a CSV (one row per prompt and engine), or export the visibility report from the AEO tool, and drop it into the snapshots folder. Drop: `data/seo/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| DataForSEO AI Optimization | stdio `dataforseo`: npx -y dataforseo-mcp-server@3.1.1 | env: `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | no | yes | vendor | 2026-09-04 |
| Profound | stdio `profound`: npx -y @profoundai/mcp@0.47.0 | env: `PROFOUND_API_KEY` | no | yes | vendor | 2026-09-04 |
| Peec AI | http `peec`: https://api.peec.ai/mcp | oauth | no | no | vendor | 2026-09-04 |
| Otterly.ai | http `otterly`: https://data.otterly.ai/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Scrunch AI | none | manual export | no | no | unverified | 2026-09-04 |
| Athena (AthenaHQ) | none | manual export | no | no | unverified | 2026-09-04 |

### ads

**Paid media**: campaign spend, impressions, clicks, conversions, cost per lead across ad platforms. Data lands in `data/ads/`.
By hand: Open the campaign report in the ads platform (Google Ads: Campaigns > Download; Meta: Ads Manager > Reports > Export; LinkedIn: Campaign Manager > Export), export it as CSV for the period, and drop the file into the snapshots folder. Drop: `data/ads/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Google Ads | stdio `googleads`: pipx run --spec git+https://github.com/googleads/google-ads-mcp.git@88f0467b9e536c562941fa52a94dd02b193c8fa4 google-ads-mcp; CLI `gcloud` | env: `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_APPLICATION_CREDENTIALS`, `GOOGLE_PROJECT_ID` | no | yes | vendor | 2026-09-04 |
| Meta Ads | http `metaads`: https://mcp.facebook.com/ads | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| LinkedIn Ads (Campaign Manager) | stdio `linkedinads`: npx -y mcp-linkedin-ads@1.1.3 | env: `LINKEDIN_ADS_ACCESS_TOKEN` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| Microsoft Advertising (Bing Ads) | stdio `microsoftads`: npx -y mcp-bing-ads@1.2.0 | env: `BING_ADS_CLIENT_ID`, `BING_ADS_CLIENT_SECRET`, `BING_ADS_DEVELOPER_TOKEN`, `BING_ADS_REFRESH_TOKEN` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| X Ads | none | manual export | yes, tools unrecorded | no | listing | 2026-09-04 |
| Reddit Ads | stdio `redditads`: npx -y mcp-reddit-ads@1.1.3 | env: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_REFRESH_TOKEN` | yes, tools unrecorded | yes | listing | 2026-09-04 |

### social

**Social media publishing and listening**: scheduling and publishing posts, post performance, mentions and listening on X, LinkedIn, Threads, Bluesky. Data lands in `data/social/`.
By hand: Export the post performance or analytics report as CSV from the scheduling tool or the network's own analytics (LinkedIn Page > Analytics > Export; X Analytics > Export data) and drop the file into the snapshots folder. Drop: `data/social/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: generic, scraping-search.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| X (Twitter) | http `x`: https://api.x.com/mcp | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| Buffer | none | manual export | yes, tools unrecorded | no | vendor | 2026-09-04 |
| Hootsuite | http `hootsuite-listen`: https://mcp.hootsuite.com/lumen (+2 variants) | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| Sprout Social | http `sproutsocial`: https://mcp.sproutsocial.com/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Typefully | http `typefully`: https://mcp.typefully.com/mcp | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| Taplio | http `taplio`: https://mcp.taplio.com/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| LinkedIn (organic pages and profiles) | none | manual export | no | no | listing | 2026-09-04 |
| Ayrshare | none | manual export | yes, tools unrecorded | no | vendor | 2026-09-04 |

### cms

**CMS**: the website and blog CMS: publishing approved content, reading what is live.
By hand: paste the draft into the CMS by hand; the agent only sets published_url in the repo Drop: `content/<piece>/ frontmatter (published_url and status)`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Webflow | http `webflow`: https://mcp.webflow.com/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Contentful | http `contentful`: https://mcp.contentful.com/mcp (+1 variant) | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Sanity | http `sanity`: https://mcp.sanity.io | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| WordPress | stdio `wordpress`: npx -y @automattic/mcp-wordpress-remote@0.4.0 | basic: `WORDPRESS_APP_PASSWORD`, `WORDPRESS_SITE_URL`, `WORDPRESS_USERNAME` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| Storyblok | http `storyblok`: https://mcp.labs.storyblok.com/mcp | bearer: `STORYBLOK_MANAGEMENT_TOKEN` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| Hygraph | http `hygraph`: https://mcp.hygraph.com/mcp | bearer: `HYGRAPH_PAT` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| Ghost | none | manual export | no | no | listing | 2026-09-04 |
| Framer | none | manual export | no | no | listing | 2026-09-04 |

### enrichment

**Enrichment**: contact and company data: enriching target accounts and people in data/accounts. Data lands in `data/accounts/`.
By hand: export the enriched list from the tool as CSV (one row per person or account, with the company domain and the fields you asked for) Drop: `data/accounts/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Apollo.io | http `apollo`: https://mcp.apollo.io/mcp | oauth | no | no | listing | 2026-09-04 |
| Clay | http `clay`: https://api.clay.com/v3/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| ZoomInfo | http `zoominfo`: https://mcp.zoominfo.com/mcp | oauth | no | no | listing | 2026-09-04 |
| Lusha | http `lusha`: https://mcp.lusha.com | header: `LUSHA_API_KEY` | no | yes | listing | 2026-09-04 |
| Hunter.io | http `hunter`: https://mcp.hunter.io/mcp (+1 variant) | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| FullEnrich | http `fullenrich`: https://mcp.fullenrich.com/mcp | oauth | no | no | listing | 2026-09-04 |
| Dropcontact | none | manual export | no | no | listing | 2026-09-04 |
| People Data Labs | none | manual export | no | no | listing | 2026-09-04 |
| Clearbit (HubSpot Breeze Intelligence) | none | manual export | no | no | listing | 2026-09-04 |
| Cognism | none | manual export | no | no | unverified | 2026-09-04 |

### intent

**Intent**: intent and signal data: which target accounts are in market, joined to data/accounts. Data lands in `data/accounts/`.
By hand: export the account list with its intent score or buying stage from the tool as CSV (one row per account, with the company domain) Drop: `data/accounts/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Common Room | http `commonroom`: https://mcp.commonroom.io/mcp | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| Demandbase | http `demandbase`: https://gateway.demandbase.com/mcp/servers/db-mcp | oauth | no | no | listing | 2026-09-04 |
| 6sense | none | manual export | no | no | listing | 2026-09-04 |
| G2 Buyer Intent | http `g2`: https://mcp.g2.com/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Warmly | http `warmly`: https://opps-api.getwarmly.com/api/mcp | oauth | no | no | listing | 2026-09-04 |
| RB2B | stdio `rb2b`: npx -y @rb2b/rb2b-apis-mcp@1.1.7 | env: `RB2B_API_KEY` | no | yes | listing | 2026-09-04 |
| Bombora | none | manual export | no | no | unverified | 2026-09-04 |
| Vector | none | manual export | no | no | listing | 2026-09-04 |

### outbound

**Outbound**: outbound sequencing and sales engagement: loading approved sequences, reading reply and meeting outcomes.
By hand: the sequence stays in content/ as text; a person loads it into the tool by hand Drop: `content/<piece>/ (the sequence steps as Markdown, one heading per step)`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Outreach | http `outreach`: https://api.outreach.io/mcp | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| Salesloft | none | manual export | yes, tools unrecorded | no | listing | 2026-09-04 |
| lemlist | http `lemlist`: https://app.lemlist.com/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Instantly | http `instantly`: https://mcp.instantly.ai/mcp | bearer: `INSTANTLY_API_KEY` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| Smartlead | stdio `smartlead`: npx -y mcp-remote@0.8.3 https://mcp.smartlead.ai/sse?user_api_key=${SMARTLEAD_API_KEY} | env: `SMARTLEAD_API_KEY` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| Apollo.io sequences | http `apollo`: https://mcp.apollo.io/mcp | oauth | no | no | listing | 2026-09-04 |

### design

**Design**: design and creative tools: reading design context, exporting assets, filling brand templates.
By hand: a person exports the asset and drops it under brand/ or content/<x>/ Drop: `brand/ (logos, templates) or content/<piece>/ (assets for one piece)`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Figma | http `figma`: https://mcp.figma.com/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Canva | http `canva`: https://mcp.canva.com/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Adobe Express | stdio `adobe-express`: npx -y @adobe/express-developer-mcp@1.0.0 | none | no | yes | listing | 2026-09-04 |

### docs

**Docs**: the team's document and wiki tools: reading briefs and notes, publishing reports where the team reads them.
By hand: the agent writes Markdown into the repo; a person copies it into the doc tool by hand Drop: `reports/ or memory/knowledge/ (the repo copy stays canonical)`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Notion | http `notion`: https://mcp.notion.com/mcp (+1 variant) | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| Google Workspace (Drive, Docs, Sheets) | http `google-workspace`: https://workspacemcp.googleapis.com/mcp/v1 | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Confluence (Atlassian Rovo MCP) | http `atlassian`: https://mcp.atlassian.com/v2/mcp (+1 variant) | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| Airtable | http `airtable`: https://mcp.airtable.com/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Coda | none | manual export | no | no | unverified | 2026-09-04 |

### tasks

**Tasks**: the team's task tool: filing follow-ups per integrations/tasks.md.
By hand: file the task as a `- [ ]` line with the owner in parentheses under `## Tasks` in the project's status.md, or on the follow-ups line of the decision in memory/decision-log.md when it belongs to no project (the fallback in integrations/tasks.md) Drop: `projects/<name>/status.md (the ## Tasks checklist)`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Linear | http `linear`: https://mcp.linear.app/mcp (+2 variants) | oauth | yes, 5 tools recorded; read-only switch | no | listing | 2026-09-04 |
| Asana | http `asana`: https://mcp.asana.com/v2/mcp | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| Jira (Atlassian Rovo MCP) | http `atlassian`: https://mcp.atlassian.com/v2/mcp (+1 variant) | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| ClickUp | http `clickup`: https://mcp.clickup.com/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| monday.com | http `monday`: https://mcp.monday.com/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Trello | http `trello`: https://mcp.trello.com/v1 | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| GitHub Issues | http `github`: https://api.githubcopilot.com/mcp/ (+2 variants); CLI `gh` | oauth | yes, 8 tools recorded; read-only switch | no | vendor | 2026-09-04 |

### chat

**Chat**: the team's chat tool: digests, alerts and red flags out; reading threads and requests in.
By hand: the digest is printed for a person to paste into the channel by hand Drop: `the channel itself; the repo keeps its copy in reports/ or memory/decision-log.md with the permalink`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Slack | http `slack`: https://mcp.slack.com/mcp; script `scripts/slack_post.py` | oauth: `SLACK_BOT_TOKEN`, `SLACK_LEADERSHIP_CHANNEL_ID`, `SLACK_REQUESTS_CHANNEL_ID`, `SLACK_TEAM_CHANNEL_ID` | yes, tools unrecorded | script | vendor | 2026-09-04 |
| Microsoft Teams | http `microsoft-teams`: https://agent365.svc.cloud.microsoft/agents/tenants/${TEAMS_TENANT_ID}/servers/mcp_TeamsServer | oauth: `TEAMS_TENANT_ID` | yes, tools unrecorded | no | listing | 2026-09-04 |

### events

**Events**: webinars and events: registrants, attendees and recordings, joined to the funnel in data/events. Data lands in `data/events/`.
By hand: export registrants and attendees from the webinar tool as CSV (one row per person, with the event name, registration time, and attended yes/no) Drop: `data/events/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Livestorm | http `livestorm`: https://mcp.livestorm.co/mcp | oauth | no | no | listing | 2026-09-04 |
| Zoom (Webinars and Meetings) | http `zoom`: https://mcp.zoom.us/mcp/zoom/streamable | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| ON24 | none | manual export | no | no | listing | 2026-09-04 |
| Goldcast | none | manual export | no | no | listing | 2026-09-04 |
| Eventbrite | none | manual export | no | no | listing | 2026-09-04 |
| Luma | none | manual export | no | no | listing | 2026-09-04 |
| Bizzabo | none | manual export | no | no | listing | 2026-09-04 |

### surveys-reviews

**Surveys and reviews**: review sites, buyer intent from review traffic, surveys, NPS and customer voice. Data lands in `data/reviews/`.
By hand: Export reviews or survey responses as CSV from the vendor dashboard (G2 Seller Solutions, Typeform Results, SurveyMonkey Analyze). Drop: `data/reviews/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| G2 | http `g2`: https://mcp.g2.com/mcp | oauth | no | no | vendor | 2026-09-04 |
| Typeform | http `typeform`: https://api.typeform.com/mcp (+1 variant) | oauth | yes, tools unrecorded | no | vendor | 2026-09-04 |
| SurveyMonkey | http `surveymonkey`: https://mcp.surveymonkey.com/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Qualtrics | none | manual export | no | no | listing | 2026-09-04 |
| Capterra / Gartner Digital Markets | none | manual export | no | no | listing | 2026-09-04 |
| TrustRadius | none | manual export | no | no | listing | 2026-09-04 |
| Trustpilot | none | manual export | no | no | listing | 2026-09-04 |
| Product Hunt | none | manual export | no | no | listing | 2026-09-04 |
| Delighted | none | manual export | no | no | listing | 2026-09-04 |

### pr-media

**PR and media**: journalist databases, press distribution, media monitoring, analyst relations. Data lands in `data/pr/`.
By hand: build the list by hand in a CSV Drop: `data/pr/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: scraping-search, generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Muck Rack | none | manual export | no | no | vendor | 2026-09-04 |
| Cision | none | manual export | no | no | vendor | 2026-09-04 |
| Meltwater | none | manual export | no | no | vendor | 2026-09-04 |
| Prowly | none | manual export | no | no | vendor | 2026-09-04 |

### scraping-search

**Scraping and search**: web scraping, actor runs, web and news search, page reading for ABM research and monitoring. Data lands in `data/accounts/`.
By hand: Export the actor run dataset or the search result list as CSV from the vendor console (Apify: Storage > Dataset > Export). Drop: `data/accounts/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Apify | http `apify`: https://mcp.apify.com; CLI `apify` | oauth | yes, 1 tools recorded | no | vendor | 2026-09-04 |
| Firecrawl | stdio `firecrawl`: npx -y firecrawl-mcp@3.24.0 (+1 variant) | env: `FIRECRAWL_API_KEY` | no | yes | vendor | 2026-09-04 |
| Exa | http `exa`: https://mcp.exa.ai/mcp (+1 variant) | none | no | yes | vendor | 2026-09-04 |
| Tavily | stdio `tavily`: npx -y tavily-mcp@0.2.22 (+1 variant) | env: `TAVILY_API_KEY` | no | yes | vendor | 2026-09-04 |
| Brave Search | stdio `brave-search`: npx -y @brave/brave-search-mcp-server@2.1.3 | env: `BRAVE_API_KEY` | no | yes | vendor | 2026-09-04 |
| Perplexity | http `perplexity`: https://api.perplexity.ai/mcp (+1 variant) | bearer: `PERPLEXITY_API_KEY` | no | yes | vendor | 2026-09-04 |
| Jina Reader | none | manual export | no | no | unverified | 2026-09-04 |
| Bright Data | http `brightdata`: https://mcp.brightdata.com/mcp?token=${BRIGHTDATA_API_TOKEN} (+1 variant) | env: `BRIGHTDATA_API_TOKEN` | no | yes | vendor | 2026-09-04 |
| Browserbase | none | manual export | no | no | vendor | 2026-09-04 |

### warehouse-bi

**Warehouse and BI**: the data warehouse, transformation layer, BI dashboards, CDP and reverse ETL that hold the joined marketing data.
By hand: Run the question in the BI tool or warehouse console and export the result as CSV. Drop: `export the query result as CSV into the matching data/<domain>/snapshots/`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| dbt | stdio `dbt`: uvx dbt-mcp==2.2.1; CLI `dbt` | env: `DBT_HOST`, `DBT_PROD_ENV_ID`, `DBT_TOKEN` | yes, tools unrecorded; read-only switch | yes | vendor | 2026-09-04 |
| Snowflake | http `snowflake`: ${SNOWFLAKE_MCP_URL}; CLI `snow` | bearer: `SNOWFLAKE_MCP_URL`, `SNOWFLAKE_PAT` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| BigQuery | http `bigquery`: https://bigquery.googleapis.com/mcp; CLI `bq` | oauth | no | no | listing | 2026-09-04 |
| Looker | http `looker`: ${LOOKER_BASE_URL}/mcp | oauth: `LOOKER_BASE_URL` | no | no | listing | 2026-09-04 |
| Metabase | http `metabase`: ${METABASE_URL}/api/metabase-mcp | header: `METABASE_API_KEY`, `METABASE_URL` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| Tableau | http `tableau`: https://mcp.tableau.com (+1 variant) | oauth | no | no | vendor | 2026-09-04 |
| Power BI | none | manual export | no | no | vendor | 2026-09-04 |
| Dreamdata | none | manual export | no | no | vendor | 2026-09-04 |
| Segment | none | manual export | no | no | listing | 2026-09-04 |
| RudderStack | http `rudderstack`: https://mcp.rudderstack.com/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Hightouch | none | manual export | no | no | vendor | 2026-09-04 |
| Census | none | manual export | no | no | listing | 2026-09-04 |

### billing

**Billing**: subscriptions, revenue, renewals, MRR and churn for PLG and self-serve reporting. Data lands in `data/crm/`.
By hand: Export customers, subscriptions or MRR movements as CSV from the billing dashboard (Stripe: Billing > Subscriptions > Export; ChartMogul: Data > Export). Drop: `data/crm/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Stripe | http `stripe`: https://mcp.stripe.com (+1 variant); CLI `stripe` | oauth | yes, tools unrecorded; read-only switch | no | vendor | 2026-09-04 |
| ChartMogul | http `chartmogul`: https://mcp.chartmogul.com | oauth | no | no | vendor | 2026-09-04 |
| Paddle | http `paddle`: https://mcp.paddle.com/mcp | bearer: `PADDLE_API_KEY` | yes, tools unrecorded | yes | listing | 2026-09-04 |

### community

**Community**: forums, member communities, community chat servers. Data lands in `data/social/`.
By hand: Export members, topics or posts as CSV from the community admin panel (Discourse: Admin > Data Explorer; Circle: Members > Export). Drop: `data/social/snapshots/YYYY-MM-DD-<source>-<what>.csv`.
Falls back to: chat, generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Discourse | stdio `discourse`: npx -y @discourse/mcp@0.3.1 --site ${DISCOURSE_SITE_URL} --profile ${DISCOURSE_MCP_PROFILE} | env: `DISCOURSE_MCP_PROFILE`, `DISCOURSE_SITE_URL` | no | yes | vendor | 2026-09-04 |
| Circle | http `circle`: https://app.circle.so/api/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Discord | none | manual export | no | no | vendor | 2026-09-04 |
| Slack (community workspace) | none | manual export | no | no | vendor | 2026-09-04 |

### context-layer

**Context layer**: positioning, messaging, ICP, product brief, personas, competitors and customer voice served live to every agent. Data lands in `strategy/`.
By hand: Keep the strategy documents as hand-edited Markdown and bump last_reviewed when the team reviews them. Drop: `strategy/*.md maintained by hand with last_reviewed dates`.
Falls back to: generic.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Calven | http `calven`: https://app.calven.ai/api/mcp | bearer: `CALVEN_MCP_KEY` | no | yes | vendor | 2026-09-04 |

### generic

**Generic connectors**: one server that reaches many apps: the long tail of tools with no vendor MCP, and one-off write actions.
By hand: A generic connector holds no data of its own; export from the bridged tool per its own category. Drop: `no data of its own; the bridged category's manual route applies`.

| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |
| --- | --- | --- | --- | --- | --- | --- |
| Zapier MCP | http `zapier`: ${ZAPIER_MCP_URL} | env: `ZAPIER_MCP_URL` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| Composio (Rube) | http `composio`: https://rube.app/mcp | oauth | yes, tools unrecorded | no | listing | 2026-09-04 |
| Pipedream MCP | http `pipedream`: ${PIPEDREAM_MCP_URL} | env: `PIPEDREAM_MCP_URL` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| Make | stdio `make`: npx -y @makehq/mcp-server@0.5.0 | env: `MAKE_API_KEY`, `MAKE_TEAM`, `MAKE_ZONE` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| n8n | http `n8n`: ${N8N_MCP_URL} | bearer: `N8N_MCP_TOKEN`, `N8N_MCP_URL` | yes, tools unrecorded | yes | listing | 2026-09-04 |
| Merge.dev, Nango, Paragon ActionKit, Unified.to | none | manual export | yes, tools unrecorded | no | listing | 2026-09-04 |
<!-- /generated:catalog -->
