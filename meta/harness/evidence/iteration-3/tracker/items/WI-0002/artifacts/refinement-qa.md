---
status: recorded
---

# Refinement Q&A — WI-0002

Round 1. Both questions below have been **filed and answered**; the stakeholder's replies are
recorded verbatim under each, which is what DoR R8 reads, so this file now declares
`status: recorded`. The answers were written in by `answer-questions` at 2026-08-28T20:18:09Z
when it propagated them (`questions/Q-001.md`, `questions/Q-002.md`). Round 2, below, applied
them to the criteria together with the three defects under "Settled without asking", asked
nothing further, and passed the Definition of Ready.

Everything under "Settled without asking" is settled *now*, from the record, and does not need
the stakeholder. It is written down so that the next round of `refine` applies the two answers to
an item whose remaining problems are already solved, rather than re-deriving all of this.

---

## The Definition of Ready audit that produced this agenda

Walked criterion by criterion against `spec/dor-dod.md` §1 on `item.md` as it stood at
2026-08-28T20:11:00Z.

| # | verdict | evidence |
|---|---------|----------|
| R1 | pass | frontmatter carries `id`, `type: work-item`, `epic: EP-001`, `priority: high`, `created`, `updated`, `depends-on: [WI-0001]`; `validate-workspace` exits 0 |
| R2 | pass | `## Story` names the role (*someone who writes markdown tables*), the capability (*the alignment I declared reflected in how each cell is padded*) and the outcome (*so that the laid-out table looks the way it will render*) |
| R3 | pass | AC1–AC6 exist, labelled and as checkboxes |
| R4 | **fail** | three separate defects, below |
| R5 | pass | `## Out of scope` names adding/removing/changing an alignment marker, and table detection — both things a reader could assume are included |
| R6 | **fail** | Q-001 and Q-002 are open and `blocking: true`. This is the intended state; R6 is what makes the suspension honest rather than a formality |
| R7 | pass | `depends-on: WI-0001`, which is `done` (`outcome: delivered`, merged at `5138b52`) |
| R8 | **fail** | this file declares `status: agenda` |
| R9 | pass | one coherent change to one function's padding decision; no split indicated |
| R10 | **fail** | the alignment marker × outer-pipe-style combination has no stated behaviour anywhere — that is Q-002, and it is exactly the gap R10 exists to make visible |

### The three R4 defects

1. **AC1 and AC2 do not say where the single guard space goes.** WI-0001 AC12 fixes a laid-out
   cell as `|`, one space, content, padding, one space, `|`. "Padded on the left" does not say
   whether the padding goes inside or outside that leading space, and the two produce different
   bytes. Fixed by wording, not by asking — see "Settled without asking" §1.
2. **AC2 is not decidable at all for an odd remainder.** "The text sits in the middle" has no
   verdict when the spare space cannot be halved. This is Q-001.
3. **AC6 contradicts AC1, AC2 and AC3 as written.** It says *every* acceptance criterion of
   WI-0001 still holds; WI-0001's AC12 says a cell is rendered with its padding *after* the
   content. For a right- or centre-aligned column those cannot both be true. Fixed by wording —
   see "Settled without asking" §2.

---

## Questions filed to the stakeholder — round 1

Both are `blocking: true` and the item is suspended at `awaiting-answer` with `resume-to: draft`.

### Q-001 — the odd column in a centred cell

> When a centred column has an odd number of spare display columns to distribute, does the extra
> one go on the left of the cell's text or on the right?

Options A (extra on the right, matching `prettier`/`pandoc`), B (extra on the left), C (widen the
column so the remainder is never odd). Recommended A. Full context, worked example and
consequences in `questions/Q-001.md`.

Carried as an open unknown since intake — `intake`'s journal records that it declined to invent a
criterion because "either split is defensible and the stakeholder has expressed no preference",
and `docs/product/vision.md` v3 names it as the one thing `refine` must put to the stakeholder
before this item can be Ready.

**Answer (stakeholder, verbatim, 2026-08-28T20:18:09Z):**

> The alignment marker decides everything. Whatever the marker says, that's where the text
> sits in the cell — every row, every column, no exceptions. For the odd one out, put the spare
> space on the right so the text leans left; if that's what the other tools do then my files should
> look the same as theirs rather than argue with them by one space.

Option A, as recommended. Propagated into AC2. The first sentence is wider than the question
asked and is what settles `Q-002` in the same direction: the marker is honoured in every column
without exception.

### Q-002 — right or centre alignment in the first column of a table with no leading `|`

> For the first column of a table written without a leading `|`, when that column's marker asks
> for right or centre alignment, what should mdtab do?

