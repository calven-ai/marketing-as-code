<!-- source: https://raw.githubusercontent.com/thatrebeccarae/claude-marketing/main/skills/utm-attribution-strategy/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# UTM governance and the attribution settings they feed

## Governance rules

- Lowercase only; the analytics tools are case-sensitive.
- Hyphens between words; no spaces, no underscores mixed with hyphens.
- Short, descriptive values; the convention is written down once
  (`data/ontology/naming.md`) and enforced at build time, not in the
  report.
- Three parameters are mandatory (`utm_source`, `utm_medium`,
  `utm_campaign`); `utm_term` for paid keywords, `utm_content` for
  variants.
- Patterns that have worked: campaign `<initiative>-<audience>-<date>`,
  content `<format>-<variant>-<placement>` (`video-testimonial-feed`,
  `cta-start-trial-hero`).

## Pitfalls that corrupt attribution

1. UTMs on internal navigation: the visitor's real source is overwritten
   by the site itself.
2. Inconsistent capitalisation across teams and tools.
3. `utm_medium` left empty, so the traffic is Unassigned.
4. Non-standard medium values that fall outside the default channel
   grouping.
5. Personal data in a parameter (a name, an email, a customer id):
   a privacy problem and a reporting mess.
6. Tagging organic Google traffic by hand, which double-counts it as a
   campaign.
7. Redirects that drop the query string (some 302s, link shorteners,
   app deep links); test the final URL, not the one you built.

## Build and check procedure

1. Audit existing links against the rules above before adding more.
2. Document the taxonomy and get the team's sign-off.
3. Build links from templates per channel.
4. Validate: no mixed case, no spaces, no PII, every value in the list.
5. Test that redirects keep the parameters.
6. Watch the analytics channel grouping for "(other)" and "Unassigned"
   as the signal that a link slipped through.
7. Review the attribution model quarterly against the sales cycle.

## Attribution model by cycle length (for `attribution-analysis`)

| Sales cycle | Model to report on |
| --- | --- |
| under 7 days | last click, or data-driven when the volume is there |
| 7 to 30 days | position-based, or data-driven |
| over 30 days | time decay, or data-driven |

GA4's models: last click, first click, linear, time decay,
position-based (40/40/20), data-driven (needs on the order of a thousand
conversions a month). Set in Admin > Attribution settings; default
lookback 30 days for clicks and 7 days for views. Record the setting in
any report that quotes GA4 conversions, because changing it changes the
history.
