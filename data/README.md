# data/

**Kind:** data, the numbers as tables, dated snapshots, and the reports built from them.

Machine-first working data: the CSV tables agents query, diff and append.
Human-readable analyses of this data go to [`reports/`](../reports/), never
here.

## Layout

| Folder | Domain |
| --- | --- |
| [ontology/](ontology/) | **Load this before touching anything else in `data/`.** Metric definitions, funnel stages, event taxonomy, naming conventions |
| [seo/](seo/) | Canonical keyword table and ranking snapshots |
| [analytics/](analytics/) | Website and product analytics snapshots (GA4, PostHog) |
| [crm/](crm/) | Pipeline, signups, email performance snapshots (CRM exports) |
| [accounts/](accounts/) | Target-account lists, ABM research, enrichment outputs |

## Conventions (load-bearing)

- **Canonical tables live at the domain root** (e.g. `seo/keywords.csv`).
  They are the single source of truth, updated in place.
- **Snapshots are immutable, dated pulls** in each domain's `snapshots/`
  folder, named `YYYY-MM-DD-<source>-<what>.csv`
  (e.g. `2026-08-31-hubspot-pipeline.csv`). Never edit a snapshot. Pull a
  new one. The date prefix sorts, so the last file is always the freshest.
- **CSV preferred**, with a header row. Keep columns stable within a domain
  so snapshots stay diffable.
- **No customer PII in a public copy, ever.** Company-level data is fine.
  Personal emails and names of individuals are not, unless this repo is
  private and the team has decided so (log the decision).

## For agents

Answering a data question? Follow "Answering questions from data" in
[AGENTS.md](../AGENTS.md). Check for an existing snapshot. Pull through
[`integrations/`](../integrations/) if it is stale. Interpret through
[`ontology/`](ontology/). Answer, and save the new pull as a snapshot.
