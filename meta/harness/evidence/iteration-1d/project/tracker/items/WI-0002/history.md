# History — WI-0002

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-22T01:34:55Z | — | draft | intake | — | created from idea intake for EP-001 |
| 2026-08-22T02:42:04Z | draft | awaiting-answer | refine | draft | Q-001 blocking: nobody has said whether the report is pairwise debts or minimised transfers, and five of six criteria depend on it |
| 2026-08-22T02:50:57Z | awaiting-answer | draft | answer-questions | — | Q-001 answered by the stakeholder: the report is the pairwise ledger; recorded as ADR-0006 and propagated into AC1, the R10 table and the refinement Q&A |
| 2026-08-22T02:59:07Z | draft | ready | refine | — | Definition of Ready passes with no override: six inherited criteria rewritten into eleven observable ones, six with worked ledgers and exact expected output, and the old nobody-owes-anybody trigger corrected against the pairwise rule |
| 2026-08-22T03:07:28Z | ready | planned | plan | — | design recorded as ADR-0008 and ADR-0009 and plan.md written: the pairwise computation becomes a pure expenses/debts.py, all eleven criteria map to a step and a named demonstration |
| 2026-08-22T03:08:06Z | planned | in-progress | implement | — | branch wi/WI-0002 created from main; starting the plan's five steps |
| 2026-08-22T03:13:29Z | in-progress | verifying | implement | — | the debts command is built on wi/WI-0002; all eleven criteria have named tests, 115 tests green, every hard gate passed on the branch head |
| 2026-08-22T03:18:12Z | verifying | in-review | verify | — | all eleven criteria demonstrated against c73f039 with commands run by verify, eight negative cases triggered, seven mutations confirm the tests bite; no defects |
| 2026-08-22T03:27:00Z | in-review | done | review-close | — | Definition of Done passes; D12 found one false claim about debts.py raising nothing, corrected as overview v6; 115 tests green on the trial merge |
