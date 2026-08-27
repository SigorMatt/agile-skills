# Plan — WI-0002 Show who owes whom

## Problem

The tool already records the people in a group and the expenses they share, and stores each
expense's per-person shares as whole minor units [src: ADR-0001; ADR-0003]. What it cannot do is
answer the question it was built for: who should hand money to whom, right now, so that the group
is square. This item adds one read-only command, `python3 -m expenses settle`, which computes each
person's overall position from what is already stored and prints a short list of payments that
settles the group [src: WI-0002 AC1]. The constraints come from three places: the stakeholder's,
who asked for payments rather than balances [src: EP-001/Q-002]; refinement's, who fixed the
properties the printed list must have and the exact strings it must print
[src: tracker/items/WI-0002/artifacts/refinement-qa.md]; and the project's, which is python3 and
its standard library with no external services [src: tracker/items/EP-001/item.md]. Nothing is
written, no stored record changes, and no new state is introduced [src: WI-0002 AC5].

## Approach

One new module joins the package, at the same layer as `money.py`:

```
expenses/cli.py        gains a third top-level command, `settle`, and its handler
expenses/settle.py     NEW — positions and the settlement, as pure functions over a dataset
expenses/store.py      unchanged
expenses/money.py      unchanged; format_amount is reused for the printed amounts
```

`settle.py` takes the dataset dictionary that `store.load()` returns and gives back plain data.
It imports nothing from `store.py` or `cli.py`, does no I/O and prints nothing, which keeps the
project's one structural rule — the layering is one-way [src: docs/architecture/overview.md] —
and lets every figure in this item be tested without touching a disk.

