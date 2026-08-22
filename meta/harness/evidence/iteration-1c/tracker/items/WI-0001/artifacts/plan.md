# Plan — WI-0001 Add and list the people who share expenses

## Problem

The tool does not exist yet: this item creates the executable, the data file and the first two
subcommands. Afterwards, the person keeping the group's books can register each friend by name and
list who is registered, against a data file that survives the process exiting. What makes it more
than a list is the rules around the edges — `ana` and ` Ana ` are the same person as `Ana`
(ADR-0003), a duplicate is refused rather than silently ignored (ADR-0005), a data file the tool
does not understand is refused rather than overwritten (AC8) — and those rules exist because
EP-001 has no edit and no delete, so anything this tool gets wrong cannot be repaired with this
tool. The constraints are fixed and not this plan's to revisit: stock CPython with no third-party
package (EP-001 SM4), one executable named `expenses` (ADR-0002), `~/.expenses.json` overridable
per run (ADR-0004), and the streams and exit codes of ADR-0005.

## Approach

A thin executable launcher over an importable package, per ADR-0008: `expenses` resolves its own
real directory onto `sys.path` and calls `expenses_tool.cli.main()`, which returns an exit code.
`store.py` owns the data file and the name rules and never prints; `cli.py` owns the parser, every
message string the criteria quote, and the exit codes. The file is one JSON object read strictly
and written atomically (ADR-0006), and every check happens before any write, so "a refusal changes
nothing" is a property of the control flow rather than something tested after the fact.

Tests come in the two layers ADR-0007 fixes: `test_store.py` imports the package and covers the
rules; `test_cli_people.py` runs `./expenses` in a subprocess against a temporary data file and
asserts on stdout, stderr and the exit code, which is the form every acceptance criterion is
written in.

## Steps

1. **Create the package skeleton and the launcher.** Add `expenses` at the repository root:
   `#!/usr/bin/env python3`, executable bit set (`git update-index --chmod=+x expenses` if needed),
   inserting `os.path.dirname(os.path.realpath(__file__))` at `sys.path[0]`, then
   `from expenses_tool.cli import main; sys.exit(main())`. Add empty `expenses_tool/__init__.py`
   and `tests/__init__.py`. Afterwards: `./expenses` runs and fails only because `cli.main` does
   not exist yet.

2. **Write `expenses_tool/store.py` — the name rules.** `normalise(name) -> str` returns
   `name.strip().casefold()`. `display(name) -> str` returns `name.strip()`. `validate_name(name)`
   raises `InvalidName("blank")` when `normalise(name)` is empty and `InvalidName("comma")` when
   the trimmed name contains `,` (ADR-0003 clause 3). No printing, no exit codes.

3. **Write `expenses_tool/store.py` — reading.** `load(path) -> dict` returns
   `{"schema": 1, "people": []}` when the path does not exist (ADR-0004 clause 3). Otherwise parse
   the file and raise `DataFileError` unless every one of these holds: it is valid JSON; the top
   level is an object; `schema` is present and is an `int` no greater than the supported version
   (1); `people`, if present, is a list of strings. A missing `people` reads as `[]` (ADR-0006
   clause 2). `DataFileError` carries the path and a short reason. Afterwards: no code path repairs
   or rewrites a file that failed to load.

4. **Write `expenses_tool/store.py` — writing.** `save(path, data)` writes to a temporary file in
   the same directory as `path` (`tempfile.mkstemp(dir=...)`), with
   `json.dump(..., indent=2, sort_keys=True)` and a trailing newline, flushes it, closes it, then
   `os.replace()`s it over `path` (ADR-0006 clause 5). On any failure the temporary file is removed
   and the original is untouched. Afterwards: a crash mid-write can leave the old file or the new
   one, never a half-written one.

5. **Write `expenses_tool/store.py` — the two operations.** `add_person(data, name)` raises
   `DuplicatePerson(existing_display_name)` when some stored name has the same `normalise()`, and
   otherwise appends `display(name)` to `data["people"]` and returns the display name.
   `list_people(data) -> list[str]` returns the stored names sorted by `normalise()` (ADR-0003
   clause 4, ADR-0005 clause 5). Both work on the in-memory dict; neither reads or writes a file.

6. **Write `expenses_tool/cli.py` — the parser.** `argparse.ArgumentParser(prog="expenses")` with
   `add_subparsers(dest="command", required=True)`. A parent parser carries
   `--data-file` (default `os.path.join(os.path.expanduser("~"), ".expenses.json")`, and
   `os.path.expanduser` applied to whatever value is given), and both subparsers take it, so it is
   written after the subcommand as the criteria do. `add-person` takes one positional `name`;
   `list-people` takes none. `main(argv=None) -> int` parses, dispatches, and returns an exit code;
   `argparse` supplies exit 2 for a usage error unchanged (ADR-0005 clause 3).

