---
title: Which cells the multiline exemption reaches, and how an exempt cell is padded
version: 3
status: current
updated: 2026-08-30T01:04:46Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0008 — Which cells the multiline exemption reaches, and how an exempt cell is padded

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** the stakeholder, recorded by answer-questions (architect), for WI-0003
- **Supersedes:** —

## Context

ADR-0007 decision 3 established *that* a cell whose content contains a line break is exempt from
its column's alignment marker and sits at the left, on the stakeholder's explicit authorisation
[src: EP-001/Q-005; src: ADR-0007]. It deliberately stopped there, and said so: *"The stakeholder
authorised the exemption, not its edges"*, listing five things it did not decide and naming
`WI-0003` as where they would be put to them [src: ADR-0007].

`refine` walked those five and routed each one [src: WI-0003]. Three did not go to a person, and
the reasons are recorded in `tracker/items/WI-0003/artifacts/refinement-qa.md`: the exemption
being per cell rather than per column is already in the stakeholder's own words twice; the
delimiter row is already outside the exemption's reach by ADR-0007 decision 6; and *"top"* has no
referent in a cell that is physically one line. Two were not answerable from anything on record
and went to the stakeholder as `WI-0003/Q-001` and `WI-0003/Q-002`. They have answered both.

This ADR records those two answers and, alongside them, where the other three edges landed, so
that a reader who follows ADR-0007's "five undecided edges" sentence arrives at one document that
accounts for all five rather than at three separate files.

**Q-001 — which written forms of a line break exempt a cell.** A pipe table's row is one physical
line, so no cell can hold a real newline character; whatever "a line break in a cell" is, it is a
convention the author types. The stakeholder was shown five candidates — `<br>`, `<br/>`,
`<br />`, `<BR>`, and a trailing backslash — as four options, with the team's recommendation
marked as the team's and placed after them [src: WI-0003/Q-001]. Their reply:

> Any way of typing a `<br>` counts — I don't type it the same way twice, so `<br>`, `<br/>`,
> `<br />` and the upper-case one should all behave identically. A backslash on the end of a cell
> is not something I write to mean a line break, so leave those cells alone and let the marker
> place them as usual. That's your A.

[src: WI-0003/Q-001]

**Q-002 — whether an exempt cell is still padded out to its column's width.** Their word for an
exempt cell at sign-off was *"plain"* [src: EP-001/Q-004], which has two readings that produce
visibly different files: the leftover spaces after the text, so every line of the table stays the
same width, or no padding at all, so the exempt row ends short and its closing pipe does not line
up. Both were put to them with a worked side-by-side example, along with a third reading under
which one `<br>` exempts a whole row [src: WI-0003/Q-002]. Their reply:

> Pad it — the left-hand table. The closing pipes lining up is the whole reason I want this tool,
> and I'd be annoyed if one `<br>` in a row put a kink in the right-hand edge. By "plain" I meant
> only that the marker shouldn't push the text around; everything else about that cell stays
> ordinary.

[src: WI-0003/Q-002]

Neither answer contradicts anything else the stakeholder has said. The cross-answer checks on both
questions are recorded in the question files and in `WI-0003`'s journal; the marker-reach conflict
that ADR-0007 exists to settle was raised and settled before either of these questions was asked,
and nothing here reopens it [src: EP-001/Q-005].

## Options considered

The stakeholder chose from the options they were shown. Both sets are reproduced, because an ADR
that shows only the chosen path documents a conclusion rather than a decision.

**For Q-001 — which forms exempt a cell** [src: WI-0003/Q-001]:

- **A — every spelling of an HTML break tag, and only those.** `<br>`, `<br/>`, `<br />`, any
  letter case, any amount of space before the slash. Cost: a cell ending in a backslash keeps
  obeying its marker, so an author who writes markdown's own line-break syntax does not get the
  exemption. Risk: low — no judgement call is required of the code, and nothing is exempted
  silently [src: WI-0003/Q-001].
