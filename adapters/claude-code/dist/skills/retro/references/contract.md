# Contract — retro v0.2.0

Rendered from `methodology/skills/retro/skill.yaml`. This is the authoritative list of what this skill must read, must produce, and must not skip. Open it when you need the exact gate list or the exit criteria; the procedure in SKILL.md is the how.

- **Persona:** process-analyst
- **Purpose:** Read an ended engagement's record and report what it shows about how the work went, with toolkit findings proposed for triage.
- **Human interaction:** none
- **Dispatched on statuses:** none — this skill is invoked directly, not scheduled
- **Item types:** `epic`
- **On success:** no status transition of its own
- **On unrecoverable failure:** none

## Inputs — every one of these must actually be read

| path | required | why |
|------|----------|-----|
| `tracker/items/{{item.id}}/item.md` | yes | the goal the engagement was given, the ending recorded on it, and which children it names |
| `tracker/items/*/history.md` | yes | the timeline - every status change, its actor and its reason; send-backs and suspensions are read from here and nowhere else |
| `tracker/items/*/journal.md` | yes | the reasoning - decisions with their rationale, what each execution actually read, which gates ran and what they said |
| `tracker/items/*/item.md` | yes | criteria, their tick state, outcomes, and any accepted gap recorded in the notes |
| `tracker/items/*/questions/*.md` | yes | who was asked what, by whom, how long it took, and what the cross-answer check said |
| `tracker/items/*/artifacts/*.md` | yes | what each stage claimed for itself - the plan, the implementation report, the verification, the review |
| `tracker/requests/*.md` | no | what the stakeholder said on their own initiative, which is the one channel nobody opened for them |
| `docs/**` | no | the documents the engagement delivered, their version headers and their change logs |
| `the project history - the commit log over the engagement's window` | no | when work actually happened, and whether the commits match what the record says happened |
| `the installed contract of every skill named in the record` | yes | whether a gate held because the contract required it or because the worker was careful - unanswerable without the contracts, and every project has them |

## Outputs

| path | kind | when |
|------|------|------|
| `tracker/items/{{item.id}}/artifacts/retro.md` | file | always |
| `tracker/items/{{item.id}}/journal.md` | append | always |

## Quality gates

Every gate below appears in the journal entry for every execution — including gates that were skipped, with the reason. A gate silently omitted is the failure the journal format exists to prevent.

| gate | enforcement | how it is checked | on failure |
|------|-------------|-------------------|------------|
| `engagement-has-ended` | hard | run `.claude/agile-skills/scripts/engagement-state {{item.id}}`, expect exit-zero | stay |
| `retro-report-is-well-formed` | hard | run `.claude/agile-skills/scripts/lint-retro {{item.id}}`, expect exit-zero | stay |
| `scope-was-not-degenerate` | hard | run `.claude/agile-skills/scripts/lint-retro {{item.id}} --require-scope`, expect exit-zero | stay |
| `the-record-was-not-touched` | hard | List every file this execution wrote. If it is not exactly artifacts/retro.md and the epic's journal.md, the retrospective has edited the record it is auditing and the report is void. | stay |
| `workspace-valid` | hard | run `.claude/agile-skills/scripts/validate-workspace`, expect exit-zero | stay |

## Escalation

- **question:** This skill never files questions. The engagement has ended - a blocking question would suspend an item with nowhere to resume to, and a question to the human would ask a person who has already been told the work is finished. Everything it would ask goes into the report as an observation or a proposal.
- **defect:** This skill never files items. A defect it finds in delivered behaviour is written into the report as a proposal, with its evidence, for a human to act on. An auditor that can create work out of what it audits cannot be told apart, in the record, from one re-litigating a decision.
- **impasse:** If the record cannot be read at all - the workspace does not validate, or the engagement has not ended - report that and stop without writing a report. If it can be read but poorly, that is not an impasse - say what could not be read under `## What was read`, and continue.

## Exit criteria — all must be true before transitioning

- [ ] artifacts/retro.md exists with its four sections in order, and its frontmatter counts agree with the workspace.
- [ ] Every item in the engagement appears in the declared scope, or the report says which did not and why.
- [ ] Every observation and every proposal carries at least one citation, and every citation resolves.
- [ ] Every citation of the form <ITEM>/Q-nnn appearing under docs/ was followed to the answer it cites and read against the answers that came after it, and the count is stated.
- [ ] Every proposal carries a classification from the closed set, and every toolkit-defect proposal carries its counterfactual and its recurrence.
- [ ] The positive record names at least one thing that held, or states that nothing did and why that is the honest reading.
- [ ] Nothing in the engagement was written except artifacts/retro.md and the epic's journal.md.
- [ ] The journal entry for this execution is written, with the status unchanged.

## Schemas this skill writes against

- Item and body schema — `.claude/agile-skills/spec/work-item.md`
- Journal and history formats — `.claude/agile-skills/spec/journal-and-history.md`
- Question protocol — `.claude/agile-skills/spec/question.md`
- Document headers and ADRs — `.claude/agile-skills/spec/doc-header.md`
- Definition of Ready and Done — `.claude/agile-skills/spec/dor-dod.md`
- IDs, statuses, transitions — `.claude/agile-skills/spec/ids-and-statuses.md`
- Workspace layout — `.claude/agile-skills/spec/workspace-layout.md`
