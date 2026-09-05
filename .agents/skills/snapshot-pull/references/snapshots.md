# Standard snapshots and their columns

The `<what>` tokens the data roles expect, per domain, with the column set
each carries. Vendor files in this folder map their fields onto these
columns. Keep columns stable so snapshots diff across months; add a column
at the end rather than renaming one. Dates are ISO `YYYY-MM-DD`; amounts
plain numbers in the account currency.

## `data/crm/` (categories `crm`, `billing`)

| `<what>` | Columns | Notes |
| --- | --- | --- |
| pipeline | `deal_id,deal_name,company,stage,amount,close_date,created_date,owner,source,last_activity` | open deals only; `stage` is the vendor label, translated in the report through `data/ontology/funnel.md` |
| new-contacts | `contact_id,company,lifecycle_stage,source,created_date,owner` | the period's new contacts; no name or email columns |
| closed-deals | `deal_id,deal_name,company,outcome,amount,close_date,created_date,owner,source,close_reason` | `outcome` is won or lost |
| customers | `company_id,company,domain,became_customer,plan,arr,owner,industry,size` | one row per account |
| contacts | `contact_id,email,first_name,last_name,company,lifecycle_stage,source,owner,created_date,last_activity` | full export for `data-hygiene-audit`; private repo only |
| companies | `company_id,company,domain,industry,size,lifecycle_stage,owner,created_date,contact_count` | full export |
| subscriptions | `subscription_id,customer_id,company,plan,status,mrr,currency,started,current_period_end,canceled_at` | from billing; `customer_id` is the billing id |

## `data/analytics/` (category `web-analytics`)

| `<what>` | Columns | Notes |
| --- | --- | --- |
| traffic-by-source | `date,source,medium,campaign,sessions,users,new_users,conversions` | one row per day and source; `conversions` counts the ontology's primary conversion event |
| conversions | `date,event,source,medium,campaign,count` | one row per day, event and source; event names as emitted |
| landing-pages | `date,page,source,medium,sessions,conversions,conversion_rate` | entry pages |
| funnel | `step,event,users,conversion_from_previous,conversion_from_start` | one row per step; `signup-funnel` and similar variants keep this shape |

## `data/ads/` (category `ads`)

| `<what>` | Columns | Notes |
| --- | --- | --- |
| campaigns | `date,campaign,status,impressions,clicks,cost,conversions,conversion_value` | one row per day and campaign; aggregates only |

## `data/email/` (category `marketing-automation`)

| `<what>` | Columns | Notes |
| --- | --- | --- |
| sends | `campaign,send_date,sends,delivered,opens,clicks,unsubscribes,bounces` | one row per send or broadcast |
| sequences | `sequence,step,sends,delivered,opens,clicks,conversions` | per-step performance of automated flows |

## `data/reviews/` (category `surveys-reviews`)

| `<what>` | Columns | Notes |
| --- | --- | --- |
| reviews | `review_id,date,rating,role,company_size,title,pros,cons` | no reviewer names in a public repo |
| nps | `response_id,date,score,role,verbatim` | |

## `data/social/` (categories `social`, `community`)

| `<what>` | Columns | Notes |
| --- | --- | --- |
| threads | `thread_id,date,channel,title,replies,views,answered,last_reply,url` | `answered` yes or no; no author handles in a public repo |
| posts | `post_id,date,channel,impressions,engagements,clicks,url` | the team's own posts |

## `data/events/` (category `events`)

| `<what>` | Columns | Notes |
| --- | --- | --- |
| `<event>-attendees` | `registrant_id,event,registered,attended,join_time,minutes_watched,company` | private repo only when names or emails are added |

## `data/seo/` (category `seo-data`)

`scripts/seo_snapshot.py` writes `volume` (`keyword,volume,difficulty,rank,url,checked`);
`seo-analyst` owns `rankings` and `keyword-ideas` with the same columns.
