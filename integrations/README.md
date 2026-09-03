# integrations/

**Kind:** agents, the workforce as instructions in English.

The registry of external tools this repo's agents can operate, and how each
one connects. Five integrations ship wired, as worked examples of the three
ways to connect a tool; the rest of your stack is added by your coding
agent following [adding-an-integration.md](adding-an-integration.md)
(MCP server first, vendor CLI second, a script last). Nothing here is a
promise that a connector will be built for you.

## Wired in this template

| Tool | For | Mechanism | Auth | Env vars (in `.env`) | Status |
| --- | --- | --- | --- | --- | --- |
| DataForSEO | keywords, SERP, audits, backlinks, LLM mentions (`seo-analyst`, `brand-monitor`, `campaign-discovery`) | official MCP in `.mcp.json` (session use) plus `scripts/seo_snapshot.py` (the scheduled refresh) | login/password | `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | wired |
| Apify | actors for ABM research (`researcher`) | official remote MCP in `.mcp.json` | OAuth (in-browser) | none | wired |
| Calven | marketing context layer: positioning, messaging, ICP, product brief, personas, competitors and battlecards, customer voice, served live to every agent (made by this repo's maintainer) | official remote MCP (Streamable HTTP) in `.mcp.json` | MCP key | `CALVEN_MCP_KEY` | wired, optional; setup in [context-layer.md](context-layer.md) |
| Granola | meeting transcripts into `memory/transcripts/inbox/` | `scripts/pull_transcripts.py`, by hand or daily via `.github/workflows/transcripts-cron.yml` (opens a PR). Granola's own MCP is OAuth-only, so the script carries the unattended path | API key | `GRANOLA_API_KEY` | wired |
| Slack | the team's front door: digests, announcements, alerts out; requests in; red flags to leadership | the team's own Slack app ([slack/](slack/)), bot token, no server; `scripts/slack_post.py` | bot token | `SLACK_BOT_TOKEN`, `SLACK_REQUESTS_CHANNEL_ID`, `SLACK_TEAM_CHANNEL_ID`, `SLACK_LEADERSHIP_CHANNEL_ID` | manifest and post script wired; inbound intake is yours to add |

The Env vars column mirrors `.env.example`; agents are blocked from reading
any `.env*` file (see [docs/secrets.md](../docs/secrets.md)), so keep the
two in sync.

Who holds which key: Apify is per person (OAuth, no key); `CALVEN_MCP_KEY`
is per person; `DATAFORSEO_*` is per person where the vendor allows;
`GRANOLA_API_KEY` and `SLACK_BOT_TOKEN` are bot keys that live only in the
GitHub environment `automation`. The full table, with owners, rotation and
what to do when someone leaves, is in [docs/secrets.md](../docs/secrets.md);
add a row there for every integration you wire.

## Known routes for common tools

Not wired. Each row says how your agent would add the tool, by the tier in
[adding-an-integration.md](adding-an-integration.md); the fuller table
there has endpoints and caveats. Checked September 2026; verify on the day.

| Tool | For | Tier, and how you would add it | Auth | Env vars it would need |
| --- | --- | --- | --- | --- |
| Asana | tasks | official remote MCP, with write tools; rewrite [tasks.md](tasks.md) from its embedded example | OAuth | none |
| monday.com | tasks (alternative) | official MCP; same shape as Asana | OAuth | none |
| HubSpot | CRM: pipeline, signups, email | official remote MCP for questions and CRM writes; a script for scheduled pipeline snapshots into `data/crm/snapshots/` | OAuth (MCP); private-app token (script) | none for the MCP; `HUBSPOT_ACCESS_TOKEN` for a script |
| Salesforce | CRM | vendor MCP for questions; the `sf` CLI for scheduled exports | OAuth | none |
| PostHog | web/product analytics | official remote MCP for questions; `posthog-cli` for scheduled pulls into `data/analytics/snapshots/` | personal API key | `POSTHOG_API_KEY`, `POSTHOG_PROJECT_ID`, `POSTHOG_HOST` |
| Google Analytics 4 | web analytics | official stdio MCP (Python) in a session; a script with a service account on a schedule | Google credentials | `GOOGLE_APPLICATION_CREDENTIALS` |
| Zoom | meeting transcripts | vendor MCP for ad hoc reading; a Server-to-Server OAuth script for the inbox pull (the guide's worked example) | OAuth app | `ZOOM_ACCOUNT_ID`, `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET` |

## MCP servers, per coding agent

`.mcp.json` (Claude Code) and `.cursor/mcp.json` (Cursor) list the same
three servers; Codex users paste the TOML from
[adding-an-integration.md](adding-an-integration.md#configuring-an-mcp-server-per-coding-agent)
into their own config. `scripts/doctor.py` checks the two JSON files agree.

- **`dataforseo`**: the official `dataforseo-mcp-server` npm package, run
  with `npx` and **pinned to a version** (`@3.1.1`), because an unpinned
  `npx -y` would run whatever was published last, with your DataForSEO
  login in its environment. Bump the version deliberately, in a proposal.
  Credentials come from `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` in
  your environment (the files use placeholders, so they hold no values;
  `DATAFORSEO_USERNAME` is set to the same login because the vendor's docs
  use that name). A remote endpoint exists too (`https://mcp.dataforseo.com/v3/mcp`,
  Basic auth header); swap the entry if you prefer not to run `npx`.
- **`apify`**: the official remote server at `https://mcp.apify.com`,
  OAuth in the browser on first use, no key.
- **`calven`**: the remote server at `https://app.calven.ai/api/mcp`,
  bearer key from `CALVEN_MCP_KEY`. This is the context-layer example from
  [context-layer.md](context-layer.md); the repo works without it.

All three entries follow the vendors' public docs as of September 2026; if
a vendor changes its server, edit both files and this list together.
Interactive Claude Code sessions ask before enabling project-scoped
servers; non-interactive runs (the GitHub action, `claude -p`) load them
without asking, which is why the entries hold placeholders and never
values. OAuth tools need no keys at all; each person authorizes in the
browser. For the rest, keys go in `.env` (copied from `.env.example`, never
committed), and the placeholders are filled from the **environment**, not
from `.env`: start the agent with `sh scripts/with_env.sh claude` in a
terminal, or add the variables in the Claude desktop app's Local
environment editor; see [docs/secrets.md](../docs/secrets.md).

## [tasks.md](tasks.md): the task-tool adapter

The one file that tells every agent where tasks go and how to file them.
`/setup` fills it in for your team's tool; until then it documents the
zero-setup fallback. **Any skill that creates tasks reads `tasks.md` first.**
That's the whole abstraction.

## For agents

- Pulling data? Use the mechanism in the registry, and save the pull as a
  snapshot per `data/README.md` naming.
- An integration isn't connected? Say exactly what export the human should
  make and where to drop it. Don't guess, and don't try to connect tools
  yourself without being asked.
- Asked to connect or build a tool? Run `add-integration`, or follow
  [adding-an-integration.md](adding-an-integration.md) by hand. One PR,
  with the checklist from that page in its description.
