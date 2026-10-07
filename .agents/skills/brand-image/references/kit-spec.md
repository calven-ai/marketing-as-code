# kit.json: the render spec of a listing kit

Plain text, next to the kit's `draft.md`; `scripts/brand_render.py batch`
renders it. Strict JSON.

```json
{
  "out": "brand/renders/2026-10-chrome-web-store-listing",
  "jobs": [
    {"file": "icon.png", "preset": "chrome-icon"},
    {"file": "promo-small.png", "preset": "chrome-promo-small", "headline": "Every tab, *summarised*"},
    {"file": "gallery-1.png", "preset": "linkedin-post", "template": "post",
     "headline": "Read the page you are on, *faster*", "shot": "dashboard.png"},
    {"file": "screenshot-1.png", "preset": "chrome-screenshot", "template": "shot", "shot": "dashboard.png"},
    {"file": "cover.png", "template": "banner", "size": "1800x320", "headline": "..."}
  ]
}
```

- `out` is relative to the repo root and optional; the default is
  `brand/renders/<the kit's folder name>/`, which is gitignored.
- `file` is a plain name ending in `.png`.
- A job takes `preset` (its size, safe area, template and icon defaults)
  or `size` (`WxH`, default safe area), and `template` to override the
  preset's.
- Content params per template: `banner` headline, theme; `post` headline,
  stat, shot, focus, theme; `icon` bg, mark, pad, radius; `shot` shot,
  fit, focus. `theme` is `brand` or `inverse`; `bg` is `brand`, `inverse`,
  `transparent` or `glow`; `mark` is `mark` or `primary`; `fit` is
  `contain` or `cover`; `focus` is `x,y` between 0 and 1. Anything else is
  refused, and every job is validated before Chrome starts.
- `max_kb` comes from the preset; `batch` and `check <kit.json>` fail a
  PNG that is the wrong size or over it.
