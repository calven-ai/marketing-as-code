# agents/: the workforce roster

**Kind:** agents, the workforce as instructions in English.

Every agent and skill in this repo, what it does, and what it needs. The
definitions live in [`.agents/skills/`](../.agents/skills/), where Claude
Code, Cursor and Codex all find them. Invoke one by slash command
(`/setup`) or ask in plain English.

The tables are generated from each skill's `description` and `metadata`
(`python3 scripts/lint.py --fix` refreshes them). Edit the skill, not the
table.

## Roles (recurring specialists)

<!-- generated:skills-roles -->
| Agent | What it does | Needs |
| --- | --- | --- |
| [brand-monitor](../.agents/skills/brand-monitor/SKILL.md) | Track how AI answer engines and LLMs mention us and our competitors, using the DataForSEO MCP's AI optimization and LLM mentions tools against the prompt set in data/seo/prompts.csv | DataForSEO MCP |
| [chief-of-staff](../.agents/skills/chief-of-staff/SKILL.md) | Process meeting transcripts from memory/transcripts/inbox/ into facts, decisions, project status updates, action items per owner, and risks and red flags | nothing (task tool and Slack optional) |
| [prototype-builder](../.agents/skills/prototype-builder/SKILL.md) | Build a disposable prototype in playgrounds/ from a one-sentence idea | nothing |
| [researcher](../.agents/skills/researcher/SKILL.md) | ABM account research with Apify actors through the official Apify MCP: people at or formerly at target accounts, company signals, social activity, saved as dated snapshots in data/accounts/ | Apify MCP |
| [seo-analyst](../.agents/skills/seo-analyst/SKILL.md) | Keyword and ranking analysis against data/seo/keywords.csv using the DataForSEO MCP | DataForSEO MCP |
<!-- /generated:skills-roles -->

## Workflows (invokable procedures)

<!-- generated:skills-workflows -->
| Skill | What it does | Needs |
| --- | --- | --- |
| [add-integration](../.agents/skills/add-integration/SKILL.md) | Connect a tool the team uses to this repo | nothing; the tool's own auth at first use |
| [campaign-discovery](../.agents/skills/campaign-discovery/SKILL.md) | Run discovery for a campaign idea given in one sentence. Composes the competitive angle, keyword volumes and current ranks, AI answer-engine prompt coverage, and an inventory of existing content into one report in reports/adhoc/ | DataForSEO MCP for the data parts; works partially without |
| [log-decision](../.agents/skills/log-decision/SKILL.md) | Record a decision in memory/decision-log.md | nothing |
| [make-dashboard](../.agents/skills/make-dashboard/SKILL.md) | Turn data into a self-contained HTML dashboard saved beside its report | nothing |
| [new-content](../.agents/skills/new-content/SKILL.md) | Scaffold a new piece of content in content/ | nothing |
| [new-project](../.agents/skills/new-project/SKILL.md) | Scaffold a project or campaign folder in projects/ | nothing |
| [qmr](../.agents/skills/qmr/SKILL.md) | Assemble the Quarterly Marketing Review | integrations help, not required |
| [review](../.agents/skills/review/SKILL.md) | Pre-publish review of a content draft against strategy, messaging, and brand voice | nothing |
| [setup](../.agents/skills/setup/SKILL.md) | Onboard a team into this repo | nothing |
<!-- /generated:skills-workflows -->

"Needs: nothing" means it works offline out of the box. Integration setup
is in [`integrations/`](../integrations/). Keys never live in this repo
([docs/secrets.md](../docs/secrets.md)).

## Running them, and adding your own

A person runs these in a coding agent by default. The recurring ones can
also run unattended in GitHub Actions; the trade-off is in
[docs/operating-model.md](../docs/operating-model.md).

An agent this roster lacks (a web analyst, a weekly ranking diff, a
newsletter assembler) is a Markdown file you add at
`.agents/skills/<name>/SKILL.md` in the same shape, followed by
`python3 scripts/sync_skills.py`. Its tool is wired per
[integrations/adding-an-integration.md](../integrations/adding-an-integration.md).
Skills others could reuse are welcome upstream
([CONTRIBUTING.md](../CONTRIBUTING.md)).
