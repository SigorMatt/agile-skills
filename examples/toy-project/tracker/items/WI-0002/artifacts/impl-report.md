# Implementation report — WI-0002

## What was built

`--top N` in `linecount.py`, as four changes inside the one file the plan names — no new module,
no new file. `linecount.py` grew from 117 to 164 lines:

- **`parse_top(value)`** (new) — returns the non-negative int `--top` means, or raises
  `ValueError` carrying the message `main` prints (ADR-0004).
- **`parse_args`** — one new argument, `--top`, with `metavar="N"` and deliberately no `type=`,
  so the value arrives as a string for `parse_top` to judge and `-t` stays an unknown option that
  argparse rejects.
- **`format_report(rows, total=None, label="total")`** — two optional parameters (ADR-0005). With
  neither, it behaves exactly as WI-0001 wrote it, including `no files` for an empty call.
- **`main`** — resolves the flag before touching the filesystem (failing with exit 2 and one
  stderr line if it is bad), and after sorting chooses between the unchanged
  `format_report(rows)` and `format_report(rows[:top], sum(...), f"total (all {len(rows)} files)")`.
  `if top is None or not rows` is what keeps `no files` winning over any N.

Tests: `tests/test_linecount.py` grew from 271 to 451 lines, 27 tests to **46**. The 19 new ones
are in three **new** classes — `ParseTopTest`, `TopFormatTest`, `TopTest` — so that no existing
test or class was touched. `git diff main -- tests/test_linecount.py | grep -c "^-[^-]"` → **0**:
the diff of the test file contains no deleted line at all, which is AC4's mechanical evidence.

One commit on `wi/WI-0002`:
`abc7c66 linecount: add --top N, limiting the rows but not the total (refs WI-0002)`

Observed behaviour on a folder of `notes.md` (128), `a.py` (7), `b.py` (3), `c.py` (1):

```
$ python3 linecount.py $D            $ python3 linecount.py --top 2 $D
128  notes.md                        128  notes.md
  7  a.py                              7  a.py
  3  b.py                            139  total (all 4 files)
  1  c.py
139  total                           $ python3 linecount.py --top 0 $D
                                     139  total (all 4 files)
$ python3 linecount.py --top abc $D  $ python3 linecount.py --top -1 $D
linecount: --top: 'abc' is not a…    linecount: --top: -1 is negative
$ echo $? → 2                        $ echo $? → 2
```

## Acceptance criteria evidence

All tests are in `tests/test_linecount.py`; the whole suite runs with `python3 -m unittest
discover` from the repository root (46 tests, exit 0 — see `## Gates`).

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — `--top 3` prints at most three rows in WI-0001's format, then the total row | `main` slices the sorted rows and hands the slice to the unchanged renderer | `TopTest.test_ac1_top_three_prints_three_rows_and_a_total`: five files (9, 7, 5, 3, 1), `--top 3` → stdout exactly `b" 9  a.txt\n 7  b.txt\n 5  c.txt\n25  total (all 5 files)\n"`, stderr empty, exit 0 |
| AC2 — the limit is applied after sorting, so a tie at the cut is broken by filename | the slice is taken from the list WI-0001's comparator already ordered; no second rule exists | `TopTest.test_ac2_tie_at_the_cut_line`: the criterion's own fixture — `big.txt` (9) and `a.md`, `b.md`, `c.md` (5 each), `--top 3` → exactly `b" 9  big.txt\n 5  a.md\n 5  b.md\n24  total (all 4 files)\n"`, and `assertNotIn(b"c.md", stdout)` |
| AC3 — the total is every file in the folder, and the label says so | `main` passes `sum(...)` over all rows and `f"total (all {len(rows)} files)"` | `TopTest.test_ac3_total_counts_every_file_and_says_so`: 27 files summing to 1204 (26×45 + 34), `--top 2` → the last stdout line is exactly `b"1204  total (all 27 files)"`, and stdout is 3 lines. Unit: `TopFormatTest.test_ac3_explicit_total_and_label` |
| AC4 — without `--top`, everything is byte-identical to WI-0001, whose tests pass unmodified | the no-flag path calls `format_report(rows)` exactly as before; the new parameters default to WI-0001's behaviour | `TopTest.test_ac4_without_the_flag_output_is_unchanged`: WI-0001 AC1's own folder → `b"128  notes.md\n  7  a.py\n135  total\n"`, empty stderr, exit 0. `TopFormatTest.test_ac4_the_old_calls_are_unchanged` re-asserts both one-argument calls. **Mechanical:** all 27 WI-0001 tests are in the passing run, and the test file's diff has zero deleted lines |
| AC5 — N larger than the file count lists everything, label intact | the slice is simply short | `TopTest.test_ac5_n_larger_than_the_folder`: three files, `--top 99` → `b"5  a.txt\n3  b.txt\n1  c.txt\n9  total (all 3 files)\n"`, exit 0 |
| AC6 — `--top 0` prints no file rows, still prints the total, exit 0 | `rows[:0]` is empty, and the explicit total makes the renderer print the total row alone | `TopTest.test_ac6_top_zero_prints_only_the_total`: stdout exactly `b"8  total (all 2 files)\n"`, stderr empty, exit 0. Unit: `TopFormatTest.test_ac6_no_rows_but_an_explicit_total_prints_the_total_row` |
| AC7 — `--top -1` and `--top abc` → nothing on stdout, one stderr line, exit 2 | `parse_top` raises, `main` prints `linecount: --top: <reason>` and returns 2 before listing anything | `TopTest.test_ac7_negative_n` and `TopTest.test_ac7_non_numeric_n`: empty stdout, `len(stderr.splitlines()) == 1`, the line contains `--top`, exit 2. Unit: `ParseTopTest.test_parse_top_rejects` over `-1`, `abc`, `""`, `3.5`, `3x` |
| AC8 — either flag position; `-t` rejected | argparse handles both, and no short form was declared | `TopTest.test_ac8_flag_position_is_free`: `--top 1 <folder>` and `<folder> --top 1` give equal stdout, stderr and exit code, and stdout is `b"5  a.txt\n8  total (all 2 files)\n"`. `TopTest.test_ac8_no_short_form`: `-t 3` → empty stdout, non-empty stderr, exit 2 |
| AC9 — an empty folder prints `no files` whatever N is | `not rows` is tested before the limit is applied | `TopTest.test_ac9_empty_folder_whatever_n_is`: subtests for `--top 0`, `3` and `99` → stdout exactly `b"no files\n"`, stderr empty, exit 0, no total row |
| AC10 — the column is as wide as the widest number printed, the total included | `width` is computed over the counts shown **plus** the total | `TopFormatTest.test_ac10_width_covers_an_explicit_total` produces the criterion's three lines byte for byte: `"   9  big.txt\n   7  next.txt\n1204  total (all 27 files)\n"`. End to end, `TopTest.test_ac10_column_width_includes_the_total` (27 files summing 1204; rows padded to the total's width) and `TopTest.test_ac10_two_largest_are_nine_and_seven` (27 files whose two largest hold 9 and 7). **The criterion's folder cannot be built** — see `## Deviations` and `questions/Q-001.md` |
| AC11 — `python3 -m unittest discover` still exits 0, new behaviour covered | 19 new tests added, none removed | the command itself: `Ran 46 tests in 1.154s`, `OK`, exit 0, from the repository root, nothing installed |

