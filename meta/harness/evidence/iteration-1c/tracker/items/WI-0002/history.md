# History — WI-0002

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-21T21:07:03Z | — | draft | intake | — | created from idea refinement for EP-001 |
| 2026-08-21T21:12:35Z | draft | awaiting-answer | intake | draft | Q-001 blocking: whether an expense share can be unequal is unstated |
| 2026-08-21T21:22:35Z | awaiting-answer | draft | answer-questions | — | Q-001 answered and propagated: shares are always equal (item.md AC1, out-of-scope, EP-001 scope) |
| 2026-08-21T21:31:44Z | draft | awaiting-answer | refine | draft | the stakeholder is not in this session; Q-002 filed (R10): whether an expense carries a date |
| 2026-08-21T21:45:36Z | awaiting-answer | draft | answer-questions | — | Q-002 answered and propagated: every expense carries a date, today by default (item.md AC1/AC3/AC6, WI-0004 AC2, EP-001 scope, vision v7) |
| 2026-08-21T22:10:58Z | draft | ready | refine | — | Definition of Ready passes R1-R10; AC1-AC9 each name a command and exact expected output; both stakeholder answers recorded verbatim in refinement-qa.md with seven assumptions and two unconstrained behaviours |
| 2026-08-21T22:12:20Z | ready | awaiting-answer | plan | ready | Q-003 blocking: AC6's check clause (date -u +%F) contradicts its own first half on a machine that is not on UTC, and only refine or answer-questions may amend a criterion |
| 2026-08-21T22:14:00Z | awaiting-answer | ready | answer-questions | — | Q-003 answered and propagated: an undated expense takes the machine's local date; AC6's check clause amended from date -u +%F to date +%F |
| 2026-08-21T22:17:02Z | ready | planned | plan | — | plan.md written with AC1-AC9 mapped to named tests; ADR-0009 records the expense record shape and its snapshotted sharers; overview bumped to v2 |
| 2026-08-21T22:17:14Z | planned | in-progress | implement | — | branch wi/WI-0002 created from main; starting plan step 1 |
| 2026-08-21T22:21:42Z | in-progress | verifying | implement | — | 62 tests pass and compileall is clean on wi/WI-0002 head aa611b6; AC1-AC9 each mapped to a named test class in impl-report.md |
| 2026-08-21T22:24:51Z | verifying | in-review | verify | — | AC1-AC9 each independently checked against commit c59b134 with quoted output; 62 tests pass; four sensitivity checks failed as they should |
| 2026-08-21T22:26:50Z | in-review | done | review-close | — | Definition of Done D1-D12 pass with evidence in review.md; 62 tests pass on the trial merge result; three findings accepted and six gaps recorded in the item's Notes |
