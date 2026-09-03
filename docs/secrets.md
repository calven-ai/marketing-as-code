# Secrets: who holds which key, and where it lives

Every integration in this repo needs one of three things: nothing (OAuth,
you sign in with your browser), a key that belongs to you, or a key that
belongs to a bot. This page says which is which, where each one lives, and
what the agents can and cannot do with them. Written for the person who
sets the repo up and for everyone who works in it afterwards.

## Two facts first

1. **Keys in GitHub only serve unattended runs.** A secret stored in GitHub
   (Settings → Environments, or Settings → Secrets) can be *written* by an
   admin and *read* by nobody: not by a person, not by a script on a laptop,
   not by a coding agent. Only a workflow running on GitHub's own machines
   sees it. So "put the key in GitHub and let the team use it" is not a
   thing. A person working locally needs their own key; GitHub holds the
   keys for the daily cron and the optional agent in Actions, and nothing
   else.
2. **A key that lands in a commit is burned.** Rotate it at the vendor the
   moment you notice; removing the commit is not enough, because history is
   forever and every clone has a copy. The lint refuses to commit anything
   shaped like a key, and the pre-push hook refuses to push it, but the rule
   stands regardless.

## Who holds which key

| Credential | Kind | Who owns it | Where it lives | Rotate it at | When someone leaves |
| --- | --- | --- | --- | --- | --- |
| Apify | per person, OAuth | each person | nowhere; the browser grant on first use | Apify: revoke the grant | remove them from the Apify organization |
| `CALVEN_MCP_KEY` | per person | each person | their own `.env` (or the desktop app's Local environment), their own 1Password item | Calven: Settings → Integrations → MCP | revoke their key in Calven |
| `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | per person where DataForSEO gives teammates their own login; otherwise the owner's, treated as a bot key | the integrations owner | each person's `.env`; the owner's copy in the shared vault; an environment secret only if a scheduled snapshot run is ever added | DataForSEO dashboard | rotate if it was ever shared with them |
| `GRANOLA_API_KEY` | bot (the daily pull) | the integrations owner | the GitHub environment `automation`; the owner's vault item | Granola: Settings → Connectors → API keys | rotate if they were the owner |
| `SLACK_BOT_TOKEN` | bot (the team's Slack app) | the Slack workspace admin | the GitHub environment `automation`; the shared vault, visible to the owner only | Slack app page: Reinstall to Workspace | rotate if they had it |
| `ANTHROPIC_API_KEY` | bot (the optional agent in Actions) | the integrations owner | the GitHub environment `automation`, nowhere else; people use their own coding-agent subscription locally, never this key | Anthropic Console; set a spend cap | rotate |
| `SLACK_*_CHANNEL_ID` | not a secret | anyone | repository Actions variables; `.env` | n/a | n/a |
| `GITHUB_TOKEN` | automatic, per workflow job | GitHub | nowhere; it exists for the length of a job with only the permissions the job declares | automatic | n/a |

Two kinds, then: **your keys**, which each person makes for themselves and
keeps on their own machine, and **the bot keys**, which one person makes
once and puts in GitHub. Add a row here for every integration you wire
([integrations/adding-an-integration.md](../integrations/adding-an-integration.md)
asks for it).

**One integrations owner.** Name one person (in
`.github/CODEOWNERS`, and in `memory/decision-log.md`) who creates the bot identities, puts each bot key in
the shared vault and in the `automation` environment, and rotates them.
Everyone else never sees a bot key. This is the "one owner, at setup, then
rarely" line in [is-this-for-you.md](is-this-for-you.md).

## Your keys, on your machine

1. Get invited to the vendor's workspace (Calven, DataForSEO, Apify) and
   generate **your own** key there. Do not ask a teammate for theirs.
2. Copy `.env.example` to `.env` at the repo root and fill in only the keys
   for tools you use. `.env` is gitignored; the lint fails if one is ever
   tracked. Keep a copy of each key in your own 1Password item.
3. Start your coding agent with the keys in its environment. The MCP servers
   in `.mcp.json` read placeholders like `${CALVEN_MCP_KEY}` from the
   **environment**, not from `.env`, so `.env` alone does nothing for them:
   - **Terminal:** `sh scripts/with_env.sh claude` (or `cursor .`, or any
     command). The launcher exports `.env` and starts the command; it
     prints nothing.
   - **Claude desktop app:** it does not read your shell, so open its
     Local environment editor (the environment settings for local sessions)
     and add the same variables there; they are stored encrypted on your
     machine and apply to every local session.
   - **1Password CLI users:** put references in `.env` instead of values,
     one per line, like `CALVEN_MCP_KEY=op://Private/Calven MCP/credential`.
     The launcher sees `op://` and runs the command through `op run`, which
     resolves the references at start and masks them in output. Scripts
     refuse an unresolved reference with a message, never by printing it.
4. Scripts (`scripts/*.py`) read `.env` themselves, so they work either way.

Never paste a key into a chat with an agent, into Slack, or into email. If
an agent asks you for a key, tell it where the key lives instead; the
skills are written to do exactly that.

## The bot keys, only in GitHub

The daily transcript pull, the Slack alert when `main` is red, and the
optional agent in Actions run with nobody watching, so they need keys that
belong to nobody. Those three keys live in one place:

**Settings → Environments → `automation` → Environment secrets.**
`sh scripts/github_setup.sh` creates the environment and restricts it to
the `main` branch; the click path is in
[github-settings.md](github-settings.md). Put `ANTHROPIC_API_KEY`,
`GRANOLA_API_KEY` and `SLACK_BOT_TOKEN` there, one secret each. Channel IDs
go under Settings → Secrets and variables → Actions → **Variables**; they
are not secrets.

Why an environment and not the plain repository secrets one click away: a
repository secret is readable by any workflow on any branch, so anyone who
can push a branch could edit a workflow file on that branch to print it. An
environment restricted to `main` gives its secrets only to jobs running on
`main`, and only a merged proposal reaches `main`. The shipped workflows
declare `environment: automation` on exactly the jobs that need a key.
(On a private repository this restriction needs GitHub Team or Pro, the
same plan the rulesets need; on Free the environment exists but the
branch rule is not enforced.)

Rules for these keys:

- One secret per key, named exactly as in `.env.example`; never a value in
  a workflow file.
- The agent in Actions (`transcripts-process.yml`) gets `ANTHROPIC_API_KEY`
  and a short-lived GitHub token and nothing else: no shell, no network,
  no Slack token. The Slack pointer is posted by a plain step after the
  agent is done, from a fixed template.
- Scope down at the vendor: read-only, project-scoped, a spend cap on the
  Anthropic key.
- Cloud and Slack-started coding-agent sessions
  ([operating-model.md](operating-model.md), mode 3) take their keys from
  the session's own environment settings in claude.ai, configured by a
  person; never from the repo.

## What the agent can and cannot read

Agents never read `.env` and never echo key values into files, logs or
chat. Part of that is enforced by `.claude/settings.json`, which the lint
keeps intact (`docs/schema.json` lists the required rules), and it is
worth knowing exactly what it does:

- **Stops:** the Read tool on any `.env*` file (including `.env.example`,
  which is why the variable names are also listed in
  `integrations/README.md`), and the file commands Claude Code recognizes
  in Bash on those files (`cat`, `head`, `tail`, `sed`, `grep`, `less`,
  `more`); `env`, `printenv`, `export -p` and `set`, which would print the
  whole environment, keys included; one-liners (`python3 -c`, `node -e`)
  that could read a file or the environment by hand; and `gh pr merge`,
  `gh pr review`, `gh secret` and force-pushes, which are a person's
  actions. It also switches off the "skip permissions" mode, so an agent
  in this repo always asks before a command it has no rule for.
- **Does not stop:** a script the agent is allowed to run, which opens
  `.env` itself; that is why the scripts in this repo read only the
  variables they need and never print one. Nor does it stop a person from
  typing `cat .env` in their own terminal, which is fine: the key is
  theirs.
- **Cursor and Codex** read the same skills but not this settings file;
  their guardrail is the skills' own rules, so hand a Cursor user a
  per-person key, not a bot key.

The deny rules are a seatbelt for accidents and for an agent that has been
talked into something by a document it read (transcripts, scraped pages,
vendor output; AGENTS.md rule 11). They are not a sandbox: a person with a
key and a terminal can always print it, and that is their key to print.

## Sharing, rotation, leaving

- **Never share a key by pasting it.** The sharing mechanism for a bot key
  is the vault plus the `automation` environment; for a personal key it is
  "get invited and make your own".
- **Rotate** a bot key when its owner changes, when someone who had it
  leaves, when a vendor reports an incident, and on a calendar (twice a
  year is plenty). Rotating means: new key at the vendor, update the vault
  item, update the environment secret, revoke the old key. Nothing in the
  repo changes.
- **When someone leaves:** remove them from the GitHub repository, the
  vendor workspaces and the vault; revoke their personal keys where the
  vendor allows (Calven, Apify); rotate any bot key they held. Write the
  date in `memory/decision-log.md`.

## If a key leaks

1. Rotate it at the vendor now, before anything else.
2. If it was in a commit, tell whoever administers the repository; they
   decide whether to rewrite history (usually not worth it) and they check
   the vendor's usage log for the window it was exposed.
3. Log it in `memory/decision-log.md` with the date, the key, and what
   changed so it does not happen again.
