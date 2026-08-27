---
id: WI-0002
type: work-item
title: Show who owes whom
status: done
priority: high
epic: EP-001
depends-on:
  - WI-0001
created: "2026-08-26T23:22:38Z"
updated: "2026-08-27T00:51:47Z"
branch: wi/WI-0002
outcome: delivered
---

## Story

As someone who shares costs with friends, I want to ask the tool who owes whom at any point, so
that we can settle up without anybody doing the arithmetic by hand.

## Acceptance criteria

Every criterion below names the commands that set up its data, the command that settles it, and
the observation that decides it, so that someone with a terminal and no context reaches the same
verdict. `$S` is a scratch data file: each criterion starts from a path that does not exist and
runs every command in it with `EXPENSES_STORE=$S`, which is a documented part of the tool.

- [x] AC1 — with `person add Ana`, `person add Ben`, `person add Cara` and
      `expense add --amount 30 --paid-by Ana --shared-by Ana,Ben,Cara` recorded,
      `python3 -m expenses settle` exits 0 and its stdout is exactly two lines which, sorted, are
      `Ben pays Ana 10.00` and `Cara pays Ana 10.00`.

- [x] AC2 — `python3 -m expenses settle` exits 0 and its stdout is exactly `no payments needed`
      in each of these three stores: (a) one where nothing has been recorded at all; (b) one where
      `person add Ana` and `person add Ben` have run and no expense has been recorded; (c) one
      where `person add Ana` and `person add Ben` have run and the only expense is
      `expense add --amount 10 --paid-by Ana --shared-by Ana`, so that every position is zero.

- [x] AC3 — with `Ana`, `Ben`, `Cara`, `Dan` and `Eve` added in that order and these three
      expenses recorded in this order —
      `--amount 30 --paid-by Ana --shared-by Ana,Ben,Cara`,
      `--amount 12 --paid-by Ben --shared-by Cara,Dan`,
      `--amount 10 --paid-by Cara --shared-by Ana,Ben,Cara` —
      `python3 -m expenses settle` exits 0 and its stdout is exactly three lines which, sorted,
      are `Ben pays Ana 1.33`, `Cara pays Ana 9.33` and `Dan pays Ana 6.00`. In particular: every
      amount is greater than zero; no name is both a payer and a receiver; `Eve`, whose position
      is zero, appears nowhere; there are three lines, one fewer than the four people whose
      position is not zero; and each debtor's amount equals what they owe overall, the three
      summing to the 16.66 owed to `Ana`.

- [x] AC4 — with AC3's store, `python3 -m expenses settle` run twice in two separate processes
      produces byte-identical stdout, compared with `cmp`.

- [x] AC5 — running `python3 -m expenses settle` changes nothing: with AC3's store, the data
      file's `md5sum` is identical before and after the run; and with `EXPENSES_STORE` pointing at
      a path that does not exist, `settle` exits 0, prints `no payments needed`, and that path
      still does not exist afterwards.

- [x] AC6 — `README.md` documents the command: it names `python3 -m expenses settle`, shows an
      example of its output, and states what it prints when there is nothing to settle.

## Out of scope

- Recording that a debt has been paid off, or settling up inside the tool. The command reports;
  it writes nothing (AC5).
- Moving money, or talking to a bank or payment service.
- Any history of how the balances changed over time; the command answers about now.
- Printing each person's net position — how much they are up or down overall. EP-001/Q-002
  offered it as option C and the stakeholder chose option B, the payment list, on its own. If
  they later want the positions as well, that is a new item, not a widening of this one.
- **Unwinding pairwise debts.** The list is computed from each person's overall position, so it
  may tell one person to pay another they never shared an expense with — Ana pays Cara, when
  every expense between them was with Ben. That is what makes the list short, and it is a
  consequence of the settlement list the stakeholder chose rather than an oversight. A mode that
  only ever pays people you actually shared with would be a different item.
- Choosing what to settle: no filtering by date, by person, or by trip. Nobody has asked for it,
  and `settle` takes no flags.
- Deleting or amending anything that was recorded wrongly. That is WI-0004.

## Notes

### What the stakeholder settled

- EP-001/Q-002 is answered. The stakeholder chose a settlement list over net positions, in their
  own words: *"The list of payments that settles it — that's what actually saves us the arguing
  after a trip."* AC1 is written against that and must not be reinterpreted as a balance report.
- How an expense divides between its sharers is **settled**: WI-0001/Q-001 was answered by the
  stakeholder — *"Equal split, keep it simple. If a bill's uneven we'll just enter it as separate
  expenses."* A person's **position** is therefore the sum of the amounts of the expenses they
  paid, minus the sum of the shares recorded against them.
