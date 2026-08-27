# Plan — WI-0004 Delete a person or an expense recorded by mistake

## Problem

The tool records people and expenses and answers who owes whom, but nothing it writes can ever be
taken back: there is no command that removes a person or an expense, so a typo sits in every
settlement for ever and the only remedy is to hand-edit the JSON file
[src: tracker/items/WI-0004/item.md]. This item adds two commands — `person delete <NAME>` and
`expense delete <NUMBER>` — to the person keeping the group's costs, who is one person at a
terminal on one machine [src: docs/product/vision.md]. Three constraints shape it. The
stakeholder's: deleting a person who is named in a recorded expense must be **refused**, saying
what stands in the way, rather than cascading or leaving the data inconsistent
[src: WI-0004/Q-001]. Refinement's: an expense is addressed by its position in `expense list`,
which gains a leading number column, and the exact strings each command prints are fixed
[src: tracker/items/WI-0004/artifacts/refinement-qa.md]. The project's: python3 and its standard
library, no external services, one JSON file rewritten whole [src: ADR-0001; tracker/items/EP-001/item.md].
Nothing about the stored record shape changes and no migration is implied [src: ADR-0006].

## Approach

No new module. The change lands in the two layers that already exist for it, and the one-way
layering is unchanged [src: docs/architecture/overview.md]:

```
expenses/cli.py        gains `person delete` and `expense delete` subparsers and two handlers;
                       expense_list() gains the leading number column
expenses/store.py      gains delete_person() and delete_expense(); nothing else changes
expenses/settle.py     unchanged  [src: ADR-0007]
expenses/money.py      unchanged
```

**Where the rules live.** `store.py` is already the only module that knows what a valid dataset
is: `add_person` and `add_expense` raise `ExpensesError` before anything is appended, which is
what makes "a refusal changes nothing on disk" a property of the layering rather than a promise
each handler keeps [src: expenses/store.py]. The two new functions follow that shape exactly —
every check first, mutation last, `save()` called by the handler only after the function returns.

The functions this plan fixes. **Signatures and contracts are the architect's; the bodies are the
developer's:**

```python
# expenses/store.py

def naming_expenses(data, name):
    # The stored expenses that name `name`, as a list of (position, expense) pairs with
    # position 1-based in recorded order. A name is "named in" an expense when it is that
    # expense's paid_by, appears in its shared_by, or is a key of its shares_minor.
    # The union of the three is deliberate: shares_minor's keys are built from shared_by
    # by add_expense, so for a dataset this tool wrote the three agree — checking all three
    # means a hand-edited file cannot slip a reference past the refusal.

def delete_person(data, name):
    # Remove `name` from data["people"], or raise ExpensesError.
    #   - name missing, empty, or whitespace-only -> "..." is not in the group  (AC7)
    #   - naming_expenses(data, name) non-empty   -> the refusal of AC3
    # Names are compared exactly, as add_person compares them [src: expenses/store.py],
    # so `ana` does not match `Ana` and is the missing-name refusal (AC7).
    # Mutates data only when neither refusal applies.

def delete_expense(data, number):
    # Remove the expense at 1-based position `number` and return the removed dict, or raise
    # ExpensesError when number < 1 or number > len(data["expenses"]) (AC7).
    # `number` is an int; turning the command-line text into one is cli.py's job.
```

**The refusal message for AC3 is fixed here, not left to the developer**, because AC3 requires
the name and the count and `verify` must have one string to compare against. It is the string the
stakeholder was shown when they chose this behaviour [src: WI-0004/Q-001]:

```
Ben is named in 2 expense(s); delete those first
```

with `2` the length of `naming_expenses(data, name)` and the `(s)` literal, not pluralised. The
success lines are equally fixed by the criteria: `deleted Ben` [src: WI-0004 AC1] and
`deleted expense 2` [src: WI-0004 AC2], each one line on stdout, exit 0.

