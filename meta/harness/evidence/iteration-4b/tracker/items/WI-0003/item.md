---
id: WI-0003
type: work-item
title: Space each card's next review according to how it was recalled
status: done
priority: high
epic: EP-001
created: "2026-08-30T01:30:04Z"
updated: "2026-08-30T04:20:06Z"
depends-on:
  - WI-0002
branch: wi/WI-0003
outcome: delivered
---

## Story

As someone reviewing daily, I want each answer to decide when I next see that card, so that the
cards I know drop out of my way and the ones I keep missing come back quickly.

## Acceptance criteria

Every criterion below is written against the invocation `ADR-0001` fixes: one executable named
`recall`, with `review` as a subcommand, interactive on standard input so that a here-document
drives it (`ADR-0001` §4). "The deck file" means the single file at
`$HOME/.local/share/recall/deck.json` in the format `ADR-0004` §2 fixes, and a criterion that
needs a card in a particular state sets it up by writing that file directly — the device
`WI-0002` used.

**How these criteria compress the calendar, and why it matters.** The ladder takes a hundred
days to walk in real time. Every criterion below instead sets a card's `due` field to today and
runs another sitting, **leaving every other field exactly as the tool wrote it**. That is
faithful rather than a trick: `ADR-0002` §4 counts the next gap from *the day the card was
reviewed*, not from the day it was due, so a card reviewed on the day its `due` says is
indistinguishable from one reviewed after a wait. It also keeps these criteria independent of
**how** a ladder position is stored, which is `plan`'s to decide (`## Notes`) — nothing below
reads or writes `rung`.

- [x] AC1 — **A card recalled correctly walks the ladder 1, 3, 7, 30 days and then holds at 30.**
      With the deck file absent, run `recall add --question <text> --answer <text>`. Then five
      times in succession: set that card's `due` in the deck file to today, leaving every other
      field as the tool left it, and run `recall review` driven by a here-document that reveals
      the answer and responds right. The `due` the tool writes after the five sittings is, in
      order, today + 1, today + 3, today + 7, today + 30 and today + 30 days. The fifth is the
      criterion's point: the gap grows on every correct answer until 30 days and then stops
      growing, with no fifth rung (`ADR-0002` §5, chosen by the stakeholder in `Q-001`).
- [x] AC2 — **A card the person did not recall is due one day after the sitting, from any rung.**
      Two observations, and the second is what makes the ladder position's reset visible rather
      than only the date's:
      (a) With a freshly added card due today, `recall review` answering wrong writes
      `due` = today + 1 — one day after the sitting, never later the same day.
      (b) Run AC1's procedure through four sittings, so the card's last gap was 30 days. Set
      `due` to today and answer **wrong**: the tool writes `due` = today + 1. Set `due` to today
      again and answer **right**: the tool writes today + **1**, not today + 30. A tool that
      moved the date but left the ladder position alone would write today + 30 here and fail.
- [x] AC3 — **A gap is counted from the day of the sitting, including when the card is overdue.**
      With a deck file holding one card whose `due` is ten days before today and whose other
      fields are as `recall add` writes them, `recall review` presents it (`WI-0002` AC13) and,
      answered right, writes `due` = today + 1 — not ten days ago plus one, which would be nine
      days in the past. Answered wrong instead, it writes `due` = today + 1 as well. Missing days
      never leaves a card stranded behind the present.
- [x] AC4 — **The sitting says when the card is next due, as the answer is recorded.** After each
      graded card, and for a wrong answer as well as a right one, stdout carries that card's new
      next-review date written as `YYYY-MM-DD` — the same string the tool writes into that card's
      `due` — after that card's answer side and before the next card's question side. Checkable
      inside AC1's and AC2's runs, and it must be demonstrated at two different gaps and on both
      answers, so that printing a constant fails: the first sitting of AC1 prints today + 1, the
      fourth prints today + 30, and AC2(b)'s wrong answer prints today + 1. Anything else the
      line says is `plan`'s (`ADR-0007` §2); the date's form is fixed here only so this criterion
      can be read by someone with a terminal, and `## Notes` records that as `refine`'s decision.
- [x] AC5 — **The rule is written down well enough to work a date out by hand, and the tool
      agrees.** `docs/process/using-recall.md` states all five of: the gaps 1, 3, 7 and 30 days;
      that the gap holds at 30 and never grows past it; that a wrong answer returns the card to
      the start of the ladder; that a gap is counted from the day of the sitting even when the
      card is overdue; and the worked example — a card added on day 0 and answered right every
      time is due on days 0, 1, 4, 11, 41, 71 and 101, and a card answered wrong on any sitting
      is due the day after that sitting. A reader following only that section reaches the same
      dates AC1 to AC3 observe. The section "What this version does not do yet" no longer says
      scheduling is unbuilt or that a reviewed card comes back tomorrow whatever the answer.
