# Plan — WI-0003 Space each card's next review according to how it was recalled

## Problem

The tool has a deck, a sitting, and a placeholder where the scheduling should be: `record_answer`
moves every card it touches to tomorrow whatever was answered, and leaves its ladder position
alone [src: recall/deck.py:92]. This item replaces that placeholder with the real arithmetic, and
tells the person about it — a right answer walks the card out along `1, 3, 7, 30` days and then
holds at thirty, a wrong answer sends it back to one day, and the sitting prints the resulting
date as each card is answered [src: ADR-0002; ADR-0007].

Four constraints shape it, and none is ours to choose. The ladder and its arithmetic are the
stakeholder's, down to the four numbers and the decision that the top rung holds
[src: EP-001/Q-003; WI-0003/Q-001; ADR-0002]. That the sitting says the next date at all is
theirs too, and is the only visible change this item makes [src: WI-0003/Q-002; ADR-0007]. The
gap is counted from the day of the sitting, not from the day the card was due, which is what
makes an overdue card safe rather than stranded [src: ADR-0002; WI-0003 AC3]. And nothing may
regress: WI-0001 and WI-0002 are delivered and signed off, and their criteria are named in AC6
[src: WI-0003 AC6].

## Approach

No new module, and no change to the three-layer split [src: docs/architecture/overview.md]. The
change is small and lands in three places, plus documentation:

- **`recall/deck.py` gains the arithmetic**, which is where the overview has said it would go
  since the first item was planned [src: docs/architecture/overview.md]. The module still never
  touches the filesystem and never prints, so the whole rule is testable without a temporary
  directory.
- **`recall/store.py` gains one range check**, beside the type checks it already runs on every
  card [src: recall/store.py:115].
- **`recall/cli.py` gains one printed line** per graded card, in the loop that already records
  the answer and saves the deck [src: recall/cli.py:182].
- **`docs/process/using-recall.md` gains the rule and loses a section that will no longer be
  true** [src: docs/process/using-recall.md].

### What `rung` means, and the arithmetic — settled in `ADR-0008`

`ADR-0004` §2 and `ADR-0002` §3–§4 describe `rung` in ways that do not pick out the same integer,
and this item is the first to read it back. `ADR-0008` settles it rather than a step below doing
so silently [src: ADR-0008]:

- `LADDER = (1, 3, 7, 30)` days, in `recall/deck.py`, beside `FIRST_RUNG = 0`
  [src: recall/deck.py:16].
- `rung` is the **index into `LADDER` of the gap the next correct answer will apply**. A card at
  `rung: 0` — every card `recall add` writes [src: recall/deck.py:73] — is moved one day out by
  its next correct answer.
- **Right**: next review is `LADDER[rung]` days after the day of the sitting; stored `rung`
  becomes `min(rung + 1, len(LADDER) - 1)`.
- **Wrong**: stored `rung` becomes `FIRST_RUNG`; next review is `LADDER[FIRST_RUNG]` days — one
  day — after the day of the sitting.
- A stored `rung` outside `0 … len(LADDER) - 1` is `DeckUnreadable`, raised at load with the card
  named, exactly as an unrecognised `grade` is [src: ADR-0006; ADR-0008]. It is not clamped: a
  deck that cannot be read is never repaired [src: ADR-0004]. Because it is caught at load,
  `record_answer` may assume the value is in range and must not re-check it.

Worked by hand, a card added on day 0 and answered right every time is due on days 0, 1, 4, 11,
41, 71 and 101 — which is the worked example in the item and the one AC5 requires the
documentation to carry [src: WI-0003 AC5].

### The line the sitting prints

`ADR-0007` fixes that the sitting names each card's next-review date, for a right answer and a
wrong one alike, and leaves the wording to this plan [src: ADR-0007]. AC4 fixes one thing inside
it — the date appears as `YYYY-MM-DD` — and leaves everything around it free [src: WI-0003 AC4].
This plan chooses:

```
  next review: 2026-09-06 (in 7 days)
```

Two indented spaces, matching the answer side and the prompts already printed for a card
[src: recall/cli.py:145]. The parenthesised gap is not required by any criterion and is one
format string; it is here because *"I don't want to be doing math to figure out when a card's
coming back"* is the sentence the stakeholder chose the ladder with [src: WI-0003/Q-001], and the
date alone makes them subtract. It is recorded under `## Assumptions` rather than in an ADR
because reversing it is deleting half a line.

The line is printed **after** the deck is saved, so that what a person is told is what is on
disk rather than what was about to be written. It is printed only for a card that was graded: a
sitting abandoned at either read prints nothing further and returns 0, which is WI-0002 AC2 and
AC9 unchanged [src: WI-0002 AC2; WI-0002 AC9].

### Interfaces this item introduces — signatures and contracts, not implementations

- `recall/deck.py`
  - `LADDER` — a module-level tuple of four integers, the days in `ADR-0002`'s ladder.
    `FIRST_RUNG` keeps its current value and meaning [src: recall/deck.py:16].
  - `record_answer(card, grade, today)` — unchanged signature, new contract: returns `card` with
    `grade` recorded, `due` set per `ADR-0008` §3 or §4, and `rung` set per the same. It stays a
    pure function over values, raises nothing, and assumes `card.rung` is in range.
  - A way for a caller to ask how many days a card's stored `due` is from a given day, so that
    `cli.py` can print the gap without recomputing the rule. Whether that is a small helper in
    `deck.py` or a subtraction at the call site is the developer's; it must not put the ladder's
    numbers in `cli.py`.
- `recall/store.py`
  - `_card_from` gains a range check on `rung`, raising `DeckUnreadable` with the same
    `card N's 'rung' …` shape its sibling messages use [src: recall/store.py:115]. No signature
    changes.
- `recall/cli.py`
  - `cmd_review` prints one line per graded card after `store.save` [src: recall/cli.py:182]. The
    sentence lives in a module constant beside `NOTHING_DUE_MESSAGE` and the prompts, as every
    other thing a person reads already does [src: recall/cli.py:96].

## Steps

1. **Add `LADDER` to `recall/deck.py`**, a tuple of the four day-counts from `ADR-0002` §2, with
   a comment naming that ADR and `ADR-0008`. Leave `FIRST_RUNG` where it is. Afterwards:
   `from recall.deck import LADDER` yields `(1, 3, 7, 30)` and nothing else in the tree has the
   numbers in it.
2. **Rewrite `record_answer` in `recall/deck.py`** to `ADR-0008` §3 and §4: a right answer sets
   `due = today + LADDER[card.rung]` days and `rung = min(card.rung + 1, len(LADDER) - 1)`; a
   wrong answer sets `rung = FIRST_RUNG` and `due = today + LADDER[FIRST_RUNG]` days. Replace the
   docstring, which currently declares itself a placeholder and says `rung` is left untouched
   [src: recall/deck.py:92]; the new one states the rule and cites `ADR-0002` and `ADR-0008`.
   Afterwards: a card at `rung: 0` answered right comes back `rung: 1`, due tomorrow; the same
   card answered wrong comes back `rung: 0`, due tomorrow; a card at `rung: 3` answered right
   comes back `rung: 3`, due in thirty days.
3. **Add the range check to `_card_from` in `recall/store.py`**, after the existing type checks
   and before the `grade` check, raising `DeckUnreadable(path, "card N's 'rung' is not a rung on
   the ladder")` — or wording of the same shape — when `rung` is negative or `>= len(LADDER)`
   [src: recall/store.py:115]. Afterwards: a deck file with `"rung": 9` makes every subcommand
   report the file and the card and exit non-zero, writing nothing, exactly as a bad `grade`
   already does.
