# Implementation report — WI-0003

## What was built

`./expenses report`, and the module behind it. The plan's ten steps were worked in order.

- **`expenses_tool/settle.py`** (new) — `shares` (ADR-0001 clause 2, the largest-remainder split),
  `balances` (every registered person, credited what they paid and debited their share of what they
  shared in), and `settle` (ADR-0010 clause 2, the greedy match). No printing, no exits, no floats.
- **`expenses_tool/cli.py`** — `render_balance`, `render_payment`, `cmd_report`, the `report`
  subparser, and the `NOBODY_OWES` constant. Every user-visible string for this command is here.
- **`tests/test_settle.py`** (new, 15 tests including three property checks) and
  **`tests/test_cli_report.py`** (new, 10 tests across nine criterion classes).
- **`README.md`** — a "Who owes whom" section with the worked example's real output, the penny
  rule, and the two things the report deliberately does not do.

Nothing was added to the data file and `store.py` was not touched: the report is a pure function of
what WI-0002 already writes.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — payments settle, at most `n-1` | `settle.settle` drops whoever reaches zero, so each payment removes at least one person | `test_cli_report.py::AC1::test_payments_settle_and_are_bounded` — parses the printed report, applies the payments to the printed balances and asserts every one reaches zero, and asserts the payment count is at most one fewer than the non-square balances; plus `test_settle.py::Settlement::test_never_more_than_n_minus_one` over every zero-sum split of four people |
| AC2 — the worked example, exactly | the whole pipeline | `AC2::test_worked_example` — builds it with five subprocess invocations and compares the **whole** stdout to `Ana is owed 15.00\nBen is square\nCass owes 15.00\n\nCass pays Ana 15.00\n`, stderr empty, exit 0 |
| AC3 — payments balance and settle | `settle.settle` moves `min(debt, credit)` each time | `AC3::test_totals_match_and_balances_clear` — three expenses including an indivisible one; sums the payments in each direction and checks each against the printed balance; `test_settle.py::Settlement::test_payments_clear_the_balances` |
| AC4 — both empty cases | `cmd_report` returns early with `NOBODY_OWES` when no expense exists, and prints it after the balances when the settlement is empty | `AC4::test_no_expenses` — stdout exactly `Nobody owes anybody\n`, no balance lines; `AC4::test_everyone_square` — stdout exactly `Ana is square\nBen is square\n\nNobody owes anybody\n` |
| AC5 — earlier invocations | `store.load` each run | `AC5::test_reads_earlier_invocations` — the example built across five separate processes, `report` run in a sixth |
| AC6 — the indivisible split | `settle.shares` | `AC6::test_indivisible_split` — one `10.00` expense; whole stdout compared to the five quoted lines |
| AC7 — the balance section | `render_balance` and the `store.normalise` sort | `AC7::test_balance_lines_and_order` — registers `Cass`, `ana`, `Ben`, `Dan`, asserts the four lines in normalised order including `Dan is square`, and that the amounts sum to zero |
| AC8 — a person registered afterwards | nothing in `balances` recomputes sharers; they come from the stored record | `AC8::test_late_person_changes_nothing` — the worked example, `add-person Dan`, then the AC2 output with `Dan is square` inserted; plus `test_settle.py::Balances::test_a_person_registered_later_does_not_change_a_past_expense` |
| AC9 — the report never writes | `cmd_report` never calls `store.save` | `AC9::test_report_does_not_write_and_repeats` — the file's bytes compared before and after, and two consecutive runs compared to each other |

## Deviations from the plan

Two, both within "how":

1. **`settle.settle` mutates its two working lists in place** rather than rebuilding them each
   round. Same algorithm, same output; the plan did not say which, and the in-place version keeps
   the tie-break sort in exactly one place.
2. **`NOBODY_OWES` is a module constant** rather than a literal in each of the two branches. The
   plan called for the same sentence in both cases, and a constant is how that is guaranteed rather
   than intended.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 87 tests`, `OK`, on branch head `a830980` |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses expenses_tool tests` → exit 0 (a syntax check; ADR-0007 clause 4) |
| `workspace-valid` | **pass** | `validate-workspace` → exit 0, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | AC1–AC9 each have a named test class in `tests/test_cli_report.py`, listed above |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → all commits name WI-0003 |

## What I did not do

- **No question was filed.** Every decision was fixed by an ADR — including the one refinement
  deliberately left open, which `plan` settled as ADR-0010.
- **No optimisation of the settlement.** ADR-0010 accepts that greedy can occasionally emit one
  payment more than a perfect solver; nothing here tries to do better, and the property test
  asserts only the `n-1` bound the criteria ask for.
- **Nothing was built for WI-0004.** The import will produce the same expense records and this
  report will read them unchanged.
- **The three behaviours the item leaves unconstrained were left alone**: which minimal settlement
  is printed when several exist (ADR-0010 decides it, but no criterion constrains it),
  `argparse`'s usage wording, and behaviour with a very large group — nothing here was measured at
  scale.
- **`docs/` was not touched by this execution.** `plan` wrote ADR-0010 and bumped the overview to
  v3 before any code existed, and nothing in the implementation contradicted either.
