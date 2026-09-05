<!-- source: https://raw.githubusercontent.com/seranking/seo-skills/main/skills/seo-backlinks-profile/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Profile health: composition, quality, diversity, trend, risk

Condensed from SE Ranking's backlinks-profile skill. One index per
report: never blend vendors, because their definitions of a backlink,
their crawls and their authority scales differ and the ratios turn into
noise. A cross-source check before a disavow is a manual research task.

## Top-line numbers

Backlinks, referring domains, dofollow share, unique IPs and subnets,
domain-to-subnet ratio, new and lost referring domains last 30 days,
toxic candidates flagged.

## Authority histogram

Bucket referring domains by authority (70+, 50 to 69, 30 to 49, 10 to 29,
0 to 9). A healthy profile has a long tail; concentration under 10 is the
warning sign.

## Anchor classes and healthy ranges

| Class | Healthy share |
| --- | --- |
| Branded (contains the brand) | 30 to 60 percent, the largest class |
| Generic ("read more", "this page") | 15 to 30 percent |
| Naked URL | 10 to 25 percent |
| Partial match | 10 to 20 percent |
| Exact-match commercial | under 5 percent; more reads as over-optimised |
| Image alt | under 10 percent |

## Diversity

Referring domains divided by unique /24 subnets: 3 to 10 is normal; many
domains on few subnets is a private-network signal.

## Trend

Net new referring domains per month over six months. Steady growth of 10
to 20 percent a year is healthy; a spike over 50 percent in a month often
means paid links; a sharp loss deserves a look at which domains went.

## Toxic candidates (two or more triggers)

- Authority under 10.
- Sitewide links (more than five pages of one domain link to us).
- Exact-match commercial anchor on more than half of a domain's links.
- Hosted in a concentrated subnet.
- Unpronounceable domain name.
- TLD from a high-spam list (verify against a current report).

Output a reviewable list with `risk_score` and `triggers`. Never disavow
from a skill; removal by request comes first, and a domain that sends
referral traffic is never disavowed.

## Health score (100)

Twenty points each for authority distribution, anchor diversity, IP and
subnet diversity, growth trajectory, toxic-candidate ratio. Re-run against
the same index a quarter later and the delta means something.

## Report sections

Health score table, top-line numbers, authority histogram, anchor table
with status against the ranges, six-month trend, toxic candidates (top
ten), next steps for a person.
