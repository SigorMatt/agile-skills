# Implementation report — WI-0002

Branch `wi/WI-0002`, six commits, `41eb102..075e339`. All ten plan steps were executed; nothing
was left undone and no question was filed.

## What was built

`recall review` — the daily session — and the per-card state it writes. Everything landed in the
two files WI-0001 delivered, plus two new test modules.

**`recall.py`, the store layer.** `STORE_VERSION` is now 2 and `READABLE_VERSIONS` is `(1, 2)`.
`load` refuses a document whose `version` is anything else through the existing `_unreadable`
path, so the message and the exit code are ADR-0004's, and it validates `due` (a string when
present) and `result` (`"right"`, `"wrong"` or `null` when present), naming the card and the
field in the style `load` already used. `save` stamps `STORE_VERSION` on every write, which is
what upgrades a version-1 document in place with no migration to run [src: ADR-0006].

**`recall.py`, four new functions**, each to the contract the plan's interface table fixed:

- `today()` — today's local date as `YYYY-MM-DD`, called once per command.
- `due_cards(document, when)` — the cards whose `due` is missing or is at or before `when`,
  sorted by `due` then `number`. A missing `due` sorts as `""`, below every real date, so a
  version-1 card comes before every dated one. Touches no disk and does not mutate the document.
- `record_result(card, right, when)` — sets `result` and sets `due` to the day after `when`.
  Touches no disk.
- `read_line(stream)` — the next line without its newline, or `None` at end of input. Built on
  `stream.readline()` rather than `input()`, because that is the only thing that tells a blank
  line (`""`) from an exhausted input (`None`).

**`recall.py`, the command.** `cmd_review(arguments, input_stream=None)` rejects any argument
with `usage: recall review` on stderr and exit 2; otherwise it loads the store, takes
`due_cards`, and for each card prints the question side, waits for Enter, prints the answer side,
waits for `y` or `n`, records the result and **saves the whole document before the next card**.
`_await_key` is the loop that makes AC5, AC9 and AC10 one behaviour: it reprints its prompt and
reads again for anything it does not recognise, and returns `None` for both `q` and end of input,
which is what makes those two end the session identically. `main` dispatches `review`, and
`USAGE` now names it.

**`README.md`** gained a `recall review` section with the key-map table and a worked session,
a `### What each card records` table naming `due` and `result` and both of `result`'s values, and
a paragraph on what `version` 1 and 2 mean. The store example is now the version-2 shape, and
"Not yet built" now names only the spaced-repetition ladder.

**`tests/support.py`** now replaces `HOME` on every run — with a directory inside the per-test
temporary directory when the caller names none — and accepts `stdin=` to pipe a session in.

## Acceptance criteria evidence

