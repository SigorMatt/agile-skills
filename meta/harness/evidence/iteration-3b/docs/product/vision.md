---
title: Product vision
version: 8
status: current
updated: 2026-08-30T01:04:46Z
updated-by: answer-questions
updated-for: EP-001
---

# Product vision

## Who this is for

People who write and maintain markdown documents **by hand, in a text editor**, and who read the
raw source at least as often as the rendered output — README authors, note-takers, anyone whose
tables live in a repository and show up in diffs.

It is not for people who only ever see markdown rendered; for them a ragged source table looks
exactly the same as a tidy one, and this tool has nothing to offer.

## What it is for

Making the **source text** of a markdown table readable, without touching anything else in the
file. The stakeholder's own statement of it, verbatim:

> A filter that reads markdown on stdin and pretty-aligns its tables: pads columns, honours
> alignment markers, leaves non-table content untouched.

[src: EP-001]

Three properties follow from that sentence, and they are the whole product:

1. **It is a filter.** Markdown in on standard input, markdown out on standard output. It
   composes with a pipe, an editor's "filter buffer through command", and a pre-commit hook.
2. **It aligns tables.** Columns padded to a uniform width; cell text placed according to the
   delimiter row's alignment markers.
3. **It is conservative.** Anything that is not a table comes back exactly as it went in. The
   tool declining to help is a much smaller failure than the tool damaging a document, and the
   design should prefer the first whenever the two are in tension.

## What it deliberately is not

- **Not a markdown formatter.** It does not wrap prose, normalise headings, renumber lists, or
  touch any construct other than a table.
- **Not a renderer.** It emits markdown, never HTML or any other format.
- **Not a linter or a repair tool.** It does not report problems with a document and does not set
  out to turn malformed tables into valid ones.
- **Not a file editor.** It does not take paths, does not edit in place, and holds no opinion
  about where your documents live.
- **Not configurable.** There is no config file and no style profile; the alignment markers in
  the document are the only input to how a table is laid out.

## What the stakeholder settled

Three questions went to the stakeholder at intake and all three came back. Their words, and what
each one fixed:

**What it runs as** — *"It is me, at my own machine, piping a file through it from my editor
before I commit — so it has to be a thing I can just run, with no build step and nothing to
install first."* [src: EP-001/Q-002] They delegated the language to us; ADR-0001 records it as a
single Python 3 script using only the standard library [src: ADR-0001].

**What counts as a table** — *"Ordinary pipe tables, the kind you showed — that is all I write. I
have never written one of those grid tables in my life and I do not want the tool looking for
them. Code blocks must be left completely alone; a fenced block full of pipes is not a table and
touching it would be the worst thing this could do. Where it cannot tell, it should pass the text
through and do nothing."* [src: EP-001/Q-003]

**What matters most** — *"Anything that is not a table comes out exactly as it went in, byte for
byte — that is the part I care about most, and I will stop using it the first time it edits a
paragraph. If a table is broken — a row with the wrong number of cells, a missing separator
line — leave it alone rather than guess what I meant; I would much rather it did nothing than
mangled something. And no trailing whitespace at the end of any line it writes: columns are as
wide as the widest cell in them, with no maximum, but nothing hangs off the right-hand edge."*
[src: EP-001/Q-001]

Read together, those answers make conservatism the product's first property rather than a nicety.
The tool declining to act is a small failure; the tool changing something that was not a table is
the failure that ends its use. ADR-0002 turned that into the recognition rule the code is checked
against [src: ADR-0002]; ADR-0003 now carries that rule, with the two amendments the stakeholder
authorised in round 1 below [src: ADR-0003].

### Round 1 of refinement, on WI-0001

Four more questions went to the stakeholder about what a tidied table looks like coming back, and
all four came back [src: WI-0001].

**Where the columns have to line up** — *"It has to line up on the screen — that is the entire
reason I want this tool, so make the columns equal in what I see, not in some count I never look
at. … If a rare emoji is off by one in some terminal I will live with it."*
[src: WI-0001/Q-001] Column widths are therefore measured as display width, not as a count of
characters, and the approximation that costs is accepted in advance.

