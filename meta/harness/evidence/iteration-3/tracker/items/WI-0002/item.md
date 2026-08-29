---
id: WI-0002
type: work-item
title: Honour the alignment markers in a table's delimiter row
status: done
priority: high
epic: EP-001
depends-on:
  - WI-0001
created: "2026-08-28T18:24:41Z"
updated: "2026-08-28T21:03:12Z"
branch: wi/WI-0002
outcome: delivered
---

## Story

As someone who writes markdown tables, I want the alignment I declared in the delimiter row to be
reflected in how each cell is padded, so that the laid-out table in my editor looks the way it
will render.

## Acceptance criteria

Every criterion below is checked against the invocation `plan` recorded for WI-0001
(`tracker/items/WI-0001/artifacts/plan.md`): a document on stdin, the document on stdout, exit 0.
"Field" means what WI-0001 AC12 leaves for a cell's text: the characters between that column's
`|` separators, less the one guard space AC12 keeps on each side — and less only one of them
where the row's outer-pipe style (WI-0001 AC14) drops the other. Alignment moves the content within the
field and changes nothing else.

- [x] AC1 — a column's alignment is read from its cell in the delimiter row, with surrounding
      spaces stripped: a cell that begins with `:` and does not end with one is **left**, one
      that ends with `:` and does not begin with one is **right**, one that does both is
      **centre**, and one with no `:` is **left**. Nothing else in the table affects it. Checked
      by feeding a four-column table whose delimiter row is `| :--- | ---: | :---: | --- |` and
      observing one column of each kind; and by feeding `|  :---  | ---:  |`, whose markers carry
      surrounding spaces, and observing the same alignments.
- [x] AC2 — in a **left** column, every cell's content starts at the left-hand edge of its field
      and the padding follows it, in the header row and every body row. Checked by feeding a table
      whose column is marked `:---` or `---` beside cells of differing width and observing every
      cell's first character at the same display column.
- [x] AC3 — in a **right** column, the padding comes first and every cell's content ends at the
      right-hand edge of its field, in the header row and every body row. Checked by feeding a
      table whose column is marked `---:` beside cells of differing width and observing every
      cell's last character at the same display column, one before the guard space.
- [x] AC4 — in a **centre** column, a cell whose content is `c` display columns wide in a field
      `W` wide is preceded by `floor((W - c) / 2)` spaces and followed by `ceil((W - c) / 2)`, so
      that when the spare space is odd the extra column falls on the **right** and the text leans
      left (`WI-0002/Q-001`). Checked by feeding a table whose centred column has a field three
      columns wide — `| ab |` over `|:---:|` over `| xyz |` — and observing the `ab` row come back
      as `| ab  |`, not `|  ab |`.
- [x] AC5 — the padding in AC2, AC3 and AC4 is counted in display columns per ADR-0002, so a cell
      containing accented letters written precomposed or decomposed, an emoji with a variation
      selector, or CJK text is aligned by what it takes up on screen (`EP-001/Q-003`). Checked
      with a right-aligned column containing `表`, `é` (U+00E9), `e`+U+0301 and an ASCII word, and
      observing that all four cells end at the same display column.
- [x] AC6 — a column's width does not depend on its alignment. Every column is
      `2 + max(display width of its header and body cells)` wide, with WI-0001 AC12's two
      qualifying clauses unchanged. Checked by laying out the same table four times, once with
      each marker in one column's delimiter cell, and observing every `|` at identical display
      columns in all four outputs.
- [x] AC7 — the guard spaces do not move. In every laid-out row, the character immediately after
      an interior `|` and the character immediately before one is a space, whatever the column's
      alignment — the only exceptions being the two WI-0001 AC14 already makes, where a row
      without a leading or trailing `|` has no separator there to guard. Checked by grepping the
      output of a right-aligned and a centred table for `|` not followed by a space.
- [x] AC8 — an empty cell in a right or centre column renders as its whole field of spaces,
      identically to one in a left column; the degenerate column whose header and body cells are
      all empty is still widened only by WI-0001 AC12's minimum-width rule. Checked by feeding a
      table with an empty `:---:` column and observing `|   |` above `|:-:|`, as it renders today.
- [x] AC9 — the delimiter row is padded to the same column widths as every other row and still
      carries the same markers it had in the input: its cells are filled with `-` across the
      whole field keeping any `:` at the ends they had, per WI-0001 AC12, and no `:` is added,
      moved or removed. Checked by feeding `|  :---  | ---:  |` and observing `|:-----|--:|`
      above a table whose columns are 6 and 3 wide.
- [x] AC10 — in a table written without a leading `|` (WI-0001 AC14), the first column is padded
      per its marker like every other column, even though for a `---:` or `:---:` marker the
      padding then lands at the very start of the line as leading whitespace; no outer `|` is
      added to compensate and no other line is changed (`WI-0002/Q-002`). Checked by feeding
      `a | b` / `---:|---` / `xxxx | y` and observing the first column's cells ending at the same
      display column in every row, with the leading spaces present. Feeding that output back in
      produces it again byte-for-byte, so WI-0001 AC6 holds; that mdtab no longer *recognises*
      such a table is the fault WI-0003 exists to fix and is out of scope here.
