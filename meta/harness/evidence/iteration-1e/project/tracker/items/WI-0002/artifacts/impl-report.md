# Implementation report — WI-0002

## What was built

One read-only command, `python3 -m expenses settle`, and the arithmetic behind it. Four commits
on `wi/WI-0002`, branched from `main` at `55536ec`:

| commit | step | what |
|---|---|---|
| `1e6853b` | 1 | `expenses/settle.py` (new) with `positions()`, and `tests/test_settle.py` (new) |
| `35ba9b9` | 2 | `settlement()` in the same module, implementing ADR-0005, with its tests |
| `0982ced` | 3, 5, 6 | the `settle` subcommand and handler in `expenses/cli.py`, the end-to-end tests in `tests/test_cli.py`, and the `### settle` section of `README.md` |
| `b873060` | 7 | `docs/architecture/overview.md` v2 → v3: `settle.py` moves out of "What is coming" into the diagram, the layering rule and a piece of its own |

`expenses/settle.py` is 60 lines and holds two functions. `positions(data)` returns each recorded
person's net in whole minor units, keyed on `data["people"]` in recorded order so that someone who
neither paid nor shared is reported as zero rather than being absent. `settlement(data)` applies
ADR-0005 — repeatedly match the largest debt against the largest credit, ties in both pools broken
by the order people were recorded — and returns `[(payer, receiver, amount_minor), ...]` in the
order generated. It imports nothing from `store.py` or `cli.py`, does no I/O and prints nothing.

`cli.py` gains a third top-level subparser and one handler, `settle_report`, which loads the
dataset, calls `settlement`, and prints either the single line `no payments needed` or one line
per payment as `Ben pays Ana 10.00`. It calls nothing that writes.

The test suite went from 50 tests to 86: 20 new in `tests/test_settle.py` over the pure functions,
13 new in `tests/test_cli.py` over the command, and 3 over the README.

## Acceptance criteria evidence

Every command below was run on the branch head, `b873060`, with `EXPENSES_STORE` pointing into a
fresh temporary directory. Output is quoted as it was printed.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| **AC1** — three people, one 30 expense, two expected lines | `settlement()` returns `[("Ben","Ana",1000),("Cara","Ana",1000)]`; the handler formats each with `format_amount` | `tests/test_cli.py::WI0002AC1SettleListsThePayments::test_thirty_shared_by_three_settles_with_two_payments_of_ten` asserts `sorted(stdout.splitlines()) == ["Ben pays Ana 10.00", "Cara pays Ana 10.00"]`. Run by hand: `person add Ana/Ben/Cara`, `expense add --amount 30 --paid-by Ana --shared-by Ana,Ben,Cara`, then `settle | sort` → `Ben pays Ana 10.00` / `Cara pays Ana 10.00`, exit 0. `tests/test_settle.py::SettlementTest::test_ac1_tie_between_two_equal_debts_goes_to_whoever_was_recorded_first` pins the pairing at the function level, and `::test_ac1_reversing_the_recorded_order_reverses_the_payments` shows the recorded-order tie-break is what decides it |
| **AC2** — three ways to have nothing to settle | The handler prints `no payments needed` whenever `settlement()` is empty | `tests/test_cli.py::WI0002AC2NothingToSettle`, three tests — `test_an_untouched_store_needs_no_payments`, `test_people_but_no_expenses_needs_no_payments`, `test_a_group_already_square_needs_no_payments` — each asserting `out == "no payments needed\n"` and code 0. Run by hand against three stores: an untouched one, one with `Ana` and `Ben` and no expense, and one whose only expense is `--amount 10 --paid-by Ana --shared-by Ana`. All three printed `no payments needed` and exited 0 |
| **AC3** — five-person dataset, exact three lines and four properties | `positions()` gives `{"Ana": 1666, "Ben": -133, "Cara": -933, "Dan": -600, "Eve": 0}`; `settlement()` turns those into three payments | `tests/test_cli.py::WI0002AC3TheListSettlesTheGroupExactly`, six tests, one per clause: the exact three sorted lines; every amount greater than zero; no name both a payer and a receiver; `Eve` appearing nowhere in stdout; exactly three lines; and the three amounts summing to 1666 minor units. `tests/test_settle.py::SettlementTest` asserts the same six at the function level plus `test_ac3_the_payments_settle_every_person_exactly`, which checks that what each person pays out net equals the debt their position records. Run by hand: `settle \| sort` → `Ben pays Ana 1.33` / `Cara pays Ana 9.33` / `Dan pays Ana 6.00`, three lines |
| **AC4** — byte-identical across two processes | Determinism comes from ADR-0005's tie-break, not from dictionary order | `tests/test_cli.py::WI0002AC4TheSameDataPrintsTheSameBytes::test_two_fresh_processes_print_byte_identical_stdout` runs `python3 -m expenses settle` twice through `subprocess.run` against the same store and asserts the two `stdout` values are equal as bytes. Run by hand on AC3's store: `settle > a.txt`, `settle > b.txt`, `cmp a.txt b.txt` → no output, exit 0 |
| **AC5** — the command changes nothing | `settle_report` calls `store.load` and never `store.save`, and `load` returns the empty dataset for a missing file without creating one | `tests/test_cli.py::WI0002AC5SettleChangesNothing::test_the_data_file_is_unchanged_across_a_settle_run` compares `hashlib.md5` of the file either side of a run; `::test_settle_creates_no_data_file_where_none_exists` asserts exit 0, `no payments needed`, and `not store.exists()` afterwards. Run by hand: `md5sum` before and after a `settle` on AC3's store, both `ad65189c9362a13c953dee6d87db2a49`; and `EXPENSES_STORE` pointed at a non-existent path → `no payments needed`, exit 0, `test ! -e` still true |
| **AC6** — the README documents it | `README.md` gains a `### settle` section, and its opening paragraph no longer says who-owes-whom is out of this version | `tests/test_cli.py::WI0002AC6TheReadmeDocumentsTheCommand`, three tests: the command name appears, a payment line matching `\w+ pays \w+ \d+\.\d\d` appears, and `no payments needed` appears. These three **failed** when the suite was run after step 5 and before step 6 — `AssertionError: 'python3 -m expenses settle' not found` — and passed after it, which is the evidence that they test the README rather than merely coexisting with it |

