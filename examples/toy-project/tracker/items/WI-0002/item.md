---
id: WI-0002
type: work-item
title: Add --top N to show only the N largest files
status: done
priority: medium
epic: EP-001
created: "2026-08-16T21:13:44Z"
updated: "2026-08-16T22:14:38Z"
depends-on:
  - WI-0001
branch: wi/WI-0002
outcome: delivered
---

## Story

As someone scanning a folder that holds a couple of hundred files, I want to ask for only the N
largest, so that I get the few files I actually care about without piping the output through
another command.

## Acceptance criteria

- [x] AC1 — `python3 linecount.py --top 3 <folder>` prints at most three file rows, in the row
      format WI-0001 AC1 fixes, followed by the total row of AC3. The rows are the first three
      of the order WI-0001 AC2 fixes (count descending, then filename ascending in byte order)
- [x] AC2 — the limit is applied after sorting, so a tie at the cut line is broken by filename
      rather than by chance. For a folder holding `big.txt` (9 lines) and `a.md`, `b.md`, `c.md`
      (5 lines each), `--top 3` prints exactly three file rows — `big.txt`, `a.md`, `b.md` — and
      no row for `c.md`
- [x] AC3 — when `--top` is given, the total row is the sum of the line counts of **every** file
      in the folder, not only of the rows shown, and its label names that: the number, two
      spaces, then `total (all M files)`, where M is the number of files in the folder — that
      is, the number of rows the same command would print without `--top`. For a folder of 27
      files summing to 1204 lines, the total row reads `1204  total (all 27 files)`
- [x] AC4 — when `--top` is not given, the total row keeps WI-0001's plain `total` label, and
      stdout, stderr and the exit code are byte-identical to what WI-0001 delivered on the same
      folder. The tests written for WI-0001 pass unmodified after this item
- [x] AC5 — `--top N` where N is larger than the number of files in the folder lists every file
      and exits 0; the total row still carries the AC3 label, because `--top` was given, even
      though every file is on screen
- [x] AC6 — `--top 0` prints no file rows, still prints the total row of AC3, and exits 0. It is
      not an error
- [x] AC7 — `--top -1`, and `--top` given a value that is not a whole number such as `--top abc`,
      print nothing on stdout, print one line on stderr naming the problem, and exit 2 — the
      same failure shape as WI-0001 AC11
- [x] AC8 — `python3 linecount.py --top 3 <folder>` and `python3 linecount.py <folder> --top 3`
      produce byte-identical stdout, stderr and exit code. No short form of the flag is
      accepted: `python3 linecount.py -t 3 <folder>` prints nothing on stdout, prints a message
      on stderr, and exits 2
- [x] AC9 — on a folder that contains no files at all, `--top 0`, `--top 3` and `--top 99` each
      print exactly `no files` on stdout, print nothing on stderr, print no total row, and exit
      0 — WI-0001 AC10 unchanged, whatever N is
