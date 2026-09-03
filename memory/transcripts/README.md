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

To process what's waiting, two ways, your choice per
[docs/operating-model.md](../../docs/operating-model.md):

- **A person, after the meeting** (the default): ask your agent to
  "process the transcript inbox" (or `/chief-of-staff`). Costs nothing
  beyond the coding-agent subscription; the person watches the run.
- **Unattended**: `.github/workflows/transcripts-process.yml` runs the same
  skill as an agent in GitHub Actions whenever transcripts land on `main`,
  and opens a "Transcripts processed" PR. Opt-in: it does nothing until the
  `ANTHROPIC_API_KEY` repository secret exists, and it bills per run.
