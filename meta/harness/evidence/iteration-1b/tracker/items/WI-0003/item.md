---
id: WI-0003
type: work-item
title: Show who owes whom
status: done
priority: high
epic: EP-001
branch: wi/WI-0003
outcome: delivered
created: "2026-08-21T18:38:55Z"
updated: "2026-08-21T20:19:02Z"
depends-on:
  - WI-0002
---

## Story

As a member of the group settling up, I want to ask the tool who owes whom and by how much, so
that we can square up without anyone re-deriving the arithmetic and disagreeing about it.

## Acceptance criteria

The subcommand is fixed by ADR-0006 and takes no arguments:

```
python3 -m expenses who-owes-whom
```

It prints **transfers**, one per line, in the form `<debtor> pays <creditor> <amount>` — for
example `Bob pays Alice 10.00`. Every amount carries exactly two decimal places (ADR-0003
point 2) and every person is shown with the spelling first entered for them (ADR-0005 point 4).

A person's **net position** is what they paid out less what they owe: the sum of the totals of
the expenses they paid, minus the sum of their shares of every expense they shared (ADR-0002,
ADR-0003). Positive means the group owes them.

The transfers are produced by the procedure ADR-0004 names when it justifies its promise:
repeatedly, the person with the largest debt pays the person owed the most, the smaller of the
two amounts; ties between equal positions are broken by the **identity key** of the name
(ADR-0005 point 3) in ascending order, so `alice` sorts before `Bob`. This is pinned here, rather
than left to the implementation, because without it no criterion about the output is decidable.

Every criterion below assumes `Alice`, `Bob`, `Carol` and `Sam Okafor` have been added with
`add-person`, and starts from a record with no expenses unless it says otherwise.

- [x] AC1 — With nothing recorded at all — no people and no expenses — `who-owes-whom` prints
  exactly `Everybody is settled up.` on standard output and exits `0`. Not an error, not silence.
- [x] AC2 — With people added but no expenses recorded, the same: exactly
  `Everybody is settled up.`, exit `0`.
- [x] AC3 — When the expenses happen to balance, the same again. After
  `add-expense 10 --paid-by Alice --shared-by Alice,Bob` and
  `add-expense 10 --paid-by Bob --shared-by Alice,Bob`, both net positions are zero and
  `who-owes-whom` prints exactly `Everybody is settled up.`, exit `0`.
- [x] AC4 — One creditor, two debtors. After
  `add-expense 30 --paid-by Alice --shared-by Alice,Bob,Carol`, `who-owes-whom` prints exactly:
  ```
  Bob pays Alice 10.00
  Carol pays Alice 10.00
  ```
  and exits `0`. Bob comes first because the two debts are equal and `bob` sorts before `carol`.
- [x] AC5 — An uneven split still settles exactly to the penny. After
  `add-expense 10 --paid-by Alice --shared-by Alice,Bob,Carol` — where the shares are 3.34, 3.33
  and 3.33 (ADR-0003 point 3) — `who-owes-whom` prints exactly:
  ```
  Bob pays Alice 3.33
  Carol pays Alice 3.33
  ```
  and exits `0`. Alice's net position is 6.66 and the two transfers come to 6.66; nothing is left
  over and nothing is rounded away.
- [x] AC6 — A transfer may name two people who never shared an expense, and that is correct, not a
  defect (ADR-0004 § *On strangers paying strangers*). After
  `add-expense 30 --paid-by Alice --shared-by Alice,Bob` and
  `add-expense 30 --paid-by Bob --shared-by Bob,Carol`, Bob's net position is zero and
  `who-owes-whom` prints exactly `Carol pays Alice 15.00` — a transfer between two people with no
  shared expense — and exits `0`.
- [x] AC7 — Paying every printed transfer leaves every person at exactly zero. Checked on AC5's
  record by hand: net positions are Alice `+6.66`, Bob `-3.33`, Carol `-3.33`; applying
  `Bob pays Alice 3.33` and `Carol pays Alice 3.33` gives `0.00` for all three. The sum of the
  amounts printed for each person, signed, equals that person's net position, for every criterion
  in this list that prints transfers.
- [x] AC8 — The number of transfers printed is at most one fewer than the number of people whose
  net position is not zero (ADR-0004 property 2). AC4: three non-zero positions, two transfers.
  AC5: three, two. AC6: two non-zero positions (Bob is zero), one transfer.
- [x] AC9 — The output is deterministic. Running `who-owes-whom` twice in succession on AC4's
  record produces byte-identical output both times, and a third run in a separate later invocation
  of the process produces the same again.
- [x] AC10 — `who-owes-whom` never modifies the record. With AC4's record in place, the bytes of
  the file named by `EXPENSES_FILE` are identical before and after running the command. Nothing
  derived is stored (ADR-0003 point 6).
- [x] AC11 — `python3 -m expenses who-owes-whom extra` prints `who-owes-whom takes no arguments.`
  on standard error, exits non-zero, and prints nothing on standard output (ADR-0006 rule 2).
  Standard error contains no line matching `Traceback (most recent call last)`.
- [x] AC12 — A person whose net position is zero is not named in the output at all. In AC6's
  record Bob is neither a debtor nor a creditor on any printed line.

## Out of scope

