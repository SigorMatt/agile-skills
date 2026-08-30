# Implementation report — WI-0002

Branch `wi/WI-0002`, two commits off `main` at `45f8d03`. Gates were run on the branch head
(`e595079`), after the last change.

## What was built

**`recall/schedule.py` — new, 55 lines.** `ADR-0009`'s module: pure functions over `store.Card`
and a date handed in by the caller. `INTERVALS` is `ADR-0002`'s ladder written down once;
`is_due()` is the `due <= today` comparison; `due_positions()` returns the **positions** of the
due cards ordered by due date, `sorted()`'s stability leaving ties in card-file order;
`after_right()` and `after_wrong()` return the rescheduled card. It imports `datetime` and
`recall.store` and nothing else, opens no file, reads no environment variable, prints nothing,
and never asks what day it is.

**`recall/cli.py` — the session, +86 lines.** `_ask(prompt, accepted)` prints the prompt, reads
one line with `input()`, strips and lowercases it, and returns it when it is accepted; anything
else prints what the prompt takes and then asks the whole question again, card text and all;
`EOFError` returns `None`. `review()` loads the card file, takes `datetime.date.today()` once,
selects the due positions, prints the count, and then for each card reveals, grades, replaces
that one position and calls `store.save()` on the whole list before the next card is printed.
`_stopped()` is the early ending, shared by `q` and end-of-input at either prompt. `_parser()`
registers a `review` subparser taking no arguments, and `main()` now dispatches on
`arguments.subcommand` instead of calling `add()` unconditionally — the trap WI-0001's review
recorded for this item.

**`tests/test_review.py` — new, 23 tests.** Each seeds a card file by writing `ADR-0007`'s format
directly into a temporary directory, points `RECALL_CARD_FILE` at it, and drives
`python3 -m recall review` as a subprocess with the keystrokes on standard input. The file is read
back by a parser written in the test module rather than by `recall.store`, so a change to the
tool's writer cannot quietly change what these tests accept.

