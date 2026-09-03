---
name: add-integration
description: Connect a tool the team uses to this repo. Use when asked "we use X, connect it", "automate pulling Y", "can the agent read Z", or when a skill needs a tool that is not wired. Walks the MCP, CLI, script ladder in integrations/adding-an-integration.md and delivers the integration as one reviewable PR.
---

# Add an integration

You connect a tool by the rules in
`integrations/adding-an-integration.md`. Read that file first, every time;
this skill is the procedure, that file is the reasoning and the contract.

## Procedure

1. **Name the jobs, not the tool.** Ask, in one round: which tool, and what
   the team wants to do with it. Read only? Write (create tasks, update
   records)? Ad hoc in a session, or on a schedule with nobody watching? A
   sentence like "we use Zoom, automate the transcripts" usually hides two
   jobs on two tiers; split them and say so.
2. **Check what is already there.** The registry (`integrations/README.md`):
   is the tool wired, or listed as a known route? A skill that would use it
   (`agents/README.md`): what does its "Needs:" line say today?
3. **Pick the tier per job, with the human.** Official MCP first, vendor
   CLI second, custom script last; move down only for a reason the guide
   lists (no server, missing write, unattended run, bulk pull). Check the
   vendor's current documentation for the server endpoint or the CLI and
   its tool list on the day; the guide's table is a starting point, not
   the truth. State the tier and the reason in one sentence and get a yes
   before building.
4. **Build the deliverables** on a branch:
   - Tier 1: the `.mcp.json` entry (env placeholders only, never a value),
     the `.cursor/mcp.json` entry in Cursor's syntax, the Codex TOML
     snippet for the PR description.
   - Tier 2: the command a skill will run, and a script only if the output
     needs reshaping into a snapshot.
   - Tier 3: a script that copies the closest shipped one and follows the
     contract (stdlib, keys via `scripts/_common.py`, `--dry-run`,
     idempotent, readable errors, output where the data lives). For a
     scheduled run, the workflow step, gated on its secret, opening a PR
     and never merging.
   - Always: the registry row, the `.env.example` lines and the matching
     Env vars column, the `scripts/README.md` row, the "Needs:" lines in
     affected skills, both run modes where the workflow is described, a
     `CHANGELOG.md` line, a decision-log entry via `log-decision`.
5. **Verify.** `python3 scripts/doctor.py` passes; the script's `--dry-run`
   runs with a dummy key and exits with its readable message, not a
   traceback; JSON files parse.
6. **Hand over.** Open the PR with the checklist from the guide in its
   description. Tell the human, in a short list, what they must do that you
   cannot: the OAuth grant on first use, the key to put in `.env`, the
   repository secret to add, the scope to grant in the vendor's settings.

## Rules

- Never put a key value in a committed file, never read `.env`, never test
  against production data the team did not offer.
- Never wire a tool nobody asked for, and never build a script where an MCP
  server or CLI would do.
- A community MCP server is somebody's script: say who maintains it and
  what it reaches before proposing it.
- If the vendor's documentation contradicts the guide's table, the vendor is
  right; fix the table in the same PR.
