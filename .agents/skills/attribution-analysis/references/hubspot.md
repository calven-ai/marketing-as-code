# HubSpot touch and source fields

The pull is `snapshot-pull` (`.agents/skills/snapshot-pull/references/hubspot.md`).
This file names where HubSpot keeps first touch, last touch and the
multi-touch views, so the three views in the readout come from fields the
portal actually records.

## Contact-level source fields

| View | Properties |
| --- | --- |
| first touch | `hs_analytics_source`, `hs_analytics_source_data_1`, `hs_analytics_source_data_2` (original source and its drill-downs), `hs_analytics_first_touch_converting_campaign`, `hs_analytics_first_url`, `hs_analytics_first_visit_timestamp` |
| last touch | `hs_analytics_last_touch_converting_campaign`, `hs_analytics_last_url`, `hs_analytics_last_visit_timestamp`, `hs_latest_source`, `hs_latest_source_data_1`, `hs_latest_source_data_2` |
| UTMs at first conversion | `hs_analytics_first_referrer`; the form submission's `utm_*` values land in the custom properties the portal maps them to (check the property list; names vary) |
| self-reported | a custom property the team's form writes (ask; commonly "how did you hear about us") |

`hs_analytics_source` values: ORGANIC_SEARCH, PAID_SEARCH, EMAIL_MARKETING,
SOCIAL_MEDIA, REFERRALS, OTHER_CAMPAIGNS, DIRECT_TRAFFIC, OFFLINE,
PAID_SOCIAL. Map them to `data/ontology/naming.md`, never the other way.

## Deal-level source

Deals inherit nothing automatically. Use the deal's associated contacts
(request associations on the deals search, or pull associations per deal
id in batches of 100) and take the first-touch fields of the earliest
associated contact for first touch, the last-touch fields of the contact
whose last visit precedes `createdate` for last touch. Deals with no
associated contact have no touches: a gap, counted.

## Multi-touch in the portal

Marketing Hub Professional and above compute attribution reports
(contact create, deal create, revenue) with first touch, last touch,
linear, U-shaped, W-shaped, full-path and time-decay models, and the
campaign attribution read tool exposes them. When available, pull the
revenue attribution report for the period as
`data/crm/snapshots/YYYY-MM-DD-hubspot-attribution.csv` with
`model,channel,campaign,deals,amount`, and use it as the multi-touch view;
say which model the portal ran. Without it, build position-based from the
touch snapshot.

## Touch snapshot

`deal_id,contact_id,touch_date,source,medium,campaign,position`: one row
per contact and per first or last touch (`position` = first or last),
plus one row per campaign membership or email click in the deal's window
when the engagement data is pulled. Contact ids only; no names or emails
in a public repo.
