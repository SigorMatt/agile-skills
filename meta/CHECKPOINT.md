# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator holds only the mission, `meta/plan.md`, this file, and each unit's
verdict. Per unit: checkpoint the intent → dispatch with scope, files to read, definition of
done, and the obligation to commit AND push → verify cheaply (git log for the sha,
`./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## The gate is GREEN at 877ee85 — 34 steps, 82 codes, selftest 290, 49 findings citations

## Current unit

**META-151b** — the E4 mechanism, part 2: **the programs**.

The paper model is in (ADR-0011 at 94606f5; specs and `pipeline.yaml` at 877ee85). This unit
builds what reads and writes it. ADR-0011 §7 lists the files; `spec/workspace-layout.md` §1.4
now fixes the log format.

- the **waiting-log writer** — appends exactly one row per halt to `tracker/waiting/<EP-ID>.md`;
  `workspace-init` creates `tracker/waiting/`.
- `scripts/lib/engagement.py` / `scripts/engagement-state` — report the silence count;
  **the reader never writes**.
- `scripts/check-epic-signoff` — the E4 verdict.
- `scripts/validate-workspace` — the waiting log's shape, and `status: abandoned` questions.
- `methodology/skills/next/` — step 3's branch and a `silence-is-recorded` gate.
- `methodology/skills/review-close/` — step 10: the E4 declaration and the ending statement.
- re-render; version bumps.

**Prove by execution that all three consumers read `threshold_rounds` from `pipeline.yaml`** —
`next`, `engagement-state`, `check-epic-signoff`. Two of them disagreeing is F-045's mechanism,
so a test that changes the value and observes all three move is the point, not a formality.

### The count, restated so no program has to re-derive it

`inbound` is the first **8 lowercase hex** of SHA-256 over a canonical rendering: one line per
`addressed-to: human` question in the engagement **whatever its status**, ascending by
`<ITEM>/<Q-ID>` — `<ITEM>/<Q-ID> <status> <answered-at or -> <sha256 of the ## Answer body,
first 8 hex>` — then one line per file in `tracker/requests/`, ascending, `<filename> <status>`.
**Count = the number of trailing rows sharing the last row's `inbound`.** Absent file = zero.
No stored counter. `next` appends **before** reading state.

### Flagged by META-151 for a decision in this unit

`pipeline.yaml`'s rule-obligation registry keys a validator status rule to a **single**
`(from, to, actor)` triple. ADR-0011's obligation 5 (`epic.closed-with-active-children`) is
satisfied by **many** moves, so META-151 registered **nothing** rather than put a false statement
in a load-bearing registry — and flagged that the new `awaiting-answer → blocked` row is exactly
the move that made that rule unsatisfiable for a child suspended at `awaiting-answer`, F-050's
shape. **Decide here:** either grow the registry's shape to admit a set of triples, or record why
the obligation stays unregistered. Do not register a false triple to make a table look complete.

- Done when: the programs land, the threshold's single source is proved by execution,
  `./scripts/check` green, journalled, committed AND pushed.
- Next units: **META-152** (`fixtures/abandoned-engagement/`, the E4 rows end to end),
  **META-153** (harness — **separate commit**).

## Owed to the next findings pass — do not lose these

1. **The elicitation deadlock.** `next` step 3 halts on **any** open human-addressed question,
   while `spec/question.md` §2 says an elicitation *"must not stop the loop"*. Both cannot hold;
   today the first wins, so an unanswered elicitation makes **every** ending unreachable, **E1
   included**. Recorded in ADR-0011 §6 with both citations, deliberately unfiled by META-150 and
   META-151. Adjacent to **F-097** (cluster 5, META-162). Needs an F-number.
2. **The registry's one-triple shape** (above), if META-151b leaves it unregistered.

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
