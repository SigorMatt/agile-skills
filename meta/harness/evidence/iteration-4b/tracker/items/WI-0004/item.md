---
id: WI-0004
type: work-item
title: Delete a card that is no longer wanted
status: done
priority: medium
epic: EP-001
created: "2026-08-30T01:37:52Z"
updated: "2026-08-30T04:59:51Z"
arose-from: EP-001/Q-001
depends-on:
  - WI-0001
branch: wi/WI-0004
outcome: delivered
---

## Story

As someone whose deck has accumulated over weeks, I want to remove a card I no longer need, so
that a card I have decided is wrong or irrelevant stops coming back at me for ever.

## Acceptance criteria

Every criterion below is written against the invocation settled by `Q-001` and `Q-002` and the
interface fixed by `ADR-0001`: one executable named `recall`, with `delete` as a fourth
subcommand (`ADR-0001` §2), taking the card's question side as an option, and interactive on
standard input so a here-document drives it (`ADR-0001` §4). "The deck file" means the single
file `WI-0001` AC7 requires, at the path and in the format `ADR-0004` §1–2 fix — so a criterion
that needs a particular deck state writes that file directly. "Exits non-zero" is `ADR-0001` §5;
no criterion fixes a particular non-zero value or any message wording.

**"The card whose question is X" means the card whose stored question side is exactly the string
X** — the same bytes, no case folding, no trimming beyond the blank check in AC7, and no
substring or prefix matching. That reading is this refinement's and not the stakeholder's; see
`## Notes`.

- [x] AC1 — With a deck of three cards, `recall delete --question "<the question side of the
      second card>"` prints that card's question side **and** its answer side to stdout and then
      asks for confirmation; supplying `y` on standard input removes it and exits 0. Afterwards
      `recall list` writes the other two cards to stdout with both sides of each unchanged, and
      the deleted card's question side does not appear in its output.
- [x] AC2 — The deletion survives the process ending. Run the AC1 deletion, let that process
      exit, then run `recall list` as a new process: the deleted card's question side does not
      appear in the second process's output, and the other two cards do.
- [x] AC3 — A deleted card is never presented in a review run, whether or not it was due. With a
      deck file holding three cards — X dated today, Y dated seven days from today, Z dated
      today — delete X and then Y, each confirmed with `y`. `recall review`, driven by a
      here-document supplying a recognised response for one card, presents only Z: neither X's
      nor Y's question side appears anywhere on stdout, and the run exits 0.
- [x] AC4 — Deleting a card that is not in the deck is refused. With a deck of two cards, run
      `recall delete --question "<a string equal to neither card's question side>"`: it writes a
      message to stderr saying no card has that question, exits non-zero, issues no confirmation
      prompt — stdout contains neither card's answer side — and leaves the deck exactly as it
      was, the deck file's bytes identical before and after.
- [x] AC5 — A question side that names two cards is refused and nothing is removed. `WI-0001`
      AC9 permits two cards with the same question side; build such a deck, then run
      `recall delete --question "<that shared question side>"`. It writes a message to stderr
      that states how many cards matched, exits non-zero, issues no confirmation prompt, and
      leaves the deck file's bytes identical before and after — **both** cards are still shown by
      `recall list`. (`Q-001`: the stakeholder chose the option that refuses here, having been
      shown that it leaves them unable to remove either card.)
- [x] AC6 — Anything but `y` at the confirmation prompt leaves the deck alone. With a deck of two
      cards, run the AC1 deletion four times, supplying in turn: `n`; a word that is neither `y`
      nor `n`; an empty line; and closed standard input (`recall delete --question "..." <
      /dev/null`). In every one of the four cases the run writes to stdout that the card was
      **not** deleted, exits 0, ends without a Python traceback on stderr, and leaves the deck
      file's bytes identical before and after; `recall list` afterwards still shows both cards.
      The prompt is asked once and is not re-asked on an unrecognised response. (`Q-002` option
      B, as the stakeholder chose it: *"removes the card on `y` and leaves the deck untouched on
      anything else."* This is deliberately unlike `recall review`, which re-asks — `WI-0002`
      AC3 — and the difference is that here not deleting is the safe outcome.)
- [x] AC7 — `recall delete` is refused when `--question` is missing or blank — omitted, given as
      `""`, or given as a string of only spaces or tabs. In every one of those four cases it
      writes a message to stderr naming the missing option, exits non-zero, issues no
      confirmation prompt, and leaves the deck exactly as it was: the deck file's bytes are
      identical before and after, and with the deck file absent it is still absent afterwards.
      (`WI-0001` AC2's rule, applied to this subcommand's one option.)
