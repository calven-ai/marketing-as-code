# Adding an integration: MCP first, CLI second, a script last

**Kind:** agents, the workforce as instructions in English.

Five integrations ship wired, as worked examples of the three ways to
connect a tool. Everything else in your stack is added by your coding
agent, following this page. Read it when the team says "we use X, connect
it", "automate pulling Y", or "why can't the agent see Z". The
`add-integration` skill walks through it step by step.

Two principles decide most of what follows:

- **Do not build what you can connect.** A vendor's MCP server or CLI is
  maintained by the vendor. A script in `scripts/` is maintained by you.
  Write code only when nothing else does the job.
- **The tier depends on who runs it.** An MCP call happens in an
  interactive session, with a person watching. Anything unattended (GitHub
  Actions) runs a CLI or a script. So the same tool can appear twice, on
  purpose: the DataForSEO MCP for questions in a session,
  `scripts/seo_snapshot.py` for the weekly refresh. Which mode a workflow
  runs in is the team's choice
  ([docs/operating-model.md](../docs/operating-model.md)).

## The ladder

| Tier | What | When it is the answer | Who maintains it |
| --- | --- | --- | --- |
| 1. Official MCP server | The vendor's own server, listed in `.mcp.json` (and the Cursor and Codex equivalents). Prefer remote with OAuth, then remote with a key, then a local stdio server | The default for anything a person asks an agent in a session: reading, and writing where the server has write tools | The vendor |
| 2. Vendor CLI | The vendor's command-line tool, called by a skill or a script, output saved as a snapshot | Scheduled or unattended runs; bulk pulls; a write the MCP lacks | The vendor |
| 3. Custom script | Stdlib Python in `scripts/`, following the contract below | No MCP and no CLI; or the run is unattended and the CLI cannot do it | You |

Move down a tier only for one of these reasons, and say which in the PR:

1. No official server or CLI exists. A community MCP server is somebody
   else's script: judge it as tier 3, not tier 1.
2. The workflow needs a write the server does not offer. Check the tool
   list first; the common task tools and CRMs do offer writes.
3. The run is unattended, scheduled, or must produce a deterministic
   snapshot. OAuth servers cannot run headless at all.
4. The pull is bulk (hundreds of rows on a schedule) and per-call MCP use
   is slow or wasteful.

Never, at any tier: put a key value in `.mcp.json` or any committed file
(env placeholders only), read `.env` from an agent, run an unpinned package
(`npx -y name@1.2.3`, never `npx -y name`), or wire a tool nobody asked for.

## Known routes for common tools

Checked September 2026 against the vendors' own documentation. Vendors
change their servers often. Verify the endpoint and the tool list on the
day you wire it, and correct this table in the same PR.

| Tool | Official MCP | Writes over MCP | CLI | The usual route |
| --- | --- | --- | --- | --- |
| Asana | remote, OAuth (`https://mcp.asana.com/v2/mcp`) | yes: create and update tasks; interactive tools confirm before committing | none official | MCP for everything, including filing tasks. `integrations/tasks.md` carries the conventions |
| monday.com | official MCP, OAuth | check the tool list | none official | MCP; same shape as Asana |
| HubSpot | remote, OAuth (`mcp.hubspot.com`), GA | yes on CRM objects and engagements; marketing content and campaign metrics read-only | `hs` exists but is developer tooling for CMS and projects, not CRM data | MCP for questions and CRM writes; a script for scheduled pipeline snapshots |
| Salesforce | vendor MCP offerings exist; verify which one your org licenses | check the tool list | `sf` CLI: queries, exports, record updates | MCP for questions; `sf` for scheduled exports and bulk work |
| PostHog | remote, personal API key (`https://mcp.posthog.com/mcp`) | yes, with read-only filtering available | `posthog-cli` | MCP for questions; the CLI for scripted, scheduled pulls |
| Google Analytics 4 | official, but a local stdio server (Python, `pipx`) using Google credentials | read-only | none for reporting; `gcloud` for auth only | stdio MCP in a session; a script with a service account for schedules |
| DataForSEO | stdio (`npx dataforseo-mcp-server`) or remote with Basic auth; wired in `.mcp.json` | n/a (data vendor) | none | MCP in a session; `scripts/seo_snapshot.py` for the weekly refresh |
| Apify | remote, OAuth (`https://mcp.apify.com`); wired | runs actors | `apify` CLI | MCP for research in a session; the CLI if a run is ever scheduled |
| Granola | remote, OAuth (`https://mcp.granola.ai/mcp`), paid plans | read-only | none | MCP for "what did we discuss"; `scripts/pull_transcripts.py` for the daily inbox pull (the MCP cannot run headless) |
| Zoom | a vendor MCP exists (transcripts, summaries, recordings; OAuth); verify its tool list | check | none for transcripts | MCP for ad-hoc reading; a Server-to-Server OAuth script for the inbox pull |
| Slack | Anthropic's own Slack app for "ask the repo from Slack"; no vendor MCP wired here | n/a | none needed | the team's own bot via `scripts/slack_post.py` (`slack/`); see the three layers there |
| GitHub | n/a inside a repo | n/a | `gh`, present on every Actions runner | the CLI, as `.github/workflows/transcripts-cron.yml` does |

