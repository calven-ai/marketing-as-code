<!-- source: https://raw.githubusercontent.com/manojbajaj95/claude-gtm-plugin/main/skills/marketing-campaign-management/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Choosing channels and setting KPIs

Condensed from the campaign-management skill above. The five stages it
uses (strategy, planning, creation, execution, measurement) map to
`campaign-plan`, the content skills, `publish`, and the data roles.

## Match the channel to the job

| Channel | Good at | Content that fits | KPI (ontology term) |
| --- | --- | --- | --- |
| Email to the house list | reaching people who already know us | announcement, sequence | clicks, replies, signups |
| LinkedIn organic and paid | B2B reach by role and company | thought leadership, document ads | engagement, leads, CPL |
| Search (paid) | intent that already exists | RSAs to a landing page | CPL, cost per SQL |
| Blog and SEO | durable traffic on a topic | guides, comparison pages | rank, organic sessions, signups |
| Webinar or event | depth with a live audience | talk, follow-up sequence | registrants, attendees, SQLs |
| Community and partners | trust from a third party | AMA, co-marketing | referred signups |
| PR | credibility, timed moments | release, briefing | coverage, referral traffic |

Double down where the team already has an advantage (an audience, a
proof, a partner) instead of running every channel at once. Most results
come from a few channels; plan for that, then cut.

## Rules of thumb the source states

- Email: about 43% opens and 2% clicks on average for marketing sends
  (label as directional; this team's own history in
  `data/email/snapshots/` wins).
- Paid: judge on CPA or CPL and, where the CRM joins, cost per SQL;
  CTR is a diagnostic, not a goal.
- Content: traffic and conversions, not time on page alone.
- Every campaign carries UTMs from `data/ontology/naming.md` on every
  link, set up before the first asset goes live.

## The pre-launch checklist

- Audience defined as a persona and stage, not a demographic.
- Goal with baseline, target and date.
- UTMs generated and tested; conversion tracking fires on the landing
  page.
- Landing page loads on mobile; the CTA matches the ad or email promise.
- Brand voice check (`review`) on every outward piece.
- Owners and live dates on every calendar row.
- Retargeting audiences created before launch.
- The decision to run is logged (`log-decision`).
