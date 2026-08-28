# History — BUG-0002

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-27T16:31:21Z | — | ready | verify | — | Found while verifying WI-0001: apply_plan reports ADR-0003's fallback as a failure, so a run in which every file moved exits non-zero |
| 2026-08-27T19:50:01Z | ready | planned | plan | — | ADR-0007 decides the tagged Outcome return; plan.md maps all four ACs to steps and named tests |
| 2026-08-27T19:50:45Z | planned | in-progress | implement | — | Branch wi/BUG-0002 created at a0fe21e; executing plan.md steps 1-9 |
| 2026-08-27T19:54:16Z | in-progress | verifying | implement | — | ADR-0007 implemented on wi/BUG-0002 at cb4a882; 68 tests pass and four mutations show AC1-AC3 are each guarded |
| 2026-08-27T19:58:59Z | verifying | in-review | verify | — | All four criteria pass on 6a5b1a7, each checked by a command this skill ran; five mutations confirm the tests are sensitive |
| 2026-08-27T20:09:59Z | in-review | awaiting-answer | review-close | in-review | Definition of Done fails on D12: overview.md paragraph 3 and ADR-0007's reversibility clause are both false against the merged code; filed Q-001 and Q-002 to the architect. Code, tests and trial merge all pass |
| 2026-08-27T20:13:10Z | awaiting-answer | in-review | answer-questions | — | Q-001 and Q-002 answered from spec/doc-header.md and propagated: overview.md v5 no longer says the fallback path is untested, ADR-0007 v2 no longer says apply_plan is imported only by cli.py |
| 2026-08-27T20:16:13Z | in-review | done | review-close | — | Accept: all twelve Definition of Done criteria pass on the merge result 88fb911; D7 and D12 clear now that overview.md v5 and ADR-0007 v2 carry the propagated answers, re-checked against the code |
