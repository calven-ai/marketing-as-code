# Naming conventions

> **Template: unfilled.** Type over the brackets, or say `/setup` and answer a
> few questions. These conventions make campaigns traceable across systems;
> agents apply them exactly and flag violations they encounter.

## UTM parameters

| Parameter | Convention | Example |
| --- | --- | --- |
| `utm_source` | [allowed values] | |
| `utm_medium` | [allowed values] | |
| `utm_campaign` | [pattern, e.g. `<year>-<campaign-slug>`] | |
| `utm_content` | [when used, pattern] | |

## Channels and sources

The default model for web reports; keep it, edit it, or replace it, and
every channel number in every report and dashboard follows this one
definition. Scope is the session's entry: the UTM tags, referrer and URL
of its first pageview, never a later page's.

Each session gets one channel, by the first rule that matches:

| # | Channel | Matches |
| --- | --- | --- |
| 1 | Direct | a referrer on the site's own domain (a session continuing, not an acquisition) |
| 2 | Paid | a paid `utm_medium` (`cpc`, `ppc`, `paid-*`, `display`, `retargeting`, `affiliate`) or an ad click id (`gclid`, `msclkid`, `gad_source`); not `fbclid`, which rides on organic shares too |
| 3 | Newsletter | `utm_medium=newsletter`, or a newsletter platform as source or referrer |
| 4 | Email | `utm_medium=email`, or a webmail or mail-app referrer |
| 5 | AI Assistant | `utm_medium=ai_assistant`, an answer engine as `utm_source` (`chatgpt.com`, `perplexity`, `claude.ai`, `gemini`, `copilot`), or an answer-engine referrer |
| 6 | Organic Search | `utm_medium=organic`, or a search-engine referrer (a search company's other apps, like docs or drive, are not search) |
| 7 | Social | `utm_medium` `social` or `influencer`, or a social or messaging referrer, mobile app packages included |
| 8 | Referral | any other referrer, any other `utm_source`, or a `?ref=` parameter |
| 9 | Direct | nothing at all |

Newsletters and answer engines strip the referrer, so the tag decides;
that is why they come before the referrer-based rules. A vendor's built-in
channel grouping is not this model; reports use this one.

**Source** is `utm_source`, else the referring domain (own domain
dropped), else `?ref=`, else `Direct`. Every session has exactly one
channel and one source, so breakdowns add up to the total.

## Campaign names across systems

[The one slug per campaign, and how it appears in the task tool, the CRM,
ad platforms, and `projects/<slug>/`: same slug everywhere.]

## File naming in this repo

- Snapshots: `YYYY-MM-DD-<source>-<what>.csv` (defined in
  `data/README.md`)
- Content folders: `YYYY-MM-<slug>/`
- Ad-hoc reports: `reports/adhoc/YYYY-MM-DD-<question-slug>/`
