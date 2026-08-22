# Implementation report — WI-0001

## What was built

The `expenses` package, its command-line entry point, its storage, and the epic's first two
subcommands. Five source files and six test files, all standard library.

| file | what it is |
|------|------------|
| `expenses/__init__.py` | empty package marker |
| `expenses/__main__.py` | `sys.exit(main(sys.argv[1:]))`, so `python3 -m expenses` works |
| `expenses/storage.py` | the only module that knows a file exists: `record_path`, `load`, `save`, `RecordError` |
| `expenses/group.py` | the only module that knows the rules: `identity_key`, `display_name`, `validate_name`, `people`, `find_person`, `add_person`, `RuleError` |
| `expenses/cli.py` | the only module that prints: `main`, the `COMMANDS` dispatch table, one handler per subcommand |
| `tests/support.py` | `CliTestCase` — a temporary record per test via `EXPENSES_FILE`, a `run_cli` helper, an `assertRefused` helper |
| `tests/test_people.py` | AC1, AC2, AC4, AC5, AC9 |
| `tests/test_duplicates.py` | AC6 |
| `tests/test_invalid_names.py` | AC7, AC8 |
| `tests/test_cli_surface.py` | AC10, AC11, the no-traceback clause, and the corrupt-record behaviour from ADR-0007 |
| `tests/test_persistence.py` | AC3, in real subprocesses |

The layering is `cli.py` → `group.py` → `storage.py`, exactly as `docs/architecture/overview.md`
(v1) sets out. Nothing below `cli.py` prints; `RuleError` and `RecordError` carry their message
and `main` catches both around the whole dispatch, which is the one place that makes "never a
traceback" true rather than something each handler has to remember.

## Acceptance criteria evidence

All evidence below is from the branch head, `b05c034` plus the report commit. `run_cli` is the
in-process helper; `invoke` in `test_persistence.py` runs a real `python3 -m expenses` process.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `cli._add_person` validates, saves, prints `Added <name>.` | `tests/test_people.py::AddAndListTest::test_add_person_with_a_space_in_the_name_is_confirmed` — asserts `(0, "Added Sam Okafor.\n", "")`. Also by hand: `python3 -m expenses add-person "Sam Okafor"` → `Added Sam Okafor.`, exit 0 |
| AC2 | `cli._people` prints one display name per line | `..._people_lists_the_person_just_added` — asserts `(0, "Sam Okafor\n", "")`; `..._surrounding_whitespace_is_stripped_from_the_stored_spelling` and `..._internal_whitespace_is_kept_in_the_stored_spelling` pin ADR-0005 point 4 in both directions |
| AC3 | `storage.load` / `storage.save` on the JSON file | `tests/test_persistence.py::PersistenceTest::test_people_added_by_earlier_invocations_are_still_there` — three separate `python3 -m expenses` **processes**; the third's stdout is `Alice\nBob\n`, exit 0. `..._a_duplicate_is_refused_across_invocations_too` shows the identity rule reads the stored record, not in-memory state |
| AC4 | `group.people` returns the stored list in order; `save` preserves it | `tests/test_people.py::..._test_people_lists_in_the_order_they_were_added` — adds `Carol`, `alice`, `Bob`; stdout is exactly `Carol\nalice\nBob\n` |
| AC5 | `cli._people` prints the empty-group line when the list is empty; a missing file loads as empty | `tests/test_people.py::..._test_people_on_an_empty_group_says_so_and_succeeds` — `(0, "No one is in the group yet.\n", "")`. By hand on a fresh `EXPENSES_FILE`: same, exit 0 |
| AC6 | `group.add_person` compares identity keys and raises `RuleError` naming the stored spelling | `tests/test_duplicates.py::DuplicateTest::test_every_spelling_of_the_same_person_is_refused` — subtests for `sam okafor`, `  SAM OKAFOR  `, `Sam  Okafor`, each exit 1 with `Sam Okafor is already in the group.`; `..._the_group_still_has_exactly_one_person_afterwards`; `..._a_genuinely_different_person_is_still_accepted` proves the rule discriminates rather than refusing everybody |
| AC7 | `group.validate_name` raises on an empty display name | `tests/test_invalid_names.py::..._test_an_empty_or_whitespace_only_name_is_refused` — `""`, `"   "`, `"\t\n"`, each exit 1 with `A name cannot be empty.` |
| AC8 | `group.validate_name` rejects `,` and `=` | `..._test_a_reserved_character_is_refused` — `Anna,Karin` and `a=b`, each exit 1 with the reserved-character message; `..._test_nobody_was_added_by_any_of_the_refusals` and `..._test_a_refusal_does_not_create_the_record_file` |
| AC9 | `identity_key` case-folds but does not fold accents | `tests/test_people.py::..._test_accented_letters_are_a_different_person` — `José` then `Jose` both succeed; `people` prints `José\nJose\n` |
| AC10 | arity checked in each handler before any work | `tests/test_cli_surface.py::ArityTest` — three tests, one per case; the two-argument case also asserts the group is still empty afterwards, so nothing was joined and stored |
| AC11 | `COMMANDS.get` returns `None`; empty `argv` handled first | `tests/test_cli_surface.py::UnknownSubcommandTest` — three tests, including that the message names the subcommands that do exist; `tests/test_persistence.py::..._test_the_module_exits_non_zero_when_given_no_subcommand` repeats the no-subcommand case as a real process, which is the only thing that exercises `__main__.py`'s exit status |
| head-of-list clause: never a traceback | one `except` around the dispatch in `cli.main` | `tests/test_cli_surface.py::NoTracebackTest::test_no_refusal_path_prints_a_traceback` — all eight refusal paths in this item, each asserted to exit non-zero with no `Traceback (most recent call last)` on stderr; `assertRefused` in `tests/support.py` re-checks it on every exact-message assertion |

