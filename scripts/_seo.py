"""Shared helpers for the search scripts (seo_snapshot, seo_rank_track, seo_diff, page_join,
gsc_snapshot): the data/seo tables, the newest snapshot of a kind, page paths, brands and the
search market. Standard library only.

    from _seo import keywords, brands, latest, path_of, market

The tables' columns and the tiers and tracks are defined in data/seo/README.md.
"""

import csv
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from _common import DATA

SEO = DATA / "seo"
SNAPSHOTS = SEO / "snapshots"
ANALYTICS = DATA / "analytics" / "snapshots"
KEYWORDS = SEO / "keywords.csv"
PROMPTS = SEO / "prompts.csv"
BRANDS = SEO / "brands.csv"
METRICS = DATA / "ontology" / "metrics.md"
TIERS = {"1": "Buy", "2": "Problem", "3": "Authority"}
TRUE = {"yes", "true", "1"}


def read_csv(path):
    """Rows of a CSV as dicts, [] when the file is missing."""
    path = Path(path)
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path, columns, rows):
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def split(value):
    """A `|`-separated cell as a list, empty parts dropped."""
    return [x.strip() for x in (value or "").split("|") if x.strip()]


def flag(value):
    return str(value or "").strip().lower() in TRUE


def num(value, default=None):
    try:
        return float(value) if "." in str(value) else int(value)
    except (TypeError, ValueError):
        return default


def weight(tier):
    """What a won or lost keyword or prompt is worth: tier 1 = 3, 2 = 2, 3 = 1."""
    return {"1": 3, "2": 2}.get(str(tier), 1)


def branded(row):
    """Branded rows (the `brand` track) measure brand ownership and never enter the headline."""
    return (row.get("track") or "").strip() == "brand"


def path_of(url):
    """A page path from a URL or a path: no scheme, host, query or trailing slash; '' for junk."""
    url = (url or "").strip()
    if not url or url.startswith("("):
        return ""
    parsed = urlparse(url if "://" in url or url.startswith("/") else "https://" + url)
    path = parsed.path if (parsed.netloc or url.startswith("/")) else ""
    if not path and parsed.netloc:
        path = "/"
    return path.rstrip("/") or ("/" if path else "")


def domain_of(url):
    host = urlparse(url if "://" in (url or "") else "https://" + (url or "")).netloc.lower()
    host = host.split("@")[-1].split(":")[0]
    return host[4:] if host.startswith("www.") else host


def same_site(host, domain):
    return host == domain or host.endswith("." + domain)


def keywords(path=KEYWORDS):
    rows = read_csv(path)
    if rows and "id" not in rows[0]:
        sys.exit(f"{path} has no `id` column; data/seo/README.md has the header.")
    return rows


def prompts(path=PROMPTS):
    """The AEO prompt set, or None while prompts.csv has no `id` column (the crosswalk needs ids)."""
    rows = read_csv(path)
    if not rows or "id" not in rows[0]:
        return None
    return rows


def brands(path=BRANDS):
    """data/seo/brands.csv as [{brand, kind, aliases, domains}]; [] when the file is absent."""
    out = []
    for r in read_csv(path):
        out.append({"brand": r.get("brand", "").strip(), "kind": r.get("kind", "").strip(),
                    "aliases": split(r.get("aliases")),
                    "domains": [d.lower() for d in split(r.get("domains"))]})
    return out


def brand_of(host, brand_rows):
    """(brand, kind) owning a host, or None."""
    for b in brand_rows:
        if any(same_site(host, d) for d in b["domains"]):
            return b["brand"], b["kind"]
    return None


def self_domains(brand_rows, extra=None):
    found = [d for b in brand_rows if b["kind"] == "self" for d in b["domains"]]
    return [d.lower() for d in ([extra] if extra else []) + found]


def snapshots(suffix, folder=SNAPSHOTS, on_or_before=None):
    """Snapshots named YYYY-MM-DD-<source>-<suffix>.csv, oldest first."""
    rx = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+-" + re.escape(suffix) + r"\.csv$")
    files = sorted(p for p in Path(folder).glob("*.csv") if rx.match(p.name))
    if on_or_before:
        files = [p for p in files if p.name[:10] <= on_or_before]
    return files


def latest(suffix, folder=SNAPSHOTS, on_or_before=None):
    files = snapshots(suffix, folder, on_or_before)
    return files[-1] if files else None


def _ontology_value(text, term):
    m = re.search(r"^\|\s*" + re.escape(term) + r"\s*\|\s*([^|]*)\|", text, re.M | re.I)
    value = m.group(1).strip() if m else ""
    return "" if not value or "[" in value else value


def market(location=None, language=None, metrics=METRICS):
    """The DataForSEO location and language fields: the flags win, then the `Search location`
    and `Search language` rows of data/ontology/metrics.md. Never a default: exits when unset."""
    text = Path(metrics).read_text(encoding="utf-8") if Path(metrics).is_file() else ""
    location = (location or _ontology_value(text, "Search location")).strip()
    language = (language or _ontology_value(text, "Search language")).strip()
    if not location or not language:
        sys.exit("No search market: fill `Search location` and `Search language` in "
                 "data/ontology/metrics.md, or pass --location and --language.")
    key = "location_code" if location.isdigit() else "location_name"
    return {key: int(location) if location.isdigit() else location, "language_code": language}
