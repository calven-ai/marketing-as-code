# integrations/

**Kind:** agents, the workforce as instructions in English.

The registry of external tools this repo's agents can operate, and how each
one connects. One setup doc per tool lands here as integrations come online
(wave 2 of [the roadmap](../docs/roadmap.md)).

## The registry

| Tool | For | Mechanism | Auth | Env vars (in `.env`) | Status |
| --- | --- | --- | --- | --- | --- |
| Asana | tasks | official remote MCP | OAuth (in-browser) | none | setup doc coming |
| monday.com | tasks (alternative) | official MCP | OAuth | none | wave 3 |
| HubSpot | CRM: pipeline, signups, email | official remote MCP | OAuth | none | setup doc coming |
| PostHog | web/product analytics | official MCP / `posthog-cli` | API key | `POSTHOG_API_KEY`, `POSTHOG_PROJECT_ID`, `POSTHOG_HOST` | setup doc coming |
| Google Analytics 4 | web analytics | Google's official MCP | service account | `GOOGLE_APPLICATION_CREDENTIALS` | setup doc coming |
| DataForSEO | keywords, SERP, audits, backlinks, LLM mentions (`seo-analyst`, `brand-monitor`, `campaign-discovery`) | official MCP, listed in `.mcp.json` | login/password | `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | in `.mcp.json`; setup doc coming |
| Apify | actors for ABM research (`researcher`) | official remote MCP, listed in `.mcp.json` | OAuth | none | in `.mcp.json`; setup doc coming |
| Granola | meeting transcripts | `scripts/pull_transcripts.py` (by hand, or daily via `.github/workflows/transcripts-cron.yml`, which opens a PR) | API key | `GRANOLA_API_KEY` | script ready |
| Zoom | meeting transcripts | script | OAuth app | tbd | wave 3 |
| Slack | the team's front door: digests, announcements, alerts out; requests in; red flags to leadership | the team's own Slack app ([slack/](slack/)), bot token, no server; `scripts/slack_post.py` | bot token | `SLACK_BOT_TOKEN`, `SLACK_REQUESTS_CHANNEL_ID`, `SLACK_TEAM_CHANNEL_ID`, `SLACK_LEADERSHIP_CHANNEL_ID` | manifest and post script ready; inbound intake wave 2 |

The Env vars column mirrors `.env.example`; agents are blocked from reading
any `.env*` file (see [docs/secrets.md](../docs/secrets.md)), so keep the
two in sync.

MCP servers are listed in `.mcp.json` (Claude Code; `.cursor/mcp.json` for
Cursor is wave 2). Two are in there today:

- **`dataforseo`**: the official `dataforseo-mcp-server` npm package, run
  with `npx`, credentials taken from `DATAFORSEO_LOGIN` and
  `DATAFORSEO_PASSWORD` in your environment (`.mcp.json` uses `${VAR}`
  placeholders, so the file holds no values). The package also accepts
  `DATAFORSEO_USERNAME` as an alias. A remote endpoint exists too
  (`https://mcp.dataforseo.com/v3/mcp`, Basic auth header); swap the entry
  if you prefer not to run `npx`.
- **`apify`**: the official remote server at `https://mcp.apify.com`,
  OAuth in the browser on first use, no key.

Both entries follow the vendors' public docs as of September 2026; if a
vendor changes its server, edit `.mcp.json` and this list together. Claude
Code asks before enabling project-scoped servers, so nothing runs until
you approve it. OAuth tools need no keys at all — each person authorizes
in the browser. For the rest, keys go in `.env` (copied from
`.env.example`, never committed) — see [docs/secrets.md](../docs/secrets.md).

## [tasks.md](tasks.md) — the task-tool adapter

The one file that tells every agent where tasks go and how to file them.
`/setup` fills it in for your team's tool; until then it documents the
zero-setup fallback. **Any skill that creates tasks reads `tasks.md` first**
— that's the whole abstraction.

## For agents

- Pulling data? Use the mechanism in the registry, and save the pull as a
  snapshot per `data/README.md` naming.
- An integration isn't connected? Say exactly what export the human should
  make and where to drop it. Don't guess, and don't try to connect tools
  yourself without being asked.
