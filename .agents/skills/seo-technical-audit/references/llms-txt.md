<!-- source: https://raw.githubusercontent.com/Infrasity-Labs/dev-gtm-claude-skills/main/skills/llms-txt-checker/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# llms.txt and AI-readiness files

Condensed from the llms-txt-checker skill in
Infrasity-Labs/dev-gtm-claude-skills. Fetch `/robots.txt`, `/llms.txt` and
`/llms-full.txt` as plain text and record status code and size for each
before auditing. A 200 with an HTML body is a soft miss (the site served
its 404 page), not a hit.

Context the source does not carry: Google states that `llms.txt` is not
used by Google Search and neither helps nor hurts rankings. Audit it as a
convenience for other AI systems and documentation tooling, never as a
ranking lever, and say so in the report.

## llms.txt structure

- Starts with one `#` title (site or product name).
- A `>` blockquote summary right under it, one or two sentences.
- `##` sections group links (Docs, API reference, Guides, and so on).
- Each link is `- [Page title](https://absolute-url): short description`.
- An `## Optional` section for secondary content is best practice.
- No nested headings inside link sections; no images, HTML or tables.

## Content completeness

- Core product and feature pages listed.
- API reference, getting-started and integration guides where they exist.
- Descriptions say something the title does not.
- Absolute URLs only; no links that 404.

## AI-readiness signals

- References `llms-full.txt` (directly or in a documentation-sets section).
- Segmented files per use case are an advanced plus.

## llms-full.txt (when present)

Non-empty; contains page content, not only links; clear boundaries between
documents; a `Source:` URL per section; clean Markdown without raw HTML or
script residue; a size warning when it would exceed a typical context
window.

## robots.txt signal

`User-agent: *` with `Allow: /`; any `Disallow` that blocks AI crawlers
(see `modern-signals.md` for the bot list); the `ai-input` and `ai-train`
hints if the site uses them.

## Facts to keep straight

- Mintlify, Fern and GitBook generate `llms.txt` (Mintlify and Fern also
  `llms-full.txt`, with a `Link: </llms.txt>; rel="llms-txt"` header);
  Astro Starlight does not.
- The standard was proposed in September 2024; `llms-full.txt` is a widely
  adopted companion, not part of the original proposal.

## Report lines

Discovery (which files answered, status, size), an llms.txt verdict with
the failed checks, the llms-full.txt verdict or "not referenced", the
robots signal, and two or three recommendations. If neither file exists,
say what a minimal one would list, drawn from the sitemap.
