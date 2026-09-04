# Stripe (source token `stripe`; category `billing`, domain `data/crm/`)

Routes (from `integrations/catalog/billing.json`): the remote MCP server
`stripe` (OAuth for a person; a restricted key `STRIPE_RESTRICTED_KEY` with
`stripe_api_read` only makes it headless and read-only), or the `stripe`
CLI in a workflow step (`stripe get /v1/subscriptions --limit 100`, JSON
out). The server can write with a key that has `stripe_api_write`; never
wire one. Billing snapshots land in `data/crm/` next to the CRM's.

## Calls per snapshot

Tool names are not verified in the catalog; check the tool list in the
session (list customers, list subscriptions, list invoices). The API
behind them:

| `<what>` | Endpoint |
| --- | --- |
| subscriptions | `GET /v1/subscriptions?status=all&limit=100&expand[]=data.customer` paged with `starting_after`; drop `incomplete` and `incomplete_expired` |
| customers | `GET /v1/customers?limit=100` when the CRM has no customer table; company from `name` or `metadata` |
| invoices (ad hoc) | `GET /v1/invoices?created[gte]=<epoch>&limit=100`, one row per paid invoice, for revenue by month |

Prefer the subscriptions call for MRR and churn questions; invoices for
cash. Say which one a number comes from.

## Mapping to the snapshot columns

`subscription_id` = `id`; `customer_id` = `customer` (the `cus_` id);
`company` = the expanded customer's `name`; `plan` = the first item's
`price.nickname` or `price.product` name; `status` = `status` as returned
(`active`, `trialing`, `past_due`, `canceled`, `unpaid`); `mrr` = the sum
over items of `quantity * price.unit_amount / 100`, divided by 12 for
yearly prices (or `interval_count` months); `currency` = the price
currency; `started` = `start_date`; `current_period_end`,
`canceled_at` = the same fields as ISO dates. Customer emails never enter
the snapshot.

## Limits and cost

- 100 objects per page; a 2,000-subscription account is 20 calls.
- Live mode allows on the order of 100 read requests per second; the
  snapshot is far below it.
- Amounts are in the smallest currency unit (cents); convert once, in
  the pull.
- Cost: free.

## Export fallback

Billing > Subscriptions > Export (CSV, all columns, the status filter
set to all). Drop at `data/crm/snapshots/YYYY-MM-DD-stripe-subscriptions.csv`,
remove the email column, compute `mrr` from the plan amount and interval,
and rename the columns to the snapshot set.
