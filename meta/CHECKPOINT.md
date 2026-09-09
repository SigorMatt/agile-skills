# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator session holds only the mission, `meta/plan.md`, this file, and
each unit's verdict. Per unit: checkpoint the intent → dispatch with scope, files to read,
definition of done, and the obligation to commit AND push → verify cheaply (git log for the
sha, `./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## CLUSTER 1 IS COMPLETE at f474027 — 34 steps green

`./scripts/check: all steps passed`; `findings citations resolve (49 cited)`; 82 codes
unchanged; selftest 290. The document-as-deliverable derivation is built, specified, contracted,
enforced, fixtured and settled in the ledger. Cluster 2 opens now.

## Current unit

**META-150** — `meta/adr/ADR-0011-stakeholder-silence-and-abandonment.md`. Derivation only.

Nothing in this pipeline can currently declare a stakeholder gone. E4 (`abandoned`) is a legal
ending in `spec/ids-and-statuses.md` §3.5 and in ADR-0006 §1, and it is **fixture-only** — the
ROADMAP §2 stamp records E2 and E4 as never executed. Derive:

1. **A silence threshold** — measured in rest-time or in unanswered rounds, **stated in
   `pipeline.yaml`** so the orchestrator and the gate cannot disagree about it (the same
   argument `ids-and-statuses.md` §3.5 makes for `scripts/engagement-state` being a program).
2. **The abandonment decision, owned by `review-close`** — an ending statement listing
   delivered children and orphaned ones **by ID**, DE-style, mirroring E2/E3.
3. Where E4 differs from E3: E3 is *the stakeholder did not accept*; E4 is *the stakeholder
   never answered*. Both leave children not `done`. Say what distinguishes them in the record,
   and how a reader tells them apart later.

- Done when: the ADR exists in the ADR-0006 shape, E4's row in ADR-0006 §1 and
  `ids-and-statuses.md` §3.5 are **reconciled, not contradicted** (if the derivation changes
  what E4 means, say so and amend explicitly), the enforcement boundary is stated per obligation,
  `./scripts/check` green, journalled, committed AND pushed.
- Next units: **META-151** (the mechanism: pipeline.yaml, dor-dod.md, review-close,
  engagement-state, check-epic-signoff), **META-152** (`fixtures/abandoned-engagement/`),
  **META-153** (harness — separate commit).

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
- **META-147b** — `intake` 0.3.0→0.4.0 and `answer-questions` 0.4.0→0.5.0 carry ADR-0010's rows
  L1 and L7 (**9adff0e**); `pipeline.yaml` untouched, because the rows change what a skill writes
  inside a document, not when an item may move. Two decisions kept: `intake` gets **no**
  `lint-claims` gate (at intake there is usually no code to cite, so that window would be empty
  by construction on nearly every execution — F-076's exact shape), the obligation is an exit
  criterion instead; and when a human's answer falsifies a K8 sentence, `answer-questions`
  **records it and leaves it** — the question's `## Consequences` names the document, the
  section and the sentence, and the plan's invalidation set gets the row disposed
  `owned-by-ending`. Nothing is lost, because `review-close` restates every section it finds.
  A seam it closed on its own initiative and flagged: an `answer-questions` execution
  propagating into `docs/` mid-flight puts paths there that `implement` never wrote, so
  `answer-questions` records those rows itself, disposed `to-update`. **Accepted as it stands.**
- **META-148** — the window (**5ae1539**), 31 steps green, 82 codes unchanged, selftest 252→273.
  `scope.py` now has **four** states, and the third is the one F-076 needed: *real and
  non-empty* → examine; *real and empty* → pass, saying the window **was searched**;
  ***out-of-scope-by-construction*** → **pass with a mark** (exit 0, a `claim.scope.by-construction`
  warning, and the scope line `NOTHING COULD HAVE BEEN IN SCOPE`) — exit 0 deliberately, because
  an item with no documents is ordinary work and a gate that fails on ordinary work is one
  somebody switches off; the honesty lives in the wording; *degenerate* → fail (F-066,
  unchanged). `constrained(window, permitted, reason)` is the only way into the third state and
  it takes the permission knowledge from the caller — **no diff can distinguish "nobody wrote a
  document" from "nobody was allowed to"**. `--plan-documents <ITEM>` widens the rule-2 window to
  the diff + invalidation set + deliverable documents; `check-verify-freshness` subtracts the
  deliverable documents from its `docs/` exemption (F-058). The new step was **proved
  non-vacuous**: stashed against the old scripts, five of its eight cases failed, each reporting
  `0 document(s) in 0 path(s)` — the empty window F-076 is about.
- **META-148b** — `scripts/lib/documents.py` + `scripts/lint-documents --rule <name>` decide
  **all eight** `[auto]` obligations (**a843114**); 34 steps, 82 codes unchanged, selftest 290.
  Every gate flipped from `manual_check` to a real command, and **each command decides less than
  the manual_check text it replaced** — the narrowing is written into each gate's own
  `description`. Bumps: `plan` 0.6.0, `implement` 0.5.0, `verify` 0.4.0, `review-close` 0.8.0,
  `intake` 0.5.0, `answer-questions` 0.6.0; `doc-header.md` revision 6 (the enumeration's
  labelled form — obligation 3 needed a *findable* form to be a shape check at all, so it was
  written into the spec rather than left as an unwritten form a gate enforced).
  **Non-vacuity proved twice**: with the script moved aside, and again with the script present
  but every `rule_*` body replaced by `return` — the second is the one that proves the
  assertions are sensitive to the rules and not merely to the file existing.
  **A contradiction between two META-147 outputs, found and corrected here**: `verify/skill.yaml`
  said a conformance row for an ADR the plan does not name *fails* the gate, while
  `verify/process.md` asks for exactly such a row. Refusing it would make the honest move
  illegal (F-050's shape). The procedure's version was implemented; the row is
  `document.adr.row.unplanned`, a **warning**, being evidence that `binding-adrs` was incomplete
  — which is D13, `review-close`'s read.
- **META-149** — cluster 1's ledger (**f474027**), append-only proved mechanically (358
  insertions, **0 deletions**), citations 43 → **49 cited**, every new sha verified with
  `git log -1` before being written (F-024's discipline).
  **Fixed, each with its resolving citation:** F-076, F-087, F-092, F-093, F-095, F-057, F-058
  — and F-057/F-058's statuses say **in those words** that the deferral's gate was met, because
  a deferral whose gate is met and not noticed is how a backlog rots.
  **F-053 is NOT fixed**: ADR-0010 consumed its class as the lifecycle-state input (the
  two-state-machines constraint) without resolving it; `transition` still has no `--outcome`, so
  `review-close` still exits non-zero on a successful transition. It stays in *half-written
  record* with F-036/F-043/F-051.
  **META-148 and META-148b filed contradictory reports about the `owned-by-ending` edge, and
  META-148 was right** — established **by execution** in a throwaway repo, not by reading: two
  hard gates on `implement` are jointly unsatisfiable there, with no legal repair but `--force`.
  META-148b's rebuttal was true of a different rule on a different skill (`lint-documents`'
  new-paragraphs scoping), while `lint-claims` rule 2 walks **every** prose paragraph in the
  window. Filed as **F-100**. Also filed: **F-101** (a deliverable document outside `docs/` is
  inside the window and outside the rule — F-052/F-066's shape reintroduced, proved by
  execution), **F-102** (obligation 10, open and *known, derived and accepted*), **F-103** (a
  universal carried by a bare plural is recognised by nothing — with a correction that
  ADR-0010's own illustration of it is wrong, because `each` IS in `QUANTIFIER_RE`).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5 is a HELD-OUT calibration engagement: this
  session does not run it and does not read its probe beyond provision-verification.
