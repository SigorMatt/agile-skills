# Implementation report — WI-0001

Branch `wi/WI-0001`, five commits, `f5285a5..4aae88d`. Every commit names WI-0001 in its subject.

## What was built

The first code in the project: a `python3 -m expenses` command-line tool that records the people
in a friend group and the expenses they share, and keeps both in one JSON file on disk.

Four modules, layered one way, as the plan's approach specifies
[src: tracker/items/WI-0001/artifacts/plan.md]:

| file | what it knows | what it must not do |
|------|---------------|---------------------|
| `expenses/money.py` | parsing an amount into minor units, formatting it back, splitting it equally | no I/O, no printing |
| `expenses/store.py` | where the dataset lives, how it is read and written, what a valid record is | no printing |
| `expenses/cli.py` | the argparse surface, the four handlers, all formatting and all printing | no arithmetic of its own |
| `expenses/__main__.py` | calling the CLI with `sys.argv[1:]` and exiting with what it returns | everything else |

`ExpensesError` is defined in `money.py`, the lowest layer, and is the single way a refusal
travels upward. `cli.main` catches it in exactly one place, writes the message to stderr and
returns 2. Because every validation happens before `store.save` is called, and `save` is the only
function that writes, "a refusal changes nothing on disk" is a property of the layering rather
than a promise repeated in each handler — which is what AC5 and AC6 turn on
[src: WI-0001 AC5; WI-0001 AC6].

The commands are the surface refinement recorded, unchanged
[src: tracker/items/WI-0001/item.md]:

```
python3 -m expenses person add <NAME>
python3 -m expenses person list
python3 -m expenses expense add --amount <AMOUNT> --paid-by <NAME> --shared-by <NAME>[,<NAME>...]
                                [--description <TEXT>] [--date <YYYY-MM-DD>]
python3 -m expenses expense list
```

`README.md` documents all four with an example of each, the flags and their defaults, what a
refusal looks like, and the `EXPENSES_STORE` / `XDG_DATA_HOME` / `~/.local/share` resolution
order [src: docs/architecture/adr/ADR-0001-one-json-file-for-the-whole-dataset.md].

## Acceptance criteria evidence

