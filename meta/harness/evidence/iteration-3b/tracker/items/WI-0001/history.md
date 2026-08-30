# History — WI-0001

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-29T21:12:23Z | — | draft | intake | — | created from the idea for EP-001: the core filter behaviour |
| 2026-08-29T21:30:19Z | draft | awaiting-answer | refine | draft | round 1 of refinement filed as Q-001 to Q-004, all blocking to human: cell width for non-ASCII text, indented tables, cell padding, and the delimiter row's appearance |
| 2026-08-29T21:39:23Z | awaiting-answer | draft | answer-questions | — | round 1 answered by the stakeholder and propagated into ADR-0003, vision v3 and both items; no blocking question remains |
| 2026-08-29T21:43:42Z | draft | ready | refine | — | round 1 answered and recorded verbatim; criteria rewritten as AC1-AC11, each observable; DoR met on all ten criteria with no override |
| 2026-08-29T21:49:46Z | ready | planned | plan | — | plan.md written with all 11 criteria mapped to named fixtures, ADR-0004 records that the delimiter row keeps its alignment markers, overview.md created, and project.yaml now names verified test and lint commands |
| 2026-08-29T21:51:42Z | planned | in-progress | implement | — | branch wi/WI-0001 created from main; executing artifacts/plan.md from step 1 |
| 2026-08-29T22:03:44Z | in-progress | verifying | implement | — | all eight gates pass on branch head e2beac6; impl-report.md maps every criterion to a named test, checked against nine mutations |
| 2026-08-29T22:10:05Z | verifying | in-review | verify | — | all 11 criteria pass on independently gathered evidence at c1c79dc; 22 self-written inputs, every negative case triggered, 11 mutations confirm test sensitivity; no defects |
| 2026-08-29T22:14:55Z | in-review | done | review-close | — | accepted: D1-D12 all pass with evidence, diff read hunk by hunk, tests green on the merge result at cad9b3b; outcome delivered |
