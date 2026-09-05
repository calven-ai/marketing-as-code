<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/revops/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Scoring model: components, build steps, stage table

Condensed from the source above.

## Lifecycle stages

| Stage | Enters when | Leaves when | Owner |
| --- | --- | --- | --- |
| subscriber | opts in to content | shows company info or engagement | marketing |
| lead | an identified contact with basic info | meets minimum fit | marketing |
| MQL | passes fit and engagement thresholds | sales accepts or rejects within the SLA | marketing |
| SQL | sales accepts and qualifies in conversation | opportunity created or recycled | SDR or AE |
| opportunity | need, authority, budget, timing confirmed | closed won or lost | AE |
| customer | closed won | expands, renews or churns | CS |

An MQL needs both fit and engagement; neither alone qualifies.

## Components

Explicit (fit): company size, industry, revenue, job title, seniority,
department, tech stack, geography. Implicit (engagement): pricing and demo
pages, case studies, downloads, webinar attendance, email clicks, product
usage in PLG. Negative: competitor domains, student and personal email
addresses, unsubscribes and complaints, disqualifying titles.

## Build steps

1. Weight the ICP attributes.
2. Find the behaviours that preceded closed-won deals; weight those.
3. Assign points; set the MQL threshold (typically 50 to 80 on a 100 scale,
   or a fit-and-engagement pair).
4. Backtest against last quarter's contacts.
5. Launch; recalibrate quarterly.

## Mistakes the source calls out

Overweighting downloads (research is not intent); no negative scoring;
a static model; treating every page visit alike (pricing is not the blog).

## Handoff and speed

MQL alert to the rep; first contact within 4 business hours; qualify or
reject within 48 hours with a reason code; rejected MQLs go to a recycling
nurture. Contact within 5 minutes is 21 times more likely to qualify;
after 30 minutes conversion drops tenfold; after 24 hours the lead is cold.

## Reference conversion bands

| Rate | Band |
| --- | --- |
| lead to MQL | 5 to 15 percent |
| MQL to SQL | 30 to 50 percent |
| SQL to opportunity | 50 to 70 percent |
| win rate | 20 to 30 percent, varies |

Bands are for sanity checks; the team's rates come from
`data/crm/snapshots/`.

## Pipeline stage hygiene

Required fields per stage (contact, source and fit score at qualified;
pain, current solution and timeline at discovery; decision makers at
evaluation; loss reason at closed lost); flag deals past twice the average
stage duration; block silent close-date pushes.
