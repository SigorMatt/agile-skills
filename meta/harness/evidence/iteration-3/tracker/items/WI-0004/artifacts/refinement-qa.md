---
status: recorded
---

# Refinement Q&A — WI-0004

**`status: recorded`.** Round 1 audited the item against the Definition of Ready, settled what the
record could settle, routed what belongs to `plan`, and filed three questions to the stakeholder.
The stakeholder answered all three on 2026-08-29; `answer-questions` propagated the answers into
the acceptance criteria and returned the item to `draft`. Round 2 completed the R10 table, named
AC5's tests, and took the item to `ready`. The exchange below is what was actually said.

---

## The Definition of Ready audit — round 1, at 2026-08-29T07:23Z

Walked criterion by criterion against `spec/dor-dod.md` §1, on `item.md` as `answer-questions`
left it at 2026-08-29T07:18:00Z.

| # | verdict | evidence |
|---|---------|----------|
| R1 | pass | frontmatter carries `id`, `type: work-item`, `epic: EP-001`, `priority: high`, `created`, `updated`, `arose-from: EP-001/Q-005`; `validate-workspace` exits 0 |
| R2 | pass | `## Story` names the role (*someone who writes markdown tables by hand and puts more than one line inside a cell*), the capability (*mdtab leaves such a cell sitting plainly at the left*) and the outcome (*so that the markers keep meaning what they mean for ordinary cells*) |
| R3 | pass | AC1–AC5 exist, labelled, as checkboxes |
| R4 | **fail** | three defects, below |
| R5 | pass | `## Out of scope` names rendering or wrapping a multi-line cell across output lines — which is the first thing a reader would assume an item about multi-line cells does — as well as the caveats and gaps already declined as work |
| R6 | **fail** | `Q-001`, `Q-002` and `Q-003` are open and `blocking: true`. This is the intended state: the item is suspended on them, and R6 is what makes that suspension honest rather than a formality |
| R7 | pass | `depends-on` is absent; the item touches how a cell's padding is chosen and needs nothing else finished first |
| R8 | **fail** | this file declared `status: agenda` |
| R9 | pass | one coherent change: one new rule about which cells obey their column's marker. `Q-002` could widen its blast radius from a cell to a column, but neither answer makes it two items |
| R10 | **fail** | the new rule crossed with the header row, with the three markers, with a cell that is *only* a break, and with the code-span case has no stated behaviour anywhere |

### The three R4 defects round 1 recorded

1. **AC1 does not define the term it turns on.** *"A cell that contains a line break"* is the
   whole subject of the item, and a markdown table row is one line of text, so no cell can contain
   an actual newline — every such break is an HTML tag, written at least five ways. Someone with a
   terminal and no context cannot tell whether `a<br/>b` is in or out. That is `Q-001`.
2. **AC3 states one of the two available answers as though it were settled.** It says *"every
   other cell in the same column is unaffected"*, which is one reading of *"markers are for normal
   cells, not those"*; the other reading is that the column goes plain. That is `Q-002`.
3. **AC5's checking clause is not yet satisfiable and repeats a known trap.** It requires the
   tests expected to change to be *named individually*, and none is named. `review-close` derived
   exactly this rule on WI-0003 after four criteria in this epic counted artefacts and had to be
   reconciled afterwards; AC5 stated the rule without obeying it.

---

## The exchange — round 1, one ask, three questions

The full text, context and options of each are in `questions/Q-001.md`, `Q-002.md` and `Q-003.md`.
Below: the question as asked, and the answer as given.

### Q-001 — Which cells does the new rule apply to — what counts as "a line break in a cell"?

Options offered: **A** exactly the characters `<br>`; **B** any HTML line-break tag however
written; **C** B, except inside a code span. `refine` recommended **B**.

> **[human]** *"If it breaks the line when I read the document, it counts — capitals, a slash,
> spaces, an attribute, doesn't matter, they are all the same thing to me and should be the same
> thing to the tool. The one in backticks is different: that is someone showing the tag, not using
> it, so that cell is an ordinary cell and keeps whatever its column says. I do write about markup
> in these tables, so please get that case right."*

**Option C**, against the recommendation, and with the reason for it. Propagated into AC1 (the
definition and the four-spelling transcript) and AC7 (the code-span cell, which must come back
byte-for-byte identical).

### Q-002 — When a cell contains a line break, does only that cell stop obeying the column's marker, or does the whole column?

Options offered: **A** only that cell; **B** the whole column. `refine` recommended **A**.

> **[human]** *"Only that cell. Putting a break in one row must not go and shift rows I never
> touched — that is exactly the kind of surprise I do not want from this thing. A ragged-looking
> column is fine; it is telling me the truth about what is in it."*

**Option A.** Propagated into AC3, which now carries the answer and a concrete three-row check
instead of stating the reading as though it were settled.

### Q-003 — Does the rule apply to a header cell that contains a line break, the same as to a body cell?

Options offered: **A** yes, the header is a cell like any other; **B** no, the header always obeys
the marker. `refine` recommended **A**.

> **[human]** *"Yes, the header is a cell like any other — if it has a break in it, it sits plain
> at the left too. I do not want a rule I have to remember an exception to, and a heading that
> reads on two lines is no different from a body cell that does."*

**Option A.** Propagated into AC6, which is new and carries the shipped tool's current centred
output as its transcript.

### Round 2 — nothing was asked

Every question of the stakeholder's was answered, and the three points that remained — naming
AC5's tests, completing this table, and the edges of what a code span is — are about this
project's own tests and markdown's own grammar. A different stakeholder would not answer them
differently, so under `SKILL.md` step 3 they were decided or routed to `plan` rather than asked.

