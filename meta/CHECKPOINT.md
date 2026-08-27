# CHECKPOINT

## Current unit: META-116 — F-055: name the mechanism the trial merge needs

META-113/114 closed F-050; META-115 closed F-049. All pushed, `./scripts/check` green at 18
assertions across 16 steps.

**Intent of this unit.** `review-close` step 8 says to trial-merge into *"a throwaway copy of
`{{trunk}}`"* and never says how. A run used `git worktree add /tmp/trial4 main`, which checks
out the **real** branch in a second directory rather than copying it, so the trial merge
fast-forwarded the real `main` — and removing the worktree did not move it back. It was the only
finding in iteration 1e that caused real damage. `check-commit-refs` caught it, the worker
rewound, and turn 13 used `--detach`.

- Step 8.1 names the command sequence literally, with one line on why `--detach` is the whole of
  it: a detached worktree has no branch to advance, so the merge has nowhere to land but a
  temporary HEAD.
- Step 8.2 becomes "discard the trial **and check the trunk did not move**" — `git rev-parse
  {{trunk}}` before and after — and a self-check entry says the same thing.
- `review-close` 0.4.1 → **0.5.0** (MINOR: a required action inside a step, not a rewording).

**The must-fail case, tied to the contract text.** A new `scripts/check` step extracts the fenced
command block from `review-close`'s own `process.md`, runs it against a throwaway git repository,
and asserts the trunk sha is unchanged — then runs the same sequence with `--detach` removed and
asserts the trunk **does** move. Extracting from the contract is what makes it a gate rather than
a demonstration: drop `--detach` from the procedure and the step fails.

## The units of this session

- [x] **META-113** — F-050 part 1: the obligation registry and its gate.
- [x] **META-114** — F-050 part 2: a deferral returns an epic to `open`.
- [x] **META-115** — F-049: the `**Status:**` bullet, tool and prose.
- **META-116** — F-055 (this unit).
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
