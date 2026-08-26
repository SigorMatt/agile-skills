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
- [x] **META-024** — skill `implement`.
- [x] **META-025** — skill `verify`.
- [x] **META-026** — skill `review-close`.
- [x] **META-027** — skill `answer-questions`.
- [x] **META-028** — skill `next` (orchestrator).

## Phase 3 — `scripts/`

- [x] **META-030** — `scripts/lib/` shared helpers (mini-YAML reader, frontmatter parser, findings printer).
- [x] **META-031** — `scripts/lint-skills` — validates every `skill.yaml` against `spec/skill-contract.md`,
      checks `process.md` structure, and enforces "no runtime names under `methodology/` or `spec/`".
- [x] **META-037** — `scripts/lib/workspace.py` — one loader/model shared by every script that
      reads a workspace, so the validator and the board can never disagree about a file.
- [x] **META-032** — `scripts/validate-workspace` — validates a consumer workspace against `spec/`.
- [x] **META-033** — `scripts/board-gen` — regenerates `tracker/board.md`.
- [x] **META-034** — `scripts/workspace-init` + `scripts/new-item` — schema-correct skeletons
      for a workspace and for an item, including derive-next-ID.
- [x] **META-036** — gate scripts `scripts/check-commit-refs` (every commit on an item branch
      references the item ID) and `scripts/check-verify-freshness` (DoD D10: verification
      postdates the last commit).
- [x] **META-035** — `scripts/check` — repo self-gate running all of the above + render determinism.

## Phase 4 — adapters

- [x] **META-040** — `adapters/README.md` — the adapter contract (capabilities, renderer inputs, conformance).
- [x] **META-041** — `adapters/claude-code/render.py` — renderer: methodology → Claude Code skills.
- [x] **META-042** — `scripts/run-gate` + `scripts/transition` — gate execution and the gated
      status change (runtime-neutral half of hard enforcement).
- [x] **META-045** — `adapters/claude-code/` hook config, install/uninstall scripts, and the
      adapter README with the gate enforcement table.
- [x] **META-043** — Rendered output committed under `adapters/claude-code/dist/`; determinism check wired
      into `scripts/check`. (done as part of META-041)
- [x] **META-044** — Deliberate failing-gate demonstration (evidence for acceptance B3).

## Phase 5 — consumer docs

- [x] **META-050** — `CONSUMER-PROMPT.md`.
- [x] **META-051** — `USAGE.md`.
- [x] **META-052** — `README.md` (project story, layout, roadmap).

## Phase 6 — end-to-end proof (`examples/toy-project/`)

- [x] **META-060** — Choose toy project; write raw idea + simulated-human answer key
      (`examples/toy-project/HUMAN-SCRIPT.md`).
- [x] **META-061** — Run `intake` + `refine` (context-free subagent; builder plays the human).
- [x] **META-062** — Run `plan` for the first work item.
- [x] **META-063** — Run `implement` (must organically raise an upstream question).
- [x] **META-064** — Run `answer-questions` (question round trip completes).
- [x] **META-065** — Run `verify` (files a BUG).
- [x] **META-066** — Drive the BUG through the pipeline to done.
- [x] **META-067** — Run `review-close`; complete remaining items until the epic is done.
- [x] **META-068** — `scripts/validate-workspace` green on the toy workspace; `board.md` regenerated.
- [x] **META-069** — Audit test by a fresh subagent → `examples/toy-project/AUDIT.md`.

## Phase 7 — close

- [x] **META-070** — Acceptance sweep: re-verify every box in `seed/03-ACCEPTANCE.md` with evidence.
- [x] **META-071** — `meta/FINAL-REPORT.md`.

## Acceptance checklist mirror (`seed/03-ACCEPTANCE.md`)

Filled in at META-070. Every box carries a pointer to evidence, and the boxes that are **not**
met say so rather than being argued into a tick.

### A. Methodology completeness
- [x] **A1** all 8 skills valid; `scripts/lint-skills` passes — `./scripts/check` step 2, "8 skill
      contracts, 0 errors". Negative-tested at META-031: six injected faults, six reported.
- [x] **A2** `pipeline.yaml` full status graph; `next` matches it — 10 statuses, 17 transitions;
      **no non-terminal status without an owner**, cross-checked in both directions by
      `lint-skills` (`ownership.unclaimed` / `ownership.race`).
