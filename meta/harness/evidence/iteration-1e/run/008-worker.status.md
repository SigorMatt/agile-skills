# Harness status — turn 8

No question was open when this turn started, so nothing needed consuming and the loop ran
straight through. Three skill executions, all on WI-0002, which went from `draft` to `verifying`
on branch `wi/WI-0002`. The turn ended on the budget, not on a stopping point. **No question was
filed this turn, to anyone** — see "Why nothing was asked" below, because that was the turn's main
judgement call.

- **`refine` on WI-0002.** Definition of Ready re-assessed criterion by criterion; R4, R8 and R10
  were failing on entry and all three now pass. The four criteria `answer-questions` left were
  rewritten and two were added: AC1 pins an exact pair of output lines, AC2 covers three ways to
  have nothing to settle (the original covered one), AC3 states the settlement properties against a
  five-person dataset whose figures were computed by *building the store with the delivered tool*
  rather than by hand, AC4 becomes a `cmp`, AC5 is new (the command writes nothing, and creates no
  data file where none exists), AC6 is new (the README documents it). `## Out of scope` went from
  four entries to seven. The Q&A file records eight candidate questions and the reason each was not
  asked.
- **`plan` on WI-0002.** Seven steps over three files, every criterion mapped to a step and to a
  specific demonstration. One ADR — **ADR-0005**, match the largest debt against the largest
  credit, ties in both pools broken by the order people were recorded — chosen over three named
  alternatives including the exponential minimum-transaction search. Worked against AC1's and
  AC3's own datasets inside the ADR, so the decision can be checked rather than believed. Three
  reversible assumptions recorded with what reversal costs. `docs/architecture/overview.md` went to
  v2 describing the module under "What is coming", deliberately not in the body, because the module
  did not exist yet and a doc that says otherwise is false.
- **`implement` on WI-0002.** Branch `wi/WI-0002` off `main` at `55536ec`, moved to `in-progress`
  before any code was written. All seven plan steps in order, six commits. `expenses/settle.py` is
  60 lines and two pure functions; `cli.py` gains a third top-level command and one handler that
  calls nothing which writes. **50 tests to 86.** Six gates pass on the branch head; `lint-clean` is
  `skipped` on ADR-0004's record. Every criterion was also run by hand on the branch head against
  fresh temporary stores, with the output quoted in `impl-report.md`. Three deviations declared,
  all in *how*.

## Why nothing was asked

WI-0002 is the item that answers the stakeholder's original question, so a turn that refined it
without asking them anything deserves its reasons stated plainly.

The one product-stake decision on this item — whether "who owes whom" means net positions or a
list of payments — was put to them as EP-001/Q-002 and answered: *"The list of payments that
settles it."* That answer went further than the choice. It states that the settlement **rule** —
which of several equally valid settlements to prefer, and in what order to print it — "is not the
stakeholder's to decide; it is refinement's, and then `plan`'s". Every remaining gap on the item
was that rule, or a naming or wording call of the kind WI-0001's refinement had already taken
without asking (its A1–A12). Eight candidates were considered and each is recorded in
`refinement-qa.md` with its verdict, so "nothing was asked" is auditable rather than asserted.

The closest call was whether the stakeholder should be asked to accept that a settlement computed
from net positions can tell one person to pay someone they never shared an expense with. It was not
asked, because it is a property of *which settlement is chosen* and therefore squarely inside what
Q-002 delegated. It is instead recorded on the item under `## Out of scope`, in the README in plain
words, and under ADR-0005's consequences — so a reader can tell it from an oversight, and the
stakeholder will meet it in the README rather than in a surprise.

## State

`engagement-state EP-001` reports **active** — BUG-0001, BUG-0002, WI-0002 and WI-0004 in flight —
so no sign-off is due and none was filed. WI-0003 is still parked on the bank CSV sample the
stakeholder said they would send; nothing this turn touched it. The workspace validates with 0
errors and 0 warnings and the branch's suite is green. The working tree is clean and checked out
on `wi/WI-0002`, which is where `verify` needs it.

Next turn's `/next` should dispatch `verify` on WI-0002.

## Notes on the toolkit

Two findings from turn 7 reproduced exactly, which is worth more than a fresh report: they are not
flukes.

1. **`check-commit-refs` still mis-diagnoses an empty range on a fresh branch** (turn 7, finding 3).
   At `planned → in-progress` the branch had no commits, and the gate reported "wi/WI-0002 is
   already merged into main ... Rewind the merge, close, then merge" — advice for the opposite
   situation. The transition correctly did not block on it, since `implement` only gates its
   completion move, but a hard-gate FAIL with confidently wrong remediation advice is the kind of
   thing a less careful run acts on. The range is empty because nothing has been committed.
2. **`lint-claims --changed-since main` still reports a scope it does not have** (turn 7, finding
   6). Run after step 6, with `README.md` edited and uncommitted, it printed "checked no documents
   changed since main" and exited 0. Later, with `docs/architecture/overview.md` modified, it
   printed "checked 1 document(s)". So the rule-2 scope looks `docs/`-only and uncommitted
   working-tree changes do not count — but the summary line reads as full coverage, and an exit 0
   on it would be taken for more than it is.
3. **The `**Status:**` bullet is still required in a body whose `**Status:**` bullet the tool
   overwrites** (turn 7, finding 2). Worked around again by writing a placeholder before each
   transition. Cheap, but it is a rule you only learn by having a transition refused.
4. **`board-gen` reports "board already current; not rewriting the timestamp" when it is current**,
   which is right — but it means a skill that calls `board-gen` as its own gate gets no positive
   confirmation that the board reflects the state it just wrote. In this turn the board was in fact
   regenerated by `transition`, so the message was accurate; a reader of the journal could not tell
   that from the message alone.
5. **`validate-workspace` catches change-log row order after the fact.** Appending a new version row
   to a `docs/` change log in the natural place — the bottom — fails `doc.changelog.order`, because
   rows are newest-first. Correct rule, but the error arrives after the write; the two documents in
   this project that have change logs both have a single row, so there is nothing in the file to
   pattern-match against.

Nothing was fixed that this turn's item does not cover: BUG-0001 and BUG-0002 are both still open
at `ready` against WI-0001's delivered behaviour, and both were deliberately left alone.

```json
{
  "stop_reason": "turn-budget-exhausted",
  "skills_run": ["refine", "plan", "implement"],
  "open_human_questions": [],
  "items_touched": ["WI-0002"],
  "last_action": "implement moved WI-0002 in-progress -> verifying with 86 tests green on wi/WI-0002 at 6b2fb40",
  "notes": "Three executions, the budget, not a stopping point. WI-0002 went draft -> ready -> planned -> in-progress -> verifying in one turn and is unmerged on wi/WI-0002. The settle command is built: two pure functions in a new expenses/settle.py, a third top-level CLI command, 50 tests to 86, every criterion also run by hand on the branch head with output quoted in impl-report.md. ADR-0005 records the settlement rule and was checked against the item's own two datasets inside the ADR. No question was filed to anyone: EP-001/Q-002's answer explicitly assigned the settlement rule to refinement and plan, and the eight candidates considered are recorded with the reason each was not asked. EP-001 is active, not at rest. WI-0003 stays parked on the bank CSV sample. Workspace validates 0 errors 0 warnings; tree clean on wi/WI-0002. Toolkit: two turn-7 findings reproduced exactly - check-commit-refs mis-diagnosing an empty range on a fresh branch as 'already merged', and lint-claims claiming a scope it does not have - which makes them reproducible defects rather than one-off observations."
}
```
