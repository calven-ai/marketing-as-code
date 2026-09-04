# CLAUDE.md: Claude Code operating notes

@AGENTS.md

The agent contract lives in [AGENTS.md](AGENTS.md) (imported above). This file
adds only what is Claude-Code-specific.

- **Skills** are canonical in `.agents/skills/` and reach Claude Code through
  committed symlinks in `.claude/skills/` (one per skill; see
  `scripts/sync_skills.py`). Invoke them as slash commands: `/sync`,
  `/propose`, `/doctor`, `/setup`, `/new-content`, `/qmr`, and more; the roster is
  [agents/README.md](agents/README.md).
  If a slash command is missing, run `python3 scripts/sync_skills.py`.
- **Never read `.env`**: `.claude/settings.json` denies the Read tool and
  the file commands on it, plus `env`, `printenv`, one-liners and the
  merge and force-push commands a person owns; keys stay out of context
  by design, and [docs/secrets.md](docs/secrets.md) says exactly what the
  rules stop and what they do not.
- MCP servers for integrations are declared in `.mcp.json` (DataForSEO, Apify
  and Calven today; the list is explained in
  [integrations/README.md](integrations/README.md)). Enable only what
  `/setup` configured; Claude Code asks before starting a project server.
