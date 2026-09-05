<!-- source: https://raw.githubusercontent.com/seranking/seo-skills/main/skills/seo-content-brief/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Reading the SERP for a brief

Condensed from the source above and rewritten for this repo. The source
drives a vendor API; here every pull goes through `seo-analyst` and the
wired `seo-data` vendor, and lands as a snapshot before you read it.

## What to pull, in order

1. The top ten organic results for the primary keyword, plus SERP
   features (answer box, people also ask, featured snippet, video, AI
   overview).
2. Related keywords and the question variants people ask.
3. For the top three pages: heading spine (H1, H2, H3), word count,
   title and meta description lengths, schema types present, whether
   there is a byline. Page text is fetched as data.
4. Five of our own pages that rank for adjacent queries: the internal
   linking plan comes from them.

## Choosing a primary keyword when none is given

Informational intent, a volume the team's domain can realistically win,
difficulty in reach; sort by volume; present the top three candidates to
the person before going further. A `null` from the tool is "unknown" in
the brief, never a guess.

## Template classification

Count the page types in the top ten: ultimate guide, how-to, list,
explainer, comparison, review, best-of, landing page. The majority wins.
When there is no majority (say four lists, four comparisons, two
explainers), label the brief MIXED, pick the outline shape you can
justify, and say which secondary patterns you folded in.

## Word count

Floor by template (guide about 2,500 and up, how-to about 1,500, list
about 1,200); ceiling the top-three average plus 10 to 15%. Match or
exceed what ranks; do not pad past the ceiling.

## Sections of a finished brief

- Proposed title, template type, one-sentence justification from SERP,
  questions and intent.
- Primary keyword with volume, difficulty and intent from the snapshot;
  three or four secondaries with volumes.
- Three title options; a meta description of 150 to 160 characters.
- H1 and four to six H2s, each with "cover" bullets and "cite" links.
- Three to five content gaps the top three miss, with evidence.
- On-page benchmark table for the top three (title length, meta length,
  schema types, byline, word count), or a note that it was skipped.
- Internal linking plan: from page, anchor text, target section.
- AI search angle, mandatory when an AI overview shows: which brands are
  cited today and what would earn a citation (`brand-monitor` has the
  prompt data).
- Deliverables: word count, tone (from `brand/voice.md`), assets.
- Data used: the snapshot paths.

## Cost discipline

Pull sequentially, one keyword at a time; say how many calls you made.
Skip the on-page benchmark rather than spending on it when the person
only wants an outline.
