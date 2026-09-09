# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator session holds only the mission, `meta/plan.md`, this file, and
each unit's verdict. Per unit: checkpoint the intent → dispatch with scope, files to read,
definition of done, and the obligation to commit AND push → verify cheaply (git log for the
sha, `./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## The gate is GREEN at 5ae1539 — 31 steps

`./scripts/check: all steps passed`. `fixtures/broken-workspace` still emits **82 codes**
(unchanged, the migration proof). `scripts/lib/selftest.py` is now **273** cases.

## Current unit

**META-148b** — the enforcement half, part 2: the **obligations**.

Build the gate script(s) that decide the eight `[auto]` obligations META-147/147b had to write
as `manual_check`, then flip those gates from `manual_check` to `command` in the contracts.
Follow the `claims.py` / `lint-claims` shape: one implementation in `scripts/lib/`, one gate
script over it — the same rule must not live in two places.

### The eight obligations, currently `manual_check`
 — currently `manual_check`, ADR-0010 marks them `[auto]`

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

### What META-148 deliberately left to this unit

`lint-claims` reads the invalidation set's `document` column and reports rows it cannot resolve
(`plan.row.malformed`, `plan.document.unreadable`), but it does **not** validate the `kind` or
`disposition` enums — that is obligations 11 and 13, and duplicating the check would put one
rule in two places. `check-verify-freshness` likewise prints plan-shape errors without failing
on them.

- Done when: each obligation has a must-fail fixture and a must-pass counterpart, the contracts
  name real commands, `./scripts/check` green with the broken-workspace count unchanged at 82
  unless a change to it is argued for, journalled, committed AND pushed.
- Next units: **META-148c** (the historical cases as fixtures), then **META-149** (findings
  statuses, including the two edges below).

## Two edges META-148 named rather than solved — META-149 files or dispositions them

- **(a)** `implement`'s widened window includes entries disposed `owned-by-ending`, which
  `implement` may read but not write. A pre-existing unsourced absolute in such a document would
  block `implement` **with no legal repair**. It cannot arise while `review-close`'s
  `--context epic` whole-tree run is green, so it is a real edge and not a present one.
- **(b)** `lint-claims` rule 2 still reads only under `docs/`, so a deliverable document declared
  **outside** `docs/` is in the window but never examined. `claim.plan.document-absent` catches
  the missing-file case, not this one.

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

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5 is a HELD-OUT calibration engagement: this
  session does not run it and does not read its probe beyond provision-verification.
