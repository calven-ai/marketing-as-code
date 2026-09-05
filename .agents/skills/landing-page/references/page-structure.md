<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/copywriting/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Landing page structure, formulas and the pre-ship list

The section order and the headline and CTA formulas are condensed from
the copywriting skill above; the framework choice, the checklist and the
SEO fields are this repo's.

## Sections, in order

1. **Above the fold**: headline, subheadline, primary CTA, one line of
   risk reversal (free trial, no card, cancel any time).
2. **Proof**: logos, a number, one short quote, close to the first CTA.
3. **Problem**: the situation in the persona's words (from reviews,
   calls, `memory/knowledge/`), so they recognise themselves.
4. **Solution as outcomes**: three to five benefits, each "so you can
   <outcome>", never a feature list.
5. **How it works**: exactly three steps, from the barrier-lowering first
   step to the outcome.
6. **Objections**: five to seven, as FAQ, comparison or guarantee: cost,
   setup time, whether it works, lock-in, security, support.
7. **Final CTA**: restate the value, repeat the CTA, repeat the risk
   reversal. The primary CTA appears at least three times on a long page.

Pick the argument's shape by traffic temperature: problem, agitate,
solve for cold traffic; attention, interest, desire, action for a known
category; before, after, bridge for a transformation; a feature-benefit
grid for a technical buyer who already wants the details.

## Headline formulas

- "<Outcome> without <pain>"
- "The <category> for <audience>"
- "Never <unpleasant event> again"
- A question that names the pain
- The winning ad headline, verbatim (message match)

Ten words or fewer; specific beats clever. Subheadline: "<Product> helps
<audience> <outcome> by <mechanism>". Test with "now you can": if the
sentence works after those words, it is a benefit.

## CTA rules

Action verb plus what they get plus a qualifier when needed: "Start the
free trial", "Get the checklist", "See pricing for my team". First person
often wins ("Start my trial"). Never "Submit", "Sign up", "Learn more",
"Click here". Risk reversal next to every CTA.

## Copy principles

Clarity over cleverness; benefits over features; specifics over
"streamline" and "optimise"; the customer's words over ours; active
voice; honest over sensational; one idea per section. Remove exclamation
marks and buzzwords without substance.

## SEO fields, at the end of the draft

- Meta title: "<Product>: <primary benefit> | <Brand>", 50 to 60
  characters.
- Meta description: "<Product> helps <audience> <outcome>. <Proof>.
  <CTA>.", 150 to 160 characters.
- Schema: `Product`, `SoftwareApplication`, `Organization` or `FAQPage`
  as JSON-LD; the target keyword in the first 100 words if the page is
  meant to rank (check `data/seo/keywords.csv`).

## Before it ships

- One primary action; navigation minimal or removed on a paid page.
- Headline matches the ad or email that sends the traffic.
- Proof within one screen of every CTA; testimonials carry name, role,
  company and a specific outcome, all approved.
- Works at 375 px; loads under 2.5 s mobile LCP; no external scripts the
  prototype does not need.
- Form asks only what the team will use; UTMs carried into the
  submission; the conversion event fires (`data/ontology/events.md`).
- Every claim has a source in the brief; urgency only when it is real.
- Reviewed by `review`, then a person.
