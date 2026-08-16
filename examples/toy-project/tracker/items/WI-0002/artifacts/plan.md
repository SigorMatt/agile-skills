# Plan — WI-0002 Add --top N to show only the N largest files

## Problem

`python3 linecount.py --top 3 <folder>` must print at most three file rows — the first three of
the order WI-0001 already fixes — followed by a total row that still counts **every** file in the
folder and says so: `1204  total (all 27 files)`. Without the flag nothing changes at all, down
to the byte. `--top 0` is a legitimate request for no file rows (and still prints the total);
`--top -1` and `--top abc` fail in WI-0001's shape — nothing on stdout, one line on stderr,
exit 2; `-t` is not accepted; and a folder with no files still prints `no files` whatever N is.

It is for someone scanning a folder of a couple of hundred files who wants the few that matter
without piping through another command. The material constraints come from the criteria of two
items at once: WI-0002 AC4 requires that WI-0001's tests pass **unmodified**, and WI-0001's
criteria are closed and may not be edited to make this item easier.

The code this changes is 117 lines of `linecount.py` on `main` (merged from `wi/WI-0001` at
`461e37f`) with 27 passing tests in `tests/test_linecount.py`.

## Approach

Four small changes inside `linecount.py`, no new file, no new module. The renderer keeps its
identity and grows two optional parameters (ADR-0005); the flag's bad values are rejected by our
own code rather than by argparse, because AC7 wants one line and argparse writes two (ADR-0004);
and `main` gains the four-line decision about which report to ask for.

Sorting, counting, listing and the failure paths of WI-0001 are untouched. `--top` slices an
already-sorted list, which is what makes AC2's tie at the cut line fall out of the existing
comparator rather than needing a rule of its own.

## Steps

1. **Add `parse_top(value)` to `linecount.py`**, above `parse_args`. It takes the raw string from
   the command line and returns a non-negative `int`, or raises `ValueError` whose message is the
   reason, ready to print. Two rejections: `int(value)` raising (message: `'<value>' is not a
   whole number`) and a negative result (message: `<n> is negative`). Observable result:
   `parse_top("3")` is 3, `parse_top("0")` is 0, `parse_top("abc")` and `parse_top("-1")` each
   raise `ValueError`.

2. **Add the flag in `parse_args`**: `parser.add_argument("--top", metavar="N", help="show only
   the N largest files")`, with **no** `type=` — the value arrives as a string for step 1 to
   validate (ADR-0004). Nothing else in `parse_args` changes, so `-t 3` remains an unknown option
   that argparse rejects with exit 2, and the no-argument case keeps the exact message WI-0001
   delivered. Observable result: `python3 linecount.py --top 3 <folder>` and `python3
   linecount.py <folder> --top 3` both parse; `python3 linecount.py -t 3 <folder>` exits 2.

3. **Give `format_report` its two optional parameters** — `format_report(rows, total=None,
   label="total")` (ADR-0005). Behaviour, in this order: no rows *and* `total is None` →
   `"no files\n"`; `total is None` → `total = sum(count for count, _ in rows)`; then the existing
   body, with `label` in place of the literal `"total"` and the width still computed over every
   count printed **plus** the total. The docstring must state that an empty `rows` with an
   explicit `total` prints the total row alone, and that deciding "the folder had no files"
   belongs to the caller. Observable result: `format_report([(128, "notes.md"), (7, "a.py")])` is
   unchanged at `"128  notes.md\n  7  a.py\n135  total\n"`; `format_report([], 1204, "total (all
   27 files)")` is `"1204  total (all 27 files)\n"`; `format_report([])` is still `"no files\n"`.

4. **Wire it in `main`.** After `parse_args` and before anything touches the filesystem, resolve
   the flag:

   ```
   top = None
   if args.top is not None:
       try:
           top = parse_top(args.top)
       except ValueError as exc:
           print(f"linecount: --top: {exc}", file=sys.stderr)
           return 2
   ```

   Then, after the existing listing, counting and sorting — which do not change — replace the
   single `print(format_report(rows), end="")` with:

   ```
   if top is None or not rows:
       text = format_report(rows)
   else:
       text = format_report(rows[:top], sum(count for count, _ in rows),
                            f"total (all {len(rows)} files)")
   print(text, end="")
   ```

   `not rows` first is what keeps AC9 true for every N: a folder with no files prints `no files`
   and no total row even when `--top 0` was given. Observable result: the six behaviours of AC1,
   AC3, AC5, AC6, AC9 and AC10, and byte-identical output to WI-0001 whenever `--top` is absent.

