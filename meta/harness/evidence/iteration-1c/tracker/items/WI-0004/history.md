# History — WI-0004

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-21T21:07:03Z | — | draft | intake | — | created from idea refinement for EP-001 |
| 2026-08-21T21:12:36Z | draft | awaiting-answer | intake | draft | Q-001 blocking: the bank CSV format and the payer/sharer rule are unknown |
| 2026-08-21T21:24:27Z | awaiting-answer | draft | answer-questions | — | Q-001 answered in part and propagated: payer and sharers given at import (AC6); CSV format still unknown, recorded in AC1 and notes for refine |
| 2026-08-21T21:31:44Z | draft | awaiting-answer | refine | draft | the stakeholder is not in this session; Q-002 re-asks the CSV sample (R4) and Q-003 asks re-import behaviour (R10) |
| 2026-08-21T21:49:15Z | awaiting-answer | draft | answer-questions | — | Q-002 and Q-003 answered and propagated: the import stays in scope and blocks EP-001's closure until the CSV sample arrives (EP-001 scope, vision v9); a repeat import warns and needs --again (item.md AC7) |
| 2026-08-21T22:42:01Z | draft | awaiting-answer | refine | draft | Q-004 blocking: the bank CSV sample is still missing, so AC1, AC2 and AC5 fail R4; the other six criteria were refined and are decidable |
| 2026-08-21T22:48:28Z | awaiting-answer | draft | answer-questions | — | Q-004 answered by the stakeholder and propagated: the sample is still missing, they have instructed us to wait rather than guess (vision v10), and the minimum ask is now the header line and one real row (AC1) |
| 2026-08-21T22:50:03Z | draft | awaiting-answer | refine | draft | Q-005 blocking: the bank CSV sample is still missing after four askings, so AC1, AC2 and AC5 fail R4; the stakeholder instructed us to wait rather than guess (Q-004), and the ask is now reduced to the header line and one real row |
| 2026-08-21T22:54:21Z | awaiting-answer | draft | answer-questions | — | Q-005 answered by the stakeholder and propagated: the bank CSV sample is still missing after five askings, reducing the ask did not help, and waiting rather than guessing is confirmed as a standing instruction (item.md R4 notes, refinement-qa Q5) |
| 2026-08-21T22:56:53Z | draft | awaiting-answer | refine | draft | Q-006 blocking: the bank CSV sample has not arrived after five askings and reducing the ask did not help, so rather than re-ask, this offers the stakeholder a route that makes AC1, AC2 and AC5 decidable without guessing - the tool taking the file's shape from them at import time |
| 2026-08-21T23:07:48Z | awaiting-answer | draft | answer-questions | — | Q-006 answered by the stakeholder and propagated: the import takes the file's shape from the command line (item.md AC1, AC2, AC5, AC10), so the CSV sample no longer blocks this item or EP-001 (vision v11, overview v4) |
| 2026-08-21T23:13:38Z | draft | ready | refine | — | Definition of Ready passed on all ten criteria, no override sought; eleven criteria each name a command and a verdict now that Q-006 removed the dependency on the bank CSV sample |
| 2026-08-21T23:20:17Z | ready | planned | plan | — | plan.md written with all eleven criteria mapped to named tests; ADR-0011 records how an imported file is identified; overview v5 |
| 2026-08-21T23:21:23Z | planned | in-progress | implement | — | branch wi/WI-0004 created from main |
| 2026-08-21T23:29:53Z | in-progress | verifying | implement | — | gates green on the branch head (145 tests, lint clean); impl-report.md maps every criterion to a named test |
| 2026-08-21T23:37:02Z | verifying | in-review | verify | — | all eleven criteria pass, checked independently against 909b394; thirteen negative paths exercised and eleven mutations confirm the tests are sensitive |
| 2026-08-21T23:44:01Z | in-review | in-progress | review-close | — | rejected on D7: README.md still says under 'What it does not do yet' that importing a bank CSV export is the next piece of work, and its command table omits import-csv; six documentation defects listed in review.md (F1-F3 this item's, F4-F6 inherited), no code change required |
| 2026-08-21T23:47:23Z | in-progress | verifying | implement | — | review's D7 send-back cleared: README documents import-csv and no longer says it is unbuilt; all six findings fixed, no code touched, 145 tests still green |
| 2026-08-21T23:52:15Z | verifying | in-review | verify | — | re-verified after the D7 send-back: all eleven criteria re-run end to end against 89cce7e, and every claim the new README makes checked by running it |
| 2026-08-21T23:57:05Z | in-review | done | review-close | — | Definition of Done passes on all twelve criteria; 145 tests green on the trial-merge result; the D7 rejection is cleared and the README now documents import-csv |