- Recording that a debt has been paid. That is WI-0004: this item computes who owes whom from the
  expenses that have been recorded, and WI-0004 adds payments as a second kind of record that the
  same calculation nets off. AC7's guarantee is stated over expenses alone here and WI-0004
  restates it over both.
- **A pairwise breakdown** — "Bob owes Alice 10 for the taxi and 5 for the pizza". The human chose
  the settling view over it (`Q-001`, ADR-0004), knowing that a printed line then cannot be traced
  back to the expense that caused it. ADR-0004 § *Consequences* records what to do if that turns
  out to bite: add the pairwise view behind a flag, as a new item.
- **Provably minimal settlement.** ADR-0004 is explicit that finding the smallest possible set of
  transfers is NP-hard and is not promised. AC8's `n - 1` bound is what is promised instead, and a
  group that finds an obviously smaller set has found a new item, not a defect.
- Any output format other than lines of text on standard output — no JSON, no table, no colour.
- Historical balances, or balances as of a chosen date (EP-001 `## Out of scope`).

## Notes

### What was decided, and by whom

`Q-001` on this item is answered by the human: "just tell us the fewest payments needed to settle
up — that's what actually happens at the end of a trip." That is **ADR-0004** — a settling set of
transfers, not netted pairwise debts — and the human is recorded as its decider, so superseding it
needs their authorisation.

**Read ADR-0004 before verifying this item.** It is deliberately careful about what "fewest"
means: the tool promises that the transfers settle everybody exactly, that there are at most
`n - 1` of them, and that the output is deterministic. It does not promise minimality, and a
transfer between two people who never shared an expense is expected — AC6 exists to say so in a
form `verify` can check.

**ADR-0003** makes AC7 an exact statement rather than an approximate one: every share is a whole
number of pennies and the shares of an expense sum to its total, so the net positions sum to zero
and a set of transfers that zeroes them leaves nothing over.

### Assumptions this refinement made without the human

The human answers asynchronously and was not present. Their one question on this item is answered
and propagated; what remained was output format and tie-breaking, which they have twice declined
to be asked about (`WI-0001/Q-001` and `Q-003`). Each is `[assumed]` in
`artifacts/refinement-qa.md`, and none was confirmed by them:

1. **The line format `<debtor> pays <creditor> <amount>`**, and the settled message
   `Everybody is settled up.` Exact text is what makes the criteria decidable.
2. **Ties are broken by identity key, ascending.** ADR-0004 property 3 requires ties to be broken
   "by the person's name" without saying how; comparing identity keys rather than raw spellings
   means the order does not depend on who typed a capital letter, which is the same reasoning
   ADR-0005 already applies to identity.
3. **The greedy procedure is pinned in the criteria.** ADR-0004 names it when justifying the
   `n - 1` bound, so this is pinning an existing decision rather than making one — but it does
   mean the criteria fix *which* valid settlement is printed, not merely that a valid one is.
   Without that, AC4 to AC6 could not name an expected output at all.
4. **`who-owes-whom` is read-only** (AC10). Nothing says so anywhere; it follows from ADR-0003
   point 6, and it is cheap to assert now and awkward to discover later.

### Left deliberately unconstrained (R10)

- **How the settlement is computed internally** — beyond the procedure the criteria pin — and
  where it lives in the code. `plan`'s to decide.
- **What happens when the record is corrupt.** `ADR-0007` point 5 already covers it for every
  subcommand and WI-0002 verified it; no criterion here repeats it.
- **Very large groups.** Nothing bounds the number of people or expenses, and no criterion names a
  time. The greedy procedure is O(n log n) in people per run and the product is for a friend
  group; if that ever stops being true it is a new item. Left so by `refine`.

### Accepted gaps, recorded at close (review-close, 2026-08-21)

Delivered as `delivered`. `artifacts/review.md` carries the Definition of Done table and four
findings; these are the gaps it accepted, repeated here because a gap that lives only in a report
is a gap that has been forgotten rather than accepted:

1. **A hand-edited record whose net positions do not sum to zero makes the tool say everybody is
   settled when somebody is not.** With a record holding one expense of 1.00 and two stated shares
   of 1.00 each — positions `Alice 0`, `Bob -1.00` — `who-owes-whom` prints
   `Everybody is settled up.` and exits `0`. The tool cannot produce such a record itself, because
   an expense's shares always sum to its total; `plan.md` § *Risks* deliberately left it unguarded
   and forbade `implement` from adding a check. Recorded with its real output so that anyone
   considering a validity check knows what it would buy.
2. **`net_positions`' ordering is a contract nothing asserts.** `plan.md` § *Assumptions* 1 says
   it returns everybody, in the order they were added; sorting the result by amount passes the
   whole suite. **WI-0004 extends this function** and should assert the ordering while it does.
3. **AC10's test uses a record with one expense**, so a rewrite that merely reorders the expense
   list would pass it — `verify` confirmed the same mutation does change the bytes on a
   two-expense record. The behaviour is correct: `_who_owes_whom` calls `load` and never `save`.
   **WI-0004 adds a third record-writing command** and should strengthen the fixture then.
4. **The `n - 1` bound is checked empirically** — 407 records — rather than proved. `ADR-0004`'s
   argument is sound and was re-derived against the loop during review.
5. **Getting the transfer amount wrong can hang rather than fail.** Rounding it down to 10p makes
   the settlement loop unable to reduce a position to zero. Anyone changing that line should know
   the failure mode is a test run that never ends.

