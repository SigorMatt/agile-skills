# History — WI-0003

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-29T10:45:17Z | — | draft | intake | — | created from the stakeholder's stated idea for EP-001 |
| 2026-08-29T12:23:25Z | draft | awaiting-answer | refine | draft | Q-001 filed to the stakeholder: which rung a brand-new card starts on, and so what a first right answer schedules |
| 2026-08-29T12:29:01Z | awaiting-answer | draft | answer-questions | — | Q-001 answered by the stakeholder: a never-answered card sits below the bottom rung; AC6 rewritten and ADR-0001 amended to v2 |
| 2026-08-29T12:31:41Z | draft | ready | refine | — | Definition of Ready passes on all ten criteria; Q-001 answered, AC6 settled and AC2 extended with the overdue case |
| 2026-08-29T12:37:35Z | ready | planned | plan | — | plan.md written; ADR-0007 records the interval field and store version 3, ADR-0001 amended to v3 and the overview to v3 |
| 2026-08-29T12:39:32Z | planned | in-progress | implement | — | branch wi/WI-0003 created from main; executing plan.md's thirteen steps |
| 2026-08-29T12:46:37Z | in-progress | verifying | implement | — | the ladder is implemented on wi/WI-0003; all six hard gates pass on the branch head and impl-report.md maps every criterion to its evidence |
| 2026-08-29T12:53:30Z | verifying | in-progress | verify | — | AC9 fails: interval: true is accepted as the 1-day rung, and due: 2026-8-9 is accepted while sorting above every real date so the card is silently never due. AC1-AC8 pass |
| 2026-08-29T12:57:13Z | in-progress | verifying | implement | — | D1 and D2 fixed in load: a JSON true is no longer read as the 1-day rung, and an unpadded due is refused rather than silently sorting the card out of every review; the AC4 card-field-row coverage gap is closed too |
| 2026-08-29T13:07:29Z | verifying | in-review | verify | — | all nine acceptance criteria pass at f841f09, each re-run independently this pass; the two AC9 defects from the first verification are closed and neither reappeared under a 30-store probe |
| 2026-08-29T13:12:14Z | in-review | done | review-close | — | Definition of Done passes D1-D12 with per-criterion evidence; the diff maps hunk by hunk to the plan, the D12 claims were checked against the code they cite, and the merge result passed 87 tests in a detached trial worktree |
