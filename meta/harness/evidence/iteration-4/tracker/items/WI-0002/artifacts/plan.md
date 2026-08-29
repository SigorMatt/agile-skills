# Plan — WI-0002 Review the cards that are due and record each answer

## Problem

Someone with a pile of cards needs a day's review to be finite: they run one command, are shown
only the cards that are due, see each question side, ask for the answer, and say whether they got
it right — and tomorrow the tool still knows what they said. This item delivers one command,
`recall review`, and the per-card state a review writes. It does **not** decide when a card comes
back; the ladder is WI-0003's, and this item writes a placeholder next-due date that WI-0003
replaces [src: WI-0003 AC2]. The constraints are already fixed: a command-line tool over one flat
pool [src: EP-001], the key map Enter / `y` / `n` / `q` [src: WI-0002/Q-001], one JSON store at
`~/.recall.json` or `RECALL_FILE` [src: ADR-0002], and the schema and write protocol of
[src: ADR-0004]. The unusual constraint on this item is that it is interactive and `verify` has
no hands: every criterion must be settled by a piped command with nobody at the keyboard
[src: WI-0002 AC9].

## Approach

Everything lands in the two files WI-0001 delivered, plus one new test module.

**One module, still.** `docs/architecture/overview.md` v1 asked to revisit at this item whether
the store should move into its own module now that a third command exists. It should not:
`recall.py` reaches roughly 280 lines with this change, one reader holds it, and the store layer
is already separated *within* the file by the contract WI-0001 fixed. Splitting it now would add
an import graph and a second file to keep in step for no reader's benefit. Recorded as
assumption 6 below with what reversal costs, and answered in the overview's v2 rather than left
hanging.

**Three new layers of behaviour**, each in `recall.py` and each with a contract this plan fixes:

| function | contract |
|----------|----------|
| `today()` | Returns today's local date as a `YYYY-MM-DD` string. One call site per command, so the whole of a run sees one date [src: ADR-0006]. |
| `due_cards(document, today)` | Returns the cards whose `due` is missing, or is a string less than or equal to `today`, sorted by `due` ascending then `number` ascending. A missing `due` sorts as the empty string, which is less than any date, so a never-scheduled card comes before every dated one — and ties break on `number` [src: WI-0002 AC8]. Does not touch the disk. |
| `record_result(card, right, today)` | Sets `card["result"]` to `"right"` or `"wrong"` and `card["due"]` to the day after `today`. Does not touch the disk [src: ADR-0006]. |
| `read_line(stream)` | Returns the next line from `stream` stripped of its trailing newline, or `None` at end of input. `""` (the reviewer pressed Enter) and `None` (input ended) are different values, and every caller must treat them differently [src: WI-0002 AC9]. |
| `cmd_review(arguments)` | The session. Takes exactly zero positional arguments. Returns 0, 1 or 2 [src: ADR-0005]. |

`read_line` is the one piece of this that is easy to get wrong, so the contract is explicit:
`input()` cannot be used, because it raises at end of input and returns the same empty string for
a blank line either way. `stream.readline()` returns `""` only at end of input and `"\n"` for a
blank line, which is exactly the distinction AC9 turns on.

**The session loop**, stated as behaviour rather than as code. `cmd_review` loads the document,
takes `due_cards`, and for each card in order:

1. prints the question side, then the reveal prompt;
2. reads lines until it gets one it recognises — an empty line reveals, `q` ends the session, and
   anything else is ignored and the prompt is printed again [src: WI-0002 AC10]; end of input
   ends the session [src: WI-0002 AC9];
3. prints the answer side, then the grade prompt;
4. reads lines until it gets `y`, `n` or `q`, ignoring anything else and reprinting the prompt;
   `q` and end of input end the session **without** recording a result for this card
   [src: WI-0002 AC5];
5. on `y` or `n`, calls `record_result` and **saves the whole document immediately**, before the
   next card [src: ADR-0006].

When the loop ends — because the due cards ran out, or because of `q`, or because input ended —
it prints the summary line and returns 0. If no card was due at all, it prints the nothing-due
line instead and returns 0, and prints no summary [src: WI-0002 AC3].

**The output contract.** The exact wording is the developer's to place; the shape, the stream and
the order are not. `refine` left the wording deliberately unconstrained [src: WI-0002].

| situation | stream | shape | exit |
|-----------|--------|-------|------|
| a card is presented | stdout | the question side on a line of its own, then a prompt naming Enter and `q` | — |
| the answer is revealed | stdout | the answer side on a line of its own, then a prompt naming `y`, `n` and `q` | — |
| a line that is not expected here | stdout | the same prompt again; nothing else, and nothing on stderr | — |
| the session ends, having presented at least one card | stdout | one line, the last on stdout, containing the number reviewed and the number right | 0 |
| nothing is due | stdout | one line saying nothing is due, and nothing else at all | 0 |
| `recall review` with any argument | stderr | `usage: recall review` | 2 |
| the store cannot be read or written | stderr | the existing store messages | 1 |

