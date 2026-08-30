# Plan — BUG-0001 A filesystem error on the deck file surfaces as a traceback, not a message

## Problem

`recall` catches one deck-file failure — the file is present and its contents are not a deck — and
lets every other one out of `main` as a Python traceback [src: BUG-0001; recall/cli.py]. Three
conditions demonstrate it: a deck directory that cannot be written, a directory sitting at the
deck's path, and a file sitting where the deck's directory belongs. The third is the one that
fails quietly — `recall list` reports an empty deck and exits 0, because `store.load` reads
`NotADirectoryError` as "no deck yet" [src: recall/store.py; BUG-0001]. For whom: the person at
the terminal, who is told either nothing they can act on or something untrue, at the moment they
most need to be told which file to go and look at. The constraints are already fixed and this
change works inside all of them: `store.py` never prints, `cli.py` owns every message
[src: docs/architecture/overview.md]; a deck that cannot be read is never repaired
[src: ADR-0004]; an absent deck and a missing parent directory are still an empty deck
[src: ADR-0004]; and nothing about the deck's format moves.

## Approach

`store.py` classifies the refusal, `cli.py` reports it — the split ADR-0010 records, chosen over
having `cli` catch `OSError` itself because only `store` knows that a write goes through a
temporary file and only `store` already owns the question of which errors mean "no deck yet"
[src: ADR-0010].

`store` grows a three-member exception family: a `DeckError` base carrying `path` and `detail`,
the existing `DeckUnreadable` unchanged beneath it, and a new `DeckInaccessible` for an operating
system refusal. Both boundaries — `load`'s single read and `save`'s whole write sequence — turn an
escaping `OSError` into a `DeckInaccessible` whose `path` is always the deck file and whose
`detail` names the obstruction where there is one. `load` narrows its absent-deck catch from
`(FileNotFoundError, NotADirectoryError)` to `FileNotFoundError` alone, which is what makes
reproduction C's `list` stop lying [src: ADR-0010].

`cli` changes at seven points and gains one function. The four `except store.DeckUnreadable`
clauses become `except store.DeckError`, and `_report_unreadable` is **not touched** — that is
what keeps the six content messages and their exit code identical by construction rather than by
retesting [src: BUG-0001 AC6]. The three `store.save` calls gain an `except
store.DeckInaccessible` around them and a new `_report_unwritable`, which says the deck could not
be written and names the deck file. Both reports exit `3`; the constant is renamed to
`EXIT_DECK_UNUSABLE` to say what it now covers, and its value does not move [src: ADR-0010].

Interfaces this fixes, so the developer does not have to invent them:

- `store.DeckError(Exception)` — `__init__(self, path, detail)`, sets `self.path` to a
  `pathlib.Path` and `self.detail` to a string, and formats `str()` as `f"{path}: {detail}"`.
  `DeckUnreadable(DeckError)` and `DeckInaccessible(DeckError)` add nothing.
- `store._obstruction(directory)` → `pathlib.Path | None`. The shallowest ancestor of
  `directory`, or `directory` itself, that exists and is not a directory. Reads the filesystem;
  writes nothing; raises nothing.
- `store._refusal(path, exc)` → `str`. The `detail` for an `OSError` raised while using the deck
  at `path`. A fragment with no leading capital and no trailing full stop, matching the shape
  `DeckUnreadable`'s details already have.
- `cli._report_unwritable(inaccessible)` → `int`. Prints to standard error and returns
  `EXIT_DECK_UNUSABLE`.

## Steps

1. **`recall/store.py` — the exception family.** Add `class DeckError(Exception)` with the
   `__init__` above, and reduce `DeckUnreadable` to `class DeckUnreadable(DeckError)` with its
   docstring kept and its body replaced by `pass`. Add `class DeckInaccessible(DeckError)` with a
   docstring saying the operating system refused an operation on the deck file. *Afterwards:*
   `store.DeckUnreadable` is raised at every place it is raised today, with the same `path`,
   `detail` and `str()`; `except store.DeckError` catches both classes.

2. **`recall/store.py` — `_obstruction(directory)`.** Walk `directory`'s ancestors from the
   filesystem root downward and then `directory` itself, using `os.path.lexists` and
   `os.path.isdir`; return the first that exists and is not a directory, else `None`. *Afterwards:*
   for a home whose `.local/share/recall` is a regular file, `_obstruction` of the deck's parent
   returns that path; for a well-formed home it returns `None`; it never raises and never writes.

