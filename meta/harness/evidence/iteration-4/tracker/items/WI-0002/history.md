# History — WI-0002

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-29T10:45:15Z | — | draft | intake | — | created from the stakeholder's stated idea for EP-001 |
| 2026-08-29T11:00:40Z | draft | awaiting-answer | refine | draft | Q-001 blocking, to human: which keys the review session uses to reveal, record right or wrong, and stop early |
| 2026-08-29T11:09:14Z | awaiting-answer | draft | answer-questions | — | Q-001 answered by the stakeholder: Enter reveals, y right, n wrong, q stops; AC1, AC2, AC5, AC6 and AC9 amended to name the keys |
| 2026-08-29T11:42:32Z | draft | ready | refine | — | Definition of Ready passes R1-R10; round 2 asked nothing, AC1/AC2/AC8/AC9 made decidable and AC10 added under the stakeholder's standing deferral |
| 2026-08-29T11:48:46Z | ready | planned | plan | — | Plan written with AC1-AC10 mapped to named assertions; ADR-0006 records the due and result fields, store version 2 and saving after each card; overview at v2 fixes that the session reads a stream, never a terminal |
| 2026-08-29T11:51:06Z | planned | in-progress | implement | — | branch wi/WI-0002 created from main at 41eb102; executing the plan's ten steps |
| 2026-08-29T11:58:32Z | in-progress | verifying | implement | — | recall review built to the plan's ten steps; AC1-AC10 each have a named test, 55 tests green, all hard gates pass on 075e339 |
| 2026-08-29T12:10:42Z | verifying | in-review | verify | — | AC1-AC10 all pass, each demonstrated by a command run against e397490; nine negative cases triggered and twelve mutants detected; two findings handed to review-close, neither a criterion failure |
| 2026-08-29T12:16:14Z | in-review | done | review-close | — | Accepted: D1-D12 all pass with individual evidence, trial merge green on the merge result; three findings and six gaps accepted and recorded in Notes, two routed to WI-0003 |
