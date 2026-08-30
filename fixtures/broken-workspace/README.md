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
| 2026-08-27 | `WI-0003` reaching `ready` on a `refinement-qa.md` that declares `status: agenda` | Definition of Ready R8 reading a field rather than a filename (F-031) |
| 2026-08-27 | `WI-0003` — an item `answer-questions` created with no `arose-from`, carrying a **deferred** blocking question while still at `draft`, and claiming an epic-only outcome; `arose-from: WI-0404` on `BUG-0001` | the creation-authority table (F-029), the deferral status (F-028), and the endings model (ADR-0006). `epic.closed-with-open-children` became `epic.closed-with-active-children` + `epic.outcome.overclaims`: "every child is done" was the entry condition for one ending out of four, and what replaces it is "every child has stopped, and an epic that closes over an undelivered child may not call itself delivered" |
| 2026-08-29 | `ADR-1-Bad_Name.md` gains a `## Corrections` table with an unsourced entry, an erratum that does not quote what it removed, a third kind nobody defined, one change-log row too few and a section after it; `ADR-0002-a-superseded-decision-that-was-corrected.md` carries an empty repair record on a decision that no longer stands | `doc-header.md` §4b — the legal repair for a standing ADR (F-067). The repair had to become possible before its shape could be wrong: before this, three *true* claims in an accepted ADR had no move that cleared them |
| 2026-08-29 | `WI-0001/Q-002` — an `elicitation` question that blocks and is addressed to the architect, with the recommendation printed in `## Context` and again above the options | the presentation rule (F-063) and `kind: elicitation` (F-064). Both failures are layout, not wording, so both are checked positionally |
| 2026-08-30 | `ADR-0002` becomes genuinely `superseded` and takes a correction dated *after* its supersession; `ADR-0003-an-empty-repair-record.md` carries the empty-section case it used to hold | F-069 — §4b's rule is about the **act**, not the state. As a state rule it described a document that could not exist: legitimately corrected while accepted, legitimately superseded afterwards, and permanently invalid. The legal shape is in `examples/toy-project`'s `ADR-0010` |
