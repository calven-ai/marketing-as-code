# AGENTS.md: the agent contract for Marketing as Code

This file is the operating contract for any coding agent working in this
repository (Claude Code, Codex, Cursor, or any AGENTS.md-aware tool).
Claude-Code-specific notes live in [CLAUDE.md](CLAUDE.md).

> **Status:** skeleton. The full contract (setup interview, per-folder fill
> rules, review workflow, memory pipeline) lands as the templates land.

## What this repository is

The second brain of a marketing team, as plain text. Strategy, messaging,
content, campaigns, data, decisions, and the agents' own instructions live
here, versioned. Agents read all of it and write into it; a human reviews and
decides.

## Ground rules

1. **Load context before working.** Read `strategy/` (positioning, messaging,
   voice) before drafting or reviewing any marketing work.
2. **Humans decide.** Agents propose: drafts, reports, prototypes, backlog
   items. Publishing, sending, and deleting need explicit human approval.
3. **Plain text first.** Markdown for knowledge, CSV for data, Issues for
   tasks. No binary files where text will do.
4. **Never commit credentials.** Keys live in untracked `.env` files. The
   `.gitignore` excludes every `.env*` variant except `.env.example`.
5. **Log decisions.** When a meeting or discussion resolves something, record
   it in `memory/decision-log.md` and file follow-ups as Issues.
6. **Prototypes are disposable.** Everything in `playgrounds/` is throwaway by
   design, never production, and gets archived once the decision is logged.
