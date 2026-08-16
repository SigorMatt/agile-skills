# `skill.yaml` and `process.md` — the skill contract

A skill is a directory under `methodology/skills/<name>/` containing exactly two files:

| File | Role |
|------|------|
| `skill.yaml` | the **contract** — machine-readable. What triggers it, what it must read, what it must produce, which gates must pass, where it goes next. |
| `process.md` | the **procedure** — human/agent-readable. The steps a competent worker follows to satisfy the contract. |

`scripts/lint-skills` validates every `skill.yaml` against this page and refuses to build
otherwise. An adapter renders a skill from these two files and nothing else: if a renderer
needs a fact that is in neither, the methodology is deficient and is fixed here — not patched
in the adapter.

Nothing in `methodology/` may name a specific agent runtime, tool, vendor, or product.

---

## 1. `skill.yaml` schema

```yaml
name: implement
version: 0.1.0
persona: developer
purpose: Execute the recorded plan on a branch, with tests, and report what was built.

when_to_use:
  - The tracker has an item at status planned and its plan.md exists.
  - Work on an item was interrupted and the item sits at in-progress.
  - A question that blocked implementation has just been answered.

dispatch:
  on_status: [planned, in-progress]
  item_types: [work-item, bug]

human_interaction: via-questions

inputs:
  - path: tracker/items/{{item.id}}/item.md
    required: true
    why: acceptance criteria are the definition of what to build
  - path: tracker/items/{{item.id}}/artifacts/plan.md
    required: true
    why: the design decisions this skill must not re-litigate
  - path: docs/architecture/**
    required: false
    why: constraints the plan assumes but does not restate

outputs:
  - path: tracker/items/{{item.id}}/artifacts/impl-report.md
    kind: file
    when: always
  - path: "branch {{item.branch}}"
    kind: branch
    when: always
  - path: tracker/items/{{item.id}}/journal.md
    kind: append
    when: always

quality_gates:
  - name: workspace-valid
    description: The workspace still satisfies the schemas after this skill's writes.
    command: scripts/validate-workspace
    expect: exit-zero
    enforcement: hard
    on_failure: retry
  - name: tests-pass
    description: The project's own test command passes on the branch head.
    command: "{{commands.test}}"
    expect: exit-zero
    enforcement: hard
    on_failure: stay
  - name: acceptance-criteria-addressed
    description: Every AC maps to a specific test or observable behaviour.
    manual_check: For each AC in item.md, name the test or command that demonstrates it.
    enforcement: advisory
    on_failure: stay

escalation:
  question: File tracker/items/{{item.id}}/questions/Q-###.md addressed to architect; set the item to awaiting-answer with resume-to recorded.
  defect: File a new bug item linked to this one via found-in; do not fix out-of-scope defects here.
  impasse: Set the item to blocked with the attempted approaches recorded in the journal.

exit_criteria:
  - Every acceptance criterion has code and a test that exercises it.
  - All hard gates passed on the branch head.
  - impl-report.md maps each AC to the evidence for it.
  - The journal entry and the history row for this execution are written.

next_status: verifying
failure_status: blocked
```

### 1.1 Field reference

| Field | Required | Type | Rules |
|-------|----------|------|-------|
| `name` | yes | string | lowercase kebab-case; MUST equal the directory name |
| `version` | yes | string | semantic version `MAJOR.MINOR.PATCH` |
| `persona` | yes | enum | `product-analyst` \| `architect` \| `developer` \| `qa-engineer` \| `reviewer` \| `scheduler` |
| `purpose` | yes | string | one sentence, ≤ 160 characters, no line breaks |
| `when_to_use` | yes | list of strings | ≥ 2 entries, each a **concrete situation**, not a restatement of the purpose |
| `dispatch` | yes | mapping | `on_status`: list of statuses (may be empty); `item_types`: list of item types |
| `human_interaction` | yes | enum | `none` \| `direct` \| `via-questions` |
| `inputs` | yes | list | each: `path` (required), `required` (bool), `why` (string) |
| `outputs` | yes | list | each: `path`, `kind` ∈ `file` \| `append` \| `branch` \| `commit` \| `status`, `when` ∈ `always` \| `on-success` \| `on-failure` \| `conditional` |
| `quality_gates` | yes | list | may be empty only for `next`; see §1.3 |
| `escalation` | yes | mapping | keys `question`, `defect`, `impasse`; each a sentence saying exactly what to write and where |
| `exit_criteria` | yes | list of strings | ≥ 2; each MUST be decidable as true or false by someone holding the workspace |
| `next_status` | yes | string or `null` | the status on success; `null` for skills that do not own a transition |
| `failure_status` | yes | string or `null` | the status on unrecoverable failure |

Unknown top-level keys are an error. A misspelled key that lints clean is a contract clause
that silently does nothing.

### 1.2 `dispatch` and the orchestrator

`dispatch.on_status` is the **only** thing the orchestrator reads to decide what to run. It is
a list of statuses, not an expression, because an expression language would need an evaluator
in every adapter and would let engineering judgement leak into the scheduler — which VISION
principle 4 forbids.

- `on_status: []` means the orchestrator never dispatches this skill from item state. `intake`
  (a human starts it) and `next` (it *is* the orchestrator) are the only skills with an empty
  list.