- [x] AC6 — **The criteria this item could invalidate still hold, read as text.** The criteria
      covered are `WI-0001` AC1 to AC9 and `WI-0002` AC1 to AC13, named here by ID rather than as
      "the earlier criteria". The assessment is a **read of those criteria's wording against the
      behaviour this item ships**, with the test suite as evidence for the answer rather than as
      its definition; a green suite that never exercises a criterion is not that criterion
      holding. Four are known to be where this item bites and must be read explicitly:
      `WI-0002` AC8 (a card finished in one sitting is not presented again the same day — every
      gap here is at least one day), `WI-0002` AC10 (both sides of every card unchanged after a
      sitting, and its `grade` still recorded per `ADR-0006`), `WI-0002` AC13 (an overdue card is
      still presented), and `WI-0001` AC3 (`recall list` still prints `question | answer` and
      nothing more — `ADR-0007` §4 leaves it alone). Where nothing executable exercises both a
      covered criterion and this item's new behaviour, say so in the verification record, then
      either add a covering case or waive that criterion **by ID** with the reason.

## Out of scope

- Letting the person tune the schedule (ease factors, custom intervals, per-card overrides).
- Rescheduling cards in bulk, or repairing a schedule after a gap in reviewing.
- Any interface for seeing the schedule other than what a review run already shows. In
  particular `recall list` gains nothing: it keeps printing `question | answer` and no dates.
  That was option C of `Q-002` and the stakeholder did not choose it (`ADR-0007` §4).
- A summary or tally at the end of a sitting. AC4 is one line per card as it is answered, and
  nothing accumulates across the sitting (`ADR-0007` §3).
- Any record of *past* answers beyond the single `grade` field `ADR-0006` already stores. No
  history, no review log, no streak — the epic excludes statistics.
- Changing the ladder later, or a way for the person to change it. The stakeholder said they
  might revisit the top rung if their deck grows (`Q-001`); that would be a new item, not a
  setting this one builds.

## Notes

`EP-001/Q-003` is answered and the criteria above state the rule rather than its shape. The
stakeholder chose a ladder with two answers over Leitner boxes and over SM-2, and named the rungs
themselves: *"Just right or wrong, no rating scale. If I get it right it comes back later each
time — a day, then three, then a week, then a month or so. If I get it wrong it goes back to the
start."* The decision, with the arithmetic and what it costs, is `ADR-0002`.

**The clause of AC1 that was a reading is now the stakeholder's decision.** They named four
intervals and stopped at *"a month or so"*; `ADR-0002` read that as the ladder topping out and
said so as its own reading, and `refine` put all three shapes to them as `Q-001`. They chose the
ladder that stops: *"Stops at a month — option A. The whole point was simple, and I don't want to
be doing math to figure out when a card's coming back."* The ladder topping out is now AC1's
fifth sitting, and `ADR-0002` v3 records the clause as theirs rather than as ours.

**`Q-002` settled what the old AC4's word *visible* meant** — a sitting prints one line per card
saying when that card is next due, at the moment the answer is recorded. `ADR-0007` records the
decision and fixes which fact the line carries, leaving its wording to `plan`. `recall list` is
unchanged and is now named in `## Out of scope`. That answer is the new AC4.

**Round 1 of refinement was asked on 2026-08-30T03:32:14Z and both questions were answered on
2026-08-30T03:38:18Z.** Two blocking questions, filed as one ask, both addressed to the
stakeholder, both now `answered` with their consequences propagated:

- `WI-0003/Q-001` — what happens above the longest gap. Options put: stop at a month; keep
  doubling with no ceiling; grow to a ceiling they name. **Answered: stop at a month**, with the
  cost of a permanent monthly floor on a large deck put to them first and accepted — *"If my deck
  gets huge later I might change my mind, but not now."* Propagated into `ADR-0002` v3.
- `WI-0003/Q-002` — whether a sitting tells you when you will next see the card. Options put:
  say nothing; one line after each answer; a silent sitting with the date added to `recall list`.
  **Answered: one line after each answer** — *"I want to actually see it's working, and one line
  isn't going to slow me down."* Propagated into `ADR-0007`, which is new.

**Round 2 of refinement rewrote the criteria in one pass and asked nothing new**, on
2026-08-30, and the item is Ready. Four criteria became six. What changed, and why:

- The old AC1 to AC3 stated arithmetic with no way to observe it. They are now AC1 (the ladder,
  walked five sittings deep so the top rung holding is demonstrated rather than asserted), AC2
  (a wrong answer, from the bottom rung and from the top, with the ladder position's **reset**
  made visible by the answer that follows it) and AC5 (the documentation, with the five things it
  must state and the worked example, decided by reading one named file).
- The old AC4 — "visible without any further run or command" — is now AC4: the printed
  next-review date, demonstrated at two different gaps and on both answers so that printing a
  constant fails.
- **AC3 is new**: a gap is counted from the day of the sitting even when the card is overdue.
  That combination was `[assumed]` in round 1's Q&A rather than written down, and R10 wanted it
  visible. It is not a new requirement — `ADR-0002` §4 already said it — but nothing was checking
  it, and `WI-0002` AC13 makes overdue cards a real case.
