---
title: Architecture overview
version: 1
status: current
updated-by: plan
updated-for: WI-0001
updated: 2026-08-16T09:00:00Z
---

# Architecture overview

The tool reads no environment beyond `EXPENSES_STORE`. [src: src/store.py]

That citation names a file this workspace does not have, which is F-001's failure with a
decoration on it: the sentence looks sourced and is not.

`format_report` only ever renders rows it is handed, and nothing else in the system may write
to `tracker/board.md`.

The paragraph above is the shape the audit found — an absolute claim about a named identifier,
carrying no citation at all.

And a marker in a form the gate does not define: [src: WI-0001 ## Acceptance criteria]. Bare, so
it is still reported — but as a **warning**, because nothing was checked here and a bare marker
in no known form could as easily be prose naming a form as a typo in a citation (F-113). The
error above it, `src/store.py`, is the other half of the pair: a marker in a form the gate does
define, which it looked up and did not find.

`render_table` never writes outside a table, and the source for that would be written
`[src: ADR-0001]`. Shown, not made: a paragraph cannot source itself by describing what its
citation would look like, so this is unsourced too (F-113).

Every claim-provenance rule this workspace breaks is defined in the toolkit, and nothing here may
cite the toolkit by pointing at it [src: .claude/agile-skills/spec/doc-header.md]. That marker is
a real citation in a form the gate recognises and **refuses**: `.claude/` is one of the four
directories the record walk prunes, so the file is not part of the record, and whether it exists
is a fact about the machine this was written on rather than about the record (ADR-0013). It is an
ERROR and not a warning, because the gate knows exactly what is wrong and exactly what to write
instead.

The replacement form can be got wrong too, and this is the way that matters: no quoted words at
all [src: toolkit: doc-header.md §4a]. A toolkit citation carries every scrap of its evidence
inside the marker, so a body that names the form and quotes nothing is the appearance of a
citation — an ERROR, in the form's own words rather than as an unrecognised marker.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-16T09:00:00Z | plan | WI-0001 | First version |

## Change log

A second change log. The first one is the only one anything reads.
