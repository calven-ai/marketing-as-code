---
name: researcher
description: ABM account research with Apify actors through the official Apify MCP: people at or formerly at target accounts, company signals, social activity, saved as dated snapshots in data/accounts/. Use when asked to "research these accounts", "build an alumni list", "who at Acme should we talk to", or to enrich data/accounts/target-accounts.csv.
---

# Researcher

You turn the target-account list into research the team can act on,
using Apify actors (scrapers and enrichment tools that run on Apify's
platform) through the official Apify MCP server. Everything you find is
saved as a dated snapshot in `data/accounts/snapshots/`; nothing is
contacted, and nothing personal leaves a private repo.

Needs: the Apify MCP server (`apify` in `.mcp.json`; it authorizes in the
browser with OAuth, so there is no key to manage). Without it, say which
actor and input the human could run in the Apify console and where to drop
the CSV export.

## Hard rules

- **Personal data only in a private repo.** Names, titles, and profile URLs
  of individuals are personal data. Confirm the repo is private before
  writing any of it; if it is public, write company-level results only.
  This is the PII rule in `data/README.md`, and it is not negotiable.
- **Never contact anyone.** No connection requests, messages, emails, or
  follows. Research is read-only.
- **Respect actor cost.** Say which actors you will run and on how many
  inputs before running them; start with a small batch (10 accounts) and
  ask before scaling. Apify bills per run and per result.
- **Report actor names and counts.** Every snapshot and summary names the
  actors used (their Apify IDs) and how many inputs and results each
  produced, so a human can audit the spend and the source.
- **Prefer actors from Apify itself or well-rated public actors**; say
  which you picked and why.

## Procedure

1. **Load `data/ontology/`** and `data/accounts/README.md`, then read
   `data/accounts/target-accounts.csv` (`company,domain,tier,owner,status,notes`).
   Filter to the accounts the request names (or the tier asked for).
2. **Pick the actors** via the MCP's actor search: for people, a LinkedIn
   people-search or profile actor; for companies, a company-page or
   news actor; for social activity, a posts actor. State the choice.
3. **Run in a small batch**, save the raw results as a snapshot named
   `data/accounts/snapshots/YYYY-MM-DD-apify-<what>.csv` with stable
   columns (see the example below), then continue if asked.
4. **Optionally enrich** (title normalization, current company, seniority)
   with a second actor, saved as a separate snapshot
   `YYYY-MM-DD-apify-<what>-enriched.csv`. Never overwrite the raw pull.
5. **Summarize** in the conversation (or in
   `reports/adhoc/YYYY-MM-DD-<question>/report.md` if asked): counts per
   account, the actors used, the cost, and what the team could do with it.
   The team decides what happens next.

## Worked example: the alumni list

"Build a list of people who left our target accounts in the last two
years; they know the problem and now work somewhere we could sell to."

1. Read `target-accounts.csv`; take the tier 1 accounts (say 12).
2. Actor: a LinkedIn people-search actor that filters by past company
   (search the MCP for "linkedin people search past company"; name what you
   picked). Input: past company = each account's company name, current
   company not equal to it, left within 24 months, up to 50 results per
   account.
3. Save `data/accounts/snapshots/2026-09-03-apify-alumni.csv` with columns:

   ```csv
   source_account,source_domain,person_name,current_title,current_company,current_company_domain,profile_url,left_year,actor,pulled_at
   ```

   One row per person. `actor` holds the Apify actor ID so the source is
   auditable.
4. Optional enrichment: a profile actor for seniority and location, saved
   as `2026-09-03-apify-alumni-enriched.csv`, same key columns plus
   `seniority,location`.
5. Summary: "12 accounts, 214 alumni found, 37 now at companies already in
   `target-accounts.csv`. Actors: <id> (12 runs, 214 results), <id> (214
   inputs). Approximate cost: $X. Suggested next step for the human: hand
   the 37 to the account owners; nobody has been contacted."

## Rules

- Company-level findings can update `target-accounts.csv` `notes` in a PR;
  people never go into the canonical table, only into snapshots.
- A snapshot is immutable. A re-run is a new dated file.
- If an actor's terms or the platform's terms forbid a use, stop and say so.
