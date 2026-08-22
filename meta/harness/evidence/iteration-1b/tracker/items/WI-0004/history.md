# History — WI-0004

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-21T18:54:29Z | — | draft | intake | — | created under EP-001 after the human's answer to EP-001/Q-001 put settling up in scope; answer-questions propagated the scope change and ran intake's item-creation procedure, which pipeline.yaml reserves to intake |
| 2026-08-21T20:22:26Z | draft | ready | refine | — | Definition of Ready passes on all ten criteria; add-payment syntax pinned, 15 decidable criteria, three inherited gaps addressed |
| 2026-08-21T20:25:14Z | ready | planned | plan | — | plan.md written with 15 criteria mapped plus 2 inherited instructions as steps; ADR-0011 (stored shape of a payment) recorded; overview.md v4 |
| 2026-08-21T20:25:27Z | planned | in-progress | implement | — | branch wi/WI-0004 created from main; executing plan.md |
| 2026-08-21T20:29:20Z | in-progress | verifying | implement | — | all six gates green on wi/WI-0004; 115 tests over AC1-AC15; 15 mutations all caught, including the three that escaped on WI-0002 and WI-0003 |
| 2026-08-21T20:32:29Z | verifying | in-review | verify | — | AC1-AC15 all pass on f3be13c; the three gaps inherited from WI-0002 and WI-0003 confirmed closed by mutation; 1 new finding, no defects |
| 2026-08-21T20:35:22Z | in-review | done | review-close | — | DoD D1-D12 all pass; epic DE1-DE4 pass with all four success measures run; trial merge clean with 115 tests green; 3 findings recorded |
