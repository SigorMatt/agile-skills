# Harness status — turn 9

No question was open when this turn started, so nothing needed consuming and the loop ran straight
through. Three skill executions: **WI-0002 was verified, reviewed, merged into `main` and closed as
`delivered`**, and **WI-0004 was taken up, refined as far as it can go without the stakeholder, and
suspended on one question to them**. The turn ends on a real pipeline stopping point — an open
human-addressed question — and the budget ran out at the same moment.

- **`verify` on WI-0002 → `in-review`.** All six criteria confirmed by commands run here, against
  fresh scratch stores, with output quoted. The one that mattered: AC3's five properties were
  checked against positions **recomputed from the raw stored JSON by a script written in the
  skill**, not by calling `expenses/settle.py`'s own `positions()` — a wrong `positions()` would
  otherwise have produced a self-consistent wrong answer that every property still held over. Six
  mutations, each reverted, establish that every criterion has a test that fails when its behaviour
  is disabled. One qualification found and recorded: **AC1's end-to-end test cannot see ADR-0005's
  tie-break**, because AC1 compares *sorted* stdout, so reversing the tie-break leaves it green;
  the rule is pinned only by two function-level tests. Not a defect — AC1 says what it says — but a
  fact about which test is load-bearing, so it was carried onto the item at close. Four gaps
  declared unverified. No defect found, no bug filed, nothing sent back.
- **`review-close` on WI-0002 → `done`, merged.** D1–D12 each recorded with its own evidence. The
  diff was read hunk by hunk and every hunk maps to a plan step; ADR-0005 was read in full against
  `expenses/settle.py` and the code implements it exactly, tie-break included. **D12 was decided by
  opening each citation**, eight claims in all — including one *pre-existing* claim that adding a
  command could have falsified ("every refusal writes to stderr and exits non-zero"), which holds
  because `settle` returns through `main()`'s common `except ExpensesError` rather than a new path.
  That is the case D12 exists for: nobody was obliged to re-check a WI-0001 sentence while
  delivering WI-0002. Trial-merged into a throwaway branch off `main` (clean, 86 tests green),
  discarded, closed while still unmerged so `check-commit-refs` had a range, then merged for real.
  Five accepted gaps moved out of the reports and onto the item.
- **`refine` on WI-0004 → `awaiting-answer`.** See below.

## The question, and why it is the only one

**`WI-0004/Q-001` — when you delete a person who is named in expenses you have already recorded,
what should the tool do?** Four options: **A** refuse and name the expenses in the way; **B**
delete the person and every expense they appear in; **C** delete the person and leave the expenses;
**D** refuse by default with an opt-in flag for B. Recommendation **A**. Option C is argued
*against* rather than offered neutrally, because it is the only one that can make `settle` print a
wrong answer without saying so — and it is exactly the unreachable-today state that WI-0002's
review recorded `positions()` as silently tolerating.

It is theirs on the two counts `refine`'s ownership test names explicitly: it is *what happens to
their data*, and it is *irreversible*, since they already ruled out an undo. The item's draft AC3
guessed at option A, but `answer-questions` wrote that criterion when it created the item, not the
stakeholder — so it was treated as the guess it is rather than as a settled rule.

**Eight other gaps were assessed and not asked**, each with its verdict in the Q&A so that "only
one question" is auditable. The closest call was how an expense is named on the command line: an
expense carries **no identifier at all** — verified by building a store with the delivered commands
and reading the JSON back — so a handle has to be invented and no option changes nothing. Decided
under WI-0001's A1 precedent (which fixed a whole command surface without asking), recorded as D2
with both rejected alternatives and its stated cost, so the stakeholder can object to it in one
glance. One gap the item said refinement must settle turned out to need nobody: "an expense that
has already been settled" has no answer because **there is no such state** — `settle` writes
nothing and marks nothing as paid. That was answered by reading, not decided.

`refinement-qa.md` is `status: agenda`, not `recorded`, because the conversation has not happened —
which is what R8 reads, and is the honest value. Seven acceptance criteria are drafted there and
deliberately **not installed** in `item.md`, because two depend on the answer.

## State

