# Architecture: how this repo is designed, and why

This document is the reasoning behind the repository structure: the target
layout, what each folder owns, and the design decisions that hold it together.
The [roadmap](roadmap.md) lists what gets built and in what order.

> **Status:** approved design, built. Waves 1 and 2 of the
> [roadmap](roadmap.md) landed the structure below, the offline workflows,
> the MCP configs, the pull scripts, the analyst skills, the context-layer
> integration, the integration guide, and the operating model. What remains
> is wave 3 (website pattern, demo company, packaging). Connectors beyond
> the worked examples are the team's to add
> ([integrations/adding-an-integration.md](../integrations/adding-an-integration.md)).

## Design principles

Five rules generate almost every decision below:

1. **A file lives with its lifecycle owner.** When two folders could claim a
   file, it goes where its lifespan matches. Content outlives the project that
   produced it, so content never lives inside a project folder. This one rule
   kills duplication without an index to maintain.
2. **Machine files and human files don't mix.** `data/` is append-only CSV
   that agents diff and query; `reports/` is dated narrative that humans read.
   Different lifecycles, different folders.
3. **Agent-agnostic by standard, not by duplication.** Definitions exist once,
   in the open format the ecosystem converged on, with the thinnest possible
   shim for tools that lag.
4. **Adapters are documents where a document will do.** The task-tool
   integration is a page of conventions agents read, not a code layer anyone
   maintains.
5. **Humans decide, so agents propose diffs.** Anything that cascades
   (transcript-driven doc updates, published content) moves through review,
   never through silent writes.

## Four kinds of files

Every file in the tree is one of four kinds. The folders are the
implementation; the four kinds are the model.

| Kind | Folders | What it is | Who writes it |
| --- | --- | --- | --- |
| Context | `strategy/`, `brand/`, `content/`, `projects/`, `memory/`, `docs/`, plus `AGENTS.md` and `CLAUDE.md` at the root | What the team knows: positioning, messaging, personas, brand, briefs and status, the decision log and knowledge base, published content, and the guides on how the team works here | The team |
| Agents | `agents/` (the roster), `.agents/skills/` (the definitions), `integrations/` (registry, task adapter, Slack app, `.mcp.json`) | The workforce, as instructions in English: every agent or skill is a Markdown file a person can read and change, plus the registry of what agents are allowed to reach | A person editing text |
| Code | `scripts/`, `playgrounds/`, `.github/workflows/` | Small deterministic scripts and throwaway prototypes, written by the agent, not by the team | The agent |
| Data | `data/`, `reports/` | The numbers as tables, dated snapshots, and the reports built from them | The tools |

Three judgment calls, stated so nobody re-litigates them:

- Content is an output that becomes context once published, because agents
  read it the way they read positioning.
- Playgrounds are code because prototypes are HTML the agent writes and the
  team throws away.
- Integrations sit with agents because they define what the agents may reach.

The split matters because each kind asks a different thing of an agent.
Context is loaded before thinking, never guessed at. Code is run instead of
reimplemented, because a script that already exists is cheaper and more
reliable than a fresh one. Data is treated as evidence: queried, diffed, and
quoted, never invented. Agents are edited as text, so changing what the
workforce does is a reviewable diff, not a deploy.

## The target tree

```
marketing-as-code/
├── .agents/skills/<name>/       # canonical agent & skill definitions (open standard)
├── .claude/skills/<name>        # per-skill symlinks into .agents/skills/ (Claude Code shim)
├── .mcp.json  .cursor/mcp.json  # the same MCP servers for Claude Code and Cursor, placeholders only
├── .github/                     # PR template, CODEOWNERS, check and housekeeping workflows, crons
│
├── strategy/                    # market truth: positioning, messaging, ICP/personas, competitive
├── brand/                       # voice + visual identity + reusable design assets
├── content/                     # single source of truth for every piece, one folder per piece
├── projects/                    # PM artifacts only; a campaign is a project with children
├── data/
│   ├── ontology/                # metrics, funnel, events, naming: the measurement truth
│   ├── seo/                     # keywords.csv (canonical) + snapshots/
│   ├── analytics/               # web analytics snapshots (GA4 / PostHog)
│   ├── crm/                     # pipeline, signups, email performance snapshots
│   └── accounts/                # prospect lists, ABM research, enrichment outputs
├── reports/                     # human-first outputs, incl. self-contained HTML dashboards
├── memory/                      # decision log, knowledge base, transcript pipeline
├── agents/                      # the human-readable workforce roster (index)
├── integrations/                # registry, the integration guide, the task-tool adapter
├── scripts/                     # deterministic non-AI code (OG images, pulls, sync, doctor)
├── playgrounds/                 # disposable prototypes
└── docs/                        # guides, this document, the roadmap
```

