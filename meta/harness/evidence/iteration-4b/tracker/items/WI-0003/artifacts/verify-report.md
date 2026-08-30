# Verification report — WI-0003

Verified-commit: c2c547ac34e7e956ff84c2dd459fc82400050ee0

## Verdict

**Pass.** All six acceptance criteria are met, each demonstrated by a command run against
`bin/recall` on the branch head, in a temporary `HOME`, with the actual output recorded below.
No criterion was ambiguous, no defect was found, no bug item was filed, and nothing was waived.
All six checkboxes in `item.md` are now ticked.

What was checked was derived from the criteria before the implementation report was consulted:
each criterion states a procedure, and the procedure below is that procedure, run with a real
here-document where the criterion says a here-document drives it.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `HOME=$(mktemp -d)`, deck file confirmed absent, then `recall add --question "capital of France" --answer "Paris"`, then five cycles of: rewrite **only** `due` to today, `recall review <<'H'\n\ny\nH` | `Added. The deck now holds 1 card(s).` then, sitting by sitting, `stored due = 2026-08-31 = today + 1`, `2026-09-02 = today + 3`, `2026-09-06 = today + 7`, `2026-09-29 = today + 30`, `2026-09-29 = today + 30` | The card as `add` wrote it was `{"question": …, "answer": …, "rung": 0, "due": "2026-08-30"}`; only `due` was rewritten between sittings. The fifth sitting is the criterion's point and it holds at thirty — there is no fifth rung. |
| AC2 | **pass** | (a) fresh card, `recall review` answering `n`. (b) four cycles answering `y`, then a cycle answering `n`, then a cycle answering `y` | (a) `stored due = 2026-08-31 = today + 1`. (b) `after four right answers: today + 30`; `answered WRONG -> today + 1`; `then answered RIGHT -> today + 1` | (b) is the observation that separates the shipped rule from the placeholder: a tool that moved the date and left the ladder position alone would have written today + 30 on the last line. |
| AC3 | **pass** | Deck file written by hand with one card, `rung: 0`, `due` = 2026-08-20 (ten days before today), then `recall review` — once answering `y`, once answering `n` | Both runs: `overdue-q` presented, then `next review: 2026-08-31 (in 1 day)`, and `stored due = 2026-08-31 = today + 1`. The rejected reading would have given today − 9 | Both halves of the criterion in one run each: the card is still presented (`WI-0002` AC13), and the gap is counted from the day of the sitting. |
| AC4 | **pass** | Read out of AC1's and AC2's runs, plus a two-card sitting: deck with `q-one`/`q-two` both due today, `recall review` answering `y` twice | AC1's sittings printed `next review: 2026-08-31 (in 1 day)`, `2026-09-02 (in 3 days)`, `2026-09-06 (in 7 days)`, `2026-09-29 (in 30 days)` — two different gaps, so a constant fails. AC2(b)'s wrong answer printed `next review: 2026-08-31 (in 1 day)`. Two-card run printed, in order: `q-one`, `a-one`, `next review: 2026-08-31`, `q-two`, `a-two`, `next review: 2026-08-31` | Each printed date equals the string then found in that card's `due`. The date's form is `YYYY-MM-DD` as the criterion fixes. Placement is after that card's answer side and before the next card's question side. |
| AC5 | **pass** | Read `docs/process/using-recall.md` v5, sections `## When each card comes back` and `## What this version does not do yet` | All five facts present: the gaps (*"1 day, then 3 days, then a week, then 30 days"*), the hold (*"stays at 30 days — the gap never grows past a month, and there is no rung above it"*), the reset (*"goes back to the start of the ladder: it is due again the day after the sitting"*), the counting rule (*"Both gaps are counted from the day of the sitting, never from the day the card was due"*), and the worked example (*"due on days 0, 1, 4, 11, 41, 71 and 101"*, with the wrong-answer clause after it). `## What this version does not do yet` contains neither "Scheduling is not built yet" nor "comes back tomorrow" | A reader following only that section derives 1, 3, 7, 30 and 30 — the dates AC1 to AC3 observed. One wording note, not a failure: the third gap is written *"a week"* rather than *"7 days"*. It is unambiguous, and the worked example gives the arithmetic explicitly (4 → 11). |
| AC6 | **pass** | The per-criterion read below, with commands run for each group and the suite as evidence | `python3 -m unittest discover -s tests -t . -q` → exit 0, **43 tests**; plus the hand runs quoted in the read | Every one of the twenty-two criteria is still true of the shipped behaviour. Nothing was waived, and no non-intersection was found. |

