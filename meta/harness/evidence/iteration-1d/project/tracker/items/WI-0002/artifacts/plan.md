# Plan — WI-0002 Show who owes whom across all recorded expenses

## Problem

Add one read-only command, `python3 -m expenses debts`, that turns the ledger WI-0001 records
into the list of debts between pairs of people. It changes nothing on disk, it takes no options
of its own, and it prints one line per pair whose balance is not zero, or a single
`Nobody owes anybody.` when no pair has one [src: WI-0002 AC1; WI-0002 AC4].

The arithmetic is already decided and this item does not reopen it. Each sharer of an expense
owes the payer the total divided by the number of sharers, rounded down to the minor unit, with
the payer absorbing the remainder (`ADR-0002`, `ADR-0004`); money is integer minor units
throughout (`ADR-0004`); the report is the **pairwise** ledger the stakeholder chose, netted per
pair and never re-routed between pairs, so a circle of debts is printed rather than collapsed
(`ADR-0006`). Names are compared trimmed and case-folded and printed in the form first typed
[src: WI-0001 AC1]; amounts print as plain two-decimal numbers [src: WI-0001 AC6].

Eleven acceptance criteria constrain it. Six of them are worked ledgers with exact expected
stdout, which makes most of this item a matter of getting the arithmetic and the ordering right
rather than deciding anything.

## Approach

`ADR-0008` puts the computation in a new module, `expenses/debts.py`, as a pure function from a
`Ledger` to an ordered list of `Debt` records, and leaves `cli.py` doing nothing but printing
what it returns. That is the one structural decision this item makes; everything else follows
`ADR-0006`'s five steps.

The computation is a single pass with one accumulator. For each unordered pair of people, keyed
by their two normalised names in sorted order, hold **one signed integer**: how many minor units
the second of the pair owes the first. Netting a pair is then addition, not a reconciliation step
afterwards, and the direction of a line is the sign at the end. This is the shape that makes
AC6's reversal (`Cara owes Ana 10.00` becoming `Ana owes Cara 2.00` after a 12.00 repayment) fall
out of the arithmetic rather than out of a special case, and it makes AC7's "never a `0.00` line"
a single `if net == 0: continue`.

Two things deliberately stay out of the accumulator. Nothing is ever moved between pairs, which
is what makes the report pairwise and the circle in AC8 printable (`ADR-0006`). And no per-person
total is computed anywhere in the code — AC3's net positions are an identity that the *tests*
compute independently from the ledger, which is the only way that criterion is worth checking
[src: WI-0002 AC3].

### The interface this item delivers

```
python3 -m expenses [--file PATH] debts
```

No options of its own. `--file` is global and must precede the subcommand, as for every other
command [src: docs/architecture/overview.md]. Exit 0 on success; the two existing failure modes
are unchanged and belong to `main` — a ledger that cannot be read is exit 1, `argparse` handles
usage errors with exit 2 [src: expenses/cli.py].

### `expenses/debts.py`, in signatures

```python
@dataclass(frozen=True)
class Debt:
    debtor: str        # display form
    creditor: str      # display form
    amount_minor: int  # always > 0

def debts(ledger: Ledger) -> list[Debt]: ...
```

`debts` returns the lines in printing order. An empty list is the AC4 condition.

## Steps

Each step ends with something observable, and the tests for a step come with it.

