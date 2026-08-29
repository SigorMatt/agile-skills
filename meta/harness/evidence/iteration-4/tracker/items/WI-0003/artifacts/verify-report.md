# Verification report — WI-0003

Verified-commit: f841f096374450ebb8c4fbb2688382c860322651

This is the **second** verification of WI-0003. The first rejected `eb4cc23` on AC9 and sent the
item back; its full text is the version of this file at commit `9cda720`, and both defects it
found are quoted with their reproductions in `impl-report.md` `## Second pass`. A condensed
record of it is in `## Appendix` below, so this file still says what happened without carrying
the whole of it twice.

Every criterion was re-run here, AC1–AC8 included. The first verification ticked those eight
against `eb4cc23` and said explicitly that the AC9 fix touches `load`, which every command goes
through — so its ticks were treated as unverified for this pass and each was re-established from
scratch. Nothing below cites `impl-report.md` as evidence.

## Verdict

**Pass — on to `in-review`.** All nine acceptance criteria are met at `f841f09`, each on a
command run here with its output recorded. The two defects the first verification found are
closed, and neither reappears in any spelling probed for.

The setup for AC2, AC3, AC5, AC6, AC7 and AC9 was derived from `README.md` alone — the field name
`interval` and its permitted values came out of the card-field table, not out of the code — which
is the property AC4 exists to give a checker with no context, and it held.

## Criteria

Throughout: `T` is `date +%F` on the machine that ran the check, which printed `2026-08-29`;
`RECALL_FILE` pointed at a scratch store under `/tmp/v3b/` for every run; a card was put on a rung
by editing that file by hand, which is what the criteria prescribe.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `recall add "die Katze" "the cat"` in an empty store, then `cat cards.json`, then `printf '\ny\n' \| recall review` | `Added card 1.`; the stored card is `"due": "2026-08-29"`, `"result": null`, `"interval": null`; the review printed `die Katze` / `[Enter] to see the answer, q to stop` / `the cat` / `[y] right, [n] wrong, q to stop` / `Reviewed 1, right 1.` | `due` is today, and the card was presented. Both halves of the criterion. |
| AC2 | **pass** | four stores, one per rung, each hand-edited to `interval: <rung>` and `due: T`, each run `printf '\ny\n' \| recall review`; then a fifth on the 3-day rung with `due` set to `T-10 days` | rung 1 → `interval 3 due 2026-09-01`; rung 3 → `interval 7 due 2026-09-05`; rung 7 → `interval 30 due 2026-09-28`; rung 30 → `interval 30 due 2026-09-28`; overdue rung 3 (due `2026-08-19`) → `interval 7 due 2026-09-05` | `T+3 = 2026-09-01`, `T+7 = 2026-09-05`, `T+30 = 2026-09-28`. Every rung move, the top rung staying put, and the overdue case measured from the review day and not from the old `due`. |
| AC3 | **pass** | five stores at `interval` `null`, `1`, `3`, `7`, `30`, each `due: T`, each run `printf '\nn\n' \| recall review`; then the 7-rung store's `due` reset to `T` and `printf '\ny\n' \| recall review` | every one of the five → `interval 1 due 2026-08-30 result wrong`; the follow-up right answer → `interval 3 due 2026-09-01` | A wrong answer returns the card to the bottom rung from anywhere, and climbing back starts from the bottom — 3 days, not the 7 it had reached. |
| AC4 | **pass** | `grep -n` on `README.md` for the ladder line, the two answer bullets and the table row; and the whole of this report's setup, done from the README | line 95 `**1 day → 3 days → 7 days → 30 days.**`; lines 97 and 99 the **right** and **wrong** bullets; line 146 `` \| `interval` \| how many days this card is currently waiting between reviews: `1`, `3`, `7` or `30`, and `null` … `` under `### What each card records` at line 137 | Worked by hand from the documentation only: a card stored with `"interval": 7` answered right today is next due `2026-09-28` — the next wait along is 30 days, counted from the review day. The AC2 run on the 7 rung produced exactly that date. |
| AC5 | **pass** | four separate processes against one store: `printf '\ny\n' \| recall review` (3 → 7), then `recall list`, then `recall review`, then `due` hand-edited to `T` and `printf '\ny\n' \| recall review` | after process 1 the file on disk holds `"due": "2026-09-05"`, `"result": "right"`, `"interval": 7`; process 2 printed `1\tdie Katze\tthe cat`; process 3 printed `Nothing is due today.`; the file still read `interval 7 due 2026-09-05`; process 4 → `interval 30 due 2026-09-28` | Process 4 climbed from 7, not from `null`, so the rung genuinely survived three process boundaries rather than being re-derived. |
| AC6 | **pass** | `recall add` into an empty store, then five rounds of `printf '\ny\n' \| recall review` with `due` reset to `T` between them; separately, a fresh card answered `printf '\nn\n'` | right #1 → `interval 1 due 2026-08-30`; #2 → `interval 3 due 2026-09-01`; #3 → `interval 7 due 2026-09-05`; #4 → `interval 30 due 2026-09-28`; #5 → `interval 30 due 2026-09-28`; wrong-first → `interval 1 due 2026-08-30 result wrong` | The sequence is 1, 3, 7, 30 in that order and the top rung is reached on the **fourth** right answer, not the third. The wrong first answer gives the same rung and the same date as the right one; only `result` differs, which is the cost the stakeholder accepted. |
| AC7 | **pass** | two cards both `interval: 7`, `due: T`; `printf '\ny\nq\n' \| recall review`, and the same store shape with `printf '\ny\n\n' \| recall review` | both sessions printed `Reviewed 1, right 1.`; in both, card 1 → `interval 30 due 2026-09-28 result right` and card 2 → `interval 7 due 2026-08-29 result None` | The card the session never got an answer for keeps its rung, its `due` **and** its null result, whether the session was quit with `q` or ran out of input at the question side. |
| AC8 | **pass** | a hand-written `"version": 2` store, cards with `due` and `result` but no `interval`, one due today (`result: "right"`) and one due `2026-11-27`; `recall list`, then `printf '\ny\n' \| recall review` | `list` printed both cards, exit 0, and left the file at `"version": 2` with no `interval` anywhere (`grep -c interval` → `0`); after the review the file is `"version": 3` with card 1 at `"due": "2026-08-30"`, `"interval": 1` and card 2 at `"interval": null` | Card 1 carried `result: "right"` and still got **1 day**, not 3 — so a card with no rung field is treated as never answered, not as one on the bottom rung. Card 2 was never due and never touched, and the next write still gave it the field. |
| AC9 | **pass** | for each store below, all three of `recall list`, `recall review`, `recall add a b`, with `cmp` against a copy taken before the run | see `## Negative and boundary cases exercised` — every case exits **1**, prints nothing on stdout, prints `recall: <path> is not a readable card store: card N has …` on stderr, and leaves the file byte-identical | Both named cases pass, and so do the two defects the first verification found. Probed well beyond the criterion's named values; the one class that is accepted is argued below and judged to be inside AC9 rather than a failure. |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 87 tests in 5.958s` / `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '[.]claude' .` → exit 0, no output |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 4 item(s), 9 document(s)`, `0 errors, 0 warnings` |
| `every-criterion-independently-checked` | **pass** | the `## Criteria` table: every row is a command run in this execution against the branch head, with its own output. `impl-report.md` was read as the contract requires and is cited nowhere as evidence. AC1–AC8's earlier ticks were re-earned rather than carried over. |
| `negative-cases-exercised` | **pass** | 30 stores built to be wrong on purpose, listed below; plus AC7's two abandoned sessions, AC8's pre-version store, AC2's top rung and overdue card, and AC3 from every rung including the never-answered one |
| `tests-would-fail-without-the-change` (advisory) | **pass** | nine mutations, one per criterion, each making a test fail; see `## Test sensitivity check` |

