# CLAUDE.md — persistent session anchor

This repository is being built per the mission in `PROMPT.md`. If you are reading this without the mission in context (fresh session, or after compaction), read `PROMPT.md`, then `meta/CHECKPOINT.md` and `meta/plan.md`, before doing anything else.

Non-negotiable habits (full definitions in PROMPT.md rules 9–10):
- Work in small committable units; `meta/CHECKPOINT.md` is overwritten with intent BEFORE each unit starts.
- Never leave the working tree dirty between units.
- State lives in files, never in conversation history. Re-read files instead of recalling them.

## Compact Instructions

When compacting this conversation, preserve verbatim:
1. The current work unit: its META-### reference and where execution stands relative to `meta/CHECKPOINT.md`.
2. The instruction that the authoritative state is on disk — `PROMPT.md`, `meta/plan.md`, `meta/CHECKPOINT.md`, `meta/journal.md` — and must be re-read after this compaction before further action.
3. Any not-yet-journaled decision or discovery from the current unit (so it can be journaled immediately after compaction).

Do not spend summary space on file contents, tool output, or completed units — all of that is recoverable from the repository.
