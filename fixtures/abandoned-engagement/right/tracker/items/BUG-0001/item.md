---
id: BUG-0001
type: bug
title: A three-way split loses a penny
status: blocked
priority: high
epic: EP-001
arose-from: WI-0001
found-in: WI-0001
created: 2026-09-06T12:10:00Z
updated: 2026-09-06T16:00:00Z
---

## Summary

Splitting an amount three ways loses a penny.

## Steps to reproduce

1. Split 10.00 three ways.
2. Add the three shares back up.

## Expected behaviour

The three shares add back up to the original amount.

## Actual behaviour

They add up to 9.99.

## Acceptance criteria

- [ ] AC1 — the three shares sum to the original amount
