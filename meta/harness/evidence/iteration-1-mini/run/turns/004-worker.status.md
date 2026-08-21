# Harness status — turn 4

The stakeholder had answered **all twelve** open questions between turns. Consuming them was the
whole of the first half of this turn, and it unblocked everything.

- Ran `answer-questions` on EP-001, WI-0001, WI-0002 and WI-0003 — the skill's first precondition
  reads as though it only covers architect-addressed questions, but its step 4 provides for
  `answered-by: human` and nothing else in the pipeline can consume a human's answer, so it did
  that job and said so in each journal.
- Propagated every answer into the artifacts the next skill actually reads. WI-0001, WI-0002 and
  WI-0003 each returned to their recorded `resume-to: draft`. Their acceptance criteria grew from
  4, 5 and 4 to 8, 8 and 7.
- Wrote six ADRs for the decisions the stakeholder delegated or that their words did not reach:
  Python 3.9+ stdlib-only; one store file per user; sharers are exactly who you name; the payer
  absorbs the rounding remainder with money as integer minor units; greedy settlement with no
  claim of minimality; and the CLI surface, which is what let a name contain a comma.
- Then ran the pipeline: `refine` → `plan` → `implement` on WI-0001. It is at `verifying` on
  branch `wi/WI-0001` with **18 passing tests**, an implementation report mapping every criterion
  to a named test, and the lint gate honestly recorded as skipped rather than passed.
- Filed one new question, `EP-001/Q-006`, and stopped.

**What refused to pass:** nothing. No gate failed, no override was recorded, `validate-workspace`
is at 0 errors and 0 warnings, and the `project.commands.test-null` warning that had been standing
since turn 1 is cleared.

**The one thing worth your attention before more code is written** is in WI-0002's `## Notes`.
Your answer to WI-0002/Q-002 was *"If I paid and it's shared by all of us, include me
automatically"* — conditional on the everyone case, which is now the default and costs you no
typing. It does not say what should happen when you name sharers explicitly and leave yourself
off. ADR-0003 decides that such a list means literally what it says, and adds a warning on stderr
as a guard. That is cheap to change **now** and impossible to change once expenses are stored,
because the data cannot distinguish "did not share" from "forgot to type my own name".

**The `blocking` field on Q-006 is `false` and should not be.** An epic at `open` is
`terminal: true` in `pipeline.yaml`, so there is no legal transition that suspends one, while
`validate-workspace` reports `question.blocking.not-suspended` if an epic carries an open blocking
question. The two rules contradict each other. Being addressed to `human` is what actually stops
the loop.

**Working tree is on `wi/WI-0001`, not `main`, deliberately.** WI-0001's tracker record — its
`verifying` status, its implementation report, its journal — lives on that branch until
`review-close` merges it. Checking out `main` would make the next turn read WI-0001 as `planned`
and re-run `implement` over its own work.

```json
{
  "stop_reason": "human-question-open",
  "open_human_questions": ["EP-001/Q-006"],
  "items_touched": ["EP-001", "WI-0001", "WI-0002", "WI-0003"],
  "last_action": "answer-questions filed EP-001/Q-006 escalating the bank CSV import request, after refine, plan and implement took WI-0001 to verifying with 18 passing tests",
  "notes": "Three toolkit findings, each journalled where it happened. (1) `next` can never dispatch `answer-questions` for a human-answered question: orchestrator step 2 stops the loop on any open human-addressed question and never reaches step 3, so the skill has to be started directly, and its first precondition is written as though only architect-addressed questions qualify. (2) `transition`'s pre-move gate run evaluates `workspace-valid` against the workspace *before* the move it is about to make, so it printed FAIL for every `answer-questions` resume - questions already `answered`, item still `awaiting-answer`, board not yet regenerated - while `transition` itself said the gates were not blocking and the post-move validation was clean. It is checking the wrong side of the transition. (3) `implement` must pass through a red validator: its step 3 requires moving to `in-progress` before writing code, its step 9 requires the journal entry at the end, so `journal.execution.missing` fires in between on every run. Also, an epic cannot be suspended at all (`open` is terminal, transitions into `awaiting-answer` are `from: any-non-terminal`), which makes `blocking: true` unusable on epic questions while the validator still demands suspension for one - the contradiction Q-001 and Q-006 both document. Finally, on this prompt rather than the toolkit: amendment A (batch every question before you stop) and amendment E (stop when a human question is open) pull against each other, because orchestrator step 2 stops the loop on the first one filed. I resolved it by doing all reachable work first and filing Q-006 last, and journalled that choice on EP-001 so the next turn does not have to guess why the question is timestamped after the implementation."
}
```
