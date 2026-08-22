---
title: Architecture overview
version: 1
status: current
updated-by: plan
updated-for: WI-0001
updated: 2026-08-16T09:00:00Z
---

# Architecture overview

The tool reads no environment beyond `EXPENSES_STORE`. [src: src/store.py]

That citation names a file this workspace does not have, which is F-001's failure with a
decoration on it: the sentence looks sourced and is not.

`format_report` only ever renders rows it is handed, and nothing else in the system may write
to `tracker/board.md`.

The paragraph above is the shape the audit found — an absolute claim about a named identifier,
carrying no citation at all.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-16T09:00:00Z | plan | WI-0001 | First version |
