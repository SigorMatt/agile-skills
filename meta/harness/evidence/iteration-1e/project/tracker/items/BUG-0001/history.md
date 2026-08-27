# History — BUG-0001

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-27T00:11:41Z | — | ready | verify | — | found while verifying WI-0001: lint-claims --all exits 1 on docs/product/vision.md lines 31 and 38, whose absolute claims carry no citation marker (spec/doc-header.md section 4a) |
| 2026-08-27T02:16:21Z | ready | planned | plan | — | design recorded as ADR-0009 (a document-only defect is fixed by the item that owns it, so implement edits vision.md) and plan.md written: eight steps, four criteria mapped, and a removal-and-restore check so AC1 cannot pass by the linter falling silent |
| 2026-08-27T02:16:58Z | planned | in-progress | implement | — | branch wi/BUG-0001 created from main at 7f5ac6c; executing the plan's eight steps |
| 2026-08-27T02:19:28Z | in-progress | verifying | implement | — | vision.md at version 4 with a resolvable citation on each of the two absolute claims; lint-claims --all exits 0 over the whole tree, and each marker was removed in turn to prove the linter still examines both paragraphs |
| 2026-08-27T02:24:18Z | verifying | in-review | verify | — | All four acceptance criteria pass with evidence gathered in this execution at 76e62a6; each citation was removed and restored to prove the linter still examines both paragraphs |
| 2026-08-27T02:28:28Z | in-review | done | review-close | — | Definition of Done passes D1 to D12 with per-criterion evidence; the two claims audited by opening what they cite, the trial merge fast-forwards and the suite passes on the merge result |
