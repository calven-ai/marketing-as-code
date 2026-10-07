# Naming conventions

Every campaign has one slug, the same in every system. Agents apply these
exactly and flag violations they find.

## UTM parameters

| Parameter | Convention | Example |
| --- | --- | --- |
| `utm_source` | `linkedin`, `hubspot`, `newsletter`, `partner-<slug>`; lowercase | `linkedin` |
| `utm_medium` | `paid-social`, `social`, `email`, `newsletter`, `referral` | `paid-social` |
| `utm_campaign` | The campaign's project slug from `projects/` | `q3-launch` |
| `utm_content` | The asset or ad set slug inside the campaign | `paid-phase-2` |

Organic search and direct traffic carry no UTMs. A link without
`utm_campaign` is never counted toward a campaign, however close its date.

## Channels and sources

The model for web reports. Scope is the session's entry: the UTM tags,
referrer and URL of its first pageview, never a later page's.

Each session gets one channel, by the first rule that matches:

| # | Channel | Matches |
| --- | --- | --- |
| 1 | Direct | a referrer on example.com (a session continuing, not an acquisition) |
| 2 | Paid | a paid `utm_medium` (`cpc`, `ppc`, `paid-*`, `display`, `retargeting`, `affiliate`) or an ad click id (`gclid`, `msclkid`, `gad_source`); not `fbclid`, which rides on organic shares too |
| 3 | Newsletter | `utm_medium=newsletter`, or a newsletter platform as source or referrer |
| 4 | Email | `utm_medium=email`, or a webmail or mail-app referrer |
| 5 | AI Assistant | `utm_medium=ai_assistant`, an answer engine as `utm_source` (`chatgpt.com`, `perplexity`, `claude.ai`, `gemini`, `copilot`), or an answer-engine referrer |
| 6 | Organic Search | `utm_medium=organic`, or a search-engine referrer (a search company's other apps, like docs or drive, are not search) |
| 7 | Social | `utm_medium` `social` or `influencer`, or a social or messaging referrer, mobile app packages included |
| 8 | Referral | any other referrer, any other `utm_source`, or a `?ref=` parameter |
| 9 | Direct | nothing at all |

**Source** is `utm_source`, else the referring domain (example.com
dropped), else `?ref=`, else `Direct`.

### The QMR roll-up

The QMR and its snapshots report five rows, so quarters compare with the
ones before this model was adopted:

| QMR row | Channels in it |
| --- | --- |
| Organic | Organic Search |
| Direct | Direct |
| Referral | Referral, AI Assistant |
| Social | Social, Paid (all paid spend is LinkedIn) |
| Email | Email, Newsletter |

## Campaign names across systems

| System | Where the slug appears | Example |
| --- | --- | --- |
| Repo | `projects/<slug>/`, content `project:` frontmatter | `projects/q3-launch/` |
| HubSpot | Campaign name; contact property `first_touch_campaign` | `q3-launch` |
| LinkedIn Ads | Campaign group = slug; campaigns `<slug>-<asset>` | `q3-launch-paid-phase-2` |
| PostHog | `utm_campaign`, `utm_content` on the first pageview | `q3-launch` / `paid-phase-2` |

## File naming in this repo

- Snapshots: `YYYY-MM-DD-<source>-<what>.csv` (defined in
  `data/README.md`)
- Content folders: `YYYY-MM-<slug>/`
- Ad-hoc reports: `reports/adhoc/YYYY-MM-DD-<question-slug>/`
