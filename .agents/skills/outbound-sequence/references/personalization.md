<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/cold-email/references/personalization.md | license: MIT | fetched: 2026-09-04 -->

# Personalisation slots and the signal stack

Condensed from the source above and adapted to this repo's slot notation.

## Four levels

| Level | What it uses | Effect |
| --- | --- | --- |
| 1 basic | `{{first_name}}`, `{{company}}`, `{{title}}` | about 5 percent lift; table stakes |
| 2 segment | "most `{{industry}}` teams struggle with `{{problem}}`" | scales through micro-segments |
| 3 role | the role's own challenge and seniority context | job-specific pain |
| 4 individual | "noticed you are hiring 3 SDRs" | 50 to 250 percent more replies when tied to the problem |

Write every sequence at level 2 or 3 in the body and leave one level-4
slot in the opener that the rep fills from research.

## Where a rep finds the level-4 fact

| Signal | Source | Opener pattern |
| --- | --- | --- |
| funding | press, Crunchbase-style data, the `researcher` snapshot | "congrats on the round; scaling usually surfaces X" |
| hiring | careers page, job posts | "hiring for Y suggests Z is on the plan" |
| tech stack | enrichment `tech_stack` column | "teams on A often hit B at your size" |
| their own post or talk | LinkedIn, podcasts | reference the specific point, not the fact of posting |
| company news | news search | "the acquisition usually creates C" |
| a job change | alumni snapshot | "you saw this problem at `{{prior_company}}`" |

Each slot gets a one-line note under the step: `{{signal}}: from
data/accounts/snapshots/<file>, column <name>`.

## Slot conventions for this repo

- Slots are `{{snake_case}}`; the brief lists every slot with its source.
- A slot the rep cannot fill means the touch is not sent to that person,
  not sent with a blank.
- Never put the first name in the subject line; it reads as automation.

## Three openers that work

- Trigger event: "Congrats on `{{trigger}}`; growth like that usually puts
  `{{problem}}` on the list."
- Observation: "Your post on `{{topic}}` landed, especially `{{detail}}`;
  it is close to how `{{problem}}` shows up for `{{role}}`s."
- Industry insight: "Most `{{role}}`s I talk to spend `{{hours}}` a week
  on `{{problem}}`; does that match?"

## What reads as fake

"I hope this finds you well"; "I saw your LinkedIn profile"; a compliment
unrelated to the problem; personal detail that crosses into creepy. Apply
the "so what" test: read the opener as the recipient and ask why they
would care; if the answer is unclear, rewrite.
