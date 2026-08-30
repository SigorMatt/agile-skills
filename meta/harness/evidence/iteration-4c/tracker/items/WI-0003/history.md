# History — WI-0003

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-30T11:15:14Z | — | draft | answer-questions | — | EP-001/Q-004: the stakeholder asked to be able to delete a card; deletion was out of scope on the epic and no item recorded it |
| 2026-08-30T11:34:55Z | draft | awaiting-answer | refine | draft | Q-001/Q-002 blocking to human: how a card is identified for deletion, and what protects against deleting the wrong one; stakeholder is asynchronous |
| 2026-08-30T11:46:44Z | awaiting-answer | draft | answer-questions | — | Q-001 and Q-002 answered by the stakeholder and propagated into AC1, new AC2, AC5, AC6, ADR-0005 and the vision; the no-match and several-match cases decided; resuming to the recorded resume-to |
| 2026-08-30T13:00:09Z | draft | ready | refine | — | Definition of Ready passes on all ten criteria: AC1 and AC2 now name the delete subcommand and its prompt, AC7-AC9 make the remaining combinations visible, depends-on WI-0001 declared; no question filed and no override |
| 2026-08-30T13:04:28Z | ready | planned | plan | — | plan.md written: delete is a third subcommand in recall/cli.py reusing _ask and store.save, carrying card positions across the confirmation; nine steps, all nine criteria mapped, four reversible assumptions, no new ADR and no document changed |
| 2026-08-30T13:05:12Z | planned | in-progress | implement | — | branch wi/WI-0003 created at 3e9c1df; executing plan.md's nine steps for the delete subcommand |
| 2026-08-30T13:11:45Z | in-progress | verifying | implement | — | delete built on wi/WI-0003 at fe70136: nine criteria, 30 new tests, 90 green, all eight gates pass on the branch head; overview.md needs two sentences repaired at review-close's D7/D12, declared not fixed |
| 2026-08-30T13:20:01Z | verifying | in-review | verify | — | All nine acceptance criteria pass against commands run on 1ebf08e, with nine mutations confirming the tests bite; no defect against this item's criteria. |
| 2026-08-30T13:26:28Z | in-review | done | review-close | — | Accepted and closed, delivered: every hunk maps to a plan step and a criterion, D1-D12 all pass, tests green on the merge result. Two false claims in docs/ repaired at the close - overview.md v5 and ADR-0005 v2 (erratum). |