5. **Extend `tests/test_linecount.py`.** Add a `TopTest` class for the end-to-end cases and add
   the `parse_top` and `format_report` cases to the existing unit classes. **Do not modify any
   existing test** — AC4 requires WI-0001's tests to pass unmodified, and an edited test is the
   one thing that would make that criterion unverifiable. The tests required are named in the
   mapping table below. Observable result: `python3 -m unittest discover` from the repository
   root exits 0, with the 27 existing tests still among the passes.

6. **Run the gates and write `artifacts/impl-report.md`**: `python3 -m unittest discover` exits 0
   on the branch head; `lint-clean` is reported **skipped** with ADR-0003 as the reason; the
   report maps each of AC1–AC11 to the test that exercises it.

`docs/architecture/overview.md` is **not** an implementation step: `plan` has already updated it
to v2 with the new function table, because `implement` and `verify` do not write to `docs/`.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `--top 3` prints at most three file rows in WI-0001's format, then the total row | 4 | `TopTest.test_ac1_top_three_prints_three_rows_and_a_total`: a folder of five files of known sizes; stdout asserted byte for byte, three file rows in count-descending order plus the total row |
| AC2 — the limit is applied after sorting, so a tie at the cut is broken by filename | 4 | `TopTest.test_ac2_tie_at_the_cut_line`: the criterion's own fixture — `big.txt` (9) and `a.md`, `b.md`, `c.md` (5 each) with `--top 3`; stdout asserted exactly, containing `big.txt`, `a.md`, `b.md` and **no** row for `c.md` |
| AC3 — with `--top`, the total is every file in the folder and the label says so | 3, 4 | `TopTest.test_ac3_total_counts_every_file_and_says_so`: 27 files summing to 1204 lines, `--top 2`; the last stdout line is exactly `1204  total (all 27 files)`. Unit: `FormatReportTest.test_ac3_explicit_total_and_label` |
| AC4 — without `--top`, output and exit code are byte-identical to WI-0001, and its tests pass unmodified | 3, 4, 5 | `TopTest.test_ac4_without_the_flag_output_is_unchanged`: WI-0001 AC1's own folder (`notes.md` 128, `a.py` 7) run with no flag, asserted against the exact bytes `b"128  notes.md\n  7  a.py\n135  total\n"`, empty stderr, exit 0 — the plain `total` label included. Plus mechanical evidence in `impl-report.md`: `git diff main..HEAD -- tests/test_linecount.py` contains no deleted line, and the 27 WI-0001 tests are in the passing run |
| AC5 — N larger than the file count lists every file, and the label stays | 4 | `TopTest.test_ac5_n_larger_than_the_folder`: three files, `--top 99`; all three rows present and the last line is `<sum>  total (all 3 files)` |
| AC6 — `--top 0` prints no file rows, still prints the labelled total, exit 0 | 3, 4 | `TopTest.test_ac6_top_zero_prints_only_the_total`: stdout is exactly one line, `<sum>  total (all M files)`, stderr empty, exit 0 |
| AC7 — `--top -1` and `--top abc` print nothing on stdout, one line on stderr, exit 2 | 1, 4 | `TopTest.test_ac7_negative_n` and `TopTest.test_ac7_non_numeric_n`: stdout empty, `len(stderr.splitlines()) == 1`, the line contains `--top`, exit 2. Unit: `ParseTopTest.test_parse_top_rejects` |
| AC8 — the flag works before or after the folder; `-t` is rejected | 2 | `TopTest.test_ac8_flag_position_is_free`: the two invocations produce equal stdout, stderr and exit code. `TopTest.test_ac8_no_short_form`: `-t 3` → empty stdout, non-empty stderr, exit 2 |
| AC9 — a folder with no files prints `no files` for `--top 0`, `3` and `99` | 4 | `TopTest.test_ac9_empty_folder_whatever_n_is`: loops over the three values; each gives stdout exactly `no files\n`, empty stderr, exit 0, and no total row |
| AC10 — the column is as wide as the widest number printed, the total included | 3 | `TopTest.test_ac10_column_width_includes_the_total`: the criterion's example **as corrected by Q-001** — 27 files summing to 1204 (`f00.txt` … `f25.txt` of 46 lines, `small.txt` of 8), `--top 2` → `  46  f00.txt\n  46  f01.txt\n1204  total (all 27 files)\n`, asserted byte for byte, so the shown rows are padded to the total's width. Also `TopTest.test_ac10_two_largest_are_nine_and_seven` (27 files whose two largest hold 9 and 7 — the half of the original example that *was* buildable) and, at the unit layer, `TopFormatTest.test_ac10_width_covers_an_explicit_total`, which produces the three lines the criterion originally named. *(This row was rewritten by `answer-questions` when Q-001 was answered; as first planned it pointed at the impossible fixture and named the unit test as a member of `FormatReportTest`.)* |
| AC11 — `python3 -m unittest discover` still exits 0, and the new behaviour is covered | 5, 6 | the command itself, from the repository root, with its output quoted in `impl-report.md`; the new tests are the ones named above |

