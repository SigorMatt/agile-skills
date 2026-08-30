# Implementation report — WI-0004

Branch `wi/WI-0004`, branched from `main` at `152c531`. Two commits: `6aabe6f` (code and tests)
and `1d46cae` (documentation). Every gate below was run on the branch head, `1d46cae`.

## What was built

`recall delete --question "<the question side>"`, the fourth subcommand, built as `plan.md`'s ten
steps describe and in that order.

- **`recall/deck.py`** — `positions_matching(deck, question)` returns the positions, in deck
  order, of every card whose stored `question` equals the given string by plain `==`: no folding,
  no stripping, no substring test. It is the counterpart of `due_positions` — it selects and
  decides nothing — and it returns every match because the count is the answer (none is AC4, one
  is AC1, two or more is AC5). `Deck.remove(position)` deletes the card and closes the gap; its
  docstring records what it must not do — it constructs no `Card`, which is why AC11 holds by
  construction — and the constraint that a caller must not reload the deck between the match and
  the removal, which `plan.md`'s risk list asked to be written down in the code.
- **`recall/store.py`** — untouched, exactly as the plan says. A deletion is load, remove, save;
  atomic writes, never repairing an unreadable deck and absent-is-empty are already `ADR-0004`'s.
- **`recall/cli.py`** — the `delete` subparser with one option, `--question`, defaulted to `None`
  rather than `required` so `cmd_delete` issues the refusal itself; two message constants
  (`DELETE_PROMPT`, ending in `[y/n]`, and `NOT_DELETED_MESSAGE`) plus `CONFIRM_RESPONSE`; and
  `cmd_delete` with the plan's five moves in order — blank check before the deck file is opened,
  the single `DeckUnreadable` site, zero matches refused, two-or-more refused, then both sides
  printed and one read through `_read_line`. No new exit code: `EXIT_REFUSED` and
  `EXIT_DECK_UNREADABLE` already carry the distinction. `cmd_list` was not edited.
- **`tests/test_delete.py`** — twelve tests, one per criterion, each running `bin/recall` as a
  child process with `HOME` in a temporary directory.
- **`docs/process/using-recall.md` v6** and **`docs/architecture/overview.md` v6** — below.

## Acceptance criteria evidence

Every test named below is in `tests/test_delete.py` and is run by
`python3 -m unittest discover -s tests -t . -q` (55 tests, OK).

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `cmd_delete` prints `card.question` then the indented `card.answer`, reads one line, and removes on a yes | `DeleteTests.test_deletes_the_named_card` — three added cards, `delete --question "der Hund"` with `y`; asserts exit 0, both sides on stdout **before** the `[y/n]` marker, and `recall list` afterwards showing two cards with `der Hund` absent and the other two sides intact |
| AC2 | `store.save` writes the whole deck before the process returns | `test_deletion_survives_the_process_ending` — the listing is a second `recall` child process sharing nothing with the first but the deck file; asserts the deleted question absent and the other two present |
| AC3 | the card is gone from the deck, so `due_positions` cannot select it | `test_deleted_card_is_never_reviewed` — a written deck with X due today, Y due in 7 days, Z due today; deletes X then Y; `recall review` driven by `"\ny\n"` asserts `Z question` on stdout, `X question` and `Y question` absent, exit 0 |
| AC4 | `positions_matching` returns `()`; refused before any prompt or write | `test_no_such_card_is_refused` — asserts non-zero exit, the typed string in stderr, no `[y/n]` on stdout, neither answer side on stdout, and `digest(deck_file)` identical before and after |
| AC5 | `len(positions) > 1` refused, with the count in the message | `test_two_matching_cards_are_refused` — a duplicated question built by two `recall add` runs (WI-0001 AC9); asserts non-zero, `"2"` in stderr, no prompt, digest identical, and both cards still listed |
| AC6 | anything but a stripped, case-folded `y` — including `None` from end of input — prints `NOT_DELETED_MESSAGE` and returns 0, having written nothing | `test_anything_but_yes_cancels` — four sub-tests: `n`, `maybe`, an empty line, and closed standard input; each asserts exit 0, `Not deleted` on stdout, no `Traceback` in stderr, **exactly one** occurrence of `[y/n]` (the prompt is not re-asked), digest identical, and both cards still listed |
| AC7 | the blank check precedes `store.deck_path()` | `test_missing_or_blank_question_is_refused` — four cases (omitted, `""`, spaces, tabs) against a deck: non-zero, `--question` in stderr, no prompt, digest identical; then the same four with the deck file deleted, asserting it is still absent |
| AC8 | `DeckUnreadable` caught at `_report_unreadable`, before the match and the prompt | `test_unreadable_deck_is_refused_not_repaired` — deck file written as `not json at all`; asserts non-zero, the deck path in stderr, no prompt, digest identical |
| AC9 | an absent deck loads as an empty one, so this is AC4's branch, and nothing on it writes | `test_absent_deck_creates_nothing` — asserts non-zero, no prompt, deck file absent, its parent directory absent, and `tree(home) == set()` — the whole home directory is still empty |
| AC10 | `remove` leaves a `Deck` of length 0 and `save` writes a valid empty deck | `test_deleting_the_last_card_leaves_an_empty_deck` — after deleting the only card, `recall list` exits 0 with the `deck is empty` marker and no card lines, then `recall add` exits 0 and the new card is listed |
| AC11 | `Deck.remove` constructs no `Card` | `test_survivors_keep_their_schedules` — a written deck with rungs 0/2/3 and due dates −2/+5/+30 days; after deleting the middle card the parsed JSON is asserted field by field (`question`, `answer`, `rung`, `due`) against the bytes read before, plus `version` unchanged, no `grade` key gained, and the surviving order `["first", "third"]` |
| AC12 | `cmd_list` was not edited and no field was added to the deck file | `test_listing_is_unchanged_by_a_deletion` — after a deletion, `card_lines` equals exactly `["die Katze | the cat", "das Pferd | the horse"]`; each line matches `^[^|]+ \| [^|]+$`, none starts with a digit or a bracketed code, and no prompt text appears. AC10's test covers the empty-deck half. The reading of `WI-0001` AC3 and AC6 against this item's behaviour, which AC12 asks for, is `verify`'s to make; the executable case exists so the criterion's "waive it by name" branch is not needed |

