# History — WI-0002

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-09-11T01:57:13Z | — | draft | intake | — | created from the stakeholder's stated idea for EP-001 |
| 2026-09-11T02:07:31Z | draft | awaiting-answer | refine | draft | round 1 filed Q-001 and Q-002 (blocking, to human); depends-on WI-0001 recorded; DoR R4, R6, R8, R10 fail |
| 2026-09-11T02:24:47Z | awaiting-answer | draft | answer-questions | — | two stakeholder answers consumed and propagated into AC8-AC10; WI-0006 filed for the capability Q-002 implied; resuming at the recorded resume-to |
| 2026-09-11T03:34:34Z | draft | awaiting-answer | refine | draft | round 2 filed Q-003, Q-004 and Q-005 (blocking, to human) on the line that records a spend; DoR R4, R6, R8 and R10 fail pending their answers, and no criterion was rewritten |
| 2026-09-11T03:48:13Z | awaiting-answer | draft | answer-questions | — | round 2's three stakeholder answers consumed and propagated into AC1, AC9, AC10 and new AC11-AC12; no conflict found; resuming at the recorded resume-to |
| 2026-09-11T03:56:23Z | draft | ready | refine | — | round 3: DoR R4 and R10 closed without asking the stakeholder anything - AC8-AC10 given an observation against the store file, AC13 and AC14 appended, four combinations left unconstrained in Notes with who left them so |
| 2026-09-11T04:05:14Z | ready | planned | plan | — | Design recorded: ADR-0006 gives a spend its own date field while at keeps meaning when the entry was written; plan.md maps all fourteen criteria to steps and observations. [gates forced] |
| 2026-09-11T04:06:14Z | planned | in-progress | implement | — | branch wi/WI-0002 created from main; implementation of the plan's seven steps begins |
| 2026-09-11T04:14:49Z | in-progress | verifying | implement | — | the plan's seven steps are executed on wi/WI-0002; all fourteen criteria have a named test, the suite is at 90 and green, and every invalidation row is disposed |
| 2026-09-11T04:25:33Z | verifying | in-review | verify | — | all fourteen acceptance criteria demonstrated independently against d94a2da; six binding ADRs conform, sixteen invalidation entries disposed and reopened; no defect found |
| 2026-09-11T04:34:43Z | in-review | in-progress | review-close | — | review rejected: docs/architecture/overview.md says envelopes knows about store, which envel/envelopes.py:12 disproves - D7 and D12 fail on one invalidation row disposed verified-still-true; repair the sentence, bump the overview, re-dispose the row, no code change |
| 2026-09-11T04:41:07Z | in-progress | verifying | implement | — | review-close finding 1 repaired: docs/architecture/overview.md v4 no longer claims envelopes knows about store, each dependency edge is cited, and the invalidation row moved verified-still-true -> to-update; no code changed and the suite is still 90 and green |
| 2026-09-11T04:52:15Z | verifying | in-review | verify | — | second verification at 51e9fd7: all fourteen criteria demonstrated independently, the repaired overview paragraph reopened with its enumeration and found true, six ADRs conform, sixteen invalidation entries disposed; no defect |
| 2026-09-11T05:01:12Z | in-review | done | review-close | — | Definition of Done passes on all thirteen criteria at the second review: the overview's dependency sentence is repaired at v4 and survives the falsifier that caught it, sixteen invalidation entries are disposed and confirmed, and the suite is green on the merge result 42dc5817 |