## AC6 — the twenty-two criteria, read by ID against what shipped

This criterion's subject is other criteria, so the assessment is a **read of each sentence
against the new behaviour**, with commands as evidence for the answer rather than as its
definition. Every criterion covered is named by ID.

**`WI-0001` AC1–AC9.** This item does not touch `cmd_add` or `cmd_list`, but it does change the
load path both of them go through, so a read of each is owed rather than assumed.

- **AC1** (add exits 0, list shows one more) — **true**. Run: `recall list` on an empty deck, two
  `recall add`s, `recall list`. Output went from `The deck is empty…` to two card lines.
- **AC2** (a blank or missing side refused, deck byte-identical) — **true**. Run:
  `recall add --question "" --answer a` → `recall add: refusing -- --question must be given and
  must not be blank. The deck was not touched.`, exit 2, and `recall list` before and after was
  byte-identical.
- **AC3** (both sides shown exactly as given) — **true**, and `ADR-0007` §4 keeps `cmd_list`
  unchanged deliberately. Run: a card added with the question `"  spaced  q  "` and answer
  `"MiXeD Case"` lists as `  spaced  q   | MiXeD Case` — leading and trailing spaces and case
  intact. Exercised *together with* the new behaviour by
  `ReviewTests.test_a_sitting_disturbs_nothing_else`, which lists before and after a sitting that
  now also reschedules, and by hand: `list before` and `list after` a two-card sitting were
  identical.
- **AC4** (persistence across processes) — **true**, and this item leans on it harder than
  anything before: AC1's five sittings are five separate processes, each reading back what the
  previous one wrote.
- **AC5** (first run creates the file and its parent) — **true**. AC1's run began with the deck
  file and its directory absent and `recall add` created both.
- **AC6** (empty deck says so, exit 0) — **true**. Run: a deck file of `{"version": 1,
  "cards": []}` → `The deck is empty. Add a card with: recall add --question "..." --answer
  "..."`, exit 0.
- **AC7** (one file, under home, not boot-cleared) — **true**. Run: after AC1's whole five-sitting
  walk, `find $HOME -type f` returned exactly `$HOME/.local/share/recall/deck.json` — the
  per-sitting atomic saves leave no temporary file behind.
- **AC8** (an unreadable deck is refused and left alone) — **true**, and this item *adds* a case
  to it rather than weakening it. Run: the classic truncated deck `{"cards": ` →
  `recall: cannot read the deck file … -- it is not valid JSON (Expecting value, line 1)…`,
  exit 3, bytes identical. The new case is boundary 5 below.
- **AC9** (duplicates allowed) — **true**. Run: the same question added twice with different
  answers listed as two cards.

**`WI-0002` AC1–AC13.** This is the subcommand the item changes, so every criterion here was
re-run rather than reasoned about.

- **AC1** (one at a time, question before answer, each question once) — **true**. The two-card run
  under AC4 shows `q-one`, `a-one`, the date line, `q-two`, `a-two`, the date line. The new line
  carries no card text, so no question side appears twice.
- **AC2** (the answer is not shown until asked for) — **true**. Run: one due card, standard input
  closed immediately → stdout has `q-one` and the reveal prompt, and neither `a-one` nor any date
  line.
- **AC3** (an unrecognised response re-asks the same card) — **true**. Run: `\nmaybe\ny\n` →
  `I did not understand that. Answer 'y' for right or 'n' for wrong.`, then the same grade prompt
  again, then exactly one date line after the recognised response.
- **AC4** (a card due later is not presented) — **true**. Run: a deck of `due-now` (today) and
  `due-later` (today + 7) → only `due-now` presented, exit 0.
- **AC5** (nothing due says so, exit 0) — **true**. Run: an all-future deck →
  `Nothing is due today. Come back tomorrow.`, exit 0. The criterion names the message by
  reference to the documentation, and `docs/process/using-recall.md` v5 still quotes that
  sentence verbatim.
- **AC6** (absent deck: the same message, nothing created) — **true**. Run: empty `HOME` →
  the same sentence, exit 0, `find $HOME -type f` empty and `~/.local/share/recall` still absent.