**Would these fail if the behaviour were removed?** Two mutations were run against the branch and
then reverted, because two criteria are the kind that a test can appear to cover without
exercising:

- making the confirmation re-ask until it recognises the reply (a `while` loop around
  `_read_line`, the shape `ADR-0009` rejects) → `FAILED (failures=2)`, `AssertionError: 2 != 1`
  from AC6's "exactly one prompt" assertion;
- making `Deck.remove` rebuild the survivors at `FIRST_RUNG` → `FAILED (failures=1)` from AC11.

The remaining ten run the real binary against a subcommand that did not exist before this branch,
so removing the behaviour removes the subcommand and every one of them fails on exit code.

## Deviations from the plan

1. **Plan step 9 said "bump `docs/architecture/overview.md` to v5"; it was already at v5.** `plan`
   made that bump itself when it wrote the design, so the sentence step 9 asked for was already
   there — written as intent ("WI-0004 adds…", cited to `plan.md`). Rather than skip the step or
   re-do it, this execution did what `implement` did for WI-0003 at overview v4: bumped to **v6**
   and restated the two WI-0004 clauses as description of what is built, citing `recall/deck.py`
   and `recall/cli.py` alongside `ADR-0009` and `WI-0004/Q-002`. What the document says did not
   change; where it says it comes from did.
2. **Steps 6 and 7 landed in one commit with steps 1–5**, not as a separate test pass. The
   procedure requires the test to come with the change rather than in a cleanup pass, so the code
   and `tests/test_delete.py` are one commit (`6aabe6f`) and the documentation is the second
   (`1d46cae`). No step was skipped or reordered in substance.
3. **Two D12 repairs in `docs/process/using-recall.md` that no plan step named.** The damaged-deck
   paragraph said `add`, `list` and `review` refuse an unreadable deck — there are now four
   subcommands — and "What this version does not do yet" listed deleting a card as future work.
   Both sentences were made false by this item's own change, so leaving them was not an option;
   both are recorded in that file's change-log row for v6.

Nothing else departed from `plan.md`. All four of its `## Assumptions` were implemented as
written: the reply is stripped and case-folded, the card prints as question-then-indented-answer,
no new exit code was added, and `positions_matching` is used only by `delete`.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 55 tests … OK` (43 before this item, 12 added) |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, `6 item(s), 12 document(s), 0 errors, 0 warnings` |
| `every-criterion-has-a-test` | **pass** | the table above names a test function for each of AC1–AC12; no criterion is demonstrated by reading the code |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → exit 0, `all 2 commit(s) on main..wi/WI-0004 name WI-0004` |
| `no-unplanned-scope` (advisory) | **pass** | the diff is five files: `recall/deck.py` (steps 1–2), `recall/cli.py` (steps 3–5), `tests/test_delete.py` (steps 6–7), `docs/process/using-recall.md` (step 8 and deviation 3), `docs/architecture/overview.md` (step 9 and deviation 1). `recall/store.py`, `bin/recall` and the other test modules are untouched |
| `cross-answer-consistency` | **pass** | `lint-answers --changed-since main` → exit 0, `checked 9 consumed human answer(s)`, 0 errors |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0, `2 document(s) … differ from main`, 0 errors |

## What I did not do

- **BUG-0001 is untouched.** A filesystem error on the deck file that is not `DeckUnreadable` —
  a permission problem, a deck path that is a directory — still escapes as a traceback, and
  `cmd_delete` inherits that from the three subcommands that already had it. It is a separate
  `ready` item and `plan.md` names folding it in here as out of scope.
- **No near-miss help on a failed match.** `plan.md`'s risk list predicts that exact matching will
  be unhelpful the first time someone types a question with a trailing space they cannot see. The
  mitigation available inside this item is what was built: the refusal quotes back what was typed
  and tells them to type it as `recall list` shows it, and `docs/process/using-recall.md` says the
  same. Suggesting a near match is a product decision and belongs to the stakeholder.
- **`positions_matching` was not adopted by `add`, `list` or `review`.** `plan.md` `## Assumptions`
  4 forbids the refactor: rewriting delivered behaviour to share it would put three closed items
  back in play against criteria that never asked for it.
- **AC12's reading of `WI-0001` AC3 and AC6 is not asserted in this report as settled.** The
  criterion says it is settled by reading those two criteria's text against this item's behaviour,
  with the test suite as evidence rather than as the definition. The executable case exists
  (`test_listing_is_unchanged_by_a_deletion`), and the reading itself is `verify`'s to make and
  record.
