---
title: A correction edits the entry in place, and a removal deletes it
version: 3
status: current
updated: 2026-09-11T18:55:51Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0011 — A correction edits the entry in place, and a removal deletes it

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** plan (architect), for WI-0005
- **Supersedes:** —

## Context

`WI-0005` adds `envel fix <ref>` and `envel remove <ref>`. What it changes is not the command
line — that is settled [src: WI-0005 AC1 "a plain word after the subcommand, as `envel spend`"] —
but the one sentence the whole data model rests on: *"`entries` is append-only within a run and
ordered as written"* [src: ADR-0002].

The stakeholder decided what a correction means, and they decided it against a history:

> *"I mistype things in the spreadsheet most weeks, so being able to correct a spend I already
> recorded matters to me more than keeping a perfect history of my own typos — if I fix an entry,
> a past summary should just show the corrected figure."* [src: EP-001/Q-005]

Two criteria make that testable and between them they rule out most of the design space. A
corrected entry must look as though the corrected values had been recorded when it was first made
[src: WI-0005 AC7 "After a correction, the listing shows the envelopes the entry touched as though the"],
and a spend whose date moved must appear in **exactly one** month's summary, the month of its new
date [src: WI-0005 AC8 "shows the corrected figure, and the corrected spend appears in exactly one month's summary"].
A removal goes further: after one, *no* line of any month may carry that reference
[src: WI-0005 AC20 "The listing the reference is read off shows the change"].

What is already settled and must survive: a balance is the plain sum of `cents` over the entries
naming an envelope, with no branch on `kind` [src: ADR-0002]; a reference is stored rather than
derived, is written once and never changed, and comes only from the document's counter
[src: ADR-0010]; and the two halves of a move are two entries, which is why a correction aimed at
one is refused rather than made to work [src: ADR-0007],
[src: WI-0005 AC13 "are each refused with a message saying a move cannot be corrected or removed"].

No format change is forced by any of this: nothing here adds, removes or renames a key, so a
document written before this item and one written after it are both `format: 2` [src: envel/store.py:11].

## Options considered

- **A — append a compensating entry.** A correction appends the difference; a removal appends the
  negation. Cost: the `entries` list stays strictly append-only and the log gains a history for
  free. Risk: it delivers the opposite of what the stakeholder asked for. A past summary would
  show both figures rather than the corrected one, which `EP-001/Q-005` refuses in terms, and a
  spend whose date moved would appear in two months rather than one, falsifying
  [src: WI-0005 AC8 "shows the corrected figure, and the corrected spend appears in exactly one month's summary"].
  A removed entry's line would also still be in the listing, with a second line beside it, against
  [src: WI-0005 AC20 "The listing the reference is read off shows the change"].
- **B — supersede the entry: mark the old one dead and append the new values.** A `superseded`
  or `removed` flag on the entry, with every reader skipping flagged entries. Cost: the list stays
  append-only and nothing is ever lost. Risk: `balance` acquires a branch on a field, which is
  exactly the sentence `ADR-0002` protects — *a balance is the sum of `cents` over the entries
  naming it* — and the branch has to be repeated in `figures`, `bounded_balance` and
  `entries_in`, four readers that today share one rule [src: envel/summary.py]. A reader that
  forgot the branch would show the stakeholder money they do not have, silently. It also stores a
  history the stakeholder said they do not want, in a file they were promised they could open in a
  text editor and understand [src: ADR-0002].
- **C — edit the entry in place; a removal deletes it from the list.** Cost: `entries` stops being
  append-only, which is a sentence in `ADR-0002` and in `docs/architecture/overview.md` that has to
  change rather than be worked around; and the old values are gone, so nothing can show what an
  entry used to say. Risk: a bug in the correction path damages data with no copy to recover it —
  mitigated only by the store being written atomically and whole [src: ADR-0002], so a failed run
  leaves the previous file intact. Gains: every reader keeps one rule, no reader changes at all,
  and `ref` stays with its entry because the entry is the same object.

## Decision

Option **C**.

1. A correction **mutates the entry** identified by `ref`, in the `entries` list, leaving its
   position in the list and its `ref` untouched. A removal **deletes that entry** from the list.
   Nothing is appended by either.
2. The fields a correction may set are the ones the criteria name and no others: `cents`, `on`,
   `description` and `envelope` on a spend
   [src: WI-0005 AC6 "The four options of AC2–AC5 may be given in any combination in one invocation, and"],
   and `cents` and `envelope` alone on an income
   [src: WI-0005 AC16 "changes its amount with"]. `kind`, `at` and `ref` are never written by
   either operation.
3. **`next-ref` is never decreased, and a removal does not touch it.** It stays the only source of
   a new reference [src: ADR-0010], which is what makes *"a number is not handed to a later
   entry"* true after a removal rather than merely likely
   [src: WI-0005 AC1 "The number an entry is given stays that entry's"].
4. `format` stays `2`. No key is added, removed or renamed, so nothing in `envel/store.py` changes
   and no document needs upgrading [src: envel/store.py:11].
