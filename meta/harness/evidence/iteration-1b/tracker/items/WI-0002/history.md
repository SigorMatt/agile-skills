# History — WI-0002

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-21T18:38:55Z | — | draft | intake | — | created from idea refinement for EP-001 |
| 2026-08-21T18:46:03Z | draft | awaiting-answer | intake | draft | Q-001 and Q-002 blocking: split shape and rounding of uneven splits undefined; both addressed to human |
| 2026-08-21T19:01:10Z | awaiting-answer | draft | answer-questions | — | Q-001 and Q-002 answered: split model recorded as ADR-0002, money representation and rounding as ADR-0003; AC5-AC7 added and WI-0003 AC4 strengthened |
| 2026-08-21T19:42:56Z | draft | ready | refine | — | Definition of Ready passes on all ten criteria; add-expense syntax pinned, 14 decidable criteria, refinement-qa.md written |
| 2026-08-21T19:47:45Z | ready | planned | plan | — | plan.md written with 14 criteria mapped; ADR-0009 (stored shape of an expense) and ADR-0010 (write failures are stated messages) recorded; overview.md v2 |
| 2026-08-21T19:47:54Z | planned | in-progress | implement | — | branch wi/WI-0002 created from main; executing plan.md |
| 2026-08-21T19:53:34Z | in-progress | verifying | implement | — | all six gates green on wi/WI-0002; 79 tests over AC1-AC14; 17 mutations all caught; impl-report.md written |
| 2026-08-21T19:57:46Z | verifying | in-review | verify | — | AC1-AC14 all pass on 10a6bc3, checked by command; 15 mutations, 13 caught and 2 shown behaviour-preserving; 3 findings, no defects |
| 2026-08-21T20:00:37Z | in-review | done | review-close | — | DoD D1-D12 all pass; trial merge clean with 79 tests green on the merge result; 5 findings recorded as accepted gaps |