- **AC7** (an unreadable deck is refused by `review` too) — **true**; the same run as `WI-0001`
  AC8, plus boundary 5.
- **AC8** (a card finished in one sitting is not presented again the same day) — **true**, and
  this is one of the four the criterion names. Every gap this item can produce is at least one
  day: the right branch applies `LADDER[rung]`, whose smallest element is 1, and the wrong branch
  applies `LADDER[FIRST_RUNG]` = 1. Run: `recall add`, a sitting answering `y`, then a second
  sitting the same day → `Nothing is due today. Come back tomorrow.`
- **AC9** (a sitting stopped part-way keeps the answers given) — **true**. Run: two due cards,
  input for the first only → the first card graded and its date line printed, the second card's
  reveal prompt then end of input, exit 0 and no traceback; a second sitting the same day
  presented `q-two` and not `q-one`.
- **AC10** (nothing outside the sitting is disturbed) — **true**, and one of the four named. Run:
  `recall list` before and after that sitting produced the identical two lines
  `q-one | a-one` / `q-two | a-two`. The grade is still recorded per `ADR-0006`: `record_answer`
  still sets it, and the unit tests assert it on every rung.
- **AC11** (no cap on a sitting) — **true**. Run: twenty-five due cards →
  `questions presented: 25 / 25` and `next-review lines: 25 / 25`, so the new line is printed once
  per graded card and nothing was dropped.
- **AC12** (a card added today is due today) — **true**. Run: `recall add`, then `recall review`
  as a second process the same day → the card presented.
- **AC13** (an overdue card is still presented) — **true**, and one of the four named.
  `due_positions` is untouched by this item. Run: AC3's ten-days-overdue card was presented on
  both answers.

**Non-intersection: none found.** For every one of the twenty-two criteria there is something
executable that exercises it *and* runs the new behaviour: `WI-0001` AC1–AC9 all go through the
changed `store.load`, and `WI-0002` AC1–AC13 all go through the changed `cmd_review` and
`record_answer`. Nothing is waived.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` on `c2c547a` with a clean working tree → exit 0, `Ran 43 tests … OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → exit 0, no output |
| `workspace-valid` | **pass** | `validate-workspace .` → `checked 6 item(s), 11 document(s)`, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | Every row of the criteria table names a command this skill ran and quotes its actual output. No row cites `impl-report.md` |
| `negative-cases-exercised` | **pass** | Six boundary conditions triggered, listed below |
| `a-criterion-about-criteria-is-read` | **pass** | AC6's read above names all twenty-two criteria by ID with a per-criterion verdict taken from their text; non-intersection was looked for and none was found; nothing waived |
| `tests-would-fail-without-the-change` (advisory) | **pass** | Six mutations run and reverted, below |

## Negative and boundary cases exercised

1. **A sitting abandoned at the reveal.** One due card, standard input closed immediately.
   → question shown, answer not shown, **no date line**, exit 0, stored `due` still today.
2. **A sitting abandoned at the grade prompt.** Reveal, then end of input.
   → answer shown, **no date line**, exit 0, stored `due` still today. The line belongs to a card
   that was graded, and neither of these graded one.
3. **An unrecognised grade response.** `\nmaybe\ny\n` → the expectation restated, the same card
   asked again, then exactly one date line.
4. **Nothing due.** An all-future deck → `Nothing is due today. Come back tomorrow.`, exit 0.
5. **A stored `rung` outside the ladder** — `-1`, `4` and `9`, each against `recall list` and
   `recall review`. Every one:
   `recall: cannot read the deck file … -- card 1's 'rung' is not a rung on the ladder (it must
   be 0 to 3). Nothing has been written and the file is exactly as it was…`, exit 3, and the
   deck's sha256 identical before and after. Refused, never clamped (`ADR-0008` §6).
6. **A classic malformed deck** (`{"cards": `) → still refused with the JSON message, exit 3,
   bytes identical. The new check did not displace the old ones.

## Test sensitivity check

Six mutations, each applied to the branch head, the suite run, then reverted. The suite was
confirmed green again afterwards.

