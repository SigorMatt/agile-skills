# Contract — implement v0.4.0

Rendered from `methodology/skills/implement/skill.yaml`. This is the authoritative list of what this skill must read, must produce, and must not skip. Open it when you need the exact gate list or the exit criteria; the procedure in SKILL.md is the how.

- **Persona:** developer
- **Purpose:** Execute the recorded plan on a branch, with tests, and report which evidence satisfies each acceptance criterion.
- **Human interaction:** via-questions
- **Dispatched on statuses:** `planned`, `in-progress`
- **Item types:** `work-item`, `bug`
- **On success:** `verifying`
- **On unrecoverable failure:** `blocked`

## Inputs — every one of these must actually be read

| path | required | why |
|------|----------|-----|
| `tracker/items/{{item.id}}/item.md` | yes | the acceptance criteria define what to build and when to stop |
| `tracker/items/{{item.id}}/artifacts/plan.md` | yes | the design decisions this skill executes and must not re-litigate, and the invalidation set, deliverable-documents and binding-adrs that bound what it may write under docs/ |
| `tracker/items/{{item.id}}/history.md` | yes | distinguishes a fresh start from resuming a branch, and carries any send-back reason |
| `tracker/items/{{item.id}}/questions/` | no | an answered question changes the plan, and the answer is in the artifacts it updated |
| `docs/architecture/adr/` | no | constraints the plan assumes but does not restate, and the decisions listed as binding-adrs that verify will judge this change against |
| `every document named in the plan's invalidation set or deliverable-documents` | no | the sentences this change makes false, and the documents it was asked to produce; this is the only part of docs/ this skill may write |
| `tracker/project.yaml` | yes | the branch prefix, the commit subject convention, and the commands the gates run |

## Outputs

| path | kind | when |
|------|------|------|
| `branch {{item.branch}}` | branch | always |
| `commits on {{item.branch}} referencing {{item.id}}` | commit | always |
| `tracker/items/{{item.id}}/artifacts/impl-report.md` | file | always |
| `the documents named in the plan's invalidation set or deliverable-documents, each with a version bump and a change-log row` | file | conditional |
| `a disposition on every entry of the plan's invalidation set, in tracker/items/{{item.id}}/artifacts/plan.md` | file | always |
| `tracker/items/{{item.id}}/journal.md` | append | always |
| `tracker/items/{{item.id}}/history.md` | append | always |

## Quality gates

Every gate below appears in the journal entry for every execution — including gates that were skipped, with the reason. A gate silently omitted is the failure the journal format exists to prevent.

| gate | enforcement | how it is checked | on failure |
|------|-------------|-------------------|------------|
| `tests-pass` | hard | run `{{commands.test}}`, expect exit-zero | stay |
| `lint-clean` | hard | run `{{commands.lint}}`, expect exit-zero | stay |
| `workspace-valid` | hard | run `.claude/agile-skills/scripts/validate-workspace`, expect exit-zero | stay |
| `every-criterion-has-a-test` | hard | For each AC, name the test function or the exact command and its expected output. An AC demonstrated only by reading the code fails this gate. | stay |
| `commits-reference-the-item` | hard | run `.claude/agile-skills/scripts/check-commit-refs {{item.id}} {{item.branch}}`, expect exit-zero | stay |
| `no-unplanned-scope` | advisory | Read the diff. Every hunk must trace to an AC or to a plan step. Anything else is either a separate item or must be removed. | stay |
| `cross-answer-consistency` | hard | run `.claude/agile-skills/scripts/lint-answers --changed-since {{trunk}}`, expect exit-zero | stay |
| `claims-are-sourced` | hard | run `.claude/agile-skills/scripts/lint-claims --changed-since {{trunk}} --plan-documents {{item.id}}`, expect exit-zero | stay |
| `document-writes-are-declared` | hard | List every path under docs/ in the branch diff. Each must appear in the plan's invalidation set or in deliverable-documents; a document you had to change that appears in neither is added to the set as a new entry before you write it, never written silently. Then read the set - every entry carries a disposition of to-update, verified-still-true, owned-by-ending or question-filed:<ITEM>/Q-###, and no entry disposed owned-by-ending was edited. An engagement-state section is not yours at any disposition. | stay |

## Escalation

- **question:** File tracker/items/{{item.id}}/questions/Q-###.md addressed to architect, set the item to awaiting-answer with resume-to recorded, and stop. Never ask the human directly and never proceed on a guess.
- **defect:** If you find a defect in behaviour delivered by another item, file a bug item with reproduction steps and found-in, and continue with this item.
- **impasse:** If the plan cannot be executed and no question would unblock it, set the item to blocked with the approaches tried and why each failed.

## Exit criteria — all must be true before transitioning

- [ ] No sentence in docs/ that cites one of the stakeholder's answers was rewritten because a later answer of theirs overtook it; that is a question, filed, not an edit (ADR-0008).
- [ ] Every acceptance criterion has code and a test or reproducible command that exercises it.
- [ ] All hard gates passed on the branch head, not on an earlier state.
- [ ] Every entry in the plan's invalidation set carries a disposition, and every entry disposed to-update was updated with a version bump and a change-log row (spec/dor-dod.md D7).
- [ ] Nothing under docs/ was written that the plan's invalidation set or deliverable-documents does not name; a document falsified mid-change was added to the set as an entry and then repaired (spec/doc-header.md section 5).
- [ ] No engagement-state section was written. An entry whose subject is one is disposed owned-by-ending and left alone; the ending owns it (spec/doc-header.md section 4a).
- [ ] impl-report.md maps each acceptance criterion to its evidence and lists any deviation from the plan.
- [ ] Every commit on the branch references the item ID.
- [ ] The journal entry and the history row for this execution are written.

## Schemas this skill writes against

- Item and body schema — `.claude/agile-skills/spec/work-item.md`
- Journal and history formats — `.claude/agile-skills/spec/journal-and-history.md`
- Question protocol — `.claude/agile-skills/spec/question.md`
- Document headers and ADRs — `.claude/agile-skills/spec/doc-header.md`
- Definition of Ready and Done — `.claude/agile-skills/spec/dor-dod.md`
- IDs, statuses, transitions — `.claude/agile-skills/spec/ids-and-statuses.md`
- Workspace layout — `.claude/agile-skills/spec/workspace-layout.md`