## Folder by folder

### `.agents/skills/`: the canonical agent and skill definitions

One folder per agent or skill, in the Agent Skills format (`SKILL.md` with
YAML frontmatter, plus optional `scripts/` and `references/`). This location
became the cross-tool standard: Cursor, OpenAI Codex CLI, Gemini CLI, GitHub
Copilot, and OpenCode discover it natively, with zero machinery on our side.

We deliberately make no format distinction between "agents" (recurring roles:
`seo-analyst`, `chief-of-staff`) and "skills" (procedures: `new-content`,
`qmr`). The standard doesn't distinguish them, and neither should we; the
roster in `agents/README.md` groups them for humans instead. A skill folder
carrying its own `scripts/` is exactly the packaging a hybrid like the
chief-of-staff (Python ingestion + judgment prompt) needs.

**Claude Code shim:** Claude Code still reads `.claude/skills/`, so we commit
*per-skill symlinks* (`.claude/skills/<name>` → `../../.agents/skills/<name>`).
Per-skill rather than a whole-directory symlink, because Claude Code writes
housekeeping files into `.claude/skills/` and a directory symlink would
redirect those into the canonical tree. `scripts/sync_skills.py` regenerates
the links (copies on Windows) and a CI check catches drift. The shim gets
deleted the day Claude Code reads `.agents/skills/` natively.

*Rejected:* visible `agents/` + `skills/` folders as canonical, with generated
per-tool adapters: three locations and a permanent sync burden, with the
standard location demoted to a derivative. Also rejected: documentation-only
pointers ("read agents/seo.md"), which lose auto-discovery and
slash-invocation in every tool. Also rejected: Claude-specific subagents
(`.claude/agents/`), which are Claude-only; skills-as-roles cover the need
portably.

### `strategy/`: market truth

Positioning, messaging, ICP, personas, product brief, competitive notes and
battlecards. This is the context layer agents load before *thinking* about
marketing: who we serve, what we claim, against whom. Product marketing's
home. Brand voice moves out (see next), because voice is consumed at
*generation* time, not planning time.