- **B — A, plus a trailing backslash at the end of the cell's text.** Cost: a cell ending in a
  backslash for some other reason — a Windows path, a literal escape — stops obeying its marker
  without the author having asked for it. Risk: the surprise is silent and shows up as a cell that
  moved for no visible reason.
- **C — the exact string `<br>` and nothing else.** Cost: `<br/>`, `<br />` and `<BR>` are
  placed by the marker like ordinary text, so the same intent typed two ways behaves two ways.
  Risk: low in code, high in surprise.
- **D — a wider rule, in the stakeholder's own words.** Any HTML tag at all, or a length
  threshold, or something not on the list.
- **Chosen: A**, by the stakeholder, in the words quoted above. Their stated reason is that they do
  not type it the same way twice, and their stated reason for rejecting B is that a trailing
  backslash is not something they write to mean a line break.

**For Q-002 — whether an exempt cell is padded** [src: WI-0003/Q-002]:

- **A — still padded, leftover spaces after the text.** Every line of the table stays the same
  width and every closing pipe lines up; the exemption means only that the marker does not move
  the cell's text. Cost: nothing visible distinguishes an exempt cell from a left-marked one in the
  output. Risk: low — it is the layout WI-0001 already ships for unmarked columns
  [src: ADR-0003].
- **B — not padded; the cell ends after its text.** Cost: the exempt row is shorter than its
  neighbours and its closing pipe does not line up, on exactly the tables the tool exists to tidy.
  Risk: it trades the tool's purpose for visibility of the exemption in the source.
- **C — not padded, and the whole row left byte-for-byte as typed.** Cost: stronger than B — one
  `<br>` anywhere exempts every cell of that row, so the row's other columns disagree with the
  rest of the table too. Risk: the same as B, multiplied by the row's width.
- **Chosen: A**, by the stakeholder, in the words quoted above.

## Decision

1. **A cell is exempt from its column's alignment marker when its text contains an HTML line-break
   tag in any spelling.** The recognised forms are `<`, then `br` in any letter case, then any
   amount of whitespace, then an optional `/`, then `>` — so `<br>`, `<br/>`, `<br />`,
   `<BR>`, `<Br />` and `<br >` all exempt, and all behave identically [src: WI-0003/Q-001].
   This is the whole of ADR-0007 decision 3's "what counts as a line break" [src: ADR-0007].
2. **A trailing backslash at the end of a cell's text does not exempt it.** Such a cell is placed
   by its column's marker exactly as any other cell is [src: WI-0003/Q-001].
3. **Nothing else exempts a cell.** No other HTML tag, no length, no character count. Decisions 1
   and 2 are the complete test [src: WI-0003/Q-001].
4. **An exempt cell is padded out to its column's width, with the leftover spaces after its text.**
   Its layout is exactly what ADR-0003 decision 9 lays down for a cell in an unmarked column
   [src: ADR-0003], so every line of a tidied table stays the same width and every closing pipe
   lines up, whatever markers the table carries [src: WI-0003/Q-002]. This is the whole of
   ADR-0007 decision 3's "whether such a cell is still padded out" [src: ADR-0007].
5. **The exemption changes where a cell's text sits and nothing else about the cell.** It is
   measured for display width like any other cell and can be its column's widest
   [src: WI-0001/Q-001; src: ADR-0003]; the one space either side of its text is untouched
   [src: WI-0001/Q-003]; no composed line gains trailing whitespace [src: EP-001/Q-001]. Carried
   forward from ADR-0007 decision 7, unchanged, and confirmed by the stakeholder's *"everything
   else about that cell stays ordinary"* [src: WI-0003/Q-002].
6. **The exemption is per cell, not per column.** A marked column containing one exempt cell places
   every one of its other cells by the marker. This is not decided here: it is the stakeholder's
   own words in both places they said them — *"markers are for normal cells, not for those"*
   [src: EP-001/Q-004] and *"markers govern everything else"* [src: EP-001/Q-005] — and ADR-0007
   decision 4 already records it. It is restated so that all five of ADR-0007's edges are
   accounted for in one place.
