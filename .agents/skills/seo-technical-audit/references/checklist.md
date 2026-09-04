<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/seo-audit/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Technical and on-page audit checklist

Condensed from the checklists in coreyhaines31/marketingskills `seo-audit`.
Walk it in this order; earlier sections block later ones.

## Priority order

1. Crawlability and indexation: can the engine find and index it?
2. Technical foundations: is it fast and functional?
3. On-page: is each page optimised for one target?
4. Content quality: does it deserve to rank?
5. Authority: does it have links and mentions? (`backlink-analysis`)

## 1. Crawlability

- `robots.txt`: no unintended blocks, important paths allowed, sitemap
  line present.
- XML sitemap: exists, reachable, only canonical indexable URLs, updated
  when pages change, valid format; index files under 50,000 URLs each.
- Architecture: key pages within three clicks of the homepage, a logical
  hierarchy, no orphan pages.
- Crawl budget (large sites): parameter URLs controlled, faceted
  navigation handled, infinite scroll has a paginated fallback, no
  session ids in URLs.

## 2. Indexation

- Compare indexed count (site: search, Search Console coverage) with the
  expected count.
- Noindex on important pages; canonicals pointing the wrong way;
  redirect chains and loops; soft 404s; duplicates without canonicals.
- Canonicalisation: every page has one, self-referencing on unique pages,
  http to https, one host (www or not), one trailing-slash rule.

## 3. Speed and Core Web Vitals

| Metric | Good | Needs work |
| --- | --- | --- |
| LCP | under 2.5 s | over 4 s is poor |
| INP | under 200 ms | over 500 ms is poor |
| CLS | under 0.1 | over 0.25 is poor |

Look at server response time, image sizing and format, JavaScript
execution, CSS delivery, caching headers, CDN, font loading. Lab numbers
(Lighthouse) and field numbers (CrUX, Search Console) differ; say which
you used.

## 4. Mobile

Responsive (no separate mobile host), tap targets sized, viewport set,
no horizontal scroll, same content as desktop.

## 5. Security and HTTPS

HTTPS everywhere, valid certificate, no mixed content, http to https
redirects, HSTS header.

## 6. URL structure

Readable and descriptive, keywords where natural, consistent, no needless
parameters, lowercase with hyphens.

## 7. On-page basics (per sampled page)

| Element | Check | Common failures |
| --- | --- | --- |
| Title | unique, keyword near the start, 50 to 60 characters, brand at the end | duplicates, truncated, missing |
| Meta description | unique, 150 to 160 characters, keyword, a reason to click | duplicates, auto-generated |
| Headings | one H1 with the keyword, H1 to H2 to H3 without skips, headings describe content | several H1s, headings used for styling |
| Content | keyword in the first 100 words, related terms, enough depth, matches intent | thin, doorway and near-duplicate pages |
| Images | descriptive file names, alt text, compressed, modern format, lazy loaded | missing alt text |
| Internal links | key pages well linked, descriptive anchors, no broken links | orphans, over-optimised anchors, footer link piles |
| Keyword targeting | one clear target per page, title, H1 and URL aligned, no two pages on one target | cannibalisation |

## Report shape

Executive summary (health, top three to five issues, quick wins), then per
finding: issue, impact (High, Medium, Low), evidence (how you found it),
fix, priority. Close with an action plan: critical fixes that block
indexation, high-impact improvements, quick wins, long-term items.
