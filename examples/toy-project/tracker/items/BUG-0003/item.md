---
id: BUG-0003
type: bug
title: A filename that is not valid UTF-8 makes the tool print a traceback and exit 1
status: done
priority: medium
epic: EP-001
created: "2026-08-16T22:30:00Z"
updated: "2026-08-17T01:30:05Z"
found-in: WI-0001
branch: wi/BUG-0003
outcome: delivered
---

## Summary

`linecount.py` never decodes a file's *contents* — that is the design, and it is what makes a PNG
count like anything else. But a file's *name* is decoded, by `os.scandir`, before the tool ever
sees it. On Linux a name that is not valid UTF-8 comes back with surrogate escapes
(`surrogateescape`), and the final `print(text, end="")` cannot encode those to stdout. The result
is a `UnicodeEncodeError` traceback on stderr, an empty stdout, and exit **1** — a status the tool
does not otherwise use and which no criterion or document defines.

This is the failure mode the human named at intake as one of the two ways the tool fails on its
own terms, and it is the one case where `wc -l *`, the tool this replaces, does better.

## Steps to reproduce

Run from the repository root, on Linux with an ext4 or similar filesystem, with `linecount.py`
from `main` at `6d1e437b4293571296809b322c47fb0dc83d1ad6`.

1. `mkdir -p /tmp/bug3`
2. Create the two files, one with a name that is not valid UTF-8:

   ```
   python3 -c "
   import os
   d = b'/tmp/bug3'
   open(os.path.join(d, b'good.txt'), 'wb').write(b'a\nb\n')
   open(os.path.join(d, b'bad\xff.txt'), 'wb').write(b'a\nb\nc\n')
   "
   ```
3. Confirm the folder holds two ordinary files: `ls -b /tmp/bug3`
4. `python3 linecount.py /tmp/bug3; echo "exit=$?"`
5. For contrast, run the tool this one replaces: `cd /tmp/bug3 && wc -l *; echo "exit=$?"`

## Expected behaviour

WI-0001 **AC1**:

> `python3 linecount.py <folder>`, with the folder path as the only argument, prints to stdout one
> row per file directly inside that folder

Both entries are regular files. Two rows and a total row are expected:

```
3  bad<0xff>.txt
2  good.txt
5  total
```

— where `<0xff>` stands for however `plan` decides the undecodable byte should reach stdout
(`wc -l *` writes it through unchanged). The exit status must be 0.

Also contradicted:

- `docs/architecture/overview.md` v2, `## Boundaries that are deliberate` — "**Bytes, not text.**
  Files are opened in binary and never decoded, so no file can raise a decoding error and every
  file gets a count by the same rule." A file here does raise a decoding error, on the way out
  rather than on the way in.
- `docs/architecture/overview.md` v2 — "Exit 0 means 'here is the answer'; exit 2 means 'I could
  not produce one'." The tool exits 1, which is neither.
- `docs/product/vision.md` v1 — "**A number, not a stack trace.** Folders contain unusual things.
  Encountering one is not an error condition; being unable to read the folder at all is."
- WI-0001 `## Notes` records the human's two stated failure conditions, the second being
  "producing a stack trace rather than a number when the folder contains something unusual".
- EP-001 `## Why now` argues this tool is needed because `wc -l *` fails on awkward folders. On
  this folder `wc -l *` succeeds and `linecount.py` does not.

## Actual behaviour

Verbatim, run from the repository root on `main` at
`6d1e437b4293571296809b322c47fb0dc83d1ad6`:

```
$ ls -b /tmp/bug3
bad\377.txt
good.txt

$ python3 linecount.py /tmp/bug3; echo "exit=$?"
Traceback (most recent call last):
  File "/home/msi/.claude/jobs/864502ae/tmp/toy/linecount/linecount.py", line 164, in <module>
    sys.exit(main(sys.argv[1:]))
             ^^^^^^^^^^^^^^^^^^
  File "/home/msi/.claude/jobs/864502ae/tmp/toy/linecount/linecount.py", line 159, in main
    print(text, end="")
UnicodeEncodeError: 'utf-8' codec can't encode character '\udcff' in position 6: surrogates not allowed
exit=1
```

All of that is on stderr. stdout is empty — not even the row for `good.txt`, because the whole
report is written by one `print`:

```
$ python3 linecount.py /tmp/bug3 2>/dev/null; echo "exit=$?"
exit=1
```

`--top` does not avoid it, since the undecodable name is in the rows shown:

```
$ python3 linecount.py --top 1 /tmp/bug3 2>&1 | tail -2
    print(text, end="")
UnicodeEncodeError: 'utf-8' codec can't encode character '\udcff' in position 6: surrogates not allowed
```

The tool being replaced handles the same folder:

```
$ cd /tmp/bug3 && wc -l *; echo "exit=$?"
 3 bad<0xff>.txt
 2 good.txt
 5 total
exit=0
```

(`<0xff>` stands for the raw byte `wc` writes through unchanged; a terminal renders it as a
replacement character.)

## Acceptance criteria

- [x] AC1 — the reproduction folder above produces two file rows and a total row on stdout, and
      exits 0. Neither the string `Traceback` nor `UnicodeEncodeError` appears on stdout or
      stderr, which is WI-0001 AC9's observable applied to this folder
- [x] AC2 — the row for the undecodable name is sorted and formatted by the same rules as every
      other row: count 3, first in the order WI-0001 AC2 fixes, right-aligned in the shared
      column with two spaces before the name. How the byte is spelled on screen is for `plan` to
      choose and record; the criterion pins that a row exists, in its sorted position, with the
      right count
- [x] AC3 — running the command twice on that unchanged folder produces byte-identical stdout
      (`cmd > a; cmd > b; diff a b` is empty and exits 0), so WI-0001 AC2 holds for this folder
      too
- [x] AC4 — `--top 1` on that folder prints one file row and the total row of WI-0002 AC3, and
      exits 0
- [x] AC5 — every existing output is unchanged on folders whose names are all valid UTF-8: the
      WI-0001 and WI-0002 tests pass unmodified, and stdout for WI-0001 AC1's worked example
      (`128··notes.md`, `··7··a.py`, `135··total`, where `·` stands for one space) is
      byte-identical
- [x] AC6 — regression tests in `tests/` cover AC1, AC2 and AC4, and each fails against the code
      as it stands at `6d1e437b4293571296809b322c47fb0dc83d1ad6`. `python3 -m unittest discover`
      from the repository root exits 0

## Notes

Found by an independent regression pass over `main` at
`6d1e437b4293571296809b322c47fb0dc83d1ad6`, run after EP-001 was closed. It is WI-0001's
behaviour: the same folder run against the `linecount.py` WI-0001 shipped (commit `5adc619`)
gives the same traceback from the equivalent line,
`print(format_report(rows), end="")`. WI-0002 neither caused nor worsened it.

WI-0001's `## Notes` already records this as a gap accepted at review — "**A filename that is not
valid UTF-8 is untested.** `os.fsencode` in the sort key exists for exactly that case ... a
genuinely undecodable name was never created." This item is that case, created and run. The
`os.fsencode` in the sort key does its job; only the printing fails.

`plan` will have to decide how the name reaches stdout. The obvious candidates are writing the
report through `sys.stdout.buffer` with `os.fsencode`, which preserves the bytes exactly as
`ls -b` and `wc` do, or reconfiguring stdout's error handler to `surrogateescape`/`backslash
replace`. The choice is visible to the user, so it belongs in an ADR rather than in the diff.

The test for this needs a filename that cannot be created on every platform, and the folder must
be built with `bytes` paths. WI-0001's `## Notes` already records that only POSIX has ever been
exercised; a skip guard for non-POSIX is expected rather than a reason not to write the test.

Environment: Linux 7.0.0-28-generic (Ubuntu 24.04), ext4, Python 3.12.3,
`LANG`/`LC_ALL` giving a UTF-8 stdout encoding, non-root user (uid 1000).

Gaps accepted at review, recorded here so they outlive the reports nobody re-reads after an item
is closed (`review-close`, 2026-08-17; evidence in `artifacts/review.md` and
`artifacts/verify-report.md`):

- **stderr's encoding is untouched.** A file that is both undecodable *and* unreadable would
  compose `linecount: <name>: <problem>` through `print` and could still raise. Outside this
  item's criteria; a separate defect if it is ever observed, with its own reproduction.
- **Only POSIX was exercised.** The regression class is `skipUnless(os.name == "posix")`, because
  such a name cannot be created on every filesystem.
- **stdout is now written exactly once, as bytes, at the end of `main`.** Anything added later
  that `print`s to stdout would interleave with it. Nothing does today, so the constraint is a
  rule for future changes rather than something a test can hold (ADR-0008, overview v4).
- **Nothing lints this project** (ADR-0003).
- **Only small reports were exercised** — the write is a single buffered call.
