---
id: WI-0003
type: work-item
title: Add --sort to order the rows by filename instead of by count
status: done
priority: medium
epic: EP-001
created: "2026-08-16T23:48:51Z"
updated: "2026-08-17T00:26:02Z"
branch: wi/WI-0003
outcome: delivered
---

## Story

As someone who keeps two folders that are meant to hold the same set of notes, I want to list a
folder's files in filename order instead of largest-first, so that the two listings come out in
the same order and I can see by eye whether the same files are present in both.

## Acceptance criteria

- [x] AC1 — `python3 linecount.py --sort name <folder>` prints one row per file in the folder, in
      the row format WI-0001 AC1 fixes, ordered by filename **ascending, compared as bytes** —
      the same comparison WI-0001 AC2 already uses to break a tie — followed by the total row of
      WI-0001 AC3 carrying the plain `total` label. For a folder holding `Zebra.md` (2 lines),
      `apple.md` (7 lines) and `notes.md` (5 lines), the file rows come out in the order
      `Zebra.md`, `apple.md`, `notes.md` — uppercase before lowercase, because that is what byte
      order does, and it exits 0
- [x] AC2 — build folder `A` holding `notes.md`, `todo.md` and `ideas.md`, and folder `B` holding
      the same three names with different contents so that the line counts differ between the
      two. `python3 linecount.py --sort name A` and `python3 linecount.py --sort name B` each
      print their file rows with the names in the order `ideas.md`, `notes.md`, `todo.md` — the
      same order in both outputs, whatever the counts are. A name present in only one of the two
      folders simply has no row in the other output; nothing marks or pads it
- [x] AC3 — `python3 linecount.py --sort count <folder>` produces stdout, stderr and an exit code
      byte-identical to `python3 linecount.py <folder>` on the same folder: count descending,
      filename ascending as the tie-break, and the plain `total` label. Spelling out the default
      changes nothing
- [x] AC4 — with no `--sort` at all, stdout, stderr and the exit code are byte-identical to what
      the tool prints today, for every invocation that names a folder. The tests written for
      WI-0001, WI-0002, BUG-0001, BUG-0002 and BUG-0003 pass unmodified after this item. **The
      one expected difference is the usage and help text:** `python3 linecount.py --help`, and
      the usage block argparse prints on a usage error such as no arguments at all, will gain the
      `--sort` option and will not match today's byte for byte. That is not a regression — it is
      the same unavoidable change `--top` made in WI-0002, written into the criterion here rather
      than rediscovered at review
- [x] AC5 — no short form is accepted: `python3 linecount.py -s name <folder>` prints nothing on
      stdout, prints a message on stderr, and exits 2 — the same shape WI-0002 AC8 fixes for `-t`
- [x] AC6 — on a folder that contains no files at all, `--sort name` and `--sort count` each
      print exactly `no files` on stdout, print nothing on stderr, print no total row, and exit
      0 — WI-0001 AC10 unchanged, whatever `--sort` says
- [x] AC7 — a `--sort` **value** that is neither `name` nor `count`, such as
      `python3 linecount.py --sort size <folder>`, prints nothing on stdout, prints exactly one
      line on stderr beginning `linecount: --sort: ` and naming the problem, and exits 2 — the
      failure shape of WI-0002 AC7, hand-checked for the same reason ADR-0004 gives. A **missing**
      value — `python3 linecount.py --sort <folder>` consuming the folder, or `--sort` as the last
      argument — is left to argparse: nothing on stdout, argparse's own usage block and message on
      stderr, exit 2
- [x] AC8 — `python3 linecount.py --sort name <folder>`, `python3 linecount.py <folder> --sort
      name` and `python3 linecount.py --sort=name <folder>` produce byte-identical stdout, stderr
      and exit code as one another
- [x] AC9 — `python3 linecount.py --top 2 --sort name <folder>` on a folder of at least three
      files exits 0, prints at most two file rows in the row format of AC1, and prints a total row
      carrying WI-0002 AC3's `total (all M files)` label because `--top` was given. **Which** two
      files are selected is deliberately not decided by this item — see `## Notes` — and this
      criterion is written so that it passes under either reading. It fixes the shape only: the
      combination must not print a traceback, must not exit non-zero, and must not lose the
      labelled total. (Analyst-derived, not asked: the human was asked about the combination and
      declined to decide it, then asked not to be held up)
- [x] AC10 — `python3 -m unittest discover`, run from the repository root after this change,
      exits 0, and the new behaviour is covered by tests in `tests/`. (Derived by the analyst from
      WI-0001 AC13 and the WI-0002 AC11 precedent rather than asked; the human confirmed it when
      it was proposed with that label — "Confirmed, add it, and label it as yours")

## Out of scope

- Any sort key other than the filename and the line count. Not size in bytes, not modification
  time, not the file extension.
- A descending filename order. The human was asked and declined one: "Ascending only — I have no
  use for descending names."
- Case-insensitive or locale-aware ordering. He was asked and chose raw byte order explicitly.
- A short form `-s`, on the precedent he set for `--top`: "Same as `--top`: one spelling."
- Changing the default. With no `--sort` the tool still lists largest first; the epic's "no flags
  for the common case" is not being traded away.
- Any change to *which* files are listed, to how a line is counted, or to the total row. This is
  a change to the order of the rows and nothing else — the human's words: "It's a view change,
  not a change to the numbers."
- Comparing two folders itself. The tool still reports on one folder; making two outputs
  comparable is the point, diffing them is the human's job with `diff`.
- Marking, padding or otherwise flagging a filename that is present in one folder and absent from
  another. A missing row is the signal: "a missing row is exactly what I'd want to see, that's
  the whole point. Don't add anything special for it."
