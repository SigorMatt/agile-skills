# Plan — WI-0001 Add and list people, stored so they survive between runs

## Problem

The project has no code at all. This item creates the `expenses` package, its command-line entry
point, and its storage, and delivers the first two of the epic's seven subcommands: `add-person`,
which adds one person to the group, and `people`, which lists the group. The group must survive
between invocations, because the tool is a set of one-shot commands that each start a process and
exit (`ADR-0001`), and every later item names people, so who is in the group is the first fact the
record has to hold.

The constraints are all recorded. Python with the standard library only, no external service
(`docs/product/prd.md` v2). One person, one machine, one file (`docs/product/vision.md` v3). Two
names denote the same person when their case-folded, whitespace-normalised forms match, and a
duplicate is refused rather than silently added (`ADR-0005`). Eleven acceptance criteria pin the
exact stdout, stderr and exit status of every path, including the exact wording of five messages.

## Approach

Three modules, one direction of dependency, as `docs/architecture/overview.md` (v1) sets out:
`cli.py` owns the streams and the exit status, `group.py` owns the rules, `storage.py` owns the
file. Nothing below `cli.py` prints; the lower layers return values or raise, and `cli.py` turns a
raised error into a message on standard error and a non-zero exit status. That is what makes every
criterion testable by calling one function with an argument list and inspecting what came back,
rather than spawning a process eleven times.

The command line is dispatched by hand rather than with `argparse` — see `## Assumptions`.

Storage is one JSON file, located by `EXPENSES_FILE` or an XDG default and written atomically
(`ADR-0007`). Reading treats a missing key as empty, so WI-0002 and WI-0004 add their kinds of
fact without a migration.

## Steps

1. **Create the package skeleton.**
   - `expenses/__init__.py` — empty.
   - `expenses/__main__.py` — imports `main` from `expenses.cli`, and runs
     `sys.exit(main(sys.argv[1:]))`. Nothing else: it exists so `python3 -m expenses` works.

   Afterwards: `python3 -m expenses` runs and exits non-zero with a message, once step 4 lands.

2. **Write `expenses/storage.py`** — the only module that knows a file exists. Interface:
   - `record_path() -> pathlib.Path` — resolves, in order: `EXPENSES_FILE` if set and non-empty;
     else `$XDG_DATA_HOME/expenses/expenses.json` if `XDG_DATA_HOME` is set and non-empty; else
     `~/.local/share/expenses/expenses.json` (`ADR-0007` point 3).
   - `class RecordError(Exception)` — a stored record that cannot be used. Its `str()` is the
     message the user will see.
   - `load() -> dict` — returns the record. A missing file returns `{"version": 1, "people": []}`;
     that is not an error (`ADR-0007` point 5). A file that cannot be read, does not parse as
     JSON, is not a JSON object, or whose `version` is not `1`, raises `RecordError` naming the
     path. Any key absent from the file reads as empty, so a file written by a later item is still
     readable here and vice versa (`ADR-0007` point 2).
   - `save(record: dict) -> None` — creates the parent directory if needed, writes the JSON to a
     temporary file **in the same directory**, and moves it over the target with `os.replace`
     (`ADR-0007` point 4).

   Afterwards: `load()` on a temporary path returns an empty record; `save()` then `load()` round
   trips; `load()` on a file containing `not json` raises `RecordError`.

3. **Write `expenses/group.py`** — the only module that knows the rules. Interface:
   - `class RuleError(Exception)` — a refusal. Its `str()` is the exact message the criteria
     require; the wording lives with the rule that produces it, and `cli.py` only prints it.
   - `identity_key(name: str) -> str` — surrounding whitespace stripped, internal runs of
     whitespace collapsed to one space, the result case-folded (`ADR-0005` point 3). Accents are
     not folded.
   - `display_name(name: str) -> str` — the name with surrounding whitespace stripped and nothing
     else changed, which is the spelling that is stored and shown (`ADR-0005` point 4). Note that
     this deliberately keeps a doubled *internal* space, which `identity_key` deliberately does
     not: the two differ, and that difference is the point.
   - `validate_name(name: str) -> str` — returns `display_name(name)`, or raises `RuleError` with
     `A name cannot be empty.` when it is empty or only whitespace, or
     `A name cannot contain a comma or an equals sign; those are reserved.` when it contains `,`
     or `=` (`ADR-0005` points 1 and 2).
   - `people(record: dict) -> list[str]` — the display names in the order they were added.
   - `add_person(record: dict, name: str) -> str` — validates, and raises `RuleError` with
     `<existing spelling> is already in the group.` when the identity key matches somebody already
     present; otherwise appends the display name to the record **in place** and returns it. It
     does not save; the caller decides that, so a refusal cannot leave a half-written file.

   Afterwards: the rules are exercisable without a file and without stdout.

