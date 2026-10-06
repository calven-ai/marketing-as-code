#!/usr/bin/env python3
"""Pull the weekly web snapshots from PostHog (one HogQL query each) into data/analytics/snapshots/YYYY-MM-DD-posthog-<what>.csv: traffic-by-source, landing-pages, page-by-source, engine-fetches, conversions, site-funnel, tracking-quality, with sessions classed human, engine_fetch or other_bot and channels per data/ontology/naming.md. --print-sql prints the queries for the MCP route, --from-results writes the CSVs from rows fetched there, --dry-run says what would run. Needs POSTHOG_API_KEY and POSTHOG_PROJECT_ID (environment or .env). Standard library only.

    python3 scripts/web_snapshot.py --domain example.com --dry-run
    python3 scripts/web_snapshot.py --domain example.com
    python3 scripts/web_snapshot.py --domain example.com --print-sql > queries.sql
    python3 scripts/web_snapshot.py --domain example.com --from-results rows.json

The window is the seven full days ending --end (default yesterday, UTC);
columns ending in _28d cover the 28 days ending the same day. Pass the event
names data/ontology/events.md defines: --cta-event for the click that hands
a visitor to the conversion, --conversion-event for the conversion itself
when the website records it (each repeatable). --domain is the site's own
domain, so links between its pages count as Direct, not as a referral.

--from-results takes a JSON object keyed by <what>, each value the rows a
query returned: a list of objects, or PostHog's {"columns": [...],
"results": [[...]]}. That is how a run through the PostHog MCP lands the
same files. Snapshots are immutable: an existing file is never overwritten.
The query model and the dashboard rules are
.agents/skills/web-analyst/references/posthog.md. The key is never printed.
"""
import argparse
import csv
import datetime as dt
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from _common import DATA, ROOT, setting

SNAPSHOTS = DATA / "analytics" / "snapshots"
SOURCE = "posthog"
DEFAULT_HOST = "https://us.posthog.com"
MAX_RETRIES = 4

# The generic lists behind the channel and class rules. Company domains never
# belong here: the team's own domain arrives through --domain.
ENGINE_SOURCES = ("chatgpt.com", "chatgpt", "openai", "chat.openai.com", "perplexity",
                  "perplexity.ai", "claude.ai", "claude", "gemini.google.com", "gemini",
                  "copilot.microsoft.com", "copilot")
ENGINE_REFERRERS = r"(^|[.])(chatgpt[.]com|openai[.]com|perplexity[.]ai|claude[.]ai|gemini[.]google[.]com|copilot[.]microsoft[.]com|you[.]com|phind[.]com|poe[.]com|grok[.]com|deepseek[.]com|mistral[.]ai)$"

# One expression for the channel, one for the source (data/ontology/naming.md).
# The reference carries the same text with example.com; a test keeps them equal.
CHANNEL_HOGQL = """multiIf(
    coalesce(s.$entry_referring_domain, '') = '{{domain}}' OR endsWith(coalesce(s.$entry_referring_domain, ''), '.{{domain}}'), 'Direct',
    match(lower(coalesce(s.$entry_utm_medium, '')), '^(cpc|ppc|paid.*|.*cpm|retargeting|display|banner|affiliate)$')
        OR coalesce(s.$entry_gclid, '') != '' OR coalesce(s.$entry_msclkid, '') != '' OR coalesce(s.$entry_gad_source, '') != '', 'Paid',
    lower(coalesce(s.$entry_utm_medium, '')) IN ('newsletter', 'newsletters')
        OR match(lower(coalesce(s.$entry_utm_source, '')), '(beehiiv|substack)')
        OR match(coalesce(s.$entry_referring_domain, ''), '(^|[.])(beehiiv[.]com|substack[.]com)$'), 'Newsletter',
    lower(coalesce(s.$entry_utm_medium, '')) IN ('email', 'e-mail', 'e_mail', 'mail')
        OR coalesce(s.$entry_referring_domain, '') IN ('com.google.android.gm', 'mail.google.com', 'outlook.live.com', 'outlook.office.com', 'outlook.office365.com', 'mail.yahoo.com', 'com.microsoft.office.outlook'), 'Email',
    lower(coalesce(s.$entry_utm_medium, '')) = 'ai_assistant'
        OR lower(coalesce(s.$entry_utm_source, '')) IN ({{engine_sources}})
        OR match(coalesce(s.$entry_referring_domain, ''), '{{engine_referrers}}'), 'AI Assistant',
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
    'Direct')"""

