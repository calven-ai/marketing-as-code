#!/usr/bin/env python3
"""Track Google ranks for every row of data/seo/keywords.csv: one live DataForSEO SERP per
keyword (top 30, AI Overview loaded), saved as data/seo/snapshots/YYYY-MM-DD-dataforseo-serp.csv
(our rank and URL, AI Overview shown and citing us, People Also Ask, who holds the top 10) and
...-dataforseo-serp-results.csv (every top-30 result, AI Overview reference, People Also Ask
question and related search). Location and language from data/ontology/metrics.md or flags;
--dry-run prints the keywords and the cost estimate, --max-usd refuses a bigger run. Needs
DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD. Standard library only.

    python3 scripts/seo_rank_track.py --dry-run
    python3 scripts/seo_rank_track.py
    python3 scripts/seo_rank_track.py --limit 3 --location "United Kingdom" --language en

Our domain is the `self` row of data/seo/brands.csv, or --domain. Brands label the top 10 when
that file exists. A run that would overwrite today's snapshot refuses before spending anything.
Score the snapshot with scripts/seo_diff.py; join it to the other sources with scripts/page_join.py.
"""
import argparse
import datetime as dt
import math
import sys
from concurrent.futures import ThreadPoolExecutor

import _seo
from _common import ROOT, snapshot_path

DEPTH = 30
# A depth-30 live SERP with the asynchronous AI Overview, measured at about $0.0055 to $0.0075.
USD_PER_SERP = 0.0075
ENDPOINT = "serp/google/organic/live/advanced"
SERP_COLUMNS = ["keyword_id", "keyword", "track", "tier", "target_url", "ok", "error", "rank",
                "url", "our_urls", "aio", "aio_cited", "aio_cited_paths", "featured_snippet",
                "paa", "top3_domains", "top10_domains", "top10_brands", "features",
                "location", "language", "checked"]
RESULT_COLUMNS = ["keyword_id", "kind", "position", "domain", "url", "title", "brand", "checked"]


def yn(value):
    return "yes" if value else "no"


def parse_serp(res, ours, brand_rows):
    """One DataForSEO SERP result -> (snapshot row fields, result rows).

    `rank` is our best organic rank_group (None outside the fetched depth); `aio_cited` whether
    an AI Overview references one of our pages."""
    items = res.get("items") or []
    organic = [i for i in items if i.get("type") == "organic"]

    def is_ours(url):
        host = _seo.domain_of(url or "")
        return any(_seo.same_site(host, d) for d in ours)

    mine = [i for i in organic if is_ours(i.get("url"))]
    best = min(mine, key=lambda i: i.get("rank_group") or 999) if mine else None
    aio_refs = []
    for i in items:
        if i.get("type") == "ai_overview":
            for ref in i.get("references") or []:
                if ref.get("url") and ref["url"] not in [r["url"] for r in aio_refs]:
                    aio_refs.append(ref)
    paa = [x.get("title") for i in items if i.get("type") == "people_also_ask"
           for x in i.get("items") or [] if x.get("title")]
    related = [x if isinstance(x, str) else (x or {}).get("title") for i in items
               if i.get("type") == "related_searches" for x in i.get("items") or []]
    related = [x for x in related if x]
    snippet = next((i for i in items if i.get("type") == "featured_snippet"), None)
    top10 = [i for i in organic if (i.get("rank_group") or 99) <= 10]
    top10_domains, top10_brands = [], []
    for i in top10:
        host = _seo.domain_of(i.get("url") or "")
        if host and host not in top10_domains:
            top10_domains.append(host)
        owner = _seo.brand_of(host, brand_rows)
        if owner and owner[1] != "self" and owner[0] not in top10_brands:
            top10_brands.append(owner[0])

    def label(url):
        owner = _seo.brand_of(_seo.domain_of(url or ""), brand_rows)
        return owner[0] if owner else ""

    row = {
        "rank": best.get("rank_group") if best else "",
        "url": _seo.path_of(best["url"]) if best else "",
        "our_urls": "|".join(sorted({_seo.path_of(i["url"]) for i in mine})),
        "aio": yn(any(i.get("type") == "ai_overview" for i in items)),
        "aio_cited": yn(any(is_ours(r["url"]) for r in aio_refs)),
        "aio_cited_paths": "|".join(sorted({_seo.path_of(r["url"]) for r in aio_refs if is_ours(r["url"])})),
        "featured_snippet": _seo.domain_of(snippet.get("url") or "") if snippet and snippet.get("url") else "",
        "paa": len(paa),
        "top3_domains": "|".join(_seo.domain_of(i.get("url") or "") for i in organic[:3]),
        "top10_domains": "|".join(top10_domains),
        "top10_brands": "|".join(top10_brands),
        "features": "|".join(sorted({i.get("type") for i in items if i.get("type") not in (None, "organic")})),
    }
    results = [{"kind": "organic", "position": i.get("rank_group"), "domain": _seo.domain_of(i.get("url") or ""),
                "url": i.get("url") or "", "title": i.get("title") or "", "brand": label(i.get("url"))}
               for i in organic[:DEPTH]]
    results += [{"kind": "ai_overview", "position": n, "domain": _seo.domain_of(r["url"]), "url": r["url"],
                 "title": r.get("title") or "", "brand": label(r["url"])} for n, r in enumerate(aio_refs[:20], 1)]
    results += [{"kind": "paa", "position": n, "title": q} for n, q in enumerate(paa[:10], 1)]
    results += [{"kind": "related", "position": n, "title": q} for n, q in enumerate(related[:10], 1)]
    return row, results


