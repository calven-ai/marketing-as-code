# CLAUDE.md: Claude Code operating notes

@AGENTS.md

The agent contract lives in [AGENTS.md](AGENTS.md) (imported above). This file
adds only what is Claude-Code-specific.

- **Skills** are canonical in `.agents/skills/` and reach Claude Code through
  committed symlinks in `.claude/skills/` (one per skill — see
  `scripts/sync_skills.py`). Invoke them as slash commands: `/setup`,
  `/new-content`, `/qmr`, … — the roster is [agents/README.md](agents/README.md).
  If a slash command is missing, run `python3 scripts/sync_skills.py`.
- **Never read `.env`** — `.claude/settings.json` denies it; keys stay out of
  context by design (see [docs/secrets.md](docs/secrets.md)).
- MCP servers for integrations will be declared in `.mcp.json` (wave 2 of
  the [roadmap](docs/roadmap.md)); it does not exist yet. Once it does,
  enable only what `/setup` configured.
