# History — BUG-0001

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-27T16:30:45Z | — | ready | verify | — | Found while verifying WI-0001: build_plan lets PermissionError escape, so the user sees a traceback |
| 2026-08-27T19:21:54Z | ready | planned | plan | — | plan.md written with AC1-AC3 each mapped to a step and a demonstration; ADR-0006 records exit 2 at the CLI boundary and why, with both halves reversible |
| 2026-08-27T19:24:09Z | planned | in-progress | implement | — | Branch wi/BUG-0001 created from main at e96c5e2; defect reproduced on the branch head (exit 1, PermissionError traceback) before any edit |
| 2026-08-27T19:27:47Z | in-progress | verifying | implement | — | AC1-AC3 delivered on wi/BUG-0001 (5f2cd4f, 068cecd); all seven gates pass on the branch head; four mutations of the fix each break the regression test |
| 2026-08-27T19:35:42Z | verifying | in-review | verify | — | AC1-AC3 all pass on d80c35a, each decided by a command run in this execution; eleven boundary conditions triggered; five mutations confirm the regression test is sensitive; BUG-0004 filed against WI-0002 for a defect this item neither causes nor claims to fix |
| 2026-08-27T19:40:52Z | in-review | done | review-close | — | D1-D12 all pass with per-criterion evidence; 64 tests green on the trial merge result 25fab17; one finding accepted (a comment's framing, fixed as part of BUG-0004) and seven gaps written into the item |
