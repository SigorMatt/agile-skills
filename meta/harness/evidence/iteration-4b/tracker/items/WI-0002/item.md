---
id: WI-0002
type: work-item
title: Review the cards that are due today and record how each went
status: done
priority: high
epic: EP-001
created: "2026-08-30T01:30:02Z"
updated: "2026-08-30T03:26:56Z"
depends-on:
  - WI-0001
branch: wi/WI-0002
outcome: delivered
---

## Story

As someone with a deck already built up, I want a single daily sitting that shows me only the
cards I am due to see and asks me how each one went, so that I spend my time on what I am about
to forget rather than on the whole deck.

## Acceptance criteria

Every criterion below is written against the invocation fixed by `ADR-0001`: one executable
named `recall`, with `review` as a subcommand, interactive on standard input so that a
here-document drives it (`ADR-0001` §4). "The deck file" means the single file WI-0001 AC7
requires, in the format `ADR-0004` §2 fixes — so a criterion that needs a card with a particular
next-review date sets one up by writing that file directly.

**"Due" means the card's stored next-review date is today or earlier**, not today exactly. That
reading is this refinement's, not the stakeholder's; see `## Notes`.

- [x] AC1 — With three cards in the deck, all due, `recall review` driven by a here-document
      that supplies enough input presents them one at a time and exits 0: for each card, its
      question side appears on stdout before its answer side, and everything printed for one
      card appears before anything printed for the next. No card's question side appears more
      than once in the run's output.
- [x] AC2 — The answer side is not shown until it is asked for. With exactly one due card and
      standard input closed immediately — `recall review < /dev/null` — stdout contains that
      card's question side and does **not** contain its answer side.
- [x] AC3 — For every card presented, the run records whether the person recalled it — right or
      wrong, a two-way choice and not a scale (`ADR-0002` §1) — and does not move on until it
      has one of exactly two recognised responses. Checkable with two due cards: supply a
      response for the first card that is neither of the two the tool's documentation names,
      then a recognised one. The run writes what it expected, asks for the **same** card again,
      and the second card's question side does not appear on stdout until the recognised
      response has been supplied.
- [x] AC4 — A card whose next-review date is later than today is not presented. With a deck file
      holding one card dated today and one dated seven days from today, `recall review` presents
      only the first: the second card's question side does not appear anywhere on stdout, and
      the run exits 0.
- [x] AC5 — When nothing is due, the run says so and exits 0 without presenting a card. With a
      deck file whose every card is dated later than today, stdout carries the message the tool's
      own documentation names for a sitting with nothing due, no card's question side appears,
      and the exit code is 0. This is not an error. (`ADR-0001` reserves the wording to `plan`, so
      the criterion names the message by reference to the documentation rather than fixing a
      sentence here — the device WI-0001 AC7(a) used. `plan` must therefore document it.)
- [x] AC6 — With the deck file absent and its parent directory absent, `recall review` reports
      nothing to review — **the same documented message as AC5** — exits 0, and creates nothing:
      the deck file and its parent directory are still absent afterwards. (`ADR-0004` §6 makes
      absent an empty deck rather than a fault, so this is not a separate condition to the person
      running it and must not read as one; and a sitting has no reason to create a deck.)
- [x] AC7 — If the deck file exists but cannot be read as a deck — truncated, malformed, or not
      the format the tool writes — `recall review` writes a message to stderr that names the
      file, presents no card, exits non-zero, and leaves the file's bytes identical before and
      after. This is WI-0001 AC8's rule extended to the third subcommand; refusing loudly rather
      than starting a fresh sitting is required, and silently treating an unreadable deck as an
      empty one is a defect.
- [x] AC8 — What was recorded during a sitting is still there after the process ends. Run
      `recall review` and answer at least one card, let that process exit, then run
      `recall review` again as a new process on the same day: the card the first run finished is
      not presented by the second — its question side does not appear on the second run's
      stdout.
- [x] AC9 — A sitting that ends part-way keeps the answers already given. With two due cards,
      run `recall review` supplying input for the first card only and then closing standard
      input. The process ends without a Python traceback on stderr, and a second run on the same
      day presents the second card and not the first. (The stakeholder's stated failure
      condition is losing progress; an answer already given is progress.)
- [x] AC10 — Nothing outside the sitting is disturbed. After any run above, `recall list` still
      shows every card that was in the deck before it, with both sides of each card unchanged.
      A sitting records answers; it does not add, remove or rewrite the text of a card.
- [x] AC11 — A sitting presents every card that is due, however many that is; it does not cap
      the number it shows. With twenty-five cards in the deck, all due, `recall review` driven by
      a here-document that supplies a recognised response for each presents all twenty-five —
      every card's question side appears on stdout — and exits 0. (The stakeholder chose this
      over a cap: *"No limit — A. Show me everything that's due."* `WI-0002/Q-001`.)