The working tree was clean before and after (`git status --short` empty), and the suite was
re-run at the end to confirm every mutation had been backed out: `Ran 87 tests`, OK.

## Negative and boundary cases exercised

Every case below is a store whose only fault is the value named. Each was run against all three
commands — `recall list`, `recall review`, `recall add a b` — with `cmp -s` against a copy taken
before the run.

**The two the criterion names, and the two the first verification found:**

| store | result |
|-------|--------|
| `due: "tomorrow"` | all three: exit **1**, stdout empty, file byte-identical, stderr `recall: /tmp/v3b/ac9/due_tomorrow/cards.json is not a readable card store: card 1 has a 'due' of 'tomorrow', which is not a YYYY-MM-DD date` |
| `interval: 5` | all three: exit **1**, stdout empty, file byte-identical, stderr `… card 1 has an 'interval' of 5, and the ladder is 1, 3, 7, 30 or null` |
| `due: "2026-8-9"` (D2) | all three: exit **1**, stdout empty, file byte-identical, stderr `… card 1 has a 'due' of '2026-8-9', which is not a YYYY-MM-DD date` |
| `interval: true` (D1) | all three: exit **1**, stdout empty, file byte-identical, stderr `… card 1 has an 'interval' of True, and the ladder is 1, 3, 7, 30 or null` |
| `interval: false` | all three: exit **1**, stdout empty, file byte-identical, stderr `… card 1 has an 'interval' of False, and …` |