- [x] AC10 — the count column is as wide as the widest number actually printed, the total
      included, so the total row lines up with the file rows even when it is the wider number.
      For a folder of 27 files summing to 1204 lines — `f00.txt` … `f25.txt` of 46 lines each
      and `small.txt` of 8 — `--top 2` prints `··46··f00.txt`, `··46··f01.txt`,
      `1204··total (all 27 files)`, where `·` stands for one space character. (The example was
      corrected by `answer-questions` for Q-001: as first written it named a folder of 27 files
      whose two largest held 9 and 7 lines *and* summed to 1204, which cannot exist. The rule in
      the first sentence is the human's, from refinement Q6, and is unchanged.)
- [x] AC11 — `python3 -m unittest discover`, run from the repository root after this change,
      exits 0, and the new behaviour is covered by tests in `tests/`. (Derived by the analyst
      from WI-0001 AC13 rather than asked; the human confirmed it when it was proposed — see
      `## Notes`)

## Out of scope

- Any other option or flag. This item adds `--top` and nothing else.
- A short form `-t`. The human declined one explicitly: "One spelling."
- Changing the sort order, the output format, or the plain `total` label established by
  WI-0001 when `--top` is absent.
- Any option to change what the total counts. With `--top` it is always every file in the
  folder; that is not configurable.
- Selecting files by a line-count threshold ("everything over 100 lines") rather than by rank.
- Recursing into subdirectories, and every other exclusion inherited from EP-001.

## Notes

The human asked for this explicitly and asked equally explicitly that it not be folded into the
first item: "One thing I do want, but as a *second* piece of work after the basic thing works:
a `--top N` flag to show only the N largest. That one's genuinely useful, I nearly always want
the top few. Don't build it into the first item."

`depends-on: WI-0001` because there is no output to limit until WI-0001 exists.

Settled at refinement (full exchange in `artifacts/refinement-qa.md`). All three open points
carried out of intake are closed:

- **What the total means when the output is limited.** It stays the sum of every file in the
  folder, and the label says so. The human chose the labelled variant over both alternatives:
  he wanted the number not to shrink when he asks for fewer rows, and he rejected leaving it
  unlabelled — "I'd definitely wonder why the column doesn't add up."
- **AC4 as intake derived it** (a bad `--top` value fails loudly and non-zero) is now confirmed
  by the human in as many words: "yes, AC4 as your analyst derived it is what I'd have said if
  asked." It is AC7 here, with the stream and the exit code pinned to WI-0001's failure shape.
- **Flag position.** Both `--top N <folder>` and `<folder> --top N` are accepted.

How this item reads against WI-0001, which is already `ready` and whose criteria were therefore
not edited:

- **`--top 0` and WI-0001 AC3.** WI-0001 AC3 says that *when at least one file is listed* the
  last line is the total row. AC6 here prints a total row when **no** file rows are listed,
  which is outside that criterion's condition rather than against it. WI-0001 was not amended;
  if a later reader believes it should be, that is an `answer-questions` change, not a silent
  edit here.
- **The empty folder still wins.** AC9 keeps WI-0001 AC10 intact: no files means `no files` and
  no total row, whatever `--top` says. So the total row of AC6 only ever appears on a folder
  that does have files.

Assumptions and analyst-derived criteria, flagged so `plan`, `implement` and `verify` see what
rests on the human's word:

- **The plural in `(all M files)` is not special-cased.** A folder of one file yields
  `(all 1 files)`. Nobody was asked; the human's example was `(all 27 files)`. Inventing a
  singular form would add a rule the criteria would then have to state, and getting it wrong is
  cosmetic. Cheap to reverse.
- **AC11 (the test command) was proposed by the analyst, not asked as a question.** The human
  confirmed it when it was put to him with that label: "add the criterion … Mark it as your own
  if that's the honest label."
- **AC8's rejection of `-t`** turns his "no short form" into an observable: `-t` must fail
  rather than merely be undocumented.

Gaps accepted at review, recorded here so they outlive the reports nobody re-reads after an item
is closed (`review-close`, 2026-08-17; evidence in `artifacts/review.md` and
`artifacts/verify-report.md`):

- **The usage line changed, and with it the no-argument error output.** WI-0001 printed
  `usage: linecount [-h] folder`; the tool now prints `usage: linecount [-h] [--top N] folder`.
  `verify` found this by running the binary WI-0001 shipped beside the new one. It is outside
  AC4's "on the same folder", WI-0001 AC12 asks only for a message on stderr and exit 2 (both
  hold), and no implementation of `--top` could leave that line alone without misdescribing the
  interface — but it *is* a difference in what the tool prints, and it is recorded rather than
  smoothed over.
- **Nothing lints this project** (ADR-0003): the 69 changed lines of `linecount.py` were read at
  review and by no tool.
- **`--top` accepts whatever Python's `int()` accepts**, so `--top 3_0` means 30 and `--top " 3 "`
  means 3. Untested; it cannot produce a wrong count, only an unexpected N.
- **The singular label was never run**: a one-file folder prints `total (all 1 files)`, as this
  item's own assumption says it should.
- **Only POSIX was exercised**, unchanged from WI-0001.

Amended after `ready`, by the only route that allows it:

- **AC10's worked example was corrected by `answer-questions` on 2026-08-17**, answering `Q-001`
  from `implement`. The example as refined described a folder that cannot exist — 27 files whose
  two largest hold 9 and 7 lines sum to at most 243, not 1204 — so no verifier could build it.
  The **rule** the criterion states, and which the human confirmed verbatim at refinement Q6
  ("size the column to the widest number actually printed, total included, so everything lines
  up"), was not touched; only the illustration was replaced with a folder that exists and
  produces the same alignment. The human's `27` and `1204` survive the correction; the "9 and 7"
  do not. Full reasoning, the two alternatives, and the files changed are in
  `questions/Q-001.md`.
