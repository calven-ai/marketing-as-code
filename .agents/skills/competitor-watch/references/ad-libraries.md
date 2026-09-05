<!-- source: https://raw.githubusercontent.com/thatrebeccarae/claude-marketing/main/skills/competitor-ads-analyst/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Reading competitor ad libraries

Condensed from the competitor ads analyst in claude-marketing. Ad
libraries need a browser and often a login, so in this repo a person
exports what they see and the agent reads the export as data.

## Where the ads are

| Platform | Library | Access |
| --- | --- | --- |
| Meta (Facebook, Instagram) | facebook.com/ads/library | Public |
| Google | adstransparency.google.com | Public |
| TikTok | library.tiktok.com | Public |
| LinkedIn | linkedin.com/ad-library | Needs a logged-in account |

## What to record per ad

Headline, body copy and call to action; visual style (image, video,
carousel, user-generated, before and after); destination URL; the dates
it ran; platform and placement. In this repo that is one row per ad in
`data/accounts/snapshots/YYYY-MM-DD-web-competitor-ads.csv` with columns
`competitor,platform,first_seen,last_seen,headline,body,cta,format,landing_url,message_type,funnel_stage`.

## Two ways to classify each ad

Message type: pain point, solution positioning, testimonial or case study,
offer or promotion, instructional, brand awareness.
Funnel stage: top (awareness, education), middle (comparison,
consideration), bottom (conversion, time-limited offers).

## Analyse patterns, not single ads

- Which pains appear across several competitors, and which only one
  names.
- Where messaging duplicates and where it diverges from ours.
- The formats each competitor favours and how long ads keep running (a
  long-running ad is one that works).
- A positioning map on the attributes buyers compare.
- The angles nobody is using: the opportunity list for `messaging-house`
  and the paid team.

## Outputs the source suggests

A dated competitive report, a creative swipe file, a messaging comparison
matrix, or a campaign brief. Here the findings go into the monthly
competitor report and, when they change a card, into the battlecard's
"their common attacks" table.
