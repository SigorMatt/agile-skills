# Specification index

These files are the **single source of truth** for the shape of a workspace and of a skill
contract. Skills cite them; adapters render them; validators enforce them. Where a skill's
`process.md` and a spec disagree, the spec wins and the skill is a defect.

Nothing here names a particular agent runtime, tool, CLI, or vendor. That is a hard rule, and
`scripts/lint-skills` fails the build on a violation. A runtime-specific concern belongs in
`adapters/<runtime>/`.

## Files

| File | Defines |
|------|---------|
| [`ids-and-statuses.md`](ids-and-statuses.md) | ID formats and allocation, item types, the status graph, legal transitions, priority ranks |
| [`work-item.md`](work-item.md) | `item.md` — frontmatter fields and body sections for epics, work items, and bugs |
| [`journal-and-history.md`](journal-and-history.md) | `journal.md` entry format; `history.md` transition format |
| [`question.md`](question.md) | `questions/Q-###.md` format and the escalation protocol |
| [`doc-header.md`](doc-header.md) | version header and change log carried by every file under `docs/`; the ADR format |
| [`dor-dod.md`](dor-dod.md) | Definition of Ready and Definition of Done, per item type |
| [`skill-contract.md`](skill-contract.md) | `skill.yaml` schema and what a `process.md` must contain |
| [`workspace-layout.md`](workspace-layout.md) | the full directory tree a workspace must have, and which files are generated |

## Normative language

- **MUST** / **MUST NOT** — a validator enforces it, or the artifact is invalid.
- **SHOULD** — a validator may warn; a skill that departs from it MUST journal why.
- **MAY** — free choice, no record required.

## Conventions that apply to every artifact

1. **Markdown with YAML frontmatter.** Every tracked artifact starts with a `---` fenced YAML
   block. A file without one is invalid — an unlabelled artifact that validated clean would be
   the easiest way for the record to rot.
2. **Append-only means append-only.** `journal.md` and `history.md` are never rewritten,
   reordered, or corrected in place. A mistake is corrected by appending a new entry that says
   so. The audit value of the trail comes entirely from this property.
3. **Timestamps are UTC ISO-8601 to the second**, e.g. `2026-08-16T21:04:33Z`. Local times make
   two entries written on different machines unorderable.
4. **Every status change is caused by exactly one skill execution**, and that execution writes
   a journal entry and a history entry. There is no such thing as a status that changed because
   someone felt like it.
5. **No state lives outside the workspace.** A skill MUST be able to do its job having read only
   the files named in its contract's `inputs`. Conversation history is not an input, is not
   durable, and is not auditable.
6. **Idempotence.** Re-running a skill on an item in the same state MUST converge to the same
   artifacts rather than duplicating them. Appending a second journal entry for the second run
   is correct and expected; creating `plan-2.md` is not.
