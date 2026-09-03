#!/usr/bin/env python3
"""Pull search volume and keyword difficulty for every row of
data/seo/keywords.csv from DataForSEO and save
data/seo/snapshots/YYYY-MM-DD-dataforseo-volume.csv. --update also refreshes
volume, difficulty and last_checked in the canonical table; --dry-run lists
what would be pulled. Needs DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD
(environment or .env). Standard library only.

    python3 scripts/seo_snapshot.py                 # snapshot only
    python3 scripts/seo_snapshot.py --update        # also refresh keywords.csv
    python3 scripts/seo_snapshot.py --dry-run       # show what would be pulled

Credentials come from DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD in the
environment or the repo's .env file. They are never printed. The snapshot
lands in data/seo/snapshots/YYYY-MM-DD-dataforseo-volume.csv with the columns
the seo-analyst skill expects: keyword,volume,difficulty,rank,url,checked.
Ranks are not pulled here (that needs a domain and a SERP check); the column
is kept so every snapshot in the folder stays diffable.
"""
import argparse
import base64
import csv
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request

from _common import ROOT as REPO, read_env_file, snapshot_path

API = "https://api.dataforseo.com/v3"
KEYWORDS = REPO / "data" / "seo" / "keywords.csv"
COLUMNS = ["keyword", "volume", "difficulty", "rank", "url", "checked"]


def load_env():
    """Fill os.environ from the repo .env for keys not already set."""
    for key, value in read_env_file().items():
        os.environ.setdefault(key, value)


def call(endpoint, payload):
    """POST one task list to a DataForSEO endpoint and return the JSON body."""
    login = os.environ.get("DATAFORSEO_LOGIN")
    password = os.environ.get("DATAFORSEO_PASSWORD")
    if not login or not password:
        sys.exit("DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD are not set. "
                 "See integrations/README.md.")
    token = base64.b64encode(f"{login}:{password}".encode()).decode()
    req = urllib.request.Request(
        f"{API}/{endpoint}",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Basic {token}",
                 "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.load(resp)
    except urllib.error.HTTPError as err:
        sys.exit(f"DataForSEO returned HTTP {err.code} for {endpoint}")
    if body.get("status_code") != 20000:
        sys.exit(f"DataForSEO error: {body.get('status_message')}")
    return body


def search_volume(keywords, location=2840, language="en"):
    """Monthly search volume per keyword, one call for the whole list."""
    task = {"keywords": keywords, "location_code": location,
            "language_code": language}
    body = call("keywords_data/google_ads/"
                "search_volume/live", [task])
    result = body["tasks"][0].get("result") or []
    return {row["keyword"]: row.get("search_volume")
            for row in result}


def keyword_difficulty(keywords, location=2840, language="en"):
    """Keyword difficulty (0 to 100) per keyword, one call."""
    task = {"keywords": keywords, "location_code": location,
            "language_code": language}
    body = call("dataforseo_labs/google/bulk_keyword_difficulty/live", [task])
    result = body["tasks"][0].get("result") or []
    items = result[0].get("items") if result else []
    return {row["keyword"]: row.get("keyword_difficulty") for row in items or []}


def read_keywords():
    with KEYWORDS.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        sys.exit(f"{KEYWORDS.relative_to(REPO)} has no rows yet. Add the "
                 "keywords the team cares about first.")
    return rows


def write_snapshot(rows, today):
    path = snapshot_path("seo", "dataforseo", "volume", day=today)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return path


def update_canonical(existing, by_keyword, today):
    """Refresh volume, difficulty, and last_checked on existing rows only."""
    for row in existing:
        fresh = by_keyword.get(row["keyword"])
        if not fresh:
            continue
        if fresh["volume"] not in (None, ""):
            row["volume"] = fresh["volume"]
        if fresh["difficulty"] not in (None, ""):
            row["difficulty"] = fresh["difficulty"]
        row["last_checked"] = today
    with KEYWORDS.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(existing[0].keys()))
        writer.writeheader()
        writer.writerows(existing)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--update", action="store_true",
                        help="also refresh volume, difficulty, last_checked in keywords.csv")
    parser.add_argument("--dry-run", action="store_true",
                        help="list the keywords and stop, no API call")
    parser.add_argument("--location", type=int, default=2840,
                        help="DataForSEO location code (default 2840, United States)")
    parser.add_argument("--language", default="en")
    args = parser.parse_args()

    load_env()
    existing = read_keywords()
    keywords = [row["keyword"] for row in existing]
    today = dt.date.today().isoformat()
    if args.dry_run:
        print(f"{len(keywords)} keywords would be pulled for location "
              f"{args.location}/{args.language}:")
        for kw in keywords:
            print(f"  {kw}")
        return

    volumes = search_volume(keywords, args.location, args.language)
    difficulty = keyword_difficulty(keywords, args.location, args.language)
    rows = []
    for row in existing:
        kw = row["keyword"]
        rows.append({
            "keyword": kw,
            "volume": volumes.get(kw, ""),
            "difficulty": difficulty.get(kw, ""),
            "rank": row.get("current_rank", ""),
            "url": row.get("target_url", ""),
            "checked": today,
        })
    path = write_snapshot(rows, today)
    print(f"saved {path.relative_to(REPO)} ({len(rows)} keywords)")
    if args.update:
        update_canonical(existing, {r["keyword"]: r for r in rows}, today)
        print(f"updated {KEYWORDS.relative_to(REPO)}")


if __name__ == "__main__":
    main()
