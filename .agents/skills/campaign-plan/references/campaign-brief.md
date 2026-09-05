<!-- source: https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/marketing/skills/campaign-plan/SKILL.md | license: Apache-2.0 | fetched: 2026-09-04 -->

# The campaign brief: questions, sections, production times

Condensed from the campaign-plan skill above (Apache-2.0; the source
repository carries no NOTICE file). Rewritten to fit
`projects/_template/campaign.md` and this repo's ontology.

## Five questions before anything is written

1. **Objective.** One goal, one number, one date, in a term
   `data/ontology/metrics.md` defines (signups, MQLs, pipeline, attendees).
   "Awareness" needs a measurable proxy the team accepts, or it is not a
   goal.
2. **Audience.** One persona from `strategy/personas.md`, one buying stage
   from `strategy/messaging.md`, the pain in the persona's own words, and
   where they can be reached.
3. **Message.** The core message and three or four supporting points, each
   with a proof (a number, a customer, a demo) from `strategy/` or the
   discovery report. No proof, no claim.
4. **Channels.** Owned, earned and paid, each with a job and an effort or
   budget note; see `channel-mix.md`.
5. **Measure.** Primary KPI, one or two secondary KPIs, the baseline, and
   where the number will be read (the snapshot in `data/`).

Fixed dates (an event, a release) and the budget range come from the
person. With no budget, plan channel-agnostic and mark paid rows as
"if funded".

## The ten sections of the brief

`campaign.md` already carries owner, dates, budget, narrative, goals and
the projects table. Add, in this order, as sections of the same file:

1. Overview: name (the slug), one-paragraph summary, the SMART objective.
2. Audience: persona, stage, pains, channels they use.
3. Key messages: the core message and the supporting points with proofs.
4. Channel strategy: owned, earned, paid, each with job, KPI, owner,
   budget share.
5. Retargeting audiences: the list in `retargeting.md`, built before
   launch.
6. Content pieces: the deliverables with priority, each a `content/` path
   once scaffolded.
7. Calendar: pointer to `calendar.md`.
8. Budget allocation by channel, with the source of each figure. The
   source's rule of thumb is 30 to 40% of a mixed campaign on paid
   acquisition; treat it as a starting point to argue with, never as the
   answer.
9. Risks and mitigations: two or three, concrete.
10. Next steps and what needs approval.

## Production times for the calendar, working back from launch

| Piece | Typical time |
| --- | --- |
| Blog post | 3 to 5 days |
| Email | 2 to 3 days |
| Social posts | 1 to 2 days |
| Landing page | 5 to 7 days |
| Video | 2 to 4 weeks |
| Ad creative set | 3 to 5 days plus platform review |

Add review time (`review` skill, then a person) before every live date,
and a week of retargeting-audience collection before the first
retargeting ad.

## Calendar row shape

`| Piece | Channel | Owner | Ready | Live | Depends on | Status |`, one row
per piece and channel, sorted by live date. Status is read from the
piece's frontmatter, not kept here.
