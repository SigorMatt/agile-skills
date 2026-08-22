# Plan — WI-0003 Show who owes whom

## Problem

The tool records who is in the group and what they have spent, and can print each sharer's share
of each expense. It cannot yet answer the question the group actually has at the end of a trip:
who hands money to whom, and how much. This item adds `who-owes-whom`, which derives every
person's net position from the recorded expenses and prints a set of transfers that settles
everybody.

Nothing here is open. `ADR-0004` records the human's choice of a settling set of transfers over a
pairwise breakdown, and is careful about what "fewest" promises: exact settlement, at most `n - 1`
transfers, and determinism — not provable minimality, which is NP-hard. `ADR-0003` makes "exact"
literal, because every share is a whole number of pennies and the shares of an expense sum to its
total, so the net positions sum to zero. `refine` then pinned the output format, the tie-break and
— this is the part to read first — **which** valid settlement is printed.

That last point is `refinement-qa.md` Q5 and it constrains this plan more than anything else: the
criteria name expected output for four worked examples, so they fix the procedure, not just its
properties. A different settlement algorithm is a change to this item's criteria and not only to
its code.

## Approach

No new module. `group.py` gains the two functions the overview has anticipated since v1 —
`net_positions` and `settle` — and `cli.py` gains one handler. Everything is derived from the
record on each run; nothing is written (`ADR-0003` point 6), which AC10 asserts directly.

The two functions are separate because they answer different questions and fail differently.
`net_positions` is arithmetic over the recorded expenses and is checkable against a hand
calculation; `settle` is a scheduling loop over those positions and is where the tie-break and the
`n - 1` bound live. Keeping them apart means AC7 (paying the transfers zeroes everybody) can be
tested against both halves independently.

## Steps

1. **Add `group.net_positions(record) -> list[(person, minor)]`.**
   - For each expense in `group.expenses(record)`: add its `total` to the payer's position, and
     subtract each sharer's share — taken from the existing `group.shares_of(expense)`, so the
     rounding rule is applied in exactly one place in the codebase.
   - Returns every person in the group, **in the order they were added**, including those at zero.
     Filtering is the caller's business; a function that silently dropped people would make AC12
     untestable from the outside.
   - Positions are whole minor units throughout (`ADR-0003` point 1). Their sum is zero for any
     record the tool itself wrote; nothing asserts that at runtime, and `## Risks` says why.

   Afterwards: on a record holding `add-expense 30 --paid-by Alice --shared-by Alice,Bob,Carol`,
   this returns `[("Alice", 2000), ("Bob", -1000), ("Carol", -1000)]`.

2. **Add `group.settle(record) -> list[(debtor, creditor, minor)]`.** The procedure the criteria
   pin, which is the one `ADR-0004` names when justifying its bound:
   - Start from `net_positions`, dropping everybody at zero.
   - While any position is non-zero: take the person with the **largest debt** and the person owed
     the **most**; emit a transfer from the first to the second for the smaller of the two
     magnitudes; reduce both positions by it. At least one of the two reaches zero each time,
     which is what bounds the output at `n - 1`.
   - **Ties are broken by identity key ascending** (`group.identity_key`, `ADR-0005` point 3), on
     both sides independently — so with equal debts, `bob` is chosen before `carol` regardless of
     how either name was typed.
   - Returns transfers in the order they were emitted.

   Afterwards: the four worked examples in AC3 to AC6 produce exactly the output those criteria
   name, checkable by hand before any code is written.

3. **Add `cli._who_owes_whom(arguments, out, err)` and register `who-owes-whom` in `COMMANDS`.**
   - Any argument → `who-owes-whom takes no arguments.` on standard error, non-zero exit
     (`ADR-0006` rule 2, AC11).
   - No transfers → exactly `Everybody is settled up.` on standard output, exit `0`.
   - Otherwise one line per transfer: `<debtor> pays <creditor> <amount>`, the amount through
     `money.format_amount`, the names as stored.
   - It calls `storage.load()` and never `storage.save()` (AC10).

   Afterwards: all twelve criteria are observable through `cli.main`, and the usage line for an
   unknown subcommand grows a fifth entry automatically.

