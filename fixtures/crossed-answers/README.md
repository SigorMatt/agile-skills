# A conflict between two of the stakeholder's own answers

Every question here is wrong on purpose except two, and the two right ones matter as much as the
wrong ones. `scripts/check` runs `scripts/lint-answers` against this tree and asserts that the
set of finding codes equals `EXPECTED-CODES.txt` **exactly**, so the rule that stops firing and
the rule that starts firing on compliant work both fail the build.

The shape is iteration 3's, reduced (`meta/findings/FINDINGS.md` F-062,
`meta/adr/ADR-0008-cross-answer-consistency.md`). The stakeholder said, at refinement, *"the
marker decides everything — every row, every column, no exceptions"*; five turns later, as the
condition on a sign-off, *"a cell with a line break sits top-left, plain, whatever the marker
says."* Both are recorded. They cannot both hold.

| Question | What it is | Code |
|----------|-----------|------|
| `WI-0002/Q-001` | the first answer, with nothing prior to reconcile | — (must produce nothing) |
| `WI-0002/Q-002` | a second real answer, so a `Checked against:` list has something to wrap onto | — (must produce nothing) |
| `WI-0003/Q-001` | the later, contradicting answer, **handled correctly**: the conflict is declared and `WI-0003/Q-002` puts both to their author | — (must produce nothing) |
| `WI-0003/Q-002` | the escalation itself, still `open` — it quotes both answers by ID and asks which wins | — |
| `WI-0004/Q-001` | the same conflict, declared and then settled privately: *"Corrected the vision document to match the newer answer"* | `answer.conflict.unescalated` |
| `WI-0004/Q-002` | a check citing an answer this workspace does not have, on the wrapped second line of its declaration | `answer.cross-check.unresolved` |
| `WI-0004/Q-003` | an answer named with no verdict — "looked at it" | `answer.cross-check.no-verdict` |
| `WI-0004/Q-004` | a section that reads like a check and says nothing checkable | `answer.cross-check.malformed` |
| `EP-001/Q-005` | the sign-off consumed with no cross-answer check at all — the iteration-3 instance | `answer.cross-check.missing` |

## The delegation, and what was spent under it

The second half of the same protocol (F-082). A stakeholder answers one question with *"whatever
is easier for you"* and every later execution has a licence nothing bounds. A decision taken
under one records `**Under delegation:** <ANSWER-ID> — <category>`, and the ending puts every
answer so spent in front of the person who gave it.

| Where | What it is | Code |
|-------|-----------|------|
| `WI-0002/artifacts/refinement-qa.md` | the compliant delegation: it resolves, it names its category, and `EP-001/Q-005` surfaces it at the ending | — (must produce nothing, in either scope) |
| `WI-0003/artifacts/plan.md` | a licence traced back to an answer this workspace does not have — and written as a **nested** line inside its assumption bullet, which is where `plan.md` puts it | `answer.delegation.unresolved` |
| `WI-0004/artifacts/refinement-qa.md` Q1 | an answer ID and nothing else: the unbounded delegation, which is the finding's own shape | `answer.delegation.no-category`, and `answer.delegation.unsurfaced` at the ending |
| `WI-0004/artifacts/refinement-qa.md` Q2 | a delegation in prose, naming no answer at all — no route back to anyone | `answer.delegation.unnamed` |
| `WI-0004/artifacts/refinement-qa.md` Q3 | a delegation citing a request that does not exist | `answer.delegation.unresolved` |
| `WI-0005/artifacts/refinement-qa.md` | the same pair again in the engagement that ended at **E4**: one delegation named in `EP-002`'s `## Ending statement`, one not. At E4 there is nobody to address, so the account of the engagement is a document | `answer.delegation.unsurfaced` (at the ending) on the second only |
| `WI-0006/artifacts/plan.md` | a delegation spent in an engagement (`EP-003`) that has filed neither a sign-off nor an ending statement, and citing `R-001`, a request that **does** exist | — (a line on stdout, and no finding) |

`answer.delegation.unsurfaced` is **not** in `EXPECTED-CODES.txt`: it is the ending's rule and
fires only under `--context epic`, which is how `review-close` runs this gate. `scripts/check`
runs the fixture both ways and pins it to exactly **two** occurrences in the second — one per
place an engagement's account of itself can live — with a silent twin beside each: `EP-001`'s
sign-off names `WI-0002/Q-002`, `EP-002`'s ending statement names `WI-0003/Q-001`, and neither
may be reported. `EP-003` is the third branch and it is deliberately quiet: an ending with no ask
at all is `scripts/check-epic-signoff`'s to refuse, and two gates reporting one failure teaches a
reader to skim.

`WI-0003` is the control, and it is deliberately awkward in four ways that a real record is
awkward: `WI-0003/Q-002` names the two answers **only inside `## Options considered`**, because
putting the person's two statements side by side as the options is how a good escalation reads;
`WI-0003/Q-001`'s verdict word sits on the *second* line of its bullet, because a verdict with its
reason attached wraps; its `Checked against:` list wraps onto a second line, because a real one
does; and it ends with a closing sentence after the last bullet, because that is where a section's
summary goes. The last two are F-073, found by regression 4b — reading a bullet to the next bullet
swallowed the closing sentence and turned `compatible` into `conflicts`, and reading the
declaration as one line left six of nine named answers unresolved and unchecked. `WI-0004/Q-002`
carries the other side of the second one: its unresolvable ID sits on the **continuation** line,
so a linter that reads one line reports a clean check over a list it read a third of.

Set equality cannot see the control regressing — `WI-0003` would start emitting a code `WI-0004`
already emits — so `scripts/check` also pins two **counts**: `answer.conflict.unescalated` and
`answer.cross-check.no-verdict` must each fire exactly once. Both were confirmed to move under a
reverting mutation. `WI-0004/Q-001` completes the set from the other side: its `## Context` names
`WI-0002/Q-001`, and that must **not** count as having asked anybody — a record that mentions the
answer it contradicts is the private settlement, not the escalation.

Rule 3 (a claim sourced to a human answer, rewritten by the execution that overtook it) is not
here: it reads a **diff**, so its case is built as a throwaway git repository inside
`scripts/check` rather than as a tree on disk.

Do not "fix" anything here. To change what is covered, change the fixture *and*
`EXPECTED-CODES.txt` in the same commit, and say why in the commit message.
