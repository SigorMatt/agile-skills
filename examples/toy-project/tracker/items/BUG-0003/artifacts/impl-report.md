# Implementation report — BUG-0003

## What was built

Plan steps 1 and 2, and nothing else. `linecount.py` 185 → 191 lines; the only behavioural change
is the last write in `main`:

```python
    # The report is data, not text: a file's name is echoed as the bytes the filesystem gave us,
    # so a name that is not valid UTF-8 prints as `ls -b` and `wc` print it, and the output does
    # not depend on the locale (BUG-0003, ADR-0008).
    sys.stdout.buffer.write(os.fsencode(text))
    sys.stdout.buffer.flush()
```

replacing `print(text, end="")`, plus one sentence in the module docstring saying that names are
bytes too and citing ADR-0008. Everything that builds `text` is untouched.

Tests: `tests/test_linecount.py` 587 → 642 lines, 55 → **60** tests, in a new class
`UndecodableNameTest` carrying `@unittest.skipUnless(os.name == "posix", …)`. Its `setUp` builds
the item's own folder with **bytes** paths — `os.path.join(os.fsencode(self.folder),
b"bad\xff.txt")` — because the name cannot be expressed as valid UTF-8 text. No existing test was
modified; the test file's diff has no deleted line.

One commit on `wi/BUG-0003`:
`8634781 linecount: write the report as bytes so an undecodable name prints (refs BUG-0003)`

The item's reproduction folder, on the branch head, piped through `cat -v` so the raw byte is
visible (`M-^?` is `0xFF`):

```
$ python3 linecount.py /tmp/bug3 | cat -v      $ python3 linecount.py --top 1 /tmp/bug3 | cat -v
3  badM-^?.txt                                 3  badM-^?.txt
2  good.txt                                    5  total (all 2 files)
5  total
$ echo $? → 0
```

Before the fix: a `UnicodeEncodeError` traceback on stderr, empty stdout, exit 1.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — two file rows and a total, exit 0, no `Traceback` or `UnicodeEncodeError` on either stream | the report never crosses stdout's text codec | `UndecodableNameTest.test_ac1_undecodable_name_does_not_abort_the_report`: stdout exactly `b"3  bad\xff.txt\n2  good.txt\n5  total\n"`, stderr `b""`, exit 0, and both markers asserted absent from both streams |
| AC2 — the row is sorted and formatted by the same rules: count 3, first, right-aligned with two spaces | nothing about assembly changed; the sort key was already `os.fsencode` | `UndecodableNameTest.test_ac2_the_row_follows_the_same_rules`: the first stdout line is exactly `b"3  bad\xff.txt"` — count, position and spacing in one assertion. The spelling is ADR-0008's choice: the raw byte, as `ls -b` and `wc` write it |
| AC3 — two runs give byte-identical stdout | the write is deterministic | `UndecodableNameTest.test_ac3_two_runs_are_byte_identical`: stdout, stderr and exit code equal across two runs |
| AC4 — `--top 1` prints one row and WI-0002 AC3's total row, exit 0 | `--top` slices before the write, unchanged | `UndecodableNameTest.test_ac4_top_one_on_that_folder`: stdout exactly `b"3  bad\xff.txt\n5  total (all 2 files)\n"`, exit 0 |
| AC5 — ASCII folders unchanged; WI-0001 and WI-0002 tests pass unmodified; WI-0001 AC1's example byte-identical | `os.fsencode` of an ASCII string is its ASCII bytes | `UndecodableNameTest.test_ac5_ascii_folders_are_byte_identical`: WI-0001 AC1's own folder → `b"128  notes.md\n  7  a.py\n135  total\n"`, empty stderr, exit 0. Plus all 55 earlier tests passing unmodified in the same run, and a test-file diff with 0 deleted lines |
| AC6 — the AC1, AC2 and AC4 tests fail against `6d1e437`; `unittest discover` exits 0 | — | with `linecount.py` restored to `6d1e437`: `FAIL: test_ac1_undecodable_name_does_not_abort_the_report`, `ERROR: test_ac2_the_row_follows_the_same_rules`, `FAIL: test_ac4_top_one_on_that_folder`. On the branch head: `Ran 60 tests in 1.794s`, `OK`, exit 0 |

### One detail worth stating plainly

At `6d1e437`, `test_ac2` reports **ERROR** rather than **FAIL**: stdout is empty there, so
`splitlines()[0]` raises `IndexError` before any assertion runs. It does not pass, which is what
AC6 requires, but "fails" and "errors" are different words in a unittest summary and a reader
comparing them should not have to guess which happened.

Also honest, and not required by any criterion: **`test_ac3` passes at `6d1e437`**. Two runs of the
old code produce identical empty stdout and identical tracebacks, so byte-identity holds for a tool
that crashes consistently. AC6 does not list AC3's test, and rightly — the test is meaningful only
beside AC1's, which pins what those identical bytes must be.

## Deviations from the plan

1. **One test more than the plan named.** The plan's mapping table listed four tests;
   `test_ac2_the_row_follows_the_same_rules` was split out from AC1's exact-bytes assertion so that
   AC2 has evidence of its own rather than sharing AC1's line. Same assertions, one more name.
2. **Nothing else.** The replacement lines, the docstring sentence, the class name, the POSIX
   guard and the bytes-path fixture are as steps 1–3 specify.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` (hard) | **pass** | `python3 -m unittest discover` on branch head `8634781` → exit 0, `Ran 60 tests in 1.794s`, `OK`. The POSIX-guarded class ran rather than skipping |
| `lint-clean` (hard) | **skipped** | `{{commands.lint}}` is null; ADR-0003. Checked nothing; not a pass |
| `workspace-valid` (hard) | **pass** | `scripts/validate-workspace` → exit 0, 0 errors, 0 warnings |
| `every-criterion-has-a-test` (hard) | **pass** | the table above names a test and the exact bytes or exit code for each of AC1–AC6 |
| `commits-reference-the-item` (hard) | **pass** | `scripts/check-commit-refs BUG-0003 wi/BUG-0003` → exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | two files: six lines of `linecount.py` (the write, its flush, their comment, one docstring sentence) and one appended test class. No other function, no other bug's behaviour |

## What I did not do

- **I did not touch stderr's encoding.** Plan assumption 2: a file that is both undecodable *and*
  unreadable could still raise while composing `linecount: <name>: <problem>`. Untested, outside
  this item's criteria, and a separate defect if it is ever observed.
- **I did not escape the byte for display.** ADR-0008 costed that (option C) and rejected it: the
  name on screen would no longer be the name on disk.
- **I did not add a test for a non-UTF-8 name under a non-UTF-8 locale** (`LC_ALL=C`). ADR-0008
  claims locale-independence as the reason for choosing bytes over `reconfigure`, and that claim is
  currently argued rather than tested. It is the one gap in this item a reader might expect to find
  covered.
- **I did not touch BUG-0001's or BUG-0002's behaviour**, both merged: `no files`,
  `no files could be read`, ADR-0006's silent skips and ADR-0002's stderr lines all go through the
  same new write and are unchanged, which the 55 existing tests confirm.
- **I did not address `BrokenPipeError`**, out of scope since WI-0001 and unchanged here: the write
  is still a single call.
