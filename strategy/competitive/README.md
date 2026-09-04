# strategy/competitive/

One file per competitor, named after them (`acme.md`), from
[_battlecard-template.md](_battlecard-template.md); `/setup` starts them and
the `battlecard` skill writes or refreshes one. A battlecard that pretends
the competitor has no strengths trains the team to lose credibility in
live deals. Write the real card. Each carries `last_reviewed` and `owner`
in its frontmatter; the freshness check flags cards not reviewed in 90
days.

Update a card when they ship something notable, when pricing changes, or
when you win or lose against them and learn why. Log the why in
`memory/decision-log.md` and distill it here.