7. **The delimiter row is untouched by decisions 1 to 6.** Its cells are composed by ADR-0004
   decision 1 and a delimiter cell holds no text, so no spelling of a break tag can appear in one.
   Carried forward from ADR-0007 decision 6, unchanged [src: ADR-0007; src: ADR-0004].
8. **"Top-left" is implemented as "left".** A pipe table's cell occupies one physical line, so
   there is no vertical dimension for text to sit at the top of. This is an assumption, not a
   decision of the stakeholder's: it was stated in `WI-0003/Q-002`'s context precisely so they
   could overturn it for free while answering, and their reply did not
   [src: WI-0003/Q-002; src: WI-0003]. **No longer an assumption.** It was put to
   them a second time, explicitly, as note 2 of the engagement's sign-off, and they answered it in
   their own words: *"'left' is all I ever meant by 'top-left' since a row is one line"*
   [src: EP-001/Q-006]. The decision is unchanged; it now stands in their name rather than in
   ours.

## Consequences

Easy: `WI-0003` becomes refinable. Every gap the Definition of Ready walk left open on it that
depended on a person is now closed [src: WI-0003], and the acceptance criteria `refine` writes
next can be checked by someone with a terminal — decision 1 names an exact set of inputs and
decision 4 names an exact output shape. Decision 4 also means the exemption needs no new layout
code: it selects the unmarked-column path the filter already has [src: ADR-0003].

Hard: decision 1 fixes a recognition rule in the tool that has nothing to do with tables. A cell
whose text happens to contain `<br>` inside a code span, or as literal text about HTML, is exempt
under decision 3's "nothing else" just as much as one that means it — the rule is textual and has
no notion of context. That is the cost of a test the stakeholder can predict without reading the
code, and it was not raised with them because no option on offer avoided it. It has been raised with
them since: it was note 1 of the engagement's sign-off, stated as the cost it is, and they
accepted it rather than asking for a narrower rule — *"a cell that merely talks about `<br>`
sitting flush left is fine"* [src: EP-001/Q-006]. Decision 1 is unchanged; what changes is that
its cost is now acknowledged by the person who pays it.

Reversibility: decision 4 is free to reverse — it selects between two layouts the filter already
implements, and one idempotent re-run of the tool over a document restores either. Decision 1 is
cheap in code and not ours to reverse: it records what the stakeholder types in their own files,
which is a fact about them rather than a choice about the design. Widening it later — to the
trailing backslash of option B, say — costs one pattern and one criterion, and would silently move
text in documents already tidied; narrowing it would do the same in the other direction. Decisions
5 to 8 inherit their reversibility from the ADRs they carry forward.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-08-30T01:04:46Z | answer-questions | EP-001 | Two additions from the stakeholder's acceptance of the engagement [src: EP-001/Q-006], neither of which changes a decision. Decision 8 (*"'Top-left' is implemented as 'left'"*) records their own confirmation of it and so stops being an assumption; the `## Consequences` "Hard" paragraph records that decision 1's mention-only cost, which it said had not been raised with them, was raised at the sign-off and accepted |
| 2 | 2026-08-30T00:57:01Z | review-close | EP-001 | Provenance correction, in the new `## Corrections`: option A under `## Options considered` now cites the question that put it to the stakeholder. The assertion is unchanged |
| 1 | 2026-08-30T00:13:37Z | answer-questions | WI-0003 | First version, recording the stakeholder's answers to `WI-0003/Q-001` (every spelling of an HTML break tag exempts a cell; a trailing backslash does not) and `WI-0003/Q-002` (an exempt cell is still padded out to its column's width). Closes the two edges ADR-0007 decision 3 left undecided, and accounts for the other three it listed |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-08-30T00:57:01Z | review-close | EP-001 | provenance | `## Options considered`, option A for `Q-001` (*"every spelling of an HTML break tag, and only those"*) now cites [src: WI-0003/Q-001], the question whose `## Options considered` it reproduces and whose answer chose it. The assertion is unchanged; the option is quoted, not restated |
