# Funnel and lifecycle stages

> **Template: unfilled.** Type over the brackets, or say `/setup` and answer a
> few questions. Agents: ask rather than assume stage semantics.

## Stages, in order

| Stage | Entry condition (exact) | Exit → next stage when | Lives in |
| --- | --- | --- | --- |
| [Visitor] | | | [analytics] |
| [Signup] | | | |
| [MQL] | | | [CRM] |
| [SQL] | | | |
| [Opportunity] | | | |
| [Customer] | | | |

## Rules of interpretation

- [Can a record skip stages? Move backwards? What does that mean in the
  data?]
- [Which system is authoritative when CRM and analytics disagree?]
- [Attribution: what model the team actually uses when saying "X came from
  Y".]

## From the website to the conversion

When the conversion happens outside the website's analytics (a product
sign-up, a CRM form), the website and the product cannot share a session.
The join is forwarded parameters, never identity: every link into the
conversion carries the session's entry attribution (the original `utm_*`
and `ref` when present, else `utm_source` and `utm_medium` derived from
the referrer by the channel rules in `naming.md`), plus `landing` (the
entry path) and `content_type`. The receiving system stores them on the
new record, and the CTA click event carries the same values, so a click
and the record it became agree on source, landing page and content type.
