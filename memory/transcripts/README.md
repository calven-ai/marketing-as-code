# memory/transcripts/

The transcript pipeline (details in [`../README.md`](../README.md)):

- **`inbox/`** — new transcripts land here. Drag a file in, or let
  `scripts/pull_transcripts.py` (wave 2) fetch them. Name:
  `YYYY-MM-DD-<meeting>.md` (`.txt`/`.vtt` fine too).
- **`processed/`** — the `chief-of-staff` skill moves transcripts here after
  extracting decisions, action items, and knowledge updates. Nothing is
  deleted.

To process what's waiting: ask your agent to "process the transcript inbox"
(or `/chief-of-staff`).
