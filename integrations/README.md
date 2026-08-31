# integrations/

The registry of external tools this repo's agents can operate, and how each
one connects. One setup doc per tool lands here as integrations come online
(wave 2 of [the roadmap](../docs/roadmap.md)).

## The registry

| Tool | For | Mechanism | Auth | Status |
| --- | --- | --- | --- | --- |
| Asana | tasks | official remote MCP | OAuth (in-browser) | setup doc coming |
| monday.com | tasks (alternative) | official MCP | OAuth | wave 3 |
| HubSpot | CRM: pipeline, signups, email | official remote MCP | OAuth | setup doc coming |
| PostHog | web/product analytics | official MCP / `posthog-cli` | API key (`.env`) | setup doc coming |
| Google Analytics 4 | web analytics | Google's official MCP | service account | setup doc coming |
| DataForSEO | keywords, SERP, audits, backlinks, LLM mentions | official MCP | login/password (`.env`) | setup doc coming |
| Apify | social scraping for ABM | official remote MCP | OAuth | wave 3 |
| Granola | meeting transcripts | `scripts/pull_transcripts.py` | API key (`.env`) | wave 2 |
| Zoom | meeting transcripts | script | OAuth app | wave 3 |

MCP servers are listed in `.mcp.json` (Claude Code) and `.cursor/mcp.json`
(Cursor) but stay disabled until `/setup` enables the ones your team uses.
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
