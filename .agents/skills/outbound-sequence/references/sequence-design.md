<!-- source: https://raw.githubusercontent.com/manojbajaj95/claude-gtm-plugin/main/skills/outbound-email-strategy/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Sequence design: the brief, lengths, reply handling, deliverability

Condensed from the source above.

## The brief, five lines

| Element | Question |
| --- | --- |
| title | who decides |
| company | which size and type |
| pain | the problem, in their words |
| trigger | why now |
| proof | the credibility that fits this persona |

In this repo these come from `strategy/personas.md`, `strategy/icp.md`,
the signal snapshot and `strategy/positioning.md`.

## Length per step

| Step | Goal | Words | CTA |
| --- | --- | --- | --- |
| 1 | relevance | 50 to 100 | soft ask |
| 2 | credibility | 75 to 125 | a time |
| 3 | another angle | 50 to 75 | yes or no |
| 4 | social proof | 60 to 90 | a simple reply |
| 5 | close out | 25 to 40 | none, or the breakup |

Options: five touches in one week (fast), five to seven over two weeks
(classic), 12 to 14 over four to six weeks (long play, for enterprise).
This repo's default is three to five; longer needs a reason in the brief.

## Reply handling for the rep

| Reply | Respond within | Do |
| --- | --- | --- |
| positive | 5 minutes | book the meeting |
| curious | 1 hour | send the proof |
| objection | same day | the scripted answer |
| timing | same day | set a dated reminder, stop the sequence |
| referral | 1 hour | new thread to the referral, mention the referrer |
| hard no | 24 hours | polite close, suppress |

## Volume while testing

20 to 50 a day in weeks 1 to 2 to find what works; 50 to 100 in weeks 3
to 4; only then more. The first batch of a new sequence stays under 50.

## Deliverability floor

SPF, DKIM and DMARC on the sending domain; complaint rate under 0.1
percent (0.3 is the hard ceiling); plain text; one link at most; a real
reply-to. If the team cannot confirm authentication, say the sequence
should not go out yet.
