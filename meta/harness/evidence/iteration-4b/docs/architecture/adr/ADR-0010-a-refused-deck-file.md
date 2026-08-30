---
title: A filesystem refusal on the deck file is store's to classify and cli's to report
version: 1
status: current
updated: 2026-08-30T05:05:46Z
updated-by: plan
updated-for: BUG-0001
---

# ADR-0010 — A filesystem refusal on the deck file is `store`'s to classify and `cli`'s to report

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** plan (architect), for BUG-0001
- **Supersedes:** —

## Context

`recall/cli.py` catches `store.DeckUnreadable` and nothing else, so every other operating-system
refusal on the deck file escapes `main` and reaches the person as a Python traceback
[src: BUG-0001]. Three reproductions are on the item, and they arrive at two different boundaries:

- **A** — the deck's directory is not writable, so `save` raises `PermissionError` out of
  `tempfile.mkstemp`, and the exception names the *temporary* file rather than the deck
  [src: BUG-0001].
- **B** — a directory is at the deck's path, so `load` raises `IsADirectoryError` out of
  `Path.read_bytes` [src: BUG-0001].
- **C** — a file is where the deck's *directory* should be. `load` raises `NotADirectoryError`,
  which `store.load` currently catches beside `FileNotFoundError` and turns into an empty deck, so
  `recall list` reports an empty deck and exits 0 [src: recall/store.py; BUG-0001].

Three things already decided constrain the answer:

- `store.py` never prints and never decides policy; `cli.py` owns everything a person sees and is
  the only layer that knows a terminal exists [src: docs/architecture/overview.md].
- A deck that cannot be read is reported and never repaired, overwritten or treated as empty
  [src: ADR-0004].
- **Absent is not the same as unreadable**: a missing file, and a missing parent directory, mean
  an empty deck [src: ADR-0004]. A file sitting where the directory belongs is neither of those
  two things, which is why C is a defect rather than a consequence of that rule.

And two of the item's criteria bear directly on where the code goes: the message for A must name
the deck file and not the temporary one, and the message for C must name the path that is in the
way [src: BUG-0001].

The item's own `## Notes` leaves exactly one question open for this decision — *"whether `store`
should wrap `OSError` in an exception of its own so `cli` catches one type rather than two"*
[src: BUG-0001].

## Options considered

- **A — `cli` catches `OSError` alongside `DeckUnreadable` at every call site.** Cost: small
  diff, no new type. Risk: `cli` would have to know that `save` writes through a temporary file
  in the destination directory, in order *not* to print `exc.filename` — that is `store`'s
  mechanism leaking into the layer that is supposed to know nothing about the file
  [src: recall/store.py]. It would also have to decide for itself which `OSError`s mean "no deck
  yet" and which mean "something is wrong", a classification `store.load` already owns and would
  then own in two places [src: recall/store.py].
- **B — `store` catches `OSError` at both of its boundaries and raises a deck-level exception
  carrying the deck's path and a short reason.** Cost: one new exception class, one base class,
  and a small classifier in `store.py`. Risk: `store` acquires a sentence fragment intended for a
  person, which is close to the printing it is forbidden to do — mitigated by the fragment being
  a value on the exception, exactly as `DeckUnreadable.detail` already is, with `cli` deciding the
  sentence around it [src: recall/store.py].
- **C — `store` returns a result object rather than raising.** Cost: every call site changes
  shape. Risk: the existing `DeckUnreadable` path stays an exception, so the module would signal
  failure two ways; and `save` has no return value today, so it would grow one solely to carry an
  error.
- **Reusing `DeckUnreadable` for an operating-system refusal, rather than adding a sibling.**
  Rejected: the item requires that the six content cases keep their existing messages
  [src: BUG-0001], and a write refused by the operating system has to say the deck could not be
  *written* — one type cannot carry both without `cli` re-deriving which it has.

## Decision

**B.** `store.py` classifies; `cli.py` reports.

1. **An exception family, not one class.** `DeckError` is the base and carries `path` and
   `detail`. `DeckUnreadable(DeckError)` keeps its present meaning exactly — the file is present
   and its *contents* are not a deck — and its `str()`, `path` and `detail` are unchanged
   [src: recall/store.py].
   `DeckInaccessible(DeckError)` is new and means the operating system refused an operation on
   the deck file.
2. **`path` on a `DeckInaccessible` is always the deck file**, never the temporary file `save`
   writes through and never an ancestor. It is the path the person is being told about, and it is
   the one thing `cli` prints from the exception.
3. **`detail` names the obstruction when there is one.** In order: if an ancestor of the deck's
   directory exists and is not a directory, the detail names that path and says a directory is
   required there; otherwise, if the deck's path is itself a directory, the detail says so;
   otherwise the detail is the operating system's own words for the error, lower-cased. The
   classifier only inspects the filesystem and never writes to it.
4. **`load` treats `FileNotFoundError` alone as an absent deck.** Every other `OSError` becomes a
   `DeckInaccessible`. This does **not** supersede `ADR-0004` §6; it implements it. A missing file
   and a missing parent directory both raise `FileNotFoundError`, so both still load as an empty
   deck, and `NotADirectoryError` — which is neither of those two things — stops being read as
   absence.
5. **One exit code covers both directions.** A deck file that could not be used exits `3`,
   whether the failure was on the read or on the write. The alternative was a fourth code for the
   write side; it is not taken, because no criterion or ADR asks a caller to tell the two apart,
   and an exit code is an observable commitment that is easier not to make than to withdraw. The
   constant is renamed to say what it now covers; its value does not move.
6. **`cli` catches `store.DeckError` where it loads and `store.DeckInaccessible` where it saves**,
   and reads no `errno` and no exception filename. The load-side message is the one that exists
   today, unchanged, so the six content messages are preserved by construction; the save-side
   message is new and says the deck could not be written.

## Consequences

- All four subcommands are covered by one change, because all four reach the deck through the
  same two `store` functions [src: recall/cli.py]. A fix at the call sites would have had to be
  repeated four times and would have been incomplete the next time a subcommand is added.
- `cli.py` gains a second report function and a second failure shape to test, and `store.py`
  gains a classifier that reads the filesystem — a module that previously only opened the one
  file it was given. The classifier can itself be refused by the operating system; it is
  specified to return "no obstruction" in that case rather than to raise.
- A person whose deck directory has been replaced by a file is now told so and gets a non-zero
  exit, where before they were told their deck was empty [src: BUG-0001]. That is a behaviour
  change on a path that previously exited 0, and it is the point of the item.
- Nothing about the deck's *format* changes, so `DECK_FORMAT_VERSION` does not move and no
  migration is implied [src: ADR-0004].
- **Reversibility: high.** The decision lives in two modules and touches no file format, no
  command-line surface and no stored data. Reversing clause 4 is one exception name in one
  `except` clause; reversing the whole of it is deleting one class and one function and moving
  four `except` clauses back. The one clause that is *not* free to reverse is 5, because an exit
  code is observable: withdrawing code `3` from the write path after a person has scripted
  against it would be a breaking change, which is the reason a fourth code was not minted.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T05:05:46Z | plan | BUG-0001 | First version: `store` classifies an operating-system refusal into `DeckInaccessible`, `load` treats only `FileNotFoundError` as absence, and `cli` reports without reading `errno` |
