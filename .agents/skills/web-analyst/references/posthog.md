# PostHog for the web analyst

Catalog id and source token `posthog`. Three routes, the same queries:

- **Script** (unattended runs, or a person with a key):
  `python3 scripts/web_snapshot.py --domain <site domain> --cta-event <event> --conversion-event <event>`
  with `POSTHOG_API_KEY` (a personal `phx_` key with `query:read`) and
  `POSTHOG_PROJECT_ID`; add `--host https://eu.posthog.com` for an EU
  project. Run `--dry-run` first.
- **MCP** (`?readonly=true`): `--print-sql` prints every query; run each
  through the server's SQL tool, collect the rows as
  `{"<what>": <rows>, ...}` in a scratch JSON file, and `--from-results
  <file>` writes the same CSVs. Never type rows into a CSV by hand.
- **CLI**: `posthog-cli api` against the query endpoint with the printed
  SQL; run `posthog-cli api --agent-help` first.

The model is `data/ontology/naming.md` (channels, sources) and
`data/ontology/metrics.md` (sessions, classes, engaged). This file is how
PostHog computes it.

## Session-entry scope

Break down on the `sessions` table's entry fields only:
`$entry_utm_source`, `$entry_utm_medium`, `$entry_referring_domain`,
`$entry_current_url`, `$entry_pathname`. Never the per-event
`properties.$referring_domain`: under memory or cookieless persistence it
drifts from the session's real entry, and the same day reads two ways on
two tiles. Count unique sessions, so every session has one channel and one
source and the bars add up to the total.

Do not use PostHog's `$channel_type`. It files a newsletter click that
arrives with `utm_medium=newsletter` and no referrer as Direct and the same
click from a mail app as Email, and an answer-engine click that carries a
tag but no referrer as Referral.

## The channel expression

Evaluated top to bottom; the first match wins. Replace `example.com` with
the site's domain (`--domain` does it in the script). A team's own
newsletter or partner domains go into the matching arm; the arm order
stays.

