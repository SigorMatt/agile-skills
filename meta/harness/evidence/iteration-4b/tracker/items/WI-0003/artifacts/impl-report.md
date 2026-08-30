# Implementation report — WI-0003

Branch `wi/WI-0003`, five commits, `88525dc..` on `main` at `a798a5e`. All eight gates pass on the
branch head. The plan's nine steps were executed in order; one deviated from, at step 8, and it is
recorded below.

## What was built

`record_answer` in `recall/deck.py` stops being a placeholder and becomes `ADR-0002` §4 to §6 as
`ADR-0008` §3 and §4 encode them. `LADDER = (1, 3, 7, 30)` sits beside `FIRST_RUNG`, and is the
only place in the tree the four numbers appear. A right answer sets the card's next review to
`LADDER[card.rung]` days after the day of the sitting and advances the stored rung by one,
capped at the last index — that cap is the ladder topping out, which the stakeholder chose in
`WI-0003/Q-001`. A wrong answer returns the stored rung to `FIRST_RUNG` and applies
`LADDER[FIRST_RUNG]`, one day. Both gaps count from the day of the sitting, so an overdue card is
neither compensated nor penalised.

`store.load` now refuses a stored `rung` outside `0 … len(LADDER) - 1` as `DeckUnreadable`, naming
the card, in the same shape as the sibling checks beside it (`ADR-0008` §6). It is refused, never
clamped. Because the value is validated at load, `record_answer` stays a total function over valid
cards and re-checks nothing.

`cmd_review` prints one line per graded card, after the deck is saved, carrying that card's new
next-review date as `YYYY-MM-DD` and the gap in whole days:

```
  next review: 2026-09-06 (in 7 days)
```

The wording is `plan.md` `## Assumptions` 1 and 2; `ADR-0007` §2 left it to the plan and no
criterion names anything in the line but the date's form. The days remaining come from a new
`deck.days_until`, so the ladder's numbers never reach `cli.py`.

`docs/process/using-recall.md` v5 gains "When each card comes back" and loses the section claiming
scheduling was unbuilt. `docs/architecture/overview.md` v4 restates two commissive clauses as
description; the design itself did not move.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — the ladder 1, 3, 7, 30, then holding | `LADDER` and `record_answer`'s right branch, `recall/deck.py` | `tests.test_review.SchedulingTests.test_a_correct_answer_walks_the_ladder_and_then_holds` — adds a card, then five times rewrites **only** its `due` to today and sits answering right; asserts the stored gaps are `[1, 3, 7, 30, 30]`. Also run by hand: five sittings printed `stored due = today+1, +3, +7, +30, +30`. Unit-level: `DeckArithmeticTests.test_record_answer_walks_the_ladder_and_holds_at_the_top`, one subtest per rung. |
| AC2 — a wrong answer, and the ladder position reset with it | `record_answer`'s wrong branch | (a) `SchedulingTests.test_a_wrong_answer_is_due_tomorrow_from_a_fresh_card` → `due` = today + 1. (b) `SchedulingTests.test_a_wrong_answer_resets_the_ladder_and_not_only_the_date` → four right answers reach today + 30, then wrong gives today + 1, then **right gives today + 1, not today + 30**. By hand: `after four right answers -> today + 30`, `then wrong -> today + 1`, `then right -> today + 1`. Unit-level: `DeckArithmeticTests.test_record_answer_sends_a_wrong_card_back_to_the_start_from_any_rung`, one subtest per rung. |
| AC3 — the gap counts from the day of the sitting, overdue included | `record_answer` adds to `today`, never to `card.due` | `SchedulingTests.test_an_overdue_card_is_scheduled_from_the_day_of_the_sitting` — a card ten days overdue, both answers: presented (`WI-0002` AC13) and stored `due` = today + 1 in each case. By hand, both answers: `presented=True -> today + 1`. Unit-level: `DeckArithmeticTests.test_record_answer_counts_from_the_sitting_not_from_the_due_date`. |
| AC4 — the sitting says when the card is next due | `NEXT_REVIEW_LINE` and `_next_review_line` in `recall/cli.py`, printed after `store.save` | `SchedulingTests.test_the_sitting_prints_the_new_date_at_two_gaps_and_on_both_answers` — asserts, on every one of four sittings, that the exact string stored in `due` appears in stdout, that the first is today + 1 and the fourth today + 30 (so a constant fails the pair), and that a following wrong answer prints today + 1. Position is `SchedulingTests.test_the_date_comes_after_that_cards_answer_and_before_the_next_question` — two graded cards, asserting `a-one` < date₁ < `q-two` and `a-two` < date₂. `SchedulingTests.test_an_abandoned_sitting_prints_no_date` covers the sitting that grades nothing. By hand, the four sittings printed `2026-08-31 (in 1 day)`, `2026-09-02 (in 3 days)`, `2026-09-06 (in 7 days)`, `2026-09-29 (in 30 days)`. |
| AC5 — the rule is written down, and the tool agrees | `docs/process/using-recall.md` v5 | `SchedulingTests.test_the_documentation_states_the_rule_and_the_worked_example` — asserts the document contains `1, 3, 7`, `30 days` and `0, 1, 4, 11, 41, 71 and 101`, and no longer contains `Scheduling is not built yet` or `comes back tomorrow whether`. The prose facts a substring cannot capture are in `## When each card comes back`: the gaps, that they hold at thirty and never grow past a month, that a wrong answer returns the card to the start, and that a gap counts from the day of the sitting even when the card is overdue. The "tool agrees" half is AC1 to AC3 above, which produce exactly the days the worked example states. |
| AC6 — `WI-0001` AC1–AC9 and `WI-0002` AC1–AC13 still hold | steps 2, 3, 4, 5 | The full suite is green on the branch head: `python3 -m unittest discover -s tests -t . -q` → exit 0, **43 tests** (32 before this item). Every one of those twenty-two criteria has its own test in `tests/test_add.py`, `tests/test_list.py`, `tests/test_review.py` and `tests/test_storage.py`, and all still pass. The read of the four named criteria is below; the full twenty-two-criterion read is `verify`'s to record, per the criterion's own wording. |

