# memory/

**Kind:** context, what the team knows.

The part that compounds: decisions, knowledge, and the meeting-transcript
pipeline that feeds them.

## Layout

| Path | Owns |
| --- | --- |
| [decision-log.md](decision-log.md) | Every decision: dated, attributed, linked to its source. Append-only. |
| `knowledge/` | The living knowledge base: one topic per file, updated as facts change |
| `transcripts/inbox/` | New meeting transcripts land here, pulled by script or dragged in by a person |
| `transcripts/processed/` | Transcripts move here once processed |

## The pipeline

1. A transcript lands in `transcripts/inbox/`, pulled by
   `scripts/pull_transcripts.py` (Granola; the daily `transcripts-cron`
   GitHub Action runs it too) or dragged in by a person. A connector for
   another meeting tool writes the same shape, per the inbox contract in
   [`transcripts/README.md`](transcripts/README.md). Name files
   `YYYY-MM-DD-<meeting>.md` (`.txt` and `.vtt` work too).
2. The `chief-of-staff` skill processes each inbox file:
   - facts worth keeping: proposed edits to `knowledge/` and any affected
     `strategy/` or `projects/` docs, as a reviewable diff, never a silent
     write
   - decisions: appended to `decision-log.md`
   - project status: entries in `projects/<name>/status.md`
   - action items: grouped per owner, filed per `integrations/tasks.md`
   - risks and red flags: in the summary, and posted to the leadership
     Slack channel when Slack is configured
3. The transcript moves to `processed/`. Nothing is deleted. A "Transcript
   processed" summary goes to the team Slack channel, or is printed when
   Slack is not set up.

## For agents

- "What did we decide about X?" Search `decision-log.md` first, then
  `knowledge/`.
- Every decision-log entry follows the format at the top of the file. Append
  only. History is the point.
- Transcripts are the most sensitive files in this repo: names, customer
  details, salaries, candid opinions. The repository is private by rule
  (AGENTS.md, rule 8); a team that still wants them out of Git ignores
  `memory/transcripts/` and versions only what the skill extracts. Log
  that choice in `decision-log.md`. Quote them in outputs only as much
  as the task needs.
