# Contract — intake v0.1.1

Rendered from `methodology/skills/intake/skill.yaml`. This is the authoritative list of what this skill must read, must produce, and must not skip. Open it when you need the exact gate list or the exit criteria; the procedure in SKILL.md is the how.

- **Persona:** product-analyst
- **Purpose:** Turn a raw idea from a human into an epic and a first set of work items in the tracker.
- **Human interaction:** direct
- **Dispatched on statuses:** none — this skill is invoked directly, not scheduled
- **Item types:** not applicable
- **On success:** `draft`
- **On unrecoverable failure:** none

## Inputs — every one of these must actually be read

| path | required | why |
|------|----------|-----|
| `the human's stated idea, in this session` | yes | this skill exists to convert it; there is no artifact to read it from yet |
| `tracker/project.yaml` | no | an existing project's name, trunk branch and commands constrain what can be proposed |
| `tracker/items/*/item.md` | no | existing items reveal overlap, and the highest allocated IDs |
| `docs/product/vision.md` | no | a new epic must be coherent with an existing product vision, or explicitly revise it |

## Outputs

| path | kind | when |
|------|------|------|
| `tracker/` | file | conditional |
| `tracker/items/{{item.id}}/item.md` | file | always |
| `docs/product/vision.md` | file | always |
| `a commit of the workspace files this execution wrote` | commit | on-success |
| `tracker/items/{{item.id}}/journal.md` | append | always |
| `tracker/items/{{item.id}}/history.md` | append | always |
| `tracker/board.md` | file | always |

## Quality gates

Every gate below appears in the journal entry for every execution — including gates that were skipped, with the reason. A gate silently omitted is the failure the journal format exists to prevent.

| gate | enforcement | how it is checked | on failure |
|------|-------------|-------------------|------------|
| `workspace-valid` | hard | run `.claude/agile-skills/scripts/validate-workspace`, expect exit-zero | stay |
| `epic-has-success-measures` | hard | Read the epic's Success measures section; each entry must be something a person could check, not a restatement of the goal. | stay |
| `items-are-separable` | advisory | For each item, state the order it could be built in and what it depends on; an item that cannot be described this way is really part of another. | stay |
| `no-solution-in-the-problem` | advisory | Read each title and story back; if it names a technology or a data structure the human did not, remove it and record what was removed. | stay |

## Escalation

- **question:** Ask the human directly, in batches, before creating anything. Only file a question artifact when the human has left the session and the answer can wait.
- **defect:** Not applicable; this skill creates work, it does not evaluate delivered behaviour.
- **impasse:** If the idea cannot be shaped into an epic with even one observable success measure, create nothing, and report to the human what is missing.

## Exit criteria — all must be true before transitioning

- [ ] An epic exists at status open with a goal, success measures, and an explicit out-of-scope list.
- [ ] At least one work item exists at status draft, each naming the epic.
- [ ] docs/product/vision.md exists and states who the product is for and what it is for.
- [ ] Every created item has journal.md and history.md with a creation entry.
- [ ] The board has been regenerated and shown to the human.

## Schemas this skill writes against

- Item and body schema — `.claude/agile-skills/spec/work-item.md`
- Journal and history formats — `.claude/agile-skills/spec/journal-and-history.md`
- Question protocol — `.claude/agile-skills/spec/question.md`
- Document headers and ADRs — `.claude/agile-skills/spec/doc-header.md`
- Definition of Ready and Done — `.claude/agile-skills/spec/dor-dod.md`
- IDs, statuses, transitions — `.claude/agile-skills/spec/ids-and-statuses.md`
- Workspace layout — `.claude/agile-skills/spec/workspace-layout.md`
