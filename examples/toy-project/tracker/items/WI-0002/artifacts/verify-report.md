# Verification report — WI-0002

Verified-commit: b2d851c665e3ee33b1df3cb559e0a43b325870b5

Branch `wi/WI-0002`, head `b2d851c` — the tracker commit that carries the answer to Q-001; the
last code commit under it is `abc7c66`, and `git status` reported no modified tracked file at any
point. Fixtures were built fresh under `/tmp/verify-wi0002-fJiq/`. Criteria were read before the
implementation report, and AC10 was read **after** Q-001 corrected it.

## Verdict

**Pass — all eleven criteria.** Every one was decided by a command run here against a fixture
built here. No defect was found, no bug filed, nothing sent back. One divergence is recorded
under AC4 that no reader should discover for themselves: the argparse usage line now advertises
`[--top N]`, so the no-argument error message is not the byte-identical one WI-0001 printed. It is
outside AC4's stated scope ("on the same folder") and unavoidable for any implementation of this
item, but it is a difference and it is named here rather than smoothed over.

## Criteria

`$L` is `linecount.py`; `$F` the fixture folder of that row; `cat -A` marks line ends with `$` so
that leading spaces are visible.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | five files (9, 7, 5, 3, 1 lines), `python3 $L --top 3 $F \| cat -A` | ` 9  a.txt$` / ` 7  b.txt$` / ` 5  c.txt$` / `25  total (all 5 files)$`, exit 0, stderr 0 bytes | exactly three file rows, in WI-0001's row format, followed by the total row |
| AC2 | **pass** | the criterion's own fixture — `big.txt` (9) and `a.md`, `b.md`, `c.md` (5 each) — `python3 $L --top 3 $F` | ` 9  big.txt$` / ` 5  a.md$` / ` 5  b.md$` / `24  total (all 4 files)$`; `grep -c c.md` → `0` | the tie at the cut line is broken by filename, not by chance: `c.md` is the one dropped, and the total still counts it (9+15=24) |
| AC3 | **pass** | 27 files summing to 1204 (26×45 + 34), `python3 $L --top 2 $F \| tail -1 \| cat -A` | `1204  total (all 27 files)$` | the total is every file in the folder, and M is the number of rows the same command prints without `--top` — checked directly: the same folder with no flag prints 28 lines, i.e. 27 file rows |
| AC4 | **pass, with one divergence recorded** | the old tool was extracted from git (`git show 461e37f:linecount.py`) and run beside the new one over four folders and three failure paths | stdout **identical**, stderr **identical**, exit codes equal (0/0) on all four folders; `linecount: …/nope: No such file or directory` and `linecount: …/README.md: Not a directory` identical, exit 2/2. WI-0001 AC1's folder still prints `128  notes.md$` / `  7  a.py$` / `135  total$`. **Divergence:** with *no argument at all*, stderr differs — `usage: linecount [-h] folder` became `usage: linecount [-h] [--top N] folder`, exit 2 in both | comparing against the code WI-0001 actually delivered is the only way to check "byte-identical to what WI-0001 delivered"; a test asserting today's bytes would prove nothing. The divergence is outside the criterion's "on the same folder" and is forced by the feature: a usage line that hid the new flag would be wrong. WI-0001's own AC12 asks only for "a message on stderr" and exit 2, both of which hold. Recorded rather than waved through |
| AC5 | **pass** | three files (5, 3, 1), `python3 $L --top 99 $F \| cat -A` | `5  a.txt$` / `3  b.txt$` / `1  c.txt$` / `9  total (all 3 files)$`, exit 0 | every file is listed and the label stays, because the flag was given |
| AC6 | **pass** | two files (5, 3), `python3 $L --top 0 $F` | stdout exactly `8  total (all 2 files)$`, stderr 0 bytes, exit 0 | no file rows, the labelled total still printed, and not an error |
| AC7 | **pass** | `python3 $L --top <v> $F` for `-1`, `abc`, `3.5` and the empty string | `-1` → `linecount: --top: -1 is negative`; `abc` → `linecount: --top: 'abc' is not a whole number`; `3.5` and `''` → the same shape. Each: stdout **0 bytes**, stderr **exactly 1 line**, exit **2** | the failure shape WI-0001 AC11 fixed, including the single line — which is why ADR-0004 kept this out of argparse's hands. `3.5` and `''` were added by this verification; the criterion names only a negative and a non-number |
| AC8 | **pass** | `python3 $L --top 1 $F` vs `python3 $L $F --top 1`; then `python3 $L -t 1 $F` | the two invocations produce byte-identical stdout (`5  a.txt$` / `8  total (all 2 files)$`), byte-identical stderr and equal exit codes (0/0). `-t 1` → stdout 0 bytes, stderr `usage: linecount [-h] [--top N] folder` + `linecount: error: unrecognized arguments: -t …`, exit 2 | the short form is refused rather than merely undocumented |
| AC9 | **pass** | an empty folder with `--top 0`, `--top 3`, `--top 99`; and a folder holding only `sub1/`, `sub2/` with `--top 3` | every case: stdout exactly `no files`, stderr 0 bytes, exit 0, no total row | WI-0001 AC10 survives the flag intact, for every N including 0 |
| AC10 | **pass** | the criterion's example **as corrected by Q-001** — `f00.txt`…`f25.txt` of 46 lines and `small.txt` of 8, i.e. 27 files and 1204 lines — `python3 $L --top 2 $F \| cat -A` | `  46  f00.txt$` / `  46  f01.txt$` / `1204  total (all 27 files)$` | byte for byte what the corrected criterion states. The column is four wide because the total is the widest number printed, and the two shown rows are padded to it. Fixture arithmetic checked independently before running: 26×46+8 = 1204 over 27 files |
| AC11 | **pass** | `python3 -m unittest discover` from the repository root, and again from a **fresh clone** of the branch (`git clone --branch wi/WI-0002 . …`) | `Ran 46 tests in 1.146s` / `OK`, exit 0 in the working tree; `Ran 46 tests in 1.153s` / `OK`, exit 0 in the clone, which contains no `.claude/` and had no install step | the new behaviour is covered by the 19 new tests, and the 27 from WI-0001 are still in the run |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` (hard) | **pass** | run by this skill: 46 tests, exit 0, on the branch head, and 46 tests, exit 0, in a fresh clone |
| `lint-clean` (hard) | **skipped** | `{{commands.lint}}` is null; ADR-0003 records why. The gate checked nothing; see `## Not verified, and why` |
| `workspace-valid` (hard) | **pass** | `scripts/validate-workspace` → exit 0, 0 errors, 0 warnings |
| `every-criterion-independently-checked` (hard) | **pass** | eleven rows above, each a command run here with its output quoted. AC4 was checked against the **old binary** rather than against the current tests — the implementation report could not have provided that evidence |
| `negative-cases-exercised` (hard) | **pass** | see below: eight conditions triggered, two of them beyond what the criteria name |
| `tests-would-fail-without-the-change` (advisory) | **pass** | 13 mutations, 13 caught; table below |

