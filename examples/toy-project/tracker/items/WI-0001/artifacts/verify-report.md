# Verification report — WI-0001

Verified-commit: 7d86345d6395330a40424832798e6d6362c0a3a7

Branch `wi/WI-0001`, head `7d86345` — the tracker commit that carries `impl-report.md`; the last
code commit under it is `86f4384`, and `git status` showed no uncommitted change to `linecount.py`
or `tests/` at any point during this verification. Everything below was run by this skill against
that head. Fixtures were built fresh under `/tmp/verify-wi0001-XgZc/`, not reused from the tests.

## Verdict

**Pass — all thirteen criteria.** Every criterion was decided by a command run here, against
fixtures built here, with the output quoted below. No defect was found, no bug item was filed, and
nothing was sent back.

## Criteria

Commands are written with `$L` for `linecount.py` and `$F` for the fixture folder of that row.
`cat -A` is used where trailing or leading spaces are part of the criterion; `$` marks end of line.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `python3 $L $F \| cat -A` on a folder holding `notes.md` (128 lines) and `a.py` (7) | `128  notes.md$` / `  7  a.py$` / `135  total$`, exit 0, stderr 0 bytes | byte-for-byte the criterion's own example: three lines, column 3 wide because the total has three digits, two spaces, bare names |
| AC2 | **pass** | `python3 $L $F \| cat -A` on `big.md` (9), `A.md` (3), `Z.md` (3), `a.md` (3); then `python3 $L $F > a.out; python3 $L $F > b.out; diff a.out b.out` | ` 9  big.md$` / ` 3  A.md$` / ` 3  Z.md$` / ` 3  a.md$` / `18  total$`; `diff` printed nothing, `exit=0` | descending by count; the three-way tie resolves `A.md` (0x41) → `Z.md` (0x5A) → `a.md` (0x61), which is byte order and not case-insensitive order. The rerun test is the criterion's own `diff` command |
| AC3 | **pass** | `python3 $L $F \| tail -1 \| cat -A` on the AC2 folder | `18  total$` | 9+3+3+3 = 18, right-aligned in the same 2-wide column as the rows above it, two spaces, the word `total`, last line of stdout |
| AC4 | **pass** | `: > $F/empty.txt`, `full.txt` of 5 lines, then `python3 $L $F \| cat -A` | `5  full.txt$` / `0  empty.txt$` / `5  total$`, exit 0 | the zero-byte file has its own row with count 0, in its sorted position (last, after the 5), and does not disturb the total |
| AC5 | **pass** | a folder holding exactly the criterion's cases — `two_nl.txt`=`a\nb\n`, `two_nonl.txt`=`a\nb`, `one.txt`=`\n`, `zero.txt` empty — then `python3 $L $F` | `2  two_nl.txt` / `2  two_nonl.txt` / `1  one.txt` / `0  zero.txt` / `5  total` | all four of the criterion's numbers, produced through the CLI rather than by calling the function |
| AC6 | **pass** | folder with `a.txt` (4 lines) and `sub/deep.txt` (99 lines); `python3 $L $F > o 2> e` | stdout `4  a.txt$` / `4  total$`; stderr 0 bytes; exit 0 | the subdirectory is neither listed nor counted — the total is 4, not 103 — and nothing is said about it on either stream |
| AC7 | **pass** | folder with `target.txt` (6), `link.txt` → `target.txt`, `dirlink` → `realdir/`, `broken` → a path that does not exist, `plain.txt` (2); `python3 $L $F > o 2> e` | ` 6  link.txt$` / ` 6  target.txt$` / ` 2  plain.txt$` / `14  total$`; stderr 0 bytes; exit 0 | the symlink to a file appears under its **own** name with the **target's** count, and is counted in the total (6+6+2=14). The directory symlink and the broken symlink are absent from stdout and produce no message, exactly as the real subdirectory in AC6 |
| AC8 | **pass** | folder with `.gitignore` (2) and `a.txt` (5); `python3 $L $F` | `5  a.txt` / `2  .gitignore` / `7  total`, exit 0 | the dotfile is listed and counted like any other file |
| AC9 | **pass** | a genuine PNG copied from the system (`/usr/share/pixmaps/hplj1020_icon.png`, `file` reports `PNG image data, 45 x 45, 8-bit/color RGBA`) beside `a.txt` (5) and `b.txt` (3); `python3 $L $F > o 2> e`; `grep -c Traceback o e` | `13  image.png` / ` 5  a.txt` / ` 3  b.txt` / `21  total`; 4 stdout lines for 3 files; stderr 0 bytes; exit 0; `grep -c Traceback` → `0` on both streams | a real binary, not a synthesised one, and it is counted by AC5's rule (13 newline bytes) rather than skipped or marked |
| AC10 | **pass** | (a) an empty folder; (b) a folder holding only `one/` and `two/`; `python3 $L $F > o 2> e` for each | both: stdout exactly `no files$`, stderr 0 bytes, exit 0 | no total row in either case, and `no files` is the whole of stdout |
| AC11 | **pass** | (a) `python3 $L /tmp/.../does-not-exist`; (b) `mkdir noread; chmod 000 noread; python3 $L .../noread` as uid 1000 | (a) stdout 0 bytes, stderr 1 line — `linecount: /tmp/verify-wi0001-XgZc/does-not-exist: No such file or directory` — exit 2. (b) stdout 0 bytes, stderr 1 line — `linecount: /tmp/verify-wi0001-XgZc/ac11/noread: Permission denied` — exit 2 | each message names the path and the problem; one line, on stderr, nothing on stdout, exit 2. Run as a non-root user (`id -u` → 1000), as the criterion requires |
| AC12 | **pass** | (a) `python3 $L README.md`; (b) `python3 $L` with no argument | (a) stdout 0 bytes, stderr `linecount: /…/README.md: Not a directory`, exit 2. (b) stdout 0 bytes, stderr `usage: linecount [-h] folder` + `linecount: error: the following arguments are required: folder`, exit 2 | both wrong invocations fail in the shape the criterion fixes. Case (b) is argparse's own message (ADR-0001), which is two lines rather than one — AC12 constrains the stream and the exit code, not the line count, unlike AC11 |
| AC13 | **pass** | `git clone --branch wi/WI-0001 . /tmp/…/clone` then `python3 -m unittest discover` from the clone root | `Ran 27 tests in 0.626s` / `OK`, exit 0 | run in a **fresh clone** that contains no `.claude/`, no virtualenv and no install step — only `docs/`, `tracker/`, `README.md`, `.gitignore`, `linecount.py`, `tests/`. Python 3.12.3, nothing installed. `grep` over the delivered code confirms the imports are `argparse`, `os`, `sys` (tool) and `os`, `struct`, `subprocess`, `sys`, `tempfile`, `unittest`, `zlib`, `linecount` (tests) — standard library throughout, and there is no dependency manifest in the repository |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` (hard) | **pass** | run by this skill on the branch head: `python3 -m unittest discover` → `Ran 27 tests in 0.653s`, `OK`, exit 0; and again in the fresh clone → 27 tests, `OK`, exit 0 |
| `lint-clean` (hard) | **skipped** | `{{commands.lint}}` is null in `tracker/project.yaml`; the gate runner reports `SKIP` — "there is nothing to run; this gate checked nothing". ADR-0003 records why the project has no linter. What this leaves unchecked is in `## Not verified, and why` |
| `workspace-valid` (hard) | **pass** | `scripts/validate-workspace` → exit 0, 0 errors, 0 warnings, run again by `scripts/transition` at the end of this execution |
| `every-criterion-independently-checked` (hard) | **pass** | the table above: each row is a command this skill ran against a fixture this skill built, with the actual output quoted. No row cites `impl-report.md`. Two criteria were checked by a route the implementation deliberately did not use — a real system PNG for AC9 rather than the generated one, and a fresh `git clone` for AC13 |
| `negative-cases-exercised` (hard) | **pass** | see `## Negative and boundary cases exercised` — nine conditions triggered, none read about |
| `tests-would-fail-without-the-change` (advisory) | **pass** | 14 mutations, each caught; see `## Test sensitivity check` |

