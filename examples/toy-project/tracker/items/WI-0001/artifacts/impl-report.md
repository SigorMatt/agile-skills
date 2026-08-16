# Implementation report — WI-0001

## What was built

`linecount.py` at the repository root, 117 lines, importing only `argparse`, `os` and `sys`, with
the five functions `artifacts/plan.md` step 2 names and in that order: `count_lines`,
`list_files`, `format_report`, `parse_args`, `main`. Beside it, `tests/` as a package holding
`test_linecount.py` — 27 tests in three classes: `CountLinesTest` and `FormatReportTest` call the
functions directly, `EndToEndTest` runs the script as a subprocess and asserts stdout, stderr and
the exit code as bytes. `.gitignore` keeps the bytecode the test run writes out of the tree.

Two commits on `wi/WI-0001`:

- `5adc619 linecount: count lines per file and print them largest first (refs WI-0001)` —
  `.gitignore`, `linecount.py`, `tests/__init__.py`, and the unit layer of `test_linecount.py`
- `86f4384 tests: end-to-end coverage of every acceptance criterion (refs WI-0001)` — the
  `EndToEndTest` class

Run against a folder holding `notes.md` (128 lines), `a.py` (7 lines) and a subdirectory:

```
$ python3 linecount.py /tmp/demo
128  notes.md
  7  a.py
135  total
$ echo $?
0
$ python3 linecount.py /nope/nope
linecount: /nope/nope: No such file or directory
$ echo $?
2
```

## Acceptance criteria evidence

