# History — BUG-0001

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-17T01:30:00Z | — | ready | verify | — | filed by independent regression verification on main: WI-0001 AC7 fails for a symlink loop |
| 2026-08-17T01:30:01Z | ready | planned | plan | — | plan.md written with all 6 criteria mapped; ADR-0006 recorded; overview bumped to v3; all three triggers reproduced first |
| 2026-08-17T01:30:02Z | planned | in-progress | implement | — | branch wi/BUG-0001 created from main; starting plan step 1 |
| 2026-08-17T01:30:03Z | in-progress | verifying | implement | — | gates green on wi/BUG-0001 head 06fc185; 50 tests pass; 3 regression tests demonstrated failing at 6d1e437; Q-002 filed non-blocking about AC6's wording |
| 2026-08-17T01:30:04Z | verifying | in-review | verify | — | all 6 criteria pass with evidence on 4bf2cba; 50 tests green; 4 mutations all caught including the wrong-placement one |
| 2026-08-17T01:30:05Z | in-review | done | review-close | — | DoD D1-D11 pass; merge result proved tree-identical and green; silence for unresolvable entries accepted and recorded in the item |