## Negative and boundary cases exercised

Every one of these was produced on a real filesystem and the tool actually run against it.

1. **Empty folder** → `no files`, exit 0, no total row (AC10).
2. **Folder of only subdirectories** → `no files`, exit 0 (AC10).
3. **Subdirectory beside a file** → not listed, not counted, nothing on stderr (AC6).
4. **Symlink to a directory** → ignored like a real subdirectory (AC7).
5. **Broken symlink** → ignored, no message, exit 0 (AC7).
6. **Zero-byte file** → row with count 0, not omitted (AC4).
7. **Path that does not exist** → empty stdout, one stderr line, exit 2 (AC11).
8. **Directory with mode `000`, as uid 1000** → empty stdout, one stderr line, exit 2 (AC11).
9. **Path that is a regular file**, and **no argument at all** → empty stdout, stderr message,
   exit 2 (AC12).

Two further conditions outside the criteria were triggered because the delivered code has a
decision about them:

- **A `chmod 000` file inside a readable folder** (ADR-0002) → `linecount: secret.txt: Permission
  denied` on stderr, the file left out of the listing and the total (`5  a.txt` / `5  total`),
  exit 0, no traceback. This is what ADR-0002 specifies.
- **stdout piped into `head`** on a folder of 200 files → `python3 linecount.py $F | head -3`
  printed the three largest (`200  f200.txt`, `199  f199.txt`, `198  f198.txt`) and the pipeline's
  first command exited 0. No `BrokenPipeError`, no traceback. This is EP-001's "can be piped into
  `head`" measure, which no single criterion of this item owns.