- [x] AC8 — If the deck file exists but cannot be read as a deck — truncated, malformed, or not
      the format the tool writes — `recall delete` writes a message to stderr that names the
      file, removes nothing, issues no confirmation prompt, exits non-zero, and leaves the
      file's bytes identical before and after. This is `WI-0001` AC8 and `WI-0002` AC7 extended
      to the fourth subcommand; refusing loudly is required, and treating an unreadable deck as
      an empty one is a defect.
- [x] AC9 — With the deck file absent and its parent directory absent, `recall delete --question
      "anything"` reports that no card has that question — AC4's case, since `ADR-0004` §6 makes
      an absent deck an empty deck — exits non-zero, and creates nothing: the deck file and its
      parent directory are still absent afterwards. Unlike `add`, a deletion has no reason to
      create a deck.
- [x] AC10 — Deleting the last card leaves a deck that is empty rather than one that is broken.
      With a deck of exactly one card, delete it and confirm with `y`: the run exits 0, and
      `recall list` afterwards writes the documented empty-deck message to stdout and exits 0 —
      the same message and exit `WI-0001` AC6 requires — rather than reporting an unreadable
      deck. `recall add` afterwards exits 0 and the added card is listed.
- [x] AC11 — A deletion does not disturb the other cards' schedules. Take a deck file whose three
      cards carry different `rung` and `due` values (`ADR-0004` §2), delete one and confirm with
      `y`, and compare the deck file before and after: the two surviving cards' entries are
      unchanged in `question`, `answer`, `rung` and `due`, they are still in the order they were
      added, and `version` is unchanged. Deleting removes a card; it does not reschedule, reorder
      or regrade the rest.
- [x] AC12 — Adding a delete command does not change what `recall list` prints. The stakeholder
      chose the naming rule that leaves the listing alone (`Q-001`), so this criterion covers
      **`WI-0001` AC3 and `WI-0001` AC6 by ID**, and it is settled by *reading those two
      criteria's text against the behaviour this item delivers*, with the test suite as evidence
      for that reading rather than as its definition. Concretely: `recall list` still writes one
      line per card carrying both sides exactly as given, with no number, no code and no column
      this item introduced, and still writes the empty-deck message and exits 0 on an empty deck.
      If no executable test exercises both `recall delete` and the listing's shape, say so in
      the verification report and then either add a case that runs `recall list` after a
      deletion, or waive it by name with the reason.

## Out of scope

- Editing a card. The stakeholder said plainly that *"editing can wait"* (`EP-001/Q-001`), so it
  stays excluded and is not folded in here.
- Undoing a deletion, a trash can, or any recovery of a deleted card.
- Deleting more than one card in one invocation.
- Deleting the whole deck.
- Any way to pick between two cards that share a question side. `WI-0001` AC9 permits such a
  pair, and the naming rule settled in `Q-001` cannot remove either of them — it refuses. The
  stakeholder was shown that hole in the option they chose and accepted it: *"If I ever end up
  with two cards that share a question, I'll deal with that separately; it's not worth building
  for."* Removing one of a duplicated pair means editing the deck file by hand.
- A flag that skips the confirmation prompt. Option C of `Q-002` offered `--yes` and the
  stakeholder chose the unconditional prompt instead, so there is no way to delete without
  confirming.

## Notes

This item exists because the stakeholder's answer to `EP-001/Q-001` contradicted an exclusion
intake had derived on its own authority: *"I want to be able to delete a card I don't need
anymore; editing can wait."* The epic's `## Out of scope` and `docs/product/vision.md` were
amended to match, and this item carries the work that was implied. It was filed as a new item
rather than folded into WI-0001, because widening an existing item to swallow new work hides the
change from the board.

Settled by the stakeholder, and no longer open (`Q-001` and `Q-002`, both answered
2026-08-30, propagated by `answer-questions`):

- **How a card is named when deleting it — by its question side.** The invocation is
  `recall delete --question "<the question text>"`. `recall list` is unchanged: no number, no
  code, no new column. If the text names exactly one card, that card is the one removed. If it
  names **two or more**, the deletion is refused, the tool says that two matched, nothing is
  removed, and the exit is non-zero per `ADR-0001` §5. If it names none, that is AC4's case
  already. The stakeholder's words: *"B — let me just type the question, that's the most natural
  way for me to say which card I mean."*
- **Whether deleting stops to check first — yes, always.** `recall delete` prints both sides of
  the card it is about to remove and asks `delete this card? [y/n]`. It removes the card on `y`
  and leaves the deck exactly as it was on anything else. There is no flag to skip the prompt.
  The stakeholder's words: *"B — show me the card and ask first. I'd rather have one extra
  keypress than lose a card to a typo."*

