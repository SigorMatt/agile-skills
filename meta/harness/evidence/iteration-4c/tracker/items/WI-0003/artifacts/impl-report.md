# Implementation report — WI-0003

## What was built

One subcommand, in the module that already held the other two. `python3 -m recall delete <front>`
finds every card whose stored front side equals the argument exactly, shows what is about to be
lost, asks, and removes exactly the one chosen.

`recall/cli.py` gains five functions and two edits:

- `_rung(card)` — the rung as a person reads it: `"2 of 4"`, and `"0 of 4 (never answered)"` on the
  rung `add` writes for a new card.
- `_described(card, indent)` — one card as four labelled lines, the labels `ADR-0007`'s own, the
  values printed verbatim so the prompt and the file read alike.
- `_confirmed(cards, position)` — the single-match prompt. Returns the position to remove, or
  `None`.
- `_chosen_among(cards, positions)` — the several-match prompt: every match listed, numbered from 1
  in card-file order, each with its four lines. Returns the chosen position, or `None`.
- `delete(front)` — load, match into a list of positions, then one of three paths: refuse without
  prompting, ask about the one match, or ask which of several. On a chosen position: `del`, save,
  `Deleted: <front>`, exit 0.
- `_parser()` gains a `delete` subparser with one positional argument, `front`.
- `main()` becomes one explicit `if` per subcommand with no fall-through, ending in an
  `AssertionError` that argparse's `required=True` makes unreachable. That last line is the point:
  a subparser added without a handler now fails loudly instead of running whichever command the
  chain happened to end with — the trap `WI-0001`'s review recorded and `WI-0002` had to disarm.

**Positions, not cards, cross the prompt.** Two cards may share a front side (`WI-0001` AC6), so
`delete` computes `[index for index, card in enumerate(cards) if card.front == front]` and removes
one of those indices. Nothing between the match and the `del` re-searches by front, so the record
removed is the one that was displayed. This mirrors what `recall/schedule.py` already does for the
review session, and it is the only place in this item where a wrong answer would silently destroy
the wrong card.

**`_ask()` was reused unchanged, and that is what made AC7 nearly free.** It already re-asks by
reprinting the whole prompt string it was given, so putting the card block inside the prompt string
satisfies "reprint the card" with no new code. The one behavioural difference from `review`: `_ask`
returns `None` at the end of the input stream, and `delete` treats that as `n` where `review`
treats it as `q`. That is `WI-0003` AC7 and it is deliberate — stopping a review costs nothing,
while the act being confirmed here is irreversible by the stakeholder's own decision.

`recall/store.py` and `recall/schedule.py` were not touched. No new module. No file outside
`recall/`, `tests/` and `tracker/` was created or changed.

`tests/test_delete.py` is new: 30 test methods in 10 classes, one class per criterion group,
following `tests/test_review.py`'s harness exactly — a card file seeded by writing `ADR-0007`'s
format directly into a temporary directory, `RECALL_CARD_FILE` pointed at it, the tool run as a
subprocess with keystrokes on stdin, and the resulting file parsed by the test module's own reader
rather than by `recall.store`. Byte-identity is asserted by comparing raw bytes against a copy
taken before the run.

## Acceptance criteria evidence