4. **Print the next-review line in `cmd_review`** in `recall/cli.py`, immediately after
   `store.save(deck, path)` inside the per-card loop [src: recall/cli.py:182], using a new module
   constant beside the other messages [src: recall/cli.py:96]. It carries the answered card's new
   `due` as `YYYY-MM-DD` and the whole-day gap from today. Afterwards: a sitting that grades two
   cards prints two such lines, each after that card's answer side and before the next card's
   question side, and a sitting that ends at either read prints none.
5. **Rewrite the unit test at `tests/test_review.py:263`**, which asserts the placeholder — it
   builds a card at `rung: 4` and requires a wrong answer to leave it there
   [src: tests/test_review.py:263]. Under step 2 a wrong answer resets the rung, and under step 3
   `4` is not a legal stored value. Replace it with tests of the new contract. Afterwards: no
   test asserts the placeholder's behaviour.
6. **Add the acceptance tests** to `tests/test_review.py`, driving `bin/recall` as a subprocess
   with `HOME` in a temporary directory [src: ADR-0005], one test per criterion as mapped below.
   AC1, AC2(b) and AC4 need a helper that rewrites **only** the `due` field of the stored deck,
   leaving `rung`, `grade` and the two sides exactly as the tool wrote them — the counterpart of
   `write_deck`, and it belongs in `tests/support.py` beside it [src: tests/support.py:121].
   Afterwards: `python3 -m unittest discover -s tests -t . -q` exercises every criterion.
7. **Rewrite `docs/process/using-recall.md`'s scheduling content** [src: docs/process/using-recall.md].
   Its "What this version does not do yet" section says scheduling is unbuilt and that a reviewed
   card comes back tomorrow whatever the answer; both become false at step 2. Replace it, and add
   the five facts AC5 names — the four gaps, that the gap holds at thirty, that a wrong answer
   returns the card to the start, that a gap is counted from the day of the sitting even when the
   card is overdue, and the worked example days 0, 1, 4, 11, 41, 71, 101. Also describe the line
   step 4 prints, since the file documents what a sitting shows. Bump the version and add a
   change-log row [src: .claude/agile-skills/spec/doc-header.md]. Afterwards: a reader following
   only that section works out the same dates the tool produces.
8. **Check `docs/architecture/overview.md` against what you built, and correct it if the design
   moved.** This execution already took it to version 3, because the shape is a plan-time
   decision: `deck.py` no longer "will" gain the rule, `cli.py`'s line and `store.py`'s new
   validation are recorded, and the entries are worded as what the design commits to rather than
   as what exists [src: docs/architecture/overview.md]. If steps 1 to 4 end up differing from it
   in any way — a different module, a different boundary — the document is what is wrong and it
   takes another version and change-log row. If they match, leave it alone: a version bump with
   no substantive change devalues every other one.
9. **Run the declared gates on the final state**: `python3 -m unittest discover -s tests -t . -q`
   and `python3 -m compileall -q recall tests` [src: tracker/project.yaml]. Afterwards: both exit
   0 and `impl-report.md` maps each criterion to the test that demonstrates it.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — the ladder 1, 3, 7, 30 and then holding | 1, 2, 6 | A subprocess test: `recall add`, then five cycles of "rewrite only `due` to today, run `recall review` answering right", asserting the stored `due` after each is today +1, +3, +7, +30, +30. The fifth cycle is the top rung holding, and it fails against any implementation that grows the gap past thirty. |
