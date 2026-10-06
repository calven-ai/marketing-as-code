# Customer feedback digest

**Reads:** `memory/transcripts/processed/`, `data/reviews/snapshots/`
(reviews, NPS, surveys), `reports/recurring/community/`,
`reports/recurring/reviews/`, `memory/knowledge/`, `strategy/personas.md`,
`strategy/messaging.md` · **Skill:** `/voice-of-customer` synthesizes the
raw material into themes and proposes persona and messaging changes; these
prompts turn it into a monthly digest and test what the themes mean.

Customers tell you things every week: on calls, in NPS comments, in
reviews, in the community. Most of it never reaches the people writing the
messaging. You walk away with a monthly read by theme, in the customers'
own words, with the changes it should drive and an honest call on which
spikes are real. For the deep synthesis, run `/voice-of-customer`; the
digest below is the monthly habit around it.

## Prompts

### Build this month's feedback digest

```
Using this repo, build this month's customer feedback digest.

FILL IN
- Month: [window]

CONTEXT
Marketing, product and customer success read this. They want what customers said, by theme, and what changed from last month.

READ FROM THE REPO
- Calls from the month in memory/transcripts/processed/.
- NPS, survey and review exports for the month in data/reviews/snapshots/.
- The latest community digest in reports/recurring/community/.

BUILD
- The top five themes, each with a count by source and two verbatims with their file.
- What's new or growing since last month's digest.
- One thing to act on per team: marketing, product, customer success.

OUTPUT
A one-page digest. Save it under reports/adhoc/ on a branch if I say save.

GROUNDING
Cite the file behind every quote and count. Quotes verbatim. Never invent a count; if a source has no export for the month, say which one is missing.
```

### Find the pillars customers never mention

```
Using this repo, find the messaging pillars customers never talk about, and the things they talk about that we never say.

CONTEXT
If customers don't use our words, prospects won't either.

READ FROM THE REPO
- The pillars and claims in strategy/messaging.md.
- Calls in memory/transcripts/processed/ and reviews in data/reviews/snapshots/.
- The customer-language file in memory/knowledge/, if the team keeps one.

COMPARE
- Per pillar: how often customers mention it, in their words, with two examples.
- Themes customers raise often that no pillar covers.
- Words customers use for the problem that our copy never uses.

OUTPUT
A table by pillar, then a list of proposed edits to strategy/messaging.md as a diff on a branch.

GROUNDING
Cite paths. A pillar with no mentions is a finding, not a failure to search harder. Don't edit strategy files directly; propose.
```

### Compare feedback across segments

```
Using this repo, compare what customers in different segments say about us.

FILL IN
- Segments: [two or three segments from the ICP]

CONTEXT
We treat all customers the same in the messaging. I suspect the segments care about different things.

READ FROM THE REPO
- Calls and reviews, matched to segment through the customers snapshot in data/crm/snapshots/.
- The segment definitions in strategy/icp.md.

BUILD
- Top three themes per segment, with counts and a verbatim each.
- Where segments agree and where they pull in opposite directions.
- Sentiment by segment where the source carries a score.

OUTPUT
A side-by-side table and three lines on what it means for the messaging.

GROUNDING
Cite paths and n per segment. Flag any segment with fewer than ten pieces of feedback as too thin.
```

## Advanced prompts

### Tell a real spike from noise

```
Tell me whether this month's jump in a complaint theme is real or noise before I escalate it. Use this repo for the theme counts over time.

FILL IN
- Theme: [e.g. onboarding, pricing, a feature]
- Months to compare: [the last six to twelve]

CONTEXT
A theme going from four mentions to nine looks like a crisis. On our volume it might be a normal month.

FROM THE REPO
- Mentions of the theme per month from data/reviews/snapshots/ and memory/transcripts/processed/, with the total feedback volume each month.
- Past digests in reports/adhoc/ for how the theme was counted before.

METHOD
- Compute the theme's share of all feedback per month.
- Build a control chart (p-chart): the mean share and the 3-sigma limits for each month's volume.
- Flag months outside the limits, or runs of six above the mean.
- Check whether volume itself changed (a new survey, a launch) and could explain it.
- If you can run code, plot the chart.

OUTPUT
The chart or table, a verdict (real shift, watch, noise) and the sentence to put in the digest.

GROUNDING
Label every number as repo (file path and n), mine, or your calculation. Say how the theme was coded so next month counts the same way.
```

## Questions to just ask

- What did customers complain about most this month?
- What's our NPS this quarter, and how many responses is it based on?
- Which customers mentioned [competitor] on calls?
- What do detractors say that promoters never do?
- What words do customers use for the problem we solve?
- Which feature requests came up more than three times this quarter?
- What did the community digest flag this week?
- Which persona gives us the lowest scores?
- Which themes from last month's digest went away?
- Are there calls from this month that haven't been processed yet?
- Which customer quotes in memory/knowledge/ are cleared for public use?
- What did customers say about onboarding in the last 90 days?
