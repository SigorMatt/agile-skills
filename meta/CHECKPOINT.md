# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator holds only the mission, `meta/plan.md`, this file, and each unit's
verdict. Per unit: checkpoint the intent → dispatch with scope, files to read, definition of
done, and the obligation to commit AND push → verify cheaply (git log for the sha,
`./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## The gate is GREEN at 4d1b7ce — 35 steps, 97 codes, selftest 307, 49 findings citations

## Current unit

**META-152** — `fixtures/abandoned-engagement/`: the E4 rows exercised **end to end**.

What is already proved: the threshold's single source, by execution (step 14b, 18
observations); the must-fail shapes (15 new codes in `fixtures/broken-workspace`). What is
**not** proved is an actual E4 **ending** — the thing the mission's acceptance asks for.

Model it on `fixtures/ended-engagement/`, which step 10 (*the termination gate*) already drives
with **one epic per verdict the gate has to reach**. Add the abandoned case:

- an engagement whose stakeholder went silent past the threshold — a `tracker/waiting/<EP-ID>.md`
  with ≥ threshold trailing rows at one `inbound` digest;
- `review-close`'s declaration: `## Ending statement` in `review.md`, mirrored in the epic's
  `## Notes`, naming **every child by ID** in its class (delivered / dropped earlier / blocked
  earlier / orphaned in flight / orphaned never started);
- orphans at `blocked`, reason prefixed `orphaned by E4:`, and **no `outcome` at all**;
- open questions closed `abandoned` with an **empty** `## Answer`;
- the epic `done`, `outcome: dropped`;
- `scripts/check-epic-signoff` **passing** it, and `scripts/engagement-state` reporting it.

**A near-miss E4 must fail**: one round short of the threshold, or an orphan carrying an
`outcome`, or a question closed `answered` with an empty body. A fixture that only shows the
happy path proves the gate can say yes, not that it can say no.

- Done when: the fixture exists both ways, a `./scripts/check` step drives it, the step is
  **proved non-vacuous** against the pre-change behaviour, gate green, journalled, committed
  AND pushed.
- Next unit: **META-153** — the harness side, in a **separate commit**: a sim job that
  legitimately declines to answer (scripted silence, logged), and the driver recognising
  *"human silent past threshold, E4 declared"* as a terminal **epic-done-class** stop rather
  than a stall. `harness/run_iteration.py` today knows only `epic-done`,
  `blocked-no-recourse` and `stalled`.

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
  - **META-151b** the programs (**4d1b7ce**), 35 steps, 82 → **97** codes (deliberate: 4
    `question.abandoned.*`, 11 `waiting.*`; `EXPECTED-CODES.txt` updated in the same commit),
    selftest 307, pipeline faults 8, shipped scripts 17. Bumps: `pipeline.yaml` 0.9.0, `next`
    0.5.0, `review-close` 0.9.0.
    **`scripts/record-halt` is a new script, not a mode of the reader** — a `--record` flag would
    make "the reader never writes" a matter of which flag a caller passed, when
    `check-epic-signoff` and `review-close` both read the count; a separate entry point makes the
    separation structural. `next` invokes it as the `silence-is-recorded` hard gate at step 3(a),
    **before** reading any verdict.
    **The registry grew rather than taking a false triple**: an entry may name a *class* of move
    (`from: any-non-terminal`, `to: terminal`, `actor: review-close`) and enumerate `satisfied_by`
    pairs; `lint-skills` checks **coverage** per item type, with classes read off the statuses
    table's own flags. **Pinning the actor is what makes it bite** — `awaiting-answer → blocked`
    existed all along for `answer-questions`, so an actor-blind check would have called that
    status covered while an orphan sat there with no move `review-close` could make. Fault 8
    proves it.
    **Threshold single-source proved by execution** (step 14b, 18 observations): the value is
    moved 3 → 5 in a copy of `pipeline.yaml` and all three consumers move with it; stubbing the
    reader to `return 3` names all three in the failure. The same step proves the reader leaves
    the log byte-identical, and that an answer resets the count while our own writes do not.
    **A rule tying an abandoned question to its epic's ending was considered and refused** —
    `review-close` closes questions before it moves the epic and `transition` validates before
    the move, so the rule would fail correct work: F-014's shape.
    `review-close`'s procedure hit the **500-line rendered body limit**; what was cut is material
    already in `spec/ids-and-statuses.md` §3.5a, replaced by a citation.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5 is a HELD-OUT calibration engagement: this
  session does not run it and does not read its probe beyond provision-verification.
