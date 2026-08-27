# History — WI-0004

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-26T23:42:32Z | — | draft | answer-questions | — | an answer widened the scope: the stakeholder asked for deletion of mistaken records (WI-0001/Q-003), scheduled after WI-0002 |
| 2026-08-27T00:56:56Z | draft | awaiting-answer | refine | draft | one blocking question to the stakeholder: what deleting a person does to that person's expenses (Q-001); DoR fails R4, R8 and R10, not overridden |
| 2026-08-27T01:02:57Z | awaiting-answer | draft | answer-questions | — | the stakeholder answered Q-001 with option A (refuse to delete a person named in an expense, and say what is in the way); propagated into refinement-qa.md and item.md, resuming at the recorded resume-to |
| 2026-08-27T01:07:37Z | draft | ready | refine | — | Definition of Ready passes on all ten criteria, not overridden: the stakeholder's answer to Q-001 became AC3 and AC4, and the four vague criteria are replaced by AC1-AC8, each naming a command and the observation that settles it |
| 2026-08-27T01:12:22Z | ready | planned | plan | — | the design is recorded: eleven steps over store.py, cli.py, the tests and the README, with ADR-0006 fixing how an expense is addressed and ADR-0007 putting the people-and-expenses invariant at the write points |
| 2026-08-27T01:14:36Z | planned | in-progress | implement | — | branch wi/WI-0004 created from main; executing the eleven-step plan |
| 2026-08-27T01:19:22Z | in-progress | verifying | implement | — | gates green on wi/WI-0004; impl-report.md written with a test named for every acceptance criterion |
| 2026-08-27T01:23:31Z | verifying | in-review | verify | — | all eight acceptance criteria pass on f4e8319, each with a command run by verify and its output; no defects |
| 2026-08-27T01:27:21Z | in-review | in-progress | review-close | — | rejected on D7 and D12: docs/architecture/overview.md v4 still describes this item's delivered work under 'What is coming', and says store.py gains two new functions when it gains three (naming_expenses, delete_person, delete_expense) |
| 2026-08-27T01:35:10Z | in-progress | verifying | implement | — | the D7/D12 send-back is fixed: docs/architecture/overview.md is at version 5 with deletion in the body and store.py's three new functions counted correctly; no code changed and the 120-test suite is green on e2a0b3d |
| 2026-08-27T01:39:56Z | verifying | in-review | verify | — | all eight acceptance criteria re-demonstrated on beb522e with commands run by verify, plus five sensitivity probes; no defects. The only change since the first verification is docs/architecture/overview.md v5, which no criterion covers |
| 2026-08-27T01:44:25Z | in-review | done | review-close | — | accepted: all twelve Definition of Done criteria pass, including D7 and D12 which rejected it last time; docs/architecture/overview.md v5 audited claim by claim against the code, a detached trial merge clean with 120 tests passing, six gaps accepted and recorded in item.md |