No prompt may contain the answer side's text before the reveal, which is what AC1 checks by the
order of four strings in the output. The summary line must be last on stdout, which is what AC6
checks.

**Storage.** ADR-0006 fixes it: `due` and `result` on each card, `version: 2` on write, versions
1 and 2 accepted on read, and a review writes the day after today into `due` as a placeholder for
WI-0003's ladder.

## Steps

1. **Extend the store layer's schema handling in `recall.py`.** Raise `STORE_VERSION` to 2. In
   `load`, after the existing shape checks, refuse a document whose `version` is neither 1 nor 2,
   through the existing `_unreadable` path so the message and exit code are the ones ADR-0004
   already fixed; and validate `due` and `result` when they are present — `due` a string,
   `result` one of `"right"`, `"wrong"` or `null` — naming the card and the field, in the style
   `load` already uses. Afterwards: a version-1 document from WI-0001 loads unchanged, a
   document with `"version": 3` makes both `recall list` and `recall review` exit 1 leaving the
   file untouched, and a card with `"result": "maybe"` does the same.

2. **Add `today()` and give `add_card` the two new fields** in `recall.py`. `add_card` sets
   `due` to `today()` and `result` to `None` on the card it appends. Afterwards:
   `recall add "a" "b"` against an empty store writes a card carrying `number`, `question`,
   `answer`, `due` — today's date — and `result: null`, and the document says `"version": 2`.

3. **Add `due_cards(document, today)` and `record_result(card, right, today)`** to the store
   layer in `recall.py`, to the contracts in `## Approach`. Neither touches the disk.
   Afterwards: importing `recall` and calling `due_cards` on a hand-built document returns the
   cards whose `due` is missing or not after the given date, in `due` then `number` order.

4. **Add `read_line(stream)`** to `recall.py`, to the contract in `## Approach`. Afterwards:
   calling it on a `StringIO` of `"\ny\n"` returns `""`, then `"y"`, then `None`.

5. **Add `cmd_review(arguments)`** to the command layer in `recall.py` and dispatch `review` to
   it from `main`, following the session loop and the output contract in `## Approach`.
   Afterwards: `printf '\ny\n\nn\n' | recall review` over two due cards presents both, records
   both, prints a summary line last and exits 0; `recall review --deck german` exits 2 with
   `usage: recall review` on stderr and changes nothing.

6. **Update `README.md`.** Move `recall review` out of "Not yet built" into `## Commands` with
   the key map and a worked example; extend the store example to the version-2 shape; and add a
   short section naming the `due` and `result` fields and stating what `"right"`, `"wrong"` and
   `null` mean — AC2 requires the field and its two values to be documented there
   [src: WI-0002 AC2], and AC8 requires a checker to know which field to hand-edit
   [src: WI-0002 AC8]. Afterwards: `grep -e 'due' -e 'result' README.md` finds the section.

7. **Harden `tests/support.py`.** Set `HOME` in `run_recall` unconditionally — to a directory
   inside the per-test temporary directory when the caller does not name one — so that no test,
   and no mutation of path resolution applied to this suite, can resolve the store to the
   checker's real home directory. This step maps to no acceptance criterion and is here for one
   reason: WI-0001's review accepted exactly this as a gap and recorded that WI-0002 and WI-0003
   inherit the suite [src: WI-0001]. Afterwards: the existing 21 tests still pass, and a test
   that omits `store=` and `home=` writes nothing under the real `$HOME`.

8. **Write `tests/test_review.py`.** Subprocess cases against the executable, driven by piped
   input, one per criterion: a two-card session presents both sides in order and exits 0 (AC1);
   the store afterwards holds differing records for the `y` card and the `n` card (AC2); an
   empty store and a just-emptied store each print one line and exit 0 (AC3); a second run the
   same day presents nothing (AC4); `q` at the question side and `q` at the answer side each end
   the session leaving the unreached cards due (AC5); the last line of stdout carries both
   numbers for a full session and for a `q` session (AC6); three due cards are all presented in
   one session and `--deck german` is rejected (AC7); hand-set `due` dates produce the
   oldest-first order and the same order twice (AC8); input ending mid-session ends it like `q`
   (AC9); an unrecognised line at either moment is ignored (AC10).

