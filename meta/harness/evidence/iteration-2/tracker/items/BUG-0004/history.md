# History — BUG-0004

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-27T19:31:55Z | — | ready | verify | — | Found while verifying BUG-0001: entry.stat() on a dangling symlink aborts build_plan, so no file in the folder is tidied |
| 2026-08-27T20:48:26Z | ready | planned | plan | — | Design recorded: ADR-0009 makes an OSError from one entry a leave action inside build_plan, leaving ADR-0006's target-level boundary untouched; plan.md settles the reason wording, the README amendment and the two regression tests |
| 2026-08-27T20:49:01Z | planned | in-progress | implement | — | Branch wi/BUG-0004 created from main at 73bb1f4; work on the plan's six steps has started |
| 2026-08-27T20:52:40Z | in-progress | verifying | implement | — | One guard in build_plan turns an OSError from a single entry into a leave action; three regression tests proven to fail against the reverted planner, README amended, and all hard gates pass on the branch head |
| 2026-08-27T20:58:11Z | verifying | in-review | verify | — | AC1-AC4 all pass against ab64484; verify-report.md written, no defects found |
| 2026-08-27T21:05:14Z | in-review | awaiting-answer | review-close | in-review | Q-001 and Q-002 blocking: the merge makes an ADR-0006 consequence paragraph untrue and moves every line ADR-0009 cites; review-close may not edit an ADR |
| 2026-08-27T21:09:01Z | awaiting-answer | in-review | answer-questions | — | Q-001 and Q-002 answered from the record and propagated: ADR-0006 v2 restates the cost paragraph ADR-0009 made untrue, ADR-0009 v2 cites planner.py by file and symbol |
| 2026-08-27T21:18:29Z | in-review | done | review-close | — | Definition of Done passes on all twelve criteria; round 1's ADR-0006 and ADR-0009 findings closed against the corrected documents, ADR-0008's blank-line citation filed as BUG-0006; trial-merged detached at 54251e84 with 72 tests green |
