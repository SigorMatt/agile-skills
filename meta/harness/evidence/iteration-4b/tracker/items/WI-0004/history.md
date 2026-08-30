# History — WI-0004

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-30T01:37:52Z | — | draft | answer-questions | — | the stakeholder's answer to EP-001/Q-001 contradicts intake's derived exclusion: deleting a card is wanted, editing is not |
| 2026-08-30T04:25:48Z | draft | awaiting-answer | refine | draft | Q-001 and Q-002 blocking, to human: how a card is named when deleting it, and whether deleting confirms first; DoR R4, R8 and R10 fail without them |
| 2026-08-30T04:31:50Z | awaiting-answer | draft | answer-questions | — | Q-001 and Q-002 answered by the human and propagated into item.md and refinement-qa.md; no blocking question remains, resuming at the recorded resume-to |
| 2026-08-30T04:36:37Z | draft | ready | refine | — | Definition of Ready passes on all ten criteria; R4, R6, R8 and R10 closed by the stakeholder's answers to Q-001 and Q-002 and a rewrite of four criteria into twelve decidable ones |
| 2026-08-30T04:41:16Z | ready | planned | plan | — | plan.md written with ten steps and a row for each of AC1-AC12; ADR-0009 records how a deletion is confirmed and why it differs from review; overview bumped to v5 |
| 2026-08-30T04:43:10Z | planned | in-progress | implement | — | starting the plan's ten steps on branch wi/WI-0004, branched from main at 152c531 |
| 2026-08-30T04:49:13Z | in-progress | verifying | implement | — | AC1-AC12 all built and tested on wi/WI-0004 (55 tests OK); impl-report.md maps each criterion to a test; all hard gates pass on branch head 1d46cae |
| 2026-08-30T04:54:32Z | verifying | in-review | verify | — | all twelve criteria pass against branch head ffef942, each demonstrated by a command run in verification; AC12's covered criteria (WI-0001 AC3, AC6) read and still true; no defect of this item's own |
| 2026-08-30T04:59:51Z | in-review | done | review-close | — | accepted: D1-D12 all pass (D12 after repairing a false claim in overview.md), trial merge 04c5a38 passes 55 tests, main confirmed unmoved; three findings repaired in review, four gaps recorded in the item's Notes |