Every test below is in `tests/test_linecount.py` and runs under `python3 -m unittest discover`
from the repository root (27 tests, exit 0, output in `## Gates`).

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — row format, column width, bare name | `format_report` right-aligns each count in `width = max(len(str(n)))` over every count *and* the total, then two spaces, then the name as `os.scandir` yielded it (a name, never a path) | `EndToEndTest.test_ac1_exact_output_for_two_files` asserts stdout is exactly `b"128  notes.md\n  7  a.py\n135  total\n"` for the folder AC1 describes. `FormatReportTest.test_ac1_format_report_unit` asserts the same string from `format_report` directly; `test_ac1_column_is_as_wide_as_the_widest_number_printed` pins the case where the total is the widest number (`[(6,"a"),(5,"b")]` → `" 6  a\n 5  b\n11  total\n"`); `EndToEndTest.test_ac1_name_is_bare_not_a_path` pins the bare name |
| AC2 — count descending, then filename ascending in byte order; reruns byte-identical | `rows.sort(key=lambda row: (-row[0], os.fsencode(row[1])))` — one total key, so the order cannot depend on `os.scandir`'s | `test_ac2_ties_break_on_filename_byte_order`: `big.md` (9), `A.md` (3), `a.md` (3) → `b" 9  big.md\n 3  A.md\n 3  a.md\n15  total\n"`, so `A.md` precedes `a.md`. `test_ac2_two_runs_are_byte_identical` runs the script twice over a folder of 12 files and asserts stdout, stderr and exit code are equal — the `diff a b` of the criterion, expressed as an assertion |
| AC3 — the total row is last, in the same column, when at least one file is listed | `format_report` appends `f"{total:>{width}}  total"` after the rows, and takes the no-rows branch before it can | `EndToEndTest.test_ac3_last_row_is_the_total_in_the_same_column`: three files of 100, 20 and 3 lines → last line `"123  total"` and 4 lines in all. `FormatReportTest.test_ac3_total_is_the_sum_and_comes_last` |
| AC4 — a zero-byte file is listed as 0, in sorted position | `count_lines` returns 0 for an empty file; nothing filters a zero count | `test_ac4_empty_file_is_listed_as_zero`: stdout is exactly `b"5  full.txt\n0  empty.txt\n5  total\n"` — the row is present, last by the sort, and the total is unaffected |
| AC5 — newline bytes, plus one for a last line without one | `count_lines` counts `b"\n"` per chunk and adds one if the final byte is neither absent nor a newline | `CountLinesTest.test_ac5_counting_rule` asserts exactly the criterion's three examples plus the empty file: `a\nb\n`→2, `a\nb`→2, `\n`→1, ``→0. `test_ac5_rule_holds_across_chunk_boundary` and `test_ac5_trailing_byte_after_a_chunk_boundary` count a file of 3 MiB (three read chunks) with and without a trailing partial line |
| AC6 — a subdirectory is not listed, nothing is said about it, exit 0 | `list_files` keeps only entries where `is_file(follow_symlinks=True)` | `test_ac6_subdirectory_is_ignored`: folder with `sub/` (itself holding a 99-line file) and `a.txt` → stdout exactly `b"4  a.txt\n4  total\n"`, stderr `b""`, exit 0 |
| AC7 — symlink to a file listed under its own name with the target's count; symlink to a directory and broken symlink ignored | the same one predicate: following symlinks makes a link to a file a file, and leaves a link to a directory and a broken link out; the name printed is the link's own | `test_ac7_symlink_to_a_file_is_listed_under_its_own_name` (stdout exactly `b" 6  link.txt\n 6  target.txt\n12  total\n"` — the link's name, the target's count), `test_ac7_symlink_to_a_directory_is_ignored`, `test_ac7_broken_symlink_is_ignored`; the last two assert stdout, empty stderr and exit 0 |
| AC8 — dotfiles listed like any other file | no name is filtered anywhere in the program | `test_ac8_dotfile_is_listed`: `.gitignore` (2 lines) and `a.txt` (5) → `b"5  a.txt\n2  .gitignore\n7  total\n"` |
| AC9 — a non-text file gets a row by the same rule; no traceback | files are opened `"rb"` and never decoded, so no decoding error is reachable | `test_ac9_a_png_is_counted_like_any_other_file` builds a real 1×1 PNG (`png_bytes()`, made with `zlib`/`struct` so no binary fixture is committed), puts it beside two text files, and asserts 4 stdout lines, `image.png` among them, empty stderr, exit 0, and `b"Traceback"` in neither stream. `CountLinesTest.test_ac9_bytes_are_never_decoded` counts a file of invalid UTF-8 (`b"\xff\xfe\n\x00\x80\n"` → 2) |
| AC10 — no files at all → exactly `no files`, no total, exit 0 | `format_report` returns `"no files\n"` for empty rows | `test_ac10_empty_folder` and `test_ac10_folder_holding_only_subdirectories`: stdout exactly `b"no files\n"`, stderr `b""`, exit 0. `FormatReportTest.test_ac10_no_rows_is_no_files_and_no_total` at the unit layer |
| AC11 — missing path, unreadable folder → nothing on stdout, one stderr line naming path and problem, exit 2 | `os.scandir` raises `FileNotFoundError` / `PermissionError`; `main` catches `OSError`, prints `linecount: {folder}: {strerror}` to stderr and returns 2 before anything is written to stdout | `test_ac11_path_that_does_not_exist` and `test_ac11_folder_that_cannot_be_read` (a directory `chmod 0o000`): each asserts empty stdout, exactly one stderr line containing the path, exit 2. Both are decorated `@unittest.skipIf(IS_ROOT, ...)`-style — the unreadable one is; the criterion says "tested as a non-root user". Both **ran** (not skipped) in the gate run below |
| AC12 — path is a regular file, or no argument → nothing on stdout, a stderr message, exit 2 | a regular file makes `os.scandir` raise `NotADirectoryError`, handled by the same branch; no argument is argparse's own error (ADR-0001), which is already stderr and exit 2 | `test_ac12_path_is_a_regular_file` and `test_ac12_no_argument_at_all`: empty stdout, non-empty stderr, exit 2 |
| AC13 — `python3 -m unittest discover` from the repository root exits 0, nothing installed | `tests/` is a package; `linecount.py` imports only `argparse`, `os`, `sys`; the tests import only stdlib plus `linecount` | the command itself: `Ran 27 tests ... OK`, exit 0, on Python 3.12.3 with no installation step. `pip` was never run and there is no dependency manifest in the repository |

Not an acceptance criterion, but delivered and tested because ADR-0002 decided it:
`test_unreadable_file_is_reported_and_skipped` — a `chmod 0o000` file inside a readable folder is
named on stderr, left out of the listing and the total, and the run still exits 0 with the rest
of the folder on stdout.

