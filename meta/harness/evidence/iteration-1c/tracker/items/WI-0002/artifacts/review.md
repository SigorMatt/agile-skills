# Review — WI-0002

## What I examined

- **The record's mechanics.** `history.md` — twelve rows chaining without a gap, including two
  suspend-and-resume pairs (`intake`→`answer-questions` on Q-001, `plan`→`answer-questions` on
  Q-003), the last row matching `item.md`. `journal.md` — ten entries against ten actors in the
  history. All three questions `answered` with `## Consequences` naming files that exist. Nine
  criteria, nine ticks.
- **Verification freshness.** `check-verify-freshness WI-0002 wi/WI-0002` → *"verified at
  c59b1342; wi/WI-0002 has moved to c662cab5 but only the record changed (5 file(s) under tracker/
  or docs/), so the verification still covers the code"*.
- **The diff, hunk by hunk:** `git diff main..HEAD` — `expenses_tool/money.py` (48 lines),
  `expenses.py` (135), `store.py` (+38), `cli.py` (+103), `tests/test_money.py` (43),
  `test_expenses.py` (119), `test_cli_expenses.py` (263), `test_store.py` (+48), `README.md` (+37),
  and the tracker files.
- **The declared gaps:** `verify-report.md` `## Not verified, and why` (six entries) and
  `impl-report.md` `## What I did not do` (five) and `## Deviations from the plan` (four).
- **The trial merge:** `wi/WI-0002` into a throwaway branch off `main`, with both project commands
  run on the merge result.

Where each hunk earns its place:

| hunk | serves |
|------|--------|
| `money.py` — `parse_amount`, `format_amount`, `InvalidAmount` | plan step 1; AC1, AC5; ADR-0001 clause 1 |
| `expenses.py` — `resolve_person`, `resolve_sharers` | plan step 2; AC2, AC4, AC8; ADR-0009 clauses 2–3 |
| `expenses.py` — `parse_date`, `today` | plan step 3; AC6; WI-0002/Q-003 |
| `expenses.py` — `record_expense`, `list_expenses` | plan step 4; AC1, AC3, AC7; ADR-0009 clause 4 |
| `store.py` — `_bad_expense`, the `expenses` guard, `empty_data` | plan step 5; AC9 and the strict-read promise of ADR-0006 clause 4 |
| `cli.py` — `render_expense` | plan step 6; AC1, AC2, AC3; ADR-0008 clause 3 |
| `cli.py` — `cmd_add_expense` and its exception mapping | plan step 7; AC1, AC4–AC9 |
| `cli.py` — `cmd_list_expenses`, the two subparsers | plan step 8; AC1, AC3, AC7 |
| `tests/test_money.py`, `test_expenses.py` | plan steps 9–10 |
| `tests/test_cli_expenses.py` | plan step 11; one class per criterion |
| `tests/test_store.py` (+2 tests, 1 assertion) | plan step 5's compatibility promise; declared as a deviation |
| `README.md` | plan step 12 |

