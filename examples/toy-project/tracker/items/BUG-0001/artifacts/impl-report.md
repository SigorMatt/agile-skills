# Implementation report — BUG-0001

## What was built

One `try` / `except OSError` in `list_files`, exactly as plan step 1 specifies, plus the docstring
that states the rule and cites ADR-0006. `linecount.py` grew from 164 to 175 lines; no other
function was opened.

```python
for entry in entries:
    try:
        resolved = entry.is_file(follow_symlinks=True)
    except OSError:
        resolved = False
    if resolved:
        names.append(entry.name)
```

`main`'s folder handler is untouched, so an `OSError` from `os.scandir` itself still means the
folder failed and still exits 2 — which is what AC5 requires and what the new
`test_ac5_an_unreadable_folder_still_exits_2` guards.

Tests: `tests/test_linecount.py` grew from 451 to 515 lines, 46 tests to **50**, in a new class
`UnresolvableEntryTest` appended after the existing ones. No existing test was modified —
`git diff main..HEAD -- tests/test_linecount.py` contains no deleted line.

One commit on `wi/BUG-0001`:
`06fc185 linecount: ignore an entry that cannot be resolved instead of aborting (refs BUG-0001)`

The item's own reproduction steps, re-run against the branch head:

```
$ python3 linecount.py /tmp/bug1a   (trigger A, symlink loop)      3  ok.txt / 3  total   exit 0
$ python3 linecount.py /tmp/bug1d   (self-referential symlink)     1  ok.txt / 1  total   exit 0
$ python3 linecount.py /tmp/bug1b/folder  (trigger B, untraversable target)
                                                                   2  ok.txt / 2  total   exit 0
$ python3 linecount.py /tmp/bug1c   (control, broken symlink)      1  ok.txt / 1  total   exit 0
```

Before the fix, the first three printed nothing on stdout, named the folder on stderr, and exited
2.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — trigger A prints `3  ok.txt` and `3  total`, nothing on stderr, exit 0 | the loop's two legs raise `OSError` from `is_file`, are caught, and are treated as not-a-file | `UnresolvableEntryTest.test_ac1_symlink_loop_does_not_abort_the_listing`: asserts stdout is exactly `b"3  ok.txt\n3  total\n"`, stderr `b""`, exit 0. Also run by hand on the item's own `/tmp/bug1a` |
| AC2 — a self-referential symlink gives the same shape | same branch | `UnresolvableEntryTest.test_ac2_self_referential_symlink`: same three assertions. Also run by hand on `/tmp/bug1d` |
| AC3 — trigger B prints `2  ok.txt` and `2  total`, exit 0, folder not blamed | a link whose target sits in a `chmod 000` directory raises `PermissionError` from `is_file` and takes the same branch | `UnresolvableEntryTest.test_ac3_symlink_into_an_untraversable_directory`: stdout exactly `b"2  ok.txt\n2  total\n"`, exit 0, stderr empty (ADR-0006 chose silence, which AC3 leaves to `plan`), and `assertNotIn(folder, stderr)` — the folder is never named. Also run by hand on `/tmp/bug1b/folder` |
| AC4 — WI-0001 AC7's three named cases unchanged | the predicate is unchanged when it does not raise | the existing `test_ac7_symlink_to_a_file_is_listed_under_its_own_name`, `test_ac7_symlink_to_a_directory_is_ignored`, `test_ac7_broken_symlink_is_ignored`, unmodified and passing in the same run; plus the control folder `/tmp/bug1c` by hand |
| AC5 — WI-0001 AC11 unchanged: a mode `000` folder still exits 2 | `main`'s folder handler was not touched; the new `except` is inside `list_files`'s loop, not around `os.scandir` | `UnresolvableEntryTest.test_ac5_an_unreadable_folder_still_exits_2`: empty stdout, exactly one stderr line naming the folder, exit 2; and the existing `test_ac11_folder_that_cannot_be_read` |
| AC6 — the regression tests fail against `6d1e437`, and `unittest discover` exits 0 | `linecount.py` was restored to `6d1e437` with the new tests in place, the suite run, then restored | **three of four fail, and the fourth cannot** — see below and `questions/Q-002.md`. `python3 -m unittest discover` exits 0 on the branch head: `Ran 50 tests in 1.380s`, `OK` |

