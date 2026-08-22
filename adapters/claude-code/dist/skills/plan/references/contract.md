# Contract — plan v0.1.2

Rendered from `methodology/skills/plan/skill.yaml`. This is the authoritative list of what this skill must read, must produce, and must not skip. Open it when you need the exact gate list or the exit criteria; the procedure in SKILL.md is the how.

- **Persona:** architect
- **Purpose:** Design the change for a Ready item, record the decisions as ADRs, and write an implementation plan someone else can execute.
- **Human interaction:** direct
- **Dispatched on statuses:** `ready`
- **Item types:** `work-item`, `bug`
- **On success:** `planned`
- **On unrecoverable failure:** `blocked`

## Inputs — every one of these must actually be read

| path | required | why |
|------|----------|-----|
| `tracker/items/{{item.id}}/item.md` | yes | the acceptance criteria are the contract this design must satisfy |
| `tracker/items/{{item.id}}/artifacts/refinement-qa.md` | no | assumptions and unresolved points recorded during refinement constrain the design |
| `docs/architecture/overview.md` | no | the existing shape of the system, which this change must fit or explicitly change |
| `docs/architecture/adr/` | no | decisions already taken must not be silently re-decided |
| `tracker/project.yaml` | yes | the trunk branch and the project's own commands, which this skill must fill in if absent |
| `the project's source code` | no | a plan written without reading what exists is a guess |

## Outputs

| path | kind | when |
|------|------|------|
| `tracker/items/{{item.id}}/artifacts/plan.md` | file | always |
| `docs/architecture/adr/ADR-####-{{item.id}}.md` | file | conditional |
| `docs/architecture/overview.md` | file | conditional |
| `tracker/project.yaml` | file | conditional |
| `a commit of the workspace files this execution wrote` | commit | on-success |
| `tracker/items/{{item.id}}/journal.md` | append | always |
| `tracker/items/{{item.id}}/history.md` | append | on-success |

## Quality gates

Every gate below appears in the journal entry for every execution — including gates that were skipped, with the reason. A gate silently omitted is the failure the journal format exists to prevent.

| gate | enforcement | how it is checked | on failure |
|------|-------------|-------------------|------------|
| `workspace-valid` | hard | run `.claude/agile-skills/scripts/validate-workspace`, expect exit-zero | stay |
| `every-criterion-is-addressed` | hard | Map every AC in item.md to a step in plan.md and to the test or observation that will demonstrate it. An AC with no step is a hole in the design. | stay |
| `project-commands-resolved` | hard | tracker/project.yaml has a real command for test and lint, or an ADR records why the project has none. A command that does not exist, or one that exits zero without checking anything, fails this gate. | stay |
| `decisions-recorded` | hard | List the choices this plan makes. For each, point to an ADR, or to an entry under Assumptions stating what would be needed to reverse it. | stay |
| `plan-is-executable-without-you` | advisory | Read the plan as if you had never seen the item. Each step must say which files to change and what the result should be, without requiring a decision the plan does not make. | stay |

## Escalation

- **question:** Prefer in order - answer from the documents and cite them, then make a reversible assumption and record it under Assumptions, then ask the human. Ask only when the decision is irreversible or depends on intent no document records.
- **defect:** If planning reveals that already-delivered behaviour is wrong, file a bug item rather than widening this plan to fix it.
- **impasse:** If the item cannot be designed without a decision nobody can make, set it to blocked and record the options and what each would cost.

## Exit criteria — all must be true before transitioning

- [ ] plan.md exists with numbered steps, each naming the files it touches and the observable result.
- [ ] Every acceptance criterion maps to at least one step and to the evidence that will demonstrate it.
- [ ] Every non-obvious decision is an ADR or a recorded reversible assumption.
- [ ] tracker/project.yaml names the test and lint commands, or an ADR records why it cannot.
- [ ] The journal entry and the history row for this execution are written.

## Schemas this skill writes against

- Item and body schema — `.claude/agile-skills/spec/work-item.md`
- Journal and history formats — `.claude/agile-skills/spec/journal-and-history.md`
- Question protocol — `.claude/agile-skills/spec/question.md`
- Document headers and ADRs — `.claude/agile-skills/spec/doc-header.md`
- Definition of Ready and Done — `.claude/agile-skills/spec/dor-dod.md`
- IDs, statuses, transitions — `.claude/agile-skills/spec/ids-and-statuses.md`
- Workspace layout — `.claude/agile-skills/spec/workspace-layout.md`