Nothing is unaccounted for. No hunk contradicts an ADR: money never becomes a float (ADR-0001),
every user-visible string is in `cli.py` (ADR-0008 clause 3), `expenses.py` and `store.py` raise
rather than print, names resolve through `store.normalise` (ADR-0003), and the record is exactly
the shape ADR-0009 clause 4 fixes.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every criterion ticked | **pass** | nine `- [x] AC` and no `- [ ] AC` in `item.md` |
| D2 | every tick cites evidence in `verify-report.md` | **pass** | its `## Criteria` table has nine rows, each with the command `verify` ran and its quoted output — including AC6's, which quotes both `date +%F` and `date -u +%F` on the day they differed |
| D3 | gates passed on the final state of the code | **pass** | `implement` on `aa611b6`, `verify` on `c59b134`, and this review on the trial merge result — `Ran 62 tests … OK`, `compileall` exit 0 |
| D4 | no open blocking question | **pass** | Q-001, Q-002, Q-003 all `answered`; Q-003's consequences are visible in AC6's current wording |
| D5 | a journal entry per execution; history chains | **pass** | ten entries against ten history rows; `validate-workspace` exit 0, which is where `history.gap` and `journal.execution.missing` would surface |
| D6 | design decisions in ADRs, cited | **pass** | ADR-0009 created by `plan` and cited from `plan.md` `## Decisions and ADRs`, from the overview's table, and from `store.py`'s and `expenses.py`'s docstrings |
| D7 | documents the change invalidated are updated | **pass** | `docs/architecture/overview.md` v1→v2 with the two new modules, the expense record and its snapshotted sharers; `README.md` gained "Recording expenses". `docs/product/vision.md` needed no change: it already said expenses carry a date (v7) and that shares are equal (v3) |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → *all 3 commit(s) on main..wi/WI-0002 name WI-0002* |
| D9 | merged into the trunk | **pass** | merged after this review and after the item was closed, in that order |
| D10 | verification postdates the code | **pass** | `check-verify-freshness` as quoted above |
| D11 | the review record says what was examined | **pass** | this document's `## What I examined`, with the per-hunk table |
| D12 | claims in `docs/` about this behaviour are still true | **pass** | re-read `overview.md` §"The pieces", §"The data" and §"The conventions every command follows" against the code. The module list matches; the envelope example matches the file the tool writes; "the sharers are snapshotted" is what `resolve_sharers(data, None)` does and what AC2 demonstrates. One claim was checked rather than remembered — the overview says a missing key reads as empty, and I loaded a WI-0001-era file through the tool to confirm it. `README.md`'s new section was checked line by line against the actual output, including the em dash in the rendered line |

## Findings

Three, none of them a send-back:

1. **`record_expense` strips the description before storing it.** No criterion asks for that and
   none forbids it: AC7 only requires a blank description to be refused. It is consistent with how
   names are handled (ADR-0003 clause 2 stores a name trimmed), and the alternative — storing
   `"  dinner  "` and rendering it with its padding — would look like a bug in the listing.
   Accepted as reasonable, and recorded here because it is behaviour nobody specified.
2. **`cmd_add_expense` catches six exception types in one block and maps each to a message.** It is
   long, and it is the right shape: every user-visible string for this command is in one place,
   which is what ADR-0008 clause 3 asks for, and the alternative — mapping inside `expenses.py` —
   would put messages in the module that must not print. Noted so that a later reader does not
   "tidy" it by moving the strings closer to the raises.
3. **The order of operations in `cmd_add_expense` is load-bearing and unenforced.** AC9 holds
   because every check precedes `store.save`. Nothing but the tests would catch a future change
   that moved a validation after the save — which the sensitivity check confirms, since replacing
   the save with `pass` failed eleven tests. Recorded as a maintenance note rather than a defect:
   the comment above the block already says why the order matters.

Nothing here would be uncomfortable to maintain. The three new modules keep the responsibilities
ADR-0008 assigned, the exception classes carry exactly the data their messages need (the name as
typed for an unknown person, the *stored* spelling for a duplicate), and the strict read gives a
distinct reason per failure rather than one catch-all.

## Accepted gaps

Recorded in the item's `## Notes` under "Accepted gaps at close", so they outlive this report:

- **An unwritable `--data-file` path still produces a traceback**, inherited from WI-0001 where it
  is already an accepted gap; `add-expense` writes through the same `store.save`.
- **A description containing ` — ` or a comma** makes the rendered line ambiguous to a parser. The
  item's R10 note records it as unconstrained; nothing in this epic parses that output.
- **Two names differing only by an accent are two people**, so `--shared-by José,Jose` is not a
  duplicate and records a two-way split. Follows from ADR-0003, which declined accent-folding.
- **`argparse`'s usage wording is unchecked**; only its exit code 2 is asserted.
- **The listing at scale is unexamined** — every check used one or two expenses.
- **Concurrent `add-expense` processes could lose a record**, since each loads, appends and
  replaces the whole file. Nothing in the epic mentions concurrency (one person, one terminal), and
  no criterion covers it. This one is new in this item and is the most likely to matter later, so
  it is written into the item rather than left in a verification report.

## Verdict

**Accepted.** The change does what WI-0002's criteria say, in a shape the project should keep, and
the record reconstructs the whole story — including the part where `plan` stopped the pipeline
rather than implement a criterion that contradicted itself, and `answer-questions` amended it from
the stakeholder's own words. Three findings, all accepted; six gaps, all now recorded on the item.
