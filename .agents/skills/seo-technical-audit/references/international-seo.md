<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/seo-audit/references/international-seo.md | license: MIT | fetched: 2026-09-04 -->

# International SEO checks

Condensed from the international-seo evidence file in
coreyhaines31/marketingskills. Only for sites with more than one language
or region. The source cites Google Search Central, Semrush and Search
Engine Land studies for each point.

## Hreflang

- Three equivalent placements: `<link>` in the head, HTTP `Link` headers,
  or `<xhtml:link>` in the sitemap. Google combines them; if the same
  language-region pair points at different URLs across methods, Google
  drops the pair.
- Reciprocal: if X lists Y, Y must list X, or the annotation is ignored.
- Self-referencing: every page includes itself in the set. The most
  common error found in audits; two thirds of implementations have an
  issue.
- `x-default`: the fallback for users matching no variant; include it on
  every variant; it may point at one of the language pages.
- Codes: ISO 639-1 language, ISO 3166-1 alpha-2 region,
  `language[-script][-region]`. A region alone is invalid. `en-UK` is
  wrong (`en-GB`); `es-419` is not an ISO region.
- At 20 or more locales, put hreflang in the sitemap: no runtime cost,
  and the child elements do not count toward the 50,000-URL limit. Focus
  on pages receiving wrong-language traffic, not every page.
- Bing treats hreflang as a weak signal and reads the `lang` attribute,
  `content-language` meta, ccTLDs and server location. Ship both.

## Canonicals across locales

- Each locale page carries a self-referencing canonical; a canonical to
  another locale overrides the hreflang and hides the page.
- Near-duplicate regional variants (en-US and en-GB) are fine with
  hreflang; do not canonicalise one to the other unless you want only one
  indexed.

## URL structure

- Subdirectories and subdomains are treated the same by Google; URL
  parameters (`?lang=en`) are not recommended.
- Mueller's default: `/` as `x-default`, each language under its own
  prefix.
- No IP-based redirects or locale-adaptive pages: Googlebot crawls from
  US addresses without an Accept-Language header, so it never sees the
  other locales. Separate URLs plus hreflang.
- One trailing-slash rule across locale paths, internal links,
  canonicals, hreflang and sitemaps.
- Search Console geotargeting per property where a locale targets one
  country.

## Content quality per locale

- Machine-translated pages with no review count as auto-generated content.
- Thin locale pages (a translated title over English body) are worse than
  no page.
- Partial translation confuses the language signal; keep navigation and
  body in one language per URL.
- Crawl budget: a 20-locale site multiplies every URL by 20; check that
  the locales worth indexing are the ones being crawled.

## What to put in the report

A table: locale, URL pattern, hreflang method, self-reference present,
reciprocal complete, x-default present, canonical self-referencing,
translation quality (reviewed, machine, partial). Then the fixes in
priority order; missing self-reference and wrong codes first.
