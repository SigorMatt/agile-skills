---
id: WI-0003
type: work-item
title: Leave a cell containing a line break at the left of its column
status: done
priority: high
epic: EP-001
created: "2026-08-29T23:52:34Z"
updated: "2026-08-30T00:52:41Z"
arose-from: EP-001/Q-004
branch: wi/WI-0003
outcome: delivered
---

## Story

As someone who writes markdown tables by hand and sometimes puts a line break inside a cell, I
want such a cell left plain at the left of its column rather than placed by the column's alignment
marker, so that a multi-line cell does not get pushed around by a marker that was meant for
ordinary one-line text.

## Acceptance criteria

*In every criterion below: **running the filter** means running the single Python 3 script
ADR-0001 specifies, with no arguments, the named input on standard input and output captured from
standard output. **A table** is what ADR-0003 recognises as one. **A content cell** is a cell of
the header row or of a body row; the delimiter row is not one. **Cell text** is what lies between
the pipes with leading and trailing whitespace removed, and `w` is its display width — the
function ADR-0003 defines. **A column's width** `W` is the display width of its widest content
cell, with the minimum of 1 ADR-0004 imposes on a column whose delimiter cell carries two colons.
**A break tag** is `<`, then `br` in any letter case, then any amount of whitespace, then an
optional `/`, then `>` [src: ADR-0008]. **An exempt cell** is a content cell whose text contains a
break tag. **Laid out left** means the cell is written between its pipes as one space, the cell
text, `W - w` spaces, one space — the same shape WI-0002 AC4 gives a column with no marker. Every
criterion is settled by comparing the filter's output against a byte-exact expected output, and
every expected output below is reproduced in full so no criterion depends on re-deriving one.*

- [x] AC1 — **Every spelling of a break tag exempts, and they behave identically.** Running the
      filter on a centre-marked table whose six body rows hold the cell texts `a<br>b`, `a<br/>b`,
      `a<br />b`, `a<BR>b`, `a<Br />b` and `a<br >b` produces exactly:

      ```
      |   form   |
      |:--------:|
      | a<br>b   |
      | a<br/>b  |
      | a<br />b |
      | a<BR>b   |
      | a<Br />b |
      | a<br >b  |
      ```

      Every one of the six is laid out left despite the centre marker, and the header cell `form`,
      which contains no break tag, is centred. [src: ADR-0008]

