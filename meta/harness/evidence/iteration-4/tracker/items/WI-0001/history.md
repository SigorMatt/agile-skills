# History — WI-0001

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-29T10:45:13Z | — | draft | intake | — | created from the stakeholder's stated idea for EP-001 |
| 2026-08-29T10:58:24Z | draft | awaiting-answer | refine | draft | Q-001 and Q-002 blocking, to human: how a card is typed in, and where the card file lives |
| 2026-08-29T11:07:00Z | awaiting-answer | draft | answer-questions | — | Q-001 answered by the stakeholder, Q-002 decided under their deferral as ADR-0002; AC1, AC4 and AC5 rewritten |
| 2026-08-29T11:12:24Z | draft | ready | refine | — | Definition of Ready passes R1-R10; round 2 asked nothing, AC5 and AC6 tightened and AC9 added under the stakeholder's standing deferral |
| 2026-08-29T11:21:00Z | ready | planned | plan | — | Plan written with AC1-AC9 mapped to named tests; ADR-0003/0004/0005 record the toolchain, the store schema and write protocol, and the command surface; project.yaml now names real test and lint commands |
| 2026-08-29T11:21:38Z | planned | in-progress | implement | — | Branch wi/WI-0001 created from main; implementation of the plan's nine steps started |
| 2026-08-29T11:25:36Z | in-progress | verifying | implement | — | recall add and recall list built on wi/WI-0001 with 21 tests; all seven gates pass at the branch head and AC1-AC9 each map to a named test |
| 2026-08-29T11:29:27Z | verifying | in-review | verify | — | AC1-AC9 all pass on independently-run commands against f23fe67; negative cases triggered, nine mutations confirm the tests bite; no defects, no bugs filed |
| 2026-08-29T11:36:14Z | in-review | done | review-close | — | Definition of Done D1-D12 all pass; diff reviewed hunk by hunk, fourteen doc claims checked against the code, tests green on the merge result; five gaps accepted and recorded in the item |