4. **Write `tests/test_who_owes_whom.py`**, using the existing `ExpenseTestCase` from
   `tests/support.py` unchanged:
   - the three settled cases (AC1 needs a bare `CliTestCase`, since AC1 has no people);
   - the four worked examples, each asserting the exact expected stdout;
   - AC7 as a property over each of those records: for every person, the signed sum of the
     transfers they appear in equals their net position, and applying every transfer leaves all
     positions at zero;
   - AC8 as a count against `len([p for p in net_positions if p != 0])` on each record;
   - AC9 twice in process, and once as a subprocess in `tests/test_persistence.py`;
   - AC10 by comparing the record file's bytes before and after;
   - AC11 and AC12.

5. **Update `docs/architecture/overview.md` to v3** — `group.py` now owns the settlement, and the
   decisions table gains a row saying where the *normative* procedure lives, which is this item's
   criteria rather than an ADR. Bump the version and add a change-log row.

6. **Run the project's own commands**: `python3 -m unittest discover -s tests -t . -q` and
   `python3 -m compileall -q expenses tests`. Both must exit `0`, and WI-0001's and WI-0002's
   tests must still pass untouched.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — nothing recorded at all → `Everybody is settled up.`, exit 0 | 1, 3 | `tests/test_who_owes_whom.py`, a bare `CliTestCase` (no people): `run_cli("who-owes-whom")` returns `(0, "Everybody is settled up.\n", "")` |
| AC2 — people, no expenses → same | 1, 3 | same file, an `ExpenseTestCase` with no expense recorded |
| AC3 — expenses that balance → same | 1, 2, 3 | the two-expense record from the criterion; asserts the same triple |
| AC4 — one creditor, two debtors, Bob first on the tie | 2, 3 | asserts stdout is exactly `Bob pays Alice 10.00\nCarol pays Alice 10.00\n` |
| AC5 — uneven split settles to the penny | 1, 2, 3 | asserts stdout is exactly `Bob pays Alice 3.33\nCarol pays Alice 3.33\n`, and that Alice's net position is `666` |
| AC6 — a transfer between two people who never shared | 2, 3 | asserts stdout is exactly `Carol pays Alice 15.00\n` |
| AC7 — paying every transfer leaves everybody at zero | 1, 2 | a test that, for each of the AC4, AC5 and AC6 records, applies every printed transfer to `net_positions` and asserts all are zero afterwards — a property, not one hand-checked case |
| AC8 — at most `n - 1` transfers | 2 | the same three records: `len(settle(record)) <= len([p for p in net_positions(record) if p])- 1` |
| AC9 — deterministic | 2, 3 | two in-process runs compared byte for byte, plus a third as a subprocess in `tests/test_persistence.py` |
| AC10 — the record is never modified | 3 | the record file's bytes read before and after `who-owes-whom`, asserted equal |
| AC11 — an argument is refused | 3 | `run_cli("who-owes-whom", "extra")` → exit non-zero, stderr `who-owes-whom takes no arguments.\n`, stdout empty, no traceback |
| AC12 — a person at zero is not named | 2, 3 | on AC6's record, asserts `"Bob"` does not appear in stdout |

## Assumptions

1. **`net_positions` returns everybody, including people at zero, in the order they were added.**
   The alternative — filtering inside — would hide the zero case from every test that does not
   reach for the internals, and AC12 is exactly about the zero case. **Reversing it** is one
   `filter` moved between two functions in the same file.
2. **`settle` recomputes the largest debtor and creditor on each iteration** rather than sorting
   once and walking. With a friend group's handful of people the cost is irrelevant, and
   recomputing is the form in which the tie-break rule is obviously applied at every step.
   **Reversing it** — sorting once and using a two-pointer walk — is a rewrite of one function
   with the same signature and the same output.
