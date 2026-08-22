# Plan — WI-0004 Record a settlement payment and net it off the balances

## Problem

The tool records the group, what they spent, and who should pay whom to settle up — but it has no
way to record that somebody actually did. Until it has one, `who-owes-whom` reports the same debts
forever, which is the failure the human named when they put settlement in scope: "otherwise the
numbers just keep racking up forever and stop meaning anything" (`EP-001/Q-001`).

This item adds the fourth and last kind of fact the product holds: a payment from one person to
another. It adds `add-payment` and `payments`, and it makes `who-owes-whom` net payments off — not
by changing `who-owes-whom`, but by changing what a net position means.

Nothing is open. `ADR-0011`, written for this item, fixes the stored shape and decides that
payments enter the arithmetic inside `group.net_positions` and nowhere else. `ADR-0003` fixes
amounts, `ADR-0005` identity, `ADR-0006` the two subcommand names, and `refine` pinned the
arguments, fifteen criteria and the exact text of eleven messages. This is the epic's last item.

## Approach

No new module and no new concept. `group.py` gains `add_payment` and `payments` beside the expense
functions, `net_positions` grows a second loop, `storage.py` gains one shape check, and `cli.py`
gains two handlers built from the same `_options` helper WI-0002 wrote.

The one structural point is `ADR-0011` point 2: **payments enter through `net_positions`**. That
is what makes `settle`, `who-owes-whom` and every future consumer correct by default, and it is
why AC5 to AC8 and AC15 require no change to WI-0003's code at all — only to its inputs.

This item also discharges two instructions left in `item.md` § *Notes* by earlier reviews. They
are not acceptance criteria, because neither is observable through a command; they are steps 5 and
6 below, and `review-close` will look for them.

## Steps

1. **Extend `expenses/storage.py` with the `payments` key.**
   - `empty_record()` gains `"payments": []`.
   - `load()` gains `_is_payment`, mirroring `_is_expense`: an object with an integer `amount`
     (not a bool), a string `from` and a string `to`. A record whose `payments` fails it raises
     `RecordError` naming the path and saying the file has not been changed (`ADR-0007` point 5).
   - An absent `payments` key still reads as empty, so every record written before this item
     loads unchanged (`ADR-0007` point 2).

   Afterwards: a WI-0003-era file loads and gains a `payments` key on its next save; a file whose
   `payments` is `{"amount": "ten"}` is refused rather than crashing later.

2. **Add the payment rules to `expenses/group.py`.**
   - `payments(record) -> list[dict]` — the recorded payments, in order.
   - `add_payment(record, amount_text, from_text, to_text) -> dict` — parses the amount through
     `money.parse_amount`; refuses zero or negative with `A payment must be for more than zero.`;
     resolves both people through the existing `find_person`, refusing an unknown one with
     `<name> is not in the group.`; refuses two names with the same identity key with
     `A payment must be between two different people.`; appends
     `{"amount": …, "from": …, "to": …}` to `record["payments"]` and returns it. It does not save.
   - **`net_positions` gains a second loop** (`ADR-0011` point 2): after the expenses, for each
     payment, add its amount to `from`'s position and subtract it from `to`'s. Nothing else in
     the function changes, and no caller of it changes.

   Afterwards: `net_positions` on AC5's record returns `Alice +1000, Bob 0, Carol -1000`, and
   `settle` — untouched — produces `Carol pays Alice 10.00`.

3. **Add the two handlers to `expenses/cli.py` and register them in `COMMANDS`.**
   - `_add_payment`: one positional (the amount) and the two required flags, via the existing
     `_options(arguments, ("--from", "--to"))`. Refuses with `add-payment needs an amount.`,
     `add-payment takes a single amount.`, `add-payment needs --from.` or
     `add-payment needs --to.`; on success calls `group.add_payment`, then `storage.save`, then
     prints `Recorded <amount> paid by <from> to <to>.`
   - `_payments`: no arguments (`payments takes no arguments.`); prints
     `No payments have been recorded yet.` when there are none, otherwise one line per payment,
     numbered from 1: `<n>. <from> paid <to> <amount>` — **past tense**, where `who-owes-whom`
     says `pays`.
   - Registering both completes the seven subcommands `ADR-0006` fixed, and the usage line for an
     unknown subcommand grows to its final form.

   Afterwards: all fifteen criteria are observable through `cli.main`.

