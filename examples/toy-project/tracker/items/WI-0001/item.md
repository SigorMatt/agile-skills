---
id: WI-0001
type: work-item
title: Count lines per file in a folder and print them largest first
status: done
priority: high
epic: EP-001
created: "2026-08-16T21:13:44Z"
updated: "2026-08-16T21:56:29Z"
branch: wi/WI-0001
outcome: delivered
---

## Story

As someone who has just opened a folder of mixed notes and code, I want one command that lists
each file in that folder with its line count, biggest first, so that I can see which two or
three files hold most of the material without opening any of them.

## Acceptance criteria

- [x] AC1 — `python3 linecount.py <folder>`, with the folder path as the only argument, prints
      to stdout one row per file directly inside that folder. Each row is the file's line count,
      right-aligned in a column as wide as the widest number printed (the total row included),
      then two spaces, then the file's bare name with no directory part. For a folder holding
      `notes.md` (128 lines) and `a.py` (7 lines), stdout is exactly the three lines
      `128··notes.md`, `··7··a.py`, `135··total`, where `·` stands for one space character (the
      column is 3 wide because `135`, the widest number printed, has three digits)
- [x] AC2 — rows are ordered by line count, largest first; two files with the same count are
      ordered by filename ascending in byte order, so `A.md` precedes `a.md`. Running the command
      twice on an unchanged folder produces byte-identical stdout (`cmd > a; cmd > b; diff a b`
      is empty and exits 0)
- [x] AC3 — when at least one file is listed, the last line of stdout is the total row: the sum
      of every count listed, right-aligned in the same column, then two spaces, then the word
      `total`
- [x] AC4 — a file of zero bytes is listed with a count of 0, in its sorted position, and is not
      omitted from the output
- [x] AC5 — a file's line count is the number of newline bytes in it, plus one if the file is
      not empty and its last byte is not a newline. So a file containing `a\nb\n` counts 2, a
      file containing `a\nb` counts 2, and a file containing only `\n` counts 1
- [x] AC6 — a subdirectory directly inside the folder is neither listed nor counted, nothing is
      printed about it on stdout or stderr, and the command exits 0
- [x] AC7 — a symlink directly inside the folder that resolves to a regular file is listed under
      the symlink's own name, with the line count of the file it points at; a symlink that
      resolves to a directory and a symlink that resolves to nothing are both ignored exactly as
      a subdirectory is — not listed, no message on stdout or stderr, exit 0
- [x] AC8 — a file whose name begins with a dot, such as `.gitignore`, is listed like any other
      file
- [x] AC9 — a file that is not text is counted by the same rule as every other file (AC5) and
      gets its own row, so running on a folder that contains a PNG prints one row per file plus
      the total row, prints nothing on stderr, exits 0, and the string `Traceback` appears
      nowhere in stdout or stderr
- [x] AC10 — a folder that contains no files at all — empty, or holding only subdirectories —
      prints exactly `no files` on stdout, prints nothing on stderr, prints no total row, and
      exits 0
- [x] AC11 — when the path given does not exist, and when it exists but cannot be read (a
      directory with mode `000`, tested as a non-root user), the command prints nothing on
      stdout, prints one line on stderr naming that path and that problem, and exits 2
- [x] AC12 — when the path given is a regular file rather than a folder, and when no argument is
      given at all, the command prints nothing on stdout, prints a message on stderr, and exits
      2. (Derived by the analyst from the human's rule for a missing path, not stated by him —
      see `## Notes`)
- [x] AC13 — the tests live in `tests/` and `python3 -m unittest discover`, run from the
      repository root on a machine with only Python 3 installed and no installation step
      performed, exits 0

## Out of scope

- The `--top N` option — the human asked for it explicitly as a second piece of work; it is
  WI-0002.
- Recursing into subdirectories, which the human deferred.
- Reporting bytes, words, or any measure other than lines.
- Any option to change the sort order, the output format, or which files are included.
- Detecting that a file is not text, or reporting it as such. Refinement settled that every file
  is counted by the same byte rule, so a JPEG shows a number like anything else.
- Counting through a symlink that points at a directory, and reporting broken symlinks.
- Installing the tool, packaging it, or providing a `linecount` command on the PATH; it is run
  as `python3 linecount.py <folder>`.

## Notes

Constraints stated by the human at intake:

- Python 3, standard library only, including for the tests. Nothing may need installing, to run
  the tool or to run its tests.
- A single `linecount.py` at the top of the repository.
- Output is plain text that can be piped into `head`.
- The folders in question hold a few dozen files, occasionally a couple of hundred, never
  thousands.
- Two stated failure conditions: needing several flags to get the obvious output, and producing
  a stack trace rather than a number when the folder contains something unusual.
- Although this is a personal utility, someone who inherits the folder must be able to run it.

Settled at refinement (full exchange in `artifacts/refinement-qa.md`). All five open points
carried out of intake are now closed:

- **Tie-break** — filename ascending, byte order. The human's stated requirement was that the
  order not shuffle between runs; AC2 carries both halves.
- **Files that are not text** — the human chose, when pressed, the option that gives every file
  one row and no special case, and said explicitly that he is content for a JPEG to show a large
  meaningless number. AC5 and AC9 encode that; the alternative considered was marking such files
  with `-` and excluding them from the total.
- **Output shape** — mirrors `wc -l`, which is the tool being replaced, so the format is one the
  human's eye already expects.
- **A folder with no files** — `no files` and exit 0, at the human's instruction: "A lonely zero
  looks like the tool broke." He redefined AC3 himself in the same answer, so the total row is
  now specified to appear only when at least one file is listed.
- **The failure path** — exit 2, message on stderr, so stdout stays pipeable into `head`.

Assumptions and analyst-derived criteria, flagged so `plan`, `implement` and `verify` see what
rests on the human's word and what does not:

- **AC12 was never put to the human.** Neither "the path is a regular file" nor "no argument at
  all" was discussed at intake or in refinement. It extends his rule for a missing or unreadable
  path to the two other ways the invocation can be wrong, and matches what `argparse` does by
  default. It is the one criterion here he has not seen.
- **AC7 (symlinks) and AC8 (dotfiles)** were proposed by the analyst and confirmed by the human
  verbatim ("Yes to both as you proposed").
- The exact wording of the stderr messages in AC11 and AC12 is deliberately not fixed; the
  criteria constrain the stream, the exit code and the fact that the message names the path and
  the problem. `plan` may choose the wording.

Gaps accepted at review, recorded here so they outlive the reports nobody re-reads after an item
is closed (`review-close`, 2026-08-17; evidence in `artifacts/review.md` `## Accepted gaps` and
`artifacts/verify-report.md` `## Not verified, and why`):

- **Nothing lints this project**, on this item or any later one (ADR-0003). The one concrete cost
  found so far is an inert `from __future__ import annotations` in `linecount.py`.
- **A filename that is not valid UTF-8 is untested.** `os.fsencode` in the sort key exists for
  exactly that case, and AC2's own example (`A.md` before `a.md`) is verified; a genuinely
  undecodable name was never created.
- **Scale beyond about 200 files, and files beyond 3 MiB, is untested**, which matches the size
  refinement fixed for this tool but is not a guarantee above it.
- **Only POSIX was exercised.** AC7 and AC11 are written in terms of symlinks and Unix
  permissions; the tool has never been run on Windows.
- **`BrokenPipeError` is unhandled.** Piping into `head` was exercised on a 200-file folder and
  did not reach it. An actual sighting is a bug item, not a silent fix.