**`tests/test_schedule.py` — new, 11 tests.** The ten rung transitions and the selection
boundaries as direct calls, with the date passed in.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `review()` prints only the front at the reveal prompt; the back is the *outcome* prompt's text, printed only after Enter is accepted | `test_the_back_is_hidden_until_enter` — with input `q\n` the session ends at the reveal prompt and standard output contains `bonjour` and **not** `hello`; with input `\nq\n` it contains `hello`. `test_review_takes_no_arguments` — `review extra` exits 2 with a usage message |
| AC2 | `schedule.due_positions()` selects on `card.due <= today` with no cap | `test_only_and_all_due_cards_are_offered` — five seeded cards due −3, −1, 0, +1, +7 days; the three due fronts appear in standard output, `due-tomorrow` and `due-next-week` do not, and the count line reads `3 cards due.` Supported by `test_a_card_is_due_from_its_date_onwards` and `test_only_the_due_cards_positions_come_back` |
| AC3 | the rung is untouched until an answer is given, and both outcomes are computed from `today`, never from `card.due` | `test_an_overdue_card_is_unpenalised` — a rung-2 card due 10 days ago; the session is started as a live subprocess, Enter is sent, and the card file is then read while the process is still running: byte-identical to the seed and still `rung: 2`. `y` then writes rung 3 due **today+7**. Also `test_an_overdue_card_answered_wrong_is_due_tomorrow` (rung 4, due −40 → rung 1, today+1) and `test_both_answers_count_from_the_day_passed_in` |
| AC4 | `store.save()` is called on the whole list immediately after each answer, inside the loop | `test_each_answer_is_written_before_the_next_card` — three due cards, input `\ny\nq\n`; the file afterwards holds card 1 at rung 2 due today+3 and cards 2 and 3 exactly as seeded, so the write cannot have waited for the end of the session. `test_only_y_and_n_are_outcomes` — `maybe` and `3` are refused at the outcome prompt, standard output names `y, n, q`, and the card is answered right exactly once |
| AC5 | `schedule.after_right()`: `min(rung + 1, HIGHEST_RUNG)`, due `INTERVALS[new rung]` days after the date passed in | `test_answering_right_walks_the_ladder` (rungs 0–4 → 1, 2, 3, 4, 4 at +1, +3, +7, +30, +30) and, at the command line, `test_right_at_the_command_line` — five cards seeded one per rung, all answered `y`, and the file read back shows exactly that sequence. `test_the_intervals_are_adr_0002s_ladder` pins `INTERVALS` to `{1: 1, 2: 3, 3: 7, 4: 30}` |
| AC6 | `schedule.after_wrong()`: rung 1, due one day after the date passed in, from any rung | `test_answering_wrong_returns_to_the_first_rung` (all five rungs → rung 1, today+1) and `test_wrong_at_the_command_line` — the same five-rung file answered `n` throughout reads back as five cards at rung 1 due today+1 |
| AC7 | each answer is on disk before the process exits, and the next session re-selects from the file | `test_a_second_session_the_same_day_offers_only_what_is_still_due` — three due cards, two answered in the first subprocess; the second subprocess prints `1 card due.`, offers `three`, and offers neither `one` nor `two` |
| AC8 | `due_positions()` returning `[]` prints `Nothing is due.` and returns before any call that writes; `store.load()` already reads a missing file as no cards | `test_nothing_due_says_so_and_writes_nothing`, three sub-tests — a file whose only card is due tomorrow, a file holding the header and no cards, and no file at all. Each: exit 0, `Nothing is due.` on standard output, standard error empty, and the file byte-identical afterwards or still absent |
| AC9 | the same immediate save as AC4; `_stopped()` returns before writing the card on screen | `test_quitting_keeps_the_answers_already_given` — input `\ny\nq\n` leaves card 1 rescheduled and cards 2 and 3 untouched and still due. `test_a_kill_at_a_prompt_keeps_the_answers_already_given` — a live subprocess is answered once, the test waits for that answer to appear in the file, asserts the process is still running, and sends **SIGKILL** (`Popen.kill()`); the file afterwards still holds the answer and the two untouched cards |
| AC10 | `review()` prints `"<n> card(s) due."` before entering the loop | `test_the_count_is_stated_before_the_first_card` — the expected number is computed **by the test**, by reading the `due: ` lines of the seeded file and comparing each to today; standard output contains `3 cards due.` and its index is asserted to be before the first front's. `test_one_due_card_is_counted_in_the_singular` covers the singular |
| AC11 | `q` is accepted at both prompts and `EOFError` returns `None`; both paths reach `_stopped()`, which prints to standard output and returns 0 | `test_q_stops_at_either_prompt` (inputs `q\n` and `\nq\n`) and `test_end_of_input_stops_the_session` (inputs `""` and `"\n"`, so the stream runs out at the reveal and the outcome prompt respectively). All four: exit 0, standard error **empty**, card file byte-identical. `test_each_prompt_names_what_it_takes` asserts each prompt names its keys |
| AC12 | `sorted(positions, key=…due)` — a total function of the stored file | `test_due_cards_are_offered_oldest_first` — four cards seeded out of order (due 0, −3, 0, −1) are offered `first, second, third, fourth`. `test_the_order_is_the_same_twice` runs a session, restores the seeded bytes exactly, runs it again, and asserts the two front sequences are equal and are the predicted one. Supported by `test_cards_sharing_a_due_date_stay_in_file_order` and `test_ties_keep_file_order_among_earlier_and_later_dates` |
| AC13 | `_ask()` loops until the line is accepted, reprinting the whole prompt including the card text | `test_an_unrecognised_key_re_asks_the_same_card` — input `x`, Enter, `z`, `y` against one rung-0 card: the front line appears **twice** in the output preceding the back, standard output contains both `Enter, q` and `y, n, q`, and the card ends at rung 1 due today+1 — answered right exactly once, so neither `x` nor `z` counted as anything. `test_an_unrecognised_key_leaves_a_quit_session_untouched` — `nope` then `q` leaves the file byte-identical |
| AC14 | `store.load()` raises `CardFileError` before the loop; `main()`'s existing handler prints and returns 1 | `test_an_unparsable_card_file_stops_the_session` — a file with `bakc:` for `back:`; exit non-zero, standard error contains the card file's path and `line 5`, standard output contains no front side, and the file is byte-identical afterwards |

