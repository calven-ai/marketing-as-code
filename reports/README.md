# reports/

Human-first outputs: analyses, recurring reports, the QMR, and dashboards.
Dated, and immutable once delivered — a new analysis is a new file, never an
edit to an old one. (The machine-readable inputs live in
[`data/`](../data/).)

## Layout

| Folder | What lands there |
| --- | --- |
| [_templates/](_templates/) | Scaffolds: `report.md`, `dashboard.html`, and the QMR pack |
| `qmr/<year>-q<n>/` | The quarterly marketing review: report + dashboard + its data checklist |
| `recurring/seo/` | Weekly/monthly keyword & ranking deltas |
| `recurring/analytics/` | Web/product analytics reports |
| `recurring/mentions/` | Brand & LLM-mention tracking (wave 3) |
| `adhoc/YYYY-MM-DD-<question>/` | One-off analyses, named after the question they answer |

## Conventions (load-bearing)

- Every report starts from [`_templates/report.md`](_templates/report.md):
  answer first, evidence second, and a **Data used** section listing the
  exact `data/` snapshot paths behind every number — a report must be
  auditable back to its inputs.
- Recurring reports are named by date: `recurring/seo/2026-09-01.md`.
- **Dashboards are single self-contained HTML files** built from
  [`_templates/dashboard.html`](_templates/dashboard.html), saved beside the
  report they support. No build step, no CDN, no external anything — they
  open in any browser, from Finder, GitHub Desktop, or a download.
- Numbers in a report mean what `data/ontology/` says they mean. A gap in
  the data is reported as a gap, never an invented number.