3. **The settlement lives in `group.py`, not a new module.** `overview.md` has said so since v1.
   `group.py` reaches roughly 230 lines with this change, which is still one screen of concepts:
   identity, membership, shares, positions, settlement. **Reversing it** is a file move and an
   import change; no behaviour and no data depends on it.

## Decisions and ADRs

| decision | where |
|----------|-------|
| A settling set of transfers, not netted pairwise debts; what "fewest" does and does not promise | `ADR-0004`, cited, not re-decided — it is the human's, and superseding it needs their authorisation |
| Whole minor units; the payer-first remainder; nothing derived is stored | `ADR-0003`, cited |
| Which valid settlement is printed, the line format, and the tie-break | **WI-0003 `item.md` and `refinement-qa.md` Q5** — pinned by `refine`, not by an ADR, and deliberately so: Q5 records both the choice and its cost |
| Identity keys as the tie-break key | `ADR-0005` point 3 via the criteria |
| The subcommand name and the no-argument rule | `ADR-0006`, cited |
| `group.py` owns the settlement; `money.py` formats; nothing new is written | `docs/architecture/overview.md` v3 |
| Where zero-position people are filtered; iterative versus sorted selection | `## Assumptions` above |

**No new ADR.** Every decision this item forces is either already recorded or is a choice with no
alternative worth a document — and the one genuinely consequential choice, pinning the procedure,
was made by `refine` in the criteria and is recorded with its cost in `refinement-qa.md` Q5.
Writing an ADR that restated it would put the same decision in two places with no way to tell
which governs. The overview's decisions table instead gains a row pointing at the criteria, so a
future reader asking "may I change the settlement algorithm?" finds the answer where they look.

`tracker/project.yaml` already carries both commands from `ADR-0008`; nothing about them changes.

## Risks

- **Nothing asserts at runtime that the net positions sum to zero.** They do, for any record the
  tool wrote, because `shares_of` sums to each expense's total. For a **hand-edited** record they
  might not, and `settle` would then loop until one side ran out and emit a transfer set that does
  not settle anybody — silently. `ADR-0007` point 5's shape check does not catch it, because the
  file would be structurally valid. No criterion covers this, and adding a guard is not this
  item's to decide; `implement` should not add one on its own initiative, and if it wants to, that
  is a question for the architect.
- **The tie-break is the only thing making AC4 decidable**, and it is easy to implement as
  "sort by amount" and get the right answer by accident on the worked examples — Python's sort is
  stable, so an implementation that never compares names would still print `Bob` before `Carol`
  when they were added in that order. A test that adds `Carol` **before** `Bob` and still expects
  `Bob pays Alice` first is the one that distinguishes the two; step 4 should include it.
- **AC7 and AC8 are properties and it is tempting to test them on one record.** The mapping table
  asks for all three transfer-producing records, because a single-creditor case exercises neither
  the multi-creditor branch of the loop nor the case where a debtor's payment is split.
- **`who-owes-whom` is the first read-only command over expenses**, so it is the first place a
  stray `storage.save()` would be invisible — the file would be rewritten with identical content.
  AC10 compares bytes, which catches a rewrite only if the serialisation differs. It would not
  catch a byte-identical rewrite, and nothing does; the mitigation is that step 3 says the handler
  never calls `save`, and a reviewer reading eleven lines can confirm it.

## Out of scope for this item

- Payments between people (WI-0004). This item's net positions are derived from expenses alone;
  WI-0004 extends the same function and restates AC7 over both kinds of fact.
- A pairwise breakdown, any output format other than text, and provable minimality — all three are
  in the item's `## Out of scope`, and the first and third are `ADR-0004`'s explicit consequences.
- Any change to `add-person`, `people`, `add-expense` or `expenses`.
- Any guard against a hand-edited record whose positions do not sum to zero — see `## Risks`.
