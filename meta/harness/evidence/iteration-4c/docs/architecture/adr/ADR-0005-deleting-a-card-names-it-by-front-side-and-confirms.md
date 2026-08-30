---
title: A card is deleted by its front side, after the tool shows it and asks
version: 2
status: current
updated: 2026-08-30T13:27:00Z
updated-by: review-close
updated-for: WI-0003
---

# ADR-0005 — A card is deleted by its front side, after the tool shows it and asks

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** answer-questions (architect), for WI-0003, on the stakeholder's answers to
  `WI-0003/Q-001` and `WI-0003/Q-002`. The ambiguity rule in the last section is the architect's
  own decision, taken under the delegation `WI-0003/Q-001` recorded when it was filed.
- **Supersedes:** —

## Context

Deletion is in the product because the stakeholder asked for it: *"I want to be able to delete a
card; editing can wait."* [src: EP-001/Q-004] Intake had listed it as out of scope on its own
inference, and their answer contradicted that, so it became WI-0003 [src: WI-0003].

`refine` found two things the item could not settle and put both to them. How a card is named for
deletion was theirs because one of the options — a number the tool assigns — needs a way to *see*
the cards, which is work no item records, so the answer could widen the epic [src: WI-0003/Q-001].
What protects against deleting the wrong card was theirs because it settles an exclusion the item
carried as *ours* (no undo, no trash) and because it bears on the failure they named for the whole
product: *"losing my progress"* [src: EP-001/Q-004] [src: WI-0003/Q-002]. Deleting a card destroys
its rung and its due date under `ADR-0002`, not only its text [src: ADR-0002].

A third question was named at the same time and deliberately not asked: what happens when the
identifier matches nothing, or matches several cards. It was not answerable then, because whether
"several" is even possible depended on `WI-0001/Q-001` — may two cards share a front side?
[src: WI-0003] Both answers have since arrived, and they can now be answered by us, which is what
`WI-0003/Q-001` said would happen [src: WI-0003/Q-001].

## Options considered

**How a card is named** [src: WI-0003/Q-001]:

- **A — By its front side, typed out.** Cost: nothing new. Risk: the front must be typed exactly,
  and with duplicate fronts allowed it can match more than one card.
- **B — By a number the tool assigns.** Cost: a listing command, which is a work item nobody has
  filed. Risk: none to the deletion itself; the cost is the new scope.
- **C — Picked during a review session.** Cost: a change to WI-0002's session. Risk: it only
  reaches cards that are due, so a card they want rid of may be unreachable for a month.

**What protects against the wrong deletion** [src: WI-0003/Q-002]:

- **A — Nothing; deleting deletes.** Cost: none. Risk: a mistyped front costs that card's whole
  schedule with no way back — a small version of the failure they named.
- **B — Show the card and ask.** Cost: one prompt, every time. Risk: it is in the way on the times
  they meant it.
- **C — Recoverable: a trash a deleted card can be restored from.** Cost: its own commands and its
  own item. Risk: the file keeps things they told it to throw away.

The stakeholder was given all three of each, with **A** and **B** recommended and each
recommendation marked as ours, and chose exactly those:

> A — by typing the front side. I don't need a numbered list for this.

[src: WI-0003/Q-001]

> B — show me the card and ask first. One keystroke is worth it to not lose a month of progress by
> fat-fingering a delete.

[src: WI-0003/Q-002]

## Decision

**A card is named for deletion by its front side, typed exactly as it was entered.** No number, no
listing, no picking from a review session [src: WI-0003/Q-001]. Their *"I don't need a numbered
list for this"* is a decision against the listing, not a deferral of it, so no work item is filed
for one and none should be inferred from this ADR.

**The tool shows the card and asks before removing anything.** Before a card is removed it displays
what is about to be lost — both sides, the rung it has reached and the date it is next due under
`ADR-0002` — and removes it only on an affirmative reply. A negative reply changes nothing and is
an ordinary outcome, not an error [src: WI-0003/Q-002] [src: ADR-0002]. The schedule is shown and
not only the text because the schedule is the part they called their progress [src: EP-001/Q-004].