## Deviations from the plan

1. **AC10's worked example describes a folder that cannot exist, and I filed a question rather
   than choosing for myself.** 27 files whose two largest hold 9 and 7 lines sum to at most 243,
   never 1204. The *rule* in AC10's first sentence is unambiguous and is what the code implements;
   the *expected output* is producible at the renderer, and `TopFormatTest.
   test_ac10_width_covers_an_explicit_total` asserts those exact three lines. Only the directory
   is impossible. I did not touch AC10 — criteria are not mine to edit — and I split the
   end-to-end evidence into two realizable fixtures, one keeping the criterion's 27 files and
   1204 total, the other keeping its "two largest hold 9 and 7". `questions/Q-001.md` (to the
   architect, **non-blocking**, with three options and a recommendation) asks how the criterion
   should be corrected. Non-blocking because implementation genuinely was not blocked: nothing
   about the delivered behaviour depends on the answer.
2. **The two new unit tests went into a new class, `TopFormatTest`, instead of into
   `FormatReportTest` as the plan named them** (and likewise `ParseTopTest` is its own class).
   Same tests, same assertions; the reason is AC4's evidence — leaving WI-0001's classes literally
   untouched is what makes "the tests pass unmodified" checkable with `grep -c "^-[^-]"` on the
   diff rather than by reading.
3. **The module docstring's usage line now reads `python3 linecount.py [--top N] <folder>`.** One
   line, no behaviour; the plan did not mention it and a docstring that omits the new flag would
   be wrong on the day it shipped.

Nothing else departs from the plan: the function names, the signature defaults, the two rejection
messages, the `main` wiring and the label text are as steps 1–4 specify.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` (hard) | **pass** | `python3 -m unittest discover` from the repository root on branch head `abc7c66` → exit 0, `Ran 46 tests in 1.154s`, `OK` — the 27 WI-0001 tests among them |
| `lint-clean` (hard) | **skipped** | `{{commands.lint}}` is null; ADR-0003 records why the project has no linter. The gate checked nothing and is not a pass |
| `workspace-valid` (hard) | **pass** | `scripts/validate-workspace` → exit 0 after the board was regenerated for the new question |
| `every-criterion-has-a-test` (hard) | **pass** | the table above names a test function and the exact bytes or exit code it asserts for each of AC1–AC11. AC10's end-to-end half is covered by two fixtures instead of the criterion's own, for the arithmetic reason in `## Deviations` |
| `commits-reference-the-item` (hard) | **pass** | `scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, "all 1 commit(s) on main..wi/WI-0002 name WI-0002" |
| `no-unplanned-scope` (advisory) | **pass** | the diff touches exactly two files. `linecount.py`: one new function, one new argument, two optional parameters, the `main` wiring, and the docstring's usage line. `tests/test_linecount.py`: three new classes appended, zero deletions. No other flag, no refactor of anything WI-0001 delivered |

## What I did not do

- **I did not correct AC10.** Editing a criterion to make it satisfiable is exactly what the
  process forbids; `Q-001` is the route, and `answer-questions` owns the edit.
- **I did not make the label plural-aware.** `(all 1 files)` is what a one-file folder prints, as
  the item's `## Notes` and the plan's assumption 2 both record.
- **I did not restrict what `int()` accepts**, so `--top 3_0` means 30 and `--top " 3 "` means 3.
  Plan assumption 1; no criterion mentions them.
- **I did not touch the WI-0001 failure paths**, so `python3 linecount.py` with no argument still
  prints argparse's two-line usage block, and `-t` does the same. AC7 asks for one line only for
  bad `--top` values, which is why ADR-0004 rejected the tempting `parser.error` override.
- **No test for `--top` combined with an unreadable file** (ADR-0002's skip). The interaction is
  described in the plan's assumption 3 — a skipped file is in neither M nor the total — but no
  criterion covers the combination and I added no test for it. It is the one gap in this item a
  reader might expect to find covered.
