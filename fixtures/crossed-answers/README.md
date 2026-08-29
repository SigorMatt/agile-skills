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

`WI-0003` is the control, and it is deliberately awkward in two ways that a real record is
awkward: `WI-0003/Q-002` names the two answers **only inside `## Options considered`**, because
putting the person's two statements side by side as the options is how a good escalation reads;
and `WI-0003/Q-001`'s verdict word sits on the *second* line of its bullet, because a verdict with
its reason attached wraps.

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