SOURCE_HOGQL = """coalesce(
    nullIf(s.$entry_utm_source, ''),
    if(coalesce(s.$entry_referring_domain, '') = '{{domain}}' OR endsWith(coalesce(s.$entry_referring_domain, ''), '.{{domain}}'),
       NULL, nullIf(nullIf(s.$entry_referring_domain, '$direct'), '')),
    nullIf(extractURLParameter(s.$entry_current_url, 'ref'), ''),
    'Direct')"""

# The path rule for sessions whose first pageview carries no content_type
# property. Edit it to the site's URL structure (or stamp content_type on
# every event and let this fall through).
CONTENT_TYPE_HOGQL = """multiIf(
    s.$entry_pathname = '/', 'home',
    s.$entry_pathname = '{{decision_path}}', 'pricing',
    match(s.$entry_pathname, '/(compare|comparisons|vs|alternatives?)(/|-|$)'), 'comparison',
    match(s.$entry_pathname, '^/templates?/'), 'template',
    match(s.$entry_pathname, '^/(blog|guides?|resources|learn|articles)/.+'), 'guide',
    match(s.$entry_pathname, '^/(product|platform|features?)(/|$)'), 'product',
    match(s.$entry_pathname, '^/(legal|privacy|terms)'), 'legal',
    'other')"""

# One row per session started in the 28 days ending {{end}}, with its class,
# channel, source, content type and engagement. Every query selects from it.
SESSIONS_HOGQL = """SELECT
    s.session_id AS sid,
    s.$start_timestamp >= toDateTime('{{end}}') - INTERVAL 6 DAY AS in_week,
    s.$entry_pathname AS landing_page,
    coalesce(nullIf(s.$entry_referring_domain, ''), '$direct') AS ref_domain,
    nullIf(s.$entry_utm_source, '') AS utm_source,
    nullIf(s.$entry_utm_medium, '') AS utm_medium,
    toFloat(s.$session_duration) AS duration,
    toInt(s.$pageview_count) AS pageviews,
    s.$is_bounce AS bounced,
    f.browser AS browser,
    f.country AS country,
    ifNull(f.max_scroll, 0) AS max_scroll,
    ifNull(f.scroll_known, 0) AS scroll_known,
    ifNull(f.clicks, 0) AS clicks,
    ifNull(f.cta, 0) AS cta,
    ifNull(f.conversions, 0) AS conversions,
    ifNull(f.decision_views, 0) AS decision_views,
    multiIf(
        (lower(coalesce(utm_source, '')) IN ({{engine_sources}}) OR lower(coalesce(utm_medium, '')) = 'ai_assistant')
            AND ref_domain = '$direct' AND duration < 5 AND max_scroll = 0 AND pageviews <= 1, 'engine_fetch',
        duration < 2 AND max_scroll = 0 AND pageviews <= 1 AND clicks = 0 AND utm_source IS NULL
            AND (ref_domain = '$direct' OR match(ref_domain, '(^|[.])(google[.][a-z.]+|bing[.]com|duckduckgo[.]com|yandex[.][a-z]+|baidu[.]com)$')), 'other_bot',
        'human') AS cls,
    {{channel}} AS channel,
    {{source}} AS source,
    coalesce(f.ctype_ev, {{content_type}}) AS content_type,
    duration >= 30 OR pageviews >= 2 OR max_scroll >= 0.5 AS engaged
FROM sessions AS s
LEFT JOIN (
    SELECT
        $session_id AS sid,
        argMinIf(toString(properties.content_type), timestamp, event = '$pageview' AND properties.content_type IS NOT NULL) AS ctype_ev,
        argMinIf(toString(properties.$browser), timestamp, event = '$pageview') AS browser,
        argMinIf(toString(properties.$geoip_country_code), timestamp, event = '$pageview') AS country,
        max(ifNull(toFloat(properties.$prev_pageview_max_scroll_percentage), 0)) AS max_scroll,
        toInt(countIf(properties.$prev_pageview_max_scroll_percentage IS NOT NULL) > 0) AS scroll_known,
        countIf(event = '$autocapture') AS clicks,
        countIf(event IN ({{cta_events}})) AS cta,
        countIf(event IN ({{conversion_events}})) AS conversions,
        countIf(event = '$pageview' AND properties.$pathname = '{{decision_path}}') AS decision_views
    FROM events
    WHERE event IN ('$pageview', '$pageleave', '$autocapture', {{cta_events}}, {{conversion_events}})
      AND timestamp >= toDateTime('{{end}}') - INTERVAL 27 DAY
      AND timestamp < toDateTime('{{end}}') + INTERVAL 1 DAY
      AND $session_id IS NOT NULL
    GROUP BY sid
) AS f ON f.sid = s.session_id
WHERE s.$start_timestamp >= toDateTime('{{end}}') - INTERVAL 27 DAY
  AND s.$start_timestamp < toDateTime('{{end}}') + INTERVAL 1 DAY"""