Every step maps to at least one criterion. Nothing in this plan exists for any other reason.

## Assumptions

1. **`parse_top` accepts what Python's `int()` accepts** — a leading `+`, surrounding whitespace,
   and underscore separators (`--top 3_0` means 30). No criterion mentions these. Reversing it is
   a `str.isdigit()` guard in `parse_top`; one function, no interface.
2. **The label is not made plural-aware**: a folder of one file yields `total (all 1 files)`. This
   is the item's own recorded assumption (`## Notes`, from refinement), not a new one. Reversing
   it is one f-string plus a criterion that says what the singular should be.
3. **M in the label counts the files the tool listed**, so a file skipped under ADR-0002 (present
   but unreadable) is in neither M nor the total. AC3 defines M as "the number of rows the same
   command would print without `--top`", which is exactly the listed files, so this follows from
   the criterion rather than being invented — but it is worth stating, because the folder can
   then contain a file that no number on screen accounts for. Reversing it would mean counting
   entries the tool could not read, which contradicts AC3's own definition.
4. **The stderr wording for a bad `--top`** (`linecount: --top: 'abc' is not a whole number`) is
   the architect's; AC7 fixes the stream, the line count and the exit code, not the sentence.
   Reversing it is one message string.

## Decisions and ADRs

| decision | where recorded | branch of the preference order |
|----------|----------------|-------------------------------|
| bad `--top` values are rejected by `parse_top`, not by argparse's `type=` | ADR-0004 | decided here; options A and B costed, both rejected against AC7 and AC4 |
| `format_report` grows `total=None, label="total"` rather than changing shape | ADR-0005 | decided here; duplication and a breaking signature both costed |
| the flag may appear before or after the folder, and `-t` is rejected | WI-0002 AC8, refinement Q4 | documented — argparse gives the first for free, and the second is what it does with an unknown option |
| the total with `--top` sums every file and carries `(all M files)` | WI-0002 AC3, refinement Q1 | documented — the human chose this over both alternatives, in his own words |
| the limit is applied after sorting | WI-0002 AC2, refinement Q3 | documented |
| `no files` still wins over any N | WI-0002 AC9, refinement Q5 | documented |
| the four assumptions above | `## Assumptions` | assumed, each with its reversal cost |
| nothing else in `linecount.py` changes | this plan | decided here: the diff is expected to touch four functions and no other line |

## Risks

- **AC4 is the one that fails silently.** Every other criterion is about new behaviour, which a
  new test will catch. AC4 is about behaviour that must *not* change, and the way it breaks is a
  well-meant tidy-up — reformatting the total row, unifying the error messages (exactly what
  ADR-0004 rejects), or "improving" a WI-0001 test while adding neighbours to it. The mitigation
  is mechanical: WI-0001's 27 tests must still be in the passing set, and the diff of
  `tests/test_linecount.py` must contain no deletions.
- **The `None` sentinel in `format_report`.** It means "derive the total", and with empty rows it
  also means "no files". A caller that forgets to decide emptiness itself prints `no files` for a
  folder that has some. Only `main` calls it, and AC6 and AC9 pin both branches — but this is the
  one place in the file where a future change can be wrong in a way the type system will not
  notice. ADR-0005 records it.
- **`--top` interacting with ADR-0002's skipped files.** If a folder holds an unreadable file, it
  is in neither M nor the total, so the labelled total is a statement about listed files, not
  about directory entries. Assumption 3 names it; no criterion covers the combination, and the
  behaviour follows from AC3's own definition of M.
- **Nothing here is bounded by folder size** any more than WI-0001 was: `rows[:top]` slices a list
  already held in memory. Refinement bounds the folder at a couple of hundred files.

## Out of scope for this item

- Any second flag, any short form, any change to the sort order or the row format, and any way to
  configure what the total counts. AC8 and the item's `## Out of scope` are explicit.
- Selecting by a line-count threshold rather than by rank.
- Making the label plural-aware, changing the plain `total` label when `--top` is absent, and
  touching any WI-0001 criterion or test.
- Recursion, other measures, ignore patterns, packaging — everything EP-001 excludes.
- Anything about `docs/product/`: this item adds a flag the vision already anticipates as the
  deferred second piece of work, and contradicts nothing in it.