**Two sources for context.** The default is Markdown in this folder, and it
has a known failure mode: it goes stale quietly. So every context file carries
`source`, `last_reviewed` and `owner` in its frontmatter, and
`scripts/doctor.py` lists files not reviewed in 90 days (CI prints the list on
every pull request). The alternative is a marketing context layer served over
MCP, where the service keeps positioning, messaging, ICP, personas and
competitors current and every agent reads the same document on every call;
the files here become fallbacks flagged `source: context-layer`. The templates
mirror the documents Calven (this repo's maintainer) serves, heading for
heading, so the switch is a frontmatter flag and not a restructuring. The
full argument, the mapping table and the connection steps are in
[integrations/context-layer.md](../integrations/context-layer.md).

*Rejected:* a pull script that mirrors a connected context layer into
`strategy/` as dated files. It is real code with a maintenance tail, and it
reintroduces the copy the MCP removes. Deferred to wave 3 as an option for
teams that need offline files.

### `brand/`: how we sound and look

`voice.md` (moved from strategy), `visual-identity.md`, machine-readable
`tokens.json` (colors, fonts; consumed by the OG-image generator and the
prototype builder), `logos/`, and `templates/` (OG-image background, social
templates). Content and design agents load `brand/` whenever they produce
anything an outsider will see.

This is the one sanctioned binary zone in the repo; the "plain text first"
ground rule gets an explicit carve-out here, because logos and image templates
have no useful text form.

*Rejected:* `strategy/brand/`, because brand is an execution-time dependency,
strategy a planning-time one, and binary assets don't belong inside "the
context layer every agent loads first."

### `content/`: the single source of truth for every piece

Unchanged mission: one folder per piece, brief first, draft second, human
review before anything ships. What's new is queryable frontmatter on every
piece:

```yaml
project: projects/q4-launch/webinar   # which project produced it
status: draft | in-review | published | evergreen
channel: blog | email | linkedin | webinar | ...
owner: name
published: YYYY-MM-DD                 # set when status flips to published
```

Email sequences, webinar assets, and case studies are content *types* here,
not new top-level folders. The frontmatter is what lets an agent answer "what
did we ship last quarter?" with a grep instead of a spreadsheet.

### `projects/`: how the team organizes the work (replaces `campaigns/`)

The filing dilemma "is this a campaign or a project?" is dissolved by one
convention: **everything is a project; a campaign is a project big enough to
have children.**

- `projects/<name>/` holds **only project-management artifacts**: `brief.md`
  (goal, audience, deliverables, owner, dates), `status.md`, working notes.
- A campaign is a folder with a `campaign.md` (narrative, goals, budget,
  timeline) containing project subfolders:

  ```
  projects/q4-launch/campaign.md
  projects/q4-launch/webinar/brief.md
  projects/q4-launch/abm-push/brief.md
  projects/one-off-report/brief.md          # standalone project, no campaign
  ```

- **Content never lives here.** The brief's Deliverables section lists
  relative repo paths into `content/`; each piece's frontmatter points back
  with `project:`. The link is greppable in both directions with no index
  file to keep in sync. Data a project produces likewise goes to `data/`.
- When a project closes, its folder moves to `projects/_archive/` (or is
  deleted). Because it held only PM artifacts, nothing of lasting value goes
  with it; the content, data, and decisions all live where they belong.

Tasks inside a project are managed in the team's task tool via
[`integrations/tasks.md`](#integrations--the-registry-and-the-task-adapter);
the brief links to the project there.

*Rejected:* separate `campaigns/` and `projects/` top-levels (the filing
ambiguity never ends); content inside project folders with a published mirror
(duplication, the exact failure this design exists to prevent); symlinks from
projects into content (break on the GitHub web UI, which this audience uses).

### `data/`: machine-first inputs

Per-domain folders, each following the same pattern: **canonical tables at the
domain root, timestamped immutable pulls in `snapshots/`**.

- `data/seo/keywords.csv`: the single source of truth for tracked keywords
  (keyword, intent, difficulty, volume, target URL, current rank).
  `data/seo/snapshots/2026-08-31-dataforseo-rankings.csv` is a dated pull.
- `data/analytics/`: GA4/PostHog snapshots. `data/crm/`: pipeline, signups,
  email performance from the CRM. `data/accounts/`: prospect lists, ABM
  research, enrichment outputs.

The snapshot naming convention `YYYY-MM-DD-<source>-<what>.csv` is
load-bearing: it's how any agent finds "the latest snapshot" without an index,
and how the weekly delta reports diff two points in time. Everything here
stays CSV so it stays diffable and queryable. No customer PII in a public
copy, ever. Analyses of this data do not live here; they go to `reports/`.

*Rejected:* reports inside `data/` (mixes append-only machine files with
human narrative, and makes PII auditing harder); one flat cross-domain
snapshots folder (the domain is the natural retrieval key).

### `data/ontology/`: the measurement truth

Four files that make raw data interpretable:

- `metrics.md`: what an MQL, SQL, PQL, signup, activation actually mean here
- `funnel.md`: lifecycle and pipeline stages, and what each transition means
- `events.md`: event taxonomy: names, properties, which system emits them
- `naming.md`: UTM conventions, campaign naming

Ground rule (AGENTS.md rule 2): **any agent reading or writing `data/`
loads `data/ontology/` first.** An unfilled ontology file instructs agents to
ask rather than assume. `/setup` interviews the team to fill these in.

It lives under `data/` because its consumers are the analysis agents and its
authors are marketing ops, the same people who own `data/`.

*Rejected:* a top-level `ontology/` (top-level real estate is for things
marketers browse; this is agent infrastructure) and `strategy/` (strategy is
market truth, ontology is measurement truth).

### `reports/`: human-first outputs

Where analyses, recurring reports, and dashboards land:

```
reports/
├── _templates/            # report.md and dashboard.html scaffolds
├── qmr/2026-q3/           # quarterly marketing review: report + dashboard
├── recurring/{seo,analytics,mentions}/
└── adhoc/2026-08-31-event-x-signups/
```

Separated from `data/` because the lifecycle differs: data is overwritten and
appended by machines; reports are dated artifacts that are immutable once
delivered.

**Dashboards are self-contained HTML files** living beside the report they
support: one file, inline CSS, a vendored chart library, and a `const DATA`
block the generating agent fills from CSV. They open in any browser straight
from Finder, GitHub Desktop, or a download: platform-agnostic by
construction, with no build step and no dependence on any one AI tool's
artifact format.

The QMR is the flagship example: a `/qmr` skill pulls fresh snapshots into
`data/`, computes deltas against last quarter using the ontology, fills the
template into `reports/qmr/<quarter>/`, and flags gaps as questions instead of
inventing numbers. It deliberately composes the analyst, the integrations,
the ontology, and the dashboard template: proof the architecture composes.

*Rejected:* a `dashboards/` top-level (splits a report from its evidence);
React or build-step dashboards (violates "no build steps for marketers").

### `memory/`: the part that compounds

```
memory/
├── decision-log.md        # dated, attributed decisions, linked to source
├── knowledge/             # topic files, fed by the chief-of-staff
└── transcripts/
    ├── inbox/             # new transcripts land here
    └── processed/         # moved here once processed
```

**The transcript pipeline** splits deterministic I/O from judgment:

1. *Ingest:* `scripts/pull_transcripts.py` pulls new meeting transcripts
   (Granola first) into `inbox/`, or a human simply drags a file in. The
   manual path works from day one with zero setup.
2. *Process:* the `chief-of-staff` skill takes each inbox file and extracts
   **decisions** → appended to `decision-log.md` (dated, attributed, linked
   to the transcript); **action items** → filed in the team's task tool per
   `integrations/tasks.md`; **facts** → proposed edits to `memory/knowledge/`
   and any affected strategy or project docs, **always as a diff for human
   review, never a silent write**. The transcript then moves to `processed/`.
3. *Automation, the team's choice:* a GitHub Actions cron pulls transcripts
   (shipped), and an opt-in workflow can run the processing skill as an
   agent; either way the output is a pull request, never a merge. Cascading
   doc edits without review is exactly the failure mode the "humans decide"
   rule exists to prevent. The person-versus-Actions trade-off is in
   [operating-model.md](operating-model.md).

### `agents/`: the human-readable roster

The "meet the workforce" front door: a table of every agent and skill: what
it does, which integrations it needs, a link to its definition in
`.agents/skills/`. An index for humans; the loadable truth lives in
`.agents/skills/`.

### `integrations/`: the registry and the task adapter

- `README.md` is the registry: what is wired (tool, mechanism, auth, env
  vars) and the known routes for common tools that are not.
- `adding-an-integration.md` is the guide a coding agent follows to add a
  tool, and the `add-integration` skill is its procedure. Per-tool setup
  docs were rejected in favour of it: the maintainers cannot keep a
  connector catalogue current, and a team's coding agent can build the one
  connector it needs in an afternoon from a good guide and a worked
  example.
- **`tasks.md`: the task-tool adapter.** GitHub Issues won't fly with a
  marketing team, so the repo integrates with the team's real task tool
  (Asana first; monday.com next). The adapter is a *document*: which tool,
  which workspace and project IDs, tagging conventions, and "how to file a
  task" in prose. Every task-creating skill carries one instruction: *read
  `integrations/tasks.md` and file tasks per its rules.* That's the whole
  abstraction, and it works identically in every coding agent. Until `/setup`
  writes it, the file documents GitHub Issues as the zero-setup fallback.

**The ladder.** A tool is connected at the highest tier that does the
job: the vendor's official MCP server (remote with OAuth preferred: no key
exists, so none can leak; each person authorizes in the browser), then the
vendor's CLI, then a small script in `scripts/` under the script contract.
Move down only for a reason: no server, a write the server lacks, an
unattended run, a bulk pull. The runtime rule decides as much as
availability does: an MCP call happens inside an interactive session, so
anything scheduled in GitHub Actions runs a CLI or a script. That is why
DataForSEO appears twice (the MCP for questions, `seo_snapshot.py` for the
weekly refresh) and why the Granola script stays although Granola has an
MCP. The full reasoning, the known routes per tool, and the per-agent
config differences (Claude Code `${VAR}`, Cursor `${env:VAR}`, Codex TOML)
are in [integrations/adding-an-integration.md](../integrations/adding-an-integration.md).
The shipped servers are listed in `.mcp.json` and `.cursor/mcp.json` with
placeholders only; Claude Code asks before starting a project server in a
session, and non-interactive runs load them without asking, which is the
reason for the placeholder rule.

*Rejected:* a code-level task adapter (a CLI wrapping Asana/monday APIs):
real engineering and permanent maintenance for a problem MCP already solves.
Also rejected: a connector catalogue maintained here (see above).

### `scripts/`: deterministic, non-AI code

Python, standard library only. Skills call these instead of
reimplementing, and a new connector copies the closest one (the script
contract is in the integration guide):

- `_common.py`: the shared helpers (`read_env_file`, `setting`,
  `snapshot_path`), so every script resolves keys and names snapshots the
  same way.
- `pull_transcripts.py`: Granola → `memory/transcripts/inbox/`, the shipped
  transcript connector; any other provider writes the same files (the
  inbox contract in `memory/transcripts/README.md`).
- `seo_snapshot.py`: the scheduled DataForSEO refresh into
  `data/seo/snapshots/`.
- `slack_post.py`: post as the team's bot.
- `sync_skills.py`: regenerates the `.claude/skills/` symlinks.
- `doctor.py`: health check (required files, symlinks intact, the two MCP
  configs listing the same servers with placeholders and no values, stale
  context files).
- `og_image.py` (planned): composes an article title over a brand
  background using `brand/tokens.json` and `brand/templates/`.

### `playgrounds/`: unchanged

Disposable prototypes instead of decks. After the meeting, log the decision
in `memory/`, archive the prototype.

### The website: a standalone sibling repo, deliberately not in here

The "marketing as code" story includes a CMS-less Astro website, but it lives
in its own repository. Three reasons:

1. **Audience.** A deployable with `node_modules`, CI, and deploy secrets
   would dominate and intimidate exactly the non-technical marketers this
   template targets. A `docs/new-to-github.md` reader should never meet
   `astro.config.mjs`.
2. **Lifecycles.** Website releases shouldn't churn the marketing repo's
   history, and strategy edits shouldn't trigger deploy pipelines.
3. **Practice.** This mirrors how the pattern already runs in production:
   the OG-image tooling originated in a separate website repo.

The repos still connect: `docs/website.md` (planned) will document the pattern, and a
GitHub Action here opens a PR against the website repo whenever a content
piece merges with `status: published`. The website repo stays dumb; it just
receives content. A companion `marketing-as-code-website` Astro template repo
is on the roadmap.

## Where things run: no server

Nothing is deployed. Work runs where a person is typing to a coding agent
(Claude Code in the terminal or desktop app, Cursor, Codex), which is the
primary mode and costs only that person's subscription; or unattended in
GitHub Actions, which runs scripts by default and an agent as an opt-in
with an API key, and in either case opens a pull request and never merges.
Every recurring workflow can run either way, and the team chooses per
workflow; the trade-off (cost, latency, human in the loop, which
integrations work headless) is written down once in
[operating-model.md](operating-model.md).

*Rejected:* a hosted service or bot the team must deploy and keep alive.
The audience is a marketing team; the runners GitHub already gives them
are the only infrastructure this design assumes.

## Secrets: three tiers

Documented fully in `docs/secrets.md` (roadmap wave 1):

1. **Prefer OAuth remote MCPs** (Asana, monday, HubSpot, Apify). No key
   exists, so no key can leak or need sharing. This quietly solves most of
   the problem.
2. **Local API keys** (DataForSEO, PostHog, Granola): `.env` copied from
   `.env.example`, gitignored. For team sharing, use a secrets manager CLI
   (1Password recommended): commit `.env.op` containing `op://` *references*
   (not values) and run tooling via `op run --env-file=.env.op`. Bitwarden
   Secrets Manager is the alternative. Never paste keys in Slack.
3. **CI keys** (the transcript cron): GitHub Actions repository secrets.

*Rejected:* encrypted secrets committed in-repo (sops/age): a key-management
ceremony this audience will get wrong.

## The routing design: "how many people attended event X and then signed up?"

The repo's job is to make any coding agent answer questions like this
correctly, in any tool. Three redundant mechanisms, because different tools
load different things:

1. **AGENTS.md carries a routing table** (universally loaded: imported by
   CLAUDE.md, read natively by Cursor and Codex): check
   `data/<domain>/snapshots/` for fresh-enough data → if missing or stale,
   pull from the source system via the integration listed in
   `integrations/README.md` and save it as a properly named snapshot →
   interpret using `data/ontology/` → answer inline; offer a dashboard only
   when asked or when the answer is genuinely multidimensional. Plus a
   "where things live" table mapping question types to folders.
2. **Folder READMEs are machine contracts**: each states what is
   authoritative there, the naming convention, and what to do when data is
   missing, so even an agent that wandered in without the table
   self-corrects.
3. **The `analyst` skill** encodes the full procedure with worked examples,
   and its frontmatter description is written to trigger on quantitative
   marketing questions, so skill-aware tools route to it automatically.

Redundancy is the point: the same question gets the same treatment whether it
was asked in Claude Code, Cursor, or Codex.