**Parsing `<NUMBER>` is `cli.py`'s job, not argparse's.** The subparser takes the argument as a
string, and the handler converts it, raising `ExpensesError("expense %r is not a positive whole
number" % text)` on anything that is not one. Declaring `type=int` would be less code but would
route `expense delete abc` through argparse's own error path — usage text on stderr and its own
exit code — while `expense delete 0` and `expense delete -1` came back as this tool's ordinary
refusals. AC7 requires all seven of its cases to behave the same way [src: WI-0004 AC7], and A2's
contract is that a refusal is one message on stderr and a non-zero exit
[src: tracker/items/WI-0001/artifacts/refinement-qa.md]. One path, one shape.

**The number column** is a change to `expense_list`'s output line, not to what it reads: the
position is `index + 1` over `store.expenses(data)`, which already returns the recorded order
[src: expenses/store.py; ADR-0006]. Two pieces of delivered work must move with it, and they are
steps in this plan rather than surprises: one WI-0001 test that reads the amount as
`line.split()[1]` [src: tests/test_cli.py], and the README's sample output [src: README.md].

## Steps

1. **`expenses/store.py` — add `naming_expenses(data, name)`.** A module-level function beside
   `expenses(data)`, returning 1-based `(position, expense)` pairs for every stored expense whose
   `paid_by`, `shared_by` or `shares_minor` keys include the exact name. Afterwards: nothing in
   the tool's behaviour has changed, and the function can be exercised directly from a test with
   a hand-built dataset dict.

2. **`expenses/store.py` — add `delete_person(data, name)`.** Strips the name; refuses an empty
   one and a name not in `data["people"]` with the same "is not in the group" shape `add_expense`
   already uses [src: expenses/store.py]; refuses with the AC3 string when `naming_expenses` is
   non-empty; otherwise removes the name from `data["people"]` and returns the stripped name.
   Afterwards: the refusals of AC3 and of AC7's person cases are decided in one place, and no
   caller can perform a deletion that breaks ADR-0007's invariant.

3. **`expenses/store.py` — add `delete_expense(data, number)`.** Refuses `number < 1` and
   `number > len(data["expenses"])` with a message naming the number; otherwise pops and returns
   the expense at `number - 1`. Afterwards: the out-of-range cases of AC7 are decided, and the
   renumbering AC2 requires is a consequence of the list rather than a separate operation.

4. **`expenses/cli.py` — add the two subparsers.** Under the existing `person` and `expense`
   nouns, a third action each: `person delete` taking a positional `name`, `expense delete`
   taking a positional `number` **as a string**. Register both in `HANDLERS` under
   `("person", "delete")` and `("expense", "delete")`. Afterwards: `python3 -m expenses person
   delete --help` and `expense delete --help` both work, and `python3 -m expenses expense` with
   no action still exits non-zero as it does today.

5. **`expenses/cli.py` — add the two handlers.** Each loads the store, calls its `store` function,
   calls `store.save()` **only on success**, and prints its one line to `out`. `person_delete`
   prints `deleted %s` with the stripped name; `expense_delete` converts its argument to an int
   first — raising `ExpensesError` per `## Approach` if it is not a positive whole number — and
   prints `deleted expense %d` with the number that was given. Afterwards: AC1, AC2, AC4 and AC7
   are all reachable from the command line, every refusal exits through the existing
   `ExpensesError` path in `main()` [src: expenses/cli.py], and no refusal has called `save()`.

6. **`expenses/cli.py` — add the number column to `expense_list`.** Prepend the 1-based position
   and two spaces to each line, leaving every existing field and the `no expenses` case untouched.
   Afterwards: `expense list` prints `1  2026-08-01  30.00  paid by Ana  shared by Ana,Ben  Taxi`,
   the empty case still prints `no expenses`, and AC2's first-field requirement holds.

7. **`tests/test_cli.py` — repair the WI-0001 test the column breaks.**
   `AC3ExpenseListShowsEveryField.test_expenses_are_listed_in_the_order_they_were_recorded` reads
   the amount as `line.split()[1]`; it becomes `line.split()[2]` [src: tests/test_cli.py].
   Afterwards: `python3 -m unittest discover -s tests -t .` passes on the WI-0001 and WI-0002
   suites with the column in place. Change nothing else about that test — it is WI-0001's
   evidence, and rewriting it would be editing a delivered criterion's proof.

