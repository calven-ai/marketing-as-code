---
name: review
description: Pre-publish review of a content draft against strategy, messaging, and brand voice. Use when asked to review, check, or QA a draft, or before any piece moves to in-review status. Reports findings; does not rewrite without being asked.
---

# Content review

Review the given draft (or the piece the conversation is about) against the
repo's own standards. You are the check that the strategy actually made it
into the words.

## Checks, in order of severity

1. **Strategy fit** — does the piece advance a pillar from
   `strategy/messaging.md`, speak to a persona from
   `strategy/icp-personas.md`, and stay inside the positioning? A
   well-written piece for the wrong audience fails review.
2. **Argument** — does it deliver the brief's stated argument? Flag drift
   between `brief.md` and the draft.
3. **Claims** — every number and factual claim traceable (to `data/`
   snapshots, cited sources, or the brief's raw material). Untraceable
   claims are findings, not style notes.
4. **Voice** — against `brand/voice.md`: the do/don't examples, the banned
   list, tone-by-context. Quote the offending sentence and show the on-voice
   rewrite.
5. **Mechanics** — frontmatter complete and correct (`project`, `channel`,
   `owner`), links resolve, naming conventions per `data/ontology/naming.md`
   if UTMs appear.

## Output

Findings ordered by severity, each with location, problem, and suggested
fix. End with a verdict: *ready for human review* / *needs work first*.
Never flip `status:` yourself past `in-review`, and don't rewrite the draft
unless asked — review and revision are separate requests.