- [x] **A3** `spec/` complete — 9 files: skill contract, work item, journal+history, question,
      doc header, IDs/statuses, DoR/DoD, workspace layout, index.
- [x] **A4** no runtime names under `methodology/` or `spec/` — enforced by `lint-skills`'
      `runtime-neutrality` scan; negative-tested at META-031.

### B. Adapter
- [x] **B1** renderer produces valid skills for all 8; docs URLs recorded — `dist/MANIFEST.md`;
      `meta/adr/ADR-0001` records every URL and the fetch date, plus what could **not** be
      confirmed.
- [x] **B2** install path documented and tested — `adapters/claude-code/README.md` §2;
      installed into a scratch project with a pre-existing `settings.json` (foreign hook and
      permissions both survived), re-installed idempotently, uninstalled cleanly; then installed
      into the toy project and used for the entire run.
- [x] **B3** gates hard-enforced; failing case demonstrated — `meta/evidence/gate-failure-demo.md`
      with a reproducible script: a failing `tests-pass` refuses `planned → in-progress`, the
      status is unchanged afterwards, the hook denies the bypass, and the identical command
      succeeds once the cause is fixed.
- [x] **B4** adapter contract complete enough for a Codex CLI adapter — `adapters/README.md`,
      five capabilities and a 12-box conformance checklist; §6 records the two questions that
      implementer will hit first.

### C. End-to-end proof
- [x] **C1** toy project idea → done using only rendered skills — `examples/toy-project/`;
      6 items and an epic, all `done`; 244 lines of tool, 77 tests.
- [x] **C2** executed by context-free subagents — every stage run by a subagent restricted to the
      project directory, given only the installed skills and `CONSUMER-PROMPT.md`.
- [x] **C3** every skill exercised, incl. a full `answer-questions` round trip — six questions
      filed by `plan`, `implement`, `verify` and `review-close`; the blocking one suspended
      WI-0003 (`in-review → awaiting-answer`, `resume-to: in-review`), the architect answered it
      from the record, `vision.md` went to v3, and the item resumed at exactly the recorded
      status. It arose organically from `spec/doc-header.md` §5, not from the exercise.
- [x] **C4** a `verify`-filed BUG reaches done — three of them (BUG-0001/2/3), all filed by an
      independent regression pass, all `done` with `outcome: delivered` and `found-in: WI-0001`,
      each with a regression test demonstrated to fail against the pre-fix build.
- [x] **C5** `validate-workspace` green; board renders — 7 items, 11 documents, 0 errors,
      0 warnings; `tracker/board.md` regenerated and staleness-checked.
- [x] **C6** audit test passes → `AUDIT.md` — a fresh agent restricted to the tracker, docs, git
      log and source reconstructed all four questions and gave a **qualified** sign-off, naming
      six specific defects the review layers missed.

### D. Consumer readiness
- [x] **D1** `USAGE.md` complete — install, workspace init, permissions for long runs (including
      the `dontAsk` warning), running, reading the trail, resuming, and debugging.
- [x] **D2** `CONSUMER-PROMPT.md` is the prompt actually used — byte-identical to the copy placed
      in the toy project and used for every run.
- [x] **D3** `README.md` project story — with an explicit "what this is not".

### E. Hygiene
- [x] **E1** clean incremental history with META refs — every commit references a META unit.
- [x] **E2** journal + ADRs + BLOCKERS + FINAL-REPORT — `meta/journal.md` covers every unit
      including the six defects the runs exposed; 5 ADRs; `BLOCKERS.md` empty as expected.

### Not met, stated plainly

- **The Definition of Ready override path was never exercised.** It was attempted deliberately
  at META-070b and `refine` **refused to record a false override**, correctly: no criterion was
  actually failing. That produced R10 instead — a real improvement to the checklist — but the
  override path itself remains untested. Carried to `meta/FINAL-REPORT.md`.
- **`blocked` was never reached.** No run hit an impasse no skill could resolve, so that status
  and its recovery path are unexercised.
- **`verifying → in-progress` (a verification send-back) never fired**, nor did
  `in-review → in-progress` (a review rejection). Both are specified and neither has run.

---

## Phase H — the two-session iteration harness

Mission: `meta/harness/HARNESS-PROMPT.md`, design: `meta/harness/DESIGN.md`, queue:
`meta/harness/PROJECT-QUEUE.md`. Same unit discipline as every phase above.

