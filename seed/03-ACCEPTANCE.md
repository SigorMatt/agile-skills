# 03 — Acceptance: Definition of Done for the builder session

The mission is complete only when every box below is checked, verified **by execution**, and the evidence is committed. Track this checklist in `meta/plan.md` and mark items only with a pointer to the evidence (script output, journal entry, or example artifact).

## A. Methodology completeness

- [ ] All 8 skills exist with valid `skill.yaml` + `process.md`; `scripts/lint-skills` validates every contract against `spec/skill-contract.md` and passes.
- [ ] `pipeline.yaml` defines the full status graph; every status has exactly one owning skill or is terminal; `next`'s algorithm matches it.
- [ ] `spec/` fully defines: skill contract, work item, journal entry, history entry, question, doc header, ID rules, Definition of Ready, Definition of Done.
- [ ] No file under `methodology/` or `spec/` mentions Claude Code or any runtime.

## B. Adapter

- [ ] Renderer produces valid Claude Code skills for all 8; current format confirmed against official docs (URLs recorded in an ADR).
- [ ] Install path documented and tested: rendered skills placed into a fresh project are discovered and trigger from natural task phrasing.
- [ ] Each declared quality gate is enforced by an executable mechanism (script/hook) — demonstrated by a deliberate failing case that blocks the transition, journaled in the toy project or meta journal.
- [ ] `adapters/README.md` adapter contract is complete enough that the Codex CLI adapter could be written without touching `methodology/`.

## C. End-to-end proof (`examples/toy-project/`)

- [ ] A small real project (builder's choice, e.g., a CLI utility with 2–3 work items) driven from raw idea → done using ONLY the rendered skills.
- [ ] Executed by context-free subagents given only the rendered skills + `CONSUMER-PROMPT.md`; for `refine`, the builder plays the human's role and marks simulated answers as such in the Q&A record.
- [ ] The run exercises every skill at least once, including `answer-questions`: at least one work item must organically raise an upstream question during implement/verify that flows through the full protocol (question filed → item `awaiting-answer` → architect answers → docs updated → work resumes).
- [ ] At least one `verify` run files a BUG that then flows to `done` through the pipeline.
- [ ] `scripts/validate-workspace` passes on the resulting workspace; `tracker/board.md` renders correctly.
- [ ] **Audit test**: a fresh subagent, given only the toy project's tracker + docs + git log, must correctly answer: What was built and why? What decisions were made and by which skill? What questions arose and how were they resolved? What did verify find? Its written answers are saved as `examples/toy-project/AUDIT.md`. If it cannot reconstruct the story, the paper trail requirement (R4) has failed — fix and re-run.

## D. Consumer readiness

- [ ] `USAGE.md` covers install, workspace init, permission setup for long autonomous runs, running, pausing/resuming, and how to read/debug the paper trail.
- [ ] `CONSUMER-PROMPT.md` exists and was the actual prompt used for the toy run (kept in sync with reality, not aspirational).
- [ ] `README.md` gives the project story for a future open-source audience: what it is, how it works, layout, and the iterate-and-deepen roadmap.

## E. Hygiene

- [ ] Git history is clean, incremental, and references META task IDs; no generated artifacts committed without their sources.
- [ ] `meta/journal.md` + ADRs cover the build; `meta/BLOCKERS.md` contains only genuinely deferred items with workarounds; `meta/FINAL-REPORT.md` written last.

## Iteration protocol (for the human, after this session)

Run a consumer session on a real demo app → review its paper trail → file findings as issues in this repo's `meta/` → a follow-up builder session fixes skills and bumps their versions → re-render → re-test. Skills carry semantic versions precisely so this loop is trackable.
