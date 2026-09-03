# memory/

**Kind:** context, what the team knows.

The part that compounds: decisions, knowledge, and the meeting-transcript
pipeline that feeds them.

## Layout

| Path | Owns |
| --- | --- |
| [decision-log.md](decision-log.md) | Every decision: dated, attributed, linked to its source. Append-only. |
| `knowledge/` | The living knowledge base: one topic per file, updated as facts change |
| `transcripts/inbox/` | New meeting transcripts land here (pulled by script, or dragged in by a human) |
| `transcripts/processed/` | Transcripts move here once processed |

## The pipeline

1. A transcript lands in `transcripts/inbox/`, via a pull script for your
   meeting tool (`scripts/pull_transcripts.py` ships for Granola; run it by
   hand, or let the daily `transcripts-cron` GitHub Action run it and open
   a PR with the new files; a connector for another provider writes the
   same files, per the inbox contract in
   [`transcripts/README.md`](transcripts/README.md)) or a simple
   drag-and-drop. Any text format works; name it `YYYY-MM-DD-<meeting>.md`
   (or `.txt`/`.vtt`).
2. The `chief-of-staff` skill processes each inbox file:
   **facts worth keeping** → proposed edits to `knowledge/` and any affected
   `strategy/` or `projects/` docs, **as a reviewable diff, never a silent
   write**;
   **decisions** → appended to `decision-log.md`;
   **project status** → routine entries in `projects/<name>/status.md`;
   **action items** → grouped per owner, filed per `integrations/tasks.md`;
   **risks and red flags** → always in the summary, and posted to the
   leadership Slack channel when Slack is configured.
3. The transcript moves to `processed/`. Nothing is deleted. A "Transcript
   processed" summary goes to the team Slack channel (or is printed when
   Slack is not set up).

## For agents

- "What did we decide about X?" → search `decision-log.md` first, then
  `knowledge/`.
- Every decision-log entry follows the format at the top of the file. Append
  only: history is the point.
- Transcripts may contain sensitive discussion; quote them in outputs only as
  much as the task needs.
- Transcripts are the most sensitive files in this repo: names, customer
  details, salaries, and candid opinions all end up in them. Keep them only
  in a **private** repo, and if the team prefers, gitignore
  `memory/transcripts/` entirely. The decisions, tasks, and knowledge
  extracted from them are what needs to be versioned, not the raw audio
  text. Log that choice in `decision-log.md`.
