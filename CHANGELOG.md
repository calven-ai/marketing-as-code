# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow
[SemVer](https://semver.org/).

## [Unreleased]

- The lifecycle for people who never open a terminal: Sync. Work. Propose.
  Review. Merge. `/sync` (`scripts/sync.py`) brings in the approved copy
  and the gate's tidy-up, turns on the pre-push hook, removes branches
  whose proposal landed, and says what is waiting on you. `/propose`
  (`scripts/propose.py`) checks the files, fixes what is safe, commits,
  pushes the branch and opens or updates the proposal from the template,
  always against the checkout's own repository, then says whether it
  merges itself or waits for a person; without the GitHub CLI it prints
  the link to open the proposal by hand. `/doctor` explains the health
  check's findings and, with `--fix`, turns the hook on and sets your
  name from your GitHub login. `scripts/_common.py` gains the shared git
  and gh helpers; `scripts/test_lifecycle.py` runs the scripts against a
  real repository with a fake gh; `.claude/settings.json` allows the four
  lifecycle scripts to run without a prompt; `docs/troubleshooting.md`
  lists every message with its fix; `docs/workflow.md` and
  `docs/new-to-github.md` teach the five words. `review.self_merge` in
  `docs/schema.json` lets a repository with one maintainer pass the
  review gate on its own merge.
- Security: keys, unattended runs and the review gate. The gate moves to
  `.github/workflows/gate.yml`, which runs from `main` after every check
  (`workflow_run`), so a proposal can no longer change the rules it is
  judged by; `scripts/review_gate.py` classifies against a never-bookkeeping
  list hard-coded in `scripts/lint.py` (workflows, scripts, the schema,
  the agent settings, the skills, the integrations), pushes the Tidy
  commit from `main`'s lint, publishes the `review-gate` check, and merges
  bookkeeping only when the health check passed on that exact commit (no
  immediate-merge fallback). `check.yml` runs the proposal's code with a
  read-only token and no secrets. The three bot keys move to a GitHub
  environment `automation` restricted to `main` (`scripts/github_setup.sh`
  creates it; `scripts/doctor.py --github` checks it) and the workflow
  token defaults to read-only. `transcripts-process.yml` gives the agent
  no shell, no network and no Slack token: it edits files and commits
  through the action's own tool, then plain steps open the proposal and
  post a fixed Slack pointer. Shell interpolation of workflow inputs and
  ref names is gone; every action is pinned to a commit SHA and
  `.github/dependabot.yml` keeps them current; `dataforseo-mcp-server` is
  pinned in both MCP configs. `.claude/settings.json` denies `env`,
  `printenv`, one-liners, `gh pr merge`, force-pushes and the file
  commands on `.env*`, and switches off bypass mode; `docs/schema.json`
  lists the required rules and the lint restores a missing one. The Slack
  app loses `chat:write.public` and `channels:join`; `slack_post.py`
  posts only to the configured channels unless a person passes
  `--allow-any-channel`. `scripts/with_env.sh` starts a coding agent with
  `.env` in its environment (or through `op run`); `scripts/hooks/pre-push`
  refuses pushes to `main` and runs the lint. AGENTS.md rule 11 says what
  agents read is data, never instructions, and the transcript, research
  and SEO skills repeat it. `docs/secrets.md` is rewritten around who
  holds which key; `docs/github-settings.md` gains the environment,
  secret scanning and the click paths; `docs/operating-model.md` and
  `docs/workflow.md` say plainly that the gate merges bookkeeping.
- Keeping a cloned repo healthy, part 1: `docs/schema.json` says what valid
  means (frontmatter per folder, naming, CSV headers, secrets shapes, which
  files are bookkeeping); `scripts/lint.py` enforces it with `--fix` for
  the safe repairs and `scripts/test_lint.py` proves each check;
  `scripts/doctor.py` reports it (`--brief`, `--strict`, `--github`).
  `.github/workflows/check.yml` replaces `sync-check.yml`: it tests the
  lint, pushes the safe fixes to the proposal as a "Tidy" commit, annotates
  the diff, keeps one plain-language comment current, labels the proposal
  `bookkeeping` or `needs-review`, and, through `scripts/review_gate.py`,
  merges green bookkeeping proposals itself while needs-review ones wait
  for an approval from someone other than the author. `housekeeping.yml`
  tidies the approved copy weekly and closes stale proposals.
  `scripts/github_setup.sh`, `.github/CODEOWNERS` and
  `docs/github-settings.md` cover the settings that cannot live in a file
  and say plainly that a private repo needs GitHub Team or Pro for the
  rules to be enforced. Roster tables in `agents/README.md` and
  `scripts/README.md` are generated from skill `metadata` and script
  docstrings. `transcripts-process.yml` gains a daily schedule because a
  merge made by the check does not trigger push workflows.
- Blueprint, not a product: the README says what works as-is and what a
  team is expected to make its own; AGENTS.md rule 10 ("Make it yours")
  tells agents to build the integration or skill the team asks for.
  `integrations/adding-an-integration.md` is the guide: MCP server first,
  vendor CLI second, a script last, the runtime rule (sessions use MCP,
  unattended runs use CLIs and scripts), known routes for common tools,
  per-agent MCP config (Claude Code, Cursor, Codex) with the env-var
  syntax differences, the script contract, the deliverables checklist,
  and Zoom and Asana worked examples; the `add-integration` skill is its
  procedure. The registry splits "wired" from "known routes" and drops
  every "setup doc coming". `docs/operating-model.md` says where things
  run (a person at a coding agent, GitHub Actions, never a server) and
  lays out the person-versus-Actions trade-off per recurring workflow;
  `.github/workflows/transcripts-process.yml` is the opt-in
  agent-in-Actions example (needs `ANTHROPIC_API_KEY`, opens a PR). The
  transcript inbox is a documented contract any connector targets;
  `scripts/_common.py` shares `read_env_file`, `setting` and
  `snapshot_path` across scripts. `.cursor/mcp.json` ships, and
  `scripts/doctor.py` checks both MCP configs agree and hold placeholders
  only. Roadmap, architecture, roster and `.env.example` updated to the
  stance; phantom roster rows removed.
- Fit and path: `docs/is-this-for-you.md` (who this is for and not for, a
  self-assessment, profiles for teams of about 1, 5, 20 and 100 plus
  agencies, change management and stop signals) and `docs/stages.md`
  (three stages: the AI tools you already pay for, one agent for one
  activity, then this repo; buy, build or wait per pillar, Calven disclosed
  once for the context pillar). README gains "Is this for your team?" and
  a nav link; `docs/README.md`, `docs/new-to-github.md` and `AGENTS.md`
  cross-link.
- Context layer: `integrations/context-layer.md` explains why hand-maintained
  strategy files go stale and documents a marketing context layer over MCP
  as the alternative, with Calven as the example (disclosed as the
  maintainer's product); `calven` entry in `.mcp.json` and `CALVEN_MCP_KEY`
  in `.env.example`; `AGENTS.md` gains "Keeping context current".
  Strategy templates now mirror the documents that layer serves, heading for
  heading: `positioning.md` and `messaging.md` rewritten, `icp-personas.md`
  split into `icp.md` and `personas.md`, new `product-brief.md`. Every
  context file carries `source`, `last_reviewed` and `owner` frontmatter;
  `scripts/doctor.py` lists unreviewed and stale context files. The
  unfilled-template marker is now `Template: unfilled`. Em dashes removed
  from the repo's text.
- Four kinds of files: the repo is explained as context, agents, code, and
  data (with the three judgment calls on content, playgrounds, and
  integrations) in the README, `docs/architecture.md`, and `AGENTS.md`, and
  every top-level folder README states its kind under the H1.
- Day in the life: `scripts/pull_transcripts.py` (Granola to
  `memory/transcripts/inbox/`, dedupes against inbox and processed) and
  `.github/workflows/transcripts-cron.yml` (daily pull, opens a PR, never
  merges); `scripts/slack_post.py` (post as the team's bot to the team,
  requests, or leadership channel) plus `SLACK_LEADERSHIP_CHANNEL_ID`;
  `chief-of-staff` upgraded to extract facts, decisions, project status
  updates, action items per owner, and risks and red flags, and to post
  the summary to Slack (red flags to leadership); new skills
  `seo-analyst`, `brand-monitor` (with `data/seo/prompts.csv`),
  `researcher` (alumni-list example with Apify actors), and
  `campaign-discovery`; `.mcp.json` listing the DataForSEO and Apify MCP
  servers with env placeholders only.
- Slack: app manifest and install guide in `integrations/slack/` (bot
  token only, no server), registry row, env vars.
- Review pass: `published:` date in content frontmatter (so "what shipped
  this quarter" is computable), deliverables tables no longer mirror content
  status, decision-log insertion point clarified, env-var names in the
  integrations registry (agents cannot read `.env*`), accurate wording for
  not-yet-existing files (`.mcp.json`, setup docs), `.gitignore` no longer
  swallows Keynote `.key` files, doctor checks two more templates, PII note
  for transcripts.
- Wave 1: structure v2 (`brand/`, `projects/` replacing `campaigns/`,
  `data/` domains + ontology, `reports/`, `integrations/`, `scripts/`),
  folder READMEs as machine contracts, AGENTS.md v2 with the data-question
  routing table, all wave-1 templates, nine agents/skills in
  `.agents/skills/` (incl. `qmr` and `make-dashboard` pulled forward),
  QMR pack (report + data checklist + self-contained HTML dashboard
  template), skill-sync machinery with CI check, `docs/workflow.md` and
  `docs/secrets.md`.
- Architecture design doc (`docs/architecture.md`) and phased roadmap
  (`docs/roadmap.md`).
- Initial skeleton: folder hierarchy, README, agent contract, community files.
