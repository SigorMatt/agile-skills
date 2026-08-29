# Implementation report — WI-0003

Branch `wi/WI-0003`. Two passes:

- **pass 1**, `ddc6280` (the ladder in `recall.py`) and `5f8aae2` (the documentation and the
  tests) — everything below except `## Second pass`;
- **pass 2**, `5d9c323` — the two AC9 defects verification found at `eb4cc23`, written up in
  `## Second pass — the send-back on AC9` at the end of this file. Read that section alongside
  the AC9 row of the evidence table, which pass 1 wrote and which was not enough.

## What was built

The interval ladder, exactly as `plan.md` designed it.

A card gains one field, `interval`: the number of days its current wait is, one of `1`, `3`,
`7`, `30`, and `null` for a card that has never been answered. `record_result` now moves it —
`next_interval` up one rung for a right answer, back to the bottom for a wrong one — and sets
`due` to **the day of the review** plus that many days, never the card's old `due` plus anything.
The placeholder `WI-0002` shipped, which pushed every reviewed card to tomorrow whichever way it
was answered, is gone.

The store goes to version 3 and reads 1, 2 and 3. `load` normalises `interval` and `result` onto
every card it returns, so a card written before this item reads as never answered and the next
write carries the field — the same in-place upgrade version 2 used, with no migration to run.
`due` is deliberately not normalised: its absence already means "due", which `due_cards` relies
on.

`load` also gained the two checks AC9 asks for. `due` must be exactly `YYYY-MM-DD` and
`interval` must be a ladder value or `null`; either being wrong makes the store unreadable on the
existing path — message on stderr naming the file and the card, exit 1, file untouched. That
closes the defect `WI-0002`'s review handed forward, where a `due` of `"tomorrow"` sorted above
every real date and removed a card from every review for good while `recall list` still showed it.

`README.md` gained a "When a card comes back" section and an `interval` row in the card-field
table. The review session's output, its keys and its report are untouched, and no command or flag
was added.

## Acceptance criteria evidence

