# Contract — refine v0.2.1

Rendered from `methodology/skills/refine/skill.yaml`. This is the authoritative list of what this skill must read, must produce, and must not skip. Open it when you need the exact gate list or the exit criteria; the procedure in SKILL.md is the how.

- **Persona:** product-analyst
- **Purpose:** Question the human until a draft item provably meets the Definition of Ready, and record the whole exchange.
- **Human interaction:** direct
- **Dispatched on statuses:** `draft`
- **Item types:** `work-item`, `bug`
- **On success:** `ready`
- **On unrecoverable failure:** `blocked`

## Inputs — every one of these must actually be read

| path | required | why |
|------|----------|-----|
| `tracker/items/{{item.id}}/item.md` | yes | the draft being refined, and the acceptance criteria to be made decidable |
| `tracker/items/{{item.id}}/history.md` | yes | an item sent back from later stages must not be re-refined as if it were new |
| `tracker/items/{{item.id}}/journal.md` | yes | intake recorded the human's original answers verbatim; re-asking them wastes the human |
| `docs/product/vision.md` | no | a criterion that contradicts the product vision is a conflict to raise, not to resolve |
| `tracker/items/*/item.md` | no | a sibling item may already own part of this scope |

## Outputs

| path | kind | when |
|------|------|------|
| `tracker/items/{{item.id}}/artifacts/refinement-qa.md` | file | always |
| `tracker/items/{{item.id}}/item.md` | file | always |
| `a commit of the workspace files this execution wrote` | commit | on-success |
| `tracker/items/{{item.id}}/journal.md` | append | always |
| `tracker/items/{{item.id}}/history.md` | append | on-success |

## Quality gates

Every gate below appears in the journal entry for every execution — including gates that were skipped, with the reason. A gate silently omitted is the failure the journal format exists to prevent.

| gate | enforcement | how it is checked | on failure |
|------|-------------|-------------------|------------|
| `workspace-valid` | hard | run `.claude/agile-skills/scripts/validate-workspace`, expect exit-zero | stay |
| `definition-of-ready` | hard | Walk spec/dor-dod.md section 1 (or 2 for a bug) criterion by criterion and record pass or fail for each with its evidence. A single overall verdict does not satisfy this gate. | stay |
| `criteria-are-decidable` | hard | For each AC, name the command to run or the artifact to inspect and the verdict that would follow. Any AC for which you cannot do this is not ready. | stay |
| `qa-recorded-verbatim` | hard | refinement-qa.md contains every question asked and every answer received, each tagged human or assumed, with nothing paraphrased into agreement. | stay |

## Escalation

- **question:** Ask the human directly and in batches while they are present. If they leave mid-refinement, file a question addressed to human, set the item to awaiting-answer with resume-to draft, and stop.
- **defect:** Not applicable; this skill shapes requirements and does not evaluate delivered behaviour.
- **impasse:** If the human cannot answer what the item needs and will not override, set the item to blocked, recording which Definition of Ready criteria remain unmet.

## Exit criteria — all must be true before transitioning

- [ ] Every question filed to the human carries product stake; implementation-only choices were decided or routed to plan, and a standing deferral was honoured for its whole category.
- [ ] Every Definition of Ready criterion is recorded as passed, or as overridden by the human with the reason.
- [ ] Every acceptance criterion names how it would be observed.
- [ ] refinement-qa.md holds the full exchange, with assumed answers marked as assumed.
- [ ] The item's Out of scope section names at least one thing a reader could reasonably assume is included.
- [ ] The journal entry and the history row for this execution are written.

## Schemas this skill writes against

- Item and body schema — `.claude/agile-skills/spec/work-item.md`
- Journal and history formats — `.claude/agile-skills/spec/journal-and-history.md`
- Question protocol — `.claude/agile-skills/spec/question.md`
- Document headers and ADRs — `.claude/agile-skills/spec/doc-header.md`
- Definition of Ready and Done — `.claude/agile-skills/spec/dor-dod.md`
- IDs, statuses, transitions — `.claude/agile-skills/spec/ids-and-statuses.md`
- Workspace layout — `.claude/agile-skills/spec/workspace-layout.md`
