# The operating model: where things run

There is no server. Nothing in this repo is deployed, hosted, or kept
alive. Work runs in one of three places, and for every recurring workflow
the team chooses between two of them. This page is that choice, written
down once.

## Three places things run

### 1. A person at a coding agent (the primary mode)

Someone opens the repo in a coding agent and types what they want. Claude
Code is what this repo is tuned for; Cursor and Codex read the same
`AGENTS.md` and skills. The agent reaches everything: the skills, the MCP
servers in `.mcp.json`, the scripts, and that person's own `.env` and OAuth
grants. The person triggers the work, watches it, and approves what ships
by merging the pull request. This is how most work happens and the mode to
learn first. The coding agent's window is the team's main interface, the
way the CRM's window used to be. It costs the person's subscription and
nothing more.

### 2. GitHub Actions (the only unattended runtime)

The team already uses GitHub, so its runners are the one place something
can run with nobody watching. Two flavours:

- **Scripts only** (shipped, the default). A scheduled workflow runs a
  deterministic script and opens a pull request with the result. It never
  merges. Keys come from the `automation` environment, which only `main`
  may use ([secrets.md](secrets.md)). Shipped: `transcripts-cron.yml`
  (Granola into the inbox, daily), `check.yml` (the health check on every
  proposal), `gate.yml` (the review gate, run from `main`) and
  `housekeeping.yml` (the weekly tidy-up).
- **An agent in Actions** (opt-in). A workflow runs a Claude Code agent on
  a schedule or a trigger, with a skill as its prompt. The agent can read
  the repo, edit files and commit to its own branch. Nothing else: no
  shell, no network, no Slack token, no way to open or merge a pull
  request. Plain steps after it open the PR and post a fixed Slack pointer.
  It needs `ANTHROPIC_API_KEY` in the `automation` environment and pays per
  token. `transcripts-process.yml` is the shipped example and does nothing
  until that key exists. Three limits: OAuth MCP servers cannot run
  headless, so only key-based servers and scripts work. Project MCP servers
  load without the usual prompt, which is why `.mcp.json` holds
  placeholders, never values. And the agent reads whatever the input
  holds, so give it as little as possible and treat its output as a
  proposal a person reads (AGENTS.md rule 11).

### 3. A session a person starts from Slack or the cloud (optional)

Someone mentions the repo's agent in a Slack thread, or starts a cloud
session. A coding-agent session opens on the repo, works, and posts a
summary and a PR link back. Layer 3 in
[integrations/slack/README.md](../integrations/slack/README.md);
availability depends on the plan. A person still starts it and still
merges.

## Two ways to run any recurring workflow

Every workflow that recurs can be run by a person on demand or by GitHub
Actions on a schedule. Both are legitimate. The trade-off:

| | A person runs it | GitHub Actions runs it |
| --- | --- | --- |
| How | `/chief-of-staff` after the meeting; `/qmr` at quarter end; "refresh the keywords" on Monday | A cron or a trigger runs a script (shipped) or an agent (opt-in) and opens a PR |
| Cost | The coding-agent subscription the person already has; no API key | An API key as a repository secret, billed per token for agent runs; scripts cost nothing beyond the vendor's data bill |
| Latency | When someone remembers | Same day, every day; nobody has to remember |
| Human in the loop | By construction: the person watches the run and reads the diff | At review: the PR is the only checkpoint, so the PR description must carry the full summary |
| Integrations | Everything, including OAuth MCP servers authorized in the browser | Key-based only; integration keys become secrets in the `automation` environment |
| Review load | The same: a PR either way for anything that cascades | The same |
| What can go wrong | It is not run | It runs on bad input with nobody watching; the PR catches it, if someone reads PRs |

**Recommendation.** Start with a person running everything. It is how
stage 2 in [stages.md](stages.md) already works, and it costs nothing
extra. Automate the one workflow whose latency hurts. For most teams that
is transcript processing: a meeting evaporates by Thursday if nobody
processed it Tuesday. Keep everything user-visible, and every strategy,
brand or ontology change, in the hands of a person. Write the choice per
workflow in `memory/decision-log.md`.

## What never runs unattended

Whatever the mode, these need a person every time (AGENTS.md rule 3,
[workflow.md](workflow.md)):

- Publishing content, sending email or Slack messages outside the team,
  changing the website.
- Deleting anything. Completing, reassigning or moving tasks in the task
  tool.
- Edits that cascade: `strategy/`, `brand/`, `data/ontology/`, pricing,
  any published claim.
