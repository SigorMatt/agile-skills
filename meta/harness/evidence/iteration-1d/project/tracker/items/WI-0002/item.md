---
id: WI-0002
type: work-item
title: Show who owes whom across all recorded expenses
status: done
priority: high
epic: EP-001
created: "2026-08-22T01:34:55Z"
depends-on:
  - WI-0001
updated: "2026-08-22T03:27:00Z"
branch: wi/WI-0002
outcome: delivered
---

## Story

As a member of a friend group with a pile of shared expenses recorded, I want to ask the tool
who owes whom, so that we can settle up without anyone reconstructing the arithmetic by hand.

## Acceptance criteria

Throughout, "the report" means `python3 -m expenses debts`, and a *ledger* is described by the
`add-person`, `add-expense` and `repay` commands that build it (`docs/architecture/overview.md`).
Amounts print as plain two-decimal numbers (`WI-0001` AC6). "A pair's balance" means everything
one of two people owes the other across all expenses and repayments between exactly those two,
netted against each other, computed as `ADR-0006` sets out.

- [x] AC1 — `python3 -m expenses debts` prints one line per pair of people whose balance is not
      zero, in the form `<debtor> owes <creditor> <amount>`, and exits 0. Names print in the form
      first typed (`WI-0001` AC1); the amount is the pair's balance, always positive
- [x] AC2 — worked example, exact output. On a ledger built by: `add-person Ana`,
      `add-person Ben`, `add-person Cara`; `add-expense --payer Ana --amount 30.00
      --description dinner --shared-by Ana --shared-by Ben --shared-by Cara`;
      `add-expense --payer Ben --amount 12.00 --description taxi --shared-by Ben
      --shared-by Cara` — the report prints exactly these three lines, in this order:

      ```
      Ben owes Ana 10.00
      Cara owes Ana 10.00
      Cara owes Ben 6.00
      ```

- [x] AC3 — the report accounts for every recorded minor unit exactly. For each person P, the sum
      of the amounts on lines where P is the debtor minus the sum where P is the creditor equals
      P's net position, computed independently from the ledger as: (the sum of P's shares of the
      expenses P shared in, by `ADR-0002`'s rule) − (the sum of the totals of the expenses P
      paid) + (repayments P received) − (repayments P made). Across all people these net
      positions sum to zero. This is an exact equality, not a tolerance (`ADR-0004`)
- [x] AC4 — when **no pair has a non-zero balance** — no people, or people with no expenses and
      no repayments, or every pair squared up — the report prints exactly `Nobody owes anybody.`
      and exits 0, rather than printing nothing. Note that "every person's net position is zero"
      is **not** the same condition and must not be used: a circle of debts has every net
      position zero and still prints lines (AC8)
- [x] AC5 — the output is ordered by debtor, then by creditor, comparing names as
      `name.strip().casefold()` (`WI-0001` AC1), so running the report twice over unchanged data
      prints the same lines in the same order
- [x] AC6 — repayments net off, worked example. Continuing AC2's ledger with
      `repay --from Ben --to Ana --amount 10.00` and `repay --from Cara --to Ana --amount 12.00`
      — Cara's repayment exceeds the 10.00 she owed Ana — the report prints exactly:

      ```
      Ana owes Cara 2.00
      Cara owes Ben 6.00
      ```

      The pair Ben/Ana is square and produces no line; the pair Cara/Ana has reversed direction
- [x] AC7 — after every debt has been repaid the report prints `Nobody owes anybody.` per AC4,
      never a line with amount `0.00`
- [x] AC8 — a circle is printed, not collapsed. On a ledger of Ana, Ben, Cara with
      `--payer Ana --amount 20.00 --shared-by Ana --shared-by Ben`,
      `--payer Ben --amount 20.00 --shared-by Ben --shared-by Cara` and
      `--payer Cara --amount 20.00 --shared-by Cara --shared-by Ana`, the report prints exactly:

      ```
      Ana owes Cara 10.00
      Ben owes Ana 10.00
      Cara owes Ben 10.00
      ```

      Every net position here is zero and three lines are still printed (`ADR-0006`)
