# Plan — WI-0002 Review the cards that are due today and record how each went

## Problem

A person with a deck built up by WI-0001 needs the sitting the tool exists for: show me the cards
I am due to see, one at a time, let me try to recall each before it shows me the answer, and take
down whether I got it. This item builds the third subcommand, `recall review`, and nothing more —
how far forward a right answer pushes a card is WI-0003's arithmetic and is excluded here.

Four constraints shape it, and none of them is ours. The shape of the conversation is fixed:
`review` *"shows a question, waits, shows the answer, and asks how it went"*, reading standard
input so a here-document can drive it [src: ADR-0001]. The grade is two-way, never a scale
[src: ADR-0002]. The sitting has **no cap** — the stakeholder was offered one and refused it,
reconciling that against their own couple-of-minutes sentence themselves: *"If it's a big pile
after a week away I'll just stop partway, that's fine by me."* [src: WI-0002/Q-001]. And that
last clause is a requirement rather than a remark: a sitting abandoned half-way must keep the
answers already given [src: WI-0002 AC9], which is the same sentence — *"don't lose my
progress"* [src: EP-001/Q-001] — that already put an atomic rename under every write
[src: ADR-0004].

## Approach

No new module and no change to the three-layer split [src: docs/architecture/overview.md]:
`store.py` keeps doing file access and no printing, `deck.py` gains the card-level operations as
values with no I/O, and `cli.py` gains everything a person sees. The one storage question the
item raises — what a sitting leaves behind about the answer itself — is settled in `ADR-0006`
and not in a step below.

### The sitting, as a contract

One pass over the due cards, in deck order, with **two reads per card**:

1. print the card's question side;
2. read a line — its content is ignored; it is the person saying "show me". End of input here
   ends the sitting **before** the answer is printed, which is what AC2 checks
   [src: WI-0002 AC2];
3. print the card's answer side;
4. prompt for the grade and read a line. Anything other than the two recognised responses is
   answered with what was expected and the **same** card's grade prompt is issued again. End of
   input here ends the sitting with this card ungraded;
5. record the grade against the card, move its due date, and **save the deck before presenting
   the next card**.

Two of those are load-bearing and are decisions rather than phrasing:

- **The re-prompt after an unrecognised response does not reprint the question side.** It cannot:
  AC1 requires that no card's question side appears more than once in a run's output
  [src: WI-0002 AC1], and AC3 requires the same card to be asked again [src: WI-0002 AC3]. The
  only shape satisfying both is a re-issued grade prompt that does not carry the card's text. For
  the same reason the grade prompt must never echo the question side.
- **The deck is saved after every graded card, not once at the end.** A sitting that ends
  part-way must keep the answers already given [src: WI-0002 AC9], and a single save at the end
  loses all of them. Each save is a whole-file atomic rewrite [src: ADR-0004], which at the scale
  of one person's vocabulary deck costs nothing worth measuring.

### Interfaces this item introduces — signatures and contracts, not implementations

- `recall/deck.py`
  - `Card` gains a fifth field, `grade`, defaulting to `None`; legal values are the module
    constants `GRADE_RIGHT = "right"` and `GRADE_WRONG = "wrong"` [src: ADR-0006]. It is declared
    last so the existing four positional fields are unaffected.
  - `Deck.replace(position, card) -> None` — put `card` at `position`, keeping the deck's length
    and order. The deck is a sequence of frozen values, so recording an answer means replacing
    one.
  - `due_positions(deck, today) -> tuple[int, ...]` — the positions of every card whose `due` is
    **on or before** `today`, in deck order. "On or before" is the item's reading of due
    [src: WI-0002 AC13]; deck order is the assumption recorded below.
  - `record_answer(card, grade, today) -> Card` — a new `Card` with `grade` set and `due` set to
    the day after `today`, `rung` untouched. **This is the placeholder WI-0003 replaces**; see
    `## Assumptions`.
- `recall/store.py`
  - `_card_from` accepts an absent `grade` key as `None`, and raises `DeckUnreadable` when the key
    is present and is not one of the two words [src: ADR-0006].
  - `_card_to_entry` emits `grade` only when it is not `None`, so an unreviewed deck serialises
    exactly as WI-0001 wrote it [src: ADR-0006].
  - `DECK_FORMAT_VERSION` does not move [src: ADR-0006].
