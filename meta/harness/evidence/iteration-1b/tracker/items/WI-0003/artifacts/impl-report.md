# Implementation report — WI-0003

## What was built

One subcommand, `who-owes-whom`, and the two functions behind it. No new module, no new stored
data, nothing written to the record.

| file | new or changed | what it is |
|------|----------------|------------|
| `expenses/group.py` | changed | `net_positions(record)` — what each person paid out less what they owe, everybody included, in the order they were added; `settle(record)` — the transfers, by the procedure the criteria pin |
| `expenses/cli.py` | changed | `_who_owes_whom` and a fifth entry in `COMMANDS` |
| `tests/test_who_owes_whom.py` | new | AC1–AC12, 16 tests |
| `tests/test_persistence.py` | changed | AC9 across two separate processes |

`net_positions` takes each sharer's share from the existing `group.shares_of`, so `ADR-0003`'s
rounding rule is applied in exactly one place in the codebase — which is what keeps it as cheap to
change as the human was promised. `settle` recomputes the largest debtor and the largest creditor
on each pass, so the tie-break by identity key applies at every step rather than once at the
start.

## Acceptance criteria evidence

Test names are given without their class where unambiguous. `run_cli` is the in-process helper;
`invoke` in `test_persistence.py` runs a real `python3 -m expenses` process.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `_who_owes_whom` prints the settled line when `settle` returns nothing; a missing record loads as empty | `test_who_owes_whom.py::NothingToSettleTest::test_an_empty_record_is_settled` — a bare `CliTestCase` with no people at all; asserts `(0, "Everybody is settled up.\n", "")` |
| AC2 | as above | `SettledTest::test_people_but_no_expenses_are_settled` |
| AC3 | `net_positions` returns all zeros, so `settle` returns nothing | `SettledTest::test_expenses_that_balance_are_settled` — the two-expense record from the criterion |
| AC4 | `settle`'s greedy loop with the identity-key tie-break | `TransfersTest::test_one_creditor_two_debtors` — stdout is exactly `Bob pays Alice 10.00\nCarol pays Alice 10.00\n`. `TieBreakTest` proves the order is the *name*'s doing: one test adds `Carol` before `Bob` and still expects Bob first, the other uses `alice`/`bob`/`CAROL` so that only a case-folded key gives the pinned order |
| AC5 | `net_positions` via `shares_of`, so the 3.34/3.33/3.33 split flows through | `TransfersTest::test_an_uneven_split_settles_to_the_penny` — asserts the positions are `{Alice: 666, Bob: -333, Carol: -333, Sam Okafor: 0}` **and** that stdout is exactly `Bob pays Alice 3.33\nCarol pays Alice 3.33\n` |
| AC6 | the greedy pairs by position, not by shared history | `TransfersTest::test_a_transfer_may_name_two_people_who_never_shared` — stdout is exactly `Carol pays Alice 15.00\n` |
| AC7 | `settle` reduces both positions by each transfer | `PropertiesTest::test_paying_every_transfer_leaves_everybody_at_zero` — applies every printed transfer to `net_positions` and asserts all are zero, over **seven** records: the three from the criteria plus a mixed-stated-share case, a four-person case, one debtor with two creditors, and two debtors with two creditors |
| AC8 | each transfer zeroes at least one person | `PropertiesTest::test_at_most_one_fewer_transfers_than_people_with_a_position` — the same seven records |
| AC9 | nothing in the computation depends on anything but the record | `DeterminismAndPurityTest::test_two_runs_produce_identical_output` in process, and `test_persistence.py::test_who_owes_whom_is_the_same_in_a_separate_process` for a real second process |
| AC10 | the handler calls `storage.load()` and never `storage.save()` | `DeterminismAndPurityTest::test_the_record_is_not_modified` — the record file's bytes read before and after, asserted equal |
| AC11 | the handler refuses any argument | `ArgumentsTest::test_who_owes_whom_takes_no_arguments` — exit non-zero, stderr exactly `who-owes-whom takes no arguments.\n`, stdout empty, no traceback |
| AC12 | `settle` drops zero positions before the loop | `TransfersTest::test_a_person_at_zero_is_not_named` — asserts Bob's position is `0` and that `"Bob"` does not appear in stdout |

### The tests were measured, and one mutation found a real hole

Thirteen mutations, applied to the real source, run against the whole suite, reverted. The first
pass caught eleven and **two survived**:

| mutation | first pass | after the fix |
|----------|-----------|---------------|
| `settle` pays the debtor's **whole** debt to one creditor instead of the smaller of the two amounts | **survived** | caught by `test_one_debtor_owing_two_creditors_splits_the_payment` |
| `settle` keeps zero-position people in the loop | **survived** | still survives — behaviour-preserving, see below |
| the settled message, and its exit status | caught (3 tests each) | |
| the transfer line with debtor and creditor swapped | caught (6) | |
| the tie-break ignoring the name entirely | caught (2) | |
| the tie-break comparing raw spelling instead of the identity key | caught (1) | |
| `net_positions` ignoring the payer's outlay, or what sharers owe | caught (15 and 9) | |
| emitting each transfer twice | caught (7) | |
| saving the record after computing | caught (1) | |
| accepting arguments | caught (1) | |
| computing shares by division instead of through `shares_of` | caught (3) | |

**The first survivor was a real gap and is now closed.** Every record in the suite had a single
creditor, so `min(-debt, credit)` and `-debt` were always the same number. `plan.md` § *Risks*
named exactly this — "a single-creditor case exercises neither the multi-creditor branch of the
loop nor the case where a debtor's payment is split" — and the first draft of these tests did not
cover it anyway. Added `test_one_debtor_owing_two_creditors_splits_the_payment` (Bob owes 30 to two
creditors owed 15 each; the output is two transfers of 15.00) and two more records to the property
tests. Re-running the mutation now fails that test.

**The second survivor is behaviour-preserving.** Leaving zero positions in `settle`'s working set
changes no output: the largest-debt and largest-credit selections are unaffected by zeros, and the
loop's guard — "stop when the extreme debtor is not in debt or the extreme creditor is not owed" —
fires as soon as only zeros remain. The filter is there for clarity and to make the guard a
backstop rather than the terminator. Recorded rather than papered over.

## Deviations from the plan

1. **`settle` carries a guard the plan did not name.** If the largest debtor is not actually in
   debt, or the largest creditor is not actually owed, the loop stops. This is only reachable for
   a hand-edited record whose positions do not sum to zero — the case `plan.md` § *Risks*
   discusses. **It is not the guard the plan told me not to add.** The plan forbade adding a
   *check* that reports or refuses such a record; this is a loop-termination condition, without
   which `while owing` would spin forever on that input rather than doing anything at all. It
   emits no message, changes no valid output, and the comment in the source says exactly this.
   Flagged because it is the one place I came closest to the line the plan drew.
2. **`net_positions` uses `position.get(person, 0)`** rather than assuming every name in an
   expense is in `people`. For any record the tool wrote they always are. For a hand-edited one
   they need not be, and the alternative is a `KeyError` traceback, which `ADR-0001` point 3
   rules out for anything a user can provoke.
3. **The tie-break for the creditor is written as `min` over `-amount`** rather than `max`, so
   that the identity key sorts ascending on both sides with the same expression. The first draft
   used `max` with a negated-name key, which worked and was unreadable.

No acceptance criterion was edited. Nothing in the plan was skipped.

## Gates

Run on the branch head, after the last code change.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 96 tests`, `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses tests` → exit 0. `ADR-0008`: a syntax check, not a linter |
| `workspace-valid` | **pass** | `validate-workspace` → exit 0 once this report and the journal entry are written; it reported `journal.execution.missing` in between, which is expected while an execution is in flight |
| `every-criterion-has-a-test` | **pass** | the table above names a test function for each of AC1–AC12; the thirteen mutations are the evidence that those tests bite, including the one that did not until it was fixed |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → exit 0 |
| `no-unplanned-scope` (advisory) | **pass, with three declared deviations** | every hunk traces to a plan step and a criterion; the three deviations above are the only additions, and the first is the one worth a reviewer's attention |

## What I did not do

- **No guard against a hand-edited record whose net positions do not sum to zero.** The plan is
  explicit that this is not mine to add and that wanting one is a question for the architect. I do
  not want one badly enough to file the question: nothing the tool writes can produce that record.
  The loop-termination condition in deviation 1 means such a record produces a short, wrong
  settlement rather than hanging — which is what the plan's risk describes as the current
  behaviour.
- **No payments, no pairwise view, no caching.** WI-0004 extends `net_positions`; nothing here
  anticipates it.
- **AC10 is weaker than it looks and I did not strengthen it.** Comparing the record file's bytes
  catches a rewrite only if the serialisation differs; a byte-identical rewrite would pass. The
  plan says so. The real assurance is that `_who_owes_whom` is eleven lines and calls no `save`.
- **`net_positions` is O(expenses × sharers) per call and `settle` calls it once.** Nothing
  caches. At this product's size that is irrelevant, and `ADR-0003` point 6 is the reason not to
  store anything derived.