**Tables that do not start at the left margin** — *"Tables under a numbered list are all over my
notes — that is half of what I write, so yes, tidy those. Quoted ones I have never written and do
not expect to, so do not spend anything on them. Whatever the indent was, put it back exactly as
it was."* [src: WI-0001/Q-002] A uniformly indented table is tidied and its indent reproduced;
a blockquoted one is not recognised.

**What a cell looks like** — *"One space each side, always. The cramped version is unreadable and
it is the readability I am paying for … I do not care how big the first diff is — one big tidy-up
and then everything is consistent forever."* [src: WI-0001/Q-003]

**What the delimiter row looks like** — *"Dashes all the way across, pipe to pipe. That row is a
rule under the header, not a row of content."* [src: WI-0001/Q-004]

Those four are recorded as decisions in ADR-0003, which supersedes ADR-0002 [src: ADR-0003].

### Round 2 of refinement, on WI-0002

One question went to the stakeholder about alignment markers — how a centred column splits an odd
number of leftover padding spaces — and their reply settled a second thing nobody had asked about
[src: WI-0002/Q-001].

**Which side an odd centring remainder falls on** — *"Put the extra space on the right. When it
cannot sit dead centre I want the text leaning towards the side I read from, and it matches the
way the rest of the file pads."* [src: WI-0002/Q-001]

**How far a marker reaches** — *"While you are on this: the alignment marker decides everything.
Whatever the marker says, that is where the text sits in the cell — every row, every column, no
exceptions."* [src: WI-0002/Q-001] No content cell of a marked column is exempt: the header cell
obeys its column's marker exactly as a body cell does.

**Narrowed by its author in round 4.** That paragraph is what the stakeholder said in round 2 and it
is kept here as they said it — but they have since withdrawn its absolute: a cell containing a line
break is exempt, and markers govern everything else [src: EP-001/Q-005]. Read the round-4 section
below with it.

Both are recorded as decisions in ADR-0005, which took the decision ADR-0004 deferred rather than
superseding anything [src: ADR-0005]. ADR-0005 is now itself superseded by ADR-0007, which carries
both of those decisions forward unchanged and narrows only the reach of a marker over a cell that
contains a line break [src: ADR-0007].

### Round 3 of refinement, on EP-001 — the condition on sign-off

The engagement reached rest and the stakeholder was asked whether they accepted it. They did not
accept it as it stood, and named one thing [src: EP-001/Q-004]:

**A cell with a line break in it** — *"A cell with a line break or a `<br>` in it should just sit
top-left, plain, whatever the column marker says; markers are for normal cells, not for those. …
Fix the multiline cells and we are done."* [src: EP-001/Q-004] That is recorded as `WI-0003`, a
draft item whose `arose-from` names this answer [src: WI-0003].

**And they confirmed the two things the sign-off flagged** — *"leaning left when it cannot split
evenly is what I asked for, and measuring by what I see on screen is the whole point."*
[src: EP-001/Q-004] Those close out the two places where what was built and what they pictured
could still have differed: the odd centring remainder [src: ADR-0005] and display-width
measurement [src: ADR-0003] are both endorsed after seeing what they do.

The first of those two statements is in tension with round 2's *"every row, every column, no
exceptions"*, and it was not settled here. It was not ours to settle: both sentences are the
stakeholder's, and one of them is recorded as a decision in their name. `EP-001/Q-005` put the two
side by side and asked which wins [src: EP-001/Q-005]; round 4 below is their reply.

### Round 4 of refinement, on EP-001 — which of their two answers wins

Asked plainly which sentence governs a cell containing a line break, with no recommendation offered
because both sentences were theirs, the stakeholder chose the later one [src: EP-001/Q-005]:

> You're right, and I over-spoke the first time — the later one wins: a cell with a line break or a
> `<br>` in it sits top-left whatever the column marker says, and markers govern everything else.
> That is your option B, and yes, treat this as me superseding what I said before.

[src: EP-001/Q-005]

That authorisation is what ADR-0007 rests on: it supersedes ADR-0005, carrying every other decision
in it forward unchanged and replacing *"no content cell is exempt"* with the exemption above
[src: ADR-0007]. Round 2's paragraph is not edited — a sentence that is wrong because its author has
since said something else is not a document defect (`spec/question.md` §2) — and the narrowing is
recorded beside it instead.