- `recall/cli.py`
  - `cmd_review(args) -> int`, and a `review` subparser taking no options [src: ADR-0001].
  - `NOTHING_DUE_MESSAGE` — one constant, used for both an all-future deck and an absent one
    [src: WI-0002 AC5; WI-0002 AC6].
  - `REVEAL_PROMPT`, `GRADE_PROMPT`, and the text naming the two recognised responses when an
    unrecognised one arrives.
  - Every prompt is written so that it reaches the person **before** the process waits — `input()`
    flushes standard output, and anything printed by hand before a read is flushed explicitly.
    Without this the tool appears to hang at a pipe.
- `tests/support.py`
  - `run_recall(*args, home, stdin=None)` — the existing helper gains a keyword for the child's
    standard input. `None` keeps today's behaviour.
  - `write_deck(path, cards)` — write a deck file directly from `(question, answer, rung, due)`
    tuples, so a criterion needing a particular next-review date can set one up without the tool
    [src: WI-0002].

### The two recognised responses

`y` for right and `n` for wrong, matched after stripping surrounding whitespace and folding case,
so `Y` and ` n ` are the same two responses rather than a third and a fourth. Exactly two, as the
grade is two-way [src: ADR-0002]. `plan` owns the wording [src: ADR-0001] and the item requires
these to be documented, because three of its criteria name the responses and the nothing-due
message by reference to the tool's own documentation rather than fixing tokens
[src: WI-0002 AC3; WI-0002 AC5]. That documentation is `docs/process/using-recall.md`, and
extending it is step 6 below — a criterion that points at documentation fails if the documentation
is not written.

## Steps

1. **Extend `tests/support.py`.** Add the `stdin` keyword to `run_recall` (passed to
   `subprocess.run` as `input=`), add `write_deck(path, cards)`, and add the marker constant the
   nothing-due assertions will use. Afterwards:
   `python3 -m unittest discover -s tests -t . -q` still exits 0 — the existing WI-0001 tests are
   unaffected, because the new keyword defaults to today's behaviour.
2. **Extend `recall/deck.py`** with the `grade` field, `GRADE_RIGHT`, `GRADE_WRONG`,
   `Deck.replace`, `due_positions` and `record_answer`, as specified above. Afterwards: a `Card`
   can be built without a grade exactly as before; `due_positions` over a deck holding dates of
   yesterday, today and tomorrow returns the first two positions in order; `record_answer` returns
   a card with the same `question`, `answer` and `rung`, a `grade`, and `due` one day later.
3. **Extend `recall/store.py`** so `grade` round-trips: absent on read means `None`, an illegal
   value raises `DeckUnreadable` naming the card, and it is written only when set. Afterwards: a
   deck saved with no graded card is byte-identical to what WI-0001 wrote for the same cards; a
   deck file whose card carries `"grade": "maybe"` raises `DeckUnreadable`.
4. **Add `cmd_review` and the `review` subparser to `recall/cli.py`**, implementing the contract
   in `## Approach` — nothing-due message and exit 0 when `due_positions` is empty; the
   two-read loop; `DeckUnreadable` caught at the same single site as the other subcommands
   [src: recall/cli.py:107]; end of input at either read ends the sitting and returns 0.
   Afterwards: `recall review` against an empty home prints the nothing-due message and exits 0,
   and against a deck with one due card prints the question and exits 0 with standard input
   closed.
5. **Write `tests/test_review.py`**, one test per criterion, per the mapping table below.
   Afterwards: `python3 -m unittest discover -s tests -t . -q` exits 0 and
   `python3 -m compileall -q recall tests` exits 0.
6. **Extend `docs/process/using-recall.md`** with a "Doing a review" section: what a sitting
   shows, that a line is pressed to reveal the answer, **the two recognised responses `y` and
   `n`**, **the nothing-due message**, that the sitting shows everything due with no cap and may
   be stopped part-way without losing the answers already given, and that what a right answer does
   to the schedule is not built yet. Rewrite "What this version does not do yet" so it no longer
   says reviewing is unbuilt. Bump the version and add a change-log row [src: ADR-0006]. This step
   is not optional dressing: AC3, AC5 and AC6 are decided by reading this file.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 4 | `tests/test_review.py` — three cards written due today, driven by six input lines; asserts each question side's index in stdout precedes its answer side's, that card *n*'s last output index precedes card *n+1*'s first, that each question side occurs exactly once, and exit 0 |
