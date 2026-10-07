#!/usr/bin/env python3
"""Pull Google Search Console performance into data/seo/snapshots/: YYYY-MM-DD-gsc-pages.csv
(clicks, impressions, CTR and position per page, this period and the one before, plus Google's
index verdict with --inspect) and YYYY-MM-DD-gsc-queries.csv (query by page, this period).
Default period: the 28 days to yesterday. Needs GSC_CLIENT_ID, GSC_CLIENT_SECRET,
GSC_REFRESH_TOKEN and GSC_SITE_URL (environment or .env); --dry-run calls nothing. Free API.
Standard library only.

    python3 scripts/gsc_snapshot.py --dry-run
    python3 scripts/gsc_snapshot.py
    python3 scripts/gsc_snapshot.py --days 7 --inspect

GSC_SITE_URL is the property as Search Console names it: `sc-domain:example.com` or
`https://www.example.com/`. --inspect runs URL Inspection on every page data/seo/keywords.csv
or data/seo/prompts.csv targets (quota: 2,000 a day per property).

The refresh token is minted once by a person (integrations/catalog/seo-data.json, Google Search
Console, script route): a Google Cloud OAuth client with the Search Console API enabled, the
consent screen published to production (a token from an app left in testing expires after seven
days), then the OAuth 2.0 Playground with "use your own OAuth credentials", the scope
https://www.googleapis.com/auth/webmasters.readonly, signed in as someone who can read the
property, and "exchange authorization code for tokens". The four values go into .env.
"""
import argparse
import datetime as dt
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

import _seo
from _common import ROOT, setting, snapshot_path

TOKEN_URL = "https://oauth2.googleapis.com/token"
QUERY_URL = "https://www.googleapis.com/webmasters/v3/sites/{site}/searchAnalytics/query"
INSPECT_URL = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
ENV = ("GSC_CLIENT_ID", "GSC_CLIENT_SECRET", "GSC_REFRESH_TOKEN", "GSC_SITE_URL")
PAGE_COLUMNS = ["page", "clicks", "impressions", "ctr", "position", "prev_clicks",
                "prev_impressions", "prev_position", "index_verdict", "index_coverage",
                "google_canonical", "last_crawl", "date_from", "date_to"]
QUERY_COLUMNS = ["query", "page", "clicks", "impressions", "ctr", "position", "date_from", "date_to"]
PAGE_SIZE = 5000


class GscError(RuntimeError):
    pass


def post(url, data, headers):
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        # Google's error body names the problem (scope, property access); it never echoes a token.
        raise GscError(f"HTTP {err.code}: {err.read().decode('utf-8', 'replace')[:300]}") from None
    except urllib.error.URLError as err:
        raise GscError(f"network: {err.reason}") from None


def access_token(client_id, client_secret, refresh_token):
    body = urllib.parse.urlencode({"client_id": client_id, "client_secret": client_secret,
                                   "refresh_token": refresh_token, "grant_type": "refresh_token"}).encode()
    return post(TOKEN_URL, body, {"Content-Type": "application/x-www-form-urlencoded"})["access_token"]


def query(token, site, start, end, dims, max_rows):
    """Search Analytics rows for one period and dimension list, paged."""
    rows, url = [], QUERY_URL.format(site=urllib.parse.quote(site, safe=""))
    while len(rows) < max_rows:
        payload = {"startDate": start.isoformat(), "endDate": end.isoformat(), "dimensions": dims,
                   "dataState": "all", "rowLimit": min(PAGE_SIZE, max_rows - len(rows)), "startRow": len(rows)}
        got = post(url, json.dumps(payload).encode(),
                   {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}).get("rows", [])
        rows += got
        if len(got) < payload["rowLimit"]:
            break
    return rows


def origin(site):
    """https://host for a property: sc-domain:example.com -> https://example.com."""
    if site.startswith("sc-domain:"):
        return "https://" + site.split(":", 1)[1].strip("/")
    p = urllib.parse.urlparse(site)
    return f"{p.scheme}://{p.netloc}"


def metrics(row):
    return {"clicks": int(row.get("clicks", 0)), "impressions": int(row.get("impressions", 0)),
            "ctr": round(float(row.get("ctr", 0)), 4), "position": round(float(row.get("position", 0)), 1)}


