<!-- source: https://raw.githubusercontent.com/seranking/seo-skills/main/skills/seo-technical-audit/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Modern signals a static crawl misses

Condensed from SE Ranking's technical-audit skill: the checks that need a
rendered page or the response headers, the AI-crawler rules, and the
scoring that turns findings into a top-10 list.

## JavaScript-rendered pages (compare raw HTML with the rendered DOM)

| Code | Check | Why it matters |
| --- | --- | --- |
| `js_canonical_mismatch` | canonical in raw HTML differs from the one after JavaScript runs | Google may use either; canonical choice becomes non-deterministic |
| `js_noindex` | `noindex` appears only after render | invisible to a static crawler, real to Google |
| `js_csr_meta_drift` | title, H1 or meta description differ between raw HTML and rendered DOM | the raw values may be what gets indexed |
| `js_render_budget` | rendered HTML under half the size of the raw HTML | render budget may run out before content loads |
| `js_soft_404` | status 200 but under 500 characters of body text after render | treated as a soft 404 |

Needs a renderer: a `scraping-search` vendor that returns rendered HTML,
or a person with browser devtools. Without one, write "not checked" for
these rows rather than a green pass.

## HTTP-layer directives and headers

- `X-Robots-Tag` with `noindex`, `nofollow` or `none` on any sampled URL.
- Security headers on the homepage and three sample URLs:
  `Content-Security-Policy`, `X-Content-Type-Options: nosniff`,
  `Referrer-Policy`, `Strict-Transport-Security` (with `preload` when the
  domain is on the preload list). `X-Frame-Options` is informational once
  CSP `frame-ancestors` is set.

## AI-crawler rules in robots.txt

Report allow or disallow scope per agent: `GPTBot`, `ChatGPT-User`,
`ClaudeBot`, `PerplexityBot`, `Google-Extended`, `Bytespider`, `CCBot`.
Blocking a search-and-cite bot means that engine cannot cite the site;
blocking a training-only bot (`CCBot`) is a separate decision. Report the
state; the team decides.

## IndexNow (Bing and others)

Look for an `IndexNow:` line or a key-file comment in `robots.txt`, an
`x-indexnow-key` response header, or `/<key>.txt`. Absent is Low
(informational); a key advertised but the file mismatching is Medium.

## Indexation reality check

When Search Console is wired or a person can run URL Inspection: for the
top five traffic URLs record status, the canonical Google chose against
the one declared, and last crawl date. A chosen canonical that differs
from the declared one on a top page is Critical whatever the other
findings say.

## Prioritising

Score each finding as severity times affected pages divided by effort
(S, M, L). The top 10 by score is the fix list. Reuse an existing crawl
under 30 days old rather than re-crawling; a fresh crawl of a large site
is the expensive step and can take half an hour. Audit large sites by
section rather than whole.

## What the skill never does

Apply a fix. It diagnoses; a person decides what ships and in which
order.
