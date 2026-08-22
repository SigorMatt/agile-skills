# Implementation report — WI-0002

## What was built

Two subcommands, `add-expense` and `expenses`, the rules behind them, and the module that turns
typed amounts into whole minor units. Two new source files, three modified, five new test modules
and two extended.

| file | new or changed | what it is |
|------|----------------|------------|
| `expenses/money.py` | new | `parse_amount`, `format_amount`, and the two constants behind them |
| `expenses/errors.py` | new | `RuleError`, moved here — see deviation 1 |
| `expenses/group.py` | changed | `add_expense`, `shares_of`, `expenses`; re-exports `RuleError` |
| `expenses/storage.py` | changed | the `expenses` key in `empty_record`, and `_is_expense` shape-checking it in `load` |
| `expenses/cli.py` | changed | `_options`, `_split_sharers`, `_add_expense`, `_expenses`, two more entries in `COMMANDS`, and `OSError` in the refusal handler |
| `tests/support.py` | changed | `ExpenseTestCase` — a `CliTestCase` with the four people the criteria assume, and a `listing()` helper |
| `tests/test_money.py` | new | `money` directly |
| `tests/test_add_expense.py` | new | AC1, AC5, AC6, AC7, AC14 |
| `tests/test_expenses_listing.py` | new | AC3, AC4 |
| `tests/test_expense_refusals.py` | new | AC8–AC13, plus ADR-0010 and record compatibility |
| `tests/test_persistence.py` | changed | AC2, as real subprocesses |

The layering the plan set out holds: `cli.py` owns the command-line syntax and everything printed,
`group.py` owns what a name and an amount *mean*, `money.py` owns text-to-integer, `storage.py`
owns the file. `group.py` never sees a comma and `cli.py` never resolves a person.

## Acceptance criteria evidence

Test names are given without their class where unambiguous. `run_cli` is the in-process helper
from `tests/support.py`; `invoke` in `test_persistence.py` runs a real `python3 -m expenses`
process.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `_add_expense` checks arity, calls `group.add_expense`, saves, prints the confirmation | `test_add_expense.py::RecordingTest::test_an_expense_is_recorded_and_confirmed` — asserts `(0, "Recorded 30.00 paid by Alice, shared by 3 people.\n", "")` |
| AC2 | `storage.save` / `storage.load` on the `expenses` key | `test_persistence.py::test_an_expense_recorded_by_one_process_is_there_for_another` — `add-person` ×3, `add-expense`, then `expenses`, each a **separate process**; the last prints the recorded line. `test_a_record_written_by_one_process_keeps_both_kinds_of_fact` shows people and expenses surviving together |
| AC3 | `_expenses` numbers from 1 and formats through `money.format_amount` | `test_expenses_listing.py::test_the_line_format_is_exact` (the exact string), `::test_expenses_are_numbered_from_one_in_the_order_recorded`, `::test_people_are_shown_with_the_spelling_first_entered` (typed `sam okafor`/`ALICE`, listed `Sam Okafor`/`Alice`), `::test_every_amount_carries_two_decimal_places` |
| AC4 | `_expenses` prints the empty-list line when there is nothing | `test_expenses_listing.py::EmptyListingTest::test_nothing_recorded_says_so_and_succeeds` — run on a record with no people either, so a missing file is covered too |
| AC5 | `shares_of` divides the whole total when nothing is stated | `test_add_expense.py::EqualSplitTest` — two tests, including a single sharer taking `12.00` with a payer who is not a sharer |
| AC6 | `shares_of` takes stated shares as given and divides the remainder | `test_add_expense.py::MixedSplitTest` — the `Alice 12.00, Bob 6.00, Carol 12.00` case and the stated-zero case printing `Bob 0.00` |
| AC7 | `shares_of` orders the unstated sharers payer-first, then by named order | `test_add_expense.py::RemainderTest` — all three lines from the criterion asserted verbatim, plus `test_the_shares_always_sum_to_the_total` over four different expenses |
| AC8 | `group.add_expense` resolves both roles through `find_person` | `test_expense_refusals.py::UnknownPersonTest` — three tests: an unknown payer, an unknown sharer, and `--paid-by sam okafor` succeeding and listing as `Sam Okafor`. The refusals also assert `expenses` is still empty and `people` gained nobody |
| AC9 | `money.parse_amount` for form and precision, `group.add_expense` for sign and magnitude | `test_expense_refusals.py::AmountTest` — five tests, one per bullet, each asserting the exact stderr; `test_money.py` covers the parser directly, including `12.`, `1e3` and `12,50` |
| AC10 | the two sum checks in `group.add_expense` | `test_expense_refusals.py::StatedSharesTest` — over-total and under-total-with-all-stated refused with their exact messages; exactly-equal accepted and listed |
| AC11 | `cli._split_sharers` for syntax, `group.add_expense` for the duplicate | `test_expense_refusals.py::SharerListTest` — five tests; the duplicate test covers `Alice,alice`, `Alice,ALICE` and `Alice,  alice  `, all giving `Alice is named twice in --shared-by.` |
| AC12 | `cli._options` and the arity checks in `_add_expense` | `test_expense_refusals.py::CommandLineTest` — six tests, one per bullet |
| AC13 | nothing is saved before every rule has passed | `test_expense_refusals.py::RefusalsRecordNothingTest` — **twenty** refusals run against one record; after each, `expenses` output is byte-identical to before and stderr contains no `Traceback (most recent call last)`. A second test asserts none of them added a person either |
| AC14 | `storage.load` preserves `people` untouched | `test_add_expense.py::RecordingTest::test_people_are_undisturbed_by_recording_an_expense` — `people` still prints the four names in the order added |