The two functions this plan fixes (signatures are the architect's; the bodies are the
developer's):

```python
# expenses/settle.py
positions(data) -> dict
    # {name: net_minor} for every person in data["people"], in recorded order.
    # net_minor = sum of amount_minor over expenses this person paid
    #           - sum of shares_minor[name] over every expense naming them.
    # Whole minor units; across a dataset the values sum to zero.

settlement(data) -> list
    # [(payer_name, receiver_name, amount_minor), ...], largest debt first,
    # computed by the rule in ADR-0005. Empty when every position is zero.
```

`cli.py` gains a `settle` subparser that takes no arguments, and one handler. The handler loads
the dataset, calls `settlement`, and either prints the single line `no payments needed` or one
line per payment in the form `Ben pays Ana 10.00`, using `format_amount` so that the amounts look
like every other amount the tool prints [src: tracker/items/WI-0002/artifacts/refinement-qa.md].
It never calls `store.save`, which is the only function in the project that writes
[src: expenses/store.py], and that is what makes AC5 a property of the design rather than a
promise.

There is one structural detail the existing parser forces. Handlers are dispatched on the pair
`(args.command, args.action)` [src: expenses/cli.py], and `settle` has no sub-action, so its
subparser must set `action` to `None` explicitly and its handler must be registered under
`("settle", None)`. Without that the command raises `AttributeError` instead of running.

The one decision this design rests on — which of the many valid settlements to print, and in what
order — is recorded as ADR-0005 rather than buried in a step.

## Steps

1. **Add `positions()` to a new `expenses/settle.py`.** Module docstring states the layering rule
   it obeys. `positions(data)` walks `data["expenses"]` once, adding each expense's `amount_minor`
   to its `paid_by` and subtracting each entry of its `shares_minor` from the named person, and
   returns a dict keyed by every name in `data["people"]` in that order, defaulting to 0 for
   anyone who neither paid nor shared. Afterwards: for the dataset of AC3 the function returns
   `{"Ana": 1666, "Ben": -133, "Cara": -933, "Dan": -600, "Eve": 0}`, and the values sum to 0.

2. **Add `settlement()` to `expenses/settle.py`.** It calls `positions()`, splits the non-zero
   entries into debtors and creditors preserving the recorded order, and applies ADR-0005: while
   both pools are non-empty, take the largest debt and the largest credit — ties broken by
   recorded order — emit `(debtor, creditor, min(debt, credit))`, and reduce both by that amount,
   dropping whichever reaches zero. Returns the payments in the order emitted. Afterwards: AC3's
   dataset returns exactly `[("Cara", "Ana", 933), ("Dan", "Ana", 600), ("Ben", "Ana", 133)]`, and
   an all-zero dataset returns `[]`.

3. **Add the `settle` command to `expenses/cli.py`.** In `build_parser()`, add a third top-level
   subparser named `settle` with help text, no arguments, and `set_defaults(action=None)`. Add a
   handler `settle_report(args, out)` that calls `store.load(store.store_path())`, then
   `settle.settlement(data)`; if the result is empty it prints exactly `no payments needed` to
   `out` and returns, otherwise it prints one line per payment as
   `"%s pays %s %s" % (payer, receiver, format_amount(amount_minor))`. Register it in `HANDLERS`
   under the key `("settle", None)`. Afterwards: `python3 -m expenses settle` runs, AC1 and AC2
   hold, and AC5 holds because the handler calls nothing that writes.

4. **Write `tests/test_settle.py`.** New file, tests over the pure functions with datasets built as
   literals — no temporary directories, because these functions never touch disk. Cover: AC3's
   five-person dataset, asserting the exact three payments, that `Eve` appears in no payment, that
   every amount is greater than zero, that no name is both a payer and a receiver, and that the
   payments number one fewer than the four non-zero positions; AC1's three-person dataset,
   asserting the tie between `Ben` and `Cara` is broken by recorded order; an all-zero dataset and
   an empty dataset, each returning `[]`; and an expense whose payer is not among its sharers.
   Afterwards: `python3 -m unittest discover -s tests -t .` passes with these added.

5. **Extend `tests/test_cli.py`.** Add a `SettleTestCase` in the style of the existing cases — a
   fresh `EXPENSES_STORE` per test. Cover: AC1 end to end, comparing sorted stdout against the two
   expected lines; AC2's three stores, each asserting stdout is exactly `no payments needed` and
   the exit code is 0; AC4 by running `settle` twice in two subprocesses, as
   `test_both_listings_are_byte_identical_from_a_fresh_process` already does for the listings
   [src: tests/test_cli.py], and comparing the bytes; AC5 by hashing the data file either side of a
   `settle` run and by pointing `EXPENSES_STORE` at a path that does not exist and asserting it
   still does not exist afterwards. Afterwards: every criterion of this item has a test that fails
   if its behaviour is removed.

6. **Document the command in `README.md`.** Add a `### settle` section under "The commands",
   after `expense list`: the command, a worked example showing the two lines of AC1, the
   `no payments needed` case, and one sentence saying the command only reports — it records
   nothing and does not mark anything as paid. Afterwards: AC6 holds.

7. **Move `settle.py` into the body of `docs/architecture/overview.md`.** The overview at v2
   describes this module under "What is coming" because it did not exist when the plan was
   written. Once it does, move it into "The pieces, and why each exists" and into the diagram,
   cite `expenses/settle.py` and ADR-0005, bump to v3 and add a change-log row
   [src: .claude/agile-skills/spec/doc-header.md]. Afterwards: the overview describes the package
   that is actually there.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — three people, one 30 expense, two expected lines | 2, 3 | `tests/test_cli.py` runs `person add` ×3, `expense add`, then `settle`, and asserts sorted stdout equals `["Ben pays Ana 10.00", "Cara pays Ana 10.00"]` with exit 0; `tests/test_settle.py` asserts the same pairing at the function level, where the `Ben`/`Cara` tie is what the recorded-order tie-break decides |
| AC2 — three ways to have nothing to settle | 2, 3 | `tests/test_cli.py`, three tests: an untouched store; `person add Ana` + `person add Ben`; and those two plus `expense add --amount 10 --paid-by Ana --shared-by Ana`. Each asserts stdout is exactly `"no payments needed\n"` and the code is 0 |
| AC3 — five-person dataset, exact three lines and four properties | 1, 2, 3 | `tests/test_cli.py` builds the dataset with the real commands and asserts sorted stdout equals the three expected lines; `tests/test_settle.py` asserts each of the four properties separately against `settlement()` — amounts positive, no name in both roles, `Eve` absent, three payments against four non-zero positions — and that the three amounts sum to Ana's 1666 |
| AC4 — byte-identical across two processes | 2 | `tests/test_cli.py` runs `python3 -m expenses settle` twice via `subprocess.run` against the same store and asserts the two `stdout` values are equal as bytes. Determinism comes from ADR-0005's tie-break, not from luck |
| AC5 — the command changes nothing | 3 | `tests/test_cli.py`: `hashlib.md5` of the data file before and after a `settle` run, asserted equal; and a second test pointing `EXPENSES_STORE` at a path in a temporary directory that does not exist, asserting exit 0, stdout `no payments needed`, and `not path.exists()` afterwards |
| AC6 — the README documents it | 6 | Reading `README.md`: it names `python3 -m expenses settle`, shows an example of the payment lines, and states the `no payments needed` case. Checked by opening the file, which is what the criterion asks for |

## Assumptions

- **The settlement lives in its own module, `expenses/settle.py`, rather than in `store.py` or in
  a handler in `cli.py`.** `store.py` is about the dataset's storage and validity and imports
  nothing but `money.py`; putting a report in it would give it a second job. A handler in `cli.py`
  would put arithmetic in the one layer that prints, which is what the project's layering rule
  exists to prevent [src: docs/architecture/overview.md]. **Reversible:** the two functions move to
  another file in the package with no change to their signatures and no change to any stored data
  or any command; one file, no migration, nothing published outside the package.
- **`positions()` keys its result on `data["people"]` in recorded order**, rather than on the names
  that appear in expenses. This is what lets a person who has been added but has shared nothing be
  reported as zero and therefore left out of the list — the `Eve` case AC3 checks — and it is what
  gives ADR-0005's tie-break its order. **Reversible:** one line, and the ordering it provides is
  the only thing that depends on it.
- **A dataset whose positions do not sum to zero is settled as far as it can be and no further.**
  The loop stops when either pool empties, which terminates on any input. Such a dataset is only
  reachable by hand-editing the file, which EP-001's success measures say nobody should need to do
  [src: tracker/items/EP-001/item.md], and no criterion of this item covers it. **Reversible:**
  raising an `ExpensesError` instead is a two-line change in `settlement()` — but it would be new
  behaviour nobody asked for, which is why it is not in this plan.

## Decisions and ADRs

| decision | where it came from | recorded as |
|---|---|---|
| Which of the valid settlements to print, and in what order | not documented anywhere, and refinement explicitly left it here [src: EP-001/Q-002] — decided by the architect, not asked of the human, because it is reversible and no intent is at stake | **ADR-0005** |
| Amounts stay whole minor units end to end; nothing rounds | answered from the documents [src: ADR-0002; ADR-0003] | cited, no new ADR — there is no alternative worth naming, since a float here would contradict a decision already taken |
| The command's name, its lack of flags, the `no payments needed` string and the `X pays Y 0.00` line form | answered from the documents — refinement fixed all four and recorded them as its own, not the stakeholder's [src: tracker/items/WI-0002/artifacts/refinement-qa.md] | cited, no new ADR |
| Where the new code lives, and what `positions()` is keyed on | assumed, reversibly | `## Assumptions`, above |
| The test command | answered from the documents [src: ADR-0004] | `tracker/project.yaml` is already filled in and is unchanged by this item |

Nothing was asked of the human. Every decision above came from the first or second branch of the
preference order; none is irreversible, and none turns on intent no document records.

## Scaffolding

None. This plan creates no file outside `tracker/` and `docs/`. The test command already runs in
this project [src: ADR-0004] and `tests/` already has its `__init__.py`, so nothing needs a marker
file in order to execute.

## Risks

- **The expected outputs in AC1 and AC3 are pinned to ADR-0005's rule.** If the rule is ever
  replaced, those criteria have to change with it. This is a real cost and it was taken
  deliberately: an unpinned criterion cannot be decided by someone with a terminal, which is what
  put the item at Ready in the first place. ADR-0005 says so under reversibility.
- **`shares_minor` is trusted as stored.** `positions()` recomputes nothing, matching `store.py`'s
  existing behaviour on read [src: ADR-0003]. A hand-edited file therefore produces a report that
  faithfully reflects a wrong dataset. Accepted, and the same risk ADR-0003 already accepted.
- **A person can be named in an expense and later be absent from `data["people"]`.** No delivered
  command can produce that — `add_expense` refuses an unknown name [src: expenses/store.py] and
  nothing deletes a person yet — but WI-0004 will add deletion, and if it deletes a person without
  touching their expenses this report would silently drop them from the totals. That is WI-0004's
  problem to solve and its criteria's to state; it is named here so that WI-0004's plan inherits
  it rather than discovering it.
- **The list reshuffles when data changes.** Adding one expense can change several lines, because
  the matching restarts from the positions. Inherent to a settlement list; noted in ADR-0005.

## Out of scope for this item

- Recording that a payment was made, or any change to stored data. The command reads
  [src: WI-0002 AC5].
- Printing each person's net position. Offered to the stakeholder as option C of EP-001/Q-002 and
  not chosen; `positions()` exists as an internal function only, and no command exposes it.
- Any flag on `settle` — no filtering by date, person or trip.
- Deleting or amending a wrong record. That is WI-0004.
- Reading a bank CSV export. That is WI-0003, which is blocked on a sample
  [src: tracker/items/EP-001/questions/Q-001.md].
