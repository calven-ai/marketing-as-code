# data/seo/

## Canonical

- **`keywords.csv`**: the single source of truth for every keyword this team
  tracks. Columns:

  ```csv
  keyword,intent,target_url,difficulty,volume,current_rank,last_checked,notes
  ```

  `intent` is one of informational, commercial, transactional or
  navigational. A row here means "we care about ranking for this", so add
  rows on purpose.
  Update `difficulty`, `volume`, `current_rank` and `last_checked` from
  fresh pulls. The three rows it ships with are examples; replace them with
  yours. `scripts/seo_snapshot.py` refreshes volume and difficulty for every
  row and saves the pull as a snapshot.

- **`prompts.csv`**: the AI answer-engine (AEO) prompt set, the questions a
  buyer types into ChatGPT, Google AI Mode or Claude. A fixed panel, so a
  change in the answers is a change in the engines, not in the questions.
  Columns:

  ```csv
  id,prompt,track,stage,intent,tier,persona,target_page,source,status,added_on,retired_on,rationale
  ```

  `id` is `P001` onwards, never reused. A prompt's text is never edited:
  set `status` to `retired` with `retired_on`, and add a new id. `stage` is
  a buying stage (awareness, consideration, decision; the axis in
  `strategy/messaging.md`, not the lifecycle in `../ontology/funnel.md`).
  `intent` is `direct` (we want to be named), `indirect` (we want our page
  cited) or `branded` (names us; measures accuracy and never counts toward
  visibility). `target_page` is the site path meant to win it; empty means
  no page answers it yet. `source` says where the wording came from
  (`transcript`, `win-loss`, `fan-out`, `seo`, `research`; join two with
  `+`) and `rationale` why it is tracked. The set changes at the quarterly
  review, at most five additions and five retirements, as a proposal; the
  `brand-monitor` skill runs it and `prompt-set-builder` drafts additions.

- **`brands.csv`**: who answer engines are checked for. Columns
  `brand,kind,aliases,domains`; `kind` is `self`, `competitor` or
  `adjacent`; `aliases` and `domains` are `|`-separated. An alias counts
  when it appears as a whole word in an answer's prose (links and URLs do
  not count); a domain counts when an answer cites it. Exactly one `self`
  row. A brand list change is a definition change for the next run.

### Tracks

Every prompt sits in one track, and each track answers one strategy
question. Replace the template rows with the team's questions.

| Track | The question it answers | Moves with |
| --- | --- | --- |
| `category` | Do engines name us when a buyer asks what to use for the job we do? | Category page, comparison lists, third-party placements |
| `alternatives` | Are we a named alternative when a competitor's customer shops or renews? | Alternatives and comparison pages, pricing answers |
| `craft` | Do engines cite our pages when someone learns the craft we serve? | Guides, templates, resources |
| `brand` | Do engines describe us correctly: what we do, for whom, at what price? | Entity facts: about, pricing, llms.txt, third-party profiles |

### Tiers

The tier is what winning a prompt is worth. A row takes the tier of the
question it asks, never of its track. Reports lead with tier 1; findings
score a won or lost mention 3, 2 or 1 by tier.

| Tier | Who asks | Winning means | Headline metric |
| --- | --- | --- | --- |
| 1 Buy | Someone choosing a tool now: shortlist, alternative, price, "is it worth it", build or buy | We are named, ideally first | Named and named first, non-branded |
| 2 Problem | Someone with the pain we remove, deciding how to handle it | Our page cited as the method, us offered as the way | Cited, then named |
| 3 Authority | Someone learning the craft | Our page cited; a mention is a bonus | Cited |

### Prompt bars

Every prompt passes all five before it enters the set.

- **Blind-buyer test (overrides the rest):** would this persona type this
  exact question if they had never heard of us? A prompt that presupposes
  our solution, stacks marketing nouns or is a feature dressed as a
  question fails, however well it maps to our positioning.
- **One category name:** the name in `strategy/positioning.md`, never a
  synonym.
- **Relevance:** the asker is a buyer or user from `strategy/icp.md`, the
  job is one we do, and being the answer gives a real chance the reader is
  a fit. Relevance over volume.
- **Wording:** a person typing into a chatbot, not a marketer describing
  the pain; one intent per prompt.
- **Stable:** no year, price or version in the text, so it reads the same
  next year.

A prompt naming one competitor runs in the same wording for each tracked
competitor (the pairs rule), so a gap between them is the engines', not
the wording's.

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable. Typical:

- `2026-08-31-dataforseo-rankings.csv`: rank check for every keyword in the
  canonical table
- `2026-08-31-dataforseo-keyword-ideas.csv`: research output, pending triage
  into `keywords.csv`
- `2026-08-31-dataforseo-aeo-results.csv`: one row per prompt and engine,
  who is named and what is cited (`scripts/aeo_track.py`), with
  `-aeo-answers.csv` beside it holding the answer text; a hand-run drop
  uses the same columns under its own source (`manual-aeo-results.csv`)
- `2026-08-31-repo-aeo-scores.csv`: the scores `scripts/aeo_diff.py --save`
  computes from the results, for an unattended run

## For agents

- Weekly delta: diff the two most recent ranking snapshots (`seo-analyst`
  skill) and write the analysis to `reports/recurring/seo/`, not here.
- Pulls go through DataForSEO (see `integrations/README.md`). Keyword and
  rank pulls: `seo-analyst`. AI answer-engine visibility: `brand-monitor`
  (`scripts/aeo_track.py` collects, `scripts/aeo_diff.py` scores).
