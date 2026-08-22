# Harness status — turn 2

The tracker was empty at the start of this turn (only the provisioning commit existed), and no
questions were outstanding, so there was nothing to consume with `answer-questions`. I ran
`intake` on the stakeholder's idea in `IDEA.md`.

What `intake` produced:

- `EP-001` — *Track shared expenses in a friend group from the command line*, with a goal, four
  checkable success measures, scope and an explicit out-of-scope list.
- Three items at `draft`: `WI-0001` (people, expenses, persistence — `critical`), `WI-0002`
  (who owes whom — `high`, `depends-on: WI-0001`), `WI-0003` (import from a bank CSV export —
  `high`, `depends-on: WI-0001`).
- `docs/product/vision.md` v1, and `project.description` filled into `tracker/project.yaml`
  (`commands.*` left null on purpose — `plan` owns them).
- Commit `62d8398`, touching only `tracker/` and `docs/`.

What refused to pass: nothing. The workspace validates with 0 errors and one warning
(`project.commands.test-null`), which is `plan`'s to clear.

Why the turn stopped: three blocking questions are open to the stakeholder, all on `EP-001`,
which is suspended at `awaiting-answer` with `resume-to: open`. The items stay at `draft`.

- **`EP-001/Q-001`** — after `WI-0001`, build `WI-0002` (who owes whom) or `WI-0003` (CSV
  import) next, and is either optional for a first version? Filed rather than guessed because
  `next` executes a guessed priority as if it were intent. Recommends `WI-0002` first.
- **`EP-001/Q-002`** — the bank CSV's real shape (a few sample lines, header included), and the
  rule by which a bank row becomes a *shared* expense, since a bank row cannot know who shared
  it. `WI-0003` cannot be made Ready without this; four options offered, recommends "payer and
  sharers named once per import, with a way to limit which rows are taken".
- **`EP-001/Q-003`** — are repayments in scope for this epic? Held out of both items' scope
  *pending the answer* rather than decided; recommends "out of scope, but designed for", since
  the storage choice in `WI-0001` is made before the question would otherwise surface.

I deliberately did **not** pre-file `refine`'s questions on the three work items. The open gaps
are written into each item's `## Notes` (uneven vs equal splits, rounding, whether an expense
has a date, storage location, pairwise vs minimised transfers, re-import idempotency), but
`refine` has not been reached on any of them, and `Q-002`'s answer likely settles the date
question by itself — asking now would risk asking something the batch already answers.

Notes on the toolkit, for its owner:

- A skill's **first** transition on a freshly created item cannot satisfy the `workspace-valid`
  hard gate at gate time: `run-gate` runs before the journal entry that the same `transition`
  invocation is about to write, so it reports `journal.execution.missing` on the very item being
  moved. Here it was harmless — `intake` gates only its completion transition to `draft`, so the
  move went through, and the closing `validate-workspace` reported 0 errors. But a skill whose
  *completion* transition is the item's first would be trapped. The F-014 downgrade mechanism
  already handles the sibling case (`question.blocking.not-suspended` was correctly downgraded);
  `journal.execution.missing` for the entry the pending move will write looks like the same
  class of finding. Recorded honestly as a correction entry on `EP-001`'s journal.
- `scripts/new-item --help` fails with `new-item: --help needs a value`; the usage text is only
  reachable by reading the file or by omitting a required flag.
- `scripts/board-gen` printed "board already current; not rewriting the timestamp" after the
  transition had regenerated it — correct behaviour, noted only because the consumer prompt's
  loop calls `board-gen` unconditionally and the message reads like a refusal.

```json
{
  "stop_reason": "human-question-open",
  "skills_run": ["intake"],
  "open_human_questions": ["EP-001/Q-001", "EP-001/Q-002", "EP-001/Q-003"],
  "items_touched": ["EP-001", "WI-0001", "WI-0002", "WI-0003"],
  "last_action": "intake created EP-001 with three draft items, filed Q-001..Q-003 to the human, and suspended EP-001 at awaiting-answer with resume-to: open",
  "notes": "Workspace validates: 0 errors, 1 warning (project.commands.test-null, owned by plan). One skill execution used of the three-execution budget; the turn stopped on the open human questions, not on the budget. Toolkit findings: workspace-valid cannot pass at gate time on an item's first transition because run-gate precedes the journal entry the same transition writes; new-item --help is broken."
}
```
