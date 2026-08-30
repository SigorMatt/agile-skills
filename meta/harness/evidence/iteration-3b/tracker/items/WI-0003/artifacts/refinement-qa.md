---
status: recorded
---

# Refinement Q&A — WI-0003

`status: recorded`. The exchange below is what was actually said. Round 1 put two questions to the
stakeholder and both came back; round 2 was considered and not held, because every remaining gap in
the Definition of Ready turned out to be closed by one of those two answers or by something already
on record. Nothing here is paraphrased into agreement, and nothing the stakeholder did not say is
tagged as though they had — in particular the *"top-left" means "left"* reading is `[assumed]`, not
`[human]`, because they left it standing rather than endorsing it.

The field was `agenda` from the moment the questions were filed until the walk finished; it moved
to `recorded` in round 2, by `refine`, which owns it. `answer-questions` propagated the answers
into `## Round 1` and deliberately did not touch this field.

What *is* final here is the routing: five things were listed as unknown when this item was
created, and this execution decided, one at a time, which of them the stakeholder must settle and
which the record already settles. That decision is recorded now rather than at the end, so that
the execution which resumes this item does not re-derive it and does not ask the stakeholder
twice.

## What the Definition of Ready needs, and where each gap goes

`refine` walked `spec/dor-dod.md` §1 before writing anything. The agenda below is that walk.

| # | Criterion | State on entry | Where it goes |
|---|-----------|----------------|---------------|
| R1 | frontmatter complete | pass — `validate-workspace` exit 0; `type`, `epic` and `priority` all set | — |
| R2 | story names role, capability, outcome | pass — "As someone who writes markdown tables by hand and sometimes puts a line break inside a cell … so that a multi-line cell does not get pushed around by a marker that was meant for ordinary one-line text" | — |
| R3 | at least one labelled AC checkbox | pass — AC1 exists as `- [ ] AC1` | — |
| R4 | every AC decidable by observation | **fail, and still failing** — AC1 is marked draft and is undecidable twice over: it says "at minimum a literal `<br>`", which does not name the set of things that qualify, and it asserts "with the column's padding to the right of the text", which presumed an answer to something nobody had been asked | `Q-001` and `Q-002` are **answered**, and both now name exact observable behaviour [src: ADR-0008]. Nothing on this row waits on a person any longer; it waits on `refine` rewriting AC1 and the R10 crossings in one pass |
| R5 | out of scope names something a reader could assume is included | pass on entry — four entries, of which "changing a column's width" and "rendering, wrapping or otherwise interpreting the line break" are both things a reader of the title could assume were included | will be extended when the criteria are rewritten, with the delimiter row's markers |
| R6 | every open question is non-blocking | **fail on entry, deliberately** — `Q-001` and `Q-002` were open and blocking. That is this round's whole purpose; it is what suspended the item | **closed.** Both are `status: answered`, `answered-by: human`, with cross-answer checks recorded and consequences named. No question on this item is open |
| R7 | nothing unfinished in `depends-on` | pass — `depends-on` is empty. The item touches the same function WI-0002 changed, and WI-0002 is `done`, outcome `delivered` | — |
| R8 | Q&A recorded verbatim, `status: recorded` | **fail** — this file is still `agenda` | the answers have arrived and `## Round 1` now carries both verbatim. The half that remains is `refine`'s: it flips this field when its walk finishes |
| R9 | one coherent change | pass — one exemption, applied in the one function that composes a content row, gated on one test of a cell's text | — |
| R10 | every combination stated, excluded, or unconstrained | **fail** — the exemption crossed with each of the three markers, with the header row, with an empty cell, with an unmarked column, with an indented table and with idempotence is not stated anywhere | most fall out of `Q-001` and `Q-002` once answered; the crossings that do not are settled from the record below and become criteria or `## Notes` entries when the criteria are rewritten |

## Round 1 — two questions, to the stakeholder — answered

Filed at `questions/Q-001.md` and `questions/Q-002.md`, both blocking, both addressed to the
human, presented as one ask. **Both are answered**, by the stakeholder, between turns. The question
and the reply are reproduced here; the options and the worked examples are in the question files,
which is where the stakeholder read them.