7. **Write `expenses_tool/cli.py` — `add-person`.** Validate the name, `load`, `add_person`,
   `save`, then print `Added <display name>` on stdout and return 0. Map the failures to exactly
   these, each on stderr, returning 1 and writing nothing:
   - `InvalidName("blank")` → `A person's name cannot be blank`
   - `InvalidName("comma")` → `A person's name cannot contain a comma`
   - `DuplicatePerson(existing)` → `<existing> is already registered`
   - `DataFileError` → `Cannot read <path>: <reason>`
   Afterwards: AC1, AC3, AC5 and the `add-person` half of AC8 hold.

8. **Write `expenses_tool/cli.py` — `list-people`.** `load`, then `list_people`. With no people,
   print `No one is registered yet` on stdout and return 0 (ADR-0005 clause 4); otherwise print one
   name per line on stdout and return 0. A `DataFileError` prints `Cannot read <path>: <reason>` on
   stderr and returns 1. `load` on a missing file must not create it. Afterwards: AC2, AC4, AC6 and
   the `list-people` half of AC8 hold.

9. **Write `tests/test_store.py`.** Import the package. Cover: `normalise` and `display` on
   `"Ana"`, `" ana "`, `"ANA"`; `validate_name` on `""`, `"   "`, `"Smith, Jr"`; `load` of a
   missing path, of valid content, and of each rejected shape from step 3 (not JSON, a JSON list,
   no `schema`, `schema: 2`, `people` not a list of strings); `save` followed by `load` round-trips;
   `save` leaves no temporary file behind; `add_person` raising `DuplicatePerson` for a
   differently-cased name; `list_people` ordering `["Cass", "ana", "Ben"]` as `["ana", "Ben",
   "Cass"]`.

10. **Write `tests/test_cli_people.py`.** One test per acceptance criterion, each running
    `./expenses` through `subprocess.run` from the repository root with a data file inside
    `tempfile.TemporaryDirectory()`, asserting on `stdout`, `stderr` and `returncode` exactly as
    the criterion states. AC2 uses three separate `subprocess.run` calls. AC7 runs with `env` where
    `HOME` points at an empty temporary directory and no `--data-file`, then asserts that exactly
    one entry appeared in that directory. AC3, AC5 and AC8 additionally read the data file's bytes
    before and after and assert they are identical.

11. **Write `README.md`.** What the tool is; that it needs only CPython; the two commands with a
    worked example; the default data file `~/.expenses.json` and `--data-file`; and the optional
    `PATH` install — copying **both** `expenses` and `expenses_tool/`, or symlinking `expenses` and
    leaving the package where it is (ADR-0008 clause 2). AC7 refers to "the path the README
    documents as the default", so this step is what makes AC7 decidable.

12. **Run both project commands and fix what they report.** `python3 -m unittest discover -s tests
    -t . -q` and `python3 -m compileall -q expenses expenses_tool tests`, both from the repository
    root, both exiting 0 on the final state of the code (`spec/dor-dod.md` D3).

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `add-person` prints `Added Ana`, exit 0; `list-people` prints `Ana` | 6, 7, 8 | `test_cli_people.py::test_ac1_add_then_list` — two `subprocess.run` calls against a fresh `--data-file`, comparing stdout to `Added Ana\n` and `Ana\n`, stderr to `""`, both exit codes to 0 |
| AC2 — the list survives the process exiting | 3, 4, 8 | `test_cli_people.py::test_ac2_persists_across_invocations` — three separate `subprocess.run` calls, the third asserting `Ana\n` |
| AC3 — `" ana "` is refused as a duplicate, nothing changes | 2, 5, 7 | `test_cli_people.py::test_ac3_duplicate_refused` — stderr `Ana is already registered\n`, stdout `""`, exit 1, the file's bytes identical before and after, and `list-people` printing exactly one line |
| AC4 — listing a non-existent store prints `No one is registered yet`, exit 0, creates nothing | 3, 8 | `test_cli_people.py::test_ac4_empty_store` — stdout compared exactly, exit 0, and `os.path.exists` on the data file still false |
| AC5 — blank and comma names refused with exact messages, nothing changes | 2, 7 | `test_cli_people.py::test_ac5_invalid_names_refused` — three invocations, each stderr compared exactly, exit 1, and `list-people` output identical before and after |
| AC6 — display and ordering | 2, 5, 8 | `test_cli_people.py::test_ac6_display_and_order` — add `Cass`, `ana`, `" Ben "`, assert stdout is exactly `ana\nBen\nCass\n` |
| AC7 — the default file in `$HOME` | 6, 11 | `test_cli_people.py::test_ac7_default_data_file` — `HOME` set to an empty temporary directory, `add-person` exits 0, `os.listdir(home)` has exactly one entry, `list-people` prints `Ana\n`; the README names that path |
| AC8 — an unreadable data file is refused, not overwritten | 3, 7, 8 | `test_cli_people.py::test_ac8_unreadable_data_file` — the file contains `not a data file`; both commands print a stderr message containing the path and no `Traceback`, exit 1, and the file's bytes are identical afterwards |

