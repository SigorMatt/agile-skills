---
title: A cell containing a line break is exempt from its column's alignment marker
version: 5
status: current
updated: 2026-08-30T00:57:01Z
updated-by: review-close
updated-for: EP-001
---

# ADR-0007 — A cell containing a line break is exempt from its column's alignment marker

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** the stakeholder, recorded by answer-questions (architect), for EP-001
- **Supersedes:** ADR-0005

## Context

ADR-0005 recorded, in the stakeholder's own words, that a column's alignment marker places the
text of every content cell in that column: *"the alignment marker decides everything. Whatever the
marker says, that is where the text sits in the cell — every row, every column, no exceptions"*
[src: WI-0002/Q-001]. Its decision 3 stated that as *"No content cell is exempt"* [src: ADR-0005],
and `docs/product/vision.md` v5 carries the same sentence with the same citation.

At the engagement's sign-off the same person made that no longer true:

> A cell with a line break or a `<br>` in it should just sit top-left, plain, whatever the column
> marker says; markers are for normal cells, not for those. … Fix the multiline cells and we are
> done.

[src: EP-001/Q-004]

Two sentences of theirs, one exempting a class of cell that the other says has no exemptions. The
cross-answer check on `EP-001/Q-004` declared the conflict and refused to settle it, because
settling it would have meant editing a recorded decision that carries their name
(`spec/question.md` §4, third condition) [src: WI-0002/Q-001; src: EP-001/Q-004]. `EP-001/Q-005`
put both sentences side by side, by ID, and asked which wins. Their reply is the authorisation
this ADR rests on:

> You're right, and I over-spoke the first time — the later one wins: a cell with a line break or a
> `<br>` in it sits top-left whatever the column marker says, and markers govern everything else.
> That is your option B, and yes, treat this as me superseding what I said before.

[src: EP-001/Q-005]

So ADR-0005 is superseded rather than corrected: what changes is what the code must do, which
`spec/doc-header.md` §4b puts on the far side of the line between a repair and a new decision. Every
other decision ADR-0005 took is carried forward here unchanged, so that one document remains the
current answer to "where does a cell's text sit"
[src: ADR-0005; src: .claude/agile-skills/spec/doc-header.md].

**What this ADR deliberately does not decide.** The stakeholder authorised the exemption, not its
edges. Five things are still undecided and none of them is guessable: what counts as "a line
break" in a cell that is physically one line (`<br>`, `<br/>`, `<br />`, casing and spacing, the
trailing-backslash convention); whether an exempt cell is still padded out to its column's width;
whether the exemption is per cell or infects its whole column; whether the delimiter row's marker
is still preserved colon-for-colon in such a column; and what "top" means in a single-line cell.
`WI-0003` records all five as questions for `refine` to put to them [src: WI-0003].

## Options considered

- **A — The earlier sentence wins; nothing is exempt.** ADR-0005 decision 3 stands as written, the
  tool keeps placing every content cell by its column's marker, and `WI-0003` is dropped. Cost: the
  stakeholder's sign-off condition is refused, and the engagement cannot end as delivered on their
  terms. Risk: it decides against them on the strength of a sentence they have since withdrawn.
- **B — The later sentence wins; a cell containing a line break is exempt.** ADR-0005 decision 3 is
  superseded by this ADR; `WI-0003` is refined, built and verified; the engagement returns for a
  fresh sign-off when it next reaches rest. Cost: one decision of theirs is narrowed, and every
  document that quoted it has to say so. Risk: low — the narrowing is theirs, in writing, with
  *"treat this as me superseding what I said before"* on it [src: EP-001/Q-005].
- **C — Reconcile the two privately, by reading "no exceptions" as having always meant "no
  exceptions among ordinary cells".** Cost: none visible, which is what makes it the dangerous one.
  Risk: high, and it is the failure this project has already recorded twice — a document rewritten
  to remove a contradiction between two of the stakeholder's statements, with the person who could
  have reconciled it in one line was never asked (F-062, and the methodology's own ADR-0008 on
  cross-answer consistency). Refused on principle, not on cost.
- **Chosen: B**, by the stakeholder, in the words quoted above. The question that put A and B to
  them offered no recommendation, deliberately: both sentences were theirs and neither was ours to
  prefer [src: EP-001/Q-005].

## Decision

1. **A column's alignment marker decides where its cell text sits within the column's width.**
   A left marker (`:---`) puts the padding to the right of the text; a right marker (`---:`) puts
   it to the left; a centre marker (`:---:`) splits it between the two sides. Carried forward from
   ADR-0005 decision 1, unchanged [src: ADR-0005].
2. **When a centred column's leftover padding is odd, the extra display column goes to the right of
   the text** — half the leftover, rounded down, on the left. Carried forward from ADR-0005
   decision 2, unchanged, and endorsed again by the stakeholder after seeing what it does
   [src: WI-0002/Q-001; src: EP-001/Q-004].
3. **A cell whose content contains a line break is exempt from its column's marker, and its text
   sits at the left of the column.** This supersedes ADR-0005 decision 3 [src: EP-001/Q-005]. What
   counts as a line break, and whether such a cell is still padded out to the column's width, are
   not decided here — they are `WI-0003`'s questions for the stakeholder [src: WI-0003;
   src: ADR-0008].
4. **Every other content cell of a marked column is placed by decision 1** — the header row and
   every body row alike. This is the half of ADR-0005 decision 3 that survives, and the stakeholder
   restated it in the same breath as the exemption: *"markers govern everything else"*
   [src: EP-001/Q-005].
5. **A column whose delimiter cell carries no marker is laid out exactly as ADR-0003 decision 9
   lays it out** — padding to the right of the text. Carried forward from ADR-0005 decision 4,
   unchanged [src: WI-0002 AC4; src: ADR-0003].
