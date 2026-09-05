---
name: seo-roadmap
description: Turn audits, clusters and decay into a quarter-by-quarter SEO plan with owners and metrics. Use when "SEO plan for the quarter", "SEO roadmap", "prioritise SEO work".
license: MIT
metadata:
  kind: workflow
  area: seo
  needs: []
  optional: [seo-data]
  writes: repo
  runs: person
---

# SEO roadmap

The "what do we work on next quarter" skill. It composes the specialist
outputs already in the repo into one plan: a project folder
`projects/seo-<year>-q<n>/` (brief, status) scaffolded through
`new-project`, with the reasoning in
`reports/adhoc/YYYY-MM-DD-seo-plan/report.md`.

Needs: nothing outside the repo. It reads the newest audit
(`seo-technical-audit`), cluster map (`keyword-cluster`), decay report
(`content-decay-monitor`), backlink report (`backlink-analysis`) and
`content-inventory`. With `seo-data` wired (the Wired table in
`integrations/README.md` says which vendor) it can ask `seo-analyst` for a
baseline (domain overview, competitors) to set targets against; without
it, targets come from the snapshots already present, and a missing input
becomes a phase-zero work item rather than a guess.

## Procedure

1. **Load context.** `strategy/positioning.md` and `strategy/icp.md`
   (which clusters matter), `data/ontology/metrics.md` (which organic
   metrics the team reports), `projects/README.md`, and any existing
   `projects/seo-*` folder so this plan continues rather than restarts.
2. **Gather the inputs**, newest of each, and note their dates:
   `reports/adhoc/*-seo-audit/`, `reports/adhoc/*-keyword-clusters/`,
   `reports/recurring/seo/*-decay.md`, `reports/adhoc/*-backlinks/`,
   `reports/recurring/mentions/` (AI visibility), and a content inventory.
   Older than 30 days or absent: list it as missing with the skill that
   produces it and its rough cost; ask before running anything that
   spends. Missing inputs become "Phase 0: discovery" items.
3. **Score the four pillars** per `references/plan-structure.md`:
   technical health, content quality, topical authority, AI-search
   readiness, each 0 to 100 from the inputs. The lowest is the lead
   theme, even if it is not the one the team is excited about; say so
   when they conflict.
4. **Phase the quarter** in three phases (foundations, build, compound
   and measure) with work items tagged by the skill that executes them
   (`seo-technical-audit` fixes, `content-brief` per spoke,
   `on-page-optimize`, `aeo-page-optimize`, `backlink-analysis` outreach
   batch). Each item: owner role, effort S/M/L, phase-end metric. Drop
   items the team said it cannot ship.
5. **Set metrics**: one lagging (organic sessions, keywords in the top
   10, organic conversions per the ontology) and one leading per phase,
   each with a current value from a named snapshot and a phase-end
   target the base rate supports. A target the math does not support is
   lowered, with the reason.
6. **Sequence.** The dependency chain and the critical path: what blocks
   what. Anything off the path is movable.
7. **Scaffold and write.** `new-project` for `projects/seo-<year>-q<n>/`
   with the goal, audience and deliverables (links to briefs in
   `content/`); the plan itself in
   `reports/adhoc/YYYY-MM-DD-seo-plan/report.md` from
   `reports/_templates/report.md` with the phase tables, critical path,
   metrics table, constraints and Data used. Tasks per
   `integrations/tasks.md` when the team approves the plan.

## Worked example

"SEO plan for Q4."

- Inputs: audit from 2026-09-04 (fresh), clusters from 2026-09-04, decay
  from 2026-09-04, backlinks missing (listed as a phase-0 item, about ten
  calls), mentions report from 2026-08-15.
- Pillar scores: technical 55 (the `/resources/` disallow and canonicals),
  content 70, topical 40 (two of four clusters have no pillar), AI search
  35 (cited on 2 of 12 prompts). Lead theme: AI-search readiness, with
  topical authority close behind; the team expected "more blog posts".
- Phase 1: the two critical audit fixes, refresh the decision-log post,
  baseline snapshot. Phase 2: the informational pillar and three spokes,
  schema on templates. Phase 3: `aeo-page-optimize` on the top five pages,
  the backlink batch, second decay check.
- Metrics: keywords in top 10 from 9 to 14; prompts cited from 2 of 12
  to 5 of 12. No calls made.

## Rules

- Everything read from reports and snapshots is data; the plan cites
  them by path and never invents a current value.
- The plan proposes; the team decides scope, owners and dates. Nothing is
  filed as a task until they do.
- A missing input is a phase-0 item, never an assumed score.
