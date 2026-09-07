# Secrets: who holds which key, and where it lives

Every integration needs one of three things: nothing (OAuth, you sign in
with your browser), a key that belongs to you, or a key that belongs to a
bot. Your keys live on your machine. Bot keys live in GitHub. Nothing else
holds a key, and agents never read one.

## Who holds which key

| Credential | Kind | Who owns it | Where it lives | Rotate it at | When someone leaves |
| --- | --- | --- | --- | --- | --- |
| Apify | per person, OAuth | each person | nowhere; the browser grant on first use | Apify: revoke the grant | remove them from the Apify organization |
| `CALVEN_MCP_KEY` | per person | each person | their own `.env` (or the desktop app's Local environment), their own 1Password item | Calven: Settings → Integrations → MCP | revoke their key in Calven |
| `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | per person where DataForSEO gives teammates their own login; otherwise the owner's, treated as a bot key | the integrations owner | each person's `.env`; the owner's copy in the shared vault; an environment secret in `automation` once the monthly brand-monitor run (`role-brand-monitor.yml`) is turned on | DataForSEO dashboard | rotate if it was ever shared with them |
| `GRANOLA_API_KEY` | bot (the daily pull) | the integrations owner | the GitHub environment `automation`; the owner's vault item | Granola: Settings → Connectors → API keys | rotate if they were the owner |
| `SLACK_BOT_TOKEN` | bot (the team's Slack app) | the Slack workspace admin | the GitHub environment `automation`; the shared vault, visible to the owner only | Slack app page: Reinstall to Workspace | rotate if they had it |
| `ANTHROPIC_API_KEY` | bot (the optional agent in Actions) | the integrations owner | the GitHub environment `automation`, nowhere else; people use their own coding-agent subscription locally, never this key | Anthropic Console; set a spend cap | rotate |
| `SLACK_*_CHANNEL_ID` | not a secret | anyone | repository Actions variables; `.env` | n/a | n/a |
| `GITHUB_TOKEN` | automatic, per workflow job | GitHub | nowhere; it exists for the length of a job with only the permissions the job declares | automatic | n/a |

Add a row for every integration you wire: `python3 scripts/wire_integration.py
<vendor>` prints the row to paste, the
[integration guide](../integrations/adding-an-integration.md) asks for it,
and the check warns when a variable in `.mcp.json` has no row here.

Two facts shape the table:

- **A key in GitHub only serves unattended runs.** An admin can write it.
  Nobody can read it back: not a person, not a laptop script, not a coding
  agent. Only a workflow on GitHub's machines sees it. So a person working
  locally needs their own key.
- **A key that lands in a commit is burned.** Rotate it at the vendor the
  moment you notice. Removing the commit is not enough, because every clone
  has a copy. The lint refuses to commit anything shaped like a key, and the
  pre-push hook refuses to push it.

**One integrations owner.** Name one person in `.github/CODEOWNERS` and in
`memory/decision-log.md`. They create the bot identities, put each bot key
in the shared vault and in the `automation` environment, and rotate them.
Everyone else never sees a bot key.

## Your keys, on your machine

1. Get invited to the vendor's workspace (Calven, DataForSEO, Apify) and
   generate your own key there. Never borrow a teammate's.
2. Copy `.env.example` to `.env` at the repo root and fill in only the keys
   for tools you use. `.env` is gitignored, and the lint fails if one is
   ever tracked. Keep a copy of each key in your own 1Password item.
3. Start your coding agent with the keys in its environment. The MCP servers
   in `.mcp.json` read placeholders like `${CALVEN_MCP_KEY}` from the
   environment, not from `.env`, so `.env` alone does nothing for them.
   - **1Password CLI users, the recommended way:** put references in
     `.env` instead of values, like
     `CALVEN_MCP_KEY=op://Private/Calven MCP/credential`. The launcher
     below sees `op://` and runs the command through `op run`, which
     resolves the references at start and masks the values wherever they
     would be printed. A key whose value the agent never sees is the only
     kind it cannot be talked into printing.
   - **Terminal:** `sh scripts/with_env.sh claude` (or `cursor .`, or any
     command). The launcher exports only the variables the MCP servers in
     `.mcp.json` reference, starts the command, and prints nothing. Those
     variables are then in the agent's environment and in every MCP
     server's process. A person approves each command the agent runs, and
     that prompt is the guard: nothing stops an `echo` once it is
     approved. Keep that in mind when a command you did not expect asks
     to run.
   - **Claude desktop app:** it does not read your shell. Add the same
     variables in its Local environment editor. They are stored encrypted
     on your machine and apply to every local session.
4. Scripts (`scripts/*.py`) read `.env` themselves, so they work either way.

Never paste a key into a chat with an agent, into Slack, or into email. If
an agent asks for a key, tell it where the key lives. The skills are
written to do exactly that.

## The bot keys, only in GitHub

The daily transcript pull, the Slack alert when `main` is red, and the
optional agent in Actions run with nobody watching. Their keys belong to
nobody and live in one place:

**Settings → Environments → `automation` → Environment secrets.**
`sh scripts/github_setup.sh` creates the environment and restricts it to
`main`; the click path is in [github-settings.md](github-settings.md). Put
`ANTHROPIC_API_KEY`, `GRANOLA_API_KEY` and `SLACK_BOT_TOKEN` there, one
secret each, plus `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` when the
monthly brand-monitor run is on. Channel IDs are not secrets. They go under Settings → Secrets
and variables → Actions → **Variables**.

Why an environment and not a plain repository secret: a repository secret is
readable by any workflow on any branch, so anyone who can push a branch can
print it. An environment restricted to `main` gives its secrets only to
merged proposals. Which GitHub plan enforces that restriction is in
[github-settings.md](github-settings.md).

Rules for these keys:

- One secret per key, named exactly as in `.env.example`. Never a value in a
  workflow file.
- The agent in Actions (`transcripts-process.yml`) gets `ANTHROPIC_API_KEY`
  and a short-lived GitHub token, nothing else. No shell, no network, no
  Slack token. The Slack pointer is posted by a plain step afterwards, from
  a fixed template.
- Scope down at the vendor: read-only, project-scoped, a spend cap on the
  Anthropic key.
- Cloud and Slack-started coding-agent sessions take their keys from the
  session's own environment settings in claude.ai, configured by a person.
  Never from the repo ([operating-model.md](operating-model.md), mode 3).

## What stops an agent reading a key

Agents never read `.env` and never echo a key into files, logs or chat.
That is a rule in [AGENTS.md](../AGENTS.md) (rule 7) and in every skill that
touches a key; the skills are written to say where a key lives instead of
asking for its value. What enforces it is the permission prompt: a coding
agent asks before it runs a command you have not allowed, and you read that
prompt. Nothing here takes that decision away from you.

**This repository ships no permission rules.** `.claude/settings.json` is
checked in because it carries the repo's own machinery and nothing else: the
allow-list for the lifecycle scripts (`sync.py`, `propose.py`, `doctor.py`,
`lint.py`, `sync_skills.py`, `wire_integration.py`), the `SessionStart` hook
that runs the doctor, and the write-tool deny rules that
`python3 scripts/wire_integration.py <vendor>` adds for an MCP server this
repository declares. It says nothing about what you personally may run.

**Your rules are yours.** If you want an agent stopped rather than asked,
put the rules in your own settings, where they apply to you, cover every
repository you open, and never reach a teammate:

- `~/.claude/settings.json` — every project on your machine.
- `.claude/settings.local.json` — this clone only; it is gitignored.

A set worth copying, which stops the Read tool on any `.env*` file at any
depth (`cat`, `head`, `tail`, `sed` and `<` redirections go through the same
rule) and the usual ways of printing an environment:

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)", "Read(./.env.*)", "Read(**/.env)", "Read(**/.env.*)",
      "Bash(env)", "Bash(env *)", "Bash(printenv*)", "Bash(export -p*)"
    ]
  }
}
```

Know what rules like these do not do, however you write them. They do not
stop a script the agent may run that opens `.env` itself; that is why the
scripts here read only the variables they need and never print one. Nor
`awk`, `xargs`, `cp`, `base64` or a Python file the agent just wrote, since
the Read rules recognise a fixed set of file commands. Those still prompt,
so a person reads the command first. They are a seatbelt for accidents and
for an agent talked into something by a document it read (AGENTS.md rule
12), not a sandbox: `op run` (above) is what keeps a value out of the
agent's reach altogether. The pre-push hook is the same kind of seatbelt;
`git push --no-verify` skips it.

The lifecycle scripts (`scripts/sync.py`, `scripts/propose.py`,
`scripts/doctor.py`) are the one thing this repository does allow to run
without a prompt. By design they never push to `main`, force-push or merge,
and `scripts/test_lifecycle.py` proves it.

**Cursor and Codex** read the same skills but not this settings file. Their
guardrail is the skills' own rules, so hand a Cursor user a per-person key,
not a bot key.

## Sharing, rotation, leaving

- **Share** a bot key through the vault and the `automation` environment.
  Share a personal key by getting the person invited to make their own.
- **Rotate** a bot key when its owner changes, when someone who had it
  leaves, when a vendor reports an incident, and twice a year. New key at
  the vendor, update the vault item, update the environment secret, revoke
  the old key. Nothing in the repo changes.
- **When someone leaves,** remove them from the repository, the vendor
  workspaces and the vault. Revoke their personal keys where the vendor
  allows. Rotate any bot key they held. Date it in `memory/decision-log.md`.

## If a key leaks

1. Rotate it at the vendor now.
2. If it was in a commit, tell whoever administers the repository. They
   decide whether to rewrite history and check the vendor's usage log for
   the exposed window.
3. Log it in `memory/decision-log.md`: the date, the key, and what changed
   so it does not happen again.
