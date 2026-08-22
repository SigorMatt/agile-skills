# Implementation report — WI-0001

Branch `wi/WI-0001`, commits `5d23d40..b7ad785` (eight, all naming the item). Every gate below
was run on the branch head after the last commit.

## What was built

`python3 -m expenses`, a standard-library-only Python package in three modules, exactly the split
`docs/architecture/overview.md` describes and `ADR-0005` constrains.

- **`expenses/model.py`** — the validators and the record types. `normalise_name` is AC1's
  matching key (`strip().casefold()`), computed on each comparison and never stored.
  `parse_name` and `parse_description` return the trimmed display form and refuse a blank one.
  `parse_amount` accepts `^[0-9]+(\.[0-9]{1,2})?$` with a value above zero and returns integer
  minor units (`ADR-0004`); `format_amount` is its inverse. `parse_date` requires
  `^\d{4}-\d{2}-\d{2}$` **before** calling `date.fromisoformat`, because `fromisoformat` also
  accepts `20260822`, which AC7 does not. `Person`, `Expense`, `Repayment` and `Ledger` are
  dataclasses with `to_dict`/`from_dict` matching `ADR-0003`'s on-disk shape;
  `Ledger.find_person` returns the stored display form of a recorded person or `None`.
- **`expenses/store.py`** — `resolve_path` (`--file`, then `EXPENSES_LEDGER`, then
  `$XDG_DATA_HOME/expenses/ledger.json` with `~/.local/share` as the `XDG_DATA_HOME` default),
  `load` (a missing file is an empty ledger; unreadable, malformed or wrongly-shaped raises
  `StoreError`) and `save` (UTF-8 JSON with a trailing newline, written to a same-directory
  temporary file and moved over the target with `os.replace`, creating parent directories).
- **`expenses/cli.py`** — the six subcommands, and one `main` that resolves the path, loads,
  dispatches one handler, and saves **only when the handler reports a change**. A
  `ValidationError` becomes a stderr line and exit 2; a `StoreError` becomes a stderr line and
  exit 1. Because the save is the last thing `main` does and no handler writes, a refusal cannot
  change the recorded data — the property is structural rather than remembered six times.
- **`expenses/__main__.py`** — `raise SystemExit(main(sys.argv[1:]))`.

Six tests files, 83 tests. `tests/cli_harness.py` gives every CLI test a scratch ledger and an
`assertRefused` that checks all three halves of the item's definition of "refused" — non-zero
exit, a non-empty stderr, and a ledger file byte-identical to before.

## Acceptance criteria evidence

