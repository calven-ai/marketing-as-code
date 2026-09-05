---
name: review
description: Pre-publish review of a content draft against strategy, messaging, and brand voice. Use when asked to review, check, or QA a draft, or before any piece moves to in-review status. Reports findings; does not rewrite without being asked.
license: MIT
metadata:
  kind: workflow
  area: content
  needs: []
  optional: [context-layer]
  writes: repo
  runs: person
---

# Content review

Review the given draft (or the piece the conversation is about) against the
repo's own standards. You are the check that the strategy actually made it
into the words.

Needs: nothing wired; `strategy/` (messaging, personas, ICP) and
`brand/voice.md` filled. With a `context-layer` integration wired (the
Wired table in `integrations/README.md`), read the strategy documents it
serves and treat the Markdown files as the fallback.

## Before the checks

If `strategy/messaging.md`, `strategy/personas.md`, `strategy/icp.md` or
`brand/voice.md` still carries `Template: unfilled`, stop: there is
nothing to review against, and a review against placeholders is confident
nonsense. Say so, suggest `/setup`, and offer only check 5 (mechanics)
in the meantime.

## Checks, in order of severity

1. **Strategy fit**: does the piece advance a pillar from
   `strategy/messaging.md`, speak to a persona from
   `strategy/personas.md` inside the fit defined by `strategy/icp.md`, and
   stay inside the positioning? A well-written piece for the wrong audience
   fails review. If a strategy file says `source: context-layer`, check
   against the document served over MCP, not the file; if its
   `last_reviewed` is older than 90 days, say so in the review.
2. **Argument**: does it deliver the brief's stated argument? Flag drift
   between `brief.md` and the draft.
3. **Claims**: every number and factual claim traceable (to `data/`
   snapshots, cited sources, or the brief's raw material). Untraceable
   claims are findings, not style notes.
4. **Voice and terminology**: against `brand/voice.md`, its do/don't
   examples and tone-by-context, plus the terms: product and feature names
   spelled as `strategy/positioning.md` and `brand/voice.md` spell them,
   the glossary and jargon the audience actually uses, and nothing from
   the banned list. Quote the offending sentence and show the on-voice
   rewrite.
5. **Mechanics**: frontmatter complete and correct (`project`, `channel`,
   `owner`), links resolve, naming conventions per `data/ontology/naming.md`
   if UTMs appear.

## Output

Findings ordered by severity, each with location, problem, and suggested
fix. End with a verdict: *ready for human review* / *needs work first*.
Never flip `status:` yourself past `in-review`, and don't rewrite the draft
unless asked; review and revision are separate requests.
