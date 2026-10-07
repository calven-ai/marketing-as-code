# The keyword set

`data/seo/keywords.csv` is the one keyword list. Research output is
proposed in a report, never kept as a second file.

## One panel with the prompt set

The keyword set and `data/seo/prompts.csv` are one panel seen from two
surfaces, with the tiers and tracks defined in `data/seo/README.md`.

- A keyword that is the search form of a prompt names it in `aeo_prompts`
  and takes its tier and track.
- `seo_diff.py` prints the crosswalk and exits 1 on a broken reference:

| Check | Rule |
| --- | --- |
| `missing_prompts` | 0: a keyword never names a retired or unknown prompt id |
| `uncovered_pages` | 0: every page an active tier-1 or tier-2 prompt targets has a tracked keyword |
| `tier_mismatch`, `track_mismatch` | 0: a keyword takes the tier and track of the prompts it names |
| `unmapped_prompts` | informational: a prompt with no searchable head term stays unmapped |

- Paired keywords (two competitors, two engines) run in the same wording,
  as their prompts do.
- Branded keywords sit in the `brand` track and mirror the branded prompts.

## Freeze and quarterly review

The set is a fixed panel between reviews, so ranks compare. Between reviews,
change only a broken row (a keyword Google reads differently), the
`aeo_prompts` mapping when the prompt set changed, or a `target_url` once
the page it names is live. Never edit a keyword's text in place: delete the
row, log it under Set log in `memory/knowledge/seo-memory.md`, and add a
new id; ids are never reused.

Once a quarter, on the same calendar as the prompt set, the report proposes
at most 10 additions and 10 retirements (keyword, track, tier, target page,
prompt ids, source, volume). A person approves; the change lands as a
proposal and takes effect at the next pull.

Candidates come from memory's Candidates list: untracked Search Console
queries with impressions (`seo_diff.py`, `candidates`), People Also Ask and
related searches in the `-serp-results.csv` snapshot, and keywords other
roles hand over. Keep only terms that fit a track and that the team would
be glad to win. Question-shaped candidates are prompt candidates too: list
them under Hand-offs for `prompt-set-builder`.