- [x] AC11 — in a table written without a trailing `|`, the last column is padded per its marker
      like every other column. For a `---:` marker the padding therefore precedes the content and
      the line ends at the content with no trailing spaces, and every row of the table still has
      the same display width (WI-0001 AC2). Checked by feeding `a | bbbb` / `---|---:` /
      `xxxx | y` and comparing line widths with `awk`.
- [x] AC12 — a table every line of which carries the same prefix (WI-0001 AC15) is aligned inside
      that prefix: the prefix is reproduced unchanged at the start of every output line and the
      alignment is applied to what follows it. Checked with a right-aligned table inside a
      blockquote (`> ` on every line) and one indented two spaces under a list item.
- [x] AC13 — a run mdtab does not recognise is still reproduced byte-for-byte, markers included:
      a run whose rows disagree about their cell count (WI-0001 AC13), their outer-pipe style
      (WI-0001 AC14) or their prefix (WI-0001 AC15) comes back exactly as it went in even when its
      delimiter row carries `:` markers, and a `|` line inside a fenced code block (WI-0001 AC8)
      is untouched. Checked
      by feeding each of those four documents with alignment markers in them and diffing input
      against output.
- [x] AC14 — every acceptance criterion of WI-0001 still holds on documents containing alignment
      markers, **except** the single clause of its AC12 that fixes a cell's padding to the right
      of its content, which AC2, AC3 and AC4 above supersede. Everything else in AC12 is still
      required: the two guard spaces, the `2 + max(...)` width, the two qualifying clauses
      idempotence forces, the delimiter-row filling and the outer-pipe rule. Checked by running
      WI-0001's shipped test suite, which passes apart from the two places that encode the
      superseded clause and are therefore updated to the placement AC3 requires:
      `tests/fixtures/basic-ascii.out.md`, whose `id` column is marked `---:`, and the
      padding-position assertion in `test_ac12_every_cell_has_exactly_one_space_against_each_pipe`,
      which is narrowed to the columns AC2 still governs rather than removed. Nothing else in that
      suite changes. Checked also by AC6 (idempotence) on the documents of AC10 and AC11.
      WI-0001's own `item.md` is not edited: it is closed, and its criteria are the record of what
      was delivered. (Checking clause amended in round 3, `WI-0002/Q-003`; the criterion's
      substance is untouched.)

## Out of scope

- Adding, removing or changing an alignment marker. The tool reports what the author wrote; it
  never decides an alignment for them.
- Detecting tables, or leaving non-table content alone — WI-0001 owns that and this item builds
  on it.
- Changing which runs mdtab recognises as a table. AC10 makes mdtab emit a bare table it will
  not recognise on a later run; fixing that is WI-0003, filed from the same answer, and this item
  must not pre-empt it by changing a recognition rule.
- Any diagnostic output. mdtab stays silent about anything it does not lay out (EP-001,
  ADR-0003).

## Notes

Depends on WI-0001: there is no padding to make alignment-aware until the padding exists. WI-0001
is `done` and merged at `5138b52`.

### What the stakeholder settled, and where it went

Round 1 filed two questions and round 2 applied the answers; both replies are verbatim in
`artifacts/refinement-qa.md` and in `questions/Q-001.md` and `Q-002.md`.

- **The marker decides, everywhere.** *"Whatever the marker says, that's where the text sits in
  the cell — every row, every column, no exceptions"* (`Q-001`). That sentence is why AC2, AC3
  and AC4 say "in the header row and every body row", and why AC10 and AC11 exist rather than an
  exception.
- **A centred cell's odd spare column goes on the right** (`Q-001`, option A), matching
  `prettier` and `pandoc`. That is AC4.
- **The first column of a bare table is aligned too, leading whitespace and all** (`Q-002`,
  option A, against the recommendation of B): *"a space at the front of the line is a price I'll
  pay. Don't add the bars, and don't leave the table alone either."* That is AC10.
- **The fault that exposes is WI-0003, not a workaround here:** *"if the tool then can't
  recognise a table it laid out itself, that's a fault in the tool and I'd want it sorted rather
  than worked around."* `answer-questions` filed WI-0003 (`arose-from: WI-0002/Q-002`) rather
  than widening this item.

The wider answers reaching this item from earlier rounds: display width (`EP-001/Q-003`,
ADR-0002) into AC5, and the recognition and punctuation policy (`WI-0001/Q-001`..`Q-003`,
ADR-0003) into AC13 and AC14.

### Assumed, not asked

Six mechanical points were settled from the record rather than put to the stakeholder, each
recorded with its basis in `artifacts/refinement-qa.md` under "Settled without asking": where the
padding sits relative to the guard spaces (AC7), how AC14 stops contradicting AC2–AC4, that
column widths do not change (AC6), that the header row is aligned like the body (AC2–AC4), that
the delimiter row is unchanged by this item (AC9), and what an empty cell does (AC8). Round 2
added two more: how the marker is read from a delimiter cell (AC1) and what a right-aligned last
column does in a table with no trailing `|` (AC11). All rest on the standing deferral *"The rest
of how it is built is your call, not mine"* (`EP-001/Q-001`) and on the marker sentence above.

