# Harness status — turn 14

The stakeholder had answered `WI-0003/Q-003`, so that was consumed first, and the turn then ran
two more skills before the three-execution budget ran out. Nothing is blocked on a question: the
board has **no open questions at all** for the first time in this run.

- **`answer-questions` on WI-0003.** The stakeholder answered `Q-003` — "No — just wait for my
  file. I don't want a name-the-columns version." That is option **A**, and it refuses **B** as
  well ("just wait" only makes sense if the export is handed over as it is). Recorded as
  **`ADR-0010`**: the importer is written against their real export and gains no column-mapping
  options; the command's arguments stay the file path, the payer, the sharers and the optional date
  range `ADR-0007` already settled. AC1 lost the clause hedging that the mapping might become a
  run-time argument; AC3, AC4 and AC5 each now say they wait on the sample and on nothing else. The
  ADR also settles three things the answer did not: where the sample should land
  (`tracker/items/WI-0003/artifacts/bank-sample.csv`), that no fourth question may be filed for it,
  and that the item is an impasse until it arrives. Item returned to `draft`, its recorded
  `resume-to`.
- **`refine` on WI-0003 → `blocked`.** The sample is nowhere in the workspace (`find -iname '*.csv'`
  returns nothing). With every question on the item answered, the Definition of Ready was applied
  for the first time: **eight criteria pass, R4 and R10 fail**, both on that one input. R6 passes
  for the first time. No fourth question was filed — the stakeholder has been asked three times and
  answered the third with an instruction, so there is nothing left to ask and `blocked` ("a
  documented impasse; a human must act") is the honest status. What could be salvaged without the
  sample was: R10's shape-independent combinations — a payer or sharer who is not a recorded
  person, a date range matching no row, whether the bounds are inclusive, whether a run whose rows
  all fail exits non-zero — are now written into `## Notes` as open, attributed to `refine`.
  **To unblock: drop a CSV (3–5 lines with the header, merchant names and amounts changed to
  anything) at `tracker/items/WI-0003/artifacts/bank-sample.csv`.** Any skill may then return the
  item to `draft`.
- **`plan` on BUG-0001 → `planned`.** The success line printed before the save, so a failed write
  reported success on stdout and an error on stderr. **`ADR-0011`** changes the handler contract to
  `str | None` — a handler returns its success line and `main` prints it only after `store.save`
  returns — so the ordering is stated once in `main` rather than remembered per command, and
  WI-0003's importer inherits it. `plan.md` has seven steps, both ACs mapped, an empty
  `## Assumptions` (the one thing that could have been assumed was checked instead), four risks,
  and a regression test that follows the bug's own reproduction in real processes and must be
  observed failing before the fix.

**What refused to pass, and what got in the way:**

1. `claims-are-sourced` failed the first `plan` transition — `lint-claims --changed-since main` is
   stricter than the whole-tree run I had used, and caught two unsourced absolutes in `ADR-0011`.
   Fixed and re-run green. Worth knowing: lint the changed set, not the tree.
2. **A toolkit defect.** `scripts/transition` interpolates `--reason` into `history.md`'s markdown
   table without escaping `|`. My reason contained `str|None`, so the row came out with 7 columns
   and the workspace stopped validating immediately after a transition the tool reported as
   successful. The three resulting errors (`history.columns`, `history.tail-mismatch`,
   `journal.status.unmatched`) name the symptom and not the cause. I repaired the cell
   (`str|None` → `str-or-None`, nothing else touched) and appended a correction entry to
   BUG-0001's journal saying exactly what was edited and why an append-only file was touched.
   Escaping the pipe, or refusing a reason containing one, would cost a line.
3. A self-inflicted one worth recording: splitting a question file on the string `## Answer`
   truncated `Q-003`, because option A's own text quotes that heading. Caught by `git diff --stat`
   and rewritten in full. Question files quote their own headings — edit them whole.

Next turn: `next` will dispatch `implement` on BUG-0001 (`planned`, the only runnable item).

```json
{
  "stop_reason": "turn-budget-exhausted",
  "skills_run": ["answer-questions", "refine", "plan"],
  "open_human_questions": [],
  "items_touched": ["WI-0003", "BUG-0001"],
  "last_action": "plan wrote BUG-0001's plan and ADR-0011, and moved the item to planned",
  "notes": "No open questions anywhere on the board for the first time this run. WI-0003 is blocked on a file only the stakeholder can supply — three questions have been asked and answered, and ADR-0010 forbids a fourth; drop a CSV at tracker/items/WI-0003/artifacts/bank-sample.csv and any skill may return it to draft. Toolkit defect: scripts/transition does not escape '|' in --reason, so a reason containing a union type corrupts the history row and breaks validation after a transition the tool reports as successful; the resulting validator errors do not name the cause. Repaired and journalled on BUG-0001. Also: lint-claims --changed-since main is stricter than the whole-tree run, so plan should use the former before transitioning."
}
```
