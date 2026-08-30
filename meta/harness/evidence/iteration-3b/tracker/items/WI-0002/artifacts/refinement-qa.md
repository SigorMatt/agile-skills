---
status: recorded
---

# Refinement Q&A — WI-0002

`status: recorded`. The exchange below is what was actually said. One question was put to the
stakeholder and answered; a second round was considered and not held, because every remaining gap
in the Definition of Ready turned out to be settled by something already on record — the reasoning
for each is under `## Round 2` and `## Settled from the record`. Nothing here is paraphrased into
agreement, and nothing the stakeholder did not say is tagged as though they had.

## What the Definition of Ready needs, and where each gap goes

`refine` walked `spec/dor-dod.md` §1 before writing anything. The agenda below is that walk. It
is recorded here rather than only in the journal so that the next execution does not re-derive
it.

| # | Criterion | State on entry | Where it goes |
|---|-----------|----------------|---------------|
| R1 | frontmatter complete | pass — `validate-workspace` exit 0 | — |
| R2 | story names role, capability, outcome | pass — "As someone who edits markdown documents by hand … so that the source table shows me the same … alignment that the rendered table will have" | — |
| R3 | at least one labelled AC checkbox | pass — AC1 to AC6 exist | — |
| R4 | every AC decidable by observation | **still fails, but nothing is now unknown** — AC1 to AC3 say "offset" and "character" where WI-0001's amended AC1 and AC2 say display width; AC3 does not say which side an odd leftover goes to; AC4 defers to another item's tests instead of naming what is read; AC5 does not name what "mean the same thing" is checked against | AC3's gap was `Q-001` and the stakeholder has answered it: the extra space goes right [src: ADR-0005]. Every remaining gap is `refine`'s to rewrite from the record; the rewrites are listed under `## Settled from the record` |
| R5 | `## Out of scope` names something a reader could assume is included | pass — it already excludes changing which alignment a column has, and column widths | will be extended when the criteria are rewritten |
| R6 | every open question is non-blocking | **pass** — `Q-001` is `answered`; no question on this item is open | — |
| R7 | nothing unfinished in `depends-on` | pass — `WI-0001` is `done`, outcome `delivered`, merged at `045c779` | — |
| R8 | Q&A recorded verbatim, `status: recorded` | **fail** — round 1 is now recorded verbatim, but the field is still `agenda` | `refine`'s to close when its walk is done and it has decided whether a round 2 is needed |
| R9 | one coherent change | pass — one change to where padding sits within a column, in one composing function [src: ADR-0004] | — |
| R10 | every combination of introduced behaviours stated, excluded, or recorded as unconstrained | **fail** — the three markers crossed with the header row, an empty cell, a zero-width column, an indented table and a malformed block are not all stated | most are already settled by recorded decisions; see `## Settled from the record`, and they become criteria or `## Notes` entries when the criteria are rewritten |

## Round 1 — one question, to the stakeholder

**Q-001 — When a centred column has an odd number of leftover padding spaces, does the extra one
go left or right of the text?** **Answered.** Filed at `questions/Q-001.md` with its options and
the cross-answer check. It was blocking: it was the only thing R4 needed that nobody had said, and
guessing it would silently have decided the appearance of every centred column in the
stakeholder's documents.

**Answer**, verbatim:

> Put the extra space on the right. When it cannot sit dead centre I want the text leaning towards
> the side I read from, and it matches the way the rest of the file pads. While you are on this:
> the alignment marker decides everything. Whatever the marker says, that is where the text sits
> in the cell — every row, every column, no exceptions.

Both halves are recorded as ADR-0005 and propagated into `item.md`'s `## Notes` and
`docs/product/vision.md` v4. The second half was not asked for and settles the header-row case on
its own authority; the R10 combination "each marker crossed with the header row" therefore needs a
criterion, not a question.

## Round 2 — considered, and not held

`refine` resumed at `draft` with four Definition of Ready criteria still failing — R4, R5, R8 and
R10 — and applied SKILL.md step 3 to each remaining gap before writing a question. None of them
reached the stakeholder, and the reason is different in each case. They are listed so that a
reader can see the decision not to ask, rather than only its result.

- **Restating AC1 to AC3 in display width rather than "offset" and "character".** `[human]`,
  already answered: *"make the columns equal in what I see, not in some count I never look at"*
  [src: WI-0001/Q-001]. Step 3's second test — already answered, do not ask again. The rewritten
  criteria carry the same display-width preamble WI-0001's do.
- **Which side an odd centring remainder falls on.** `[human]`, answered in round 1 above and now
  AC3's arithmetic.
- **Whether the header cell of a marked column obeys the marker.** `[human]`, answered in round 1
  by *"every row, every column, no exceptions"*. AC1, AC2 and AC3 each say "the header row
  included" on that authority.
- **Where the padding goes in an empty cell, and in a column whose cells are all empty.**
  `[assumed]` — not a new decision. It falls out of AC1 to AC3 with `w = 0` and of ADR-0004's
  minimum width of 1 for a doubly-colonned cell. Written as AC5 so it is visible rather than
  inferred, and checked for idempotence there because that is the case where a composed row could
  stop being recognisable.
- **What "the markers mean the same thing" is checked against.** `[assumed]` — colon-for-colon
  identity per column, between input and output, which is ADR-0004 restated as an observation.
  AC7. Asking would have been asking the stakeholder to specify a test.
- **How the criteria that WI-0001 already owns are re-read.** `[assumed]` — the procedure is
  `spec/dor-dod.md`'s, and AC9 names WI-0001's criteria by ID and says the verdict is a read of
  their text with the suite as evidence. WI-0001 AC3 is called out by name as the one whose text
  this item changes, so that nobody repairs it by editing it.