`unittest` was run as `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 83 tests`,
`OK`. Each row below names the test method that would fail if the behaviour were removed.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `add-person` trims and stores the typed form; a duplicate under `normalise_name` and a blank name are both refused | `tests/test_cli_people.py::TestAddPerson::test_adding_a_person_exits_zero_and_they_appear_in_the_listing`, `::test_every_spelling_ac1_calls_a_duplicate_is_refused` (subtests `ana`, ` Ana `, `ANA`, `Ana`), `::test_a_blank_or_whitespace_only_name_is_refused`; `tests/test_model.py::TestFindPerson::test_every_spelling_ac1_names_finds_the_stored_person` |
| AC2 | `people` prints one name per line in insertion order, in the form first typed; `No people recorded.` and exit 0 when empty | `tests/test_cli_people.py::TestPeopleListing::test_an_empty_ledger_says_so_and_exits_zero`, `::test_people_are_listed_in_the_order_added_and_the_form_first_typed` (asserts exactly `["Ana", "ben", "CARA"]`), `::test_a_name_typed_with_surrounding_space_is_listed_trimmed` |
| AC3 | `add-expense` requires a recorded payer and recorded sharers, refuses a repeated sharer and a blank description, and does not require the payer to share | `tests/test_cli_expenses.py::TestAddExpense::test_an_unrecorded_payer_is_refused`, `::test_an_unrecorded_sharer_is_refused`, `::test_the_same_person_named_twice_among_the_sharers_is_refused` (`--shared-by Ana --shared-by ana`), `::test_a_blank_description_is_refused`, `::test_the_payer_need_not_be_one_of_the_sharers`, `::test_sharers_are_stored_in_the_form_the_person_was_first_recorded_in` |
| AC4 | omitting `--shared-by` resolves the sharers to everyone recorded at that moment and stores them by name | `tests/test_cli_expenses.py::TestDefaultSharers::test_everyone_recorded_right_now_shares_it_and_nobody_added_later_does` — records with Ana and Ben present, then adds Cara, then asserts the stored sharers are `["Ana", "Ben"]` and Cara appears nowhere in the listing |
| AC5 | the stored record holds `amount_minor` and `sharers` and nothing else that could be a per-person amount; the command's own usage output offers no such option | `tests/test_cli_expenses.py::TestStoredShape::test_sixty_shared_by_three_stores_one_amount_and_three_sharers` — asserts `amount_minor == 6000`, three sharers, and that the record's keys are **exactly** `["amount_minor", "date", "description", "payer", "sharers"]`; `::test_the_commands_own_usage_output_offers_no_per_person_amount_option` reads the real `add-expense --help` text |
| AC6 | `parse_amount` is the single gate on every amount, in `add-expense` and in `repay` alike | `tests/test_model.py::TestParseAmount::test_accepted_forms_become_minor_units`, `::test_every_form_ac6_names_as_refused_is_refused` (eleven subtests: `0`, `0.00`, `-5`, `+5`, `12.`, `.5`, `12.505`, `1,234.56`, `€12.50`, `abc`, `""`); through the CLI, `tests/test_cli_expenses.py::TestAmountThroughTheCli::test_every_refused_amount_is_refused_and_leaves_the_ledger_unchanged` runs all eleven and checks the file bytes each time |
| AC7 | `--date` is parsed by `parse_date`; omitting it records `date.today().isoformat()` | `tests/test_model.py::TestParseDate::test_every_form_ac7_names_as_refused_is_refused` and `::test_the_compact_iso_form_fromisoformat_accepts_is_still_refused`; `tests/test_cli_expenses.py::TestDateThroughTheCli::test_a_stated_date_is_recorded`, `::test_an_omitted_date_records_the_machines_current_local_date` (captures `date.today()` in the same run, per the plan's risk note) |
| AC8 | `expenses` prints date, payer, amount, description and sharers per record in insertion order; `No expenses recorded.` and exit 0 when empty | `tests/test_cli_expenses.py::TestExpenseListing::test_an_empty_ledger_says_so_and_exits_zero`, `::test_each_expense_shows_its_date_payer_amount_description_and_sharers`, `::test_expenses_are_listed_in_the_order_they_were_recorded` |
| AC9 | `resolve_path`'s precedence, plus creation on first write and refusal of an unusable location | `tests/test_store.py::TestResolvePath` (six methods, including `::test_the_default_does_not_depend_on_the_working_directory`); `tests/test_persistence.py::TestLocation::test_two_locations_do_not_see_each_others_data`, `::test_what_one_run_records_the_next_run_lists_at_the_default_location`, `::test_a_record_under_a_given_location_does_not_appear_at_the_default`, `::test_a_location_that_does_not_exist_yet_is_created_on_the_first_write`, `::test_a_location_that_cannot_be_written_is_refused`, `::test_a_location_that_cannot_be_read_is_refused_and_left_alone` |
| AC10 | everything is on disk, so a new process sees it | `tests/test_persistence.py::TestSurvivesProcessExit::test_a_second_and_third_process_list_identical_output` and `::test_the_listings_hold_the_same_fields_and_order_after_a_restart` — each `run()` is a real `subprocess` invocation of `python3 -m expenses`, not a second call to `main()` |
| AC11 | `repay` requires two recorded people, refuses a self-repayment under AC1's matching, and accepts a repayment with no expense behind it | `tests/test_cli_repayments.py::TestRepay::test_a_repayment_is_accepted_even_when_no_expense_involves_either_person`, `::test_repaying_yourself_is_refused_including_under_ac1_matching` (subtests `Ana`, `ana`, ` ANA `), `::test_an_unrecorded_person_on_either_side_is_refused`, `::test_the_amount_follows_ac6`, `::test_the_date_follows_ac7` |
| AC12 | `repayments` prints date, who paid whom and how much, in insertion order, with a line when empty; the two listings never show each other's records | `tests/test_cli_repayments.py::TestRepaymentListing::test_an_empty_ledger_says_so_and_exits_zero`, `::test_each_repayment_shows_its_date_who_paid_whom_and_how_much`, `::test_repayments_are_listed_in_the_order_they_were_recorded`, `::test_neither_listing_shows_the_others_records`, `::test_the_two_record_kinds_are_separate_arrays_on_disk` |

The head of the criteria defines "refused" as three things together. `assertRefused` in
`tests/cli_harness.py` asserts all three, and every refusal test in the CLI suites goes through
it, so no refusal is demonstrated by its exit code alone.

## Deviations from the plan

1. **The six subcommands are registered across steps 4, 5 and 6 rather than all in step 4.** The
   plan's step 4 says "build the argparse parser with the global `--file` and the six
   subcommands", but four of the six handlers do not exist until steps 5 and 6, so a step-4 commit
   registering all six would not import. Each step now registers the subcommands it implements.
   The parser at the branch head is exactly the one the plan specifies — `python3 -m expenses
   --help` lists all six. This changed **how**, not **what**.
2. **`model.py` gained two validators the plan did not name: `parse_name` and
   `parse_description`.** The plan named `normalise_name`, `parse_amount`, `format_amount` and
   `parse_date`. AC1 and AC3 also require blank names and blank descriptions to be refused, and
   the plan's own design principle is that every rule about what an acceptable input is lives in
   `model.py` so WI-0003's importer reuses it. Putting these two in `cli.py` instead would have
   been the deviation.
3. **`model.today()` exists as a one-line wrapper over `date.today()`.** Not in the plan. It keeps
   `cli.py` from importing `datetime` for the single AC7 default, and gives WI-0003 the same
   entry point. Trivially reversible.
4. **`load` raises `StoreError` for a document that is valid JSON but not shaped like a ledger**
   (for example `{"people": [{"nome": "Ana"}]}`), not only for malformed JSON. The plan's
   assumption 5 says a corrupt file must never be treated as an empty one; a wrongly-shaped
   document is the same hazard reached by a different route, and the alternative was an unhandled
   `KeyError` traceback.
5. **`docs/architecture/overview.md` went to v2, where the plan's step 8 said to leave the docs
   alone unless implementation changed the shape.** The shape did not change; one sentence in v1
   was however false about the delivered code — it said the normalised name "is an index built
   when the ledger is loaded", and `find_person` scans `people` and computes the key per
   comparison. A document making a false statement about the code is worth a version bump on its
   own. The same edit adds the command list and the fact that `--file` must precede the
   subcommand.

Nothing in the plan's `## Assumptions` was reversed. Exit codes are 2 for a refusal and 1 for a
ledger that cannot be read or written, as assumption 2 states.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 83 tests in 2.315s`, `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses tests` → exit 0. Per `ADR-0005` this is a syntax check, not a style linter: it means every file parses, and no more |
| `workspace-valid` | **pass** | `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | the table above names a test method for each of AC1–AC12; none is demonstrated by reading the code |
| `commits-reference-the-item` | **pass** | `.claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, "all 8 commit(s) on main..wi/WI-0001 name WI-0001" |
| `no-unplanned-scope` (advisory) | **pass** | `git diff --name-only main..wi/WI-0001` is 16 files: five under `expenses/`, six under `tests/`, `docs/architecture/overview.md`, and four tracker files that are this execution's own record. Every hunk traces to a plan step; the five deviations above are the only places the diff exceeds the plan's letter |
| `claims-are-sourced` | **pass** | `.claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 0 errors, 0 warnings |

## What I did not do

- **No `README.md`.** The plan's step 8 offered one conditionally; the command list went into
  `docs/architecture/overview.md` v2 instead, which is where this workspace keeps durable
  knowledge. A person cloning the repo has no top-level usage file.
- **`--file` after the subcommand is a usage error.** `python3 -m expenses people --file X` exits
  2 with `unrecognized arguments`. This is what the plan specified — `--file` is global and
  precedes the subcommand — and it is now written in `overview.md` v2 rather than only in the
  plan. It is a real ergonomic edge, and reversing it would mean adding `--file` to each
  subparser. No acceptance criterion constrains the position, so this was not treated as a
  question.
- **No concurrency protection.** Two processes writing the same ledger at once can lose one of the
  two changes: each loads, mutates and replaces the whole file, and `os.replace` makes the write
  atomic but not serialised. Nothing in the item or in `ADR-0003` asks for locking, and the tool
  is one person on one machine [src: docs/product/vision.md], but a reviewer should know the
  guarantee is "never a half-written file", not "never a lost update".
- **`Ledger.find_person` is a linear scan**, and `add-person` calls it twice on the duplicate
  path. Irrelevant at a friend group's scale; noted because `overview.md` v1 claimed an index and
  v2 now says plainly that there is not one.
- **`version` is written but never read.** `ADR-0003` puts it there so a later format change has
  somewhere to branch. `load` does not check it, so a future ledger written by a newer version
  would be read as if it were version 1 rather than refused. There is nothing on disk to migrate
  yet and no second version to distinguish, so adding the check now would be speculative — but it
  is a gap a later item has to close before the field earns its keep.
- **No bug items were filed.** Nothing was found in another item's delivered behaviour, because
  nothing else has been delivered.