- [x] AC9 — a remainder that does not divide evenly stays with the payer. On a ledger of Ana, Ben,
      Cara with `--payer Ana --amount 10.00 --shared-by Ana --shared-by Ben --shared-by Cara`,
      the report prints exactly `Ben owes Ana 3.33` and `Cara owes Ana 3.33` — 6.66 in total, the
      remaining 3.34 being Ana's own share (`ADR-0002`)
- [x] AC10 — a repayment between two people who share no expense prints the debt the other way
      round. On a ledger of Ana and Ben with no expenses and `repay --from Ana --to Ben
      --amount 5.00`, the report prints exactly `Ben owes Ana 5.00`
- [x] AC11 — a recorded person who has neither paid for nor shared in anything, and has made and
      received no repayment, produces no line and does not prevent AC4's `Nobody owes anybody.`
      On a ledger of Ana, Ben and Cara with no expenses and no repayments, the report prints
      exactly `Nobody owes anybody.` and exits 0

## Out of scope

- Recording a repayment; the command that does that, and its storage, are WI-0001 (AC7, AC8).
  This item consumes what WI-0001 records.
- Any output format other than the one this item settles on — no CSV, JSON or export.
- Filtering the report by date, person or description.
- **Suggesting how to settle up in the fewest transfers.** That is the option the stakeholder
  rejected on `Q-001` (`ADR-0006`). If it is ever wanted it is a separate command over the same
  data, not a change to this one.
- **A per-person summary or totals line.** The report prints debt lines and nothing else.
- **Explaining a line** — no breakdown of which expenses make up an amount. The traceability the
  stakeholder asked for is that a line *can* be reconciled against `python3 -m expenses expenses`
  by hand, not that the tool does it for them.

## Notes

`refine` must settle before this item is Ready:

- ~~Whether the report is the raw pairwise ledger or a **minimised** set of transfers.~~
  **Settled 2026-08-22T02:48:51Z.** The stakeholder answered `Q-001`: the **pairwise** ledger.
  `ADR-0006` records the decision, their reason (any line must trace back to what those two
  people actually shared) and the five computation steps. AC1 above now says so.
- How rounding is *presented*. The rounding **rule** is now settled: `ADR-0002` fixes that an
  expense is split equally and that the payer absorbs the remainder, so each non-payer sharer owes
  the total divided by the number of sharers rounded down to the minor unit, and the payer carries
  the rest. That gives AC2 a property that can actually be tested — the shares of any one expense
  sum to its recorded total exactly. What `refine` must still settle is how the *printed* debts
  relate to those net positions when the report aggregates across expenses, and whether the
  printed lines are required to sum to the net positions to the last minor unit.
- AC5 and AC6 were added by `answer-questions` when the stakeholder answered `EP-001/Q-003`
  ("let us log that someone paid, so the report doesn't go stale"). `ADR-0001` records why
  repayments became two criteria on existing items rather than a fourth work item. `refine` must
  still settle how a repayment that overshoots the debt is presented, and whether the report
  distinguishes "settled" from "never owed anything".

### Settled inputs from WI-0001's refinement, 2026-08-22T01:55:49Z

The stakeholder answered five questions on WI-0001 and `answer-questions` propagated them. Four
of the answers reach this item's arithmetic and are recorded here so that `refine` and `plan` do
not re-derive them:

- **Splits are equal.** No per-person share is ever entered or stored (`WI-0001/Q-001`,
  `WI-0001` AC5), so this item computes each sharer's share rather than reading one.
- **The payer absorbs the rounding remainder** (`WI-0001/Q-002`, `ADR-0002`). This is applied
  here, not in WI-0001: WI-0001 stores an expense's total and its sharers only.
- **Amounts are plain two-decimal numbers** (`WI-0001` AC6), which fixes what an amount printed
  by this report should look like.
- **Every expense and every repayment carries a date** (`WI-0001` AC7, AC11). This item does not
  filter or sort by date — that stays out of scope — but the field exists, so a later filtering
  item would not need a migration.

