---
id: WI-0002
type: work-item
title: Honour column alignment markers when aligning table cells
status: done
priority: medium
epic: EP-001
depends-on:
  - WI-0001
created: "2026-08-29T21:12:27Z"
updated: "2026-08-29T23:41:41Z"
branch: wi/WI-0002
outcome: delivered
---

## Story

As someone who edits markdown documents by hand, I want the filter to place each column's cell
text according to that column's alignment marker in the delimiter row, so that the source table
shows me the same left, right or centre alignment that the rendered table will have.

## Acceptance criteria

*In every criterion below: **running the filter** means running the single Python 3 script
ADR-0001 specifies, with no arguments, the named input on standard input and output captured from
standard output. **Display width** is the function ADR-0003 defines — 2 for a character whose
`unicodedata.east_asian_width` is `W` or `F`, 0 for a combining mark, 1 otherwise. **A table** is
what ADR-0003 recognises as one. **A column's width** `W` is the display width of its widest
content cell, over the header row and the body rows only, with the minimum of 1 ADR-0004 imposes
on a column whose delimiter cell carries two colons. **A content cell** is a cell of the header
row or of a body row; the delimiter row is not one. **Cell text** is what lies between the pipes
with leading and trailing whitespace removed, and `w` is its display width. Every criterion is
settled by comparing the filter's output against a byte-exact expected output; "the same offset"
is always an offset in display columns, never in characters.*

- [x] AC1 — **Left marker.** Given a table with a column whose input delimiter cell begins with
      `:` and does not end with `:`, every content cell of that column in the output is `|`, one
      space, the cell text, `W - w` spaces, one space. So the text's first display column is the
      same on every row of that column, the header row included, and all padding is to its right.
- [x] AC2 — **Right marker.** Given a table with a column whose input delimiter cell ends with
      `:` and does not begin with `:`, every content cell of that column in the output is `|`,
      one space, `W - w` spaces, the cell text, one space. So the text's last display column is
      the same on every row of that column, the header row included, and all padding is to its
      left.
- [x] AC3 — **Centre marker, including the odd remainder.** Given a table with a column whose
      input delimiter cell both begins and ends with `:`, every content cell of that column in
      the output is `|`, one space, `(W - w) // 2` spaces, the cell text, `W - w - (W - w) // 2`
      spaces, one space — integer division, so when `W - w` is odd the extra space is to the
      **right** of the text [src: WI-0002/Q-001; ADR-0005]. Concretely, a centred column of width
      3 holding the text `ab` is written `| ab  |` and not `|  ab |`, and one holding `Q` is
      written `| Q |` with one space of padding on each side.
- [x] AC4 — **No marker.** Given a table with a column whose input delimiter cell contains no
      colon, every content cell of that column in the output is `|`, one space, the cell text,
      `W - w` spaces, one space — byte-identical to what WI-0001 AC3 requires, and unchanged by
      this item.
- [x] AC5 — **Empty cells and zero-width marked columns.** Given a table in which one row's cell
      is empty in a left-marked, a right-marked and a centre-marked column, each such cell is
      written by AC1, AC2 or AC3 with `w = 0`: `W + 2` spaces between the pipes in every case,
      differing only in the marker. Given a table in which **every** content cell of a marked
      column is empty, that column's output is: for `:---`, `W = 0` and each content cell is two
      spaces; for `---:`, the same; for `:---:`, `W = 1` and each content cell is three spaces
      [src: ADR-0004]. Running the filter on that output leaves it byte-identical.
- [x] AC6 — **Markers and display width together.** Given a table with a left-marked, a
      right-marked and a centre-marked column whose cells include an East Asian wide character,
      an emoji and a letter carrying a combining accent, every line of the output table has the
      same display width, and each column occupies the same span of display columns on every row
      of the table including the delimiter row.
- [x] AC7 — **Markers survive, and mean the same thing.** For every column of every table in the
      output, the output delimiter cell begins with `:` if and only if the input delimiter cell
      began with `:`, and ends with `:` if and only if the input's ended with `:`; between the
      colons it is hyphens only, and the whole cell occupies `W + 2` characters with no spaces
      [src: ADR-0004]. That colon-for-colon identity, column by column, is what "means the same
      thing" is checked as: the filter adds no colon, removes none, and moves none to the other
      end of a cell.
- [x] AC8 — **Idempotence over marked tables.** Running the filter on its own output produces
      output byte-identical to that output, for each of the inputs named in AC1 to AC7.
- [x] AC9 — **WI-0001's criteria re-read by ID, not assumed.** `artifacts/verify-report.md`
      records a verdict for each of WI-0001 AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10 and
      AC11, reached by reading that criterion's own **text** against what the filter now does. The
      suite is evidence for a verdict, never its definition. Two things the report must state
      rather than leave to inference:
      - **WI-0001 AC3 is the one this item's behaviour changes.** Its text — a content cell is
        `|`, one space, the text, "spaces padding it to the column's width", one space — reads as
        padding always following the text. The verdict must say that this now holds only for a
        column whose delimiter cell carries no marker, name AC4 above as where that case is
        asserted, and cite ADR-0005 for the marked case. WI-0001's own criteria are not edited.
      - **Where no test exercises both a WI-0001 criterion and a marked column**, the report names
        that criterion by ID, states the non-intersection, and then either adds a covering case or
        waives that criterion by ID with the reason.
