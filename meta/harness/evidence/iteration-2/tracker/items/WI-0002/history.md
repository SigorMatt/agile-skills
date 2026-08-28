# History — WI-0002

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-27T15:44:21Z | — | draft | intake | — | created from the stakeholder's stated idea for EP-001; the age half of 'by type and age' |
| 2026-08-27T16:44:34Z | draft | awaiting-answer | refine | draft | Two blocking questions filed to the human: Q-001 how type and age combine into a folder tree, Q-002 what counts as old and how many bands. DoR R4, R8 and R10 fail on both; six further gaps were answered or routed without asking |
| 2026-08-27T17:59:36Z | awaiting-answer | draft | answer-questions | — | WI-0002/Q-001 and Q-002 answered by the stakeholder and propagated into item.md, refinement-qa.md, vision.md v4 and WI-0003; returned to the recorded resume-to |
| 2026-08-27T18:04:12Z | draft | ready | refine | — | Definition of Ready passes: round 2 rewrote AC1-AC5 as AC1-AC13 against the stakeholder's answers, every R10 combination has a criterion or an exclusion, and refinement-qa.md is recorded |
| 2026-08-27T18:08:16Z | ready | planned | plan | — | plan.md written with all thirteen criteria mapped to a step and a demonstration; ADR-0005 records the age rule's shape, the design question refine routed to plan |
| 2026-08-27T18:11:21Z | planned | in-progress | implement | — | branch wi/WI-0002 created from main; executing plan.md's nine steps |
| 2026-08-27T18:18:18Z | in-progress | verifying | implement | — | all nine plan steps executed; six hard gates green on the branch head and every AC1-AC13 named to a test in impl-report.md |
| 2026-08-27T19:12:37Z | verifying | in-review | verify | — | All thirteen acceptance criteria confirmed with evidence on 93a9585; --help staleness filed as BUG-0003, which no WI-0002 criterion covers |
| 2026-08-27T19:17:03Z | in-review | done | review-close | — | Definition of Done passes D1-D12 with per-criterion evidence; 63 tests green on the trial merge result f0adf5e0; nine gaps accepted and recorded in item Notes; BUG-0003 filed for the stale --help text |
