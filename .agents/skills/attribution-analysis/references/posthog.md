# PostHog touch and source properties

The pull is `snapshot-pull` (`.agents/skills/snapshot-pull/references/posthog.md`).
PostHog stores first-touch and last-touch acquisition on the person, and
every session's entry source on the session, so the three views are
queries over properties the SDK already set.

## Properties

| View | Where |
| --- | --- |
| first touch (person) | `person.properties.$initial_utm_source`, `$initial_utm_medium`, `$initial_utm_campaign`, `$initial_utm_content`, `$initial_referring_domain`, `$initial_current_url`; set once, on the first event |
| last touch (person) | `person.properties.utm_source`, `utm_medium`, `utm_campaign`, `$referring_domain`; overwritten on each new session that carries them |
| per session | `sessions` table: `$entry_utm_source`, `$entry_utm_medium`, `$entry_utm_campaign`, `$entry_referring_domain`, `$entry_current_url`, `$channel_type` (PostHog's channel grouping) |
| every touch | one row per `$pageview` with `properties.utm_*` and `$referring_domain`, the input for a linear or position-based view |
| self-reported | a custom event or person property the signup form sets (ask) |

## HogQL per view

- First touch of converting persons:
  `SELECT person.properties.$initial_utm_source AS source, person.properties.$initial_utm_medium AS medium, person.properties.$initial_utm_campaign AS campaign, count(DISTINCT person_id) FROM events WHERE event = '<conversion event>' AND timestamp >= '<start>' AND timestamp < '<end>' GROUP BY 1,2,3`
- Last touch (the converting session):
  `SELECT s.$entry_utm_source, s.$entry_utm_medium, s.$entry_utm_campaign, count(DISTINCT e.person_id) FROM events e JOIN sessions s ON e.$session_id = s.session_id WHERE e.event = '<conversion event>' AND ... GROUP BY 1,2,3`
- All touches for position-based: every `$pageview` with a non-empty
  `utm_source` or a non-empty `$referring_domain` by persons who
  converted in the period, ordered by timestamp per person; save as
  `data/analytics/snapshots/YYYY-MM-DD-posthog-touches.csv`
  (`person_id,touch_date,source,medium,campaign,position`).

Conversion events are the ones `data/ontology/events.md` marks; never
assume `signed_up` means what it says.

## Joining to the CRM

The join key is `distinct_id` or the person's email when the product
identifies users and the CRM stores the same id; PostHog has a HubSpot
and a Salesforce destination that write it. Without a key, the web view
and the deal view are two tables side by side. Person ids are pseudonymous
but can be linked; treat a touch snapshot with person ids like contact
ids under the PII rule.
