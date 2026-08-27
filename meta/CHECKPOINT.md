# CHECKPOINT

## Phase III is complete. There is no next unit.

Builder micro-session 2.6 closed the three findings `meta/FINAL-REPORT-2.5.md` §9 named as
conditions on the iteration-2 go, and nothing else. Everything is on `main` and pushed. Read
**§11 of `meta/FINAL-REPORT-2.5.md`** first — the closing note, not a new report.

Where things stand:

- **F-050 fixed** (`a0e7db5`, `e1c55e9`) — the class before the instance. `pipeline.yaml` 0.5.0
  carries `rule_obligations`: a validator rule that requires an item to be at one of a fixed set
  of statuses declares the item types it applies to and the transition that satisfies it.
  `validate-workspace` reads that scope; `lint-skills` checks it against the transition table
  both ways. The instance: a deferred blocking question returns an **epic** to `open`, because
  `blocked` on an epic is the E3 ending and only `review-close` reaches it.
- **F-049 fixed** (`5b615ec`) — the `**Status:**` bullet is the transition tool's, so a body
  passed to it need not carry one. Standalone `journal-entry` still requires it; a body missing
  a bullet the tool does not write is still refused. Seven `## Journaling` sections rewritten.
- **F-055 fixed** (`63f8917`) — `review-close` 0.5.0 prints `git worktree add --detach ...` and
  requires a `git rev-parse` of the trunk before and after. The must-fail case is extracted from
  the contract's own fenced block.
- `./scripts/check`: **19 assertions across 17 steps**, all passing.
- Findings: **49 fixed, 15 open**, 1 rejected, 1 deferred.

## What the owner does next

**Launch `iteration-2-tidy`.** §9's go stands and its three conditions are met. `tidy` has no
blocked seed, so it should reach a **clean** ending (E1 or E2) — 1e exercised E3 only, and three
of the four endings still have no run behind them. It also has an adversarial DoR-override
variant, and the epic-level deferral F-050 was filed against is now a legal, tested path rather
than a trap.

Do **not** start the Codex adapter or the content packs: ROADMAP §2 condition 1 (a full consumer
run with zero version bumps) does not hold, and this session bumped eight contracts.

The fifteen open findings — F-008, F-030, F-035, F-036, F-043, F-048 and F-051…F-060 minus the
three closed here — ride along into iteration 2's evidence and are prioritised by what that run
does with them.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** `origin` is
  `git@github.com:SigorMatt/agile-skills.git`; `main` tracks it.
- **Never record a commit sha by amending the commit being cited** (F-024).
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- **Do not modify the toolkit while a harness run is in flight.** `meta/` and `harness/` are
  exempt from the W4 rule; everything else trips it.
- Every change traces to an F-### or H-###. Behavioural skill change ⇒ version bump. Spec change
  ⇒ a `## Revisions` row **appended in order** — twice now the row has been inserted above the
  one before it. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture, and — where a rule could be satisfied
  vacuously — a fixture proving it can be passed. Where the rule *is* a written procedure, the
  case reads the commands out of the contract, so editing the contract breaks the gate (F-055).
- **When you add a rule, enumerate the item types it applies to.** A program does this now for
  status rules (`rule_obligations`); nothing does it for the next shape of rule.
- Toolkit commits and harness commits stay separate.
