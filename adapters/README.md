# The adapter contract

The methodology in `methodology/` is runtime-neutral on purpose. An **adapter** renders it into
whatever form a particular agent runtime can actually load, install it into a project, and wire
the quality gates to that runtime's strongest enforcement mechanism.

This file defines what an adapter must do. It is written so that a second adapter — for a
different runtime — can be built **without editing anything under `methodology/` or `spec/`**.
If you find yourself needing to change the methodology to make an adapter work, that is a defect
in the methodology and it is fixed there, for every adapter, rather than patched in yours.

Existing adapters: [`claude-code/`](claude-code/).

---

## 1. What an adapter consumes

Exactly four things, and nothing else:

| Input | What it provides |
|-------|------------------|
| `methodology/skills/<name>/skill.yaml` | the contract: triggers, inputs, outputs, gates, escalation, exit criteria, transitions |
| `methodology/skills/<name>/process.md` | the procedure a worker follows |
| `methodology/pipeline.yaml` | the status graph, the status→skill map, the orchestrator's algorithm |
| `spec/*.md` | the schemas the process refers to, shipped as reference material |

An adapter MUST NOT hold per-skill knowledge. If your renderer contains
`if skill == "implement"`, you have moved methodology into the adapter, and the next adapter
will have to re-derive it. Everything a renderer needs to treat a skill differently is a
*declared field* — `human_interaction`, `dispatch.on_status`, `quality_gates[].enforcement` —
and if the field you need does not exist, add it to `spec/skill-contract.md`.

---

## 2. Capabilities an adapter must map

Each capability says what the methodology needs, what a runtime may substitute, and what an
adapter must document when the runtime cannot provide it.

### C1 — Skill discovery and triggering

**Needed:** a way for the agent to load the right skill's procedure at the right moment, in two
modes: *explicitly* (the operator or the orchestrator names a skill) and *by relevance* (the
agent recognises that a stated situation matches a skill).

**Provided by:** whatever the runtime offers — a skills directory, a plugin manifest, a prompt
library, a set of slash commands, or, at minimum, files the agent is instructed to read.

**Contract:**
- Every skill in `pipeline.yaml`'s `skills:` list MUST be reachable explicitly.
- `when_to_use` MUST be surfaced in whatever the runtime matches against for relevance-based
  triggering. If the runtime has no such mechanism, explicit invocation alone is acceptable, and
  the adapter MUST say so — because `CONSUMER-PROMPT.md` then has to name skills rather than
  describe situations.
- If the runtime truncates the text it matches against, the adapter MUST fail its own build when
  a rendered description would be truncated, rather than shipping a skill that silently stops
  triggering.

### C2 — Asking the human

**Needed:** `intake` and `refine` (`human_interaction: direct`) must be able to put questions to
a human and receive answers in the same session. `plan` and `answer-questions` use it rarely.
`implement`, `verify`, `review-close` and `next` MUST NOT be able to.

**Provided by:** a structured question tool, an interactive prompt, or simply printing the
questions and stopping.

**Contract:**
- The adapter MUST provide a way for a `direct` skill to ask, and MUST document the fallback
  when the mechanism is unavailable (for example when the runtime is in a non-interactive mode).
  The fallback is always the same: print the batched questions and stop. Never proceed on an
  invented answer.
- Where the runtime can **remove** the questioning capability for a specific skill, the adapter
  MUST do so for every skill whose `human_interaction` is `none` or `via-questions`. That turns
  R2's rule from an instruction into an enforced constraint, and it is the single highest-value
  thing an adapter can add.
- Where the runtime cannot remove it, the adapter MUST document that the rule is convention
  only.

### C3 — Gate execution

**Needed:** the `command` of every quality gate must run as a real command, its exit status must
be compared with `expect`, and a failing gate with `enforcement: hard` must **prevent** the
status transition.

**Provided by:** a hook that can block an action, a wrapper the agent must call, or — weakest —
an instruction in the rendered procedure.

**Contract:**
- The adapter MUST ship the gate commands as executable scripts installed into the project, and
  MUST resolve `{{...}}` placeholders (`spec/skill-contract.md` §1.4) from `tracker/project.yaml`
  and the item being acted on.
- A placeholder that resolves to `null` MUST make the gate **skipped**, and the skip MUST be
  reported. It MUST NOT be reported as a pass.
- The adapter MUST document, per gate, whether enforcement is **hard** (the runtime blocks) or
  **convention** (the procedure says so and nothing stops it). Claiming enforcement the runtime
  does not provide is the one thing that would make the whole "executable gates" premise a lie.
- Blocking mechanisms differ in what they can block. An adapter MUST NOT design a gate around a
  mechanism that fires *after* the action it is meant to prevent.

### C4 — Install and uninstall

**Needed:** placing the rendered skills, the gate scripts, `pipeline.yaml` and the `spec/`
reference material into a target project, and removing them again.

**Contract:**
- Install MUST be idempotent: running it twice produces the same tree and does not duplicate
  anything.
