# The document obligations, both ways

`ADR-0010`'s enforcement table numbers twenty obligations and marks twelve `[auto]`. Eight of
those had no implementation and stood in six skill contracts as `manual_check` — an instruction
where a gate was claimed. `scripts/lint-documents` decides them, and this fixture is what proves
each rule can fail **and** can be passed by work a person would actually produce.

Two workspaces, and both directions matter:

- **`wrong/`** — every artifact is wrong on purpose. `scripts/check` runs the five workspace-only
  rules over it and asserts that the set of emitted codes equals `EXPECTED-CODES.txt` **exactly**,
  so a rule that stops firing fails the build and so does a rule that starts firing somewhere new.
- **`right/`** — the same shapes, correct. Every rule must report **nothing** over it. A rule
  nobody can satisfy is not a rule; the must-fail half alone would let one ship.

The three rules that read a **diff** — `document-writes-are-declared`,
`engagement-state-is-left-to-the-ending` and `propagated-claims-carry-their-obligation` — are not
here. A diff is not a tree, so their cases are built as throwaway git repositories inside
`scripts/check`, the way `lint-answers`' rule 3 and the claims window already are.

## What each item in `wrong/` is wrong about

| Item | The defect | Codes |
|------|-----------|-------|
| `WI-0001` | a plan whose `kind` and `disposition` are prose, with no `## Binding ADRs` at all, and no verification report to dispose anything | `document.kind.unknown`, `document.disposition.unknown`, `document.binding-adrs.missing`, `document.verify.section.missing`, `document.adr.section.missing` |
| `WI-0002` | the plan is well formed — an **open** disposition is legal at `planned` and this item is the control for that — and the verification decided nothing: a bare `conforms`, a row that records a reading instead of a verdict, a verdict for an ADR the plan does not name, a row naming no ADR, an entry with no row, and a binding ADR with no row at all | `document.disposition.open`, `document.verify.row.missing`, `document.adr.verdict.unsupported`, `document.adr.verdict.unknown`, `document.adr.verdict.missing`, `document.adr.row.unplanned` (a **warning** — recording an ADR the plan missed is the honest move; it is evidence the plan's list was incomplete, which is D13's read, not this gate's refusal), `document.adr.row.unreadable` |
| `WI-0003` | `## Binding ADRs` says *"the usual ones"* — a list naming nothing a reader can resolve | `document.binding-adrs.unreadable` |
| `WI-0004` | `## Binding ADRs` is present and says nothing. Present-and-silent and absent are different defects and this fixture holds both, because a section that answers nothing is not an answer | `document.binding-adrs.empty` |
| `EP-001` | an ending whose `review.md` has no `## Sections restated at the ending` | `document.review.section.missing` |
| `EP-002` | an ending that restated the section it noticed and not the other one — F-093's shape, one document further on | `document.engagement-state.not-restated` |

And in `wrong/docs/`: `product/vision.md` carries **two** `## Engagement state` sections (the
convention is one per document, which is what makes the workspace's set enumerable at all);
`architecture/overview.md` opens one and puts nothing in it; `process/ways-of-working.md` has
none, which is what `--document` is pointed at to produce `document.engagement-state.absent`.

## What this fixture deliberately does not cover

**ADR-0010's obligation 10** — whether a sentence that *is* an engagement-state claim was written
**into** a section rather than left loose in the body. It has no mechanical half, everything else
about `## Engagement state` rests on it, and F-093's own sentence was written loose.
`wrong/docs/process/ways-of-working.md` contains exactly such a loose sentence and **no rule here
fires on it** — that absence is the point, and it is why `engagement-state-is-delimited` prints
what it cannot see on every run.

Do not "fix" anything here. To change what is covered, change the fixture *and*
`EXPECTED-CODES.txt` in the same commit, and say why in the commit message.
