# CHECKPOINT

## Current unit: META-115 — F-049: the `**Status:**` bullet, prose against tool

META-113 and META-114 closed F-050 — the class (`rule_obligations`, checked against the
transition table) and the instance (a deferral returns an epic to `open`). Both pushed.

**Intent of this unit.** Every `## Journaling` section says the transition *"writes the
`**Status:**` bullet itself"*, which reads as *you need not write one*; `check_body` then
refuses a body without it. Six failed transitions across five turns and four skills in one run.

The mission says decide which side is right. **Both are, in different respects**, and the split
is what the worker's own complaint points at:

- **The tool.** `force_status_bullet` already appends the bullet when it is absent, so requiring
  the caller to supply one the tool immediately overwrites is a formality — the duplication
  F-019 was meant to remove. When a transition supplies the status line, a missing
  `**Status:**` bullet stops being an error, and the tool inserts its own before `**Result:**`.
  Standalone `journal-entry` keeps the requirement, because there nothing else would write it.
- **The prose.** Seven `## Journaling` sections say what the tool does inaccurately and say
  nothing about the bullets that are structurally mandatory (`**Commands:**` and
  `**Artifacts:**` refused an execution in the same run). Say what the body must carry, and
  point at `--template` as the answer rather than as a footnote.

Must-fail and must-pass, by execution: a body with no `**Status:**` bullet is accepted through
`transition` and the entry carries the move actually made; the same body is refused by
`journal-entry` on its own; and a body missing `**Gates:**` is still refused by both.

## The units of this session

- [x] **META-113** — F-050 part 1: the obligation registry and its gate.
- [x] **META-114** — F-050 part 2: a deferral returns an epic to `open`.
- **META-115** — F-049 (this unit).
- **META-116** — F-055: name `git worktree add --detach` in `review-close`, with the must-fail case.
- **META-117** — findings statuses with citations that resolve, `./scripts/check` green,
  `meta/FINAL-REPORT-2.5.md` §11.

Then **stop**. Do not run iteration 2 — the owner launches it.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- **Never record a commit sha by amending the commit being cited** (F-024).
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Every change traces to an F-### or H-###. Behavioural skill change ⇒ version bump. Spec change
  ⇒ a `## Revisions` row **appended in order**. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture, and — where a rule could be satisfied
  vacuously — a fixture proving it can be passed.
