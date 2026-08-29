---
title: A false statement inside a standing decision is corrected in place, not superseded
version: 1
status: current
updated: 2026-08-28T22:39:29Z
updated-by: plan
updated-for: BUG-0001
---

# ADR-0009 — A false statement inside a standing decision is corrected in place, not superseded

- **Status:** accepted
- **Date:** 2026-08-28
- **Decided by:** plan (architect), for [src: BUG-0001]
- **Supersedes:** —

## Context

[src: BUG-0001] requires that `## Decision` item 4 of [src: ADR-0007] stop asserting something
false. The sentence is *"A column's width does not depend on its marker"*, and one command
falsifies it: a column narrow enough for `_column_widths`' floor to bind comes out wider with
`:-:` than with `---` from identical content. The criterion it cites — [src: WI-0002 AC6] — says
*alignment*, which is a different thing and is true.

What makes this a decision rather than an edit is `spec/doc-header.md` §4:

> An ADR is **never edited to change its decision**. It is superseded by a new ADR that cites it.

Read strictly, that forbids touching `## Decision` at all, and the only route to a true ADR-0007
would be superseding it. But ADR-0007's decision is **not wrong**. Option A — alignment is placed
inside the cell's field, the guard spaces stay outside it, `_column_widths` is untouched — is
correct, is implemented, and is what `mdtab/table.py` does today. What is wrong is one clause of
the *justification* attached to item 4. There is no rule for that case, and this project now needs
one, because the same shape recurs: [src: BUG-0001] found the identical sentence in
`docs/architecture/overview.md` and in a test docstring in `tests/test_units.py`, each having
re-quoted the previous rather than re-read the code.

Three properties are in tension, and no option keeps all three:

1. an ADR's `## Decision` is not rewritten after the fact, so a reader can trust that what it
   says is what was decided;
2. no document in `docs/` states something false — which is not an aspiration here but a
   Definition of Done criterion, D12 for an item and DE6 for an engagement
   [src: .claude/agile-skills/spec/dor-dod.md], and the one [src: BUG-0001] failed;
3. an ADR marked `superseded` means "this is no longer how the system works", and readers,
   citations and `lint-claims` all rely on that meaning.

## Options considered

- **A — Correct the false clause inside ADR-0007, keep `status: accepted`, and record the
  correction in its change log with the old sentence quoted in full.** Cost: `## Decision` is
  edited after the fact, which property 1 exists to prevent; the mitigation is that the change-log
  row quotes what the sentence used to say, so nothing is destroyed and the edit is visible to
  anyone reading the document from the bottom. Risk: taken as licence, this becomes "ADRs may be
  rewritten when they turn out to be wrong", which would gut property 1 — so the conditions below
  are part of the decision, not commentary on it.
- **B — Supersede ADR-0007 with a new ADR restating the same decision, corrected.** Cost: high,
  and paid by every future reader. ADR-0007 is cited from `docs/architecture/overview.md` and from
  [src: WI-0002] in several places; all of those citations would then point at a document marked
  `superseded` whose decision is still in force. Risk: it makes `superseded` mean two different
  things — "replaced by a different decision" and "replaced by the same decision, spelled
  correctly" — and a reader who sees the marker will reasonably assume the first and go looking
  for a change to the system that never happened. It also writes a second full ADR for a
  correction of one clause, which is the padding `spec/doc-header.md` §4 warns against.
- **C — Leave ADR-0007 alone; correct only `docs/architecture/overview.md` and note there that
  the ADR is wrong.** Cost: the overview's corrected sentence would cite a document that
  contradicts it, which is worse than the state [src: BUG-0001] describes: today the two agree
  and are both wrong, and after C they would disagree. Risk: property 2 stays broken in the
  document that is meant to be authoritative, and the next reader to consult ADR-0007 directly —
  which is what `docs/architecture/overview.md` tells them to do — gets the false sentence with
  nothing beside it.

## Decision

**A**, under four conditions that are what distinguish a correction from a rewrite. An ADR's
`## Decision` may be edited in place only when **all four** hold:

1. **The decision itself is unchanged.** The option chosen, and what the code must do to conform,
   are identical before and after. If a reader would have to change any code to satisfy the new
   text, it is a new decision and option B applies.
2. **The edited text was false against the code**, demonstrably — by a command, or by a named
   function a reader can open. "Clearer wording" does not qualify; neither does a claim that is
   merely unsupported rather than wrong.
3. **The change log quotes the removed text verbatim** and names the item that forced the
   correction. The old sentence stays readable in the document forever; only its position moves,
   from the part a reader trusts to the part that records history.
4. **`status` stays `accepted`,** because the decision is still in force, and `version` is bumped.

Applied here: ADR-0007 item 4 keeps *"`_column_widths` is not touched"*, which is true and is the
substance of item 4; the clause *"A column's width does not depend on its marker [src: WI-0002
AC6]"* is replaced by one that says what [src: WI-0002 AC6] actually says, and points at
`docs/architecture/overview.md`'s *"How wide a column is"* bullet for what a column's width *does*
depend on. ADR-0007 goes to version 2, `status: accepted`, with the removed sentence quoted in its
change-log row.

## Consequences

**Easy.** Correcting a false statement no longer costs a superseded ADR, so there is no incentive
to leave one standing. `superseded` keeps its single meaning. Every existing `[src: ADR-0007]`
citation stays valid and keeps pointing at a document that is both current and true.

**Hard.** `## Decision` is no longer strictly append-only, so a reader who wants to know what an
ADR said originally must read its change log rather than trusting the body. Condition 3 is what
makes that possible and it is the condition most likely to be skipped under time pressure — a
correction whose change-log row says "fixed a wrong sentence" without quoting it destroys exactly
the evidence this decision promises to keep.

**Reversibility.** Cheap, and worth stating because it is not obvious. Reversing this decision
means adopting option B as the rule instead: nothing already corrected has to be undone, because a
document corrected under A can afterwards be superseded under B if the project decides that is
better. Nothing is deleted by A, so nothing is lost by changing the rule later. What could not be
undone cheaply is the opposite order — superseding first and then wanting the ADR back as current
— which is a further reason to prefer A now.

**What this does not license.** It is not a general permission to edit ADRs. Condition 1 is the
line: the moment a correction would change what the code has to do, it is a new decision, and
`spec/doc-header.md` §4's rule applies with full force.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-28T22:39:29Z | plan | BUG-0001 | First version |
