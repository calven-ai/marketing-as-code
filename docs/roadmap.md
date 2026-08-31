# Roadmap: everything this repo will contain

The complete build list — structure, templates, agents & skills, scripts,
integrations, docs — phased into three waves. The reasoning behind the
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

## Wave 1 — the promise is true with zero integrations

Goal: clone the template, run `/setup`, and complete a real content workflow
entirely offline. No API keys required for anything in this wave.

### Structure

- [ ] Create `brand/`, `projects/` (retiring `campaigns/`), `reports/`,
      `integrations/`, `scripts/`, `data/{ontology,seo,analytics,crm,accounts}`,
      `memory/{knowledge,transcripts/{inbox,processed}}`
- [ ] Rewrite every folder README as a machine contract: what is
      authoritative here, naming conventions, what to do when something is
      missing
- [ ] AGENTS.md v2 — the full contract: ontology-first rule, the
      data-question routing table, the lifecycle-owner rule, the brand
      binary carve-out, review workflow
- [ ] README v2 — updated folder table and quick start
- [ ] `.github/PULL_REQUEST_TEMPLATE.md` — the human-review ritual
- [ ] `.env.example`

### Templates

- [ ] `strategy/` — positioning, messaging hierarchy, ICP & personas,
      competitive notes + battlecard
- [ ] `brand/` — voice.md, visual-identity.md, tokens.json, templates/
      placeholder
- [ ] `content/_template/` — brief + draft with frontmatter
      (`project`, `status`, `channel`, `owner`)
- [ ] `projects/_template/` — brief.md, status.md; plus campaign.md template
- [ ] `data/ontology/` — metrics.md, funnel.md, events.md, naming.md
      (unfilled versions instruct agents to ask, not assume)
- [ ] `memory/decision-log.md` — seeded with the entry format

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

- [ ] `scripts/sync_skills.py` + committed `.claude/skills/` per-skill
      symlinks
- [ ] `.github/workflows/sync-check.yml` — CI drift check for the symlinks
- [ ] `.claude/settings.json` — safe permission defaults
- [ ] `scripts/doctor.py` — env, symlink, and config health check

### Docs

- [ ] `docs/workflow.md` — the PR review ritual, written for GitHub Desktop
      users
- [ ] `docs/secrets.md` — the three-tier secrets story
- [ ] Finish `docs/new-to-github.md` and cross-link the new docs

---

## Wave 2 — integrations and the analyst loop

Goal: the killer UX works. A marketer asks "how many people attended event X
and then signed up?" and the repo routes it: snapshot → source system →
ontology → answer.

### Integrations

- [ ] `.mcp.json` + `.cursor/mcp.json` — servers listed, disabled by default
- [ ] `integrations/README.md` — the registry (tool, mechanism, auth, status,
      env vars)
- [ ] `integrations/tasks.md` template — the task-tool adapter document
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

### Scripts

- [ ] `scripts/pull_transcripts.py` — **Granola** → `memory/transcripts/inbox/`
- [ ] `scripts/og_image.py` — port from the Calven website repo; reads
      `brand/tokens.json` + `brand/templates/`
- [ ] Snapshot naming helper (shared by pull scripts)

### Report infrastructure

- [ ] `reports/_templates/report.md`
- [ ] `reports/_templates/dashboard.html` — single file, vendored chart
      library, `const DATA` block
- [ ] `reports/_templates/qmr/` — QMR report + dashboard scaffolds
- [ ] Optional: `.github/workflows/transcripts-cron.yml` — runs the pipeline
      on a schedule, **opens a PR, never merges**

---

## Wave 3 — breadth, story, ecosystem

### Agents & skills

| Definition | Kind | Purpose |
| --- | --- | --- |
| `brand-monitor` | Role | LLM/AEO mention tracking via DataForSEO → `reports/recurring/mentions/` |
| `researcher` | Role | ABM account research via Apify actors (LinkedIn/social) → `data/accounts/` |

### Integrations

- [ ] monday.com as the second task adapter
- [ ] Zoom transcripts in `pull_transcripts.py`
- [ ] Data enrichment (vendor TBD — Apify actors vs Clay/Breeze; open
      question)

### Website

- [ ] `docs/website.md` — the sibling-repo pattern
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
