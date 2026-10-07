# Scoring linking domains and prospects

A deterministic score, so a "new strong link" means the same thing every
run. Apply it to every referring domain and prospect in the snapshot and
add `category`, `relevance`, `score` and `tier` columns to the report's
tables; the snapshot stays as pulled.

## Classify once per domain

Read the linking page (or, for a prospect, the domain and the competitors
it links to; read a page only when that is unclear) and set:

- `category`: review_directory, analyst, publication, newsletter,
  community, news, partner, forum, ai_directory, startup_database, social,
  competitor, other, link_farm
- `relevance` to the buyers in `strategy/icp.md`: high, medium, low
- a one-line reason: who they are and why they link

**Link farm by rule**, before any reading: a spam score of 50 or more, or
an anchor selling links (backlinks, PBN, dofollow, link building, guest
post, SEO service, "DA 50"). Farms are counted once, never called a gain,
and never a reason to act: Google ignores them, so never propose a disavow.

## Score (0 to 100)

| Part | Points |
| --- | --- |
| Authority (max 40) | the linking host's organic traffic when known: 10,000+ = 40, 1,000+ = 32, 100+ = 24, 10+ = 14, any = 6; otherwise domain rank, capped at 24 (rank follows the platform, so a blog on a big host inherits it): 150+ = 24, 50+ = 14, any = 6 |
| Relevance (max 30) | high 30, medium 15, low 5; unclassified counts as medium for a link we have, low for a prospect |
| Category (max 10) | review_directory, analyst, publication, newsletter, community, news, partner 10; forum 8; ai_directory, startup_database 6; social, other 3; competitor, link_farm 0; unclassified 5 |
| Link (max 20) | ours: dofollow 15, in the body of a page 5; prospects: 5 per competitor linked beyond the first |

**Tier A** 65 and up, **B** 40 to 64, **C** below 40, `spam` for farms. A
low-relevance prospect is C whatever its score: big but off-topic is not
worth outreach.

## Reading the result

- The number that counts is real linking domains (tiers A, B and C), by
  tier, this pull against the last.
- New links ranked by score with the page they point to; a page of ours
  that earns links is a format to repeat.
- A lost A or B link is a vendor-index fact until one backlinks call
  filtered to that domain confirms it; then it is a reclaim target.
- Prospects worth outreach are tier A and B; the rest are listed, not
  pursued.
