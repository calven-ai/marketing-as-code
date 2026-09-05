<!-- source: https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/marketing/skills/email-sequence/SKILL.md | license: Apache-2.0 | fetched: 2026-09-04 -->

# Designing the sequence: questions, lengths, logic, the per-email record

Condensed from the email-sequence skill above (Apache-2.0; the source
repository carries no NOTICE file).

## Ask first

1. Sequence type (below).
2. The one goal, as an ontology event.
3. Who enters, and how they are segmented.
4. How many emails the team will maintain.
5. Cadence constraints (send days, quiet periods, other sequences).
6. Voice: `brand/voice.md`, and anything specific to this audience.
7. What to feature: offers, assets, capabilities, proof.

## Lengths by type

| Type | Emails | Span |
| --- | --- | --- |
| Onboarding | 5 to 7 | 14 to 21 days |
| Lead nurture | 4 to 6 | 3 to 4 weeks |
| Re-engagement | 3 to 4 | 10 to 14 days |
| Win-back | 3 to 5 | 30 days |
| Product launch | 4 to 6 | 2 to 3 weeks |
| Event follow-up | 3 to 4 | 7 to 10 days |
| Upgrade or upsell | 3 to 5 | 2 to 3 weeks |
| Educational drip | 5 to 8 | 4 to 6 weeks |

Event follow-up: the recording and the one thing to do next within 24
hours; the deeper piece on day 2 to 3; the offer (demo, trial, call) on
day 5 to 7; a last nudge for those who clicked but did not act. Split
attendees from registrants who did not attend; they get different first
emails.

## Four phases

1. Strategy: the narrative arc across the sequence, the journey it sits
   in (`data/ontology/funnel.md`), how the ask escalates, the metric.
2. Emails: each one written to the record below.
3. Logic: branches, exits, re-entry, suppression.
4. Measurement: what `email-performance` will read for this sequence,
   and the expected range with its source.

## Per-email record

- Subject lines: two or three variants.
- Preview text: 40 to 90 characters.
- Purpose: one sentence.
- Body: formatted, in the voice guide.
- Primary CTA and its destination (a `content/` path or URL with UTMs).
- Timing: days after the previous email or the trigger.
- Condition: who is skipped, and why.

## Logic to state explicitly

- Trigger and entry conditions (the exact event or property).
- Branches: on click, on reply, on a stage change.
- Exits: converted, replied, unsubscribed, moved stage, sales-owned.
- Re-entry: never, after N days, or on a new trigger.
- Suppression: customers, open opportunities, contacts in another
  sequence, bounced or complained addresses.

## Deliverables

An overview table (email, day, subject, CTA, condition), the full drafts,
a text flow diagram showing branches and exits, the logic reference, two
or three A/B suggestions (subject, timing, CTA), and the metrics to
track.