One question was filed to the **architect**, `Q-004`, `blocking: false`: `docs/product/vision.md`
v7 says these three are unsettled, which the answers have made untrue, and `refine` does not write
`docs/`.

---

## Settled without asking, and on what basis

None of this went to the stakeholder, per `SKILL.md` step 3: re-asking something the record
already answers is how a stakeholder's attention gets spent on nothing.

1. **What "top-left" means in a tool that emits one line per row.** *"Left"* is what AC1 states and
   is checkable. *"Top"* has no referent in mdtab's output, where a row is one line; it describes
   how a viewer renders the cell, which mdtab does not control and this item does not change.
   `[assumed]` — recorded so a reader can disagree with it rather than having to notice it.
2. **The column's width is still measured from the cell's text exactly as typed.** `a<br>b` is six
   characters wide and stays six, rather than being measured as its longest rendered line (`b`,
   one). `[assumed]` — the basis is EP-001's success measure, *"every row has its `|` characters
   at the same display column … when the output is viewed in a fixed-width font"*, together with
   ADR-0002. mdtab's output is read as plain text in an editor; a column narrower than the text in
   it would put the pipes out of line in the very place the tool exists to line them up.
3. **The alignment marker itself is untouched in the delimiter row.** A `:---:` column containing
   a multi-line cell still comes back with `:---:`, widened to the column. `[assumed]` — the basis
   is the stakeholder's own phrasing, *"whatever the column marker says"*, which presumes the
   marker is still there, and EP-001 `## Out of scope`: the tool changes spacing, not content.
   AC2 states it.
4. **A cell whose entire content is a break** — `| <br> |` — is a cell containing a line break and
   is covered by AC1; it needs no rule of its own. `[assumed]`.
5. **Nothing else about the tool changes.** Recognition, run extent, fenced code blocks, prefixes,
   escaped pipes, CRLF: this item changes what decides a cell's padding and nothing else. The
   epic's standing properties (idempotence, non-table lines byte-for-byte, silence, exit 0) are
   AC4 and are checked, not assumed. `[assumed]` as to scope.
6. **This item is expected to change no existing test.** `grep -rniE '<br' tests/` exits 1: no test
   and no fixture in the repository contains a `br` tag, so no existing expectation is about a
   document AC1's rule reaches. `[assumed]`, from the repository rather than from anyone — AC5
   names the twenty tests that must nonetheless pass unmodified.

---

## Routed to `plan`, not to a person

None of these would be answered differently by a different stakeholder, so under `SKILL.md` step 3
they are design decisions and are in the item's `## Notes` for `plan` to settle.

1. **Where the per-cell override lives** — in the scanner, in the table model, or at render time —
   and whether ADR-0007 (*alignment is placed inside the `cells` field*) is amended or gains a
   companion. ADR-0007 is not contradicted by anything here: it says where alignment padding goes
   inside a cell's field, and this item changes which cells obey their column's marker.
2. **How the break is detected in the cell text**, and its interaction with the existing
   escaped-pipe handling.
3. **How much of a code span the tool needs to understand** to satisfy AC7, including the three
   cases `## Notes` leaves deliberately unconstrained: an unbalanced backtick, a multi-backtick
   span, and a cell holding a tag both inside and outside a span. This is the only part of the
   item that is new machinery rather than a new use of old machinery.

---

## The R10 table, complete

Every combination of the behaviour this item introduces with what the tool already does. Every row
is stated in a criterion, named in `## Out of scope`, or recorded in `## Notes` as deliberately
unconstrained with who left it so.

| the new rule crossed with … | state |
|---|---|
| a `:---:` (centre) column | AC1, first transcript — the cell sits left |
| a `---:` (right) column | AC1, second transcript — the cell sits left |
| a `:---` (left) column | no change: left is already where the rule puts it |
| a column with no marker | no change: unmarked columns already pad on the right |
| the delimiter row's marker text | AC2 — unchanged, widened to the column |
| the header row | **AC6** — a header cell with a break sits left like any other cell |
| `<br/>`, `<br />`, `<BR>`, a tag with attributes | **AC1** — all count; case, slash, spaces and attributes make no difference |
| a break written inside a code span | **AC7** — not a break; the cell keeps obeying its marker, and the transcript must come back byte-for-byte identical |
| an unbalanced backtick, a multi-backtick span, a tag both inside and outside a span | **deliberately unconstrained** by `refine` at round 2, `## Notes`; `plan` decides and records |
| a `br` tag in a delimiter cell | impossible: a delimiter cell containing anything but dashes, colons and spaces stops the run being a table (`tests.test_units.ColumnAlignmentTest.test_a_delimiter_cell_with_no_dash_is_not_a_delimiter_row_at_all`), `## Notes` |
| the other cells of the same column | **AC3** — unaffected; only the cell with the break sits left |
| a cell that is only a break | settled above, item 4 — it is a cell containing a break, so AC1 |
| column width measurement (ADR-0002) | settled above, item 2 — measured from the text as typed |
| a wide or combining character in the same cell | unchanged: width is display width [src: ADR-0002], and this item moves padding rather than measuring it |
| idempotence, non-table lines, silence, exit 0 | AC4 — checked on every document the criteria name |
| the shipped test suite | AC5 — no existing test expected to change, twenty named that must pass unmodified |
| recognition rules, run extent, fenced code, prefixes, escaped pipes, CRLF | untouched; `## Out of scope` and settled item 5 |

---

## Override

None. No Definition of Ready criterion was overridden, and none needed to be.
