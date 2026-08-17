# Verification report — WI-0003

Verified-commit: 8792e410bb27c9256e466bc77895fb7a85598131

Verified by `verify` v0.1.1 (qa-engineer) on 2026-08-17T00:20:00Z, on branch `wi/WI-0003`.
Every command below was run by this execution against that commit. The implementation report was
read after the criteria, and is cited nowhere as evidence.

## Verdict

**Pass.** All ten acceptance criteria are met, each demonstrated by a command run here. No
criterion failed, none was ambiguous, no bug was filed, and the item is not sent back.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `python3 linecount.py --sort name $F` on a folder holding `Zebra.md` (2 lines), `apple.md` (7), `notes.md` (5) | ` 2  Zebra.md` / ` 7  apple.md` / ` 5  notes.md` / `14  total`, exit 0, stderr 0 bytes | Exactly the criterion's order, uppercase before lowercase. Byte order was checked separately end to end on a folder holding `Aaa.txt`, `bad.txt` and `bad\xff.txt`: output was `Aaa.txt`, `bad.txt`, `bad\xff.txt`, exit 0 — `.` (0x2e) before `\xff`, and an undecodable name neither reorders nor aborts |
| AC2 | **pass** | `python3 linecount.py --sort name` on folder `A` (notes 3, todo 1, ideas 2) and folder `B` (notes 40, todo 12, ideas 7), then `diff` of the two filename columns | `A`: `ideas.md, notes.md, todo.md`; `B`: `ideas.md, notes.md, todo.md`; `diff` reports no difference | Counter-check run deliberately: the same two folders in **count** order give `notes, ideas, todo` and `notes, todo, ideas`, and `diff` exits 1. So the shared order is the flag's doing, not a coincidence of the fixture |
| AC3 | **pass** | `python3 linecount.py --sort count $F` and `python3 linecount.py $F`, compared with `cmp` on stdout and stderr | `stdout: IDENTICAL`, `stderr: IDENTICAL (0 bytes)`, both exit 0 | Spelling out the default costs nothing |
| AC4 | **pass** | `git show main:linecount.py > /tmp/old_linecount.py`, then both versions on the same folder, compared with `cmp` | `stdout: IDENTICAL`, `stderr: IDENTICAL`, both exit 0; output ` 7  apple.md` / ` 5  notes.md` / ` 2  Zebra.md` / `14  total` | Checked against the *previous* tool, not against a description of it. The 60 pre-existing tests are unmodified — `git diff --numstat main..HEAD -- tests/test_linecount.py` → `172 0`, no line removed — and pass. The excepted difference is real and was observed: `usage: linecount [-h] [--top N] folder` → `usage: linecount [-h] [--top N] [--sort KEY] folder` |
| AC5 | **pass** | `python3 linecount.py -s name $F` | exit 2, stdout 0 bytes, stderr `usage: …` + `linecount: error: unrecognized arguments: -s /tmp/…` | Argparse's error, unchanged, which is what the criterion asks for |
| AC6 | **pass** | `python3 linecount.py --sort name $E` and `--sort count $E` on an empty folder | both: stdout exactly `no files\n`, stderr 0 bytes, exit 0 | WI-0001 AC10 intact under both values |
| AC7 | **pass** | `python3 linecount.py --sort size $F`; then `linecount.py $F --sort` and `linecount.py --sort $F` | bad value: exit 2, stdout 0 bytes, stderr **1 line**: `linecount: --sort: 'size' is not 'name' or 'count'`. Trailing `--sort`: exit 2, stdout 0 bytes, `usage:` + `linecount: error: argument --sort: expected one argument`. `--sort <folder>`: exit 2, stdout 0 bytes, `usage:` + `linecount: error: the following arguments are required: folder` | Both halves of the criterion, and the split between our message and argparse's, hold exactly |
| AC8 | **pass** | `--sort name $F`, `$F --sort name`, `--sort=name $F`, compared pairwise with `cmp` | all three exit 0; `stdout: ALL THREE IDENTICAL`, `stderr: ALL THREE IDENTICAL (empty)` | |
| AC9 | **pass** | `python3 linecount.py --top 2 --sort name $F` on the three-file folder | exit 0, stderr 0 bytes, 2 file rows, last line `14  total (all 3 files)` | Shape only, as the criterion says. **Observed selection: `Zebra.md`, `apple.md`** — the two alphabetically first, not the two largest. Recorded as an observation of current behaviour, **not** as a verdict: no criterion fixes it and ADR-0009 records why. Boundaries also exercised: `--top 0 --sort name` prints the total row alone, exit 0; `--top 99 --sort name` prints all three, exit 0 |
| AC10 | **pass** | `python3 -m unittest discover` from the repository root | `Ran 77 tests in 2.428s` / `OK`, exit 0 | 17 tests added by this item in `ParseSortTest`, `SortRowsTest` and `SortTest`; the sensitivity of those tests is checked below |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover` run here on `8792e41` → exit 0, `Ran 77 tests`, `OK` |
| `lint-clean` | **skipped** | `commands.lint` is `null` in `tracker/project.yaml`; ADR-0003 records that no linter ships with CPython and the project may not depend on one. Skipped, never passed — see `## Not verified, and why` |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | Every row above names a command this execution ran and quotes its actual output. The implementation report is cited as evidence nowhere |
| `negative-cases-exercised` | **pass** | See the section below — six error or boundary conditions were triggered, not read about |
| `tests-would-fail-without-the-change` (advisory) | **pass** | Three separate breakages, below |