## Test sensitivity check

Each behaviour was disabled in `linecount.py`, `python3 -m unittest discover` was run, and the
file was restored with `git checkout -- linecount.py` before the next mutation (script:
`/tmp/verify-wi0001-XgZc/sensitivity.py`, outside the repository; `git status` was clean
afterwards). **14 mutations, 14 caught — none left the suite green.**

| behaviour removed | suite | first tests to fail |
|-------------------|-------|---------------------|
| the total row is not appended | FAIL | 15 tests, including `test_ac1_exact_output_for_two_files`, `test_ac3_last_row_is_the_total_in_the_same_column` |
| column width computed over the counts only, excluding the total | FAIL | `test_ac1_column_is_as_wide_as_the_widest_number_printed`, `test_ac2_ties_break_on_filename_byte_order`, `test_ac7_symlink_to_a_file_is_listed_under_its_own_name` |
| sort ascending instead of descending | FAIL | `test_ac1_exact_output_for_two_files`, `test_ac2_ties_break_on_filename_byte_order`, +2 |
| tie-break by filename dropped (`reverse=True` on count alone) | FAIL | `test_ac2_ties_break_on_filename_byte_order`, +3 |
| zero-count files dropped from the rows | FAIL | `test_ac4_empty_file_is_listed_as_zero` |
| the `+1` for a last line without a newline removed | FAIL | `test_ac5_counting_rule`, `test_ac5_trailing_byte_after_a_chunk_boundary` |
| `is_file(follow_symlinks=True)` → `not is_dir(follow_symlinks=False)` | FAIL | `test_ac7_broken_symlink_is_ignored`, `test_ac7_symlink_to_a_directory_is_ignored` |
| symlinks no longer followed | FAIL | `test_ac7_symlink_to_a_file_is_listed_under_its_own_name` |
| dotfiles filtered out | FAIL | `test_ac8_dotfile_is_listed` |
| files opened as text instead of bytes | FAIL | 16 tests, including `test_ac5_counting_rule` |
| `no files` → empty string | FAIL | `test_ac10_empty_folder`, `test_ac10_folder_holding_only_subdirectories`, `test_ac10_no_rows_is_no_files_and_no_total` |
| the folder-error branch returns 0 instead of 2 | FAIL | `test_ac11_path_that_does_not_exist`, `test_ac11_folder_that_cannot_be_read`, `test_ac12_path_is_a_regular_file` |
| ADR-0002's stderr line removed | FAIL | `test_unreadable_file_is_reported_and_skipped` |
| every entry listed, directories included (`if True:`) | FAIL | `test_ac6_subdirectory_is_ignored`, `test_ac7_*`, `test_ac10_folder_holding_only_subdirectories` |

