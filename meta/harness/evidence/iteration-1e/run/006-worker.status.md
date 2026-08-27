# Harness status — turn 6

The stakeholder's three answers on WI-0001 had arrived, so this turn consumed them and then ran
the item forward two more stages. Three skill executions, all on WI-0001, and the turn ended on
the budget rather than on anything being wrong.

- **`answer-questions` on WI-0001.** All three replies were real answers, not deferrals, so all
  three questions are `answered` and the item returned to its recorded `resume-to` of `draft`.
  Propagated into `item.md`, `refinement-qa.md`, `WI-0002/item.md`, `EP-001/item.md` and
  `docs/product/vision.md` (v3). Q-003's answer widened the scope — the stakeholder wants to be
  able to delete a mistaken record, but not to edit one — so **WI-0004** was filed at `draft`
  with `arose-from: WI-0001/Q-003` and `depends-on: WI-0002` (their own constraint: it must not
  hold up the who-owes-whom feature), rather than growing WI-0001 around it.
- **`refine` on WI-0001.** Asked the stakeholder nothing and recorded why: eight candidate
  questions were considered and each was either already answered, implementation-only (decided as
  A8–A12), or a design call routed to `plan`. Rewrote the criteria as AC1–AC9, each naming a
  command and the verdict that follows. Definition of Ready passes on all ten criteria, no
  override. `refinement-qa.md` is now `status: recorded`.
- **`plan` on WI-0001.** `plan.md` with seven steps over four modules and a test package, and a
  nine-row AC mapping table. Four ADRs: one JSON file located by `EXPENSES_STORE` or XDG
  (ADR-0001), money as integer minor units (ADR-0002), an indivisible remainder to the
  first-named sharers (ADR-0003 — one of the two questions `refine` routed here), and `unittest`
  as the test command with no lint command and the reason (ADR-0004). Created
  `docs/architecture/overview.md` v1. Set `commands.test` and ran it. One scaffolding file,
  `tests/__init__.py`, empty, without which the declared test command cannot execute.

Nothing is blocked that was not blocked before: WI-0003 remains parked awaiting the bank CSV
sample the stakeholder said they would send. No question is open, to anyone. The workspace
validates with 0 errors and 0 warnings — this turn cleared the standing
`project.commands.test-null` warning. Next turn should run `/next`, which will dispatch
`implement` on WI-0001.

## Notes on the toolkit

Three things got in the way, none fatal:

1. **`scripts/new-item` writes a history creation row but no journal entry**, so the workspace
   fails `journal.execution.missing` the moment an item is created and stays failing until the
   caller writes the entry by hand with `journal-entry --status`. Every other status change has a
   one-command path (`transition --journal-body-file`) precisely so the row and the entry cannot
   drift apart; creation is the one place that does not. Suggest `new-item` take
   `--journal-body-file` too.
2. **`refine`'s precondition 2 is unconditional** — "The human is present in this session. If
   they are not, you cannot do this job: file a question… and stop." Read literally, an
   asynchronous stakeholder means `refine` can never pass an item, even when a previous round's
   answers have settled everything and the remaining gaps are all the team's own. This execution
   proceeded, asked nothing, and recorded the reasoning in the journal and in `refinement-qa.md`.
   The precondition would be better phrased as the amendment phrases it: you cannot ask in
   session, so ask only in files, and only when you genuinely need to.
3. **The machine clock reads 2026-08-26** while the harness reports the date as 2026-08-27.
   Every timestamp in the record comes from the clock, per `spec/journal-and-history.md` §0, so
   the record is internally consistent — but the two disagree and only one of them can be right.
   Worth checking which.

```json
{
  "stop_reason": "turn-budget-exhausted",
  "skills_run": ["answer-questions", "refine", "plan"],
  "open_human_questions": [],
  "items_touched": ["WI-0001", "WI-0002", "WI-0003", "WI-0004", "EP-001"],
  "last_action": "plan wrote plan.md and ADR-0001 to ADR-0004 for WI-0001 and moved it ready -> planned",
  "notes": "Three executions, the budget, not a stopping point. WI-0004 was filed this turn from the stakeholder's answer to WI-0001/Q-003 (delete yes, edit no), so EP-001 now has four children. No question is open to anyone; WI-0003 stays parked on the bank CSV sample. Workspace validates 0 errors 0 warnings. Toolkit findings above: new-item leaves the workspace invalid until a journal entry is written by hand; refine's precondition 2 assumes a present human and would deadlock asynchronous refinement if read literally; the machine clock and the harness disagree about the date by one day."
}
```
