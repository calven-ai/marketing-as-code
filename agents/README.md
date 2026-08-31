# agents/: the workforce roster

Every agent and skill in this repo, what it does, and what it needs. This
page is the index for humans; the definitions any coding agent actually loads
live in [`.agents/skills/`](../.agents/skills/) (the Agent Skills open
standard — Cursor, Codex, and friends discover them there automatically;
Claude Code reads the same files via `.claude/skills/` symlinks).

Invoke any of these by slash command (`/setup`) in tools that support it, or
just ask in plain English — the descriptions are written so your agent routes
correctly.

## Roles (recurring specialists)

| Agent | What it does | Needs |
| --- | --- | --- |
| [chief-of-staff](../.agents/skills/chief-of-staff/SKILL.md) | Processes meeting transcripts: decisions → log, action items → your task tool, doc updates as reviewable diffs | nothing (task tool optional) |
| [prototype-builder](../.agents/skills/prototype-builder/SKILL.md) | Builds a disposable prototype in `playgrounds/` from one sentence, on-brand | nothing |
| analyst *(wave 2)* | Routes any quantitative marketing question: snapshots → source pulls → ontology → answer | integrations |
| seo-analyst *(wave 2)* | Keyword & ranking analysis against `data/seo/keywords.csv` | DataForSEO |
| web-analyst *(wave 2)* | Web/product analytics snapshots and reports | GA4 / PostHog |
| brand-monitor *(wave 3)* | Brand & LLM/AEO mention tracking | DataForSEO |
| researcher *(wave 3)* | ABM account research via scraping | Apify |

## Workflows (invokable procedures)

| Skill | What it does | Needs |
| --- | --- | --- |
| [setup](../.agents/skills/setup/SKILL.md) | The onboarding interview: fills strategy, brand, and ontology; connects integrations | nothing |
| [new-content](../.agents/skills/new-content/SKILL.md) | Scaffolds a content piece with wired frontmatter | nothing |
| [new-project](../.agents/skills/new-project/SKILL.md) | Scaffolds a project or campaign folder | nothing |
| [review](../.agents/skills/review/SKILL.md) | Pre-publish check of a draft against strategy, voice, and brand | nothing |
| [log-decision](../.agents/skills/log-decision/SKILL.md) | Appends a properly formatted entry to the decision log | nothing |
| [qmr](../.agents/skills/qmr/SKILL.md) | Assembles the quarterly marketing review: data checklist → snapshots → deltas → report + dashboard | integrations help, not required |
| [make-dashboard](../.agents/skills/make-dashboard/SKILL.md) | Turns data into a self-contained HTML dashboard beside its report | nothing |
| weekly-seo *(wave 2)* | Diffs ranking snapshots into a delta report | DataForSEO |

"Needs: nothing" means it works offline out of the box. Integration setup
lives in [`integrations/`](../integrations/); keys never live in this repo
(see [docs/secrets.md](../docs/secrets.md)).
