# reports/recurring/pipeline/

Pipeline reports, one file per run, named by date: `YYYY-MM-DD.md`. The
`pipeline-report` skill writes them weekly from the `*-pipeline.csv`
snapshots in `data/crm/snapshots/`. `YYYY-MM-DD-monthly.md` is the
month-end run, which adds the forecast.
