---
title: rung is the index of the gap the next correct answer applies, and a stored value outside the ladder is an unreadable deck
version: 1
status: current
updated: 2026-08-30T03:50:43Z
updated-by: plan
updated-for: WI-0003
---

# ADR-0008 — `rung` is the index of the gap the next correct answer applies, and a stored value outside the ladder is an unreadable deck

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** plan (architect), for WI-0003
- **Supersedes:** — (extends `ADR-0002`, which fixes the ladder, and `ADR-0004`, which fixes the
  deck file; nothing in either is reversed [src: ADR-0002; ADR-0004])

## Context

WI-0003 is the item that first reads `rung` back. Until now nothing did: `recall add` writes
`0` and `record_answer` returns the card with `rung` untouched, whatever was answered
[src: recall/deck.py:73; recall/deck.py:92]. So the field has been written and round-tripped for
two items without anyone having to say precisely what a given integer means.

Two standing sentences describe it and they do not pick out the same integer.

- `ADR-0004` §2 says `rung` *"is the index into `ADR-0002`'s ladder"*, and that `add` writes
  `0` [src: ADR-0004].
- `ADR-0002` §3 says a new card *"starts below the ladder"*, and §4 says a right answer
  *"moves the card up one rung, and its next review is that rung's number of days after the day
  it was reviewed"* [src: ADR-0002].

Read together: a new card is at `0`, `0` is an index into `[1, 3, 7, 30]`, and the card is
nonetheless *below* the ladder. Both sentences are satisfiable at once, but only if someone says
whether `rung: 2` means the card has taken the 3-day gap or is about to take the 7-day one. The
difference is one integer in the file and nothing else — every observable date is identical under
both readings, which is exactly why nobody has had to decide it and why WI-0003's refinement
routed it here rather than to the stakeholder [src: tracker/items/WI-0003/item.md].

The second question is what happens when the integer is outside the ladder — a hand-edited deck,
or one written by a later version. Today `store.py` accepts any integer and `load` returns it
unchanged [src: recall/store.py:115]. Once the arithmetic indexes the ladder with it, an
out-of-range value has to mean something, and "whatever Python does" means an `IndexError` and a
traceback — the failure `BUG-0001` was filed about [src: tracker/items/BUG-0001/item.md].

## Options considered

**On what `rung` counts:**

- **A — the index of the gap the *next* correct answer applies.** `0` means the next correct
  answer moves the card one day out; `3` means thirty days. Cost: nothing to change — it is the
  value `add` already writes [src: recall/deck.py:73], and it satisfies `ADR-0004` §2's "index
  into the ladder" word for word [src: ADR-0004]. Risk: `ADR-0002`
  §4's phrasing has to be read as describing the same step from the other end — the card takes
  the rung it had not yet taken. **Chosen.**
- **B — the number of rungs climbed, `0` meaning below the ladder and `4` meaning the top.**
  Cost: also none, and it matches `ADR-0002` §3 and §4 phrase for phrase. Risk: it makes `rung`
  a one-based position rather than an index, which contradicts `ADR-0004` §2 in the only sentence
  that ever defined the field; correcting that sentence would be an erratum against an ADR whose
  decision is not wrong.
- **C — store the gap in days rather than a position.** Cost: a format change and a migration,
  for a field two items already write. Risk: it puts the ladder's numbers in every deck file, so
  changing the ladder later would mean rewriting decks rather than one constant — the opposite of
  the reversibility `ADR-0002` claims.

**On an out-of-range stored value:**

- **D — refuse the deck**, as `DeckUnreadable`, named like any other malformed field. Cost: one
  range check beside the type checks already in `_card_from` [src: recall/store.py:115]. Risk: a
  deck a person hand-edited badly stops working until they fix it. **Chosen.**
- **E — clamp it into range** and carry on. Cost: one `min`/`max`. Risk: it silently reschedules
  somebody's cards, and it is precisely the repair `ADR-0004` §5 refuses — *"a deck that cannot
  be read is never repaired"* [src: ADR-0004]. A person who typed `40` and meant `3` would be
  told nothing.
