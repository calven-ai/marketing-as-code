# Naming conventions

> **Template: unfilled.** Type over the brackets, or say `/setup` and answer a
> few questions. These conventions make campaigns traceable across systems;
> agents apply them exactly and flag violations they encounter.

## UTM parameters

| Parameter | Convention | Example |
| --- | --- | --- |
| `utm_source` | [allowed values] | |
| `utm_medium` | [allowed values] | |
| `utm_campaign` | [pattern, e.g. `<year>-<campaign-slug>`] | |
| `utm_content` | [when used, pattern] | |

## Campaign names across systems

[The one slug per campaign, and how it appears in the task tool, the CRM,
ad platforms, and `projects/<slug>/`: same slug everywhere.]

## File naming in this repo

- Snapshots: `YYYY-MM-DD-<source>-<what>.csv` (defined in
  `data/README.md`)
- Content folders: `YYYY-MM-<slug>/`
- Ad-hoc reports: `reports/adhoc/YYYY-MM-DD-<question-slug>/`
