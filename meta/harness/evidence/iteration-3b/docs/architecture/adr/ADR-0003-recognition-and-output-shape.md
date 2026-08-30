---
title: Table recognition and output shape, after the stakeholder's round-1 answers
version: 4
status: current
updated: 2026-08-29T23:45:10Z
updated-by: review-close
updated-for: WI-0002
---

# ADR-0003 — Table recognition and output shape, after the stakeholder's round-1 answers

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** answer-questions (architect), for WI-0001
- **Supersedes:** ADR-0002

## Context

`refine` put four questions to the stakeholder about WI-0001 and all four came back
[src: WI-0001/Q-001; WI-0001/Q-002; WI-0001/Q-003; WI-0001/Q-004]. Two of them settle things
ADR-0002 had already decided the other way, and two settle things no document had decided at all,
so ADR-0002 can no longer be the document a reader acts on. This ADR restates the recognition
rule in full — carrying forward everything ADR-0002 decided that the answers did not disturb —
and adds the output shape, so that `plan` and `implement` have one current document to check code
against rather than two that disagree.

**Indented tables.** ADR-0002 decision 2 required every line of a table to begin with `|` in
column one, and said in as many words that `refine` and `plan` could put that back to the
stakeholder if it mattered. `Q-002` did exactly that, quoting the rule and its consequence [src: WI-0001/Q-002]. The
answer:

> Tables under a numbered list are all over my notes — that is half of what I write, so yes,
> tidy those. Quoted ones I have never written and do not expect to, so do not spend anything on
> them. Whatever the indent was, put it back exactly as it was.

[src: WI-0001/Q-002]

That is the stakeholder authorising the change to a recorded decision, on the question that was
put to them for that purpose — which is what `spec/question.md` §4 requires before an ADR is
superseded. It authorises option B of that question and explicitly declines option C, so
blockquoted tables stay unrecognised.

**How a cell's width is measured.** ADR-0002 decision 7 fixed a column's width as its widest
cell without saying what "widest" counts, which is unambiguous only for ASCII. `Q-001` asked
[src: WI-0001/Q-001], and
the answer chose display width over character count:

> It has to line up on the screen — that is the entire reason I want this tool, so make the
> columns equal in what I see, not in some count I never look at. I write English almost all the
> time, but names with accents turn up and I paste an emoji into a status column more often than
> I would like to admit, and those are exactly the tables that come out crooked today. If a rare
> emoji is off by one in some terminal I will live with it.

[src: WI-0001/Q-001]

The last sentence is what makes this decidable rather than a research project: an approximation
that is occasionally off by one on an emoji is accepted in advance.

**What the cells and the delimiter row look like.** Neither was fixed by any document, and WI-0001
AC1 and AC2 are satisfiable by several different files. `Q-003` fixed the padding — *"One space
each side, always"* [src: WI-0001/Q-003] — and `Q-004` fixed the delimiter row — *"Dashes all the
way across, pipe to pipe. That row is a rule under the header, not a row of content"*
[src: WI-0001/Q-004].

Two things follow that the stakeholder did not state and that this ADR therefore decides.

1. **Whether the delimiter row's own dashes count towards a column's width.** ADR-0002 decision 7
   included the delimiter row among the cells a width is taken from. Under `Q-004` [src:
WI-0001/Q-004] the delimiter
   row carries no content and is composed to whatever width the column already has, so letting an
   input's long dash run widen a column would inflate the table permanently for no reason the
   stakeholder would recognise. Their own words settle the reading: that row is *"a rule under
   the header, not a row of content"*.
2. **How deep an indent may be before the block is code rather than a table.** Four or more
   leading spaces is also markdown's indented-code syntax, and `Q-002`'s option B named that as
   the cost of the option the stakeholder chose. See the options below.

## Options considered

On the indent depth:

- **A —** Recognise an indented table only up to three leading spaces, the point at which
  markdown's indented-code syntax begins. Cost: `10. ` produces a four-space indent, and a table
  under a nested list produces more, so a share of exactly the tables the stakeholder called
  *"half of what I write"* would still be silently skipped, with no way for them to tell that
  from the tool not working. Risk: low for damage, high for disappointment.
- **B —** Recognise a uniformly indented pipe block at any depth, and do not look for indented
  code blocks at all. Cost: a pipe table written inside an *indented* code block — someone
  showing raw markdown without fencing it — would be tidied. Risk: bounded. The block must still
  be a well-formed pipe table by every other rule below, which prose and most code are not, and
  the stakeholder's stated protection is for **fenced** blocks [src: EP-001/Q-003], which is
  preserved exactly.
- **Chosen: B**, because A fails the thing the answer asked for and B's failure case is narrow,
  visible and harmless — an example table comes back aligned. Widening to a rule that also
  tracked indented code blocks is available later if it ever bites.

