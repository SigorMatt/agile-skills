# Verification report — WI-0001

Verified-commit: 1c65c4f9cffe90192d598301f58474bd5f4d086b

## Verdict

**Pass.** All eleven acceptance criteria were checked by running commands against the branch head
and reading the actual output; all eleven pass. Every criterion's coverage was also checked for
sensitivity by breaking the behaviour and confirming the suite fails — eleven mutations, eleven
caught. No defect found, no criterion ambiguous, nothing sent back, no bug filed.

The criteria were read and the checks derived from them **before** `impl-report.md` was opened, so
that the checks test the criteria rather than the implementation. Where the report and this
verification agree, they agree independently.

## Criteria

Each command below was run from the project root with `EXPENSES_FILE` pointed at a fresh path in a
temporary directory. Output is quoted as captured; `|` marks a line break in a captured stream.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `python3 -m expenses add-person "Sam Okafor"` | exit `0`, stdout `Added Sam Okafor.` + newline (confirmed byte for byte with `od -c`), stderr empty | the space in the name is kept |
| AC2 | **pass** | `python3 -m expenses people`, after AC1 | exit `0`, stdout exactly one line, `Sam Okafor`, stderr empty | `wc -l` = 1, so exactly one line and it is newline-terminated |
| AC2 (spelling rule) | **pass** | `add-person "   Sam  Okafor   "` then `people` | `Added Sam  Okafor.`; `people` prints `Sam  Okafor` | surrounding whitespace stripped, the doubled internal space kept — ADR-0005 point 4 versus point 3, checked in both directions |
| AC3 | **pass** | three separate processes: `add-person Alice`, `add-person Bob`, `people` | `Added Alice.` / `Added Bob.` / `Alice`+`Bob` on two lines, each exit `0` | three real invocations of `python3 -m expenses`, not three calls into one process |
| AC4 | **pass** | `add-person Carol`, `add-person alice`, `add-person Bob`, then `people` | exit `0`, stdout `Carol`, `alice`, `Bob` on three lines, nothing else, stderr empty | insertion order, not alphabetical: `alice` sorts first and prints second |
| AC5 | **pass** | `python3 -m expenses people` on an empty record | exit `0`, stdout `No one is in the group yet.`, stderr empty | the record file does not exist at this point, so this also covers "a missing file is not an error" |
| AC6 | **pass** | with `Sam Okafor` present: `add-person "sam okafor"`, `add-person "  SAM OKAFOR  "`, `add-person "Sam  Okafor"` | each exit `1`, stderr `Sam Okafor is already in the group.`, stdout empty | all three spellings refused, and the message names the stored spelling. `people` afterwards prints one line. `add-person "Sam Okonkwo"` still succeeds, so the rule discriminates rather than refusing everybody |
| AC7 | **pass** | `add-person ""`, `add-person "   "`, `add-person "<tab>"` | each exit `1`, stderr `A name cannot be empty.`, stdout empty | the record file was never created, and `people` afterwards prints the empty-group message |
| AC8 | **pass** | `add-person "Anna,Karin"`, `add-person "a=b"` | each exit `1`, stderr `A name cannot contain a comma or an equals sign; those are reserved.` | `people` afterwards prints the empty-group message, so nobody was added |
| AC9 | **pass** | `add-person "José"` then `add-person "Jose"` then `people` | both adds exit `0`; `people` prints two lines, `José` and `Jose` | accents are not folded together |
| AC10 | **pass** | `add-person` (no name); `add-person Sam Okafor` (unquoted, two arguments); `people extra` | exit `1` with `add-person needs a name.`; exit `1` with `add-person takes a single name; quote it if it contains spaces.`; exit `1` with `people takes no arguments.` | after the two-argument case, `people` prints the empty-group message — the words were not silently joined and stored |
| AC11 | **pass** | `python3 -m expenses no-such-command`; `python3 -m expenses` | exit `1`, stderr `Unknown subcommand: no-such-command.` then a usage line and `Subcommands: add-person, people`; exit `1`, stderr `No subcommand given.` then the same two lines | the first names the unknown subcommand, as the criterion requires. The bare-module exit status was also checked directly: `python3 -m expenses; echo $?` → `1` |
| head-of-list clause | **pass** | every refusal above, with `grep -q 'Traceback (most recent call last)'` on the captured stderr | no match on any of them | eleven refusal invocations across AC6 to AC11, plus the four corrupt-record probes below |

