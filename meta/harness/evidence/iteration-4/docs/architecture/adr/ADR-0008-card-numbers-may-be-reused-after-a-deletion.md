---
title: Keep deriving the next card number from the largest one stored, and let numbers be reused
version: 1
status: current
updated: 2026-08-29T13:34:39Z
updated-by: plan
updated-for: WI-0004
---

# ADR-0008 — Keep deriving the next card number from the largest one stored, and let numbers be reused

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** plan (architect), for WI-0004
- **Supersedes:** —

## Context

`ADR-0004` chose to derive the next card number from the cards present — one more than the
largest `number` stored — over keeping a separate counter field. It weighed the cost of that
choice as *"if someone hand-deletes the last card from the file, the next card added reuses its
number. Risk: low; nothing in the epic deletes a card"* [src: ADR-0004].

WI-0004 removes that premise: `recall delete` is exactly a thing in the epic that deletes a card
[src: WI-0004]. Reuse stops being something only a hand edit can reach and becomes reachable by
two ordinary commands — delete the highest-numbered card, add another, and the new one takes the
old one's number. `refine` recorded this as a design question for `plan` rather than deciding it,
and recorded that no acceptance criterion constrains it either way [src: WI-0004].

Two things bound the decision. `AC3` requires that deleting a card does not renumber the
survivors, so whatever is chosen, a stored `number` stays with its card [src: WI-0004 AC3]. And
the store is a file the user is expected to open and edit by hand: `WI-0003` made hand-editing
`due` and `interval` the documented way to move a card [src: README.md; src: ADR-0007].

## Options considered

- **F — keep deriving it from the cards present (`ADR-0004`'s choice, re-weighed).** Cost: one
  number can name two different cards over the life of a store, and reaching that no longer
  needs a text editor. Risk: bounded and small. Nothing in the store or the tool refers to a card
  by number except the card object itself — there is no history, no per-card log and no
  statistics, the last of which the stakeholder declined by name at sign-off
  [src: EP-001/Q-005]. `recall list` is the only place a number is ever shown, and it reads the
  cards, so it cannot show a stale one [src: recall.py].
- **G — store a separate counter field (`ADR-0004`'s rejected option).** Cost: a store version 4,
  a new document field, and a read path that has to invent the counter for every existing
  version-3 document — which it would do by taking the largest number present, i.e. by doing F
  once. It also re-incurs the objection `ADR-0004` raised against it: a second source of truth
  that can disagree with the cards after any hand edit [src: ADR-0004]. That objection is
  stronger now than when it was written, because hand-editing is documented practice rather than
  a hypothetical [src: README.md].
- **H — never reduce the largest number, by leaving a tombstone behind for each deleted card.**
  Cost: deleted cards stay in the file. That contradicts what the item asks for — `AC1` and `AC3`
  are checked by reading the store and finding the card gone — and it would put rows in a file
  the user reads by hand that mean nothing to them [src: WI-0004 AC1; src: WI-0004 AC3].

## Decision

Option F, unchanged from `ADR-0004`. The premise moved; the answer did not.

- The next card number is one more than the largest `number` in `cards`, and 1 when there are
  none. `add_card` is not modified by this item [src: recall.py; src: ADR-0004].
- Deleting a card removes its object from `cards` and touches no other card, so every surviving
  card keeps the number it already had [src: WI-0004 AC3].
- **A number may therefore be reused.** Delete the highest-numbered card and the next card added
  takes that number. This is accepted behaviour, not a defect, and the README says so where the
  store is described.
- **The store's schema does not change and `STORE_VERSION` stays at 3.** Deleting removes a card
  object and adds no field, so nothing in `ADR-0004`'s or `ADR-0007`'s shape is different
  [src: ADR-0004; src: ADR-0007]. This settles the third question `refine` routed here
  [src: WI-0004].

## Consequences

What becomes easy: `delete` is a removal from a list followed by the existing write protocol.
There is no counter to keep in step, no migration to run, and no version of the store that this
tool reads differently than it did before this item.

What becomes hard: a user who remembers "card 4" across a delete-then-add sees a different card
under that number. The exposure is narrow — numbers come from `recall list` and from `recall
add`'s confirmation, both of which report the state at the moment they run — but it is real, and
it is the kind of thing that is only harmless if it is written down, so the README carries it.

Anyone who later adds something that refers to a card across time — a review history, a
statistics command, an export — must not use the card number as its identifier. That is the
constraint this ADR leaves behind.

**Reversibility: high.** Moving to option G later costs a store version bump and a read path
that derives the counter for older documents, which is precisely what it would have cost today.
Nothing this decision writes to disk has to be undone first, because it writes nothing new.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-29T13:34:39Z | plan | WI-0004 | First version: ADR-0004's option F re-weighed against the premise WI-0004 removes, and kept; numbers may be reused; the store schema and version are unchanged |