### AC6 — the four criteria named in the criterion, read against what shipped

- **`WI-0002` AC8** (a card finished in one sitting is not presented again the same day). Holds.
  Every gap this item can produce is at least one day: the right branch applies `LADDER[rung]`,
  whose smallest element is 1, and the wrong branch applies `LADDER[FIRST_RUNG]`, which is 1.
  Exercised against the new behaviour by `ReviewTests.test_an_answer_survives_the_process_ending`,
  which grades a card and then runs a second sitting the same day.
- **`WI-0002` AC10** (both sides unchanged after a sitting, and the grade still recorded).
  Holds. `record_answer` still returns one `dataclasses.replace` of one card and touches neither
  side nor the deck's length; `grade` is still set on every graded card. Exercised by
  `ReviewTests.test_a_sitting_disturbs_nothing_else` and, at unit level, by the two new
  `DeckArithmeticTests` cases, which assert `(question, answer)` and `grade` explicitly on every
  rung.
- **`WI-0002` AC13** (an overdue card is still presented). Holds. `due_positions` is untouched by
  this item. Exercised against the new behaviour twice:
  `ReviewTests.test_an_overdue_card_is_still_presented` and this item's AC3 test, which asserts
  the overdue card appears in stdout before checking what it was rescheduled to.
- **`WI-0001` AC3** (`recall list` still prints `question | answer` and nothing more). Holds.
  `cmd_list` is untouched — `ADR-0007` §4 leaves it alone, and `## Out of scope` names it.
  Exercised against the new behaviour by `ReviewTests.test_a_sitting_disturbs_nothing_else`,
  which compares `recall list` output before and after a sitting that now also reschedules.

**Nothing was waived.** Every one of the four is exercised by something executable that also runs
the new behaviour.

### The tests can fail

Run deliberately, and recorded because `plan.md` `## Risks` says a weak suite would go green
against the code this item replaces:

- With `record_answer` reverted to the placeholder (move to tomorrow, leave the rung), the suite
  fails 10 cases: `test_a_correct_answer_walks_the_ladder_and_then_holds`,
  `test_a_wrong_answer_resets_the_ladder_and_not_only_the_date`,
  `test_the_sitting_prints_the_new_date_at_two_gaps_and_on_both_answers`, and both new unit tests
  across their subtests. **AC3's tests do not fail** against the placeholder, because a placeholder
  that always says "tomorrow" is accidentally right about an overdue card.
