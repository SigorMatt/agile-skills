# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator holds only the mission, `meta/plan.md`, this file, and each unit's
verdict. Per unit: checkpoint the intent → dispatch with scope, files to read, definition of
done, and the obligation to commit AND push → verify cheaply (git log for the sha,
`./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## The gate is GREEN at e9f8d79 — 36 steps, 97 codes, selftest 307, 49 findings citations

E4 now executes end to end in fixtures. What remains of cluster 2 is the **harness** half.

## Current unit

**META-153** — the harness side of E4. **A SEPARATE COMMIT from the toolkit** (standing rule).

Two halves, both named in the mission:

1. **A sim job that legitimately declines to answer** — scripted silence, logged. The persona is
   already staged: `harness/skills/simulated-human/personas/ghosting-founder.md` phase 2 says
   *take the turn, read the board, write no `## Answer`, log the withholding tagged
   `[PLANTED: ghosting]`*. The harness must treat that as a **successful turn that answered
   nothing**, not as a failed or empty turn.
2. **The driver recognising the ending.** `harness/run_iteration.py` knows three terminal
   stops — `epic-done`, `blocked-no-recourse`, `stalled` — and E4 falls through to **`stalled`**,
   which is a lie about what happened. It must recognise *"human silent past threshold, E4
   declared"* as a terminal **epic-done-class** stop. H-008's lesson applies directly: a stall is
   a fact about the driver's own progress, an ending is a fact about the **engagement**, and the
   two coincided until they didn't.

Note the asymmetry the driver must respect: a run can be genuinely stalled *and* the engagement
not abandoned, and vice versa. `scripts/engagement-state` is the authority on the second
(`abandoned` is now one of its verdicts) — the driver should ask it rather than infer.

- Done when: `harness/tests/test_harness.py` green with new cases covering both halves, the
  E4 stop distinguished from `stalled` **by execution** in a test rather than by reading,
  journalled, committed AND pushed as a **harness commit**.
- Next unit: **META-153b** — cluster 2's findings pass (the four items below).

## Owed to the findings ledger — META-153b files these

1. **The elicitation deadlock.** `next` step 3 halts on **any** open human-addressed question,
   while `spec/question.md` §2 says an elicitation *"must not stop the loop"*. Both cannot hold;
   today the first wins, so an unanswered elicitation makes **every** ending unreachable, **E1
   included**. Recorded in ADR-0011 §6 with both citations; deliberately unfiled three times now.
   Adjacent to **F-097** (cluster 5, META-162).
2. **`check-epic-signoff` refuses an epic with no sign-off and prints no reason at all** — the
   bare header with an empty bullet list, because the block that would explain DE7 and list the
   children sits after an early `return 1` and is **unreachable**. **Predates E4**:
   `git show 77a5d96:scripts/check-epic-signoff` has the same shape, and
   `fixtures/ended-engagement`'s `EP-003` — the F-045 case, *"the engagement nobody was ever
   asked about"* — has always failed this way under an assertion that reads only the exit code.
3. **The gate accepts a sign-off that claims a reply it does not have.** It collects the refusal
   (*says answered but its `## Answer` is empty*) into `problems`, then discards it — `problems`
   is printed only when `silence` is also `None`. The program whose whole subject is the E3/E4
   distinction passes it; only `validate-workspace` catches it.
4. **`engagement-state` prints `rest reached at <t>` under verdicts that never reached rest** —
   `rest_since` is a boundary derived from children's timestamps, not a statement that rest
   happened. Pre-existing, cosmetic in effect, but a false sentence in a program's output.

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
  - **META-152** `fixtures/abandoned-engagement/`, both ways (**e9f8d79**), 36 steps, 97 codes
    unchanged. `right/` is a **valid workspace** holding the three states E4 has to reach:
    **EP-001** silence *before* rest, six children — one per §3.5a class — three orphans at
    `blocked` with no `outcome`, two questions `abandoned` with empty `## Answer`, epic
    `done`/`dropped`; **EP-002** silence *after* rest, the epic taking the new
    `awaiting-answer → done` row; **EP-003** the moment *before* the declaration, verdict
    `abandoned` and the gate correctly failing. All digests **computed**, not invented; EP-003's
    is recomputed inside `./scripts/check` and required to match. Must-fail: a round short, an
    orphan carrying an `outcome`, a sign-off `answered` with an empty body, an ending statement
    omitting a child. **Non-vacuity proved in the strong form** — five deciding function bodies
    stubbed, five distinct failures. It also surfaced **three defects in the mechanism, reported
    and not bent around** — see *Owed to the findings ledger* above.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5 is a HELD-OUT calibration engagement: this
  session does not run it and does not read its probe beyond provision-verification.
