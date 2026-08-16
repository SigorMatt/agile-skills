# 01 — Requirements

"MUST" items are binding for this build. "LATER" items must not be built now, but nothing may be designed in a way that blocks them.

## R1 — The skill set (v1 pipeline)

MUST deliver these skills, each with a full contract and procedure per `02-ARCHITECTURE.md`:

| # | Skill | Role persona | Purpose |
|---|-------|--------------|---------|
| 1 | `intake` | Product analyst | Turn a raw idea into epic + initial work items in the tracker |
| 2 | `refine` | Product analyst + human | Interactively grill the human until an item meets the Definition of Ready |
| 3 | `plan` | Architect | Produce design/ADR + implementation plan; may question the human |
| 4 | `implement` | Developer | Execute the plan; code + tests on a branch; raise questions upstream when blocked |
| 5 | `verify` | QA engineer | Independently validate against requirements and gates; file bugs |
| 6 | `review-close` | Reviewer | Code/docs review, Definition of Done validation, merge, close item |
| 7 | `answer-questions` | Architect | Triage open questions from downstream skills; answer or escalate to human |
| 0 | `next` (orchestrator) | Scheduler | Pick the next runnable action from workspace state and dispatch the right skill |

MUST: `next` contains zero engineering knowledge — it reads tracker state, consults `pipeline.yaml`, dispatches, and updates status. Nothing else.

## R2 — Human interaction protocol

- MUST: `intake` and `refine` are **interactive**: they question the human directly in-session (batched, focused questions; challenge vague answers; record the full Q&A verbatim in the tracker before proceeding). Refinement ends only when the Definition of Ready checklist passes or the human explicitly overrides (override is journaled).
- MUST: `plan` MAY ask the human directly when a design decision materially depends on intent the docs do not capture. Preference order: (1) answer from existing docs, (2) make a reversible assumption and record it, (3) ask the human. Every question asked and every assumption made is recorded.
- MUST: `implement` and `verify` NEVER ask the human directly. They file question artifacts addressed to the architect (see R4). The `answer-questions` skill answers from context where possible and escalates to the human only when necessary; answers flow back down as updated docs/plans, not as chat lore.
- MUST: while any blocking question is open, the affected item's status is `awaiting-answer` and the orchestrator will not advance it.

## R3 — Workspace: filesystem Jira + Confluence

MUST specify and validate a workspace layout (created inside the *consumer's* project) that mimics a real team's tooling using only markdown + git:

- `tracker/` — Jira-equivalent: epics, work items, bugs; each with YAML frontmatter (id, type, title, status, priority, epic, timestamps, links), an append-only status **history**, and per-item directories holding all artifacts for that item.
- `docs/` — Confluence-equivalent: product docs (vision, PRD), architecture docs (overview, ADRs), process docs. Each doc carries a version header and a change log; git provides the diffs.
- MUST: statuses, transitions, ID formats, and file schemas are formally specified (see `02-ARCHITECTURE.md`) and enforced by a validation script (`scripts/validate-workspace`), so drift is caught mechanically.
- MUST: a generated `tracker/board.md` gives a human an at-a-glance Kanban snapshot of all items and statuses.

## R4 — Paper trail (reviewable and debuggable)

For every skill execution, MUST produce:

1. A **journal entry** in the item's `journal.md` (append-only): timestamp, skill name+version, persona, inputs read, key decisions with rationale, commands executed with outcomes, gate results (pass/fail per gate), resulting status, and pointers to artifacts produced.
2. **Status history** appended to the item (`from → to`, by which skill, when, why).
3. **Questions** as first-class artifacts: `questions/Q-###.md` with frontmatter (from-skill, addressed-to: architect|human, blocking: true|false, status: open|answered), the question body, and — later — the answer and its consequences (which docs/plans were updated).
4. **Git commits** that reference the work item ID, so `git log --grep WI-0007` reconstructs an item's entire code history.

Quality bar: a human reading only the tracker + docs + git log must be able to answer "what happened, in what order, why, and who (which skill) decided it" for any item — the same audit a manager could do on a well-run human team.

## R5 — Claude Code adapter

- MUST: a build step (`adapters/claude-code/`) that renders every methodology skill into a valid, installable Claude Code skill, and an `install` script/instruction that places them into a target project.
- MUST: rendered skills follow current Claude Code conventions (verify against official docs at build time — frontmatter fields, discovery path, description-based triggering). Descriptions must be written to trigger reliably ("pushy" phrasing listing concrete situations), and bodies must use progressive disclosure: keep SKILL.md lean and reference the contract/checklists as bundled resource files rather than inlining everything.
- MUST: gate enforcement uses the strongest mechanism the runtime offers (e.g., hooks or executable gate scripts that must exit 0), with prompt-level instruction only as a fallback. Document which gates are hard-enforced vs. convention.
- MUST: `adapters/README.md` defines the **adapter contract**: the capabilities any runtime adapter must map (skill discovery/triggering, interactive human questioning, gate execution, optional subagent spawning) and how the renderer consumes `skill.yaml` + `process.md`. LATER: `adapters/codex-cli/` implements this contract; nothing in the design may assume Claude Code is the only runtime.

## R6 — Consumer onboarding

MUST deliver:

- `USAGE.md` — install rendered skills into a fresh project, initialize the workspace, configure permissions for long autonomous runs, run the pipeline, read the paper trail, resume after interruption.
- `CONSUMER-PROMPT.md` — the exact kickoff prompt for the consumer session: it instructs that session to initialize the workspace, run `intake` + `refine` interactively with the human on their idea, then loop `next` autonomously until the epic is done or a human-addressed question opens, and to surface the board and open questions whenever it pauses.

## R7 — Proof

MUST: `examples/toy-project/` — a small but real project (e.g., a CLI utility) driven from idea to done through the rendered skills, executed by context-free subagents, committed with its complete paper trail. This is both the acceptance test and reference documentation of what a correct run looks like.

## Out of scope for v1 (LATER)

Sprint ceremonies (planning/review/retro), estimation, multi-item parallelism, retro-driven self-improvement of skills, CI/CD integration, Codex CLI adapter, real Jira/Confluence sync.
