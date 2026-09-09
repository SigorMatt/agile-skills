# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator session holds only the mission, `meta/plan.md`, this file, and
each unit's verdict. Per unit: checkpoint the intent → dispatch with scope, files to read,
definition of done, and the obligation to commit AND push → verify cheaply (git log for the
sha, `./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## !! The gate is RED, knowingly, and META-147 is what closes it

`./scripts/check` fails **one** step at c1fbde8: `rendered output is current` — META-146 changed
`spec/doc-header.md` and `spec/dor-dod.md`, and `adapters/claude-code/dist/agile-skills/spec/`
still holds the pre-change copies. `render.py` copies `spec/*` verbatim, so the re-render is
mechanical. Every other step passes. A fresh session resuming here should NOT treat this as a
regression: run `adapters/claude-code/render.py` as part of META-147.

## Current unit

**META-147** — the skill contracts carry ADR-0010, then re-render.

ADR-0010's contract-level to-dos, verbatim from its own reckoning:

7. `methodology/skills/implement/skill.yaml` — the `claims-are-sourced` window becomes
   diff **+** invalidation set **+** deliverable documents (it is `--changed-since {{trunk}}`
   today). This is F-076's fix at the contract level; the `lint-claims` half is META-148.
8. `methodology/skills/plan/skill.yaml` — new outputs: the **invalidation set**,
   `deliverable-documents`, `binding-adrs`; exit criteria to match (F-087).
9. `methodology/skills/verify/skill.yaml` — new gate: a per-ADR conformance verdict
   (`conforms` / `violates` / `not-engaged`) per binding ADR, in `verify-report.md`; plus
   checking the invalidation set's dispositions. `verify` writes no document — that stays,
   now derived (F-092).
10. `methodology/skills/review-close/skill.yaml` — the ending contract gains the K8
    restatement, D7 becomes confirmation against the set, and D13 (`binding-adrs`
    completeness) joins its criteria (F-093).

Plus: `methodology/pipeline.yaml` where these outputs are handed between skills; semver bumps
on every contract touched; `adapters/claude-code/render.py` re-run and the dist committed.

**The K8 delimiter is `## Engagement state`, exactly one section per document.** META-146
concretised it (the ADR named no literal shape); contracts and scripts must use that exact
heading or change it in `spec/doc-header.md` §4a in the same commit.

- Done when: the four contracts + `pipeline.yaml` carry the derivation, dist re-rendered,
  `scripts/lint-skills` clean, **`./scripts/check` green again**, journalled, committed AND
  pushed.
- Next unit: **META-148** (the enforcement half — `scope.py`'s fourth state,
  `check-verify-freshness`, `lint-claims`' window, and the must-fail fixtures).

## Done this session

- **META-144** — Phase VI laid out in `meta/plan.md` (2c4b0b7, 0deafc0).
- **META-145** — `meta/adr/ADR-0010-document-as-deliverable.md`, 699 lines (**3701069**).
  Binding decisions: `doc-header.md` §5 **does not hold**, the claims gate **stays on
  `implement`** (F-076); record-vs-deliverable is a property of **sentences**, not files; **K8**,
  the engagement-state statement, is a third claim kind **owned by the ending** (F-093); the
  **invalidation set** is a `plan` output consumed by `implement`, `verify`, `review-close`,
  `check-verify-freshness` and the claims window (F-087); a **quantified** claim discharges only
  by member enumeration in the audit row (F-095); **`verify`** decides ADR conformance per ID,
  `review-close` checks only that `binding-adrs` is complete (F-092). Residual gap, named and
  unsolved: a false sentence found **after** the engagement closes has no owner.
- **META-146** — the two spec files carry it (**c1fbde8**). `doc-header.md` §5's absolute
  removed; §4a gains the three-kind claim table, the definition of a *checked* claim, the audit
  row, the enumeration obligation and the `## Engagement state` convention. `dor-dod.md`: D7
  becomes confirmation against the invalidation set, D12/DE6 gain enumeration and exclude K8,
  DE4 gains the ending's restatement, **D13** is new (`binding-adrs` completeness, `[skill]`).
  Both Revisions tables stamped 2026-09-10.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5 is a HELD-OUT calibration engagement: this
  session does not run it and does not read its probe beyond provision-verification.