| mutation | tests that failed |
|----------|-------------------|
| M1 — `record_answer` reverted to the placeholder (tomorrow, `rung` untouched) | `test_a_correct_answer_walks_the_ladder_and_then_holds` (AC1), `test_a_wrong_answer_resets_the_ladder_and_not_only_the_date` (AC2), `test_the_sitting_prints_the_new_date_at_two_gaps_and_on_both_answers` (AC4), and both new unit tests |
| M2 — the gap counted from `card.due` instead of the day of the sitting | exactly `test_an_overdue_card_is_scheduled_from_the_day_of_the_sitting` (AC3) and `test_record_answer_counts_from_the_sitting_not_from_the_due_date` |
| M3 — the top-rung cap removed (`min` dropped) | `test_a_correct_answer_walks_the_ladder_and_then_holds` (AC1), plus three others |
| M4 — the printed next-review line deleted | `test_the_sitting_prints_the_new_date_at_two_gaps_and_on_both_answers` and `test_the_date_comes_after_that_cards_answer_and_before_the_next_question` (AC4), and nothing else |
| M5 — the `rung` range check removed from `store.load` | `test_a_rung_outside_the_ladder_is_refused_like_any_other_bad_field` |
| M6 — `docs/process/using-recall.md` reverted to `main`'s version | `test_the_documentation_states_the_rule_and_the_worked_example` (AC5) |

Every criterion has at least one test that fails when its behaviour is removed. M2 is the one
worth keeping: AC3's tests are the **only** two that catch a gap counted from the due date, and
they do not fail under M1 — a placeholder that always says "tomorrow" is accidentally right about
an overdue card. Without AC3 that reading would have shipped unnoticed.

## Diff read against the plan

`git diff main..HEAD` is three source files, two test files, two documents and the tracker.
Every source hunk traces to a plan step: `LADDER` and `record_answer` to steps 1 and 2,
`days_until` to step 4's explicitly-open interface note, the `store.py` range check to step 3,
`NEXT_REVIEW_LINE` and `_next_review_line` to step 4, the test changes to steps 5 and 6,
`using-recall.md` to step 7 and `overview.md` to step 8. **No unaccounted hunk, and no behaviour
that no criterion and no plan step asks for.**

Two things in the diff are `plan.md`'s assumptions rather than any criterion, and both are
declared there: the words around the date in the printed line (`  next review: <date> (in N
day(s))`, `## Assumptions` 1–2) and the line being printed after the save rather than before it
(`## Assumptions` 3). Behaviour 3 was checked: a sitting that grades nothing prints nothing
(boundary cases 1 and 2).

## Defects found

**None.** No send-back, and no bug item filed.

`BUG-0001` remains open and untouched, which is correct: a filesystem error other than
`DeckUnreadable` on the deck file still reaches the person as a traceback, no criterion of this
item covers it, and this item did not widen to absorb it. The new `DeckUnreadable` from an
out-of-range `rung` travels `ADR-0004` §5's existing route and is reported the same way as every
other unreadable deck — confirmed by boundary case 5, which produced a message and exit 3, not a
traceback.

## Not verified, and why

- **The worked example's later days — 41, 71 and 101 — were not observed at real calendar
  distance.** No criterion asks for that and it would take a hundred days. What was observed is
  the arithmetic that produces them: five sittings giving gaps 1, 3, 7, 30, 30, which is exactly
  the sequence 0 → 1 → 4 → 11 → 41 → 71 → 101. The compression is faithful because the gap is
  counted from the day of the sitting, which AC3 verified independently.
- **A card whose `due` is far in the future being brought forward** is not a case this item has:
  nothing rewrites `due` except a graded answer. Not verified because nothing to verify.
- **`docs/architecture/overview.md`'s claim that the load path serves "`add`, `list` and, later,
  `review`"** is stale — `review` shipped with `WI-0002`. `impl-report.md` declares it and leaves
  it. It is outside this item's D12 scope (the staleness is about `review` existing, not about
  scheduling), it misleads nobody about behaviour, and it is a one-line correction for whoever
  next opens that file. Recorded here so it is not lost.
- **Independence, stated plainly.** This verification and the implementation it checks were
  performed in the same session by the same agent under different personas, which is how this
  pipeline is built. The mitigation used was procedural rather than organisational: every check
  above was derived from the criterion's own text and run as a fresh command against
  `bin/recall`, and no row of the criteria table takes `impl-report.md` as its evidence. A reader
  who wants to re-derive the verdict can run the commands quoted here.