All 50 tests run under the project's declared test command
[src: run: python3 -m unittest discover -s tests -t . → exit 0, "Ran 50 tests in 0.466s", OK].
Test names below are as `unittest -v` prints them.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — add a person, list them, duplicate refused, `Ana` and `ana` distinct | `store.add_person` strips the name, refuses an empty result and refuses a name already present compared exactly; `cli.person_list` prints one name per line in recorded order | `test_cli.AC1PersonAddAndList.test_a_person_is_added_and_then_listed`; `.test_adding_the_same_person_twice_is_refused_and_leaves_one_ana` (asserts non-zero exit, `Ana` on stderr, and `person list` splitting to exactly `["Ana"]`); `.test_ana_and_ana_lowercase_are_two_people`. At the unit level, `test_store.AddPersonTests` (5 tests) |
| AC2 — 30.00 shared by three records 10.00 each, summing to exactly 30.00 | `money.split_equally` computes the shares and `store.add_expense` stores them beside the amount | `test_cli.AC2ExpenseIsRecordedWithEqualShares.test_thirty_shared_by_three_records_ten_each_summing_to_thirty` — reads the JSON at `EXPENSES_STORE` and asserts `amount_minor == 3000`, `shares_minor == {"Ana": 1000, "Ben": 1000, "Cara": 1000}` and `sum(...) == 3000`. Also `test_store.AddExpenseTests.test_an_expense_records_amount_payer_sharers_and_equal_shares` |
| AC3 — `expense list` shows amount, payer, sharers, date and description, in recorded order | `cli.expense_list` prints one line per expense from the stored list, in stored order | `test_cli.AC3ExpenseListShowsEveryField.test_each_entry_shows_amount_payer_sharers_date_and_description_in_order` — two expenses, each line asserted to contain all five fields; `.test_expenses_are_listed_in_the_order_they_were_recorded` — three amounts recorded 3, 1, 2 and read back `["3.00", "1.00", "2.00"]` |
| AC4 — byte-identical stdout from a new process | the dataset is the only state, and both listings print from it in stored order with an explicit format | `test_cli.AC4ARerunInANewProcessPrintsTheSameBytes.test_both_listings_are_byte_identical_from_a_fresh_process` — runs both listings twice via `subprocess.run([sys.executable, "-m", "expenses", ...])` with the same `EXPENSES_STORE`, asserts the bytes are equal, and asserts they equal the in-process output too |
| AC5 — unknown sharer and unknown payer refused by name, nothing changed | `store.add_expense` checks the payer, then each sharer, naming the first unknown one, before anything is appended | `test_cli.AC5UnknownNamesAreRefused.test_an_unknown_sharer_is_refused_by_name_and_changes_nothing` and `.test_an_unknown_payer_is_refused_by_name_and_changes_nothing` — each captures both listings, runs the refused command, asserts non-zero exit and `Dan` on stderr, and asserts both listings are unchanged |
| AC6 — ten invalid inputs refused, nothing changed | `money.parse_amount` (whole-string match, and zero refused), `cli.parse_date` (`YYYY-MM-DD` and a real date), `store.add_person` (empty name), `store.add_expense` (no sharer, repeated sharer) | `test_cli.AC6EveryInvalidInputIsRefused.test_all_ten_invalid_inputs_are_refused_and_change_nothing` — a `subTest` per case over exactly the ten the criterion names, each asserting non-zero exit, non-empty stderr, and both listings byte-identical to before |
| AC7 — description and date default independently and round-trip | `--description` defaults to `""` and is stripped; `--date` defaults to `datetime.date.today().isoformat()` | `test_cli.AC7DescriptionAndDateDefaultIndependently` — four tests: neither flag (asserts today's date, computed in the test, and an empty description, and that `expense list` shows today); `--description taxi` alone; `--date 2026-08-01` alone; and `--description ""` recording the identical entry to omitting it |
| AC8 — 10.00 over three sums exactly, and repeat runs agree | `money.split_equally` gives the remainder one unit each to the first-named sharers [src: docs/architecture/adr/ADR-0003-remainder-goes-to-the-first-named-sharers.md] | `test_cli.AC8AnUnevenSplitSumsExactlyAndRepeatsIdentically.test_ten_over_three_sums_to_exactly_ten` (shares sum to 1000); `.test_the_same_sequence_against_a_fresh_store_prints_the_same_bytes` — the same four commands against two fresh temporary stores, `expense list` compared. At the unit level `test_money.SplitEquallyTests.test_an_uneven_split_gives_the_extra_units_to_the_first_sharers` (`[334, 333, 333]`) and `.test_every_split_sums_to_exactly_the_amount` (7 amounts × 7 sharer counts) |
| AC9 — empty store prints `no people` and `no expenses`, exit 0 | `store.load` returns the empty dataset for a missing file; each listing prints its fixed string | `test_cli.AC9AnEmptyStoreListsNothingAndSucceeds.test_person_list_says_no_people`, `.test_expense_list_says_no_expenses`, and `.test_neither_listing_creates_the_data_file` |

Every test above asserts a specific value, so removing the behaviour fails it: the AC1 duplicate
test asserts a non-zero exit and the name on stderr, AC4 and AC8 compare captured bytes, and AC6
asserts both listings are unchanged after each of ten refusals. None of them would pass against
an empty implementation.

## Deviations from the plan

1. **The tests were written with the module each one covers, not in one pass at step 6.**
   `tests/test_money.py` landed in the same commit as `money.py`, `tests/test_store.py` with
   `store.py`, and `tests/test_cli.py` with `cli.py`. The plan groups them as step 6
   [src: tracker/items/WI-0001/artifacts/plan.md] but this skill requires the test to come with
   the change in the same commit, so the *how* was adapted and the *what* was not: all three
   modules exist with exactly the coverage step 6 lists — path resolution via `EXPENSES_STORE`,
   the missing file, the round trip, every refusal in `add_person` and `add_expense`, the file
   being unchanged after a refusal, each command end to end, and both byte-identical-repeat
   criteria.
2. **`store.py` exposes `people()`, `expenses()` and `empty_dataset()` beyond the signatures the
   plan fixed.** The plan's interface block names `people` and `expenses` in its prose list of
   operations but gives signatures only for the others; `empty_dataset()` is the value the plan
   says `load()` returns for a missing file, named so that the tests can assert against it
   without repeating the literal. No behaviour differs from the plan.
3. **`cli.main` takes optional `out` and `err` streams**, defaulting to `sys.stdout` and
   `sys.stderr`. The plan's signature is `main(argv)`. This is what lets `tests/test_cli.py`
   capture stdout and stderr per command without replacing process-wide streams; AC4 still
   exercises the real process through `subprocess.run`, so the in-process path is not the only
   one tested.
4. **The confirmation lines are `added <name>` and `added <amount> paid by <payer>`**, which the
   plan explicitly left to the developer [src: tracker/items/WI-0001/artifacts/plan.md].

No deviation changes what is delivered, so none of them was a question for the architect.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | [src: run: python3 -m unittest discover -s tests -t . → exit 0, "Ran 50 tests", OK], run on the branch head at `4aae88d` |
| `lint-clean` | **skipped** | `commands.lint` is `null` in `tracker/project.yaml` and ADR-0004 is the record of why — the standard library ships no linter and the project may not install one [src: docs/architecture/adr/ADR-0004-unittest-for-tests-and-no-lint-command.md]. Nothing was checked; this is not a pass |
| `workspace-valid` | **pass** | [src: run: python3 .claude/agile-skills/scripts/validate-workspace . → exit 0, 0 errors, 0 warnings] |
| `every-criterion-has-a-test` | **pass** | the table above names a test function for each of AC1–AC9; no criterion rests on reading the code |
| `commits-reference-the-item` | **pass** | [src: run: python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001 → exit 0, "all 5 commit(s) on main..wi/WI-0001 name WI-0001"] |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main..wi/WI-0001 --stat` is 13 files: the four modules, the three test modules, `README.md` (step 7), and four tracker files this execution's own record moves. Every hunk traces to a plan step |
| `claims-are-sourced` | **pass** | [src: run: python3 .claude/agile-skills/scripts/lint-claims --changed-since main → exit 0, 0 errors, 0 warnings]. See `## What I did not do` for what a whole-tree run reports |

## What I did not do

- **`docs/product/vision.md` fails `lint-claims --all` with two errors, and I left them alone.**
  [src: run: python3 .claude/agile-skills/scripts/lint-claims --all → exit 1, 2 errors:
  `vision.md:31 claim.unsourced` about `WI-0001/Q-001`, `vision.md:38 claim.unsourced` about
  `WI-0001/Q-003`]. Both are absolutes whose source is named inline in backticks rather than in a
  `[src: ...]` marker, in a document `answer-questions` wrote before this execution. They are
  outside this item's diff, the contracted gate is `--changed-since {{trunk}}` and it passes, and
  fixing what I noticed on the way is what this skill tells me not to do. I could not file it as
  a bug item either: `pipeline.yaml` has no `from: null → ready` creation row whose actor is
  `implement`, so `new-item` would refuse it. It is recorded here and in the journal so that
  `verify` — which does have that authority — can file it.
- **Nothing else from the plan is outstanding.** All seven steps are done, including step 7's
  README.
- **No concurrency protection.** Two processes writing at once can lose one of the writes; the
  atomic replace protects against a torn file, not against a lost update. Out of scope per
  ADR-0001 and the vision, and no criterion asks for it.
- **`--amount` has no upper bound and no currency.** Deliberate [src:
  docs/architecture/adr/ADR-0002-money-as-integer-minor-units.md].
- **A hand-edited data file is believed.** `store.load` checks the JSON is an object with
  `version: 1`; it does not recompute shares or check that they sum to the amount. Accepted and
  recorded in ADR-0003's consequences.
