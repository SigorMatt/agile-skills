# History — BUG-0001

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-22T02:27:53Z | — | ready | verify | — | found while verifying WI-0001: all three recording commands print their success line before main attempts the save, so a write failure reports both success and error |
| 2026-08-22T03:44:14Z | ready | planned | plan | — | plan.md written and ADR-0011 recorded: the handler contract becomes str-or-None so main prints the success line only after store.save returns, which fixes all three commands at once and gives WI-0003's importer the ordering for free |
| 2026-08-22T03:48:14Z | planned | in-progress | implement | — | branch wi/BUG-0001 created from main at 17ca1fa; executing the plan's seven steps, starting with the regression test so its failure against the unfixed code is on the record |
| 2026-08-22T03:51:18Z | in-progress | verifying | implement | — | the handler contract of ADR-0011 is implemented: main saves and only then prints, so a failed write says nothing on stdout for all three recording commands; regression test recorded failing against the unfixed code and passing on the branch head |
| 2026-08-22T03:55:59Z | verifying | in-review | verify | — | AC1 and AC2 both pass on evidence gathered here: the six reproduction steps give empty stdout, stderr and exit 1 for all three commands, and the regression test fails with the three pre-fix lines when print is moved back above the save |
| 2026-08-22T04:00:22Z | in-review | done | review-close | — | accepted: all twelve Definition of Done criteria pass, D12 after correcting a stale lede in overview.md; trial merge into a copy of main gave 116 tests green, and four declared gaps were carried into the item's Notes |