### Definition of Ready, as assessed by `refine` at 2026-08-22T02:39:45Z

**Not Ready.** R1, R2, R3, R5, R7, R8 and R9 pass or became satisfiable during this execution;
**R4 fails on AC1, AC2, AC4, AC5 and AC6**, and **R10 fails**, for one reason: nobody has said
whether the report is the **pairwise** set of debts or the **minimised** set of transfers that
clears the same net positions. `Q-001` puts that to the stakeholder with a worked three-person
example. The item is suspended at `awaiting-answer` with `resume-to: draft` and the acceptance
criteria above are **unchanged** — none was rewritten on a guess, because the choice cascades
into five of the six. `artifacts/refinement-qa.md` carries the round and, deliberately, no answer.

The per-criterion record is in this execution's journal entry under `**Gates:**`.

### Six decisions taken by `refine` and not put to the stakeholder

These close the parts of this item's `## Notes` that did **not** need the stakeholder. Each is
presentation, or a property that holds identically whichever option `Q-001` selects; each is
reversible until `implement` writes code. They are listed here, not only in the Q&A, because
`answer-questions`, `plan`, `implement` and `verify` inherit them.

| # | assumed | why not asked |
|---|---------|---------------|
| 1 | The printed debts account for every recorded cent exactly: the printed amounts sum, per person, to that person's net position, with no minor unit invented or lost | AC2's balance property made exact. `ADR-0004` holds money as integer minor units, so this is free under either option and a test can assert equality rather than a tolerance. This is the second bullet of the list above — how rounding is *presented* — now settled. |
| 2 | Only non-zero debts are printed; a squared-up pair produces no line | AC3 and AC6 already require it; this states it as a rule. |
| 3 | The report does not distinguish "settled — was owed, now repaid" from "never owed anything"; both produce no line | Listed above as something `refine` must settle. It is presentation, it follows from 2, and a "settled" line added later changes one print statement and no data. |
| 4 | Lines are ordered by debtor name, then creditor name, compared under WI-0001 AC1's rule (trimmed, ignoring case) | AC4 demands a deterministic order and names none. Sorting by name stays stable when an expense is inserted; recording order does not. |
| 5 | The report prints debt lines only — no per-person net summary, no totals | AC1 fixes the form and `## Out of scope` already excludes other formats. |
| 6 | A recorded person involved in nothing contributes no line, and does not prevent AC3's "nobody owes anybody" | The boundary case `verify` would otherwise have to invent. Follows from 2. |

The third bullet of the list above — how a repayment that **overshoots** a debt is presented — is
already answered by AC5 as written ("once it exceeds that, turns into B owing A") together with
assumptions 1 and 2, under either option. It needed no question.

### R10 — the combinations this item introduces, and where each is settled

**Re-stated against the criteria as they now read, 2026-08-22T02:56:51Z.** The AC numbers below
are the new ones; the old-to-new map is in the section after this one.

| combination | where |
|-------------|-------|
| report × no people recorded | AC4 — `Nobody owes anybody.`, exit 0 |
| report × people recorded but no expenses | AC4, and AC11 as a worked example |
| report × an expense whose payer is not among its sharers | AC3's net-position formula covers it: the payer is owed the whole total, since they have no share of it (`ADR-0002`, `ADR-0004`) |
| report × an amount that does not divide evenly | AC9 — worked example, 10.00 among three, payer keeps the 3.34 |
| report × a repayment smaller than the debt | AC6 — Cara's pair with Ben is untouched by her repayment to Ana |
| report × a repayment equal to the debt | AC6 — the Ben/Ana pair is square and prints no line |
| report × a repayment larger than the debt | AC6 — the Cara/Ana pair reverses direction |
| report × every debt repaid | AC7 — `Nobody owes anybody.`, never a `0.00` line |
| report × a repayment between two people who share no expense | AC10 — worked example, prints the debt the other way round (`ADR-0006`) |
| report × a circular set of debts (A owes B owes C owes A) | AC8 — the circle is **printed**; every net position is zero and three lines still appear (`ADR-0006`) |
| report × a person recorded who is involved in nothing | AC11 — no line, and it does not suppress AC4 |
| report run twice over unchanged data | AC5 — ordered by debtor then creditor under the trimmed, case-folded comparison |
| report × an unreadable or missing data location | WI-0001 AC9 already fixes this for every command; this item adds nothing to it, and it is not restated here |
| report × the `--file` option | WI-0001 AC9; `--file` is global and must precede the subcommand (`docs/architecture/overview.md`). This item introduces no option of its own, which is why the combination table is short |