8. **`tests/test_store.py` — cover the three new store functions directly.** `naming_expenses`
   against a dataset where a name is payer only, sharer only, both, and neither; `delete_person`
   refusing the in-use name, the unknown name, the wrong case and the empty name, and succeeding
   on an unused one; `delete_expense` at the first, last, out-of-range and zero positions. Each
   refusal asserts that `data` is unchanged. Afterwards: the rules of ADR-0007 are pinned without
   going through the command line.

9. **`tests/test_cli.py` — add a class per acceptance criterion**, following the existing
   `AC<n><what>` naming [src: tests/test_cli.py]. AC1, AC2, AC3, AC4, AC6 and AC7 through
   `main()` with a temporary store; AC5 through the existing `subprocess` helper that runs a
   fresh `python3 -m expenses` [src: tests/test_cli.py]. AC3 and AC7 assert the data file's bytes
   are unchanged across the attempt, and AC7's empty-store cases assert the file does not exist
   afterwards. Afterwards: every criterion except AC8 has a test that fails without the change.

10. **`README.md` — document both commands.** Replace the `expense list` sample with the numbered
    form; add a `person delete` and an `expense delete` section with a worked example each; state
    that deleting a person named in an expense is refused and the expenses must go first; state
    that the numbers renumber after a deletion. Afterwards: AC8's four checks all pass on a read.

11. **Run the gate command** — `python3 -m unittest discover -s tests -t .` — and confirm it
    passes on the final state of the code, not on an earlier one.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `person delete Ben` with no expenses prints `deleted Ben`; `person list` prints `Ana` | 2, 4, 5 | a `tests/test_cli.py` class asserting exit 0, stdout exactly `deleted Ben\n`, and `person list` stdout exactly `Ana\n` |
| AC2 — numbered listing; `expense delete 2` prints `deleted expense 2`; the rest renumber; the last deletion leaves `no expenses` | 3, 4, 5, 6 | a `tests/test_cli.py` class building the TWO-EXPENSE STORE, asserting the first fields are `1` and `2`, then the exact stdout of the deletion, then the one remaining line beginning `1`, then `no expenses` |
| AC3 — `person delete Ben` and `person delete Ana` refused, stdout empty, stderr names the person and `2`, file bytes unchanged | 1, 2, 5 | a `tests/test_cli.py` class asserting non-zero exit, empty stdout, stderr containing the name and `2`, `Path.read_bytes()` equal before and after, and `person list` still showing both |
| AC4 — with the expenses gone, `person delete Ben` exits 0 and prints `deleted Ben` | 1, 2, 3, 5 | the same class, after two `expense delete 1` calls: exit 0, exact stdout, `person list` exactly `Ana\n` |
| AC5 — deletions survive the process exiting | 5 | a class using the existing `run_in_a_new_process` helper, comparing the fresh process's stdout bytes with the in-process listing's [src: tests/test_cli.py] |
| AC6 — `settle` before and after a deletion; the refusal leaves `settle` unchanged | 3, 5 | a `tests/test_cli.py` class asserting `Ben pays Ana 15.00`, then `no payments needed` after `expense delete 1`, and byte-identical `settle` output across a refused `person delete Ben` |
| AC7 — nine refusals against the two-expense store and two against an empty one | 2, 3, 5 | a class looping the nine argument vectors, each asserting non-zero exit, empty stdout, non-empty stderr and unchanged file bytes; plus two empty-store cases asserting the store path does not exist afterwards |
| AC8 — README documents both commands, the numbered sample, the refusal and the renumbering | 10 | reading `README.md` for the four things AC8 names; the existing README tests show the shape this project already uses for that [src: tests/test_cli.py] |

## Assumptions

- **The AC3 refusal message is `<name> is named in <n> expense(s); delete those first`.** Taken
  from the option the stakeholder chose, where that exact string was shown to them
  [src: WI-0004/Q-001]. AC3 constrains only that the message contain the name and the count
  [src: WI-0004 AC3], so the rest is this plan's choice. Reversing it is one string literal in
  `expenses/store.py` and the tests that assert it — one file each, no data, no interface.
- **`naming_expenses` checks `shares_minor`'s keys as well as `paid_by` and `shared_by`.** For any
  dataset this tool wrote the three agree, because `add_expense` builds `shares_minor` from
  `shared_by` [src: expenses/store.py], so the extra check costs nothing and only ever refuses
  more. Reversing it is one expression in one function.
