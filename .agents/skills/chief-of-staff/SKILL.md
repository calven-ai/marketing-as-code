---
name: chief-of-staff
description: Process meeting transcripts from memory/transcripts/inbox/ into decisions, action items, and knowledge updates. Use when asked to "process the transcript inbox", "process this meeting", or when a new transcript needs turning into decisions, tasks, and doc updates.
---

# Chief of staff: transcript processing

Meetings stop evaporating here. For each transcript in
`memory/transcripts/inbox/` (or the specific one named), extract everything
of lasting value and route it to where it lives.

## Per transcript

1. **Read it fully.** Note the meeting date, attendees, and purpose (from
   the filename and content).
2. **Extract decisions** — things that were *resolved*, not merely
   discussed. Append each to `memory/decision-log.md` in its exact format
   (date, decided-by, source = the transcript's `processed/` path, context,
   follow-ups). When resolution is ambiguous, list it under "unclear —
   confirm?" in your summary instead of logging it.
3. **Extract action items** — owner, task, deadline where stated. File them
   per `integrations/tasks.md`, each linking back to the transcript.
4. **Extract facts worth keeping** — learnings, customer quotes, plans that
   affect existing docs. Propose updates to `memory/knowledge/` (new topic
   file or edit) and to any affected `strategy/`, `brand/`, or `projects/`
   docs. **Always as a reviewable diff / PR — never a silent write.**
   Project `status.md` updates that merely record what the meeting said
   about that project are the one routine exception: apply those directly.
5. **Move the transcript** to `memory/transcripts/processed/` (same
   filename).

## Summary (always, per transcript)

Decisions logged (count + one-liners) · tasks filed (owner → task) ·
doc updates proposed · anything unclear that needs a human's confirmation.

## Rules

- Attribute only what the transcript supports; transcription errors exist —
  when a name or number looks garbled, flag it.
- Quote sparingly in outputs; transcripts can contain sensitive discussion.
- Never delete a transcript, and never process `processed/` files twice.
