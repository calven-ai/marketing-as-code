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
- **Never read `.env`**: a rule, not a wall. The checked-in
  `.claude/settings.json` carries only this repo's own machinery (the
  allow-list for the lifecycle scripts, the doctor hook, and the write-tool
  deny rules `wire_integration.py` adds for a server declared here), so
  nothing stops you mechanically. Keys stay out of context because you keep
  them out; [docs/secrets.md](docs/secrets.md) has the deny rules to copy
  into your own settings if you want them enforced.
- **Every session opens with the doctor's lines** (a `SessionStart` hook
  runs `scripts/doctor.py --brief`). Act on them before anything else:
  problems mean `/doctor`, unfilled templates mean `/setup`, "make it
  yours" items mean [docs/make-it-yours.md](docs/make-it-yours.md).
- MCP servers for integrations are declared in `.mcp.json` (DataForSEO, Apify
  and Calven today; the list is explained in
  [integrations/README.md](integrations/README.md)). Claude Code asks about
  all three in the first session, before `/setup` has run: No to all three
  is the right answer, and `/setup` says which to turn on afterwards.