### AC6's demonstration, in full

With `git show 6d1e437:linecount.py > linecount.py` and the new tests in place:

```
FAIL: test_ac1_symlink_loop_does_not_abort_the_listing
FAIL: test_ac2_self_referential_symlink
FAIL: test_ac3_symlink_into_an_untraversable_directory
Ran 50 tests in 1.381s
FAILED (failures=3)
```

then `linecount.py` restored and the suite green again at 50 tests.

`test_ac5_an_unreadable_folder_still_exits_2` passes at `6d1e437`, and must: AC5 is behaviour that
is **unchanged** by this fix, so a test asserting it cannot fail against the old code without
contradicting AC5 itself. AC6's "each fails" cannot hold for that one test. I did not edit AC6;
`questions/Q-002.md` (non-blocking, to the architect) states the problem, quotes the measurement,
and recommends scoping the failing clause to AC1–AC3 — the wording BUG-0002's AC7 already uses.

## Deviations from the plan

1. **A question was filed about AC6's wording** (`Q-002`), which the plan did not anticipate. The
   plan's step 3 already stated the expected outcome — "the three tests for AC1, AC2 and AC3 fail
   on the old code and pass on the new; the AC5 test passes on both" — so the substance is as
   designed; what the plan did not do was notice that AC6's text says "each". Filed non-blocking:
   nothing about the delivered behaviour depends on the answer.
2. **Nothing else.** The code change, its placement, the `except OSError` breadth, the docstring
   citation, the test class name and the four test names are as steps 1 and 2 specify.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` (hard) | **pass** | `python3 -m unittest discover` from the repository root on branch head `06fc185` → exit 0, `Ran 50 tests in 1.380s`, `OK`. The two root-guarded tests ran rather than skipping |
| `lint-clean` (hard) | **skipped** | `{{commands.lint}}` is null; ADR-0003 records why. Checked nothing; not a pass |
| `workspace-valid` (hard) | **pass** | `scripts/validate-workspace` → exit 0, 0 errors, 0 warnings |
| `every-criterion-has-a-test` (hard) | **pass** | the table above names a test and the exact bytes or exit code it asserts for each of AC1–AC6 |
| `commits-reference-the-item` (hard) | **pass** | `scripts/check-commit-refs BUG-0001 wi/BUG-0001` → exit 0, "all 1 commit(s) on main..wi/BUG-0001 name BUG-0001" |
| `no-unplanned-scope` (advisory) | **pass** | the diff touches two files: eleven lines of `linecount.py` (the `try`/`except` and the docstring) and one appended test class. No other function, no output format, no other bug's symptom |

## What I did not do

- **I did not fix BUG-0002's symptom**, though this fix walks past it: a folder whose entries are
  *all* unresolvable now prints `no files`, which is the same false answer BUG-0002 is about from
  a different cause. It is BUG-0002's, it is named in this item's plan under `## Risks` and
  `## Out of scope for this item`, and whoever fixes BUG-0002 should check this case against their
  fix.
- **I did not touch BUG-0003's printing path.**
- **I did not report unresolvable entries on stderr.** ADR-0006 decided silence and AC1 requires
  it; option B in that ADR is the alternative if a future criterion ever asks for it.
- **I did not narrow `except OSError` to a tuple of errnos.** Plan assumption 2: naming a subset
  would leave the next unlisted errno as a fresh instance of this same bug.
- **No test for an entry that is neither file nor directory nor symlink** — a socket or a device
  node in the folder. `is_file()` returns `False` for them without raising, so they are ignored
  and always were; no criterion mentions them and I added no coverage.