Every test below is in `tests/`, run by `python3 -m unittest discover -s tests -t .`. Names are
given unqualified; the module is in the second column.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `cmd_review` prints `card["question"]`, then waits in `_await_key` for `KEY_REVEAL` before printing `card["answer"]`; the loop moves to the next card only after that | `test_review.py::test_ac1_cards_are_presented_one_at_a_time_question_side_first` asserts `die Katze` < `the cat` < `der Hund` < `the dog` by index in stdout after `printf '\ny\n\nn\n'`. `test_ac1_an_answer_side_is_not_shown_before_its_enter_is_read` drives `q\n` alone: `die Katze` appears, `the cat` does not — so the reveal is caused by the Enter, not by reaching the card |
| AC2 | `record_result` sets `result` to `"right"` or `"wrong"`; `cmd_review` saves the document after each card | `test_review.py::test_ac2_the_y_card_and_the_n_card_are_recorded_differently_and_persist` re-reads the store file after the process ended and asserts card 1 is `"right"`, card 2 is `"wrong"`, and the two differ. `test_docs.py::test_the_readme_names_the_fields_a_review_writes_and_what_they_mean` asserts `README.md` contains `` `result` ``, `"right"`, `"wrong"` and `` `null` `` |
| AC3 | `cmd_review` prints `NOTHING_DUE` and returns 0 when `due_cards` is empty, printing no summary and nothing else | `test_review.py::test_ac3_an_empty_store_prints_one_line_and_exits_zero` and `test_ac3_a_just_emptied_pile_prints_the_same_single_line` each assert exactly one line on stdout, empty stderr and exit 0 — the second immediately after a session that reviewed every due card |
| AC4 | `record_result` sets `due` to the day after today, and `due_cards` takes only `due <= today` | `test_review.py::test_ac4_a_card_reviewed_today_is_not_presented_again_today` runs a full session and then a second one, asserting neither card's question side appears in the second run's stdout |
| AC5 | `_await_key` returns `None` on `q` at either moment; `cmd_review` breaks without calling `record_result` | `test_review.py::test_ac5_q_at_the_question_side_ends_the_session_and_keeps_what_was_recorded` — three cards, `printf '\ny\nq\n'`: no third card in stdout, the store holds `{1: right, 2: null, 3: null}`, and a following session presents cards 2 and 3 and not card 1. `test_ac5_q_at_the_answer_side_records_nothing_for_that_card` — `printf '\ny\n\nq\n'` from the same start: `the dog` was revealed, `das Pferd` never appears, card 2's `result` is still `null`, and card 2 is still due |
| AC6 | `cmd_review` prints `Reviewed {reviewed}, right {right}.` after the loop, whichever way the loop ended | `test_review.py::test_ac6_the_last_line_carries_the_reviewed_count_and_the_right_count` asserts `stdout.splitlines()[-1]` of the AC2 session contains `2` and `1`; `test_ac6_the_summary_line_is_printed_after_a_q_too` asserts the last line of the first AC5 session contains `1` |
| AC7 | the loop runs over every card `due_cards` returned, from the one flat `cards` array; `cmd_review` rejects a non-empty `arguments` before touching the store | `test_review.py::test_ac7_one_session_covers_every_due_card_in_the_flat_pool` — three cards, one session, all six sides in stdout and all three results recorded. `test_ac7_review_takes_no_deck_tag_or_filter_argument` — `recall review --deck german` exits 2 with `usage: recall review` on stderr, empty stdout and all three results still `null`, and a following session presents all three |
| AC8 | `due_cards` sorts by `(due, number)` | `test_review.py::test_ac8_due_cards_are_presented_oldest_first_and_the_order_is_stable` sets `due` by hand in the store file — two days ago for card 3, yesterday for cards 1 and 2 — copies the file aside, and reads the order out one card per `q\n` session, asserting `das Pferd`, `die Katze`, `der Hund`. It then restores the copy and reruns, asserting the same first card. `test_session_parts.py::test_the_order_is_oldest_due_first_then_ascending_number` asserts the same order on `due_cards` directly |
| AC9 | `read_line` returns `None` only at end of input, and `_await_key` treats it exactly as `q` | every case in `test_review.py` is piped through `subprocess.run(input=...)`, which is the first half. `test_ac9_input_that_ends_mid_session_ends_it_exactly_as_q_does` — `printf '\ny\n'` over two due cards: card 1 recorded `"right"`, card 2 still `null` and still presented by the next run, a last line containing `1`, exit 0. `test_session_parts.py::test_a_blank_line_and_the_end_of_input_are_different_values` pins the distinction itself |
| AC10 | `_await_key` reprints its prompt and reads again for any line it does not recognise, recording nothing and not ending | `test_review.py::test_ac10_a_line_outside_the_key_map_is_ignored_and_the_prompt_repeats` — one due card, `printf 'x\n\nz\ny\n'`: exit 0, `result` `"right"`, a last line containing `1`, and the reveal prompt and the grade prompt each appearing exactly **twice** in stdout |

**These tests were checked against mutants, not just run.** Four behaviours were removed one at a
time from a copy of `recall.py` and the suite re-run, to establish that the criteria above are
demonstrated rather than merely accompanied:

| behaviour removed | suite result |
|-------------------|--------------|
| the sort in `due_cards` | 3 failures |
| `record_result` no longer moves `due` | 8 failures |
| a wrong answer records the same value as a right one | 3 failures |
| an unrecognised line ends the session instead of being ignored | 1 failure |

The working tree was restored from the copy after each; `git status` was clean afterwards and the
committed `recall.py` is the unmutated one.

## Deviations from the plan

Four, all in **how** rather than **what**. None changes what is delivered.

1. **The tests were written with the code they demonstrate, not in a later pass.** The plan puts
   all the test-writing in steps 8 and 9, after steps 1–7. This skill's procedure requires the
   test to come with the change in the same commit, so each plan step's tests were written into
   its own commit. Every test the plan named exists; only its commit changed.

2. **A new test module, `tests/test_session_parts.py`, holds the unit tests for steps 3 and 4.**
   The plan's steps 3 and 4 each state an "Afterwards" that is a unit-level check —
   `due_cards` on a hand-built document, `read_line` on a `StringIO` — but name no file for them,
   and neither belongs in `test_review.py` (subprocess cases) or `test_store.py` (the file on
   disk). Ten cases, importing `recall` directly.