**Probed beyond the criterion's named values.** The first verification found both of its defects
by trying values AC9 does not name, and `impl-report.md` says in as many words that repeating
that search is the verifier's job. It was repeated. All of the following are **refused** — exit
1, empty stdout, a stderr message naming the file, the card, the field and the value, and the
file byte-identical:

- `due` of the wrong **type**: `20260829` (a JSON number), `null`, `true`, `["2026-08-29"]`,
  `{"y": 2026}`. None of these produces a traceback; each is reported as a `due` that is not a
  date.
- `due` strings that parse somewhere but are not the documented shape: `"20260829"`,
  `"2026-13-45"`, `"2026-02-30"`, `" 2026-08-29"`, `"2026-08-29 "`, `"2026-08-29T00:00:00"`,
  `"٢٠٢٦-٠٨-٢٩"` (Arabic-Indic digits, which `%Y-%m-%d` will parse), `""`, `"999-01-01"`,
  `"10000-01-01"`.
- `interval` values outside the ladder: `"3"` (a string), `-1`, `0`, `[1]`, `{"a": 1}`, `1e400`
  (reported as `inf`).
- A bad value on the **second** card rather than the first: `card 2 has a 'due' of 'tomorrow'` —
  so the check is over every card, not only the one that happens to be first.

**Accepted, correctly:** `"0999-01-01"` and `"9999-12-31"` are well-formed and zero-padded, so
they are read and sort correctly against ordinary dates. A card with **no** `due` key is read and
is due, which is what `README.md` says of a version-1 card; reviewing it right gave
`interval 1, due 2026-08-30`. A card with no `interval` key is read as never answered (AC8).

