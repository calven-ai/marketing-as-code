<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/schema/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Schema markup for one page

Condensed from coreyhaines31/marketingskills `schema`.

## Principles

1. Accuracy first: markup describes only what is on the page, and is
   updated when the page changes.
2. JSON-LD, in the head or at the end of the body; it is what Google
   recommends and the easiest to maintain.
3. Only types Google supports for rich results, and only where the page
   meets the eligibility rules; no markup to game a feature.
4. Validate before shipping; watch Search Console enhancements after.

## Which type

| Type | Use for | Required | Recommended |
| --- | --- | --- | --- |
| Organization | company homepage or about page, once | name, url | logo, sameAs (social and profile URLs), contactPoint |
| WebSite | homepage | name, url | potentialAction for site search |
| Article or BlogPosting | posts, news | headline, image, datePublished, author | dateModified, publisher, description |
| Product | product pages | name, image, offers (price, availability) | sku, brand, aggregateRating, review |
| SoftwareApplication | SaaS or app pages | name, offers | applicationCategory, operatingSystem |
| FAQPage | a real FAQ section | mainEntity (Question and Answer pairs) | |
| HowTo | tutorials with steps | name, step | totalTime, tool |
| BreadcrumbList | any page with breadcrumbs | itemListElement (position, name, item) | |
| Event | webinars, events | name, startDate, location | endDate, organizer, offers |

Several types on one page go in one `@graph` array under one
`@context`.

## Common errors

- Missing required properties: check the type's documentation.
- Invalid values: dates in ISO 8601, URLs absolute, enumerations exact.
- Markup that does not match visible content (a rating with no visible
  reviews, an FAQ with no visible questions): a policy violation, not a
  shortcut.

## Implementation notes

Static site: paste the block into the template. React or Next.js: render
it in the head component from page data. CMS: use the SEO plugin's
structured-data field rather than pasting into the body.

## Validation checklist

- Passes the Rich Results Test and the schema.org validator.
- No errors or warnings.
- Matches the page content.
- All required properties present.

## Where the block lands in this repo

For a draft, under a `## SEO` heading at the end of `content/<x>/draft.md`
as a fenced `json` block; `publish` moves it into the CMS. For a live
page, in the change table of the report with the file or template it
belongs in.