## Deviations from the plan

Three, all in *how* rather than *what*. Nothing delivered differs from what the plan specified.

1. **Tests were written with each change rather than as steps 4 and 5.** The plan puts
   `tests/test_settle.py` at step 4, after both functions exist. In fact `positions()`' tests
   landed with `positions()` in `1e6853b` and `settlement()`'s with `settlement()` in `35ba9b9`,
   which is what this skill's procedure asks for — the test comes with the change, in the same
   commit. Same files, same coverage, earlier.
2. **Steps 3, 5 and 6 landed in one commit rather than three.** AC6's tests assert on
   `README.md`, so committing the command and its tests before the README would have left
   `0982ced`'s predecessor with a failing suite. Splitting the documentation out would have made
   an intermediate commit red for a reason unrelated to the code in it.
3. **`tests/test_settle.py` holds twenty tests where the plan named nine cases.** The extra
   eleven are the plan's own cases split one assertion per test — AC3's four properties are four
   tests rather than one — plus two the plan implies but does not list: a two-creditor dataset,
   which is the only shape where ADR-0005's creditor-side tie-break is exercised at all, and the
   recorded-order-swapped variant of AC1. No new behaviour was built for either.

One thing the plan predicted and got right, recorded because it would otherwise look like a
deviation: `settle` has no sub-action, so its subparser sets `action=None` and its handler is
registered under `("settle", None)`. Without that the command raises `AttributeError`. The plan
names this in `## Approach`; it is implemented exactly as written.

## Gates

All run on the branch head, `b873060`, after the last change.

| gate | result | evidence |
|---|---|---|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → `Ran 86 tests`, `OK`, exit 0 |
| `lint-clean` | **skipped** | `commands.lint` is `null` in `tracker/project.yaml`. ADR-0004 records why: the project installs nothing, the standard library ships no linter. The gate checked nothing and is not reported as a pass |
| `workspace-valid` | **pass** | `scripts/validate-workspace .` → checked 7 items and 7 documents, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | Six criteria, each named to a test function in the table above: AC1 → `WI0002AC1SettleListsThePayments`, AC2 → `WI0002AC2NothingToSettle` (3 tests), AC3 → `WI0002AC3TheListSettlesTheGroupExactly` (6 tests), AC4 → `WI0002AC4TheSameDataPrintsTheSameBytes`, AC5 → `WI0002AC5SettleChangesNothing` (2 tests), AC6 → `WI0002AC6TheReadmeDocumentsTheCommand` (3 tests). No criterion rests on reading the code |
| `commits-reference-the-item` | **pass** | `scripts/check-commit-refs WI-0002 wi/WI-0002` → `all 4 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main...wi/WI-0002 --stat` → 6 files, 437 insertions, 25 deletions. `expenses/settle.py` is steps 1–2; `expenses/cli.py` is step 3; `tests/test_settle.py` and `tests/test_cli.py` are steps 4–5; `README.md` is step 6; `docs/architecture/overview.md` is step 7. Every deletion is in `README.md`'s opening paragraph and `overview.md`'s "What is coming", both of which said who-owes-whom was not built yet. No hunk is untraceable |
| `claims-are-sourced` | **pass** | `scripts/lint-claims --changed-since main` → 1 document checked, 0 errors, 0 warnings, exit 0 |

## What I did not do

- **No test asserts the unsettled-dataset case.** The plan's third assumption says a dataset whose
  positions do not sum to zero is settled as far as it can be. No delivered command can produce
  that state, so building one would mean hand-writing a JSON file that the tool would never write,
  and no criterion of this item covers it. The loop's termination on any input is a property of
  the code — either pool empties — not a claim a test backs here.
- **`positions()` is not exposed by any command.** It is an internal function. Printing net
  positions was offered to the stakeholder as option C of EP-001/Q-002 and not chosen, so no
  command surfaces it, and none of the six criteria asks for one.
- **`tracker/project.yaml` is unchanged.** `commands.test` was already a real command;
  `commands.lint` stays null on ADR-0004's record. Nothing in this item changes either.
- **Nothing was fixed that this item does not cover.** BUG-0001 and BUG-0002 are both open at
  `ready` against behaviour delivered by WI-0001, and both were left alone. In particular
  BUG-0002 — `store.save` letting an `OSError` escape as a traceback — is untouched by this
  change, because `settle` never calls `save`.
- **No new defect was found in delivered behaviour**, so no bug was filed by this execution.
- **One risk the plan records is not addressed here and should not be.** If WI-0004 deletes a
  person without touching their expenses, `positions()` would silently drop them from the totals,
  because it keys on `data["people"]`. No delivered command can reach that state today. It is
  WI-0004's to solve and its criteria's to state; it is repeated here so that whoever plans
  WI-0004 meets it in this item's record as well as in its own.