4. **Write `expenses/cli.py`** — the only module that prints. Interface:
   - `main(argv: list[str]) -> int` — returns the process exit status. It looks the subcommand up
     in a dispatch table `{"add-person": ..., "people": ...}` and calls the handler with the
     remaining arguments.
   - Every handler returns `0` on success. Every refusal prints one line to standard error and
     returns `1`.
   - `main` catches `RuleError` and `RecordError` around the whole dispatch and turns each into
     its message on standard error and a return of `1`. This is the single place that guarantees
     "never a traceback" (`ADR-0001` point 3) for the paths those two cover.
   - `add-person` handler: exactly one argument. None → `add-person needs a name.`; more than one →
     `add-person takes a single name; quote it if it contains spaces.`, and nothing is added.
     Otherwise call `group.add_person`, `storage.save`, and print `Added <display name>.` to
     standard output.
   - `people` handler: no arguments. Any argument → `people takes no arguments.` (`ADR-0006`
     rule 2). Otherwise print one display name per line, or, when the group is empty,
     `No one is in the group yet.` — both on standard output, exit `0`.
   - Unknown subcommand → `Unknown subcommand: <name>.` followed by a line naming the known
     subcommands, on standard error, return `1`. No subcommand at all → a usage line naming the
     known subcommands, on standard error, return `1`.

   Afterwards: all eleven criteria are observable through `main`.

5. **Create the test package.**
   - `tests/__init__.py` — empty, so `unittest discover` can import the package (`ADR-0008`).
   - `tests/support.py` — a `CliTestCase(unittest.TestCase)` base class that, per test, creates a
     temporary directory, points `EXPENSES_FILE` at a path inside it, restores the environment
     afterwards, and offers `run(*args) -> (code, out, err)` which calls `cli.main(list(args))`
     with stdout and stderr captured. This helper is written once here and reused by WI-0002 to
     WI-0004.

6. **Write the tests**, one module per cluster of criteria, each asserting on the exact strings
   and exit statuses the criteria name:
   - `tests/test_people.py` — AC1, AC2, AC4, AC5, AC9.
   - `tests/test_duplicates.py` — AC6, including all three spellings, and that `people` still
     prints one line afterwards.
   - `tests/test_invalid_names.py` — AC7, AC8, and that nobody was added in either case.
   - `tests/test_cli_surface.py` — AC10 and AC11, including that standard error contains no
     `Traceback (most recent call last)` on every refusal path.
   - `tests/test_persistence.py` — **AC3, and it must use real subprocesses**:
     `subprocess.run([sys.executable, "-m", "expenses", ...])` three times, with `cwd` set to the
     project root and `EXPENSES_FILE` in the environment. Calling `main()` three times in one
     process would pass even if the record were held in a module-level variable, which is exactly
     what AC3 exists to rule out. The same module carries one subprocess check of `python3 -m
     expenses` with no arguments, so that `__main__.py`'s exit status is exercised for real.

