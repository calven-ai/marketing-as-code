<!-- source: https://raw.githubusercontent.com/apify/awesome-skills/bcb7fb8935d2f36f0ec4143fe3a40efc0c191f0b/skills/apify-easy-competitive-intelligence/reference/modules/hiring-signals.md | license: Apache-2.0 | fetched: 2026-09-14 -->
# Hiring Signal Analysis

**When to use**: Infer competitor's strategic direction from hiring patterns.

## Data Gathering

```
# 1: LinkedIn job listings
call-actor: curious_coder/linkedin-jobs-scraper

# 2: Fallback — careers page
call-actor: apify/website-content-crawler  # [competitor-url]/careers

# 3: Glassdoor — culture, salaries, internal signals
call-actor: memo23/glassdoor-scraper-ppr

# 4: Recent hiring news
call-actor: apify/google-search-scraper
  input: { "queries": "[competitor] hiring jobs careers [current-year]\n[competitor] layoffs OR expansion [previous-year] [current-year]" }
```

**0 LinkedIn results = signal** (not hiring aggressively). Glassdoor compensates — reviews reveal culture/strategy even without active hiring.

## Analysis

Categorize roles by department. Hiring velocity (scaling/stable/contracting). Technology signals from JDs. Geographic expansion. Seniority mix: hiring leaders = new initiative, hiring ICs = scaling existing.
