---
title: A run shares an indent rather than repeating one
version: 1
status: current
updated: 2026-08-28T21:23:07Z
updated-by: plan
updated-for: WI-0003
---

# ADR-0008 — A run shares an indent rather than repeating one

- **Status:** accepted
- **Date:** 2026-08-28
- **Decided by:** the stakeholder, answering `WI-0003/Q-001` with option A after being shown the
  documents it changes; the mechanics below derived from that answer and from
  [src: WI-0003 AC1] by plan (architect), for WI-0003
- **Supersedes:** ADR-0003

## Context

[src: ADR-0003] settled which runs of lines mdtab is willing to touch, in four rules, and its
rule 2 required every line of a run to carry a **byte-identical** prefix of spaces, tabs and `>`.
That rule was written when the only thing that could put a space at the start of a table line was
the author.

[src: WI-0002] changed that. Honouring a `---:` or `:---:` marker in the first column of a table
written without outer `|` bars puts the padding at the very start of the line, so mdtab's own
output has leading spaces on its header and body rows and none on its delimiter row
[src: WI-0002 AC10]. Rule 2 then refuses the run, and the tool stops recognising a table it laid
out itself. The bytes are still a fixed point [src: WI-0001 AC6], so the fault is invisible until
someone edits a cell and re-runs the tool — which is the commonest reason to run it.

The stakeholder was shown the fault, the fix, and the fix's price, and chose the fix:

> *"Yes, tidy it. Spaces at the front of a line are part of how the table sits, not something I
> put there on purpose, and a table with two spaces on one row and none on the next isn't tangled
> — it's just untidy, which is the exact thing I wanted the tool for. Tabs and the quote marks
> having to match exactly sounds right to me, and where the fix goes in the code is yours to
> decide."* [src: WI-0003/Q-001]

That reverses part of what rule 2 says, and [src: .claude/agile-skills/spec/doc-header.md] §4 is
explicit that an ADR is never edited to change its decision — it is superseded by a new one that
cites it. So this record restates all four rules rather than amending one in place. **Rules 1, 3
and 4 are reproduced from ADR-0003 unchanged in substance and are not reopened here**; only
rule 2 is decided anew.

The other thing the stakeholder settled is what a tab means. Nothing in this project defines how
wide one is — [src: ADR-0002] fixes a display width for every character mdtab measures and a tab
is not among them, because its width depends on where it lands and on the reader's settings. A
rule that let a tab and some spaces be "the same indentation" would have to invent that width.

## Options considered

- **A — The shared prefix is the longest common prefix, and every line's remainder past it must
  be spaces.** Cost: one new function and a two-line change to the recognition rule. Risk: a bare
  run whose rows carry different numbers of leading spaces starts being laid out where it is
  left alone today, and comes back at the shallowest indent in the run. That is a real behaviour
  change on documents that exist, and it is the one the stakeholder was shown and accepted
  [src: WI-0003/Q-001; src: WI-0003 AC5].
- **B — Re-recognise only a run whose leading spaces are already exactly the padding the markers
  call for.** Cost: about the same to build, plus a dependency from the recognition rule onto the
  layout arithmetic, which today runs strictly after it. Risk: it fixes the fault only until the
  table is edited. Change a word in the first column — the commonest reason to re-run the tool —
  and the padding no longer matches, the run stops being recognised, and it is ragged again. It
  buys a narrower rule at the cost of the fault returning exactly when it would be noticed.
- **C — Leave rule 2 alone and accept that mdtab will not re-tidy a bare table whose first column
  is right- or centre-aligned.** Cost: nothing to build. Risk: it contradicts the stakeholder's
  answer to [src: WI-0002/Q-002] — *"if the tool then can't recognise a table it laid out itself,
  that's a fault in the tool and I'd want it sorted rather than worked around"* — and leaves the
  tool producing output it will not accept back.
- **D — Treat a tab as some number of spaces so that tab- and space-indented lines can share a
  prefix.** Cost: small. Risk: it requires inventing a tab width that neither [src: ADR-0002] nor
  the stakeholder has ever supplied, and it would change tab-indented documents that are left
  alone today. Rejected in terms by [src: WI-0003/Q-001].

**A**, which is what the stakeholder chose.

## Decision

A run of consecutive lines is **laid out** only when all four of these hold; otherwise every line
of the run is reproduced byte-for-byte, and nothing is written on stderr [src: EP-001].

1. **It is a table.** Its second line is a delimiter row, per [src: WI-0001 AC7], judged after the
   shared prefix in rule 2 has been stripped. *(Unchanged from ADR-0003.)*

