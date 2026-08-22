# Implementation report — WI-0002

## What was built

Two subcommands, `add-expense` and `list-expenses`, on top of two new modules and one extension to
an existing one. The plan's thirteen steps were worked in order.

- **`expenses_tool/money.py`** (new) — `parse_amount` accepts a positive decimal with at most two
  places and returns whole pence by integer arithmetic; `format_amount` renders pence back to two
  places. No `float` and no `Decimal` appears in the file (ADR-0001 clause 1). `1.005` raises
  rather than rounding.
- **`expenses_tool/expenses.py`** (new) — `resolve_person` and `resolve_sharers` (including the
  snapshot when `--shared-by` is omitted), `parse_date` and `today`, `record_expense` and
  `list_expenses`. It raises and never prints, per ADR-0008 clause 3.
- **`expenses_tool/store.py`** — `load` now validates `expenses` as strictly as it validates
  `people`, with a specific reason per failure; `empty_data` carries the new key. A data file
  written by WI-0001, with no `expenses` key at all, still loads (ADR-0006 clause 2).
- **`expenses_tool/cli.py`** — `render_expense` (the single rendering, used by both the
  confirmation and the listing), the two new handlers, and their subparsers. Every user-visible
  string is here.
- **`tests/test_money.py`** (new, 5 tests), **`tests/test_expenses.py`** (new, 11),
  **`tests/test_cli_expenses.py`** (new, 14 across nine criterion classes), and two new cases in
  **`tests/test_store.py`**.
- **`README.md`** — a "Recording expenses" section with a worked example, the amount grammar, what
  `--shared-by` defaults to and that it is snapshotted, and the date default.

## Acceptance criteria evidence

Every test named below is in `tests/test_cli_expenses.py` unless stated, and runs `./expenses` in a
subprocess against a data file in a fresh `TemporaryDirectory`.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — the confirmation, and no per-person amount | `cmd_add_expense` prints `Added ` + `render_expense`; `add-expense` has no `--share-amount`, so `argparse` rejects it | `AC1::test_records_and_confirms` — stdout exactly `Added 2026-08-14 30.00 dinner — paid by Ana, shared by Ana, Ben, Cass\n`, stderr empty, exit 0; `AC1::test_share_amount_is_a_usage_error` — exit 2, and the listing still `No expenses recorded yet` |
| AC2 — omitted sharers snapshot everyone | `resolve_sharers(data, None)` returns the registered people sorted by `store.normalise`, and the list is stored | `AC2::test_defaults_to_everyone_and_snapshots` — confirmation names all three; then `add-person Dan`; then `list-expenses` still shows `Ana, Ben, Cass` |
| AC3 — persistence, order, empty listing | `store.save`/`load`; `list_expenses` sorts by date with a stable sort | `AC3::test_lists_in_date_order_across_invocations` — two records in separate invocations, the `2026-08-02` line printed first; `AC3::test_empty_listing` — stdout `No expenses recorded yet\n`, exit 0 |
| AC4 — unknown people; a case-different sharer is known | `resolve_person` raises `UnknownPerson` carrying the name as typed; matching is `store.normalise` | `AC4::test_unknown_person_refused` — stderr `Unknown person: Dan\n` for payer and for sharer, exit 1, file bytes identical; `AC4::test_case_different_sharer_resolves` — `--paid-by ana --shared-by ana,BEN` exits 0 and renders `paid by Ana, shared by Ana, Ben` |
| AC5 — the amount grammar | `money.parse_amount`, checked before anything else | `AC5::test_bad_amounts_refused` — four sub-tests comparing stderr exactly, then the listing still empty; `AC5::test_accepted_amounts_render` — `30` and `30.5` render as `30.00` and `30.50` |
| AC6 — `--date`, the local default, malformed dates | `expenses.parse_date` checks the layout and the value; `expenses.today()` is `datetime.date.today()` | `AC6::test_default_date_is_todays_local_date` — the line begins with `datetime.date.today().isoformat()`, the same clock `date +%F` reads; `AC6::test_bad_dates_refused` — three sub-tests comparing stderr exactly |
| AC7 — description required and non-blank | `--description` is `required=True`; `record_expense` raises `BlankDescription` | `AC7::test_missing_description_is_a_usage_error` — exit 2; `AC7::test_blank_description_refused` — stderr `An expense needs a description\n`, exit 1 |
| AC8 — duplicate or empty `--shared-by` | `resolve_sharers` raises `DuplicateSharer` (carrying the stored spelling) or `NoSharers` | `AC8::test_duplicate_sharer_refused` — stderr `Ana is named twice in --shared-by\n`, bytes unchanged; `AC8::test_empty_shared_by_refused` — stderr `--shared-by must name at least one person\n`, bytes unchanged |
| AC9 — refusals leave the history intact | every check precedes `store.save` in `cmd_add_expense` | `AC9::test_refusals_do_not_change_the_listing` — one refusal from each of AC4–AC8, asserting after each that `list-expenses` output and the file's bytes are identical to before |

