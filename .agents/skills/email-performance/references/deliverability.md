# Deliverability: what to read, the thresholds, the fixes

Nothing here is a target; the team's own history in
`data/email/snapshots/` comes first. These are the levels at which
mailbox providers start treating a sender differently.

## DNS records, read as data

Look up the sending domain (and any subdomain the tool sends from) with
`dig TXT <domain>` or the team's DNS console, and save one row per record
to `data/email/snapshots/YYYY-MM-DD-web-dns.csv` with
`domain,record,value,verdict`:

- **SPF**: a TXT record starting `v=spf1` that includes the sending
  tool's include and ends `~all` or `-all`. More than ten DNS lookups in
  the chain fails silently; count them.
- **DKIM**: a TXT record at `<selector>._domainkey.<domain>` for the
  selector the tool gave; the tool's settings page shows whether it
  verifies.
- **DMARC**: a TXT record at `_dmarc.<domain>` starting `v=DMARC1`. `p=none`
  only reports; `p=quarantine` or `p=reject` protects. `rua=` should point
  at an address someone reads.
- **Custom tracking domain**: links should resolve to the team's domain,
  not the tool's shared one.

Gmail and Yahoo require SPF and DKIM alignment, a DMARC record, one-click
unsubscribe headers and a complaint rate under 0.3% (aim under 0.1%) for
anyone sending about 5,000 messages a day.

## Rates and thresholds

| Metric | Computed as | Watch | Act |
| --- | --- | --- | --- |
| Delivery rate | delivered / sent | under 98% | under 95% |
| Hard bounce rate | hard bounces / sent | over 1% | over 2% |
| Spam complaint rate | complaints / delivered | over 0.1% | over 0.3% |
| Unsubscribe rate | unsubscribes / delivered | over 0.5% on one send | over 1% |
| Click rate | unique clicks / delivered | falling three months running | |
| Open rate | unique opens / delivered | falling on every send at once | |

Open rates are inflated by clients that prefetch images (Apple Mail
Privacy Protection) and vary by audience; report them, lead with clicks
and replies. A simultaneous drop in opens across all sends with steady
clicks per open is a placement change (spam or promotions tab), not a
content change.

## Common causes and the fix a person makes

- Hard bounces up after a list import: the import was old or bought;
  remove the bounced addresses, stop mailing the segment, and never
  re-import.
- Complaints up on one send: the segment did not expect it; check the
  consent source and the unsubscribe link's visibility.
- Opens down everywhere: authentication changed, a new sending domain,
  or a spam trap hit; check DNS first, then the tool's reputation panel,
  then Google Postmaster Tools for the domain.
- Engagement decaying in a sequence step: rewrite that step
  (`nurture-sequence`) or shorten the sequence.
- A segment that has not opened or clicked in 90 to 180 days: propose a
  re-engagement sequence, then suppression; sending to the unengaged
  lowers placement for everyone.

## What this skill never does

It never sends a test, edits a record, changes a list or a suppression.
It reads, computes, and writes the fix as a proposal in the report.