- **Which function places the padding, and how an escaped pipe is measured.** Routed to `plan`,
  not to a person: the answer would be the same whoever asked for the tool. Recorded in the item's
  `## Notes`.

The one thing that would have gone to the stakeholder in a round 2 — a maximum column width, or
any behaviour they might want that nobody has thought to ask about — has a standing answer already
[src: EP-001/Q-001] and an open channel that is not this item's to open.

## Definition of Ready — the walk at exit

The table under `## What the Definition of Ready needs` records the state on entry and is left as
it was. This is the same walk, re-run after the criteria were rewritten.

| # | Criterion | Verdict | Evidence |
|---|-----------|---------|----------|
| R1 | frontmatter complete | **pass** | `validate-workspace`, exit 0 |
| R2 | story names role, capability, outcome | **pass** | unchanged: "As someone who edits markdown documents by hand … so that the source table shows me the same left, right or centre alignment that the rendered table will have" |
| R3 | at least one labelled AC checkbox | **pass** | AC1 to AC10, each a `- [ ] AC<n>` |
| R4 | every AC decidable by observation | **pass** | every criterion names the input, the exact output text expected, and the comparison; AC1 to AC4 give the cell as a formula in `W` and `w`, AC3 gives two worked examples, AC9 names what the report must contain. No criterion carries an adjective without a threshold |
| R5 | out of scope names something a reader could assume is included | **pass** | six entries, of which "where a marker's colons sit inside the delimiter cell" and "checking that a renderer agrees" are both things a reader of the title would reasonably expect |
| R6 | every open question is non-blocking | **pass** | no question on this item is open; `Q-001` is `answered` |
| R7 | nothing unfinished in `depends-on` | **pass** | `WI-0001` is `done`, merged at `045c779` |
| R8 | Q&A recorded verbatim, `status: recorded` | **pass** | this file, `status: recorded`, with round 1 verbatim and round 2's non-asking recorded |
| R9 | one coherent change | **pass** | one change to where padding sits within a column, in the one function that composes a content row [src: mdtab.py] |
| R10 | every combination stated, excluded, or recorded as unconstrained | **pass** | the item's `## Notes` carries the crossing table: eleven crossings, each pointing at the criterion, the scope entry or the deliberate non-constraint that covers it |

**No override.** Every criterion passes on its own terms; `## Override` below is unchanged.

## Settled from the record — not asked, and why

Everything below was checked against the artifact that settles it, not remembered. None of it was
put to the stakeholder, because each is either already their own answer or an architecture
decision recorded and shipped under WI-0001. `intake` and the earlier `answer-questions` execution
left three things "still for `refine` to settle" in this item's `## Notes`; two of the three turn
out to be settled already, and the finding is recorded here so nobody asks about them again.

- **Where a marker's colons sit inside the delimiter cell.** *Settled* — ADR-0004 decision 1: the
  cell's leading colon if the input had one, then hyphens, then its trailing colon if the input
  had one, occupying exactly `width + 2` characters with no spaces. Shipped in WI-0001 and
  verified there; `mdtab.py` `compose_delimiter()` is the code. This item's `## Notes` said it was
  still open; it is not.
- **Whether a delimiter cell of exactly `:-:` or a single `-` is accepted.** *Settled* — ADR-0003
  decision 3 recognises a delimiter cell as optional colon, one or more hyphens, optional colon,
  so both are accepted. `mdtab.py` `is_delimiter_cell()` is the code. Also on this item's "still
  to settle" list; also not open.
- **A zero-width column marked `:-:`.** *Settled* — ADR-0004 decision 2 raises such a column's
  width to a minimum of 1, so `:`, a hyphen and `:` always fit and the output stays recognisable
  to the filter that produced it.
- **Whether alignment is measured in display width or characters.** *Settled by the stakeholder* —
  *"make the columns equal in what I see, not in some count I never look at"* [src: WI-0001/Q-001],
  recorded as ADR-0003 decision 7. AC1 to AC3 must be restated in display width; that is a
  rewording of the criteria to match a decision already taken, not a new decision.
- **Where a right-aligned or centred column's padding sits relative to the cell's two spaces.**
  *Settled by the stakeholder* — *"One space each side, always"* [src: WI-0001/Q-003] and *"no
  trailing whitespace at the end of any line it writes"* [src: EP-001/Q-001], recorded as ADR-0003
  decisions 6 and 9. Padding moves **within** the column's width, never into or out of the two
  spaces, and never outside the closing pipe.
- **Whether the header cell obeys its column's marker.** *Settled by the stakeholder, in round 1*
  — *"every row, every column, no exceptions"* [src: WI-0002/Q-001], recorded as ADR-0005
  decision 3. It was previously entered here as settled by the item's own story — the source shows
  the alignment the rendered table will have, and every renderer aligns the header cell with its
  column — which was a reading rather than an answer; it is now their own words. AC1 to AC3
  already say "every cell's text in that column", which includes the header row.
- **What happens to a marker on a block that is not a well-formed table.** *Settled* — ADR-0003
  decision 4 copies such a block byte for byte as a whole, so alignment never runs on one.
- **What happens to a marker on an indented table.** *Settled* — ADR-0003 decision 11 re-emits the
  block's own whitespace prefix on every composed line and excludes it from the column widths.
- **Implementation of the change.** Routed to `plan`, not to the stakeholder: which function
  places the padding, and how it is expressed, would be the same whoever asked for the tool.

## Override

None. No Definition of Ready criterion has been overridden. The item passes to `ready` on the
walk under `## Definition of Ready — the walk at exit`, with every criterion met.
