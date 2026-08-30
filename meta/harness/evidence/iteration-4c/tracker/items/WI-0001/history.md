# History — WI-0001

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-30T11:04:20Z | — | draft | intake | — | created from the stakeholder's stated idea for EP-001 |
| 2026-08-30T11:32:14Z | draft | awaiting-answer | refine | draft | Q-001/Q-002 blocking to human: what a duplicate front side does, and whether the card file must be readable by eye; stakeholder is asynchronous |
| 2026-08-30T11:42:27Z | awaiting-answer | draft | answer-questions | — | Q-001 and Q-002 answered by the stakeholder and propagated into AC3, AC5, new AC6, ADR-0004 and the vision; resuming to the recorded resume-to |
| 2026-08-30T11:49:54Z | draft | ready | refine | — | Definition of Ready met on all ten criteria: AC1-AC4 rewritten to name the add subcommand and the observation that settles each, AC7 and AC8 added for the empty side and the missing card file, argument count left deliberately unconstrained |
| 2026-08-30T12:00:31Z | ready | planned | plan | — | plan.md written with seven steps and an AC1-AC8 mapping; ADR-0006, ADR-0007 and ADR-0008 recorded; overview.md created; project.yaml test and lint commands filled in |
| 2026-08-30T12:01:08Z | planned | in-progress | implement | — | branch wi/WI-0001 created from main at 5c667e0; executing plan.md |
| 2026-08-30T12:05:13Z | in-progress | verifying | implement | — | 26 tests pass on wi/WI-0001; each of AC1-AC8 mapped to a named test in impl-report.md; all hard gates green on the branch head |
| 2026-08-30T12:09:30Z | verifying | in-review | verify | — | AC1-AC8 all pass on f22f9c0, each with a command run by verify and its output; nine negative cases exercised; eight mutations confirmed test sensitivity; AC2's machine restart declared as substituted, not skipped |
| 2026-08-30T12:17:47Z | in-review | done | review-close | — | Definition of Done passes D1-D12; diff read hunk by hunk against plan.md and the ADRs; trial merge c3b2f60 green on 26 tests and the lint command; D12 audit found two false sentences about the card file's location and repaired them in place as ADR-0008 v3 errata and overview.md v2 |
