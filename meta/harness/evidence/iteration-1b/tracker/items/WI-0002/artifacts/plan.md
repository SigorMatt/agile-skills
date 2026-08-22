# Plan — WI-0002 Record an expense paid by one person and shared by several

## Problem

The tool records who is in the group and nothing else. This item adds the second of the four kinds
of fact the product holds: an expense — a total, the one person who paid it, and the people who
shared it, any of whom may carry a stated share — together with the command that lists expenses
back with each sharer's share worked out.

The constraints are all recorded and none of them is open. `ADR-0002` fixes the split model and
the six ways an entry can be invalid. `ADR-0003` fixes money as whole minor units, at most two
decimal places on entry and exactly two on display, the payer-first remainder rule, and — the part
that shapes the storage — that no derived share is ever stored. `ADR-0005` fixes who a named
person is and reserves `,` and `=` so the sharer list fits on one line. `ADR-0006` fixes the two
subcommand names, and `refine` pinned their arguments and the exact text of eighteen messages in
fourteen acceptance criteria. `ADR-0007` fixes the file; this plan fills in the `expenses` key it
left open.

## Approach

The three-layer shape from `docs/architecture/overview.md` is unchanged and this item fits inside
it: `cli.py` gains two handlers and a small option parser, `group.py` gains the expense rules,
`storage.py` gains one shape check, and a new `money.py` owns the one thing that is neither
command line nor group rule — turning `12.5` into `1250` and `1250` back into `12.50`.

The split between `cli.py` and `group.py` for the sharer list is deliberate and is the one
structural decision in this item. **Syntax is `cli.py`'s**: splitting `Alice,Bob=6,Carol` on the
two reserved characters and rejecting `Bob=`, `Alice=1=2` and an empty element. **Meaning is
`group.py`'s**: whether those names are in the group, whether the same person appears twice, and
whether the stated shares can work against the total. That way `group.py` never sees a comma and
`cli.py` never resolves a person.

Everything the two subcommands print is derived on each run from what was stored (`ADR-0003`
point 6, `ADR-0009` point 4). Nothing computed is written.

## Steps

1. **Add `expenses/money.py`** — the only module that converts between what a user types and the
   integers everything else uses.
   - `parse_amount(text) -> int` — accepts an optional sign, digits, and at most two decimal
     places; returns whole minor units. Raises `group.RuleError` with `<text> is not an amount.`
     for anything else and `Amounts have at most two decimal places: <text>.` for too much
     precision (`ADR-0003` point 2). It does **not** judge sign or magnitude — "more than zero"
     is a rule about an expense, not about an amount, and it lives with the rule that needs it.
   - `format_amount(minor) -> str` — exactly two decimal places, always (`ADR-0003` point 2).

   Afterwards: `12`, `12.5` and `12.50` all parse to `1250`; `12.505` and `twelve` raise;
   `format_amount(0)` is `0.00`.

2. **Extend `expenses/storage.py`** with the `expenses` key.
   - `empty_record()` gains `"expenses": []`.
   - `load()` gains a shape check for `expenses` mirroring the one for `people`: a list of
     objects, each with an integer `total`, a string `paid_by`, and a `shares` list of objects
     with a string `person` and an optional integer `amount` (`ADR-0009` points 1 to 3). A record
     that fails it raises `RecordError` naming the path and saying the file has not been changed,
     exactly as the `people` check does (`ADR-0007` point 5).
   - Nothing else in this module changes. An absent `expenses` key still reads as empty, so a file
     written by WI-0001 loads without a migration (`ADR-0007` point 2).

   Afterwards: a WI-0001-era file loads and gains an `expenses` key on its next save; a file whose
   `expenses` is `"nope"` is refused rather than crashing later.