1. **`expenses/debts.py` — the computation.** New module, importing `Ledger` and
   `normalise_name` from `expenses.model` and nothing else from the package (`ADR-0008`). Define
   `Debt` as above and `debts(ledger)` as:

   1. Build `display`, a mapping from normalised name to display form, from `ledger.people` in
      order. When a name on an expense or a repayment is not among `ledger.people` — reachable
      only in a hand-edited ledger, since every command resolves names through `find_person`
      first [src: expenses/cli.py] — fall back to the form recorded on that record, first
      occurrence winning. This is what implements "printed in the form first typed"
      [src: WI-0001 AC1].
   2. Build `net`, a `dict` from a key `(lo, hi)` of two normalised names with `lo < hi` to an
      `int`, defaulting to 0, read as "how many minor units `hi` owes `lo`". A helper
      `_add(net, debtor_key, creditor_key, amount)` adds `+amount` when `debtor_key` is the `hi`
      of the pair and `-amount` when it is the `lo`, and does nothing when the two keys are
      equal.
   3. For each expense: let `n = len(expense.sharers)`. If `n == 0`, skip it — nobody owes
      anything and the payer has absorbed the whole total, which is the same rule as every other
      expense (`ADR-0009`). Otherwise `share = expense.amount_minor // n`, and for each sharer
      whose normalised name differs from the payer's, `_add(net, sharer, payer, share)`. The
      remainder is never allocated; it stays with the payer by construction (`ADR-0002`,
      `ADR-0004`, `ADR-0009`), and there is no branch on whether the payer is among the sharers.
   4. For each repayment: `_add(net, repayment.to_person, repayment.from_person, amount_minor)`
      — the person repaid owes the repayer, which is what "a repayment reduces what A owes B"
      becomes in a signed accumulator, and is why AC10's repayment between two people who share
      nothing prints a debt the other way round (`ADR-0006` step 3).
   5. Turn `net` into `Debt`s: skip every zero; for a positive value the debtor is `hi` and the
      creditor is `lo`; for a negative one they swap and the amount is negated. Sort by
      `(normalise_name(debtor), normalise_name(creditor))` and return.

   **After:** the module imports cleanly and `python3 -m compileall -q expenses tests` exits 0.

2. **`tests/test_debts.py` — the arithmetic, tested without the CLI.** A `unittest.TestCase`
   that builds `Ledger` objects directly. Cover: the AC2 ledger, the AC6 ledger, the AC8 circle,
   the AC9 uneven split, the AC10 lone repayment, an empty ledger, a ledger of people with
   nothing recorded, and the `ADR-0009` case — payer not among the sharers, with a total that
   does not divide evenly. Add one test for the AC3 identity that runs over **every** ledger the
   file builds: for each person, `sum(d.amount_minor for d in result if d.debtor is P)` minus
   `sum(... if d.creditor is P)` must equal the net position computed inline in the test from the
   ledger — shares of the expenses P shared in, less the totals P paid, plus repayments received,
   less repayments made, with a non-sharing payer's own share being the leftover per `ADR-0009`
   — and the net positions must sum to 0. **After:** `commands.test` exits 0 and the new file's
   tests are among those run.

3. **`expenses/cli.py` — the subcommand.** Add `NOBODY_OWES = "Nobody owes anybody."` beside the
   three existing empty-listing constants. Add a `debts` subparser with no arguments and
   `set_defaults(handler=cmd_debts)`, registered after `repayments` so `--help` lists it last.
   Add `cmd_debts(args, ledger)`: call `debts.debts(ledger)`; if the list is empty print
   `NOBODY_OWES`; otherwise print `f"{d.debtor} owes {d.creditor} {model.format_amount(d.amount_minor)}"`
   for each; `return False`, so `main` saves nothing. **After:** `python3 -m expenses --file
   /tmp/x.json debts` on a missing file prints `Nobody owes anybody.` and exits 0.

4. **`tests/test_cli_debts.py` — the criteria, end to end.** A `CliTestCase` per
   `tests/cli_harness.py`, building each ledger with real `add-person`, `add-expense` and `repay`
   invocations and asserting `result.lines` equals the exact expected list. One test per worked
   example — AC2, AC6, AC8, AC9, AC10, AC11 — plus: AC4 on an empty ledger and on people with no
   records; AC5 by running `debts` twice over unchanged data and asserting identical output, and
   once with names typed in mixed case and surrounding spaces to show the ordering uses the
   trimmed, case-folded form while the printed name is the one first typed; AC7 by repaying every
   debt in the AC2 ledger exactly and asserting the output is `Nobody owes anybody.` with no
   `0.00` anywhere; and AC1's exit code and unchanged ledger bytes. **After:** `commands.test`
   exits 0 with all eleven criteria covered.

5. **Re-check `docs/architecture/overview.md` against what was built.** This plan bumps it to v4
   with the fourth module, the `debts` command and the new dependency edge. If step 1 or 3
   departed from what v4 says, correct it and add a change-log row, as `implement` did for v2
   [src: docs/architecture/overview.md]. **After:** the overview describes the code that exists.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — one line per non-zero pair, `<debtor> owes <creditor> <amount>`, exit 0, first-typed names, positive amount | 1, 3, 4 | `tests/test_cli_debts.py`: the AC2 ledger → exit 0, three lines each matching the form; a person added as `Ana` and referred to as ` ana ` thereafter prints as `Ana`; `self.ledger_bytes()` is unchanged by running `debts` |