- With the gap counted from `card.due` instead of `today`, exactly the two AC3 tests fail —
  `test_an_overdue_card_is_scheduled_from_the_day_of_the_sitting` and
  `test_record_answer_counts_from_the_sitting_not_from_the_due_date` — which is the reading that
  criterion exists to exclude.

## Deviations from the plan

1. **Step 8 said to leave `docs/architecture/overview.md` alone if the design matched, and I
   edited it anyway.** The design does match: `deck.py` holds the arithmetic with the four numbers
   in one constant, `cli.py` prints the line, `store.py` refuses an out-of-range rung — exactly
   version 3's account. What I changed is tense. Version 3 was written at plan time and said
   "WI-0003's plan puts it there" and "its ladder position once WI-0003 lands", both citing the
   plan; on a merged trunk those read as pending work that is in fact built, which is the kind of
   sentence D12 exists to catch. Two clauses now read as description and cite the code. The
   change-log row says in terms that no design decision moved, so a reader can tell this version
   from one that records a change of shape.
2. **A helper the plan left open.** Step 4's interface note allowed either a helper in `deck.py`
   or a subtraction at the call site for the days remaining, with the constraint that the ladder's
   numbers must not reach `cli.py`. I added `deck.days_until(due, today)` — one line, and it keeps
   `cli.py` free of date arithmetic as well as of the ladder.
3. **The store-level range check got its own test class**, `LadderStorageTests` in
   `tests/test_review.py`, rather than going unexercised. No acceptance criterion covers it — the
   item's criteria deliberately never read or write `rung` — but it is plan step 3 and `ADR-0008`
   §6, and it is the branch that keeps `record_answer` total. It asserts all three of: non-zero
   exit, the card named on stderr, and the deck left byte-for-byte alone.
4. **`recall/deck.py`'s module docstring was rewritten.** It said the overview "puts the scheduling
   arithmetic here when WI-0003 arrives", which this item makes false. Not a plan step; it is the
   same D12 obligation one file lower down.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, 43 tests |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 6 items, 11 documents, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | The table above names a test function for all six criteria. AC5's is a read of one named file, made mechanical by asserting the phrases and the absence of the two stale ones; AC6's is the green suite plus the four explicit reads, none waived |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → exit 0, "all 4 commit(s) on main..wi/WI-0003 name WI-0003" (five after this report's commit) |
| `no-unplanned-scope` (advisory) | **pass** | The diff is three source files, two test files and two documents. Every hunk traces to a plan step: `deck.py` to 1, 2 and deviation 2; `store.py` to 3; `cli.py` to 4; `tests/` to 5 and 6 and deviation 3; `using-recall.md` to 7; `overview.md` to 8 as deviated |
| `cross-answer-consistency` | **pass** | `lint-answers --changed-since main` → exit 0, 7 consumed human answers checked, 2 changed documents in the window |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0, 2 documents examined |

## What I did not do

- **`BUG-0001` is untouched.** A filesystem error other than `DeckUnreadable` on the deck file
  still reaches the person as a traceback. It is open, it is not this item's, and this item did not
  widen to absorb it. Step 3's new `DeckUnreadable` travels `ADR-0004` §5's existing route and
  changes nothing about how errors are reported.
- **The full `WI-0001` AC1–AC9 and `WI-0002` AC1–AC13 read is not written out here.** AC6 asks for
  it "in the verification record", so the twenty-two-criterion read belongs in `verify-report.md`.
  What is here is the evidence that supports it — the green suite, and the four criteria the
  criterion names explicitly, read individually.
- **`docs/product/vision.md` was not touched.** Nothing in it describes the scheduling arithmetic
  at a level this item changes; it was taken to v4 when `Q-001` and `Q-002` were consumed.
- **One stale phrase in `overview.md` was left as it is**: `store.py`'s bullet still says the load
  path serves "`add`, `list` and, later, `review`", though `review` shipped with `WI-0002`. It is
  outside D12's scope for this item — the staleness is about `review` existing, not about the
  scheduling behaviour this item touched — and fixing it here would put a hunk in the diff that
  traces to no criterion and no plan step. Worth a one-line correction by whoever next has a
  reason to open that file.
