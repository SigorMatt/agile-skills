# Implementation report — WI-0004

## What was built

Two subcommands, `add-payment` and `payments`, the fourth key in the record, and four lines in
`net_positions`. No new module. `who-owes-whom`, `settle` and `shares_of` are untouched.

| file | changed | what |
|------|---------|------|
| `expenses/storage.py` | yes | `payments` in `empty_record()`; `_is_payment` shape check in `load()` |
| `expenses/group.py` | yes | `payments(record)`, `add_payment(...)`, and the second loop in `net_positions` that folds payments in (`ADR-0011` point 2) |
| `expenses/cli.py` | yes | `_add_payment`, `_payments`, and the last two entries in `COMMANDS` — the seven subcommands `ADR-0006` fixed are now all present |
| `tests/test_payments.py` | new | AC1, AC3–AC15, 16 tests |
| `tests/test_who_owes_whom.py` | yes | plan steps 5 and 6 — see below |
| `tests/test_persistence.py` | yes | AC2 as real subprocesses |

The record now holds all four kinds of fact the product promises, and nothing else:

```json
{"version": 1,
 "people":   ["Alice", "Bob", "Carol"],
 "expenses": [{"paid_by": "Alice", "shares": [{"person": "Alice"}, …], "total": 3000}],
 "payments": [{"amount": 1000, "from": "Bob", "to": "Alice"}]}
```

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `_add_payment` validates, saves, prints the confirmation | `test_payments.py::RecordingTest::test_a_payment_is_recorded_and_confirmed` — asserts `(0, "Recorded 10.00 paid by Bob to Alice.\n", "")` |
| AC2 | `storage.save` / `load` on the `payments` key | `test_persistence.py::test_a_payment_recorded_by_one_process_is_there_for_another` — five separate `python3 -m expenses` **processes**; the fourth prints `1. Bob paid Alice 10.00`, the fifth prints `Carol pays Alice 10.00` |
| AC3 | `_payments` numbers from 1, past tense, `money.format_amount` | `RecordingTest::test_payments_are_listed_in_the_order_recorded` — one payment, then two, asserting both listings exactly, including `2. Carol paid Sam Okafor 2.50` |
| AC4 | `_payments` prints the empty line when there are none | `RecordingTest::test_nothing_recorded_says_so_and_succeeds` — `(0, "No payments have been recorded yet.\n", "")` |
| AC5 | the second loop in `net_positions` | `SettlementTest::test_a_full_payment_removes_that_debt` — asserts the two-transfer output **before** the payment and the single-transfer output after |
| AC6 | as above, with a partial amount | `SettlementTest::test_a_part_payment_reduces_the_debt_by_what_was_paid` — `Carol pays Alice 10.00\nBob pays Alice 6.00\n`, Carol first because her debt is now larger |
| AC7 | positions all reach zero, so `settle` returns nothing | `SettlementTest::test_payments_that_cover_every_debt_leave_everybody_settled` — `Everybody is settled up.` |
| AC8 | an overpayment is accepted; positions reverse | `SettlementTest::test_overpaying_is_accepted_and_reverses_the_direction` — exits `0`, then `Alice pays Bob 10.00\nCarol pays Bob 10.00\n` |
| AC9 | both people resolved through `find_person` | `RefusalTest::test_a_person_who_is_not_in_the_group_is_refused` — unknown as `--from` and as `--to`, each refused, with `payments` and `people` unchanged; `test_a_known_person_typed_differently_is_accepted` — `--from "sam okafor"` succeeds and lists as `Sam Okafor` |
| AC10 | identity keys compared after both are resolved | `RefusalTest::test_a_payment_to_oneself_is_refused` — `Alice`, `ALICE` and `  alice  ` against `Alice`, all three refused |
| AC11 | `money.parse_amount` then the sign check | `RefusalTest::test_a_malformed_or_out_of_range_amount_is_refused` — four subtests, each asserting the pinned stderr |
| AC12 | `_options` and the arity checks | `RefusalTest::test_the_command_line_is_checked` — six subtests, one per bullet |
| AC13 | nothing is saved until every rule has passed | `RefusalsRecordNothingTest` — twelve refusals against a record holding an expense and a payment; after each, `payments`, `expenses`, `people` **and `who-owes-whom`** all print exactly what they printed before, and stderr never contains a traceback. **Plus** `RefusalLeavesNoFileTest` — on a record with no file at all, three refusals each leave no file behind |
| AC14 | `load` preserves `people` and `expenses` untouched | `RecordingTest::test_people_and_expenses_are_undisturbed` — `people` prints the four names in order and `expenses` prints byte-identically to before the payment |
| AC15 | a payment with no expense behind it still moves positions | `SettlementTest::test_a_payment_with_no_expense_behind_it_is_owed_back` — `Alice pays Bob 10.00\n` |