- **AC6 is new**: the criteria of `WI-0001` and `WI-0002` that this item could invalidate, named
  by ID, assessed as a read of their text with the suite as evidence rather than as definition
  (`spec/dor-dod.md`, the R10/§6a procedure).
- Nothing was asked of the stakeholder in round 2. Everything outstanding was either theirs and
  already answered (`Q-001`, `Q-002`), settled by a standing decision (`ADR-0002`, `ADR-0004`,
  `ADR-0007`), or a design choice routed to `plan` below.

`artifacts/refinement-qa.md` now says `status: recorded` and holds both rounds: round 1's
questions and the stakeholder's verbatim answers, and round 2's decisions with what each was
based on.

**Two open design questions routed to `plan` rather than to the stakeholder** (Definition of
Ready R10, recorded so they are visible rather than decided). Both would have the same answer
whoever the stakeholder was, so neither is theirs, and `refine` leaves both unconstrained:

1. **What the tool does with a card whose stored ladder position is outside the ladder** — a
   hand-edited deck, or a deck written by a later version. `recall/store.py` round-trips whatever
   integer `rung` holds, so the choice is between clamping it into range and refusing the deck as
   unreadable, which is what that module already does for an unrecognised `grade` (`ADR-0006`
   §3). No criterion above touches `rung`, deliberately, so either answer satisfies all six.
2. **How a ladder position is encoded in `rung`.** `ADR-0004` §2 fixes it as an integer index
   into `ADR-0002`'s ladder and `recall add` writes `0`; `ADR-0002` §3 says a new card starts
   *below* the ladder while §4 says a right answer moves it up one and then uses that rung's
   number. Those two readings differ by one in what `0` means, and the observable dates —
   gaps 1, 3, 7, 30, 30 from a freshly added card — are identical under both. `plan` picks one
   and says which; AC1 to AC4 are written so that the choice cannot change their verdict.

**One thing in the criteria is `refine`'s decision and not the stakeholder's:** AC4 requires the
printed next-review date to appear as `YYYY-MM-DD`. `ADR-0007` §2 leaves the line's wording to
`plan`, and this fixes one string inside it, because a criterion nobody can grep is not
decidable and R4 fails without it. It is the same form the deck file already uses (`ADR-0004`
§2) and the same one the worked example in `docs/process/using-recall.md` will carry. `plan` may
put any wording around it — *"next in 7 days (2026-09-06)"* satisfies AC4.

**Two things this item inherits from WI-0002's closing, and must not lose.** Both are in that
item's `## Notes` under what the second review added:

- `recall/deck.py`'s `record_answer` is the placeholder this item replaces, and its docstring
  overclaims: it satisfies only the second clause of `ADR-0002` §6. **A wrong answer must reset
  `rung` as well as the date** — the two coincide today only because nothing has ever moved a
  card off `FIRST_RUNG`.
- `docs/process/using-recall.md` §"What this version does not do yet" is written on the premise
  that scheduling is unbuilt, and cites `recall/deck.py:92` and `:73`. This item invalidates that
  whole section, so Definition of Done D7 and D12 land on it.

**Two things review accepted rather than sent back, recorded here so they outlive this item**
(`artifacts/review.md` F1 and F2):

1. **`ADR-0008` `## Consequences` ends with a clause this item falsified.** It reads *"No deck
   file in any test carries a `rung` other than `0`"*, which was true when `plan` wrote it and is
   no longer: `LadderStorageTests` writes decks with `rung` of `-1`, `4` and `9` to prove §6
   refuses them. `ADR-0008` §7 — that the deck format version stays at 1 — is unaffected and
   still sound, because those decks exist to be refused and nothing the tool writes carries a
   rung outside the ladder. The repair is a `spec/doc-header.md` §4b `erratum`. Review attempted
   it and reverted it: editing that paragraph trips `cross-answer-consistency`, because the block
   also carries `[src: WI-0003/Q-001]` and `transition` runs its gates before writing the journal
   bullet that would satisfy them. **The next execution to open `ADR-0008` can do it in one
   command** — review-close's journal entry on this item names `WI-0003/Q-001` on its
   `**Cross-answer check:**` bullet, and `lint-answers` scans every journal in the workspace.
2. **Fifteen line-anchored citations in `ADR-0006`, `ADR-0007` and `ADR-0008` now point at the
   wrong lines**, because this item shifted the five files they name. Nothing fails —
   `spec/doc-header.md` §4a resolves a workspace-path citation when the file exists — but the
   one-hop checkability the line numbers were carrying is gone. A convention problem rather than
   this item's defect; recorded so it is not rediscovered from scratch.

Also carried forward, from `verify-report.md` and `impl-report.md`: `docs/architecture/overview.md`
still says `store.py`'s load path serves *"`add`, `list` and, later, `review`"* though `review`
shipped with `WI-0002` — a one-line correction for whoever next opens that file, outside this
item's D12 scope.