- [x] AC2 — **Nothing else exempts a cell, a trailing backslash included.** Running the filter on
      a centre-marked table whose five body rows hold the cell texts `freeze\`, `C:\dir\`,
      `<b>bold</b>`, `<break>` and `brr` produces exactly:

      ```
      |    text     |
      |:-----------:|
      |   freeze\   |
      |   C:\dir\   |
      | <b>bold</b> |
      |   <break>   |
      |     brr     |
      ```

      None of the five is exempt: each is centred by WI-0002 AC3. A trailing backslash is not a
      break tag, and neither is another HTML tag nor a word beginning `br` [src: ADR-0008].

- [x] AC3 — **Each marker, the header row, and one exempt cell not affecting its neighbours.**
      Running the filter on a table with a left-marked, a right-marked and a centre-marked column,
      in which the right-marked column's **header** cell and one body cell of the centre-marked
      column contain a break tag, produces exactly:

      ```
      | id | own<br>er | state  |
      |:---|----------:|:------:|
      | 1  |     alice |   ok   |
      | 22 |        bo | x<br>y |
      | 3  |         c |  done  |
      ```

      Three things are settled by that output and each must be read off it: the exemption reaches
      a **header** cell exactly as it reaches a body cell (`own<br>er` is laid out left under a
      right marker); it is **per cell, not per column** (`alice`, `bo` and `c` are still
      right-aligned in that same column, and `ok` and `done` are still centred in the column that
      holds `x<br>y`); and the left-marked column, which holds no break tag anywhere, is untouched
      [src: ADR-0008; src: ADR-0007].

- [x] AC4 — **A column with no marker is unaffected either way.** Running the filter on a table
      with a column whose delimiter cell contains no colon writes every content cell of that
      column laid out left, whether or not it contains a break tag. The exemption and the
      no-marker rule produce the identical layout, so no output byte differs from what WI-0001 AC3
      and WI-0002 AC4 already require of that column.

- [x] AC5 — **An exempt cell is padded to its column's width, so the closing pipes line up.**
      Running the filter on a two-column centre-marked table whose widest cell is an exempt one
      produces exactly:

      ```
      |  Task  |         Notes         |
      |:------:|:---------------------:|
      | deploy | build<br>test<br>ship |
      | review |         ready         |
      |  ship  |          ok           |
      ```

      Every line of that output has the same display width and its `|` characters at the same
      display columns, the row containing the break tag included [src: WI-0003/Q-002]. The exempt
      cell is measured for width like any other and is here its column's widest, which is why
      `W - w` is zero for it and `ready` and `ok` are centred within the width it set
      [src: ADR-0008].

- [x] AC6 — **A column every one of whose content cells is exempt.** Running the filter on a
      table with two right-marked columns, the first of which has a break tag in its header cell
      and in both body cells, produces exactly:

      ```
      | h<br>1   | plain |
      |---------:|------:|
      | a<br>b   |     x |
      | cc<br>dd |    yy |
      ```

      Every content cell of the first column is laid out left; its delimiter cell still ends in
      `:` and begins with a hyphen, exactly as the input's did; and the second column, which holds
      no break tag, is right-aligned throughout. A wholly exempt column does not lose its marker,
      it only stops being placed by it [src: ADR-0008].

- [x] AC7 — **An empty cell is not exempt, and the delimiter row is never exempt.** An empty cell
      contains no break tag, so it is placed by its column's marker exactly as WI-0002 AC5
      requires, unchanged by this item. And for every column of every table in the output, the
      delimiter cell begins with `:` if and only if the input's did, ends with `:` if and only if
      the input's did, is hyphens between, and occupies `W + 2` characters with no spaces — for
      the tables of AC1, AC2, AC3, AC5 and AC6 alike. A delimiter cell holds no text and can hold
      no break tag [src: ADR-0007; src: ADR-0004].

- [x] AC8 — **An indented table is still tidied; a block that is not a table is still copied.**
      Running the filter on a table indented by three spaces, one of whose cells contains a break
      tag, reproduces that indent on every line and lays that cell out left, per WI-0001 AC6.
      Running the filter on a fenced code block whose lines look like table rows containing
      `<br>`, and on a malformed table block containing `<br>` — a body row with a different
      number of cells from its header — returns each block byte for byte identical to its input,
      per ADR-0003 decision 4 and WI-0001 AC7 and AC8. The break tag is looked for only in a cell
      of a block already recognised as a table, so it can never cause a block to be touched that
      would otherwise have been passed through.

- [x] AC9 — **Idempotence.** Running the filter on its own output produces output byte-identical
      to that output, for each of the inputs named in AC1 to AC8.

- [x] AC10 — **WI-0001's and WI-0002's criteria re-read by ID, not assumed.**
      `artifacts/verify-report.md` records a verdict for each of WI-0001 AC1, AC2, AC3, AC4, AC5,
      AC6, AC7, AC8, AC9, AC10 and AC11, and for each of WI-0002 AC1, AC2, AC3, AC4, AC5, AC6,
      AC7, AC8, AC9 and AC10, reached by reading that criterion's own **text** against what the
      filter now does. The suite is evidence for a verdict, never its definition. Three things the
      report must state rather than leave to inference:
      - **WI-0002 AC1, AC2 and AC3 are the ones this item's behaviour narrows.** Each says
        *"every content cell of that column"* is placed by its marker. That now holds only of a
        content cell containing no break tag. The verdict on each must say so, name AC3 above as
        where the exception is asserted, and cite ADR-0007 and ADR-0008 for the authority.
        WI-0002's criteria are not edited: their author narrowed them, and a criterion that
        records what was agreed at the time is not a defect [src: EP-001/Q-005].
      - **WI-0002 AC8's idempotence and AC7's marker identity still hold**, and the verdict must
        say against which of AC1 to AC9 above that was read, not merely that the suite is green.
      - **Where no test exercises both a prior criterion and a break tag**, the report names that
        criterion by ID, states the non-intersection, and then either adds a covering case or
        waives that criterion by ID with the reason.

- [x] AC11 — **Tests.** An automated test exists for each of AC1 to AC10, each naming in its own
      name the criterion it covers under the prefix convention ADR-0006 fixes, and the whole suite
      passes with the command recorded in `tracker/project.yaml`
      (`python3 -m unittest discover -s tests -t .`). The filter exits with status 0 for every
      input named in AC1 to AC9.

## Out of scope

- **Rendering, wrapping or interpreting the break tag.** The filter does not turn `<br>` into a
  newline, does not split the cell across lines, and does not know what a renderer will do with
  it. It emits the cell text exactly as it arrived and only stops the marker moving it.
- **Changing which alignment a column has.** The filter reads markers; it never adds, removes or
  alters one, and an exempt cell does not strip its column's marker from the delimiter row
  [src: ADR-0004; src: ADR-0007]. A reader who expects "exempt from the marker" to mean the
  colons disappear is looking at the wrong item.
- **Changing a column's width, or the one space either side of a cell's text.** An exempt cell is
  measured like any other and can be its column's widest [src: WI-0001/Q-001], and the two
  surrounding spaces are untouched [src: WI-0001/Q-003]. The exemption moves text inside the
  column's width and never into or out of those spaces.
- **Any other convention for a line break.** A trailing backslash does not exempt a cell, and
  neither does any other HTML tag, an entity, or a cell's length [src: WI-0003/Q-001;
  src: ADR-0008]. The stakeholder was shown the backslash and declined it; widening the rule
  later is a new decision, not a bug in this one.
- **Recognition.** Whether a block is a table at all is settled by ADR-0002 as amended by
  ADR-0003, and a break tag inside a fenced or malformed block never reaches cell composition.
- **Checking that a renderer agrees.** The criteria compare the filter's output against expected
  text. No criterion renders a table or asserts anything about how any renderer displays it.

## Notes`.

