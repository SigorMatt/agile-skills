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
| `WI-0003/Q-001` | the later, contradicting answer, **handled correctly**: the conflict is declared and `WI-0003/Q-002` puts both to their author | — (must produce nothing) |
| `WI-0003/Q-002` | the escalation itself, still `open` — it quotes both answers by ID and asks which wins | — |
| `WI-0004/Q-001` | the same conflict, declared and then settled privately: *"Corrected the vision document to match the newer answer"* | `answer.conflict.unescalated` |
| `WI-0004/Q-002` | a check citing an answer this workspace does not have | `answer.cross-check.unresolved` |
| `WI-0004/Q-003` | an answer named with no verdict — "looked at it" | `answer.cross-check.no-verdict` |
| `WI-0004/Q-004` | a section that reads like a check and says nothing checkable | `answer.cross-check.malformed` |
| `EP-001/Q-005` | the sign-off consumed with no cross-answer check at all — the iteration-3 instance | `answer.cross-check.missing` |

`WI-0003` is the control. If the escalation search breaks, `WI-0003/Q-001` starts producing
`answer.conflict.unescalated`, an extra code appears, and the assertion fails — which is why the
compliant case lives in the must-fail fixture rather than beside it.

Rule 3 (a claim sourced to a human answer, rewritten by the execution that overtook it) is not
here: it reads a **diff**, so its case is built as a throwaway git repository inside
`scripts/check` rather than as a tree on disk.

Do not "fix" anything here. To change what is covered, change the fixture *and*
`EXPECTED-CODES.txt` in the same commit, and say why in the commit message.
