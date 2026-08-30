# Verification report — WI-0002

Verified-commit: c50694d40bb4e7074b9a768494571656309ecfc6

## Verdict

**Pass.** All thirteen acceptance criteria hold. This is the **second** verification of this item:
the first passed at `b51c502c`, `review-close` then rejected the item on **D12** — a claim in
`docs/process/using-recall.md` that the code does not support — and `implement` answered that
rejection in `d479eac..c50694d`. This report supersedes the first, which is preserved in git
(`git show f15d122:tracker/items/WI-0002/artifacts/verify-report.md`) and whose claims audit is
quoted in `artifacts/review.md`.

**Every criterion was re-demonstrated from scratch by this execution**, not carried over. The
reason is not ceremony: three criteria — AC3, AC5 and AC6 — name their expected output by
reference to *"the tool's own documentation"*, and the document is precisely what changed. A
verification that reused the earlier evidence would be checking those three against a version of
the document that no longer exists.

Every verdict below comes from driving the real `recall` executable from a scratch home directory
with a here-document or a redirected file on standard input — the invocation form the criteria
are written against (`ADR-0001` §4). The developer's suite was run too, but as evidence *beside*
these checks. **No verdict rests on `impl-report.md`.**

The documentation standard for AC3, AC5 and AC6 was read at this head **before any command was
run**. `docs/process/using-recall.md` v4 §"Doing a review" names the two responses as **`y` and
`n`** (line 61) and the nothing-due line as **`Nothing is due today. Come back tomorrow.`**
(line 79).

## Criteria

Scratch homes are under `/tmp/vfy/`; `W` is the checkout. Decks needing a particular date were
written directly, as the criteria's preamble permits.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | deck of `q-one`/`q-two`/`q-three` all due today; `HOME=/tmp/vfy/h1 $W/bin/recall review` driven by six input lines | exit 0. stdout: `q-one` / `[press return…] a-one` / `did you get it right? [y/n] q-two` / … / `a-three`. Indices computed in Python: `{q-one:0, a-one:43, q-two:79, a-two:122, q-three:158, a-three:203}` | question precedes answer for all three (`True True True`); card *n* finishes before card *n+1* starts (`True True`); each question side occurs exactly **1** time |
| AC2 | **pass** | one due card `die Katze`/`the cat`; `recall review < /dev/null` | exit 0. stdout is `die Katze` then `  [press return to see the answer] ` and nothing more | `grep -c 'die Katze'` = 1, `grep -c 'the cat'` = **0**. The answer is not shown |
| AC3 | **pass** | two due cards; input `\n maybe \n y \n \n y` | exit 0. stdout carries `I did not understand that. Answer 'y' for right or 'n' for wrong.` between two grade prompts | `first-q` occurs exactly 1 time; **2** grade prompts appear before `second-q` (prompt indices 55, 153; `second-q` at 181), so the *same* card was re-asked and the second card did not appear until `y` arrived; stored deck shows `"grade": "right"` on card 1. The two responses named match the documentation read above |
| AC4 | **pass** | deck with `due-now` today and `due-later` at today+7; input `\n y` | exit 0. stdout: `due-now` / `a` / grade prompt only | `grep -c 'due-later'` = **0** |
| AC5 | **pass** | deck whose two cards are both at today+7; `recall review < /dev/null` | exit 0. stdout is exactly `Nothing is due today. Come back tomorrow.` | the documented line, present once; neither question side appears; stderr empty |
| AC6 | **pass** | empty home, deck file and parent directory both absent; `recall review < /dev/null` | exit 0. stdout `Nothing is due today. Come back tomorrow.` | before: neither exists. after: neither exists, and `find /tmp/vfy/h6 -mindepth 1` returns **0 entries**. `diff` against AC5's stdout: **identical** — the *same* message, as the criterion requires |
| AC7 | **pass** | eight damaged decks in turn, each with `sha256sum` before and after; `recall review < /dev/null` | all eight exit **3**; each stderr begins `recall: cannot read the deck file /tmp/vfy/h7/.local/share/recall/deck.json -- …`; stdout empty in all eight | cases: not JSON; truncated JSON; `cards` not a list; a missing required key; `due` not a date; `"grade": "maybe"`; `"grade": null`; empty file. Each names the path, presents no card, exits non-zero, leaves bytes identical, and **does not** print the nothing-due line |
| AC8 | **pass** | one due card graded `y` in a first process; a second `recall review < /dev/null` as a new process | run 1 exit 0; run 2 exit 0 with stdout `Nothing is due today. Come back tomorrow.` | `grep -c 'survivor-q'` on run 2 = **0** |
| AC9 | **pass** | two due cards; input for the first only (`\n y`), then EOF; then a second run | run 1 exit 0, **stderr empty**, `grep -c Traceback` = 0; run 2 stdout is `pending-q` … | run 2: `pending-q` present (1), `kept-q` absent (0) — the answer given before the stop was kept and the unanswered card is still waiting |
| AC10 | **pass** | `recall list` captured before and after a full two-card sitting (`y` then `n`) | before and after are both `alpha q \| alpha a` / `beta q \| beta a`; `diff -q` → **identical** | the stored deck afterwards shows both cards' `question`/`answer` untouched and only `grade` and `due` changed |
| AC11 | **pass** | twenty-five cards `cap-q000`…`cap-q024`, all due; fifty input lines | exit 0; distinct question sides on stdout = **25 of 25**, first `cap-q000`, last `cap-q024` | a cap set at exactly 25 would satisfy the criterion as written, so a **60**-card deck was run as well: exit 0, **60 of 60** distinct question sides |
| AC12 | **pass** | absent deck; `recall add --question brand-new-q --answer brand-new-a`, then `recall review < /dev/null` as a second process | add: `Added. The deck now holds 1 card(s).`, exit 0. review: exit 0, stdout `brand-new-q` then the reveal prompt | `grep -c 'brand-new-q'` = 1 |
| AC13 | **pass** | one card dated today−7; input `\n y` | exit 0; stdout `overdue-q` / `c` / grade prompt | `grep -c 'overdue-q'` = 1 — an overdue card is still presented |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → `Ran 32 tests in 3.429s` / `OK`, exit 0, run by this skill on head `c50694d` |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → `checked 6 item(s), 9 document(s)` / `0 errors, 0 warnings`, exit 0 |
| `every-criterion-independently-checked` | **pass** | the thirteen rows above; every one is a command this execution ran with its output quoted. None cites `impl-report.md` |
| `negative-cases-exercised` | **pass** | the section below — eleven conditions triggered, not read about |
| `a-criterion-about-criteria-is-read` | **pass (vacuous, and stated rather than assumed)** | see below |
| `tests-would-fail-without-the-change` (advisory) | **pass** | sixteen mutations, below; every criterion has at least one test that fails when its behaviour is removed |