## Deviations from the plan

1. **An existing WI-0001 unit test was updated.** `tests/test_store.py::test_a_missing_file_is_an_empty_store`
   asserted `{"schema": 1, "people": []}`, and `empty_data()` now also carries `"expenses": []`.
   This is an intentional extension rather than a defect in delivered behaviour: no WI-0001
   acceptance criterion mentions the dict's shape, and all of WI-0001's end-to-end tests still pass
   untouched. Two tests were added alongside it — a WI-0001-era file with no `expenses` key still
   loads, and five malformed expense shapes are refused.
2. **`resolve_sharers` filters out empty parts before deciding the list is empty**, so
   `--shared-by ","` and `--shared-by " , "` take AC8's "must name at least one person" message
   rather than reporting an unknown person named "". The plan said "raise `NoSharers` if the result
   is empty or every part is blank"; this is that, with the order of operations made explicit.
3. **`parse_date` checks the layout with three character comparisons** rather than a regex, since
   `date.fromisoformat` then does the calendar validation. Same effect as the plan's step 3, less
   machinery.
4. **A test-helper bug was found and fixed during this execution**, not in the tool: the helper
   that builds `add-expense` arguments dropped a `None` *value* while keeping its option name,
   which made AC2's and AC6's "omit the option" cases into usage errors. Both tests failed loudly
   before the fix, which is the behaviour a sensitivity check would have wanted anyway.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 62 tests`, `OK`, on branch head `aa611b6` after the last change |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses expenses_tool tests` → exit 0. ADR-0007 clause 4: a syntax check, not a style linter |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | AC1–AC9 each have a named test class in `tests/test_cli_expenses.py`, listed in the table above |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → `all 1 commit(s) on main..wi/WI-0002 name WI-0002` |

## What I did not do

- **No question was filed.** The one decision that would have needed it — which clock dates an
  undated expense — was already settled by `Q-003` before this execution started.
- **Nothing was built for WI-0003 or WI-0004.** No balance, no total, no import history key.
  `record_expense` is the single path a future import will reuse, but nothing anticipates a CSV.
- **The two behaviours the item leaves unconstrained were left alone**: `argparse`'s usage wording
  (only its exit code 2 is asserted), and a description containing ` — ` or a comma, which is
  stored and printed verbatim and makes the rendered line ambiguous to a parser. Nothing in this
  epic parses that output.
- **`--data-file` pointing somewhere unwritable still produces a traceback**, unchanged from
  WI-0001 and recorded there as an accepted gap. `add-expense` writes through the same `store.save`,
  so it inherits the same gap; no criterion covers it.
- **`docs/` was not touched.** `plan` bumped the overview to v2 and wrote ADR-0009 before any code
  existed, and nothing in the implementation contradicted either.