2. **The run shares an indent.** A line's prefix is its maximal leading run of characters drawn
   from space, tab and `>`. The run's **shared prefix** is the longest common prefix, byte for
   byte, of its lines' prefixes. The run is recognised only when, for every line, the part of that
   line's prefix which follows the shared prefix consists of space characters and nothing else.
   The **shared** prefix — not each line's own — is stripped before the run is parsed and
   reproduced unchanged at the start of every output line. Every space past it belongs to the row
   and therefore to that row's first cell, and is trimmed with the rest of that cell's leading
   spaces [src: WI-0001 AC11].

   So a run whose lines differ only in how many spaces they carry is a table, and comes back at
   the shared prefix; a run whose lines differ by a tab or by a `>` is not, exactly as before
   [src: WI-0003 AC5; src: WI-0003 AC6]. *(This is the rule that changed. ADR-0003 required the
   whole prefix to be byte-identical.)*

3. **Every row has the same number of cells.** Cells are the fields left by splitting a row on
   its unescaped `|` characters (`\|` is not a separator, [src: WI-0001 AC10]) and discarding the
   empty field produced by a leading pipe and the one produced by a trailing pipe. The header row,
   the delimiter row and every body row must agree. *(Unchanged from ADR-0003.)*

4. **Every row has the same outer-pipe style.** A row *has a leading pipe* when its first
   character after the shared prefix is `|`, and *has a trailing pipe* when its last non-whitespace
   character is an unescaped `|`. Every row of the run must agree on both. Both styles are
   recognised — `| a | b |` and `a | b` are equally tables — and a mixed run is not.
   *(Unchanged from ADR-0003 apart from "shared prefix" replacing "prefix".)*

When a run is laid out, the tool **changes spaces and nothing else**. It never adds a `|` to a row
that lacked one, never removes one from a row that had one, and never touches the characters of a
cell [src: WI-0001 AC11]. ADR-0003 also said "never alters the prefix"; that sentence is now
narrower and is stated here as it actually holds: the shared prefix is reproduced unchanged, and
spaces past it are cell padding like any other and are re-laid-out. A table written without outer
pipes still comes back without outer pipes [src: WI-0001/Q-002].

The rules are stated as recognition rules rather than as repairs, and rule 2's relaxation does not
change that: a run mdtab does not fully understand still falls into a single branch whose whole
behaviour is "copy the bytes through" [src: mdtab/table.py].

## Consequences

What becomes easy: mdtab recognises its own output again in every case, so a document can be
tidied, edited and tidied again without a class of table quietly falling out of the set the tool
will touch. That property is what [src: docs/architecture/overview.md] recorded as lost when
WI-0002 shipped, and this restores it. The rules stay four, the failure branch stays one, and
nothing about layout changes.

What becomes hard: mdtab's idea of an indent is now a property of a **run**, not of a line, so
reading one line no longer tells you what will be stripped from it. Anything that wants to know a
table's indentation must ask for the run's shared prefix rather than compute a line's prefix, and
the two functions must not be confused. This is the first rule in the project that cannot be
decided from a single line.

What changes for documents that exist: a table written without outer `|` bars whose rows carry
different numbers of leading spaces is laid out where today it is left alone, and comes back at
the shallowest indent in the run. This is a real change to documents nobody has asked to have
changed, it is the price of the rest, and it was put to the stakeholder in those words before it
was chosen [src: WI-0003/Q-001]. Tables written **with** outer bars are unaffected, and not by
luck: if every row starts with `|` after the shared prefix then their prefixes were already equal,
and if one row has extra spaces before its `|` then that row has no leading pipe while its
neighbours do, so rule 4 refuses the run for that reason instead [src: WI-0003 AC7]. All 33
fixture documents the project ships produce byte-identical output before and after
[src: WI-0003 AC8].

**Reversibility: high, and in both directions.** Tightening rule 2 back to byte-identical prefixes
is a one-line change to one function and would move the affected documents back into the
byte-for-byte branch; no other rule and no layout code depends on which prefix was chosen.
Relaxing further — accepting a tab where others have spaces, say — remains additive in the sense
ADR-0003 described, and remains a decision for the stakeholder rather than for an architect,
because it changes which of their documents the tool touches. What is still not reversible without
their authorisation is the "never the punctuation" promise [src: WI-0001/Q-002], which this
decision does not touch.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-28T21:23:07Z | plan | WI-0003 | First version, superseding ADR-0003. Rule 2 becomes a shared-prefix rule so that mdtab recognises the bare right-aligned tables it now emits; rules 1, 3 and 4 are reproduced unchanged. Decided by the stakeholder in WI-0003/Q-001 |
