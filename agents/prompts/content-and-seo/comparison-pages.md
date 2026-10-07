# Comparison pages

**Reads:** `strategy/competitive/`, `strategy/positioning.md`,
`data/seo/keywords.csv`, `data/crm/snapshots/` (closed deals),
`memory/transcripts/processed/` · **Skills:** `/battlecard` writes the
honest view and `/comparison-page` turns it into the page; these prompts
pick which pages to build, gather the switcher proof and attack the draft
before a buyer, or the competitor, does.

Buyers search "[competitor] alternatives" right before they choose. You
walk away with a page that's fair enough to be believed and specific
enough to win: where you're better, where they are, and who should pick
which. The skill writes from the battlecard. The prompts make sure you
build the right pages first and that every claim on them survives a
hostile read.

## Prompts

### Decide which comparison pages to build

```
Using this repo, rank which comparison or alternatives pages to build next.

CONTEXT
I can build two this quarter. I want the ones that matter most in deals and in search.

READ FROM THE REPO
- Every battlecard in strategy/competitive/, with last_reviewed.
- Closed deals by competitor in the newest closed-deals snapshot in data/crm/snapshots/.
- Rows in data/seo/keywords.csv that name a competitor or say "alternative" or "vs".

BUILD
- A table: competitor, deals in the last two quarters, win rate with n, keyword rows and volume, existing page in content/ (path or none), battlecard age.
- A ranked top three with the reason.
- Any competitor that needs a battlecard refresh first.

OUTPUT
The table and the top three.

GROUNDING
Cite paths and n. Never estimate a volume; if keywords.csv has no row, say so. If there's no battlecard, the next step is /battlecard, not a page.
```

### Collect the switcher proof

```
Using this repo, gather the evidence the page needs from customers who chose us over the competitor.

FILL IN
- Competitor: [competitor]

CONTEXT
A comparison page lives or dies on proof from people who looked at both.

READ FROM THE REPO
- Won deals against the competitor in data/crm/snapshots/ (the closed-deals and coded deals files).
- Their calls in memory/transcripts/processed/.
- The battlecard's "where they win" section.

BUILD
- Verbatim lines on why they chose us, grouped by reason, each with its path.
- What buyers said the competitor did better, so the page can be honest about it.
- Quotes that would need customer approval before going public.

OUTPUT
A proof sheet for the brief.

GROUNDING
Quotes verbatim with paths. No customer name goes public without approval; mark each quote "approval needed".
```

### Check a live page is still right

```
Using this repo, check our comparison page against the current battlecard.

FILL IN
- Page: [piece]

CONTEXT
Competitors change pricing and ship features. A wrong comparison page costs trust and invites a letter.

READ FROM THE REPO
- The page's draft in content/.
- The competitor's battlecard in strategy/competitive/ and the latest competitor-watch report in reports/recurring/competitive/.
- strategy/product-brief.md, for our own claims.

CHECK
- Every claim about them: still matches the battlecard? Dated?
- Every claim about us: matches the product brief?
- Anything the competitor changed since the page was published.

OUTPUT
A list of lines to fix, with the source for the correction.

GROUNDING
Cite paths. Pricing older than a quarter is "re-check on their public page", never restated from memory.
```

## Advanced prompts

### Red-team the page as the competitor's team

```
Attack our comparison page the way the competitor's marketing and legal team would, then fix what breaks. Use this repo for what we can actually prove.

FILL IN
- Page: [piece]

CONTEXT
If the page has a claim we can't back, they'll find it, and buyers will hear about it.

FROM THE REPO
- The page's draft in content/.
- The competitor's battlecard in strategy/competitive/.
- strategy/product-brief.md and the proof in strategy/messaging.md.

METHOD
- Round 1, their legal: flag every claim that is unverifiable, outdated, or a comparison without a stated basis.
- Round 2, their marketing: write the rebuttal post they'd publish, quoting our page.
- Round 3, a neutral buyer: read both and say who they believe and why.
- Fix each flagged line: back it with a cited source, soften it to what's provable, or cut it.

OUTPUT
A table of flagged lines (claim, attack, verdict, fixed line), then the rebuttal post they'd write, then the revised draft as a diff on a branch.

GROUNDING
Every kept claim cites a repo path. Never invent a capability for either side. The rebuttal is a simulation; label it so.
```

## Questions to just ask

- Which competitors do we lose to most, and do we have a page for each?
- What does the [competitor] battlecard say they do better than us?
- When was the [competitor] battlecard last reviewed?
- Which keywords mention a competitor, and what ranks for them?
- What did customers who switched from [competitor] say on calls?
- Does our [competitor] page still match their battlecard?
- Which claims on [piece] have no source in the repo?
- What changed at [competitor] in the last competitor-watch report?
- Which won deals against [competitor] could give us a quote?
- Who should pick [competitor] over us, according to our battlecard?
- What's our win rate against [competitor], and how many deals is it?
