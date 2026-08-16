# History — BUG-0003

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-17T01:30:00Z | — | ready | verify | — | filed by independent regression verification on main: overview v2's no-decoding boundary and the exit-code contract both fail |
| 2026-08-17T01:30:01Z | ready | planned | plan | — | plan.md written with all 6 criteria mapped; ADR-0008 recorded; overview bumped to v4; reproduction and mechanism established first |
| 2026-08-17T01:30:02Z | planned | in-progress | implement | — | branch wi/BUG-0003 created from main; starting plan step 1 |
| 2026-08-17T01:30:03Z | in-progress | verifying | implement | — | gates green on wi/BUG-0003 head 8634781; 60 tests pass; the AC1, AC2 and AC4 tests demonstrated failing at 6d1e437 |
| 2026-08-17T01:30:04Z | verifying | in-review | verify | — | all 6 criteria pass with evidence on 21d583d; 60 tests green; Q-001 filed non-blocking about ADR-0008's non-reproducing example |
| 2026-08-17T01:30:05Z | in-review | done | review-close | — | DoD D1-D11 pass; merge result proved tree-identical and green; ADR-0008's corrected reasoning checked in place |
