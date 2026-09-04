<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/site-architecture/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Site architecture reference

Condensed from the source above and rewritten for this repo.

## Discovery questions

1. New site, or restructuring an existing one? If existing, what hurts
   (bounce, rankings, findability)?
2. Site type: SaaS marketing, content, e-commerce, docs, hybrid, small
   business?
3. How many pages exist or are planned?
4. Which five pages matter most, by traffic or business value?
5. Which URLs must survive (backlinks, rankings, bookmarks)?
6. Who are the audiences and what does each come to do?

## Depth by site type

| Type | Depth | Sections | URL pattern |
| --- | --- | --- | --- |
| SaaS marketing | 2 to 3 | home, features, pricing, blog, docs | `/features/<name>` |
| Content | 2 to 3 | home, blog, categories, about | `/blog/<slug>` |
| Docs | 3 to 4 | home, guides, reference | `/docs/<section>/<page>` |
| Hybrid SaaS and content | 3 to 4 | home, product, blog, resources, docs | `/product/<feature>` |
| Small business | 1 to 2 | home, services, about, contact | `/services/<name>` |

Go as flat as the navigation allows; add a level when a dropdown would
hold more than about twenty items. Important pages within three clicks
of home; anything four levels deep is a symptom.

## URL rules

Human-readable, hyphens not underscores, the path mirrors the
hierarchy, one trailing-slash convention, lowercase enforced by
redirect, short but descriptive. Patterns: `/features/<name>`,
`/pricing`, `/blog/<slug>`, `/blog/category/<slug>`,
`/customers/<slug>`, `/docs/<section>/<page>`, `/compare/<competitor>`,
`/integrations/<name>`, `/templates/<slug>`, `/privacy`, landing pages
at `/<slug>` or `/lp/<slug>`.

Mistakes: dates in blog URLs, over-nesting, ids instead of slugs,
content behind query parameters, two patterns for one page type, and
any URL change without a redirect.

## Navigation

Header: four to seven items ordered by use, the logo home-linked on the
left, the primary CTA rightmost, a mega-menu of at most three or four
columns. Footer: product, resources, company, legal columns.
Breadcrumbs: `Home > Parent > Page`, every segment but the last
clickable, mirroring the URL. Sidebar for section navigation in docs;
contextual links in the body for next steps.

## Internal linking

- No orphans: every page has at least one inbound internal link.
- Descriptive anchors, never "click here".
- About five to ten internal links per thousand words.
- The important pages (home, features, pricing) get the most inbound
  links.
- Hub and spoke: the hub links every spoke, spokes link back and to
  each other where it helps; feature pages link case studies, posts
  link product pages.

Link audit: no 404s, breadcrumbs on every page, related-content links
on posts, cross-section links present.

## Redirects

Every old URL gets a 301 to its new home; the map is a table of old
URL, new URL, type. Missing redirects lose backlinks and rankings and
break bookmarks. In this repo the map is a snapshot,
`data/seo/snapshots/YYYY-MM-DD-repo-redirects.csv`, so a migration can
be audited later.

## Deliverables of a plan

1. The hierarchy as a text tree with URLs.
2. The URL map: page, URL, parent, nav location, priority.
3. The navigation spec: header, footer, sidebar, breadcrumbs.
4. The internal-linking plan: hubs, spokes, cross-section links, the
   orphan audit, recommended links per key page.
5. The redirect map when URLs change.
