# Plan — WI-0002

## Steps

1. Rename the store path.

## Invalidation set

| document | what | kind | why | disposition |
|---|---|---|---|---|
| `docs/product/vision.md` | the sentence naming `store.py` | cited-fact | the path changes | to-update |
| `docs/architecture/overview.md` | the shape of the loader | quantified | a module is added | — |

## Deliverable documents

- none

## Binding ADRs

- ADR-0001 — the store path is read from one place
- ADR-0002 — rows are ordered before they are written
- ADR-0004 — errors are reported, never swallowed
