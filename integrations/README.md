# integrations/

**Kind:** agents, the workforce as instructions in English.

The registry of tools this repo's agents can reach, and how each one
connects. Skills never name a vendor: they name an integration *category*
(`crm`, `web-analytics`, `ads`, and so on), and this page says which vendor
fills each category in this repo. Five ship wired. For the rest of your
stack, [the catalog](catalog/README.md) holds the routes for the common
vendors in every category, `python3 scripts/wire_integration.py <vendor>`
wires one, and [adding-an-integration.md](adding-an-integration.md) carries
the rules for a tool the catalog does not know.

## Wired in this repo

Rendered from [`wired.json`](wired.json) and the catalog by
`python3 scripts/lint.py --fix`; the wire script edits `wired.json`, never
this table.

<!-- generated:wired -->
| Category | Vendor | Route | Auth | Env vars (in `.env`) | Writes | Since |
| --- | --- | --- | --- | --- | --- | --- |
| [transcripts](catalog/README.md#transcripts) | Granola | `scripts/pull_transcripts.py` (the unattended path; daily via .github/workflows/transcripts-cron.yml) | key in the environment | `GRANOLA_API_KEY` | n/a | 2026-08-31 |
| [seo-data](catalog/README.md#seo-data) | DataForSEO | MCP `dataforseo` (stdio) in `.mcp.json`; `scripts/seo_snapshot.py` (the scheduled refresh: search volume and difficulty for every row of data/seo/keywords.csv into data/seo/snapshots/YYYY-MM-DD-dataforseo-volume.csv; --update also refreshes the canonical table) | env: app.dataforseo.com > API access | `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | n/a | 2026-08-31 |
| [ai-visibility](catalog/README.md#ai-visibility) | DataForSEO AI Optimization | MCP `dataforseo` (stdio) in `.mcp.json` | env: app.dataforseo.com > API access | `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | n/a | 2026-08-31 |
| [tasks](catalog/README.md#tasks) | none | manual: in-repo checklists, the fallback in integrations/tasks.md; /setup binds the team's tool | | none | | |
| [chat](catalog/README.md#chat) | Slack | `scripts/slack_post.py` (the team's own Slack app (integrations/slack/); outbound posts only) | key in the environment | `SLACK_BOT_TOKEN`, `SLACK_LEADERSHIP_CHANNEL_ID`, `SLACK_REQUESTS_CHANNEL_ID`, `SLACK_TEAM_CHANNEL_ID` | allowed | 2026-08-31 |
| [scraping-search](catalog/README.md#scraping-search) | Apify | MCP `apify` (http) in `.mcp.json` | oauth: browser grant on first use | none | allowed | 2026-08-31 |
| [context-layer](catalog/README.md#context-layer) | Calven | MCP `calven` (http) in `.mcp.json` | bearer: Calven: Settings > Integrations > MCP | `CALVEN_MCP_KEY` | n/a | 2026-08-31 |
<!-- /generated:wired -->

The Env vars column mirrors `.env.example`. Agents cannot read any `.env*`
file, so keep the two in sync (the check does). Who owns each key, where it
lives and how to rotate it is in [docs/secrets.md](../docs/secrets.md).

## Every category

What each category is for, what fills it here, and which skills need it.
A skill whose category is not wired says exactly which export a person
should drop where, and stops; it never guesses.

<!-- generated:categories -->
| Category | For | Wired | In the catalog | Needed by |
| --- | --- | --- | --- | --- |
| [crm](catalog/README.md#crm) | pipeline, contacts, companies, deals, lifecycle stages | not wired | HubSpot, Salesforce, Pipedrive, Close, Attio, Zoho CRM, Microsoft Dynamics 365 (falls back to generic) | [account-signals](../.agents/skills/account-signals/SKILL.md), [advocacy-program](../.agents/skills/advocacy-program/SKILL.md), [attribution-analysis](../.agents/skills/attribution-analysis/SKILL.md), [churn-signals](../.agents/skills/churn-signals/SKILL.md), [closed-lost-revival](../.agents/skills/closed-lost-revival/SKILL.md), [data-hygiene-audit](../.agents/skills/data-hygiene-audit/SKILL.md), [expansion-play](../.agents/skills/expansion-play/SKILL.md), [pipeline-report](../.agents/skills/pipeline-report/SKILL.md), [win-loss](../.agents/skills/win-loss/SKILL.md) (+9 optional) |
| [marketing-automation](catalog/README.md#marketing-automation) | campaigns, flows and journeys, audiences and segments, email performance | not wired | HubSpot Marketing Hub, Marketo (Adobe), Customer.io, Braze, Klaviyo, Mailchimp, ActiveCampaign, Brevo, Iterable, Intercom, Resend (falls back to generic) | [email-performance](../.agents/skills/email-performance/SKILL.md) (+5 optional) |
| [transcripts](catalog/README.md#transcripts) | meeting transcripts, call summaries, action items into memory/transcripts/inbox/ | Granola | Granola, Gong, Fireflies.ai, Fathom, Otter.ai, Grain, Avoma, tl;dv, Zoom, Google Meet (Gemini notes via Workspace MCP) (falls back to generic) | (+5 optional) |
| [web-analytics](catalog/README.md#web-analytics) | traffic, sessions, conversions, funnels, retention, session replay | not wired | Google Analytics 4, PostHog, Mixpanel, Amplitude, Plausible, Matomo, Adobe Analytics / Customer Journey Analytics, Microsoft Clarity, Heap and Hotjar (Contentsquare) (falls back to generic) | [attribution-analysis](../.agents/skills/attribution-analysis/SKILL.md), [web-analyst](../.agents/skills/web-analyst/SKILL.md) (+10 optional) |
| [seo-data](catalog/README.md#seo-data) | keyword volumes and difficulty, rankings, SERP features, backlinks, site audits, Search Console performance | DataForSEO | DataForSEO, Ahrefs, Semrush, Moz, Google Search Console, Similarweb, Screaming Frog SEO Spider, Bing Webmaster Tools (falls back to generic) | [backlink-analysis](../.agents/skills/backlink-analysis/SKILL.md), [content-decay-monitor](../.agents/skills/content-decay-monitor/SKILL.md), [keyword-cluster](../.agents/skills/keyword-cluster/SKILL.md), [seo-analyst](../.agents/skills/seo-analyst/SKILL.md) (+11 optional) |
| [ai-visibility](catalog/README.md#ai-visibility) | how AI answer engines mention and cite us and competitors against the prompt set in data/seo/prompts.csv | DataForSEO AI Optimization | DataForSEO AI Optimization, Profound, Peec AI, Otterly.ai, Scrunch AI, Athena (AthenaHQ) (falls back to generic) | [ai-share-of-voice](../.agents/skills/ai-share-of-voice/SKILL.md), [brand-monitor](../.agents/skills/brand-monitor/SKILL.md) (+3 optional) |
| [ads](catalog/README.md#ads) | campaign spend, impressions, clicks, conversions, cost per lead across ad platforms | not wired | Google Ads, Meta Ads, LinkedIn Ads (Campaign Manager), Microsoft Advertising (Bing Ads), X Ads, Reddit Ads (falls back to generic) | [ads-account-audit](../.agents/skills/ads-account-audit/SKILL.md), [ads-performance](../.agents/skills/ads-performance/SKILL.md) (+5 optional) |
| [social](catalog/README.md#social) | scheduling and publishing posts, post performance, mentions and listening on X, LinkedIn, Threads, Bluesky | not wired | X (Twitter), Buffer, Hootsuite, Sprout Social, Typefully, Taplio, LinkedIn (organic pages and profiles), Ayrshare (falls back to generic, scraping-search) | [social-performance](../.agents/skills/social-performance/SKILL.md) (+3 optional) |
| [cms](catalog/README.md#cms) | the website and blog CMS: publishing approved content, reading what is live | not wired | Webflow, Contentful, Sanity, WordPress, Storyblok, Hygraph, Ghost, Framer (falls back to generic) | (+2 optional) |
| [enrichment](catalog/README.md#enrichment) | contact and company data: enriching target accounts and people in data/accounts | not wired | Apollo.io, Clay, ZoomInfo, Lusha, Hunter.io, FullEnrich, Dropcontact, People Data Labs, Clearbit (HubSpot Breeze Intelligence), Cognism (falls back to generic) | (+4 optional) |
| [intent](catalog/README.md#intent) | intent and signal data: which target accounts are in market, joined to data/accounts | not wired | Common Room, Demandbase, 6sense, G2 Buyer Intent, Warmly, RB2B, Bombora, Vector (falls back to generic) | (+1 optional) |
| [outbound](catalog/README.md#outbound) | outbound sequencing and sales engagement: loading approved sequences, reading reply and meeting outcomes | not wired | Outreach, Salesloft, lemlist, Instantly, Smartlead, Apollo.io sequences (falls back to generic) | (+2 optional) |
| [design](catalog/README.md#design) | design and creative tools: reading design context, exporting assets, filling brand templates | not wired | Figma, Canva, Adobe Express (falls back to generic) | (+2 optional) |
| [docs](catalog/README.md#docs) | the team's document and wiki tools: reading briefs and notes, publishing reports where the team reads them | not wired | Notion, Google Workspace (Drive, Docs, Sheets), Confluence (Atlassian Rovo MCP), Airtable, Coda (falls back to generic) | (+3 optional) |
| [tasks](catalog/README.md#tasks) | the team's task tool: filing follow-ups per integrations/tasks.md | manual | Linear, Asana, Jira (Atlassian Rovo MCP), ClickUp, monday.com, Trello, GitHub Issues (falls back to generic) | (+12 optional) |
| [chat](catalog/README.md#chat) | the team's chat tool: digests, alerts and red flags out; reading threads and requests in | Slack | Slack, Microsoft Teams (falls back to generic) | (+6 optional) |
| [events](catalog/README.md#events) | webinars and events: registrants, attendees and recordings, joined to the funnel in data/events | not wired | Livestorm, Zoom (Webinars and Meetings), ON24, Goldcast, Eventbrite, Luma, Bizzabo (falls back to generic) | (+3 optional) |
| [surveys-reviews](catalog/README.md#surveys-reviews) | review sites, buyer intent from review traffic, surveys, NPS and customer voice | not wired | G2, Typeform, SurveyMonkey, Qualtrics, Capterra / Gartner Digital Markets, TrustRadius, Trustpilot, Product Hunt, Delighted (falls back to generic) | [review-monitor](../.agents/skills/review-monitor/SKILL.md) (+3 optional) |
| [pr-media](catalog/README.md#pr-media) | journalist databases, press distribution, media monitoring, analyst relations | not wired | Muck Rack, Cision, Meltwater, Prowly (falls back to scraping-search, generic) | (+2 optional) |
| [scraping-search](catalog/README.md#scraping-search) | web scraping, actor runs, web and news search, page reading for ABM research and monitoring | Apify | Apify, Firecrawl, Exa, Tavily, Brave Search, Perplexity, Jina Reader, Bright Data, Browserbase (falls back to generic) | [researcher](../.agents/skills/researcher/SKILL.md) (+5 optional) |
| [warehouse-bi](catalog/README.md#warehouse-bi) | the data warehouse, transformation layer, BI dashboards, CDP and reverse ETL that hold the joined marketing data | not wired | dbt, Snowflake, BigQuery, Looker, Metabase, Tableau, Power BI, Dreamdata, Segment, RudderStack, Hightouch, Census (falls back to generic) | (+3 optional) |
| [billing](catalog/README.md#billing) | subscriptions, revenue, renewals, MRR and churn for PLG and self-serve reporting | not wired | Stripe, ChartMogul, Paddle (falls back to generic) | (+3 optional) |
| [community](catalog/README.md#community) | forums, member communities, community chat servers | not wired | Discourse, Circle, Discord, Slack (community workspace) (falls back to chat, generic) | [community-digest](../.agents/skills/community-digest/SKILL.md) (+1 optional) |
| [context-layer](catalog/README.md#context-layer) | positioning, messaging, ICP, product brief, personas, competitors and customer voice served live to every agent | Calven | Calven (falls back to generic) | (+9 optional) |
| [generic](catalog/README.md#generic) | one server that reaches many apps: the long tail of tools with no vendor MCP, and one-off write actions | not wired | Zapier MCP, Composio (Rube), Pipedream MCP, Make, n8n, Merge.dev, Nango, Paragon ActionKit, Unified.to | nobody yet |
<!-- /generated:categories -->

## MCP servers, per coding agent

`.mcp.json` (Claude Code) and `.cursor/mcp.json` (Cursor) list the same
servers; the wire script keeps them together, and `scripts/doctor.py`
checks they agree. Codex users paste the TOML the wire script prints, in
the shape from
[the guide](adding-an-integration.md#configuring-an-mcp-server-per-coding-agent).

- **`dataforseo`**: the official `dataforseo-mcp-server` npm package, run
  with `npx` and pinned to `@3.1.1`. It needs Node.js on the machine;
  without Node, swap in the remote endpoint below. Unpinned `npx -y` would run whatever
  was published last, with your DataForSEO login in its environment. Bump
  the version on purpose, in a proposal. Credentials come from
  `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` in your environment. A
  remote endpoint exists too (`https://mcp.dataforseo.com/v3/mcp`, Basic
  auth); swap the entry if you prefer not to run `npx`.
- **`apify`**: the official remote server at `https://mcp.apify.com`.
  OAuth in the browser on first use, no key.
- **`calven`**: the remote server at `https://app.calven.ai/api/mcp`,
  bearer key from `CALVEN_MCP_KEY`. The repo works without it.

The entries hold placeholders, never values. Non-interactive runs (the
GitHub action, `claude -p`) load project servers without asking, so a value
in the file would run anywhere the repo is checked out. Placeholders are
filled from the environment, not from `.env`; how to start an agent with
them is in [docs/secrets.md](../docs/secrets.md).

A server that can write (create a contact, send an email, post) has its
write tools denied in `.claude/settings.json` the day it is wired; the
wire script adds the rules from the catalog's `write_tools`, and `--allow-writes`
records the team's decision to lift them in `wired.json`. Even then, a
skill only stages drafts and asks before each write (AGENTS.md rule 3).

## [tasks.md](tasks.md): the task-tool adapter

The one file that tells every agent where tasks go and how to file them.
`/setup` fills it in for your team's tool. Until then it documents the
zero-setup fallback. **Any skill that creates tasks reads `tasks.md` first.**
That is the whole abstraction.

## For agents

- Pulling data? Find the category's wired vendor above, use that mechanism
  (the skill's `references/<vendor>.md` has the tool names), and save the
  pull as a snapshot named per `data/README.md`.
- Category not wired? Say exactly what export the human should make and
  where to drop it (the category's manual route in the catalog). Never
  guess, and never connect a tool unasked.
- Asked to connect or build a tool? Run `add-integration`: it checks the
  catalog first and wires with the script when the vendor is there. One PR,
  with the guide's checklist in its description.
