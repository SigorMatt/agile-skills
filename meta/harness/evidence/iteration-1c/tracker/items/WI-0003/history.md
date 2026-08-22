# History — WI-0003

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-21T21:07:03Z | — | draft | intake | — | created from idea refinement for EP-001 |
| 2026-08-21T21:12:35Z | draft | awaiting-answer | intake | draft | Q-001 and Q-002 blocking: report shape and rounding rule unstated |
| 2026-08-21T21:20:39Z | awaiting-answer | draft | answer-questions | — | Q-001 and Q-002 answered and propagated: report is a settlement (item.md AC1/AC3), rounding fixed by ADR-0001 (AC6) |
| 2026-08-21T21:31:44Z | draft | awaiting-answer | refine | draft | the stakeholder is not in this session; Q-003 filed (R10): whether the report also prints per-person balances |
| 2026-08-21T21:46:59Z | awaiting-answer | draft | answer-questions | — | Q-003 answered and propagated: the report prints per-person balances before the payments (item.md AC7, AC4; vision v8) |
| 2026-08-21T22:29:04Z | draft | ready | refine | — | Definition of Ready passes R1-R10; AC1-AC9 name ./expenses report and quote two complete expected reports; three stakeholder answers recorded verbatim in refinement-qa.md |
| 2026-08-21T22:31:18Z | ready | planned | plan | — | plan.md written with AC1-AC9 mapped to named tests; ADR-0010 records the greedy settlement, its tie-break and its print order; overview bumped to v3 |
| 2026-08-21T22:31:41Z | planned | in-progress | implement | — | branch wi/WI-0003 created from main; starting plan step 1 |
| 2026-08-21T22:34:24Z | in-progress | verifying | implement | — | 87 tests pass and compileall is clean on wi/WI-0003 head a830980; AC1-AC9 each mapped to a named test class in impl-report.md |
| 2026-08-21T22:37:37Z | verifying | in-review | verify | — | AC1-AC9 each independently checked against commit e8a8231 with quoted output; 87 tests pass; one finding reported — AC9 cannot detect a content-identical write, so the behaviour was checked by inode and mtime |
| 2026-08-21T22:39:25Z | in-review | done | review-close | — | Definition of Done D1-D12 pass with evidence in review.md; 87 tests pass on the trial merge result; AC9's insensitivity recorded on the item rather than sent back, since the delivered behaviour is correct |
