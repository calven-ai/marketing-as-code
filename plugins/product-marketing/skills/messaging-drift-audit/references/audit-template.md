# Audit template

The exact structure to return. Open this in the Output step.

```markdown
# Messaging drift audit: <Company>, <YYYY-MM-DD>
Reference: <approved messaging, its date>. Surfaces checked: <n>. High <n>, medium <n>, low <n>, none <n>. Different company: <n>.

## Drift by surface
| Surface | URL or file | Scope (company / product) | Captured text (verbatim) | Severity | Assessment | Date |
| --- | --- | --- | --- | --- | --- | --- |
High first, then medium, low, none.

## Message coverage
| Message | <Surface 1> | <Surface 2> | <Surface 3> | ... |
| --- | --- | --- | --- | --- |
| Category label | verbatim / paraphrased / contradicted / absent | | | |
| One-liner | | | | |
| Pillar: <name> | | | | |
| Proof: <claim> | | | | |

## Vertical coverage
| Priority vertical | Matched variation or page | Level | Note |
| --- | --- | --- | --- |

## Competitor contrast: <Competitor>
| Their words (verbatim) | Our surface saying the same | What it means for the messaging |
| --- | --- | --- |

## Fixes
| # | Severity | Surface | Current (verbatim) | Replace with (from the reference) | Where to edit |
| --- | --- | --- | --- | --- | --- |

## Not checked
- <surface>: <not found / identity rejected / host marketing only / could not load>

## Sources
1. <title, URL or file name, date read>
```
