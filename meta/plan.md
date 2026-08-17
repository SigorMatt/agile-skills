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