3. **Add the expense rules to `expenses/group.py`.**
   - `add_expense(record, total_text, payer_text, sharers) -> dict` where `sharers` is the list of
     `(name_text, amount_text_or_None)` pairs `cli.py` produced, **in the order named**. It
     resolves the payer and every sharer through the existing `find_person` (`ADR-0005` point 5),
     parses the amounts through `money`, applies every rule below, appends the expense to
     `record["expenses"]` in the shape `ADR-0009` fixes, and returns it. It does not save.
   - `shares_of(expense) -> list[(person, minor)]` — the derivation, in named order:
     stated shares are taken as given; the remainder (`total` less the sum of the stated ones) is
     divided among the sharers with none, each getting `remainder // k`, and the first
     `remainder % k` of them one minor unit more, ordered **payer first if the payer is one of
     them, then the rest in named order** (`ADR-0003` point 3). With no unstated sharer the
     remainder is zero and there is nothing to divide.
   - `expenses(record) -> list[dict]` — the recorded expenses, in order.
   - The refusals, each raising `RuleError` with the exact text the criteria pin: an unknown
     person, the same person named twice (compared by identity key), a total that is zero or
     negative, a negative stated share, stated shares over the total, and stated shares under the
     total when every sharer has one (`ADR-0002` § *Decision*).

   Afterwards: every rule in `ADR-0002` and `ADR-0003` is exercisable without a file and without
   stdout, and `shares_of` sums to `total` for every accepted expense.

4. **Add a small option parser and the two handlers to `expenses/cli.py`.**
   - `_options(arguments, known) -> (positionals, options)` — walks the argument list, treats any
     token beginning `--` as an option name that must be in `known` and must take the next token
     as its value. Raises `RuleError` with `Unknown option: <name>.` or
     `<name> was given more than once.` (AC12).
   - `_split_sharers(text) -> list[(name, amount_text_or_None)]` — splits on `,`, then each
     element on `=`, raising `RuleError` with `--shared-by needs at least one name.`,
     `A name cannot be empty.`, `<element> has no amount after the equals sign.` or
     `<element> has more than one equals sign.` (AC11). Names are passed through untouched;
     `group` decides what they mean.
   - `_add_expense` handler: one positional (the total) and the two required flags; refuses with
     `add-expense needs a total.`, `add-expense needs --paid-by.` or
     `add-expense needs --shared-by.`; on success calls `group.add_expense`, then `storage.save`,
     then prints `Recorded <total> paid by <payer>, shared by <n> people.`
   - `_expenses` handler: no arguments (`expenses takes no arguments.`); prints
     `No expenses have been recorded yet.` when there are none, otherwise one line per expense,
     numbered from 1:
     `<n>. <total> paid by <payer>, shared by <person> <share>, <person> <share>, …`
     with every amount through `money.format_amount` and every person as stored.
   - Register both in `COMMANDS`, which automatically extends the usage line WI-0001 prints for an
     unknown subcommand.
   - **Widen the `except` clause to include `OSError`**, reporting
     `Cannot save to <path>: <reason>.` per `ADR-0010`. This is the gap WI-0001's review handed to
     this execution. See `## Risks` — the branch itself is not covered by any criterion here.

   Afterwards: all fourteen criteria are observable through `cli.main`.

5. **Extend the tests**, reusing `tests/support.py` from WI-0001 unchanged:
   - `tests/test_money.py` — `parse_amount` and `format_amount` directly, including `12`, `12.5`,
     `12.50`, `0.01`, `12.505`, `twelve`, and the round trip.
   - `tests/test_add_expense.py` — AC1, AC5, AC6, AC7, AC14.
   - `tests/test_expenses_listing.py` — AC3, AC4.
   - `tests/test_expense_refusals.py` — AC8, AC9, AC10, AC11, AC12, AC13.
   - `tests/test_persistence.py` — extended with AC2, as real subprocesses, for the same reason
     WI-0001 needed them: three in-process calls would pass even if the record were held in a
     module-level variable.

