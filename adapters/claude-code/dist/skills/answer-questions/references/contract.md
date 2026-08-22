# Contract — answer-questions v0.1.2

Rendered from `methodology/skills/answer-questions/skill.yaml`. This is the authoritative list of what this skill must read, must produce, and must not skip. Open it when you need the exact gate list or the exit criteria; the procedure in SKILL.md is the how.

- **Persona:** architect
- **Purpose:** Answer downstream skills' open questions from the record, propagate each answer into the authoritative artifacts, and escalate only when required.
- **Human interaction:** direct
- **Dispatched on statuses:** `awaiting-answer`
- **Item types:** `work-item`, `bug`, `epic`
- **On success:** no status transition of its own
- **On unrecoverable failure:** `blocked`

## Inputs — every one of these must actually be read

| path | required | why |
|------|----------|-----|
| `tracker/items/{{item.id}}/questions/` | yes | the questions to triage, with the asker's context, options and recommendation |
| `tracker/items/{{item.id}}/item.md` | yes | the acceptance criteria an answer may have to amend |
| `tracker/items/{{item.id}}/artifacts/plan.md` | no | most answers land here, and an answer that does not reach an artifact has not been given |
| `tracker/items/{{item.id}}/history.md` | yes | carries the resume-to status the item must be returned to |
| `docs/architecture/adr/` | yes | an answer that contradicts a recorded decision is an escalation, not an answer |
| `docs/product/` | no | intent recorded at intake or refinement often already answers the question |
| `tracker/items/*/artifacts/refinement-qa.md` | no | the human may have already answered this during refinement |

## Outputs

| path | kind | when |
|------|------|------|
| `tracker/items/{{item.id}}/questions/Q-###.md` | file | always |
| `tracker/items/{{item.id}}/artifacts/plan.md` | file | conditional |
| `tracker/items/{{item.id}}/item.md` | file | always |
| `docs/architecture/adr/ADR-####-{{item.id}}.md` | file | conditional |
| `a commit of the workspace files this execution wrote` | commit | on-success |
| `tracker/items/{{item.id}}/journal.md` | append | always |
| `tracker/items/{{item.id}}/history.md` | append | on-success |

## Quality gates

Every gate below appears in the journal entry for every execution — including gates that were skipped, with the reason. A gate silently omitted is the failure the journal format exists to prevent.

| gate | enforcement | how it is checked | on failure |
|------|-------------|-------------------|------------|
| `answer-is-propagated` | hard | For each question answered, open each file named in its Consequences section and confirm the change is there. A Consequences section naming no file fails this gate. | stay |
| `answered-from-the-record` | hard | For each answer, cite the document, ADR, or Q&A entry it follows from - or state explicitly that the record was silent and record the new decision as an ADR. | stay |
| `escalation-is-justified` | hard | For each question re-addressed to human, name which condition in spec/question.md section 4 applies. Effort is not a condition. | stay |
| `workspace-valid` | hard | run `.claude/agile-skills/scripts/validate-workspace`, expect exit-zero | stay |
| `item-resumed-correctly` | hard | Compare the new history row's target status with the resume-to value on the row that suspended the item. They must match. | stay |

## Escalation

- **question:** When the record cannot settle it, re-address the question to human, keep it open, state which escalation condition applies, and stop the loop rather than guessing.
- **defect:** If a question reveals that delivered behaviour is wrong, file a bug item; do not fix it inside the answer.
- **impasse:** If the human is unavailable and the question is blocking, leave the item at awaiting-answer and report it. An unanswerable question is not a reason to unblock the item.

## Exit criteria — all must be true before transitioning

- [ ] Every question this execution handled is either answered with consequences, or addressed to the human with the condition stated.
- [ ] Every file named in a Consequences section actually contains the change.
- [ ] Items whose blocking questions are all resolved are returned to their recorded resume-to status.
- [ ] Any new decision is recorded as an ADR, cited from the question.
- [ ] The journal entry and the history row for this execution are written.

## Schemas this skill writes against

- Item and body schema — `.claude/agile-skills/spec/work-item.md`
- Journal and history formats — `.claude/agile-skills/spec/journal-and-history.md`
- Question protocol — `.claude/agile-skills/spec/question.md`
- Document headers and ADRs — `.claude/agile-skills/spec/doc-header.md`
- Definition of Ready and Done — `.claude/agile-skills/spec/dor-dod.md`
- IDs, statuses, transitions — `.claude/agile-skills/spec/ids-and-statuses.md`
- Workspace layout — `.claude/agile-skills/spec/workspace-layout.md`