- **F — leave it undefined.** Cost: none now. Risk: an `IndexError` and a traceback, which is a
  defect this project has already filed once [src: tracker/items/BUG-0001/item.md].

## Decision

1. **`LADDER = (1, 3, 7, 30)`, in days, lives in `recall/deck.py`** beside `FIRST_RUNG`, which
   stays `0` [src: recall/deck.py:16]. It is the machine-readable form of `ADR-0002` §2 and the
   only place the four numbers appear in code.
2. **`rung` is the index into `LADDER` of the gap the next *correct* answer will apply.** A card
   at `rung: 0` — every card `recall add` writes [src: recall/deck.py:73] — is moved one day out
   by its next correct answer. A card at `rung: 3` is moved thirty days out, and stays at `3`.
3. **A correct answer applies `LADDER[rung]` and then advances**: the card's next review is
   `LADDER[rung]` days after the day of the sitting, and its stored `rung` becomes
   `min(rung + 1, len(LADDER) - 1)`. The `min` is `ADR-0002` §5 — the gap holds at thirty days
   and there is no fifth rung [src: ADR-0002].
4. **A wrong answer returns the card to `FIRST_RUNG` and applies `LADDER[FIRST_RUNG]`**: stored
   `rung` becomes `0` and the next review is one day after the day of the sitting. That is both
   clauses of `ADR-0002` §6 in one step, and it makes a missed card indistinguishable from a
   fresh one, which is what *"it goes back to the start"* says [src: EP-001/Q-003].
5. **Both gaps are counted from the day of the sitting**, never from the date the card was due
   [src: ADR-0002]. An overdue card is not compensated and not penalised.
6. **A stored `rung` outside `0 … len(LADDER) - 1` is `DeckUnreadable`**, raised by
   `store.load` with the card named, exactly as an unrecognised `grade` is
   [src: ADR-0006; recall/store.py:115]. It is not clamped and not repaired [src: ADR-0004].
   Because validation happens at load, everything downstream of it — `record_answer` included —
   may assume the value is in range and does not re-check.
7. **`DECK_FORMAT_VERSION` stays at 1.** No key is added, no key changes type, and no deck any
   version of this tool has written carries a `rung` other than `0`, because nothing until now
   ever changed it [src: recall/deck.py:92]. This is a tightening of an existing field's legal
   values, not a migration.

## Consequences

- The arithmetic is four lines in `recall/deck.py` and reads as `ADR-0002` §4 to §6 in order,
  which is what makes WI-0003 AC1 to AC3 checkable by a reader as well as by a test
  [src: tracker/items/WI-0003/item.md].
- The four numbers exist once in the code. Changing the ladder — which the stakeholder said they
  might want if their deck grows [src: WI-0003/Q-001] — is editing `LADDER` and nothing else.
- Every criterion WI-0003 carries is independent of this decision: none of them reads or writes
  `rung`, deliberately [src: tracker/items/WI-0003/item.md]. So §2's choice between A and B could
  be reversed without touching a single criterion.
- One existing unit test asserts the placeholder's behaviour directly — it builds a card at
  `rung: 4` and requires a wrong answer to leave it there [src: tests/test_review.py:263]. Under
  §4 a wrong answer resets it, and under §6 `4` is not a legal stored value at all. That test is
  asserting the placeholder WI-0003 exists to replace, and WI-0003 rewrites it. No deck file in
  any test carries a `rung` other than `0` [src: tests/support.py:135].
- A person who hand-edits their deck and mistypes the rung is told, on the next command, which
  card and which field — rather than being silently rescheduled or shown a traceback.
- **Reversibility: high, and different for the two halves.** §2's encoding is one file and no
  data migration: swapping to option B means changing `record_answer` and the range in §6, and
  rewriting the integer in decks in the field, of which there are none outside a test. §6 is one
  branch in `_card_from`; removing it restores today's behaviour exactly. Neither is a published
  interface: `rung` is documented as ordinary JSON a person may read [src: docs/process/using-recall.md],
  not as a format anything else consumes.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T03:50:43Z | plan | WI-0003 | First version, deciding what `rung` counts and what an out-of-range stored value does, while planning WI-0003 |
