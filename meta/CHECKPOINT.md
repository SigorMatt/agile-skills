# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator holds only the mission, `meta/plan.md`, this file, and each unit's
verdict. Per unit: checkpoint the intent → dispatch with scope, files to read, definition of
done, and the obligation to commit AND push → verify cheaply (git log for the sha,
`./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## The gate is GREEN — 35 steps, 97 codes, selftest 307, 49 findings citations

## Current unit

**META-152** — `fixtures/abandoned-engagement/`, the E4 rows end to end. META-151b landed the
programs; this is the fixture that runs them over a whole engagement.

- ADR-0011's `ghosting-founder` walkthrough is the worked example, and §6 names what it does
  **not** exercise: every child there is *orphaned, never started*, so the fixture must also carry
  an *orphaned, in flight* child (at `in-progress` with a branch, or at `in-review`), and a second
  shape where the silence begins **after** rest — a sign-off filed, open, and ending `abandoned`
  with an empty `## Answer`, which is the case `check-epic-signoff`'s new branch is for.
- The programs to run it against: `scripts/record-halt`, `scripts/engagement-state`,
  `scripts/check-epic-signoff`, `scripts/validate-workspace`.
- The waiting log's format is `spec/workspace-layout.md` §1.4 and it is now enforced by eleven
  `waiting.*` validator codes — write rows with `record-halt` rather than by hand where possible.
- Next after: **META-153** (harness — **separate commit**).

## Done in META-151b

- `scripts/record-halt` is the waiting-log writer, a **new script** rather than a mode of
  `engagement-state`, so that "the reader never writes" is structural rather than a flag
  discipline. `next`'s `silence-is-recorded` gate is that command with no arguments; it records
  only where a halt exists, so it can run on every pass.
- **The registry decision: obligation 5 is registered, and the shape grew to admit it.** An entry
  may now name a **class** of move (`from: any-non-terminal`, `to: terminal`, `actor:`) and
  enumerate the concrete pairs under `satisfied_by`; `lint-skills` checks **coverage** per item
  type, with the classes read off the statuses table's own flags. Pinning the actor is what makes
  it bite — `awaiting-answer → blocked` existed for `answer-questions` all along. Non-vacuity is
  `scripts/check` step 11, fault 8: change that row's actor and `obligation.unsatisfiable` comes
  back for both item types. `validate-workspace` reads the entry for the rule's scope.
- **The threshold's single source is proved by execution** (new step 14b, 18 observations): 3 → 5
  over one unchanged workspace, and `record-halt`, `engagement-state` and `check-epic-signoff`
  each change their mind. Also proved there: a reader leaves the log byte-identical, and an answer
  resets the count while our own writes do not.
- `check-epic-signoff` gains a second **accepting branch**, not a relaxation: threshold reached,
  an ask that stood unanswered (so *ending while never having asked* stays illegal), no sign-off
  left `open`, and `## Ending statement` in `review.md` naming every child.
- Three `spec/workspace-layout.md` §1.4 sentences were underspecified and were fixed **in the same
  commit**: `*.md` only for request lines, the `## Answer` body hashed with trailing whitespace
  stripped and nothing else normalised, and which epics a halt is against.
- `review-close`'s procedure was cut to fit the 500-line rendered body limit; what was cut is
  reference already in `spec/ids-and-statuses.md` §3.5a, and every rule a reader could get wrong
  stayed.

## Owed to the next findings pass — do not lose these

1. **The elicitation deadlock.** `next` step 3 halts on **any** open human-addressed question,
   while `spec/question.md` §2 says an elicitation *"must not stop the loop"*. Both cannot hold;
   today the first wins, so an unanswered elicitation makes **every** ending unreachable, **E1
   included**. Recorded in ADR-0011 §6 with both citations, deliberately unfiled by META-150 and
   META-151. Adjacent to **F-097** (cluster 5, META-162). Needs an F-number.
2. ~~The registry's one-triple shape~~ — **resolved in META-151b**: the shape grew and
   `epic.closed-with-active-children` is registered. Nothing owed.

## Done this session

- **META-144** Phase VI planned (2c4b0b7, 0deafc0).
- **CLUSTER 1 — document-as-deliverable — COMPLETE.** Full detail is in the ADR, the journal and
  the ledger; the shas are the record.
  - **META-145** `meta/adr/ADR-0010-document-as-deliverable.md`, 699 lines (**3701069**).
    `doc-header.md` §5 does not hold, the claims gate **stays on `implement`** (F-076);
    record-vs-deliverable is a property of **sentences**, not files; **K8** engagement-state
    statements are **owned by the ending** (F-093); the **invalidation set** is a `plan` output
    (F-087); quantified claims discharge only by member enumeration in the audit row (F-095);
    `verify` decides ADR conformance, `review-close` checks the list is complete (F-092).
  - **META-146** the two spec files carry it (**c1fbde8**); D13 new, marked `[skill]` honestly.
  - **META-147** four contracts + `pipeline.yaml` + dist (**5e6434d**). **META-147b** `intake`
    and `answer-questions` (**9adff0e**) — `intake` gets **no** `lint-claims` gate, because that
    window would be empty by construction, F-076's shape in a new place.
  - **META-148** the window (**5ae1539**): `scope.py`'s fourth state
    *out-of-scope-by-construction* passes **with a mark**; `constrained()` takes the permission
    knowledge from the caller, because **no diff can distinguish "nobody wrote a document" from
    "nobody was allowed to"**. Proved non-vacuous: 5 of 8 cases failed against the old scripts.
  - **META-148b** all eight `[auto]` obligations become real commands via
    `scripts/lib/documents.py` + `lint-documents` (**a843114**); each decides **less** than the
    `manual_check` it replaced, and says so. **Obligation 10 is not claimed** — a fixture holds a
    loose K8 sentence no rule fires on, deliberately. Non-vacuity proved **twice**, the second
    time with every rule body stubbed to `return`.
  - **META-148c ABSORBED, not skipped** — its cases already run as by-execution steps from the
    two units before it; re-authoring would put one assertion in two places.
  - **META-149** the ledger (**f474027**), append-only proved mechanically (358 insertions, **0
    deletions**), citations 43 → 49. Fixed: F-076, F-087, F-092, F-093, F-095, F-057, F-058 —
    the last two saying **in those words** that their deferral's gate was met. **F-053 NOT
    fixed**, consumed as input only. **META-148 and META-148b had filed contradictory reports;
    META-148 was right**, established **by execution** — two hard gates on `implement` jointly
    unsatisfiable, no legal repair but `--force`. Filed **F-100**; also **F-101** (a deliverable
    document outside `docs/`), **F-102** (obligation 10, *known, derived and accepted*),
    **F-103** (a bare-plural universal — with a correction that ADR-0010's own illustration of
    it is wrong).
- **CLUSTER 2 — E4 — in progress.**
  - **META-150** `meta/adr/ADR-0011-stakeholder-silence-and-abandonment.md`, 627 lines
    (**94606f5**). The threshold is a **silent round**, default **3**, in `pipeline.yaml`.
    Rejected: **wall-clock** (measures how long the pipeline was switched off — wrong in **both**
    directions) and **turns** (the harness's unit; importing it puts the harness inside the
    contract it grades, ADR-0005). The count is **derived** from an append-only log, the halt is
    recorded **before** state is read, and **the reader never writes**. Resets on a partial
    answer and on a deferral (presence, not compliance — F-028). `review-close` declares E4; the
    ending statement is **a document, not a question**, because there is nobody to address.
    Orphans go to `blocked` with **no `outcome` at all**. **E3 vs E4 in one test: did the
    stakeholder's own words arrive?** F-060 is **not** a dependency.
  - **META-151** the model on paper (**877ee85**), gate green. **ADR-0006 was repaired by a
    header pointer — `**Amended by:** ADR-0011` — and no `## Corrections` entry**, argued four
    ways: neither correction kind fits (nothing in §1 is false or unsourced); §4b's own boundary
    (*"if a reader would have to change any code…, it is a new decision"*) rules it out, and
    stretching that condition **in the file its own ledger watches** would be this repo failing
    F-067; a correction entry is structurally illegal there anyway (no change log, no
    frontmatter); house precedent is forward declaration. **Three absolutes had to be amended
    rather than deleted** — each was true of four endings and false once E4-by-silence exists.
    *Ending while never having asked is still illegal*: E4 permits an ask with an **empty**
    `## Answer`, never a missing ask. A near-miss caught by the library crosscheck: three new
    `pipeline.yaml` scalars carried `: ` inside a plain scalar — `miniyaml` accepted them,
    **PyYAML did not**.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5 is a HELD-OUT calibration engagement: this
  session does not run it and does not read its probe beyond provision-verification.
