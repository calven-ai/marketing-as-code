# Marketing operations

You own the definitions and the plumbing, so every other team's numbers
are only as good as yours. In this repo the definitions are
`data/ontology/` (metrics, funnel, events, naming) and the evidence is the
snapshots under `data/`. These prompts test the definitions, read the
funnel through them and catch bad data before it reaches a report. CRM
edits and automation changes stay in their tools, behind your review.

| Use case | What it gets you | Skills it leans on |
| --- | --- | --- |
| [Funnel and lead definitions](funnel-and-lead-definitions.md) | MQL, scoring and handoff rules written down and tested against what converts | `/lead-lifecycle-spec`, `/tracking-spec` |
| [Pipeline reporting](pipeline-reporting.md) | The funnel read through the ontology, with the change that matters called out | `/pipeline-report`, `/web-analyst`, `/snapshot-pull` |
| [Attribution](attribution.md) | Which channels drive pipeline under each model, and which model to standardise on | `/attribution-analysis` |
| [A/B tests](ab-tests.md) | Tests designed with enough traffic to answer, and results read honestly | `/ab-test-plan` |
| [CRM data quality](crm-data-quality.md) | The gaps and errors that would break this month's reports, ranked by impact | `/data-hygiene-audit`, `/utm-builder` |
