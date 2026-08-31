# memory/

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

1. A transcript lands in `transcripts/inbox/` — via
   `scripts/pull_transcripts.py` or a simple drag-and-drop. Any text format
   works; name it `YYYY-MM-DD-<meeting>.md` (or `.txt`/`.vtt`).
2. The `chief-of-staff` skill processes each inbox file:
   **decisions** → appended to `decision-log.md`;
   **action items** → filed per `integrations/tasks.md`;
   **facts worth keeping** → proposed edits to `knowledge/` and any affected
   `strategy/` or `projects/` docs, **as a reviewable diff, never a silent
   write**.
3. The transcript moves to `processed/`. Nothing is deleted.

## For agents

- "What did we decide about X?" → search `decision-log.md` first, then
  `knowledge/`.
- Every decision-log entry follows the format at the top of the file. Append
  only — history is the point.
- Transcripts may contain sensitive discussion; quote them in outputs only as
  much as the task needs.
