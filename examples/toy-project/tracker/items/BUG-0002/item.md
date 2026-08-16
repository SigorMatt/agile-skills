---
id: BUG-0002
type: bug
title: "A folder whose files are all unreadable prints \"no files\" on stdout"
status: done
priority: medium
epic: EP-001
created: "2026-08-16T22:30:00Z"
updated: "2026-08-17T01:30:05Z"
found-in: WI-0001
branch: wi/BUG-0002
outcome: delivered
---

## Summary

ADR-0002 decided that a file which cannot be read is omitted from the listing and reported on one
line of stderr, with the exit status staying 0. WI-0001 AC10 decided that a folder with no files
in it prints exactly `no files`. Each rule is obeyed. Their combination produces a false answer:
when *every* file in a folder is skipped, `rows` is empty, `main` takes its `not rows` branch, and
stdout — the stream the tool exists to produce, and the only one that survives a pipe or a
redirect — says `no files` about a folder that is full of files.

ADR-0005 names this output as the one way its design can be misused: "If a third caller ever
forgets, it prints `no files` for a folder that had some". `main` is that caller, and it does not
distinguish "the folder had none" from "I could not read any of them".

The condition is not exotic. It is reached by a folder of files owned by someone else, and by a
folder whose own mode is `r--` (readable, not traversable) — the shape a directory has when it
comes off read-only media or out of a badly-extracted archive.

## Steps to reproduce

Run from any shell, as a non-root user, with `linecount.py` from `main` at
`6d1e437b4293571296809b322c47fb0dc83d1ad6`.

**Trigger A — every file in the folder is unreadable.**

1. `mkdir -p /tmp/bug2a`
2. `printf 'a\n' > /tmp/bug2a/one.txt`
3. `printf 'b\nc\n' > /tmp/bug2a/two.txt`
4. `chmod 000 /tmp/bug2a/one.txt /tmp/bug2a/two.txt`
5. `python3 linecount.py /tmp/bug2a; echo "exit=$?"`
6. Now discard stderr, as a pipe or a redirect would:
   `python3 linecount.py /tmp/bug2a 2>/dev/null; echo "exit=$?"`
7. Clean up with `chmod 644 /tmp/bug2a/one.txt /tmp/bug2a/two.txt`

**Trigger B — the folder is readable but not traversable.**

1. `mkdir -p /tmp/bug2b`
2. `printf 'a\nb\n' > /tmp/bug2b/f.txt`
3. `printf 'c\n' > /tmp/bug2b/g.txt`
4. `chmod 444 /tmp/bug2b`
5. `python3 linecount.py /tmp/bug2b; echo "exit=$?"`
6. Clean up with `chmod 755 /tmp/bug2b`

**Control — a genuinely empty folder, which must keep printing `no files`.**

1. `mkdir -p /tmp/bug2c`
2. `python3 linecount.py /tmp/bug2c; echo "exit=$?"`

## Expected behaviour

WI-0001 **AC10** defines what `no files` means:

> a folder that contains no files at all — empty, or holding only subdirectories — prints exactly
> `no files` on stdout, prints nothing on stderr, prints no total row, and exits 0

Both trigger folders contain files. `no files` is the answer to a different question, and stdout
should not give it here. Whatever it says instead, a reader of stdout alone must be able to tell
trigger A apart from the control folder, which is a folder that really has nothing in it.

Also contradicted:

- `docs/architecture/overview.md` v2 — "Exit 0 means 'here is the answer'". The tool exits 0 and
  the answer it gives is wrong.
- ADR-0005 `## Consequences` — the `None` sentinel "means 'the folder had no files' is a judgement
  `main` makes, not one the renderer can make on its own. If a third caller ever forgets, it
  prints `no files` for a folder that had some — the one way this design can be misused."
- EP-001 `## Goal` — "The command works on any folder the person can read ... and when it cannot
  do its job it says so plainly". On stdout it does not say so at all.

The exact replacement wording is deliberately left open, exactly as WI-0001 AC11 and AC12 leave
the wording of their stderr messages open; `plan` may choose it. What is pinned is that stdout
must not claim there are no files, that the per-file stderr lines and the exit status of ADR-0002
are unchanged, and that a genuinely empty folder still prints exactly `no files`.

## Actual behaviour

Verbatim, run from the repository root on `main` at
`6d1e437b4293571296809b322c47fb0dc83d1ad6`. In the first block the two `linecount:` lines are on
stderr and `no files` is on stdout.

Trigger A:

```
$ python3 linecount.py /tmp/bug2a; echo "exit=$?"
linecount: one.txt: Permission denied
linecount: two.txt: Permission denied
no files
exit=0
```

Step 6 — stdout alone, which is what a pipe or a redirect keeps:

```
$ python3 linecount.py /tmp/bug2a 2>/dev/null; echo "exit=$?"
no files
exit=0
```

That output is byte-for-byte identical to the control folder, which contains nothing:

```
$ python3 linecount.py /tmp/bug2c; echo "exit=$?"
no files
exit=0
```

Trigger B:

```
$ python3 linecount.py /tmp/bug2b; echo "exit=$?"
linecount: g.txt: Permission denied
linecount: f.txt: Permission denied
no files
exit=0
```

`--top` makes no difference, because `main` short-circuits on `not rows`:

```
$ python3 linecount.py --top 3 /tmp/bug2a; echo "exit=$?"
linecount: one.txt: Permission denied
linecount: two.txt: Permission denied
no files
exit=0
```

## Acceptance criteria

- [x] AC1 — for trigger A, stdout does not contain the line `no files`, and the exit status stays
      0. The two `linecount: <name>: Permission denied` lines on stderr are unchanged, one per
      skipped file, as ADR-0002 requires
- [x] AC2 — the stdout of trigger A differs from the stdout of the control folder
      (`/tmp/bug2c`, which contains nothing), so a reader who sees only stdout can tell the two
      apart
- [x] AC3 — trigger B behaves as trigger A does: exit 0, the per-file stderr lines unchanged, and
      stdout not claiming the folder has no files
- [x] AC4 — WI-0001 AC10 is unchanged: an empty folder, and a folder holding only
      subdirectories, each still print exactly `no files` on stdout, print nothing on stderr,
      print no total row, and exit 0
- [x] AC5 — WI-0002 AC9 is unchanged: on a folder that contains no files at all, `--top 0`,
      `--top 3` and `--top 99` each still print exactly `no files`, nothing on stderr, and exit 0
- [x] AC6 — a folder with one readable and one unreadable file is unchanged from today: the
      readable file's row, the total row, one stderr line for the skipped file, exit 0
- [x] AC7 — regression tests in `tests/` cover AC1, AC2, AC3 and AC4, and the tests for AC1–AC3
      fail against the code as it stands at `6d1e437b4293571296809b322c47fb0dc83d1ad6`.
      `python3 -m unittest discover` from the repository root exits 0

## Notes

Found by an independent regression pass over `main` at
`6d1e437b4293571296809b322c47fb0dc83d1ad6`, run after EP-001 was closed. The behaviour is
WI-0001's: the same folders were run against the `linecount.py` WI-0001 shipped (commit
`5adc619`) and produce byte-identical stdout, stderr and exit code. WI-0002's `if top is None or
not rows` inherits it rather than causing it.

Why WI-0001's verification did not catch it: `tests/test_linecount.py` has
`test_unreadable_file_is_reported_and_skipped`, which puts **one** unreadable file in a folder
that also has a readable one — the case where the listing survives. Nothing exercises the folder
where the skip list is everything.

The order of the stderr lines follows directory order and is not sorted, so it may differ from
the quotes above between machines. Nothing constrains it: WI-0001 AC2's byte-identity requirement
is about stdout.

A related observation, recorded here rather than filed separately because it has the same root
and is settled by its own criterion's wording. With `--top` and one skipped file, the label reads
`total (all 1 files)` for a folder of two files. Build it with
`mkdir -p /tmp/bug2d; printf 'a\nb\nc\n' > /tmp/bug2d/ok.txt; printf 'x\n' > /tmp/bug2d/no.txt;
chmod 000 /tmp/bug2d/no.txt`:

```
$ python3 linecount.py --top 5 /tmp/bug2d; echo "exit=$?"
linecount: no.txt: Permission denied
3  ok.txt
3  total (all 1 files)
exit=0
```

WI-0002 AC3 defines M two ways in one sentence — "the number of files in the folder — that is,
the number of rows the same command would print without `--top`" — and a skipped file makes the
two halves disagree. The implementation follows the second half, which is the operative gloss, so
this is not filed as a defect. Whoever fixes this bug should check whether their fix changes what
M counts, and say so.

Environment: Linux 7.0.0-28-generic (Ubuntu 24.04), Python 3.12.3, non-root user (uid 1000).

Gaps accepted at review, recorded here so they outlive the reports nobody re-reads after an item
is closed (`review-close`, 2026-08-17; evidence in `artifacts/review.md` and
`artifacts/verify-report.md`):

- **No test asserts that a folder of *only* unresolvable entries still prints `no files`.**
  `verify` ran it by hand and it is correct — an entry that cannot be resolved is not a file, so
  the skipped-file counter never sees it (ADR-0006) — but nothing in the suite would notice if a
  future change made the counter include them.
- **No test for a folder mixing unreadable files with unresolvable entries.** Run by hand: it
  prints `no files could be read` with one stderr line, which is what the plan's assumption 2 says.
- **The wording `no files could be read` is ADR-0007's choice**, not a criterion's. AC1 and AC2
  pin only that stdout must not claim the folder is empty.
- **Nothing lints this project** (ADR-0003).
- **Only POSIX was exercised**, and only folders of two or three files — the shape does not change
  with scale, but scale was not run.
