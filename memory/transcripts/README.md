# memory/transcripts/

The transcript pipeline (details in [`../README.md`](../README.md)):

- **`inbox/`**: new transcripts land here. Drag a file in, or let
  `scripts/pull_transcripts.py` fetch them from Granola. Name:
  `YYYY-MM-DD-<meeting>.md` (`.txt`/`.vtt` fine too). The daily
  `transcripts-cron` GitHub Action runs the same script and opens a pull
  request titled "Transcripts: <date>" when something new landed; merge it,
  then process.
- **`processed/`**: the `chief-of-staff` skill moves transcripts here after
  extracting decisions, project status, action items, facts, and red flags.
  Nothing is deleted.

To process what's waiting, two ways, your choice per
[docs/operating-model.md](../../docs/operating-model.md):

- **A person, after the meeting** (the default): ask your agent to
  "process the transcript inbox" (or `/chief-of-staff`). Costs nothing
  beyond the coding-agent subscription; the person watches the run.
- **Unattended**: `.github/workflows/transcripts-process.yml` runs the same
  skill as an agent in GitHub Actions whenever transcripts land on `main`,
  and opens a "Transcripts processed" PR. Opt-in: it does nothing until the
  `ANTHROPIC_API_KEY` repository secret exists, and it bills per run.