## Negative and boundary cases exercised

1. **`--top 0`** on a folder with files → the total row alone, exit 0 (AC6).
2. **`--top 99`** — N beyond the file count → everything listed, label intact (AC5).
3. **`--top -1`** → one stderr line, exit 2 (AC7).
4. **`--top abc`** → one stderr line, exit 2 (AC7).
5. **`--top 3.5`** → one stderr line, exit 2 — *not named by any criterion; added here*.
6. **`--top ""`** (empty string) → one stderr line, exit 2 — *not named by any criterion; added
   here*. Both behave exactly as `abc` does.
7. **`-t 1`** → argparse's rejection, empty stdout, exit 2 (AC8).
8. **An empty folder, and a folder of only subdirectories**, each with three values of N →
   `no files`, exit 0 (AC9).

One interaction outside every criterion, exercised because the plan predicted it (assumption 3)
and the implementation report declared it untested:

- **`--top 1` on a folder holding an unreadable file** (`chmod 000`, ADR-0002's case): stdout
  `5  a.txt` / `9  total (all 2 files)`, stderr `linecount: secret.txt: Permission denied`, exit 0.
  The skipped file is in neither M nor the total, which is what AC3's own definition of M implies
  ("the number of rows the same command would print without `--top`"). Behaviour matches the
  plan's stated assumption; no defect.

## Test sensitivity check

Each behaviour was disabled in `linecount.py`, `python3 -m unittest discover` was run, and the
file restored with `git checkout` before the next mutation (script:
`/tmp/verify-wi0002-fJiq/sensitivity.py`, outside the repository; `git status` clean afterwards).
**13 mutations, 13 caught.**

| behaviour removed | caught by |
|-------------------|-----------|
| the limit is not applied at all (`rows` instead of `rows[:top]`) | 7 tests, incl. `test_ac1_top_three_prints_three_rows_and_a_total` |
| the last N are taken instead of the first | 5 tests, incl. `test_ac2_tie_at_the_cut_line` |
| the total sums only the rows shown | 7 tests, incl. `test_ac3_total_counts_every_file_and_says_so` |
| the label reverts to plain `total` | 8 tests |
| M counts the shown rows instead of every file | 7 tests |
| `no files` no longer wins over N (`if top is None`) | `test_ac9_empty_folder_whatever_n_is` |
| the negative check in `parse_top` removed | `test_ac7_negative_n`, `test_parse_top_rejects` |
| `--top` given `type=int`, so argparse reports the non-numeric case in two lines | `test_ac7_non_numeric_n` |
| the bad-value branch no longer returns 2 | `test_ac7_negative_n`, `test_ac7_non_numeric_n` |
| the width no longer covers the total | 9 tests, incl. `test_ac10_width_covers_an_explicit_total` |
| an explicit total with no rows falls back to `no files` | `test_ac6_top_zero_prints_only_the_total`, `test_ac6_no_rows_but_an_explicit_total_prints_the_total_row` |
| the plain path stops deriving its own total | 16 tests — every WI-0001 output test |
| a `-t` short form is added | `test_ac8_no_short_form` |

## Diff review against the plan

`git diff main..wi/WI-0002 --stat -- linecount.py tests/` → `linecount.py` +69/−11,
`tests/test_linecount.py` +180/−0. Every hunk traces to a plan step: `parse_top` (step 1), the
`--top` argument (step 2), `format_report`'s two optional parameters (step 3), `main`'s
resolution and report choice (step 4), three new test classes (step 5). The docstring's usage line
is the one hunk outside the plan; `impl-report.md` declares it, and it would have been wrong to
leave it stale.

AC4's mechanical evidence was re-derived here rather than accepted: the test file's diff contains
**0** deleted lines, the old file's 27 `def test_` names all still exist in the new file (`comm`
reports none missing), and the suite reports 46 tests.