- [x] **META-072** — Phase H plan + `ADR-0005`: headless Claude Code specifics confirmed against
      the current docs and the installed CLI (flags, permission modes, model per invocation,
      transcript capture), and the harness's own architectural choices.
- [x] **META-073** — `harness/provision.py` — mechanical throwaway-project setup, idempotent,
      refuses a non-empty unexpected directory. Verified by provisioning a real project and
      running `validate-workspace` in it.
- [x] **META-074** — `harness/skills/simulated-human/` — `SKILL.md`, `personas/`, `probes/`
      (queue entries 1–4), and the SIM-LOG protocol including planted-vs-organic tagging.
- [x] **META-075** — `harness/prompts/` — versioned worker and sim turn prompts, including the
      F-008 interim async protocol for the worker.
- [x] **META-076** — `harness/run_iteration.py` — the driver: turn alternation, driver-computed
      status, stop conditions, iteration log, per-turn transcript capture.
- [x] **META-077** — contamination assertions + `harness/tests/` — the audit fires on deliberate
      violations (fixtures) and passes on clean transcripts; wired into `scripts/check`.
- [x] **META-078** — driver restart: resume an interrupted run from `state.json`; verified by
      killing a run mid-turn and rerunning.
- [x] **META-079** — `harness/USAGE.md`, verified by following it literally.
- [x] **META-080** — the mini end-to-end iteration on queue entry 1 (`expenses`), artefacts
      committed under `meta/harness/evidence/`.
- [x] **META-081** — findings F-011+ from the run, and `meta/harness/FINAL-REPORT.md`.

---

## Phase I — builder session two: work the findings ledger

Mission: `meta/BUILDER-2-PROMPT.md`. Backlog: `meta/findings/FINDINGS.md`. Same unit discipline.
Every unit names the finding(s) it closes; a finding is `fixed` only when execution proves it,
with a must-fail fixture for every enforcement change. Toolkit and harness commits stay separate.

### Cluster 1 — enforcement integrity
- [x] **META-082** — Phase I plan + checkpoint (this unit).
- [x] **META-083** — F-019: every script resolves the workspace root itself; process contracts
      forbid chaining `transition`; validator cross-checks journal `**Status:**` lines against
      `history.md` rows. Must-fail fixture for the divergence.
- [x] **META-084** — F-017 (mechanism): `scripts/journal-entry` is the only sanctioned writer
      of a journal entry — it stamps the heading from a clock read and the skill's own installed
      contract; `transition --journal-body-file` writes the history row and the entry from one
      clock read, so they cannot diverge. Spec forbids estimated timestamps and gives `journal.md`
      the restamp exception. Validator rejects entries stamped in the future or outside the
      workspace's git activity window. Must-fail fixtures.
- [x] **META-084b** — F-017 (adoption): every skill's `## Journaling` section uses the script;
      version bumps; re-render.
- [x] **META-085** — F-018: the write guard decides on the write target, not the command string.
      Fixtures both ways (mention allowed, write denied).
- [x] **META-086** — F-001: claim-provenance lint — factual justifications in ADRs/reviews/docs
      must cite an artifact; `validate-workspace` fails unsourced ones. Must-fail fixture.

### Cluster 2 — the acceptance loop
- [x] **META-087** — F-013: an epic becomes suspendable; pipeline.yaml terminal-status
      contradiction resolved; validator and intake agree. Must-fail fixture.
- [x] **META-088** — F-022: epic sign-off gate — `review-close` files a blocking human-addressed
      acceptance question; the epic cannot reach `done` until it is answered. Must-fail fixture.
- [x] **META-089** — F-021: stakeholder-initiated request artifact, detected and routed by `next`.

### Cluster 3 — pipeline/spec correctness
- [x] **META-090** — F-011 (`answer-questions` precondition), F-014 (gates run against the
      post-move state), F-015 (journal written with the status move), F-016 (epic-level record
      commits have a stated home).

> **Order change, 2026-08-22 (META-090):** cluster 6 runs before clusters 4 and 5. Iteration 1d
> is the regression gate for clusters 1, 2 **and** 6, and its expected shape — the sign-off gate
> fires and the sim answers it — depends on H-004 and H-007. Clusters 4 and 5 are the ones to
> drop if the session runs short, per the mission's own priority order.

### Cluster 4 — refine calibration
- [x] **META-091** — F-020 (grouped presentation per item per round) and F-023 (routing test:
      product-stake to the human, implementation-only decided and recorded, standing deferrals
      honoured by category).

