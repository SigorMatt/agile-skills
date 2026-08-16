# Plan — BUG-0002 A folder whose files are all unreadable prints "no files" on stdout

## Problem

A folder of files nobody can read prints `no files` on stdout and exits 0 — byte-identical to what
a genuinely empty folder prints. The stderr lines that name each skipped file are correct and are
also the only evidence, so a pipe or a redirect keeps the wrong half of the answer. Reproduced on
`main` at `15a0216` before planning, for both of the item's triggers and its control:

```
$ python3 linecount.py /tmp/bug2a 2>/dev/null   → no files     (two chmod 000 files)
$ python3 linecount.py /tmp/bug2b 2>/dev/null   → no files     (folder chmod 444)
$ python3 linecount.py /tmp/bug2c 2>/dev/null   → no files     (genuinely empty)
```

Neither rule is wrong on its own: ADR-0002 says a file that cannot be read is skipped, named on
stderr, exit 0; WI-0001 AC10 says a folder with no files prints `no files`. `main` never
distinguished "there were none" from "I could not read any", which is the misuse ADR-0005
predicted when it wrote that deciding emptiness "is the **caller's** job".

## Approach

Count the files that failed to read, and let that count choose the sentence — `no files` when the
folder really held none, `no files could be read` when it held some and none of them could be
counted (ADR-0007). `format_report` gains one optional parameter so that every byte of the report
still comes out of one function, exactly as ADR-0005 established for `--top`.

Nothing else changes. `count_lines`, `list_files`, the sort key, the row format, the total, the
`--top` slice and label, ADR-0002's stderr lines and every exit status are untouched.

## Steps

1. **Give `format_report` an `empty` parameter** in `linecount.py`:
   `format_report(rows, total=None, label="total", empty="no files")`. The no-rows branch returns
   `f"{empty}\n"` instead of the literal. Extend the docstring to say that the caller chooses the
   sentence because only the caller knows *why* there are no rows, citing ADR-0007. Observable
   result: `format_report([])` is still exactly `"no files\n"`, and
   `format_report([], empty="no files could be read")` is `"no files could be read\n"`.

2. **Count the skipped files in `main`.** Replace the `except OSError` body's single `print` with
   a counter increment beside it:

   ```python
   rows, unreadable = [], 0
   for name in names:
       try:
           rows.append((count_lines(os.path.join(args.folder, name)), name))
       except OSError as exc:
           unreadable += 1
           print(f"linecount: {name}: {exc.strerror or exc}", file=sys.stderr)
   ```

   Observable result: no behaviour change yet; the stderr lines are identical.

3. **Choose the sentence in `main`'s report branch.** Replace `if top is None or not rows:` with:

   ```python
   if not rows:
       # `no files` means the folder held none. If it held some and every one failed to read,
       # say that instead — ADR-0007. `--top` has nothing to limit either way.
       text = format_report(rows, empty="no files could be read") if unreadable \
           else format_report(rows)
   elif top is None:
       text = format_report(rows)
   else:
       text = format_report(rows[:top], sum(count for count, _ in rows),
                            f"total (all {len(rows)} files)")
   ```

   Observable result: trigger A prints `no files could be read` on stdout with its two stderr
   lines and exit 0; an empty folder still prints exactly `no files`; a folder with one readable
   and one unreadable file is unchanged.

4. **Add regression tests to `tests/test_linecount.py`** in a new class `AllFilesSkippedTest`,
   appended after the existing classes; no existing test is modified. The five tests are named in
   the mapping table below. The permission-based ones carry the file's existing
   `@unittest.skipIf(IS_ROOT, NOT_AS_ROOT)` guard.

5. **Demonstrate the AC1, AC2 and AC3 tests fail against `6d1e437`**, which AC7 requires:
   `git show 6d1e437:linecount.py > linecount.py`, run `python3 -m unittest discover`, record the
   failures, restore. The AC4 test passes on both sides — it asserts behaviour that must not
   change — which is the shape AC7 already scopes correctly ("the tests for AC1–AC3 fail").

6. **Run the gates and write `artifacts/impl-report.md`**, mapping AC1–AC7 to evidence and stating
   explicitly whether the fix changed what `--top`'s label counts (it does not).