Decided by `refine` and **assumed**, not said by the stakeholder. Each is recorded in
`artifacts/refinement-qa.md` as `[assumed]` with the deferral or delivered decision it rests on,
and each is cheap to reverse, which is why none was put to them:

- **Matching is exact.** The preamble to `## Acceptance criteria` fixes it: the stored question
  side must equal the typed string byte for byte. `WI-0001` AC3 stores and prints a question side
  *"exactly as it was given — no trimming …, no case change, no truncation"*, so exact is what
  *"let me just type the question"* (`Q-001`) means when the thing you are typing is what the
  listing showed you. The alternatives — case folding, substring matching — would let a typed
  string match a card the person did not mean, which is the accident `Q-002`'s answer exists to
  prevent. The failure mode of being too strict is AC4: refused, nothing removed, retype it. If
  it turns out to be annoying in daily use, loosening it is a change with product stake and it
  goes to the stakeholder rather than being decided here.
- **Declining is not a failure.** AC6 exits 0 for `n`, an unrecognised reply, an empty line and
  closed standard input, because `ADR-0001` §5 reserves non-zero for *"a refused or failed
  operation"* and a person answering `n` got exactly what they asked for. To keep the outcome
  observable whatever the exit code, AC6 requires the run to say on stdout that the card was not
  deleted.
- **Message wording and the exact non-zero exit values.** Left to `plan`, under the stakeholder's
  standing deferral over how things are worded — *"nothing fancier than that"* (`EP-001/Q-001`),
  recorded as `plan`'s in `EP-001/Q-002`'s consequences. No criterion here fixes a sentence;
  where one needs a message it names it by reference to the tool's own documentation, the device
  `WI-0001` AC7(a) and `WI-0002` AC5 use, which obliges `plan` to document it.
- **Priority stays `medium`.** The item's own `## Notes` invited `refine` to rank it. It is the
  last item in the epic, nothing depends on it, and the stakeholder did not rank it, so `medium`
  stands. That is `refine`'s decision, not theirs.

Left to `plan` as design, not routed to anyone:

- Where the removal lives — whether `Deck` grows a method, how the matching is done, whether the
  confirmation read reuses `cli._read_line`. `ADR-0004` §4 already fixes that every write is
  atomic, so the part of this with a stake in *"don't lose my progress"* is decided.
- Whether `recall delete` also accepts the question as a bare positional argument. No criterion
  requires it and none forbids it; `ADR-0001` §3 shows the option form is the one that must
  exist.

**Definition of Ready R10 — where each combination this item introduces is accounted for.** The
combinations were listed in `artifacts/refinement-qa.md` before the questions were asked, and
none is left invisible: (a) two cards sharing the named question — AC5, and no way to pick
between them is in `## Out of scope`; (b) the confirmation guard — AC1 for `y`, AC6 for
everything else, and a skip flag is in `## Out of scope`; (c) deleting the last card — AC10;
(d) the deck absent — AC9 — and the deck unreadable — AC8; (e) the deletion seen by `recall
list` — AC1 — by `recall review` — AC3 — and after the process ends — AC2; (f) delete against
the scheduling — AC11, and AC3 for a card that was not due. Two further combinations that were
not on that list: a missing or blank `--question` — AC7 — and delete against the shape of the
listing — AC12.

**Accepted at review, and carried past this item's closing** (`artifacts/review.md`
`## Accepted gaps`, 2026-08-30):

1. **`recall delete` inherits `BUG-0001`.** With the deck path existing as a directory,
   `recall delete --question "x"` exits 1 with an `IsADirectoryError` traceback. AC8 is not
   violated — it governs a file that cannot be read *as a deck*, which refuses correctly with
   exit 3 — and `BUG-0001` already describes the class. What is new: the fix now has **four**
   subcommands to cover rather than three.
2. **Concurrency is unverified.** Two deletions racing over one deck file is specified nowhere
   and nothing exercises it; `ADR-0004` §4's atomic rename bounds the damage to "one write
   wins", which is an argument and not a measurement.
3. **Exact matching will be unhelpful before it is wrong** — a question typed with an invisible
   trailing space gets "no card has that question" and no hint. The shipped mitigation is the
   refusal quoting back what was typed; anything better is a product decision.
4. **AC7's tab case was delivered through shell quoting**, not through an interactive terminal
   where readline may intercept a tab. That is a property of terminals, not of `recall`.

Two documents were repaired during review rather than sent back, both recorded in their own
change logs: `docs/architecture/overview.md` v7 (the `store.py` load-path sentence still named
three subcommands, and this item gave it a fourth caller) and `docs/process/using-recall.md` v7
(two over-width lines re-wrapped, no claim changed).