**Deletion is permanent. There is no undo, no trash and no archive.** This exclusion stood on
WI-0003 as the architect's inference with a note saying it had to be put to the stakeholder; it has
been, and they chose the confirmation over the trash. It is now their decision, and the item
records it as such [src: WI-0003/Q-002] [src: WI-0003].

**A front side matching no card deletes nothing.** The tool says which front it did not find,
exits non-zero, and leaves the stored file unchanged. This is the architect's decision under the
standing delegation [src: EP-001/Q-004]; `refine` recorded it in advance as ours to take once the
answers landed, in exactly these terms [src: WI-0003].

**A front side matching several cards lists them and asks which one.** This is the architect's
decision, and it is the one place where two of the stakeholder's answers meet. `WI-0001/Q-001`
allows two cards to share a front — *"add it and warn me"* — so a front-side delete can match more
than one card [src: WI-0001/Q-001]. The tool shows every match with both sides, its rung and its
due date, and asks which to remove; exactly the chosen one is removed and every other match is left
untouched. Declining removes nothing.

The reason this and not the alternatives: refusing on ambiguity would make the duplicated cards
**undeletable**, because there is no listing and no number to fall back on, and that would take
away a capability the stakeholder asked for on a case their own other answer creates. Deleting all
the matches is the opposite of what they asked for in `WI-0003/Q-002`. Extending the prompt from
"this one, yes or no" to "which of these" costs nothing they have not already accepted: they agreed
to be asked every time [src: WI-0003/Q-002].

## Consequences

Easy: nothing new has to exist. Deletion needs only the stored file WI-0001 writes and the front
sides already in it, and the prompt is the same mechanism whether there is one match or several
[src: WI-0001].

Hard: every deletion costs a prompt, including the ones the person meant, and they accepted that
explicitly. Deleting several cards in a row is several prompts. Nothing here provides a way to skip
the prompt, and adding one later — a force flag — would be a change to their decision and needs
their authorisation, not ours.

Also: WI-0003 cannot be built before WI-0001, because it reads and rewrites the same file. The
item declares `depends-on: WI-0001`, so Definition of Ready R7 is satisfied in substance and the
orchestrator will not make WI-0003 runnable until WI-0001 is `done` [src: WI-0003]. See
`## Corrections`: this clause said the opposite when the ADR was written, and the second `refine`
execution on the item made it false.

Reversibility: **cheap for the prompt, cheap for the ambiguity rule, expensive for neither.** Both
are behaviour at the terminal and neither changes what is stored, so changing them later migrates
nothing — unlike `ADR-0004`'s file format [src: ADR-0004]. The prompt is nevertheless the
stakeholder's decision and not ours, so removing it needs them; the ambiguity rule is ours and a
later ADR can replace it.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-30T13:27:00Z | review-close | WI-0003 | One `erratum` correction, recorded below: `## Consequences` said the item declared no `depends-on`, and by the time the item was built it declared one. Nothing about the decision changes — no clause of `## Decision` is touched and no code would have to change to satisfy the new sentence. |
| 1 | 2026-08-30T11:43:03Z | answer-questions | WI-0003 | First version: records the stakeholder's answers to `WI-0003/Q-001` and `WI-0003/Q-002` — delete by front side, with the card shown and confirmed first, and no undo — and the two cases they delegated: a front matching nothing, and a front matching several cards. |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-08-30T13:27:00Z | review-close | WI-0003 | erratum | `## Consequences`, third paragraph, said: *"The item declares no `depends-on` and passes Definition of Ready R7 in form; the sequencing is recorded on the item and in its Q&A for `plan` to meet deliberately"*. That was true when this ADR was written, and the second `refine` execution on WI-0003 falsified it — the item's front matter now declares `depends-on: WI-0001` [src: WI-0003], and its history records the move that added it [src: tracker/items/WI-0003/history.md]. Replaced with a clause stating the declared dependency and what it buys, which is R7 in substance rather than in form. The decision itself — delete by front side, shown and confirmed, permanent, with the no-match and several-match rules — is untouched, and no code would have to change to satisfy the new text. |
