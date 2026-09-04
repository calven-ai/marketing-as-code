# memory/transcripts/

Where meeting transcripts land, and where they go once processed. The
pipeline is in [`../README.md`](../README.md).

- **`inbox/`**: new transcripts. Drag a file in, or let
  `scripts/pull_transcripts.py` fetch them from Granola. The daily
  `transcripts-cron` GitHub Action runs the same script and opens a
  "Transcripts: <date>" pull request when something landed. That proposal is
  bookkeeping, so it merges itself once the checks pass.
- **`processed/`**: where the `chief-of-staff` skill moves a transcript after
  extracting decisions, project status, action items, facts and red flags.
  Nothing is deleted.

## The inbox contract

Any connector, for any meeting tool, writes files the processing skill can
read without knowing where they came from. `scripts/pull_transcripts.py`
(Granola) is the shipped example; a Zoom or Fireflies connector is a copy
of it that writes the same shape
([integrations/adding-an-integration.md](../../integrations/adding-an-integration.md)
has the worked example).

- **Filename:** `YYYY-MM-DD-<slug>.md`, the meeting date and a slug of its
  title. `.txt` and `.vtt` are accepted for files a person drags in.
- **Frontmatter:** `title`, `date` (`YYYY-MM-DD`), `source` (the provider,
  lower case: `granola`, `zoom`, `manual`), `<source>_id` (the provider's
  ID for the meeting, so re-runs can dedupe), and optionally
  `attendees: [...]`.
- **Body:** an H1 with the title, then the transcript as paragraphs of
  `**Speaker:** what they said`, in order. Speaker names as the provider
  gives them; no cleanup, no summary. The skill does the judgment.
- **Dedupe:** a connector skips any filename that already exists in
  `inbox/` or `processed/`, so re-running is safe and processed meetings
  never come back.
- **Sensitivity:** see [`../README.md`](../README.md): private repo only,
  or gitignore this folder and version only what the skill extracts.

```markdown
---
title: "Weekly marketing sync"
date: 2026-09-03
source: granola
granola_id: 3f9c...
attendees: ["Maria", "Tom"]
---

# Weekly marketing sync

**Maria:** The webinar page is at 4.1 percent now.

**Tom:** Then we move the date and tell the speaker today.
```

To process what is waiting, ask your agent to "process the transcript inbox"
(or run `/chief-of-staff`). Unattended, `.github/workflows/transcripts-process.yml`
runs the same skill in GitHub Actions when transcripts land on `main`; it
does nothing until the `ANTHROPIC_API_KEY` repository secret exists, and it
bills per run. The trade-off is in
[docs/operating-model.md](../../docs/operating-model.md).
