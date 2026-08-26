---
id: WI-0003
type: work-item
title: An item created without provenance, carrying a deferred blocking question
status: draft
priority: medium
epic: EP-001
created: 2026-08-16T13:00:00Z
updated: 2026-08-16T13:10:00Z
outcome: delivered-partial
---

## Story

As a validator author, I want an item whose creation nobody can account for, so that the
creation-authority table is enforceable rather than advisory.

## Acceptance criteria

- [ ] AC1 — `item.arose-from.missing` fires: `answer-questions` created it and recorded nothing
- [ ] AC2 — `question.deferred.not-blocked` fires: a deferred blocking question, item at `draft`
- [ ] AC3 — `item.outcome.epic-only` fires: `delivered-partial` records how an *engagement*
  ended and is not a work item's to claim

## Out of scope

- Anything the other fixture items already cover.
