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
| [make-dashboard](../.agents/skills/make-dashboard/SKILL.md) | workflow | Turn data into a self-contained HTML dashboard saved beside its report | nothing (optional: [warehouse-bi](../integrations/catalog/README.md#warehouse-bi)) |
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
| [battlecard](../.agents/skills/battlecard/SKILL.md) | workflow | Write or refresh a competitor battlecard in strategy/competitive/ from the template | nothing (optional: [seo-data](../integrations/catalog/README.md#seo-data), [context-layer](../integrations/catalog/README.md#context-layer)) |
<!-- /generated:skills-product-marketing -->

## Content

<!-- generated:skills-content -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [review](../.agents/skills/review/SKILL.md) | workflow | Pre-publish review of a content draft against strategy, messaging, and brand voice | nothing (optional: [context-layer](../integrations/catalog/README.md#context-layer)) |
<!-- /generated:skills-content -->

## Organic search

<!-- generated:skills-seo -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [seo-analyst](../.agents/skills/seo-analyst/SKILL.md) | role (weekly) | Keyword and ranking analysis against data/seo/keywords.csv using the DataForSEO MCP | [seo-data](../integrations/catalog/README.md#seo-data) |
<!-- /generated:skills-seo -->

## AI visibility

<!-- generated:skills-aeo -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [brand-monitor](../.agents/skills/brand-monitor/SKILL.md) | role (monthly) | Track how AI answer engines and LLMs mention us and our competitors, using the DataForSEO MCP's AI optimization and LLM mentions tools against the prompt set in data/seo/prompts.csv | [ai-visibility](../integrations/catalog/README.md#ai-visibility) |
<!-- /generated:skills-aeo -->

## Social

<!-- generated:skills-social -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
<!-- /generated:skills-social -->

## Demand generation and paid

<!-- generated:skills-paid -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [campaign-discovery](../.agents/skills/campaign-discovery/SKILL.md) | workflow | Run discovery for a campaign idea given in one sentence. Composes the competitive angle, keyword volumes and current ranks, AI answer-engine prompt coverage, and an inventory of existing content into one report in reports/adhoc/ | nothing (optional: [seo-data](../integrations/catalog/README.md#seo-data), [ai-visibility](../integrations/catalog/README.md#ai-visibility)) |
<!-- /generated:skills-paid -->

## Email and lifecycle

<!-- generated:skills-email -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
<!-- /generated:skills-email -->

## Pipeline and ABM

<!-- generated:skills-pipeline -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [researcher](../.agents/skills/researcher/SKILL.md) | role (on-demand) | ABM account research with Apify actors through the official Apify MCP: people at or formerly at target accounts, company signals, social activity, saved as dated snapshots in data/accounts/ | [scraping-search](../integrations/catalog/README.md#scraping-search) (optional: [crm](../integrations/catalog/README.md#crm), [enrichment](../integrations/catalog/README.md#enrichment)) |
<!-- /generated:skills-pipeline -->

## Events and webinars

<!-- generated:skills-events -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
<!-- /generated:skills-events -->

## PR and analyst relations

<!-- generated:skills-pr -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
<!-- /generated:skills-pr -->

## Partner marketing

<!-- generated:skills-partner -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
<!-- /generated:skills-partner -->

## Community

<!-- generated:skills-community -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
<!-- /generated:skills-community -->

## Customer marketing

<!-- generated:skills-customer -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
<!-- /generated:skills-customer -->

## Marketing operations

<!-- generated:skills-ops -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
<!-- /generated:skills-ops -->

## Web

<!-- generated:skills-web -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
<!-- /generated:skills-web -->

## Brand

<!-- generated:skills-brand -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
<!-- /generated:skills-brand -->

## Leadership and planning

<!-- generated:skills-leadership -->
| Skill | Kind | What it does | Needs |
| --- | --- | --- | --- |
| [chief-of-staff](../.agents/skills/chief-of-staff/SKILL.md) | role (on-demand) | Process meeting transcripts from memory/transcripts/inbox/ into facts, decisions, project status updates, action items per owner, and risks and red flags | nothing (optional: [transcripts](../integrations/catalog/README.md#transcripts), [tasks](../integrations/catalog/README.md#tasks), [chat](../integrations/catalog/README.md#chat)) |
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