| AC2 | 4 | one due card, `stdin=""` (immediate EOF); asserts the question side is in stdout, the answer side is **not**, and exit 0 |
| AC3 | 4 | two due cards; input `reveal`, `maybe`, `y`, `reveal`, `y`; asserts the run names the two expected responses, that the second card's question side does not appear before the `y`, and that the first card ends up graded in the deck file |
| AC4 | 2, 4 | deck written directly with one card due today and one due today+7; asserts the second question side is absent from stdout and exit 0 |
| AC5 | 4 | deck written directly with every card due today+7; asserts the documented nothing-due marker is in stdout, no question side appears, and exit 0 |
| AC6 | 4 | empty scratch home, no deck and no parent directory; asserts the **same** nothing-due marker, exit 0, and that `deck.json` and `~/.local/share/recall` are still absent afterwards |
| AC7 | 4 | six damaged decks as WI-0001 AC8 used; asserts stderr names the deck path, no question side on stdout, non-zero exit, and `sha256` identical before and after |
| AC8 | 4, 3 | one due card, graded `y` in a first process; a second `recall review` in a new process asserts the question side is absent from its stdout |
| AC9 | 4, 3 | two due cards, input for the first only then EOF; asserts no `Traceback` in stderr, and that a second run presents the second card's question side and not the first's |
| AC10 | 2, 3 | `recall list` captured before and after a full sitting; asserts the two outputs are identical, so both sides of every card and their order survive |
| AC11 | 4 | twenty-five cards written due today, fifty input lines; asserts all twenty-five question sides appear and exit 0 — nothing caps the sitting |
| AC12 | 4 | `recall add` then `recall review` in a second process, same day; asserts the added question side appears on stdout |
| AC13 | 2, 4 | deck written directly with one card due today−7; asserts its question side appears and exit 0 |

## Assumptions

Each is reversible in the sense step 4 of this skill's procedure requires: one file, no data
migration, no published interface change.

- **Due cards are presented in deck order** — the order they were added, which is the order
  `recall list` already shows [src: ADR-0004]. `refine` left this deliberately unconstrained and
  routed it here [src: WI-0002]. Oldest-due-first is the alternative worth naming, and with no cap
  on the sitting it changes the sequence but never the set, since everything due is shown either
  way [src: WI-0002 AC11]. Deck order wins on two counts: it is deterministic, so a test and a
  by-hand check agree, and it is the one order the tool has already taught the person. Shuffling
  was rejected outright — it would need a seed to be checkable. **Reversing it** is the ordering
  expression inside `due_positions`, one line, with no stored state affected.
- **A sitting that ends part-way exits 0.** Not an assumption about intent so much as a reading:
  exit codes are `0` for success and non-zero for *"a refused or failed operation"*
  [src: ADR-0001], and stopping part-way is neither — it is the thing the stakeholder said they
  would do [src: WI-0002/Q-001], with the answers already given kept [src: WI-0002 AC9]. A
  non-zero code would report their normal use of the tool as a failure. **Reversing it** is one
  `return` in `cmd_review`.
- **The placeholder forward step moves a card to the day after the sitting, whatever the grade,
  and does not touch `rung`.** The item excludes deciding how far a right answer pushes a card
  and requires only that the card stops being due for the rest of the day [src: WI-0002]. Two
  properties make this the cheapest placeholder to remove: for a *wrong* answer it is already the
  real rule, exactly [src: ADR-0002], so WI-0003 only has to add the right-answer ladder walk; and
  leaving `rung` untouched means no card acquires a ladder position that the real arithmetic never
  gave it, so there is no stored state for WI-0003 to undo. **Reversing it** is `record_answer`,
  one function, and it is where WI-0003 will land.
- **A completed sitting prints no closing line.** The item excludes *"any summary, tally or
  statistic at the end of a sitting"* [src: WI-0002], so the last thing a person sees is the last
  card's grade prompt. This is a deliberate reading of an exclusion and it is the assumption here
  most likely to be wrong in a person's hands rather than on paper. **Reversing it** is one
  `print` — but it should be reversed by asking the stakeholder, not by a later plan deciding a
  tally is fine after all.