Test names below are in `tests/test_schedule.py` unless another file is named. The suite drives
the delivered `recall` as a subprocess against a scratch store, putting cards on rungs by editing
the store file, which is the mechanism the item requires and `README.md` documents.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — a new card is due the day it is added, and `review` presents it | `add_card` sets `due` to `today()`; unchanged from WI-0001, and checked here so this item cannot break it | `NewCardTest.test_a_new_card_is_due_the_day_it_is_added_and_is_presented`. By hand on 2026-08-29: `recall add "die Katze" "the cat"` → `Added card 1.`, store holds `"due": "2026-08-29"`, `"interval": null` |
| AC2 — a right answer moves up one rung; 30 stays; measured from the review day | `next_interval(current, True)` takes the next `LADDER` value, or stays at the last; `record_result` adds it to `when` | `RightAnswerTest.test_a_right_answer_moves_the_card_up_one_rung` (subTests rung=1→3, 3→7, 7→30), `.test_the_top_rung_stays_the_top_rung`, `.test_the_new_date_is_measured_from_the_review_and_not_from_the_old_due` (a card 10 days overdue on the 3-day rung → due 7 days after **today**). In-process: `test_session_parts.NextIntervalTest.test_a_right_answer_moves_one_rung_up`, `.test_the_top_rung_is_the_top`, `RecordResultTest.test_the_new_date_runs_from_the_review_and_not_from_the_old_due` |
| AC3 — a wrong answer returns to the bottom rung from any rung, and climbing back starts there | `next_interval(anything, False)` returns `LADDER[0]` | `WrongAnswerTest.test_a_wrong_answer_returns_the_card_to_the_bottom_rung_from_any_rung` (subTests rung=1, 3, 7, 30 — each leaves `interval: 1` and `due` tomorrow), `.test_climbing_back_starts_from_the_bottom_rung_not_from_where_it_was` (wrong on the 7-day rung, then right → 3 days, not 7). In-process: `NextIntervalTest.test_a_wrong_answer_returns_to_the_bottom_rung_from_anywhere` |
| AC4 — the ladder is written down in `README.md` | the "When a card comes back" section under `### recall review`, and the `interval` row in the card-field table | `tests/test_docs.py::test_the_readme_names_the_ladder_and_the_field_that_carries_it` asserts the field name `interval` is present in backticks and that "1 day", "3 days", "7 days", "30 days" appear **in that order**. Worked by hand from the documentation alone: a card with `"interval": 7` reviewed right on 2026-08-29 is next due 2026-09-28 — the section says the next wait along is 30 days, counted from the day you review |
| AC5 — scheduling state survives ending and restarting | `save` writes both fields; every command is a separate process | `PersistenceTest.test_the_schedule_survives_ending_and_restarting_the_program`: a session moves a card 3 → 7; the file on disk holds `interval: 7`; a second process `recall list` shows the card and does not disturb it; a third `recall review` says `Nothing is due today.`; after hand-editing `due` to today, a fourth process climbs to 30 — from 7, not from `null` |
| AC6 — a never-answered card is below the bottom rung, so 1 day, then 3, and four right answers to reach the top | `add_card` writes `"interval": None`; `next_interval(None, True)` returns `LADDER[0]` | `NeverAnsweredCardTest.test_a_new_cards_first_right_answer_schedules_it_one_day_out`, `.test_four_right_answers_reach_the_top_rung_not_three` (asserts the sequence is exactly `[1, 3, 7, 30]`), `.test_a_wrong_first_answer_gives_the_same_schedule_and_a_different_result` (same rung and date as a right answer; only `result` differs, which is the cost the stakeholder accepted). By hand on 2026-08-29: add → `interval: null`; `printf '\ny\n' \| recall review` → `1 2026-08-30`; `due` reset to today, reviewed right again → `3 2026-09-01` |
| AC7 — a card the session never reached keeps its rung and its due date | `record_result` is called per card and only for cards answered; unchanged from WI-0002 | `UnreachedCardTest.test_a_card_the_session_never_reached_by_quitting_keeps_its_schedule` (`printf '\ny\nq\n'`) and `.test_a_card_the_session_never_reached_because_the_input_ran_out_keeps_its_schedule` (`printf '\ny\n'`). Each asserts the first card moved 7 → 30 **and** that the second still has `interval: 7`, `due` today and `result: null` |
| AC8 — a store written before this item works and is upgraded in place | `READABLE_VERSIONS` includes 2; `load`'s `setdefault` pass; `save` stamps 3 | `OlderStoreTest.test_a_store_without_the_rung_field_is_read_without_error`, `.test_a_card_without_the_rung_field_is_treated_as_never_answered` (its first right answer gives 1 day, not 3), `.test_the_next_write_carries_the_rung_field_on_every_card_it_holds` — including the card that was not due and was never touched. `tests/test_store.py::test_a_version_1_store_is_read_and_upgraded_by_the_next_write` covers version 1 |
| AC9 — an unreadable scheduling value stops the tool, and the file is untouched | `_is_date` and the `interval` membership check in `load`, both raising `_unreadable` | `UnreadableSchedulingValueTest`, three tests × three commands: `due: "tomorrow"`, `interval: 5`, and `due: "20260829"`. Each asserts exit 1, the message naming **the file, the card and the offending field and value**, empty stdout, and the file's bytes unchanged. By hand: `recall list`, `recall review` and `recall add a b` each printed `recall: /tmp/wi3/demo/bad.json is not a readable card store: card 1 has a 'due' of 'tomorrow', which is not a YYYY-MM-DD date`, exit 1, and `cmp` reported the file byte-identical |

## Deviations from the plan

1. **Step 11 named two existing assertions to move; there were three.**
   `tests/test_store.py::test_a_new_card_is_due_today_with_no_recorded_result` asserts the card's
   key list exactly, so adding `interval` moved it as well as the two the plan listed. It was
   updated the same way — version `2` → `3`, `interval` added to the expected key list and
   asserted `null` — and not weakened. `plan.md`'s `## Risks` says a third test needing a change
   is a signal to re-read the criterion; re-read, this is AC1 and AC6 (a new card is due today and
   sits below the bottom rung), and the test now states both. Nothing about what it checks changed
   except the numbers this item moves.

2. **`README.md`'s `## Not yet built` section was rewritten; no plan step named it.**
   It said "the ladder that pushes a card you keep getting right further and further out is not
   here yet", which step 6 makes false. Leaving it would have contradicted the section step 7
   adds. It now says the schedule is here and names what is deliberately absent — decks, tags,
   statistics, and any command for seeing or setting a schedule — which is what the item's
   `## Out of scope` excludes. No behaviour is described that does not exist.

