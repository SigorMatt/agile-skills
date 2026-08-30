---
id: BUG-0001
type: bug
title: A filesystem error on the deck file surfaces as a traceback, not a message
status: done
priority: medium
epic: EP-001
created: "2026-08-30T02:07:30Z"
updated: "2026-08-30T05:43:23Z"
found-in: WI-0001
branch: wi/BUG-0001
outcome: delivered
---

## Summary

`recall/cli.py` catches `store.DeckUnreadable` and nothing else, so any *other* filesystem error
on the deck file — a permission problem, a deck path that is a directory — escapes `main` and
reaches the person as a Python traceback with a non-zero exit. Found while verifying WI-0001, on
branch `wi/WI-0001` at commit `7c552ef`, by exercising boundary conditions beyond the criteria.

This is **not** a failure of any WI-0001 acceptance criterion, and WI-0001 was not sent back for
it. AC8 is scoped by its own text to a deck file the tool "cannot read as a deck — it is
truncated, malformed, or not the format the tool writes", which is a statement about the file's
*contents*; all six content cases were exercised during verification and all six refuse cleanly.
Neither condition below is a content problem, and no criterion on WI-0001 covers either. Under
`verify`'s classification rule — "does an acceptance criterion of this item say the behaviour
should be different? If no, it is a bug" — this is a bug.

**Three reproductions, one defect.** They are filed together rather than separately because
they share a single root cause at a single boundary: `cmd_add` and `cmd_list` catch
`DeckUnreadable` but not `OSError`. One fix closes all three, and a regression test would be
unable to demonstrate the fix without covering both paths — `save`'s and `load`'s.

**Reproduction C is the one to look at first**, and it was added by `review-close` rather than by
`verify`. It is the only one of the three that fails *quietly*: `recall list` reports an empty
deck and exits 0. `store.load` catches `NotADirectoryError` alongside `FileNotFoundError` and
returns an empty `Deck` for both, but they are not the same condition — one means "there is no
deck yet", the other means "something is where the deck's directory should be". `ADR-0004` §6
draws exactly that line ("absent is not the same as unreadable"), and this is the one place the
code blurs it. Nothing is lost, because the subsequent `add` fails before writing — but a person
whose deck directory has been replaced by a file is told they have no cards, which is the shape
of the failure the stakeholder named.

Nothing is lost in either case: no deck is truncated, overwritten or replaced, so the
stakeholder's stated failure condition — *"don't lose my progress"* — is not in play. What is
wrong is that the tool stops being usable at the exact moment it should be telling a person what
to do about their deck.

## Steps to reproduce

Both reproductions are against `bin/recall` on `PATH`, with `HOME` pointed at a scratch directory.

**A — the deck's directory is not writable.**

1. `mkdir -p "$H/.local/share/recall" && chmod 500 "$H/.local/share/recall"`
2. `HOME="$H" recall add --question q --answer a`

**B — something other than a file is at the deck path.**

1. `mkdir -p "$H/.local/share/recall/deck.json"`
2. `HOME="$H" recall list`

**C — a file is where the deck's directory should be.**

1. `mkdir -p "$H/.local/share" && printf 'not a directory' > "$H/.local/share/recall"`
2. `HOME="$H" recall list` — reports an empty deck, exit 0
3. `HOME="$H" recall add --question q --answer a` — traceback, exit 1

## Expected behaviour

The same shape of refusal `ADR-0004` §5 and WI-0001 AC8 already establish for a deck that cannot
be read: a message on standard error that says what is wrong and names the file, a non-zero exit,
and nothing written. `ADR-0001` §5 puts it generally — "exit codes carry the outcome... with the
reason written to standard error". A traceback is not a reason written for a person.

## Actual behaviour

**A**, exit 1:

```
    fd = _os.open(file, flags, 0o600)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [Errno 13] Permission denied:
'/.../.local/share/recall/deck.json.5u4wwd96.tmp'
```

**B**, exit 1:

```
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
IsADirectoryError: [Errno 21] Is a directory:
'/.../.local/share/recall/deck.json'
```

**C**, `list` at exit **0**:

```
The deck is empty. Add a card with: recall add --question "..." --answer "..."
```

