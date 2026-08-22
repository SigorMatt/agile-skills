# Plan — WI-0003 Show who owes whom

## Problem

The tool records who paid for what and who shared in it; it does not yet answer the question the
stakeholder actually asked — *"at any point show who owes whom"*. This item adds `./expenses
report`, which prints each person's overall balance and then the payments that settle the group up.
It computes and prints; it stores nothing new and changes nothing that exists.

The constraints are all recorded. The report is a **settlement**, not a debt-by-debt listing
(WI-0003/Q-001, the stakeholder's own choice); balances are printed alongside it because they are
what make it checkable by hand (Q-003); money is whole pence and an indivisible amount is split by
largest remainder in trimmed case-folded name order (ADR-0001); the sharers of an expense are the
ones stored on it, not the people registered today (ADR-0009 clause 3); and the streams and exit
codes are ADR-0005's. The criteria quote two complete expected reports, so the output format has no
latitude at all.

## Approach

One new module, `expenses_tool/settle.py`, holding the two computations — balances from expenses,
and payments from balances — and nothing about presentation. `cli.py` gains `cmd_report` and the
two rendering helpers, because every user-visible string belongs there (ADR-0008 clause 3).

The settlement algorithm is ADR-0010: repeatedly match the largest debtor to the largest creditor,
tie-broken by name, which achieves AC1's `n-1` bound by construction. The printed payments are
sorted by payer then payee, so the algorithm's internal order never reaches the screen.

Nothing in this item writes: `cmd_report` calls `store.load` and never `store.save`, which is what
AC9 checks from outside.

## Steps

1. **`expenses_tool/settle.py` — balances.** `balances(data) -> dict[str, int]` returns a balance in
   whole pence for **every registered person**, including those who shared in nothing (AC7), keyed
   by the stored display name. For each expense: credit `paid_by` the full `amount_pence`; debit
   each name in `shared_by` their share, computed by `shares()` below. An expense naming somebody
   not in `people` cannot arise (WI-0002 AC4, ADR-0009 clause 5) and is not defended against.

2. **`expenses_tool/settle.py` — the split.** `shares(amount_pence, sharers) -> dict[str, int]`
   implements ADR-0001 clause 2 exactly: `base = amount // n`, `r = amount % n`, sharers sorted by
   `store.normalise`, the first `r` of them owing `base + 1` and the rest `base`. It returns a
   mapping and asserts nothing; its correctness is that the values sum to `amount_pence`.

3. **`expenses_tool/settle.py` — the settlement.** `settle(balances) -> list[tuple[str, str, int]]`
   implements ADR-0010 clause 2: debtors and creditors as two lists sorted by amount descending then
   by `store.normalise`, repeatedly emitting `(debtor, creditor, min(debt, credit))` and reducing
   both, dropping anyone who reaches zero. It returns the payments **unsorted for printing**;
   ordering the output is the caller's job (ADR-0010 clause 4).

4. **`expenses_tool/cli.py` — rendering the two sections.** `render_balance(name, pence) -> str`
   returns `f"{name} is owed {format_amount(pence)}"` for a positive balance,
   `f"{name} owes {format_amount(-pence)}"` for a negative one, and `f"{name} is square"` for zero.
   `render_payment(payer, payee, pence) -> str` returns
   `f"{payer} pays {payee} {format_amount(pence)}"`. Both are the only place these strings exist.

5. **`expenses_tool/cli.py` — `cmd_report`.** Load; compute balances; if there are no expenses
   recorded, print exactly `Nobody owes anybody` and return 0 with no balance lines (AC4). Otherwise
   print one balance line per registered person in `store.normalise` order; print a blank line;
   then either the payments — sorted by `store.normalise` of the payer, then of the payee — or, if
   there are none, `Nobody owes anybody` (AC4's second half). Return 0. A `store.DataFileError` is
   refused exactly as everywhere else: `Cannot read <path>: <reason>` on stderr, exit 1.

6. **`expenses_tool/cli.py` — the subparser.** `report`, taking the shared `--data-file` and
   nothing else (the item's `## Out of scope`).

7. **`tests/test_settle.py`.** `shares` for an even split, for `1000` three ways (`334, 333, 333`,
   the ADR-0001 example), for one sharer, and a property check that the shares always sum to the
   amount across a range of amounts and group sizes. `balances` for the worked example, for a payer
   who is not a sharer, for a person who shared in nothing, and that every balance set sums to
   zero. `settle` for the worked example, for the AC6 case, for an already-square group (no
   payments), and a property check that the payments settle the balances and number at most `n-1`.

8. **`tests/test_cli_report.py`.** One class per acceptance criterion, AC1 to AC9, each building
   its data with real `add-person` and `add-expense` invocations and then running `./expenses
   report` in a subprocess, comparing whole stdout against the criteria's quoted text where they
   quote it (AC2, AC4, AC6) and the specific property otherwise.

9. **`README.md`.** A "Who owes whom" section: the command, the worked example with its output, the
   two sections, and a sentence on what the report does not do (it does not explain a payment,
   because netting means a payment corresponds to no single expense).

10. **Run both project commands** from the repository root on the final state of the code.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — payments that settle, at most `n-1` of them | 3, 5 | `test_cli_report.py::AC1::test_payments_settle_and_are_bounded` — three people, two expenses, asserting one payment line and that applying it zeroes the printed balances; and `test_settle.py::Settlement::test_never_more_than_n_minus_one` over generated balance sets |
| AC2 — the worked example, exactly | 1, 2, 3, 4, 5 | `AC2::test_worked_example` — builds it with five invocations, compares the **whole** stdout to the four quoted lines including the blank line, exit 0 |
| AC3 — payments balance and settle | 3, 5 | `AC3::test_totals_match_and_balances_clear` — sums the payment amounts in each direction from the printed output and applies them to the printed balances; `test_settle.py::Settlement::test_payments_clear_the_balances` |
| AC4 — both empty cases | 5 | `AC4::test_no_expenses` — stdout exactly `Nobody owes anybody\n`, no balance lines, exit 0; `AC4::test_everyone_square` — one expense paid and shared by the same person, asserting the balance section, a blank line, then `Nobody owes anybody` |
| AC5 — records from earlier invocations | 1, 5 | `AC5::test_reads_earlier_invocations` — the worked example built across three separate `subprocess.run` calls, `report` run in a fourth |
| AC6 — the indivisible split | 2, 3, 5 | `AC6::test_indivisible_split` — one `10.00` expense, comparing the whole stdout to the five quoted lines |
| AC7 — the balance section | 1, 4, 5 | `AC7::test_balance_lines_and_order` — checks the three line forms, `store.normalise` ordering, that a person who shared in nothing is `is square`, and that the amounts sum to zero |
| AC8 — a person registered afterwards | 1, 5 | `AC8::test_late_person_changes_nothing` — the worked example, then `add-person Dan`, then `report`, asserting AC2's output with `Dan is square` inserted in name order |
| AC9 — the report never writes | 5 | `AC9::test_report_does_not_write_and_repeats` — `cmp` of the data file's bytes before and after, and two consecutive runs compared to each other |

## Assumptions

- **A person with a zero balance never appears in a payment**, even when they shared in expenses.
  ADR-0010 clause 5 says so; it falls out of the algorithm rather than needing a check. Reversal is
  meaningless — there is no payment to make.
- **The blank line between the sections is a single `print()`**, so the output ends with exactly one
  newline after the last payment. AC2 and AC6 quote the whole output, so this is pinned by them
  rather than assumed loosely.
- **`balances` iterates `data["people"]` for its keys**, so a person appears in the report exactly
  once and in registration order before sorting. Reversal is one line.
- **The report treats "no expenses" and "no payments" as different code paths** producing the same
  sentence, because AC4 asks for the sentence alone in the first case and after the balances in the
  second.

## Decisions and ADRs

- **ADR-0010 — the greedy settlement.** Route: decided, because `refine` explicitly left "which
  settlement when several are minimal" to `plan` and named it as unconstrained. Options considered
  were greedy, a provably minimal search, a clearing-house variant that fails AC3, and the pairwise
  listing the stakeholder rejected. The ADR fixes the tie-break and the print order, which is what
  makes the report deterministic and therefore checkable.
- **Answered from existing documents, not re-decided:** the split rule and its worked example
  (ADR-0001 clause 2), the subcommand name (ADR-0002 clause 3), the sort key (ADR-0003 clause 4),
  `--data-file` (ADR-0004), streams and exit codes including "nothing to show is not an error"
  (ADR-0005 clauses 2 and 4), the record an expense stores and its snapshotted sharers (ADR-0009 —
  which is what makes AC8 true without any work in this item), the test layers (ADR-0007 clause 3),
  and where a user-visible string may live (ADR-0008 clause 3).
- **No new stored state and no change to the data file.** The report is a pure function of what is
  already there, which is why this item touches neither `store.py` nor ADR-0006.
- **`tracker/project.yaml` needs no change.**
- **`docs/architecture/overview.md` will need a bump** for the new module and the new command.

## Risks

- **AC8 is already true and could be untested by accident.** Nothing in this item computes sharers
  — they come from the stored record (ADR-0009 clause 3) — so an implementation that ignored AC8
  entirely would still pass it. The criterion is worth keeping precisely because the natural
  shortcut in a *report* is to recompute "everyone" from `data["people"]`, and the test would catch
  that regression in this item or a later one.
- **A payer who is not a sharer is easy to get wrong.** They are credited the full amount and debited
  nothing, so their balance is the whole expense. Step 7's unit test covers it; no acceptance
  criterion does, because the item's examples all have the payer sharing.
- **`shares` must not use floating point.** ADR-0001 clause 1 forbids it, and a `/` where `//` was
  meant would produce balances that look right and fail to sum to zero. The property test in step 7
  is the guard.
- **The greedy settlement can occasionally emit one payment more than a perfect solver.** ADR-0010
  records this and the criteria accept it; it is stated here so nobody later reads a suboptimal
  settlement as a defect.
- **Reading the report as authoritative about the past.** The report reflects the ledger *now*: it
  has no way to show what was owed last week, and nothing in the epic records a settlement having
  been made. A reader could take "Cass owes Ana 15.00" as still true after Cass has paid. That is
  EP-001's stated scope, not a defect, and the README says so.

## Out of scope for this item

- Recording that a payment was made, or marking a debt settled (EP-001).
- Explaining a payment, or showing which expenses produced a balance (the item's `## Out of scope`;
  it is also option C from Q-003, which the stakeholder did not choose).
- Any option on `report` other than `--data-file`, and any output format other than the text the
  criteria quote.
- The CSV import (WI-0004), which will feed this report through the same records.