- **Q-001 — Which of `<br>`, `<br/>`, `<br />`, `<BR>` and a trailing backslash makes a cell
  exempt?** `[human]`. Product stake, and the first of `spec/question.md` §4's conditions: it
  depended on intent no document records — what the stakeholder actually types in their own files.
  A pipe table's row is one physical line, so no cell can hold a real newline; whatever "a line
  break in a cell" is, it is a convention they write, and the tool recognising the wrong set would
  either exempt cells they wanted centred or fail to exempt the ones they meant.

  **Answer**, verbatim:

  > Any way of typing a `<br>` counts — I don't type it the same way twice, so `<br>`, `<br/>`,
  > `<br />` and the upper-case one should all behave identically. A backslash on the end of a cell
  > is not something I write to mean a line break, so leave those cells alone and let the marker
  > place them as usual. That's your A.

  They chose option A of four. Recorded as ADR-0008 decisions 1 to 3, and propagated into
  `item.md` `## Notes` and `docs/product/vision.md` v7. It fixes an exact set of inputs, so the R4
  half that read "does not name the set of things that qualify" is closed: a criterion can now be
  written that someone with a terminal can decide.

- **Q-002 — Is an exempt cell still padded out to its column's width, or does it end after its
  text?** `[human]`. Product stake, and `spec/question.md` §4's fourth condition: the record was
  genuinely silent on this case and either choice is visible in every file they run the tool over.
  Their word for it was *"plain"*, which has two readings. Two of their own answers leaned towards
  padding — *"columns are as wide as the widest cell in them"* [src: EP-001/Q-001] and *"it has to
  line up on the screen"* [src: WI-0001/Q-001] — but neither was said about this case, and writing
  a criterion on our reading of one word of theirs is the move this protocol exists to prevent.

  **Answer**, verbatim:

  > Pad it — the left-hand table. The closing pipes lining up is the whole reason I want this tool,
  > and I'd be annoyed if one `<br>` in a row put a kink in the right-hand edge. By "plain" I meant
  > only that the marker shouldn't push the text around; everything else about that cell stays
  > ordinary.

  They chose option A of three, and in doing so said what *"plain"* had meant at sign-off
  [src: EP-001/Q-004]: the marker, and nothing else. Recorded as ADR-0008 decisions 4 and 5, and
  propagated into the same three places. It also confirms, unprompted, the `## Settled from the
  record` entry below on the two spaces either side of a cell's text — *"everything else about that
  cell stays ordinary"*.

  The reply left the *"top-left" means "left"* assumption standing. It was stated in this question's
  `## Context` for exactly that purpose, and it is recorded as ADR-0008 decision 8, still tagged
  `[assumed]` rather than `[human]`: silence on an assumption we flagged is not the same as them
  endorsing it, and it stays overturnable at no cost.

That was all of them for this round, and nothing further on this item goes to the stakeholder.

## Settled from the record — not asked, and why

The item's `## Notes` listed **five** things for `refine` to put to the stakeholder. Three of them
do not go to a person, and each is a different reason. They are listed so a reader can see the
decision not to ask, rather than only its result. `refine` SKILL.md step 3's test was applied to
each in order, and the test that fired is named.

- **Whether the exemption is per cell or per column** — *"does one `<br>` cell make its whole
  column behave as if unmarked, or only that one cell?"* **Already answered; do not ask again**
  (step 3, second test). Their sentence is per-cell in both halves and in both places they said
  it: *"A **cell** with a line break … should just sit top-left … markers are for normal cells,
  not for those"* [src: EP-001/Q-004], and *"a cell with a line break … sits top-left whatever the
  column marker says, **and markers govern everything else**"* [src: EP-001/Q-005]. "Markers are
  for normal cells" and "markers govern everything else" both say the marker keeps applying to the
  cells that are not exempt, including the normal cells of the same column. Recorded as
  `[human]`, from their own words, and it becomes a criterion — a marked column containing one
  exempt cell has all its *other* cells placed by the marker.

