# History — WI-0001

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-21T18:38:55Z | — | draft | intake | — | created from idea refinement for EP-001 |
| 2026-08-21T18:45:59Z | draft | awaiting-answer | intake | draft | Q-001 blocking: whether the tool is one-shot subcommands or an interactive session is undecided; addressed to human |
| 2026-08-21T18:57:44Z | awaiting-answer | draft | answer-questions | — | Q-001 answered: the human delegated the command surface, decided as ADR-0001 (one-shot subcommands); propagated into WI-0001..WI-0004 criteria and notes |
| 2026-08-21T19:08:02Z | draft | awaiting-answer | refine | draft | Q-002, Q-003, Q-004 blocking: duplicate-name rule, subcommand names, and what a name may contain; DoR R4, R6, R8 and R10 fail without them; all addressed to human |
| 2026-08-21T19:17:01Z | awaiting-answer | draft | answer-questions | — | Q-002, Q-003 and Q-004 answered: ADR-0005 (name identity) and ADR-0006 (subcommand vocabulary) recorded and propagated into WI-0001..WI-0004 and prd.md v2 |
| 2026-08-21T19:20:45Z | draft | ready | refine | — | Definition of Ready passes on all ten criteria; 3 human answers consumed, 11 decidable criteria, refinement-qa.md written |
| 2026-08-21T19:26:26Z | ready | planned | plan | — | plan.md written with 11 criteria mapped; ADR-0007 (JSON storage) and ADR-0008 (unittest, no linter) recorded; overview.md created; project commands filled in |
| 2026-08-21T19:26:45Z | planned | in-progress | implement | — | branch wi/WI-0001 created from main; executing plan.md |
| 2026-08-21T19:30:55Z | in-progress | verifying | implement | — | all six gates green on wi/WI-0001; 28 tests over AC1-AC11; impl-report.md written |
| 2026-08-21T19:34:16Z | verifying | in-review | verify | — | AC1-AC11 all pass on 1c65c4f, checked by command; 11 mutations all caught; no defects |
| 2026-08-21T19:38:37Z | in-review | done | review-close | — | DoD D1-D12 all pass; trial merge clean with 28 tests green on the merge result; 2 findings recorded as accepted gaps |
