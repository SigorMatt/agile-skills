---
id: WI-0002
type: work-item
title: Record an expense paid by one person and shared by several
status: done
priority: high
epic: EP-001
branch: wi/WI-0002
outcome: delivered
created: "2026-08-21T18:38:55Z"
updated: "2026-08-21T20:00:37Z"
depends-on:
  - WI-0001
---

## Story

As someone who has just paid for something on behalf of part of the group, I want to record what
it cost, who paid it, and who shared it, so that the cost is captured at the moment it happened
rather than reconstructed from memory later.

## Acceptance criteria

The two subcommands are fixed by ADR-0006. Their arguments are pinned here:

```
python3 -m expenses add-expense <total> --paid-by <name> --shared-by <name>[=<amount>][,<name>[=<amount>]]...
python3 -m expenses expenses
```

Both flags are required and each may be given at most once. An amount — the total or a stated
share — is written with at most two decimal places: `12`, `12.5` and `12.50` all mean the same
thing (ADR-0003 point 2). The comma separates sharers and the equals sign attaches a stated share
to one of them; neither may appear in a name, which is why ADR-0005 point 2 reserves them.

"Exits non-zero" means, throughout: a message on standard error, an exit status other than `0`,
nothing added to the record, and no Python traceback — standard error contains no line matching
`Traceback (most recent call last)`.

Every criterion below assumes `Alice`, `Bob`, `Carol` and `Sam Okafor` have already been added
with `add-person` (WI-0001), unless it says otherwise.

- [x] AC1 — `python3 -m expenses add-expense 30 --paid-by Alice --shared-by Alice,Bob,Carol`
  prints `Recorded 30.00 paid by Alice, shared by 3 people.` on standard output and exits `0`.
- [x] AC2 — Persistence: with the expense above recorded by one invocation, a separate, later
  invocation of `python3 -m expenses expenses` lists it. Nothing is re-entered.
- [x] AC3 — `python3 -m expenses expenses` prints one line per expense, in the order they were
  recorded, numbered from `1`, and exits `0`. After AC1 the single line is exactly:
  `1. 30.00 paid by Alice, shared by Alice 10.00, Bob 10.00, Carol 10.00`.
  Every amount carries exactly two decimal places (ADR-0003 point 2), and every person is shown
  with the spelling first entered for them (ADR-0005 point 4).
- [x] AC4 — `python3 -m expenses expenses` with nothing recorded prints exactly
  `No expenses have been recorded yet.` on standard output and exits `0` (ADR-0006 rule 2).
- [x] AC5 — Equal split is the default and needs no extra syntax (ADR-0002). With no `=` anywhere
  in `--shared-by`, the whole total is divided equally among the sharers named. A single sharer
  takes the whole total: `add-expense 12 --paid-by Alice --shared-by Bob` then `expenses` prints
  `1. 12.00 paid by Alice, shared by Bob 12.00`. The payer need not be a sharer, as here.
- [x] AC6 — Any subset of sharers may carry a stated share, and the remainder is split equally
  among the rest (ADR-0002). `add-expense 30 --paid-by Alice --shared-by Alice,Bob=6,Carol` then
  `expenses` prints `1. 30.00 paid by Alice, shared by Alice 12.00, Bob 6.00, Carol 12.00`. When
  the stated shares already come to the total and some sharer carries none, that sharer's share is
  `0.00` and is shown as such:
  `add-expense 10 --paid-by Alice --shared-by Alice=10,Bob` prints
  `1. 10.00 paid by Alice, shared by Alice 10.00, Bob 0.00`.
- [x] AC7 — An uneven division puts the odd pennies on the payer first, then on the remaining
  sharers in the order they were named, and the shares still sum to the total exactly (ADR-0003
  points 3 and 4):
  - `add-expense 10 --paid-by Alice --shared-by Alice,Bob,Carol` →
    `1. 10.00 paid by Alice, shared by Alice 3.34, Bob 3.33, Carol 3.33`;
  - with a payer who is not a sharer,
    `add-expense 10 --paid-by "Sam Okafor" --shared-by Alice,Bob,Carol` →
    `1. 10.00 paid by Sam Okafor, shared by Alice 3.34, Bob 3.33, Carol 3.33`;
  - the same order applies to the remainder in the mixed form, where only the sharers without a
    stated share divide it: `add-expense 10.01 --paid-by Bob --shared-by Alice,Bob,Carol=1` →
    `1. 10.01 paid by Bob, shared by Alice 4.50, Bob 4.51, Carol 1.00` — 9.01 is left after
    Carol's stated 1.00, and the odd penny goes to Bob because he is the payer, even though Alice
    was named first.