6. **Update `docs/architecture/overview.md` to v2** — a fourth module (`money.py`) and the
   sentence about what `group.py` now owns. Bump the version and add a change-log row.

7. **Run the project's own commands and record the output**: `python3 -m unittest discover -s
   tests -t . -q` and `python3 -m compileall -q expenses tests`. Both must exit `0`, and the
   WI-0001 tests must still pass unchanged — AC14 is the criterion, but the whole suite is the
   evidence.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `add-expense 30 --paid-by Alice --shared-by Alice,Bob,Carol` → `Recorded 30.00 paid by Alice, shared by 3 people.`, exit 0 | 3, 4 | `tests/test_add_expense.py`: `run_cli(...)` returns exactly that triple |
| AC2 — persistence across separate invocations | 2, 5 | `tests/test_persistence.py`: `add-expense` in one `python3 -m expenses` **process**, `expenses` in another, the second printing the recorded line |
| AC3 — listing format, numbered from 1, two decimals, stored spellings | 3, 4 | `tests/test_expenses_listing.py`: stdout is exactly `1. 30.00 paid by Alice, shared by Alice 10.00, Bob 10.00, Carol 10.00\n` |
| AC4 — empty listing message, exit 0 | 4 | `tests/test_expenses_listing.py`: `run_cli("expenses")` on a fresh record returns `(0, "No expenses have been recorded yet.\n", "")` |
| AC5 — equal split by default; a single sharer takes the total; payer need not share | 3 | `tests/test_add_expense.py`: `add-expense 12 --paid-by Alice --shared-by Bob` then `expenses` → `1. 12.00 paid by Alice, shared by Bob 12.00` |
| AC6 — mixed form, and a stated-zero remainder shown as `0.00` | 3 | `tests/test_add_expense.py`: both examples in the criterion asserted verbatim |
| AC7 — payer-first remainder, three worked examples | 3 | `tests/test_add_expense.py`: all three lines asserted verbatim, including the `10.01` case where the payer is named second and still takes the odd penny |
| AC8 — unknown person refused; identity key resolves a known one | 3 | `tests/test_expense_refusals.py`: `Dave is not in the group.` on stderr, exit non-zero, and `expenses` + `people` unchanged; `--paid-by "sam okafor"` succeeds and lists as `Sam Okafor` |
| AC9 — five malformed or out-of-range amounts | 1, 3 | `tests/test_expense_refusals.py`: one subtest per bullet, each asserting the pinned stderr text |
| AC10 — stated shares over the total, under it with all stated, and exactly equal with all stated | 3 | `tests/test_expense_refusals.py`: two refusals with their exact messages, one acceptance exiting 0 |
| AC11 — five malformed sharer lists | 4 | `tests/test_expense_refusals.py`: one subtest per bullet, including `Alice,alice` and `Alice,ALICE` both giving `Alice is named twice in --shared-by.` |
| AC12 — six command-line failures | 4 | `tests/test_expense_refusals.py`: one subtest per bullet, each asserting the pinned stderr text |
| AC13 — no refusal records anything, and none prints a traceback | 3, 4 | `tests/test_expense_refusals.py`: a test that runs every refusal above in one record and asserts `expenses` output is unchanged and stderr never contains `Traceback (most recent call last)` |
| AC14 — WI-0001's data is undisturbed | 2, 3 | `tests/test_add_expense.py`: after AC1, `run_cli("people")` still prints the four names in the order added |

## Assumptions

1. **`money.parse_amount` does not judge sign or magnitude.** "More than zero" is a rule about an
   expense total and "not negative" a rule about a stated share, and both live in `group.py` with
   the messages the criteria pin. **Reversing it** — folding the checks into the parser — is a
   move of two conditions between two files, with no interface or data change.
2. **The option parser is written by hand rather than with `argparse`,** continuing WI-0001's
   assumption for the same reason: the criteria pin `Unknown option: --split-by.` and
   `--paid-by was given more than once.`, and `argparse` writes its own messages and exits from
   inside the parser. **Reversing it** is a rewrite of `cli.py` alone; no criterion names the
   mechanism.
3. **A stated share of `0` is stored as `0`, not omitted.** `ADR-0009` point 3 requires the
   distinction, and AC6 makes it observable: an omitted amount means "divide the remainder", a
   stated `0` means "owes nothing". **Reversing it** would change stored data, so it is the one
   assumption here that is not free to undo — which is why it is in the ADR as well.

## Decisions and ADRs

| decision | where |
|----------|-------|
| The stored shape of one expense, and that no derived share is stored | `ADR-0009` (new) |
| A failure to write the record is a stated message, not a traceback; `Exception` is still not caught | `ADR-0010` (new) |
| A fourth module, `money.py`, and what `group.py` now owns | `docs/architecture/overview.md` v2 |
| The split model and the six refusal conditions | `ADR-0002`, cited, not re-decided |
| Minor units, two decimal places, payer-first remainder, derived-not-stored | `ADR-0003`, cited |
| Identity keys, reserved `,` and `=` | `ADR-0005`, cited |
| The subcommand names and the no-argument rule for listings | `ADR-0006`, cited |
| The file, its location, atomic write, missing versus corrupt | `ADR-0007`, cited |
| Parser scope, hand-rolled options, stated zero | `## Assumptions` above |