### The tests were measured, not just run

Seventeen deliberate mutations, one per criterion or per rule, each applied to the real source,
run against the whole suite, and reverted. **All seventeen were caught.** The ones worth naming:

| mutation | caught by |
|----------|-----------|
| `shares_of` drops the payer-first ordering | **1 test** — `test_only_the_unstated_sharers_divide_the_remainder_and_the_payer_leads_them`, the AC7 case `plan.md` § *Risks* said would be the only thing catching it |
| `shares_of` ignores stated shares entirely | 4 tests |
| `shares_of` never adds the odd penny | 4 tests, including `test_the_shares_always_sum_to_the_total` |
| `add_expense` skips the payer membership check | 2 tests |
| the total sign check is removed | 2 tests |
| `parse_amount` accepts any precision | 4 tests |
| either sum check is removed | 2 tests each |
| the duplicate-sharer check is removed | 2 tests |
| `_options` ignores a repeated or unknown option | 1 and 2 tests |
| `_add_expense` never saves | 15 tests |
| `storage.load` drops `people` | 36 tests |

The narrowest is the payer-first ordering, caught by exactly one test. That is the risk the plan
named first, and it is worth knowing that the margin there is one test rather than four.

## Deviations from the plan

1. **`RuleError` moved to a new `expenses/errors.py`, and `group.py` re-exports it.** The plan
   has `money.parse_amount` raise `group.RuleError` while `group.add_expense` calls
   `money.parse_amount` — a circular import: importing `group` would import `money`, which would
   import a `group` that had not yet defined `RuleError`. Moving the class to a third module both
   import is the smallest fix that keeps every name the plan uses working: `group.RuleError` still
   resolves, and `cli.py`'s `except (group.RuleError, storage.RecordError)` is untouched. This is
   *how*, not *what* — no behaviour differs.
2. **`ExpenseTestCase` added to `tests/support.py`.** The plan said to reuse `support.py`
   unchanged. Every criterion here assumes four people already added, so the alternative was
   repeating that setup in four test modules. `CliTestCase` is unchanged and WI-0001's tests still
   use it exactly as they did.
3. **`_options` refuses an option with no value** — `--paid-by` as the last token, or followed by
   another `--option` — with `<name> needs a value.` No criterion covers this: AC12 lists six
   command-line failures and this is not one of them. It exists because the alternative is an
   `IndexError` traceback. Flagged here rather than buried; see `## What I did not do`.
4. **`_add_expense` refuses more than one positional** with `add-expense takes a single total.`
   Also not covered by any criterion, for the same reason and with the same flag.
5. **`storage._is_expense` also rejects an empty `shares` list and booleans-as-integers.** The
   plan named the field types; `ADR-0002` requires at least one sharer, and Python's `bool` is an
   `int`, so `{"total": true}` would otherwise pass a naive `isinstance` check.

No acceptance criterion was edited. Nothing in the plan was skipped.

## Gates

Run on the branch head, after the last code change.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 79 tests`, `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses tests` → exit 0. As `ADR-0008` records, this is a syntax check and not a linter |
| `workspace-valid` | **pass** | `validate-workspace` → exit 0, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | the table above names a test function for each of AC1–AC14; the seventeen mutations are the evidence that those tests fail when the behaviour is removed |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → exit 0 |
| `no-unplanned-scope` (advisory) | **pass, with five declared deviations** | every hunk traces to a plan step and a criterion, except the five above and the `OSError` branch, each named with the ADR or the reason that required it |

## What I did not do

- **Three pieces of behaviour have no acceptance criterion behind them**, and `verify` should
  record all three as unverified rather than as passing:
  1. `ADR-0010`'s `OSError` handling. The plan declared this in advance — the decision was handed
     to this item by WI-0001's review, and `plan` may not write criteria. A test exists
     (`WriteFailureTest`) and it passes, but it satisfies no criterion, and its docstring says so.
  2. `--paid-by` with no value (deviation 3).
  3. `add-expense` with two positionals (deviation 4).
- **Nothing was built for WI-0003 or WI-0004.** No balance, no netting, no `payments` key. The
  function WI-0003 will build on, `group.shares_of`, exists because AC3 needs it today.
- **No expense identifier.** The numbers `expenses` prints are computed at print time from list
  position; nothing accepts one as an argument, because nothing edits or deletes an expense.
- **`money.parse_amount` accepts a leading `+`** (`+12` is `1200`). Not required by any criterion
  and not forbidden; it falls out of handling the leading `-` that AC9 needs, and refusing it
  would have been the extra code, not the saving.
- **The `expenses` key is written into the record the first time anything is saved**, including by
  `add-person`, because `empty_record()` now contains it. A record written by WI-0001 and never
  re-saved keeps its old shape and still loads — tested by
  `RecordCompatibilityTest::test_a_record_with_no_expenses_key_reads_as_having_none`.
- **Nothing checks that a stored expense names people who are still in the group.** Nothing
  removes a person, so it cannot go stale today; `plan.md` § *Risks* records what would change if
  removal were ever added.