## Deviations from the plan

1. **`_ask()` derives its refusal message from `accepted` rather than taking the wording as a
   third argument.** The plan specified `_ask(prompt, accepted)` and said an unaccepted line
   "prints what is accepted and then reprints the whole prompt". `_named()` turns `("", "q")` into
   `Enter, q` and `("y", "n", "q")` into `y, n, q` mechanically, so the signature is the plan's
   and no prompt can name keys it does not accept. How, not what.
2. **The outcome prompt prints the card's back only, not its front and back.** This is the plan's
   own wording (`_ask` "with its back as the prompt"); it is recorded here because it is what makes
   AC13's evidence readable — the front appearing exactly twice before the back is a check that
   would be meaningless if the outcome prompt reprinted the front too.
3. **`PROMPT_MARK` is a module constant** rather than an inline `"> "`. One line, no behaviour.

Nothing else. Steps 1–8 were executed in order; no step was found impossible as written, and
nothing in the plan changed what gets delivered.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, **60 tests**, `OK`. WI-0001's 26 among them, unchanged |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | the table above: AC1–AC14 each name a test function, and every one of them is a test that reads the tool's output or the bytes of the card file |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → exit 0, "all 2 commit(s) on main..wi/WI-0002 name WI-0002" |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main..HEAD` read hunk by hunk: `recall/schedule.py` is plan steps 1–2; the `cli.py` hunks are steps 3, 4 and 5; the two test files are steps 6 and 7. No hunk touches `add()`, `store.py`, or anything outside them |
| `cross-answer-consistency` | **pass** | `lint-answers --changed-since main` → exit 0. This execution edited no document, so no sentence citing a stakeholder answer was touched |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0, and `lint-claims --all` → exit 0 as well, because the `--changed-since` window is empty for an item that changed no document |

**The tests bite.** Two mutations were run against the finished code and reverted:

- moving `store.save()` out of the loop to a single call at the end failed
  `test_each_answer_is_written_before_the_next_card`,
  `test_quitting_keeps_the_answers_already_given`,
  `test_a_kill_at_a_prompt_keeps_the_answers_already_given` and
  `test_a_second_session_the_same_day_offers_only_what_is_still_due`;
- returning `due_positions()`' list unsorted failed `test_due_cards_are_offered_oldest_first`,
  `test_the_order_is_the_same_twice`, `test_the_oldest_due_date_comes_first` and
  `test_ties_keep_file_order_among_earlier_and_later_dates`.

Both were run on a copy and the originals restored before the branch was committed; `git status`
was clean of source modifications afterwards.

## What I did not do

**`docs/architecture/overview.md` will be stale the moment this branch merges, and I did not
touch it.** Three sentences in it describe the state this item changes:

- *"`add` is built [src: recall/cli.py]; `review` is planned
  [src: tracker/items/WI-0002/artifacts/plan.md]"* — `review` is built on this branch;
- the `## The pieces` bullet for the schedule module ends *"WI-0002 is the item that puts it in"* —
  it is in;
- the document's opening line still reads *"as it stands after WI-0001 was planned and before any
  of it was built"*, which WI-0001's merge already overtook.

`spec/doc-header.md` §5 says plainly that `implement` does not write to `docs/`, and this skill's
own contract lists no document among its outputs, so repairing them here would have been the
circular edit that rule exists to prevent. **This is a D7 and D12 handover to `review-close`**: a
version bump and a change-log row on `overview.md` are owed at the close of this item. Note that
`lint-claims --changed-since main` cannot find any of it — the window is empty because this branch
changed no document — so it has to be read, not run.

**No bug item was filed and no defect was found in WI-0001's behaviour.** Its 26 tests pass
unchanged against the new dispatch in `main()`.

**Nothing in the plan was left undone.** All eight steps were executed. The plan's own risks stand
as it recorded them: `input()` means `y` is followed by Enter; one whole-file rewrite and two
`fsync` calls per answer; a session that crosses midnight schedules from the day it began.
