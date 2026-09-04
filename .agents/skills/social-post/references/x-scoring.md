<!-- source: https://raw.githubusercontent.com/manojbajaj95/claude-gtm-plugin/main/skills/x-impact-checker/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Scoring an X post before it goes out

Condensed from the x-impact-checker skill in
manojbajaj95/claude-gtm-plugin, which scores a draft against the
engagement signals X's open-sourced ranking describes. A score is a
review aid, not a promise of reach.

## The 100 points

### Core engagement, 60

| Factor | Max | Full marks when |
| --- | --- | --- |
| Reply | 22 | a direct question or a debatable claim; 12 for an invitation to respond; 4 for a plain statement |
| Repost | 16 | an actionable insight or surprising fact; 8 interesting but niche |
| Like | 12 | emotionally resonant or a personal story; 6 a useful reference |
| Quote | 10 | a strong opinion that invites commentary; 5 thought-provoking |

### Extended engagement, 25

Dwell time 6 (depth rewards reading), continuous dwell 4 (a thread or a
story arc), click 5 (a compelling link with context; 1 for a bare URL),
photo expand 4, video view 3, quoted click 3 (a bold claim that invites
checking).

### Relationship, 15

Profile click 5 (creates curiosity about the author, shows expertise),
follow 4 (signals ongoing value, a cadence), share 2, share by DM 2
("send this to a friend" content), copy link 2 (bookmark-worthy).

### Penalties

Not interested minus 5 to 15 (clickbait, irrelevant); mute risk minus 5
to 15 (repetitive patterns); block risk minus 10 to 25 (aggressive
tone); report risk minus 15 to 30 (policy or spam signals).

### Grades

90 to 100 S; 75 to 89 A; 60 to 74 B; 45 to 59 C; 30 to 44 D; below 30 F.
Rewrite anything under B.

## Before and after, per factor

- Reply: "Just shipped a feature" becomes "Ship fast and buggy, or slow
  and stable? We chose speed. Right call?"
- Repost: "I learned something today" becomes a numbered list of three
  concrete patterns with the result they produced.
- Like: "Debugging is hard" becomes the specific 2 a.m. story with the
  lesson.
- Quote: "TypeScript is useful" becomes "TypeScript's real value is
  documentation; the type errors are a bonus."
- Continuous dwell: a thread marker and a narrative ("1/8, day 1 to 7:
  validation").
- Profile click: credentials in the first line ("after N years doing X,
  here is what I wish I knew").
- Follow: a series ("tip 47; a new one every Monday").

## Limits the source flags

Text analysis only: it cannot see the author's history, timing or the
audience, and language handling is uneven. Use the score to compare
variants of one post, not to predict numbers.

## In this repo

Score every X draft in `content/<x>/draft.md` under a `## Score` line
with the grade and the two weakest factors; `social-performance` later
checks whether the grades tracked the real numbers.