## Out of scope

- Changing where any *other* cell's text sits. Cells with no line break in them keep the behaviour
  WI-0002 delivered.
- Changing a column's width, the two spaces either side of a cell's text, or the delimiter row.
  None of those is what the stakeholder's reply was about.
- Rendering, wrapping or otherwise interpreting the line break. The tool does not turn a `<br>`
  into anything; it only stops the marker moving the cell that contains one.
- Recognition. Whether a block is a table at all is settled by ADR-0002 as amended by ADR-0003 and
  is not reopened here.

## Notes

**Why this item exists.** It was created by `answer-questions` from the stakeholder's reply to the
engagement's sign-off question, which is why its `arose-from` is `EP-001/Q-004` rather than a
vision or a request. Their words, verbatim:

> A cell with a line break or a `<br>` in it should just sit top-left, plain, whatever the column
> marker says; markers are for normal cells, not for those. … Fix the multiline cells and we are
> done.

[src: EP-001/Q-004]

**This item is authorised; it is no longer contingent.** It used to be. That sentence contradicted
an earlier one of theirs — *"the alignment marker decides everything … every row, every column, no
exceptions"* [src: WI-0002/Q-001] — which was recorded as `ADR-0005` decision 3, so `EP-001/Q-005`
put both to the stakeholder and asked which wins. They chose the later one and authorised the
supersession in as many words:

> You're right, and I over-spoke the first time — the later one wins: a cell with a line break or a
> `<br>` in it sits top-left whatever the column marker says, and markers govern everything else.
> That is your option B, and yes, treat this as me superseding what I said before.

[src: EP-001/Q-005]

`ADR-0007` records that decision and supersedes `ADR-0005` [src: ADR-0007]. This item may therefore
be refined, planned and built; what must **not** happen is any of it being planned or built before
the two questions refinement has put to the stakeholder — `Q-001` and `Q-002` — are answered,
because neither is decidable from the record.

**Refinement round 1, 2026-08-30 — where the five went.** `refine` applied SKILL.md step 3 to each
of the five things listed here when the item was created. Two went to the stakeholder and three did
not; the full reasoning is in `artifacts/refinement-qa.md`, and the short form is:

- **What counts as "a line break" in a cell** — asked, as `Q-001` (blocking). **Answered by the
  stakeholder**; see `## What the stakeholder answered` below.
- **Whether an exempt cell is still padded out to its column's width** — asked, as `Q-002`
  (blocking). **Answered by the stakeholder**; see `## What the stakeholder answered` below.
- **Whether the exemption is per cell or per column** — **not asked; they already answered it.**
  *"Markers are for normal cells, not for those"* [src: EP-001/Q-004] and *"markers govern
  everything else"* [src: EP-001/Q-005] both say the marker keeps applying to the cells that are
  not exempt, in the same column included. Per cell.
