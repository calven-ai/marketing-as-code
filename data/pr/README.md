# data/pr/

Media lists and coverage. Fed by the `pr-media` integration category (the
media database) and `scraping-search` (coverage found on the open web). See
`integrations/README.md`.

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable, named per
`data/README.md`. Typical:

- `2026-08-31-apify-coverage.csv`: articles that mention the brand, with
  outlet, author, date and link
- `2026-08-31-repo-media-list.csv`: the outlets and journalists the team
  pitches, computed in-repo (`repo` is the source token for that)

The `media-outreach` and `coverage-tracker` skills write here.

## Rules

- Media lists hold journalists' names and contact details: private repo
  only, per the PII rule from `data/`. Coverage rows keyed by outlet and
  URL are safe anywhere.
- Load `data/ontology/` first. Coverage is a source in
  `data/ontology/naming.md`, so referral traffic from it can be tied back.
- Outreach is a human act. No agent emails anyone on a list here.
