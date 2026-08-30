# Implementation report — WI-0002

Branch `wi/WI-0002`, head `ef7a00d`. Suite: 32 tests, exit 0.

**Two executions of `implement` have run on this item, and this report covers both.** The
sections below are the item's report, not a single run's; where the two differ, execution 2 is
stated first because it is the current state.

## Executions

| # | when | commits | what it did |
|---|------|---------|-------------|
| 1 | 2026-08-30T02:44–02:53Z | `d2ca976..76b4aff`, six | Built `recall review` from `plan.md`'s six steps, with a test per criterion |
| 2 | 2026-08-30T03:07Z onward | `6cd5fc1`, `ef7a00d`, two | Answered `review-close`'s rejection: **F1**, a false claim in `docs/process/using-recall.md`, and **F2**, a stranded comment in `recall/cli.py`. No behaviour changed |

Execution 2 exists because `review-close` rejected the item on **D12** and sent it back to
`in-progress`. Its scope is `artifacts/review.md`'s two findings and nothing else: that document
states in terms that all thirteen criteria hold, were independently demonstrated at `b51c502`,
and should not be re-done. They were re-run, not re-derived — see `## Acceptance criteria
evidence`.

## What was built

**Execution 2** changed two things and no behaviour:

- **`docs/process/using-recall.md` v3 → v4** (`6cd5fc1`). §"What this version does not do yet"
  claimed *"Your answers are recorded against the cards in the meantime, so nothing you review
  now has to be reviewed again to catch the scheduler up [src: ADR-0006]"*. `ADR-0006` does not
  say that — its only sentence about WI-0003 is that WI-0003 *"inherits a field it does not have
  to add"* — and the code does not do it: `record_answer` leaves `rung` untouched by design, and
  nothing anywhere reads `grade` back into scheduling. The paragraph now says what is true: the
  answer is written into the deck file, nothing reads it back yet, the card moves to tomorrow
  whatever it was, and every card is still on the bottom rung `recall add` gave it — which is
  where it will start climbing from when WI-0003 lands. Version bumped with a change-log row.
- **`recall/cli.py`** (`ef7a00d`). The `#:` block stating that neither prompt may carry the
  card's text — AC1's guard — sat above `RIGHT_RESPONSE`/`WRONG_RESPONSE`/`GRADE_RESPONSES`,
  fused to the block describing them, while `REVEAL_PROMPT` and `GRADE_PROMPT` carried no comment
  at all. Moved onto the constants it governs. Comment only: no string, constant or branch
  changed, which the unchanged 32-test suite and the AC1 mutation below both bear out.

**Execution 1** built `recall review` — the third subcommand, and the sitting it drives. No
new module: `store.py`
still does file access and no printing, `deck.py` gains card-level operations as values with no
I/O, `cli.py` gains everything a person sees, exactly as `plan.md` §Approach specified.

- **`recall/deck.py`** — `Card` gains an optional fifth field `grade`, declared last and
  defaulting to `None`, holding one of `GRADE_RIGHT`/`GRADE_WRONG` (`ADR-0006` §1–2).
  `Deck.replace(position, card)` puts a card back at its position, keeping length and order.
  `due_positions(deck, today)` returns the positions of every card whose date is **on or before**
  today, in deck order. `record_answer(card, grade, today)` is the placeholder WI-0003 replaces:
  grade recorded, `due` moved to the day after the sitting whatever the answer, `rung` untouched.
- **`recall/store.py`** — `grade` round-trips. Absent on read is a card never reviewed; present
  and not one of the two words is `DeckUnreadable`, named like any other malformed field; written
  only when set, so a deck of unreviewed cards is byte-identical to what WI-0001 wrote.
  `DECK_FORMAT_VERSION` does not move (`ADR-0006` §5).
- **`recall/cli.py`** — `cmd_review`, the `review` subparser (no options), `NOTHING_DUE_MESSAGE`,
  `REVEAL_PROMPT`, `GRADE_PROMPT`, `UNRECOGNISED_GRADE_MESSAGE`, and `GRADE_RESPONSES` mapping
  `y`→right and `n`→wrong after stripping whitespace and folding case. Two reads per card; the
  deck saved after every graded card; `DeckUnreadable` caught at the same single site as `add` and
  `list`; end of input at either read ends the sitting and returns 0.
- **`tests/support.py`** — `run_recall` gains `stdin`; `write_deck`, `days_from_today` and
  `stored_cards` added; `NOTHING_DUE_MARKER` added beside `EMPTY_DECK_MARKER`.
- **`tests/test_review.py`** — thirteen acceptance tests, one per criterion and named for it,
  plus three unit tests for the deck and store layer beneath them.