Every row names test methods in `tests/test_delete.py`. None rests on reading the code.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — `delete <front>`, `y`, card removed, confirmation naming the front, exit 0 | `delete()`'s removal path: `del cards[chosen]`, `store.save`, `print("Deleted: …")`, `EXIT_OK` | `DeletingTests.test_a_confirmed_delete_removes_the_card_and_names_it` (asserts exit 0, `Deleted: bonjour` on stdout, and that only the other card remains); `DeletingTests.test_the_survivor_keeps_every_field` |
| AC2 — the card and its schedule shown first; `y`/`n` stated; `n` writes nothing, exits 0 | `_confirmed()` builds `About to delete:` + `_described(card, "  ")` + `Delete it? y to delete, n to keep.` | `ConfirmationTests.test_the_prompt_shows_both_sides_and_the_schedule` (front, back, `3 of 4`, and the stored due date all in stdout); `…test_the_prompt_names_the_answers_it_takes`; `…test_a_never_answered_card_says_so`; `…test_declining_writes_nothing_and_exits_zero` (exit 0, `Nothing was deleted.`, bytes unchanged); `…test_nothing_is_removed_before_the_answer_is_given` (a `Popen` session read from **outside** the running process while the prompt waits — the card is still in the file) |
| AC3 — the deleted card is never offered again; the others keep their state | the card is removed from the file, so `schedule.due_positions` cannot select it | `NeverOfferedAgainTests.test_the_deleted_card_is_absent_from_the_next_session` (a real `review` run before says `3 cards due.`, after says `2 cards due.` and the deleted front appears nowhere in the session's output); `…test_the_other_cards_keep_their_own_state` (front, back, rung and due of both survivors compared exactly) |
| AC4 — the deletion is in the stored file; the emptied file still works | `store.save` rewrites the whole file through `ADR-0008`'s temp-file-and-rename | `PersistenceTests.test_the_card_is_gone_from_the_stored_file` (no `front: bonjour` line in the file's text); `…test_deleting_the_last_card_leaves_a_usable_file` (delete the only card, then a real `review` exits 0 with `Nothing is due.` and a real `add` exits 0 and lands in the file) |
| AC5 — no match: no prompt, the front named, non-zero exit, file byte-identical | `delete()`'s first branch returns `EXIT_REFUSED` before any prompt and never calls `store.save` | `NoMatchTests.test_a_populated_file_with_no_such_front`; `…test_a_file_holding_no_cards`; `…test_no_card_file_at_all` (asserts the file is still absent); `…test_a_near_miss_is_not_a_match` (four sub-tests: `Bonjour`, ` bonjour`, `bonjour `, `bonjou`). Each asserts non-zero exit, the front quoted in stderr, no `About to delete` anywhere in the output, and unchanged bytes |
| AC6 — several matches listed and numbered; the chosen one goes; `n` keeps them all | `_chosen_among()` lists each match with `_described(card, "      ")` under `[n]`, accepts the numbers plus `n`, and maps the answer back to `positions[number - 1]` | `SeveralMatchesTests.test_every_match_is_listed_with_both_sides_and_its_schedule` (three backs, `[1]`/`[2]`/`[3]`, three distinct rungs including `0 of 4 (never answered)`, a due date, and `n to keep them all`); `…test_the_chosen_card_goes_and_the_others_stay` (answer `2`; the other two compared field by field); `…test_the_first_and_the_last_can_each_be_chosen` (sub-tests for `1` and `3`); `…test_declining_keeps_them_all`; `…test_a_card_with_a_different_front_is_never_listed` |
| AC7 — unrecognised input re-asks with the card reprinted; a closed stream deletes nothing | `_ask()`'s existing re-prompt loop, plus `delete()` treating `None` as a decline | `PromptInputTests.test_an_unrecognised_answer_re_asks_with_the_card_reprinted` (`About to delete:` and `back:  hello` each appear exactly **twice**, and `This prompt takes: y, n.` appears); `…test_an_unrecognised_answer_re_asks_the_whole_listing` (same, for the numbered prompt); `…test_an_unrecognised_answer_is_never_a_yes`; `…test_the_end_of_the_stream_deletes_nothing_at_the_single_prompt`; `…test_the_end_of_the_stream_deletes_nothing_at_the_listing_prompt` |
| AC8 — an unparseable card file stops `delete` before any prompt | `store.load` raises `CardFileError` into `main()`'s existing handler, before `delete()` prints anything | `UnparsableFileTests.test_an_unparsable_file_stops_before_any_prompt` (a corrupt `rung: later` line; asserts non-zero exit, the card file's path and `line 6` in stderr, no `About to delete`, and unchanged bytes) |
| AC9 — wrong argument count is a usage error; an empty argument is AC5's no-match | argparse's `required` positional; no validation of the argument's content | `ArgumentTests.test_no_argument_is_a_usage_error` (`usage` and `delete` both in stderr, exit 2, file unchanged); `…test_two_arguments_are_a_usage_error`; `…test_an_empty_or_blank_argument_matches_nothing` (sub-tests for `""` and `"   "`, each asserting `No card has the front` and a non-zero exit) |

Plus one criterion-free guard: `OtherSubcommandsTests.test_add_and_review_still_dispatch_to_themselves`,
which is the regression test for the rewritten `main()`.

**The tests were checked for bite.** Seven mutations were applied to `recall/cli.py`, the whole
suite run against each, and the file restored:

| mutation | result |
|----------|--------|
| `_confirmed` returns the position without asking | FAILED (8) |
| `_chosen_among` always returns `positions[0]` | FAILED (2) |
| front matching becomes `.strip().lower()` on both sides | FAILED (4) |
| the end of the input stream deletes instead of declining | FAILED (1) |
| the no-match path exits `EXIT_OK` | FAILED (9) |
| `_described` drops the rung and the due date | FAILED (3) |
| `main()` dispatches `delete` to `add` | FAILED (30) |
| (restored) | OK, 90 tests |

## Deviations from the plan

**One, and it is a split rather than a change.** The plan's `## Approach` described `delete()` as
doing the prompting itself, in three inline branches. It was written as three functions instead —
`_confirmed()` and `_chosen_among()` beside `delete()` — because both prompts return the same
thing, "a position or nothing", and folding them into one function made the removal path read as
though it might run twice. Nothing observable changes: the same prompts, the same accepted answers,
the same exit codes. This is `how`, not `what`, which the procedure allows without a question.