- Merging. A person merges everything except bookkeeping, which the gate
  on `main` merges once the check is green. What counts as bookkeeping is
  defined in [workflow.md](workflow.md).

## Who triggers what

| Workflow | A person, on demand | Unattended, in Actions |
| --- | --- | --- |
| Sync a checkout with the approved copy | `/sync`, `python3 scripts/sync.py` | Never |
| Propose a change | `/propose`, `python3 scripts/propose.py` | The workflows open their own proposals (`transcripts-cron.yml`, `housekeeping.yml`) |
| Pull transcripts into the inbox | `python3 scripts/pull_transcripts.py` | `transcripts-cron.yml`, daily, opens a PR (shipped) |
| Process the inbox | `/chief-of-staff` after the meeting (the default) | `transcripts-process.yml`, on merge of an inbox PR, opens a PR that a person reads: the gate never merges an unattended run's proposal (opt-in, needs `ANTHROPIC_API_KEY`) |
| Refresh keyword volumes and difficulty | `python3 scripts/seo_snapshot.py --update` | A cron step running the same script, yours to add |
| Rankings, SERP questions, keyword ideas | `/seo-analyst` (the wired `seo-data` server) | Not headless; the script covers the scheduled part |
| Run a role unattended | never directly | `role-run.yml`, reusable, called by a `role-<skill>.yml` with a schedule: filters `.mcp.json` to the servers the caller names, hands the run only their keys, opens a PR that a person reads, snapshots included (opt-in, needs `ANTHROPIC_API_KEY` plus those keys in `automation`) |
| AI answer-engine mentions | `/brand-monitor` | `role-brand-monitor.yml`, monthly, through `role-run.yml` (shipped, dormant until the keys exist) |
| Pipeline, web, ads, email, social, reviews, PR, community, account and churn reports; content decay, competitor watch, status roundup, context freshness, the weekly report | `/<skill>` from the roster in `agents/README.md` | A `role-<skill>.yml` caller copied from `role-brand-monitor.yml`, yours to add once the role's categories are wired to a key-based server or a script; the check refuses a caller whose skill needs an OAuth server or writes to external systems |
| Quarterly review | `/qmr` | By hand: it needs the team's judgment and the exports it asks for |
| Account research | `/researcher` (the wired `scraping-search` server, OAuth) | Not headless |
| Every workflow skill: discovery, plans, briefs, drafts, reviews, audits, prototypes, projects | Always a person | Never |
| Slack digests and alerts | `python3 scripts/slack_post.py` from a skill | Scheduled workflows calling the same script, yours to add; the message table is in `integrations/slack/README.md` |
| Health check | `/doctor`, `python3 scripts/doctor.py` | `check.yml` on every proposal and on `main`: tests the lint, annotates, keeps the sticky comment current; read-only, no secrets (shipped) |
| Review gate | `python3 scripts/review_gate.py --pr N --dry-run` | `gate.yml` after every check run, from `main`: classifies, pushes the safe fixes as a Tidy commit, labels, publishes `review-gate`, merges green bookkeeping proposals (shipped) |
| Tidy the approved copy | `python3 scripts/doctor.py --fix` | `housekeeping.yml`, Mondays: the safe fixes as one bookkeeping proposal; stale proposals closed after three weeks (shipped) |
| Repository settings | `sh scripts/github_setup.sh`, then `python3 scripts/doctor.py --github` | Never; settings are applied once by an admin ([github-settings.md](github-settings.md)) |

When you add an integration or a workflow, add its row here. The checklist
in [integrations/adding-an-integration.md](../integrations/adding-an-integration.md)
asks for it.

## Turning a workflow off

Four scheduled workflows run in every copy of this repo whether or not you
asked: `housekeeping.yml` opens a tidy-up proposal on Mondays when the
approved copy needs one; `transcripts-cron.yml` runs daily and does
nothing until a Granola key exists; `transcripts-process.yml` runs daily
and does nothing until an Anthropic key exists; `role-brand-monitor.yml`
runs monthly and does nothing until that key and the DataForSEO login
exist. The dormant three cost a few seconds of runner time. The first
Monday's "Housekeeping" proposal is expected; it is short, read it once.

To stop one: on GitHub, Actions tab, pick the workflow, the "..." menu,
"Disable workflow". The file stays and you can turn it back on. To remove
it for good, delete the file under `.github/workflows/` and its row in the
table above, in a proposal.
