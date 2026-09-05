<!-- source: https://raw.githubusercontent.com/thatrebeccarae/claude-marketing/main/skills/brand-dna/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Reading the visual identity off an asset or a page

Condensed from the brand DNA skill in claude-marketing. The source
extracts a brand profile from a website; the same attributes are what
design QA compares against `brand/tokens.json` and
`brand/visual-identity.md`.

## Attributes to extract

| Attribute | Where to read it | Compare against |
| --- | --- | --- |
| Colours: primary, secondary, background, text | The hero, primary button, header; on a page, the CSS on those elements | `colors` in `brand/tokens.json` |
| Typography: heading and body | Font declarations on headings and body; font imports | `fonts` in `brand/tokens.json` |
| Imagery style | Photography, illustration, flat, 3D; subject (people, product, abstract); mood (clean, busy, dark, airy) | The imagery section of `brand/visual-identity.md` |
| Voice signals in the copy | Headline, hero copy, calls to action | `brand/voice.md` |
| Aesthetic qualities | Mood words, texture, how much negative space | The identity file's imagery and layout notes |

Dark mode: if the background is dark, the token roles swap; check that
the asset used the dark variant rather than inverting the light one.

## Voice signals on a scale

The source scores copy on 1 to 10 axes, neutral at 5: formal to casual,
expert to accessible, bold to subtle, rational to emotional, traditional
to innovative, playful to serious. A single asset does not need the
number; it needs to sit on the same side as the guide's three
adjectives.

## Procedure the source uses

1. Get the URL or the file; do not proceed without it.
2. Read the homepage first, then about and product pages (skipped in
   quick mode).
3. Extract colours, fonts, voice signals, imagery, values, audience.
4. Build the profile with `null` for anything not confidently seen; never
   guess.
5. Show a summary: name, voice descriptors, primary colour, typography,
   audience.

## Confidence

Sparse pages and JavaScript-rendered elements lower confidence; say so.
For design QA, "could not read the font from a flattened PNG" is a
finding for the person, not a pass.

## Output

The source writes a JSON profile other tools read. Here the equivalent is
`brand/tokens.json`, which already exists; QA reports the deltas between
what the asset shows and what the tokens say.
