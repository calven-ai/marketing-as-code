<!-- source: https://raw.githubusercontent.com/Infrasity-Labs/dev-gtm-claude-skills/main/skills/orphan-pages-internal-linking-opportunities/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Orphan pages and the inbound-link map

Condensed from the orphan-pages skill in
Infrasity-Labs/dev-gtm-claude-skills. Its output was an HTML report; here
the map is a CSV and the linking briefs go into the audit report.

## Find the blog section

1. Normalise the host (`https://`, one www rule, no trailing slash).
2. Read `robots.txt` for a `Sitemap:` line; default to `/sitemap.xml`.
3. A sitemap index lists child sitemaps: fetch each and merge the URLs.
4. Detect the content prefix from the URL patterns (`/blog/`, `/articles/`,
   `/posts/`, `/insights/`, `/resources/`, `/learn/`, `/guides/`): the
   most frequent uniform prefix wins; keep several if several qualify.
   Never hard-code `/blog/`. Drop the listing page itself.
5. If the sitemap shows no content section, read the homepage navigation
   for the blog link and collect post URLs from that page.

## Build the inbound map

For every post, read the page and collect the links in the article body
(not navigation, header or footer) that point at other posts on the same
host, normalised (absolute, no query, no fragment, no trailing slash).
Then invert: for each post, how many other posts link to it and which.

| Inbound links | Class |
| --- | --- |
| 0 | orphan |
| 1 to 2 | low-linked |
| 3 or more | healthy |

Save as `data/seo/snapshots/YYYY-MM-DD-repo-inbound-links.csv` with
columns `url,inbound,linked_from,class`. With `scraping-search` wired the
crawl is one actor run; without it, sample the posts you can read and say
the map is partial.

## Anchor text for each orphan

Derive six to eight keyword variants from the slug, pull their volume
through `seo-analyst` (one search-volume call for the batch), and take
the highest-volume phrase as the anchor. Fallback: the slug with hyphens
turned into spaces. Read the page and write a two-sentence summary of
what it covers.

## The linking brief

For each orphan pick three topically related, well-linked posts as
sources. For each source say where the link goes (the H2 or H3 section,
the paragraph, what surrounds it: precise enough that an editor finds it
without guessing) and draft the sentence or two that carries the anchor
naturally. The same anchor text in all three placements, and it must read
as if it had always been there.

## Rules kept

- Anchor text is fixed per orphan.
- Placement descriptions are specific; "somewhere in the intro" is not a
  brief.
- Say which orphans fell back to the slug because no volume came back.
- The briefs are proposals; edits to live pages go through `publish` and
  a person.