QUERIES = {
    "traffic-by-source": """SELECT
    cls AS session_class, channel, source, utm_medium AS medium,
    toInt(count()) AS sessions,
    toInt(countIf(engaged)) AS engaged_sessions,
    toInt(countIf(bounced)) AS bounced,
    round(quantile(0.5)(duration), 1) AS duration_p50,
    toInt(sum(pageviews)) AS pageviews,
    toInt(countIf(cta > 0)) AS cta_sessions,
    toInt(countIf(conversions > 0)) AS conversions
FROM ({{sessions}})
WHERE in_week
GROUP BY session_class, channel, source, medium
ORDER BY session_class, sessions DESC, channel, source
LIMIT 500""",
    "landing-pages": """SELECT
    landing_page, content_type,
    toInt(count()) AS sessions,
    toInt(countIf(engaged)) AS engaged_sessions,
    toInt(countIf(bounced)) AS bounced,
    round(quantile(0.5)(duration), 1) AS duration_p50,
    round(sum(pageviews) / count(), 2) AS pv_per_session,
    round(quantileIf(0.5)(max_scroll, scroll_known = 1), 2) AS scroll_p50,
    toInt(countIf(cta > 0)) AS cta_sessions,
    toInt(countIf(conversions > 0)) AS conversions
FROM ({{sessions}})
WHERE in_week AND cls = 'human'
GROUP BY landing_page, content_type
ORDER BY sessions DESC, landing_page
LIMIT 200""",
    "page-by-source": """SELECT
    landing_page, content_type, channel, source,
    toInt(countIf(in_week)) AS sessions_7d,
    toInt(count()) AS sessions_28d,
    toInt(countIf(in_week AND engaged)) AS engaged_7d,
    toInt(countIf(engaged)) AS engaged_28d,
    toInt(countIf(cta > 0)) AS cta_sessions_28d,
    toInt(countIf(conversions > 0)) AS conversions_28d,
    round(quantile(0.5)(duration), 1) AS duration_p50_28d
FROM ({{sessions}})
WHERE cls = 'human'
GROUP BY landing_page, content_type, channel, source
ORDER BY sessions_28d DESC, sessions_7d DESC, landing_page
LIMIT 300""",
    "engine-fetches": """SELECT
    landing_page, content_type,
    coalesce(utm_source, ref_domain) AS engine,
    toInt(countIf(cls = 'engine_fetch' AND in_week)) AS fetches_7d,
    toInt(countIf(cls = 'engine_fetch')) AS fetches_28d,
    toInt(countIf(cls = 'other_bot' AND in_week)) AS untagged_fetches_7d,
    toInt(countIf(cls = 'human' AND channel = 'AI Assistant' AND in_week)) AS human_ai_7d,
    toInt(countIf(cls = 'human' AND channel = 'AI Assistant')) AS human_ai_28d,
    toInt(countIf(cls = 'human' AND channel = 'AI Assistant' AND in_week AND engaged)) AS human_ai_engaged_7d,
    toInt(countIf(cls = 'human' AND in_week AND cta > 0)) AS cta_sessions_7d
FROM ({{sessions}})
GROUP BY landing_page, content_type, engine
HAVING fetches_28d + untagged_fetches_7d + human_ai_28d > 0
ORDER BY fetches_7d DESC, human_ai_7d DESC, fetches_28d DESC, landing_page
LIMIT 300""",
    "conversions": """SELECT
    e.event AS event,
    toString(e.properties.location) AS location,
    e.properties.$pathname AS page_path,
    x.channel AS channel,
    x.source AS source,
    toInt(count()) AS events,
    toInt(uniq(e.$session_id)) AS sessions
FROM events AS e
JOIN ({{sessions}}) AS x ON x.sid = e.$session_id
WHERE e.event IN ({{cta_events}}, {{conversion_events}})
  AND e.timestamp >= toDateTime('{{end}}') - INTERVAL 6 DAY
  AND e.timestamp < toDateTime('{{end}}') + INTERVAL 1 DAY
  AND x.cls = 'human'
GROUP BY event, location, page_path, channel, source
ORDER BY event, events DESC, location
LIMIT 500""",
    "site-funnel": """SELECT
    toInt(count()) AS sessions_all,
    toInt(countIf(cls = 'human')) AS sessions_human,
    toInt(countIf(cls = 'engine_fetch')) AS engine_fetch,
    toInt(countIf(cls = 'other_bot')) AS other_bot,
    toInt(countIf(cls = 'human' AND engaged)) AS engaged,
    toInt(countIf(cls = 'human' AND decision_views > 0)) AS decision_view,
    toInt(countIf(cls = 'human' AND cta > 0)) AS cta,
    toInt(countIf(cls = 'human' AND conversions > 0)) AS conversion,
    toInt(sumIf(pageviews, cls = 'human')) AS pageviews_human
FROM ({{sessions}})
WHERE in_week
LIMIT 1""",
    "tracking-quality": """SELECT
    ev.pageviews_7d AS pageviews_7d,
    if(ev.pageviews_7d = 0, NULL, round(ev.pageleaves_7d / ev.pageviews_7d, 4)) AS pageleave_coverage,
    if(ev.pageviews_7d = 0, NULL, round(ev.with_prev_7d / ev.pageviews_7d, 4)) AS scroll_coverage,
    ev.cta_events_7d AS cta_events_7d,
    ev.cta_attr_mismatch AS cta_attr_mismatch,
    ev.cta_without_attr AS cta_without_attr,
    ev.exceptions_7d AS exceptions_7d,
    ev.rageclicks_7d AS rageclicks_7d,
    ev.lcp_p75_ms AS lcp_p75_ms,
    fx.engine_fetch_7d AS engine_fetch_7d,
    fx.engine_fetch_browsers AS engine_fetch_browsers,
    fx.engine_fetch_countries AS engine_fetch_countries
FROM (
    SELECT
        toInt(countIf(event = '$pageview')) AS pageviews_7d,
        toInt(countIf(event = '$pageleave')) AS pageleaves_7d,
        toInt(countIf(event = '$pageview' AND properties.$prev_pageview_pathname IS NOT NULL)) AS with_prev_7d,
        toInt(countIf(event IN ({{cta_events}}))) AS cta_events_7d,
        toInt(countIf(event IN ({{cta_events}}) AND properties.utm_source IS NOT NULL
                      AND session.$entry_utm_source IS NOT NULL AND session.$entry_utm_source != ''
                      AND toString(properties.utm_source) != session.$entry_utm_source)) AS cta_attr_mismatch,
        toInt(countIf(event IN ({{cta_events}}) AND properties.utm_source IS NULL)) AS cta_without_attr,
        toInt(countIf(event = '$exception')) AS exceptions_7d,
        toInt(countIf(event = '$rageclick')) AS rageclicks_7d,
        round(quantileIf(0.75)(toFloat(properties.$web_vitals_LCP_value),
                               event = '$web_vitals' AND properties.$web_vitals_LCP_value IS NOT NULL)) AS lcp_p75_ms
    FROM events
    WHERE event IN ('$pageview', '$pageleave', '$exception', '$rageclick', '$web_vitals', {{cta_events}})
      AND timestamp >= toDateTime('{{end}}') - INTERVAL 6 DAY
      AND timestamp < toDateTime('{{end}}') + INTERVAL 1 DAY
) AS ev
CROSS JOIN (
    SELECT
        toInt(countIf(cls = 'engine_fetch')) AS engine_fetch_7d,
        toInt(uniqIf(browser, cls = 'engine_fetch')) AS engine_fetch_browsers,
        toInt(uniqIf(country, cls = 'engine_fetch')) AS engine_fetch_countries
    FROM ({{sessions}})
    WHERE in_week
) AS fx
LIMIT 1""",
}

