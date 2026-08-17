# Implementation report — WI-0003

Written by `implement` v0.1.0 (developer) on 2026-08-17T00:12:00Z, on branch `wi/WI-0003`
(commit `214dc3d`, one commit on `main..wi/WI-0003`).

## What was built

`linecount.py` gains two functions and loses one inline expression:

- **`parse_sort(value)`** — returns `"name"` or `"count"`, or raises `ValueError` whose text is the
  reason. Sits beside `parse_top` and has the same contract, for the reason ADR-0004 gives: the
  value is judged in our code so the message is one line, while argparse keeps every usage error
  it already owned.
- **`sort_rows(rows, order)`** — returns a new list in the requested order: count descending then
  name ascending, or name ascending. Both keys compare `os.fsencode`d names, so the order does not
  depend on `LANG` and is defined for a name that is not valid UTF-8 (ADR-0008). This is now the
  only place in the tool where either order is written down.
- **`parse_args`** declares `--sort` with `metavar="KEY"`, `default="count"`, no `type=` and no
  `choices=`. The default is what makes `--sort count` and no flag the same code path.
- **`main`** validates `--sort` immediately after `--top` and before the folder is read, then calls
  `rows = sort_rows(rows, order)` where it used to call `rows.sort(...)` inline. Its three printing
  branches, including `rows[:top]`, are unchanged.

The module docstring records the new usage line and what the two orders are. 17 tests were added
to `tests/test_linecount.py`; the 60 that were already there are byte-for-byte unmodified
(`git diff -U0 tests/test_linecount.py` removes no line of the file).

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|--------------------|----------|
| AC1 | `sort_rows(..., "name")` keys on `os.fsencode(name)` alone | `SortTest.test_ac1_name_order` asserts stdout is exactly `b" 2  Zebra.md\n 7  apple.md\n 5  notes.md\n14  total\n"` with stderr empty and exit 0 — the criterion's own folder, uppercase first. Unit half: `SortRowsTest.test_name_order_is_byte_order`, and `test_name_order_survives_a_name_that_is_not_utf_8` |
| AC2 | the name order does not read the counts, so equal names give equal order | `SortTest.test_ac2_two_folders_line_up` builds `A` (3/1/2 lines) and `B` (40/12/7 lines) with the same three names, asserts the filename column of both is `[ideas.md, notes.md, todo.md]`, and asserts the two stdouts *differ* so the shared order is not an artefact of identical files |
| AC3 | `default="count"` means no flag and `--sort count` take the same branch | `SortTest.test_ac3_count_is_byte_identical_to_no_flag` compares stdout, stderr and returncode of `--sort count <folder>` against `<folder>` |
| AC4 | nothing on the no-flag path changed except which function holds the key | The 60 pre-existing tests pass unmodified — `python3 -m unittest discover` → `Ran 77 tests … OK` — plus `SortTest.test_ac4_default_output_is_still_the_count_order` asserting the exact bytes `b" 7  apple.md\n 5  notes.md\n 2  Zebra.md\n14  total\n"`. The usage/help text did change, as AC4 excepts: `usage: linecount [-h] [--top N] [--sort KEY] folder` |
| AC5 | no short form was declared | `SortTest.test_ac5_no_short_form`: `-s name <folder>` → stdout empty, stderr non-empty, exit 2 |
| AC6 | `sort_rows` on an empty list is a no-op, and the `if not rows:` branch is untouched | `SortTest.test_ac6_empty_folder_whatever_the_order` runs both values on an empty folder: stdout exactly `no files\n`, stderr empty, exit 0 |
| AC7 | `parse_sort` raises; `main` prints one line and returns 2. A missing value never reaches us | `SortTest.test_ac7_bad_value_is_one_line` asserts stdout empty, `len(stderr.splitlines()) == 1`, the prefix `linecount: --sort: `, exit 2. Observed: `linecount: --sort: 'size' is not 'name' or 'count'`. `SortTest.test_ac7_missing_value_is_argparse_s` covers both missing-value spellings: stdout empty, `usage:` in stderr, exit 2. Unit half: `ParseSortTest` |
| AC8 | argparse handles position and the `=` form; we added nothing | `SortTest.test_ac8_spellings_agree` compares all three spellings pairwise on stdout, stderr and returncode |
| AC9 | the slice was not touched, so the combination keeps WI-0002's shape | `SortTest.test_ac9_top_and_sort_together_keep_their_shape`: exit 0, stderr empty, at most two file rows, last line ends `total (all 3 files)`. It asserts nothing about which files, by design (ADR-0009) |
| AC10 | tests added in `tests/`, run with the project's own command | `python3 -m unittest discover` from the repository root → exit 0, `Ran 77 tests in 2.305s`, `OK`. New classes: `ParseSortTest`, `SortRowsTest`, `SortTest`, plus the `row_names` helper |

## Deviations from the plan

- **One comment the plan did not name.** Step 5 said to leave the `rows[:top]` branch exactly as
  it is. Its code is unchanged, but I added five comment lines above the slice recording that "the
  order above" is now `--sort`'s, that the selection is unspecified on purpose, and that ADR-0009
  is where that is written down. ADR-0009's own `## Consequences` says the cost of option D is
  carried by a reader who has only the code, so the pointer belongs there. No behaviour changed.
- **`parse_args`' docstring** was updated as well as the module docstring (step 6 named only the
  module docstring). It described `argv` as being turned into "the folder path and the raw `--top`
  value", which would have been wrong after step 2.
- Nothing else. The eight steps were executed in order, and steps 1–5 are exactly the functions and
  lines the plan named.

## Gates

Run on the branch head (`214dc3d`), after the last change.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover` → exit 0, `Ran 77 tests in 2.305s`, `OK` |
| `lint-clean` | **skipped** | `commands.lint` is `null` in `tracker/project.yaml`. ADR-0003 records why the project has no linter and may not add one. Skipped, not passed: the 63 changed lines of `linecount.py` were read by a person and by no tool |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | Every row of the table above names a test function, not a file to read. AC4 additionally rests on the unmodified 60 |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → `all 1 commit(s) on main..wi/WI-0003 name WI-0003`, exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | The diff is 63 lines of `linecount.py` and 172 of tests. Every hunk traces to a plan step: docstring (6), `parse_sort` (1), `--sort` declaration (2), `sort_rows` (3), validation in `main` (4), the one changed sort line (5), tests (7). The two exceptions are declared under Deviations |

## What I did not do

- **I did not decide what `--top N --sort name` selects.** With the slice untouched it takes the N
  alphabetically first: on the AC1 folder, `--top 2 --sort name` prints `Zebra.md` and `apple.md`,
  not the two largest. That is a fact about today's code, recorded here because the item asked for
  it to be recorded — it is not a decision, nobody agreed to it, and ADR-0009 says what to change
  if the human wants the other reading. I filed no question about it: the item's `## Notes`
  instruct `plan` and `implement` not to, because the human declined to have it settled by anyone
  else.
- **I did not update the argparse `description`**, which still reads "List the files in a folder
  with their line counts, largest first." That remains true of the default and no criterion covers
  it, but it no longer describes the whole interface. Left alone rather than widened into
  unrequested scope; a reviewer may reasonably think it should be revisited.
- **I did not add an end-to-end test for a non-UTF-8 name under `--sort name`.** The byte-order
  rule is covered at the unit layer (`test_name_order_survives_a_name_that_is_not_utf_8`) and no
  criterion asks for it end to end; BUG-0003's own class already covers that path for the default
  order.
- **I did not touch `format_report`, `count_lines` or `list_files`**, nor any existing test.
