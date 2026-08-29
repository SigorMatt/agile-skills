---
title: Lay out only tables the tool fully understands, and never change a table's punctuation
version: 2
status: superseded
updated: 2026-08-28T21:23:07Z
updated-by: plan
updated-for: WI-0003
superseded-by: docs/architecture/adr/ADR-0008-a-run-shares-an-indent-rather-than-repeating-one.md
---

# ADR-0003 — Lay out only tables the tool fully understands, and never change a table's punctuation

- **Status:** superseded
- **Date:** 2026-08-28
- **Decided by:** the stakeholder, answering `WI-0001/Q-001`, `WI-0001/Q-002` and
  `WI-0001/Q-003`; the recognition rule below derived from those answers by answer-questions
  (architect), for WI-0001
- **Supersedes:** —
- **Superseded by:** ADR-0008, for WI-0003

> **Read ADR-0008 instead.** Rule 2 below — every line of a run carrying a byte-identical prefix
> — was reversed by the stakeholder in `WI-0003/Q-001`, because it stopped mdtab recognising the
> bare right-aligned tables its own layout emits. ADR-0008 restates all four rules with rule 2
> replaced by a shared-prefix rule. Rules 1, 3 and 4, and the "never the punctuation" promise, are
> carried into ADR-0008 unchanged; this file is kept because it is what was believed, and decided,
> when WI-0001 shipped.

## Context

[src: ADR-0002] settled how wide a cell is. What was still undecided was which runs of lines the
tool is willing to touch at all, and what it may change when it touches one. `refine` filed three
questions on WI-0001 rather than guessing, and the stakeholder answered all three in one round.
Read together they are one policy, not three, which is why they are recorded in one ADR.

On a table whose rows disagree about how many cells they have:

> *"Leave it alone. A table with a row that doesn't match is a table I got wrong, and I want to
> see it still looking wrong so I go and fix it — not have the tool invent a third column or
> leave bits hanging off the end of a line. The tool's job is to tidy tables it understands, and
> if it doesn't understand one it should keep its hands off."* [src: WI-0001/Q-001]

On a pipe table written without outer `|` characters:

> *"Yes, that's still a table and it should line up. But whichever way I wrote it is the way it
> stays — if I didn't put the outer bars in, don't add them for me. I only want the spacing
> changed, never the punctuation."* [src: WI-0001/Q-002]

On a table indented inside a blockquote or a list item:

> *"Align them. I put tables under bullet points all the time and quote them in notes, and a
> table that's indented is still a table — it would be odd if those were the ones that stayed
> ragged. If a table is indented in some tangled way you can't make sense of, that's one you
> leave alone, same as any other table you don't understand."* [src: WI-0001/Q-003]

Two of those sentences generalise beyond the question that produced them — *"if it doesn't
understand one it should keep its hands off"* and *"same as any other table you don't
understand"* — and the stakeholder used the second to dispose of a case they had not been asked
about. That is an instruction to have **one** rule for unrecognised tables rather than a rule per
construct, and it settles a case nobody asked: a run whose rows disagree about their outer-pipe
style. Preserving each row's own punctuation there would keep the promise in `WI-0001/Q-002`
[src: WI-0001/Q-002] but break
the promise in WI-0001 AC2 that the pipes line up, producing a table that is neither tidied nor
left alone — the one outcome no answer asked for.

What none of this settles is the mechanics, and the mechanics have to be written down because
recognition is threaded through every layout decision and every test: "the same number of cells",
"the same style" and "the same indent" each need a rule a reader with a terminal can apply.
Deciding those is the architect's job under the delegation in [src: ADR-0001].

## Options considered

- **A — Recognise conservatively: lay out a run only when every row agrees about its cell count,
  its outer-pipe style and its leading prefix; otherwise reproduce the run byte-for-byte.**
  Cost: three checks before layout, and a class of real tables — a blockquote whose rows are
  indented unevenly, say — comes back untouched with nothing said about why. Risk: low. The
  failure mode is doing nothing, which is exactly the failure mode the stakeholder asked for in
  all three answers.
- **B — Recognise conservatively on cell count, but repair the other two: normalise outer pipes
  and re-indent to the shallowest prefix.** Cost: about the same to build. Risk: it changes
  punctuation and leading whitespace on lines the stakeholder did not ask to have changed, which
  `WI-0001/Q-002` rules out in terms (*"never the punctuation"*) [src: WI-0001/Q-002].