| AC2 — worked example, exact output | 1, 3, 4 | `tests/test_cli_debts.py`: builds the ledger with the six commands as written and asserts `result.lines == ["Ben owes Ana 10.00", "Cara owes Ana 10.00", "Cara owes Ben 6.00"]` |
| AC3 — the printed lines account for every minor unit; net positions sum to zero | 1, 2 | `tests/test_debts.py`: for every ledger the file builds, each person's signed line-total equals their net position recomputed inline from the ledger, asserted with `assertEqual` on `int`s, and `sum(net.values()) == 0` |
| AC4 — `Nobody owes anybody.` and exit 0 when no pair has a non-zero balance | 1, 3, 4 | `tests/test_cli_debts.py`: three cases — no people at all; Ana, Ben, Cara with nothing recorded; the AC2 ledger fully repaid — each asserting `result.lines == ["Nobody owes anybody."]` and `result.code == 0` |
| AC5 — ordered by debtor then creditor under `name.strip().casefold()`, stable across runs | 1, 4 | `tests/test_cli_debts.py`: a ledger whose people are added as `ana`, `BEN`, ` Cara ` and whose later commands use other casings → the lines come out in case-folded name order with the first-typed capitalisation; running `debts` twice gives identical `result.out` |
| AC6 — repayments net off, worked example including an overshoot | 1, 3, 4 | `tests/test_cli_debts.py`: AC2's ledger plus the two `repay` commands → `result.lines == ["Ana owes Cara 2.00", "Cara owes Ben 6.00"]` |
| AC7 — never a `0.00` line once everything is repaid | 1, 4 | `tests/test_cli_debts.py`: the AC2 ledger with `repay Ben→Ana 10.00`, `repay Cara→Ana 10.00`, `repay Cara→Ben 6.00` → `["Nobody owes anybody."]`, and `"0.00" not in result.out` |
| AC8 — a circle is printed, not collapsed | 1, 4 | `tests/test_cli_debts.py`: the three-expense circle → `result.lines == ["Ana owes Cara 10.00", "Ben owes Ana 10.00", "Cara owes Ben 10.00"]`, with an accompanying assertion in `tests/test_debts.py` that every net position in that ledger is 0 |
| AC9 — an uneven remainder stays with the payer | 1, 2, 4 | `tests/test_cli_debts.py`: 10.00 among Ana, Ben, Cara paid by Ana → `["Ben owes Ana 3.33", "Cara owes Ana 3.33"]`; `tests/test_debts.py` adds the `ADR-0009` variant where the payer is not a sharer |
| AC10 — a repayment between people who share no expense reverses | 1, 3, 4 | `tests/test_cli_debts.py`: Ana and Ben, no expenses, `repay --from Ana --to Ben --amount 5.00` → `["Ben owes Ana 5.00"]` |
| AC11 — a person involved in nothing produces no line and does not suppress AC4 | 1, 4 | `tests/test_cli_debts.py`: Ana, Ben, Cara with nothing recorded → `["Nobody owes anybody."]`; and the AC2 ledger with a fourth person `Dan` added → the same three lines as AC2 and no mention of `Dan` |

## Assumptions

Each is reversible in the sense `spec/question.md` §1 means: one file, no stored data, no
interface anyone outside the package depends on.

1. **`debts` prints nothing but debt lines — no header, no blank line, no trailing summary.** AC2,
   AC6, AC8, AC9 and AC10 each say "prints exactly" and then give only the lines, so a header
   would fail them as written [src: WI-0002 AC2]. Reversing: one `print`, and the six exact-output
   tests would have to change with it, which is the right amount of friction.
2. **An expense with an empty sharer list contributes nothing.** Not reachable through the CLI —
   `_resolve_sharers` returns every recorded person when `--shared-by` is omitted, and the payer
   is always recorded [src: expenses/cli.py] — but reachable in a hand-edited ledger, and the
   alternative is `ZeroDivisionError` on a file the store happily loads. Skipping is the same rule
   as every other expense taken to its limit: nobody owes anything, the payer absorbed the total
   (`ADR-0009`). Reversing: one line, and it has no test of its own beyond not crashing.
