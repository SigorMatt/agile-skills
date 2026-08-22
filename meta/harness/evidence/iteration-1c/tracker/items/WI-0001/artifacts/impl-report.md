# Implementation report — WI-0001

## What was built

The tool itself, since nothing existed before this item: an executable `expenses` at the
repository root, the `expenses_tool` package behind it, the `add-person` and `list-people`
subcommands, the JSON data file, a README, and 27 tests.

- **`expenses`** — the launcher, eight lines of logic-free glue. It puts
  `os.path.dirname(os.path.realpath(__file__))` at the front of `sys.path` and calls
  `expenses_tool.cli.main()` (ADR-0008 clauses 1 and 2). `realpath` is what lets a symlink on
  `PATH` still find the package.
- **`expenses_tool/store.py`** — the data file and the rules over it. `normalise`, `display` and
  `validate_name` implement ADR-0003; `load` reads strictly and `save` writes atomically per
  ADR-0006; `add_person` and `list_people` work on the in-memory dict. It raises `DataFileError`,
  `InvalidName` and `DuplicatePerson`, and it neither prints nor exits.
- **`expenses_tool/cli.py`** — the `argparse` parser, the two handlers, every user-visible string,
  and the exit codes of ADR-0005. `main(argv=None)` returns an exit code; only the launcher calls
  `sys.exit`.
- **`tests/test_store.py`** — 17 unit tests over the rules.
- **`tests/test_cli_people.py`** — 10 end-to-end tests, one class per acceptance criterion plus two
  for the usage-error exit code, each running the real `./expenses` in a subprocess.
- **`README.md`** — the commands, the name rules, the data file and `--data-file`, the optional
  `PATH` install, and the table of exit codes. AC7 refers to "the path the README documents as the
  default", so the README is load-bearing for that criterion rather than decoration.

## Acceptance criteria evidence

Every test below is in `tests/test_cli_people.py` and runs `./expenses` in a subprocess against a
data file inside a fresh `TemporaryDirectory`, so each criterion starts from an empty store.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — `Added Ana` then `Ana`, exit 0 | `cmd_add_person` prints `Added <stored name>` and returns 0; `cmd_list_people` prints one name per line | `AC1::test_ac1_add_then_list` — asserts stdout `"Added Ana\n"`, stderr `""`, exit 0; then stdout `"Ana\n"`, exit 0 |
| AC2 — survives the process exiting | `store.save` writes the file; each invocation re-reads it | `AC2::test_ac2_persists_across_invocations` — three separate `subprocess.run` calls; the third asserts stdout `"Ana\n"` |
| AC3 — `" ana "` refused, nothing changes | `store.add_person` compares `normalise()` and raises `DuplicatePerson`; `cli` prints on stderr and returns 1 before any `save` | `AC3::test_ac3_duplicate_refused` — stderr `"Ana is already registered\n"`, stdout `""`, exit 1, the file's bytes identical before and after, and `list-people` printing exactly `["Ana"]` |
| AC4 — empty store prints and exits 0, creates nothing | `store.load` returns an empty store for a missing path and does not create it; `cli` prints the message on stdout | `AC4::test_ac4_empty_store` — stdout `"No one is registered yet\n"`, stderr `""`, exit 0, `os.path.exists(data_file)` still false |
| AC5 — blank and comma names refused, nothing changes | `store.validate_name` raises `InvalidName("blank"\|"comma")` before anything is stored | `AC5::test_ac5_invalid_names_refused` — three sub-tests: stderr `"A person's name cannot be blank\n"` twice and `"A person's name cannot contain a comma\n"` once, stdout `""`, exit 1, file bytes unchanged after each, and the listing identical before and after |
| AC6 — display and order | `store.display` trims; `store.list_people` sorts by `normalise` | `AC6::test_ac6_display_and_order` — adds `Cass`, `ana`, `" Ben "`; asserts stdout is exactly `"ana\nBen\nCass\n"` |
| AC7 — the default file in `$HOME` | `--data-file` defaults to `~/.expenses.json`, expanded with `os.path.expanduser` | `AC7::test_ac7_default_data_file` — `HOME` set to an empty temporary directory; `add-person` exits 0; `os.listdir(home)` is exactly `[".expenses.json"]`; `list-people` prints `"Ana\n"`. The README documents that path under "Where your data lives" |
| AC8 — an unreadable file is refused, not overwritten | `store.load` raises `DataFileError` for anything that is not this tool's file; `cli` catches it and returns 1 without saving | `AC8::test_ac8_unreadable_data_file` — file contains `not a data file`; for both `list-people` and `add-person`: stderr contains the path, contains no `Traceback`, stdout `""`, exit 1, bytes unchanged |

Each test fails if the behaviour is removed: they compare exact strings and exit codes rather than
asserting that something ran. The three refusal criteria additionally compare the data file's bytes
before and after, so an implementation that printed the right message *and* stored the person would
fail them.

## Deviations from the plan

Three, all within "how" rather than "what":

1. **`store.load` also raises `DataFileError` when `people` is present but is not a list of
   strings, and when the top level is not an object.** The plan named both checks; this is a note
   that they are implemented as one guard each rather than a single schema validation pass, which
   keeps each `reason` string specific enough to be useful in the message.
2. **`save` calls `os.fsync` before `os.replace`.** The plan said "flushes it, closes it, then
   replaces". `flush()` alone moves the bytes to the OS, not to disk; without `fsync` a crash can
   leave a renamed but empty file, which is the exact failure the atomic write exists to prevent.
   No criterion changes.
3. **Two extra tests were written that map to no acceptance criterion** —
   `UsageErrors::test_an_unknown_subcommand_exits_2` and `::test_a_missing_name_exits_2`. The
   item's `## Notes` records the *wording* of a usage error as deliberately unconstrained, but
   ADR-0005 clause 3 fixes the exit code at 2, and nothing else would hold that in place. They are
   named here rather than hidden because the plan's mapping table does not contain them.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 27 tests … OK`, run on the branch head (`1dd3f09`) after the last change |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses expenses_tool tests` → exit 0. ADR-0007 clause 4 records that this is a syntax check, not a style linter: none is installed and none can be installed here |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | AC1–AC8 each have a named test in the table above; `tests/test_cli_people.py` has one class per criterion |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → `all 1 commit(s) on main..wi/WI-0001 name WI-0001` |

## What I did not do

- **No question was filed**, because none was needed: every decision inside the plan's latitude was
  either fixed by an ADR or reversible in one file.
- **The two behaviours the item records as deliberately unconstrained were left unconstrained.**
  `argparse`'s usage *text* is unchanged (only its exit code is asserted), and a `--data-file` path
  that cannot be written is not handled specially — `mkstemp` raises and Python reports it. That is
  the state the item's `## Notes` describes, not an oversight, but it does mean an unwritable
  `--data-file` produces a traceback rather than a polite refusal. It is the one place in this item
  where the tool is less careful than ADR-0005 clause 2 would suggest, and it is deliberate:
  changing it now would be building behaviour no criterion covers.
- **Nothing was built for the later items.** No `expenses` key is written into the data file, and
  `store.py` has no expense, report or import machinery. ADR-0006 clause 2's missing-key rule is
  what lets WI-0002 and WI-0004 add theirs without a migration.
- **`docs/` was not touched.** The plan created the architecture overview and three ADRs before any
  code existed, and nothing in the implementation contradicted them.
