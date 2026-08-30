# History — WI-0003

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-30T01:30:04Z | — | draft | intake | — | created from EP-001 intake: the scheduling rule is the third observable slice |
| 2026-08-30T03:34:48Z | draft | awaiting-answer | refine | draft | two blocking questions to the stakeholder: what happens above the top rung of the ladder (Q-001) and whether a sitting says when the card is next due (Q-002) |
| 2026-08-30T03:43:10Z | awaiting-answer | draft | answer-questions | — | Q-001 and Q-002 answered by the stakeholder and propagated: the ladder stops at a month (ADR-0002 v3) and a sitting prints each card's next-review date (ADR-0007, new); resumed to the recorded resume-to |
| 2026-08-30T03:48:40Z | draft | ready | refine | — | Definition of Ready passed on every criterion; round 2 rewrote four criteria into six decidable ones from the stakeholder's answers to Q-001 and Q-002 and asked nothing new |
| 2026-08-30T03:55:25Z | ready | planned | plan | — | plan.md written with all six criteria mapped; ADR-0008 records what rung counts and what an out-of-range one does; overview at v3 |
| 2026-08-30T03:58:05Z | planned | in-progress | implement | — | branch wi/WI-0003 created from main; executing plan.md's nine steps |
| 2026-08-30T04:06:16Z | in-progress | verifying | implement | — | the interval ladder, the reset, the overdue rule and the printed next-review date are built and tested; all eight gates pass on wi/WI-0003 and impl-report.md maps all six criteria to evidence |
| 2026-08-30T04:12:05Z | verifying | in-review | verify | — | all six criteria pass on commit c2c547a, each demonstrated by a command run in verification; WI-0001 AC1-AC9 and WI-0002 AC1-AC13 re-read individually and all still hold, nothing waived; no defect found |
| 2026-08-30T04:20:06Z | in-review | done | review-close | — | Definition of Done passes on all twelve criteria; merge result green over 43 tests at trial 196df9a; two low-severity record findings accepted and recorded in ## Notes rather than sent back |
