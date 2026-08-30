---
title: The card file is human-readable text that the tool owns and rewrites
version: 1
status: current
updated: 2026-08-30T11:38:16Z
updated-by: answer-questions
updated-for: WI-0001
---

# ADR-0004 — The card file is human-readable text that the tool owns and rewrites

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** answer-questions (architect), for WI-0001, on the stakeholder's answer to
  `WI-0001/Q-002`
- **Supersedes:** —

## Context

The stakeholder said where their cards must live and nothing about what is in the file:
*"It needs to live in a file on my machine that survives a reboot."* [src: EP-001/Q-004] They
delegated the rest of how the tool is built: *"As for how it's actually built — whatever you
think is best."* [src: EP-001/Q-004]

Intake nevertheless wrote WI-0001's AC5 to promise more than that sentence — that both sides of
every card and its scheduling state can be read out of the file with an ordinary text tool while
the tool is not running — and flagged at the time that this was intake's addition and had to be
put to the stakeholder rather than left standing as if they had asked for it [src: WI-0001].

`refine` did not settle it under the standing delegation, and was right not to. This is the one
decision on the item that is expensive to undo: the person's cards and their study history
accumulate in whatever the first version writes, so a later change of shape means migrating real
history or losing it — and *"losing my progress"* is one of the two things they named as making
the product a failure [src: EP-001/Q-004]. That is the irreversible-commitment condition in
`spec/question.md` §4, so it was escalated as `WI-0001/Q-002`.

## Options considered

- **A — Readable, and hand-editing is supported.** Plain text the person may edit directly.
  Cost: the tool must cope with whatever a half-finished hand edit leaves behind — missing
  fields, malformed rows, duplicate state — which is real work no item records. Risk: a promise
  to accept arbitrary human edits is far harder to keep than it looks, and breaking it later is
  worse than never making it.
- **B — Readable, but the file is the tool's to write.** Plain text the person can open and read
  at any time; hand-editing is not supported, and the tool may rewrite or reformat the file
  whenever it saves. Cost: choosing a readable format, and being bound to keep it readable.
  Risk: someone edits it anyway and gets a result nobody promised.
- **C — The format is ours.** A file at a documented path that survives a reboot, and nothing
  more is promised about its contents. Cost: none. Risk: checking that a card survived means
  asking the tool, because there is no other way to look — so the person has only the tool's word
  for the one promise they care most about.

The stakeholder was given all three, with **B** recommended and the recommendation marked as
ours, and chose **B**:

> B. I want to be able to open it and see my cards are still there, but I'm not asking to
> hand-edit it — that's a different thing.

[src: WI-0001/Q-002]

## Decision

**The card file is human-readable text.** Both sides of every card, and every part of its
scheduling state — the rung it has reached and the date it is next due under `ADR-0002` — can be
read out of the file with an ordinary text tool, with the tool not running, by a person who has
read the documentation and nothing else [src: WI-0001/Q-002] [src: ADR-0002]. No part of a card
or its schedule may be stored in a form that has to be decoded to be seen: not compressed, not
binary, not an opaque encoding of a field. This is the promise the stakeholder asked for and it
binds every later version, not only the first.

**The file is the tool's to write.** Hand-editing is not supported: the tool may rewrite,
reorder or reformat the file whenever it saves, and it makes no promise about the result of
editing it externally. The person's guarantee is that they can always *look*, which is what they
asked for [src: WI-0001/Q-002].

**The exact format is still `plan`'s to choose**, within that constraint. Any format a person
can read and understand from the documentation satisfies this ADR; which one it is has no product
stake and remains under the stakeholder's standing delegation [src: EP-001/Q-004].

**Accepting hand-edited files is out of scope and is not deferred work waiting to be scheduled.**
The stakeholder declined it in the same sentence — *"I'm not asking to hand-edit it — that's a
different thing"* — so no item is filed for it. If they ask later it is a new work item with its
own criteria, not an amendment to WI-0001 [src: WI-0001/Q-002].

## Consequences

Easy: the person can verify the promise everything else rests on — that their progress is still
there — with `cat`, rather than by taking the tool's word for it [src: EP-001/Q-004]. WI-0001's
AC5 and WI-0002's criterion that a reader can check the due set against the stored file by hand
both become decidable by a person with a terminal and no context, which is what the Definition of
Ready asks of a criterion [src: WI-0001] [src: WI-0002]. `ADR-0002` already assumed this — it
records that a card's scheduling state is a rung and a date "both readable by eye in the stored
file" — so this ADR makes an assumption that was already load-bearing into a stated commitment
[src: ADR-0002].

Hard: the commitment binds every future version. Any later change that would make part of a card
or its schedule unreadable — compression, a binary index, an encoded field — needs a superseding
ADR and the stakeholder's authorisation, because this decision is theirs and not ours.

Also: a readable format is somewhat larger and somewhat slower than a packed one. At one person's
vocabulary deck that difference is not observable, and no criterion on any item bounds file size
or startup time.

Reversibility: **expensive, deliberately.** This is the decision the escalation existed for. The
person's real study history accumulates in this file, so changing its shape later means either
migrating that history or losing it, and losing it is a named failure of the product
[src: EP-001/Q-004]. Choosing a readable format costs nothing now and keeps the expensive move
from ever being necessary.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T11:38:16Z | answer-questions | WI-0001 | First version: records the stakeholder's answer to `WI-0001/Q-002` — the card file is readable text, the tool owns it, hand-editing is not supported — and confirms WI-0001's AC5, which intake had written ahead of their decision. |
