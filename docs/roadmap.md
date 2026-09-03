# Roadmap: everything this repo will contain

The complete build list (structure, templates, agents & skills, scripts,
integrations, docs), phased into three waves. The reasoning behind the
structure and every design decision lives in [architecture.md](architecture.md).

Conventions used below:

- **Agents & skills** are both Agent Skills definitions in `.agents/skills/`
  (see [architecture.md](architecture.md) for why they share one format).
  "Role" = a recurring specialist; "Workflow" = an invokable procedure.
- Checkboxes track landing on `main`; completed items also get a CHANGELOG
  entry.

Confirmed sequencing decisions: **Asana** is the first task-tool integration
(monday.com second), **Granola** the first transcript source (Zoom later),
`campaigns/` is renamed to `projects/`, and the template ships blank with a
demo company on a separate branch later.

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
- [x] `.github/workflows/sync-check.yml`: CI drift check for the symlinks
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
- [ ] `.cursor/mcp.json`: the same list for Cursor
- [x] `integrations/README.md`: the registry (tool, mechanism, auth, status,
      env vars)
- [x] `integrations/tasks.md` template: the task-tool adapter document
- [ ] Setup docs: **Asana** (first task tool), **HubSpot**, **PostHog**,
      **GA4**, **DataForSEO**

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
`scripts/slack_post.py`); the Asana filing part still waits on the Asana
setup doc.

### Scripts

- [x] `scripts/pull_transcripts.py`: **Granola** → `memory/transcripts/inbox/`
- [x] `scripts/slack_post.py`: post as the team's Slack bot (team, requests,
      leadership channels)
- [ ] `scripts/og_image.py`: port from the Calven website repo; reads
      `brand/tokens.json` + `brand/templates/`
- [ ] Snapshot naming helper (shared by pull scripts)

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

- [ ] monday.com as the second task adapter
- [ ] Zoom transcripts in `pull_transcripts.py`
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
- **Granola MCP**: official status of Granola's MCP endpoint to be verified
  at build time; the pull script is the reliable fallback either way.
- **Context-layer stubs**: once a team connects a context layer, the mirrored
  strategy files become two-line fallbacks flagged `source: context-layer`.
  Keep them (routing table stays intact) or delete them? Stubs for now.