### `a-criterion-about-criteria-is-read`

**No criterion of WI-0002 has other criteria as its subject.** AC1–AC13 were each read for that
shape; every one is written over the tool's observable behaviour, and none says "the earlier
criteria still hold". The gate is therefore **vacuous on this item**, and it is recorded as
vacuous rather than as satisfied by something else.

The thing the gate exists to catch was checked anyway, in its own words: **nothing executable
exercises WI-0001's criteria and a *graded* deck together**, because every WI-0001 test builds
its deck through `recall add`, which never writes a `grade`. A covering test is **waived by
name** — `tests/test_add.py` and `tests/test_list.py` would each need a hand-written graded
fixture to add a case that only re-checks WI-0001's own criteria, which are already covered, and
`ADR-0006` §2 makes the new key optional on read specifically so that this intersection is
uninteresting. Instead the intersection was run by hand, against `/tmp/vfy/h10` whose two cards
carry `"right"` and `"wrong"`:

- **WI-0001 AC1** — `recall add --question "capital of France" --answer "Paris"` → `Added. The
  deck now holds 3 card(s).`, exit 0. Holds.
- **WI-0001 AC2** — `recall add --question "   " --answer "x"` → `recall add: refusing --
  --question must be given and must not be blank. The deck was not touched.`, exit 2. Holds.
- **WI-0001 AC3** — `recall list` → all cards, both sides, in order. Holds.
- **WI-0001 AC9** — a second card with the same question side is accepted; `recall list` shows
  both. Holds.
- After all four, the graded cards still read `('alpha q', 'right', 2)` and
  `('beta q', 'wrong', 0)` — the grades and rungs survived every WI-0001 operation.

## Negative and boundary cases exercised

Each was **triggered** by a command this execution ran.

1. **EOF at the reveal read** (AC2) — `recall review < /dev/null` with one due card. Exit 0, the
   answer never printed.
2. **EOF at the grade read** (AC9) — input for the first card only. Exit 0, stderr empty, no
   traceback, the answer already given kept.