## Deviations from the plan

1. **The `planned → in-progress` transition happened after the first commit, not before it.**
   The plan follows `implement`'s procedure, which says to move the item to `in-progress` before
   writing code. `scripts/transition` runs *all* of `implement`'s hard gates on every transition
   it makes, and two of them — `tests-pass` and `commits-reference-the-item` — cannot pass before
   any code exists (`NO TESTS RAN`, exit 5; `no commits on main..wi/WI-0001`). The refusal is in
   this item's journal. The alternative was `--force`, which records `[gates forced]` in the
   history reason forever and would have made a genuinely clean gate run look overridden. So the
   first slice (`.gitignore`, `linecount.py`, the unit tests) was committed first and the
   transition made immediately after, with both gates passing for real. The window in which the
   item said `planned` while a branch existed lasted one commit, and `branch: wi/WI-0001` was
   already written into `item.md` by the refused attempt, so a resuming run would have found the
   branch rather than starting over. This is a rough edge in the tooling, not in the plan.
2. **Some test names differ from the plan's, and four tests were added.** The plan named one test
   per criterion; the names delivered are the same tests, occasionally spelled more explicitly
   (`test_ac11_missing_path` → `test_ac11_path_that_does_not_exist`). Four tests exist that the
   plan did not name, all of them additional evidence for criteria that already had a test:
   `test_ac1_name_is_bare_not_a_path`, `test_ac1_column_is_as_wide_as_the_widest_number_printed`,
   `test_ac5_trailing_byte_after_a_chunk_boundary`, `test_ac9_bytes_are_never_decoded`. No new
   behaviour came with them.
3. **The PNG is built in the test rather than committed as a fixture.** `png_bytes()` assembles a
   real 1×1 PNG with `zlib` and `struct`. Same criterion, no binary blob in the repository.

Nothing else departs from the plan: the function names, signatures, sort key, chunk size, message
shapes and exit codes are as step 2 specifies.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` (hard) | **pass** | `python3 -m unittest discover` from the repository root → exit 0, `Ran 27 tests in 0.765s / OK`, run on branch head `86f4384`. Verbose output confirms the two root-guarded tests ran rather than skipping |
| `lint-clean` (hard) | **skipped** | `{{commands.lint}}` is null in `tracker/project.yaml`. ADR-0003 records why the project has no linter: none ships with CPython, and EP-001 and the vision forbid depending on an installed one. The gate checked nothing and is not reported as a pass |
| `workspace-valid` (hard) | **pass** | `scripts/validate-workspace` → exit 0, 0 errors, 0 warnings |
| `every-criterion-has-a-test` (hard) | **pass** | the table above names, for each of AC1–AC13, at least one test function and the exact bytes or exit code it asserts. No criterion rests on reading the code |
| `commits-reference-the-item` (hard) | **pass** | `scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0; both commits on `main..wi/WI-0001` carry `WI-0001` in the subject |
| `no-unplanned-scope` (advisory) | **pass** | the branch adds four files and changes none: `.gitignore` (plan step 1), `linecount.py` (step 2), `tests/__init__.py` and `tests/test_linecount.py` (step 3). Every function in `linecount.py` is one the plan names; there is no option, no flag and no code path that no criterion or ADR asks for |

## What I did not do

- **No `--top`, in any form.** `format_report` takes rows and derives the total from them, so
  WI-0002 will have to change its signature — which is what that item's criteria call for. There
  is no hidden parameter waiting for it.
- **No `BrokenPipeError` handling.** The plan puts it out of scope: at the folder sizes this item
  claims the report fits in a pipe buffer, and no criterion mentions it. If it is ever observed,
  it is a bug item.
- **No packaging, no `linecount` on the PATH, no README change.** None is asked for by any
  criterion, and the README is one line naming the project.
- **No test for a filename that is not valid UTF-8.** `os.fsencode` in the sort key is there to
  make AC2's byte order true for such names, and the criterion's own example (`A.md` before
  `a.md`) is covered, but a genuinely undecodable filename is untested. It is the one place where
  a reader might expect more coverage than there is.
- **Nothing was fixed outside this item.** Nothing needed it: this is the first code in the
  repository.
