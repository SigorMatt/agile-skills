---
title: Store a card's rung as the interval in days, at store version 3
version: 1
status: current
updated: 2026-08-29T12:33:35Z
updated-by: plan
updated-for: WI-0003
---

# ADR-0007 — Store a card's rung as the interval in days, at store version 3

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** plan (architect), for WI-0003
- **Supersedes:** —

## Context

WI-0003 replaces the placeholder next-due date `review` writes today with the ladder
[src: ADR-0006; src: WI-0003 AC2]. To do that a card has to carry which rung it is on, and four
things about that field are already fixed elsewhere:

- The ladder is 1, 3, 7, 30 days; a right answer moves a card up one rung, a wrong answer returns
  it to the bottom, and a card that has never been answered sits **below** the bottom rung, so its
  first right answer schedules it one day out [src: ADR-0001; src: WI-0003/Q-001].
- `README.md` must name the field and the values it may hold, and a reader with a card's stored
  fields and `README.md` must be able to state the card's next due date without reading code
  [src: WI-0003 AC4].
- A value the tool cannot read stops it — a message on stderr, exit 1, the file untouched — rather
  than being ignored [src: WI-0003 AC9].
- A store written before this item is read and upgraded in place, and its cards read as never
  answered [src: WI-0003 AC8].

What is not fixed, and what this ADR decides, is the field's **representation**, the store
**version** that carries it, and where the ladder itself lives. Refinement routed all three here
rather than to the stakeholder [src: WI-0003].

The store is a file a person opens and reads; that is its purpose rather than a side effect
[src: WI-0001 AC5; src: ADR-0002]. WI-0003 sharpens that: hand-editing the store is now the
documented and only way to move a card, and the way every one of its criteria is checked
[src: WI-0003].

## Options considered

On the representation:

- **A — the interval in days: `interval`, one of `1`, `3`, `7`, `30`, and `null` for a card that
  has never been answered.** The two scheduling fields are then mutually checkable by eye: `due`
  is the review date plus `interval`, so a reader can confirm a card's schedule from the card
  alone [src: WI-0003 AC4]. A person hand-editing sets `7` to mean a week, with no lookup. Cost:
  changing an existing rung's *value* strands every card holding the old one, because `load`
  refuses an interval the ladder does not contain [src: WI-0003 AC9] — so that change needs a
  migration. Risk: low, and the cost is narrow (adding a rung costs nothing; only changing or
  removing one bites).
- **B — a rung index: `rung`, `0`–`3`, `null` for never answered.** Cost: `rung: 2` means nothing
  without `README.md` open beside it, and it cannot be checked against `due` by eye — which is
  most of what AC4 asks a reader to be able to do [src: WI-0003 AC4]. Benefit: changing a rung's
  value needs no migration, because an index survives it. Risk: low.
- **C — a name: `"week"`, `"month"`.** Cost: it invents a vocabulary that then has to be kept in
  step with the numbers, and "month" is not 30 days. Risk: medium, for no gain over A.

On the version:

- **D — bump `version` to 3, and read 1, 2 and 3.** Cost: one more value in
  `READABLE_VERSIONS` and one test to update. Risk: low.
- **E — leave `version` at 2 and add the field silently.** Cost: two documents both claiming
  version 2 with different card shapes, which is the failure the field exists to prevent
  [src: ADR-0004; src: ADR-0006]. Risk: high.

On where the ladder lives:

- **F — one module-level constant in `recall.py`.** Cost: none worth naming; the module is the
  whole program [src: docs/architecture/overview.md]. Risk: low.
- **G — a table in the store, so a user could retune it.** Cost: it delivers per-user tuning,
  which WI-0003 excludes explicitly [src: WI-0003]. Risk: high — it is scope nobody asked for.

## Decision

Options A, D and F.

**The field is `interval`: the number of days the current wait is.** Its values are exactly the
four the ladder names — `1`, `3`, `7`, `30` — and `null` for a card that has never been answered,
which is the same idiom `result` already uses for the same idea [src: ADR-0006]. A card object at
version 3 is:

```json
{ "number": 1, "question": "die Katze", "answer": "the cat",
  "due": "2026-09-01", "result": "right", "interval": 3 }
```

**The moves, as arithmetic on that field.** A right answer takes the next value in the ladder
after the current one, and `null` takes the first; a card already at `30` stays at `30`. A wrong
answer takes the first value, whatever the card held [src: ADR-0001]. The new `due` is then the
**day of the review** plus the new `interval`, never the card's old `due` plus anything — so a
card reviewed ten days late gets its full interval from the day it was actually reviewed
[src: WI-0003 AC2].

**Store version 3.** `save` stamps `3`; `load` accepts `1`, `2` and `3` and refuses anything else
with the message and exit code any unusable store gets [src: ADR-0004]. A card read from an older
document has no `interval`, which is read as `null` — never answered — and the next write carries
the field on every card [src: WI-0003 AC8]. That is the same in-place upgrade version 2 used, and
there is still no migration to run [src: ADR-0006].

**`load` now validates both scheduling fields, and this is a deliberate tightening.** A `due` must
be exactly `YYYY-MM-DD`, and an `interval` must be one of the ladder's values or `null`; anything
else makes the document unreadable, reported and left alone [src: WI-0003 AC9]. Until now `load`
checked only that `due` was a string [src: recall.py], which let `"tomorrow"` through — where it
sorted above every real date and removed the card from every review for ever, while `recall list`
went on showing it. That was reproduced during WI-0002's verification and handed to this item
[src: WI-0002; src: WI-0003]. It is fixed here rather than filed as a bug because WI-0003 is what
makes hand-editing these two fields the documented way to move a card, and so makes the typo far
likelier than it was.

**The ladder is one constant in `recall.py`,** `LADDER = (1, 3, 7, 30)`, and the module holds the
whole program [src: docs/architecture/overview.md]. It is not in the store and not configurable:
per-card and per-user tuning are excluded by the item [src: WI-0003].

## Consequences

What becomes easy: a person reading a card can check its schedule against itself — `due` is the
last review plus `interval` — which is what AC4 asks of `README.md` and its reader
[src: WI-0003 AC4]. Setting a card's rung by hand is typing the number of days you want, with no
table to consult. The never-answered state costs no new value, because `null` already means
"never reviewed" on the neighbouring field [src: ADR-0006].

What becomes hard: **changing a rung's value is now a migration.** A card holding `14` after the
ladder dropped 14 is a store `load` refuses [src: WI-0003 AC9], so retuning the ladder means
rewriting stored cards — where an index would have survived it. Adding a rung is still free, and
removing or changing one is the case that bites. `ADR-0001`'s reversibility note has been amended
to say so rather than left to be discovered [src: ADR-0001]. And validation that used to be
absent is now load-bearing: a store a previous `recall` happily read can become one this `recall`
refuses, which is the intended behaviour and is still a change a user could meet.

**Reversibility: medium on the representation, high on the version and the ladder's home.**
Swapping `interval` for a rung index touches `load`, `record_result`, `README.md`, the tests that
name the field, and every card already stored [src: recall.py; src: WI-0003 AC8] — the last of
those is what makes it medium rather than cheap. Bumping the version again is one constant and one tuple. Moving the ladder constant is
a rename.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-29T12:33:35Z | plan | WI-0003 | First version: the `interval` field in days with `null` for never answered, store version 3 and the read rule for 1 and 2, the strict validation of `due` and `interval` that AC9 requires, and the ladder as one constant in `recall.py` |
