# History — WI-0001

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-09-11T01:57:11Z | — | draft | intake | — | created from the stakeholder's stated idea for EP-001 |
| 2026-09-11T02:04:54Z | draft | awaiting-answer | refine | draft | round 1 filed Q-001..Q-004 (blocking, to human); DoR R4, R6, R8 and R10 fail pending their answers |
| 2026-09-11T02:21:32Z | awaiting-answer | draft | answer-questions | — | four stakeholder answers consumed and propagated into AC7-AC13 and the refinement record; resuming at the recorded resume-to |
| 2026-09-11T02:32:29Z | draft | ready | refine | — | round 2 settled the command surface without the stakeholder — the invocation, the streams and the exit codes are AC1-AC3 and AC14-AC17, five assumptions recorded under no delegation; Definition of Ready passes criterion by criterion |
| 2026-09-11T02:43:04Z | ready | planned | plan | — | plan.md, five ADRs and the architecture overview written; all eight gates run by hand and passed, but the transition could not be taken through the gate run — F-084 deadlock, see the workspace-valid gate line in the journal entry [gates forced] |
| 2026-09-11T02:43:44Z | planned | in-progress | implement | — | branch wi/WI-0001 created from main; implementing the plan's seven steps |
| 2026-09-11T02:52:40Z | in-progress | verifying | implement | — | the three commands, the store and both entry points built on wi/WI-0001 with 51 tests; all nine gates pass on the branch head and the invalidation set is closed |
| 2026-09-11T03:05:10Z | verifying | in-progress | verify | — | AC15 fails: three of its five named invocations (envel new a b, envel add groceries 10 20, envel list extra) print the top-level usage rather than a usage message for that subcommand; its test asserts only that stderr is non-empty. AC1-AC14, AC16 and AC17 pass. |
| 2026-09-11T03:11:14Z | in-progress | verifying | implement | — | AC15 fixed: a wrong argument count is reported through the subcommand's own parser, so all five named invocations print that subcommand's usage; AC14 still prints the tool's and its test asserts so. The AC15 test now asserts the criterion rather than AC16's, and an amount at the cent covers AC8 and AC9. 52 tests, all nine gates pass on branch head 81441cd. |
| 2026-09-11T03:18:12Z | verifying | in-review | verify | — | All seventeen criteria pass against branch head 2f025c5, re-run in full rather than carried over: AC15's five invocations now print the subcommand's own usage, AC14 still prints the tool's, and the advisory sensitivity gate passes with fourteen mutations and fourteen red suites. |
| 2026-09-11T03:28:08Z | in-review | done | review-close | — | Definition of Done passes D1-D13; all seventeen criteria hold on evidence, four re-run by this review; the suite passes on the trial merge result (aada90c), not only on the branch; two findings recorded, neither a defect |