3. **`tests/test_session_parts.py`'s `RecordResultTest` was rewritten, not only extended.**
   Step 10 asked for `next_interval` cases, which are added as `NextIntervalTest`. But three
   `RecordResultTest` tests described the placeholder ("pushed to tomorrow", "also pushed to
   tomorrow") and passed only because a never-answered card's first right answer happens to give
   one day. Their docstrings would have been false. They now put the card on the 3-day rung and
   assert 7, and a separate test covers the never-answered case where both answers do give
   tomorrow. Nothing was deleted.

4. **The AC9 tests were tightened after they were first written.** As first written they hand-wrote
   a version-3 store and asserted only exit 1 and the file being named — which they satisfied
   against `main`'s `recall.py`, where version 3 is refused for its *version*. They now assert the
   message names the card, the field and the value, so they can only pass on the check AC9 is
   about. Recorded because the first version of that test would have been a gate that passed
   without checking anything.

Everything else went as `plan.md` wrote it, including the ordering constraint `## Risks` names:
step 3 (`load`'s validation) was implemented before step 6 (`record_result`), so `next_interval`
never has to guess at a value outside the ladder. Both of the plan's reversible assumptions were
implemented as stated — `strptime` rather than `date.fromisoformat` (`test_a_due_in_another_date_format_stops_the_tool`
is the case that distinguishes them), and normalisation on read rather than a migration pass.

## Gates

All run on the branch head `5f8aae2`, after the last change.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, **82 tests, OK** (55 before this item) |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '[.]claude' .` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 4 items and 9 documents, 0 errors 0 warnings |
| `every-criterion-has-a-test` | **pass** | the table above names a test function for each of AC1–AC9; none is demonstrated by reading the code. Checked the other way too: with `main`'s `recall.py` restored, **16 of the 18 tests in `test_schedule.py` fail**. The two that do not are AC1's (a regression over WI-0001's behaviour, which `plan.md`'s mapping declares as one) and AC8's read-without-error (a store with no `interval` was readable before, and its two sibling tests — treated-as-never-answered and upgraded-in-place — do fail) |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → exit 0, "all 2 commit(s) on main..wi/WI-0003 name WI-0003" |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main..wi/WI-0003` read hunk by hunk. `recall.py`: the ladder constant and the versions (step 1), `next_interval` (2), `load`'s two checks and `_is_date` (3), the normalisation loop (4), `add_card` (5), `record_result` (6). `README.md`: steps 7 and 8, plus deviation 2. Tests: steps 9–12, plus deviation 3. No hunk is untraceable |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0. It reports no documents changed: this item changed `README.md` and code, and created no ADR — `plan` wrote `ADR-0007` before implementation began, so it is already on `main` |

## What I did not do

- **No ADR was written or amended.** `plan.md` recorded every design decision in `ADR-0007` and
  the `ADR-0001` v3 amendment before this execution started, and nothing here departed from them.
- **The four deviations above are the whole of what differs from the plan.** Nothing was left
  undone: all thirteen steps were executed.
- **Nothing was tidied that this item did not need.** `due_cards` still sorts a missing `due` as
  the empty string, and `cmd_review` still saves the whole document after each card — both were
  looked at while working nearby and both were left exactly as WI-0002 delivered them.
- **No bug item was filed.** The one defect this item inherited — a `due` that is a string but not
  a date — is AC9 and is fixed here, so there was nothing left to file.
- **Timezones are untouched.** `due` remains a local date with no zone, which `ADR-0006` recorded
  as a known limitation and `plan.md` put out of scope.

## Second pass — the send-back on AC9

`verify` rejected `eb4cc23`, ticking AC1–AC8 and failing AC9. `verify-report.md` records both
defects with reproductions; this section records what was done about them. Nothing else on the
branch was touched, and no acceptance criterion was changed.

### D1 — a JSON `true` in `interval` was accepted as the 1-day rung

`load`'s check was `card["interval"] not in (*LADDER, None)`, and `True == 1` in Python, so
`True in (1, 3, 7, 30, None)` is true and the value passed. The card was then silently on the
bottom rung: verification saw it promoted to 3 by a right answer, with nothing reported.

**Fix:** an `isinstance(card["interval"], bool)` test now precedes the membership test. That is
the pattern `load` already uses a few lines above for `number`, which had the identical trap
guarded from the start — the verifier pointed at it, and following it keeps one idiom in the file
rather than two. `false` was already refused (`False == 0`, not a ladder value), which is why the
gap hid; both are refused now.

**Evidence:** `test_schedule.py::UnreadableSchedulingValueTest.test_a_rung_of_json_true_stops_the_tool`
and `.test_a_rung_of_json_false_stops_the_tool`, each over all three commands. By hand, the
verifier's own reproduction: `recall list`, `recall review` and `recall add a b` against a store
whose card has `"interval": true` each exit **1** with
`recall: /tmp/v3/D1fix/cards.json is not a readable card store: card 1 has an 'interval' of True, and the ladder is 1, 3, 7, 30 or null`,
and `cmp` reports the file byte-identical.

### D2 — an unpadded `due` was accepted and the card was never due again

`_is_date` used `strptime(value, "%Y-%m-%d")`, which accepts `2026-8-9` as readily as
`2026-08-09`. But `due_cards` compares `due` as a **string**, so the unpadded value sorted above
every zero-padded date: the card was listed by `recall list`, never presented by `recall review`,
and nothing was printed. That is `WI-0002`'s handed-forward defect in a second spelling, and the
one AC9 was written to close.

**Fix:** `_is_date` now requires the round trip — the parsed date must print back as the value
given, so the only accepted form is the canonical `YYYY-MM-DD`. `strptime` is kept for the parse,
because it still refuses `20260829` and datetimes where `date.fromisoformat` would not.

This reverses a choice `plan.md` recorded under `## Assumptions` — "`strptime(...)` is the right
strictness for AC9's `due` check" — which was stated there as reversible at the cost of "one
expression in `load` and a test". That is exactly what it cost, and nothing is stored differently,
so there is no migration. It was not escalated for that reason: the plan named the assumption, named
its cost, and verification is what falsified it.

**Evidence:**
`test_schedule.py::UnreadableSchedulingValueTest.test_an_unpadded_due_stops_the_tool_rather_than_dropping_the_card`,
over all three commands; and `.test_every_padded_date_the_readme_documents_is_still_accepted`,
which checks the fix did not start refusing well-formed dates (`2026-01-02`, `2026-12-31`,
`2026-02-28`, today). By hand: all three commands against a store whose card has
`"due": "2026-8-9"` exit **1** with
`... card 1 has a 'due' of '2026-8-9', which is not a YYYY-MM-DD date`, `cmp` byte-identical.

### The AC4 coverage gap verification recorded

`verify-report.md` noted that deleting `README.md`'s `interval` row from the card-field table left
all 82 tests green, because the prose section names `interval` too — so AC4's "a row in the
card-field table" clause was untested. That was recorded as a gap, not a criterion failure, and it
is closed here: `test_docs.py::test_the_readme_card_field_table_has_a_row_for_the_rung_field`
asserts exactly one line beginning `` | `interval` | `` and that it names all five values. Confirmed
sensitive: renaming that row's first cell makes the test fail and nothing else notice.

### What did not change

`README.md` and `ADR-0007` are untouched. Both already say `due` is exactly `YYYY-MM-DD` and
`interval` is one of the four values or `null`; it was the code that did not match them, so there
was nothing to correct in either. In particular `README.md`'s sentence "Nothing is silently
dropped or repaired" was left as it is, which the verifier asked for — it is true of this commit
and was not true of `eb4cc23`.

No acceptance criterion was edited. No behaviour outside `load` changed: `next_interval`,
`record_result`, `add_card` and every command are byte-identical to pass 1.

### Gates, pass 2

All run on branch head `5d9c32329fefeaa6ed51fd75d6cd47d1e4ca5a09`.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, **87 tests, OK** (82 after pass 1; five added here) |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '[.]claude' .` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 4 items and 9 documents, 0 errors 0 warnings |
| `every-criterion-has-a-test` | **pass** | AC1–AC8's evidence is unchanged and their code is untouched. AC9 now has, in addition to the two cases pass 1 covered, the four tests named above. Checked in the removal direction: with `eb4cc23`'s `recall.py` restored, `test_a_rung_of_json_true_stops_the_tool` and `test_an_unpadded_due_stops_the_tool_rather_than_dropping_the_card` both fail; with the README row renamed, `test_the_readme_card_field_table_has_a_row_for_the_rung_field` fails and no other test does |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → exit 0, "all 6 commit(s) on main..wi/WI-0003 name WI-0003" |
| `no-unplanned-scope` (advisory) | **pass** | pass 2's diff is three hunks in `recall.py` (`_is_date`'s round trip, the `bool` guard, and the comments on each) and two test files. Every one traces to D1, D2 or the AC4 gap the send-back recorded |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0 |

### What I did not do, pass 2

- **I did not re-verify AC1–AC8.** `verify-report.md` ticks them against `eb4cc23` and says
  explicitly that the AC9 fix touches `load`, so the next verification must re-run all nine. The
  full suite passing at `5d9c323` is evidence, not a substitute for that.
- **I did not search exhaustively for other values that slip through `load`.** D1 and D2 were both
  found by probing beyond the criterion's named examples, and that is the verifier's job to repeat.
  What I can say is narrower: the two named in the send-back are closed, and `false`, `"3"`,
  `"tomorrow"`, `20260829` and `2026-13-45` are all still refused, each with a test.
- **I did not touch `due_cards`' string comparison**, which is the underlying reason an unpadded
  date is dangerous. Making it parse dates rather than compare strings would be a change to
  behaviour `WI-0002` delivered, with no criterion of this item behind it. `load` refusing the
  value is what AC9 asks for, and it is what was done.