### The tests were checked against mutations, not just run

A passing suite proves nothing about whether it would catch a regression, so three deliberate
mutations were made and reverted:

| mutation | result |
|----------|--------|
| `identity_key` returns the name unchanged (exact match only) | 7 failures |
| `cli._add_person` never calls `storage.save` | 13 failures |
| `display_name` collapses internal whitespace, like `identity_key` | **0 failures — a real hole** |

The third one is the risk `plan.md` names first, and the suite as first written did not cover it:
nothing distinguished the display rule from the identity rule on internal whitespace. Added
`tests/test_people.py::..._test_internal_whitespace_is_kept_in_the_stored_spelling`, which fails
against that mutation and passes against the real code. This is recorded because a reader should
be able to tell that the coverage was measured rather than assumed.

## Deviations from the plan

1. **`cli.main` takes two optional stream arguments**, `main(argv, out=None, err=None)`, defaulting
   to `sys.stdout` and `sys.stderr` at call time. The plan specified `main(argv) -> int`. Every
   caller in the plan still works unchanged — `__main__.py` calls `main(sys.argv[1:])` — and the
   observable behaviour is identical. It was done so `tests/support.run_cli` can capture the two
   streams by passing them in rather than by patching module globals. This is *how*, not *what*.
2. **`group.find_person` exists and is not in the plan's interface list.** `add_person` needed the
   stored spelling of the person it collides with, in order to name it in the message AC6 requires,
   and ADR-0005 point 5 says the same resolution applies wherever a person is named — so it is
   written once, as its own function, for WI-0002 and WI-0004 to use rather than reimplement. It
   adds no behaviour beyond what AC6 needs today.
3. **`storage.load` validates the shape it read**, rejecting a top-level value that is not an
   object, a `version` that is not `1`, and a `people` that is not a list of strings. The plan
   named the first two; the third was added because a record whose `people` contained a number
   would otherwise crash with a traceback later, in `identity_key`, which contradicts ADR-0001
   point 3. Covered by `tests/test_cli_surface.py::CorruptRecordTest`.
4. **The helper is `run_cli`, not `run`** as plan step 5 named it. `unittest.TestCase.run` is the
   method the framework calls to execute a test; defining a helper with that name would have
   replaced it and broken every test in the suite. Renamed rather than escalated, because it is a
   name, not a behaviour.

Nothing here changes what is delivered. No acceptance criterion was edited.

## Gates

Run on the branch head, after the last code change.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 28 tests ... OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses tests` → exit 0, no output |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | the table above: every one of AC1–AC11 names a test function, and the three mutation runs show the suite fails when the behaviour is removed |
| `commits-reference-the-item` | **pass** | `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | every hunk traces to a plan step and an AC; the three deviations above are the only additions, and each is named with the criterion or ADR that required it |

## What I did not do

- **No `expenses` or `payments` key is written into the record.** ADR-0007 point 2 makes adding
  them free in WI-0002 and WI-0004, so writing empty lists now would be scope this item does not
  own.
- **No README, packaging metadata or console script**, per the plan's out-of-scope list. The only
  documented invocation is `python3 -m expenses`, run from the project root.
- **No locking and no concurrent-writer handling** — excluded by `docs/product/vision.md` (v3) and
  by this item's `## Out of scope`. Two processes writing at once will lose one of the writes; the
  atomic replace means neither will corrupt the file.
- **`commands.build` is still null** in `tracker/project.yaml`. There is nothing to build, and the
  plan left it null deliberately rather than fabricating a command that would pass vacuously.
- **The permissions of the created record file are whatever the process umask gives.** Nothing
  asks for anything stricter, and the file holds names, not secrets. Naming it here because a
  reader might expect a data file in `~/.local/share` to be mode 600, and it is not.