# The CSV columns per snapshot, after date_from and date_to. The query's
# aliases must match them; --from-results is checked against them.
COLUMNS = {
    "traffic-by-source": ["session_class", "channel", "source", "medium", "sessions", "engaged_sessions",
                          "bounced", "duration_p50", "pageviews", "cta_sessions", "conversions"],
    "landing-pages": ["landing_page", "content_type", "sessions", "engaged_sessions", "bounced",
                      "duration_p50", "pv_per_session", "scroll_p50", "cta_sessions", "conversions"],
    "page-by-source": ["landing_page", "content_type", "channel", "source", "sessions_7d", "sessions_28d",
                       "engaged_7d", "engaged_28d", "cta_sessions_28d", "conversions_28d", "duration_p50_28d"],
    "engine-fetches": ["landing_page", "content_type", "engine", "fetches_7d", "fetches_28d",
                       "untagged_fetches_7d", "human_ai_7d", "human_ai_28d", "human_ai_engaged_7d",
                       "cta_sessions_7d"],
    "conversions": ["event", "location", "page_path", "channel", "source", "events", "sessions"],
    "site-funnel": ["sessions_all", "sessions_human", "engine_fetch", "other_bot", "engaged",
                    "decision_view", "cta", "conversion", "pageviews_human"],
    "tracking-quality": ["pageviews_7d", "pageleave_coverage", "scroll_coverage", "cta_events_7d",
                         "cta_attr_mismatch", "cta_without_attr", "exceptions_7d", "rageclicks_7d",
                         "lcp_p75_ms", "engine_fetch_7d", "engine_fetch_browsers", "engine_fetch_countries"],
}