- [x] AC12 — A card added today is due in today's sitting. With the deck file absent, run
      `recall add --question <text> --answer <text>` and then `recall review` as a second process
      on the same day: the card just added is presented — its question side appears on stdout.
      (`WI-0002/Q-002`; confirms `ADR-0002` §3, which `recall add` already implements.)
- [x] AC13 — A card whose review date has already passed is still presented. With a deck file
      holding one card dated seven days **before** today, `recall review` presents it — its
      question side appears on stdout — and exits 0. This is the reading of "due" stated above
      made checkable: missing a day puts a card in the next sitting rather than dropping it out
      of the schedule, which is *"don't lose my progress"* (`EP-001/Q-001`) applied to the
      schedule. The reading is `refine`'s, not the stakeholder's; it was put in front of them in
      `WI-0002/Q-001`'s `## Context` with an invitation to say if it was wrong, and they answered
      without contesting it — which is not the same as their having chosen it.

## Out of scope

- Deciding how far forward a card is pushed by a given answer — that is WI-0003. This item needs
  only that an answer is captured and stored against the card, and that the card stops being due
  for the rest of the day (AC8). Whatever forward step this item uses is a placeholder WI-0003
  replaces, and it is `plan`'s to choose.
- Reviewing cards that are not due, or a "study everything" mode.
- Reviewing one named card on demand, or re-reviewing a card already finished today.
- Undoing an answer once given, or correcting one from an earlier sitting.
- Any summary, tally or statistic at the end of a sitting beyond what AC5 requires. The epic
  excludes statistics and streaks.
- Filesystem errors on the deck file that are not content problems — a permission denial, a
  directory where the file should be. AC7 covers a deck whose **content** is not a deck; the
  rest is `BUG-0001`, which is already open against the other subcommands.

## Notes