3. **`recall/store.py` — `_refusal(path, exc)`.** In this order: if `_obstruction(path.parent)`
   is not `None`, return a fragment naming that path and saying the deck's directory has to be a
   directory; else if `path` is a directory, return a fragment saying the deck's path is a
   directory rather than a file; else return `exc.strerror` lower-cased, falling back to the
   exception's class name when `strerror` is `None`. *Afterwards:* reproduction A yields
   `"permission denied"`, B yields the directory fragment, C yields the fragment naming
   `<home>/.local/share/recall`.

4. **`recall/store.py` — `load`.** Change `except (FileNotFoundError, NotADirectoryError)` to
   `except FileNotFoundError`, and add, immediately after it, `except OSError as exc: raise
   DeckInaccessible(path, _refusal(path, exc)) from exc`. Update the module docstring's sentence
   about `ADR-0004` §6 to say that only an absent file or an absent parent directory is an empty
   deck, and that anything else the operating system refuses is a `DeckInaccessible`.
   *Afterwards:* an absent deck and an absent parent still return an empty `Deck`; reproduction B
   and reproduction C's `list` raise `DeckInaccessible`; `load` still writes nothing on any path.

5. **`recall/store.py` — `save`.** Wrap the existing body — the `path.parent.mkdir`, the
   `mkstemp`, the write and the `os.replace`, including the `except BaseException` cleanup, which
   is kept exactly as it is — so that an `OSError` escaping it is re-raised as
   `DeckInaccessible(path, _refusal(path, exc))`. *Afterwards:* reproduction A and reproduction
   C's `add` raise `DeckInaccessible` naming the **deck** file rather than the temporary file, the
   temporary file is still removed on every failure, and the deck on disk is untouched.

6. **`recall/cli.py` — the four read sites.** In `cmd_add`, `cmd_list`, `cmd_review` and
   `cmd_delete`, change `except store.DeckUnreadable as unreadable` to `except store.DeckError as
   unreadable`. Leave `_report_unreadable` unmodified, including its wording and its return value.
   *Afterwards:* the six content cases produce byte-identical messages and the same exit code as
   before this item, and an operating-system refusal on the read side produces the same sentence
   with the new `detail` inside it.