def fetch(keyword, place, ours, brand_rows, retry=True):
    """One keyword's SERP -> (row fields, result rows, cost). Errors are kept on the row."""
    from seo_snapshot import call  # the DataForSEO POST; reads the two keys, never prints them
    task_in = {"keyword": keyword["keyword"], "depth": DEPTH, "load_async_ai_overview": True, **place}
    try:
        body = call(ENDPOINT, [task_in])
    except SystemExit as err:
        return {"ok": "no", "error": str(err)[:200]}, [], 0.0
    cost = float(body.get("cost") or 0)
    task = (body.get("tasks") or [{}])[0]
    if task.get("status_code") != 20000 or not task.get("result"):
        if retry and task.get("status_code") == 40101:  # Google's transient error: one retry
            row, results, again = fetch(keyword, place, ours, brand_rows, retry=False)
            return row, results, cost + again
        return {"ok": "no", "error": f"{task.get('status_code')} {task.get('status_message')}"}, [], cost
    row, results = parse_serp(task["result"][0], ours, brand_rows)
    return {"ok": "yes", **row}, results, cost


def estimate(n):
    """The run's cost in dollars, rounded up to the cent."""
    return math.ceil(n * USD_PER_SERP * 100 - 1e-9) / 100


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--location", help="DataForSEO location name or code (else data/ontology/metrics.md)")
    ap.add_argument("--language", help="language code, e.g. en (else data/ontology/metrics.md)")
    ap.add_argument("--domain", help="our domain, when data/seo/brands.csv has no `self` row")
    ap.add_argument("--limit", type=int, help="only the first N keywords (a smoke test)")
    ap.add_argument("--max-usd", type=float, default=2.0, help="refuse a run estimated above this (default 2)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true", help="print keywords, market and estimate; no call")
    a = ap.parse_args(argv)

    rows = _seo.keywords()
    if not rows:
        sys.exit("data/seo/keywords.csv has no rows yet. Add the keywords the team cares about first.")
    rows = rows[: a.limit] if a.limit else rows
    place = _seo.market(a.location, a.language)
    brand_rows = _seo.brands()
    ours = _seo.self_domains(brand_rows, a.domain)
    if not ours:
        sys.exit("No domain of ours: add the `self` row to data/seo/brands.csv or pass --domain.")
    where = place.get("location_name") or place.get("location_code")
    est = estimate(len(rows))
    print(f"{len(rows)} keywords · {where} / {place['language_code']} · depth {DEPTH} · est ${est}")
    if a.dry_run:
        for r in rows:
            print(f"  {r['id']}  T{r.get('tier') or '?'}  {r.get('track') or '-'}  {r['keyword']}")
        return 0
    if est > a.max_usd:
        sys.exit(f"estimated ${est} exceeds --max-usd {a.max_usd}; trim the set or raise the cap")
    today = dt.date.today().isoformat()
    serp_path = snapshot_path("seo", "dataforseo", "serp", day=today)
    results_path = snapshot_path("seo", "dataforseo", "serp-results", day=today)
    if serp_path.exists():
        sys.exit(f"{serp_path.relative_to(ROOT)} exists; snapshots are immutable.")

    with ThreadPoolExecutor(max_workers=max(1, a.workers)) as pool:
        done = list(pool.map(lambda k: fetch(k, place, ours, brand_rows), rows))
    if all(row.get("ok") != "yes" for row, _, _ in done):
        sys.exit("every SERP call failed; nothing written: " + done[0][0].get("error", ""))
    out, details, cost = [], [], 0.0
    for k, (row, results, c) in zip(rows, done):
        cost += c
        base = {"keyword_id": k["id"], "keyword": k["keyword"], "track": k.get("track", ""),
                "tier": k.get("tier", ""), "target_url": k.get("target_url", ""),
                "location": where, "language": place["language_code"], "checked": today}
        out.append({**base, "error": "", **row})
        details += [{"keyword_id": k["id"], "checked": today, **r} for r in results]
    _seo.write_csv(serp_path, SERP_COLUMNS, out)
    _seo.write_csv(results_path, RESULT_COLUMNS, details)
    ok = [r for r in out if r["ok"] == "yes" and not _seo.branded(r)]
    top10 = sum(1 for r in ok if r["rank"] and int(r["rank"]) <= 10)
    errors = sum(1 for r in out if r["ok"] != "yes")
    print(f"saved {serp_path.relative_to(ROOT)} and {results_path.name}: non-branded top 10 on "
          f"{top10} of {len(ok)} · {errors} errors · {len(out)} calls, ${cost:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