- Every non-terminal status in `pipeline.yaml` MUST be claimed by exactly one skill's
  `on_status`. `scripts/lint-skills` cross-checks this in both directions: a status no skill
  claims is a stall, and a status two skills claim is a race.

### 1.3 `quality_gates`

| Key | Required | Rules |
|-----|----------|-------|
| `name` | yes | kebab-case, unique within the skill; this is the name that appears in the journal |
| `description` | yes | what the gate establishes, in one sentence |
| `command` | one of | a shell command, possibly containing placeholders (§1.4) |
| `manual_check` | one of | what the worker must verify by inspection, when no command can decide it |
| `expect` | with `command` | `exit-zero` (default) or `exit-nonzero` |
| `enforcement` | yes | `hard` \| `advisory` |
| `on_failure` | yes | `stay` (keep the current status and fix) \| `retry` \| `escalate` \| a status name |

Rules:

- A gate MUST have exactly one of `command` or `manual_check`. A gate with both invites
  reporting the manual check when the command fails.
- **`enforcement: hard` means an adapter MUST prevent the transition when the gate fails**, by
  the strongest mechanism that runtime offers. `advisory` means the skill must run it, record
  the result, and may proceed on failure with the reason journaled. Which gates are actually
  hard-enforced in a given runtime is documented by that adapter, not claimed here.
- A gate MUST be runnable by an agent with no conversational context — its `command` cannot
  depend on a variable that only the current session knows.
- Every gate appears in the journal for every execution of the skill, including gates that were
  skipped, with the reason. See `journal-and-history.md` §2.2.

### 1.4 Placeholders

Placeholders use `{{...}}` and are resolved by the adapter or gate runner at execution time
against the workspace, never by the methodology.

| Placeholder | Resolves to |
|-------------|-------------|
| `{{item.id}}` | the item being acted on, e.g. `WI-0007` |
| `{{item.branch}}` | that item's `branch` field, e.g. `wi/WI-0007` |
| `{{item.type}}` | `epic` \| `work-item` \| `bug` |
| `{{workspace}}` | the workspace root (the consumer project's root) |
| `{{trunk}}` | `project.trunk-branch` from `tracker/project.yaml` |
| `{{commands.test}}` | `commands.test` from `tracker/project.yaml` |
| `{{commands.lint}}` | `commands.lint` from `tracker/project.yaml` |
| `{{commands.build}}` | `commands.build` from `tracker/project.yaml` |

A `{{commands.*}}` placeholder that resolves to `null` makes the gate **skipped**, and the
skill MUST journal it as skipped with the reason. It MUST NOT be reported as passed. `plan` is
responsible for filling these in; its exit criteria require either a value or an ADR recording
why the project has no such command.

An unknown placeholder is a lint error, so a typo cannot degrade into an empty string that
makes a gate trivially pass.

---

## 2. `process.md`

`process.md` is written for **a competent worker with zero context beyond the workspace**. It
may not assume the reader saw an earlier step, a previous run, or any conversation. Every run
of a skill is that worker's first day.

### 2.1 Required sections, in this order

```markdown
# <skill-name> — <persona>

<One paragraph: what this role is responsible for and what it must not do.>

## Preconditions
## Steps
## Journaling
## Self-check
## Failure and escalation
```

| Section | Must contain |
|---------|--------------|
| `## Preconditions` | what must be true before starting, and what to do if it is not. Includes re-reading the item and its history — never trusting recollection. |
| `## Steps` | numbered steps. Each says **what to read**, **what to decide**, **what to write**. A step that only says what to think about is not a step. |
| `## Journaling` | exactly what this skill writes to `journal.md` and `history.md`, including which gates to list. |
| `## Self-check` | the exit criteria restated as questions the worker answers before transitioning, plus the specific ways this skill is known to go wrong. |
| `## Failure and escalation` | what to do when a gate fails, when a question is needed, and when the situation is an impasse. |

### 2.2 Rules

- `## Steps` MUST include, as its first step, re-reading the item's current state from disk.
  Skills are resumed after interruptions; the most likely wrong assumption is that the
  workspace is as this skill last left it.
- The last step MUST be the status transition, and it MUST come **after** journaling. If the
  process is interrupted between them, an item whose status advanced without a journal entry is
  a silent gap; a journal entry without the transition is merely a repeat next run.
- `## Self-check` MUST name at least two **specific** failure modes for this skill — the things
  this role actually gets wrong — not generic advice. This section is the main defence against
  a plausible-looking but wrong execution, and it is where lessons from a bad run get recorded.
- Cross-references to `spec/` are by filename and section, so a reader can open exactly one
  more file rather than the whole spec.

---

## 3. Versioning

Skills carry semantic versions so the iterate-and-deepen loop is trackable:

- **PATCH** — wording, clarifications, a new self-check entry. No contract change.
- **MINOR** — a new gate, a new output, a new step. Existing workspaces stay valid.
- **MAJOR** — a changed status transition, a removed output, a renamed gate. Existing workspaces
  may need migration.

A change to `skill.yaml` or `process.md` MUST bump the version in the same commit. The rendered
skills carry the version, so a paper trail names the exact contract that produced it — which is
what makes "the toy run used skill X v0.1.0, and it went wrong here" an actionable report.