## Defects found

None. No criterion of this item failed; no behaviour delivered by another item was found broken —
WI-0001's output is byte-identical on every folder tested, checked against the binary it actually
shipped.

## Not verified, and why

- **Lint.** No lint command exists (ADR-0003), so nothing checked style or unused names on the 69
  changed lines of `linecount.py`. Unchanged from WI-0001, and unchanged for every future item
  until that ADR is revisited.
- **The no-argument usage line.** Recorded under AC4 as a divergence rather than verified as
  compliant: no criterion in either item fixes the *content* of argparse's usage block, so there
  is nothing to check it against. Flagged for `review-close` because it is the one observable
  difference in behaviour WI-0001 delivered.
- **`--top` with a value Python's `int()` accepts but a person might not** — `3_0` (meaning 30),
  `+3`, `" 3 "`. The plan records these as assumption 1; I did not exercise them. They cannot
  produce a wrong count, only an unexpected N.
- **Very large N or very large folders.** `--top 99` on three files is the largest overshoot
  exercised; the item is bounded at a couple of hundred files, and `rows[:top]` cannot fail.
- **The singular label.** `(all 1 files)` on a one-file folder was not run. It is the item's own
  recorded assumption; no criterion states it either way.
- **Non-POSIX platforms**, unchanged from WI-0001.
