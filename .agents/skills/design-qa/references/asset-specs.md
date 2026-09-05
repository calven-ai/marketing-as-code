# Asset specs and the QA checklist

Dimensions, safe zones and the checks per channel. Platforms change their
specs; treat these as the starting point and confirm on the platform's
help page when a pixel matters.

## Dimensions by channel

| Channel | Asset | Size (px) | Notes |
| --- | --- | --- | --- |
| web | Open Graph and share image | 1200 × 630 | Keep text inside the middle 1000 × 500; some previews crop to 1:1 |
| web | Hero image | 1600 × 900 or wider | Provide a 1:1 crop for mobile |
| linkedin | Single image post | 1200 × 1200 or 1200 × 627 | Square gets more feed area |
| linkedin | Carousel (PDF) | 1080 × 1080 per page | Ten pages or fewer; readable at phone size |
| social | X image | 1600 × 900 | Timeline crops to 16:9 |
| social | Instagram feed | 1080 × 1350 | Portrait fills the feed |
| email | Header or hero | 600 wide, 2× for retina (1200) | Under 200 KB; alt text required |
| ad | LinkedIn single image | 1200 × 627 | Text at most 20 percent of the area reads better |
| ad | Meta feed | 1080 × 1080 and 1080 × 1350 | Both; the platform picks |
| webinar | Event card | 1920 × 1080 | Speaker photos at least 400 × 400 |
| pr | Logo for press | SVG plus 2000 px PNG on transparent | Both the primary and the mark |
| talk | Slides | 1920 × 1080 | Titles at least 40 pt |

## The checklist

1. Tokens: every colour on the asset is a token value or a tint the
   identity file allows; fonts are the token fonts or their fallbacks.
2. Logo: the right version for the background; clear space at least the
   height of the mark on all sides; not stretched, recoloured or placed
   on a busy area; not below the minimum size the identity file states.
3. Contrast: body text at least 4.5:1 against its background, large text
   3:1 (WCAG AA); check the worst spot, not the average.
4. Legibility at size: read the asset at the size it will appear (a
   phone for social, a thumbnail for share images).
5. Safe zones: nothing important within 5 percent of the edge, and clear
   of the platform's overlays (profile picture, captions, buttons).
6. Imagery: matches the identity file's style, subject and mood; no stock
   image that a competitor could use; people shown with consent.
7. Copy: passes `brand/voice.md` and the banned list; no orphaned words;
   product names as the glossary spells them.
8. File: right format (SVG for logos, PNG for flat graphics, JPEG for
   photos, PDF for carousels), right size, named `<piece>-<channel>-<size>`,
   saved in the piece's folder, alt text written in the brief.

## The design brief (`assets.md`)

Purpose and channel; dimensions from the table; the one-line message;
the copy that appears on the asset, final; imagery direction from the
identity file (style, subject, mood, what to avoid); tokens by name;
the template to start from, if any; two or three references; owner, due
date, where the file goes.
