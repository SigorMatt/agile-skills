# Implementation report — WI-0002

## What was built

One new module and one new subcommand, on branch `wi/WI-0002`.

`expenses/debts.py` holds `ADR-0006`'s five computation steps as a single pure function,
`debts(ledger) -> list[Debt]`, plus the frozen `Debt` dataclass it returns. It imports `Ledger`
and `normalise_name` from `expenses.model` and nothing else from the package; it opens no file,
prints nothing and raises nothing.

The accumulator is one signed integer per unordered pair of people, keyed by the pair's two
normalised names in sorted order and read as "how many minor units the second owes the first".
Netting a pair is therefore addition rather than a reconciliation pass: a pair that squares up
reaches zero and is skipped, and a repayment that overshoots crosses zero and the line comes out
the other way round. Nothing is ever moved between pairs, which is what makes AC8's circle
printable.

`expenses/cli.py` gains a `debts` subparser with no options of its own, the constant
`NOBODY_OWES`, and `cmd_debts`, which prints and returns `False` so `main` saves nothing.

`docs/architecture/overview.md` went to v5: v4 described the module in advance, and step 5 of the
plan was to re-check that description against the built code. It needed no correction, only the
"not yet built" wording removed, a sentence about the accumulator, and citations to the module
itself.

## Acceptance criteria evidence

`tests/test_cli_debts.py` runs the real CLI through `tests/cli_harness.py`;
`tests/test_debts.py` calls the function directly. All 115 tests pass
[src: run: `python3 -m unittest discover -s tests -t . -q` → exit 0, 115 tests, OK].

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — one line per non-zero pair, `<debtor> owes <creditor> <amount>`, exit 0, first-typed names, positive amount | `cmd_debts` formats each `Debt` with `model.format_amount`; `debts()` returns only positive balances | `TestReportShape.test_every_line_has_the_debtor_owes_creditor_amount_form_and_exits_zero` splits every line and checks the shape, the exit code and the empty stderr; `test_names_print_in_the_form_first_typed` records an expense as ` ANA ` and `ana` and gets `Ben owes Ana 5.00`; `test_the_report_records_nothing` compares the ledger bytes before and after; `TestBalance.test_no_debt_is_zero_or_negative` over all eleven ledgers |
| AC2 — worked example, exact output | the two-expense ledger through the real commands | `TestWorkedExamples.test_ac2_three_lines_in_this_order` asserts `["Ben owes Ana 10.00", "Cara owes Ana 10.00", "Cara owes Ben 6.00"]`; `TestWorkedLedgers.test_ac2_two_expenses_three_people` asserts the same at function level |
| AC3 — the printed lines account for every recorded minor unit; net positions sum to zero | integer minor units throughout; `//` and no float anywhere in `debts.py` | `TestBalance.test_every_ledger_balances_person_by_person` runs over all eleven registered ledgers: for each person, debtor-total minus creditor-total equals a net position recomputed by `net_positions()` from the ledger alone, asserted with `assertEqual` on `int`s; `TestBalance.test_the_net_positions_of_every_ledger_sum_to_zero` |
| AC4 — `Nobody owes anybody.` and exit 0 when no pair has a non-zero balance | `cmd_debts` prints `NOBODY_OWES` on an empty list | `TestNobodyOwesAnybody.test_ac4_an_empty_ledger`, `test_ac11_people_with_nothing_recorded`, `test_ac7_every_debt_repaid_prints_no_zero_line` — three different routes to the empty report, each asserting the exact single line and exit 0 |
| AC5 — ordered by debtor then creditor under `name.strip().casefold()`, stable across runs | the final `lines.sort` keys on `normalise_name` of both names, not on the display forms | `TestOrdering.test_debtors_are_ordered_case_insensitively_while_the_names_keep_their_case` (people `ana`, `Ben`, `Cara`: sorting display forms would put `Cara` first); `test_creditors_are_ordered_case_insensitively_too` (`ana` before `Ben` as creditor); `test_running_the_report_twice_over_unchanged_data_prints_the_same_thing`; `test_the_order_does_not_depend_on_when_an_expense_was_recorded` |
| AC6 — repayments net off, worked example including an overshoot | a repayment adds to the same signed pair total as the expenses | `TestWorkedExamples.test_ac6_repayments_net_off_and_an_overshoot_reverses_the_pair` asserts `["Ana owes Cara 2.00", "Cara owes Ben 6.00"]` |
| AC7 — never a `0.00` line once everything is repaid | `if balance == 0: continue` before a `Debt` is made | `TestNobodyOwesAnybody.test_ac7_every_debt_repaid_prints_no_zero_line` asserts the single empty-report line and `"0.00" not in result.out` |
| AC8 — a circle is printed, not collapsed | no amount is moved between pairs | `TestWorkedExamples.test_ac8_a_circle_is_printed_not_collapsed` asserts the exact three lines; `TestWorkedLedgers.test_ac8_a_circle_is_printed_although_every_net_position_is_zero` additionally asserts `set(net_positions(...).values()) == {0}` for that ledger |
| AC9 — an uneven remainder stays with the payer | `share = amount_minor // len(sharers)`, and the payer is never a debtor to themselves | `TestWorkedExamples.test_ac9_an_uneven_split_leaves_the_remainder_with_the_payer` asserts `["Ben owes Ana 3.33", "Cara owes Ana 3.33"]`; `TestWorkedLedgers.test_adr0009_a_non_sharing_payer_absorbs_the_odd_cent` covers `ADR-0009`'s case, 10.01 between two sharers whose payer is not one of them |
| AC10 — a repayment between people who share no expense reverses | the repayment creates the pair | `TestWorkedExamples.test_ac10_a_repayment_between_people_who_share_nothing_reverses` asserts `["Ben owes Ana 5.00"]` |
| AC11 — a person involved in nothing produces no line and does not suppress AC4 | such a person appears in no pair | `TestNobodyOwesAnybody.test_ac11_people_with_nothing_recorded`; `test_ac11_an_uninvolved_person_neither_adds_a_line_nor_removes_one` adds `Dan` to the AC2 ledger and asserts the output is byte-identical and contains no `Dan` |