9. **Extend `tests/test_store.py` and `tests/test_docs.py`.** In `test_store.py`: a version-1
   document is read and is upgraded to version 2 by the next write, a version-3 document is
   refused with exit 1 and left byte-identical, and a newly added card carries today's date and
   a null result. In `test_docs.py`: `README.md` names `due`, `result`, `right` and `wrong`.

10. **Run both gate commands from the repository root** — `python3 -m unittest discover -s tests
    -t .` and `python3 -m compileall -q -x '[.]claude' .` — and report their output in the
    implementation report [src: ADR-0003].

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — a session presents due cards one at a time, question side before answer side | 2, 3, 4, 5 | `tests/test_review.py`: two cards added, `printf '\ny\n\nn\n'` piped in, and the stdout checked for the index of `die Katze` < `the cat` < `der Hund`, with `the cat` absent from the output produced before the first empty line was consumed |
| AC2 — `y`/`n` recorded, and the two records differ in the store | 1, 2, 3, 5 | `tests/test_review.py`: after that session, the store is parsed and card 1's `result` is `"right"` while card 2's is `"wrong"`; `tests/test_docs.py`: `README.md` contains `result`, `right` and `wrong` |
| AC3 — nothing due prints one line, presents no card, exits 0 | 3, 5 | `tests/test_review.py`: `recall review` against a store with no cards, and again immediately after a session that reviewed every due card — each asserts exactly one line on stdout, empty stderr, exit 0 |
| AC4 — a card reviewed today is not presented again today | 3, 5 | `tests/test_review.py`: after the AC2 session, a fresh `recall review` produces the same single nothing-due line and neither card's text appears in it |
| AC5 — `q` at either moment ends the session, keeping recorded results and leaving the rest due | 3, 5 | `tests/test_review.py`: three cards; `printf '\ny\nq\n'` then a following `recall review` presenting cards 2 and 3 and not card 1; and from the same starting state `printf '\ny\n\nq\n'`, after which card 2 is still due and its `result` is still `null` |
| AC6 — the last line of stdout carries the reviewed count and the right count | 5 | `tests/test_review.py`: `stdout.splitlines()[-1]` of the AC2 session contains `2` and `1`, and of the first AC5 session contains `1` and `1` |
| AC7 — every due card in one session; no deck, tag or filter argument | 3, 5 | `tests/test_review.py`: three due cards presented in one uninterrupted session; and `recall review --deck german` exiting 2 with `usage` on stderr, followed by a session that still presents all three |
| AC8 — oldest-due-first, ties by card number, stable across runs | 3, 5 | `tests/test_review.py`: three cards whose stored `due` is set by hand to two days ago (card 3) and yesterday (cards 1 and 2); the presentation order is 3, 1, 2; the store file is restored from a copy and a second run gives the same order |
| AC9 — drivable from a pipe; input ending mid-session ends it like `q` | 4, 5 | `tests/test_review.py`: every case in this module is piped, so the whole module is the first half; and `printf '\ny\n'` over two due cards asserting card 1 recorded, card 2 still `null` and still due, the summary line present, exit 0 |
| AC10 — an unexpected line is ignored and the prompt repeats | 5 | `tests/test_review.py`: one due card and `printf 'x\n\nz\ny\n'`, asserting exit 0, `result` `"right"`, the last line carrying `1` and `1`, and the reveal prompt appearing twice in stdout |

## Assumptions

1. **`due` is a local calendar date, `YYYY-MM-DD`, with no time and no timezone.** ADR-0001 fixes
   due-ness by date rather than clock time; this is the smallest thing that carries it and it
   sorts correctly as a string. Reversing: the format string in `today()`, the comparison in
   `due_cards`, and a migration for stored cards. Cheap today — no card carries a `due` yet — and
   medium once they do, which is why it is in ADR-0006 as well.
2. **A card whose `due` is missing is due.** This is what makes a version-1 store from WI-0001
   work unchanged, and it agrees with ADR-0001's "a newly added card is due the day it is added".
   Reversing: one condition in `due_cards`.
3. **The reviewer's line is compared after stripping the trailing newline and nothing else** — no
   trimming of surrounding spaces, no case folding. So ` y` and `Y` are unrecognised lines and
   AC10 ignores them. Chosen because AC10 says "not one of the keys expected", and accepting
   variants is behaviour nobody asked for. Reversing: one normalising call in `cmd_review`.
4. **The summary line is printed whenever at least one card was presented**, including a session
   ended by `q` before any result was recorded — it then reports zero reviewed. AC6 requires the
   line after a `q` session and does not say the count must be non-zero. Reversing: one
   condition.
5. **The wording of every prompt and line is the developer's**, required only to exist, to name
   the right keys, and to carry the right numbers [src: WI-0002]. Reversing: string constants in
   one file and the tests that assert on them.