- [x] AC10 — **Tests.** An automated test exists for each of AC1 to AC9, each naming the
      criterion it covers, and the whole suite passes with the command recorded in
      `tracker/project.yaml`. The filter exits with status 0 for every input named in AC1 to AC8.

## Out of scope

- **Changing which alignment a column has.** The filter reads markers; it never adds, removes or
  alters one, and it holds no default it would impose on a markerless column [src: ADR-0004].
- **Where a marker's colons sit inside the delimiter cell.** ADR-0004 fixed that under WI-0001 —
  leading colon, hyphens, trailing colon — and this item does not revisit it. A reader who expects
  "honours alignment markers" to mean the colons move is looking at the wrong item.
- **Alignment inside anything that is not a well-formed table.** A block ADR-0003 declines to
  recognise is copied byte for byte whether or not it contains something that looks like a
  marker, and nothing reports that it was skipped.
- **Column widths, non-table passthrough, indentation and fenced blocks.** WI-0001 established
  all four and this item changes none of them; a marked column's width is computed exactly as an
  unmarked one's is.
- **Checking that a renderer agrees.** The criteria compare the filter's output against expected
  text. No criterion renders a table or asserts anything about how any renderer displays it.
- **Any maximum column width, wrapping or truncation.** Columns grow to fit
  [src: EP-001/Q-001], so there is never a case where alignment has to choose what to drop.

## Notes

**What the stakeholder settled, and where it now lives.** `Q-001` asked one question and the reply
settled two things [src: WI-0002/Q-001]:

- The extra space of an odd centring remainder goes to the **right** of the text — *"Put the extra
  space on the right. When it cannot sit dead centre I want the text leaning towards the side I
  read from, and it matches the way the rest of the file pads."* AC3 states it as arithmetic.
- *"the alignment marker decides everything. Whatever the marker says, that is where the text sits
  in the cell — every row, every column, no exceptions."* So no content cell of a marked column is
  exempt; AC1, AC2 and AC3 each say "the header row included" for that reason.

Both are recorded as ADR-0005, which is what `plan` and `implement` check the code against. The
reading that *"every row"* does not reach the delimiter row — which the same stakeholder calls
*"a rule under the header, not a row of content"* [src: WI-0001/Q-004] — and the reading that
*"every column"* does not reach a column with no marker are both recorded there with their basis,
and re-checked in `questions/Q-001.md` under `## Cross-answer check`. Neither was decided by
narrowing one of their sentences to fit the other.

**DoR R10 — every combination of the behaviours this item introduces.** The behaviours are the
three markers and their absence; there are no options, flags or modes [src: WI-0001]. Each is
crossed with every case that could change the answer, and each crossing is stated somewhere:

| crossed with | where it is stated |
|--------------|--------------------|
| the header row | AC1, AC2, AC3 — "the header row included" |
| a body row | AC1, AC2, AC3 |
| the delimiter row | out of scope above, and ADR-0005: it carries no text to place |
| an empty cell | AC5, first sentence |
| a column whose cells are all empty | AC5, second sentence |
| wide, emoji and combining characters | AC6 |
| a second and third marked column in the same table | AC5, AC6 — each names three marked columns in one table |
| running the filter twice | AC8 |
| an indented table | unconstrained by this item **on purpose**: ADR-0003 re-emits the block's own whitespace prefix on every composed line and excludes it from the widths, so marker handling cannot interact with it. Left so by `refine` |
| a block that is not a well-formed table | out of scope above; ADR-0003 copies it whole, so alignment never runs on one |
| a fenced or blockquoted block | out of scope above; inherited unchanged from WI-0001 |

**What is deliberately left to `plan`.** Which function places the padding and how the split is
expressed — `compose_row` is the single place WI-0001 put cell composition [src: mdtab.py] — and
how an escaped pipe inside a cell is measured, which `docs/product/vision.md` already routes to
`plan` rather than to the stakeholder. Neither would have a different answer for a different
stakeholder.

**Inherited, and worth seeing before it is rediscovered.** `validate-workspace` and `lint-claims`
walk every `*.md` file and decode it as UTF-8 with no error handler, so the non-UTF-8 fixture this
project needs is named `tests/fixtures/not_utf8.markdown` to keep them working. WI-0001 recorded
it; renaming that fixture to `.md` breaks two gates.

**AC3's second worked example describes a width-1 column, and the arithmetic governs.** AC3's
governing sentence asks for `(W - w) // 2` spaces before the text and `W - w - (W - w) // 2`
after. Its second illustration — *"one holding `Q` is written `| Q |` with one space of padding on
each side"* — sets `W = 3, w = 1`, for which that arithmetic gives `|  Q  |`; `| Q |` is what a
width-**1** centred column gives. The arithmetic is what the filter is checked against, and
`ADR-0005` decision 6 keeps the one space either side of the cell text untouched, so a width-3
centred cell cannot be written with no padding at all [src: ADR-0005]. `verify` ran both parities
and passed AC3 on the arithmetic [src: tracker/items/WI-0002/artifacts/verify-report.md], and
`review-close` reached the same reading independently and asked for it to be recorded here rather
than lost at the close [src: tracker/items/WI-0002/artifacts/review.md]. The criterion's text is
`refine`'s and is not edited; this note says how it was read, by whom, and why.
