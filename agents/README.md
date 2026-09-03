# agents/: the workforce roster

**Kind:** agents, the workforce as instructions in English.

Every agent and skill in this repo, what it does, and what it needs. This
page is the index for humans; the definitions any coding agent actually loads
live in [`.agents/skills/`](../.agents/skills/) (the Agent Skills open
standard: Cursor, Codex, and friends discover them there automatically;
Claude Code reads the same files via `.claude/skills/` symlinks).

Invoke any of these by slash command (`/setup`) in tools that support it, or
just ask in plain English; the descriptions are written so your agent routes
correctly.

## Roles (recurring specialists)

| Agent | What it does | Needs |
| --- | --- | --- |
| [chief-of-staff](../.agents/skills/chief-of-staff/SKILL.md) | Processes meeting transcripts: facts → knowledge diffs, decisions → log, project status → `status.md`, action items per owner → your task tool, risks and red flags → summary and the leadership Slack channel | nothing (task tool and Slack optional) |
| [prototype-builder](../.agents/skills/prototype-builder/SKILL.md) | Builds a disposable prototype in `playgrounds/` from one sentence, on-brand | nothing |
| [seo-analyst](../.agents/skills/seo-analyst/SKILL.md) | Keyword volumes, difficulty, current ranks, and SERP competitors against `data/seo/keywords.csv`; every pull saved as a snapshot, analysis in `reports/` | DataForSEO MCP |
| [brand-monitor](../.agents/skills/brand-monitor/SKILL.md) | AI answer-engine (AEO) and LLM mention tracking for the prompt set in `data/seo/prompts.csv`: who is cited, and whether we are, in `reports/recurring/mentions/` | DataForSEO MCP |
| [researcher](../.agents/skills/researcher/SKILL.md) | ABM account research with Apify actors (people at or formerly at target accounts, company signals) saved to `data/accounts/snapshots/`; private repo only, never contacts anyone | Apify MCP |

## Workflows (invokable procedures)

| Skill | What it does | Needs |
| --- | --- | --- |
| [setup](../.agents/skills/setup/SKILL.md) | The onboarding interview: fills strategy, brand, and ontology; connects the wired integrations and lists the rest as follow-ups | nothing |
| [add-integration](../.agents/skills/add-integration/SKILL.md) | Connects a tool the team uses: picks the tier (MCP server, CLI, script) per `integrations/adding-an-integration.md` and delivers the integration as one PR | nothing; the tool's own auth at first use |
| [new-content](../.agents/skills/new-content/SKILL.md) | Scaffolds a content piece with wired frontmatter | nothing |
| [new-project](../.agents/skills/new-project/SKILL.md) | Scaffolds a project or campaign folder | nothing |
| [review](../.agents/skills/review/SKILL.md) | Pre-publish check of a draft against strategy, voice, and brand | nothing |
| [log-decision](../.agents/skills/log-decision/SKILL.md) | Appends a properly formatted entry to the decision log | nothing |
| [qmr](../.agents/skills/qmr/SKILL.md) | Assembles the quarterly marketing review: data checklist → snapshots → deltas → report + dashboard | integrations help, not required |
| [make-dashboard](../.agents/skills/make-dashboard/SKILL.md) | Turns data into a self-contained HTML dashboard beside its report | nothing |
| [campaign-discovery](../.agents/skills/campaign-discovery/SKILL.md) | From a one-sentence campaign idea: competitive angle, keyword volumes and ranks, AI answer-engine coverage, content inventory, into one report in `reports/adhoc/` with a "what we would need to produce" list | DataForSEO MCP for the data parts; works partially without |

"Needs: nothing" means it works offline out of the box. Integration setup
lives in [`integrations/`](../integrations/); keys never live in this repo
(see [docs/secrets.md](../docs/secrets.md)).

## Running them, and adding your own

Every one of these is run by a person in a coding agent by default. The
recurring ones (transcript processing, the keyword refresh, the mentions
report) can also run unattended in GitHub Actions if the team opts in;
[docs/operating-model.md](../docs/operating-model.md) has the trade-off and
a who-triggers-what table.

An agent this roster lacks (a web analyst on your analytics tool, a weekly
ranking diff, a newsletter assembler) is a Markdown file you add to
`.agents/skills/<name>/SKILL.md` in the same shape as these, followed by
`python3 scripts/sync_skills.py`. The tool it needs is added per
[integrations/adding-an-integration.md](../integrations/adding-an-integration.md).
Skills others could reuse are welcome upstream
([CONTRIBUTING.md](../CONTRIBUTING.md)).