- Install MUST place `pipeline.yaml` and the workspace scripts where `scripts/validate-workspace`
  will find them (it searches `--pipeline`, then beside itself, then `../methodology/`), so a
  consumer project needs no copy of `methodology/`.
- Install MUST NOT modify the project's own source code, its version control history, or any
  configuration outside the paths it documents.
- Uninstall MUST remove exactly what install added, and MUST NOT remove the workspace
  (`tracker/`, `docs/`) — that is the project's record, not the adapter's.
- The installer MUST record the methodology version it installed, so a project can tell which
  contracts produced its paper trail.

### C5 — Isolated execution (optional)

**Needed:** nothing. But a runtime that can run a skill in a fresh context with no memory of
prior steps makes the pipeline markedly more honest: `verify` genuinely independent of
`implement` is the clearest case.

**Contract:** if the runtime offers it, the adapter SHOULD use it for `verify` and for the
acceptance-test runs, and MUST document which skills it isolates. If it does not, everything
still works — the workspace is the only channel between skills by design, so isolation is a
strengthening, never a prerequisite.

---

## 3. What a renderer must produce

For each skill:

1. **The procedure**, in whatever form the runtime loads, derived from `process.md` without
   rewriting its meaning. Adapters may reformat and may add runtime-specific preamble; they may
   not paraphrase steps, drop the self-check, or reorder the required sections.
2. **A trigger description** derived from `purpose` + `when_to_use`, with the concrete situations
   first. Descriptions are what make relevance-based triggering work, and the situations are the
   part that matches how a person actually phrases a request.
3. **The contract, as reference material** — a rendered form of `skill.yaml` the agent can open
   when it needs the exact gate list or exit criteria, rather than carrying it in context at all
   times.
4. **The schemas it cites**, from `spec/`, as reference material reachable from the procedure.

Rendering MUST be **deterministic**: rendering twice from the same source produces byte-identical
output. The repository's own gate re-renders and diffs against the committed output, which is
only meaningful if the renderer is stable. No timestamps, no hostnames, no dictionary-iteration
order.

---

## 4. What an adapter must document

In `adapters/<runtime>/README.md`:

- The exact install path and what is placed where.
- The runtime version and format the renderer targets, and how that was confirmed — with URLs
  and a date. Formats change; an adapter that cannot say when it last checked is a guess.
- A **gate enforcement table**: every gate of every skill, and whether it is hard-enforced or
  convention in this runtime.
- Which of C1–C5 the runtime provides, which it does not, and what the fallback is.
- How to uninstall.

---

## 5. Conformance checklist

A new adapter is conformant when every box can be ticked with evidence:

- [ ] **A1** The renderer reads only `skill.yaml`, `process.md`, `pipeline.yaml`, and `spec/`.
- [ ] **A2** The renderer contains no per-skill special cases; behaviour varies only by declared
      contract fields.
- [ ] **A3** Rendering is byte-deterministic; a re-render of unchanged sources produces no diff.
- [ ] **A4** All eight skills render, and each is explicitly invocable in the target runtime.
- [ ] **A5** `when_to_use` reaches whatever the runtime matches on, or the adapter documents that
      relevance-based triggering is unavailable.
- [ ] **A6** Skills with `human_interaction` of `none` or `via-questions` cannot ask the human,
      by runtime constraint where possible and by documented convention otherwise.
- [ ] **A7** Every gate `command` runs as a real command with placeholders resolved; a `null`
      placeholder yields a reported skip, never a pass.
- [ ] **A8** At least one `enforcement: hard` gate is demonstrated **blocking** a transition in a
      deliberate failing case, and the demonstration is recorded.
- [ ] **A9** Install is idempotent; uninstall removes exactly what install added and leaves
      `tracker/` and `docs/` untouched.
- [ ] **A10** `scripts/validate-workspace` runs in an installed project with no additional
      dependencies.
- [ ] **A11** The adapter README carries the gate enforcement table and the C1–C5 mapping.
- [ ] **A12** No file under `methodology/` or `spec/` was changed to make the adapter work — or,
      if one was, the change is runtime-neutral and improves the methodology for every adapter.

---

## 6. Notes for a `codex-cli/` adapter

Recorded so the next implementer starts from the questions rather than discovering them:

- **C2 is the interesting one.** If the runtime has no structured way to ask a human and no way
  to *remove* the ability from a skill, then R2's separation between "may ask" and "must file a
  question" becomes convention. That is acceptable, and it must be stated in the README, because
  the consumer's expectations about how much the pipeline will interrupt them depend on it.
- **C3 varies most.** Where no blocking hook exists, the strongest available substitute is a
  wrapper script that performs the transition and refuses when a gate fails — that is, make the
  transition itself the gated action rather than trying to gate the agent's intent.
- **The workspace is already portable.** `tracker/` and `docs/` are plain markdown and the
  scripts are standard-library Python, so a project can be handed between runtimes without
  migration. Keep it that way: an adapter that stores state outside the workspace breaks the
  property that makes the methodology worth having.
