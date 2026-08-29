# History — WI-0004

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-29T13:18:40Z | — | draft | answer-questions | — | the stakeholder's answer to EP-001/Q-005 chose option B and named deleting a card as the one follow-up they want; EP-001's Out of scope said such a request becomes a new item |
| 2026-08-29T13:26:42Z | draft | awaiting-answer | refine | draft | Q-001 blocking, to human: whether recall delete confirms before deleting. DoR R4, R6 and R8 fail on that one answer; the other nine criteria are written and the design questions are routed to plan |
| 2026-08-29T13:30:20Z | awaiting-answer | draft | answer-questions | — | Q-001 answered by the human: delete immediately, print both sides, no prompt; AC2 rewritten as a decidable check and refinement-qa.md updated |
| 2026-08-29T13:32:31Z | draft | ready | refine | — | Definition of Ready passed on all ten criteria in round 2; Q-001 answered, AC2 rewritten to pin both output streams, refinement-qa.md now status: recorded |
| 2026-08-29T13:38:16Z | ready | planned | plan | — | plan.md written with all ten criteria mapped; ADR-0008 (card numbers may be reused, schema unchanged) and ADR-0009 (exit 1 widened) settle the three questions refine routed here; overview bumped to v4 |
| 2026-08-29T13:40:07Z | planned | in-progress | implement | — | branch wi/WI-0004 created from main at 6e9e5cc; fresh start, no partial work to reconcile |
| 2026-08-29T13:46:38Z | in-progress | verifying | implement | — | all six hard gates green on wi/WI-0004 head (101 tests, 5 commits) at the second attempt; the first was refused on four unresolvable plan citations in impl-report.md, fixed in 1b1c674; the report maps each of AC1-AC10 to a named test function |
| 2026-08-29T13:53:15Z | verifying | in-review | verify | — | all ten criteria demonstrated by commands verify ran at 0a26e4ae and ticked; two findings recorded for review-close rather than sent back - impl-report.md misattributes a mutation to AC5, and AC5's test survives a crashing implementation |
| 2026-08-29T13:58:30Z | in-review | done | review-close | — | accepted: all ten criteria met, D1-D12 each recorded with evidence, trial merge clean with 101 tests green on the merge result; three findings recorded as accepted gaps in the item's Notes rather than sent back |