- **`datetime.date.today()` is read directly, with no injectable clock.** Every criterion that
  needs a particular date sets it up by writing the deck file with a date computed relative to
  today [src: WI-0002], which is how the criteria are written and what makes an injectable clock
  unnecessary. `cmd_add` already works this way [src: recall/cli.py:80]. **Reversing it** would be
  a parameter on two functions; nothing stored depends on it.

## Decisions and ADRs

- **`ADR-0006` — what a sitting records against a card.** Created by this execution. The item asks
  that an answer be *"stored against the card"* [src: WI-0002] and `ADR-0004` owns the file, so
  this is a storage decision and not a step. Optional fifth key `grade`, two legal values, absent
  until a card is reviewed, rejected when malformed, and the format version does not move. Options
  weighed: store nothing but the consequence, and an append-only review log — the second rejected
  partly because it is the substrate for the statistics the epic excludes.
- **Answered from existing documents, no ADR needed** — recorded here so a reader can see they
  were decided rather than skipped: the conversation's shape, two reads per card [src: ADR-0001];
  two responses and not a scale [src: ADR-0002]; exit 0 on an early end [src: ADR-0001]; a deck
  that cannot be read is reported and never repaired, which is why `review` catches
  `DeckUnreadable` at the same single site as `add` and `list` rather than starting a fresh
  sitting [src: ADR-0004; WI-0002 AC7].
- **Nothing was asked of the stakeholder.** No decision here is irreversible, and none turns on
  intent no document records — the two that did were asked at refinement and are answered
  [src: WI-0002/Q-001; WI-0002/Q-002].
- **No ADR was superseded, and no two answers of theirs were reconciled.** The one place that
  could have happened is the couple-of-minutes sentence against the no-cap answer, and it needs
  no reconciling here: the stakeholder settled it themselves inside the answer, and this plan
  quotes their reconciliation rather than choosing between the two [src: WI-0002/Q-001].

## Scaffolding

`none`. Every file this plan touches already exists, `commands.test` and `commands.lint` are
already set and already run [src: tracker/project.yaml], and the test discovery pattern is
already satisfied by four existing test files — so there is no command that could not otherwise
execute.

## Risks

- **The grade prompt or the re-prompt echoing the card's question text would break AC1**, which
  requires each question side to appear exactly once [src: WI-0002 AC1]. It is an easy and
  natural thing to write ("Did you get *der Bahnhof* right?"). Stated in `## Approach` as a
  contract for that reason.
- **Buffering.** With standard output on a pipe it is block-buffered, so a prompt printed without
  a flush before a blocking read leaves a person looking at nothing while the tool waits. The
  tests will not catch it — they supply all input up front and read the buffer at exit — so the
  contract in `## Approach` is the only thing standing between this plan and a tool that appears
  to hang for its user and passes every criterion.
- **A sitting that runs across midnight** would compute `today` once and grade against it. No
  criterion covers it and no behaviour here is wrong for it; it is named so a later reader does
  not think it was missed. The same applies to a test suite started seconds before midnight —
  a flake, not a defect, and cheap to re-run.
- **`BUG-0001` is not fixed here and must not be.** It covers filesystem errors that are not
  content problems — a permission denial, a directory where the deck should be — surfacing as
  tracebacks [src: BUG-0001]. `review` will reach the deck through the same `store.load` as `add`
  and `list` [src: recall/store.py:48], so it inherits the same weakness, and fixing the bug later
  will fix it for `review` too. AC7 here is about deck *content* only, and a passing AC7 is not
  evidence about `BUG-0001` [src: WI-0002].
- **The placeholder is invisible in the tool's output.** A person reviewing a card gets it back
  tomorrow whether they got it right or wrong, which will look like a bug to anyone who has read
  the vision. Step 6 requires the documentation to say the schedule is not built yet, and that
  sentence is the only thing preventing it being filed as one.

## Out of scope for this item

- The interval ladder — how far a right answer pushes a card. `WI-0003` [src: ADR-0002].
- Deleting a card, `WI-0004`, and editing one, which the epic excludes
  [src: docs/product/vision.md].
- Reviewing cards that are not due, a "study everything" mode, reviewing one named card, undoing
  an answer, and any end-of-sitting tally — all excluded by the item [src: WI-0002].
- Any cap on the length of a sitting, and any clock-based limit. The stakeholder refused both
  [src: WI-0002/Q-001].
- `BUG-0001`, per `## Risks`.