3. **Eight damaged decks** (AC7) — not JSON, truncated JSON, `cards` not a list, a missing
   required key, `due` not a date, `"grade": "maybe"`, `"grade": null`, and an empty file. All
   exit 3, name the path, print nothing to stdout, and leave the bytes identical. The two
   `grade` cases are the format surface this item added, and `null` is the one `plan.md` step 3
   left unaddressed and `ADR-0006` §3 settles.
4. **An unrecognised response** (AC3) — `maybe`. Re-asked the same card.
5. **A superstring of a recognised response** — `yes`. **Rejected** (2 grade prompts, the
   unrecognised message printed once). A prefix matcher would have accepted it; this one does
   not.
6. **A bare empty line at the grade prompt** — what a person produces by pressing Return.
   **Rejected**, same shape.
7. **Case and surrounding whitespace** — `  Y  `. **Accepted** first time, stored as `right`,
   which is what the documentation promises.
8. **The due boundary in three places** — today−7 (presented, AC13), today (presented), today+7
   (not presented, AC4).
9. **An empty deck with no file and no parent directory** (AC6) — nothing created, verified with
   `find`.
10. **A sitting larger than the criterion's witness** — 60 due cards, all presented.
11. **A card at a non-zero rung** — `/tmp/vfy/h10`'s `alpha q` was written at `rung: 2` on
    purpose, so that "the ladder position does not move" could fail visibly if it were false.

## Test sensitivity check

Sixteen mutations, each applied to the source, the suite run, and the source restored from the
in-memory original. Every criterion has at least one test that fails when its behaviour is
removed. The suite is `OK` and `git status` is clean after the sweep.

| mutation | criterion | tests that failed |
|----------|-----------|-------------------|
| every question side printed twice | AC1 | `test_due_cards_are_presented_one_at_a_time`, `test_an_unrecognised_response_re_asks_the_same_card` |
| answer printed before the reveal read | AC2 | `test_answer_is_not_shown_until_it_is_asked_for` |
| any response accepted as `right` | AC3 | `test_an_unrecognised_response_re_asks_the_same_card` |
| every card treated as due | AC4 | `test_a_card_due_later_is_not_presented`, `test_nothing_due_says_so_and_exits_zero`, `test_due_positions_is_on_or_before_today_in_deck_order`, +2 |
| nothing-due message removed | AC5, AC6 | `test_nothing_due_says_so_and_exits_zero`, `test_absent_deck_reports_nothing_due_and_creates_nothing` |
| the deck saved on the nothing-due path | AC6 | `test_absent_deck_reports_nothing_due_and_creates_nothing` |
| an unreadable deck quietly becomes an empty one | AC7 | `test_unreadable_deck_is_refused_and_left_alone` |
| the answer never recorded | AC8, AC9 | `test_an_answer_survives_the_process_ending`, `test_a_sitting_stopped_part_way_keeps_the_answers_given`, `test_an_unrecognised_response_re_asks_the_same_card` |
| deck saved once at the end instead of per card | AC9 | `test_a_sitting_stopped_part_way_keeps_the_answers_given` |
| `record_answer` rewrites the question side | AC10 | `test_a_sitting_disturbs_nothing_else`, `test_record_answer_keeps_the_card_and_moves_it_off_today` |
| the sitting capped at twenty cards | AC11 | `test_a_sitting_is_not_capped` |
| a card added today dated tomorrow | AC12 | `test_a_card_added_today_is_due_today`, +2 |
| due means exactly today | AC13 | `test_an_overdue_card_is_still_presented`, `test_due_positions_is_on_or_before_today_in_deck_order` |

Three further mutations were attempted with a wrong source string and reported
`MUTATION DID NOT APPLY (0 matches)` rather than silently passing — they were rewritten against
the real text of `due_positions` and re-run, and are the AC4/AC11/AC13 rows above. Recorded
because a mutation that does not apply looks exactly like a mutation nothing catches.

**A sensitivity note, kept rather than smoothed over:** the AC1 mutation is caught by AC1's own
test *and* by AC3's. That is fine. But AC3's mutation is caught only by AC3's test and AC1's
mutation only by two tests that both assert occurrence counts — so the "each question side
appears exactly once" rule is what is really under test in both places, and a defect in
presentation *order* that preserved the counts would be caught by
`test_due_cards_are_presented_one_at_a_time` alone.

## The change under verification