7. **`recall/cli.py` — the three write sites and the new report.** Rename
   `EXIT_DECK_UNREADABLE` to `EXIT_DECK_UNUSABLE`, keeping the value `3`, and update its comment
   to say it covers a deck file that could not be used in either direction [src: ADR-0010]. Add
   `_report_unwritable(inaccessible)`, printing to standard error a message that names
   `inaccessible.path`, says the deck could not be written, gives `inaccessible.detail`, and says
   nothing was written and the file is exactly as it was before this attempt; it returns
   `EXIT_DECK_UNUSABLE`. Wrap each of the three `store.save(...)` calls — one in `cmd_add`, one
   inside `cmd_review`'s per-card loop, one in `cmd_delete` — in `try` / `except
   store.DeckInaccessible as inaccessible: return _report_unwritable(inaccessible)`. *Afterwards:*
   no subcommand can leave an `OSError` on the deck file uncaught, and a sitting whose save is
   refused stops there with a message, keeping every answer it had already written.

8. **`tests/test_deck_file_errors.py` — the three reproductions.** A new module built on
   `tests.support`, one test per reproduction, each driving `bin/recall` as a subprocess:
   - `test_unwritable_deck_directory_is_refused` — reproduction A: create the deck's directory,
     `chmod 0o500`, restore the mode with `addCleanup` so the temporary home can be removed, run
     `recall add`. Asserts a non-zero exit, `str(self.deck_file)` in standard error, `".tmp"` not
     in either stream, and `"Traceback"` in neither stream. Guarded by
     `if os.geteuid() == 0: self.skipTest(...)`, per ## Assumptions 3.
   - `test_directory_at_the_deck_path_is_refused` — reproduction B: `self.deck_file.mkdir(parents=True)`,
     run `recall list`. Same three assertions.
   - `test_file_where_the_deck_directory_belongs_is_refused` — reproduction C: write a regular
     file at `self.home / ".local" / "share" / "recall"`, then run **both** `recall list` and
     `recall add`. Asserts a non-zero exit from each, and that each names that obstructing path in
     standard error.

   Every one of the three captures `support.tree(self.home)` and a `support.digest` for each file
   in it before and after, and asserts both are identical afterwards.

9. **`tests/test_deck_file_errors.py` — the six content cases.** One test that walks the six
   malformed decks `WI-0001` AC8 covers — truncated JSON, text that is not JSON, JSON that is not
   an object, an object with no `cards` array, a card missing a field, and an empty file — as
   subtests, running `recall add` and `recall list` against each. Asserts a non-zero exit, the
   deck path in standard error, and the detail substring the existing code produces for that case
   (`"not valid JSON"`, `"not a JSON object"` for the top level, `"no 'cards' array"`,
   `"has no 'question'"`). *Afterwards:* AC6 is decided by running the suite rather than by
   reading the diff.

10. **`docs/process/using-recall.md`.** Extend *"What happens if that file gets damaged"* with the
    case where the operating system refuses the file rather than the file being malformed: that
    `recall` names the deck file, says whether it could not be read or could not be written, names
    what is in the way when something is, writes nothing and exits non-zero; and that a file
    sitting where `~/.local/share/recall` belongs is reported rather than reported as an empty
    deck. Bump to version 8 with a change-log row.

11. **`docs/architecture/overview.md`.** In the `store.py` bullet, record that `store` also
    classifies an operating-system refusal on the deck file and raises it as a deck-level
    exception, so `cli` catches `store.DeckError` and never reads `errno` or an exception's
    filename; and that absent, unreadable and inaccessible are three distinct outcomes rather than
    two. Bump to version 8 with a change-log row.

12. **Run the gates and record the mutation.** Run `python3 -m compileall -q recall tests` and
    `python3 -m unittest discover -s tests -t . -q`; all 55 existing tests plus the new ones must
    pass. Then, for AC5, remove each piece of handling in turn — step 4's `except OSError` clause,
    step 4's narrowing of the absent catch, step 5's wrapper, step 7's `except
    store.DeckInaccessible` clauses — re-run the suite, and record in `impl-report.md` which tests
    fail for each. Restore the code afterwards and re-run to confirm the suite is green again.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — reproduction A names the deck file, not the temporary file, says it could not be written, exits non-zero, no traceback | 3, 5, 7 | `test_unwritable_deck_directory_is_refused`: exit non-zero, `str(deck_file)` in stderr, `".tmp"` absent from both streams, `"Traceback"` absent from both streams |
| AC2 — reproduction B names the deck file, says it could not be read, exits non-zero, no traceback | 3, 4, 6 | `test_directory_at_the_deck_path_is_refused`: exit non-zero, `str(deck_file)` and `"cannot read"` in stderr, `"Traceback"` absent from both streams |
| AC3 — reproduction C exits non-zero from **both** `list` and `add`, and the message names the path in the way | 2, 3, 4, 5, 6, 7 | `test_file_where_the_deck_directory_belongs_is_refused`: two invocations, each non-zero, each with `str(home / ".local/share/recall")` in stderr |
| AC4 — in all three cases nothing under the deck's directory is created, modified or removed | 4, 5 | all three tests above: `support.tree(home)` equal before and after, and `support.digest` equal for every file in it |
| AC5 — a regression test covers all three reproductions and fails if the handling is removed | 8, 12 | the mutation table in `impl-report.md`, naming which of the three tests fail with each of the four pieces of handling removed |
| AC6 — the six content cases still refuse with their existing messages | 6, 9 | `_report_unreadable` and `DeckUnreadable`'s details are unmodified (readable in the diff), and the six-case subtest asserts each existing detail substring and a non-zero exit for `add` and `list` |

## Assumptions

1. **The wording of both messages is not fixed by any criterion.** AC1, AC2 and AC3 name what must
   appear — the deck file, the path in the way, "could not be written", "could not be read" — and
   the tests assert those substrings rather than whole sentences, as every earlier item's tests do
   [src: tracker/items/WI-0001/artifacts/plan.md]. *Reversing:* one format string in `cli.py` and
   the substrings in one test module; no ADR and no document quotes the new sentence except
   `using-recall.md`, which cites it.
2. **`_refusal` falls back to the operating system's own words** (`exc.strerror`, lower-cased) for
   anything outside the two shapes step 3 names. This is a deliberate default rather than an
   enumeration: the set of `OSError`s a filesystem can raise is open, and a fragment like
   `"no space left on device"` is more use to a person than a generic sentence. *Reversing:* one
   `return` in one function; no criterion names a `strerror` string, and the only thing they
   require of it is that no traceback appears.
3. **Reproduction A's test skips when the process runs as root**, where mode `0o500` does not
   prevent writing and the reproduction does not reproduce. This project's suite runs as an
   unprivileged user (`id -u` → `1000`), so the test runs here. *Reversing:* delete the guard;
   recorded again under ## Risks because it is the one place a green suite could mean less than it
   appears to.
4. **A refused save inside a sitting ends the sitting with the message and a non-zero exit**, and
   the answers already saved for earlier cards stay saved. No criterion on this item covers
   `review`, but `cmd_review` calls `save` and so must catch, and stopping is the only option
   consistent with `WI-0002` AC9's guarantee that a part-way sitting keeps what it recorded
   [src: recall/cli.py]. *Reversing:* one branch in `cmd_review`.
5. **The six content cases are exactly the six `WI-0001` AC8 names**, and their existing detail
   substrings are the ones `store._card_from` and `load` produce today [src: recall/store.py].
   *Reversing:* the substrings in one test.

## Decisions and ADRs

| decision | where it is recorded | branch of the preference order |
|----------|----------------------|-------------------------------|
| `store` wraps `OSError` rather than `cli` catching it; a `DeckError` base with `DeckUnreadable` and a new `DeckInaccessible` beneath it | `ADR-0010` §1, §2, and its options list | asked of the documents, then decided — `BUG-0001`'s ## Notes routed it here explicitly |
| `load` treats `FileNotFoundError` alone as absence, so reproduction C stops reporting an empty deck | `ADR-0010` §4 | documented — `ADR-0004` §6 names a missing file and a missing parent directory, and neither is `NotADirectoryError` |
| `detail` names the obstructing path when there is one, otherwise the deck's own path and the operating system's words | `ADR-0010` §3 | documented — `BUG-0001` AC3 requires the path in the way to be named |
| Exit code `3` covers both a refused read and a refused write; no fourth code is minted | `ADR-0010` §5 | decided — an exit code is observable and the plan states the reversal cost |
| `_report_unreadable` is not modified, so the six content messages are preserved by construction | this plan, steps 6 and 9 | documented — `BUG-0001` AC6 |
| The two message wordings, the `strerror` fallback, the root guard, and a sitting's behaviour on a refused save | ## Assumptions 1–5 above | assumed, each with its reversal cost |

## Scaffolding

None. This plan creates no file outside `tracker/` and `docs/`; `tests/` already exists with an
`__init__.py`, and both declared commands run today
(`python3 -m unittest discover -s tests -t . -q` → `Ran 55 tests … OK`).

## Risks

- **Running as root would make reproduction A unreproducible.** Mode bits do not restrain a
  privileged process, so the test would skip and AC5's demonstration would rest on two
  reproductions rather than three. Checked rather than assumed: this project's tests run as uid
  `1000`. If a future runner is root, the skip is visible in the suite's output rather than silent.
- **Narrowing `load`'s absent catch touches criteria three items depend on.** `WI-0001` AC5 and
  AC6 and `WI-0002` AC6 all rest on an absent deck loading as an empty one. They are safe because
  a missing file and a missing parent directory both raise `FileNotFoundError` — but that is the
  claim this step lives or dies by, and step 12 re-runs the whole suite, including
  `test_absent_file_loads_as_an_empty_deck` and `test_first_run_creates_storage`, precisely to
  check it.
- **`_obstruction` reads the filesystem while an error is being reported**, and those reads can
  themselves be refused. It is specified to return `None` rather than raise, so the worst case is
  a less specific message, never a second traceback on the way out of the first.
- **Wrapping `save`'s whole body catches more than the three reproductions.** An `ENOSPC` during
  `json.dump`, or a refused `os.fsync`, now becomes a `DeckInaccessible` rather than a traceback.
  That is intended, and `## Assumptions` 2 is what makes the message for it readable; the risk is
  that a genuine programming error inside `save` that happens to be an `OSError` would be reported
  as a deck problem. Nothing in `save` raises `OSError` for a non-filesystem reason today.
- **This item has no `refinement-qa.md`.** It was filed at `ready` by `verify`, which the pipeline
  allows for a bug with reproduction steps, so there is no recorded Q&A behind its criteria and no
  `[assumed]` or `[unresolved]` entries to design around. The criteria and the three reproductions
  in `item.md` are the whole of the contract.

## Out of scope for this item

- The newline-in-a-question-side observation recorded against `WI-0001`, which belongs to whoever
  refines a criterion that parses `list` output [src: BUG-0001].
- Relocating the deck — a flag, an environment variable or a configuration file [src: ADR-0004].
- Repairing, retrying, moving aside or creating anything in order to clear an obstruction.
  `recall` reports and stops [src: ADR-0004].
- Two `recall` processes running at once. Nothing in this epic has verified concurrent use, and
  this item does not change that either way.
- Any change to the deck's format or to `DECK_FORMAT_VERSION` [src: ADR-0004].