**Accepted, and argued.** `interval: 1.0` and `interval: 3.0` — JSON floats — are accepted, reach
`next_interval`, and behave as the 1-day and 3-day rungs: reviewing the `1.0` card right gave
`interval 3, due 2026-09-01`, and the file was rewritten with the integer `3`. This is the class
the first verification left open ("whether any other such value exists was not exhaustively
searched"), so it is answered here rather than left hanging.

It is **not** recorded as a failure of AC9, and the reasoning is on the record so it can be
disagreed with. AC9 refuses "a value `README.md` does not list". JSON has a single number type:
`1.0` and `1` denote the same number, and `README.md`'s row lists the number 1. The contrast with
D1 is the point — JSON `true` is a *boolean*, not a number of days, so it was never a value the
README listed, and it was silently reinterpreted as a rung the user had not written. `1.0` is
reinterpreted as nothing; it is the rung the user wrote, it schedules the card identically, the
card is not dropped, and the next write canonicalises it to `1`. AC9's harm — "No command
silently drops the card" — does not arise.

## Test sensitivity check

Nine mutations, one per criterion, each applied to a copy-backed working tree and backed out
immediately. In each case the whole suite was run and the named test failed; `git status --short`
was empty afterwards and the suite returned to 87 passing.

| for | mutation | test that failed |
|-----|----------|------------------|
| AC1 | `add_card` writes a fixed `"2099-01-01"` instead of `when` | `test_schedule.NewCardTest.test_a_new_card_is_due_the_day_it_is_added_and_is_presented` (and twelve `test_review` tests besides) |
| AC2 | `next_interval` returns `LADDER[position]` — a right answer stays put | `test_schedule.RightAnswerTest.test_a_right_answer_moves_the_card_up_one_rung` at rungs 1, 3 and 7, plus `.test_the_new_date_is_measured_from_the_review_and_not_from_the_old_due` |
| AC3 | a wrong answer returns `current` instead of `LADDER[0]` | `test_schedule.WrongAnswerTest.test_a_wrong_answer_returns_the_card_to_the_bottom_rung_from_any_rung` at rungs 3, 7 and 30, plus `.test_climbing_back_starts_from_the_bottom_rung_not_from_where_it_was` |
| AC4 | the `` | `interval` | `` row deleted from `README.md`'s card-field table | `test_docs.ReadmeTest.test_the_readme_card_field_table_has_a_row_for_the_rung_field` — **and nothing else**, which is the gap the first verification recorded, now closed |
| AC4 | the ladder line `**1 day → 3 days → 7 days → 30 days.**` replaced | `test_docs.ReadmeTest.test_the_readme_names_the_ladder_and_the_field_that_carries_it` |
| AC5 | `save` strips `interval` from every card before writing | `test_schedule.PersistenceTest.test_the_schedule_survives_ending_and_restarting_the_program` |
| AC6 | `add_card` writes `"interval": 1` — a new card starts **on** the bottom rung | `test_schedule.NeverAnsweredCardTest.test_a_new_cards_first_right_answer_schedules_it_one_day_out` and `.test_four_right_answers_reach_the_top_rung_not_three` |
| AC7 | the card in hand is recorded when the session ends early | `test_review.ReviewTest.test_ac5_q_at_the_answer_side_records_nothing_for_that_card` |
| AC8 | `load` no longer does `card.setdefault("interval", None)` | `test_schedule.OlderStoreTest.test_the_next_write_carries_the_rung_field_on_every_card_it_holds` and `test_store.StoreTest.test_a_version_1_store_is_read_and_upgraded_by_the_next_write` |
| AC9 | `_is_date` drops the round trip (`return True`) | `test_schedule.UnreadableSchedulingValueTest.test_an_unpadded_due_stops_the_tool_rather_than_dropping_the_card`, all three commands |
| AC9 | the `isinstance(..., bool)` guard removed from `load` | `test_schedule.UnreadableSchedulingValueTest.test_a_rung_of_json_true_stops_the_tool`, all three commands |

AC7's mutation is worth a note: the test that caught it belongs to WI-0002, not to this item's
new suite. This item's own `UnreachedCardTest` asserts the unreached card's rung and date, which
that mutation does not disturb — it touches the card the session *was* on. The behaviour is
covered, but by an older test; recorded so it is visible rather than implied.

## Defects found

**None.** Nothing was sent back and no bug item was filed.

The two defects of the first verification are closed at this commit, and each was re-run here
rather than taken on trust. Nothing was found in the diff that no criterion, plan step or
declared deviation explains: `git diff main..HEAD` on `recall.py` is plan steps 1–6 plus the two
pass-2 fixes to `load`, and on `README.md` is steps 7 and 8 plus the `## Not yet built` rewrite
that `impl-report.md` declares as deviation 2. The four deviations were read and each traces to a
plan step or to its own stated reasoning.

Two things were **looked at and deliberately not filed**, because no criterion of this item covers
them and neither is a defect in behaviour delivered elsewhere:

- `due_cards` still compares `due` as a string rather than as a date. That is the underlying
  reason an unpadded date was dangerous, and `load` refusing the value is what AC9 asks for. The
  string comparison is correct for every value `load` now admits, because they are all canonical
  and zero-padded — checked at the edges with `"0999-01-01"` and `"9999-12-31"`. There is nothing
  to file.
- `cmd_review` saves the whole document after each card. Unchanged from WI-0002, no criterion here
  touches it, and it caused nothing observed in this verification.

## Not verified, and why

- **Behaviour across a real change of date.** Everything was run on one day, `2026-08-29`, with
  later and earlier dates simulated by hand-editing `due` — the mechanism the criteria themselves
  prescribe. A card genuinely left alone for 30 days was not observed and no criterion asks for
  it.
- **Timezones and clock changes.** `due` is a local date with no zone; `ADR-0006` records that as
  a known limitation and the item puts it out of scope, so it was not probed. Unchanged from the
  first verification.
- **Stores larger than two cards, and concurrent processes.** No criterion covers either. AC7 was
  checked at two cards, AC8 at two.
- **Exhaustiveness of the AC9 probe.** Thirty malformed stores were tried, chosen to attack the
  ways a value can be wrong — wrong type, wrong shape, wrong position in the file, and equal-but-
  not-identical to a ladder value. That is a broader net than the first pass and it caught the one
  remaining class (JSON floats, argued above), but it is a search, not a proof. What can be stated
  is narrower: of everything tried, only values that are genuinely the documented ones are
  accepted.
- **`recall add` against a store that is unreadable for a reason other than these two fields.**
  Covered by WI-0001 and WI-0002 and not re-run here; AC9's three commands were exercised only
  against scheduling-value faults, which is what the criterion asks for.

## Appendix — the first verification, condensed

The full report is the version of this file at commit `9cda720`; both defects are reproduced in
full in `impl-report.md` `## Second pass`. In summary, at `eb4cc23` it ticked AC1–AC8 and failed
AC9 on two counts, both found by probing values AC9 does not name:

1. **D1 — `interval: true` was accepted as the 1-day rung.** `True == 1` in Python, so a JSON
   `true` passed the membership test and the card was silently put on a rung the user never
   wrote.
2. **D2 — `due: "2026-8-9"` was accepted and the card was never due again.** `strptime` takes
   unpadded fields, but `due_cards` compares `due` as a string, so the value sorted above every
   zero-padded date: listed by `recall list`, never presented by `recall review`, nothing
   printed. WI-0002's handed-forward defect in a second spelling.

It also recorded, as a gap rather than a failure, that deleting `README.md`'s `interval` table row
left all 82 tests green — AC4's card-field-row clause was untested. Both defects and the gap are
closed at `f841f09`, each re-checked here.
