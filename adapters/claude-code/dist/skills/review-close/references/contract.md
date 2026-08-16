# Contract — review-close v0.1.0

Rendered from `methodology/skills/review-close/skill.yaml`. This is the authoritative list of what this skill must read, must produce, and must not skip. Open it when you need the exact gate list or the exit criteria; the procedure in SKILL.md is the how.

- **Persona:** reviewer
- **Purpose:** Review the change and its record against the Definition of Done, then merge and close the item, or reject it with reasons.
- **Human interaction:** via-questions
- **Dispatched on statuses:** `in-review`
- **Item types:** `work-item`, `bug`
- **On success:** `done`
- **On unrecoverable failure:** `in-progress`

## Inputs — every one of these must actually be read

| path | required | why |
|------|----------|-----|
| `tracker/items/{{item.id}}/item.md` | yes | the criteria, their tick state, and the outcome to be recorded |
| `tracker/items/{{item.id}}/artifacts/verify-report.md` | yes | the evidence behind each tick, and the declared gaps |
| `tracker/items/{{item.id}}/artifacts/impl-report.md` | yes | declared deviations from the plan, which the review must judge |
| `tracker/items/{{item.id}}/artifacts/plan.md` | yes | the design the change is reviewed against |
| `tracker/items/{{item.id}}/journal.md` | yes | the Definition of Done includes the completeness of the record itself |
| `tracker/items/{{item.id}}/history.md` | yes | a gap in the chain means a status changed outside a skill |
| `the diff of {{item.branch}} against {{trunk}}` | yes | the review judges the change, not the description of it |
| `docs/architecture/adr/` | no | the change must not silently contradict a recorded decision |

## Outputs

| path | kind | when |
|------|------|------|
| `tracker/items/{{item.id}}/artifacts/review.md` | file | always |
| `tracker/items/{{item.id}}/item.md` | file | always |
| `merge of {{item.branch}} into {{trunk}}` | commit | on-success |
| `tracker/items/EP-###/item.md` | file | conditional |
| `tracker/items/{{item.id}}/journal.md` | append | always |
| `tracker/items/{{item.id}}/history.md` | append | always |

## Quality gates

Every gate below appears in the journal entry for every execution — including gates that were skipped, with the reason. A gate silently omitted is the failure the journal format exists to prevent.

| gate | enforcement | how it is checked | on failure |
|------|-------------|-------------------|------------|
| `definition-of-done` | hard | Walk spec/dor-dod.md section 3 criterion by criterion and record pass or fail for each with its evidence. A single overall verdict does not satisfy this gate. | stay |
| `verification-postdates-the-code` | hard | run `.claude/agile-skills/scripts/check-verify-freshness {{item.id}} {{item.branch}}`, expect exit-zero | verifying |
| `commits-reference-the-item` | hard | run `.claude/agile-skills/scripts/check-commit-refs {{item.id}} {{item.branch}}`, expect exit-zero | stay |
| `tests-pass-on-the-merge-result` | hard | run `{{commands.test}}`, expect exit-zero | stay |
| `workspace-valid` | hard | run `.claude/agile-skills/scripts/validate-workspace`, expect exit-zero | stay |
| `record-is-reconstructible` | hard | Answer, using only those sources - what was built and why, which decisions were made and by which skill, what questions arose and how they were resolved, what verification found. Any answer you cannot give is a defect in the record, not in the reader. | stay |

## Escalation

- **question:** File tracker/items/{{item.id}}/questions/Q-###.md addressed to architect when the change contradicts a recorded decision and it is unclear which should give way. Set the item to awaiting-answer with resume-to in-review and stop.
- **defect:** A defect in this item's own delivery sends it back to in-progress with reasons. A defect elsewhere, noticed during review, becomes a bug item.
- **impasse:** If the item cannot be merged for reasons outside the change itself, set it to blocked with what was tried.

## Exit criteria — all must be true before transitioning

- [ ] Every Definition of Done criterion is recorded as passed, or the item was rejected.
- [ ] review.md states what was examined, not only the verdict.
- [ ] The branch is merged into the trunk and the item is done with an outcome recorded.
- [ ] If this was the epic's last open child, the epic Definition of Done was applied and the epic closed or explicitly left open with the reason.
- [ ] The journal entry and the history row for this execution are written.

## Schemas this skill writes against

- Item and body schema — `.claude/agile-skills/spec/work-item.md`
- Journal and history formats — `.claude/agile-skills/spec/journal-and-history.md`
- Question protocol — `.claude/agile-skills/spec/question.md`
- Document headers and ADRs — `.claude/agile-skills/spec/doc-header.md`
- Definition of Ready and Done — `.claude/agile-skills/spec/dor-dod.md`
- IDs, statuses, transitions — `.claude/agile-skills/spec/ids-and-statuses.md`
- Workspace layout — `.claude/agile-skills/spec/workspace-layout.md`