## Configuring an MCP server, per coding agent

The four tools this repo is written for read different files. The server
list is the same; the syntax is not, and one difference bites silently.

| Coding agent | File | Shape | Env var syntax | OAuth login |
| --- | --- | --- | --- | --- |
| Claude Code | `.mcp.json` at the repo root (committed) | `mcpServers.<name>` with `"type": "stdio"` + `command`/`args`/`env`, or `"type": "http"` + `url`/`headers` | `${VAR}` and `${VAR:-default}`, expanded in `command`, `args`, `env`, `url`, `headers` | `claude mcp login <name>`, or the prompt on first use |
| Cursor | `.cursor/mcp.json` (committed) | same `mcpServers.<name>`, no `type` key: `command`/`args`/`env` or `url`/`headers` | `${env:VAR}` (a bare `${VAR}` is passed through as literal text) | browser prompt on first use |
| Codex | `~/.codex/config.toml` (global) or `.codex/config.toml` (trusted projects only) | `[mcp_servers.<name>]` with `command`/`args`/`env`, or `url` + `bearer_token_env_var` / `http_headers` / `env_http_headers` | `bearer_token_env_var = "VAR"` names the variable; do not inline the value | `codex mcp login <name>` |
| Claude desktop app, chat | Settings > Connectors (UI) | remote servers only, added by URL per person | n/a | in the UI |

Three traps:

- **Entries stay key-free.** `.mcp.json` holds placeholders
  (`${CALVEN_MCP_KEY}`), never values. Non-interactive runs (`claude -p`,
  the GitHub action, cloud sessions) load project servers without asking,
  so a value in that file would run anywhere the repo is checked out.
- **Do not copy `.mcp.json` to `.cursor/mcp.json` byte for byte.** Change
  `${VAR}` to `${env:VAR}` and drop the `type` key. `scripts/doctor.py`
  checks that both files list the same server names.
- **Codex gets a snippet, not a committed file.** Its project config only
  loads for trusted projects and its auth fields differ. Put the TOML in
  the PR description and in the registry row.

