# The operating model: where things run

There is no server. Nothing in this repo is deployed, hosted, or kept
alive. Work runs in one of three places, and for every recurring workflow
the team chooses between two of them. This page is that choice, written
down once so nobody has to guess.

## Three places things run

### 1. A person at a coding agent (the primary mode)

Someone opens the repo in a coding agent and types what they want. Claude
Code, in the terminal or inside the Claude desktop app, is what this repo
is tuned for; Cursor and Codex read the same `AGENTS.md` and skills. The
agent reaches everything: the skills in `.agents/skills/`, the MCP servers
in `.mcp.json`, the scripts in `scripts/`, and that person's own `.env`
and OAuth grants. The person triggers the work, watches it, and approves
what ships by merging the pull request.

This is how most of the work happens, and it is the mode to learn first:
the coding agent's window is the marketing team's main interface for
working in the repo, the way the CRM's window used to be. It costs the
person's coding-agent subscription and nothing more; no API key exists.

The chat surfaces (the Claude desktop app's chat with connectors, ChatGPT)
are stage 1 in [stages.md](stages.md): useful, but they run connectors,
not this repo's skills or scripts. A stage-3 team works in a coding agent.

### 2. GitHub Actions (the only unattended runtime)

The team already uses GitHub, so its runners are the one place something
can run with nobody watching. Two flavours:

- **Scripts only** (shipped, the default). A scheduled workflow runs a
  deterministic script and opens a pull request with the result; it never
  merges. Keys come from repository secrets
  ([secrets.md](secrets.md), tier 3). `transcripts-cron.yml` (Granola into
  the inbox, daily), `check.yml` (the health check on every proposal, which
  also approves bookkeeping proposals) and `housekeeping.yml` (the weekly
  tidy-up) are the shipped examples.
- **An agent in Actions** (opt-in). A workflow runs a Claude Code agent on
  a schedule or on a trigger, with a skill as its prompt, and the agent
  opens a pull request. It never merges, publishes, or sends. It needs an
  Anthropic API key as a repository secret and pays per token.
  `transcripts-process.yml` is the shipped example: it does nothing until
  the `ANTHROPIC_API_KEY` secret exists. Two limits in this mode: OAuth
  MCP servers cannot run headless, so only key-based servers and scripts
  work; and project MCP servers load without the usual prompt, which is
  why `.mcp.json` entries hold placeholders and never values.

### 3. A session a person starts from Slack or the cloud (optional)

Someone mentions the repo's agent in a Slack thread, or starts a cloud
session, and a coding-agent session opens on the repo, works, and posts a
summary and a PR link back. Layer 3 in
[integrations/slack/README.md](../integrations/slack/README.md);
availability depends on the plan. A person still starts it and still
merges.

## Two ways to run any recurring workflow

Every workflow that recurs (a meeting to process, a weekly keyword
refresh, the quarterly review) can be run by a person on demand or by
GitHub Actions on a schedule. Both are legitimate. The trade-off:

| | A person runs it | GitHub Actions runs it |
| --- | --- | --- |
| How | `/chief-of-staff` after the meeting; `/qmr` at quarter end; "refresh the keywords" on Monday | A cron or a trigger runs a script (shipped) or an agent (opt-in) and opens a PR |
| Cost | The coding-agent subscription the person already has; no API key | An API key as a repository secret, billed per token for agent runs; scripts cost nothing beyond the vendor's data bill |
| Latency | When someone remembers | Same day, every day; nobody has to remember |
| Human in the loop | By construction: the person watches the run and reads the diff | At review: the PR is the only checkpoint, so the PR description must carry the full summary |
| Integrations | Everything, including OAuth MCP servers authorized in the browser | Key-based only; integration keys also become repository secrets |
| Review load | The same: a PR either way for anything that cascades | The same |
| What can go wrong | It is not run | It runs on bad input with nobody watching; the PR catches it, if someone reads PRs |

**Recommendation.** Start with a person running everything; it is how
stage 2 in [stages.md](stages.md) already works ("a human still triggers
the agent, every time"), and it costs nothing extra. Automate the one
workflow whose latency actually hurts (for most teams that is transcript
processing: a meeting evaporates by Thursday if nobody processed it
Tuesday). Keep everything user-visible, and every strategy, brand, or
ontology change, in the hands of a person. Write the choice per workflow
in `memory/decision-log.md`.

## What never runs unattended

Whatever the mode, these need a person, every time (AGENTS.md rule 3,
[workflow.md](workflow.md)):

- Publishing content, sending email or Slack messages to people outside the
  team, changing the website.
- Deleting anything; completing, reassigning, or moving tasks in the task
  tool.
- Edits that cascade: `strategy/`, `brand/`, `data/ontology/`, pricing,
  and any published claim.
- Merging. Merging is the approval, and only a person merges.

## Who triggers what

| Workflow | A person, on demand | Unattended, in Actions |
| --- | --- | --- |
| Pull transcripts into the inbox | `python3 scripts/pull_transcripts.py` | `transcripts-cron.yml`, daily, opens a PR (shipped) |
| Process the inbox | `/chief-of-staff` after the meeting (the default) | `transcripts-process.yml`, on merge of an inbox PR, opens a PR (opt-in, needs `ANTHROPIC_API_KEY`) |
| Refresh keyword volumes and difficulty | `python3 scripts/seo_snapshot.py --update` | A cron step running the same script, yours to add |
| Rankings, SERP questions, keyword ideas | `/seo-analyst` (DataForSEO MCP) | Not headless; the script covers the scheduled part |
| AI answer-engine mentions | `/brand-monitor` | An agent-in-Actions workflow on a schedule, yours to add, or by hand |
| Quarterly review | `/qmr` | By hand: it needs the team's judgment and the exports it asks for |
| Account research | `/researcher` (Apify MCP, OAuth) | Not headless |
| Campaign discovery, content, review, prototypes, projects | Always a person | Never |
| Slack digests and alerts | `python3 scripts/slack_post.py` from a skill | Scheduled workflows calling the same script, yours to add; the message table is in `integrations/slack/README.md` |
| Health check | `python3 scripts/doctor.py` | `check.yml` on every proposal and on `main`: tests the lint, pushes the safe fixes, annotates, labels, and merges bookkeeping proposals (shipped) |
| Tidy the approved copy | `python3 scripts/doctor.py --fix` | `housekeeping.yml`, Mondays: the safe fixes as one bookkeeping proposal; stale proposals closed after three weeks (shipped) |
| Repository settings | `sh scripts/github_setup.sh`, then `python3 scripts/doctor.py --github` | Never; settings are applied once by an admin ([github-settings.md](github-settings.md)) |

When you add an integration or a workflow, add its row here and say both
modes where the workflow is described; the checklist in
[integrations/adding-an-integration.md](../integrations/adding-an-integration.md)
asks for it.