- **`expense delete` reports the number the person typed**, not the position in some canonical
  order — they are the same thing under ADR-0006, and this only matters if that ADR is ever
  superseded. Reversing it is one format string.
- **No test is added for AC8.** It is a documentation criterion checked by reading, and `verify`
  reads it. The project has precedent for asserting README content from a test
  [src: tests/test_cli.py]; adding one here would pin wording that AC8 deliberately leaves open.
  Reversing it is a new test class and nothing else.

## Decisions and ADRs

- **How a single expense is addressed** — `ADR-0006`. Refinement had recorded the position-based
  handle as an assumption for an architect to confirm; this execution confirmed it against the
  two alternatives it rejected and recorded the data-format and stable-output consequences that
  refinement could not weigh. Route: **decided**, and the ADR states its reversibility.
- **Where the people-and-expenses invariant is enforced** — `ADR-0007`. The stakeholder decided
  the *behaviour* [src: WI-0004/Q-001]; the ADR decides which layer holds it, and records
  explicitly that `settle.positions()` is left alone and that the guarantee does not extend to
  data this tool did not write — which is the fact WI-0003 will need. Route: **decided**.
- **Refusals go through `ExpensesError`, not argparse's `type=`** — recorded in `## Approach`
  above with its reasoning. Route: **documented** — it follows from the tool's existing refusal
  contract [src: tracker/items/WI-0001/artifacts/refinement-qa.md] and needs no ADR, because the
  alternative is not a decision about the system, only about which code path a refusal takes.
- **No question was put to the human.** Nothing in this plan is irreversible and nothing turns on
  intent no document records: the one decision that did was asked and answered before this item
  was Ready [src: WI-0004/Q-001]. Route: **none asked**.

## Scaffolding

`none`. Both test modules already exist and `commands.test` already runs
[src: tracker/project.yaml].

## Risks

- **The number column changes output that WI-0001 delivered.** It breaks no WI-0001 acceptance
  criterion — AC3 asks for the fields and the recorded order, both untouched [src: WI-0001 AC3] —
  but it does break one WI-0001 test, and step 7 repairs it. The risk is that the repair is
  mistaken for licence to adjust other WI-0001 tests; it is not. If any other WI-0001 or WI-0002
  test fails after step 6, that is a real regression and the change is wrong, not the test.
- **`person delete` deleting the *last* person, or an expense's sharers becoming empty.** Neither
  can happen: `delete_person` refuses while any expense names the person [src: WI-0004 AC3], so
  no stored expense can lose a sharer, and a group with no expenses can be emptied of people
  harmlessly. Stated because it is the first thing a reader worries about.
- **`settle` after a person is deleted.** Covered by AC6 and safe by construction under ADR-0007:
  the only person who can be deleted is one no expense names, whose position is 0
  [src: expenses/settle.py]. Their disappearance cannot change any payment.
- **AC7's empty-store cases require that a refusal creates no file.** `store.save()` is what
  creates the parent directory and the file [src: expenses/store.py], and step 5 calls it only on
  success — so this holds by the same layering that makes every other refusal leave the disk
  alone. The risk is a handler that saves unconditionally, which is why step 5 names it.
- **This plan does not touch `store.VERSION` or the stored record shape** [src: ADR-0006]. If a
  step appears to need to, the plan is wrong and the item should come back, not be widened.

## Out of scope for this item

Everything in the item's `## Out of scope` [src: tracker/items/WI-0004/item.md], and in
particular: no `--and-their-expenses` cascade flag, which the stakeholder was offered and declined
[src: WI-0004/Q-001]; no confirmation prompt; no stable expense identifier; no undo and no record
of what was deleted; no editing in place. Two further exclusions belong to this plan rather than
the item: `store.load()` gains **no** consistency check — that is option B of ADR-0007 and was
rejected [src: ADR-0007] — and `settle.positions()` is **not** changed, for the same reason
[src: ADR-0007]. And the defect BUG-0002 records, a write the operating system refuses escaping as
a traceback [src: BUG-0002], is not fixed here even though `delete` adds two more callers of
`store.save()`; it has its own item and widening this plan would make both unverifiable.
