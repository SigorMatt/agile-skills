# History — WI-0001

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-21T21:07:03Z | — | draft | intake | — | created from idea refinement for EP-001 |
| 2026-08-21T21:30:39Z | draft | awaiting-answer | refine | draft | the stakeholder is not in this session; Q-001..Q-004 filed for the Definition of Ready failures (R4, R8, R10): command surface, name identity, data file location, output and exit codes |
| 2026-08-21T21:43:54Z | awaiting-answer | draft | answer-questions | — | Q-001 to Q-004 answered and propagated: ADR-0002 (CLI surface), ADR-0003 (name identity), ADR-0004 (data file), ADR-0005 (output and exit codes); item.md AC1-AC7 rewritten |
| 2026-08-21T21:52:24Z | draft | ready | refine | — | Definition of Ready passes R1-R10; AC1-AC8 each name a command and exact expected output; the four answered questions recorded verbatim in refinement-qa.md |
| 2026-08-21T21:57:32Z | ready | planned | plan | — | plan.md written with AC1-AC8 mapped to named tests; ADR-0006 (JSON, atomic write), ADR-0007 (unittest, project commands), ADR-0008 (launcher over expenses_tool) recorded; architecture overview created |
| 2026-08-21T21:57:50Z | planned | in-progress | implement | — | branch wi/WI-0001 created from main; starting plan step 1 |
| 2026-08-21T22:01:13Z | in-progress | verifying | implement | — | 27 tests pass and compileall is clean on wi/WI-0001 head 1dd3f09; AC1-AC8 each mapped to a named test in impl-report.md |
| 2026-08-21T22:03:41Z | verifying | in-review | verify | — | AC1-AC8 each independently checked against commit 5288776 with quoted output; 27 tests pass; three sensitivity checks failed as they should |
| 2026-08-21T22:05:54Z | in-review | done | review-close | — | Definition of Done D1-D12 pass with evidence in review.md; 27 tests pass on the trial merge result; two findings accepted and recorded in the item's Notes |