- **`docs/process/using-recall.md` v3** — "Doing a review", and "What this version does not do
  yet" rewritten. Three criteria are decided by reading this file, so it is part of the delivery
  and not documentation of it.

## Acceptance criteria evidence

**Execution 2 added no criterion and removed no behaviour**, so the thirteen rows below stand
unchanged. They were re-run rather than re-asserted: the full suite is green on the branch head
`ef7a00d` (`Ran 32 tests ... OK`, exit 0). One mutation was re-applied this execution, chosen
because it is the one F2 is about — the guard whose comment moved. Adding a second
`print(card.question)` in `cmd_review` makes `test_due_cards_are_presented_one_at_a_time` fail
with *"q-one must appear exactly once in the run's output"* and
`test_an_unrecognised_response_re_asks_the_same_card` fail with `2 != 1`; the source was restored
and the suite is green again. So AC1's guard is still enforced by a test after the comment moved,
which is the only thing the comment move could plausibly have disturbed.

The **F1 fix has no test and cannot have one.** It is a sentence in a document; no acceptance
criterion of this item is about it, and the project has no prose-checking gate that could decide
whether a citation *supports* a sentence — `lint-claims` proves only that a citation *resolves*,
which is exactly why it passed over the false claim. It is recorded under `## What I did not do`.

Every row below names a test in `tests/test_review.py` (run with
`python3 -m unittest discover -s tests -t . -q`, exit 0) **and** the mutation that was applied to
the source to prove the test would fail if the behaviour were removed. The mutation column is the
`every-criterion-has-a-test` gate's evidence: a test that passes against a broken implementation
demonstrates nothing, so each was checked rather than asserted.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `cmd_review` prints the question, waits, prints the answer, and finishes a card before starting the next; no prompt carries card text | `test_due_cards_are_presented_one_at_a_time` — three due cards, six input lines; asserts each question precedes its answer, `a-one` precedes `q-two`, `a-two` precedes `q-three`, each question occurs exactly once, exit 0. **Mutation:** printing all questions up front → this test FAILS |
| AC2 | the reveal read happens before `print(card.answer)`; EOF there returns before the answer | `test_answer_is_not_shown_until_it_is_asked_for` — one due card, `stdin=""`; asserts `die Katze` in stdout, `the cat` not in stdout, exit 0. **Mutation:** printing the answer before the read → FAILS |
| AC3 | `_read_grade` loops until `GRADE_RESPONSES` matches, printing `UNRECOGNISED_GRADE_MESSAGE` and re-issuing the *same* card's grade prompt without reprinting the question | `test_an_unrecognised_response_re_asks_the_same_card` — two due cards, input `\n maybe y \n y`; asserts `'y'` and `'n'` are named, the grade prompt appears **twice** before `second-q` appears, `first-q` occurs exactly once, and `stored_cards()[0]["grade"] == "right"`. **Mutations:** accepting any response → FAILS; reprinting the question on re-ask → FAILS |
| AC4 | `due_positions` filters on `card.due <= today` | `test_a_card_due_later_is_not_presented` — one card today, one at today+7; asserts `due-later` absent from stdout, exit 0. **Mutation:** treating every card as due → FAILS |
| AC5 | empty `due_positions` prints `NOTHING_DUE_MESSAGE` and returns `EXIT_OK` | `test_nothing_due_says_so_and_exits_zero` — all cards at today+7; asserts `NOTHING_DUE_MARKER` in stdout, neither question present, exit 0. **Mutations:** removing the message → FAILS; treating every card as due → FAILS |
| AC6 | `store.load` returns an empty deck for an absent file and never writes; the nothing-due branch returns before any `save` | `test_absent_deck_reports_nothing_due_and_creates_nothing` — empty home; asserts the **same** marker, exit 0, and that `deck.json` and its parent are still absent. **Mutations:** saving on the nothing-due path → FAILS; removing the message → FAILS |
| AC7 | `DeckUnreadable` caught at the single site shared with `add` and `list`; `_report_unreadable` writes to stderr and returns `EXIT_DECK_UNREADABLE` | `test_unreadable_deck_is_refused_and_left_alone` — six damaged decks as subtests, including a `"grade": "maybe"` deck; asserts non-zero exit, the deck path on stderr, stdout empty, the nothing-due marker **absent** (an unreadable deck must not read as an empty one), and `sha256` identical before and after. **Mutation:** treating an unreadable deck as empty → FAILS |
| AC8 | `store.save` after every graded card | `test_an_answer_survives_the_process_ending` — one due card graded in a first process; a second `recall review` asserts its question is absent from stdout. **Mutation:** recording nothing → FAILS |
| AC9 | the same per-card save, plus `EOFError` handled at both reads so EOF ends the sitting with `EXIT_OK` and no traceback | `test_a_sitting_stopped_part_way_keeps_the_answers_given` — two due cards, input for the first only; asserts no `Traceback` on stderr, then that a second run presents `pending-q` and not `kept-q`. **Mutations:** saving once at the end → FAILS; recording nothing → FAILS |
| AC10 | `Deck.replace` at a fixed position; `record_answer` touches only `grade` and `due` | `test_a_sitting_disturbs_nothing_else` — `recall list` captured before and after a full sitting; asserts the two outputs are identical. **Mutation:** upper-casing the question in `record_answer` → FAILS |
| AC11 | `due_positions` returns every due position; nothing slices it | `test_a_sitting_is_not_capped` — twenty-five due cards, fifty input lines; asserts all twenty-five questions appear, exit 0. **Mutation:** capping at 20 → FAILS |
| AC12 | `new_card` already dates a card today (WI-0001) and `due_positions` includes today | `test_a_card_added_today_is_due_today` — absent deck, `recall add`, then `recall review` as a second process; asserts `brand-new-q` in stdout. **Mutation:** `new_card` dating a card tomorrow → FAILS |
| AC13 | `card.due <= today`, not `==` | `test_an_overdue_card_is_still_presented` — one card dated today−7; asserts its question appears, exit 0. **Mutation:** `due == today` → FAILS |

