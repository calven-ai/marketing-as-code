---
name: prototype-builder
description: Build a disposable prototype in playgrounds/ from a one-sentence idea. Use when someone wants to bring a prototype to a meeting instead of a deck - a landing page mock, campaign concept page, email sequence preview, ad variant board, or storyboard.
license: MIT
metadata:
  kind: workflow
  area: core
  needs: []
  writes: repo
  runs: person
---

# Prototype builder

Come to meetings with the thing itself, not a deck about it. Build the
smallest artifact that makes the idea judgeable.

## Procedure

1. **Load `brand/`** (voice, visual identity, `tokens.json`) and the
   relevant `strategy/` context. On-brand prototypes get judged on the idea;
   off-brand ones get judged on the wrong fonts.
2. **Create `playgrounds/YYYY-MM-DD-<slug>/`** containing:
   - The prototype itself. Default form: **a single self-contained HTML
     file** (inline CSS, brand tokens applied, no build step, no CDN) that
     opens in any browser. An email sequence is one page showing each email
     in sequence; an ad board is one page of variants side by side.
   - A `README.md`: the one-sentence idea, what feedback is sought, and
     "disposable: decision goes to memory/decision-log.md".
3. **Fake honestly.** Placeholder metrics, imagery, and quotes are fine if
   you label them as fake in-context (e.g. "[illustrative]"). Never
   fabricate a real customer's endorsement.
4. **After the meeting** (when told the outcome): log the decision via
   `log-decision`, then move the prototype folder to
   `playgrounds/_archive/`.

## Rules

- Never production: nothing in `playgrounds/` ships, gets published, or gets
  linked externally.
- Speed beats polish, brand beats speed: rough is fine, off-voice is not.
