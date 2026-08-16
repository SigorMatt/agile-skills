# History — BUG-0002

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-17T01:30:00Z | — | ready | verify | — | filed by independent regression verification on main: ADR-0002 and WI-0001 AC10 combine into a false answer |
| 2026-08-17T01:30:01Z | ready | planned | plan | — | plan.md written with all 7 criteria mapped; ADR-0007 recorded; both triggers and the control reproduced first |
| 2026-08-17T01:30:02Z | planned | in-progress | implement | — | branch wi/BUG-0002 created from main; starting plan step 1 |
| 2026-08-17T01:30:03Z | in-progress | verifying | implement | — | gates green on wi/BUG-0002 head 277c89c; 55 tests pass; 3 regression tests demonstrated failing at 6d1e437 |
| 2026-08-17T01:30:04Z | verifying | in-review | verify | — | all 7 criteria pass with evidence on e1e2985; 55 tests green; 5 mutations all caught; both ADR boundaries exercised |
| 2026-08-17T01:30:05Z | in-review | done | review-close | — | DoD D1-D11 pass; merge result proved tree-identical and green; the new stdout sentence accepted and recorded as an interface change |
