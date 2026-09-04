<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/analytics/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# The monthly UTM and event audit

Condensed from the source above and rewritten for this repo. The rules
themselves live in `data/ontology/naming.md` and
`data/ontology/events.md`; this file is how to check against them.

## UTM parameters

| Parameter | Job | Typical values |
| --- | --- | --- |
| `utm_source` | where the traffic came from | google, newsletter, linkedin |
| `utm_medium` | the channel type | cpc, email, social, referral |
| `utm_campaign` | the initiative | the campaign slug from `projects/` |
| `utm_content` | the creative or placement | hero_cta, footer_link |
| `utm_term` | the paid keyword | as the ad platform sets it |

Conventions the source recommends and this repo's ontology should
state: lowercase everywhere, one separator, one slug per campaign
across every system, specific but short.

## Checking a month of campaigns

For each row of the `utm-campaigns` snapshot, set `conforms` and
`reason`:

1. Case: any uppercase character in a parameter.
2. Allowed values: `utm_source` and `utm_medium` outside the lists in
   `naming.md`.
3. Pattern: `utm_campaign` not matching the pattern in `naming.md`, or
   naming a campaign with no `projects/<slug>/` folder.
4. Missing: `utm_medium` present with no `utm_source`, or the reverse.
5. Drift: the same campaign spelled two ways in the month.

Report the count of non-conforming sessions, the top offenders, and
the fix as a task per `integrations/tasks.md`. `utm-builder` generates
links that pass these checks in the first place.

## Events worth having on a marketing site

The source's baseline: `cta_clicked` (button text, location),
`form_submitted` (form type), `signup_completed` (method, source),
`demo_requested`. Names are object plus action, lowercase with
underscores, with context in properties rather than in the name. If
`data/ontology/events.md` lacks an event the report needs, propose the
row; never invent one in the report.

## Validation checks when numbers look wrong

Events fire on the right condition; property values populate; no
duplicate firing (two containers, two triggers); works on mobile and
across browsers; conversions record; no personal data in properties.
Cookie consent in the EU, UK and California means the numbers undercount
by design; say so in the caveats rather than adjusting them.

## Principle

Track for decisions, not for data. Start from the question the team
will act on and work backward to the report; a metric nobody would act
on is left out of the weekly.
