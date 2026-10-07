# Paid ads

**Reads:** `strategy/personas.md`, `strategy/messaging.md`,
`strategy/competitive/`, `projects/<campaign>/campaign.md`,
`data/ads/snapshots/`, `reports/recurring/ads/` · **Skills:** `/ad-brief`
writes angles and variants, `/ads-performance` reports the week and
`/ads-account-audit` finds wasted spend; these prompts diagnose, rank and
decide between them.

Paid is where a weak message costs real money fast. You're about to put
budget behind copy, or a variant just lost and nobody knows why. You walk
away with variants ranked against the persona before spend, a diagnosis
when an ad underperforms, and a cost ceiling you can defend. For fresh
variants, `/ad-brief` does it; for the weekly numbers, `/ads-performance`.

## Prompts

### Rank ad variants before spend

```
Using this repo, rank the ad variants below for the persona before we spend on them.

FILL IN
- Persona: [persona]
- Channel: [channel]
- Variants: [paste the variants]

CONTEXT
We can afford to run two. I want the two most likely to earn a qualified click, not the cleverest.

READ FROM THE REPO
- The persona's pains and words in strategy/personas.md.
- The pillar and proof in strategy/messaging.md.
- The campaign's landing page draft in content/, so ad and page make the same promise.

SCORE
- Per variant: relevance to the persona's pain, proof behind the claim, match with the landing page, voice.
- The click you'd get from someone outside the ICP, and why.

OUTPUT
A ranked table with scores and one line each, then the two to run.

GROUNDING
Cite the path behind each score. A claim with no source is marked unsupported, not softened. Don't invent a click rate.
```

### Diagnose why an ad lost

```
Using this repo, tell me why the losing ad below lost and what to test next.

FILL IN
- Campaign: [campaign]
- Winner and loser: [paste both ads]

CONTEXT
"The other one won" isn't a learning. I want a reason we can reuse.

READ FROM THE REPO
- Results for both ads in the latest data/ads/snapshots/ file for this campaign.
- The campaign's targets in projects/ (campaign.md).
- The persona in strategy/personas.md.

BUILD
- Whether the gap is real given the clicks and spend (say if it's too small to call).
- The one difference that most likely explains it: hook, offer, proof, audience or format.
- The next test that isolates that difference.

OUTPUT
Three short paragraphs: verdict, reason, next test.

GROUNDING
Use only snapshot numbers, with the path and n. If the ads aren't in a snapshot, say which export to drop in data/ads/snapshots/.
```

### Write ads for searches on a competitor's name

```
Using this repo, write search ads for people searching for the competitor below.

FILL IN
- Competitor: [competitor]

CONTEXT
Someone typing their name is already shopping. The ad has to give them a fair reason to look at us, without claims we can't back.

READ FROM THE REPO
- The competitor's battlecard in strategy/competitive/.
- Our positioning in strategy/positioning.md.
- Any comparison page we've published in content/.

WRITE
- Three angles where we're genuinely stronger, each with proof.
- Five headline and description pairs per angle, inside the platform limits.
- The comparison page each should land on, or a note that we need one.

OUTPUT
A table of variants by angle.

GROUNDING
Cite the battlecard line behind every claim. Never invent a competitor weakness, price or customer. Don't use their trademark in the copy; say if the battlecard flags a legal note.
```

## Advanced prompts

### Find the break-even cost per click by segment

```
Work out the most I can pay per click in each segment and still pay back. Use this repo for conversion rates through the funnel, deal size and win rate.

FILL IN
- Channel: [channel]
- Payback target: [months]
- Gross margin: [percent, or "check the plan"]

CONTEXT
We bid the same everywhere. Some segments are worth twice the click; others lose money at any price.

FROM THE REPO
- Click to lead, lead to MQL, MQL to opportunity and win rate per segment, from data/crm/snapshots/ and data/ads/snapshots/.
- Average deal size per segment from the closed-deals snapshot.
- How data/ontology/metrics.md defines each stage.

METHOD
- Build the funnel per segment and compute break-even CPC.
- Run a Monte Carlo: treat each conversion rate as a Beta from its counts and deal size as its observed spread. Draw 10,000 times.
- Report the CPC at which payback holds in 80% of draws.
- Show which input moves the answer most (sensitivity).
- If you can run code, do it in Python and give me the script.

OUTPUT
A table: segment, median break-even CPC, the 80% safe CPC, the input it's most sensitive to. Then the bid change I should make.

GROUNDING
Label every number as repo (file path and n), mine, or your assumption. Flag any segment with fewer than 20 opportunities as too thin to model.
```

### Call the ad test early, or don't

```
Tell me whether I can call this ad test now or have to keep spending. Use this repo for the results so far.

FILL IN
- Campaign: [campaign]
- Variants: [the two ad names]

CONTEXT
Every extra day costs budget. Calling it on noise costs more.

FROM THE REPO
- Impressions, clicks and conversions per variant from data/ads/snapshots/.
- The primary conversion as data/ontology/events.md names it.

METHOD
- Model each variant's conversion rate as a Beta posterior.
- Report the probability B beats A and the expected loss of picking each.
- Stop if expected loss is under a threshold I set (default 0.1 percentage points); otherwise estimate the days left at current spend.
- If you can run code, simulate it and plot both posteriors.

OUTPUT
A verdict (call it, keep going, it's a tie) with the numbers behind it.

GROUNDING
Label every number as repo (file path and n), mine, or your calculation. Don't call a winner on clicks if the test was meant to be on conversions.
```

## Questions to just ask

- What did we spend on paid last month, by campaign?
- Which campaign has the lowest cost per MQL this quarter?
- Which ads ran longest without a refresh?
- What's the target CPL in the [campaign] brief, and are we under it?
- Which persona does each running campaign target?
- Does the landing page for [campaign] make the same promise as the ads?
- Which claims in our ads have no proof in the messaging file?
- What did the last ads account audit flag that's still open?
- Which segments convert from click to opportunity at all?
- Is there a comparison page we can send [competitor] searches to?
- What did last week's ads report say to pause?
- Which ad snapshots are older than a month?
