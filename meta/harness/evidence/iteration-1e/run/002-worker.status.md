# Harness status — turn 2

The workspace had been provisioned but held no items, so this turn started the pipeline from the
stakeholder's opening statement in `IDEA.md`.

- Ran `intake`. Created **EP-001** ("Track and settle shared expenses in a friend group from the
  command line") with four checkable success measures and an explicit out-of-scope list, plus
  three work items at `draft`:
  - **WI-0001** — record people and expenses from the command line, stored on disk (high)
  - **WI-0002** — show who owes whom (high, `depends-on: WI-0001`)
  - **WI-0003** — import expenses from a bank CSV export (medium, `depends-on: WI-0001`)
- Wrote `docs/product/vision.md` v1 and filled in `project.description`. Left `commands.*` null
  for `plan`, as the contract requires.
- Filed **three blocking questions to the human** on EP-001, as one batch, and suspended the epic
  to `awaiting-answer` with `resume-to: open`:
  - `Q-001` — what the bank's CSV export actually looks like (a sample file, or the header row and
    which columns hold amount/date/description). WI-0003 has no decidable criterion without it.
  - `Q-002` — does "who owes whom" mean each person's net position, or a list of payments that
    settles the group? Two readings, different output, different criteria.
  - `Q-003` — after WI-0001, which comes next: WI-0002 or WI-0003? No ordering was stated, and the
    current high/high/medium priorities are an explicit placeholder, not a decision.
- Committed everything as `0e09290` (`tracker: create EP-001 and its first three work items`),
  including `IDEA.md`, which the journal cites as its input.
- Ran `next`. It validated the workspace (0 errors, 1 warning — `commands.test` still null, which
  is `plan`'s to fix), found no open requests, and stopped at step 3 on the three human-addressed
  questions. Nothing was dispatched.

Nothing failed and nothing is blocked. Two things intake deliberately did **not** decide are
recorded as notes on WI-0001 rather than as assumptions: how an expense divides between its
sharers (equal split is the plain reading of "shared by some or all", but was not said), and how
amounts are represented and rounded. Both are refinement's to settle.

```json
{
  "stop_reason": "human-question-open",
  "skills_run": ["intake", "next"],
  "open_human_questions": ["EP-001/Q-001", "EP-001/Q-002", "EP-001/Q-003"],
  "items_touched": ["EP-001", "WI-0001", "WI-0002", "WI-0003"],
  "last_action": "next validated the workspace and stopped on three open human-addressed questions on EP-001; nothing dispatched",
  "notes": "next is the dispatcher and does not count against the 3-skill turn budget, so this turn spent 1 of 3. One piece of toolkit friction: `scripts/transition --journal-body-file` REJECTS a body that has no `**Status:**` bullet ('the journal body is not a legal entry'), but spec/journal-and-history.md 2.2 and the transition script's own help both say the transition tool writes that bullet itself from the move it made. The caller therefore has to write a Status bullet that the tool then overwrites, which is exactly the duplication F-019 was meant to remove. Harmless once known, but it costs a failed transition to discover, and the error message does not say the bullet's content is ignored."
}
```
