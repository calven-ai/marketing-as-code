# Run output, filing and hand-offs

## The weekly write-up

`reports/recurring/seo/YYYY-MM-DD.md`, the skeleton the three search roles
share, sections only when they have content:

1. **The one thing**: what, so what, now what, in three lines.
2. **Scoreboard**: the tier table first (keywords, top 10, top 30, AI
   Overview citing us; this run and last), the branded line, Search Console
   clicks, impressions and CTR against the period before, `k of n` targeted
   pages indexed, one line scoring the last forecast.
3. **Findings**, ranked by tier then score: what, tier, gap class and
   evidence level, now what, with keyword ids and pages.
4. **Pages**: the `page_join.py` rows that matter, then who holds the top
   10 (brands and domains per track).
5. **Refresh candidates and striking distance.**
6. **Set changes**: crosswalk numbers, rows fixed, the quarterly proposal
   when due.
7. **Last actions**: moved / not moved / not due.
8. **Hand-offs**, with the numbers.
9. **Data caveats**: missing sources, a changed set, a market change.
10. **Tasks filed.**
11. **Evidence**: every snapshot path, extra calls and their cost.

## Who owns a finding

The owner is where the fix lives:

| Fix | Owner |
| --- | --- |
| whether Google indexes, ranks and gets clicks on a page (index, canonical, title, internal links, backlinks, CTR), and whether an AI Overview cites it | SEO (you) |
| how answer engines read and cite a page (answer structure, entity facts, third-party lists) | AEO: `brand-monitor`, `aeo-page-optimize` |
| everything after the landing (UX, call to action, tracking) | web: `web-analyst`, `cro-audit` |

A non-owner never files: it lists the finding under Hand-offs. A missing
page serves all three; whoever sees it first files it once, naming its
prompts and keywords.

## Filing

At most three tasks a run, per `integrations/tasks.md`. Before filing,
search open tasks for the marker lines `seo-finding:`, `aeo-finding:` and
`web-finding:` and for the page path; a match gets this run's numbers as a
comment instead of a new task.

Three kinds: **new piece** (class 3; a page of ours that already ranks or
gets impressions for the keyword makes it a refresh candidate instead),
**technical fix** (classes 2 and 4, and a `ctr_gap` title fix), **link
target** (class 6, or a lost strong link to reclaim).

Title `SEO: <observation> → <action>`. Body: Evidence (keyword ids and
text, tier, rank, the top 3 domains, the format the top 10 rewards, the
prompts on the same page) · gap class and evidence level · proposed action
· target metric and its current value · check date (4 weeks for technical
fixes and link targets, 8 for new pieces) · decision rule · `Page: <path>`
(or `Page: none (new piece)`) · the marker line `seo-finding: <slug>` ·
`Source: reports/recurring/seo/YYYY-MM-DD.md`.
