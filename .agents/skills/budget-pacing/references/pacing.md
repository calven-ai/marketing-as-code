<!-- source: https://raw.githubusercontent.com/NEON-Rutger/B2B-revops-skills/main/revops-revenue-planning/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Pacing math, thresholds and the two inputs

The reforecast discipline (plan of record, named triggers, locked
parameters) is condensed from the revenue-planning skill above; the
formulas and the file shapes are this repo's.

## The plan of record

One budget per campaign, in `projects/<campaign>/campaign.md`, with its
period. Pacing compares spend to that line and to nothing else. When the
team changes a budget, the change is a diff to `campaign.md` with a
decision logged through `log-decision`; the pacing report never edits it.
Keep the original plan visible when a mid-period change happens: report
against the current plan and name the earlier one in Caveats.

Reforecast triggers worth borrowing: two consecutive months with actual
variance over 15% of plan, or a forecast that misses by more than 20%
twice, means the plan is wrong, not the spend. Say so in the report
instead of flagging the same campaign every week.

## Formulas

With `B` the period budget, `D` days in the period, `d` days elapsed
(through the last full day in the snapshot), `S` month-to-date spend,
`r7` the mean daily spend over the trailing 7 days:

- expected spend to date `E = B * d / D`
- pace index `P = S / E` (1.00 is on pace)
- projection `F = S + r7 * (D - d)`
- remaining `R = B - S`; runway in days `R / r7`
- invoice variance `(invoice - platform) / platform` for the last closed
  month, per platform account

Platforms can spend up to 2x the daily budget on a single day and even
out over the month; judge pace on the trailing 7 days, not on one day.

## Default thresholds (the team can change them in `campaign.md`)

| Flag | Condition |
| --- | --- |
| Over pace | `P > 1.15` and `F > B` |
| Under pace | `P < 0.85` for a campaign that is not impression-limited |
| Runway | runway shorter than `D - d` |
| Unplanned | spend on a campaign name that joins no project |
| Invoice variance | over 5%, or any invoice line with no platform account |
| Stale | platform snapshot older than 3 days at run time |

Under pace has two causes with opposite fixes: budget-limited (raise the
budget) and impression-limited (audience or rank; a budget change does
nothing). Google exposes lost impression share for budget and for rank;
LinkedIn shows audience penetration. Name the cause.

## Inputs

**Platform spend**: `data/ads/snapshots/YYYY-MM-DD-<vendor>-campaigns.csv`
with `campaign,platform,period_start,period_end,spend,impressions,clicks,conversions,cost_per_conversion,currency`
(the shape `ads-performance` writes). For pacing, pull month to date and
keep `period_start` at the first of the month. Daily budgets: Google Ads
`campaign_budget.amount_micros`; LinkedIn Campaign Manager shows Daily
Budget in the campaign list export.

**Finance export**: `data/ads/snapshots/YYYY-MM-DD-finance-invoices.csv`
with `invoice_date,platform,account,period_start,period_end,amount,currency,invoice_id`.
Ask finance for the ad-platform invoices of the last closed month; one row
per invoice. Company-level data only, no card numbers.

## Reading the variance

Fees on top of media (agency, LinkedIn's management fees), promotional
credits, VAT, currency conversion on the invoice date, and platforms that
invoice on a threshold rather than a calendar month all produce
differences. Under 5% is normal; over it, list the likely cause and ask
finance before calling it a problem.