- **Whether the delimiter row's marker is still preserved colon-for-colon in such a column.**
  **Already settled by a recorded decision** (step 3, second test). ADR-0004 decision 1 fixes a
  delimiter cell as the leading colon the input had, hyphens, the trailing colon the input had,
  filling `width + 2` with no spaces; the filter adds no marker, removes none and moves none, and
  WI-0002 verified it. ADR-0007 decision 6 carries that forward and says in terms that the
  exemption cannot reach the delimiter row, because a delimiter cell holds no text and can hold no
  `<br>`. Nothing in either of the stakeholder's replies asks to change it. Recorded as
  `[assumed]` — the assumption being that they did not mean to reopen a decision they never
  mentioned — and it becomes a criterion and an `## Out of scope` entry, so that a column whose
  cells ignore the marker while the marker stays in the file is stated rather than discovered.

- **What "top-left" means when a cell occupies one line.** **Not a product decision at all**
  (step 3, fourth test — and weaker than that: it is not a decision anyone can take). A pipe
  table's cell is one physical line; there is no vertical dimension for anything to sit at the top
  of, so "top" has no referent and no implementation. Recorded as `[assumed]`: we read
  *"top-left"* as *"left"*, on the reading that it is how the HTML default is usually described.
  Asking would be asking the stakeholder to explain their own idiom. It is stated in `Q-002`'s
  context so they can correct it for free while answering something they do care about, and it
  goes into the item's `## Notes` as an assumption either of them can overturn.

Three further things were checked and are settled by decisions already shipped, and were never on
the "must ask" list. They are recorded so that nobody re-opens them:

- **How a column's width is measured, and whether an exempt cell counts towards it.** Settled —
  display width, ADR-0003 decision 7, reaffirmed by the stakeholder at sign-off (*"measuring by
  what I see on screen is the whole point"* [src: EP-001/Q-004]). An exempt cell is measured like
  any other and can be its column's widest.
- **The two spaces either side of a cell's text.** Settled by the stakeholder — *"One space each
  side, always"* [src: WI-0001/Q-003], ADR-0003 decisions 6 and 9. The exemption moves text
  *within* the column's width and never into or out of those two spaces.
- **What happens to a `<br>` inside a block that is not a well-formed table, or inside a fenced
  code block.** Settled — ADR-0003 decision 4 copies such a block byte for byte before any cell is
  ever composed, so the exemption never runs on one [src: EP-001/Q-003].

## Routed to `plan`, not to a person

- **How the exemption is expressed in the code** — where the test for a line break lives, whether
  it is a compiled pattern or a substring search, and how it interacts with the escaped-pipe
  question WI-0001 already routed to `plan`. The answer would be the same whoever had asked for
  the tool. It is in the item's `## Notes`.

## Round 2 — considered, and not held

Nothing was asked. `refine` re-walked `spec/dor-dod.md` §1 with the two answers in hand and every
remaining gap closed without a person, so a second round would have been the failure F-023 records:
routing to the stakeholder a decision that was not theirs to make. SKILL.md step 3's test was
applied to each remaining gap and the test that fired is named.

- **The exact set of strings that counts as a break tag** — **already answered**, in round 1.
  Writing it as a shape (`<`, `br` in any case, whitespace, an optional `/`, `>`) rather than as a
  closed list of the four spellings they happened to name is `refine`'s reading of *"I don't type
  it the same way twice"* [src: WI-0003/Q-001], and it is recorded as `ADR-0008` decision 1 by
  `answer-questions` before this round began. Asking them to enumerate `<br >` and `<Br/>` would
  have been asking them to do the tool's job.
- **Whether a break tag inside a fenced or malformed block matters** — **already settled**, by
  ADR-0003 decision 4: such a block is copied byte for byte before any cell is composed
  [src: EP-001/Q-003]. It becomes AC8 rather than a question.
- **Whether an exempt cell that is also the widest sets its column's width** — **already settled**,
  and confirmed twice: *"columns are as wide as the widest cell in them"* [src: EP-001/Q-001] and
  *"everything else about that cell stays ordinary"* [src: WI-0003/Q-002]. It becomes AC5.
- **How the exemption is expressed in code** — **implementation-only; routed to `plan`.** Whether
  the test is a compiled pattern or a substring search, and where it lives, would be the same
  answer whoever had asked for the tool. It stays in the item's `## Notes`.
- **An exempt cell that also contains an escaped pipe** — **left deliberately unconstrained**, and
  recorded as such in `## Notes` with who left it so, per R10. WI-0001 already routed the escaped
  pipe to `plan` and `plan` has not settled it; deciding it here would settle another item's
  question inside this one.

## The R10 crossings, and where each one is stated

R10 does not require a combination to be decided, only to be **visible**. This is the full
enumeration for this item; the third column names where a reader finds it.

| the exemption crossed with | behaviour | where |
|---|---|---|
| a left marker | exempt cell laid out left; the column's other cells still left-placed | AC3 |
| a right marker | exempt cell laid out left; the column's other cells still right-placed | AC3, AC6 |
| a centre marker | exempt cell laid out left; the column's other cells still centred | AC1, AC3, AC5 |
| no marker at all | no observable difference — the two rules give the identical layout | AC4 |
| the header row | reaches a header cell exactly as a body cell | AC1, AC3, AC6 |
| an empty cell | an empty cell holds no break tag, so it is placed by its marker as before | AC7 |
| a column that is entirely exempt | every content cell laid out left; the marker stays in the delimiter row | AC6 |
| the delimiter row | unreachable — a delimiter cell holds no text | AC7 |
| column width | exempt cell measured like any other; may be the widest | AC5 |
| the two spaces either side | untouched | the criteria preamble, `## Out of scope` |
| a trailing backslash | not exempt | AC2 |
| another HTML tag, or a word beginning `br` | not exempt | AC2 |
| an indented table | indent reproduced, exemption applies | AC8 |
| a fenced code block | block copied byte for byte; never composed | AC8 |
| a malformed table block | block copied byte for byte; never composed | AC8 |
| idempotence | re-running the filter on its output changes nothing | AC9 |
| WI-0001 and WI-0002's criteria | re-read by ID, with the three this narrows named | AC10 |
| an escaped pipe in the same cell | **deliberately unconstrained** | `## Notes`, and WI-0001's open question to `plan` |

## Definition of Ready — the walk at exit

| # | Criterion | Verdict |
|---|-----------|---------|
| R1 | frontmatter complete | **pass** — `validate-workspace` exit 0; `type`, `epic` and `priority` set |
| R2 | story names role, capability, outcome | **pass** — unchanged from entry, and still true of the criteria as rewritten |
| R3 | at least one labelled AC checkbox | **pass** — AC1 to AC11, each `- [ ] AC<n>` |
| R4 | every AC decidable by observation | **pass** — AC1, AC2, AC3, AC5 and AC6 each quote a byte-exact expected output in full; AC4, AC7, AC8 and AC9 name the comparison and the verdict that follows; AC10 names 21 criteria by ID and the read to perform; AC11 names the command. No criterion contains an unmeasurable adjective |
| R5 | out of scope names something a reader could assume is included | **pass** — six entries, of which "rendering, wrapping or interpreting the break tag" and "changing which alignment a column has" are both things a reader of the title could assume were included |
| R6 | every open question is non-blocking | **pass** — no question on this item is open; `Q-001` and `Q-002` are `answered` |
| R7 | nothing unfinished in `depends-on` | **pass** — `depends-on` is empty; WI-0002, whose function this touches, is `done`, outcome `delivered` |
| R8 | Q&A recorded verbatim, `status: recorded` | **pass** — this file, `recorded`, with both questions and both replies verbatim and every answer tagged |
| R9 | one coherent change | **pass** — one exemption, one test of a cell's text, applied in the one function that composes a content row |
| R10 | every combination stated, excluded or unconstrained | **pass** — the eighteen crossings above, one of them deliberately unconstrained with who left it so |

## Override

None, and none was sought. The item was not passed to `ready` in round 1: it moved to
`awaiting-answer` with `resume-to: draft`, which is what the Definition of Ready failing is
supposed to produce when the person who can close the gap is not here. They closed it in their own
words, and round 2 passed all ten criteria on their merits. No criterion was waived and none needed
to be.
