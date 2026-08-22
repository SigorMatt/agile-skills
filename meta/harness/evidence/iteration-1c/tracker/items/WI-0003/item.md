---
id: WI-0003
type: work-item
title: Show who owes whom
status: done
priority: high
epic: EP-001
branch: wi/WI-0003
created: "2026-08-21T21:07:03Z"
updated: "2026-08-21T22:39:25Z"
outcome: delivered
---

## Story

As the person keeping the group's books, I want one command that tells me who owes whom and how
much across everything recorded so far, so that the group can settle up without anyone doing
the arithmetic or trusting someone else's.

## Acceptance criteria

Every criterion is checked from the repository root against `$T`, a data file that does not exist
when the criterion starts. People are registered with `./expenses add-person` and expenses recorded
with `./expenses add-expense` (WI-0001, WI-0002).

The report has two parts, in this order, separated by a blank line:

```
<name> is owed <amount>        one line per registered person, in trimmed case-folded name order
<name> owes <amount>
<name> is square

<payer> pays <payee> <amount>  the payments to make, sorted by payer then payee, same name order
```

Amounts are to two decimal places with no currency symbol. **The worked example** AC2 refers to is:
`Ana`, `Ben` and `Cass` registered in that order; `Ana` pays `30.00` for `dinner` shared by all
three; `Ben` pays `15.00` for `taxi` shared by all three; `Cass` pays nothing. Each person's share
is `15.00`, so `Ana` is owed `15.00`, `Ben` is square and `Cass` owes `15.00`, and the single
payment is `Cass pays Ana 15.00`.

- [x] AC1 — `./expenses report --data-file "$T"` prints the payments to make, each on its own line
      reading `<payer> pays <payee> <amount>`, and exits 0. Making exactly those payments leaves
      every person square, and the number of payment lines is at most one fewer than the number of
      people whose balance is not zero (WI-0003/Q-001: a settlement, not a debt-by-debt listing)
- [x] AC2 — run against the worked example above, `./expenses report --data-file "$T"` prints
      exactly:

      ```
      Ana is owed 15.00
      Ben is square
      Cass owes 15.00

      Cass pays Ana 15.00
      ```

      and exits 0. Every figure follows from the two expenses by hand: `30.00` and `15.00` each
      divided three ways is `10.00` and `5.00`, so each person's share of everything is `15.00`
- [x] AC3 — the payments balance and settle: for the worked example and for any other data, the
      total paid across the printed payments equals the total received, and applying every printed
      payment to the balances printed above them leaves every balance at `0.00`
- [x] AC4 — `./expenses report --data-file "$T"` with no expenses recorded prints exactly
      `Nobody owes anybody` on stdout, prints no balance lines, and exits 0 (ADR-0005 clause 4).
      The same line, after the balances and a blank line, is printed when expenses exist but every
      balance is zero — a report never ends with an empty section
- [x] AC5 — the report reflects expenses recorded in earlier, separate invocations of the tool: the
      worked example built across three invocations produces the AC2 output when `report` is run in
      a fourth
- [x] AC6 — an expense whose amount does not divide evenly among its sharers is split by ADR-0001:
      whole pence, `base = amount // n` each, and the leftover `amount % n` pennies given one each
      to the sharers sorted first by trimmed case-folded name. With `Ana`, `Ben` and `Cass`
      registered and one expense of `10.00` paid by `Ana` and shared by all three, the shares are
      `3.34`, `3.33` and `3.33`, so `./expenses report` prints exactly:

      ```
      Ana is owed 6.66
      Ben owes 3.33
      Cass owes 3.33

      Ben pays Ana 3.33
      Cass pays Ana 3.33
      ```
- [x] AC7 — the report prints each person's overall balance before the payments: one line per
      registered person, reading `<name> is owed <amount>`, `<name> owes <amount>` or
      `<name> is square`, in trimmed case-folded name order (ADR-0003 clause 4). A person who is
      registered but shared in nothing appears, as `is square`. The amounts owed and the amounts
      due each sum to the same total, so the balance lines sum to zero (WI-0003/Q-003)
- [x] AC8 — a person registered after an expense was recorded does not change that expense's share:
      building the worked example, then `./expenses add-person Dan`, then `./expenses report`
      prints the AC2 balances and payment unchanged, with `Dan is square` inserted in name order
- [x] AC9 — the report reads the ledger and never writes it: `cmp` shows `$T` byte-for-byte
      unchanged after `./expenses report` has been run, and running the report twice in a row
      prints identical output both times

## Out of scope

- Listing every pairwise debt as it arose, or one line per pair of people. The stakeholder chose
  the settlement reading in WI-0003/Q-001 — "I just want the actual payments — who pays whom to
  settle up. Don't need every individual debt listed out." A payment the report prints therefore
  need not correspond to any single expense, and the tool is not required to explain why a given
  pair appears.
- Marking a debt as settled, or recording a repayment; the epic excludes it.
- Filtering the report by date, by person, or by expense.
- Any output format other than text on the terminal (no CSV, JSON or HTML export).
- Explaining a payment. A printed payment need not correspond to any single expense — that is what
  netting means — so the report does not say which expenses produced it, and there is no
  `--explain`, no per-expense breakdown and no history of how a balance was reached.
- Any option on `report`. It takes `--data-file` and nothing else: no `--person`, no `--since`, no
  `--currency`, no way to change the format.

## Notes

Both questions this item was suspended on are answered, and the criteria above have been
sharpened accordingly by `answer-questions`.

