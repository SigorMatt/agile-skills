# Journal — WI-0004

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-06T09:05:00Z — intake v0.5.0 — product-analyst

- **Item:** WI-0004
- **Trigger:** the orchestrator dispatched intake on WI-0004
- **Inputs read:** `tracker/items/WI-0004/item.md`, its history and its artifacts
- **Decisions:** refined from the idea
- **Questions raised:** none
- **Commands:** `scripts/transition WI-0004 --to draft`
- **Gates:** all applicable gates ran and passed
- **Artifacts:** `tracker/items/WI-0004/history.md`
- **Status:** created at `draft`
- **Result:** refined from the idea

## 2026-09-06T09:45:00Z — refine v0.3.0 — product-analyst

- **Item:** WI-0004
- **Trigger:** the orchestrator dispatched refine on WI-0004
- **Inputs read:** `tracker/items/WI-0004/item.md`, its history and its artifacts
- **Decisions:** Definition of Ready passes
- **Questions raised:** none
- **Commands:** `scripts/transition WI-0004 --to ready`
- **Gates:** all applicable gates ran and passed
- **Artifacts:** `tracker/items/WI-0004/history.md`
- **Status:** `draft` → `ready`
- **Result:** Definition of Ready passes

## 2026-09-06T10:15:00Z — plan v0.6.0 — architect

- **Item:** WI-0004
- **Trigger:** the orchestrator dispatched plan on WI-0004
- **Inputs read:** `tracker/items/WI-0004/item.md`, its history and its artifacts
- **Decisions:** plan.md written
- **Questions raised:** none
- **Commands:** `scripts/transition WI-0004 --to planned`
- **Gates:** all applicable gates ran and passed
- **Artifacts:** `tracker/items/WI-0004/history.md`
- **Status:** `ready` → `planned`
- **Result:** plan.md written

## 2026-09-06T10:45:00Z — implement v0.5.0 — developer

- **Item:** WI-0004
- **Trigger:** the orchestrator dispatched implement on WI-0004
- **Inputs read:** `tracker/items/WI-0004/item.md`, its history and its artifacts
- **Decisions:** branch wi/WI-0004 created
- **Questions raised:** none
- **Commands:** `scripts/transition WI-0004 --to in-progress`
- **Gates:** all applicable gates ran and passed
- **Artifacts:** `tracker/items/WI-0004/history.md`
- **Status:** `planned` → `in-progress`
- **Result:** branch wi/WI-0004 created

## 2026-09-07T14:00:00Z — implement v0.5.0 — developer

- **Item:** WI-0004
- **Trigger:** the orchestrator dispatched implement on WI-0004
- **Inputs read:** `tracker/items/WI-0004/item.md`, its history and its artifacts
- **Decisions:** blocking question WI-0004/Q-001 filed: the currency column is undecided
- **Questions raised:** none
- **Commands:** `scripts/transition WI-0004 --to awaiting-answer`
- **Gates:** all applicable gates ran and passed
- **Artifacts:** `tracker/items/WI-0004/history.md`
- **Status:** `in-progress` → `awaiting-answer`
- **Result:** blocking question WI-0004/Q-001 filed: the currency column is undecided

## 2026-09-08T10:00:00Z — review-close v0.9.0 — reviewer

- **Item:** WI-0004
- **Trigger:** the orchestrator dispatched review-close on WI-0004
- **Inputs read:** `tracker/items/WI-0004/item.md`, its history and its artifacts
- **Decisions:** Orphaned in flight, suspended on a question nobody will answer. `awaiting-answer` is not suspendable, so the generic impasse row cannot reach it and `answer-questions`' deferral row needs a reply that is not coming: the move is `awaiting-answer → blocked`, actor `review-close`, which exists for exactly this (ADR-0011 §5).
- **Questions raised:** none
- **Commands:** `scripts/transition WI-0004 --to blocked`
- **Gates:** all applicable gates ran and passed
- **Artifacts:** `tracker/items/WI-0004/history.md`
- **Status:** `awaiting-answer` → `blocked`
- **Result:** orphaned by E4: the engagement was abandoned after 3 silent rounds against a threshold of 3; this item's work stops here and stays resumable
