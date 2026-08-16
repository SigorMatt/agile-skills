# Implementation report — BUG-0002

## What was built

Three small changes in `linecount.py`, exactly as plan steps 1–3 specify; 175 → 184 lines.

- **`format_report(rows, total=None, label="total", empty="no files")`** — the no-rows branch
  returns `f"{empty}\n"`. The default keeps WI-0001's behaviour byte-for-byte.
- **`main` counts what it skipped** — `rows, unreadable = [], 0`, and the `except OSError` branch
  increments the counter beside the stderr line it already printed. The line itself is unchanged.
- **`main` chooses the sentence** — `if not rows:` now asks *why* there are none:

```python
    if not rows:
        text = format_report(rows, empty="no files could be read") if unreadable \
            else format_report(rows)
    elif top is None:
        text = format_report(rows)
    else:
        text = format_report(rows[:top], sum(count for count, _ in rows),
                             f"total (all {len(rows)} files)")
```

Tests: `tests/test_linecount.py` 515 → 587 lines, 50 → **55** tests, in a new class
`AllFilesSkippedTest`. No existing test was modified; the diff of the test file has no deleted
line.

One commit on `wi/BUG-0002`:
`277c89c linecount: say when a folder's files were all skipped instead of no files (refs BUG-0002)`

The item's own triggers, re-run on the branch head:

```
$ python3 linecount.py /tmp/bug2a          $ python3 linecount.py /tmp/bug2a 2>/dev/null
linecount: one.txt: Permission denied      no files could be read
linecount: two.txt: Permission denied      $ echo $? → 0
no files could be read
$ echo $? → 0                              $ python3 linecount.py /tmp/bug2c   (control)
                                           no files
$ python3 linecount.py /tmp/bug2b          $ echo $? → 0
linecount: g.txt: Permission denied
linecount: f.txt: Permission denied
no files could be read
```

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — trigger A's stdout does not contain `no files`, exit 0, both stderr lines unchanged | the `unreadable` counter routes the no-rows case to a different sentence | `AllFilesSkippedTest.test_ac1_all_unreadable_does_not_claim_no_files`: stdout exactly `b"no files could be read\n"`, `assertNotIn(b"no files\n", stdout)`, exactly two stderr lines each containing `Permission denied`, exit 0 |
| AC2 — trigger A's stdout differs from the control folder's | the two cases now take different branches | `AllFilesSkippedTest.test_ac2_stdout_differs_from_an_empty_folder`: builds both, runs both, asserts the stdouts are unequal and that the empty folder's is exactly `b"no files\n"`, both exit 0 |
| AC3 — trigger B behaves as A | `chmod 444` lists the names but forbids opening them, so every file is skipped and the counter is 2 | `AllFilesSkippedTest.test_ac3_untraversable_folder`: stdout exactly `b"no files could be read\n"`, two stderr lines, exit 0 |
| AC4 — WI-0001 AC10 unchanged | with `unreadable == 0` the call is `format_report(rows)`, whose default is unchanged | `AllFilesSkippedTest.test_ac4_empty_and_subdirectory_only_folders_are_unchanged`: an empty folder and then the same folder holding only `sub/` — each stdout exactly `b"no files\n"`, stderr empty, no total row, exit 0. Plus the existing `test_ac10_empty_folder` and `test_ac10_folder_holding_only_subdirectories`, unmodified |
| AC5 — WI-0002 AC9 unchanged | `--top` is not consulted when there are no rows | the existing `test_ac9_empty_folder_whatever_n_is` (subtests `--top 0`, `3`, `99`), unmodified and passing; and by hand: all three print `no files` on `/tmp/bug2c` |
| AC6 — one readable and one unreadable file is unchanged | that folder has a row, so the branch is never reached | the existing `test_unreadable_file_is_reported_and_skipped`, unmodified; and by hand on `/tmp/bug2d`: `linecount: no.txt: Permission denied` on stderr, `3  ok.txt` / `3  total` on stdout, exit 0 |
| AC7 — the AC1–AC3 tests fail against `6d1e437`; `unittest discover` exits 0 | — | with `linecount.py` restored to `6d1e437`: `FAILED (failures=6, errors=1)`, including `FAIL: test_ac1_all_unreadable_does_not_claim_no_files`, `FAIL: test_ac2_stdout_differs_from_an_empty_folder`, `FAIL: test_ac3_untraversable_folder`. On the branch head: `Ran 55 tests in 1.437s`, `OK`, exit 0 |

The other four failures at `6d1e437` are BUG-0001's three regression tests and an `ERROR` in
`test_the_renderer_still_defaults_to_no_files`, which calls `format_report(..., empty=...)` — a
parameter that code does not have. Both are expected: that commit predates both fixes.

## Deviations from the plan

1. **One test more than the plan named.** `test_the_renderer_still_defaults_to_no_files` asserts
   the renderer's default is untouched *and* that the new parameter works —
   `format_report([]) == "no files\n"` and `format_report([], empty="no files could be read") ==
   "no files could be read\n"`. It is the unit-level guard for AC4, which the plan mapped only to
   end-to-end tests.
2. **Nothing else.** The parameter name and default, the counter, the branch, the sentence and the
   comments are as steps 1–3 specify.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` (hard) | **pass** | `python3 -m unittest discover` on branch head `277c89c` → exit 0, `Ran 55 tests in 1.437s`, `OK`; the permission-guarded tests ran rather than skipping |
| `lint-clean` (hard) | **skipped** | `{{commands.lint}}` is null; ADR-0003. Checked nothing; not a pass |
| `workspace-valid` (hard) | **pass** | `scripts/validate-workspace` → exit 0, 0 errors, 0 warnings |
| `every-criterion-has-a-test` (hard) | **pass** | the table above names a test and the exact bytes or exit code for each of AC1–AC7 |
| `commits-reference-the-item` (hard) | **pass** | `scripts/check-commit-refs BUG-0002 wi/BUG-0002` → exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | the diff touches two files: nine lines of `linecount.py` (a parameter, a counter, a branch, their comments) and one appended test class. `count_lines`, `list_files`, the sort key, the row format and `--top`'s slice and label are untouched |

## What the fix did **not** change

The plan required this to be stated explicitly, because BUG-0002's `## Notes` raises it:

- **`--top`'s label still counts the files that were listed.** On `/tmp/bug2d` (one readable file,
  one `chmod 000`), `python3 linecount.py --top 5` prints `3  ok.txt` and
  `3  total (all 1 files)` — exactly as before this fix. The item's notes call that an observation
  about WI-0002 AC3 defining M two ways in one sentence, not a defect, and nothing here changes
  either definition.
- **ADR-0002's stderr lines and exit status.** Same wording, same stream, same exit 0, one line
  per skipped file.
- **BUG-0001's rule.** An entry that cannot be *resolved* is still silent and still not a file, so
  a folder of nothing but symlink loops still prints `no files` — the counter only counts entries
  that were established to be files and then failed to read.

## What I did not do

- **I did not touch BUG-0003's printing path.** An undecodable filename still raises on the way to
  stdout; that is BUG-0003, still open.
- **I did not put the skipped count on stdout.** ADR-0007 costed that (option D) and rejected it:
  stderr already itemises the files by name.
- **No test for a folder mixing unreadable files with unresolvable entries.** Plan assumption 2
  says it prints `no files could be read` because at least one entry was a file; no criterion
  covers the mixture and I added no coverage for it. It is the one gap in this item a reader might
  expect to find tested.
- **I did not bump `docs/architecture/overview.md`.** The plan settled that: the function table's
  line for `format_report` still reads true, and ADR-0007 carries the decision.
