---
name: make-dashboard
description: Turn data into a self-contained HTML dashboard beside its report, or a spec for the team's BI tool. Use when asked for a dashboard, chart or visual view, or when a report's answer is too multidimensional for prose.
license: MIT
metadata:
  kind: workflow
  area: core
  needs: []
  optional: [warehouse-bi]
  writes: repo
  runs: person
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
   with twenty charts answers nothing. Then remove `data-example="replace"`
   from the `<html>` tag and the example line from the footer: the check
   refuses a dashboard that still carries the template's numbers.
4. **List sources**: the footer's data-sources line gets the exact snapshot
   paths used, same as a report's "Data used" section.

## BI mode

With a `warehouse-bi` integration wired (the Wired table in
`integrations/README.md`), also write a spec the team can build in its BI
tool: one section per dashboard in `memory/knowledge/dashboards.md`, created the first time and updated in place later.
Each section lists the metrics by their `data/ontology/metrics.md` names,
the filters (period, segment, channel), and for every metric the snapshot
and column it comes from today, so the warehouse model maps to the same
definitions. Never build in the BI tool itself: the spec is the proposal,
and a person builds it or approves it.

## Rules

- One file, no external requests: check you added no `<script src>`,
  `<link>`, or web-font references.
- Charts label their units and time ranges; deltas say what they're deltas
  against.
