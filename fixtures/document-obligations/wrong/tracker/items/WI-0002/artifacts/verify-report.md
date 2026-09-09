# Verification report — WI-0002

Verified-commit: 0000000000000000000000000000000000000000

## Verdict

Passed.

## ADR conformance

| ADR | verdict | clause quoted from its Decision | file and line, or why not engaged |
|---|---|---|---|
| ADR-0001 | conforms | it says the store path is read once | src/store.py |
| ADR-0002 | looked at it | — | — |
| ADR-0003 | not-engaged | — | this change does not order anything |
| the ordering one | conforms | "rows are ordered before they are written" | src/store.py:41 |

## Invalidation set

| document | disposition | what I reopened, and what I found |
|---|---|---|
| `docs/product/vision.md` | to-update | the sentence now names the new path |
