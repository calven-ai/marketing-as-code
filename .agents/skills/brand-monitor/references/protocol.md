# The brand-monitor protocol

The judgment half of the weekly run. `scripts/aeo_diff.py` has already
counted; this is how to read the counts and the answers behind them.

## 1. Scoreboard, by tier

Start from the non-branded tier table (naming us on a prompt that names us
proves nothing):

- **Tier 1 Buy:** named and named first, this run and rolling 4, by
  engine. A tier-1 change outranks any tier-2 or tier-3 change.
- **Tier 2 Problem:** our pages cited, then named.
- **Tier 3 Authority:** our pages cited; a mention is a bonus.

Then three headline metrics on non-branded prompts: visibility (named, by
tier, stage and engine), content influence (our pages cited whether or not
we are named: which pages, for which prompts) and share of voice (who owns
which stage). Read by track as well: each track answers one strategy
question in `data/seo/README.md`. Branded prompts are scored as brand
accuracy (answers with no factual error, `k of n`, from step 2).

One run is a sample; answers are stochastic. A single flip on one prompt is
an observation unless it repeats or the prompt is branded. On the first run
there are no deltas, trend, forecast score or last actions: say so once.

## 2. Audit every mention

For each answer that names us, classify prominence: `recommended` (the
pick, or first for our buyer), `listed` (one option among several),
`passing` (named without a reason) or `negative`. Check every claim about
us against `strategy/product-brief.md` and `strategy/positioning.md`: what
we do, for whom, plans and prices. A wrong fact is an `entity` finding
whatever the rate does. Audit branded prompts every run, named or not.

## 3. Why not us

Work the gaps in tier order: every tier-1 prompt where we are absent,
tier-2 prompts where neither our page is cited nor we are named, tier-3
prompts only where a page we own lost its citation, plus every loss
finding. Read the answers and stop at the first rung with evidence:

1. **Measurement.** An engine error, a clarifying question instead of an
   answer, or a detection error (a brand alias matched in a title or
   another product's name). Fix `data/seo/brands.csv` aliases in a
   proposal and re-score with `aeo_diff.py --redetect`.
2. **Entity.** Engines do not know us or describe us wrongly. Fix the facts
   engines read: llms.txt, about, product and pricing pages, structured
   data, consistent third-party profiles.
3. **Content.** No page answers the question (`target_page` empty or off
   topic). Fix: a page of a named type (comparison, alternatives, guide,
   template, FAQ) on the prompt's topic, through `aeo-page-optimize`.
4. **Page fitness.** A page exists and is not cited. Compare it with the
   pages engines do cite: answer in the first lines, comparison table,
   named alternatives, a current date, the prompt's wording, listed in
   llms.txt. Fetched but not cited is fitness; never fetched is discovery.
5. **Distribution and authority.** Engines answer from third-party lists,
   review sites and communities (`cited_domains`) where we are absent. Fix:
   get onto the specific pages they cite; name the URLs.
6. **Positioning.** Engines name us but for the wrong job or buyer. Hand to
   `positioning-refresh` with the exact answer lines.

Give each gap an evidence level: **observed** (the answers show it) or
**inferred** (it fits, nothing links it), naming the alternative not ruled
out. Up to ten extra calls a run may re-ask a prompt or test a variant; a
re-ask is evidence only and never changes the snapshot or n.

## 4. Pages

Every page of ours cited this run or targeted by a tier-1 or tier-2 prompt:
the prompts citing it, by engine, and, where the web and SEO roles' latest
snapshots hold them, its sessions from AI assistants and its Google rank.
Quote their numbers; never recompute them. Cited and never visited means
the answer satisfies without a click: fine for awareness, a problem for a
decision prompt.

## 5. Last actions and the set

Score each open `aeo-finding:` task whose check date has arrived: moved,
not moved (against its decision rule) or not due. Two checks without
movement make it "The one thing". Prompt and brand changes follow the
freeze in SKILL.md; every change is listed under Set changes and in the
memory file's Set log.

## 6. Forecast and memory

End the report with the forecast line SKILL.md gives: integer ranges for
next run's non-branded named, cited and named-first counts you would bet
80 percent on, with one line of why. The next `aeo_diff.py` scores it and
ranks a miss first. Then rewrite `memory/knowledge/aeo-memory.md`: add,
score or drop Watch items (each with a check date), add a pattern you had
to work out, append Events, Candidates and the Set log, prune to about 150
lines.

## Filing once

The owner is where the fix lives: how engines read and cite a page (llms.txt,
answer structure, entity facts, third-party lists) is this role's; whether
Google indexes and ranks it belongs to `seo-analyst`; everything after the
landing to `web-analyst`. A non-owner lists the gap under Hand-offs with its
numbers. A task body carries: evidence (prompt ids, text, tier, engines,
`k of n`, quoted answer lines, cited domains), gap class and evidence
level, the proposed action (content type and topic, target page or the
exact third-party URL), the target metric and its current value, a check
date (2 weeks for entity and page fitness, 4 for content and
distribution), the decision rule, `Page: <path>` (or `Page: none (new
piece)`), the marker line `aeo-finding: <slug>` and the report path.

## Report skeleton

Sections only when they have content, in this order: The one thing (the
bet it moves, the tier it serves) · Scoreboard (tier table first, then
stage and engine, brand accuracy, last forecast scored) · How engines
describe us (prompt, engine, prominence, accuracy, the quoted line) ·
Findings (ranked by tier then score: what, tier, gap class and evidence,
now what) · Pages · Who wins where we do not (per stage: brands named,
domains cited) · Last actions · Set changes · Hand-offs · Data caveats ·
Tasks filed · Evidence (calls, cost) · Data used. The forecast line closes
the report.
