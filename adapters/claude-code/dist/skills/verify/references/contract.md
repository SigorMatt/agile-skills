# Contract — verify v0.2.0

Rendered from `methodology/skills/verify/skill.yaml`. This is the authoritative list of what this skill must read, must produce, and must not skip. Open it when you need the exact gate list or the exit criteria; the procedure in SKILL.md is the how.

- **Persona:** qa-engineer
- **Purpose:** Independently decide whether an item meets its acceptance criteria, with evidence, and file bugs for what is wrong.
- **Human interaction:** via-questions
- **Dispatched on statuses:** `verifying`
- **Item types:** `work-item`, `bug`
- **On success:** `in-review`
- **On unrecoverable failure:** `in-progress`

## Inputs — every one of these must actually be read

| path | required | why |
|------|----------|-----|
| `tracker/items/{{item.id}}/item.md` | yes | the acceptance criteria are the only standard this skill judges against |
| `tracker/items/{{item.id}}/artifacts/impl-report.md` | yes | the claimed evidence, which this skill checks rather than trusts |
| `tracker/items/{{item.id}}/artifacts/plan.md` | yes | deviations from the plan are where undeclared behaviour hides |
| `tracker/items/{{item.id}}/artifacts/refinement-qa.md` | no | settles what a criterion meant when its wording is contested |
| `the code on branch {{item.branch}}` | yes | verification runs against the branch head, not against a description of it |
| `tracker/project.yaml` | yes | the commands the gates run |

## Outputs

| path | kind | when |
|------|------|------|
| `tracker/items/{{item.id}}/artifacts/verify-report.md` | file | always |
| `tracker/items/{{item.id}}/item.md` | file | always |
| `tracker/items/BUG-####/item.md` | file | conditional |
| `a commit of the workspace files this execution wrote` | commit | on-success |
| `tracker/items/{{item.id}}/journal.md` | append | always |
| `tracker/items/{{item.id}}/history.md` | append | always |

## Quality gates

Every gate below appears in the journal entry for every execution — including gates that were skipped, with the reason. A gate silently omitted is the failure the journal format exists to prevent.

| gate | enforcement | how it is checked | on failure |
|------|-------------|-------------------|------------|
| `tests-pass` | hard | run `{{commands.test}}`, expect exit-zero | escalate |
| `lint-clean` | hard | run `{{commands.lint}}`, expect exit-zero | escalate |
| `workspace-valid` | hard | run `.claude/agile-skills/scripts/validate-workspace`, expect exit-zero | stay |
| `every-criterion-independently-checked` | hard | For each AC, record the command this skill ran and its actual output. Citing the implementation report as evidence fails this gate. | stay |
| `negative-cases-exercised` | hard | For each criterion describing an error, an empty input, or a boundary, record the command that produced that condition and what happened. | stay |
| `a-criterion-about-criteria-is-read` | hard | For each criterion of the form "the earlier criteria still hold", name every criterion it covers by ID and state, per criterion, whether its sentence is still true of the new behaviour. Record the tests as evidence for that answer. Where nothing executable exercises the old criterion and the new behaviour together, say so in those words and either add a case or waive it by name. "The suite is green" answers a different question (spec/dor-dod.md, F-065). | stay |
| `tests-would-fail-without-the-change` | advisory | For at least one test per criterion, confirm it fails when the behaviour is disabled or reverted, and record how that was confirmed. | stay |

## Escalation

- **question:** File tracker/items/{{item.id}}/questions/Q-###.md addressed to architect when a criterion is ambiguous and the record does not settle it. Set the item to awaiting-answer with resume-to verifying and stop. Never ask the human directly.
- **defect:** A failure of this item's own criteria sends the item back to in-progress. A failure of behaviour delivered by another item is a new bug item at status ready, with reproduction steps, real output, and found-in.
- **impasse:** If verification cannot be performed at all - the code will not run, the environment is unusable - set the item to blocked with what was tried.

## Exit criteria — all must be true before transitioning

- [ ] A criterion whose subject is other criteria names them by ID and carries a per-criterion verdict read from their text, with any non-intersection stated and a covering case added or waived by name.
- [ ] Every acceptance criterion has a verdict backed by a command this skill ran and its actual output.
- [ ] Every criterion that passed is ticked in item.md, and no criterion is ticked without evidence.
- [ ] Failures are recorded as a send-back for this item's own criteria, or as bug items for behaviour delivered elsewhere.
- [ ] verify-report.md records the verdicts, the gates, and the defects found.
- [ ] The journal entry and the history row for this execution are written.

## Schemas this skill writes against

- Item and body schema — `.claude/agile-skills/spec/work-item.md`
- Journal and history formats — `.claude/agile-skills/spec/journal-and-history.md`
- Question protocol — `.claude/agile-skills/spec/question.md`
- Document headers and ADRs — `.claude/agile-skills/spec/doc-header.md`
- Definition of Ready and Done — `.claude/agile-skills/spec/dor-dod.md`
- IDs, statuses, transitions — `.claude/agile-skills/spec/ids-and-statuses.md`
- Workspace layout — `.claude/agile-skills/spec/workspace-layout.md`