DOMAIN_RE = re.compile(r"^(?=.{4,253}$)([a-z0-9-]+\.)+[a-z]{2,}$")
EVENT_RE = re.compile(r"^[A-Za-z0-9_$:. -]{1,100}$")
PATH_RE = re.compile(r"^/[A-Za-z0-9/_.-]{0,200}$")


def quoted(values):
    return ", ".join(f"'{v}'" for v in values)


def build_queries(end, domain, cta_events, conversion_events, decision_path="/pricing"):
    """{what: HogQL} with every placeholder filled. Arguments are validated
    first, because they are pasted into SQL."""
    if not DOMAIN_RE.match(domain or ""):
        sys.exit(f"--domain {domain!r} is not a bare domain like example.com")
    for name in [*cta_events, *conversion_events]:
        if not EVENT_RE.match(name):
            sys.exit(f"event name {name!r} has characters an event name never has")
    if not cta_events or not conversion_events:
        sys.exit("give at least one --cta-event and one --conversion-event (data/ontology/events.md)")
    if not PATH_RE.match(decision_path):
        sys.exit(f"--decision-path {decision_path!r} is not a site path like /pricing")
    end = dt.date.fromisoformat(str(end)).isoformat()

    def fill(sql):
        return (sql.replace("{{sessions}}", SESSIONS_HOGQL)
                   .replace("{{channel}}", CHANNEL_HOGQL)
                   .replace("{{source}}", SOURCE_HOGQL)
                   .replace("{{content_type}}", CONTENT_TYPE_HOGQL)
                   .replace("{{engine_sources}}", quoted(ENGINE_SOURCES))
                   .replace("{{engine_referrers}}", ENGINE_REFERRERS)
                   .replace("{{cta_events}}", quoted(cta_events))
                   .replace("{{conversion_events}}", quoted(conversion_events))
                   .replace("{{decision_path}}", decision_path)
                   .replace("{{domain}}", domain)
                   .replace("{{end}}", end))
    return {what: fill(sql) for what, sql in QUERIES.items()}