6. **The delimiter row is not a content row and decisions 1 to 4 do not reach it.** Its cells are
   composed by ADR-0004 decision 1: the leading colon the input had, then hyphens, then the
   trailing colon the input had, filling `width + 2` with no spaces. Carried forward from ADR-0005
   decision 5, unchanged [src: ADR-0004]. A delimiter cell holds no text and can hold no `<br>`, so
   decision 3 cannot reach it either.
7. **Nothing here changes how a column's width is computed, or the one space either side of a
   cell's text.** A column is still as wide as the display width of its widest cell
   [src: WI-0001/Q-001], the two surrounding spaces are untouched [src: WI-0001/Q-003], and no
   composed line gains trailing whitespace [src: EP-001/Q-001]. Carried forward from ADR-0005
   decision 6, unchanged; decision 3 moves where a cell's text sits inside its column, not what the
   column measures.

## Consequences

Easy: decisions 1, 2 and 4 to 7 are what the code already does, verified with evidence against
WI-0002's ten criteria, so nothing that ships today has to change to satisfy this ADR
[src: WI-0002]. The engagement has runnable work again — `WI-0003` — where before this answer it
had none, and a fresh sign-off is due when it next reaches rest [src: EP-001/Q-004].

Hard: decision 3 is stated at exactly the resolution the stakeholder authorised and no further, so
it is not yet enough to implement from. Anyone reaching for it before `WI-0003` is Ready will find
five undecided edges and must not guess past them [src: WI-0003]. The second cost is documentary:
`ADR-0005` is now `superseded` and every document that cites it for the marker rule — the vision's
round-2 paragraph in particular — has to point a reader here as well, without rewriting the
stakeholder's round-2 words, which remain what they said at the time [src: ADR-0005].

Reversibility: decision 3 is cheap in code and expensive in documents, in the same way ADR-0005
decision 2 was. It has since been built — `WI-0003` shipped `has_break_tag` and the branch in
`compose_row` that consumes it [src: mdtab.py; src: WI-0003] — so reversing it no longer costs only
this file and the paragraphs that cite it: it would also move every multiline cell in every
document the tool has been run over, which is one idempotent re-run of the filter. It is
not ours to reverse in either case: it is the stakeholder's decision, taken in the knowledge that
it narrows an earlier one of their own, and only they may take it back. Decisions 1, 2 and 4 to 7
inherit ADR-0005's reversibility unchanged.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 5 | 2026-08-30T00:57:01Z | review-close | EP-001 | Erratum, in `## Corrections`: the `## Consequences` reversibility paragraph's clause *"Nothing has been built against it yet"* is replaced, because `WI-0003` has since shipped the exemption. No decision changes and nothing is superseded |
| 4 | 2026-08-30T00:57:01Z | review-close | EP-001 | Provenance correction, in `## Corrections`: the `## Context` paragraph beginning *"So ADR-0005 is superseded rather than corrected"* now carries a citation. The assertion is unchanged |
| 3 | 2026-08-30T00:57:01Z | review-close | EP-001 | Provenance correction, in `## Corrections`: the `## Context` paragraph beginning *"Two sentences of theirs"* now carries a citation. The assertion is unchanged. Versions 3, 4 and 5 were made by one execution of `review-close` at the engagement's ending, in response to `lint-claims --context epic`; they carry the same timestamp because they were one edit, and are three versions because each is one correction |
| 2 | 2026-08-30T00:13:37Z | answer-questions | WI-0003 | Provenance correction: decision 3's sentence naming the two edges it does not decide now also cites `ADR-0008`, where the stakeholder's answers to `WI-0003/Q-001` and `WI-0003/Q-002` decided them. The assertion is unchanged |
| 1 | 2026-08-29T23:58:20Z | answer-questions | EP-001 | First version, recording the stakeholder's answer to `EP-001/Q-005`: a cell containing a line break is exempt from its column's marker and sits at the left. Supersedes ADR-0005, carrying its decisions 1, 2, 4, 5 and 6 forward unchanged and narrowing its decision 3 |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-08-30T00:57:01Z | review-close | EP-001 | provenance | `## Context`: the paragraph beginning *"Two sentences of theirs"* now cites [src: WI-0002/Q-001; src: EP-001/Q-004], the two answers whose contradiction it describes. The assertion is unchanged |
| 2026-08-30T00:57:01Z | review-close | EP-001 | provenance | `## Context`: the paragraph beginning *"So ADR-0005 is superseded rather than corrected"* now cites [src: ADR-0005; src: .claude/agile-skills/spec/doc-header.md], the ADR whose decisions it says are carried forward and the section that draws the repair/supersession line. The assertion is unchanged |
| 2026-08-30T00:57:01Z | review-close | EP-001 | erratum | `## Consequences`, reversibility paragraph, said *"Nothing has been built against it yet, so reversing it today costs only this file and the paragraphs that cite it; reversing it after `WI-0003` ships would move every multiline cell in every document the tool has been run over"*. `WI-0003` has shipped: [src: mdtab.py] defines `has_break_tag` at line 263 and `compose_row` consumes it at line 303, and [src: WI-0003] closed `delivered`. Replaced with a clause in the perfect tense that keeps the same reversal cost. No code would have to change to satisfy the new text, so this is a repair and not a new decision |
| 2026-08-30T00:13:37Z | answer-questions | WI-0003 | provenance | `## Decision` item 3: *"they are `WI-0003`'s questions for the stakeholder"* now cites [src: ADR-0008] alongside [src: WI-0003]. Both edges have since been answered by the stakeholder and recorded there; this ADR still does not decide them, so the assertion is unchanged |