### Routed to `plan`, not to the stakeholder

- How alignment is carried from the delimiter-row parse to the layout — an argument to the cell
  renderer, a per-column value computed once, or something else. `docs/architecture/overview.md`
  v2 constrains only that anything touching a column's width goes through the single width
  function and keeps both of the rules WI-0001 AC6 forces; this item changes no width (AC6).
- Whether the field-width arithmetic for a dropped guard space (AC10, AC11) is expressed as a
  narrower field or as a special case at the row's ends.

### AC14's checking clause amended, round 3

`verify` filed `Q-003` because AC14 carried two clauses that could not both hold: it excepts the
single clause of WI-0001 AC12 that fixes a cell's padding to the right of its content, and it also
required WI-0001's shipped test suite to run *unchanged* — while two places in that suite encode
exactly the excepted clause, both reached through the fixture `basic-ascii`, whose delimiter row
is `|---|:---|---:|`.

`answer-questions` took option A of that question and amended the **checking clause only**. What
AC14 requires of the tool is unchanged, and no behaviour, test or fixture changed as a result of
the amendment — the two places had already been updated by `implement`, which declared it as
deviation 1, and `verify` confirmed AC14's substance independently on documents of its own before
filing the question. What changed is a sentence that described an impossible check.

This is the second time this project has amended a criterion's wording rather than its substance;
the first was `WI-0001/Q-005`, and `review-close` wrote there that *"the wording of AC12 is what
should change, not the code"*. The basis is the same and so is the route.

### For WI-0003, noticed here and not acted on

The recognition fault AC10 creates has a second form nobody has written down yet: inside a
blockquote or an indented table (AC12), a right-aligned first column puts its padding immediately
after the prefix, so on a later run the prefix that gets compared is longer on some lines than
others — the same failure as the bare case, arrived at differently. WI-0003's refinement should
cover both.

### What the review accepted rather than sent back

`review-close` found two things, both sentences rather than behaviour, and accepted both with the
correction recorded here so it is found from the item and not only from `artifacts/review.md`.

- **`docs/product/vision.md` v4 states the recognition property before conceding it.** *"A table
  mdtab has laid out is a table mdtab still recognises: making that true where those leading
  spaces appear is WI-0003…"* — true read whole, false read as far as the colon, and this item is
  what makes it false. `docs/architecture/overview.md` v3 states the same fact the right way
  round, under "A property the tool no longer has".
- **ADR-0007 §Decision 1 and `column_alignments`' docstring both say the delimiter row's markers
  are read in exactly one place.** The alignment is — one definition, one call site, checked —
  but `_column_widths` (`mdtab/table.py:166`) and `_render_delimiter` (`:202`) read the same
  delimiter cell for the minimum-width rule and for re-rendering. Both sentences want the words
  "for alignment" in them.

Both put an absolute first and its qualification second, which is the shape that propagates when
a sentence is quoted at the comma. Two in one item is a pattern worth watching for a third.

### What WI-0003 must edit when it lands

Not code: the two documents that record the property WI-0003 restores.

1. `docs/architecture/overview.md` — the whole "A property the tool no longer has" section. It
   says of itself that a reader who finds it there after WI-0003 should treat it as stale.
2. `docs/product/vision.md` — the sentence in finding 1 above, which becomes plainly true once
   WI-0003 lands and should stop hedging.

The second form of the fault is still undemonstrated: inside a blockquote or an indented table, a
right-aligned first column pads immediately after the prefix, so a later run compares prefixes of
different lengths. No fixture exercises it — AC12's two both use markers that pad on the far side.

### Gaps accepted at close

Carried here from `artifacts/review.md`'s `## Accepted gaps`, so they survive the item.

1. **The verification's independence is weaker than the pipeline intends** — the same session ran
   `implement` earlier in the same turn. `verify` declared it and used three defences; the review
   is a fourth. Worth knowing when reading the fourteen ticks.
2. **The recognition fault is deliberate and unfixed** — the stakeholder chose it with the cost in
   front of them (`Q-002`), ADR-0007 records it, AC10 requires it, WI-0003 owns it. The bytes stay
   stable, so nothing is corrupted; what is lost is the second tidy-up, silently.
3. **`column_alignments` is public and unguarded against a `rows` list shorter than two.** No
   reachable input hits it — `lay_out` rejects short runs before calling it — so the guard lives
   in the caller, which WI-0003 will change.
4. **The ten new fixtures' expected outputs were hand-written and never independently re-derived**
   as a set. `implement` counted display columns by hand, `verify` used its own documents
   instead, and the review re-derived four of the ten. The same gap WI-0001 recorded, one item on.
5. **Performance, concurrency and large inputs are unexercised.** No criterion mentions them; the
   largest document run through the tool in this item was 27 lines.