Three unit tests in `DeckArithmeticTests` sit under the above so a failure names the layer:
`test_due_positions_is_on_or_before_today_in_deck_order`,
`test_record_answer_keeps_the_card_and_moves_it_off_today`, and
`test_an_unreviewed_deck_serialises_exactly_as_wi_0001_wrote_it` (`ADR-0006` §4).

## Deviations from the plan

**Execution 2 executed no plan step.** `plan.md` has six and all six were completed by execution
1; a rejection from `review-close` is not a plan step and `plan.md` was not re-litigated. Its
work is `artifacts/review.md`'s findings F1 (blocking) and F2 (accepted, non-blocking, taken in
the same pass because the file was open). F3 — `Card.grade` annotated `str` while defaulting to
`None` — was left alone: the review marked it an observation with no action, and the project runs
no type checker (`commands.lint` is `compileall`, a syntax check, per `ADR-0003`).

**Execution 1's three deviations** follow, all "how" rather than "what". None changes what is
delivered.

1. **`run_recall`'s `stdin` default is an immediately-closed pipe, not the parent's inherited
   standard input.** Plan step 1 says the keyword "defaults to today's behaviour", and today's
   behaviour is inheritance. For `add` and `list` the two are indistinguishable — neither reads
   standard input — so no existing test changes meaning. The reason for the change is that a
   `review` test which forgot to pass `stdin` would inherit the runner's terminal and hang the
   suite instead of failing at EOF. Reversing it is `input=stdin` on one line.
2. **A stored `"grade": null` is `DeckUnreadable`, not "absent".** `plan.md` step 3 says "absent
   on read is `None`", which left a literal JSON `null` unaddressed. `ADR-0006` §3 does address
   it — present and not one of the two words is unreadable — so the ADR was followed. The tool
   never writes `null` (`ADR-0006` §4), so this can only be reached by hand-editing.
3. **Two deck-layer changes were committed without their tests in the same commit.** The skill
   asks for the test alongside the change; `plan.md` puts every test in step 5, after steps 2–4.
   The plan was followed, and each step's own "Afterwards" check was executed at the time and its
   output recorded (below). The durable tests landed one commit later in `c99a800`.

Plan step 2's afterwards check, run at the time:

```
card without a grade: Card(question='q', answer='a', rung=0, due=datetime.date(2026, 8, 30), grade=None)
due_positions: (0, 1)
record_answer: Card(question='q', answer='a', rung=0, due=datetime.date(2026, 8, 31), grade='right') | same q/a/rung: True | due+1: True
```

Plan step 3's afterwards check, run at the time:

```
unreviewed deck byte-identical to WI-0001's form: True
'grade': 'maybe' raises DeckUnreadable: card 1's 'grade' is not 'right' or 'wrong'
'grade': null raises DeckUnreadable: card 1's 'grade' is not 'right' or 'wrong'
graded round-trip: Card(question='q', answer='a', rung=2, due=datetime.date(2026, 8, 30), grade='right')
```

One correction made during step 4 and worth naming: the response tokens were first derived from
the grade constants' initials (`r`/`w`). `plan.md` §"The two recognised responses" fixes them as
`y` and `n`, and step 6 requires those two letters to be documented. Corrected before the step
was committed; `RIGHT_RESPONSE` and `WRONG_RESPONSE` now hold them explicitly.

## Gates