One observation worth recording: the seventh mutation (listing anything that is not a directory)
was **not** caught by `test_ac6_subdirectory_is_ignored`, because that test's only non-file entry
is a real directory, which that mutation still excludes. AC6 is covered — the fourteenth mutation
shows the test is sensitive to directories being listed — but AC6's test would not notice a
regression that only affected non-file, non-directory entries. Not a defect: no criterion mentions
sockets or device nodes.

## Defects found

None. No criterion of this item failed, so there is nothing to send back; no behaviour delivered
by another item was exercised, so there is no bug to file. (WI-0001 is the first code in the
repository — there is no other item's behaviour to break.)

## Diff review against the plan

`git diff --stat main..wi/WI-0001` shows four new code files and no modification to anything that
existed: `.gitignore` (2 lines, plan step 1), `linecount.py` (117, step 2), `tests/__init__.py` (0,
step 3), `tests/test_linecount.py` (271, step 3); the rest of the diff is `tracker/`. Every
function in `linecount.py` is one plan step 2 names, with the signature it names. There is no
flag, no option, no configuration and no code path that no criterion or ADR accounts for.

The only line in the delivered code that traces to neither a criterion nor a plan step is
`from __future__ import annotations` at the top of `linecount.py`: it has no effect on this file's
behaviour, since no annotation in it is evaluated. It is noise, not scope.

The three deviations declared in `impl-report.md` were checked rather than accepted: the two
commits and their subjects are as described (`git log main..wi/WI-0001`), the four extra tests
exist and each asserts a clause of a criterion that already had a test, and `png_bytes()` builds a
real PNG — which this verification did not rely on, having used a system PNG instead.

## Not verified, and why

- **Lint.** There is no lint command (`commands.lint: null`, ADR-0003), so nothing checked style,
  unused imports, shadowed names, or the `from __future__` line noted above. On a 117-line module
  read at review this is a small gap, but it is a real one and it will recur on every item in this
  project until that ADR is revisited.
- **Non-UTF-8 filenames.** AC2 says "byte order", and the code sorts with `os.fsencode`, which is
  what makes that true for names that are not valid UTF-8. The criterion's own example (`A.md`
  before `a.md`) is verified; a genuinely undecodable filename was not created. The implementation
  report declares the same gap. Reaching it needs a filename the terminal cannot render, and no
  criterion asks for one.
- **Very large folders and very large files.** The plan bounds the item at "a few dozen files,
  occasionally a couple of hundred". Two hundred files were exercised (the `head` case above); a
  folder of thousands, and a file of many gigabytes, were not. The chunked read is exercised at
  3 MiB by `test_ac5_rule_holds_across_chunk_boundary`.
- **Non-POSIX platforms.** AC7 and AC11 assume symlinks and Unix permissions. Everything here ran
  on Linux as uid 1000. Nothing in the item asks for Windows, and the root-guarded tests were not
  exercised in their skipping form (they ran).
- **`--top`.** Not present, not verified — it is WI-0002, and this item's `## Out of scope` says
  so.