## Negative and boundary cases exercised

1. **Rejected short form** — `-s name $F` → exit 2, nothing on stdout (AC5).
2. **Bad `--sort` value** — `--sort size $F` → exit 2, exactly one line on stderr with the
   `linecount: --sort: ` prefix (AC7).
3. **Missing `--sort` value, two ways** — `$F --sort` (argparse: "expected one argument") and
   `--sort $F` (argparse: "the following arguments are required: folder"). Both exit 2 with an
   empty stdout (AC7).
4. **Empty folder, both orders** — `no files`, no total row, nothing on stderr, exit 0 (AC6).
5. **`--top` boundaries with `--sort name`** — `--top 0` (total row alone) and `--top 99` (every
   file), both exit 0 (AC9).
6. **A filename that is not valid UTF-8, under `--sort name`** — sorted in byte position, printed
   as `ls -b` prints it, exit 0, no traceback (AC1; the path BUG-0003 was filed about).

## Test sensitivity check

Each break was applied to `linecount.py`, the suite run, and the file restored from a backup;
`git status` afterwards shows no modification.

| break | result |
|-------|--------|
| `sort_rows` ignores `order` and always returns the count order | **3 failures**: `SortRowsTest.test_name_order_is_byte_order`, `SortTest.test_ac1_name_order`, `SortTest.test_ac2_two_folders_line_up` |
| `parse_sort` raises for nothing (accepts any value) | **7 failures**: all six `ParseSortTest.test_parse_sort_rejects` subtests and `SortTest.test_ac7_bad_value_is_one_line` |
| `--sort` declared with argparse `choices=("name", "count")` instead of our own check | **1 failure**: `SortTest.test_ac7_bad_value_is_one_line` — the design choice ADR-0004 forced is itself under test, because argparse's rejection is two lines and the criterion wants one |

The third break is the interesting one: it is a plausible "tidier" refactor that a future
maintainer might apply, and the suite catches it.

## Defects found

**None.** No criterion of this item failed, so there is no send-back; no behaviour delivered by
another item was found to be wrong, so no bug was filed.

Two observations that are explicitly *not* defects, recorded so review can see they were
considered:

- **`--top N --sort name` selects the N alphabetically first.** Verified as shape-only under AC9
  and reported above as an observation. The item's `## Notes` instruct `verify` not to raise a
  defect for the selection being one reading rather than the other, and no criterion says which it
  should be. Nothing here may be cited as settling it.
- **Argparse's `description` still reads "List the files in a folder with their line counts,
  largest first."** That is true of the default and untrue of nothing, no criterion covers it, and
  AC4 excepts the help text from byte-identity. It was already incomplete after WI-0002 added
  `--top`, so it is pre-existing and unchanged by this item, not a regression. `implement`
  declared it under `## What I did not do`; recorded here for the reviewer rather than filed.

## Not verified, and why

- **Lint.** There is no lint command (ADR-0003), so nothing statically checked the 63 changed
  lines of `linecount.py` or the 172 added test lines. They were read by a person here and in
  review; no tool has read them. This is the same gap every item in this epic carries.
- **The help text's content.** `--help`'s body and the argparse `description` are pinned by no
  criterion. Beyond confirming the usage line changed exactly as AC4 excepts, nothing about them
  was verified.
- **Which files `--top N --sort name` selects.** Deliberately unverified: no criterion defines it
  (ADR-0009). Its *shape* was verified under AC9, and the observed selection is recorded above as
  an observation only.
- **Non-POSIX platforms.** Everything was run on Linux with `python3` from this environment. No
  Windows or macOS behaviour was exercised, unchanged from every earlier item in this epic.
- **Very large folders and very long names.** No criterion mentions them and no fixture here
  exceeds three files; the sort is in memory, as it was before this item.
