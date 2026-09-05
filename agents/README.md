# agents/: the workforce roster

**Kind:** agents, the workforce as instructions in English.

Every agent and skill in this repo, what it does, and what it needs. The
definitions live in [`.agents/skills/`](../.agents/skills/). Cursor and
Codex read that folder directly; Claude Code reads the same files through
the symlinks in `.claude/skills/`. Run one by slash command in Claude Code
(`/setup`), by `$setup` in Codex, or ask for it in plain English anywhere.

The tables are generated from each skill's `description` and `metadata`
(`python3 scripts/lint.py --fix` refreshes them). Edit the skill, not the
table. A **role** is a recurring specialist with a cadence; a **workflow**
is a procedure you run once. The **Needs** column names integration
categories, never vendors: which vendor fills each category in this repo
is the Wired table in [`integrations/README.md`](../integrations/README.md),
and the catalog of vendors per category is
[`integrations/catalog/README.md`](../integrations/catalog/README.md).
"nothing" means the skill works offline, from the repo alone; "(optional:
…)" means it does more with that category wired and degrades to a repo-only
path without it. Keys never live in this repo
([docs/secrets.md](../docs/secrets.md)).

## Core: the repo lifecycle

<!-- generated:skills-core -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [add-integration](../.agents/skills/add-integration/SKILL.md) | workflow | Connect a tool the team uses to this repo | nothing |
| [doctor](../.agents/skills/doctor/SKILL.md) | workflow | Say what is wrong with this checkout in plain words and fix what is safe | nothing |
| [log-decision](../.agents/skills/log-decision/SKILL.md) | workflow | Record a decision in memory/decision-log.md | nothing |
| [make-dashboard](../.agents/skills/make-dashboard/SKILL.md) | workflow | Turn data into a self-contained HTML dashboard saved beside its report, or a spec for the team's BI tool | nothing (optional: [warehouse-bi](../integrations/catalog/README.md#warehouse-bi)) |
| [new-content](../.agents/skills/new-content/SKILL.md) | workflow | Scaffold a new piece of content in content/ | nothing |
| [new-project](../.agents/skills/new-project/SKILL.md) | workflow | Scaffold a project or campaign folder in projects/ | nothing (optional: [tasks](../integrations/catalog/README.md#tasks)) |
| [propose](../.agents/skills/propose/SKILL.md) | workflow | Turn what changed into a proposal (a pull request) and hand back the link | nothing |
| [prototype-builder](../.agents/skills/prototype-builder/SKILL.md) | workflow | Build a disposable prototype in playgrounds/ from a one-sentence idea | nothing |
| [setup](../.agents/skills/setup/SKILL.md) | workflow | Onboard a team into this repo | nothing (optional: [context-layer](../integrations/catalog/README.md#context-layer), [tasks](../integrations/catalog/README.md#tasks)) |
| [sync](../.agents/skills/sync/SKILL.md) | workflow | Bring in the latest approved copy and say what is waiting on you | nothing |
<!-- /generated:skills-core -->

## Product marketing

<!-- generated:skills-product-marketing -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [competitor-watch](../.agents/skills/competitor-watch/SKILL.md) | role (monthly) | Track what changed on each competitor's pricing, positioning, product and ad-library pages since last month and flag battlecards to refresh | nothing (optional: [scraping-search](../integrations/catalog/README.md#scraping-search)) |
| [battlecard](../.agents/skills/battlecard/SKILL.md) | workflow | Write or refresh a competitor battlecard in strategy/competitive/ from the template | nothing (optional: [seo-data](../integrations/catalog/README.md#seo-data), [context-layer](../integrations/catalog/README.md#context-layer)) |
| [comparison-page](../.agents/skills/comparison-page/SKILL.md) | workflow | Write a fair "us vs Acme" or "alternatives to Acme" page from the battlecard and the keyword table | nothing (optional: [seo-data](../integrations/catalog/README.md#seo-data)) |
| [icp-refresh](../.agents/skills/icp-refresh/SKILL.md) | workflow | Test the ICP and its tier definitions against who actually buys, stays and churns, and propose changes to strategy/icp.md | nothing (optional: [crm](../integrations/catalog/README.md#crm), [context-layer](../integrations/catalog/README.md#context-layer)) |
| [launch-plan](../.agents/skills/launch-plan/SKILL.md) | workflow | Plan a product or feature launch: tier, narrative, channel plan, asset list and owners, as a project folder plus content stubs | nothing (optional: [tasks](../integrations/catalog/README.md#tasks)) |
| [messaging-house](../.agents/skills/messaging-house/SKILL.md) | workflow | Build or refresh the messaging framework in strategy/messaging.md: pillars, proof, claims per persona and buying stage | nothing (optional: [context-layer](../integrations/catalog/README.md#context-layer)) |
| [persona-builder](../.agents/skills/persona-builder/SKILL.md) | workflow | Write or refresh a persona in strategy/personas.md from interviews, CRM facts and customer language, never from stereotypes | nothing (optional: [transcripts](../integrations/catalog/README.md#transcripts), [context-layer](../integrations/catalog/README.md#context-layer)) |
| [positioning-refresh](../.agents/skills/positioning-refresh/SKILL.md) | workflow | Propose a reviewed update to strategy/positioning.md from decisions, win/loss and competitive evidence, with the list of files that inherit the change | nothing (optional: [context-layer](../integrations/catalog/README.md#context-layer)) |
| [release-notes-to-marketing](../.agents/skills/release-notes-to-marketing/SKILL.md) | workflow | Turn a product changelog into customer-facing copy: what changed, why it matters per persona, as email, post and blog drafts | nothing |
| [sales-enablement-kit](../.agents/skills/sales-enablement-kit/SKILL.md) | workflow | Write sales or partner collateral: one-pager, pitch narrative, objection handling, demo talk track, partner kit | nothing (optional: [docs](../integrations/catalog/README.md#docs)) |
| [win-loss](../.agents/skills/win-loss/SKILL.md) | workflow | Synthesise why deals were won and lost this period from closed deals and call transcripts, by competitor, segment and reason | [crm](../integrations/catalog/README.md#crm) (optional: [transcripts](../integrations/catalog/README.md#transcripts)) |
<!-- /generated:skills-product-marketing -->

## Content

<!-- generated:skills-content -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [case-study](../.agents/skills/case-study/SKILL.md) | workflow | Write a customer case study or quote pack from a call transcript and verified numbers, with a quote-approval checklist | nothing (optional: [transcripts](../integrations/catalog/README.md#transcripts)) |
| [content-brief](../.agents/skills/content-brief/SKILL.md) | workflow | Fill a content brief: argument, persona, keyword and SERP outline, sources, distribution; or a refresh brief for a decaying piece | nothing (optional: [seo-data](../integrations/catalog/README.md#seo-data)) |
| [content-calendar](../.agents/skills/content-calendar/SKILL.md) | workflow | Build or refresh the editorial and social calendar from what is in flight, launches and events, one row per piece and channel | nothing (optional: [tasks](../integrations/catalog/README.md#tasks)) |
| [content-inventory](../.agents/skills/content-inventory/SKILL.md) | workflow | List what content exists by channel, status, owner, age and topic, and what could be reused or must not be duplicated | nothing |
| [content-strategy](../.agents/skills/content-strategy/SKILL.md) | workflow | Decide what content to make next quarter: pillars, clusters, formats and gaps against keywords, AI prompts and the inventory | nothing (optional: [seo-data](../integrations/catalog/README.md#seo-data), [ai-visibility](../integrations/catalog/README.md#ai-visibility)) |
| [edit-copy](../.agents/skills/edit-copy/SKILL.md) | workflow | Line-edit a draft: tighten, cut filler, remove AI tells, keep the argument and voice | nothing |
| [repurpose](../.agents/skills/repurpose/SKILL.md) | workflow | Turn one published piece into channel variants and an employee-advocacy pack | nothing |
| [review](../.agents/skills/review/SKILL.md) | workflow | Pre-publish review of a content draft against strategy, messaging, and brand voice | nothing (optional: [context-layer](../integrations/catalog/README.md#context-layer)) |
| [write-draft](../.agents/skills/write-draft/SKILL.md) | workflow | Write the draft from its brief in the team's voice, for any channel including email and community replies | nothing (optional: [context-layer](../integrations/catalog/README.md#context-layer)) |
<!-- /generated:skills-content -->

## Organic search

<!-- generated:skills-seo -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [content-decay-monitor](../.agents/skills/content-decay-monitor/SKILL.md) | role (monthly) | Find published pages losing rank or organic traffic month over month and rank them for refresh | [seo-data](../integrations/catalog/README.md#seo-data) (optional: [web-analytics](../integrations/catalog/README.md#web-analytics)) |
| [seo-analyst](../.agents/skills/seo-analyst/SKILL.md) | role (weekly) | Keyword and ranking analysis against data/seo/keywords.csv through the wired seo-data integration | [seo-data](../integrations/catalog/README.md#seo-data) |
| [backlink-analysis](../.agents/skills/backlink-analysis/SKILL.md) | workflow | Profile our backlinks and the gap versus competitors, with link targets worth pursuing | [seo-data](../integrations/catalog/README.md#seo-data) |
| [keyword-cluster](../.agents/skills/keyword-cluster/SKILL.md) | workflow | Group keywords by intent into pillar and spoke clusters mapped to existing or proposed pages | [seo-data](../integrations/catalog/README.md#seo-data) |
| [on-page-optimize](../.agents/skills/on-page-optimize/SKILL.md) | workflow | Optimise one page or draft for its target keyword: title, meta, headings, entities, internal links and schema | nothing (optional: [seo-data](../integrations/catalog/README.md#seo-data)) |
| [seo-roadmap](../.agents/skills/seo-roadmap/SKILL.md) | workflow | Turn audits, clusters and decay into a quarter-by-quarter SEO plan with owners and metrics | nothing (optional: [seo-data](../integrations/catalog/README.md#seo-data)) |
| [seo-technical-audit](../.agents/skills/seo-technical-audit/SKILL.md) | workflow | Audit crawlability, indexation, speed, on-page basics, orphan pages, schema and AI-readiness (llms.txt) as a prioritised fix list | nothing (optional: [seo-data](../integrations/catalog/README.md#seo-data), [scraping-search](../integrations/catalog/README.md#scraping-search)) |
<!-- /generated:skills-seo -->

## AI visibility

<!-- generated:skills-aeo -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [brand-monitor](../.agents/skills/brand-monitor/SKILL.md) | role (monthly) | Track how AI answer engines and LLMs mention us and our competitors through the wired ai-visibility integration, against the prompt set in data/seo/prompts.csv | [ai-visibility](../integrations/catalog/README.md#ai-visibility) |
| [aeo-page-optimize](../.agents/skills/aeo-page-optimize/SKILL.md) | workflow | Make a page citable by answer engines: direct answers, question headings, entities, passage structure, proof | nothing (optional: [ai-visibility](../integrations/catalog/README.md#ai-visibility)) |
| [ai-share-of-voice](../.agents/skills/ai-share-of-voice/SKILL.md) | workflow | Compute share of voice in AI answers versus competitors across the prompt set and over time | [ai-visibility](../integrations/catalog/README.md#ai-visibility) |
| [prompt-set-builder](../.agents/skills/prompt-set-builder/SKILL.md) | workflow | Propose buyer prompts for data/seo/prompts.csv per persona and buying stage, never rewriting existing ones | nothing |
<!-- /generated:skills-aeo -->

## Social

<!-- generated:skills-social -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [social-listening](../.agents/skills/social-listening/SKILL.md) | role (weekly) | Track brand, competitor and category mentions on LinkedIn, X, Reddit and forums and surface buyer questions and red flags | nothing (optional: [scraping-search](../integrations/catalog/README.md#scraping-search), [social](../integrations/catalog/README.md#social), [chat](../integrations/catalog/README.md#chat)) |
| [social-performance](../.agents/skills/social-performance/SKILL.md) | role (monthly) | Report what worked on social this month by post type, hook and topic, and update what-resonates knowledge | [social](../integrations/catalog/README.md#social) |
| [social-post](../.agents/skills/social-post/SKILL.md) | workflow | Write a LinkedIn or X post in the company or an exec voice with hook, body and CTA | nothing |
<!-- /generated:skills-social -->

## Demand generation and paid

<!-- generated:skills-paid -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [ads-performance](../.agents/skills/ads-performance/SKILL.md) | role (weekly) | Weekly paid report: spend, CPL, CAC and pipeline by campaign versus target, with what to pause or scale | [ads](../integrations/catalog/README.md#ads) (optional: [crm](../integrations/catalog/README.md#crm)) |
| [budget-pacing](../.agents/skills/budget-pacing/SKILL.md) | role (weekly) | Spend versus plan by campaign and program, month to date and projected, with over and under alerts | nothing (optional: [ads](../integrations/catalog/README.md#ads), [chat](../integrations/catalog/README.md#chat)) |
| [ab-test-plan](../.agents/skills/ab-test-plan/SKILL.md) | workflow | Design an A/B test: hypothesis, primary metric per the ontology, sample size, duration, stop rule; record the result later | nothing (optional: [web-analytics](../integrations/catalog/README.md#web-analytics)) |
| [ad-brief](../.agents/skills/ad-brief/SKILL.md) | workflow | Write ad angles and copy variants per platform and persona for a campaign | nothing |
| [ads-account-audit](../.agents/skills/ads-account-audit/SKILL.md) | workflow | Audit a paid account against a checklist: structure, wasted spend, targeting, conversion tracking, creative fatigue | [ads](../integrations/catalog/README.md#ads) |
| [campaign-discovery](../.agents/skills/campaign-discovery/SKILL.md) | workflow | Run discovery for a campaign idea given in one sentence. Composes the competitive angle, keyword volumes and current ranks, AI answer-engine prompt coverage, and an inventory of existing content into one report in reports/adhoc/ | nothing (optional: [seo-data](../integrations/catalog/README.md#seo-data), [ai-visibility](../integrations/catalog/README.md#ai-visibility)) |
| [campaign-plan](../.agents/skills/campaign-plan/SKILL.md) | workflow | Turn a discovery report into a campaign: narrative, channels including retargeting audiences, budget, calendar, KPIs and owners | nothing (optional: [tasks](../integrations/catalog/README.md#tasks)) |
| [cro-audit](../.agents/skills/cro-audit/SKILL.md) | workflow | Diagnose why a page or flow under-converts and rank hypotheses to test | nothing (optional: [web-analytics](../integrations/catalog/README.md#web-analytics)) |
| [landing-page](../.agents/skills/landing-page/SKILL.md) | workflow | Write landing page copy for a campaign and mock it as a prototype | nothing (optional: [design](../integrations/catalog/README.md#design)) |
<!-- /generated:skills-paid -->

## Email and lifecycle

<!-- generated:skills-email -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [email-performance](../.agents/skills/email-performance/SKILL.md) | role (monthly) | Monthly email report by send and sequence: engagement, replies, unsubscribes, bounces and deliverability health | [marketing-automation](../integrations/catalog/README.md#marketing-automation) |
| [lifecycle-map](../.agents/skills/lifecycle-map/SKILL.md) | workflow | Map every automated email to a lifecycle stage and list gaps and overlaps | nothing (optional: [marketing-automation](../integrations/catalog/README.md#marketing-automation)) |
| [newsletter](../.agents/skills/newsletter/SKILL.md) | workflow | Assemble the monthly newsletter, prospect or customer edition, from what shipped, was published and was decided | nothing |
| [nurture-sequence](../.agents/skills/nurture-sequence/SKILL.md) | workflow | Design a nurture, onboarding or post-event sequence: emails, timing, triggers, exits, each linking existing content | nothing (optional: [marketing-automation](../integrations/catalog/README.md#marketing-automation)) |
<!-- /generated:skills-email -->

## Pipeline and ABM

<!-- generated:skills-pipeline -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [account-signals](../.agents/skills/account-signals/SKILL.md) | role (weekly) | Weekly account heat: intent, web and CRM engagement per target account with buying-group coverage and who to hand to sales | [crm](../integrations/catalog/README.md#crm) (optional: [intent](../integrations/catalog/README.md#intent), [web-analytics](../integrations/catalog/README.md#web-analytics)) |
| [researcher](../.agents/skills/researcher/SKILL.md) | role (on-demand) | ABM account research through the wired scraping and enrichment tools: people at or formerly at target accounts, company signals, social activity, saved as dated snapshots in data/accounts/; or a pre-call account brief from those snapshots plus CRM history | [scraping-search](../integrations/catalog/README.md#scraping-search) (optional: [crm](../integrations/catalog/README.md#crm), [enrichment](../integrations/catalog/README.md#enrichment)) |
| [closed-lost-revival](../.agents/skills/closed-lost-revival/SKILL.md) | workflow | Quarterly sweep of closed-lost deals, gone-quiet proposals and champions who changed jobs, ranked for re-approach | [crm](../integrations/catalog/README.md#crm) (optional: [enrichment](../integrations/catalog/README.md#enrichment), [outbound](../integrations/catalog/README.md#outbound)) |
| [lead-lifecycle-spec](../.agents/skills/lead-lifecycle-spec/SKILL.md) | workflow | Define or revise lead scoring, routing and the MQL-to-SDR handoff with SLAs, as an ontology proposal | nothing (optional: [crm](../integrations/catalog/README.md#crm), [marketing-automation](../integrations/catalog/README.md#marketing-automation)) |
| [outbound-sequence](../.agents/skills/outbound-sequence/SKILL.md) | workflow | Write an outbound sequence for a persona and signal with personalisation slots and follow-ups | nothing (optional: [outbound](../integrations/catalog/README.md#outbound)) |
| [target-account-list](../.agents/skills/target-account-list/SKILL.md) | workflow | Build or enrich the target account list by ICP tier with firmographics, excluding customers and lost accounts | nothing (optional: [enrichment](../integrations/catalog/README.md#enrichment), [crm](../integrations/catalog/README.md#crm)) |
<!-- /generated:skills-pipeline -->

## Events and webinars

<!-- generated:skills-events -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [event-followup](../.agents/skills/event-followup/SKILL.md) | workflow | Turn an attendee list into tiered follow-ups within 48 hours: who gets what, drafts, CRM import spec, owner tasks | nothing (optional: [events](../integrations/catalog/README.md#events), [crm](../integrations/catalog/README.md#crm), [tasks](../integrations/catalog/README.md#tasks)) |
| [event-plan](../.agents/skills/event-plan/SKILL.md) | workflow | Plan a webinar, sponsorship, speaking slot or attended event: goal, target accounts, funnel, assets, ROI model, CFP if speaking | nothing (optional: [events](../integrations/catalog/README.md#events), [tasks](../integrations/catalog/README.md#tasks)) |
<!-- /generated:skills-events -->

## PR and analyst relations

<!-- generated:skills-pr -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [coverage-tracker](../.agents/skills/coverage-tracker/SKILL.md) | role (monthly) | Monthly press and podcast coverage of us and competitors with share of voice and notable pieces | nothing (optional: [pr-media](../integrations/catalog/README.md#pr-media), [scraping-search](../integrations/catalog/README.md#scraping-search)) |
| [analyst-brief](../.agents/skills/analyst-brief/SKILL.md) | workflow | Prepare an analyst briefing: narrative, proof, competitive stance, likely questions | nothing (optional: [docs](../integrations/catalog/README.md#docs)) |
| [media-outreach](../.agents/skills/media-outreach/SKILL.md) | workflow | Build the journalist and outlet list for a story and write the pitches, never sending | nothing (optional: [pr-media](../integrations/catalog/README.md#pr-media), [scraping-search](../integrations/catalog/README.md#scraping-search)) |
| [press-release](../.agents/skills/press-release/SKILL.md) | workflow | Write a press release, announcement or holding statement with approved quotes and a boilerplate | nothing |
<!-- /generated:skills-pr -->

## Partner marketing

<!-- generated:skills-partner -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [co-marketing-plan](../.agents/skills/co-marketing-plan/SKILL.md) | workflow | Plan a joint campaign with a partner: assets, split of work, timeline, shared metrics | nothing (optional: [tasks](../integrations/catalog/README.md#tasks)) |
| [partner-scan](../.agents/skills/partner-scan/SKILL.md) | workflow | Find and rank co-marketing and integration partner candidates by ICP overlap and reach | nothing (optional: [enrichment](../integrations/catalog/README.md#enrichment)) |
<!-- /generated:skills-partner -->

## Community

<!-- generated:skills-community -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [community-digest](../.agents/skills/community-digest/SKILL.md) | role (weekly) | Weekly digest of community threads: top questions, feature requests, churn signals, threads needing an answer | [community](../integrations/catalog/README.md#community) (optional: [chat](../integrations/catalog/README.md#chat)) |
| [community-plan](../.agents/skills/community-plan/SKILL.md) | workflow | Decide whether and how to run a community: platform, rituals, moderation, metrics | nothing (optional: [community](../integrations/catalog/README.md#community)) |
<!-- /generated:skills-community -->

## Customer marketing

<!-- generated:skills-customer -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [churn-signals](../.agents/skills/churn-signals/SKILL.md) | role (weekly) | Weekly at-risk list: usage drops, renewals inside 120 days, support spikes, with the save lever per account | [crm](../integrations/catalog/README.md#crm) (optional: [billing](../integrations/catalog/README.md#billing), [web-analytics](../integrations/catalog/README.md#web-analytics), [chat](../integrations/catalog/README.md#chat)) |
| [review-monitor](../.agents/skills/review-monitor/SKILL.md) | role (monthly) | Monthly review-site report: ratings, themes, competitor comparison, quotable lines | [surveys-reviews](../integrations/catalog/README.md#surveys-reviews) |
| [advocacy-program](../.agents/skills/advocacy-program/SKILL.md) | workflow | Run the reviews-and-references program: who to ask, for what, with drafts and a reference roster | [crm](../integrations/catalog/README.md#crm) (optional: [surveys-reviews](../integrations/catalog/README.md#surveys-reviews)) |
| [expansion-play](../.agents/skills/expansion-play/SKILL.md) | workflow | Find customers ready for expansion by usage, whitespace and contract timing | [crm](../integrations/catalog/README.md#crm) (optional: [billing](../integrations/catalog/README.md#billing), [web-analytics](../integrations/catalog/README.md#web-analytics)) |
| [voice-of-customer](../.agents/skills/voice-of-customer/SKILL.md) | workflow | Synthesise interviews, surveys, NPS and reviews into themes, verbatims and proposed persona or messaging changes; or design the survey | nothing (optional: [transcripts](../integrations/catalog/README.md#transcripts), [surveys-reviews](../integrations/catalog/README.md#surveys-reviews)) |
<!-- /generated:skills-customer -->

## Marketing operations

<!-- generated:skills-ops -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [data-hygiene-audit](../.agents/skills/data-hygiene-audit/SKILL.md) | role (monthly) | Monthly CRM hygiene: duplicates, missing fields, bad lifecycle stages, orphan records, with a fix list | [crm](../integrations/catalog/README.md#crm) |
| [pipeline-report](../.agents/skills/pipeline-report/SKILL.md) | role (weekly) | Weekly funnel and pipeline report: stage conversion, velocity, marketing-sourced and influenced pipeline versus target; the monthly run adds a quarter forecast | [crm](../integrations/catalog/README.md#crm) (optional: [warehouse-bi](../integrations/catalog/README.md#warehouse-bi)) |
| [attribution-analysis](../.agents/skills/attribution-analysis/SKILL.md) | workflow | Compare first-touch, last-touch and multi-touch views of which channels drive pipeline, and propose the model to standardise on | [crm](../integrations/catalog/README.md#crm), [web-analytics](../integrations/catalog/README.md#web-analytics) (optional: [ads](../integrations/catalog/README.md#ads), [warehouse-bi](../integrations/catalog/README.md#warehouse-bi)) |
| [martech-audit](../.agents/skills/martech-audit/SKILL.md) | workflow | Inventory the marketing stack: what is paid for, connected, used, and what could be wired or dropped | nothing |
| [program-retro](../.agents/skills/program-retro/SKILL.md) | workflow | Retro a launch, event or campaign two to eight weeks after: results versus goal, what worked, playbook updates | nothing (optional: [crm](../integrations/catalog/README.md#crm), [web-analytics](../integrations/catalog/README.md#web-analytics), [ads](../integrations/catalog/README.md#ads)) |
| [snapshot-pull](../.agents/skills/snapshot-pull/SKILL.md) | workflow | Pull one named snapshot from a wired integration into data/<domain>/snapshots/, or say exactly which export to drop there | nothing (optional: [crm](../integrations/catalog/README.md#crm), [web-analytics](../integrations/catalog/README.md#web-analytics), [ads](../integrations/catalog/README.md#ads), [marketing-automation](../integrations/catalog/README.md#marketing-automation), [seo-data](../integrations/catalog/README.md#seo-data), [social](../integrations/catalog/README.md#social), [surveys-reviews](../integrations/catalog/README.md#surveys-reviews), [events](../integrations/catalog/README.md#events), [billing](../integrations/catalog/README.md#billing)) |
| [tracking-spec](../.agents/skills/tracking-spec/SKILL.md) | workflow | Define an event or audit implemented events against the ontology and list gaps | nothing (optional: [web-analytics](../integrations/catalog/README.md#web-analytics)) |
| [utm-builder](../.agents/skills/utm-builder/SKILL.md) | workflow | Generate UTM links for a campaign that pass the naming rules in data/ontology/naming.md | nothing |
<!-- /generated:skills-ops -->

## Web

<!-- generated:skills-web -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [web-analyst](../.agents/skills/web-analyst/SKILL.md) | role (weekly) | Weekly web report: traffic by source, conversions, top pages, deltas; the monthly run adds page performance and non-conforming UTMs | [web-analytics](../integrations/catalog/README.md#web-analytics) |
| [publish](../.agents/skills/publish/SKILL.md) | workflow | Move an approved draft to published: set frontmatter in a PR, stage it as a CMS draft or scheduled post when wired, and list distribution steps | nothing (optional: [cms](../integrations/catalog/README.md#cms), [social](../integrations/catalog/README.md#social)) |
| [site-architecture](../.agents/skills/site-architecture/SKILL.md) | workflow | Plan page hierarchy, navigation, URL structure and redirects for a section or the whole site | nothing (optional: [seo-data](../integrations/catalog/README.md#seo-data), [cms](../integrations/catalog/README.md#cms)) |
| [web-copy-audit](../.agents/skills/web-copy-audit/SKILL.md) | workflow | Review the homepage, pricing and key pages against positioning, messaging and voice | nothing |
<!-- /generated:skills-web -->

## Brand

<!-- generated:skills-brand -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [design-qa](../.agents/skills/design-qa/SKILL.md) | workflow | Check an asset against the visual identity and tokens, or write the design brief for a missing one | nothing (optional: [design](../integrations/catalog/README.md#design)) |
| [voice-refresh](../.agents/skills/voice-refresh/SKILL.md) | workflow | Refresh brand/voice.md from the pieces that worked and the recurring review findings, with the cascade listed | nothing |
<!-- /generated:skills-brand -->

## Leadership and planning

<!-- generated:skills-leadership -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [chief-of-staff](../.agents/skills/chief-of-staff/SKILL.md) | role (on-demand) | Process meeting transcripts from memory/transcripts/inbox/ into facts, decisions, project status updates, action items per owner, and risks and red flags | nothing (optional: [transcripts](../integrations/catalog/README.md#transcripts), [tasks](../integrations/catalog/README.md#tasks), [chat](../integrations/catalog/README.md#chat)) |
| [context-freshness](../.agents/skills/context-freshness/SKILL.md) | role (monthly) | Monthly judgment pass on context: files past 90 days, contradictions between strategy, knowledge and the decision log, and which refresh to run | nothing (optional: [context-layer](../integrations/catalog/README.md#context-layer)) |
| [project-status-roundup](../.agents/skills/project-status-roundup/SKILL.md) | role (weekly) | Weekly pass over every project: propose a status entry from tasks and reports, flag projects with no update in 14 days | nothing (optional: [tasks](../integrations/catalog/README.md#tasks)) |
| [weekly-report](../.agents/skills/weekly-report/SKILL.md) | role (weekly) | Friday digest and month-end review: what shipped, headline numbers with deltas, risks, decisions needed, next week | nothing (optional: [chat](../integrations/catalog/README.md#chat), [tasks](../integrations/catalog/README.md#tasks)) |
| [marketing-plan](../.agents/skills/marketing-plan/SKILL.md) | workflow | Draft the annual plan and quarterly OKRs: targets per ontology metric, programs, budget, owners | nothing |
| [meeting-prep](../.agents/skills/meeting-prep/SKILL.md) | workflow | Prepare for a meeting: agenda from project status, open decisions, numbers, last meeting's actions | nothing (optional: [tasks](../integrations/catalog/README.md#tasks), [docs](../integrations/catalog/README.md#docs)) |
| [qmr](../.agents/skills/qmr/SKILL.md) | workflow | Assemble the Quarterly Marketing Review | nothing (optional: [crm](../integrations/catalog/README.md#crm), [web-analytics](../integrations/catalog/README.md#web-analytics), [ads](../integrations/catalog/README.md#ads), [marketing-automation](../integrations/catalog/README.md#marketing-automation), [seo-data](../integrations/catalog/README.md#seo-data)) |
<!-- /generated:skills-leadership -->

## Running them, and adding your own

A person runs these in a coding agent by default. A role whose every
category is wired to a key-based server or a script can also run unattended
in GitHub Actions through `.github/workflows/role-run.yml`; the trade-off
and the opt-in are in [docs/operating-model.md](../docs/operating-model.md).

A skill this roster lacks is a Markdown file you add at
`.agents/skills/<name>/SKILL.md` in the shape of
[docs/skill-authoring.md](../docs/skill-authoring.md), followed by
`python3 scripts/sync_skills.py`. Its tool is wired per
[integrations/adding-an-integration.md](../integrations/adding-an-integration.md).
Skills others could reuse are welcome upstream
([CONTRIBUTING.md](../CONTRIBUTING.md)).
