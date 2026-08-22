# Harness status — turn 4

The stakeholder had answered all three of `intake`'s questions since the last turn, so this turn
began by consuming them, then took the pipeline one step further before it hit the human again.

**What I did**

- **`answer-questions` on EP-001** — consumed `Q-001`, `Q-002` and `Q-003` and propagated them
  into eight files, then returned the epic to its recorded `resume-to: open`.
  - `Q-001` (build order): WI-0001 → WI-0002 → WI-0003, and neither WI-0002 nor WI-0003 is
    optional — the stakeholder said explicitly they are not shipping without the import.
    Propagated by lowering WI-0003 to `medium` and adding `depends-on: WI-0002`.
  - `Q-002` (bank CSV): **deferred**, not answered — "I'll send you a sample later". Marked
    `answered` because that reply is what they said and it has a consequence, and recorded
    loudly as a deferral: no CSV shape was guessed, and WI-0003 now carries an instruction that
    `refine` must file a fresh question citing `Q-002` rather than attempt the item.
  - `Q-003` (repayments): **in scope**. Recorded as `ADR-0001` and folded into WI-0001 (AC7, AC8:
    record and persist a repayment) and WI-0002 (AC5, AC6: net it into the report).
- **`next`** dispatched `refine` on WI-0001 (`critical`, no unfinished dependencies; WI-0002 and
  WI-0003 both rejected on unfinished `depends-on`).
- **`refine` on WI-0001** — its precondition 2 (the human is present) fails in this session, so
  it did what its procedure specifies for that case. It assessed the Definition of Ready criterion
  by criterion first (**R4, R6, R8 and R10 fail**; R1, R2, R3, R5, R7, R9 pass), filed five
  blocking questions to the human, and suspended the item with `resume-to: draft`. **No acceptance
  criterion was rewritten** — the criteria are exactly as `intake` and `answer-questions` left
  them.

**What I filed** — five questions on WI-0001, each tied to a named DoR criterion and each with
options and a recommendation so a one-word answer is usable: `Q-001` equal vs uneven splits;
`Q-002` amount format and who absorbs the rounding remainder; `Q-003` whether an expense carries a
date; `Q-004` one fixed data file or pointable; `Q-005` whether `ana` is the same person as `Ana`.

**What refused to pass** — `refine`'s `definition-of-ready`, `criteria-are-decidable` and
`qa-recorded-verbatim` gates, all correctly, which is why WI-0001 is suspended rather than `ready`.
`validate-workspace` is at 0 errors, 1 warning (`project.commands.test-null`, `plan`'s to clear).

**Skills run, in order:** `answer-questions`, `refine`. Two of the three-execution budget; the
turn stopped on the open human questions, not on the budget.

**Deliberately not done** — I did not pre-file `refine`'s questions for WI-0002 or WI-0003.
Neither is runnable (both have unfinished `depends-on`), so neither has been reached, and
`Q-001`/`Q-002` on WI-0001 already constrain WI-0002's arithmetic — that cross-item effect is
noted inside those question files rather than duplicated. `refinement-qa.md` records the exclusion
and its reasoning so the next session does not re-derive it.

**Notes for the toolkit's owner**

1. **An architect can widen an epic's scope but cannot open the item that widening implies.**
   `pipeline.yaml` and `spec/ids-and-statuses.md` §4 make `— → draft` legal only for the actor
   `intake`; the other route in, `tracker/requests/`, is by `spec/request.md` §2 authored only by
   the human, so a skill may not write one on their behalf. `Q-003`'s own option A said "adds a
   fourth work item", the stakeholder chose it, and `answer-questions` had no legal way to create
   it. Folding into WI-0001 and WI-0002 worked **only because both happened to still be at
   `draft`**, where criteria are not frozen. Had either been `ready` or later, an accepted scope
   change would have had nowhere to go at all. Recorded in `ADR-0001` rather than smoothed over.
2. **A deferred answer has no representation.** A question is `open` or `answered`, and "I'll send
   you a sample later" is neither. Leaving it open deadlocks `next` forever (the F-011 shape);
   marking it answered says something untrue about the facts. I marked it answered and carried the
   deferral as an explicit blocker on WI-0003, but a third status — `deferred`, which does not stop
   the loop and does not claim the question was settled — would express this honestly.
3. **Delivery order can only be expressed as `priority`.** `selection_key` is priority rank, then
   `created`, then id. To encode the stakeholder's explicit "build the import last" I had to lower
   WI-0003 to `medium` — on an item they had just called non-optional. Three files now say in
   words that this is scheduling and not importance, which is a lot of prose to work around a
   missing field.
4. **DoR R8 is an `[auto]` check on `refinement-qa.md`.** When `refine` is interrupted before the
   conversation happens, the honest thing is to write the agenda down for the next session — but a
   file that merely exists could read to an automated check as R8 satisfied. I mitigated it with a
   banner as the first thing in the file; a `status:` field the checker reads would be better.
5. `scripts/board-gen` printed "board already current; not rewriting the timestamp" both times the
   loop called it, because the preceding `transition` had already regenerated it. Correct
   behaviour; it reads like a refusal. (Also reported in turn 2.)
6. `scripts/new-item --help` still fails with `new-item: --id is required`. (Reported in turn 2.)

```json
{
  "stop_reason": "human-question-open",
  "skills_run": ["answer-questions", "refine"],
  "open_human_questions": ["WI-0001/Q-001", "WI-0001/Q-002", "WI-0001/Q-003", "WI-0001/Q-004", "WI-0001/Q-005"],
  "items_touched": ["EP-001", "WI-0001", "WI-0002", "WI-0003"],
  "last_action": "refine assessed WI-0001 against the Definition of Ready, filed five blocking questions to the human, and suspended it at awaiting-answer with resume-to: draft",
  "notes": "Workspace validates: 0 errors, 1 warning (project.commands.test-null, plan's to clear). Two of three skill executions used; stopped on the open human questions, not the budget. EP-001/Q-001 and Q-003 were answered and propagated into 8 files (ADR-0001 created, vision.md v2, four new acceptance criteria across WI-0001 and WI-0002). EP-001/Q-002 was deferred by the stakeholder rather than answered; WI-0003 is recorded as unrefinable until the promised CSV sample arrives, with no CSV shape guessed. Main toolkit findings: answer-questions cannot create the work item an accepted scope widening implies (only intake may, and tracker/requests is human-authored), and the question protocol has no way to represent a deferred answer without either deadlocking next or overstating what was settled."
}
```
