# Journal — WI-0003

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-06T12:05:00Z — intake v0.5.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** the orchestrator dispatched intake on WI-0003
- **Inputs read:** `tracker/items/WI-0003/item.md`, its history and its artifacts
- **Decisions:** refined from the idea
- **Questions raised:** none
- **Commands:** `scripts/transition WI-0003 --to draft`
- **Gates:**
  - `workspace-valid` → **pass** (recorded by the execution that made this move)
  - `epic-has-success-measures` → **pass** (recorded by the execution that made this move)
  - `an-open-question-was-asked` → **pass** (recorded by the execution that made this move)
  - `engagement-state-is-delimited` → **pass** (recorded by the execution that made this move)
  - `items-are-separable` → **pass** (recorded by the execution that made this move)
  - `no-solution-in-the-problem` → **pass** (recorded by the execution that made this move)
- **Artifacts:** `tracker/items/WI-0003/history.md`
- **Status:** created at `draft`
- **Result:** refined from the idea

## 2026-09-06T13:00:00Z — refine v0.3.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** the orchestrator dispatched refine on WI-0003
- **Inputs read:** `tracker/items/WI-0003/item.md`, its history and its artifacts
- **Decisions:** a documented impasse: the itemised bill format is the stakeholder's to supply
- **Questions raised:** none
- **Commands:** `scripts/transition WI-0003 --to blocked`
- **Gates:**
  - `workspace-valid` → **pass** (recorded by the execution that made this move)
  - `definition-of-ready` → **pass** (recorded by the execution that made this move)
  - `criteria-are-decidable` → **pass** (recorded by the execution that made this move)
  - `cross-answer-consistency` → **pass** (recorded by the execution that made this move)
  - `qa-recorded-verbatim` → **pass** (recorded by the execution that made this move)
- **Artifacts:** `tracker/items/WI-0003/history.md`
- **Status:** `draft` → `blocked`
- **Result:** a documented impasse: the itemised bill format is the stakeholder's to supply
