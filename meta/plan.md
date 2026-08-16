# Build plan — agile-skills v1

Each `META-###` is ONE committable work unit (PROMPT.md rule 9). Tick a box only with a
pointer to evidence (commit, script output, artifact path).

Legend: `[ ]` todo · `[~]` in progress · `[x]` done

## Phase 0 — Build scaffolding

- [x] **META-001** — `git init`, `meta/` scaffolding (plan, journal, CHECKPOINT, BLOCKERS), `.gitignore`.
- [x] **META-002** — Verify current Claude Code skill format against official docs; record findings +
      URLs in `meta/adr/ADR-0001-claude-code-skill-format.md`. (PROMPT rule 6)
- [x] **META-003** — ADR-0002: scripting language & dependency policy for `scripts/`; `scripts/lib/`
      skeleton with a self-test.

## Phase 1 — `spec/` (single source of truth, runtime-neutral)

- [x] **META-010** — `spec/README.md` (spec index + conventions) and `spec/ids-and-statuses.md`
      (ID formats, status set, legal transitions, actor rules).
- [x] **META-011** — `spec/work-item.md` (item.md frontmatter + body schema, incl. epics & bugs).
- [x] **META-012** — `spec/journal-and-history.md` (journal entry schema, history entry schema).
- [x] **META-013** — `spec/question.md` (question artifact schema + protocol).
- [x] **META-014** — `spec/doc-header.md` (docs/ version header + change log schema, ADR schema).
- [x] **META-015** — `spec/dor-dod.md` (Definition of Ready, Definition of Done checklists).
- [x] **META-016** — `spec/skill-contract.md` (skill.yaml schema, process.md requirements).
- [x] **META-017** — `spec/workspace-layout.md` (full consumer workspace tree + required files).

## Phase 2 — `methodology/`

- [x] **META-020** — `methodology/pipeline.yaml` (status graph, status→skill map, dispatch rules).
- [x] **META-021** — skill `intake` (skill.yaml + process.md).
- [x] **META-022** — skill `refine`.
- [x] **META-023** — skill `plan`.
- [ ] **META-024** — skill `implement`.
- [ ] **META-025** — skill `verify`.
- [ ] **META-026** — skill `review-close`.
- [ ] **META-027** — skill `answer-questions`.
- [ ] **META-028** — skill `next` (orchestrator).

## Phase 3 — `scripts/`

- [x] **META-030** — `scripts/lib/` shared helpers (mini-YAML reader, frontmatter parser, findings printer).
- [ ] **META-031** — `scripts/lint-skills` — validates every `skill.yaml` against `spec/skill-contract.md`,
      checks `process.md` structure, and enforces "no runtime names under `methodology/` or `spec/`".
- [ ] **META-032** — `scripts/validate-workspace` — validates a consumer workspace against `spec/`.
- [ ] **META-033** — `scripts/board-gen` — regenerates `tracker/board.md`.
- [ ] **META-034** — `scripts/workspace-init` — creates a fresh consumer workspace skeleton.
- [ ] **META-035** — `scripts/check` — repo self-gate running all of the above + render determinism.

## Phase 4 — adapters

- [ ] **META-040** — `adapters/README.md` — the adapter contract (capabilities, renderer inputs, conformance).
- [ ] **META-041** — `adapters/claude-code/render.py` — renderer: methodology → Claude Code skills.
- [ ] **META-042** — `adapters/claude-code/` gate scripts + hook config (hard enforcement) + install script.
- [ ] **META-043** — Rendered output committed under `adapters/claude-code/dist/`; determinism check wired
      into `scripts/check`.
- [ ] **META-044** — Deliberate failing-gate demonstration (evidence for acceptance B3).

## Phase 5 — consumer docs

- [ ] **META-050** — `CONSUMER-PROMPT.md`.
- [ ] **META-051** — `USAGE.md`.
- [ ] **META-052** — `README.md` (project story, layout, roadmap).

## Phase 6 — end-to-end proof (`examples/toy-project/`)

- [ ] **META-060** — Choose toy project; write raw idea + simulated-human answer key
      (`examples/toy-project/HUMAN-SCRIPT.md`).
- [ ] **META-061** — Run `intake` + `refine` (context-free subagent; builder plays the human).
- [ ] **META-062** — Run `plan` for the first work item.
- [ ] **META-063** — Run `implement` (must organically raise an upstream question).
- [ ] **META-064** — Run `answer-questions` (question round trip completes).
- [ ] **META-065** — Run `verify` (files a BUG).
- [ ] **META-066** — Drive the BUG through the pipeline to done.
- [ ] **META-067** — Run `review-close`; complete remaining items until the epic is done.
- [ ] **META-068** — `scripts/validate-workspace` green on the toy workspace; `board.md` regenerated.
- [ ] **META-069** — Audit test by a fresh subagent → `examples/toy-project/AUDIT.md`.

## Phase 7 — close

- [ ] **META-070** — Acceptance sweep: re-verify every box in `seed/03-ACCEPTANCE.md` with evidence.
- [ ] **META-071** — `meta/FINAL-REPORT.md`.

## Acceptance checklist mirror (`seed/03-ACCEPTANCE.md`)

Filled in during META-070; each box needs an evidence pointer, not an assertion.

### A. Methodology completeness
- [ ] A1 all 8 skills valid; `scripts/lint-skills` passes
- [ ] A2 `pipeline.yaml` full status graph; `next` matches it
- [ ] A3 `spec/` complete (contract, item, journal, history, question, doc header, IDs, DoR, DoD)
- [ ] A4 no runtime names under `methodology/` or `spec/`

### B. Adapter
- [ ] B1 renderer produces valid skills for all 8; docs URLs recorded in an ADR
- [ ] B2 install path documented and tested (discovery + triggering)
- [ ] B3 gates hard-enforced; deliberate failing case demonstrated and journaled
- [ ] B4 adapter contract complete enough to write a Codex CLI adapter

### C. End-to-end proof
- [ ] C1 toy project driven idea → done using only rendered skills
- [ ] C2 executed by context-free subagents
- [ ] C3 every skill exercised, incl. a full `answer-questions` round trip
- [ ] C4 a `verify`-filed BUG reaches done
- [ ] C5 `validate-workspace` green; `board.md` renders
- [ ] C6 audit test passes → `AUDIT.md`

### D. Consumer readiness
- [ ] D1 `USAGE.md` complete
- [ ] D2 `CONSUMER-PROMPT.md` is the prompt actually used
- [ ] D3 `README.md` project story

### E. Hygiene
- [ ] E1 clean incremental git history referencing META IDs
- [ ] E2 journal + ADRs + BLOCKERS + FINAL-REPORT
