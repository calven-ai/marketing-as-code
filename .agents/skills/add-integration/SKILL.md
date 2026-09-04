---
name: add-integration
description: Connect a tool the team uses to this repo. Use when asked "we use X, connect it", "automate pulling Y", "can the agent read Z", or when a skill needs a tool that is not wired. Walks the MCP, CLI, script ladder in integrations/adding-an-integration.md and delivers the integration as one reviewable PR.
license: MIT
metadata:
  kind: workflow
  area: core
  needs: []
  writes: repo
  runs: person
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
2. **Check the catalog first.** Name the category the job belongs to
   (`crm`, `web-analytics`, `ads`, and so on; the list is the category
   table in `integrations/README.md`). Then
   `python3 scripts/wire_integration.py --category <category>`: it shows
   what the catalog knows for that category, vendors, routes (MCP, CLI,
   script, manual export), auth, writes, and when each entry was last
   verified. The Wired table in `integrations/README.md` shows what is
   bound today; `agents/README.md` shows which skills need the category.
   If the vendor is in the catalog, the work is step 4a; if not, it is a
   catalog entry plus step 4a.
3. **Pick the tier per job, with the human.** Official MCP first, vendor
   CLI second, custom script last; move down only for a reason the guide
   lists (no server, missing write, unattended run, bulk pull). Check the
   vendor's current documentation for the server endpoint or the CLI and
   its tool list on the day; a catalog entry marked `listing` or
   `unverified` is a lead, not the truth. State the tier and the reason in
   one sentence and get a yes before building.
4. **Build the deliverables** on a branch:
   - 4a. Tier 1, vendor in the catalog:
     `python3 scripts/wire_integration.py <vendor>` (or
     `<vendor>:<variant>`; `--dry-run` first). It edits `.mcp.json`,
     `.cursor/mcp.json`, `.env.example`, `integrations/wired.json` and the
     write-tool deny rules in `.claude/settings.json`, and prints the Codex
     snippet and the `docs/secrets.md` row. Then
     `python3 scripts/lint.py --fix` regenerates the registry tables. Never
     edit those tables by hand.
   - 4b. Tier 1, vendor not in the catalog: add its entry to
     `integrations/catalog/<category>.json` in the shape of a neighbour
     (`verified: vendor` if you read the vendor's own page, `listing` if a
     directory; `checked` today; `source_url`; every `npx` or `uvx` package
     pinned), then wire it as in 4a.
   - Tier 2: the command a skill will run, and a script only if the output
     needs reshaping into a snapshot; record it as the vendor's `cli` or
     `script` route in the catalog entry.
   - Tier 3: a script that copies the closest shipped one and follows the
     contract (stdlib, keys via `scripts/_common.py`, `--dry-run`,
     idempotent, readable errors, output where the data lives). For a
     scheduled run, the workflow step, gated on its secret, opening a PR
     and never merging.
   - Always: `references/<vendor>.md` in every skill that lists the
     category as a need (`docs/skill-authoring.md` says what goes in it),
     the `scripts/README.md` row for a new script, both run modes where the
     workflow is described, a `CHANGELOG.md` line, a decision-log entry via
     `log-decision`.
5. **Verify.** `python3 scripts/doctor.py` passes; the script's `--dry-run`
   runs with a dummy key and exits with its readable message, not a
   traceback; JSON files parse.
6. **Hand over.** Open the PR with the checklist from the guide in its
   description. Tell the human, in a short list, what they must do that you
   cannot: the OAuth grant on first use, the key to put in `.env`, the
   repository secret to add, the scope to grant in the vendor's settings.
   Then say, in one paragraph, what they will be asked to review: a
   binding in `integrations/wired.json`, `.env.example` lines, and either
   an MCP entry or a script. They read the rendered Wired table and the
   description; the check reads the code.

## Rules

- Never put a key value in a committed file, never read `.env`, never test
  against production data the team did not offer.
- Never wire a tool nobody asked for, and never build a script where an MCP
  server or CLI would do.
- A community MCP server is somebody's script: say who maintains it and
  what it reaches before proposing it; in the catalog it is `listing` at
  best, never `vendor`.
- A server that can write is wired with its write tools denied; lifting
  that (`--allow-writes`) is the team's decision, logged, and even then a
  skill only stages drafts and asks before each write.
- If the vendor's documentation contradicts a catalog entry, the vendor is
  right; fix the entry and its `checked` date in the same PR.