def window(end):
    end = dt.date.fromisoformat(str(end))
    return (end - dt.timedelta(days=6)).isoformat(), end.isoformat()


def normalise(payload):
    """Rows as a list of dicts, from a list of dicts or PostHog's {columns, results}."""
    if isinstance(payload, dict) and "results" in payload:
        cols = payload.get("columns") or []
        return [dict(zip(cols, row)) for row in payload.get("results") or []]
    if isinstance(payload, list) and all(isinstance(r, dict) for r in payload):
        return payload
    sys.exit("each result must be a list of objects or {\"columns\": [...], \"results\": [[...]]}")


def snapshot_file(what, day, folder=None):
    return Path(folder or SNAPSHOTS) / f"{day}-{SOURCE}-{what}.csv"


def write_snapshot(what, rows, end, day, folder=None):
    """Write one CSV: date_from, date_to, then COLUMNS[what] in order. Refuses
    to overwrite, and refuses rows missing a column."""
    path = snapshot_file(what, day, folder)
    if path.exists():
        sys.exit(f"{path.name} exists; "
                 "snapshots are immutable, so pull again tomorrow or delete the file you just made")
    cols = COLUMNS[what]
    for row in rows:
        missing = [c for c in cols if c not in row]
        if missing:
            sys.exit(f"{what}: rows lack {', '.join(missing)}; was the query edited?")
    date_from, date_to = window(end)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["date_from", "date_to", *cols])
        for row in rows:
            writer.writerow([date_from, date_to, *("" if row[c] is None else row[c] for c in cols)])
    return path


