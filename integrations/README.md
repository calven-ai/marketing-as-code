# integrations/

**Kind:** agents, the workforce as instructions in English.

The registry of tools this repo's agents can reach, and how each one
connects. Five ship wired. The rest of your stack is a job for your coding
agent, by the rules in [adding-an-integration.md](adding-an-integration.md).

## Wired in this template

| Tool | For | Mechanism | Auth | Env vars (in `.env`) | Status |
| --- | --- | --- | --- | --- | --- |
| DataForSEO | keywords, SERP, audits, backlinks, LLM mentions (`seo-analyst`, `brand-monitor`, `campaign-discovery`) | official MCP in `.mcp.json` for sessions; `scripts/seo_snapshot.py` for the scheduled refresh | login/password | `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | wired |
| Apify | actors for ABM research (`researcher`) | official remote MCP in `.mcp.json` | OAuth, in the browser | none | wired |
| Calven | the marketing context layer: positioning, messaging, ICP, product brief, personas, competitors, customer voice, served live to every agent | official remote MCP in `.mcp.json` | MCP key | `CALVEN_MCP_KEY` | wired, optional; setup in [context-layer.md](context-layer.md) |
| Granola | meeting transcripts into `memory/transcripts/inbox/` | `scripts/pull_transcripts.py`, by hand or daily via `.github/workflows/transcripts-cron.yml`. Granola's MCP is OAuth-only, so the script carries the unattended path | API key | `GRANOLA_API_KEY` | wired |
| Slack | the team's front door: digests, alerts and red flags out; requests in | the team's own Slack app ([slack/](slack/)) and `scripts/slack_post.py`, no server | bot token | `SLACK_BOT_TOKEN`, `SLACK_REQUESTS_CHANNEL_ID`, `SLACK_TEAM_CHANNEL_ID`, `SLACK_LEADERSHIP_CHANNEL_ID` | manifest and post script wired; inbound intake is yours to add |

The Env vars column mirrors `.env.example`. Agents cannot read any `.env*`
file, so keep the two in sync. Who owns each key, where it lives and how to
rotate it is in [docs/secrets.md](../docs/secrets.md).

## Known routes for common tools

Not wired. Your agent adds these by the ladder in the guide, which carries
the endpoints, the write support and the caveats per tool: Asana,
monday.com, HubSpot, Salesforce, PostHog, Google Analytics 4, Zoom, and
GitHub itself. Checked September 2026. Verify on the day you wire one.

## MCP servers, per coding agent

`.mcp.json` (Claude Code) and `.cursor/mcp.json` (Cursor) list the same
three servers. Codex users paste the TOML from
[the guide](adding-an-integration.md#configuring-an-mcp-server-per-coding-agent).
`scripts/doctor.py` checks the two JSON files agree.

- **`dataforseo`**: the official `dataforseo-mcp-server` npm package, run
  with `npx` and pinned to `@3.1.1`. Unpinned `npx -y` would run whatever
  was published last, with your DataForSEO login in its environment. Bump
  the version on purpose, in a proposal. Credentials come from
  `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` in your environment. A
  remote endpoint exists too (`https://mcp.dataforseo.com/v3/mcp`, Basic
  auth); swap the entry if you prefer not to run `npx`.
- **`apify`**: the official remote server at `https://mcp.apify.com`.
  OAuth in the browser on first use, no key.
- **`calven`**: the remote server at `https://app.calven.ai/api/mcp`,
  bearer key from `CALVEN_MCP_KEY`. The repo works without it.

The entries hold placeholders, never values. Non-interactive runs (the
GitHub action, `claude -p`) load project servers without asking, so a value
in the file would run anywhere the repo is checked out. Placeholders are
filled from the environment, not from `.env`; how to start an agent with
them is in [docs/secrets.md](../docs/secrets.md).

## [tasks.md](tasks.md): the task-tool adapter

The one file that tells every agent where tasks go and how to file them.
`/setup` fills it in for your team's tool. Until then it documents the
zero-setup fallback. **Any skill that creates tasks reads `tasks.md` first.**
That is the whole abstraction.

## For agents

- Pulling data? Use the mechanism in the registry and save the pull as a
  snapshot, named per `data/README.md`.
- Integration not connected? Say exactly what export the human should make
  and where to drop it. Never guess, and never connect a tool unasked.
- Asked to connect or build a tool? Run `add-integration`, or follow
  [adding-an-integration.md](adding-an-integration.md) by hand. One PR,
  with that page's checklist in its description.
