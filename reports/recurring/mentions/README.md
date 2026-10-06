# reports/recurring/mentions/

AI answer-engine visibility reports, one file per run, named by date:
`YYYY-MM-DD.md`. The `brand-monitor` skill writes them from the
`*-aeo-results.csv` and `*-aeo-answers.csv` snapshots in
`data/seo/snapshots/`, scored by `scripts/aeo_diff.py`; each ends with
the forecast line the next scoring reads. `YYYY-MM-DD-sov.md` is the
share-of-voice view the `ai-share-of-voice` skill writes from the same
snapshots.