3. **A name appearing on a record but not in `people` prints in the form the record carries.**
   Also only reachable by hand-editing. The alternative is to refuse to report, which would make
   a loadable ledger unreportable. Reversing: one lookup.
4. **`debts` is registered last in `--help`.** Cosmetic; no criterion mentions it. Reversing: move
   one block.

## Decisions and ADRs

| decision | route | record |
|----------|-------|--------|
| The computation is a pure module `expenses/debts.py`, not a CLI handler and not a `Ledger` method | decided | `ADR-0008` |
| An uneven split whose payer is not a sharer leaves the remainder owed by nobody, and that is how AC3's "P's share" is read | decided | `ADR-0009` |
| The report is the pairwise ledger, netted per pair, circles printed | documented | `ADR-0006`, followed — steps 1–5 of this plan are its five steps |
| Each sharer owes `total // n`, the payer absorbs the remainder | documented | `ADR-0002`, restated as `divmod` by `ADR-0004`, followed |
| Money stays integer minor units through the whole computation | documented | `ADR-0004`, followed |
| The command is named `debts`; the empty-report line is exactly `Nobody owes anybody.`; lines are ordered by debtor then creditor | documented | `refine`'s three recorded decisions, now in AC1, AC4 and AC5 [src: WI-0002] |
| Test and lint commands | documented | `ADR-0005`; both already in `tracker/project.yaml` and both run green here [src: run: `python3 -m unittest discover -s tests -t . -q` → exit 0, 83 tests, OK; run: `python3 -m compileall -q expenses tests` → exit 0] |

Nothing was asked of the human. The one place the record disagreed with itself — where an uneven
split's remainder goes when the payer is not a sharer — was answerable from `ADR-0002` and
`ADR-0004` and is arithmetic rather than intent, so it took the top branch of the preference
order with an ADR to make the reading findable.

## Risks

- **AC3's wording admits a second reading, and under it AC3 contradicts itself.** `ADR-0009`
  records which reading governs and why, but `verify` will read the criterion before the ADR. If
  verification files a defect about a non-sharing payer being owed less than the total, the
  answer is `ADR-0009`, not a code change [src: WI-0002 AC3].
- **The signed-pair accumulator is easy to get backwards.** The key is sorted by normalised name,
  so which of the two people a positive number refers to depends on `lo < hi`, not on who was
  mentioned first. AC6 and AC10 are the two criteria that would catch an inversion, and both are
  in step 4 — if either passes while the other fails, the sign convention is the place to look.
- **Ordering compares normalised names, printing uses display names.** Sorting the display forms
  instead would put `BEN` before `ana`, which AC5 forbids. The mixed-case test in step 4 exists
  for exactly this and would otherwise be an untested distinction [src: WI-0002 AC5].
- **BUG-0001 is open against `cli.py`** — a failed ledger write still prints the success line
  [src: BUG-0001]. `debts` writes nothing, so it cannot be affected, and this plan does not touch
  the path involved. Named here so that a reviewer does not read step 3 as an attempt to fix it.
- **The lint gate is a syntax check.** `compileall` proves that every file parses and nothing more
  (`ADR-0005`). A green `no-lint-errors` on the new module means less than the name suggests.
- **83 tests pass today** [src: run: `python3 -m unittest discover -s tests -t . -q` → exit 0, 83
  tests, OK]. Step 3 adds a subparser to a shared parser, so a regression would show up in the
  existing CLI tests rather than the new ones; a green run of the whole suite is the evidence
  that matters, not a green run of `tests/test_cli_debts.py`.

## Out of scope for this item

- A minimised settlement, or any command that reduces the number of transfers. The stakeholder
  rejected it on `Q-001` and `ADR-0006` records that adding it later is a separate command over
  the same data.
- Any per-person summary, totals line, or explanation of which expenses make up a line
  [src: WI-0002].
- Any output format other than the printed lines — no CSV, JSON or export; no filtering by date,
  person or description [src: WI-0002].
- Recording a repayment, and anything else about how the ledger is written. WI-0001 owns it; this
  item only reads.
- Fixing BUG-0001, which is its own item under the same epic.
- The CSV import (WI-0003), which depends on this item being done but changes nothing here.
