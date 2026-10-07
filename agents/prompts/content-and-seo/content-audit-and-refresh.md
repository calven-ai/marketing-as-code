# Content audit and refresh

**Reads:** `content/` frontmatter, `data/seo/snapshots/` (rankings),
`data/analytics/snapshots/` (landing pages), `strategy/`,
`memory/decision-log.md` · **Skills:** `/content-decay-monitor` finds the
pages sliding in rank or traffic and `/content-inventory` lists what
exists; these prompts catch the pages that are wrong rather than slipping,
and decide what to do with each.

Something changed: the positioning moved, a product shipped, a competitor
repriced, or traffic just looks soft. You walk away with a refresh batch
ranked by what it's worth and a keep, merge or kill call on the rest. Decay
is the easy half and the skill handles it. The harder half is the page that
ranks fine and says something you no longer believe.

## Prompts

### Find pages a strategy change made stale

```
Using this repo, find published pieces that contradict what we now say.

FILL IN
- Since: [the date of the change, or "the last positioning or messaging edit"]

CONTEXT
We changed the story. Old pages still tell the old one.

READ FROM THE REPO
- The git history of strategy/positioning.md, strategy/messaging.md and strategy/product-brief.md since the date: what changed.
- Decisions since the date in memory/decision-log.md.
- Every published or evergreen piece in content/.

BUILD
- What changed, in three lines, with the commit or decision behind each.
- Each piece that uses a dropped term, an old claim, a retired pillar or an outdated product fact, with the line quoted.
- Severity: wrong (a false claim), off-message (old framing), or fine.

OUTPUT
A table: piece path, published_url, the line, what it should say now, severity.

GROUNDING
Quote lines exactly. Cite the strategy file or decision for each "should say now". Don't flag a piece for style alone.
```

### Prioritise the refresh batch

```
Using this repo, turn the decay report and the stale-page list into one ranked refresh batch.

FILL IN
- Stale list: [paste the table from the prompt above, or "none"]
- Capacity: [pieces we can refresh this month]

CONTEXT
I can't refresh everything. I want the batch that recovers the most.

READ FROM THE REPO
- The newest decay report in reports/recurring/seo/.
- data/seo/keywords.csv for each piece's keyword, volume and intent.
- The latest landing-pages snapshot in data/analytics/snapshots/, if there is one.

BUILD
- One list merging decaying and stale pieces.
- A score per piece: traffic or rank at stake, commercial intent, severity of what's wrong.
- The top pieces that fit capacity, each with the refresh type: facts only, rewrite, or merge into another page.

OUTPUT
A ranked table, then the command to run per piece (/content-brief for a refresh brief).

GROUNDING
Cite paths. If there's no decay report or rankings snapshot, say which to run or drop in data/seo/snapshots/. Never estimate a rank or a session count.
```

### Decide keep, merge or kill for the long tail

```
Using this repo, make a keep, merge or kill call on our older pieces.

FILL IN
- Older than: [e.g. 18 months]

CONTEXT
Thin, overlapping pages split our rankings and confuse answer engines.

READ FROM THE REPO
- Every published piece in content/ older than the cutoff.
- data/seo/keywords.csv: which keyword each targets.
- The newest rankings snapshot in data/seo/snapshots/.

BUILD
- Groups of pieces targeting the same keyword or question.
- Per piece: keep, merge into (path), or kill with a redirect target.
- The redirects list for whoever runs the site.

OUTPUT
A table and the redirects list, as a proposal on a branch, never a deletion.

GROUNDING
Cite paths. Nothing is deleted or redirected until a person approves; this is a proposal.
```

## Advanced prompts

### Prove refreshes pay off with a control group

```
Measure whether last quarter's refreshes actually recovered traffic, against pieces we didn't touch. Use this repo for which pieces were refreshed and the ranking and traffic history.

FILL IN
- Refreshed in: [quarter]

CONTEXT
We spend real hours on refreshes. I want to know if they work before I ask for more.

FROM THE REPO
- Pieces refreshed in the period, from the git history of content/ and the frontmatter.
- Rankings snapshots before and after in data/seo/snapshots/.
- Landing-page snapshots before and after in data/analytics/snapshots/, if they exist.

METHOD
- Build a control group: unrefreshed pieces matched on age, intent and starting rank.
- Run a difference-in-differences on rank and sessions: refreshed change minus control change, with an interval.
- Check the parallel-trends assumption on the periods before the refresh. Say if it fails.
- Split by refresh type (facts only, rewrite, merge) if n allows.
- If you can run code, do it in Python and give me the script.

OUTPUT
The effect per refresh type with intervals and n, a verdict (works, unclear, doesn't), and one chart.

GROUNDING
Label every number as repo (path and n), mine, or your calculation. Say when n is too small. Never fill a missing snapshot with an estimate.
```

## Questions to just ask

- Which published pieces still mention [old term]?
- What changed in our positioning since [date]?
- Which pages lost the most rank between the last two snapshots?
- Which pieces have published set but no published_url?
- What's the oldest published piece with commercial intent?
- Which two pages target the same keyword?
- Which comparison pages are older than their competitor's battlecard update?
- Which pieces reference a product fact the product brief no longer has?
- When was the last decay report, and what did it recommend?
- Which refreshed pieces from last quarter recovered rank?
- Which evergreen pieces haven't been touched in a year?
- Is the claim on [piece] still true according to our product brief?
