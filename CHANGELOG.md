# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow
[SemVer](https://semver.org/).

## [Unreleased]

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