### Cluster 5 — consumer readiness
- [x] **META-092** — F-002 (.gitkeep), F-003 (.gitignore), F-005 (uninitialised state),
      F-004 + F-012 (USAGE corrections).
- [x] **META-093** — F-007: `scripts/export` with profiles.
- [x] **META-094** — F-009: README positioning.

### Cluster 6 — harness
- [x] **META-095** — H-002 (resumable vs terminal stop classes; honest `--fresh` hint) and
      H-003 (`provision.py --wipe` / true-fresh semantics, documented).
- [x] **META-096** — H-004 (answers-pending schedules a sim turn first), H-007 (the sim gets a
      closing turn before any epic-done stop is accepted), H-005 (killed-turn cost + stale-status
      handling) and H-006 (bounded skill executions per worker turn). Merged into one unit:
      all four are the driver's turn loop and its prompt, and splitting them would mean two
      commits touching the same twenty lines.

### The regression gate
- [x] **META-098** — re-render, `./scripts/check` green including every new must-fail fixture.
- [x] **META-099** — iteration 1d configured (`iteration-1d-expenses`, fresh project
      `expenses-1d`, 1c's setup plus a stakeholder who refuses every alternative) and run.
- [x] **META-100** — findings pass over 1d's trail; anything new filed as F-024+/H-008+.
- [x] **META-101** — FINDINGS.md statuses current; `meta/FINAL-REPORT-2.md`.

---

## Phase II — builder session 2.5 (`meta/BUILDER-2.5-PROMPT.md`)

A compact fix session between builder two and iteration 2: derive the termination model once
(the F-013 class: F-029, F-045, F-046), close the correctness findings that would corrupt
iteration 2's evidence (F-028, F-031, F-034, F-038), and prove both on iteration 1e.

Riding along **open on purpose** — F-008, F-030, F-035, F-036, F-043, F-048. Scope discipline
outranks completeness in a .5 session.

### The derivation

- [x] **META-102** — `meta/adr/ADR-0006-termination-model.md`: every legal ending of an
      engagement, every mid-flight event that changes the item set, the termination gate, and
      the creation-authority table. Derivation only; no code.
- [x] **META-103** — spec re-derived from ADR-0006: `ids-and-statuses.md` (epic endings, the
      transition table, creation authority), `work-item.md` (`arose-from`, the
      `delivered-partial` outcome), `dor-dod.md` (DE1 and DE7 generalised), `question.md`
      (sign-off = the termination question; `status: deferred`, F-028).
- [ ] **META-104** — `pipeline.yaml` 0.4.0: transitions gain `applies_to` and `gated`; the epic
      ending rows; creation rows carry `provenance`. New `lint-skills` rules; must-fail cases.
- [ ] **META-105** — enforcement: `scripts/engagement-state` (is the engagement at rest?),
      `check-epic-signoff` as the **termination** gate (fires on every ending; names every child
      not delivered — F-045, F-046), `transition` gating for an epic's ending moves,
      `validate-workspace` for provenance, deferred questions and epic-outcome honesty.
- [ ] **META-106** — skill contracts re-derived: `review-close` (ends the engagement),
      `answer-questions` (deferral), `next` (the close-out step), `refine`/`verify` creation
      authority. Version bumps, re-render.
- [ ] **META-107** — fixtures both ways: every historical contradiction as a case — F-013's epic
      suspension, F-029's two occurrences, F-045's impasse, F-046's unshown bug — plus a
      must-pass `fixtures/ended-engagement/`. Wired into `./scripts/check`.

### The correctness batch

- [ ] **META-108** — F-031 (DoR R8 reads a field, not a filename), F-034 (`plan` and scaffolding
      — resolved by ADR either way), F-038 (the committed-invalid window, stated in
      `spec/skill-contract.md` §2.3).
- [ ] **META-109** — ledger statuses current with real commit citations; `./scripts/check` green
      end to end, rendered output current.

### The regression gate

- [ ] **META-110** — iteration 1e configured (1d's config and probe unchanged, project
      `expenses-1e`, max-turns 18) and run.
- [ ] **META-111** — findings pass over 1e's trail; anything new filed as F-049+/H-###.
- [ ] **META-112** — `meta/FINAL-REPORT-2.5.md`, with the go/no-go for iteration 2.