`docs/architecture/overview.md` needs no version bump: the function table's description of
`format_report` — "the caller may override the total and its label" — still reads true with one
more optional parameter, and no boundary in that document changes. ADR-0007 is where this
decision lives.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — trigger A's stdout does not contain `no files`, exit 0, the two stderr lines unchanged | 2, 3 | `AllFilesSkippedTest.test_ac1_all_unreadable_does_not_claim_no_files`: two `chmod 000` files; asserts stdout is exactly `b"no files could be read\n"`, that `b"no files\n"` is not the stdout, that stderr has exactly two lines each naming a file and `Permission denied`, and exit 0 |
| AC2 — trigger A's stdout differs from the control folder's | 3 | `AllFilesSkippedTest.test_ac2_stdout_differs_from_an_empty_folder`: builds both folders, runs both, asserts the two stdouts are unequal and that the empty one is exactly `b"no files\n"` |
| AC3 — trigger B behaves as A | 3 | `AllFilesSkippedTest.test_ac3_untraversable_folder`: a folder `chmod 444` holding two files; asserts stdout is exactly `b"no files could be read\n"`, exit 0, and two stderr lines |
| AC4 — WI-0001 AC10 unchanged | 1, 3 | `AllFilesSkippedTest.test_ac4_empty_and_subdirectory_only_folders_are_unchanged`: an empty folder and one holding only subdirectories; each asserts stdout exactly `b"no files\n"`, stderr empty, no total row, exit 0. Plus the existing `test_ac10_empty_folder` and `test_ac10_folder_holding_only_subdirectories`, unmodified |
| AC5 — WI-0002 AC9 unchanged | 3 | the existing `test_ac9_empty_folder_whatever_n_is` (subtests for `--top 0`, `3`, `99`), unmodified and passing |
| AC6 — one readable and one unreadable file is unchanged | 2, 3 | the existing `test_unreadable_file_is_reported_and_skipped`, unmodified: the readable file's row, the total row, one stderr line, exit 0 |
| AC7 — the AC1–AC3 tests fail against `6d1e437`; `unittest discover` exits 0 | 4, 5 | the run recorded in step 5 and quoted in `impl-report.md`; the suite on the branch head exits 0 |

## Assumptions

1. **The wording `no files could be read`.** ADR-0007 chose it over silence, a zero total, and a
   count-carrying variant. The criteria pin only that stdout must not claim there are no files, so
   the sentence is the architect's. Reversing it is one default parameter value.
2. **A folder mixing unreadable files with unresolvable entries prints `no files could be read`.**
   At least one entry was a file, so that is the honest half; the unresolvable ones stay silent
   under ADR-0006. No criterion covers the mixture. Reversing it means a second counter.
3. **`--top` is not consulted when there are no rows.** There is nothing to limit, and WI-0002 AC9
   already fixes the empty-folder case for every N. Reversing it would mean printing a total row
   for a folder with no countable files, which BUG-0002 AC1 forbids in spirit and no criterion
   asks for.

## Decisions and ADRs

| decision | where recorded | branch of the preference order |
|----------|----------------|-------------------------------|
| stdout distinguishes "no files" from "none could be read", and the wording of the second | ADR-0007 | decided here, four options costed |
| the judgement lives in `main`, the rendering in `format_report` | ADR-0007, ADR-0005 | documented — ADR-0005 already assigns emptiness to the caller; this fix is that rule applied |
| the per-file stderr lines and exit 0 are unchanged | ADR-0002, BUG-0002 AC1 and AC6 | documented |
| an empty folder, a subdirectory-only folder, and any `--top` on them are unchanged | WI-0001 AC10, WI-0002 AC9, BUG-0002 AC4 and AC5 | documented |
| the wording, the mixed-folder case, and ignoring `--top` when there are no rows | `## Assumptions` | assumed, each with its reversal cost |

## Risks

- **Weakening AC4 while fixing AC1.** The two are one branch apart: `no files` must survive for a
  folder that really has none, including one holding only subdirectories and — since BUG-0001 —
  one holding only entries that cannot be resolved. The AC4 test and the two existing AC10 tests
  are the guard, and the mixed case is stated in assumption 2 rather than left to be discovered.
- **A parser somewhere.** Nothing in the record consumes this output programmatically, but a third
  stdout shape is a real interface change for anyone who did. It is recorded in ADR-0007's
  consequences rather than assumed away.
- **Scope creep into BUG-0003.** The printing path is one line away from where BUG-0003's
  `UnicodeEncodeError` is raised. This item does not touch how text reaches stdout, only which
  text.

## Out of scope for this item

- **BUG-0003.** An undecodable filename still raises on the way to stdout; nothing here changes
  the printing mechanism.
- **What `--top`'s label counts.** A folder of two files where one is skipped still prints
  `total (all 1 files)`. BUG-0002's own notes raise this as an observation about WI-0002 AC3's two
  definitions of M, explicitly not as a defect, and this fix does not change either definition.
  `impl-report.md` must state that it did not.
- Reporting skipped files on stdout, changing their stderr wording, or changing the exit status.
- Any change to `count_lines`, `list_files`, the sort key, the row format, the total, or `--top`'s
  behaviour when there are rows to show.
