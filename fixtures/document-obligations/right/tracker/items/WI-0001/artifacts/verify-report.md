# Verification report — WI-0001

Verified-commit: 0000000000000000000000000000000000000000

## Verdict

Passed.

## ADR conformance

| ADR | verdict | clause quoted from its Decision | file and line, or why not engaged |
|---|---|---|---|
| ADR-0001 | conforms | "The store path is read from one place and passed down." | src/store.py:14 |

## Invalidation set

| document | disposition | what I reopened, and what I found |
|---|---|---|
| `docs/product/vision.md` | to-update | the sentence names the new constant, and the version is 3 |
| `docs/architecture/overview.md` | verified-still-true | reopened the loader paragraph; still true at the branch head |
