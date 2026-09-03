# Secrets: keys without the pain (or the leaks)

Three tiers, from "no key exists" down. The `.gitignore` already refuses
every `.env*` variant except `.env.example`; never work around it.

## Tier 1: OAuth (most tools need no key at all)

Asana, monday.com, HubSpot, and Apify connect through official remote MCP
servers using OAuth: the first time an agent uses one, your browser opens,
you sign in, done. Nothing to store, share, rotate, or leak, and each
teammate authorizes as themselves. **Prefer these whenever a tool offers
them.**

## Tier 2: local API keys, shared through a secrets manager

Some tools use plain keys (DataForSEO, PostHog, Granola). Locally:

1. Copy `.env.example` to `.env` (stays on your machine, gitignored).
2. Fill in only the keys for tools you actually use.

**Sharing with the team: never paste keys in Slack or email.** Use a secrets
manager the team already has:

- **1Password (recommended):** store each key in a shared vault. With the
  1Password CLI, a committed `.env.op` file can hold *references* like
  `op://Marketing/DataForSEO/credential` (safe to commit because they
  contain no secret), and `op run --env-file=.env.op -- <command>` injects
  real values at runtime. Rotating a key updates everyone at once.
- **Bitwarden Secrets Manager** works the same way for Bitwarden teams.
- No manager? Share via each tool's own team features (invite teammates so
  they generate their *own* keys) before falling back to a password-manager
  shared note.

## Tier 3: CI keys

Automation that runs on GitHub (the transcript cron, wave 2) gets keys from
**GitHub Actions repository secrets** (repo → Settings → Secrets and
variables → Actions). Same rules: one secret per key, no secrets in
workflow files.

## House rules

- A key that ever lands in a commit is **burned**: rotate it immediately;
  removing the commit is not enough, history is forever.
- Agents never read `.env` and never echo key values into files, logs, or
  chat. Claude Code enforces part of this: `.claude/settings.json` denies
  the Read tool (and `cat`/`head`/`tail`/`sed` in Bash) on every `.env*`
  file, including `.env.example`, which is why the variable names are also
  listed in `integrations/README.md`. The rule cannot stop a script that
  opens the file itself, so scripts in this repo read keys only from the
  environment and never print them.
- Scope keys down where the provider allows (read-only, project-scoped).