- Delivery order, from EP-001/Q-003: WI-0001, then this item, then WI-0003. The stakeholder
  delegated the order (*"Whatever you think is best on the order"*) and `answer-questions` chose
  it, because this item is what makes the tool answer the question it was built for.
- Depends on WI-0001, which is `done`: there was nothing to report on until people and expenses
  could be recorded.

### What refinement settled, and under whose authority

EP-001/Q-002's answer states that the settlement rule is not the stakeholder's to decide but
refinement's and then `plan`'s. Under that delegation, and recorded in full in
`artifacts/refinement-qa.md` as B1–B7, refinement fixed: the command (`settle`, no flags), what a
position is, the properties the printed list must have, the exact `no payments needed` string,
the `X pays Y 10.00` line form, and that the command writes nothing. None of these was put to the
stakeholder and none is recorded as theirs.

- No rounding arises in this item. WI-0001 stores each expense's shares as whole minor units that
  already sum to exactly the amount paid, so every position is exact and the positions sum to
  exactly zero. The indivisible-unit rule was decided on WI-0001 and is recorded in ADR-0003;
  this item neither restates nor revisits it.

### Open design questions for `plan`

- **Which settlement, exactly.** AC3's dataset has a single creditor, so its expected output is
  forced by the properties in `artifacts/refinement-qa.md` B3 and not by any particular algorithm.
  With more than one creditor those properties still leave a choice, and `plan` must record the
  rule that makes it — which debtor is matched against which creditor, and in what order the lines
  print. The only constraint refinement places on it is that it be deterministic, which is what
  AC4 checks.
- **Where the arithmetic lives.** Whether positions are computed in a new module, in `store.py`,
  or in the command handler is `plan`'s.

### Deliberately unconstrained

- How many people or expenses the command must cope with, and how fast it must run. Nothing is
  said about either. Left unconstrained by **refinement**: the stakeholder described a friend
  group, `docs/product/vision.md` records one person on one machine, and a threshold nobody asked
  for is a threshold nobody believes.

### What review accepted as gaps, at close

`review-close` accepted five declared gaps rather than sending the item back. They are recorded
here because once an item is `done` nobody opens its verification report again, and a gap that
lives only in a report stops being true without anyone noticing
[src: tracker/items/WI-0002/artifacts/review.md].

- **Nothing was linted.** `commands.lint` is null in `tracker/project.yaml` on ADR-0004's record —
  the project installs nothing and the standard library ships no linter. `implement` and `verify`
  both reported the gate as `skipped` rather than as a pass. Everything this item claims rests on
  behaviour, not on style checks.
- **`settlement()`'s docstring claims it terminates on a dataset whose positions do not sum to
  zero, and no test covers that.** No delivered command can produce such a dataset, so a test
  would need a hand-written file the tool would never write. Declared in `plan.md`'s third
  assumption. Treat the docstring as a design note, not as evidence.
- **`positions()` silently ignores a name that appears in an expense but not in `data["people"]`.**
  Unreachable today — `add_expense` refuses an unknown name and nothing deletes a person. **WI-0004
  adds deletion, and if it deletes a person without touching their expenses, this report will
  silently drop them from the totals.** It is WI-0004's to solve and its criteria's to state
  [src: tracker/items/WI-0002/artifacts/plan.md].
- **Scale was never exercised.** Consistent with `## Deliberately unconstrained` above: no
  threshold was ever set, so there was nothing to check against.
- **No acceptance criterion reaches ADR-0005's creditor-side tie-break.** AC1's and AC3's datasets
  each have a single creditor. `tests/test_settle.py::test_two_creditors_are_paid_largest_credit_first`
  covers it and passes, but that is a test the implementation chose to write rather than a
  criterion this item can be held to.

One more fact about the tests, found by `verify` through mutation and worth having here: **AC1's
end-to-end test cannot detect a change to ADR-0005's tie-break**, because AC1 compares *sorted*
stdout. Reversing the tie-break leaves `WI0002AC1SettleListsThePayments` green. The rule is pinned
instead by `tests/test_settle.py::test_ac1_tie_between_two_equal_debts_goes_to_whoever_was_recorded_first`
and `::test_ac1_reversing_the_recorded_order_reverses_the_payments`. Whoever changes ADR-0005 should
change those, and should not read a green AC1 as agreement
[src: tracker/items/WI-0002/artifacts/verify-report.md].
