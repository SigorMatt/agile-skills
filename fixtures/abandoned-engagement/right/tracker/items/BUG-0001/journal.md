# Journal — BUG-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-06T12:10:00Z — verify v0.5.1 — qa-engineer

- **Item:** BUG-0001
- **Trigger:** the orchestrator dispatched verify on BUG-0001
- **Inputs read:** `tracker/items/BUG-0001/item.md`, its history and its artifacts
- **Decisions:** found while verifying WI-0001; a bug with reproduction steps is already ready
- **Questions raised:** none
- **Commands:** `scripts/transition BUG-0001 --to ready`
- **Gates:**
  - `tests-pass` → **pass** (recorded by the execution that made this move)
  - `lint-clean` → **pass** (recorded by the execution that made this move)
  - `workspace-valid` → **pass** (recorded by the execution that made this move)
  - `every-criterion-independently-checked` → **pass** (recorded by the execution that made this move)
  - `negative-cases-exercised` → **pass** (recorded by the execution that made this move)
  - `a-criterion-about-criteria-is-read` → **pass** (recorded by the execution that made this move)
  - `adr-conformance-is-decided` → **pass** (recorded by the execution that made this move)
  - `invalidation-set-is-disposed` → **pass** (recorded by the execution that made this move)
  - `tests-would-fail-without-the-change` → **pass** (recorded by the execution that made this move)
- **Artifacts:** `tracker/items/BUG-0001/history.md`
- **Status:** created at `ready`
- **Result:** found while verifying WI-0001; a bug with reproduction steps is already ready

## 2026-09-06T16:00:00Z — plan v0.6.1 — architect

- **Item:** BUG-0001
- **Trigger:** the orchestrator dispatched plan on BUG-0001
- **Inputs read:** `tracker/items/BUG-0001/item.md`, its history and its artifacts
- **Decisions:** a documented impasse: the rounding rule is the stakeholder's to choose and no skill may choose it for them
- **Questions raised:** none
- **Commands:** `scripts/transition BUG-0001 --to blocked`
- **Gates:**
  - `workspace-valid` → **pass** (recorded by the execution that made this move)
  - `every-criterion-is-addressed` → **pass** (recorded by the execution that made this move)
  - `project-commands-resolved` → **pass** (recorded by the execution that made this move)
  - `decisions-recorded` → **pass** (recorded by the execution that made this move)
  - `plan-is-executable-without-you` → **pass** (recorded by the execution that made this move)
  - `documents-at-risk-are-enumerated` → **pass** (recorded by the execution that made this move)
  - `cross-answer-consistency` → **pass** (recorded by the execution that made this move)
  - `claims-are-sourced` → **pass** (recorded by the execution that made this move)
- **Artifacts:** `tracker/items/BUG-0001/history.md`
- **Status:** `ready` → `blocked`
- **Result:** a documented impasse: the rounding rule is the stakeholder's to choose and no skill may choose it for them