- **Whether the delimiter row's marker is still preserved colon-for-colon** — **not asked; already
  decided.** ADR-0004 decision 1 and ADR-0007 decision 6: the filter adds, removes and moves no
  marker, and the exemption cannot reach a row whose cells hold no text [src: ADR-0007].
- **What "top" means in a one-line cell** — **not asked; assumed.** A pipe table's cell is one
  physical line, so "top" has no referent and no implementation; *"top-left"* is read as *"left"*.
  `Q-002`'s context states the assumption so the stakeholder can overturn it for free.

**Open design question, for `plan` rather than for a person.** How the exemption is expressed in
code — where the test for a line break lives, whether it is a compiled pattern or a substring
search, and how it interacts with the escaped-pipe question WI-0001 already routed to `plan`.

**What the stakeholder answered, 2026-08-30 — round 1's two questions.** Both are propagated into
`ADR-0008`, `docs/product/vision.md` v7 and `artifacts/refinement-qa.md`. Their words, verbatim:

> Any way of typing a `<br>` counts — I don't type it the same way twice, so `<br>`, `<br/>`,
> `<br />` and the upper-case one should all behave identically. A backslash on the end of a cell
> is not something I write to mean a line break, so leave those cells alone and let the marker
> place them as usual. That's your A.

[src: WI-0003/Q-001]

> Pad it — the left-hand table. The closing pipes lining up is the whole reason I want this tool,
> and I'd be annoyed if one `<br>` in a row put a kink in the right-hand edge. By "plain" I meant
> only that the marker shouldn't push the text around; everything else about that cell stays
> ordinary.

[src: WI-0003/Q-002]

What `refine` must now write criteria from, all of it recorded as decisions in `ADR-0008`:

- A cell is exempt when its text contains `<`, then `br` in any letter case, then any whitespace,
  then an optional `/`, then `>`. So `<br>`, `<br/>`, `<br />`, `<BR>`, `<Br />` and `<br >` all
  exempt, and all behave identically [src: ADR-0008].
- A trailing backslash does **not** exempt a cell; it keeps obeying its column's marker
  [src: ADR-0008]. Nothing else exempts a cell either — no other tag, no length threshold.
- An exempt cell is padded out to its column's width with the leftover spaces after its text,
  which is exactly what an unmarked column already gets [src: ADR-0003; src: ADR-0008]. Every line
  of the table stays the same width and every closing pipe lines up.
- The exemption moves where a cell's text sits and changes nothing else about it: the cell is
  measured for width like any other and can be its column's widest, and the one space either side
  is untouched [src: ADR-0008].

**No acceptance criterion was amended by `answer-questions`.** The item was at `draft`, its
criteria were not frozen, and the provisional AC1 had to be replaced wholesale together with the
R10 crossings `refinement-qa.md` lists. What the criteria had to say was recorded here and in
`artifacts/refinement-qa.md`; `refine` wrote them in round 2 below.

**Refinement round 2, 2026-08-30 — the walk finished, nothing asked.** The constraint recorded
above — that none of this may be planned or built until `Q-001` and `Q-002` are answered — is
**discharged**: both are `answered`, `answered-by: human`, and propagated. Round 2 held no
conversation and needed none: every gap the Definition of Ready had left was closed either by the
two answers or from the record, and nothing new arose that carries product stake. The provisional
AC1 was replaced by AC1 to AC11, five of which quote a byte-exact expected output in full so that
`verify` can settle them with a diff and no re-derivation.

**Deliberately unconstrained, and who left it so.** One R10 crossing has no stated behaviour on
this item and is named here rather than in a criterion: **an exempt cell that also contains an
escaped pipe (`\|`)**. How an escaped pipe is measured and re-emitted is WI-0001's open design
question, routed to `plan` and still unanswered [src: WI-0001]; whatever `plan` settles there
applies to an exempt cell unchanged, because the exemption decides where a cell's text sits and
not what its text is or how wide it is [src: ADR-0008]. `refine` left it unconstrained rather than
deciding it, because deciding it here would settle WI-0001's question in the wrong item. It is not
a stakeholder question: the answer would be the same whoever had asked for the tool.

**What is already settled and must not be re-asked.** Column widths are display width, not
character count [src: WI-0001/Q-001]; one space each side of a cell's text, always
[src: WI-0001/Q-003]; no line ends in a space or a tab [src: EP-001/Q-001]; a malformed or
unrecognised table is passed through untouched [src: EP-001/Q-003; src: ADR-0003].
