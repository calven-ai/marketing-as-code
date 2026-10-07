# Attribution

**Reads:** `data/crm/snapshots/` (closed deals), `data/analytics/snapshots/`
(conversions), `data/ads/snapshots/`, `data/ontology/funnel.md`,
`data/ontology/naming.md` · **Skills:** `/attribution-analysis` puts
first-touch, last-touch and multi-touch side by side and proposes a model;
these prompts answer the question someone actually asked and test how much
the answer depends on the model.

Someone asks "what's driving pipeline?" and the honest answer is "depends
which model you ask". You walk away with an answer to the real question
(should we fund this channel?), the models that agree and disagree, and how
sensitive the call is to the assumptions. The skill builds the comparison.
The prompts turn it into a decision.

## Prompts

### Answer "which channels drive pipeline"

```
Using this repo, answer which channels drive pipeline, in a way I can repeat to the exec team.

FILL IN
- Window: [window]

CONTEXT
The exec team wants one answer. I want one they won't have to unlearn next quarter.

READ FROM THE REPO
- The latest attribution report in reports/adhoc/, if there is one.
- The attribution model the team uses in data/ontology/funnel.md.
- The newest closed-deals and conversions snapshots in data/crm/snapshots/ and data/analytics/snapshots/.

BUILD
- Pipeline by channel under the agreed model, with n.
- Where first-touch and last-touch disagree with it by more than ten points.
- One sentence per channel: what we can say with confidence and what we can't.

OUTPUT
A table and five sentences for a slide.

GROUNDING
Cite paths and n. If no model is agreed in the ontology, say so and suggest /attribution-analysis. If an export is missing, name it.
```

### Check tracking before trusting the numbers

```
Using this repo, check whether our source data is clean enough to attribute anything.

FILL IN
- Window: [window]

CONTEXT
Half of attribution arguments are really about broken UTMs and empty source fields.

READ FROM THE REPO
- The UTM rules in data/ontology/naming.md.
- The newest conversions snapshot in data/analytics/snapshots/ and contacts snapshot in data/crm/snapshots/.
- The UTM tables in active campaigns' campaign.md files in projects/.

BUILD
- Share of conversions and deals with no source, an unknown source, or a source that breaks the naming rules.
- The campaigns with the most broken links.
- How much pipeline sits in "unattributed".

OUTPUT
A short table and the fixes, ordered by pipeline affected. Suggest /utm-builder for the campaigns with broken links.

GROUNDING
Cite paths and n. Don't reassign unattributed deals by guessing.
```

### Make the channel ROI case

```
Using this repo, put spend next to attributed pipeline per channel.

FILL IN
- Window: [window]

CONTEXT
Budget season. I need cost per opportunity and pipeline per dollar by channel.

READ FROM THE REPO
- Spend by channel from the newest snapshots in data/ads/snapshots/.
- Attributed pipeline under the agreed model from the latest attribution report.
- The pipeline definition in data/ontology/metrics.md.

BUILD
- A table: channel, spend, opportunities, pipeline, cost per opportunity, pipeline per dollar, each with n.
- Channels where spend isn't in the repo, listed as gaps.

OUTPUT
The table and the three channels to scrutinise.

GROUNDING
Cite paths. Never estimate spend; name the export to drop in data/ads/snapshots/.
```

## Advanced prompts

### Test how much the answer depends on the model

```
Run a sensitivity analysis on our channel attribution and tell me which conclusions survive any reasonable model. Use this repo for the deals, their touches and spend.

FILL IN
- Window: [window]
- Decision: [e.g. cut paid social by half, double events]

CONTEXT
If the budget call flips when we change the model, it isn't a data-driven call. I want to know which calls are robust.

FROM THE REPO
- Won and lost deals with touches and dates from the closed-deals and conversions snapshots in data/crm/snapshots/ and data/analytics/snapshots/.
- Spend by channel from data/ads/snapshots/.
- The agreed model in data/ontology/funnel.md.

METHOD
- Compute channel credit under first-touch, last-touch, linear, time-decay (half-life 7, 14, 30 days) and position-based (40/20/40 and 30/40/30).
- For each channel, show the range of credit across models.
- Apply the decision to each model and see whether the expected effect on pipeline changes sign.
- Flag conclusions that hold under every model as robust; the rest as model-dependent.
- If you can run code, do it in Python with the models as functions and give me the script.

OUTPUT
A tornado chart or table of credit ranges per channel, the decision's effect under each model, and a robust-or-not verdict.

GROUNDING
Label every number as repo (path and n), mine, or your calculation. Attribution isn't causation; say so in the verdict, and suggest a holdout test via /ab-test-plan where it matters.
```

## Questions to just ask

- What attribution model do we use, per the ontology?
- How much pipeline came from paid last quarter under that model?
- Which channel looks best first-touch and worst last-touch?
- What share of deals has no source recorded?
- Which campaigns broke the UTM rules this month?
- What did the last attribution report recommend?
- What's our cost per opportunity on [channel]?
- How many touches does a won deal have on average?
- Which sources appear in the CRM that aren't in our naming rules?
- Is the ads spend snapshot recent enough to answer an ROI question?
- How long from first touch to opportunity, by channel?