Nothing else. The nine steps ran in order and each one's stated outcome held. `## Scaffolding` said
`none` and none was created.

## Gates

All eight run on the branch head `fe70136`, after the last change.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → `Ran 90 tests … OK`, exit 0. 60 from `WI-0001` and `WI-0002`, 30 new |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → exit 0, no output |
| `workspace-valid` | **pass** | `validate-workspace .` → 4 items, 11 documents, 0 errors, 0 warnings, exit 0 |
| `every-criterion-has-a-test` | **pass** | the table above: nine criteria, each mapped to named test methods, none demonstrated by reading the code |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → "all 1 commit(s) on main..wi/WI-0003 name WI-0003", exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main..wi/WI-0003 --stat` is two files: `recall/cli.py` (+97) and `tests/test_delete.py` (new). Every hunk in `cli.py` is one of plan steps 2, 3, 4, 5 or 6. No neighbouring code was tidied, no unrelated defect fixed |
| `cross-answer-consistency` | **pass** | `lint-answers --changed-since main` → exit 0, 9 consumed human answers checked. This execution edited no sentence in `docs/` at all, so the rule it enforces had nothing to catch |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0 |

**What the claims gate could not see, and what a hand read found.** `lint-claims --changed-since
main` reported *"0 document(s) in 0 path(s) differ from main"* — an empty window, because a work
item's branch changes no document by design: `plan` writes its ADRs on the trunk before the branch
exists, and `spec/doc-header.md` §5 forbids `implement` and `verify` from writing to `docs/` at
all. So the twelve documents were read by hand instead, against the code on this branch:

- `docs/product/vision.md` v6, the *"Throw a card away"* bullet — **true, and now demonstrably so.**
  It promises deletion named by the front side, the card and its ladder position and due date shown,
  removal only on a yes, and permanence. All four are what `delete()` does and each has a test above.
  It cites `WI-0003/Q-001` and `WI-0003/Q-002`, the stakeholder's own answers, and nothing they have
  said since touches it, so ADR-0008 §3's refused repair does not arise.
- `docs/product/vision.md` v6, the exclusions at lines 125–127 — **true**: nothing here amends a
  card, and there is no trash, archive or undo.
- `docs/architecture/adr/ADR-0005` — **true in every clause**, including the two the architect
  decided: the no-match refusal and the several-match listing. Both are implemented as written.
- `docs/architecture/adr/ADR-0007` and `ADR-0008` — **true**: `delete` reads and writes through
  `store.load`/`store.save` unchanged, so the format, the path and the atomic rewrite are as
  documented.
- **`docs/architecture/overview.md` v4 — two sentences are now false, and I may not repair them.**
  Its opening line says the shape stands *"with `add` and `review` built and merged, and `delete`
  not yet started"*, and `## How it is run` says *"`delete` is named here so a reader can see where
  it will attach"*. `delete` is built; on merge both become plainly wrong, and the section describes
  none of its behaviour. `spec/doc-header.md` §5 names `implement` and `verify` as skills that do
  not write to `docs/`, so this is declared here as a **D7 and D12 obligation for `review-close`**
  rather than fixed. What it needs: the opening line updated, `## How it is run` given a paragraph
  for `delete` alongside `review`'s, and a change-log row with a version bump.

## What I did not do

- **I did not tick any acceptance criterion in `item.md`.** All nine checkboxes are still `[ ]`.
  Ticking them is `verify`'s, per `spec/work-item.md`, and plan step 9 says so explicitly.
- **I did not touch `docs/`.** See the paragraph above: `overview.md` needs a repair and it is
  `review-close`'s to make.
- **I did not merge.** The work is on `wi/WI-0003` at `fe70136`; `main` is untouched at `3e9c1df`.
- **I did not address the concurrent-writer gap.** `delete` reads the file, waits at a prompt for as
  long as the person likes, then writes back the list it read, so a second `recall` process writing
  in between would be lost. The plan named this as a risk and put it out of scope; it is the gap
  `WI-0002`'s close already accepted for the whole tool, not a new one, and it belongs to
  `recall/store.py` for every subcommand at once if it is ever taken on.
- **I did not add a way to delete several cards, a listing command, or a force flag.** All three are
  in the item's `## Out of scope` and two of them rest on the stakeholder's own words.
- **I did not test against a real deck or a real restart.** Every test uses `RECALL_CARD_FILE` in a
  temporary directory. AC4's "survives stopping and starting the tool" is demonstrated by separate
  subprocess invocations against the same file, not by rebooting a machine — the same limit
  `WI-0001` recorded for its own AC2.