`WI-0003` is no longer contingent: the work is authorised, and `refine` may take it to the
stakeholder for the five things the exemption's edges still depend on [src: WI-0003]. When it is
delivered the engagement reaches rest again and a fresh sign-off is due, because the last one
accepted something else [src: EP-001/Q-004].

### Round 5 of refinement, on WI-0003 — the edges of the exemption

`refine` walked the five things ADR-0007 left undecided about the multiline-cell exemption and put
two of them to the stakeholder, as one ask, with the team's recommendation marked as the team's and
placed after the options [src: WI-0003]. Both came back.

**Which cells count as having a line break in them** — *"Any way of typing a `<br>` counts — I
don't type it the same way twice, so `<br>`, `<br/>`, `<br />` and the upper-case one should all
behave identically. A backslash on the end of a cell is not something I write to mean a line break,
so leave those cells alone and let the marker place them as usual."* [src: WI-0003/Q-001] Every
spelling of an HTML break tag exempts a cell; a trailing backslash does not, and such a cell keeps
obeying its column's marker.

**What an exempt cell looks like coming out** — *"Pad it — the left-hand table. The closing pipes
lining up is the whole reason I want this tool, and I'd be annoyed if one `<br>` in a row put a
kink in the right-hand edge. By 'plain' I meant only that the marker shouldn't push the text
around; everything else about that cell stays ordinary."* [src: WI-0003/Q-002] An exempt cell is
still padded out to its column's width, with the leftover spaces after its text — the same layout
an unmarked column already gets [src: ADR-0003]. That also settles what they meant by *"plain"* at
sign-off [src: EP-001/Q-004]: it was about the marker, and about nothing else.

The other three edges did not go to them, and the reasoning for each is in
`tracker/items/WI-0003/artifacts/refinement-qa.md`. The exemption being per cell rather than per
column is already their own words twice over — *"markers are for normal cells, not for those"*
[src: EP-001/Q-004] and *"markers govern everything else"* [src: EP-001/Q-005]. The delimiter row
is already outside the exemption's reach, because a delimiter cell holds no text [src: ADR-0007].
And *"top"* has no referent in a cell that is physically one line, so it is read as *"left"* — an
assumption, put in front of them inside `WI-0003/Q-002` so they could overturn it while answering
something they did care about, and left standing [src: WI-0003/Q-002].

All five are now recorded in ADR-0008, which closes what ADR-0007 deliberately did not decide
[src: ADR-0008; src: ADR-0007]. `WI-0003` returns to `refine` with nothing on it waiting on a
person.

### Round 6, on EP-001 — the acceptance

The engagement reached rest a second time, with `WI-0003` delivered, and the sign-off was put to
the stakeholder again — because the previous one had accepted something else [src: EP-001/Q-004].
They were asked plainly whether they accepted it, shown all three work items and all eight success
measures, and given three notes on places where what was built and what they pictured could still
differ. They accepted [src: EP-001/Q-006]:

> Yes — I accept it as it stands, your option A. The one thing I held it up for is built and none
> of your three notes changes my mind: a cell that merely talks about `<br>` sitting flush left is
> fine, "left" is all I ever meant by "top-left" since a row is one line, and I have never once
> written an escaped pipe in the same cell as a line break. If that last one ever bites me I will
> come back to you with it as a new job rather than call this one unfinished.

[src: EP-001/Q-006]

Three things in that reply outlive the closing, and each settles something the record had been
carrying as ours rather than theirs:

**A cell that only mentions a break tag is exempt too, and that is acceptable.** The exemption
test is textual — it looks at the cell's text and has no notion of context — so a cell reading
``use `<br>` for a line break`` is placed flush left exactly as one that means it. ADR-0008
recorded that cost and recorded that it had not been put to them; it has now, and they took it
[src: ADR-0008; src: EP-001/Q-006].

**"Top-left" always meant "left".** ADR-0008 decision 8 held this as an assumption, stated in
`WI-0003/Q-002`'s context so they could overturn it for free and left standing when they did not
[src: WI-0003/Q-002]. It is now their own sentence, so the decision stands in their name rather
than in ours [src: ADR-0008].

