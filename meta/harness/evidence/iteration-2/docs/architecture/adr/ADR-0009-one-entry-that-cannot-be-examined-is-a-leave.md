---
title: An entry the planner cannot examine becomes a leave action, not an aborted run
version: 3
status: current
updated: 2026-08-28T13:57:57Z
updated-by: implement
updated-for: BUG-0006
---

# ADR-0009 — An entry the planner cannot examine becomes a `leave` action, not an aborted run

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for BUG-0004
- **Supersedes:** —

## Context

One dangling symlink in the target folder costs the user the whole folder. `build_plan` calls
`entry.stat()` on every entry with a recognised extension, and `stat` on a symlink whose target
is gone raises `FileNotFoundError` out of the loop, out of `build_plan`, and into `cli.py`'s
`except OSError` — where ADR-0006's handler reports the *target folder* as unreadable and exits 2
[src: BUG-0004; src: tidy/planner.py; src: tidy/cli.py; src: ADR-0006]. The folder was read
perfectly well. The user is told otherwise, no file in it is tidied, and stdout is empty
[src: run: python3 -m tidy /tmp/bug4 → exit 2, "tidy: /tmp/bug4 cannot be read: No such file or
directory", stdout empty].

The dangling symlink is one member of a class, and the class is wider than the item's fixture.
`os.DirEntry.is_dir()` catches `FileNotFoundError` internally but lets every other `OSError`
through, so an entry that is a **symlink loop** aborts the same scan one call earlier — before
any extension is even looked at
[src: run: python3 -m tidy /tmp/bug4loop → exit 2, "tidy: /tmp/bug4loop cannot be read: Too many
levels of symbolic links"; src: tidy/planner.py]. Whatever is decided here has to be about
"an entry that cannot be interrogated", not about broken symlinks.

Two existing decisions bound the answer. ADR-0002 puts every per-entry decision in `planner.py`
and nothing else there [src: ADR-0002]. ADR-0006 decided that a failure to list **the target
folder** is reported at the CLI boundary as exit 2, and rejected an option (its option D) that
would have moved that reporting into the planner [src: ADR-0006]. This decision is the other
half of the same boundary and must not disturb it: the target failing and one entry failing are
different events, and only the second one has somewhere useful to be reported.

## Options considered

- **A — Catch the `OSError` per entry inside `build_plan` and emit a `leave` action for that
  entry.** The scan continues; every other file is planned and reported as usual. Cost: the
  planner's failure surface grows by one reason string, and a reader of `build_plan` has to see
  that the guard wraps only the two calls that interrogate the filesystem. Risk: a guard written
  too widely would turn a defect in the planner's own logic into a `leave` line — mitigated by
  scoping it to `entry.is_dir()` and `entry.stat()`, which are the only calls in the loop body
  that touch an entry [src: tidy/planner.py].
- **B — Skip the unexaminable entry silently.** Cost: the user is never told that something in
  their folder was passed over, which is the one thing the preview exists to prevent
  [src: docs/product/vision.md]. It satisfies BUG-0004 AC1 and quietly breaks the product's
  central promise. Risk: the file is invisible in both modes, so nobody finds out until they go
  looking for it.
- **C — Age symlinks by the link rather than by its target** — `entry.stat(follow_symlinks=False)`
  — so a dangling symlink has an age and gets moved like any other file. Cost: it changes how
  **every** symlink is aged, which WI-0002's review examined and accepted as it stands
  [src: WI-0002]; no criterion asks for that change, and it belongs to an item that says so. It
  also does not fix the class: the symlink loop above raises in `is_dir()`, before any `stat`
  call, and an entry that fails with `EACCES` or `EIO` still aborts the run. Risk: worth naming
  because it *looks* sufficient — the move would even succeed, since `os.link` on this platform
  hard-links the symlink itself rather than following it
  [src: run: os.link("/tmp/bug4/broken.pdf", "/tmp/bug4dest/broken.pdf") → no error, the dangling
  link was hard-linked]. So the argument against C is the ageing semantics and the incomplete
  coverage, not an apply-time failure; a future reader reconstructing this decision from the
  symptom alone would get that wrong.
- **D — Keep aborting, and improve the CLI message** so it says which entry failed instead of
  blaming the folder. Cost: it fixes BUG-0004 AC2 and leaves AC1 exactly as it is — one bad entry
  still costs the user every good one. Risk: it reads as a fix, and the item's own
  `## Expected behaviour` rules it out [src: BUG-0004 AC1].

## Decision

**A.** An `OSError` raised while interrogating a single entry is caught inside `build_plan`'s
loop and becomes `Action(kind="leave", name=<entry name>, reason="cannot be examined: <the
operating system's reason>")`; the loop then continues with the next entry
[src: tidy/planner.py; src: BUG-0004 AC1].

Four details are fixed here, because each is checkable against the code and each would otherwise
be settled silently in a plan step:

1. **The guard covers `entry.is_dir()` and `entry.stat()`, and nothing else.** Those are the two
   calls in the loop body that ask the filesystem about the entry, and both are demonstrated
   above to raise on a real fixture [src: tidy/planner.py]. The collision helpers use
   `os.path.lexists` and `os.path.isdir`, which return rather than raise
   [src: tidy/planner.py], so widening the guard around them would buy nothing and hide more.
2. **`os.scandir(folder)` stays outside the guard.** Listing the target is ADR-0006's case, it is
   already handled at the CLI boundary, and BUG-0001's regression test asserts that behaviour
   [src: ADR-0006; src: tests/test_cli.py]. An entry-level guard that also swallowed the scan
   would silently reverse a decision this one is not allowed to touch.
3. **The clause is `except OSError`, not `except FileNotFoundError`.** The item reproduces with
   `ENOENT`, but `ELOOP` reaches the user identically today, and `EACCES` and `EIO` are the same
   event from the entry's point of view. Narrowing to the reproduced errno would leave the rest
   of the class aborting the run while claiming it was handled — the same reasoning ADR-0006
   detail 1 applies at the target level [src: ADR-0006].
4. **The reason carries the operating system's own words**, via `error.strerror`, and names no
   cause the code has not established. `ENOENT` on an entry `scandir` just listed is almost
   always a broken symlink and sometimes a file deleted mid-scan; the planner cannot tell which,
   so it says what failed rather than why it thinks it failed. This is ADR-0006 detail 2 applied
   one level down [src: ADR-0006].

The exit status does not change: a `leave` is a planned outcome, not a failed move, and only a
`"failed"` outcome from `apply_plan` makes the process exit non-zero [src: ADR-0007;
src: tidy/cli.py]. A run over a folder with one unexaminable entry and one ordinary file
exits **0**, in both modes, and `README.md` is amended to say that a run which left files is
still a success [src: BUG-0004 AC3; src: README.md].

## Consequences

- The planner's contract widens by one sentence: `build_plan` returns an action for every entry
  it was asked about, including the ones the filesystem would not describe. It still writes
  nothing and still decides every destination itself [src: ADR-0002; src: tidy/planner.py].
- The two error boundaries are now explicit and different, which is the part worth remembering:
  **the target folder failing is the CLI's** (one line on stderr, empty stdout, exit 2, ADR-0006),
  **one entry failing is the planner's** (a `leave` line on stdout, the run continues, exit
  unchanged). Neither can be moved without contradicting the other's ADR [src: ADR-0006].
- The preview keeps its promise for this case as well: what the run says it will do to each entry
  is what a user sees before anything moves, including for the entries it cannot handle
  [src: docs/product/vision.md].
- A file removed between `os.scandir` and `entry.stat()` now produces a `leave` line rather than
  an aborted run. That is a race no plan can close — the listing is a snapshot — and reporting it
  per entry is the honest form of it.
- **The citations in this record name files and symbols, not line numbers.** They were line numbers
  in v1 and every one of them was exact against `main` — and wrong the moment the nine-line guard
  this ADR decides was inserted above them, by one line in two places and by nineteen in another
  [src: BUG-0004/Q-002]. That is not carelessness but the shape of the thing: an ADR about a change
  to a file cites that file, and the change is what moves its own line numbers. The prose names
  `entry.is_dir()`, `entry.stat()`, `os.path.lexists` and `os.path.isdir` in full, so a reader has
  an exact search term that cannot drift.
- **Reversibility: cheap.** The guard is one `try`/`except` in one function in `tidy/planner.py`
  plus one reason-string helper; no data on disk, no signature change, no other module involved
  [src: tidy/planner.py]. Moving to C later is one keyword argument and a new item to justify the
  ageing change; moving to B is deleting the `Action` the guard appends.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-08-28T13:57:57Z | implement | BUG-0006 | The two `tidy/cli.py:NN` citations v2 left exact — `:67` in `## Context` and `:93` in `## Decision` — became file-level. Both had drifted twenty-one lines under WI-0003's `--rules` block: `except OSError` is at 88 and the `"failed"` return at 114. The prose names both symbols. This completes for `tidy/cli.py` the sweep v2 performed for `tidy/planner.py`, and makes this record's own `## Consequences` bullet about line numbers true of the whole document. Per ADR-0013 |
| 2 | 2026-08-27T21:06:34Z | answer-questions | BUG-0004 | Answering BUG-0004/Q-002: the six `tidy/planner.py:NN` citations were exact against `main` and pointed at the wrong lines once this ADR's own guard was inserted above them. Replaced with file-level citations, the named symbols in the prose carrying the precision, and a consequence recording why |
| 1 | 2026-08-27T20:45:46Z | plan | BUG-0004 | First version: an `OSError` from one entry becomes a `leave` action inside `build_plan`, leaving ADR-0006's target-level boundary untouched |