Options A (emit the leading spaces anyway), B (that one cell position stays flush left), C (leave
the whole table alone), D (add the outer bars). Recommended B. Full context in
`questions/Q-002.md`, including the demonstration against the shipped tool.

Not previously known. It surfaced during this audit as the R10 combination
`alignment marker × outer-pipe style`, and it is a product question rather than a design one
because every option loses something the stakeholder can see: either mdtab stops recognising its
own output, or one cell position's declared alignment is not shown, or a well-formed table is
never tidied, or punctuation they did not write appears in their file.

**Answer (stakeholder, verbatim, 2026-08-28T20:18:09Z):**

> Honour the marker there too. If I wrote the colon on that column I meant it, and I don't
> want one column quietly ignoring what I asked for because of where it happens to sit on the line —
> a space at the front of the line is a price I'll pay. Don't add the bars, and don't leave the table
> alone either; and if the tool then can't recognise a table it laid out itself, that's a fault in
> the tool and I'd want it sorted rather than worked around.

Option A, against the recommendation of B. Propagated into AC7. The last clause refuses the cost
that made A the un-recommended option rather than accepting it, so it is not a decision this item
can absorb: it is work no item recorded, filed as **WI-0003** with `arose-from: WI-0002/Q-002`.

---

## Settled without asking

Recorded here rather than put to the stakeholder, per the routing test in `refine`'s step 3.
Nothing in this section is a guess: each item names what settles it.

### 1. Where the padding goes relative to the guard spaces — `[assumed]`

A laid-out cell keeps WI-0001 AC12's shape exactly — `|`, one space, then the field, then one
space, `|` — and alignment redistributes the padding **inside** that field and nowhere else. So a
right-aligned cell is `|`, space, padding, content, space, `|`. The guard spaces are not padding
and are never moved or dropped, except where AC14's outer-pipe style already drops one of them.

*Why this is not a question:* it is forced by AC6 — WI-0001's AC2 (every `|` at the same display
column in every row) and AC12's column arithmetic both hold only if the field's width is
unchanged, and the guard spaces are what make a table readable at all. Any other reading changes
the column widths, which this item is not for. Relying on the stakeholder's standing deferral
*"The rest of how it's built is your call, not mine"* (`EP-001/Q-001`) for the fact that they do
not care which byte holds a space, given the visible result is identical.

### 2. How AC6 stops contradicting AC1–AC3 — `[assumed]`

AC6 will be reworded to require every WI-0001 criterion to hold **except the clause of AC12 that
fixes the padding to the right of the content**, which this item supersedes and which is named
explicitly. Everything else in AC12 — the two guard spaces, the `2 + max(...)` column width, the
two width rules AC6-of-WI-0001 forces, the delimiter-row filling, the outer-pipe rule — is
unchanged and is still required.

