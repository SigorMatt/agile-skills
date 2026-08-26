# Deliberately broken workspace

Every file here is wrong on purpose. `scripts/check` runs `scripts/validate-workspace` against
this tree and asserts that the set of finding codes it produces equals `EXPECTED-CODES.txt`
exactly — so a rule that silently stops firing fails the build, which is the failure mode a
validator is most prone to and least likely to notice.

Do not "fix" anything here. To change what is covered, change the fixture *and*
`EXPECTED-CODES.txt` in the same commit, and say why in the commit message.

## What was added, and when

| Date | Cases | For |
|------|-------|-----|
| 2026-08-27 | `WI-0003` — an item `answer-questions` created with no `arose-from`, carrying a **deferred** blocking question while still at `draft`, and claiming an epic-only outcome; `arose-from: WI-0404` on `BUG-0001` | the creation-authority table (F-029), the deferral status (F-028), and the endings model (ADR-0006). `epic.closed-with-open-children` became `epic.closed-with-active-children` + `epic.outcome.overclaims`: "every child is done" was the entry condition for one ending out of four, and what replaces it is "every child has stopped, and an epic that closes over an undelivered child may not call itself delivered" |
