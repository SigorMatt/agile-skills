# Plan — BUG-0003 A filename that is not valid UTF-8 makes the tool print a traceback and exit 1

## Problem

A folder holding a file whose name is not valid UTF-8 produces no report at all: the whole listing
is written by one `print`, that `print` raises `UnicodeEncodeError` on the surrogate escapes
`os.scandir` hands back, and the process exits **1** — a status the tool defines nowhere. The
ordinary file beside it is never printed either. `wc -l *`, the tool this replaces, prints the same
folder and exits 0.

Reproduced on `main` at `2946f57` before planning, with the item's own steps:

```
$ ls -b /tmp/bug3                    bad\377.txt   good.txt
$ python3 linecount.py /tmp/bug3      UnicodeEncodeError … exit=1   (stdout empty)
$ cd /tmp/bug3 && wc -l *             3 bad?.txt / 2 good.txt / 5 total, exit 0
```

The sort is not the problem: WI-0001 chose `os.fsencode` as the sort key exactly so its "byte
order" would be true for such names. Only the printing fails, and it fails at the one line where
the finished report crosses from `str` into the terminal.

## Approach

Write the report as **bytes** — `sys.stdout.buffer.write(os.fsencode(text))` — instead of as text
through `print` (ADR-0008). The report is still assembled as `str`, with the same rows, order,
column arithmetic and sentences; only the boundary changes, and it converts once, with the encoder
that round-trips what `os.scandir` produced.

This is a smaller change than it looks and a larger decision than it looks: it makes stdout
locale-independent, which is what distinguishes it from reconfiguring the stream's error handler
(ADR-0008 option B, which still breaks on `café.txt` when stdout's encoding is genuinely not
UTF-8 — `PYTHONIOENCODING=ascii`. The `LC_ALL=C` example this plan first gave does not
reproduce; corrected in ADR-0008 v2 for Q-001.)

Nothing else changes: not `count_lines`, `list_files`, `format_report`, `parse_top`, `parse_args`,
the sort key, the row format, the total, `--top`, the stderr messages, or any exit status.

## Steps

1. **Replace the final write in `main`** in `linecount.py`:

   ```python
   # The report is data, not text: a file's name is echoed as the bytes the filesystem gave us,
   # so a name that is not valid UTF-8 prints as `ls -b` and `wc` print it, and the output does
   # not depend on the locale (BUG-0003, ADR-0008).
   sys.stdout.buffer.write(os.fsencode(text))
   sys.stdout.buffer.flush()
   ```

   replacing `print(text, end="")`. Nothing above this line moves. Observable result: on the
   reproduction folder, stdout is `3  bad\xff.txt` / `2  good.txt` / `5  total` with the raw byte
   `0xFF` in the name, and the exit status is 0.

2. **Extend the module docstring's "bytes" sentence** to say that names are echoed as bytes too,
   citing ADR-0008 — one sentence, so a reader of the file learns why stdout is written the way it
   is. Observable result: no behaviour change.

3. **Add regression tests to `tests/test_linecount.py`** in a new class `UndecodableNameTest`,
   appended; no existing test modified. The folder is built with **bytes** paths
   (`os.path.join(os.fsencode(folder), b"bad\xff.txt")`), and the class carries a POSIX guard —
   `@unittest.skipUnless(os.name == "posix", ...)` — because such a name cannot be created
   everywhere. The four tests are named in the mapping table below. Observable result:
   `python3 -m unittest discover` from the repository root exits 0.

4. **Demonstrate the AC1, AC2 and AC4 tests fail against `6d1e437`**, which AC6 requires:
   `git show 6d1e437:linecount.py > linecount.py`, run the suite, record, restore.

5. **Run the gates and write `artifacts/impl-report.md`**, mapping AC1–AC6 to evidence and stating
   what did not change — in particular that ASCII-named folders produce byte-identical output.

