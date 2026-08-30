# History — BUG-0001

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-30T02:07:30Z | — | ready | verify | — | found while verifying WI-0001: two conditions outside every WI-0001 criterion reach the user as an uncaught traceback |
| 2026-08-30T05:09:18Z | ready | planned | plan | — | design recorded in ADR-0010 and plan.md: store classifies an OS refusal into DeckInaccessible and cli reports it; all six criteria mapped to steps |
| 2026-08-30T05:10:05Z | planned | in-progress | implement | — | starting the plan's twelve steps on branch wi/BUG-0001, branched from main at ec112a4 |
| 2026-08-30T05:18:15Z | in-progress | verifying | implement | — | all six criteria built and tested on wi/BUG-0001 (61 tests OK); four mutations recorded for AC5; all hard gates pass on branch head b1cbc9f |
| 2026-08-30T05:25:13Z | verifying | in-progress | verify | — | D1: store._refusal's Path.is_dir() re-raises PermissionError, so an unreadable deck directory (chmod 000) still reaches the person as a double traceback at exit 1 — contradicting plan.md step 2, ADR-0010 Consequences and the function's own docstring. All six criteria pass at 20bfbb3; none ticked, because the fix changes code AC1-AC3 rest on |
| 2026-08-30T05:33:46Z | in-progress | verifying | implement | — | D1 fixed: _refusal's middle branch uses os.path.isdir, so the classifier no longer raises while classifying; two regression tests and mutation M5 demonstrate it, and all six criteria are re-measured at branch head 5bf6141 |
| 2026-08-30T05:39:14Z | verifying | in-review | verify | — | all six criteria pass at bb74d04, each from a command run in verification; D1 is fixed and none of eight boundary conditions produces a traceback; two observations recorded, neither filed |
| 2026-08-30T05:43:23Z | in-review | done | review-close | — | accepted: D1-D12 all pass with per-criterion evidence, the merge result is green (63 tests OK at trial merge 68c05a9), three cosmetic findings and five gaps recorded in ## Notes |
