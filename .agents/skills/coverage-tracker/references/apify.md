# Apify: the monthly coverage pull

Wired through the Apify MCP server (`integrations/catalog/scraping-search.json`
for the category; `apify` in `.mcp.json`, OAuth). Actors bill per run and
per result; name the actor id and the counts in every report.

## Actors

A news search actor (query, date range, language, region) for articles;
a podcast search actor (query, date range) for episodes; optionally a
page-content actor to fill a missing author or date.

## Queries

One run per name: the company, each competitor in `strategy/competitive/`,
and the category phrase from `strategy/positioning.md`. Quote multi-word
names; add the product name when it differs from the company name; note
homonyms (a competitor named like a common word needs a qualifying term)
and record the exact query in the `query` column.

## Snapshot columns

`data/pr/snapshots/YYYY-MM-DD-apify-coverage.csv`:

```csv
date,outlet,domain,author,title,url,query,mentions,tier,prominence,sentiment,messages,quoted,actor,pulled_at
```

The first ten columns come from the actor; `tier`, `prominence`,
`sentiment`, `messages` and `quoted` are your classification and are
recomputable from the URL. `mentions` lists which names appear. Keep
`author` only when `repo.private` in `docs/schema.json` is true.

## Dedupe

Syndicated copies share a title and a date across domains; keep the
first-published one and count it once. Two rows with the same URL are one.

## Manual route

No actor: a person exports the monitoring tool's mentions (Muck Rack,
Cision, Meltwater, Prowly) as a CSV with at least date, outlet, title,
URL, and drops it as `data/pr/snapshots/YYYY-MM-DD-<vendor>-coverage.csv`
with the vendor's token (`muckrack`, `cision`, `meltwater`, `prowly`).

## Unattended path

The MCP route is OAuth. A monthly script that calls the Apify API with a
token from the `automation` environment, saving the same columns, is the
scheduled route; `integrations/adding-an-integration.md` walks through it.