3. **One assertion in step 1's test waited for step 5.** The plan's step 1 says a `"version": 3`
   document must make `recall list` **and** `recall review` exit 1, but `review` does not exist
   until step 5. The test was written with the `list` and `add` arms in step 1's commit and the
   `review` arm added in step 5's commit, where it could pass. The finished test
   (`test_store.py::test_a_store_from_a_newer_version_is_refused_and_left_untouched`) covers all
   three commands.

4. **`cmd_review` takes an optional `input_stream` parameter**, defaulting to `sys.stdin`. The
   plan's interface table gives it the signature `cmd_review(arguments)`. The parameter is
   unused by `main` and by every test — all of which drive the real executable through a real
   pipe — and exists so that the session can be exercised in-process without a subprocess if a
   later item needs it. It is one keyword argument with a default, and removing it costs one
   line. Declared here rather than quietly, because it is a widening of an interface the plan
   fixed.

**Two things worth a reviewer's attention, neither a deviation.**

- `test_ac8_...` reads the presentation order out one card at a time, by running a `q\n` session,
  noting which card it showed, pushing that card's `due` ten days out and running again. That is
  more machinery than "read three questions out of one session's stdout", and it is deliberate: a
  single session's stdout shows the cards in order, but asserting on it would also be asserting
  that no prompt or blank line falls between them, which `refine` left deliberately unconstrained.
  Reading one card per run asserts only the order.
- `tests/support.py`'s `setUp` now creates a `home/` directory inside every test's temporary
  directory, and `test_the_default_store_is_dot_recall_json_in_the_home_directory` was simplified
  to use it rather than making its own. That is plan step 7 landing in an existing test.

## Gates

Every gate below was run on the branch head, `075e339`, after the last commit.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → `Ran 55 tests in 3.782s / OK`, exit 0. WI-0001 left 21; this item adds 34 |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '[.]claude' .` → exit 0, no output |
| `workspace-valid` | **pass** | `validate-workspace .` → `checked 4 item(s), 8 document(s) / 0 errors, 0 warnings`, exit 0 |
| `every-criterion-has-a-test` | **pass** | the table above names a test function for each of AC1–AC10, and the mutation table shows four of the behaviours behind them failing the suite when removed |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → `all 6 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main --stat` is 11 files. Seven are product code, docs and tests, each traced to a plan step: `recall.py` (1–5), `README.md` (6), `tests/support.py` (7), `tests/test_review.py` (8), `tests/test_store.py` (1, 2, 7), `tests/test_docs.py` (9), `tests/test_session_parts.py` (3, 4 — deviation 2). The other four are this item's own record: `tracker/board.md`, `item.md`, `history.md`, `journal.md` |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → `checked no documents changed since main / 0 errors, 0 warnings`, exit 0. Nothing under `docs/` changed on this branch: ADR-0006 and the architecture overview were both written by `plan` and are already on `main` |

## What I did not do

Nothing in the plan was left undone: all ten steps were executed, and every test the plan's step
8 and step 9 name exists.

Deliberately not done, and each already recorded as out of this item's scope:

- **The interval ladder.** A card answered right comes back tomorrow, exactly as a card answered
  wrong does. That is ADR-0006's declared placeholder and WI-0003 replaces it. Between this item
  and that one, the tool is knowingly wrong about *when* a card returns — it is right about
  *whether* it returns and about what was answered. `README.md`'s "Not yet built" says so in the
  user's own terms.
- **Anything requiring a terminal.** No raw keypresses, no clearing, no colour. Prompts are
  printed on lines of their own and nothing depends on partial-line flushing, which is what the
  plan's `## Risks` asked for.
- **No injectable clock**, per plan assumption 7. `today()` reads the real date. AC8 produces
  past due dates by editing the store file instead, which is what the criterion specifies.
- **No migration command.** A version-1 store is upgraded by the next write.

Two things a reader might expect and will not find:

- **`recall list` does not show `due` or `result`.** The item excludes any output that shows a
  card's recorded results back to the reviewer, so `list` is untouched and the store file is the
  only place to see them.
- **`due` is a bare local date with no timezone**, and a session that crosses local midnight sees
  the date it started with. Both are recorded in ADR-0006 and in the plan's `## Risks`; neither
  is defended against and no criterion asks.
