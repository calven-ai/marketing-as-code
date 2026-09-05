<!-- source: https://raw.githubusercontent.com/NEON-Rutger/B2B-revops-skills/main/data-enrichment/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Enrichment: fields, waterfall, freshness, snapshot columns

Condensed from the source above and mapped to this repo's snapshot layout.

## Fields, by priority

| Priority | Company fields | Person fields (private repo only) |
| --- | --- | --- |
| 1 | headcount, industry, revenue band, HQ country, website | job title |
| 2 | description, technologies, funding stage and last round | seniority, department |
| 3 | social profiles | profile URL |

Enrich priority 1 for every candidate; priority 2 only for the survivors of
the ICP pass; person fields only through the `researcher` skill.

## Snapshot columns

`data/accounts/snapshots/YYYY-MM-DD-<vendor>-firmographics.csv`:

```csv
domain,company,industry,headcount,revenue_band,country,tech_stack,funding_stage,source,pulled_at
```

`source` is the vendor's id; `tech_stack` is a semicolon-separated list;
an unknown value is an empty cell, never a guess.

## Waterfall

No single provider covers everything: single-provider match rates run
35 to 52 percent, a waterfall of two or more providers 78 to 95 percent.
Order: the primary vendor, then a fallback for the gaps, then a specialist
layer for technographics. Track the match rate per step and stop when the
remaining gaps are not worth the credits.

## Freshness

| Record | Re-enrich |
| --- | --- |
| target account (ABM) | monthly |
| active lead | every 90 days |
| customer account | every 180 days |
| dormant account | yearly |

Data decays about 2 percent a month, 22 to 30 percent a year. A
firmographics snapshot older than a quarter is a reason to pull again.

## Cost rules

- Enrich only records that passed a quality gate (valid domain, not a
  competitor, not already a customer).
- Batch in groups of 50 to 100; batches are cheaper than one-off calls.
- Cache: do not re-enrich a domain that is in a snapshot from this month.
- Report credits used; alert the team at 80 percent of the monthly budget.

## Quality checks before proposing rows

Match rate per provider (below 60 percent is a problem), priority-1 field
coverage (aim above 80 percent), plausibility (does headcount match the
industry and the funding stage?), and a pilot of 100 to 500 records before
committing a budget to a new provider.

## Compliance

Keep a legitimate-interest note and a signed processing agreement with
each provider on file; record the provider and the date per row (`source`,
`pulled_at`) so a deletion request can be honoured.
