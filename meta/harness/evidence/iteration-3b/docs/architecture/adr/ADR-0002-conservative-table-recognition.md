---
title: Conservative table recognition — strict pipe tables, everything else passes through
version: 2
status: superseded
superseded-by: docs/architecture/adr/ADR-0003-recognition-and-output-shape.md
updated: 2026-08-29T21:35:22Z
updated-by: answer-questions
updated-for: WI-0001
---

# ADR-0002 — Conservative table recognition — strict pipe tables, everything else passes through

- **Status:** superseded
- **Superseded by:** ADR-0003
- **Date:** 2026-08-29
- **Decided by:** answer-questions (architect), for EP-001
- **Supersedes:** —

> **This ADR is no longer the document to act on.** ADR-0003 replaces it. The stakeholder was
> asked about decision 2 — whether a table has to start at the left margin — and answered that
> tables indented under a list must be tidied [src: WI-0001/Q-002], which is the authorisation
> this document itself invited. ADR-0003 carries decisions 1 and 3 to 6 forward unchanged, amends
> 2 and 7, and adds the output shape. What is written below is what was believed on
> 2026-08-29 before the stakeholder answered, and it is kept for that reason.

## Context

Everything this tool does depends on where it draws the line between "a table I may reformat" and
"text I must copy". `intake` asked the stakeholder where that line falls (EP-001/Q-003) and, in
the same round, asked what else mattered that nobody had asked about (EP-001/Q-001). Both came
back, and between them they settle the shape of the rule.

On the dialect [src: EP-001/Q-003]:

> Ordinary pipe tables, the kind you showed — that is all I write. I have never written one of
> those grid tables in my life and I do not want the tool looking for them. Code blocks must be
> left completely alone; a fenced block full of pipes is not a table and touching it would be the
> worst thing this could do. Where it cannot tell, it should pass the text through and do nothing.

On conservatism generally [src: EP-001/Q-001]:

> Anything that is not a table comes out exactly as it went in, byte for byte — that is the part
> I care about most, and I will stop using it the first time it edits a paragraph. If a table is
> broken — a row with the wrong number of cells, a missing separator line — leave it alone rather
> than guess what I meant; I would much rather it did nothing than mangled something. And no
> trailing whitespace at the end of any line it writes: columns are as wide as the widest cell in
> them, with no maximum, but nothing hangs off the right-hand edge.

Three things in those answers are stated outright and are not ours to decide: no grid tables,
fenced code blocks untouched, and a malformed table left exactly as it is. Two are not stated,
and the stakeholder cannot be asked about them cheaply, so this ADR decides them from what they
did say.

1. **Are the outer pipes required?** `intake` offered a strict rule (option A, outer pipes
   mandatory) and a permissive one (option B, outer pipes optional). The stakeholder answered
   "the kind you showed", pointing at an example that carries a leading and a trailing pipe on
   every line, and added the tie-breaker: "where it cannot tell, it should pass the text through
   and do nothing". They did not address optionality directly.
2. **What does "no trailing whitespace at the end of any line it writes" mean for a passthrough
   line that already had trailing whitespace in the input?** Read literally and in isolation, it
   would have the tool strip that whitespace, which would contradict byte-for-byte passthrough —
   in the same answer, two sentences earlier.

## Options considered

On the outer pipes:

- **A —** Require a leading and a trailing pipe on every line of a table block. Cost: a table the
  stakeholder wrote without outer pipes comes back untouched, with nothing said about why. Risk:
  low — the failure is "did nothing", which is the failure they asked for twice.
- **B —** Accept tables whose outer pipes are absent, as GitHub does. Cost: a broader recognizer
  that must decide whether a line of prose containing a pipe, or a two-line fragment, is a table.
  Risk: higher, and asymmetric — every extra thing recognised is another way to edit something
  that was not a table, which is the one failure mode the stakeholder said would make them stop
  using the tool.

On the trailing whitespace:

- **C —** "Any line it writes" means every output line, so trailing whitespace is stripped from
  passthrough lines too. Cost: contradicts "exactly as it went in, byte for byte", which the same
  answer names as the part they care about most. Risk: high — it makes the tool a whitespace
  formatter for the whole document, which is what "not a markdown formatter" rules out.
- **D —** "Any line it writes" means the table lines the tool composes; a line it copies is
  copied, not written. Cost: output can still contain trailing whitespace, on non-table lines
  that arrived with it. Risk: low, and the residue is visibly the input's, not ours.

## Decision

The filter recognises exactly one thing: a **GitHub-flavoured pipe table with outer pipes**,
outside a fenced code block, whose rows are internally consistent. Everything else is copied.

1. **Fences first.** While reading, the filter tracks fenced code blocks opened and closed by
   ``` or ~~~ . Lines inside a fence are copied unchanged and are never candidates for a table,
   whatever they look like.
2. **A candidate block** is two or more contiguous lines, each of which begins with `|` and ends
   with `|` once trailing whitespace is disregarded. A line missing either outer pipe ends the
   candidate block, and a table written without outer pipes is not recognised.
3. **A candidate block is a table** only if its second line is a delimiter row — every cell
   matching optional colon, one or more hyphens, optional colon — and the first line, the
   delimiter row and every subsequent line all have the same number of cells.
4. **A candidate block that is not a table is copied byte for byte**, as a whole. That covers a
   missing delimiter row, a delimiter row with the wrong number of cells, and a body row with the
   wrong number of cells. The filter does not repair, pad out, or truncate a ragged row, and it
   does not reformat the rows that were well-formed while leaving the broken one alone: the unit
   that is reformatted or left alone is the whole block.
5. **No other table syntax is recognised.** Grid tables, rst simple tables, and anything drawn
   with `+---+` borders are ordinary text and are copied. The filter does not look for them.
6. **Lines the filter composes carry no trailing whitespace.** A line it copies is copied
   verbatim, including any trailing whitespace it arrived with, and including its line ending.
7. **A column's width is the width of the widest cell in it**, header and delimiter row included,
   with no maximum. Nothing is truncated and no line is wrapped.

## Consequences

Easy: the recogniser is a small state machine that can be read in one sitting, and every case it
declines to handle degrades to copying, so the worst outcome of a bug in it is that a table is
not tidied. The rules above are directly testable — each of 1 to 7 is a test with an input file
and an expected output file.

Hard: the stakeholder gets no feedback when a table is skipped. If they write a table without
outer pipes, or mistype a delimiter row, the tool silently does nothing and they must notice the
absence of a change. They accepted that trade explicitly ("I would much rather it did nothing
than mangled something"), but it is the cost, and if it becomes annoying it will be reported as
"it ignored my table" rather than as a bug in recognition.

Also hard: rule 4 means one bad row suppresses the whole table, including its good rows. That is
the strictest reading of "leave it alone rather than guess what I meant", and it is deliberate —
reformatting some rows of a table and not others would produce exactly the mangled-looking output
they said they did not want.

Reversibility: **high in one direction, low in the other.** Widening the recogniser later —
optional outer pipes, or reformatting the well-formed rows of a ragged table — is additive: it
only changes the behaviour of input that is currently passed through, and every existing test
keeps its meaning. Narrowing it again after documents have been reformatted under a wider rule
would be the expensive direction. That asymmetry is why the strict rule is the one to start with,
and it is why decisions 2 and 4 are safe for us to take rather than escalate.

`refine` and `plan` may put decisions 2 and 4 back to the stakeholder if they turn out to matter
more than this ADR assumes. They are recorded here as decisions, not as facts about what the
stakeholder said.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-29T21:35:22Z | answer-questions | WI-0001 | Superseded by ADR-0003 after the stakeholder's answers to WI-0001/Q-001 to Q-004; no decision in this document was edited |
| 1 | 2026-08-29T21:22:16Z | answer-questions | EP-001 | First version, from the stakeholder's answers to EP-001/Q-001 and EP-001/Q-003 |