- [x] AC8 — A name that is not in the group is refused, and identity keys decide membership
  (ADR-0005 point 5):
  - `add-expense 30 --paid-by Dave --shared-by Alice,Bob` prints `Dave is not in the group.` on
    standard error and exits non-zero; `expenses` afterwards prints the empty-list message, and
    `people` does not list `Dave` — neither the person nor the expense is created;
  - `add-expense 30 --paid-by "sam okafor" --shared-by Alice,Bob` **succeeds**, and `expenses`
    shows the payer as `Sam Okafor`.
- [x] AC9 — A malformed or out-of-range amount is refused, and nothing is recorded:
  - `add-expense twelve --paid-by Alice --shared-by Bob` → `twelve is not an amount.`;
  - `add-expense 12.505 --paid-by Alice --shared-by Bob` →
    `Amounts have at most two decimal places: 12.505.`;
  - `add-expense 0 --paid-by Alice --shared-by Bob` and `add-expense -5 …` →
    `An expense must be for more than zero.`;
  - `add-expense 30 --paid-by Alice --shared-by Alice=-5,Bob` →
    `A stated share cannot be negative: Alice=-5.`;
  - `add-expense 30 --paid-by Alice --shared-by Alice=1.005,Bob` →
    `Amounts have at most two decimal places: 1.005.`.
- [x] AC10 — Stated shares that cannot work are refused (ADR-0002):
  - over the total — `add-expense 10 --paid-by Alice --shared-by Alice=6,Bob=7` →
    `The stated shares come to 13.00, which is more than the total of 10.00.`;
  - under the total with every sharer stated — `add-expense 10 --paid-by Alice --shared-by
    Alice=2,Bob=3` → `The stated shares come to 5.00, which is less than the total of 10.00, and
    every sharer has a stated share.`;
  - equal to the total with every sharer stated is **accepted**: `add-expense 10 --paid-by Alice
    --shared-by Alice=4,Bob=6` exits `0`.
- [x] AC11 — A malformed sharer list is refused:
  - `--shared-by ""` → `--shared-by needs at least one name.`;
  - `--shared-by Alice,,Bob` → `A name cannot be empty.`;
  - `--shared-by Alice,Bob=` → `Bob= has no amount after the equals sign.`;
  - `--shared-by Alice=1=2,Bob` → `Alice=1=2 has more than one equals sign.`;
  - `--shared-by Alice,alice` and `--shared-by Alice,ALICE` → `Alice is named twice in
    --shared-by.` — the same person may not be listed twice, and sameness is the identity key of
    ADR-0005 point 3, not the spelling.
- [x] AC12 — The command line itself is checked, and each failure exits non-zero with a message on
  standard error:
  - `add-expense --paid-by Alice --shared-by Bob` — no total — → `add-expense needs a total.`;
  - `add-expense 30 --shared-by Bob` → `add-expense needs --paid-by.`;
  - `add-expense 30 --paid-by Alice` → `add-expense needs --shared-by.`;
  - `add-expense 30 --paid-by Alice --paid-by Bob --shared-by Carol` →
    `--paid-by was given more than once.`;
  - `add-expense 30 --paid-by Alice --shared-by Bob --split-by Carol` →
    `Unknown option: --split-by.`;
  - `expenses extra` → `expenses takes no arguments.` (ADR-0006 rule 2).
- [x] AC13 — Every refusal in AC8 to AC12 records nothing: after any of them, `expenses` prints
  exactly what it printed before, and standard error carries no
  `Traceback (most recent call last)`.
- [x] AC14 — Adding an expense does not disturb what WI-0001 recorded: after AC1,
  `python3 -m expenses people` still prints `Alice`, `Bob`, `Carol` and `Sam Okafor` in the order
  they were added, and exits `0`.

## Out of scope

- Computing or displaying balances, or who owes whom; that is WI-0003.
- Editing or deleting an expense once recorded (see EP-001 `## Out of scope`).
- **What an expense was for.** There is no description, label, note, category, tag or date on an
  expense. `docs/product/prd.md` (v2) § *The facts the tool holds* enumerates an expense as an
  amount, one payer and one or more sharers, and item 4 of that list says "Nothing else". A reader
  would reasonably expect to be able to type `--for "dinner"`, and they cannot; the consequence is
  that `expenses` output distinguishes two expenses only by their number, amount and people. This
  is a product decision recorded in the PRD, not a decision taken here.
- Attachments, receipts, currencies other than the single unnamed one, and any per-expense
  exchange rate (`prd.md` v2 § *Constraints*).
- Removing or renaming a person, which WI-0001 already excludes and which would be the only way to
  repair an expense recorded against the wrong person.

## Notes

### What was decided, and by whom

Both of this item's questions are answered.