```sql
multiIf(
    coalesce(s.$entry_referring_domain, '') = 'example.com' OR endsWith(coalesce(s.$entry_referring_domain, ''), '.example.com'), 'Direct',
    match(lower(coalesce(s.$entry_utm_medium, '')), '^(cpc|ppc|paid.*|.*cpm|retargeting|display|banner|affiliate)$')
        OR coalesce(s.$entry_gclid, '') != '' OR coalesce(s.$entry_msclkid, '') != '' OR coalesce(s.$entry_gad_source, '') != '', 'Paid',
    lower(coalesce(s.$entry_utm_medium, '')) IN ('newsletter', 'newsletters')
        OR match(lower(coalesce(s.$entry_utm_source, '')), '(beehiiv|substack)')
        OR match(coalesce(s.$entry_referring_domain, ''), '(^|[.])(beehiiv[.]com|substack[.]com)$'), 'Newsletter',
    lower(coalesce(s.$entry_utm_medium, '')) IN ('email', 'e-mail', 'e_mail', 'mail')
        OR coalesce(s.$entry_referring_domain, '') IN ('com.google.android.gm', 'mail.google.com', 'outlook.live.com', 'outlook.office.com', 'outlook.office365.com', 'mail.yahoo.com', 'com.microsoft.office.outlook'), 'Email',
    lower(coalesce(s.$entry_utm_medium, '')) = 'ai_assistant'
        OR lower(coalesce(s.$entry_utm_source, '')) IN ('chatgpt.com', 'chatgpt', 'openai', 'chat.openai.com', 'perplexity', 'perplexity.ai', 'claude.ai', 'claude', 'gemini.google.com', 'gemini', 'copilot.microsoft.com', 'copilot')
        OR match(coalesce(s.$entry_referring_domain, ''), '(^|[.])(chatgpt[.]com|openai[.]com|perplexity[.]ai|claude[.]ai|gemini[.]google[.]com|copilot[.]microsoft[.]com|you[.]com|phind[.]com|poe[.]com|grok[.]com|deepseek[.]com|mistral[.]ai)$'), 'AI Assistant',
    lower(coalesce(s.$entry_utm_medium, '')) = 'organic'
        OR (match(coalesce(s.$entry_referring_domain, ''), '(^|[.])google[.][a-z]{2,3}([.][a-z]{2})?$')
            AND coalesce(s.$entry_referring_domain, '') NOT IN ('docs.google.com', 'drive.google.com', 'sites.google.com', 'groups.google.com', 'calendar.google.com', 'meet.google.com', 'mail.google.com'))
        OR coalesce(s.$entry_referring_domain, '') = 'com.google.android.googlequicksearchbox'
        OR match(coalesce(s.$entry_referring_domain, ''), '(^|[.])(bing[.]com|duckduckgo[.]com|search[.]yahoo[.]com|ecosia[.]org|search[.]brave[.]com|baidu[.]com|yandex[.](ru|com)|startpage[.]com|qwant[.]com)$'), 'Organic Search',
    lower(coalesce(s.$entry_utm_medium, '')) IN ('social', 'influencer')
        OR match(coalesce(s.$entry_referring_domain, ''), '(^|[.])(linkedin[.]com|lnkd[.]in|t[.]co|twitter[.]com|x[.]com|facebook[.]com|messenger[.]com|instagram[.]com|reddit[.]com|news[.]ycombinator[.]com|youtube[.]com|threads[.]net|bsky[.]app|discord[.]com|slack[.]com)$')
        OR coalesce(s.$entry_referring_domain, '') IN ('com.linkedin.android', 'com.slack', 'com.twitter.android', 'com.reddit.frontpage', 'com.facebook.katana', 'statics.teams.cdn.office.net', 'web.telegram.org'), 'Social',
    coalesce(s.$entry_referring_domain, '') NOT IN ('', '$direct') OR coalesce(s.$entry_utm_source, '') != ''
        OR coalesce(extractURLParameter(s.$entry_current_url, 'ref'), '') != '', 'Referral',
    'Direct')
```

## The source expression

`utm_source`, else the referring domain (self-referrals dropped), else
`?ref=` on the entry URL (directory listings often send only that), else
`Direct`.

```sql
coalesce(
    nullIf(s.$entry_utm_source, ''),
    if(coalesce(s.$entry_referring_domain, '') = 'example.com' OR endsWith(coalesce(s.$entry_referring_domain, ''), '.example.com'),
       NULL, nullIf(nullIf(s.$entry_referring_domain, '$direct'), '')),
    nullIf(extractURLParameter(s.$entry_current_url, 'ref'), ''),
    'Direct')
```

## Session classes

posthog-js drops known crawler user agents, so what reaches PostHog from
an answer engine is its link fetcher running a stock browser: one
pageview, a second or less, no scroll, no click, a `utm_source` naming the
engine and no referrer (engines tag their outbound links and strip the
referrer). The session fragment (`SESSIONS_HOGQL` in
`scripts/web_snapshot.py`) classes every session:

| Class | Rule | Use |
| --- | --- | --- |
| `engine_fetch` | engine `utm_source` or `utm_medium=ai_assistant`, no referrer, under 5 s, no scroll, at most one pageview | the AEO leading indicator; counted per page and engine, never in a rate |
| `other_bot` | the same shape without a tag, no referrer or a search-engine one, under 2 s, no click | a count; a search engine's own fetcher lands here |
| `human` | everything else | the denominator of every rate |

`tracking-quality` watches the rule: engine fetches from one browser
across many countries is the fetcher signature; many browsers means the
rule is catching people, so retune the thresholds before trusting the
split. A `content_type` property the site stamps on every event wins over
the path rule (`CONTENT_TYPE_HOGQL`), which a team edits to its URL
structure.

## The weekly snapshots

Seven full days ending yesterday (UTC); `_28d` columns cover the 28 days
to the same day. Every query has an explicit `LIMIT` and reads at most 28
days. Each CSV starts `date_from,date_to`.

