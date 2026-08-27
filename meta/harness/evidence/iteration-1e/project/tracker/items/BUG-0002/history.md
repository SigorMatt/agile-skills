# History — BUG-0002

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-27T00:16:35Z | — | ready | review-close | — | found while reviewing WI-0001: store.load turns an OSError into a refusal but store.save does not, so an unwritable store prints a Python traceback and exits 1 |
| 2026-08-27T01:51:54Z | ready | planned | plan | — | design recorded as ADR-0008 (an OSError on the dataset becomes an ExpensesError inside store.py) and plan.md written: nine steps, five criteria mapped, three regression tests behind a write-probe skip |
| 2026-08-27T01:52:45Z | planned | in-progress | implement | — | branch wi/BUG-0002 created from main at 37e57f0; executing the plan's nine steps |
| 2026-08-27T01:56:45Z | in-progress | verifying | implement | — | save now turns an OSError into ExpensesError naming the path (ADR-0008); three subprocess regression tests behind a write probe; 123 tests pass on branch head f23bfda |
| 2026-08-27T02:00:08Z | verifying | in-review | verify | — | all five criteria pass against d8b4c4e, each decided by a command run in this session; one non-blocking finding recorded for the reviewer |
| 2026-08-27T02:10:02Z | in-review | done | review-close | — | accepted: twelve of twelve Definition of Done criteria pass, the detached trial merge is clean and green at 123 tests, and verify's one finding was opened and did not hold (review.md F1) |