### `Q-001` answered by the stakeholder, propagated 2026-08-22T02:48:51Z

The stakeholder chose **option A — the pairwise ledger** [src: WI-0002/Q-001]:

> "A — I want the pairwise breakdown. If the number ever gets questioned I want it to trace
> straight back to what those two people actually shared, not to some clever routing through
> somebody else's taxi. Fewer transfers doesn't matter as much as nobody being able to argue
> about a line."

`answer-questions` recorded it as `ADR-0006`, amended **AC1** above to state the pairwise rule
(legitimate here: the item is at `draft`, so criteria are not yet frozen), and settled the two
`Q-001`-dependent rows of the R10 table. AC2, AC3, AC4, AC5 and AC6 were **not** rewritten — the
answer makes each of them decidable as written, and sharpening their wording is the next `refine`
execution's job together with the R4 and R10 verdict. The six decisions `refine` took without
asking are unaffected: every one of them was chosen to hold under either option.

The item returns to `draft` with no blocking question open.

### Definition of Ready, as assessed by `refine` at 2026-08-22T02:56:51Z

**Ready.** No override was recorded; nothing was waived. Per-criterion:

| # | verdict | evidence |
|---|---------|----------|
| R1 | pass | frontmatter complete; `type: work-item`, `epic: EP-001`, `priority: high` |
| R2 | pass | `## Story` names the role (a member of a friend group), the capability (ask the tool who owes whom) and the outcome ("so that we can settle up without anyone reconstructing the arithmetic by hand") |
| R3 | pass | eleven criteria, `AC1`–`AC11`, each a checkbox |
| R4 | **pass, after a rewrite of all six inherited criteria.** Every criterion now names a command to run and an output to inspect. Four carry a complete ledger and its exact expected stdout (AC2, AC6, AC8, AC9, AC10, AC11); AC3 states an arithmetic identity computable from the ledger by hand; AC5 names the comparison function. No criterion contains an adjective without a threshold |
| R5 | pass | six exclusions, three of them added by this execution — minimised settlement, per-person summary, per-line explanation — each being something a reader could reasonably assume is included |
| R6 | pass | `Q-001` is `answered`; no open question on this item |
| R7 | pass | `depends-on: WI-0001`, which is `done` |
| R8 | pass | `artifacts/refinement-qa.md` records both rounds, with `[human]`, `[assumed]` and `[refine]` tags |
| R9 | pass | one command, over data that already exists, with no new storage and no new option. One coherent change |
| R10 | pass | the table above: fourteen combinations, every one landing on a criterion, an ADR or an explicit "not restated here" |

### The criteria were renumbered — old to new

The six inherited criteria became eleven. Nothing was dropped; the boundary cases that were
previously only *assumptions* in this section became criteria of their own, which is what R4
demanded of them.

| was | is now | what changed |
|-----|--------|--------------|
| AC1 — "a set of debts" | AC1 + AC2 | the pairwise rule (`ADR-0006`) plus a worked example with exact expected output |
| AC2 — "the debts balance" | AC3 | the identity is now written out and computable by hand, per person and in total |
| AC3 — "nobody owes anybody" | AC4 + AC11 | the trigger condition was **corrected** (see below) and the exact string fixed as `Nobody owes anybody.` |
| AC4 — "deterministic output" | AC5 | the order is now named — debtor, then creditor, compared as `name.strip().casefold()` |
| AC5 — "repayments net off" | AC6 | one worked example covering a repayment smaller than, equal to and larger than the debt |
| AC6 — "no zero-amount debts once repaid" | AC7 | unchanged in meaning; now points at AC4's exact string |
| — | AC8, AC9, AC10 | the circle, the uneven split and the repayment between strangers: three of `refine`'s earlier assumptions and two of the R10 rows `Q-001` settled, promoted into criteria with worked examples |