On the delimiter row and width:

- **C —** Keep ADR-0002 decision 7 as written: the delimiter row's cells count towards the
  column width. Cost: a hand-drawn `|------------------|` freezes a wide column into every future
  run, and the stakeholder would see a table that will not narrow. Risk: low but permanent-looking.
- **D —** Take the width from the header and body cells only; compose the delimiter row to fit.
  Cost: the first run over an existing document narrows some tables, which is a bigger first diff.
  The stakeholder has already said the size of the first diff is not a concern
  [src: WI-0001/Q-003]. Risk: low.
- **Chosen: D.**

## Decision

The filter recognises exactly one thing: a **GitHub-flavoured pipe table with outer pipes**,
optionally indented by whitespace, outside a fenced code block, whose rows are internally
consistent. Everything else is copied.

1. **Fences first.** While reading, the filter tracks fenced code blocks opened and closed by
   ``` or ~~~ . Lines inside a fence are copied unchanged and are never candidates for a table,
   whatever they look like. (Unchanged from ADR-0002 decision 1.)
2. **A candidate block** is two or more contiguous lines that share a byte-identical leading
   whitespace prefix — possibly empty — and, after that prefix is removed, each begins with `|`
   and ends with `|` once trailing whitespace is disregarded. A line whose leading whitespace
   differs from the block's, or which is missing either outer pipe, ends the candidate block. A
   table written without outer pipes is not recognised. The prefix may contain only whitespace:
   a `>` makes the block a blockquote, which is not recognised and is copied.
3. **A candidate block is a table** only if its second line is a delimiter row — every cell
   matching optional colon, one or more hyphens, optional colon — and the first line, the
   delimiter row and every subsequent line all have the same number of cells. (Unchanged from
   ADR-0002 decision 3.)
4. **A candidate block that is not a table is copied byte for byte**, as a whole: a missing
   delimiter row, a delimiter row with the wrong number of cells, and a body row with the wrong
   number of cells all suppress the whole block. The filter does not repair, pad out or truncate
   a ragged row, and does not reformat the well-formed rows of a block that has a broken one.
   (Unchanged from ADR-0002 decision 4.)
5. **No other table syntax is recognised.** Grid tables, rst simple tables and anything drawn
   with `+---+` borders are ordinary text and are copied. The filter does not look for them.
   (Unchanged from ADR-0002 decision 5.)
6. **Lines the filter composes carry no trailing whitespace.** A line it copies is copied
   verbatim, including any trailing whitespace it arrived with, and including its line ending.
   (Unchanged from ADR-0002 decision 6.)
7. **A cell's width is its display width**, not its character count: each character contributes
   2 if `unicodedata.east_asian_width` reports `W` or `F`, 0 if `unicodedata.combining` is
   non-zero or its category is `Mn` or `Me`, and 1 otherwise. This is an approximation of what a
   terminal does and is accepted as one; emoji in particular may be off by one in some terminals
   [src: WI-0001/Q-001].
8. **A column's width is the display width of its widest cell content**, taken over the header
   row and the body rows only — the delimiter row does not contribute — with no maximum. Nothing
   is truncated and no line is wrapped. Cell content is the text between the pipes with leading
   and trailing whitespace stripped.
9. **Every content cell is written as** a pipe, one space, the cell's text, padding to the
   column width, one space, so a column occupies `width + 2` characters between its pipes. An
   empty cell is written as `width + 2` spaces, which is two only when the column's width is
   zero [src: mdtab.py; src: ADR-0004]. This applies to the header row and to every body
   row. [src: ADR-0004; ADR-0005]
10. **The delimiter row is written as** a pipe followed by `width + 2` hyphens for each column,
    with no padding spaces: a solid rule from pipe to pipe. Alignment markers are WI-0002's
    subject and are out of scope here; this rule describes a delimiter cell that carries no
    marker.
11. **An indented table is re-emitted with its own prefix**, byte for byte, on every line the
    filter composes, and the prefix takes no part in the column widths.

## Consequences

Easy: every rule above is a test with an input file and an expected output file, and the output
of the filter is now fully determined by its input — there is no case left where two different
files would both satisfy the acceptance criteria. Decision 7 costs one `unicodedata` lookup per
character and no dependency, which keeps ADR-0001's single-stdlib-script shape intact.

Hard: decision 7 makes "every line of the table is the same length" false as a way of checking
the tool for any table containing wide or combining characters, so WI-0001's criteria have to be
written in terms of display width instead — which is a weaker thing for a test to assert and needs
the test to compute the same width function the code does. The honest mitigation is that the
width function is small enough to be tested directly, on its own, against a table of known cases.

Also hard: decision 2 means the filter will tidy a pipe table sitting inside an *indented* code
block. Nothing in the tool distinguishes the two, deliberately, and the stakeholder's protection
for **fenced** blocks is untouched.

Reversibility:

- Decision 2, indent: reversing to left-margin-only is cheap in code and expensive in documents —
  tables already tidied stay tidied. Widening further, to blockquote prefixes, remains additive.
- Decision 7, display width: reversible in code; documents formatted under it would need one
  re-run to change, and the re-run is idempotent, so the cost is one diff.
- Decisions 9 and 10, padding and the delimiter row: reversing either rewrites every table in
  every document the tool has been run over. That is the least reversible decision here, which is
  precisely why it was put to the stakeholder rather than assumed.
- Decision 8, the delimiter row not contributing to width: cheap either way.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 4 | 2026-08-29T23:45:10Z | review-close | WI-0002 | Erratum, in `## Corrections`: decision 9's clause *"An empty cell is written as two spaces"* was false for any column wider than zero and for an all-empty `:---:` column, whose width ADR-0004 decision 2 raises to 1. Replaced with the `width + 2` form the code has always produced [src: mdtab.py]. No decision changes, nothing is superseded, and no code would change to satisfy the new text |
| 3 | 2026-08-29T23:17:37Z | answer-questions | WI-0002 | Provenance only, in `## Corrections`: the current citation for `compose_row`, whose line number in the 2026-08-29T22:29:53Z row went stale when WI-0002 moved the function [src: mdtab.py], plus sources for three `## Context` absolutes that carried none. Decision 9 and the earlier correction row are both untouched [src: WI-0002] |
| 2 | 2026-08-29T22:29:53Z | answer-questions | WI-0002 | Provenance only: decision 9 now cites ADR-0004 decision 3 and ADR-0005, which take the marked-column case it was silent on. Its assertion is unchanged |
| 1 | 2026-08-29T21:35:22Z | answer-questions | WI-0001 | First version. Supersedes ADR-0002: carries decisions 1 and 3–6 forward unchanged, amends recognition to allow a uniform whitespace indent (WI-0001/Q-002) and width to be measured by display width over content rows only (WI-0001/Q-001, Q-004), and adds the output shape (WI-0001/Q-003, Q-004) |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-08-29T22:29:53Z | answer-questions | WI-0002 | provenance | `## Decision` item 9 — *"Every content cell is written as a pipe, one space, the cell's text, padding to the column width, one space"* — now carries [src: ADR-0004; ADR-0005]. The assertion is unchanged; the citation says where the marked-column case, which item 9 never decided, is decided. Added because a reader checking `compose_row` against item 9 alone would read it as complete [src: mdtab.py:207] |
| 2026-08-29T23:17:37Z | answer-questions | WI-0002 | provenance | Four citations, no assertion touched. (a) The row above ends *"a reader checking `compose_row` against item 9 alone would read it as complete"* and cites `[src: mdtab.py:207]`; WI-0002 moved `compose_row` from line 207 to 244, so that pointer now resolves to the last line of `column_widths`. `## Corrections` is append-only, so the earlier row stands as written and this one carries what replaces it: [src: mdtab.py], naming the function rather than a line, and [src: ADR-0005] for where the marked-column case is decided. (b) `## Context` *"Indented tables"*, *"`Q-002` did exactly that"*, now cites [src: WI-0001/Q-002]. (c) `## Context` *"How a cell's width is measured"*, *"`Q-001` asked"*, now cites [src: WI-0001/Q-001]. (d) `## Decision` preamble, *"Under `Q-004` the delimiter row carries no content"*, now cites [src: WI-0001/Q-004] |
| 2026-08-29T23:45:10Z | review-close | WI-0002 | erratum | `## Decision` item 9 said: *"An empty cell is written as two spaces."* That is true only of a zero-width column. Read against the code, an empty cell is written as `width + 2` spaces, because `compose_row` computes `pad = width - display_width(cell)` and emits one space, `pad` spaces, one space [src: mdtab.py] — five for an empty cell in a width-3 column [src: run: printf '| L | R |\n|---|---|\n| aaa | bbb |\n|  |  |\n' | python3 mdtab.py -> last row is `|     |     |`], and three, not two, for an all-empty `:---:` column, whose width ADR-0004 decision 2 raises to a minimum of 1 [src: ADR-0004; src: run: printf '|  |\n|:---:|\n|  |\n' | python3 mdtab.py -> last row is `|   |`]. Two spaces remains correct for an all-empty `:---` or `---:` column, where the width is 0 [src: WI-0002 AC5]. The clause predates WI-0002 — it was equally false under WI-0001, and WI-0001 AC3 carries the same wording, which is not edited [src: WI-0001] — and was found by WI-0002's D12 audit because AC5 is about exactly this case. Replaced with the `width + 2` form; the assertion the paragraph makes about cell shape is otherwise unchanged and no code would have to change to satisfy the new text |
