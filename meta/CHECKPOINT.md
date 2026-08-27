# CHECKPOINT

## Phase II is complete. There is no next unit.

Builder session 2.5 derived the termination model, closed the correctness batch, and ran
iteration 1e as its regression gate. Everything is on `main` and pushed. Read
[`meta/FINAL-REPORT-2.5.md`](FINAL-REPORT-2.5.md) first.

Where things stand:

- **ADR-0006** derives the four legal endings of an engagement, the termination gate, and the
  creation-authority table. **ADR-0007** resolves `plan`'s scaffolding conflict. F-013's class —
  F-029 (+F-042), F-045, F-046 — is closed by derivation rather than by exception.
- **46 findings fixed**, each citing a commit `./scripts/check` verifies. **18 open**, 1 rejected,
  1 deferred.
- `./scripts/check`: **16 assertions across 14 steps**, all passing — including three new ones:
  the termination gate at every ending, the pipeline invariants under injected faults, and the
  derived model exercised by execution against a real workspace.
- **Iteration 1e** ended at E3, the impasse, **through the stakeholder** — the sign-off fired
  naming every child, the stakeholder refused, and the ending was recorded on the epic. 20 turns,
  $100.23, zero contamination violations. Banked at `meta/harness/evidence/iteration-1e/`,
  read-only.

## What the owner does next

**The report's verdict is GO for iteration 2** (`iteration-2-tidy`), with three conditions:

1. **Fix F-050 first** — an epic-level question cannot legally be `deferred`. It is a live
   contradiction, it was introduced by this session, and `tidy`'s adversarial stakeholder is
   exactly the kind to produce an epic-level deferral.
2. **Fix F-049** — five `## Journaling` sections say the tool *writes* the `**Status:**` bullet
   when it *requires* it. Six failed transitions in one run; a one-word fix.
3. **Fix F-055** — `review-close` says "trial-merge into a throwaway copy of the trunk" without
   saying how, and `git worktree add <path> main` advanced the real trunk. Name `--detach`.

Then run `iteration-2-tidy`. It has no blocked seed, so it should reach a **clean** ending (E1 or
E2) — 1e exercised E3 only, and three of the four endings still have no run behind them.

Do **not** start the Codex adapter or the content packs: ROADMAP §2 condition 1 (a full consumer
run with zero version bumps) does not hold and is not close.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** `origin` is
  `git@github.com:SigorMatt/agile-skills.git`; `main` tracks it.
- **Never record a commit sha by amending the commit being cited** (F-024). Commit the work, then
  record the sha in a follow-up commit. `scripts/check` enforces it — and note that the step
  itself was blind to the plural `commits a, b, c` form until META-109.
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- **Do not modify the toolkit while a harness run is in flight.** `meta/` and `harness/` are
  exempt from the W4 rule; everything else trips it.
- Every change traces to an F-### or H-###. Behavioural skill change ⇒ version bump. Spec change
  ⇒ a `## Revisions` row. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture, and — where a rule could be satisfied
  vacuously — a fixture proving it can be passed.
- **New, from F-050:** when you add a rule, enumerate the item types it applies to, and check it
  against the transitions that are legal for each. That is the one check that would have caught
  this session's own defect.
- Toolkit commits and harness commits stay separate.
