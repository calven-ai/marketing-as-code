# PostHog for the web analyst

The wired route is PostHog's remote MCP (catalog id `posthog`, source
token `posthog`) with `?readonly=true` in the URL, or `posthog-cli api`
for a scripted run. Check the server's tool list in the session; the
useful ones run a HogQL query, list insights, and read a dashboard.
`snapshot-pull` does the pull; this file says what to ask for.

## Read the ontology first

`data/ontology/events.md` names the events that count as conversions
and which system emits them. PostHog's own `$pageview`, `$pageleave`
and `$autocapture` are not conversions. Never assume `signed_up` means
what it says; the ontology says.

## Weekly queries (HogQL, last seven full days)

Traffic by source: sessions grouped by the session's entry
`$referring_domain`, `$entry_utm_source`, `$entry_utm_medium`, with the
channel type PostHog derives (`$channel_type`) as `channel_group`. Count
distinct `$session_id` as sessions and distinct persons as users; a
person whose first seen date is inside the window is a new user.

Conversions: count of each ontology event grouped by the channel type of
the session it happened in; distinct persons as `users`.

Landing pages: sessions grouped by `$entry_pathname`, with the count of
sessions that also fired an ontology event as `conversions`.

Use the `sessions` table where the project has it; otherwise derive
from `events` by `$session_id`. Ask for full days ending yesterday and
say when the project's timezone differs from the team's.

## Monthly additions

Pages: `$pageview` grouped by `pathname` with views, distinct persons,
and engagement seconds from `$pageleave` where available. UTM campaigns:
sessions grouped by `$entry_utm_source`, `$entry_utm_medium`,
`$entry_utm_campaign`, `$entry_utm_content`; `conforms` and `reason` are
computed here against `data/ontology/naming.md`.

## Field to column mapping

| Column | PostHog field |
| --- | --- |
| `source`, `medium` | `$entry_utm_source` or `$referring_domain`, `$entry_utm_medium` |
| `channel_group` | `$channel_type` |
| `sessions` | count distinct `$session_id` |
| `users`, `new_users` | count distinct person; first seen in window |
| `engaged_sessions` | sessions longer than ten seconds or with two pageviews or an event |
| `landing_page` | `$entry_pathname` |
| `page_path`, `views` | `pathname`, count of `$pageview` |

State the definition of `engaged_sessions` you used in the report's
caveats; PostHog has no built-in equivalent to GA4's.

## Cost and limits

HogQL queries count against the project's query budget; on the free
tier they cost nothing and on paid plans they are metered per query.
Say how many queries you ran (three weekly, five monthly) and keep each
to one window.

## Without the MCP

Open the insight (Trends or a SQL insight) for each query, export as
CSV, and drop it into `data/analytics/snapshots/` with the names in the
skill; rename columns to the ones above.
