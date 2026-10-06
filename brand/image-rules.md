# Image rules

What goes into a banner, post, icon or screenshot rendered from `templates/`
by `scripts/brand_render.py`. The templates apply the look from
[tokens.json](tokens.json); these rules govern the content. The renderer
accepts content only and refuses style options.

## Copy

- **Say what the viewer gets.** Someone glancing at the image learns what
  the product does for them on that surface. A name plus a platform
  ("[Product] for [platform]", "[Product] x [platform]") says nothing: the
  logo already shows who you are. Name the outcome in the viewer's terms:
  "Turn [platform] calls into *battle cards*".
- **One gradient phrase** of up to three words, marked `*like this*`, on
  the outcome, never on your name or a partner's.
- **Banners:** the headline is the only text. At most two lines and about
  40 characters (the renderer refuses past 45). No eyebrow, no subline.
- **Posts:** up to three lines and about 50 characters (refused past 60).
  The post copy carries the rest.
- Copy comes from `strategy/messaging.md` and passes [voice.md](voice.md).

## Look (set by the templates)

- **Surface:** `colors.background` with `colors.text`. `theme=inverse`
  swaps them; use it only when a surface demands the other background and
  say why.
- **Glow:** exactly one, `colors.primary` into `colors.accent`, its centre
  outside the frame below the bottom right, so only the rim enters.
- **Logo:** `logo.primary`, top left on wide and tall shapes, at the right
  end of strips wider than 4:1. Icons use `logo.mark`.
- **Alignment:** left. A banner without a headline centres the logo; that
  is the only centred case.
- **Sizing:** one rule for every banner shape: the headline starts at 5.7%
  of the width, capped at 24% of the safe height (22% on strips), and
  shrinks until it fits; the logo is 3.7% of the width. These are the
  proportions of a 1200x630 link preview with 68 px type, so it reads at
  thumbnail size. The empty space is deliberate: do not ask for bigger type.
- **Never:** stock photos, extra shapes, patterns, a second glow, or
  accent colors as fills.

## Posts

A feed image must stop the scroll on a phone, where a 1080 px image shows
about 380 px wide.

- **Type** is never a fixed size: the headline grows or shrinks until its
  ink covers a fixed share of the safe area (28% square and portrait, 32%
  landscape; 19% and 22% with a screenshot), so long copy sets smaller and
  every post keeps the same space around its text.
- **Margins:** 7% of the width on every side. Keep anything that matters
  out of the bottom 12%, where LinkedIn can overlay the engagement bar.
- **Screenshot** (`shot`) whenever the post is about the product; text only
  for opinions, announcements and quotes. Pass a file name from
  `screenshots/`, never an outside image, and pick the screenshot whose
  top-left area shows what the headline claims. `focus=x,y` zooms to one
  feature, because a whole app screen is unreadable at phone size.
- **Stat** (`stat`): one real number of at most 6 characters (`3x`,
  `41%`), shown huge in the gradient with the headline as the claim
  beneath. Only figures from a snapshot in `data/` or a cited source,
  never invented. A stat post carries no screenshot, and the stat is its
  only gradient.
- **Formats:** portrait 4:5 (`portrait-4x5`) is the default feed format,
  about a quarter more room than square in a phone feed; square next;
  landscape (`linkedin-post`, `x-post`) for link-style posts and X.

## Safe areas

The `safe` insets in `templates/sizes.json` encode what each surface
covers or crops; check them whenever you add or verify a preset.

- **LinkedIn company cover:** the Page logo overlaps the lower left on
  desktop, so text starts 300 px in.
- **LinkedIn personal background:** the profile photo covers the lower
  left; content stays in the central 1260x300.
- **X header:** the avatar covers the lower left and mobile crops about
  60 px top and bottom; the bottom inset is 110 px.
- **YouTube banner:** only the centre 1546x423 shows on every device.

Each surface shows images at its own display size, so the same rule gives
different pixel sizes per surface. That is expected.
