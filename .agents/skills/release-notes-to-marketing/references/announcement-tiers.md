# Announcement tiers and the shape of each asset

Which changes deserve which assets, and what each asset holds. The tier
is a judgment the person confirms; the shapes are fixed so the drafts
compare across releases.

## Tiers

| Tier | Typical change | Assets | Also |
| --- | --- | --- | --- |
| Major | New product, new module, a capability that changes how a persona works, a pricing or packaging change | Email, LinkedIn post, blog post | Suggest `launch-plan`; sales gets a note through `sales-enablement-kit` |
| Medium | A notable feature, a new integration, a visible redesign | Email, LinkedIn post | The blog gets it in the next roundup |
| Minor | Small improvements, performance, fixes | One paragraph in the next "what's new" roundup | Nothing standalone |
| Silent | Internal changes, security patches the team does not announce, deprecations with their own notice | Nothing | Ask before writing anything about a deprecation |

Two mediums shipping in the same week can be bundled into one major-style
email; three minors are still a roundup.

## The translation grid

One row per change that makes the cut:

| Change (product brief name) | Type | Persona | Why it matters (their words) | What to do | Pillar |
| --- | --- | --- | --- | --- | --- |

The "why it matters" cell is the whole job. If it reads like the changelog
line with "now you can" in front, it is not done; it should name the pain
from `strategy/personas.md` that goes away.

## Email

- Subject: the one change that matters most, under 50 characters, no
  "exciting".
- Preview line: the second change, or the outcome.
- Body: changes in order of customer impact, each as a bold lead and one
  or two sentences; a single call to action at the end; a link to the
  full notes.
- Footer facts: who has it, from when, any action required.

## LinkedIn post

One change, one persona, one outcome, in the voice's register; the first
line does the work because the rest is folded. No bullet list of features,
no hashtag pile. A question or a concrete before-and-after beats "we're
thrilled".

## Blog post

Title says what shipped; an opening paragraph on why (the pillar); one
section per change with what, why it matters, how to use it, and where a
screenshot goes (a request to `design-qa`, not a placeholder image);
availability and next steps at the end.

## What to leave out

Internal ticket ids, engineering detail the persona does not act on,
fixes for problems the customer never saw, and anything embargoed. Say in
the hand-over what was left out so the person can pull it back in.