def page_rows(cur, prev, index, start, end):
    """One row per page path: this period, the one before, the index verdict. Two URLs with one
    path (www, a trailing slash) are added up, position weighted by impressions."""
    pages = {}

    def add(rows, prefix):
        for r in rows:
            path = _seo.path_of(r["keys"][0])
            if not path:
                continue
            e = pages.setdefault(path, {"page": path})
            m = metrics(r)
            imp = e.get(prefix + "impressions", 0) + m["impressions"]
            if imp:
                e[prefix + "position"] = round((e.get(prefix + "position", 0) * e.get(prefix + "impressions", 0)
                                                + m["position"] * m["impressions"]) / imp, 1)
            e[prefix + "clicks"] = e.get(prefix + "clicks", 0) + m["clicks"]
            e[prefix + "impressions"] = imp

    add(cur, "")
    add(prev, "prev_")
    for path, res in (index or {}).items():
        pages.setdefault(path, {"page": path}).update(res)
    out = []
    for e in pages.values():
        e.setdefault("clicks", 0)
        e.setdefault("impressions", 0)
        e["ctr"] = round(e["clicks"] / e["impressions"], 4) if e["impressions"] else 0
        out.append({**e, "date_from": start.isoformat(), "date_to": end.isoformat()})
    out.sort(key=lambda e: (-e["clicks"], -e["impressions"], e["page"]))
    return out


def query_rows(rows, start, end):
    out = [{"query": r["keys"][0], "page": _seo.path_of(r["keys"][1]), **metrics(r),
            "date_from": start.isoformat(), "date_to": end.isoformat()} for r in rows]
    out.sort(key=lambda r: (-r["clicks"], -r["impressions"], r["query"], r["page"]))
    return out


def inspect(token, site, url):
    """URL Inspection: Google's own verdict on one page."""
    try:
        res = post(INSPECT_URL, json.dumps({"inspectionUrl": url, "siteUrl": site}).encode(),
                   {"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    except GscError as err:
        return {"index_verdict": "ERROR", "index_coverage": str(err)[:120]}
    s = (res.get("inspectionResult") or {}).get("indexStatusResult") or {}
    return {"index_verdict": s.get("verdict") or "", "index_coverage": s.get("coverageState") or "",
            "google_canonical": s.get("googleCanonical") or "", "last_crawl": (s.get("lastCrawlTime") or "")[:10]}


def targeted_pages():
    rows = [r.get("target_url") for r in _seo.read_csv(_seo.KEYWORDS)]
    rows += [r.get("target_page") for r in _seo.read_csv(_seo.PROMPTS) if r.get("status", "active") != "retired"]
    return sorted({_seo.path_of(p) for p in rows} - {""})


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--days", type=int, default=28, help="period length in days (default 28)")
    ap.add_argument("--end", type=dt.date.fromisoformat, help="last day, YYYY-MM-DD (default yesterday)")
    ap.add_argument("--inspect", action="store_true", help="URL Inspection for every targeted page")
    ap.add_argument("--max-rows", type=int, default=25000, help="query-by-page rows to keep (default 25000)")
    ap.add_argument("--dry-run", action="store_true", help="say what would be pulled; no call")
    a = ap.parse_args(argv)
    end = a.end or dt.date.today() - dt.timedelta(days=1)
    start = end - dt.timedelta(days=a.days - 1)
    prev_end, prev_start = start - dt.timedelta(days=1), start - dt.timedelta(days=a.days)
    pages = targeted_pages() if a.inspect else []
    print(f"Search Console {start} to {end} (previous {prev_start} to {prev_end})"
          + (f"; URL Inspection on {len(pages)} targeted pages" if a.inspect else ""))
    if a.dry_run:
        for p in pages:
            print(f"  inspect {p}")
        return 0
    creds = [setting(name) for name in ENV]
    missing = [name for name, value in zip(ENV, creds) if not value]
    if missing:
        sys.exit(f"{', '.join(missing)} not set; the script docstring says how to mint them. "
                 "By hand: Search Console > Performance > Export, dropped as "
                 "data/seo/snapshots/YYYY-MM-DD-gsc-<what>.csv.")
    today = dt.date.today().isoformat()
    pages_path = snapshot_path("seo", "gsc", "pages", day=today)
    queries_path = snapshot_path("seo", "gsc", "queries", day=today)
    if pages_path.exists():
        sys.exit(f"{pages_path.relative_to(ROOT)} exists; snapshots are immutable.")
    site = creds[3]
    try:
        token = access_token(*creds[:3])
        cur = query(token, site, start, end, ["page"], a.max_rows)
        prev = query(token, site, prev_start, prev_end, ["page"], a.max_rows)
        pairs = query(token, site, start, end, ["query", "page"], a.max_rows)
    except GscError as err:
        sys.exit(f"Search Console failed: {err}")
    index = {p: inspect(token, site, origin(site) + p) for p in pages}
    page_out = page_rows(cur, prev, index, start, end)
    _seo.write_csv(pages_path, PAGE_COLUMNS, page_out)
    _seo.write_csv(queries_path, QUERY_COLUMNS, query_rows(pairs, start, end))
    clicks = sum(r["clicks"] for r in page_out)
    print(f"saved {pages_path.relative_to(ROOT)} ({len(page_out)} pages, {clicks} clicks) and "
          f"{queries_path.name} ({len(pairs)} rows); {3 + len(pages)} calls, no cost")
    return 0


if __name__ == "__main__":
    sys.exit(main())
