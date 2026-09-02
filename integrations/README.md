# integrations/

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
| DataForSEO | keywords, SERP, audits, backlinks, LLM mentions | official MCP | login/password | `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | setup doc coming |
| Apify | social scraping for ABM | official remote MCP | OAuth | none | wave 3 |
| Granola | meeting transcripts | `scripts/pull_transcripts.py` | API key | `GRANOLA_API_KEY` | wave 2 |
| Zoom | meeting transcripts | script | OAuth app | tbd | wave 3 |
| Slack | the team's front door: digests, announcements, alerts out; requests in | the team's own Slack app ([slack/](slack/)), bot token, no server | bot token | `SLACK_BOT_TOKEN`, `SLACK_REQUESTS_CHANNEL_ID`, `SLACK_TEAM_CHANNEL_ID` | manifest ready; scripts wave 2 |

The Env vars column mirrors `.env.example`; agents are blocked from reading
any `.env*` file (see [docs/secrets.md](../docs/secrets.md)), so keep the
two in sync.

MCP servers will be listed in `.mcp.json` (Claude Code) and
`.cursor/mcp.json` (Cursor) — neither file exists yet (wave 2). Once they
do, servers stay disabled until `/setup` enables the ones your team uses.
OAuth tools need no keys at all — each person authorizes in the browser. For
the rest, keys go in `.env` (copied from `.env.example`, never committed) —
see [docs/secrets.md](../docs/secrets.md).

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