`Q-001` — the human requires equal and unequal splits both to work: "usually equal, but sometimes
someone only had part of it and wants to put in a different amount". The shape of that is
**ADR-0002**: any subset of sharers may carry a stated share, and the remainder is split equally
among the rest. AC5, AC6 and AC10 are that decision.

`Q-002` — the human deferred the rounding rule ("not sure yet — go ahead anyway, we'll decide
later"). It is decided as **ADR-0003**: money is whole minor units, amounts carry at most two
decimal places, and the odd pennies of an uneven division go to the payer first. AC7 is that rule.
ADR-0003 keeps shares derived rather than stored precisely so the group can still change its mind
without invalidating anything already recorded.

**ADR-0001** fixes the invocation, exit-code and stream contract; **ADR-0006** fixes the two
subcommand names; **ADR-0005** fixes who a named person is and reserves `,` and `=`, which is what
makes the `--shared-by Alice,Bob=6,Carol` form possible at all.

### Assumptions this refinement made without the human

The human answers asynchronously and was not present. Nothing here needed them: both of their
answers were already on file, and what remained was syntax and wording, which they have twice
declined to be asked about (`WI-0001/Q-001` and `Q-003`, both "whatever you think is best"). Each
is recorded `[assumed]` in `artifacts/refinement-qa.md` and none was confirmed by them:

1. **The argument shape** — a positional total, then `--paid-by` and `--shared-by`, both required.
   The alternative considered was making `--shared-by` optional and defaulting to everybody in the
   group, which the original idea ("shared by some or all") would have supported. Rejected because
   a default that silently includes a person is the kind of mistake this epic cannot repair: there
   is no command to edit or delete an expense.
2. **The exact wording of every message**, and the exact shape of a listed line
   (`1. 30.00 paid by Alice, shared by Alice 10.00, Bob 10.00, Carol 10.00`). Exact text is what
   makes the criteria decidable by someone with no context; the wording is cosmetic.
3. **Expenses are numbered from 1 in the order recorded**, in the listing only. The numbers are
   not identifiers — nothing accepts one as an argument, because nothing edits or deletes an
   expense.
4. **The same person may not appear twice in `--shared-by`** (AC11). Both alternatives — silently
   merging the two entries, or letting somebody carry two shares — decide an arithmetic question
   nobody asked, and a refusal is the only option that cannot be silently wrong.

If the human contradicts any of these, each is a small change to this item and its implementation.

### Left deliberately unconstrained (R10)

- **Where and how an expense is stored.** `ADR-0007` already decides the file and its format, and
  point 2 of it makes adding an `expenses` key free; the exact JSON shape of one expense is
  `plan`'s to choose. Left so by `refine`.
- **The behaviour when a write fails** — an unwritable directory or a full disk — is still
  undecided across the whole project. WI-0001's review closed with this as an accepted gap and
  named this item's `plan` execution as where it should be settled, because `storage.save` is
  inherited unchanged. It is not an acceptance criterion here; it is a decision `plan` owes.
- **Whether `expenses` output is stable under a future change to the rounding rule.** ADR-0003
  point 5 makes shares derived rather than stored, so changing the rule changes this listing for
  past expenses too. That is intended, and no criterion pins the old output.

### Accepted gaps, recorded at close (review-close, 2026-08-21)

Delivered as `delivered`. `artifacts/review.md` carries the Definition of Done table and five
findings; these are the gaps it accepted, repeated here because a gap that lives only in a report
is a gap that has been forgotten rather than accepted:

1. **`ADR-0010`'s write-failure message satisfies no criterion on this item.** With the target
   directory unwritable, `add-expense` prints `Cannot save to <path>: Permission denied.` and
   exits non-zero — the gap WI-0001's review handed to this item's planning, now closed in code.
   `plan` may not write criteria, so it has none; `implement` and `verify` both exercised it.
2. **Two command-line behaviours have no criterion**: `--paid-by` with no value gives
   `--paid-by needs a value.`, and `add-expense 30 40 …` gives `add-expense takes a single
   total.` Both refuse sensibly; neither is pinned.
3. **"A refusal creates no record file" is pinned for `add-person` but not for `add-expense`.**
   The behaviour is correct today and `verify` checked it, but two of its fifteen mutations
   survived precisely because nothing asserts it. **WI-0004's refinement should pin it**, since
   `add-payment` is the third command that writes.
4. **`shared by 1 people.`** — the confirmation line says "1 people" when an expense has one
   sharer. AC1 pins that sentence only for its three-sharer case, so nothing is violated. The next
   `refine` execution to touch a confirmation message should pin the plural.
5. **Two rules that must agree are written twice**: `group.RESERVED_CHARACTERS` is the tuple a
   name is checked against, while `cli._split_sharers` splits on the same two characters as
   control flow. Reserving a third character would change one and not the other.

