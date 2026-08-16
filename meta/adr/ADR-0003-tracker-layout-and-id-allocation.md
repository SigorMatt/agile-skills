# ADR-0003 — Uniform item directories, and IDs derived from the filesystem

- **Status:** accepted
- **Date:** 2026-08-16
- **Unit:** META-010

## Context

`seed/02-ARCHITECTURE.md` §3 fixes the ID formats and shows one per-item directory
(`tracker/items/WI-0007/`). It does not say where epics and bugs live, nor how the next number
in a sequence is chosen. Both are decisions a validator and an orchestrator have to agree on
exactly, so they are made here rather than left to whichever skill writes first.

## Decision 1 — every tracked entity gets the same directory shape

Epics, work items and bugs all live at `tracker/items/<ID>/`, with the same file set:
`item.md`, `journal.md`, `history.md`, `questions/`, `artifacts/`. The `type` frontmatter field
distinguishes them; the ID prefix agrees with it.

Alternatives considered:

- `tracker/epics/EP-001/` + `tracker/items/WI-0001/` + `tracker/bugs/BUG-0001/`. Reads more like
  Jira's mental model, and was rejected: it triples the traversal logic in
  `validate-workspace`, `board-gen` and the orchestrator, and each of those three would have to
  re-learn "which directories hold trackable things" — the exact kind of duplicated knowledge
  that drifts.
- Flat files (`tracker/items/WI-0001.md`) with journals in a parallel tree. Rejected because it
  separates an item from its own artifacts, and R4 wants everything for an item in one place a
  reviewer can open.

Consequences: one glob (`tracker/items/*/`) enumerates the whole tracker. An epic carries a
journal and a history for free, which turns out to matter — `intake` needs somewhere to record
how a raw idea became this set of items, and that record belongs to the epic.

## Decision 2 — the next ID is derived from the filesystem, not from a counter

To allocate an ID, scan for the highest existing number of that kind and add one. Items that
are `done` still count. There is no `.counters` file.

Rejected: a counter file. It is a second source of truth. The failure it invites is specific and
likely here: a session dies between incrementing the counter and creating the directory (PROMPT
rule 9 exists precisely because sessions die mid-unit), and afterwards nothing in the workspace
reveals that the counter is ahead. The next allocation silently skips a number, which is
harmless, or a partially-created directory is retried and collides, which is not.

Derivation has one real cost: it requires IDs never to be reused, so a deleted item would free
its number and let a later item inherit its `git log --grep WI-0007` history. The spec closes
that by forbidding deletion outright — an abandoned item is closed with `outcome: dropped`.

## Decision 3 — `awaiting-answer` records the status it suspends

The status graph has one node with more than one legal exit that depends on history rather than
on state: `awaiting-answer`. Rather than infer the return status (say, from which skill filed
the question), the history entry stores it explicitly and `answer-questions` restores it.

The inference version was tried on paper and fails an obvious case: `verify` files a blocking
question, and inference would return the item to `verifying`, which happens to be right — but
`review-close` filing a question would return the item to `verifying` too, discarding a
completed verification. Explicit is one field; inference is a bug per calling skill.
