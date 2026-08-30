# Contract — next v0.4.0

Rendered from `methodology/skills/next/skill.yaml`. This is the authoritative list of what this skill must read, must produce, and must not skip. Open it when you need the exact gate list or the exit criteria; the procedure in SKILL.md is the how.

- **Persona:** scheduler
- **Purpose:** Pick the single next runnable action from workspace state and dispatch the skill that owns it.
- **Human interaction:** none
- **Dispatched on statuses:** none — this skill is invoked directly, not scheduled
- **Item types:** not applicable
- **On success:** no status transition of its own
- **On unrecoverable failure:** none

## Inputs — every one of these must actually be read

| path | required | why |
|------|----------|-----|
| `tracker/requests/` | no | an open stakeholder request outranks selecting work, so it is read before the candidate set is built |
| `methodology/pipeline.yaml` | yes | the status graph, the status-to-skill map, and the selection key - this skill's entire world model |
| `tracker/items/*/item.md` | yes | the statuses, priorities, dependencies and creation times the selection key ranks |
| `tracker/items/*/questions/*.md` | yes | an open blocking question changes what may run, and a human-addressed question stops the loop |
| `tracker/items/*/history.md` | no | reports where an item stopped when nothing is runnable |
| `scripts/engagement-state <EP-ID>` | yes | whether an engagement is running, over, or fully closed - the one judgement this skill is not allowed to make for itself |

## Outputs

| path | kind | when |
|------|------|------|
| `tracker/board.md` | file | always |
| `a dispatch decision, reported to the caller` | status | always |

## Quality gates

Every gate below appears in the journal entry for every execution — including gates that were skipped, with the reason. A gate silently omitted is the failure the journal format exists to prevent.

| gate | enforcement | how it is checked | on failure |
|------|-------------|-------------------|------------|
| `workspace-valid` | hard | run `.claude/agile-skills/scripts/validate-workspace`, expect exit-zero | stay |
| `engagements-are-ended` | hard | For every epic still at open, state the verdict scripts/engagement-state gave it. If any is at-rest and this run did not dispatch review-close on it, the run stopped on an engagement that is over and nobody has told the stakeholder. | stay |
| `ended-engagements-are-read` | hard | For every epic at done or blocked, state the verdict scripts/engagement-state gave it. If any is ended rather than closed and this run did not dispatch retro on it, the run reported an engagement as finished that has not read its own trail. | stay |
| `board-current` | hard | run `.claude/agile-skills/scripts/board-gen`, expect exit-zero | stay |
| `selection-is-deterministic` | hard | State the candidate set and the selection key values that eliminated each rejected candidate. If any candidate was rejected for a reason not in the key, the selection is invalid. | stay |

## Escalation

- **question:** This skill never files questions. It surfaces questions others filed and stops.
- **defect:** This skill never evaluates work. A defect it appears to see is invisible to it - it reads status, not content.
- **impasse:** If the workspace does not validate, report the validator output and stop. Dispatching against a broken workspace would make every downstream skill unsound.

## Exit criteria — all must be true before transitioning

- [ ] The workspace validated, or the run stopped with the validator's output.
- [ ] The board was regenerated.
- [ ] Exactly one of - a question was surfaced and the loop stopped, a skill was dispatched, or the board was reported with the reason nothing is runnable.
- [ ] Every epic was asked scripts/engagement-state, and none of them is at-rest and undispatched, or ended and unread.
- [ ] The dispatch decision names the item, its status, and the owning skill taken from pipeline.yaml.

## Schemas this skill writes against

- Item and body schema — `.claude/agile-skills/spec/work-item.md`
- Journal and history formats — `.claude/agile-skills/spec/journal-and-history.md`
- Question protocol — `.claude/agile-skills/spec/question.md`
- Document headers and ADRs — `.claude/agile-skills/spec/doc-header.md`
- Definition of Ready and Done — `.claude/agile-skills/spec/dor-dod.md`
- IDs, statuses, transitions — `.claude/agile-skills/spec/ids-and-statuses.md`
- Workspace layout — `.claude/agile-skills/spec/workspace-layout.md`