Checkboxes in `item.md` were ticked only after the corresponding row above was produced.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q`, run here on the branch head → exit `0`, `Ran 28 tests in 0.474s`, `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses tests` → exit `0`, no output. Recorded with the caveat ADR-0008 states: this is a syntax check, not a linter, so a green result means every file parses and nothing more |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit `0`, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | the table above — every row is a command run during this verification with its captured output. No row cites `impl-report.md`, and the criteria were read before that report was |
| `negative-cases-exercised` | **pass** | all six refusal criteria triggered, not read about: AC6 (three spellings), AC7 (three empty forms), AC8 (both reserved characters), AC10 (three arity failures), AC11 (both forms). Plus six boundary probes below that no criterion requires |

## Negative and boundary cases exercised

Beyond the criteria, to see what happens where nothing is specified:

| probe | result |
|-------|--------|
| record file contains `not json` | `people` and `add-person` both exit `1` with `<path> is not valid JSON; it has not been changed.`; the file is byte-identical afterwards |
| record file contains `[]` (an array, not an object) | exit `1`, `<path> does not contain an expenses record; it has not been changed.` |
| record contains `{"version":1,"people":[1]}` | exit `1`, `The people in <path> are not a list of names; it has not been changed.` — the case that would otherwise have crashed inside `identity_key` |
| record declares `"version":99` | exit `1`, a message naming both versions; the file is not touched |
| record carries an unknown `expenses` key | `people` works, `add-person Bo` succeeds, **and the unknown key survives the write** — ADR-0007 point 2's forward-compatibility claim, checked rather than assumed |
| `EXPENSES_FILE` points at a directory | exit `1`, `Cannot read <path>: Is a directory.` — an `OSError` turned into a message, not a traceback |
| `EXPENSES_FILE` unset, `XDG_DATA_HOME` set | the record is created at `$XDG_DATA_HOME/expenses/expenses.json` — ADR-0007 point 3's middle branch |

No probe produced a traceback, and no probe overwrote a file it could not read.

## Test sensitivity check

Eleven mutations, one per criterion, each applied to the source, run against the whole suite, and
reverted. **All eleven were caught.**

| mutation | criterion it attacks | caught by |
|----------|----------------------|-----------|
| `identity_key` returns the name unchanged | AC6 | 5 tests, including the cross-process one |
| `add-person` never calls `storage.save` | AC2, AC3 | 12 tests |
| `display_name` collapses internal whitespace | AC1, AC2 | `test_internal_whitespace_is_kept_in_the_stored_spelling` |
| the empty-group message is changed | AC5 | 3 tests |
| `people` returns the list reversed | AC4 | 3 tests |
| the empty-name check is deleted | AC7 | 3 tests |
| the reserved-character check is deleted | AC8 | 4 tests |
| `identity_key` stops case-folding (keeps whitespace collapsing) | AC6 | 5 tests |
| two arguments are joined instead of refused | AC10 | `test_add_person_with_two_arguments_is_refused_and_not_joined` |
| an unknown subcommand returns `0` | AC11 | 3 tests |
| `identity_key` folds accents together | AC9 | `test_accented_letters_are_a_different_person` |

The suite was confirmed green again after the last revert, and `git status` shows no modification
to any tracked source file.

Two of these — the internal-whitespace mutation and the case-folding one — are the pair the plan
named as this item's first risk, and the implementation report records that the suite as first
written did **not** catch the first of them. It does now, and this verification confirms that
independently rather than taking the report's word for it.

## Defects found

None.

## Not verified, and why

- **The default location `~/.local/share/expenses/expenses.json`** (ADR-0007 point 3, third
  branch) was not exercised, because doing so would write to the real home directory of whoever
  runs this. The first branch (`EXPENSES_FILE`) and the second (`XDG_DATA_HOME`) were both checked
  live, and the third differs from the second only in which base directory is used.
- **Atomicity of the write** (ADR-0007 point 4) is asserted by construction — `tempfile.mkstemp`
  in the target's own directory followed by `os.replace` — and was read in the source, not
  demonstrated. Demonstrating it would mean killing the process inside `save`, which no criterion
  requires and which this project has no harness for. What *was* checked is the consequence that
  matters for a user: a record that cannot be read is never overwritten.
- **Concurrent writers.** Out of scope on this item and excluded by `docs/product/vision.md` (v3).
  Nothing here says what two simultaneous `add-person` runs do; on this implementation one would
  silently win.
- **File permissions on the created record.** The implementation report declares that the file
  gets whatever the umask gives. Confirmed by reading the code; not asserted by any criterion, so
  no verdict is recorded either way.
- **`lint-clean` covers syntax only.** ADR-0008 says so; recorded here because a green gate name
  reads stronger than what it checked. Style, unused names and type errors are unchecked in this
  project by design.
