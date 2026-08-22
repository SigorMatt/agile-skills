# Harness status — turn 6

The stakeholder's five answers had landed on WI-0001's questions, so this turn consumed them and
carried the item two more stages. Three skills ran; the budget stopped the turn, not the pipeline.

- **`answer-questions` on WI-0001.** All five `Q-00n` answers propagated and closed. Four were the
  stakeholder's own words; the fifth (`Q-002`) was half theirs and half a delegation — "who eats
  the odd cent — not sure yet, go ahead anyway" — which was decided as the architect rather than
  re-escalated, and recorded as **ADR-0002** (the payer absorbs the remainder). Propagated into
  `WI-0001/item.md` (8 criteria → 12), `WI-0002` and `WI-0003` notes, `docs/product/vision.md`
  (v2 → v3), and `refinement-qa.md`. The item resumed at its recorded `resume-to: draft`. An epic
  journal entry records the two product boundaries that reached `EP-001`'s record.
- **`refine` on WI-0001 → `ready`.** Definition of Ready passes on all ten criteria with **no
  override**. The twelve criteria were rewritten so each names an observation; "refused" is
  defined once as stderr message + non-zero exit + no change to recorded data. Nine decisions were
  taken **without asking** the stakeholder — date format, listing order, empty-listing output,
  blank-name and duplicate-sharer refusals, and the repayment date — each tagged `[assumed]` in
  the Q&A and tabled in `## Notes` with why it was not worth a round trip. R10 is answered with a
  thirteen-row combination table.
- **`plan` on WI-0001 → `planned`.** Greenfield: no code existed. Created
  `docs/architecture/overview.md` v1, `artifacts/plan.md` (8 steps, all 12 ACs mapped to specific
  demonstrations), and three ADRs — **ADR-0003** (one JSON ledger at an XDG default, chosen per
  run, written atomically), **ADR-0004** (integer minor units; no float, no `Decimal`),
  **ADR-0005** (standard library only). `tracker/project.yaml` now has real, *actually run*
  commands: `test` = `python3 -m unittest discover -s tests -t . -q`, `lint` =
  `python3 -m compileall -q expenses tests`.

Nothing is blocked; no question is open; the workspace validates with 0 errors and 0 warnings.
The next turn's `next` will dispatch `implement` on WI-0001.

## Things worth knowing

- **`lint-claims` ignores file arguments.** Running
  `lint-claims <path> <path> …` prints "checked the whole tree" and exits 0 regardless of what
  was passed. Only the `--changed-since` form the `claims-are-sourced` gate uses actually checks
  new work. This turn's `plan` self-checked with file paths, believed it had passed, and was then
  refused by the transition with 12 real errors. A worker that treats its own manual run as
  evidence will record a pass for a check it never ran. Recorded in WI-0001's `plan` journal
  entry as well.
- **The `claims-are-sourced` failure was worth having.** All 12 findings were genuine absolute
  claims ("never", "every", "no", "exactly") about a backticked identifier with nothing behind
  them. They were fixed by adding citations, not by softening the sentences.
- **`unittest discover` exits 5 on an empty suite**, so the `tests-pass` gate cannot go green over
  zero tests. That shaped the plan: tests are attached to each step rather than to a final one.
- **`commands.lint` is weaker than its name.** No linter is installed and the project takes no
  third-party dependencies, so lint is a `compileall` syntax check. Recorded in ADR-0005, in a
  comment beside the key in `project.yaml`, and in the plan's `## Risks`, so a green
  `no-lint-errors` gate is not read as more than "every file parses".
- **`plan` wrote two files outside `tracker/` and `docs/`** — empty `expenses/__init__.py` and
  `tests/__init__.py` — solely so the test and lint commands could be run before being recorded,
  as the skill's own self-check demands. Flagged in the plan's `## Risks`.
- **One assumption a stakeholder could reasonably reject** is flagged in two places: that a
  repayment carries a date. `Q-003`'s answer speaks only about expenses; the extension was the
  architect's, and it is free to reverse until `implement` writes a store.

```json
{
  "stop_reason": "turn-budget-exhausted",
  "skills_run": ["answer-questions", "refine", "plan"],
  "open_human_questions": [],
  "items_touched": ["WI-0001", "WI-0002", "WI-0003", "EP-001"],
  "last_action": "plan moved WI-0001 ready → planned after ADR-0003/0004/0005 and plan.md; the claims-are-sourced gate refused the first attempt and passed after 12 citations were added",
  "notes": "lint-claims silently ignores explicit file paths and reports 'checked the whole tree' with exit 0 — only --changed-since checks new work, so a skill self-checking with file arguments can believe it passed a gate it never ran. Everything else behaved. Workspace validates 0 errors, 0 warnings; no open questions; next turn dispatches implement on WI-0001."
}
```