Three of the criteria were also checked by mutation, to confirm the tests would fail if the
behaviour were removed rather than passing against anything:

- sorting by the display forms instead of the normalised ones → 2 failures
  [src: run: `python3 -m unittest discover -s tests -t . -q` with `lines.sort(key=lambda debt: (debt.debtor, debt.creditor))` → exit 1, FAILED (failures=2)]
- ignoring the repayments entirely → 11 failures
  [src: run: `python3 -m unittest discover -s tests -t . -q` with the repayment loop emptied → exit 1, FAILED (failures=11)]

The module was restored from a copy after each and the suite re-run green
[src: run: `python3 -m unittest discover -s tests -t . -q` → exit 0, 115 tests, OK].

## Deviations from the plan

Two, both in *how* rather than *what*.

1. **The plan's step 1.1 said the display-name fallback takes "first occurrence winning" and
   named `ledger.people` as the primary source. Built as written, using `dict.setdefault` over
   people first and then over the records** — the plan did not say what to iterate for the
   fallback, and `_display_names` walks expenses then repayments. No criterion reaches this path;
   it exists so a hand-edited ledger reports rather than raising `KeyError`.
2. **The plan's step 3 said the `debts` subparser is registered after `repayments` "so `--help`
   lists it last", and it is. But `cli.py` imports the module as `debts_module`**, because the
   subparser variable inside `build_parser` is called `debts` and the plan's own step 3 named it
   that. Naming the import rather than the local keeps the plan's wording intact.

Nothing in the plan's five steps was skipped or reordered.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, 115 tests, OK (83 before this item) |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses tests` → exit 0. It is a syntax check and nothing more (`ADR-0005`) |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | the table above: every one of the eleven criteria names at least one test function, and none is demonstrated by reading the code |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | the diff is `expenses/debts.py` (new), `tests/test_debts.py` (new), `tests/test_cli_debts.py` (new), four hunks in `expenses/cli.py` (import, constant, subparser, handler), the overview's v5 edit, and the tracker's own files. Every hunk traces to a plan step |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0 |

## What I did not do

- **I did not fix `expenses/cli.py`'s module docstring**, which still opens "the only module that
  prints, and the only one that exits". The second half is false — `main` returns an `int` and
  `__main__.py` raises the `SystemExit` — and `docs/architecture/overview.md` v3 records
  `review-close` correcting exactly that sentence in the overview while leaving the docstring
  alone [src: docs/architecture/overview.md]. It is a WI-0001 artefact, no criterion of this item
  touches it, and fixing it here would put a hunk in the diff that traces to nothing. Left for
  whoever owns it.
- **I did not touch BUG-0001**, the open bug about a failed ledger write still printing the
  success line [src: BUG-0001]. `debts` writes nothing, so it is unaffected.
- **I added no `--format`, no filtering and no per-person summary.** All three are named in the
  item's `## Out of scope`.
- **The empty-sharer-list and unknown-name-on-a-record paths have no acceptance criterion.** They
  are only reachable by hand-editing the ledger file, and they are covered by
  `TestWorkedLedgers.test_an_expense_nobody_shares_owes_nobody_anything` and by the
  `_display_names` fallback rather than by anything a user can type. The plan records both as
  reversible assumptions.
