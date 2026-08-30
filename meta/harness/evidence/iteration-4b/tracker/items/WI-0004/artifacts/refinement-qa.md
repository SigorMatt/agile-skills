---
status: recorded
---

# Refinement Q&A — WI-0004

**This file is the record of the exchange.** It was written as an agenda when round 1's two
questions were filed on 2026-08-30T04:24Z and the stakeholder had not yet answered; they answered
both, `answer-questions` propagated the answers into `item.md` on 2026-08-30T04:31Z, and this
second `refine` execution rewrote the criteria and flipped the file to `status: recorded`. Round
1 is the only round: no second round was needed, and the reasons the remaining gaps were not put
to the stakeholder are in `## Round 1 — decided here, not asked` below.

## What was read before asking

- `tracker/items/WI-0004/item.md` — the draft, its four criteria, its four exclusions, and its
  `## Notes`, which name exactly one thing as `refine`'s to settle with the stakeholder.
- `tracker/items/WI-0004/history.md` — one row, `— → draft`, actor `answer-questions`. This is a
  **fresh** draft created when an answer widened the scope, not an item sent back from a later
  stage, so the whole story is open rather than one named defect.
- `tracker/items/WI-0004/journal.md` — `answer-questions`' creation entry, which records that
  how a card is named when deleting it was deliberately left undecided and why.
- Every human answer in this workspace: `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`,
  `Q-003.md`; `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md`;
  `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md`.
- `tracker/items/WI-0001/item.md` — the delivered criteria a delete command can collide with,
  AC3 (what `recall list` prints) and AC9 (duplicate questions are allowed) in particular.
- `tracker/items/WI-0002/item.md`, `tracker/items/WI-0003/item.md` — the delivered review and
  scheduling behaviour AC3 of this item has to hold against.
- `docs/architecture/adr/ADR-0001-a-command-line-interface.md` (v1) — §2 already reserves a
  subcommand for this item; §5 fixes exit codes.
- `docs/architecture/adr/ADR-0004-the-deck-file.md`, `ADR-0006`, `ADR-0008` — the deck file's
  format, what a card carries, and what an unreadable deck does.
- `docs/process/using-recall.md` (v5) — what the tool tells a person today.
- `recall/cli.py`, `recall/deck.py`, `recall/store.py` — what `list` actually prints, what a
  `Card` actually holds, and what `Deck` can actually do, so that the options put to the
  stakeholder describe the tool that is there rather than one we imagine.

## The Definition of Ready gaps that set this agenda

Recorded before the questions were written, per the procedure. `R` numbers are
`spec/dor-dod.md` §1.

The `Verdict now` column below is **round 1's** verdict, written before the questions were sent.
The `Verdict at close` column is this execution's, after the answers landed. Both are kept: the
first is what set the agenda, the second is the `definition-of-ready` gate's per-criterion
result.

| # | Verdict now | Why |
|---|-------------|-----|
| R1 | pass | frontmatter complete; `type`, `epic` and `priority` all set (`validate-workspace`, exit 0, 0 errors) |
| R2 | pass | role ("someone whose deck has accumulated over weeks"), capability ("remove a card I no longer need"), and a "so that" outcome |
| R3 | pass | four criteria, labelled `AC1`–`AC4`, all checkboxes |
| R4 | **fail** | not one criterion names an invocation. All four turn on the phrase "deleting a card" and nothing says how a card is named, so there is no command to run. AC4 — "asking to delete a card that does not exist" — cannot even be stated until it is settled what naming a card means. This is `Q-001` |
| R5 | pass | four exclusions, and the first of them (editing) is precisely what a reader would assume an item about removing cards had swallowed |
| R6 | **fail by this execution's own doing** | `Q-001` and `Q-002` are open and blocking. That is the suspension working, not a defect in the item |
| R7 | pass | `depends-on: WI-0001`, which is `done` |
| R8 | **fail** | this file, and it says `agenda` |
| R9 | pass | one coherent change: a `delete` subcommand, a removal on `Deck`, and the documentation. Not two items |
| R10 | **fail** | the combinations this item introduces are not all visible. Named here so that none of them is lost: (a) deleting when two cards share the named question, which `WI-0001` AC9 deliberately permits — folded into `Q-001`, because each option answers it differently; (b) whether the removal is guarded by a confirmation, which is `Q-002`; (c) deleting the last card in the deck, leaving it empty; (d) deleting when the deck file is absent, and when it exists but cannot be read; (e) whether a deletion is visible to `recall list`, to `recall review`, and after the process ends — AC1, AC2 and AC3 cover the three; (f) whether `delete` and the scheduling interact at all. (c) to (f) are `refine`'s to write as criteria once `Q-001` and `Q-002` are answered, and are not questions for the stakeholder |

## Round 1 — asked

