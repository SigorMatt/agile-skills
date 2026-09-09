# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator session holds only the mission, `meta/plan.md`, this file, and
each unit's verdict. Per unit: checkpoint the intent → dispatch with scope, files to read,
definition of done, and the obligation to commit AND push → verify cheaply (git log for the
sha, `./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## The gate is GREEN at a843114 — 34 steps

`./scripts/check: all steps passed`. `fixtures/broken-workspace` still **82 codes**.
Library self-test **290** cases. Cluster 1 is complete except for its findings statuses.

**META-148c was absorbed, not skipped.** Its content — the derivation's historical cases run as
fixtures — already landed as two by-execution steps (*the document window (F-076, F-058, 8
cases)* and *the document obligations by execution (F-087, F-093, F-095, 8 cases)*), each proved
non-vacuous against the pre-change scripts. Re-authoring them would put one assertion in two
places. What is left of it is F-053's class, which is a status decision and belongs below.

## Current unit

**META-149** — cluster 1's findings statuses, with resolving citations.

Every status must cite what settles it — the ADR section, the spec revision, the contract
version, the `./scripts/check` step. `meta/findings/FINDINGS.md` is **appended to, never
rewritten**: existing finding text stays, the new status and its reasoning go below it.

Settle from the derived model:

- **F-076** — `implement`'s claims gate examines an empty window by construction. Settled:
  `doc-header.md` §5's absolute does not hold, the gate stays on `implement`, the window widened
  (`--plan-documents`), and `scope.py` gained *out-of-scope-by-construction*.
- **F-087** — the invalidation set is a `plan` output and the falsification question is asked
  where the change is made.
- **F-093** — engagement-state sections are owned by the ending.
- **F-095** — quantified claims need member enumeration recorded in the audit row.
- **F-092** — `verify` decides ADR conformance per ID; `review-close` checks only that
  `binding-adrs` is complete (D13).
- **F-057, F-058** — the two founding members of the *document-as-deliverable* class. The class
  was deferred behind "an ADR-0006-shaped derivation"; that gate has now been met.
- **F-053** — NOT fixed here. Its *class* was the lifecycle-state input to ADR-0010; record what
  it contributed and what remains, and leave it in the *half-written record* class (F-036,
  F-043, F-051) behind its named gate. Do not mark it fixed.

Also file or disposition the **two edges META-148 named** and the **two reaches META-148b
declared**, so none is rediscovered later as a fresh finding:

1. `implement`'s widened window can include an `owned-by-ending` document it may read but not
   write; a pre-existing unsourced absolute there would block it with no legal repair. META-148b
   reports this is **avoided by construction** — the quantified rule reads only paragraphs *new*
   in the diff — so check that claim before filing, and file only what survives it.
2. A deliverable document declared **outside** `docs/` is in the window but never examined
   (`lint-claims` rule 2 reads only under `docs/`).
3. **Obligation 10 is not claimed by anything** — whether a K8 sentence was written into its
   section rather than left loose. `fixtures/document-obligations/wrong/docs/process/
   ways-of-working.md` holds such a sentence that no rule fires on, deliberately.
4. Obligation 5's partial reach: a universal phrased without a quantifier word is caught by
   nothing.

- Done when: every cluster-1 finding has a current status with a resolving citation, the four
  items above are filed or dispositioned, `./scripts/check` green (step *findings citations
  resolve* included), journalled, committed AND pushed.
- Next unit: **META-150** — cluster 2 opens: ADR-0011, the silence threshold and E4.

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

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5 is a HELD-OUT calibration engagement: this
  session does not run it and does not read its probe beyond provision-verification.