| `<what>` | Rows | Columns after the dates |
| --- | --- | --- |
| `traffic-by-source` | class x channel x source x medium, top 500 | `session_class,channel,source,medium,sessions,engaged_sessions,bounced,duration_p50,pageviews,cta_sessions,conversions` |
| `landing-pages` | human sessions by entry page, top 200 | `landing_page,content_type,sessions,engaged_sessions,bounced,duration_p50,pv_per_session,scroll_p50,cta_sessions,conversions` |
| `page-by-source` | human, entry page x channel x source, top 300 | `landing_page,content_type,channel,source,sessions_7d,sessions_28d,engaged_7d,engaged_28d,cta_sessions_28d,conversions_28d,duration_p50_28d` |
| `engine-fetches` | entry page x engine, where a fetch or a human AI-assistant session happened in 28 days | `landing_page,content_type,engine,fetches_7d,fetches_28d,untagged_fetches_7d,human_ai_7d,human_ai_28d,human_ai_engaged_7d,cta_sessions_7d` |
| `conversions` | CTA and conversion events in human sessions, by location, page, channel, source | `event,location,page_path,channel,source,events,sessions` |
| `site-funnel` | one row | `sessions_all,sessions_human,engine_fetch,other_bot,engaged,decision_view,cta,conversion,pageviews_human` |
| `tracking-quality` | one row | `pageviews_7d,pageleave_coverage,scroll_coverage,cta_events_7d,cta_attr_mismatch,cta_without_attr,exceptions_7d,rageclicks_7d,lcp_p75_ms,engine_fetch_7d,engine_fetch_browsers,engine_fetch_countries` |

`cta_sessions` and `conversions` count sessions with at least one such
event. A conversion recorded in another system reads 0 here and joins
through the forwarded parameters (`data/ontology/funnel.md`);
`cta_attr_mismatch` (the CTA's forwarded `utm_source` against the
session's entry source) must stay 0, and `cta_without_attr` is 0 once the
site forwards attribution. `pageleave_coverage` near 0 means time on page
and scroll are gone.

## Drill queries

A few per finding, each with an explicit `LIMIT` and a window of 90 days
or less, selecting from the session fragment so the channel and class
rules stay the same. Replays: human sessions only, and describe what the
person did, never who they are.

## Dashboards

When a finding needed a drill query, saving it as an insight makes it a
number next week. Every tile:

- uses session-entry scope and the channel expression above, verbatim;
- counts unique sessions and says "sessions", never "visitors";
- has no period in its title ("(30d)"): the dashboard's date filter
  overrides the insight's, so the title lies once someone changes it;
- selects human-only numbers from the session fragment with
  `cls = 'human'`;
- carries a description under 400 characters naming the rule it applies.

Name what an agent creates `analyst/<what it shows>`; never edit or delete
a tile, dashboard or subscription someone else made. The MCP stays
read-only unless the team lifts that for this.

## Monthly additions

Pages: `$pageview` by `pathname` with views, and engagement from
`$pageleave`. UTM campaigns: human sessions by `$entry_utm_source`,
`$entry_utm_medium`, `$entry_utm_campaign`, `$entry_utm_content`;
`conforms` and `reason` are computed against `data/ontology/naming.md`.

## Cost and limits

HogQL queries are free on the free tier and metered on paid plans; the
weekly run is seven. Without a `LIMIT` a result stops at 100 rows. Rate
limits are per key; the script retries a 429.

## Caveat to state

With cookieless or memory persistence the anonymous id resets on every
full page load: pageviews are exact, sessions directional, and a reload
mid-visit shows as a self-referral (counted Direct). Say it once under
Data caveats.

## Without the MCP or a key

Paste each query from `--print-sql` into a SQL insight, export it as CSV,
and save it as `data/analytics/snapshots/YYYY-MM-DD-posthog-<what>.csv`
with the columns above.
