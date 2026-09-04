<!-- source: https://raw.githubusercontent.com/manojbajaj95/claude-gtm-plugin/main/skills/content-strategy-and-planning/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Planning the calendar

Condensed from the source above and rewritten for this repo.

## Shape of the calendar

A month is laid out week by week; each row carries the day, the channel,
the content type, the topic and a status. This repo's version adds the
repo path of the piece and its owner, and takes `status` from the piece's
own frontmatter rather than tracking it twice.

## The one ordering rule

Every piece is searchable, shareable or both, and is prioritised in that
order. A slot with no searchable candidate goes to the strongest
shareable one; a slot with neither stays empty rather than filled with
filler.

## Content types by effort and job

| Type | Effort | Job |
| --- | --- | --- |
| LinkedIn or social post | low | engagement, brand |
| Blog post | low to medium | search, awareness |
| Case study | medium | proof |
| Video | medium | engagement |
| Whitepaper or guide | high | lead generation |
| Webinar | high | demand |

A worked monthly mix the source gives for a small team: eight LinkedIn
posts, two blog posts, one case study. Treat it as a starting point and
size to what the team actually shipped last month (`content-inventory`
tells you).

## Pillars before slots

1. Pick three to five pillars, from the product, the audience, search
   data or competitor coverage; here they come from
   `strategy/messaging.md`.
2. Map subtopic clusters under each.
3. Fill the calendar from the clusters, so a month reads as a few themes
   rather than a scatter.

## Trust signals to schedule on purpose

Customer evidence (case studies, quotes), expert credentials, claims with
specific numbers, method transparency, security and compliance pages,
visible publication dates. If none of these appear in a quarter, add a
row.

## From calendar row to brief

Each row that reaches its production date needs a brief: primary keyword
and a few secondaries, the top of the SERP and its format, an outline
with the keyword in the H1 and mapped H2s, and a word count target. That
is the `content-brief` skill; the calendar only names the row.