The chat surfaces (the Claude desktop app's chat, ChatGPT) run connectors,
not this repo's skills or scripts. They are stage 1 in
[docs/stages.md](../docs/stages.md). The coding agents are Claude Code,
Cursor and Codex.

The remote entry with a key, in the three forms:

```json
"calven": {
  "type": "http",
  "url": "https://app.calven.ai/api/mcp",
  "headers": { "Authorization": "Bearer ${CALVEN_MCP_KEY}" }
}
```

```json
"calven": {
  "url": "https://app.calven.ai/api/mcp",
  "headers": { "Authorization": "Bearer ${env:CALVEN_MCP_KEY}" }
}
```

```toml
[mcp_servers.calven]
url = "https://app.calven.ai/api/mcp"
bearer_token_env_var = "CALVEN_MCP_KEY"
```

## The CLI tier

Install the vendor's CLI per its own docs: each person on their machine, and
a workflow step on the Actions runner. Authenticate as yourself. The CLI
keeps its own credential store, so nothing lands in `.env` unless the CLI
reads a variable; then the name goes into `.env.example` and the registry
row. Call it from a skill (which names the exact command) or from a script
(when the output needs reshaping). Prefer JSON output and save the result
under `data/<domain>/snapshots/` with the naming in
[data/README.md](../data/README.md). `gh` in
`.github/workflows/transcripts-cron.yml` is the shipped example.

## The script contract

Every script in `scripts/` follows these rules. The three shipped scripts
(`pull_transcripts.py`, `slack_post.py`, `seo_snapshot.py`) are the
reference; a new connector copies the closest one.

1. **Python 3.9 or newer, standard library only.** `urllib`, `json`, `csv`,
   `argparse`. No `requests`, no package to install. A marketer's laptop
   has Python; it does not have a virtualenv.
2. **Keys from the environment, then `.env` at the repo root.** Use
   `read_env_file` and `setting` from `scripts/_common.py`. Never print a
   key, not even in `--dry-run`. Scripts are the only code in this repo
   allowed to open `.env`.
3. **A missing key exits with a message that names the variable and where
   to get it.** Copy the `api_key()` function in `pull_transcripts.py`.
4. **`--dry-run` always exists** and writes nothing.
5. **Idempotent.** Re-running is safe: dedupe against what exists
   (`existing_filenames()` in `pull_transcripts.py`), and never overwrite a
   snapshot; write a new dated one.
6. **Output where the data lives.** Transcripts to
   `memory/transcripts/inbox/` in the inbox contract
   ([memory/transcripts/README.md](../memory/transcripts/README.md));
   tables to `data/<domain>/snapshots/YYYY-MM-DD-<source>-<what>.csv` with
   a header row and columns stable within the domain.
7. **A docstring in the shape of `slack_post.py`:** what it does, usage
   lines, where the configuration comes from, what is never printed.
8. **Readable errors, no tracebacks for expected failures** (401, network
   down, empty result). Exit code 1 on failure so a workflow step fails
   visibly.
9. **A row in `scripts/README.md`** and, for a scheduled run, a step in a
   workflow that opens a PR and never merges.

## What a finished integration contains

One PR, reviewed like any other, with this list in its description:

- [ ] A row in the registry table in [README.md](README.md) (tool, for,
      mechanism, auth, env vars, status), or a corrected "known route" row
- [ ] `.env.example` lines for every variable the mechanism reads, and the
      registry's Env vars column kept identical (agents cannot read `.env*`)
- [ ] For tier 1: the `.mcp.json` entry, the matching `.cursor/mcp.json`
      entry, and the Codex TOML snippet in the PR description
- [ ] For tier 2 or 3: the script (contract above) and its
      `scripts/README.md` row; for a scheduled run, the workflow step
      (`environment: automation` on the job) and the environment secret
      it needs
- [ ] A row in the "Who holds which key" table in
      [docs/secrets.md](../docs/secrets.md): per person or bot, who owns
      it, where it lives, how to rotate it
- [ ] Every package or action the integration runs is pinned (an npm
      version, a commit SHA), and the vendor's own server is preferred
      over a community one
- [ ] The skills that change: which `SKILL.md` "Needs:" line now names the
      tool, and what the skill does when it is not connected (say what
      export to drop where; never guess numbers)
- [ ] If the workflow recurs: both run modes stated where the workflow is
      described, per [docs/operating-model.md](../docs/operating-model.md)
- [ ] A `CHANGELOG.md` line
- [ ] A decision-log entry (`/log-decision`): which tool, which tier, why,
      who decided
- [ ] `python3 scripts/doctor.py` passes

## Worked example: "We use Zoom. Automate reading the transcripts."

Two jobs hide in that sentence, and they land on different tiers.

**Ad hoc: "what did we say about pricing on Tuesday?"** Tier 1. Add Zoom's
MCP server to `.mcp.json` and `.cursor/mcp.json` (OAuth, so no key), check
its tool list returns transcripts, and the agent reads them in the session.
Nothing else changes.

**The pipeline: every meeting lands in the inbox and gets processed.**
Tier 3, because it is unattended. The PR contains:

- `scripts/pull_transcripts_zoom.py`, a copy of `pull_transcripts.py` with
  the Granola API swapped for Zoom's Server-to-Server OAuth app. Same
  `--since`, `--limit`, `--dry-run`, same dedupe against `inbox/` and
  `processed/`, files written in the inbox contract with `source: zoom`.
- `.env.example`: a `ZOOM_ACCOUNT_ID`, `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET`
  block naming the Zoom App Marketplace page they come from.
- `.github/workflows/transcripts-cron.yml`: a second "Pull new transcripts"
  step calling the Zoom script, gated on its secrets like the Granola step.
- `integrations/README.md`: a Zoom row in "Wired in this template" and the
  "known route" row removed.
- `scripts/README.md`: one row. `memory/README.md` and
  `memory/transcripts/README.md`: "Granola or Zoom" where the pull is named.
- `CHANGELOG.md` line; decision-log entry "Transcripts pulled from Zoom".

Processing does not change. `chief-of-staff` reads the inbox and does not
care which provider wrote the file. That is what the inbox contract is for.

## Worked example: "File the action items in Asana."

Tier 1, with writes. The PR contains:

- `.mcp.json` and `.cursor/mcp.json`: the Asana entry (remote, OAuth, no
  key); the Codex snippet in the PR description.
- `integrations/tasks.md`: the "Current tool" section rewritten from its
  embedded example. Every task-creating skill already reads that file, so
  no skill changes.
- The registry row moved from "known routes" to "wired".
- `CHANGELOG.md` line; decision-log entry "Tasks live in Asana".

No script, no key, no workflow. The first time a person's agent files a
task, the browser opens for the OAuth grant, and Asana's interactive tools
confirm before anything is created.

## Contributing a connector back

A connector that follows this page is welcome upstream as an example others
copy ([CONTRIBUTING.md](../CONTRIBUTING.md)). The maintainers do not build
or keep connectors for tools they do not use; the ladder is the promise.
