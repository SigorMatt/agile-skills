---
title: The store is read once per command
version: 1
status: current
updated: 2026-08-29T10:00:00Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0001 — The store is read once per command

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

Every command needs the whole card list, and the file is small.

## Options considered

- **A —** read once at start-up. Cost: the file is re-read between commands. Risk: low.
- **B —** keep an open handle. Cost: locking. Risk: a stale handle after an external edit.

## Decision

Read the file once, at the start of each command.

## Consequences

Easy: no locking. Hard: nothing. Reversing this is cheap — the read is one function.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-29T10:00:00Z | plan | WI-0001 | First version |