and then `add`, exit 1:

```
    os.mkdir(self, mode)
FileExistsError: [Errno 17] File exists: '/.../.local/share/recall'
```

A and B are the full traceback; the lines above are their tails. Note that A's message names the
*temporary* file rather than the deck, which is an implementation detail a person cannot act on,
and that C reports success while showing a person none of their cards.

## Acceptance criteria

- [x] AC1 — reproduction A writes a message to stderr that names the deck file — not the
      temporary file — says the deck could not be written, and exits non-zero. No traceback
      appears on either stream.
- [x] AC2 — reproduction B writes a message to stderr that names the deck file, says it could not
      be read, and exits non-zero. No traceback appears on either stream.
- [x] AC3 — reproduction C exits non-zero from **both** `recall list` and `recall add`, and the
      message names the path that is in the way. `list` reporting an empty deck at exit 0 is the
      defect, so a fix that only quietens `add` does not satisfy this.
- [x] AC4 — in all three cases nothing under the deck's directory is created, modified or
      removed: the directory listing and every file's `sha256` are identical before and after.
- [x] AC5 — a regression test covers all three reproductions and fails if the handling is
      removed, demonstrated by removing it and recording which tests fail.
- [x] AC6 — the six content cases WI-0001 AC8 covers still refuse with their existing messages:
      truncated JSON, text that is not JSON, JSON that is not an object, an object with no
      `cards` array, a card missing a field, and an empty file.

## Notes

**Where the fix belongs.** `docs/architecture/overview.md` gives `store.py` the rule that it
never prints and `cli.py` the rule that it owns everything a person sees, so the catch belongs in
`cli.py` beside the existing `DeckUnreadable` handler — not inside `store.py`. Whether `store`
should wrap `OSError` in an exception of its own so `cli` catches one type rather than two is a
design question for `plan`, not a decision this report takes.

Reproduction C additionally needs `store.load` to stop treating `NotADirectoryError` as absence.
That is a one-line change with a real consequence, and it is the reason C is worth its own
acceptance criterion rather than being folded into A and B.

**Not covered by this bug.** A question side containing a newline makes `recall list` print a card
across two lines, which no criterion forbids and which nothing currently depends on. It is
recorded in `tracker/items/WI-0001/artifacts/verify-report.md` as an observation, and it belongs
to whoever refines a criterion that parses `list` output — not here.

**Accepted at review, and left open deliberately.** `review-close` closed this item over the
following, each recorded here because a report nobody reads again is not a record
(`review.md`, `## Accepted gaps`):

1. **A dangling symlink where the deck's directory belongs still reports an empty deck at exit
   0.** Unchanged by this item — `read_bytes` raises `FileNotFoundError` for it before and after —
   and defensible under `ADR-0004` §6, which makes *"a missing parent directory"* an empty deck.
   Whether a dangling symlink is "missing" or "in the way" is a question about that ADR's wording,
   for whoever next refines a criterion about the deck's directory.
2. **A write that fails *after* the temporary file is opened is untested** — `ENOSPC` during
   `json.dump`, a refused `fsync`, a refused `os.replace`. `save`'s wrapper covers them by
   construction and `_refusal` falls through to the operating system's words, but provoking a full
   filesystem was beyond both the implementation and the verification.
3. **`_refusal`'s `strerror is None` fallback is unexercised.** No condition reached in
   verification produced an `OSError` without a `strerror`.
4. **Behaviour as root, and under concurrency, is untested.** The three mode-dependent test
   classes skip when `os.geteuid() == 0`; both runs were as uid `1000`. Two `recall` processes
   against one deck is untested here as everywhere else in this epic.
5. **Two cosmetic inaccuracies were not sent back**, because each costs a full implement-and-verify
   cycle and neither misleads about behaviour: `cli.py` binds `except store.DeckError as
   unreadable`, whose name is now narrower than what it can hold, and
   `tests/test_deck_file_errors.py`'s module docstring still enumerates the three reproductions
   where the file now has four classes. The example block for the obstruction message in
   `docs/process/using-recall.md` §"What happens if that file gets damaged" quotes the first
   sentence of the message only, where the block above it quotes the whole of one.
