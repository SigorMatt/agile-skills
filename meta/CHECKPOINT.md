# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator session holds only the mission, `meta/plan.md`, this file, and
each unit's verdict. Per unit: checkpoint the intent → dispatch with scope, files to read,
definition of done, and the obligation to commit AND push → verify cheaply (git log for the
sha, `./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## The gate is GREEN at 9adff0e

`./scripts/check: all steps passed`. Cluster 1's derivation, specs and six contracts are in.
What remains of cluster 1 is the **enforcement half** — the scripts that decide the obligations
ADR-0010 marks `[auto]` but nothing implements yet — split into three units because the
accumulated to-do list is too large for one.

## Current unit

**META-148** — the enforcement half, part 1: the **window**.

1. **`scripts/lib/scope.py` gains a fourth state**, *out-of-scope-by-construction* — distinct
   from "a real window that is empty". Its docstring's three-state model and its justification
   ("real and empty is a pass **because the comparison could have found something**") are
   directly falsified by F-076 and must be rewritten, not patched around.
2. **`scripts/lint-claims --plan-documents <ITEM-ID>`** — the flag does not exist;
   `implement`'s `claims-are-sourced` gate already names it:
   `scripts/lint-claims --changed-since {{trunk}} --plan-documents {{item.id}}`.
   Semantics the contract assumes: the rule-2 window is the branch diff **plus** every path in
   that item's `## Invalidation set` **plus** its `## Deliverable documents`.
   (`lint-claims`' parser already takes `--flag value`, so the form parses.)
3. **`scripts/check-verify-freshness`** (~line 94): the `path.startswith("docs/")` exemption
   must subtract the item's declared deliverable documents — a document that IS the deliverable
   is not record, and treating it as record is F-058.

- Done when: all three land with fixtures **both ways** (a case that must fail and a case that
  must pass), a new `./scripts/check` step proving it, `./scripts/check` green, journalled,
  committed AND pushed.
- Next units: **META-148b** (the eight `[auto]` obligations, listed below, still written as
  `manual_check`), then **META-148c** (the historical cases as fixtures), then **META-149**
  (findings statuses).

### The eight obligations META-148b owns — currently `manual_check`, ADR-0010 marks them `[auto]`

| gate | contract | ADR-0010 obligation |
|---|---|---|
| `documents-at-risk-are-enumerated` | `plan` | 11 |
| `document-writes-are-declared` | `implement` | 13 + 19 |
| `adr-conformance-is-decided` | `verify` | 15 |
| `invalidation-set-is-disposed` | `verify` | 13 |
| `engagement-state-is-restated` | `review-close` | 6–8 |
| `engagement-state-is-delimited` | `intake` | 6 |
| `engagement-state-is-left-to-the-ending` | `answer-questions` | 7 |
| `propagated-claims-carry-their-obligation` | `answer-questions` | 3 |

Obligation 10 — whether a K8 sentence was *written into* its section rather than left loose —
has **no mechanical half at all**, and the whole K8 mechanism rests on it. It stays `[skill]`.
Do not let a unit quietly claim it.

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

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5 is a HELD-OUT calibration engagement: this
  session does not run it and does not read its probe beyond provision-verification.
