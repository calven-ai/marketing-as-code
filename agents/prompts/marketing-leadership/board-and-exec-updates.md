# Board and exec updates

**Reads:** `reports/qmr/`, `reports/recurring/pipeline/` and
`reports/recurring/weekly/`, `strategy/positioning.md`,
`strategy/competitive/`, `memory/decision-log.md` · **Skills:** `/qmr` and
`/pipeline-report` produce the numbers; `/meeting-prep` builds the agenda.
These prompts write the marketing pages a board or exec team actually
reads.

The board pack is due Thursday and marketing gets three slides. They'll be
read by people who see a dozen companies a quarter and spot a soft number
from across the room. You walk away with pages that say what happened,
what it means and what you need, every number with its source and sample,
and a short answer ready for the question nobody wants.

## Prompts

### Write the marketing pages of the board pack

```
Using this repo, write the marketing section of the board pack for the period below.

FILL IN
- Period: [quarter]
- Pages: [how many, usually two or three]

CONTEXT
Board members want the trend, the cause and the ask. No vanity metrics, no channel detail they can't act on.

READ FROM THE REPO
- This period's QMR in reports/qmr/.
- The last three pipeline reports in reports/recurring/pipeline/.
- Decisions from the period in memory/decision-log.md.

BUILD
- Page one: pipeline created and marketing-sourced share against plan, with the trend over four quarters.
- Page two: what worked, what didn't, what changes, each in two lines with the evidence.
- Page three, if asked: the competitive picture from strategy/competitive/ and the latest competitor watch.
- Each page ends with one ask or decision for the board, or "none".

OUTPUT
The pages as Markdown, one heading per slide, speaker notes under each. Slides if I say deck.

GROUNDING
Every number carries its source path and n in the notes. Use the ontology's metric names. Don't show a metric the QMR didn't measure.
```

### Draft the monthly exec update

```
Using this repo, draft this month's marketing update for the exec team.

FILL IN
- Month: [month]

CONTEXT
Execs read it in two minutes on a phone. They want what moved, what's at risk and what I need from them.

READ FROM THE REPO
- This month's weekly reports and the month-end edition in reports/recurring/weekly/.
- Projects marked at risk or blocked in projects/*/status.md.
- Decisions from the month in memory/decision-log.md.

BUILD
- Three numbers that moved, each with the change and the source.
- Up to three risks, each with the owner and what would unblock it.
- One ask, or none.

OUTPUT
Under 200 words, ready to paste into email or chat.

GROUNDING
Cite paths in a footnote list. A project with no status entry in 14 days is listed as "no update", not assumed on track.
```

## Advanced prompts

### Red-team the board pages

```
Red-team the marketing pages of the board pack as a skeptical board member, and tell me where they'll push. Use this repo for the numbers behind each claim.

FILL IN
- Pages: [paste the draft pages]

CONTEXT
A board member who has seen a hundred of these will find the soft spot in thirty seconds. I'd rather find it first.

FROM THE REPO
- The QMR and its Data used section in reports/qmr/.
- The metric definitions in data/ontology/metrics.md.
- Last period's board pages, if they're in reports/.

METHOD
- Take three board personas: the operator who ran marketing before, the investor who compares you with their portfolio, the finance-minded member who wants cost per dollar of pipeline.
- Each reads the pages and writes the three hardest questions, in their voice.
- For every claim, check it against the source: is the number right, is n big enough, did the definition change since last period, is a trend drawn from two points?
- Score each claim: solid, needs a caveat, or cut.

OUTPUT
A table: claim, verdict, the question it invites, the fix. Then the three questions most likely to come up, with a two-sentence answer each.

GROUNDING
Label every number as repo (file path and n), mine, or your calculation. The board personas are lenses, not real people; their questions must rest on what the pages actually say.
```

## Questions to just ask

- How much pipeline did marketing source last quarter, and what share of the total?
- What did we tell the board last quarter that we have to follow up on?
- Which projects are at risk right now, and who owns them?
- How has our win rate against [competitor] moved over the last four quarters?
- Which number in the board pack has the smallest sample behind it?
- What did we decide this month that execs should hear about?
- Did any metric definition change this year that breaks a quarter-over-quarter comparison?
- What's the one-line positioning we'd say to the board, from positioning.md?
- Which program would I cut first if the board asked for 10% back?
- What's still missing from this quarter's QMR data checklist?
