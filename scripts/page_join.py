#!/usr/bin/env python3
"""One row per page path joining the newest snapshot of every search source: Google ranks
(scripts/seo_rank_track.py), AI answer citations (the AEO results snapshot), Search Console
(scripts/gsc_snapshot.py) and landing-page sessions (data/analytics/snapshots/*-landing-pages.csv).
Prints a table, --csv or --json; --on YYYY-MM-DD reads the newest snapshots on or before a date.
Every search role reads this instead of joining by hand. No network.

    python3 scripts/page_join.py
    python3 scripts/page_join.py --csv > /tmp/pages.csv
    python3 scripts/page_join.py --page /pricing

Columns: keywords targeting the page (data/seo/keywords.csv `target_url`), keywords it ranks
for and its best rank, keywords ranking it in the top 10, keywords whose AI Overview cites it;
Search Console clicks, impressions, CTR, position and index verdict; AEO prompts targeting it
(data/seo/prompts.csv `target_page`) and non-branded answers citing it (`cited_self` rows of the
AEO results, their `cited_paths`); sessions, engaged sessions and conversions. A source with no
snapshot is named on the first line and its columns stay empty; nothing is recomputed.
"""
import argparse
import collections
import csv
import json
import sys

import _seo

COLUMNS = ["page", "keywords", "ranks_with", "best_rank", "top10", "aio_cited",
           "gsc_clicks", "gsc_impressions", "gsc_ctr", "gsc_position", "index",
           "aeo_prompts", "aeo_cited", "sessions", "engaged_sessions", "conversions"]


def sources(on=None):
    """The newest snapshot path of each source on or before `on` (None when there is none)."""
    return {"serp": _seo.latest("serp", on_or_before=on),
            "aeo": _seo.latest("aeo-results", on_or_before=on),
            "gsc": _seo.latest("gsc-pages", on_or_before=on),
            "web": _seo.latest("landing-pages", folder=_seo.ANALYTICS, on_or_before=on)}


def join(serp=(), keywords=(), aeo=(), prompts=(), gsc=(), web=()):
    """page path -> one entry with every source's numbers for it. Rows are snapshot dicts."""
    pages = collections.defaultdict(lambda: {"keywords": [], "ranks_with": [], "best_rank": None,
                                             "top10": [], "aio_cited": [], "aeo_prompts": [],
                                             "aeo_cited": 0})
    for k in keywords:
        p = _seo.path_of(k.get("target_url"))
        if p:
            pages[p]["keywords"].append(k["id"])
    for r in serp:
        if not _seo.flag(r.get("ok")):
            continue
        rank, p = _seo.num(r.get("rank")), _seo.path_of(r.get("url"))
        if rank and p:
            e = pages[p]
            e["ranks_with"].append(r["keyword_id"])
            e["best_rank"] = rank if e["best_rank"] is None else min(e["best_rank"], rank)
            if rank <= 10:
                e["top10"].append(r["keyword_id"])
        for c in _seo.split(r.get("aio_cited_paths")):
            pages[_seo.path_of(c)]["aio_cited"].append(r["keyword_id"])
    by_id = {p.get("id"): p for p in prompts or []}
    for p in prompts or []:
        page = _seo.path_of(p.get("target_page"))
        if page and p.get("status", "active") != "retired":
            pages[page]["aeo_prompts"].append(p["id"])
    for a in aeo:
        if not (_seo.flag(a.get("answered", "yes")) and _seo.flag(a.get("cited_self"))):
            continue
        if (by_id.get(a.get("prompt_id")) or {}).get("intent") == "branded":
            continue
        for c in set(_seo.path_of(x) for x in _seo.split(a.get("cited_paths"))):
            if c:
                pages[c]["aeo_cited"] += 1
    for g in gsc:
        p = _seo.path_of(g.get("page"))
        if p:
            e = pages[p]
            e["gsc_clicks"] = _seo.num(g.get("clicks"), 0)
            e["gsc_impressions"] = _seo.num(g.get("impressions"), 0)
            e["gsc_ctr"] = g.get("ctr", "")
            e["gsc_position"] = g.get("position", "")
            e["index"] = g.get("index_verdict", "")
    for w in web:
        p = _seo.path_of(w.get("landing_page"))
        if p:
            e = pages[p]
            for col in ("sessions", "engaged_sessions", "conversions"):
                e[col] = e.get(col, 0) + (_seo.num(w.get(col), 0) or 0)
    return dict(sorted(pages.items()))


def load(on=None):
    """(the join, the source paths) from the newest snapshots."""
    src = sources(on)
    read = {k: _seo.read_csv(p) if p else [] for k, p in src.items()}
    joined = join(read["serp"], _seo.keywords(), read["aeo"], _seo.prompts() or [], read["gsc"], read["web"])
    return joined, src


def flat(page, e):
    row = {"page": page}
    for col in COLUMNS[1:]:
        v = e.get(col, "")
        row[col] = "|".join(v) if isinstance(v, list) else ("" if v is None else v)
    return row


def table(rows):
    widths = {c: max(len(c), *(len(str(r[c])) for r in rows)) for c in COLUMNS} if rows else {}
    out = ["  ".join(c.ljust(widths[c]) for c in COLUMNS)] if rows else []
    for r in rows:
        out.append("  ".join(str(r[c]).ljust(widths[c]) for c in COLUMNS))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--on", help="newest snapshots on or before YYYY-MM-DD")
    ap.add_argument("--page", help="only this page path")
    fmt = ap.add_mutually_exclusive_group()
    fmt.add_argument("--csv", action="store_true")
    fmt.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    joined, src = load(a.on)
    if a.page:
        joined = {p: e for p, e in joined.items() if p == _seo.path_of(a.page)}
    rows = [flat(p, e) for p, e in joined.items()]
    names = {k: (p.name if p else None) for k, p in src.items()}
    if a.json:
        print(json.dumps({"sources": names, "pages": joined}, indent=2))
        return 0
    if a.csv:
        writer = csv.DictWriter(sys.stdout, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
        return 0
    print("sources: " + " · ".join(f"{k} {v or 'none'}" for k, v in names.items()))
    print(table(rows) if rows else "no pages: no snapshot names a page yet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