5. **The invariant is checked against the candidate document, not the live one.** Both operations
   build the changed document first and then read the balance of every envelope the change touched
   — at most two, the entry's envelope before and after — and refuse if either is negative
   [src: WI-0005 AC9 "A correction that would take an envelope below zero is refused: nothing is changed,"],
   [src: WI-0005 AC18 "Removing an income, correcting one downwards, or moving one to another envelope"].
   A refusal returns the caller's document untouched and `envel/cli.py` writes nothing, which is
   how *"nothing is changed"* is delivered rather than promised
   [src: envel/cli.py:217].
6. **Neither operation reads or writes an entry's history, because there is none.** Anything that
   wants to know what an entry used to say is a different item and a different decision.

## Consequences

**Easy.** Every reader in the tool is unchanged — `balance`, `figures`, `bounded_balance`,
`entries_in` and `entry_line` all keep the single rule they share, with no branch on a flag and no
filtering of dead entries [src: envel/summary.py], [src: envel/envelopes.py]. That is what makes
four of this item's criteria fall out of the design rather than needing code: the listing after a
correction [src: WI-0005 AC20 "The listing the reference is read off shows the change"], a past
month's summary [src: WI-0005 AC8 "shows the corrected figure, and the corrected spend appears in exactly one month's summary"],
the balance afterwards [src: WI-0005 AC7 "After a correction, the listing shows the envelopes the entry touched as though the"],
and persistence across invocations
[src: WI-0005 AC14 "A correction or a removal made in one invocation is still reflected in the listing"].
The reference survives because the entry object does, which is the property `ADR-0010` was written
to provide.

**Hard.** The log is no longer append-only, so `ADR-0002`'s sentence and the matching one in
`docs/architecture/overview.md` stop being true and are repaired by this item rather than left
[src: ADR-0002]. And a correction is destructive: there is no copy of what an entry said before.
The mitigation is the one already in the file's design — the store is written whole and atomically
[src: ADR-0002] — so a failure leaves the previous file, but a *successful* wrong correction is not
recoverable inside the tool. The stakeholder chose that trade explicitly [src: EP-001/Q-005] and
this ADR does not soften it.

**Reversibility: moderate, and it does not decay.** No stored shape changes
[src: envel/store.py:11], so reversing to A or B needs no third `format` and no migration of
anybody's file — unlike `ADR-0010` [src: ADR-0010], whose irreversibility came from numbers the
person had written down outside the tool. What reversal
costs is the operations themselves and their tests: two functions in `envel/envelopes.py`, their
two dispatch branches in `envel/cli.py`, and one test module. What could not be reversed is the
data already lost — an entry corrected under this decision cannot be restored by adopting B later,
because the old values were never written anywhere. So the decision is cheap to change and its
effects are not, which is the honest shape of it.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-09-11T18:55:51Z | answer-questions | EP-001 | One `erratum` correction, recorded below, correcting an earlier **correction row** rather than this ADR's prose — the route `ADR-0013` [src: ADR-0013] decides. The `2026-09-11T10:40:54Z` row states what `envel/cli.py:165` contains, and it contains something else. The earlier row is untouched and its substantive point stands. Answering `EP-001/Q-008`. |
| 2 | 2026-09-11T10:40:54Z | answer-questions | WI-0005 | One provenance correction, recorded below: `## Decision` 5's citation for *"`envel/cli.py` writes nothing"* moved from `envel/cli.py:165` to `envel/cli.py:217`, because `WI-0005`'s own change to `envel/cli.py` pushed `if result.changed:` down by 52 lines. The assertion is unchanged and no code has to change to satisfy the new text. Answering `WI-0005/Q-009`. |
| 1 | 2026-09-11T09:28:46Z | plan | WI-0005 | First version: a correction mutates the entry in place and a removal deletes it, `next-ref` is never decreased, `format` stays 2, and the below-zero invariant is checked against the candidate document. |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-09-11T18:55:51Z | answer-questions | EP-001 | erratum | The row stamped `2026-09-11T10:40:54Z` in this section says the old citation `[src: envel/cli.py:165]` *"was that statement when this ADR was written and is now `elif arguments.command == \"spend\":`"*. The second half is false: `elif arguments.command == "spend":` is at `envel/cli.py:163` [src: envel/cli.py:163], and `envel/cli.py:165` is `document,` [src: envel/cli.py:165], an argument to `envelopes.record_spend`. Nor did it drift — `envel/cli.py`'s last change is `WI-0005`'s own [src: commit a88691f], before that row was written, so the line number was wrong when it was typed. What the row was **for** is unaffected and still correct: the statement it tracks is `if result.changed:` at `envel/cli.py:217` [src: envel/cli.py:217], and `## Decision` 5's citation reads that. The earlier row is left exactly as it stands, per `ADR-0013` [src: ADR-0013]. Found by `EP-001`'s claims audit at the ending; answering `EP-001/Q-008`. |
| 2026-09-11T10:40:54Z | answer-questions | WI-0005 | provenance | `## Decision` 5: *"A refusal returns the caller's document untouched and `envel/cli.py` writes nothing, which is how `nothing is changed` is delivered rather than promised"* cited `[src: envel/cli.py:165]`, which was that statement when this ADR was written and is now `elif arguments.command == "spend":`. `WI-0005` added two subparsers and the *no option given* check above it, moving `if result.changed:` to line 217 [src: envel/cli.py:217]. The citation now reads `[src: envel/cli.py:217]`; the assertion is unchanged, and `verify` measured the store file after every refusal on this item without one of them writing. Answering `WI-0005/Q-009`. |