4. **Write `tests/test_payments.py`**, using `ExpenseTestCase` from `tests/support.py`:
   - AC1, AC3, AC4 (the confirmation, the listing, the empty listing);
   - AC5 to AC8 and AC15, each asserting the exact `who-owes-whom` output the criterion names;
   - AC9 to AC12, one test per bullet, each asserting the pinned stderr;
   - AC13 as a loop over every refusal, asserting `payments`, `expenses` and `people` are
     unchanged — **and, on a fresh record with no file, that a refused `add-payment` leaves no
     file behind**, which is the gap WI-0002's review handed here;
   - AC14 after AC5's record;
   - AC2 as real subprocesses, in `tests/test_persistence.py`.

5. **Discharge the first inherited instruction** (`item.md` § *Notes* 2, from WI-0003's review):
   add a test asserting `group.net_positions` returns **everybody, in the order they were
   added** — including people at zero. WI-0003's plan states it as a contract and nothing asserts
   it; sorting the result by amount currently passes the whole suite. Put it in
   `tests/test_who_owes_whom.py`, beside the function's other tests.

6. **Discharge the second** (`item.md` § *Notes* 3): strengthen the purity assertion so it uses a
   record with **two expenses and two payments**, not one expense. WI-0003's
   `test_the_record_is_not_modified` cannot distinguish "does not write" from "writes something
   reordered", because reversing a one-element list is a no-op. Extend that test, or add one
   beside it, and assert the same for `payments` and `expenses` while there.

7. **Update `docs/architecture/overview.md` to v4** — the record now holds all four kinds of fact,
   `group.py` owns the payment rules, and the "what is not here yet" section is emptied, because
   this is the epic's last item. Bump the version and add a change-log row.

8. **Run the project's own commands**: `python3 -m unittest discover -s tests -t . -q` and
   `python3 -m compileall -q expenses tests`. Both must exit `0`, and all 96 existing tests must
   still pass — AC14 is the criterion for the data, but the suite is the evidence for the code.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 2, 3 | `tests/test_payments.py`: `run_cli("add-payment", "10", "--from", "Bob", "--to", "Alice")` returns `(0, "Recorded 10.00 paid by Bob to Alice.\n", "")` |
| AC2 | 1, 4 | `tests/test_persistence.py`: `add-payment` in one `python3 -m expenses` **process**, `payments` in another, the second printing the recorded line |
| AC3 | 3 | `tests/test_payments.py`: stdout is exactly `1. Bob paid Alice 10.00\n`; a second test records two and asserts the numbering and order |
| AC4 | 3 | `run_cli("payments")` on a fresh record returns `(0, "No payments have been recorded yet.\n", "")` |
| AC5 | 2 | after the expense and the payment, `run_cli("who-owes-whom")` stdout is exactly `Carol pays Alice 10.00\n` |
| AC6 | 2 | the 4.00 part payment; stdout is exactly `Carol pays Alice 10.00\nBob pays Alice 6.00\n` |
| AC7 | 2 | both payments; stdout is exactly `Everybody is settled up.\n` |
| AC8 | 2 | the 30.00 overpayment; stdout is exactly `Alice pays Bob 10.00\nCarol pays Bob 10.00\n` |
| AC9 | 2 | `--from Dave` → exit non-zero, stderr `Dave is not in the group.\n`, and `payments` + `people` unchanged; `--from "sam okafor"` succeeds and lists as `Sam Okafor` |
| AC10 | 2 | `--from Alice --to Alice` and `--from ALICE --to Alice` → stderr `A payment must be between two different people.\n` |
| AC11 | 2 | three subtests: `ten is not an amount.`, `Amounts have at most two decimal places: 10.005.`, `A payment must be for more than zero.` for both `0` and `-5` |
| AC12 | 3 | six subtests, one per bullet, each asserting the pinned stderr |
| AC13 | 2, 3, 4 | a loop over every refusal above: `payments`, `expenses` and `people` output identical before and after, no `Traceback (most recent call last)` on stderr — **plus** a test on a record with no file yet, asserting the file still does not exist after a refused `add-payment` |
| AC14 | 1, 2 | after AC5's record, `run_cli("people")` prints the four names in order and `run_cli("expenses")` prints the expense with its shares unchanged |
| AC15 | 2 | no expenses at all, one payment; `who-owes-whom` stdout is exactly `Alice pays Bob 10.00\n` |
| *(not a criterion)* | 5 | `tests/test_who_owes_whom.py`: `net_positions` returns everybody, including zeros, in the order they were added — the contract WI-0003 documented and nothing asserted |
| *(not a criterion)* | 6 | the purity assertion, on a record with two expenses **and** two payments |

## Assumptions

1. **`add-payment` reuses `cli._options` unchanged.** It was written for `add-expense` and takes
   the set of known flags as an argument, so `("--from", "--to")` needs nothing new — including
   the repeated-flag and unknown-option messages AC12 pins, which are the same two strings.
   **Reversing it** — giving `add-payment` its own parser — is one function in one file.
2. **`payments` and `expenses` do not share a listing helper.** `refine` left this unconstrained.
   The two lines differ in every part except the numbering, so a shared helper would be a
   parameter for each field. **Reversing it** is a refactor of two functions in `cli.py` with no
   change to output.
3. **The order of the two refusals in `add_payment` — unknown person before self-payment.**
   `add-payment 10 --from Dave --to Dave` reports that Dave is not in the group rather than that
   the two are the same person. Both are true; membership is the more useful thing to be told
   first, and it is the check that already exists. **Reversing it** is two swapped blocks.

## Decisions and ADRs

| decision | where |
|----------|-------|
| The stored shape of a payment; a payment is not modelled as an expense; payments enter the arithmetic inside `net_positions` and nowhere else | `ADR-0011` (new) |
| Whole minor units, two decimal places, nothing derived stored | `ADR-0003`, cited |
| Identity keys decide who a typed name is, everywhere | `ADR-0005`, cited |
| The two subcommand names and the no-argument rule for listings | `ADR-0006`, cited |
| The file, atomic write, missing versus corrupt | `ADR-0007`, cited |
| A failed write is a stated message | `ADR-0010`, cited — it applies to `add-payment` for free, since the catch is in `cli.main` |
| What `who-owes-whom` prints, and which settlement | `ADR-0004` and WI-0003's criteria, cited; **this item changes neither** |
| Option parser reuse, no shared listing helper, refusal ordering | `## Assumptions` above |

`tracker/project.yaml` already carries both commands from `ADR-0008`; nothing changes.

## Risks

- **The `net_positions` change is the whole item, and it is four lines.** Everything else is
  plumbing. If those four lines are wrong in sign, AC5 to AC8 and AC15 all fail together and
  loudly — but a subtler error, folding payments in twice, would make AC5 pass and AC6 fail, which
  is why the criteria include a part payment as well as a full one.
- **Step 5's test is the only thing that will ever assert `net_positions`' ordering**, and it is
  easy to write in a way that passes for the wrong reason — for example by comparing sets, or by
  using a record where insertion order and alphabetical order coincide. It should use people whose
  added order differs from both their alphabetical order and their position magnitudes.
- **Step 6 can be written so that it still cannot fail.** The point is a record where *reordering*
  is detectable: at least two expenses and two payments, with different amounts. A second
  one-element list would repeat WI-0003's mistake in a new place.
- **AC13's "no file is left behind" needs a record with no file at all**, which means no people
  either — so the refusal it exercises has to be one that does not require a person to exist. A
  bad amount (`add-payment ten --from Bob --to Alice`) refuses before the record is even loaded;
  an unknown-person refusal on an empty group also works, since the group is empty. Either is
  fine, but a test that first adds people has already created the file and proves nothing.
- **Nothing links a payment to a debt**, so a payment recorded twice looks exactly like two
  payments that really happened, and the tool will believe it. That is inherent in the model
  (`ADR-0011` § *Consequences*) and there is no criterion about it.

## Out of scope for this item

- Editing or deleting a recorded payment; any "settle everybody" reset; refusing or warning about
  an overpayment. All three are in the item's `## Out of scope`, the last one deliberately.
- Any description, date or reason on a payment (`prd.md` v2, "Nothing else").
- Any change to `who-owes-whom`, `settle`, `shares_of`, `add-expense` or `add-person`. This item
  changes what `net_positions` reads and nothing else about the arithmetic.
- Linking a payment to the debt it discharges, or detecting a duplicate payment — see `## Risks`.
