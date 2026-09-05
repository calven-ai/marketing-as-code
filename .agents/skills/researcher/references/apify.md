# Apify for the researcher

The `scraping-search` category wired to Apify: the official remote MCP
server at `https://mcp.apify.com` (`apify` in `.mcp.json`), authorized in
the browser with OAuth on first use, so there is no key to manage and no
unattended run. Actors are programs on Apify's platform; you find one,
call it with a JSON input, and read its dataset.

## The MCP tools

| Tool | Use |
| --- | --- |
| `search-actors` | full-text search of the Apify Store by what you need ("linkedin people search past company", "company news"); returns IDs, ratings, pricing model and run counts |
| `fetch-actor-details` | the actor's README and input schema before you call it: read both, and say what you picked and why |
| `call-actor` | runs the actor with your input and waits; the result is the run's default dataset |
| `get-actor-output` | reads a finished run's dataset when a call timed out or you are continuing a batch |
| `apify-slash-rag-web-browser` | the built-in web search and page reader for a quick look at a company site or a news item without picking an actor |

Tool names are the server's as configured; the connected server's tool
list is authoritative. The server can add other actors as tools on
request, but keep to the four above unless the task needs more.

## Actor families the procedure names

Pick by searching, not from memory: actors change owners and pricing. The
families, with what to look for:

- **People at or formerly at an account**: a LinkedIn people-search actor
  that filters by current or past company, or a profile scraper fed with
  profile URLs. Personal data: private repo only.
- **Company signals**: a company-page scraper (headcount, description,
  recent posts), a news or Google News scraper for the company name, and
  `apify/website-content-crawler` for the account's own site.
- **Social activity**: a posts scraper for the account's page or its
  people's public posts; the built-in `apify/rag-web-browser` for a
  one-off look.
- **Search**: `apify/google-search-scraper` when the question is "what is
  out there about Acme".

Prefer actors published by `apify` itself, then well-rated public actors
with recent runs; an actor with no runs in months or a warning in its
README is a reason to pick another. An actor whose terms, or the source
platform's terms, forbid the use is a stop, not a workaround.

## Cost and batch rules

Actors bill per result (pay-per-result), per event, or per compute unit
plus proxy traffic (rental); `fetch-actor-details` shows which. Before
any run: say the actor, the input count and the expected cost; start with
10 accounts or 50 results and ask before scaling. Cap every call with the
actor's `maxResults` or equivalent. A run that is still going when the
call returns is picked up with `get-actor-output`, never re-run. The
summary reports, per actor, runs, inputs, results and the rough total; the
console (Storage > Dataset) holds the raw dataset a person can export by
hand as the manual route.

## The `actor` column

Every snapshot row carries `actor`: the actor's ID in `owner/name` form
(`apify/google-search-scraper`), as returned by `search-actors`, so a
person can open the Store page and audit the source and the spend.
Enriched snapshots carry the enriching actor's ID in the same column, with
the raw pull's ID kept in the raw file.
