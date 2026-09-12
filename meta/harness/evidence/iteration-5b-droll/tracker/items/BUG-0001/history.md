# History — BUG-0001

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-09-11T22:47:26Z | — | ready | verify | — | Filed by verify while verifying WI-0001: 3289 bytes of captured run-gate output committed to the repository root at 6788e55 by WI-0001's plan execution, outside every acceptance criterion of the item being verified |
| 2026-09-11T23:18:10Z | ready | planned | plan | — | plan.md written: four steps and one deletion, git rm planned on wi/BUG-0001 merged to the trunk by the ordinary close. No droll source, test or document is touched and no ADR was needed - both decisions were answered from existing documents. The invalidation set is none, deliberately: ADR-0004 point 4a records that --plan-documents widens implement's claims-are-sourced window to every document a plan names, so naming docs/product/vision.md defensively would drag an engagement-state sentence nobody may repair into this item's window. All four ADRs are listed, two binding and two not-engaged |
