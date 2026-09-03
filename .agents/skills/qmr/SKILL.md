---
name: qmr
description: Assemble the Quarterly Marketing Review. Use when asked to prepare, start, or update the QMR, quarterly review, or quarterly report. Drives the data checklist, gathers snapshots (via integrations or human exports), computes deltas vs last quarter, and fills the report and dashboard.
---

# QMR: the quarterly marketing review

You assemble the quarter's evidence and narrative skeleton; the team brings
the judgment. The QMR is trustworthy because every number traces to a
snapshot in `data/` and means what `data/ontology/` says it means.

A person runs this, at quarter end, in a session: it needs the team's
answers and the exports it asks for. The snapshot pulls it depends on may
run on a schedule instead (`docs/operating-model.md`).

## Procedure

1. **Open the quarter's folder.** `reports/qmr/<year>-q<n>/` (ask which
   quarter if ambiguous). Copy in the pack from `reports/_templates/qmr/`:
   `report.md` and `data-checklist.md`. If the folder exists, resume; the
   checklist tracks what's still missing.

2. **Work the data checklist.** `data-checklist.md` lists every snapshot the
   QMR needs, its expected path, and how to get it. For each item:
   - Already in `data/*/snapshots/` and covering the quarter → check it off
     with the path.
   - Integration connected (`integrations/README.md`) → pull it, save it
     under the expected snapshot name, check it off.
   - No integration → give the human the exact export instruction from the
     checklist ("In HubSpot: … export as CSV, drop it at
     `data/crm/snapshots/<name>.csv`") and leave the item open. **Batch all
     the export asks into one list**; nobody wants seven interruptions.

3. **Compute.** With the snapshots in hand: quarter's headline metrics vs
   targets, funnel conversion by stage, deltas vs the previous quarter's QMR
   (read `reports/qmr/<prev>/report.md`; its Data-used section names the
   comparable snapshots). All terms per `data/ontology/metrics.md` and
   `funnel.md`. Content shipped: grep `content/` frontmatter for
   `status: published` with a `published:` date inside the quarter. Projects: read `projects/*/status.md` and
   `_archive/` for what closed.

4. **Fill `report.md`.** Numbers and evidence fully; narrative sections
   (wins, misses, lessons) as *drafted claims the data supports*, each
   flagged for the team to confirm or rewrite. Decisions-needed section:
   collect open questions from project statuses and anything the quarter's
   data obviously raises.

5. **Dashboard.** Build `dashboard.html` next to the report via the
   `make-dashboard` skill: headline metrics with vs-target and vs-last-Q
   deltas, the funnel, trend lines where ≥2 quarters of snapshots exist.

6. **Report status.** End with: checklist items still open (and who owes
   which export), numbers that couldn't be computed and why, and the flagged
   narrative claims awaiting confirmation.

## Rules

- **A gap is a gap.** An uncomputable metric appears in the report as
  "missing: needs <snapshot>", never an estimate silently presented as
  fact.
- First QMR ever? No previous quarter to diff. Say so, and establish this
  one as the baseline.
- If `data/ontology/metrics.md` is unfilled for a headline metric, that's a
  blocking question for the team, not a definition you pick.
