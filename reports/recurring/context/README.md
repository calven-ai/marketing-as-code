# reports/recurring/context/

Context-freshness reports, one file per run, named by date: `YYYY-MM-DD.md`.
The `context-freshness` skill writes them monthly from the `last_reviewed`
dates in `strategy/` and `brand/` and the entries in
`memory/decision-log.md`: what is stale, what contradicts a decision, and
what to review next.