Both questions were filed as one ask, on 2026-08-30T04:24Z, and both are blocking. The item is
suspended at `awaiting-answer` with `resume-to: draft`.

### Q1 — `questions/Q-001.md`: how do you say which card you mean?

> When you delete a card, how do you tell `recall` which card you mean?

Three options were put: **A** a number `recall list` would print at the front of each line; **B**
the question side itself, with an ambiguous match refused; **C** a short fixed code stored on
each card and printed by `recall list`. The team's preference, stated last and marked as ours,
is **B**, with its hole named — B is the only one of the three that leaves a person unable to
remove either of two cards that share a question.

**Answer:** `[human]` **B.** *"B — let me just type the question, that's the most natural way
for me to say which card I mean. If I ever end up with two cards that share a question, I'll deal
with that separately; it's not worth building for."* Propagated into `item.md` by
`answer-questions` on 2026-08-30: the invocation is `recall delete --question "<text>"`,
`recall list` is unchanged, and a text matching two or more cards refuses the deletion and removes
nothing. The hole in B — no way to remove either of two cards sharing a question — was put to them
and accepted, and is now an `## Out of scope` bullet.

### Q2 — `questions/Q-002.md`: does deleting stop to check with you?

> When you delete a card, should `recall` show you the card and ask you to confirm before
> removing it, or just remove it?

Three options were put: **A** remove it and print what went; **B** show the card and ask
`delete this card? [y/n]`; **C** ask by default with a `--yes` to skip. The team's preference,
stated last and marked as ours, is **B**.

**Answer:** `[human]` **B.** *"B — show me the card and ask first. I'd rather have one extra
keypress than lose a card to a typo."* Propagated into `item.md` by `answer-questions` on
2026-08-30: `recall delete` prints both sides of the card and asks `delete this card? [y/n]`,
removing it on `y` and leaving the deck untouched on anything else, with no flag to skip. Option
C's `--yes` is now an `## Out of scope` bullet, so its absence is a recorded decision.

## Round 1 — the Definition of Ready at close

Written by this execution, after the two answers landed and the criteria were rewritten. This is
the `definition-of-ready` gate's evidence, criterion by criterion, and it supersedes nothing in
the table above — that table is round 1's verdict and is kept as the record of what set the
agenda.

| # | Verdict at close | Evidence |
|---|------------------|----------|
| R1 | pass | `validate-workspace` exit 0; `type: work-item`, `epic: EP-001`, `priority: medium` all set |
| R2 | pass | unchanged from round 1: role, capability and a "so that" outcome |
| R3 | pass | twelve criteria, `AC1`–`AC12`, every one a checkbox; `validate-workspace` exit 0 |
| R4 | **fail → pass.** Round 1's four criteria all read "after deleting a card" with no invocation anywhere. Rewritten as twelve, each naming a command to run and what would be observed. The preamble fixes the three things they all lean on — the invocation, what "the card whose question is X" means, and that no criterion fixes a message or a particular non-zero exit value. No criterion carries an unmeasurable adjective: the words that would have been "safely", "gracefully" and "cleanly" are AC6 ("the deck file's bytes identical before and after"), AC8 ("names the file … bytes identical") and AC10 ("the documented empty-deck message … exits 0") | see `criteria-are-decidable` in the journal for the command settling each of the twelve |
| R5 | pass | `## Out of scope` has six entries, and two of them are exactly what a reader would assume this item included: editing a card, and some way of picking between two cards that share a question |
| R6 | **fail → pass** | `Q-001` and `Q-002` are both `status: answered`; no question on this item is open, blocking or otherwise |
| R7 | pass | `depends-on: WI-0001`, which is `done` |
| R8 | **fail → pass** | this file, and it now says `recorded` |
| R9 | pass | one coherent change: a `delete` subcommand, a removal on `Deck`, and the documentation. AC12 is a read of two delivered criteria, not a second body of work |
| R10 | **fail → pass** | every combination is accounted for, and the map is in the item's `## Notes` under the R10 heading — twelve criteria and two `## Out of scope` bullets between them cover (a) to (f) from round 1's list, plus two combinations that list missed |

## Round 1 — decided here, not asked

Three gaps were left after the two answers landed. None was sent to the stakeholder, and the
reason is recorded for each rather than left to be inferred. All three are `[assumed]`, all three
are written into the item's `## Notes`, and all three are cheap to reverse.

- **What "the card whose question is X" matches — exactly, byte for byte.** `[assumed]`
  Rests on delivered behaviour rather than on a deferral: `WI-0001` AC3 stores and prints a
  question side *"exactly as it was given — no trimming …, no case change, no truncation"*, so
  the string the person types is the string the listing showed them. Not asked because the
  failure mode is benign and visible — AC4 refuses and removes nothing, so a too-strict match
  costs a retype — and because the looser alternatives would let a typed string match a card
  they did not mean, which is the accident `Q-002`'s own answer is against. Recorded in
  `## Notes` as reversible with product stake: if exact matching is annoying in use, that goes
  to the stakeholder rather than being loosened here.