def run_query(sql, host, project, key):
    """POST one HogQL query to /api/projects/<id>/query/; rows as dicts. Retries on 429."""
    url = f"{host.rstrip('/')}/api/projects/{project}/query/"
    body = json.dumps({"query": {"kind": "HogQLQuery", "query": sql}}).encode()
    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(url, data=body, method="POST", headers={
            "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                payload = json.loads(resp.read())
            break
        except urllib.error.HTTPError as err:
            if err.code == 429 and attempt < MAX_RETRIES - 1:
                time.sleep(float(err.headers.get("Retry-After") or 2 ** (attempt + 2)))
                continue
            detail = err.read().decode("utf-8", "replace")[:400]
            raise RuntimeError(f"HTTP {err.code}: {detail}") from None
        except urllib.error.URLError as err:
            raise RuntimeError(f"network error: {err.reason}") from None
    if payload.get("error"):
        raise RuntimeError(str(payload["error"]))
    return normalise(payload)


def yesterday_utc():
    return dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=1)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--domain", required=True, help="the site's own domain, e.g. example.com")
    ap.add_argument("--end", default=None, help="last full day of the window, YYYY-MM-DD (default yesterday, UTC)")
    ap.add_argument("--cta-event", action="append", dest="cta_events",
                    help="the click that hands a visitor on to the conversion (repeatable; default cta_clicked)")
    ap.add_argument("--conversion-event", action="append", dest="conversion_events",
                    help="the conversion event as data/ontology/events.md names it (repeatable; default signup_completed)")
    ap.add_argument("--decision-path", default="/pricing", help="the page where the decision is made (default /pricing)")
    ap.add_argument("--only", choices=sorted(QUERIES), help="one snapshot only")
    ap.add_argument("--host", default=DEFAULT_HOST, help="PostHog host (EU: https://eu.posthog.com)")
    ap.add_argument("--print-sql", action="store_true", help="print the queries and stop; no network, no key")
    ap.add_argument("--from-results", metavar="JSON", help="write the CSVs from rows fetched elsewhere (the MCP route)")
    ap.add_argument("--dry-run", action="store_true", help="say what would run and be written; no network")
    args = ap.parse_args(argv)

    end = dt.date.fromisoformat(args.end) if args.end else yesterday_utc()
    if end >= dt.datetime.now(dt.timezone.utc).date():
        sys.exit(f"--end {end} is not a complete day yet (UTC); use yesterday or earlier")
    queries = build_queries(end, args.domain, args.cta_events or ["cta_clicked"],
                            args.conversion_events or ["signup_completed"], args.decision_path)
    if args.only:
        queries = {args.only: queries[args.only]}
    day = dt.date.today().isoformat()
    date_from, date_to = window(end)

    if args.print_sql:
        print(f"-- window: {date_from} to {date_to} (columns ending _28d: the 28 days to {date_to})")
        for what, sql in queries.items():
            print(f"-- ===== {what} -> {snapshot_file(what, day).relative_to(ROOT)} =====")
            print(sql.rstrip() + ";\n")
        return 0

    if args.from_results:
        try:
            results = json.loads(Path(args.from_results).read_text(encoding="utf-8"))
        except (OSError, ValueError) as err:
            sys.exit(f"cannot read {args.from_results}: {err}")
        unknown = sorted(set(results) - set(COLUMNS))
        if unknown:
            sys.exit(f"unknown snapshot names in {args.from_results}: {', '.join(unknown)}")
        for what in [w for w in queries if w in results]:
            path = write_snapshot(what, normalise(results[what]), end, day)
            print(f"saved {path.relative_to(ROOT)}")
        return 0

    project, key = setting("POSTHOG_PROJECT_ID"), setting("POSTHOG_API_KEY")
    if args.dry_run:
        print(f"window {date_from} to {date_to}, project id {'set' if project else 'MISSING'}, "
              f"key {'set' if key else 'MISSING'}, {len(queries)} queries against {args.host}:")
        for what in queries:
            print(f"  {what} -> {snapshot_file(what, day).relative_to(ROOT)}")
        return 0
    if not project or not key:
        sys.exit("POSTHOG_API_KEY and POSTHOG_PROJECT_ID are not set (environment or .env). "
                 "See integrations/catalog/web-analytics.json and docs/secrets.md.")
    for i, (what, sql) in enumerate(queries.items()):
        if i:
            time.sleep(1)
        try:
            rows = run_query(sql, args.host, project, key)
        except RuntimeError as err:
            sys.exit(f"[{what}] query failed: {err}")
        path = write_snapshot(what, rows, end, day)
        print(f"saved {path.relative_to(ROOT)} ({len(rows)} rows)")
    print(f"{len(queries)} queries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