**One inherited criterion was wrong, and the pairwise answer is what exposed it.** Old AC3 said
the report says "nobody owes anybody" when "every person's net position is zero". Under a
minimised settlement those two conditions coincide. Under the pairwise report chosen on `Q-001`
they do not: a circle of debts has every net position zero and must still print its lines. Had
AC3 been carried forward unchanged, AC3 and the pairwise rule would have contradicted each other
on exactly the case `ADR-0006` calls out, and `verify` would have had to choose between two
criteria. AC4 now triggers on "no pair has a non-zero balance", and AC8 pins the circle down with
a worked example. This correction was made by `refine`, not by the stakeholder; it changes no
behaviour they asked for, and it is the reason the criteria were renumbered rather than edited in
place.

### Decisions taken by `refine` in this execution and not put to the stakeholder

Three, all reversible, all recorded here rather than only in the Q&A:

| # | decided | why not asked |
|---|---------|---------------|
| 1 | The command is `debts` — `python3 -m expenses debts` | R4 cannot pass without naming the command a reader would type. The existing commands are `people`, `expenses`, `repayments` — plural nouns for listings — and `debts` is the same word the stakeholder's own question used. Renaming it later is one line of `argparse` |
| 2 | The empty-report line is exactly `Nobody owes anybody.` | AC4 requires an exact string or it is not decidable. It matches the shape of the messages WI-0001 already prints — `No people recorded.`, `No expenses recorded.` — and reuses the wording already in AC3 and AC6 as `intake` and `answer-questions` wrote them. The stakeholder has not used this phrase themselves; it is `refine`'s wording, which is why it is listed here as a decision rather than as recorded intent |
| 3 | AC4's trigger is "no pair has a non-zero balance", not "every net position is zero" | Correcting a contradiction between two criteria is `refine`'s job, not the stakeholder's. The distinction is invisible unless a circle exists, and it changes nothing they asked for |

### Accepted gaps, recorded by `review-close` at 2026-08-22T03:23:54Z

The item was accepted and closed with these five gaps open. They are written here rather than
only in `artifacts/review.md`, because once an item is `done` nobody reads its reports again.

1. **`expenses/debts.py`'s module docstring says "raises nothing — every ledger the store can load
   has a debt report".** It does not: a hand-edited ledger whose `amount_minor` is a JSON string
   loads and then raises `TypeError` out of `share = expense.amount_minor // len(expense.sharers)`.
   `docs/architecture/overview.md` v6 carries the correction; the docstring was left because
   changing source after verification would send the item back to `verifying` for one sentence.
   Whoever next opens `debts.py` should fix it in the same commit.
2. **`expenses/cli.py`'s module docstring still says the module is "the only one that exits".**
   False since `main` returns an `int`; inherited from WI-0001, corrected in the overview at v3,
   flagged by `implement` and `verify` here. Same treatment, same instruction.
3. **The underlying robustness defect has no bug item.** A ledger whose recorded values are the
   wrong type loads without a `StoreError` and crashes the `debts`, `expenses` and `repayments`
   commands with a traceback, though `store.py` documents refusing a mis-shaped file. It belongs
   to WI-0001, not here. `review-close` could not file it: `pipeline.yaml` allows only `verify` to
   create an item at `ready` and only `intake` at `draft`. See `artifacts/review.md` finding F2.
4. **Scale and the default ledger location are unverified for `debts`** — thirteen small ledgers,
   all driven through `--file`. No criterion states a size, and the default path is WI-0001 AC9's.
5. **Concurrency and terminal rendering were not tested.** No criterion mentions either.
