---
title: One environment variable
version: 1
status: accepted
updated-by: plan
updated-for: WI-0001
updated: 2026-08-16T09:00:00Z
---

# ADR-0001 — One environment variable

## Context

The store location has to be configurable without a configuration file.

## Options considered

- **A —** a single environment variable. Cost: none. Risk: no per-profile override.
- **B —** a configuration file. Cost: a parser and a search path. Risk: more to get wrong.

## Decision

A single variable, `EXPENSES_STORE`. Nothing else in the tool reads the environment
[src: WI-0001 AC1].

## Consequences

Reversible: adding a configuration file later is additive, and this ADR would be superseded
rather than edited.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-16T09:00:00Z | plan | WI-0001 | First version |