The item was sent back for one thing, so the change itself was read as well as the criteria.
`git diff b51c502..c50694d -- recall tests` is **four lines moved in `recall/cli.py`, all of them
comment**: the `#:` block stating that neither prompt may carry the card's text, relocated from
above `RIGHT_RESPONSE`/`WRONG_RESPONSE` to above `REVEAL_PROMPT`/`GRADE_PROMPT`. No string, no
constant, no branch. That is review finding F2, and the AC1 mutation above confirms the guard it
describes is still enforced by a test after the move.

The other change is the document, and it is the whole reason for the send-back. The corrected
paragraph was audited the way `review-close` audited the one it replaced — **from the citations,
not from the prose** — and against the decks this verification produced:

| claim | opened / demonstrated | verdict |
|-------|----------------------|---------|
| a card comes back tomorrow whether right or wrong | `/tmp/vfy/h10` after `y` then `n`: both cards `"due": "2026-08-31"` | supported |
| answers are written into the deck file against the cards as you give them `[src: ADR-0006]` | `ADR-0006` §1 (`grade` records the most recent answer) and §4 (written only when set); demonstrated by AC3's and AC10's stored decks, and by AC9 where the answer given before the stop was on disk | supported |
| nothing reads them back yet; `record_answer` leaves the ladder position exactly as it was `[src: recall/deck.py:92]` | `recall/deck.py:92–102` is `dataclasses.replace(card, grade=…, due=today+1)`; `grep -rn "\.grade" recall/` finds reads only in `store._card_to_entry`'s serialisation | supported |
| every card is still on the bottom rung `recall add` put it on `[src: recall/deck.py:73]` | `new_card` sets `rung=FIRST_RUNG`; `grep -rn rung recall/` shows the only other mentions are `store`'s round-trip. **See the observation below** | supported, with one qualification |
| that is where it will start climbing from when the ladder lands | follows from the row above; hedged on WI-0003 landing, and `ADR-0006`'s consequences say WI-0003 changes `rung` and `due` | supported |

## Defects found

**None.** No criterion of this item fails, so there is no send-back, and no bug item was filed —
nothing here is a defect in behaviour another item delivered.

One **observation**, recorded rather than raised, because `review-close` owns D12 and should see
that it was looked at rather than missed:

**O1 — "every card is still on the bottom rung `recall add` put it on" is true of every card the
tool creates, and not of a card someone hand-edited.** `store` round-trips whatever integer
`rung` the file holds — this verification wrote a card at `rung: 2` by hand and it stayed at 2 —
and `ADR-0004` chose JSON partly so a person *can* open the deck in an editor. So the sentence's
first clause is defeasible by hand-editing. It is recorded as an observation and not as a
finding because (a) `recall add` is the only way the tool itself makes a card and it always uses
`FIRST_RUNG`, (b) the sentence's operative promise — *"that is where it will start climbing from
when the ladder lands"* — stays true for a hand-edited card too, and (c) a person who set a rung
by hand is not the person the sentence could mislead. If `review-close` reads it more strictly,
the fix is one word (*"every card `recall add` made"*), not a redesign.

## Not verified, and why

- **What WI-0003 will actually do with `rung` and `grade`.** The corrected paragraph says a card
  will start climbing from where it is now. That is a claim about an item not yet built, and no
  command can settle it here; it rests on `record_answer` leaving `rung` alone, which *was*
  demonstrated, plus `ADR-0006`'s consequences. If WI-0003 is planned differently, this sentence
  is the one to revisit.
- **A sitting spanning midnight.** `datetime.date.today()` is read once per process with no
  injectable clock (`plan.md` §Assumptions), so a sitting that crosses midnight is unexercised.
  No criterion covers it. A suite started in the last seconds before midnight can flake; that is
  a re-run, not a defect.
- **`BUG-0001`'s territory.** Filesystem errors that are not deck-*content* problems — a
  permission denial, a directory where the deck file should be — were **not** exercised, on
  purpose. AC7 is about content, `BUG-0001` is already open at `ready` against `add` and `list`
  for the rest, and this item's `## Out of scope` excludes it. **A passing AC7 is not evidence
  about `BUG-0001`.**
- **Presentation order.** Cards came out in deck order in every run above, but no criterion
  constrains the order, so this is an observation and not a verdict. `plan.md` records deck order
  as an assumption with its reversal cost.
- **The reveal prompt's trailing space.** Driven from a pipe, the answer lands on the same line
  as the prompt (visible in AC1's output). Every criterion is written over substring order in
  stdout, which is unaffected, and `ADR-0001` says the tool runs at a terminal. Declared, not
  judged.
