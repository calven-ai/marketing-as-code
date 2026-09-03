# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow
[SemVer](https://semver.org/).

## [Unreleased]

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
