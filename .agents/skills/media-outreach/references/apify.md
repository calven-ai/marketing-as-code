# Apify: finding who covers the category

Wired through the Apify MCP server (`integrations/catalog/scraping-search.json`
for the category; `apify` in `.mcp.json`, OAuth). Actors run on Apify's
platform and bill per run and per result. Check the server's actor search
in the session; name the actor id you picked and why.

## Actors to look for

- A news search actor (Google News or a news API style) taking query
  terms, a date range and a language: the category phrase from
  `strategy/positioning.md`, each competitor's name from
  `strategy/competitive/`, and the company name.
- A podcast search actor for episodes mentioning the category.
- A page-content actor to read an article's byline and date when the
  search result lacks them.

## Snapshot

`data/pr/snapshots/YYYY-MM-DD-apify-coverage.csv`:

```csv
date,outlet,domain,author,title,url,query,mentions,actor,pulled_at
```

`mentions` is a semicolon list of the brand and competitor names found in
the title or lead; `actor` the Apify actor id. Outlet and URL rows are
safe anywhere; `author` is a journalist's name and is kept only when
`repo.private` in `docs/schema.json` is true.

## Cost discipline

Run one query with a 90-day window first, report the result count and
the cost, then widen to 12 months and the competitor names on approval.
A launch-sized pull is a few hundred results; state the number.

## Deriving the media list

Group the coverage rows by author and outlet; three or more relevant
pieces in a year marks a beat. The `media-list` snapshot is computed
from this in-repo, so its vendor token is `repo`.