- **C — Lay out whatever can be parsed, per row: keep each row's own outer pipes and its own
  indent, pad the cells that exist.** Cost: no recognition checks at all, so it is the smallest.
  Risk: the output of a mixed-style or unevenly-indented table has its pipes at different display
  columns per row, so WI-0001 AC2 fails on a table the tool nevertheless rewrote. It also
  contradicts `WI-0001/Q-001` [src: WI-0001/Q-001], since a short row would simply be padded
  to fewer columns.
- **D — Only lay out tables at column one with outer pipes on every row** (the narrow reading).
  Cost: nothing. Risk: contradicts `Q-002` and `Q-003` directly, both of which asked for the
  wider forms to be aligned.

## Decision

A run of consecutive lines is **laid out** only when all four of these hold; otherwise every line
of the run is reproduced byte-for-byte, and nothing is written on stderr [src: EP-001].

1. **It is a table.** Its second line is a delimiter row, per WI-0001 AC7, judged after the
   prefix in rule 2 has been stripped.
2. **Every line carries a byte-identical prefix.** A line's prefix is its maximal leading run of
   characters drawn from space, tab and `>`. All lines of the run must have the same prefix, byte
   for byte. The prefix is stripped before the table is parsed and laid out, and reproduced
   unchanged at the start of every output line of the table. This is what lays out a table inside
   a blockquote (`> `) or under a list item (`  `), and what leaves a "tangled" indent —
   `>   |…|` beside `> |…|`, or a nested quote whose rows carry different depths — alone.
3. **Every row has the same number of cells.** Cells are the fields left by splitting a row on
   its unescaped `|` characters (`\|` is not a separator, WI-0001 AC10) and discarding the empty
   field produced by a leading pipe and the one produced by a trailing pipe. The header row, the
   delimiter row and every body row must agree. A row with one cell too many or too few makes the
   whole run unrecognised.
4. **Every row has the same outer-pipe style.** A row *has a leading pipe* when its first
   character after the prefix is `|`, and *has a trailing pipe* when its last non-whitespace
   character is an unescaped `|`. Every row of the run must agree on both. Both styles are
   recognised — `| a | b |` and `a | b` are equally tables — and a mixed run is not.

When a run is laid out, the tool **changes spaces and nothing else**. It never adds a `|` to a
row that lacked one, never removes one from a row that had one, never alters the prefix, and
never touches the characters of a cell [src: WI-0001 AC11]. A table written without outer pipes
comes back without outer pipes.

The four rules are stated as recognition rules rather than as repairs so that the tool's whole
behaviour on anything it does not fully understand is a single sentence: it copies the bytes
through. That sentence is checkable by feeding a document in and diffing it, and it is what the
stakeholder asked for three times in three different words.

## Consequences

What becomes easy: the tool can never mangle a table. Every construct it does not model —
malformed rows, mixed punctuation, irregular indentation, and anything nobody has thought of yet
— falls into one branch with one behaviour, and the test for that branch is byte equality rather
than a bespoke expectation per construct. Tables in blockquotes and under list items, which are a
large fraction of the stakeholder's tables [src: WI-0001/Q-003], are aligned without any special
case beyond "strip the prefix, lay out, put it back".

What becomes hard: silence is the only diagnostic. A user whose table came back ragged has no way
to learn which of the four rules it failed, because the epic puts diagnostics out of scope
[src: EP-001] and `Q-001` confirmed the stakeholder prefers the ragged table as its own signal.
Rule 2 also means the tool's idea of an indent is textual rather than structural: it does not
know what a list item is, so a table under a list marker is aligned only when its own lines are
indented uniformly, and a continuation line indented to a different depth stops it being
recognised.

**Reversibility: high, in one direction.** Every rule here can be *relaxed* additively — teaching
the tool to lay out a mixed-style run, or to normalise prefixes — because doing so only moves
documents from the byte-for-byte branch into the laid-out branch, and no document that is aligned
today would change. Tightening is likewise cheap. What is not reversible without the
stakeholder's authorisation is the "never the punctuation" promise, which is an explicit answer
[src: WI-0001/Q-002] and which options B and C both breach.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-28T21:23:07Z | plan | WI-0003 | Superseded by ADR-0008. Rule 2 was reversed by the stakeholder in WI-0003/Q-001; status and a pointer added, and no rule text edited — the decision this file records is what was believed when WI-0001 shipped. Three bare `Q-00n` references qualified to `WI-0001/Q-00n` and given `[src:]` markers, which doc-header.md §4a requires of the next execution to touch a file |
| 1 | 2026-08-28T18:43:43Z | answer-questions | WI-0001 | First version, recording the stakeholder's answers to WI-0001/Q-001..Q-003 and the four recognition rules derived from them |
