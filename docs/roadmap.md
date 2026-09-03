# Roadmap: everything this repo will contain

The complete build list (structure, templates, agents & skills, scripts,
integrations, docs), phased into three waves. The reasoning behind the
structure and every design decision lives in [architecture.md](architecture.md).

The stance, so the checkboxes read right: the maintainers ship the
structure, the offline workflows, the guides, one worked example per way
of connecting a tool (MCP server, CLI, script), and the guide for adding
the rest ([integrations/adding-an-integration.md](../integrations/adding-an-integration.md)).
Connectors for tools the maintainers do not use are not on this list; they
are the team's job with its coding agent, and welcome back upstream as
examples ([CONTRIBUTING.md](../CONTRIBUTING.md)). The repo is a blueprint
([README](../README.md#a-blueprint-not-a-product)), not a product with a
connector catalogue.

Conventions used below:

- **Agents & skills** are both Agent Skills definitions in `.agents/skills/`
  (see [architecture.md](architecture.md) for why they share one format).
  "Role" = a recurring specialist; "Workflow" = an invokable procedure.
- Checkboxes track landing on `main`; completed items also get a CHANGELOG
  entry.

Confirmed sequencing decisions: **Granola** is the shipped transcript
connector and the worked example for the script tier; **Asana** is the
worked example for a write-capable MCP in the guide (not wired; the team
adds it in one PR); `campaigns/` is renamed to `projects/`; and the
template ships blank with a demo company on a separate branch later.

---

## Wave 1: the promise is true with zero integrations

Goal: clone the template, run `/setup`, and complete a real content workflow
entirely offline. No API keys required for anything in this wave.

### Structure

- [x] Create `brand/`, `projects/` (retiring `campaigns/`), `reports/`,
      `integrations/`, `scripts/`, `data/{ontology,seo,analytics,crm,accounts}`,
      `memory/{knowledge,transcripts/{inbox,processed}}`
- [x] Rewrite every folder README as a machine contract: what is
      authoritative here, naming conventions, what to do when something is
      missing
- [x] AGENTS.md v2: the full contract: ontology-first rule, the
      data-question routing table, the lifecycle-owner rule, the brand
      binary carve-out, review workflow
- [x] README v2: updated folder table and quick start
- [x] `.github/PULL_REQUEST_TEMPLATE.md`: the human-review ritual
- [x] `.env.example`

### Templates

- [x] `strategy/`: positioning, messaging, ICP, personas, product brief
      (headings mirror the documents a marketing context layer serves over
      MCP), competitive notes + battlecard
- [x] `brand/`: voice.md, visual-identity.md, tokens.json, templates/
      placeholder
- [x] `content/_template/`: brief + draft with frontmatter
      (`project`, `status`, `channel`, `owner`)
- [x] `projects/_template/`: brief.md, status.md; plus campaign.md template
- [x] `data/ontology/`: metrics.md, funnel.md, events.md, naming.md
      (unfilled versions instruct agents to ask, not assume)
- [x] `memory/decision-log.md`: seeded with the entry format

### Agents & skills (no keys needed)

| Definition | Kind | Purpose |
| --- | --- | --- |
| `setup` | Workflow | The interview: fills strategy, brand, and ontology from the team's answers; enables the MCP servers they use; writes `integrations/tasks.md` |
| `new-content` | Workflow | Scaffold a content piece: brief first, frontmatter wired to its project |
| `new-project` | Workflow | Scaffold a project or campaign folder from the templates |
| `review` | Workflow | Pre-publish check of a draft against strategy, voice, and brand |
| `log-decision` | Workflow | Append a properly formatted, attributed entry to the decision log |
| `chief-of-staff` | Role | Process `memory/transcripts/inbox/`: decisions → log, action items → tasks (in-folder checklist fallback until a task tool is connected), doc updates as reviewable diffs |
| `prototype-builder` | Role | Build a disposable prototype in `playgrounds/` from one sentence, using `brand/` |

### Machinery

- [x] `scripts/sync_skills.py` + committed `.claude/skills/` per-skill
      symlinks
- [x] `.github/workflows/check.yml`: the deterministic checks on every proposal (replaced `sync-check.yml`)
- [x] `.claude/settings.json`: safe permission defaults
- [x] `scripts/doctor.py`: env, symlink, and config health check

### Docs

- [x] `docs/workflow.md`: the PR review ritual, written for GitHub Desktop
      users
- [x] `docs/secrets.md`: the three-tier secrets story
- [x] `docs/is-this-for-you.md` and `docs/stages.md`: the fit check
      (team-size profiles, change management) and the three-stage path;
      README gains "Is this for your team?"
- [ ] Finish `docs/new-to-github.md` and cross-link the new docs

---

## Wave 2: integrations and the analyst loop

Goal: the killer UX works. A marketer asks "how many people attended event X
and then signed up?" and the repo routes it: snapshot → source system →
ontology → answer.

### Integrations

- [x] `.mcp.json`: DataForSEO, Apify and Calven listed (keys via env
      placeholders; Claude Code asks before enabling)
- [x] `integrations/context-layer.md`: why hand-maintained context goes
      stale, the marketing context layer over MCP as the alternative,
      Calven as the documented example
- [x] `last_reviewed` frontmatter on every context file + the staleness
      list in `scripts/doctor.py`
- [x] `.cursor/mcp.json`: the same list for Cursor, in Cursor's syntax;
      `scripts/doctor.py` checks the two files agree and hold no values
- [x] `integrations/README.md`: the registry (tool, mechanism, auth, status,
      env vars)
- [x] `integrations/tasks.md` template: the task-tool adapter document
- [x] `integrations/adding-an-integration.md`: the guide (MCP server, then
      CLI, then script; the runtime rule; per-agent MCP config; the script
      contract; the deliverables checklist; Zoom and Asana worked examples)
      and the `add-integration` skill. Per-tool setup docs are not planned:
      the registry's "known routes" table plus the guide replace them, and
      community connector examples are welcome
- [x] `docs/operating-model.md`: where things run, the person-versus-Actions
      trade-off per recurring workflow, what never runs unattended
- [x] `.github/workflows/transcripts-process.yml`: the opt-in agent-in-Actions
      example (chief-of-staff on the inbox, opens a PR, needs
      `ANTHROPIC_API_KEY`)

### Agents & skills

| Definition | Kind | Purpose |
| --- | --- | --- |
| `analyst` | Role | The data-question router: snapshots → pulls → ontology → answer (worked examples included) |
| `seo-analyst` | Role | Keyword & ranking analysis against `data/seo/keywords.csv` via DataForSEO |
| `weekly-seo` | Workflow | Diff latest snapshots, write the delta report to `reports/recurring/seo/` |
| `web-analyst` | Role | GA4/PostHog snapshot + analysis into `reports/recurring/analytics/` |
| `make-dashboard` | Workflow | Copy `reports/_templates/dashboard.html`, inline the data, save beside the report |
| `qmr` | Workflow | The quarterly marketing review: pull snapshots, compute deltas vs last quarter via the ontology, fill the template, flag gaps as questions |
| `chief-of-staff` (upgrade) | Role | Files action items as real Asana tasks per `integrations/tasks.md` |
| `campaign-discovery` | Workflow | One-sentence campaign idea → competitive angle, keywords and ranks, AI answer-engine coverage, content inventory, one report in `reports/adhoc/` |

Shipped early with wave 1 (offline-capable versions): the `qmr` skill (works
the QMR data checklist with or without integrations), `make-dashboard`, and
the full wave-1 agents & skills table above. Shipped since: `seo-analyst`,
`campaign-discovery`, and the `chief-of-staff` upgrade (project status
updates, action items per owner, risks and red flags, Slack notify via
`scripts/slack_post.py`); filing into a real task tool starts the day the
team wires one per `integrations/tasks.md`.

### Keeping it healthy

- [x] `docs/schema.json`: what valid means, in one file
- [x] `scripts/lint.py` + `scripts/test_lint.py`: the deterministic checks
      (frontmatter, naming, placement, CSV headers, links, secrets, generated
      roster tables) with `--fix`; `scripts/doctor.py` reports them
- [x] `.github/workflows/check.yml`: tests, safe fixes pushed as a Tidy
      commit, annotations, a sticky comment, labels; bookkeeping proposals
      merge themselves, the rest wait for a person (`scripts/review_gate.py`)
- [x] `.github/workflows/housekeeping.yml`: weekly tidy proposal, stale
      proposals closed
- [x] `scripts/github_setup.sh`, `.github/CODEOWNERS`,
      `docs/github-settings.md`: the settings that cannot live in a file
- [x] Security hardening: `gate.yml` runs the review gate from `main`;
      `check.yml` is read-only; the bot keys live in the `automation`
      environment; the agent in Actions has no shell; actions and the
      DataForSEO server are pinned; `scripts/hooks/pre-push`,
      `scripts/with_env.sh`; `docs/secrets.md` rewritten around who holds
      which key; AGENTS.md rule 11 (untrusted content)
- [ ] `scripts/sync.py`, `scripts/propose.py` and the `sync`, `propose`,
      `doctor` skills: the five-word lifecycle for people who do not know
      Git; `docs/troubleshooting.md`; `docs/new-to-github.md` finished
- [ ] The AI layer: `audit`, `cascade`, `integration-check` skills;
      `context-review.yml`, `weekly-audit.yml`, `integration-check.yml`,
      `claude.yml`; Claude Code hooks that run the lint after every edit;
      `scripts/integration_check.py`

### Scripts

- [x] `scripts/pull_transcripts.py`: **Granola** → `memory/transcripts/inbox/`
- [x] `scripts/slack_post.py`: post as the team's Slack bot (team, requests,
      leadership channels)
- [ ] `scripts/og_image.py`: port from the Calven website repo; reads
      `brand/tokens.json` + `brand/templates/`
- [x] `scripts/_common.py`: `read_env_file`, `setting`, `snapshot_path`,
      shared by every script

### Report infrastructure

- [x] `reports/_templates/report.md`
- [x] `reports/_templates/dashboard.html`: single file, dependency-free
      inline chart helpers, `const DATA` block
- [x] `reports/_templates/qmr/`: QMR report + dashboard scaffolds
- [x] `.github/workflows/transcripts-cron.yml`: pulls transcripts daily,
      **opens a PR, never merges**

---

## Wave 3: breadth, story, ecosystem

### Agents & skills

| Definition | Kind | Purpose |
| --- | --- | --- |
| `brand-monitor` | Role | LLM/AEO mention tracking via DataForSEO → `reports/recurring/mentions/` (shipped) |
| `researcher` | Role | ABM account research via Apify actors (LinkedIn/social) → `data/accounts/` (shipped, alumni-list example) |

### Integrations

- monday.com, Zoom, HubSpot, PostHog, GA4, Salesforce: not planned by the
  maintainers. Each is a "known route" in `integrations/README.md`; a team
  adds it with `add-integration`, and a connector contributed back as a
  worked example is welcome
- [ ] Data enrichment (vendor TBD: Apify actors vs Clay/Breeze; open
      question)
- [ ] Optional context pull script: mirror a connected context layer into
      `strategy/` as dated files, for teams that need offline copies

### Website

- [ ] `docs/website.md`: the sibling-repo pattern
- [ ] Content→website sync Action: on merge of `status: published`, open a PR
      against the website repo
- [ ] Companion `marketing-as-code-website` Astro template repo

### Ecosystem

- [ ] Optional GitHub Pages workflow serving `reports/` at a URL
- [ ] Demo-company branch (fictional company, every folder filled) for
      screenshots and the article
- [ ] Claude Code plugin / skill-marketplace packaging of the skill set

---

## Open questions

- **Enrichment vendor** (wave 3): no clean official integration exists for
  6sense-style enrichment. Apify actors, or a specific vendor (Clay,
  HubSpot Breeze)?
- ~~**Granola MCP**~~: resolved. Granola's official MCP exists (remote,
  OAuth-only, paid plans), which makes it a session tool; the pull script
  stays because an OAuth server cannot run in the daily cron. That is the
  ladder's runtime rule, not a fallback.
- **Context-layer stubs**: once a team connects a context layer, the mirrored
  strategy files become two-line fallbacks flagged `source: context-layer`.
  Keep them (routing table stays intact) or delete them? Stubs for now.
