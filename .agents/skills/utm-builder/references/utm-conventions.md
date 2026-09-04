<!-- source: https://raw.githubusercontent.com/manojbajaj95/claude-gtm-plugin/main/skills/utm-builder/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# A starting UTM convention

Propose this to a team whose `data/ontology/naming.md` is still a
template, as a diff; the team edits and merges. Everything is lowercase,
words separated by hyphens, no spaces, because analytics tools treat
`LinkedIn` and `linkedin` as two campaigns.

## Parameters

| Parameter | Required | Holds | Pattern |
| --- | --- | --- | --- |
| `utm_source` | yes | where the click came from | one token from the allowed list |
| `utm_medium` | yes | the channel type | one token from the allowed list |
| `utm_campaign` | yes | the campaign | `<yyyy>-<slug>` or `<yyyy-mm>-<slug>`, the same slug as `projects/<slug>/` |
| `utm_content` | when there is more than one link per channel | the variant or placement | `<format>-<variant>` or `<placement>`, e.g. `video-a`, `hero`, `footer` |
| `utm_term` | paid search only | the keyword or ad group | the keyword, hyphenated |

## Allowed sources (extend on purpose)

- Paid: `google`, `bing`, `linkedin`, `meta`, `x`, `reddit`, `youtube`
- Organic social: the same tokens with `medium=social`; never
  `linkedin-organic` as a source, the medium carries organic vs paid
- Email: `newsletter`, `nurture`, `product`, `sales` (a rep's sequence)
- Partners and referrals: `partner-<name>`, `affiliate-<name>`,
  `podcast-<name>`, `event-<slug>`, `pr-<outlet>`

## Allowed mediums

- Paid: `cpc`, `paid-social`, `display`, `video`, `retargeting`
- Owned: `email`, `social`, `blog`, `webinar`, `podcast`
- Earned: `referral`, `pr`, `partner`
- Other: `sms`, `push`, `qr`

Mediums matter twice: they group channels in the report, and GA4's
default channel grouping recognises a fixed set (`cpc`, `email`,
`social`, `paid-social`, `display`, `referral`, `affiliate`, `video`,
`organic`); a medium outside it lands in Unassigned. Keep to the list or
document the exception.

## Campaign naming

`<yyyy>-<slug>` with the slug identical to the project folder, the CRM
campaign and the ad platform campaign. Add a segment only when the same
campaign runs to distinct audiences: `2026-q4-launch-enterprise`.

## Common mistakes

| Mistake | Effect | Fix |
| --- | --- | --- |
| mixed case | duplicate campaigns in every report | lowercase everything |
| spaces or `%20` | broken URLs, duplicate rows | hyphens |
| missing `utm_medium` | traffic falls into Unassigned | always set it |
| generic campaign (`launch`) | no way to tell years apart | date prefix plus a specific slug |
| a source per placement (`linkedin-feed`) | the source list explodes | placement goes in `utm_content` |
| UTMs on internal links | the session's original source is overwritten | never tag links inside the site |

## Output

A link table per campaign: `Channel | Source | Medium | Content |
Full URL`, one row per variant, grouped by channel, kept in the campaign
file so the report can join on the slug.