`engagement-state EP-001` reports **active** — BUG-0001, BUG-0002 and WI-0004 in flight, plus the
open question — so no sign-off is due and none was filed. WI-0003 is still parked on the bank CSV
sample; nothing this turn touched it, and no question was re-filed for it because `blocked` is not
suspendable, so a question there could not be accompanied by the suspension the protocol requires.
BUG-0001 and BUG-0002 remain `ready` and were deliberately left alone. Workspace validates 0 errors
0 warnings; tree clean on `main` at `427a8c3`; 86 tests green on the trunk.

## Notes on the toolkit

1. **`outcome` and `status: done` cannot be written together, and one order or the other must fail
   validation.** `spec/work-item.md` requires `outcome` if and only if `status: done`, but
   `transition`'s `--resolving` models only the status change. Setting `outcome: delivered` before
   the transition failed the pre-flight `workspace-valid` hard gate with `item.outcome.premature`;
   removing it let the transition through, which then reported *"the transition was applied, but
   the workspace no longer validates"* with `item.outcome.missing` — a non-zero exit on a move that
   succeeded. The workaround is to write `outcome` immediately afterwards, but a `review-close` that
   stopped at the first non-zero exit would leave a `done` item in an invalid workspace. Easiest
   fix: teach `--resolving` that a resolution to `done` implies an outcome, or let `transition` take
   `--outcome`.
2. **`lint-claims --changed-since main` still overstates its scope** (turn 7 finding 6, turn 8
   finding 2 — now three turns running). Run at review time with `README.md`,
   `docs/architecture/overview.md`, `expenses/settle.py` and two test files changed on the branch,
   it printed `checked 1 document(s)` and exited 0. Correct behaviour, misleading summary: an exit 0
   on that line reads as coverage it does not have. The eight-claim D12 table in `review.md` is what
   actually carried that gate.
3. **`board-gen` says "board already current; not rewriting the timestamp" even when the board was
   regenerated by `transition` moments earlier** (turn 8 finding 4, reproduced). A skill calling
   `board-gen` as its own gate gets no positive confirmation that the board reflects the state it
   just wrote.
4. **`check-verify-freshness` is the good counter-example and deserves saying so.** It did not just
   compare hashes: it reported *"wi/WI-0002 has moved to 04e662c2 but only the record changed (5
   file(s) under tracker/ or docs/), so the verification still covers the code"*. That is a gate
   explaining its own reasoning, and it is exactly what D10 needs — the other scripts' terse
   summaries are what findings 2 and 3 are about.
5. **The `**Status:**` bullet workaround was not needed this turn.** Writing the real move into the
   journal body and letting `transition` overwrite it worked cleanly three times. Turn 8's finding 3
   may have been about writing a *placeholder*; writing the actual `from → to` is fine.

```json
{
  "stop_reason": "human-question-open",
  "skills_run": ["verify", "review-close", "refine"],
  "open_human_questions": ["WI-0004/Q-001"],
  "items_touched": ["WI-0002", "WI-0004"],
  "last_action": "refine filed WI-0004/Q-001 to the stakeholder and suspended WI-0004 at awaiting-answer with resume-to draft",
  "notes": "Three executions; the turn ended on an open human question and on the budget at the same moment. WI-0002 is delivered: verified with evidence gathered independently (AC3's properties checked against positions recomputed from raw JSON, not from the code under test), reviewed against D1-D12 with D12 decided by opening each citation, trial-merged, closed, and merged into main. 86 tests green on the trunk. Five accepted gaps were moved from the reports onto the item so they survive the close - most consequentially that positions() silently drops a name absent from data['people'], which WI-0004 must solve. verify found by mutation that AC1's end-to-end test cannot detect a change to ADR-0005's tie-break, since AC1 compares sorted stdout; recorded, not sent back. WI-0004 then got one question to the stakeholder - what deleting a person does to their expenses - with eight other gaps assessed and closed without them, four assumptions recorded under WI-0001's A1 precedent, and one gap answered by reading rather than deciding. refinement-qa.md is status: agenda and seven drafted criteria are deliberately not installed. EP-001 is active, not at rest. Toolkit: a new and real defect - outcome and status:done cannot be written together, because transition's --resolving does not model the dependent field, so review-close must take a non-zero exit on a transition that actually succeeded; plus lint-claims overstating its scope for the third turn running."
}
```
