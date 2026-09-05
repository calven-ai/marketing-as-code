<!-- source: https://raw.githubusercontent.com/manojbajaj95/claude-gtm-plugin/main/skills/ab-test-setup/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# The experiment record and the pre-launch QA

Condensed from the A/B test setup skill above, reshaped as the file
`projects/<x>/experiments/<slug>.md` this repo keeps.

## Sections of the record

```markdown
# Experiment: <slug>

- **Page or flow:** <url or step>
- **Owner:** <name> · **Project:** projects/<x>
- **Status:** planned | running | done
- **Dates:** planned start, planned end (computed), actual

## Hypothesis
Because <observation, snapshot path>, we believe <change> will <effect>
for <audience>. We will know when <primary metric> moves by <MDE>.

## Variants
| Variant | What changes | Screenshot or copy |

## Metrics
- Primary: <ontology event or metric>
- Secondary: <list>
- Guardrails: <metric, the level that stops the test>

## Sizing
Baseline <rate> from <snapshot>; MDE <relative %>; sample <n> per
variant; traffic <n>/week from <snapshot>; duration <weeks>; split
<50/50>.

## Implementation
Client-side or server-side; where the flag or variant lives; who
builds it.

## Pre-launch QA
- [ ] every variant renders on desktop and at 375 px
- [ ] the primary event fires once per conversion in every variant
- [ ] the split is random and sticky per visitor
- [ ] UTMs and the funnel snapshot can tell the variants apart
- [ ] no other change to the page is scheduled during the run
- [ ] end date on the calendar; nobody reads results before it

## Result (appended when done)
Sample reached per variant; primary metric per variant with the 95%
interval and p-value; secondary and guardrail outcomes; segment notes;
decision (ship, reject, iterate); learning; decision-log link.
```

## The ten steps the source walks

Assess the context and constraints; write the hypothesis; design one
meaningful variant; compute the sample; define primary, secondary and
guardrail metrics; implement; QA every variant and the tracking; run
without peeking or mid-test changes; analyse significance, effect size
and segments; document hypothesis, result and learning.

## Analysis rules

Significance at p under 0.05, then check the effect size against the
minimum detectable effect (a significant 2% lift when 20% was needed is
not the win that was planned), then the guardrails, then segments only
when signals are mixed, and only as questions for the next test.