- Deciding which files `--top N --sort name` selects. Left open on purpose at the human's
  instruction; see `## Notes`. AC9 constrains only the shape of that output, not its content.
- Recursing into subdirectories, and every other exclusion inherited from EP-001.

## Notes

The human asked for this after EP-001 had been closed and delivered: "sometimes I want it sorted
by filename instead of by count — when I'm looking for a particular file rather than the big
ones. Add a `--sort` option for that." EP-001 was reopened to carry it, per
`spec/ids-and-statuses.md` §3.4; see the epic's journal entry for that decision.

The shape of the option is his, from intake Q2: `--sort name` and `--sort count`, with `count`
the default when the flag is absent. The full exchange is in `tracker/items/EP-001/journal.md`.

**Settled at refinement** (the full exchange, verbatim, is in `artifacts/refinement-qa.md`). Two
of the three open points intake carried are closed. The failure shape of a bad `--sort` value is
AC7 — our own one-line message for a bad *value*, argparse's own error for a *missing* one, split
that way on his instruction. The test criterion is AC10, analyst-derived and confirmed with that
label. Separately, AC2 was rewritten from "compared row for row by eye" into a worked example a
stranger can run, and AC4 gained the usage-line exception before any code exists rather than
after a review discovered it, as happened on WI-0002.

**Deliberately undefined: which files `--top N --sort name` selects.** This is the third open
point, and it is not closed — by decision, not by omission. The human was asked, with both
readings and a worked example, and answered:

> No. I don't want to pick, and I don't want you picking and then writing it down as though it
> were decided — I've seen how that reads six months later. Leave it genuinely open. I'll tell
> you what I want the first time I actually type both flags together, and not before.
>
> And don't hold the item up over it. Mark it Ready and get going on the part I do know I want.

The two readings, recorded so that whoever eventually asks him can put the same two options back
to him: either `--top` still selects the N **largest** files and `--sort name` only orders those N
for display, or the name order is applied first and `--top N` returns the N **alphabetically
first** files. On a folder holding `big.txt` (90 lines), `mid.txt` (50) and `apple.md` (3),
`--top 2 --sort name` gives `big.txt`, `mid.txt` under the first reading and `apple.md`, `big.txt`
under the second.

What that means for the skills downstream, none of which can ask him:

- **`plan` and `implement`:** this is not a blocking unknown, so do not file a question about it.
  He was asked and chose to leave it unconstrained; escalating it to the architect would get it
  decided by someone other than him and written down as a decision, which is the exact outcome he
  refused. Write whatever falls out of the simplest code that satisfies AC1–AC10, record in the
  journal what that turned out to be, and do not describe it as a decision, do not attribute it to
  him, and do not add a criterion blessing it.
- **`verify`:** AC9 makes you run the combination, so your report will contain an observation of
  what the code does. That is a record of current behaviour, not a contract. Do not cite it as
  settled, and do not raise a defect because the selection is one reading rather than the other —
  no criterion says which it should be.
- **When he first types both flags** and says what he wants, that is a new item under EP-001 (or a
  bug, if what he finds is a crash — AC9 is what makes that distinction possible).

**Gaps accepted at review**, recorded here so they outlive the reports nobody re-reads after an
item is closed (`review-close`, 2026-08-17; evidence in `artifacts/review.md`,
`artifacts/verify-report.md` and `artifacts/impl-report.md`):

- **`--top N --sort name` selects the N alphabetically first.** Observed, not decided: with
  `--sort name` the existing `rows[:top]` slice takes the first N of the name order. On the
  criteria's own three-file folder, `--top 2 --sort name` prints `Zebra.md` and `apple.md`, not
  the two largest. No criterion fixes this (AC9 pins only exit 0, at most N rows, and the labelled
  total), ADR-0009 records why it was left open and that reaching the other reading is one line in
  `main`. When the human first types both flags and says what he wants, that is a new item — or a
  bug only if what he finds is a crash, which AC9 forbids.
- **Argparse's `description` still reads "List the files in a folder with their line counts,
  largest first."** True of the default and of nothing else; `--help` now lists two flags the
  sentence does not mention. It was already partial after WI-0002 added `--top`, so it is
  pre-existing rather than a regression here, no criterion covers it, and AC4 excepts the help text
  from byte-identity. `implement` declared it rather than widening the diff.
- **`sort_rows`'s `else` branch silently means "count".** Any `order` value that is not exactly
  `"name"` returns the count order rather than raising — `sort_rows(rows, "nmae")` would look like
  it worked. It is unreachable today because `parse_sort` gates the only call site and
  `ParseSortTest` proves it rejects everything else, and `verify` confirmed that test is sensitive.
  Recorded because an unreachable-today branch stops being unreachable the moment a second call
  site is added.

**No Definition of Ready override was recorded, although he offered one** ("If that means
overriding your checklist, override it — that's my call, isn't it?"). It is his call, and an
override would have been recorded loudly if the item needed one. It does not: R1–R9 all pass on
the refined item, and the per-criterion evidence is in this item's journal. R4 requires that every
acceptance criterion be decidable by observation, and every one of AC1–AC10 is; the checklist has
no completeness criterion for an item to fail by leaving one flag combination unconstrained. The
override record must name the criteria that were not met, and naming one here would mean writing
down something untrue. `artifacts/refinement-qa.md` closes with the full reasoning.

`priority: medium` was set by the analyst, not stated by the human. It is the only open item in
the tracker, so there is no ordering to get wrong; `medium` matches `--top` and says what is
true — the epic's delivered goal stands without this.

No `depends-on` is recorded: WI-0001 and WI-0002 are both `done`, so there is nothing unfinished
to sequence after. The item does build on the order WI-0001 fixed and the flag WI-0002 added,
and the criteria cite them by ID.
