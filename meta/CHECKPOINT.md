# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator session holds only the mission, `meta/plan.md`, this file, and
each unit's verdict. Per unit: checkpoint the intent → dispatch with scope, files to read,
definition of done, and the obligation to commit AND push → verify cheaply (git log for the
sha, `./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## The gate is GREEN at 94606f5 — 34 steps. Cluster 1 complete; cluster 2 derived.

## Current unit

**META-151** — the E4 mechanism, part 1: the model on paper.

ADR-0011 §7 *"The changes this obliges, named"* lists them file by file. This unit takes the
spec and `pipeline.yaml` half; META-151b takes the programs.

- `spec/ids-and-statuses.md` §3.5's E4 row and `meta/adr/ADR-0006-termination-model.md` §1's
  E4 row — **amended**: E4 gains a **second route**, silence, alongside withdrawal. ADR-0006 is
  a standing ADR: repair it the legal way (`spec/doc-header.md` §4b, `## Corrections`), do not
  rewrite its decision.
- §3.4's `done → open` row: condition widened to §3.4's own prose (*a child item filed after
  closure*), so a **returning** stakeholder's request has a legal way back in.
- `spec/question.md` §2/§3 — the new `status: abandoned`, with an **empty** `## Answer`. Forced:
  leaving questions open deadlocks `next` step 3 for ever, and `answered`/`deferred` both assert
  a reply arrived.
- `spec/dor-dod.md` — DE7/DE8's E4 form is **asked, not answered**; DE4's trigger becomes *after
  the ending is determined* (this amends ADR-0010 §4.3 — say so).
- `spec/workspace-layout.md` — `tracker/waiting/<EP-ID>.md`, the append-only halt log.
- `methodology/pipeline.yaml` — the `termination.silence` block
  (`threshold_rounds`, default **3**), and **two new transition rows**, both F-050's shape found
  by derivation rather than by a run: `awaiting-answer → blocked` (`review-close`,
  work-item/bug — `awaiting-answer` is not suspendable, so the generic impasse row cannot reach
  it) and `awaiting-answer → done` (`review-close`, epic, gated).

- Done when: all of the above land, revisions rows appended, `./scripts/check` green,
  journalled, committed AND pushed.
- Next units: **META-151b** (the programs), **META-152** (`fixtures/abandoned-engagement/`),
  **META-153** (harness, separate commit).

## A finding ADR-0011 surfaced and correctly declined to file — the next findings pass owes it

`next` step 3 halts on **any** open human-addressed question, while `spec/question.md` §2 says an
elicitation *"must not stop the loop"*. Both cannot hold; today the first wins. Consequence: an
unanswered elicitation halts the workspace and — because rest requires no open question anywhere
— makes **every** ending unreachable, **E1 included**. ADR-0011 §6 records it with both
citations. It is adjacent to **F-097** (cluster 5, META-162) and must be filed with an F-number
by whichever unit gets there first. Do not lose it.

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
- **META-150** — `meta/adr/ADR-0011-stakeholder-silence-and-abandonment.md`, 627 lines
  (**94606f5**). **The threshold is a *silent round***: one orchestrator execution that ended at
  *waiting on the human* and observed **no inbound change** since the previous such execution.
  Inbound = only what a stakeholder can change. Default **3**, in `pipeline.yaml` as
  `termination.silence.threshold_rounds`, read by all three consumers (`next`,
  `engagement-state`, `check-epic-signoff`) — because two of them disagreeing is F-045's
  mechanism. Resets on **any** inbound change including a partial answer and a deferral (it
  measures presence, not compliance — F-028: a deferral is a reply); never resets on anything we
  write. Rejected: **wall-clock** measures how long the pipeline was switched off, so it is wrong
  in **both** directions; **turns** are the harness's unit and importing one puts the harness
  inside the contract it exists to grade (ADR-0005). The count is **derived** from an append-only
  log `tracker/waiting/<EP-ID>.md` — the trailing run of equal inbound digests (ADR-0003's
  no-counter argument) — the halt is recorded **before** the state is read, and **the reader
  never writes**, because `engagement-state` is consulted by the gate and by `review-close` and a
  counting reader would advance the clock by being asked.
  **`review-close` declares E4**; the ending statement is **a document, not a question** (there
  is nobody to address) — `## Ending statement` in `review.md`, mirrored in the epic's
  `## Notes`. Children classify from status alone: delivered / dropped earlier / blocked earlier
  / **orphaned, in flight** / **orphaned, never started**; orphans move to `blocked` with reason
  prefix `orphaned by E4:` and take **no `outcome` at all**, because the validator makes outcome
  present *iff* `done`. **E3 vs E4 in one test: did the stakeholder's own words arrive?** The
  `done`/`blocked` asymmetry is justified, not amended — `blocked` means *a human must act*,
  which at E4 is a standing instruction to wait for nobody, and `done` on an epic is the one
  state in this pipeline that reopens, so the ending most likely to be wrong is the only
  undoable one. **F-060 is not a dependency**: abandonment is only ever declared against an open
  ask, and F-060's case is the opposite one.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5 is a HELD-OUT calibration engagement: this
  session does not run it and does not read its probe beyond provision-verification.