| AC2 — a wrong answer, from any rung, and the ladder position reset with it | 2, 6 | Two subprocess tests. (a) a freshly added card answered wrong stores `due` = today + 1. (b) the AC1 cycle run four times, then answered wrong (`due` = today + 1), then `due` rewritten to today and answered right: the stored `due` is today + 1, not today + 30. (b) fails against today's `record_answer`, which moves the date and leaves `rung` alone [src: recall/deck.py:92]. |
| AC3 — the gap is counted from the day of the sitting, overdue included | 2, 6 | A subprocess test per answer: a deck file written with `due` ten days before today and `rung: 0` [src: tests/support.py:121], reviewed once. The stored `due` is today + 1 in both cases — nine days in the future of the date it missed would be today − 9, so the two readings cannot both pass. |
| AC4 — the sitting says when the card is next due | 4, 6 | A subprocess test asserting stdout: the `YYYY-MM-DD` string for today + 1 appears in the first cycle's output and today + 30 in the fourth, each after that card's answer side; and the wrong-answer run of AC2(b) prints today + 1. Printing a constant fails the pair, and each printed date is compared against the `due` actually written to the deck file [src: tests/support.py:145]. |
| AC5 — the rule is written down and the tool agrees | 7 | A read of `docs/process/using-recall.md` for the five named facts and the worked example, plus the observation that the "does not do yet" section no longer claims scheduling is unbuilt. The "tool agrees" half is AC1 to AC3's tests, which produce the same dates the worked example states. |
| AC6 — WI-0001 AC1–AC9 and WI-0002 AC1–AC13 still hold | 2, 3, 4, 5, 9 | A read of those twenty-two criteria against the shipped behaviour, recorded in `verify-report.md`, with the existing suite as evidence — it exercises all of them today and must stay green [src: run: python3 -m unittest discover -s tests -t . -q → exit 0, 32 tests]. The four named in the criterion get an explicit sentence each: WI-0002 AC8 (every gap here is at least one day, so a finished card is not re-presented the same day), WI-0002 AC10 (`record_answer` still replaces one card and touches neither side nor the deck's length), WI-0002 AC13 (`due_positions` is untouched), WI-0001 AC3 (`cmd_list` is untouched — `ADR-0007` §4). Where nothing executable exercises both a covered criterion and the new behaviour, say so and then cover or waive by ID. |

## Assumptions

Each is reversible in the sense the escalation rule requires — one file, no data migration, no
change to a published interface [src: .claude/agile-skills/spec/question.md].

1. **The line reads `  next review: <YYYY-MM-DD> (in <n> days)`, indented two spaces.** AC4 fixes
   only the date's form and `ADR-0007` §2 leaves the rest to this plan. Reversing it is editing
   one module constant in `cli.py`; no criterion names the surrounding words, deliberately —
   `plan` chose the sentence and `implement` must not choose a different one without saying so.
2. **The gap is printed in whole days and singular is handled** — "in 1 day", not "in 1 days".
   Nothing requires it; it costs one conditional and its absence is the kind of thing that reads
   as carelessness in the one line this item adds to the person's screen.
3. **The line goes after `store.save`, not before it.** Reversing it is moving one statement. It
   is a preference for telling the person only what is already durable, and it costs nothing:
   `save` raises rather than returning a failure, so a save that fails prints nothing.
4. **The range check in step 3 rejects rather than clamps, and lives in `store.py` rather than in
   `deck.py`.** The rejection is `ADR-0008` §6 and is not an assumption; *where* it lives is —
   `store.py` is the layer that already turns a bad field into `DeckUnreadable`
   [src: recall/store.py:115], and putting it there is what lets `record_answer` stay a total
   function over valid cards. Reversing it is moving one branch.
5. **The helper that rewrites only `due` lives in `tests/support.py`.** It is test scaffolding,
   not behaviour; `write_deck` is already there and this is its counterpart
   [src: tests/support.py:121].

## Decisions and ADRs

| decision | where it is recorded | route |
|----------|---------------------|-------|
| What `rung` counts, and the arithmetic for both answers | `ADR-0008` §2–§5 | decided — two standing sentences disagreed and the item routed it here [src: tracker/items/WI-0003/item.md] |
| What an out-of-range stored `rung` does | `ADR-0008` §6 | decided, from `ADR-0004` §5 and `ADR-0006` §3 |
| That the deck format version does not move | `ADR-0008` §7 | decided, from `ADR-0004` §3 |
| That the sitting prints the next date at all, and that `recall list` does not | `ADR-0007` | the stakeholder's, already answered [src: WI-0003/Q-002] |
| The ladder, the top rung holding, and the reset | `ADR-0002` | the stakeholder's, already answered [src: EP-001/Q-003; WI-0003/Q-001] |
| The wording of the printed line | `## Assumptions` 1–3 | assumed, reversible in one constant |
| Where the range check lives, and the test helper | `## Assumptions` 4–5 | assumed, reversible in one branch |
| The test and lint commands | `tracker/project.yaml`, unchanged | already resolved for WI-0001 [src: ADR-0003] |

Nothing was asked of the stakeholder by this execution. Both questions this item carries were
answered before it, and no decision above is irreversible or turns on intent no document records.

## Scaffolding

`none`. Both declared commands already run in this project against the existing tree — the test
command discovers four test modules and the lint command compiles two packages
[src: tracker/project.yaml] — so nothing had to be created for a gate to execute.

## Risks

- **The placeholder passes a date-only check, so a weak test suite would not notice the ladder
  position never moving.** `record_answer` today moves a card to tomorrow and leaves `rung`
  exactly as it was [src: recall/deck.py:92], and every card in every deck is on the bottom rung,
  so *"answered wrong, comes back tomorrow"* is already true. AC2(b) is the criterion that
  distinguishes them and step 6 must actually implement it; a suite that tests only single
  sittings would go green against the code this item is replacing.
- **The five-cycle test rewrites the deck file between runs, and a careless helper would drop
  `grade` or reset `rung`.** That would make AC1 pass against an implementation that never
  advances the ladder at all, because every cycle would start from `rung: 0` and every gap would
  be one day. The helper in step 6 must preserve every key it does not set, and the test should
  assert the `rung` it did not touch is the one the tool wrote.
- **`ADR-0008` §6 tightens a field's legal values on an existing format.** It is safe here only
  because nothing has ever written a `rung` other than `0` [src: recall/deck.py:92] and no test
  deck file carries another [src: tests/support.py:135]. If that were wrong, decks in the field
  would stop loading. The one place a non-zero `rung` appears today is a unit test constructing a
  `Card` directly, which never goes through `store.load` [src: tests/test_review.py:263].
- **Two documents make claims this item falsifies**, and D7 and D12 land on both:
  `docs/process/using-recall.md`'s "What this version does not do yet" [src: docs/process/using-recall.md]
  and `docs/architecture/overview.md`'s "will land there when WI-0003 arrives"
  [src: docs/architecture/overview.md]. Steps 7 and 8 exist for them; skipping either leaves a
  false sentence with a citation on it, which is the failure D12 was written for.
- **`BUG-0001` is open and touches the same call path** — a filesystem error on the deck file
  surfaces as a traceback [src: tracker/items/BUG-0001/item.md]. It is not this item's to fix and
  this plan does not widen to absorb it; step 3's new `DeckUnreadable` is `ADR-0004` §5's existing
  route and not a change to how errors are reported.

## Out of scope for this item

- Anything on `recall list`. It keeps printing `question | answer` and gains no dates
  [src: ADR-0007; WI-0003].
- A summary or tally at the end of a sitting, and any record of past answers beyond the single
  `grade` field `ADR-0006` already stores [src: ADR-0006; WI-0003].
- Letting the person change the ladder, or any setting at all. The stakeholder said they might
  revisit the top rung if their deck grows [src: WI-0003/Q-001]; that is a future item, not a
  flag this one builds [src: WI-0003].
- Fixing `BUG-0001` [src: tracker/items/BUG-0001/item.md].
- Repairing or migrating a deck whose `rung` is out of range. Step 3 refuses it; nothing offers to
  fix it [src: ADR-0004].
