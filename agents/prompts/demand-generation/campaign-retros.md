# Campaign retros

**Reads:** `projects/<campaign>/` (brief or `campaign.md`, `status.md`),
`content/` frontmatter, `data/crm/snapshots/`, `data/ads/snapshots/`,
`data/analytics/snapshots/`, `memory/decision-log.md` · **Skill:**
`/program-retro` writes the retro against the goal; these prompts dig into
lead quality, what really drove pipeline, and the next brief.

The campaign ended a month ago. Leadership wants to know if it worked, and
"we got 400 leads" won't survive the first question. You walk away with a
verdict against the goal in the brief, an honest read of lead quality, and
the changes that go into the next brief. Run `/program-retro` for the
retro itself; the prompts below are for the questions it raises.

## Prompts

### Judge whether the leads were worth having

```
Using this repo, tell me whether the leads from the campaign below were worth having.

FILL IN
- Campaign: [campaign]

CONTEXT
The lead count looks good. I want to know how many fit the ICP, how many moved a stage, and what they cost per qualified one.

READ FROM THE REPO
- New contacts and pipeline for the campaign in data/crm/snapshots/ (matched by the campaign's UTM slug).
- strategy/icp.md and strategy/personas.md.
- Spend in data/ads/snapshots/ and the goal in the campaign's brief in projects/.

BUILD
- Leads by fit: ICP tier, persona match, no match.
- Progression: how many reached MQL, SQL and opportunity, per data/ontology/funnel.md.
- Cost per lead, per MQL and per opportunity, against the target in the brief.

OUTPUT
One table and a three-line verdict.

GROUNDING
Cite paths and n. Stage names mean what the ontology says. If the pipeline snapshot predates the campaign end, say which export to drop in data/crm/snapshots/.
```

### Diagnose the results by channel

```
Using this repo, break the campaign's results down by channel and tell me which ones earned their budget.

FILL IN
- Campaign: [campaign]

CONTEXT
We spread budget across channels. I want to know where to put it next time.

READ FROM THE REPO
- The channel plan and targets in the campaign's campaign.md in projects/.
- Traffic by source in data/analytics/snapshots/, spend in data/ads/snapshots/, pipeline in data/crm/snapshots/.
- The pieces it shipped in content/ (project frontmatter pointing at the campaign).

BUILD
- Per channel: spend, traffic, leads, opportunities, cost per opportunity, against target.
- Which pieces of content drove the most qualified traffic.
- Where the data can't tell channels apart (missing UTMs), and how much that hides.

OUTPUT
A table by channel and a short paragraph on what to keep, cut and fix.

GROUNDING
Cite paths and n. Don't attribute pipeline to a channel the data can't trace; say "untracked" instead.
```

### Turn the retro into the next brief

```
Using this repo, turn the campaign's retro into the opening section of the next brief.

FILL IN
- Retro: [name its folder in reports/adhoc/]

CONTEXT
Retros get written and forgotten. I want the learnings to be the first thing the next campaign's team reads.

READ FROM THE REPO
- The retro report.
- The playbooks in memory/knowledge/ and decisions logged against the campaign in memory/decision-log.md.
- The brief template in projects/_template/campaign.md.

BUILD
- Keep, change, stop: three bullets each, each tied to evidence in the retro.
- Proposed edits to the relevant playbook in memory/knowledge/.
- Draft decision-log entries for anything the team should settle.

OUTPUT
The brief section and the playbook diff, proposed on a branch.

GROUNDING
Every bullet cites the retro line it comes from. Don't log a decision nobody made: draft it and ask.
```

## Advanced prompts

### Replay the campaign as a counterfactual

```
Replay the campaign as if we'd spent the budget differently, and tell me what we'd likely have gotten. Use this repo for the actual results by channel and the funnel rates.

FILL IN
- Campaign: [campaign]
- Alternatives: [two or three, e.g. all on LinkedIn, half on events, double the nurture]

CONTEXT
The next budget conversation will ask "was that the best use of the money?" I want a ranged answer, not a shrug.

FROM THE REPO
- Spend, leads and opportunities by channel from data/ads/snapshots/ and data/crm/snapshots/.
- Funnel conversion by channel over the last four quarters, for a baseline outside this campaign.
- The goal in the campaign's brief.

METHOD
- Fit a cost-per-opportunity curve per channel with diminishing returns (assume a square-root response unless the data shows more).
- For each alternative, simulate opportunities with the uncertainty in each channel's rates (Monte Carlo, 5,000 draws).
- Compare the distribution of outcomes to what actually happened.
- If you can run code, plot the distributions side by side.

OUTPUT
A table: alternative, median opportunities, 80% range, probability it beats actual. Then what I'd change next time.

GROUNDING
Label every number as repo (file path and n), mine, or your assumption. Say clearly that the response curve is an assumption and show what happens if it's linear.
```

## Questions to just ask

- Did [campaign] hit the goal in its brief?
- How many opportunities came from [campaign], and how many fit the ICP?
- What did [campaign] cost per opportunity?
- Which piece of content from [campaign] got the most traffic?
- Which leads from [campaign] had no UTM?
- Is there a retro for [campaign] yet?
- What did the last three retros say to change, and did we?
- Which campaigns this year missed their goal?
- What decisions were logged against [campaign]?
- Which persona converted best in [campaign]?
- What's in the event playbook in memory/knowledge/?
- How long after [campaign] ended did its opportunities close?