*Why this is not a question:* the stakeholder asked for the alignment markers to be honoured, and
`docs/product/vision.md` v3 already promises it ("with the alignment the author declared in each
table's delimiter row reflected in how the cells are padded"). The contradiction is a drafting
defect in this item, not an open decision. **WI-0001's `item.md` will not be edited** — it is
closed, and its criteria are the record of what was delivered; the supersession is recorded here
and in this item.

### 3. Column widths do not change — `[assumed]`

This item changes *where* the padding sits in a cell, never *how much* there is. Column widths
stay exactly what `docs/architecture/overview.md` v2 records under "How wide a column is",
including both rules idempotence forces. A criterion will say so, because a plausible wrong
implementation widens centred columns.

*Why this is not a question:* the overview states the rule is `plan`'s to keep, in terms — "*Anything
that later wants to change a column's width — honouring the alignment markers, for one — must go
through this function and keep both rules*" — and Q-001 option C is the only variant that would
change a width, so the stakeholder gets to see that possibility there.

### 4. The header row is aligned like the body rows — `[assumed]`

A column's marker applies to its header cell as well as its body cells. The draft criteria
already say "in every row", every markdown renderer does the same, and no option anywhere in the
record suggests otherwise.

### 5. The delimiter row is unchanged by this item — `[from the record]`

WI-0001 AC12 already settles the delimiter row completely: its cells are filled with `-` across
the whole field, keeping any `:` at the ends they had. There is nothing in a row of dashes to
align, so AC5 of this item is a regression restatement rather than new behaviour. It stays.

### 6. An empty cell — `[assumed]`

An empty cell in a right- or centre-aligned column renders as its whole field of spaces,
identically to a left-aligned one, because there is no content to place. The degenerate all-empty
column that WI-0001 AC12 widens to fit `:---:` is the same case. A criterion will name it so
`verify` checks it rather than inferring it.

### 7. Routed to `plan`, not to anyone — `[implementation]`

How the alignment is represented between the recognition code and the layout code, and whether
`_render_cell` takes an alignment argument or is split, is a design decision with the same answer
whoever the stakeholder is. It goes in `## Notes` for `plan`, not in a question.

---

---

## Round 2 — 2026-08-28, after the answers

No new question was put to the stakeholder. Round 2 applied the two answers and the three defects
round 1 had recorded, and settled two further points from the record. The acceptance criteria were
rewritten once, as round 1 intended: AC1–AC14 replace the old AC1–AC7.

### What the answers became

| answer | criterion |
|--------|-----------|
| `Q-001` — the odd spare display column goes on the right | AC4 |
| `Q-001` — *"the marker decides… every row, every column, no exceptions"* | AC2, AC3, AC4 ("the header row and every body row"), and the existence of AC10 and AC11 instead of exceptions |
| `Q-002` — the first column of a bare table is aligned, leading whitespace and all | AC10 |
| `Q-002` — *"that's a fault in the tool and I'd want it sorted"* | WI-0003, filed by `answer-questions`; named as out of scope here |

### The three round-1 defects, now fixed

1. **Where the padding sits relative to the guard spaces.** The criteria now define "field" once,
   in the preamble, as what AC12 of WI-0001 leaves between the guard spaces, and AC7 makes the
   guard spaces checkable on their own (`|` is always followed by a space, except at the two row
   ends AC14 of WI-0001 already excepts).
2. **AC6 contradicting AC1–AC3.** Now AC14, which excepts by name the one clause of WI-0001 AC12
   that this item supersedes — padding after the content — and keeps the rest explicitly.
3. **AC2 undecidable for an odd remainder.** Now AC4, with the arithmetic written out.

### Settled without asking, round 2

#### 8. How the marker is read from a delimiter cell — `[assumed]`

AC1: strip the surrounding spaces from the delimiter cell, then a leading `:` means left, a
trailing `:` means right, both mean centre, neither means left.

*Why this is not a question:* it is what every markdown renderer does, and it is what makes the
stakeholder's own words operative — the marker they wrote is the marker mdtab reads. The
recognition of a delimiter row is WI-0001 AC7's and is unchanged: a cell with no `-` in it is not
a delimiter cell, so `| : |` is not a delimiter row and the run is left alone. Confirmed against
the shipped tool rather than assumed:

```
$ printf '| a | b |\n| : | --- |\n| xxxx | y |\n' | python3 -m mdtab
| a | b |
| : | --- |
| xxxx | y |
```

#### 9. A right-aligned last column in a table with no trailing `|` — `[assumed]`

AC11: the marker is honoured there too, so the padding precedes the content and the line ends at
the content rather than in trailing spaces.

*Why this is not a question:* the stakeholder's answer to `Q-001` disposes of it — *"every row,
every column, no exceptions"* — and it is the same shape as `Q-002`, which they answered by
accepting the cosmetic cost. It costs strictly less than `Q-002` did: no leading whitespace is
produced, so mdtab still recognises the table afterwards, and every row keeps the same display
width because the field width is unchanged.

### The Definition of Ready audit, round 2

Walked against `spec/dor-dod.md` §1 on `item.md` as rewritten.

| # | verdict | evidence |
|---|---------|----------|
| R1 | pass | frontmatter complete; `validate-workspace` exits 0 |
| R2 | pass | `## Story` unchanged: role, capability, outcome |
| R3 | pass | AC1–AC14, labelled, as checkboxes |
| R4 | pass | every criterion names the document to feed and the output to observe; the two that were adjectival in round 1 ("sits in the middle", "padded on both sides") are now arithmetic (AC4) or a grep (AC7) |
| R5 | pass | four exclusions, including the recognition fault WI-0003 owns and the tool's silence |
| R6 | pass | `Q-001` and `Q-002` are `answered`; no question is open |
| R7 | pass | `depends-on: WI-0001`, `done`, merged at `5138b52` |
| R8 | pass | this file, `status: recorded`, holds both replies verbatim |
| R9 | pass | one change to where a cell's content sits inside a field it already has; nothing here is separable except the recognition fault, which was separated into WI-0003 |
| R10 | pass | the combinations are enumerated in the criteria rather than left implicit: marker × outer-pipe style (AC10, AC11), marker × prefix (AC12), marker × empty cell (AC8), marker × non-ASCII width (AC5), marker × delimiter row (AC9), marker × a run mdtab does not recognise (AC13). The one combination deliberately left unconstrained is named in `## Notes` for WI-0003: a right-aligned first column inside a blockquote prefix |

## Override

None. No Definition of Ready criterion has been overridden, and none is unmet.
