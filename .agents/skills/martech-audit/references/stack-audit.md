<!-- source: https://raw.githubusercontent.com/NEON-Rutger/B2B-revops-skills/main/revops-tech-stack/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Stack audit: fields, layers, verdicts

## Fields per tool

| Field | Where the evidence is |
| --- | --- |
| name, vendor, category id | `integrations/catalog/` |
| purpose (the capability it serves) | project briefs, the decision log, the team |
| owner | the team |
| annual cost (licence plus hidden: admin time, integration upkeep, overage) | the invoices snapshot; the team for the hidden part |
| seats paid, seats active last month | the tool's admin page, asked |
| renewal date and notice period | the contract, asked |
| integrations and sync health | `integrations/README.md`, the tool's admin |
| wired here | `integrations/wired.json`; possible routes from the catalog |

## Layers

- Core (every team): the CRM, marketing automation, the team's chat.
- Intelligence (by stage): analytics, conversation intelligence, intent,
  customer success, forecasting.
- Automation: iPaaS and generic connectors, documents and CPQ, data
  operations (warehouse, reverse ETL).

## Verdict matrix

| Fit for the capability | Value delivered | Verdict |
| --- | --- | --- |
| high | high | core: keep, drive adoption |
| high | low (under-used) | optimise: training, process, or wire it so the agents use it |
| needed | under-performing | question: reconfigure or evaluate an alternative before renewal |
| low | low | cut: remove at renewal, redirect the budget |

Rules of thumb: under 50% of paid seats active in a month is under-used;
if removing a tool breaks nothing, it is a cut candidate; two tools
serving one capability need a reason or a verdict; budget integration
upkeep as a share of the licence cost every year.

## Six-step audit

1. Inventory, with the fields above.
2. Usage: flag under 50% monthly active.
3. Capability map: overlaps and gaps against the categories the skills
   need.
4. Value: what changes if the tool goes away.
5. Integration health: syncs work, on time, one system of record per
   fact.
6. Roadmap fit: does the stack support next year's plan.

## Sizing by stage (orientation, not a target)

| Stage | Tools | Annual spend |
| --- | --- | --- |
| startup (under 5M ARR, under 10 in go-to-market) | 3 to 5 | 5k to 15k |
| scale-up (5M to 25M, 10 to 50) | 6 to 12 | 50k to 200k |
| growth (25M to 100M, 50 to 200) | 12 to 20 | 300k to 1M |

A startup running a growth-stage stack pays for tools nobody operates.

## Architecture rules the verdicts lean on

One tool per capability; the CRM is the hub and satellites sync to it;
process before platform; automate data capture, not decisions; prefer
composable tools with good APIs over suites; match complexity to stage.