- **What `recall delete` exits with when the person declines — 0.** `[assumed]`
  `ADR-0001` §5 reserves non-zero for *"a refused or failed operation"*, and a person answering
  `n` got what they asked for. Not asked because it is an exit code, which is squarely inside
  the category their *"nothing fancier than that"* (`EP-001/Q-001`) defers, and because AC6
  makes the outcome observable on stdout regardless of what the exit code turns out to be.
- **The wording of every message, and the particular non-zero values.** `[assumed]`
  The same standing deferral, already recorded as `plan`'s in `EP-001/Q-002`'s consequences. No
  criterion here fixes a sentence; AC10 names the empty-deck message by reference to the tool's
  own documentation — the device `WI-0001` AC7(a) and `WI-0002` AC5 use — which obliges `plan`
  to document it rather than leaving it to `implement` to invent.

## Cross-answer check

Both of round 1's answers were checked against every prior recorded human answer when
`answer-questions` consumed them; the verdicts are in `questions/Q-001.md` and `questions/Q-002.md`
under their own `## Cross-answer check` headings, and none is `conflicts`. This execution wrote
twelve criteria and three assumptions from those answers, so the check is repeated here for what
was written rather than for what was said:

Checked against: `EP-001/Q-001`; `EP-001/Q-002`; `EP-001/Q-003`; `WI-0002/Q-001`;
`WI-0002/Q-002`; `WI-0003/Q-001`; `WI-0003/Q-002`.

- `EP-001/Q-001` — **compatible.** *"I want to be able to delete a card I don't need anymore"* is
  what AC1 delivers. *"Don't lose my progress"* is what AC5, AC6, AC8 and AC11 protect: nothing is
  removed on an ambiguous match, on anything but `y`, or on a deck that cannot be read, and the
  surviving cards' `rung` and `due` are untouched. *"Nothing fancier than that"* is why AC6 asks
  once instead of re-asking and why no criterion fixes a message.
- `EP-001/Q-002` — **compatible.** Every criterion is a command with an exit code and some text on
  a stream, which is what the command-line choice makes possible.
- `EP-001/Q-003` — **compatible.** It settles how a card is graded and rescheduled. AC11 is the
  criterion where the two meet, and it requires the ladder to be left alone by a deletion rather
  than altering it.
- `WI-0002/Q-001` — **compatible.** No cap on a sitting; AC3 only removes cards from a sitting,
  never bounds it.
- `WI-0002/Q-002` — **compatible.** A card added today is due today; AC10's closing check
  (`recall add` after the last card is deleted) exercises that rule and does not change it.
- `WI-0003/Q-001` — **compatible.** The ladder stops at a month; AC11 requires `rung` and `due` to
  survive a deletion unchanged, which is that decision holding rather than being touched.
- `WI-0003/Q-002` — **compatible.** A sitting prints each card's next date; AC12 keeps `recall
  list` as it is, and no criterion here changes what a sitting prints.

No verdict is `conflicts`, so no question was filed under ADR-0008 §3, and no recorded sentence of
theirs was reworded anywhere in this execution.

## What was deliberately not asked, and why

Recorded so that a later reader can see the questions that were considered and dropped, rather
than only the two that were sent.

- **What `recall delete` prints on success, and what exit code it uses when it refuses.** Not
  asked. `ADR-0001` §5 already fixes exit codes — `0` for success, non-zero for a refused
  operation with the reason on standard error — and the stakeholder's *"nothing fancier than
  that"* (`EP-001/Q-001`) is a standing deferral over message wording, which
  `EP-001/Q-002`'s consequences record as left to `plan`. `refine` will write the criteria
  against ADR-0001 §5 and mark the wording `[assumed]`.
- **Whether deleting more than one card in one invocation should be possible.** Not asked; it is
  already in the item's `## Out of scope`, put there when the item was created.
- **Whether a deleted card can be recovered.** Not asked; also already excluded, and `Q-002`
  states the exclusion to the stakeholder in its `## Context` rather than reopening it, because
  the guard question is meaningful only if the deletion is final.
- **This item's priority.** The item's `## Notes` say *"The stakeholder did not rank it;
  `refine` may."* Left at `medium`. It is the last item in the epic, nothing depends on it, and
  a rank the stakeholder did not ask for is not worth a question — this is `refine`'s decision
  and is recorded as such, not as theirs.
- **How the deletion is implemented** — where the removal lives, whether `Deck` grows a method,
  how the file is rewritten. Design, and `plan`'s under its own preference order. `ADR-0004` §4
  already fixes that every write is atomic, so the one part of this with a stake in the
  stakeholder's *"don't lose my progress"* is already decided.