## Assumptions

- **The supported `schema` is `1`, and a higher value is refused rather than tolerated.** Reversal
  is one comparison in `store.load` and costs nothing while no file with a higher version exists.
- **`Cannot read <path>: <reason>` is the wording for a `DataFileError`.** AC8 requires only that
  the message names the file and contains no traceback, so this is `implement`'s to keep or refine
  within that constraint — unlike AC5's messages, which the criteria quote exactly and which are
  therefore fixed.
- **The temporary file for an atomic write is created in the target's directory.** `os.replace` is
  atomic only within a filesystem, so a temporary file in `/tmp` would silently degrade to a
  copy-then-rename across devices. Reversal would mean giving up clause 5 of ADR-0006, which is
  not a reversal anyone should want.
- **`argparse`'s usage text and its exit code 2 are accepted unchanged**, as the item's `## Notes`
  records under R10. Reversal is a custom `error()` override in one place.

## Decisions and ADRs

- **ADR-0006 — one JSON object per data file, written atomically.** Chosen over SQLite, CSV and
  `pickle`; completes ADR-0004 clause 4, which reserved the format for `plan`. Route: decided, with
  the criteria that depend on it (AC3, AC5, AC8) named in its context.
- **ADR-0007 — tests with the standard library's `unittest`.** `pytest` is not installed here and
  cannot be installed; `commands.test` and `commands.lint` are now filled in with commands that
  have been run in this project, and `commands.build` stays `null` with the reason recorded.
- **ADR-0008 — a thin launcher over `expenses_tool/`.** Completes ADR-0002 clause 1. The launcher
  resolving its own real path is what makes the optional `PATH` install of ADR-0002 clause 2 work
  when `expenses` is a symlink.
- **Answered from existing documents, not re-decided here:** the command names and invocation
  (ADR-0002), the identity rule and the listing order (ADR-0003), the default file and the override
  (ADR-0004), every stream and exit code (ADR-0005), and the exact message strings AC5 quotes
  (WI-0001 `artifacts/refinement-qa.md`, tagged `[assumed]` under the stakeholder's delegation).
- **`docs/architecture/overview.md` was created** at v1, because this is the first planned item and
  an overview written after three items exist is archaeology.

## Risks

- **The launcher may not find its package when installed onto `PATH`.** If `expenses` is copied
  rather than symlinked and `expenses_tool/` is left behind, the tool fails on import with a
  message from Python rather than from this tool. Step 11 makes the README say to copy both or to
  symlink; no criterion covers it, because the criteria all run `./expenses` from the repository
  root. This is the most likely way a real user's first run fails.
- **AC7 asserts "exactly one new file in `$HOME`".** If `implement` ever writes anything else into
  the home directory — a lock file, a backup, a leftover temporary file from a failed atomic write
  — that criterion fails. That is intentional: it is also how a stray temporary file would be
  caught.
- **`os.replace` is atomic only within a filesystem.** A `--data-file` pointing across a mount from
  its own directory is not a case that can arise, since the temporary file is created in the target
  directory, but a `--data-file` in a directory the user cannot write to fails at `mkstemp` — one
  of the two behaviours the item's `## Notes` records as deliberately unconstrained.
- **Case-folding is not accent-folding.** `José` and `Jose` remain two people (ADR-0003 option C,
  declined). If the stakeholder has an accented name in the group and types it inconsistently, this
  plan produces exactly the duplicate the item exists to prevent — visibly, at least, since
  `list-people` will show both.
- **Every write rewrites the whole file.** Irrelevant at this size, and stated so that nobody later
  reads the atomic-write step as a performance decision.

## Out of scope for this item

- Expenses, the report and the CSV import (WI-0002, WI-0003, WI-0004). `store.py` gains nothing
  speculative for them: no `expenses` key is written by this item, and ADR-0006 clause 2's
  missing-key rule is what lets them add it later without a migration.
- Removing or renaming a person; editing or deleting anything (EP-001).
- Any packaging, installer, or `pyproject.toml`. ADR-0002 fixes the invocation as `./expenses` and
  ADR-0007 records why there is no build step.
- A style linter. None is installed and none can be; ADR-0007 clause 4 records what
  `commands.lint` does instead, and that it is a syntax check rather than a style check.
