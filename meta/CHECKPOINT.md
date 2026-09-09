# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator session holds only the mission, `meta/plan.md`, this file, and
each unit's verdict. Per unit: checkpoint the intent → dispatch with scope, files to read,
definition of done, and the obligation to commit AND push → verify cheaply (git log for the
sha, `./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## The gate is GREEN at 5e6434d

META-146's spec change and META-147's contract change are both in, and the dist is re-rendered.
`./scripts/check: all steps passed`.

## Current unit

**META-147b** — the two contracts ADR-0010 touches that META-147 did not own.

META-147 flagged these rather than leaving them to be rediscovered as a finding:

- `methodology/skills/intake/` — ADR-0010 §3.2 row **L1**: `intake` writes the **initial**
  `## Engagement state` section into the documents it creates. It is the only skill that writes
  a K8 sentence outside the ending.
- `methodology/skills/answer-questions/` — §3.2 row **L7**: the K1–K4 write, under
  `spec/doc-header.md` §4a's obligations (a quantified claim it propagates needs its
  enumeration; it may not write a K8 sentence, which is the ending's).

- Done when: both contracts + their `process.md` carry the rows, semver bumped, `pipeline.yaml`
  updated if a handoff changes, dist re-rendered, `./scripts/check` green, journalled,
  committed AND pushed.
- Next unit: **META-148** (the enforcement half — `scope.py`'s fourth state,
  `check-verify-freshness`, `lint-claims --plan-documents`, and the must-fail fixtures).

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
- **META-146** — the two spec files carry it (**c1fbde8**). §5's absolute removed; §4a gains the
  three-kind claim table, the definition of a *checked* claim, the audit row, the enumeration
  obligation and the `## Engagement state` convention. `dor-dod.md`: D7 confirms against the
  set, D12/DE6 gain enumeration and exclude K8, DE4 gains the ending's restatement, **D13** is
  new (`binding-adrs` completeness, `[skill]` — no mechanical half exists yet).
- **META-147** — four contracts + `pipeline.yaml` + dist (**5e6434d**), gate green.
  Bumps: `plan` 0.4.1→0.5.0, `implement` 0.3.0→0.4.0, `verify` 0.2.0→0.3.0, `review-close`
  0.6.0→0.7.0, `pipeline.yaml` 0.6.0→0.7.0 — all minor.
  **Where the new outputs live** (META-148 writes fixtures against these): three new sections of
  `tracker/items/<ID>/artifacts/plan.md` — `## Invalidation set`
  (`| document | what | kind | why | disposition |`; kind ∈ `cited-fact`|`quantified`|
  `engagement-state`; disposition ∈ `to-update`|`verified-still-true`|`owned-by-ending`|
  `question-filed:<ITEM>/Q-###`; an empty set is one row saying `none`, an absent section is not
  an empty one), `## Deliverable documents`, `## Binding ADRs`. Consumers: `impl-report.md`
  gains `## Documents`; `verify-report.md` gains `## ADR conformance` and `## Invalidation set`;
  `review.md` gains `## Invalidation set confirmation` and `## Sections restated at the ending`
  — deliberately NOT `## Engagement state`, because that literal is the delimiter a script
  enumerates and an item artifact carrying one would plant a K8 section inside a record.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5 is a HELD-OUT calibration engagement: this
  session does not run it and does not read its probe beyond provision-verification.