- **WI-0003/Q-001 — the report is a settlement, not a debt listing.** The stakeholder chose
  option B over the recommended option C: "I just want the actual payments — who pays whom to
  settle up. Don't need every individual debt listed out." AC1 and AC3 were rewritten in those
  terms and the pairwise reading is now explicitly out of scope. Per-person balances are still
  computed — a settlement cannot be produced without them — but the stakeholder did not ask for
  them to be printed, so AC1 does not require it. Whether to print them anyway is a presentation
  question for `refine`, not a blocker.
- **WI-0003/Q-003 — the report prints balances as well as payments.** The stakeholder chose
  option B: "Yeah, show each person's balance too, not just the payments — makes it easier to
  check." AC7 states it. The balances come first and the payments follow, because the payments are
  derived from the balances and a reader checking the report by hand (AC2) works in that order.
  This is a strict addition to AC1, not a substitute: the pairwise listing the stakeholder declined
  in Q-001 stays out of scope, and a balance line is one line per *person*, never one per pair.
- **WI-0003/Q-002 — the rounding rule is ADR-0001.** The stakeholder declined to choose and
  authorised proceeding ("Not sure yet — go ahead anyway, we'll decide later"), so the architect
  decided: whole pence internally, and leftover pennies handed one each to the alphabetically
  first sharers. AC6 states the rule with a worked example; ADR-0001 records the options, the
  reasoning, and the fact that the whole-pence part of it is expensive to reverse once data
  exists.

`refine` still has to pin the exact command name and the exact output wording that AC1, AC2 and
AC4 refer to as "documented", and to fix the worked example AC2 names. Two decisions made for
WI-0001 bind it while it does so: **ADR-0002** (the surface is `./expenses <subcommand>`, and
`report` is the reserved name for this one) and **ADR-0005** (stdout and exit 0 for output and for
"nothing to show"; stderr and exit 1 only for a refusal). Amounts print to two decimal places with
no currency symbol, per AC7.

### Decided during refinement, and by whom

`refine` fixed the following. All are recorded as `[assumed]` in `artifacts/refinement-qa.md`, and
all rest on conventions the stakeholder delegated for WI-0001 (Q-004) and that `answer-questions`
recorded as ADR-0002 and ADR-0005 and stated as binding on the later items.

- **The command is `./expenses report`**, the name ADR-0002 clause 3 reserved. It takes only
  `--data-file`.
- **The two sections, their order and the blank line between them.** The stakeholder asked for
  balances "too, not just the payments — makes it easier to check" (Q-003), and a reader checking
  by hand works from the balances to the payments, so the balances come first.
- **The three balance line forms** — `is owed`, `owes`, `is square` — and the payment form
  `<payer> pays <payee> <amount>`. These are the shapes the questions themselves showed the
  stakeholder, so they are the wording they have already seen.
- **Payments are printed sorted by payer then payee**, in the same trimmed case-folded order the
  balances use. A settlement's *internal* order is an artefact of whatever algorithm produces it;
  sorting the output makes AC2 and AC6 comparable without constraining `plan`'s algorithm.
- **`Nobody owes anybody` is the message for both empty cases** — no expenses at all, and expenses
  that happen to leave everyone square. A report that printed balances and then nothing would read
  as truncated.
- **The worked example is fixed in the criteria**, not left to `verify` to invent, because AC2
  requires a reader to reproduce it by hand and they cannot do that against an example that changes.
- **A person who shared in nothing still gets a balance line** (`is square`). Omitting them would
  make a registered person invisible in the only view that shows standing.

### Left deliberately unconstrained (R10)

Recorded so the gaps are visible rather than absent, per `spec/dor-dod.md` R10. Left by `refine`.

- **Which settlement is produced when more than one satisfies AC1 and AC3.** With three or more
  people there can be several minimal settlements; the criteria pin the two worked examples, where
  the answer is unique, and otherwise require only that the payments settle and are at most `n-1`.
  `plan` chooses the algorithm and `ADR` records it if the choice is not obvious.
- **`argparse`'s usage-error wording**, as on WI-0001 and WI-0002; only the exit code 2 is fixed
  (ADR-0005 clause 3).
- **How the report behaves with a very large group.** Every criterion here uses three or four
  people. Nothing states an upper bound and nothing performs one.

One case cannot arise and so has no criterion: a payment involving somebody who is not registered.
Expenses can only name registered people (WI-0002 AC4), and nobody can be removed (EP-001), so
every balance belongs to a registered person.

### Accepted gaps at close

Recorded by `review-close` so that they outlive this item's closure. `artifacts/review.md` has the
reasoning.

- **AC9 cannot detect the regression it exists to prevent.** It asks that `cmp` show the data file
  byte-for-byte unchanged after a report, and a report that rewrote the file with identical content
  would satisfy that. `verify` found this by adding `store.save` to `cmd_report` and watching every
  test still pass. The delivered behaviour is correct — `cmd_report` calls no writer, and the file's
  inode and mtime are unchanged after a report — but **the test suite will not catch a future change
  that starts writing**. Anyone touching `report` should check that by hand, or strengthen the
  criterion first.
- **Which settlement is printed when several are minimal** is ADR-0010's choice and no criterion
  constrains it; greedy can occasionally emit one payment more than a perfect solver would.
- **Behaviour with a very large group is unexamined** — every check used three or four people.
- **A hand-edited ledger naming a sharer who is not registered** would be reported rather than
  refused (ADR-0009 clause 5 says it cannot arise through the tool).
- **`argparse`'s usage wording is unchecked**; only its exit code 2 is fixed.
- **The report describes the ledger, not the settling-up.** After Cass pays Ana, it still says Cass
  owes Ana: recording a settlement is out of scope for EP-001, and this is the thing a real user is
  most likely to be surprised by.
