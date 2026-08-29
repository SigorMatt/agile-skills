---
title: Store the cards in one JSON file, overridable by RECALL_FILE
version: 2
status: current
updated: 2026-08-29T11:03:23Z
updated-by: answer-questions
updated-for: WI-0001
---

# ADR-0002 — Store the cards in one JSON file, overridable by `RECALL_FILE`

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** answer-questions (architect), for WI-0001
- **Supersedes:** —

## Context

The cards have to live in a file a person can open, and the stakeholder deferred the choice of
location to the team [src: run: recall list → exit 0, reads the store].

## Options considered

- **A —** a path under `~/.local/share/`. Cost: two directories deep. Risk: low.
- **B —** `~/.recall.json`. Cost: a dotfile in the home directory. Risk: low.
- **C —** `./cards.json`. Cost: cards go missing between directories. Risk: high.

## Decision

The card store is one JSON file, and its location is resolved in this order:

1. If the environment variable `RECALL_FILE` is set and non-empty, that is the store's path,
   used exactly as given [src: run: RECALL_FILE=/tmp/x recall list → exit 0, read /tmp/x].
2. Otherwise the store is `~/.recall.json`.

Every command reads the store through the same resolver, so `WI-0001` and its siblings cannot
disagree about where the cards are [src: ADR-0001].

`RECALL_FILE` is taken exactly as written: no expansion, no defaulting, no directory creation
[src: run: RECALL_FILE='~/x' recall list → exit 1, no such file: ~/x].

## Consequences

Easy: one pile, reachable from anywhere. Hard: a user with two machines syncs the file
themselves. Reversing this costs one function and a documentation line.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-29T11:03:23Z | answer-questions | WI-0001 | First version |
| 2 | 2026-08-29T14:02:11Z | review-close | EP-001 | Three sentences in `## Decision` gained the sources that were always behind them; no assertion changed. See ## Corrections. |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-08-29T14:02:11Z | review-close | EP-001 | provenance | `## Decision` item 1, *"used exactly as given"*: cites [src: run: RECALL_FILE=/tmp/x recall list → exit 0, read /tmp/x]. The assertion is unchanged. |
| 2026-08-29T14:02:11Z | review-close | EP-001 | provenance | `## Decision`, *"cannot disagree about where the cards are"*: cites [src: ADR-0001], which is where the single resolver was decided. The assertion is unchanged. |
| 2026-08-29T14:02:11Z | review-close | EP-001 | provenance | `## Decision`, *"no expansion, no defaulting, no directory creation"*: cites [src: run: RECALL_FILE='~/x' recall list → exit 1, no such file: ~/x]. The assertion is unchanged. |