**Execution 2 — run on the branch head `ef7a00d`, after the last change**, which is `ef7a00d`
itself. Every command below was issued after both commits landed.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → `Ran 32 tests in 3.400s` / `OK`, exit 0 |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → `checked 6 item(s), 9 document(s)` / `0 errors, 0 warnings`, exit 0 |
| `every-criterion-has-a-test` | **pass** | the thirteen-row table above, unchanged and re-run green at head; plus AC1's mutation re-applied this execution and confirmed to fail two tests, then restored |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → `all 12 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | `git diff d479eac..HEAD` is four hunks in two files: the frontmatter version bump, the F1 paragraph, the F1 change-log row, and F2's comment move. Every one traces to a named review finding; nothing else is touched |
| `cross-answer-consistency` | **pass** | `lint-answers --changed-since main` → `claim window: 1 path(s) differ from main (d2ca976) under docs` / `checked 5 consumed human answer(s)` / `0 errors, 0 warnings`, exit 0. The window is non-degenerate: it saw the one document this execution changed |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main --context work-item` → `1 document(s) in 1 path(s) differ from main` / `0 errors, 0 warnings`, exit 0. **This gate passed over F1's false claim too**, and that is not a defect in it: it proves a citation resolves, not that it supports its sentence |

**Execution 1 — run on the branch head `76b4aff`**, after its last change.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → `Ran 32 tests ... OK`, exit 0 |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → `checked 6 item(s), 9 document(s) — 0 errors, 0 warnings` |
| `every-criterion-has-a-test` | **pass** | the table above: thirteen tests, thirteen criteria, and fourteen mutations proving each test fails when its behaviour is removed |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → `all 6 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | six source/doc files, each traceable to a numbered plan step; the only other files in the diff are `tracker/` bookkeeping written by `transition` and `board-gen` |
| `cross-answer-consistency` | **pass** | `lint-answers --changed-since main` → `checked 5 consumed human answer(s)`, 0 errors |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → 0 errors, 0 warnings |

## What I did not do

**Execution 2:**

- **I did not re-verify the thirteen criteria.** They were demonstrated independently by `verify`
  against `b51c502` and the review confirms it; this execution ran the suite and one mutation,
  which is a check that nothing broke, not a fresh demonstration. `verify` needs to satisfy
  itself about the changed document and about nothing else — that is the honest handover.
- **The F1 fix carries no test**, for the reason in `## Acceptance criteria evidence`: there is
  no criterion about the document's prose and no gate in this project that could decide the
  claim. Its correctness rests on a read, and a reader repeating it needs `deck.py:92`
  (`record_answer`, `rung` untouched), `deck.py:73` (`rung=FIRST_RUNG`, the only place `rung` is
  ever set outside `store`'s round-trip), and `grep -rn grade recall/` (written and validated,
  never read into scheduling). All three were run this execution.
- **F3 was left alone** — see `## Deviations from the plan`.
- **`review.md`'s five accepted gaps were not closed**, because accepting them is what the
  review did. They are in the item's `## Notes` and stay there.

**Execution 1:**

- **`BUG-0001` is not fixed, deliberately.** `review` reaches the deck through the same
  `store.load` as `add` and `list`, so it inherits the same weakness: a filesystem error that is
  not a content problem — a permission denial, a directory where the deck file should be — still
  escapes as a traceback. `plan.md` §Risks requires this, the item excludes it, and AC7 is about
  deck *content* only. **A passing AC7 is not evidence about `BUG-0001`.**
- **The schedule is a placeholder.** Every reviewed card comes back the next day whatever the
  answer, and `rung` is never moved. That is what the item asks for and what WI-0003 replaces.
  `docs/process/using-recall.md` v3 says so plainly, because otherwise it looks like a defect.
- **A sitting prints no closing line** — no tally, no count, nothing after the last card's grade
  prompt. `plan.md` records this as the assumption most likely to be wrong in a person's hands,
  and says it should be reversed by asking the stakeholder rather than by a later plan.
- **The reveal prompt does not end in a newline of its own.** Driven from a pipe, the answer is
  printed on the same line as the prompt, because the newline a person's Return supplies never
  arrives. At a terminal — the only place `ADR-0001` says this tool runs — it reads correctly.
  Every criterion is written over substring order in stdout, which is unaffected. Named here
  rather than left for `verify` to find in the raw output.
- **No injectable clock.** `datetime.date.today()` is read directly, per `plan.md` §Assumptions.
  A suite started in the last seconds before midnight can flake; that is a re-run, not a defect.
- **Card order is deck order** and nothing tests an alternative, because `refine` left the order
  deliberately unconstrained and `plan.md` chose deck order with its reversal cost recorded.
