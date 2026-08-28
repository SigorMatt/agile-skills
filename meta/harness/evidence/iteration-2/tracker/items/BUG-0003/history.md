# History — BUG-0003

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-27T19:10:49Z | — | ready | verify | — | Found while verifying WI-0002: the CLI help text describes destinations as chosen by file type only, which age routing made false |
| 2026-08-27T20:24:28Z | ready | planned | plan | — | Design recorded: ADR-0008 keeps the help text as prose guarded by a test that reads DEFAULT_BANDS, and plan.md settles the exact description and epilog wording |
| 2026-08-27T20:25:17Z | planned | in-progress | implement | — | Branch wi/BUG-0003 created from main at b76b27c; work on the plan's five steps has started |
| 2026-08-27T20:27:54Z | in-progress | verifying | implement | — | Two strings in build_parser rewritten and a regression test added that reads DEFAULT_BANDS; all hard gates pass on the branch head and the test is proven to fail against the old wording |
| 2026-08-27T20:32:45Z | verifying | in-review | verify | — | All four criteria pass on f575fc9, each demonstrated by a command run in this execution; one declared finding on AC4's two readings goes to the review |
| 2026-08-27T20:41:15Z | in-review | done | review-close | — | Definition of Done passes criterion by criterion; three hunks each traceable to a criterion, suite green on the trial merge result 4420b83, and ADR-0004's stale test count corrected on the way through |
