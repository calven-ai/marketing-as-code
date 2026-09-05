<!-- source: https://raw.githubusercontent.com/thatrebeccarae/claude-marketing/main/skills/google-ads/CHECKS.md | license: MIT | fetched: 2026-09-04 -->

# Google Ads audit checks (74)

Pass conditions condensed from the checklist above. Score each pass, fail,
unknown or not applicable, with the snapshot and number that decided it.

## Conversion tracking (11)

| Id | Check | Pass when |
| --- | --- | --- |
| CT1 | Primary conversion action exists | one primary action, with conversions in the last 30 days |
| CT2 | Enhanced conversions | active and verified |
| CT3 | Server-side tracking | deployed and verified (unknown via API) |
| CT4 | Consent Mode v2 (EU/EEA traffic) | advanced mode with a CMP (unknown via API) |
| CT5 | Conversion window matches the sales cycle | 30 to 90 days for B2B, 30 for lead gen, 7 for ecommerce |
| CT6 | Macro versus micro separation | primaries are macro conversions; micro events are secondary |
| CT7 | Attribution model | data-driven |
| CT8 | Conversion values | dynamic for ecommerce; value rules for lead gen |
| CT9 | No duplicate counting | GA4 and Ads do not both count the same action as primary |
| CT10 | GA4 linked | linked, audiences shared, numbers consistent |
| CT11 | Google tag fires on every page | verified by a person |

## Wasted spend and negatives (8)

| Id | Check | Pass when |
| --- | --- | --- |
| WS1 | Search terms reviewed | within the last 14 days |
| WS2 | Negative lists exist | at least 3 themed lists (competitor, jobs, free, irrelevant) |
| WS3 | Lists applied | at account level or to every relevant campaign |
| WS4 | Irrelevant term spend | under 5% of spend in 30 days |
| WS5 | Broad match pairing | every broad keyword runs under smart bidding |
| WS6 | Close variants | over 90% relevant |
| WS7 | Search term visibility | over 60% of search spend visible in the report |
| WS8 | Zero-conversion keywords | none with over 100 clicks and 0 conversions |

## Account structure (12)

| Id | Check | Pass when |
| --- | --- | --- |
| ST1, ST2 | Campaign and ad group naming | one consistent pattern (this repo: `data/ontology/naming.md`) |
| ST3 | Single-theme ad groups | 10 or fewer keywords, one theme |
| ST4 | Campaigns per objective | 5 or fewer per funnel stage |
| ST5 | Brand and non-brand separated | own campaigns, budgets and bidding |
| ST6 | PMax present where eligible | active with proper asset groups |
| ST7 | Search and PMax brand overlap | brand exclusions on in PMax |
| ST8 | Budget follows priority | top performers not budget-limited |
| ST9 | Daily budget pacing | no campaign hits its cap before 6 pm |
| ST10 | Ad schedule | matches business hours where it matters |
| ST11 | Geo targeting | "presence" for local or regional accounts |
| ST12 | Networks | search partners and display off for search campaigns unless intended |

## Keywords and quality score (8)

| Id | Check | Pass when |
| --- | --- | --- |
| KW1 | Average quality score | 7 or higher |
| KW2 | Critical low QS | under 10% of keywords at QS 3 or below |
| KW3, KW4, KW5 | Below-average components | expected CTR under 20%, ad relevance under 20%, landing page under 15% of keywords |
| KW6 | Top spenders | top 20 keywords by spend all QS 7 or higher |
| KW7 | Zero-impression keywords | none in 30 days |
| KW8 | Keyword to ad relevance | headlines carry the ad group's keyword variants |

## Ads and assets (17)

| Id | Check | Pass when |
| --- | --- | --- |
| AD1 | RSAs per ad group | at least 1, 2 recommended |
| AD2, AD3 | RSA headline and description counts | 8+ headlines (12 to 15 ideal), 3+ descriptions (4 ideal) |
| AD4 | RSA ad strength | good or excellent |
| AD5 | Pinning | strategic: 1 to 2 positions, 2 to 3 variants each |
| AD6, AD7, AD8 | PMax asset density | 20+ images, 5+ logos, 5+ videos per group; video in 16:9, 1:1, 9:16; 2+ asset groups |
| AD9 | PMax final URL expansion | set on purpose |
| AD10 | Copy relevance | headlines carry the ad group's keyword |
| AD11 | Copy freshness | new copy tested in the last 90 days |
| AD12 | CTR against benchmark | at or above the account's own history, then the industry range |
| AD13, AD14 | PMax signals and strength | first-party audience signals; good or excellent |
| AD15 | PMax brand cannibalisation | under 15% of PMax conversions from brand terms |
| AD16, AD17 | PMax search themes and negatives | configured |

## Settings and targeting (18)

| Id | Check | Pass when |
| --- | --- | --- |
| SE1 to SE6 | Assets | 4+ sitelinks, 4+ callouts, 1+ structured snippet, image assets, call tracking, lead form with CRM link where used |
| SE7 | Audience segments in observation | several applied |
| SE8 | Customer match | list uploaded, refreshed in 30 days |
| SE9 | Placement exclusions | account-level for games, apps, made-for-ads sites |
| SE10 | Landing page speed | mobile LCP under 2.5 s (under 2.0 ideal) |
| SE11, SE12 | Landing page relevance and schema | message match; product, FAQ or service schema |
| SE13 | Smart bidding | every campaign with 15+ conversions in 30 days |
| SE14 | Target CPA or ROAS | within 20% of trailing performance |
| SE15 | Learning phase | under 25% of campaigns learning or limited |
| SE16 | Budget constraint | top performers not constrained |
| SE17 | Manual CPC | only on campaigns under 15 conversions a month |
| SE18 | Portfolio strategies | low-volume campaigns grouped |