**Both questions to the stakeholder are answered, and the item is no longer suspended.** They
were `WI-0002/Q-001` (does a sitting cap how many cards it presents?) and `WI-0002/Q-002` (is a
card added today due in today's sitting?). Both were answered in the stakeholder's own words and
both answers are recorded verbatim in `artifacts/refinement-qa.md`, which is now `recorded`.

- `Q-001` — **no cap.** *"No limit — A. Show me everything that's due. If it's a big pile after a
  week away I'll just stop partway, that's fine by me."* Added as **AC11**.
- `Q-002` — **due the day it is added.** *"Today — A. If I've just added a card I want to try
  recalling it right away, not wait till tomorrow."* Added as **AC12**. This confirms intake's
  assumption and `ADR-0002` §3, and matches what `recall add` already stores
  (`recall/deck.py` `new_card` writes `due` = the day added), so no delivered behaviour changes.

**The couple-of-minutes sitting is a design concern, not a criterion, and that is the
stakeholder's own choice.** Their failure condition — *"a review session that drags on more than
a couple minutes"* (`EP-001/Q-001`) — was put back to them as `Q-001` with the trade-off spelled
out, including that choosing no cap means the sentence stays a constraint we design towards and
does not become a criterion. They chose no cap anyway and supplied their own reconciliation:
they will stop partway. Nothing in this item bounds the length of a sitting, and nothing should
be added later that does without asking them again.

Two consequences follow for whoever builds and verifies this:

- **AC9 carries more weight than its wording suggests.** "I'll just stop partway" is now the
  stakeholder's stated coping mechanism for a long pile, so a sitting that loses answers when it
  is abandoned half-way does not merely fail AC9 — it removes the thing they are relying on.
- **A long sitting is not a defect.** A verifier finding that twenty-five due cards take longer
  than a couple of minutes has found the behaviour the stakeholder asked for (AC11), not a bug.

**Decided at refinement rather than asked, with the basis.** All are in
`artifacts/refinement-qa.md` marked `[assumed]`:

- **"Due" means today or earlier.** A card whose date has passed still comes back. The other
  reading would drop a card out of the schedule for good the first time a day is missed, which is
  *"don't lose my progress"* (`EP-001/Q-001`) applied to the schedule. Named in `Q-001`'s context
  so the stakeholder saw it while answering, and now checkable as **AC13** — round 1 stated the
  reading in prose and left no criterion that exercised an overdue card.
- **An interrupted sitting keeps the answers already given** (AC9), for the same sentence.
- **The witness sizes in the criteria are `refine`'s, not requirements.** AC11's twenty-five
  cards is a number chosen to sit comfortably above any batch size an implementation might pick
  by accident; the requirement is that there is no cap, not that twenty-five is special. Same for
  AC1's three and AC4's seven days. None of these is a threshold the stakeholder gave.
- **AC5 and AC6 report nothing-due with the same message.** `ADR-0004` §6 makes an absent deck an
  empty deck rather than a fault, so an empty deck and an all-future deck are the same situation
  to the person running it, and two different messages would invent a distinction the record
  denies. The wording itself remains `plan`'s (`ADR-0001`).

**Open design questions, routed to `plan` rather than to the stakeholder**, because the answer
would be the same whoever the stakeholder was:

- **The order due cards are presented in** — oldest-due first, insertion order, or shuffled. No
  criterion depends on it; AC1 is written over "each due card" rather than over a sequence.
  Recorded here as deliberately unconstrained, left so by `refine` (Definition of Ready R10).
- **The wording of the prompts, the two grade responses, and the nothing-due message.**
  `ADR-0001` reserves message wording to `plan`. AC3 names the two responses, and AC5 and AC6 the
  nothing-due message, by reference to the tool's own documentation rather than fixing tokens
  here — the way WI-0001 AC7(a) did for the deck path. **So `plan` must document all three:** a
  criterion that points at documentation fails if the documentation is not written.
- **The exit code of a sitting that ends early** (AC9). AC9 requires only that it ends without a
  traceback. Deliberately unconstrained, left so by `refine`.
- **The placeholder forward step** that makes AC8 true before WI-0003 exists. It must stop the
  card being due for the rest of the day and must be cheap for WI-0003 to replace.

**Accepted at review, and recorded here so they survive this item's closing.** The full
reasoning is in `artifacts/review.md` §"Accepted gaps"; these are the four a later reader needs.

- **A stranded doc-comment in `recall/cli.py`** (review finding F2). The `#:` block describing
  `REVEAL_PROMPT`/`GRADE_PROMPT` — *"neither may carry the card's text"*, which is AC1's guard —
  sits above `RIGHT_RESPONSE`/`WRONG_RESPONSE` instead, and the prompts carry no comment. Not
  blocking: the same rule is restated in `_read_grade`'s docstring and in `plan.md` §Approach, and
  `test_due_cards_are_presented_one_at_a_time` fails if a prompt ever echoes the question side.
- **`BUG-0001` is untouched, and a passing AC7 is not evidence about it.** `review` reaches the
  deck through the same `store.load` as `add` and `list`, so it inherits the same weakness with
  filesystem errors that are not deck-*content* problems. Deliberate: `plan.md` §Risks requires
  it and the bug is already open at `ready`.
- **A sitting spanning midnight is unexercised**, because `datetime.date.today()` is read once per
  process with no injectable clock. No criterion covers it; a suite started seconds before
  midnight can flake, which is a re-run and not a defect.
- **Presentation order is deck order and no criterion constrains it.** `refine` left it
  deliberately unconstrained and `plan.md` chose deck order with its reversal cost recorded. A
  later change to the order would break no criterion of this item.

**Added at the second review, when the item was accepted and closed.** The full reasoning is in
`artifacts/review.md` §Findings; these three are what a later reader — WI-0003's author above all
— needs.

- **`record_answer`'s docstring overclaims conformance to `ADR-0002`, and WI-0003 must not
  inherit the claim** (review finding F1). `recall/deck.py:100` says *"For a wrong answer this
  already is ADR-0002's rule"*, and `plan.md` §Assumptions says the same with the word
  *"exactly"*. It is not exact. `ADR-0002` §Decision 6 has **two** clauses — *"Wrong sends the
  card back to the first rung, so its next review is one day after the day it was reviewed"* —
  and the placeholder satisfies only the second. `rung` is left untouched whatever the answer,
  which is deliberate and correct for this item. **So WI-0003 has to add the rung reset for a
  wrong answer as well as the ladder walk for a right one.** The two coincide today only because
  nothing has ever moved a card off `FIRST_RUNG`. Accepted rather than sent back because it
  breaks no criterion, is not in `docs/`, and lives in the one function `plan.md` says WI-0003
  replaces — so a note here reaches its audience and a reworded docstring would not.
- **Two documents carry a stale enumeration from when there were two subcommands** (review
  finding F2), neither of them false about the rule it states: `ADR-0004` §5 says *"both
  subcommands report the path"* where there are now three, and `docs/architecture/overview.md`
  says the load path serves *"`add`, `list` and, later, `review`"*. The one-clause fixes are
  "every subcommand that reads the deck" and dropping "later"; worth taking by whichever item
  next opens either file. Accepted because the substance of both sentences is true and neither
  can cause a reader to act wrongly — the line the review draws between a stale enumeration and
  the false claim it rejected the first time.
- **"Every card is still on the bottom rung `recall add` put it on" is true of every card the
  tool creates, and defeasible by hand-editing the deck** (review finding F3, raised by `verify`
  as O1). `store` round-trips whatever integer `rung` the file holds. Left as written, because
  the sentence's citation supports exactly what it asserts about the cards `recall add` makes and
  its operative promise holds for a hand-edited card too. The tightening, if a later reader wants
  it, is *"every card `recall add` made"*.

**How this item sits against `BUG-0001`.** The bug is open at `ready` against `add` and `list`
for filesystem errors that escape as tracebacks. AC7 here is about deck *content*, which is the
same rule WI-0001 AC8 already carries. If `review` is built on the same `store.load`, fixing
`BUG-0001` fixes it for `review` too — but no criterion of this item covers that, and `verify`
must not read a passing AC7 as evidence about the bug.
