# Harness status — turn 2

This turn was a no-op for the pipeline, and that is the finding.

- **Amendment B first.** I swept every `tracker/items/*/questions/Q-*.md`. Thirteen of the
  sixteen questions are already `status: answered`. The three that are `open` — `WI-0002/Q-004`,
  `Q-005`, `Q-006`, all `addressed-to: human`, all `blocking: true`, filed by `refine` at
  `2026-08-21T03:46:54Z` — still carry the literal placeholder
  `<!-- filled in by answer-questions -->` under `## Answer`. **The stakeholder has not answered
  them.** There was therefore nothing for `answer-questions` to consume, and I did not run it.
- **Then the loop.** `validate-workspace` passed clean (4 items, 8 documents, 0 errors,
  0 warnings). `board-gen` reported the board already current. `/next` executed
  `orchestrator.steps` and halted at step 2 — open human-addressed questions stop the loop before
  the candidate set is ever built.
- **Nothing else was runnable anyway.** WI-0001 is `done`. WI-0002 is `awaiting-answer` on the
  three questions. WI-0003 is `ready`, but its frontmatter records `depends-on: WI-0002`, which is
  not `done`, so it fails the `runnable` test at step 4 regardless. EP-001 is `open` and advances
  only through its children.
- **Nothing new was filed.** Amendment A's batching only licenses questions I can already state.
  The one item that could produce more is WI-0003, whose next skill is `plan` — and I have not
  reached `plan`, so any question I invented there would be exactly the padding the amendment
  forbids. I left it.
- **Nothing was written.** No artifact, no history row, no commit; the working tree is clean at
  `f8502bd`. `next` writes no item journal by contract, and the board did not change.

## What the owner should know

The turn cost a full round trip and moved nothing, because turn 1's three questions were not
answered before turn 2 started. Turn 1's last commit is timestamped `06:55:35 +0300` and the
question files `06:47:45`; no file in the workspace has been touched since. The pipeline is
behaving exactly as specified — the loss is scheduling, not correctness. Turn 3 will be identical
unless the three `## Answer` sections are filled in.

One toolkit observation, inherited rather than new: `EP-001/questions/Q-001.md` documents a real
contradiction in the spec — `pipeline.yaml` makes the epic status `open` `terminal: true`, so no
legal transition can suspend an epic into `awaiting-answer`, yet `validate-workspace` reports
`question.blocking.not-suspended` if an epic carries an open blocking question. `intake`'s
escalation instruction for an epic is therefore uncarryable. Turn 1 worked around it with
`blocking: false` and a written explanation. Worth fixing upstream.

```json
{
  "stop_reason": "human-question-open",
  "open_human_questions": ["WI-0002/Q-004", "WI-0002/Q-005", "WI-0002/Q-006"],
  "items_touched": [],
  "last_action": "next halted at orchestrator step 2 — three human-addressed blocking questions on WI-0002 are open and unanswered; no answers had arrived to consume, nothing was dispatched, nothing was written",
  "notes": "Turn 2 was a genuine no-op: the stakeholder did not answer turn 1's questions (WI-0002 Q-004..Q-006 still hold the answer-questions placeholder), so amendment B had nothing to consume and the orchestrator stopped before building a candidate set. WI-0003 was not runnable either, on depends-on WI-0002. Workspace validates clean and the tree is clean at f8502bd. Turn 3 repeats identically unless those three answers land. Inherited toolkit defect, documented in EP-001/Q-001: epic status 'open' is terminal in pipeline.yaml so an epic cannot legally be suspended into awaiting-answer, yet validate-workspace demands suspension for an open blocking question on an epic — intake's escalation path for epics cannot be executed as written."
}
```