6. **The store layer stays inside `recall.py`.** The overview asked for this to be revisited at
   this item; the answer is no, at roughly 280 lines and one reader. Reversing: move six
   functions into `store.py` and add one import — no stored data changes and no criterion moves.
7. **No injectable clock.** No criterion of this item needs "today" to be something other than
   today: AC8 produces past due dates by editing the file, not by moving the clock. WI-0003 may
   well need one; deciding it here would be designing past this item. Reversing: give `today()` a
   parameter and thread it through three call sites.

## Decisions and ADRs

| decision | where | branch of the preference order |
|----------|-------|-------------------------------|
| What a review stores on a card, the version-2 schema, the read rule for version 1, the day-after placeholder, and saving after each card | ADR-0006 | decided here — WI-0002's criteria force per-card state that no document had allocated |
| The store's location, format, write protocol, creation rule and failure cases | ADR-0002, ADR-0004, already recorded | answered from the documents |
| The interval ladder, due-ness by date, a new card due the day it is added | ADR-0001, already recorded | answered from the documents |
| Entry point, positional-only arguments, exit codes, streams | ADR-0005, already recorded | answered from the documents |
| The key map, the pipe-drivability requirement, ignoring an unexpected key, end of input ending the session | WI-0002 AC1–AC10, already recorded | answered from the item — `refine` settled all of it, `Q-001` with the stakeholder and the rest under their standing deferral |
| Keeping the store layer in `recall.py`; the date format; the missing-`due` rule; line comparison; the summary after a bare `q`; prompt wording; no injectable clock | `## Assumptions` above | reversible assumptions |

Nothing in this plan was asked of the stakeholder. Everything open at the start of it was either
settled in a document already, or was one of the three questions `refine` routed to `plan` in the
item's `## Notes`, or is a reversible assumption recorded above.

**The one place this plan touches a recorded decision**, stated here as well as in ADR-0006 so
that a reviewer does not have to find it: ADR-0004 predicted that WI-0003 would add the
scheduling fields and bump the store's version. WI-0002's criteria require persisted per-card
state, so it happens here instead. ADR-0006 uses ADR-0004's `version` seam exactly as designed
and changes none of its decisions, so it is recorded as a new ADR rather than as a supersession,
and the reasoning is written into ADR-0006's `## Context` where a later reader will meet it.

## Scaffolding

`none`. Every file this plan creates or edits outside `tracker/` and `docs/` is product code,
documentation or a test, and each is written by `implement`.

## Risks

- **The session's correctness lives in a loop that reads a stream, and the tests drive it through
  a pipe only.** Nothing in this item is ever exercised with a real terminal, by design
  [src: WI-0002]. If a person's terminal buffers differently from a pipe — no output flushing
  between the prompt and the read, say — every test passes and the tool is unusable at a
  keyboard. The developer should print prompts on their own lines and not rely on partial-line
  output.
- **A session that crosses local midnight sees two dates.** `today()` is called once per command
  in this design, which bounds it: a session started before midnight records the day after the
  date it started with. A test that adds a card and reviews it within one second of midnight
  could still see the card become due again. Nothing here defends against it and no criterion
  asks; it is recorded so a future flake is recognised rather than re-diagnosed.
- **`due` is a bare local date** [src: ADR-0006]. Correct for one person on one machine, which is
  what the epic scopes [src: EP-001]; wrong the moment the store moves between timezones, which
  the epic excludes.
- **The placeholder next-due rule is knowingly wrong for a right answer** until WI-0003 lands
  [src: WI-0003 AC2]. Between this item and that one, a card answered right comes back tomorrow.
  It is recorded in ADR-0006 and in the item, and it is the thing most likely to be read as a
  defect by someone who meets the tool in between.
- **Saving after every card multiplies whole-document rewrites by the size of the session.** Fine
  for one person's vocabulary and already the accepted cost of ADR-0004's protocol; it is the
  first thing that would have to change at a scale nobody in this epic has asked for.

## Out of scope for this item

- Computing when a reviewed card is next due: the ladder, the rung, and the fields that carry
  them are WI-0003's [src: WI-0003 AC2; src: WI-0003 AC3].
- Anything requiring standard input to be a terminal — raw single-keypress reading, screen
  clearing, cursor control, colour [src: WI-0002].
- Any command or output that shows a card's recorded results back to the reviewer
  [src: WI-0002].
- Editing or deleting a card, undoing a grade, forcing or shuffling a session, and any grade
  finer than right or wrong [src: WI-0002; src: EP-001].
- Any migration tooling. A version-1 store is upgraded in place by the next write and there is
  no separate command to run [src: ADR-0006].
