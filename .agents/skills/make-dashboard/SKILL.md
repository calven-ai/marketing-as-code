---
name: make-dashboard
description: Turn data into a self-contained HTML dashboard saved beside its report. Use when asked for a dashboard, chart, or visual view of marketing data, or when a report's answer is multidimensional enough that prose can't carry it.
metadata:
  kind: workflow
  needs: nothing
---

# Make a dashboard

Dashboards here are single HTML files: inline CSS, an inlined `DATA` object,
and the tiny chart helper already inside the template. They open in any
browser with no build step, CDN, or platform dependency. That's the
contract; never break it by adding external references.

## Procedure

1. **Get the numbers right first.** Source everything from `data/` snapshots
   (pull fresh ones per AGENTS.md "Answering questions from data" if
   needed), interpreted through `data/ontology/`. A dashboard is a report, so
   the same "never invent a number" rule applies.
2. **Copy `reports/_templates/dashboard.html`** to the folder of the report
   it supports (`reports/qmr/<q>/`, `reports/recurring/<domain>/`, or
   `reports/adhoc/YYYY-MM-DD-<question>/`). A dashboard never lives alone;
   if there's no report yet, create one from `reports/_templates/report.md`.
3. **Fill it in**: title, date, the `DATA` object, and the render calls;
   the template documents its own helpers (`bigNumber`, `barChart`,
   `lineChart`, `table`) with examples. Apply `brand/tokens.json` colors if
   filled. Keep it to the few views that answer the question; a dashboard
   with twenty charts answers nothing.
4. **List sources**: the footer's data-sources line gets the exact snapshot
   paths used, same as a report's "Data used" section.

## Rules

- One file, no external requests: check you added no `<script src>`,
  `<link>`, or web-font references.
- Charts label their units and time ranges; deltas say what they're deltas
  against.
