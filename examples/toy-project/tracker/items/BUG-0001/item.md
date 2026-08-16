---
id: BUG-0001
type: bug
title: A symlink that cannot be stat'ed aborts the listing and blames the folder
status: done
priority: high
epic: EP-001
created: "2026-08-16T22:30:00Z"
updated: "2026-08-17T01:30:05Z"
found-in: WI-0001
branch: wi/BUG-0001
outcome: delivered
---

## Summary

`list_files` decides what to list with `entry.is_file(follow_symlinks=True)`. That call swallows
`FileNotFoundError` — which is why a plain broken symlink is ignored correctly, as WI-0001 AC7
requires — but it lets every **other** `OSError` out. `main` wraps `list_files` in a single
`except OSError` that reports the failure as a failure of the *folder* and returns 2. So one
awkward symlink among otherwise ordinary files destroys the entire report: nothing is printed on
stdout, the readable files are never counted, and the message on stderr names the folder and a
problem the folder does not have.

Two triggers were reproduced on `main` at commit `6d1e437b4293571296809b322c47fb0dc83d1ad6`: a
symlink loop (`ELOOP`) and a symlink into a directory the user cannot traverse (`EACCES`). Both
are entries a real folder can hold, and neither is the folder being unreadable.

## Steps to reproduce

Run each block from any shell, as a non-root user, with `linecount.py` from `main` at
`6d1e437b4293571296809b322c47fb0dc83d1ad6`.

**Trigger A — a symlink loop.**

1. `mkdir -p /tmp/bug1a`
2. `printf 'a\nb\nc\n' > /tmp/bug1a/ok.txt`
3. `ln -s p /tmp/bug1a/q`
4. `ln -s q /tmp/bug1a/p`
5. `python3 linecount.py /tmp/bug1a; echo "exit=$?"`

**Trigger B — a symlink into a directory the user cannot traverse.**

1. `mkdir -p /tmp/bug1b/vault /tmp/bug1b/folder`
2. `printf 'secret\n' > /tmp/bug1b/vault/hidden.txt`
3. `chmod 000 /tmp/bug1b/vault`
4. `printf 'a\nb\n' > /tmp/bug1b/folder/ok.txt`
5. `ln -s /tmp/bug1b/vault/hidden.txt /tmp/bug1b/folder/into-vault`
6. `python3 linecount.py /tmp/bug1b/folder; echo "exit=$?"`
7. Clean up with `chmod 755 /tmp/bug1b/vault`

**Control — the same shape with a plain broken symlink, which behaves correctly.**

1. `mkdir -p /tmp/bug1c`
2. `printf 'a\n' > /tmp/bug1c/ok.txt`
3. `ln -s nowhere /tmp/bug1c/gone`
4. `python3 linecount.py /tmp/bug1c; echo "exit=$?"`

## Expected behaviour

WI-0001 **AC7**, quoted in full for the relevant half:

> a symlink that resolves to a directory and a symlink that resolves to nothing are both ignored
> exactly as a subdirectory is — not listed, no message on stdout or stderr, exit 0

A symlink loop resolves to nothing: following it yields no file. A symlink into a directory the
user cannot traverse likewise yields no file this tool can count. Under AC7 each should be
ignored silently, and under WI-0001 **AC1** the folder's real file (`ok.txt`) should still get
its row and the total row.

So trigger A should print

```
3  ok.txt
3  total
```

on stdout, print nothing on stderr, and exit 0 — exactly what the control case already does.
Trigger B should print `2  ok.txt` and `2  total` and exit 0; if anything is said about
`into-vault` at all, ADR-0002's shape (one line on stderr naming the entry, the listing intact,
exit 0) is the precedent, not a fatal error.

Also contradicted:

- `docs/product/vision.md` v1 — "Folders contain unusual things. Encountering one is not an
  error condition; being unable to read the folder at all is." The folder here is perfectly
  readable.
- `docs/architecture/overview.md` v2 — "Exit 0 means 'here is the answer'; exit 2 means 'I could
  not produce one'." The tool can produce an answer for `ok.txt` and does not.
- ADR-0002 — "The rule holds for exactly one thing: an `OSError` raised while opening or reading
  an entry that the listing step already established is a file. It does not apply to the folder
  itself, which is AC11's territory and exits 2." These `OSError`s are raised *by the listing
  step* about an entry, and they are nonetheless routed to the folder's exit-2 path.
- EP-001 `## Success measures` — "On a folder that contains at least one subdirectory, the
  command exits 0 and prints counts for the files, where `wc -l *` on the same folder reports an
  error for the subdirectory." Trigger A's folder also contains a subdirectory-like awkwardness
  and the command does not exit 0.

## Actual behaviour

Verbatim, run from the repository root on `main` at
`6d1e437b4293571296809b322c47fb0dc83d1ad6`. The single line shown for each failing case is on
**stderr**; stdout is empty in all three.

Trigger A:

```
$ python3 linecount.py /tmp/bug1a; echo "exit=$?"
linecount: /tmp/bug1a: Too many levels of symbolic links
exit=2
```

`ok.txt` is never counted, and the message names the folder rather than the symlink.

A single self-referential symlink (`ln -s self /tmp/bug1d/self`) behaves identically:

```
$ python3 linecount.py /tmp/bug1d; echo "exit=$?"
linecount: /tmp/bug1d: Too many levels of symbolic links
exit=2
```

Trigger B:

```
$ python3 linecount.py /tmp/bug1b/folder; echo "exit=$?"
linecount: /tmp/bug1b/folder: Permission denied
exit=2
```

`/tmp/bug1b/folder` is mode 755 and readable. The permission problem belongs to
`/tmp/bug1b/vault`, which the message never mentions.

Control case, for contrast — the same folder shape with a plain broken symlink is handled
correctly, which is why AC7 verified clean:

```
$ python3 linecount.py /tmp/bug1c; echo "exit=$?"
1  ok.txt
1  total
exit=0
```

## Acceptance criteria

- [x] AC1 — trigger A above prints exactly `3  ok.txt` and `3  total` on stdout (two spaces
      before each name and label, per WI-0001 AC1), prints nothing on stderr, and exits 0
- [x] AC2 — a folder holding one readable file and one self-referential symlink (`ln -s self
      self`) produces the same shape: the readable file's row, the total row, and exit 0
- [x] AC3 — trigger B above prints `2  ok.txt` and `2  total` on stdout and exits 0. Any message
      about `into-vault` goes to stderr, on one line, naming that entry and not the folder —
      ADR-0002's shape. Whether such a message is printed at all is for `plan` to decide and
      record; the criterion pins the stream, the exit code, and that the folder is not blamed
- [x] AC4 — WI-0001 AC7's existing cases are unchanged: a symlink to a regular file is still
      listed under its own name with its target's count, and a symlink to a directory and a
      plain broken symlink are still ignored with nothing on stdout or stderr and exit 0
- [x] AC5 — WI-0001 AC11 is unchanged: a folder that genuinely cannot be listed (a directory of
      mode `000`, tested as a non-root user) still prints nothing on stdout, one line on stderr
      naming that path and the problem, and exits 2
- [x] AC6 — regression tests in `tests/` cover AC1, AC2, AC3 and AC5; the tests for AC1, AC2 and
      AC3 each fail against the code as it stands at
      `6d1e437b4293571296809b322c47fb0dc83d1ad6`. `python3 -m unittest discover` from the
      repository root exits 0. (Scoped by `answer-questions` for Q-002: as first written it
      required *each* of the four to fail there, which the AC5 test cannot do — AC5 is behaviour
      this fix leaves unchanged, so a test asserting it passes against the old code by
      construction. This is the wording BUG-0002 AC7 already uses.)

## Notes

Found by an independent regression pass over `main` at
`6d1e437b4293571296809b322c47fb0dc83d1ad6`, run after EP-001 was closed. It is a defect in
behaviour WI-0001 delivered, not a failure of WI-0002: the same folders were run against the
`linecount.py` WI-0001 shipped (commit `5adc619`) and behave the same way, and `--top` changes
nothing about it.

Why WI-0001's own verification did not catch it: AC7 names three symlink cases — to a file, to a
directory, to nothing — and `tests/test_linecount.py` has one test for each. A symlink loop and a
symlink whose target cannot be stat'ed are both instances of "resolves to nothing" that the three
named cases do not reach, and `DirEntry.is_file()` treats them differently from the tested cases:
it catches `FileNotFoundError` and nothing else.

The root cause is one line of `list_files` plus one `except` in `main`. `plan` should note that
the fix has to keep the two `OSError` sources distinguishable — the one `os.scandir(folder)`
raises about the folder (AC11, exit 2) and the one `entry.is_file()` raises about an entry (this
bug, exit 0) — which today are caught by the same handler.

Environment: Linux 7.0.0-28-generic (Ubuntu 24.04), Python 3.12.3, non-root user (uid 1000).

Gaps accepted at review, recorded here so they outlive the reports nobody re-reads after an item
is closed (`review-close`, 2026-08-17; evidence in `artifacts/review.md` and
`artifacts/verify-report.md`):

- **An entry that cannot be resolved is now invisible.** ADR-0006 chose silence and AC1 requires it
  for the loop case, so a folder can hold a symlink the tool never mentions on either stream. The
  alternative (one line on stderr, ADR-0002's shape) is costed in that ADR and would need a
  criterion change, not a code change.
- **Nothing lints this project** (ADR-0003): the eleven changed lines were read at review and by
  no tool.
- **Entries that are neither file, directory nor symlink** — a socket, a device node — are
  untested. `DirEntry.is_file()` returns `False` for them without raising, so they take neither the
  old path nor the new one.
- **Only POSIX was exercised**, unchanged from WI-0001.
- **BUG-0002's symptom is untouched by this fix**: a folder whose entries are *all* unresolvable
  still prints `no files`. That is BUG-0002's to fix, and whoever does should check this case
  against their fix.

Amended after `ready`, by the only route that allows it:

- **AC6's failing clause was scoped by `answer-questions` on 2026-08-17**, answering `Q-002` from
  `implement`. The demand that a regression test fail without the fix is unchanged and still
  applies to every test that asserts *new* behaviour; what was removed is a requirement the AC5
  test could not meet without contradicting AC5 itself. Measured before the amendment: with
  `linecount.py` restored to `6d1e437`, the AC1, AC2 and AC3 tests failed and the AC5 test passed.
  Full reasoning, the two alternatives, and the files changed are in `questions/Q-002.md`.
