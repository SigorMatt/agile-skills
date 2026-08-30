---
title: A sitting records the last answer as an optional card field, and the deck format version does not move
version: 1
status: current
updated: 2026-08-30T02:38:36Z
updated-by: plan
updated-for: WI-0002
---

# ADR-0006 — A sitting records the last answer as an optional card field, and the deck format version does not move

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** plan (architect), for WI-0002
- **Supersedes:** — (extends `ADR-0004`, which fixes the deck file; nothing in it is reversed
  [src: ADR-0004])

## Context

WI-0002 asks for a sitting that presents the due cards and records how each one went. Its
`## Out of scope` draws the line for this item at *"an answer is captured and stored against the
card, and that the card stops being due for the rest of the day"* [src: WI-0002]. The first half
of that sentence is a storage question and `ADR-0004` owns storage, so it is answered here rather
than in a plan step.

What the record already fixes, and what it does not:

- A card is stored with exactly four keys — `question`, `answer`, `rung`, `due` — and `load`
  raises `DeckUnreadable` when any of them is missing or of the wrong type
  [src: recall/store.py:112].
- `ADR-0002` settled what scheduling needs per card: a ladder position and a next-review date,
  and no ease factor [src: ADR-0002]. It did not say anything about keeping the answer itself,
  because scheduling does not need it — the next date is computed at the moment the answer is
  given [src: ADR-0002].
- Grading is two-way, right or wrong, never a scale [src: EP-001/Q-003; ADR-0002].
- `ADR-0004` §3 writes a `version` into the file *"so a later format change is a migration"*
  [src: ADR-0004].

So the question is genuinely open, and it is a storage-shape question rather than a plan step:
does a sitting leave anything behind about the answer itself, or only its consequence?

## Options considered

- **A — An optional `grade` key on each card**, holding `"right"` or `"wrong"`, absent until the
  card has been reviewed. Cost: one key, one branch on read, one branch on write. Old decks —
  every deck any user has today, since `add` has never written it — load unchanged, because they
  simply lack the key. Risk: it is one more thing `load` must validate, and a value outside the
  two words has to be rejected rather than ignored, or `ADR-0004` §5's "a deck that cannot be
  read is never repaired" quietly weakens into "unless the damage is in a field we added later".
- **B — Store nothing but the consequence.** The answer changes `due` (and later `rung`) and is
  then forgotten. Cost: none; the format does not move at all. Risk: it does not do what the item
  asks. *"Stored against the card"* is the item's phrase and B stores nothing against the card.
  It also forecloses cheaply-answerable questions later — "when did I last get this wrong" needs
  a field that was never written, and no amount of schedule state reconstructs it.
- **C — An append-only review log**, a second array in the deck file recording every answer with
  its date. Cost: materially more — a second structure to validate, and a file that grows without
  bound on a deck a person reviews daily for years. Risk: it is the natural substrate for
  statistics and streaks, which the epic excludes in terms [src: docs/product/vision.md]. Building
  the storage for an excluded feature is how the exclusion stops holding.
- **Recommendation and choice: A.** It is what the item asked for, at the smallest size that
  means anything. C is where this would go if statistics were ever wanted, and A does not block
  it: a log can be added later beside the field.

## Decision

1. **Each stored card may carry a fifth key, `grade`**, whose only legal values are the strings
   `"right"` and `"wrong"`. It records the most recent answer, not a history.
2. **The key is optional on read.** A card entry without it loads as a card whose grade is
   unknown, which is what every card written by `recall add` is [src: recall/deck.py:48]. This is
   not leniency about damage: the four keys `ADR-0004` fixed remain required, and their absence
   remains `DeckUnreadable` [src: ADR-0004].
3. **A `grade` key that is present and is not one of the two words is `DeckUnreadable`**, named
   like any other malformed field. `ADR-0004` §5 refuses to repair a deck it cannot read, and a
   field added later is not exempt from that.
4. **The key is written only when it has a value.** A card that has never been reviewed is
   serialised with four keys exactly as before, so a deck of unreviewed cards is byte-identical
   to what WI-0001 wrote.
5. **`DECK_FORMAT_VERSION` stays at 1.** The change is additive and optional in both directions:
   a deck written before it loads without it, and a deck written after it would load in the
   earlier code, which ignores keys it does not know [src: recall/store.py:112]. `ADR-0004` §3's
   version exists for a change that would make one of those two false, and spending it on a
   compatible extension would leave nothing to distinguish a real migration by.

## Consequences

- WI-0002 AC3's *"the run records whether the person recalled it"* has somewhere to be recorded
  [src: WI-0002 AC3], and WI-0002 AC10's requirement that both sides of every card are unchanged
  after a sitting stays easy to hold, because nothing else about the card is touched
  [src: WI-0002 AC10].
- WI-0003 inherits a field it does not have to add. It changes `rung` and `due`; `grade` is
  already there and already validated.
- A person reading their deck in an editor can see how the last sitting went. `ADR-0004` chose
  JSON partly so that reading it by hand is possible.
- The epic's exclusion of statistics is not weakened: one field holding one word supports no
  streak and no dashboard, and option C — the shape that would — was rejected for that reason.
- **Reversibility: high.** Removing the field is deleting one branch in `_card_to_entry`, one in
  `_card_from`, and one dataclass field; decks already carrying it would still load under the
  four-key rule, because an unknown key is ignored. Adding a review log later (option C) is not
  made harder by this and does not require undoing it.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T02:38:36Z | plan | WI-0002 | First version, deciding what a sitting stores against a card while planning WI-0002 |
