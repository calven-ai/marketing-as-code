<!-- source: https://raw.githubusercontent.com/NEON-Rutger/B2B-revops-skills/main/revops-data-governance/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Data quality dimensions, rules and the score

## The five dimensions

| Dimension | Measures | Target |
| --- | --- | --- |
| Completeness | records with every required field filled, per stage | 95% |
| Accuracy | a sample of 50 to 100 records checked against the source (website, invoice, enrichment) | 90% |
| Consistency | the same fact identical across systems (CRM vs billing vs marketing automation) | 99% |
| Timeliness | stage changes recorded within two business days; activity current | 85% |
| Uniqueness | no duplicate contacts per account, no duplicate accounts per domain | 99% |

```
score = completeness * 0.25 + accuracy * 0.25 + consistency * 0.25
      + timeliness * 0.15 + uniqueness * 0.10
```

Target 85% or better, monthly. A dimension the snapshots cannot measure
(accuracy needs a sample check, consistency needs a second system) is
reported as unmeasured and left out of the score with the weights
renormalised; say so.

## Required fields, kept minimal

- Contact: email, first name, last name, account link.
- Opportunity: account link, name, stage, close date (amount and owner
  are the report's additions).
- Subscription or customer: ARR, contract dates, renewal date, discount.
- A contact tied to five or more accounts is a data error, not a fact.

## Duplicate rules

- Exact match (high confidence): email; domain plus company size; phone.
- Fuzzy match (review): name variants ("Acme Corp" vs "ACME
  CORPORATION"); propose, never auto-merge.
- Survivor: the most complete and most recently active contact; the older
  account; every activity, opportunity and subscription moves to the
  survivor; never merge a parent into a subsidiary; log every merge with
  who approved it.
- Before creation: link, create, review or reject. Reject a contact with
  no email and no phone, an account with no domain and no legal entity.

## Prevention rules to propose

- Validation: email format, phone country code, no past dates except
  close date, stages move forward without approval.
- Picklists over free text for stage, industry, deal type, region, source.
- Defaults: currency, initial stage, country inherited from the account.
- Every active field has an owner and a documented use; a field with
  neither is a deprecation candidate (announce two weeks, migrate four,
  hide two, delete after six months with an archive export).
- One system owns each fact: account name in the CRM, revenue in billing
  synced one way, stage in the CRM, subscription dates in finance.
  Bidirectional sync needs a written conflict rule.

## Cadence and escalation

| When | Scope | Escalate when |
| --- | --- | --- |
| weekly | automated scans: fuzzy duplicate accounts, null required fields, stage anomalies, sync failures | more than five new duplicates; three sync failures in a week |
| monthly | this report: the score, its trend, the fix list | any dimension under 85% |
| quarterly | sample audits: 5% of closed opportunities, churned accounts and enriched records | |
| annually | field audit: unused three months or more is a deprecation candidate | |

Anomalies worth a same-day flag: a close date in the past on an open
deal, a single opportunity far above the largest ever won, a stage change
with no activity for 30 days, a deal that closed in under three days or
took over a year.

## Naming, when the team asks

Prefixes by owner keep custom fields findable: `mktg_`, `sales_`, `cs_`,
`rev_`, `int_` (integration), `calc_` (formula). No `tmp_`, `test_`, `x_`.
