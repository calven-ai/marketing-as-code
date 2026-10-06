# brand/templates/

HTML templates that `scripts/brand_render.py` renders to exact-size PNGs
with headless Chrome. Colors, fonts and logos come from
[`../tokens.json`](../tokens.json) at render time; with it empty, images
render in a neutral grey default and the script says so. What goes into
them is [`../image-rules.md`](../image-rules.md).

| File | What |
| --- | --- |
| `banner.html` | Banners, covers, link previews: logo and one headline; the layout follows the aspect ratio |
| `post.html` | Feed posts: big type, optionally a screenshot or one stat |
| `icon.html` | The logo mark on a tile: app icons, avatars, marketplace logos |
| `shot.html` | One screenshot from `../screenshots/` at an exact size, no text |
| `template.js`, `template.css` | The shared runtime: reads the query string, applies tokens, fits the type |
| `sizes.json` | Every surface's size and safe area, with its spec source and the date it was verified |

```sh
python3 scripts/brand_render.py presets
python3 scripts/brand_render.py render post --preset portrait-4x5 --param "headline=Plans you can *diff*"
python3 scripts/brand_render.py og content/2026-09-why-plain-text-wins
python3 scripts/brand_render.py render banner --preset og --param headline=Hi --print-url   # open in a browser
```

PNGs land in `brand/renders/` (gitignored), because the spec reproduces
them. A new surface is a new entry in `sizes.json`: `source` is the
platform's own spec page, `verified` the day you checked it, `null` while
unconfirmed.