7. **Run the project's own commands and record the output**: `python3 -m unittest discover -s
   tests -t . -q` and `python3 -m compileall -q expenses tests`, both from the project root. Both
   must exit `0`.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `add-person "Sam Okafor"` prints `Added Sam Okafor.`, exits 0 | 3, 4 | `tests/test_people.py`: `run("add-person", "Sam Okafor")` returns `(0, "Added Sam Okafor.\n", "")` |
| AC2 — `people` then prints exactly `Sam Okafor` | 3, 4 | `tests/test_people.py`: after the above, `run("people")` returns `(0, "Sam Okafor\n", "")` |
| AC3 — persistence across three separate invocations | 2, 6 | `tests/test_persistence.py`: three `subprocess.run` calls of `python3 -m expenses`; the third's stdout is `Alice\nBob\n` and its exit status `0` |
| AC4 — insertion order, one per line, nothing else | 3, 4 | `tests/test_people.py`: add `Carol`, `alice`, `Bob`; `run("people")` stdout is exactly `Carol\nalice\nBob\n` |
| AC5 — empty group prints `No one is in the group yet.`, exits 0 | 4 | `tests/test_people.py`: `run("people")` on a fresh record returns `(0, "No one is in the group yet.\n", "")` |
| AC6 — duplicate refused for all three spellings | 3, 4 | `tests/test_duplicates.py`: for each of `sam okafor`, `  SAM OKAFOR  `, `Sam  Okafor`, `run("add-person", s)` returns code `1` and stderr `Sam Okafor is already in the group.\n`; then `run("people")` stdout is one line |
| AC7 — empty or whitespace-only name refused | 3, 4 | `tests/test_invalid_names.py`: `run("add-person", "")` and `run("add-person", "   ")` each return code `1`, stderr `A name cannot be empty.\n`; `run("people")` prints the empty-group message |
| AC8 — comma or equals sign refused | 3, 4 | `tests/test_invalid_names.py`: `run("add-person", "Anna,Karin")` and `run("add-person", "a=b")` each return code `1` with the reserved-character message; nobody added |
| AC9 — accents distinct | 3 | `tests/test_people.py`: add `José` then `Jose`; the second returns `0` and `run("people")` prints two lines |
| AC10 — argument arity on both subcommands | 4 | `tests/test_cli_surface.py`: `run("add-person")`, `run("add-person", "Sam", "Okafor")`, `run("people", "extra")` each return `1` with the stated stderr message, and the record is unchanged after the second |
| AC11 — unknown subcommand, and none at all | 4, 6 | `tests/test_cli_surface.py`: `run("no-such-command")` returns `1` with stderr naming `no-such-command`; `run()` returns `1` with a usage message; `tests/test_persistence.py` repeats the no-subcommand case as a subprocess to check `__main__.py`'s exit status |
| all | 4, 6 | every refusal test also asserts that stderr contains no `Traceback (most recent call last)`, which is the general clause at the head of the criteria list |

## Assumptions

1. **The command line is dispatched by hand, not with `argparse`.** The criteria pin the exact
   text of five messages and require specific wording for three arity failures and for an unknown
   subcommand; `argparse` produces its own messages, exits `2` from inside the parser, and would
   have to be subclassed to be overridden — more code than the dispatch it replaces, for seven
   subcommands with fixed shapes. **Reversing it** means rewriting `cli.py` alone: no stored data
   changes, no other module changes, and no acceptance criterion changes, because the criteria
   describe the observable behaviour rather than the mechanism. WI-0002 is the item to revisit
   this on, since it is the first to carry flags.
2. **Refusals exit with status `1`.** `ADR-0001` requires only "non-zero", and every criterion is
   written as "exits non-zero", so nothing depends on the value. **Reversing it** is one constant
   in `cli.py`.
3. **The tests call `cli.main()` in-process, except where AC3 and AC11 need a real process.**
   Capturing streams in-process is what makes eleven criteria cheap to assert exactly; the two
   subprocess tests are there because persistence and `__main__.py`'s exit status are the two
   things in-process testing genuinely cannot prove. **Reversing it** — making every test a
   subprocess — costs a slower suite and a rewrite of `tests/support.py`, and no production code.

## Decisions and ADRs

| decision | where |
|----------|-------|
| One JSON file; its shape; where it lives; atomic write; missing versus corrupt | `ADR-0007` (new) |
| `unittest` as the test framework; `compileall` recorded as a syntax check, not a linter | `ADR-0008` (new) |
| The three-layer module shape and what each layer may know | `docs/architecture/overview.md` v1 (new) |
| The invocation form, exit-code and stream contract | `ADR-0001`, cited, not re-decided |
| What a name may be; when two names are one person; where the identity rule applies | `ADR-0005`, cited, not re-decided |
| The subcommand names `add-person` and `people` | `ADR-0006`, cited, not re-decided |
| Hand-rolled dispatch; exit status `1`; in-process tests | `## Assumptions` above, with reversal costs |

`tracker/project.yaml` now carries the two commands from `ADR-0008`, both of which were run on
this machine — including against a deliberately failing test and a deliberately broken file — to
confirm they exit non-zero when they should.

## Risks

- **The identity rule and the display rule differ by exactly one transformation**, and it is easy
  to write one where the other is meant. If `display_name` collapsed internal whitespace, `Sam
  Okafor` entered as `Sam  Okafor` would print wrong; if `identity_key` did not collapse it, AC6's
  third spelling would be accepted as a second person. Step 3 names both functions separately and
  the tests assert both directions, which is the mitigation.
- **`str.split()` with no argument does both jobs at once** — it strips and splits on runs of
  whitespace — so `" ".join(name.split())` is the whole of the identity normalisation. That is
  convenient enough to be worth stating, because reaching for `strip()` plus `replace("  ", " ")`
  instead would be wrong for three consecutive spaces.
- **AC3 can pass falsely.** A record held in a module-level variable satisfies three in-process
  calls and fails the criterion's actual meaning. Step 6 requires subprocesses for that one test;
  if that requirement is dropped, the criterion stops testing anything.
- **`EXPENSES_FILE` must be honoured on every path, including the error paths.** A test that
  leaked to the real default location would write to the developer's home directory. The base
  class in step 5 sets it per test and restores the environment afterwards; `record_path()` is
  read at call time rather than cached at import, so a test that changes the variable after import
  still works.
- **`os.replace` is atomic only within one filesystem.** Step 2 writes the temporary file in the
  target's own directory, which is what makes that true. Writing it to the system temporary
  directory instead would break the guarantee on a machine where `/tmp` is a different filesystem.

## Out of scope for this item

- Expenses, payments, balances, and the other five subcommands. WI-0002, WI-0003, WI-0004.
- Removing or renaming a person; anything about a person beyond their name.
- Any migration machinery. `ADR-0007` point 2 makes the next two items' additions migration-free,
  so there is nothing to build until a change is made that is not backward-compatible.
- Locking or any handling of two processes writing at once (`docs/product/vision.md` v3).
- A README, packaging metadata, or a console-script entry point. Nothing asks for them, and
  `python3 -m expenses` is the invocation every criterion in this epic is written against.