**Nothing further was asked for.** They were offered option B — accept, and name what comes next —
with the escaped-pipe case, a maximum column width, reading a file by path and blockquoted tables
named as candidates. They chose A and said why: the escaped-pipe case has never arisen in their
own writing, and if it ever does it is a new job. So no follow-up item exists, and that is their
decision rather than an omission [src: EP-001/Q-006].

## What is not yet decided

- Whether a table written **without** its outer pipes should be recognised. ADR-0003 keeps
  ADR-0002's decision not to recognise it, from the stakeholder's "where it cannot tell, do
  nothing" rather than from anything they said about pipes, and both record that it is cheap to
  widen later [src: ADR-0003].
- How an escaped pipe (`\|`) inside a cell is measured and re-emitted. Routed to `plan` rather
  than to the stakeholder, because GitHub-flavoured markdown already answers it
  [src: WI-0001]. It stayed undecided through the whole engagement, and it was named to the
  stakeholder at the sign-off — as note 3, in the sharper form of a cell holding both an escaped
  pipe and a break tag — with an offer to record it as follow-up work. They declined the offer
  rather than the problem: *"I have never once written an escaped pipe in the same cell as a line
  break. If that last one ever bites me I will come back to you with it as a new job"*
  [src: EP-001/Q-006]. So it remains open by their decision, and unscheduled.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 8 | 2026-08-30T01:04:46Z | answer-questions | EP-001 | Added round 6: the stakeholder's acceptance of the engagement, verbatim — option A, no follow-up items — and the three things in it that outlive the closing: a cell that only mentions a break tag is exempt and that is acceptable, *"left"* is all *"top-left"* ever meant, and nothing further was asked for. The escaped-pipe bullet under what is not yet decided now records that they were shown it at the sign-off and chose not to hold the engagement for it |
| 7 | 2026-08-30T00:13:37Z | answer-questions | WI-0003 | Added round 5: the stakeholder's answers to `WI-0003/Q-001` and `WI-0003/Q-002`, verbatim — every spelling of `<br>` exempts a cell, a trailing backslash does not, and an exempt cell is still padded out to its column's width — and where the other three edges of the exemption went. Dropped the unsettled bullet listing those five edges: all five are now recorded in ADR-0008, so the list is no longer open rather than being answered differently |
| 6 | 2026-08-29T23:58:20Z | answer-questions | EP-001 | Added round 4: the stakeholder's answer to `EP-001/Q-005`, verbatim — the later sentence wins, a cell with a line break sits top-left whatever the marker says, and they authorise superseding what they said before. Round 2's paragraph is kept as they wrote it, with a note that its author has since narrowed it; the ADR-0005 pointer now names ADR-0007 as the current decision. The unsettled marker-reach bullet is replaced by the five edges of the exemption `WI-0003` must still ask about |
| 5 | 2026-08-29T23:51:02Z | answer-questions | EP-001 | Added round 3: the stakeholder's reply to the sign-off, verbatim — a cell with a line break sits top-left whatever the marker says, and their confirmation of the odd-remainder and display-width decisions. Added the unsettled reach of a marker over such a cell, pointing at `EP-001/Q-005`. Round 2's paragraphs are untouched: the sentence this one is in tension with is theirs, not a document defect |
| 4 | 2026-08-29T22:30:16Z | answer-questions | WI-0002 | Added the stakeholder's round-2 answer on WI-0002 (an odd centring remainder goes right; a marker places text in every content cell of its column) and pointed at ADR-0005. Dropped the centring-remainder and delimiter-colon entry from what is not yet decided: the first is now their answer, the second was already settled by ADR-0004 decision 1 |
| 3 | 2026-08-29T21:35:22Z | answer-questions | WI-0001 | Added the stakeholder's round-1 answers on WI-0001 (display width, indented tables, cell padding, delimiter row) and pointed the recognition rule at ADR-0003, which supersedes ADR-0002 |
| 2 | 2026-08-29T21:22:33Z | answer-questions | EP-001 | Replaced the three open unknowns with the stakeholder's answers to EP-001/Q-001, Q-002 and Q-003, and pointed at ADR-0001 and ADR-0002 |
| 1 | 2026-08-29T21:14:21Z | intake | EP-001 | First version, from the stakeholder's stated idea |