### The two instructions from earlier reviews (plan steps 5 and 6)

Neither is an acceptance criterion — `refine` was right that neither is observable through a
command — so both are reported here rather than in the table above.

- **Step 5, from WI-0003's review:** `test_who_owes_whom.py::NetPositionsContractTest::
  test_everybody_is_returned_in_the_order_they_were_added` asserts that `net_positions` returns
  everybody, including a person at zero, in the order they were added. Following `plan.md`
  § *Risks*, the people are `Zoe`, `alice`, `Mo`, `Bea` — an added order that matches neither
  alphabetical order nor the order of their positions — so the test cannot pass by coincidence.
  `Bea` is in nothing and stays at `0`.
- **Step 6, from WI-0003's review:** `DeterminismAndPurityTest`'s fixture now holds **two
  expenses and two payments**, with different amounts, where WI-0003's held one expense. A
  rewrite that merely reordered either list is now detectable. Added
  `test_neither_listing_command_modifies_the_record_either`, which makes the same assertion for
  `expenses`, `payments` and `people`.

### Every mutation was caught, including the three that escaped on earlier items

Fifteen mutations, applied to the real source, run against the whole suite, reverted. **All
fifteen caught.** The three worth naming are the ones that map to gaps two earlier reviews
recorded:

| mutation | previously | now |
|----------|-----------|-----|
| save the record before validating (a refusal creates a file) | **survived** on WI-0002 | caught by `RefusalLeavesNoFileTest` |
| sort `net_positions` by amount instead of insertion order | **survived** on WI-0003 | caught by `NetPositionsContractTest` |
| reorder and rewrite the record during `who-owes-whom` | **survived** on WI-0003 | caught by `test_the_record_is_not_modified`, on the two-expense fixture |

The rest: the confirmation wording (3 tests), never saving the payment (8), swapping `from` and
`to` in the listing (3), the empty-listing message (2), the **sign** of the payment fold (5),
double-counting each payment (6), ignoring payments entirely (6), skipping the recipient's
membership check (1), allowing a self-payment (2), allowing a zero or negative amount (2),
ignoring a missing `--to` (2), and dropping the `payments` key on save (8).

The sign, double-count and ignore mutations are the three that `plan.md` § *Risks* said would
either fail loudly or fail asymmetrically. They fail loudly: five, six and six tests.

## Deviations from the plan

1. **`RefusalLeavesNoFileTest` is a plain `unittest.TestCase`, not an `ExpenseTestCase`.** The
   plan required a record with no file, and every `ExpenseTestCase` adds four people in `setUp`,
   which creates one. It therefore repeats the temporary-directory and `EXPENSES_FILE` setup by
   hand. This is exactly the trap `plan.md` § *Risks* names, and the class docstring says so.
2. **AC13's test also asserts `who-owes-whom` is unchanged**, not only the three listings. It
   costs one line and it is the output a user would actually notice going wrong.
3. **`group.__all__` gained four names** — `net_positions`, `settle`, `add_payment`, `payments`.
   The list was written in WI-0002 and WI-0003 did not update it, so it was already out of date
   before this item. Adding this item's two names without the other two would have left it
   wrong in a new way. Naming it as a deviation because it touches a line no criterion covers.

No acceptance criterion was edited. Nothing in the plan was skipped.

## Gates

Run on the branch head, after the last code change.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 115 tests`, `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses tests` → exit 0 (`ADR-0008`: a syntax check) |
| `workspace-valid` | **pass** | `validate-workspace` → exit 0 once this report and the journal entry exist |
| `every-criterion-has-a-test` | **pass** | the table above names a test for each of AC1–AC15; fifteen mutations show they bite |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → exit 0 |
| `no-unplanned-scope` (advisory) | **pass, with three declared deviations** | every hunk traces to a plan step and a criterion; `who-owes-whom`, `settle` and `shares_of` are untouched, as the plan's out-of-scope list required |

## What I did not do

- **Nothing links a payment to the debt it discharges**, so recording the same payment twice looks
  exactly like two payments that really happened and the tool believes it. `ADR-0011`
  § *Consequences* and `plan.md` § *Risks* both say so; no criterion covers it.
- **No duplicate detection, no reset, no correction command, no description on a payment.** All
  are in the item's `## Out of scope`.
- **`payments` and `expenses` still do not share a listing helper** (plan assumption 2). The two
  lines differ in every part except the numbering.
- **The `payments` key is written into the record the first time anything is saved**, including by
  `add-person`, because `empty_record()` now contains it. A record written by an earlier item and
  never re-saved keeps its old shape and still loads — `_is_payment` is only applied to a key that
  is present.
- **I did not touch WI-0003's `settle` or `who-owes-whom`,** and the five settlement criteria here
  pass because the inputs changed, not the algorithm. That was the plan's central claim and it
  held.
