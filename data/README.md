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
| [crm/](crm/) | Pipeline, signups, contacts and companies (CRM exports) |
| [accounts/](accounts/) | Target-account lists, ABM research, enrichment outputs |
| [ads/](ads/) | Paid campaign snapshots and the finance export for budget pacing |
| [email/](email/) | Email and marketing-automation performance snapshots |
| [social/](social/) | Organic social stats, listening pulls, community threads |
| [events/](events/) | Webinar and event attendee lists, follow-up specs |
| [pr/](pr/) | Media lists and coverage |
| [reviews/](reviews/) | Review-site, NPS and survey exports |

## Conventions (load-bearing)

- **Canonical tables live at the domain root** (e.g. `seo/keywords.csv`).
  They are the single source of truth, updated in place.
- **Snapshots are immutable, dated pulls** in each domain's `snapshots/`
  folder, named `YYYY-MM-DD-<source>-<what>.csv`
  (e.g. `2026-08-31-hubspot-pipeline.csv`). `<source>` is the wired
  vendor's token, one lowercase run (`googleads`, `hubspot`); `repo` means
  computed in-repo, `finance` a finance export. Never edit a snapshot. Pull
  a new one. The date prefix sorts, so the last file is always the
  freshest.
- **CSV preferred**, with a header row. Keep columns stable within a domain
  so snapshots stay diffable.
- **Personal data is a decision, not a default.** The repository is private
  by rule (AGENTS.md, rule 8). Company-level data is always fine. Personal
  emails and names of individuals come in only once the team has decided so
  and logged the decision; a copy that turns out to be public holds none.

## For agents

Answering a data question? Follow "Answering questions from data" in
[AGENTS.md](../AGENTS.md). Check for an existing snapshot. Pull through
[`integrations/`](../integrations/) if it is stale. Interpret through
[`ontology/`](ontology/). Answer, and save the new pull as a snapshot.
