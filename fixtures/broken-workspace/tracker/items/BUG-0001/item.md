---
id: BUG-0001
type: work-item
title: A bug whose type, status and outcome are each wrong
status: reviewing
priority: critical
epic: EP-001
created: 2026-08-16T12:00:00Z
updated: 2026-08-16T12:30:00Z
outcome: delivered
found-in: WI-0404
---

## Summary

The type says work-item, the status is not a status, and the outcome is set on an open item.

## Steps to reproduce

1. Run the validator against this fixture.

## Expected behaviour

Each defect is reported with its own code.

## Actual behaviour

See EXPECTED-CODES.txt.

## Acceptance criteria

- [ ] AC1 — the defects above are each reported
- [ ] AC2 — a regression test covers this fixture