`tracker/project.yaml` already carries both commands from `ADR-0008`; nothing about them changes.

## Risks

- **The `OSError` branch from `ADR-0010` is not covered by any acceptance criterion on this
  item.** No criterion here exercises a write failure, and `plan` may not write criteria. It is
  implemented inside the refusal handling AC13 does exercise, and it is declared here so that
  `verify` records it under "not verified" rather than discovering it, and so `review-close` sees
  a known gap rather than an unrequested change. A test may still be written for it; it just
  cannot be claimed as satisfying a criterion.
- **The remainder order is the easiest thing in this item to get subtly wrong.** `ADR-0003`
  point 3 orders the *unstated* sharers, payer first, then named order — three separate
  conditions. AC7's third example exists precisely to catch an implementation that orders by named
  position alone, and `refine`'s journal records that its own first draft of that example used a
  total that divided evenly and would have proved nothing. Any test written for AC7 must use a
  total whose division leaves a remainder.
- **`group.expenses` and the module-level name `expenses` collide conceptually.** The package is
  called `expenses`, the subcommand is called `expenses`, and the accessor is called `expenses`.
  Nothing breaks, but a reader of `group.py` should not have to work out which is meant; if the
  developer finds it genuinely confusing, renaming the accessor is inside the plan's latitude.
- **Compatibility in both directions is assumed and only one direction is proven.** A
  WI-0001-era file has no `expenses` key and reads as empty here, which `ADR-0007` point 2
  guarantees and step 2 preserves. The reverse — WI-0001's code reading a file this item wrote —
  also works, because that `load` ignores keys it does not know, and WI-0001's verification
  demonstrated exactly that with an unknown `expenses` key surviving a save. Neither direction is
  an acceptance criterion, so if step 2's shape check is written too strictly, the first direction
  could break without any criterion noticing.
- **Nothing validates that a stored expense names people who are still in the group**, because
  nothing removes a person. If removal is ever added, every expense becomes a dangling reference
  and this assumption becomes a defect.

## Out of scope for this item

- Balances and who owes whom (WI-0003), and payments (WI-0004). `shares_of` is the function
  WI-0003 will build on, but nothing in this item sums across expenses.
- Editing or deleting a recorded expense, and therefore any notion of an expense identifier. The
  numbers `expenses` prints are display only.
- A description, label, date or category on an expense — excluded by `docs/product/prd.md` (v2)
  and named in this item's `## Out of scope`.
- Any change to `add-person` or `people` beyond the shared `except` clause in `cli.main` that
  `ADR-0010` widens.