`docs/architecture/overview.md` goes to **v4** in this planning execution, not in `implement`: its
`## Boundaries that are deliberate` section states "bytes, not text" about file *contents*, and
after this change the same boundary covers names on the way out. `implement` may not write to
`docs/`.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — the reproduction folder prints two file rows and a total, exits 0, and neither `Traceback` nor `UnicodeEncodeError` appears on either stream | 1 | `UndecodableNameTest.test_ac1_undecodable_name_does_not_abort_the_report`: builds `good.txt` (2 lines) and `bad\xff.txt` (3) with bytes paths; asserts stdout is exactly `b"3  bad\xff.txt\n2  good.txt\n5  total\n"`, stderr `b""`, exit 0, and that neither marker appears in either stream |
| AC2 — the row for that name is sorted and formatted by the same rules: count 3, first in WI-0001 AC2's order, right-aligned with two spaces | 1 | the same test's exact-bytes assertion pins all three: the count, the position (3 before 2), and the two spaces. `plan` chooses the spelling: the raw bytes, as ADR-0008 decides |
| AC3 — running twice on the unchanged folder gives byte-identical stdout | 1 | `UndecodableNameTest.test_ac3_two_runs_are_byte_identical`: runs the command twice and asserts stdout, stderr and exit code are equal — the criterion's own `diff` expressed as an assertion |
| AC4 — `--top 1` prints one file row and WI-0002 AC3's total row, exit 0 | 1 | `UndecodableNameTest.test_ac4_top_one_on_that_folder`: asserts stdout is exactly `b"3  bad\xff.txt\n5  total (all 2 files)\n"`, exit 0 |
| AC5 — ASCII-named folders are unchanged; WI-0001 and WI-0002 tests pass unmodified; WI-0001 AC1's example is byte-identical | 1 | `UndecodableNameTest.test_ac5_ascii_folders_are_byte_identical`: WI-0001 AC1's own folder (`notes.md` 128, `a.py` 7) → stdout exactly `b"128  notes.md\n  7  a.py\n135  total\n"`. Plus the whole existing suite — 55 tests — passing unmodified in the same run |
| AC6 — the regression tests fail against `6d1e437`; `unittest discover` exits 0 | 3, 4 | the run recorded in step 4 and quoted in `impl-report.md`. All three tests named by AC6 assert new behaviour, so each of them does fail there |

## Assumptions

1. **The undecodable byte reaches stdout raw**, as `ls -b` and `wc` write it, rather than escaped.
   ADR-0008 decides this and costs the alternatives; AC2 explicitly leaves the spelling to `plan`.
   Reversing it is an `.encode(errors="backslashreplace")` at the same one boundary.
2. **Error messages on stderr keep using `print`.** They are the tool's own sentences; the one
   place a name appears in them is `linecount: <name>: <problem>`, which is best-effort. A folder
   whose *unreadable* file also has an undecodable name could therefore still raise on stderr —
   untested, out of this item's criteria, and named here rather than discovered later.
3. **`tests/` gains a POSIX guard for this class.** A name that is not valid UTF-8 cannot be
   created on every filesystem; WI-0001's notes already record that only POSIX has been exercised.
   Reversing it is deleting a decorator.

## Decisions and ADRs

| decision | where recorded | branch of the preference order |
|----------|----------------|-------------------------------|
| the report is written to `sys.stdout.buffer` as `os.fsencode`d bytes | ADR-0008 | decided here, four options costed |
| the boundary "bytes, not text" now covers names as well as contents | ADR-0008, `docs/architecture/overview.md` v4 | decided here |
| the row's count, position and spacing follow WI-0001 AC1 and AC2 unchanged | BUG-0003 AC2, WI-0001 AC1/AC2 | documented |
| the sort key already handles these names | WI-0001 AC2's `os.fsencode` | documented — nothing to change |
| the raw-byte spelling, stderr's best-effort encoding, and the POSIX guard | `## Assumptions` | assumed, each with its reversal cost |

## Risks

- **Interleaving.** stdout is now written once as bytes at the end of `main`; anything added later
  that `print`s to stdout would interleave with the buffered write. The mitigation is that there is
  exactly one stdout write and it flushes; the constraint is recorded in ADR-0008's consequences so
  the next person meets it deliberately.
- **A silent change for everyone else.** Every existing user's output goes through a different code
  path, even though the bytes are identical for ASCII names. AC5's test and the 55 existing tests
  are the guard, and `impl-report.md` must state that they passed unmodified.
- **stderr is not covered.** Assumption 2: a name that is undecodable *and* unreadable would still
  raise while composing an ADR-0002 message. No criterion covers it; recorded rather than fixed,
  because fixing it would widen this item into a second change with no criterion of its own.

## Out of scope for this item

- **stderr's encoding**, per assumption 2 — a separate defect if it is ever observed, with its own
  reproduction.
- `BrokenPipeError`, out of scope since WI-0001 and unchanged by this fix.
- Any change to counting, listing, sorting, the row format, the total, `--top`, the sentences, the
  stderr wording, or any exit status.
- Normalising, escaping or transliterating names for display.
- BUG-0001's and BUG-0002's behaviour, both merged and both untouched here.
