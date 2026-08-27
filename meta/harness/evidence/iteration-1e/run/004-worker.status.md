# Harness status — turn 4

The stakeholder had answered all three of intake's questions on EP-001 since the last turn, so
this turn consumed them first, then refined the first work item until it needed them again.

**`answer-questions` on EP-001.** Two of the three replies were answers and one was a deferral.

- Q-002 answered: "who owes whom" means a list of payments that settles the group, not net
  positions. Propagated into WI-0002 — AC1–AC3 amended, AC4 added (the same data must print the
  same payments in the same order, which was part of what the chosen option entailed), net
  positions recorded as out of scope since they were offered and not chosen.
- Q-003 half answered, half delegated. The stakeholder handed us the ordering ("whatever you
  think is best"), so it was decided here: WI-0001, WI-0002, WI-0003. They refused to drop
  anything ("the import's part of what I asked for too"), so WI-0003 went from `medium` to
  `high`. Checked that this does not reorder anything — the selection key breaks a priority tie
  on `created`, and WI-0002 is two seconds older.
- Q-001 was a deferral: *"I'll send you a sample later."* That takes option A and refuses
  inventing a layout or dropping the item, but it is not the layout. Move 1 of `question.md` §2
  was taken — decide under the deferral — and the decision is the one Q-001's own recommendation
  named for exactly this reply: park WI-0003 and deliver the rest. **WI-0003 is at `blocked`**
  with `resume-to: draft` and one exit condition written into its notes: a sample of the bank's
  CSV export, or its header row plus two or three example rows. Nothing about the format has
  been invented.

EP-001 returned to `open`, its recorded `resume-to`. The vision went to v2.

**`refine` on WI-0001.** Definition of Ready fails on R4 (every criterion said "a documented
command" and named none, so none is decidable), R8 (no Q&A record existed) and R10 (seven
behaviour combinations had no stated behaviour). R1, R2, R3, R5, R6, R7, R9 pass.

Every gap was sorted by who owns it before anything was filed. **Seven were refinement's own and
are now decided** and written into the item's `## Notes`, each marked `[assumed — refine, not
asked]`: the command surface (`python3 -m expenses person|expense …`), exit codes and streams,
person identity, what an amount is, the sharer rules, the requirement that shares sum exactly to
the amount paid, and leaving the store's location to `plan`. Two further design questions went to
`plan` rather than to a person: the remainder rule (constrained only to be deterministic) and
where the data lives.

**Three went to the stakeholder**, filed as one ask, each one decision, each changing what the
software is or what counts as correct. The acceptance criteria were deliberately *not* rewritten
— AC2 and AC3 depend on two of the pending answers — but the proposed AC1–AC6 are written out in
`artifacts/refinement-qa.md`, which stays at `status: agenda` because the conversation has not
happened. The next execution folds in three answers instead of repeating the analysis.

Stopped on the first stop condition after that: human-addressed questions are open. Two of the
three skill executions in the budget were used; the third was not started, because filing the
questions is what ended the turn.

**Two things about the toolkit.**

1. **An epic-level question cannot legally be marked `deferred`.** `validate-workspace` applies
   `question.deferred.not-blocked` to every item type, requiring the item carrying the question to
   be at `blocked`; but `pipeline.yaml` scopes `awaiting-answer → blocked` for `answer-questions`
   to `work-item` and `bug`, and an epic may reach `blocked` only as the E3 impasse ending through
   `review-close`. So `deferred` on an epic-level question produces a workspace no legal move can
   repair. Move 1 was available here so this execution was not forced, but a deferral that could
   not be decided under would have left `answer-questions` with no legal action at all. The
   deferral machinery assumes the deferred question lives on the item it parks. Recorded in
   EP-001's journal.
2. **`transition --journal-body-file` rejects a body with no `**Status:**` bullet**, even though
   the documentation says the tool writes that bullet itself from the move it actually made
   (`journal-and-history.md` §2.2, and the transition's own `--help` step 5). Minor, but it costs
   a failed invocation the first time.

```json
{
  "stop_reason": "human-question-open",
  "skills_run": ["answer-questions", "refine"],
  "open_human_questions": ["WI-0001/Q-001", "WI-0001/Q-002", "WI-0001/Q-003"],
  "items_touched": ["EP-001", "WI-0001", "WI-0002", "WI-0003"],
  "last_action": "refine filed three questions on WI-0001 and suspended it to awaiting-answer with resume-to: draft",
  "notes": "EP-001's three intake questions are all consumed and propagated; the epic is back at open. WI-0003 is parked at blocked awaiting the bank CSV sample the stakeholder said they would send - that is the honest state, not a failure, and the epic cannot end as fully delivered until it moves. Two toolkit findings above: an epic-level question has no legal `deferred` state, and transition rejects a journal body missing the Status bullet it writes itself."
}
```
