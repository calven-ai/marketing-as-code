<!-- source: https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/marketing/skills/campaign-plan/SKILL.md | license: Apache-2.0 | fetched: 2026-09-04 -->

# Cadence, lead times and the campaign shape

Condensed from the source above and rewritten for this repo. The numbers
are the source's defaults, not measurements of this team.

## Building the calendar

Set the milestones (launch, event, quarter end), work backward with the
production lead times, map each piece to a buying stage, batch by theme,
balance channels across the weeks, and keep about 20% of the slots free.

Calendar columns in the source: week, piece, channel, owner or notes,
status. This repo's table adds the repo path and a `depends on` column.

## Production lead times

| Piece | Lead time |
| --- | --- |
| Blog post | 3 to 5 working days |
| Email | 2 to 3 working days |
| Social posts | 1 to 2 working days |
| Landing page | 5 to 7 working days |
| Video | 2 to 4 weeks |
| Ebook or whitepaper | 2 to 4 weeks |

Add review time on top: every piece passes `review` and a person before
it ships.

## Cadence defaults

- Blog: one to four posts a week
- Email: weekly or every two weeks
- Social: three to seven posts per platform a week
- Paid: continuous, with creative refreshed every two to four weeks

Halve these for a team of one or two; a cadence the team cannot hold is
worse than a slower one it can.

## Channels by ownership

Owned (blog, email, organic social, webinars, podcast) is where
conversion happens; earned (PR, guest content, partners, community,
reviews) and paid (search, social, display, sponsored content, events)
are chosen by where the audience is, the buying stage, the budget and
what already performed. The calendar shows all three so a launch week
does not land on owned channels alone.

## A campaign's calendar section

When the calendar belongs to a campaign, its `campaign.md` already holds
the narrative and the goals; the calendar file holds the week-by-week
breakdown and the list of pieces needed with a priority each. Metrics per
campaign type (reach for awareness, MQLs and cost per lead for lead
generation, signups and activation for a launch, registrations and
attendance for events) are defined in `data/ontology/metrics.md`, never
here.
