---
source: repo
last_reviewed: 2026-09-30
owner: Tomas Berg
---

# Visual identity

A light in the dark: night-blue surfaces, one warm amber signal, a lot of
calm space. Nothing on a Beacon page should look like an alarm.

## Colors

| Role | Hex | Usage |
| --- | --- | --- |
| Primary | `#F2A93B` | Beacon amber: the mark, links, the one button that matters |
| Secondary | `#1E3A5F` | Harbour navy: panels, cards, wordmark on light backgrounds |
| Background | `#0F1B2D` | Night: the default surface for site, images and slides |
| Text | `#F4F1EA` | Paper: body and headings on night; the light surface for `theme=inverse` |
| Accent / success / warning | `#FFD27A` | Glow: the end of the amber gradient and highlights; never a fill |

- **Night is the default** for anything marketing: site, banners, social,
  slides. Paper is for documents and partners that need a light page.
- **Amber is a signal, not a fill:** the mark, one gradient phrase, one
  button. A page that is mostly amber has lost the point.
- **Navy is structure:** panels and cards on night, the wordmark on paper.
  Never body text on night; it fails contrast.
- Red is for the product's own incident states only, never for marketing.

## Typography

- Headings: Space Grotesk, 500 and 700, loaded from Google Fonts.
- Body: Inter, 400 and 600, loaded from Google Fonts.
- Fallback stack: system-ui, -apple-system, sans-serif.

## Logo usage

- Files live in `logos/`: `primary.svg` (mark and wordmark, paper text) and
  `mark.svg` for night backgrounds; `primary-inverse.svg` and
  `mark-inverse.svg` (navy text) for light ones.
- Clear space on every side: the height of the mark's dot times two.
  Minimum width 96 px for the full logo, 20 px for the mark.
- Never recolour, stretch, outline, add a shadow, or set the wordmark
  without the mark.

## Imagery

Product UI and type, no photography and no stock. Screenshots are
stylised, on night, with real Beacon wording (templates, segments,
updates) rather than lorem ipsum. One amber glow per image at most;
illustrations, when needed, are flat line drawings in paper and amber.

## Templates

`templates/` renders banners, posts and icons in the colors, fonts and logos
of [tokens.json](tokens.json) (`scripts/brand_render.py`); what goes into
them is [image-rules.md](image-rules.md).
