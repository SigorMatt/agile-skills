# CHECKPOINT

## Builder session five is COMPLETE. There is no next unit in this session.

`meta/BUILDER-5-PROMPT.md` is done: META-144 through META-165, committed and pushed.
`./scripts/check` is green across **45 steps**; `fixtures/broken-workspace` emits **108** codes;
`scripts/lib/selftest.py` is **356** cases; `harness/tests/test_harness.py` is **110** tests.
The ledger holds **133** entries and every one carries a readable current status, enforced by
step 17c. Read `meta/FINAL-REPORT-5.md` and `meta/ROADMAP.md` §4 first.

**What was built.** Three derivations and their machinery.
- **ADR-0010 — document-as-deliverable.** Record-vs-deliverable is a property of **sentences**,
  not files. Three claim kinds; **K8** engagement-state statements are **owned by the ending**.
  The **invalidation set** is a `plan` output. `doc-header.md` §5's absolute does not hold and
  the claims gate **stays on `implement`**, whose window no longer stands empty by construction.
- **ADR-0011 — stakeholder silence and abandonment.** E4 is reachable: a **silent round**,
  default 3, stated once in `pipeline.yaml` and read by all three consumers. `review-close`
  declares it; the ending statement is a **document, not a question**, because there is nobody
  to address.
- **ADR-0012 — which questions stop the loop.** Only an **outstanding ask** halts, and it halts
  **last**. The one-action rule is preserved, unamended: F-097's collect-pass already existed —
  it is the loop; only the step order was wrong.

**What is NOT proven, and the report says so.** **No live run has produced an E4.** **Nothing in
cluster 1 has met a real engagement.** Each of the eight `[auto]` obligations decides **less**
than the `manual_check` it replaced, and says so in its own gate description. **Obligation 10 is
claimed by nothing**, and the K8 mechanism rests on it.

## What the owner does next — `meta/ROADMAP.md` §4 and FINAL-REPORT-5 §8

1. **Iteration 5 (`envel`)** — E2 *and* the held-out retro calibration. First, because it is the
   only step whose value is destroyed by anything happening before it.
2. **Owner reviews the trail and writes findings down — before reading the retro's report.**
3. **Read the retro report and score it** against step 2. The first recall number honest to quote.
4. **Iteration 5b (`droll`)** — the first live test of E4. Last, because it is the most likely to
   produce a toolkit change, and a change before step 3 contaminates the calibration.

Both configs are **provision-verified and torn down**. **Neither iteration was run**, and
iteration 5's probe was **not read** — its existence was established by `isfile` + `getsize`.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten — and **the LAST status bullet is the current one** (F-112; step 17c).
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.**

## For the next builder session — what this session's method showed

- **Strong-form non-vacuity proofs** (stub the deciding body; run the stubs against your *own*
  new cases) caught a defect in the unit's own new tests **five times**, including an assertion
  that could not fail because `ADR-0012` contains the substring `R-001`.
- **An orchestrator's summary is hearsay.** Sub-agents corrected these briefs by reading the
  code at least four times — F-105 is unreachable on every input, not merely late; F-107 fires
  under every verdict; F-111 is wider than reported *and* its reported consequence does not
  survive the code; META-148 and META-148b filed contradictory reports and **execution** settled
  it. META-165 then corrected four claims in this very file.
- **Measure before scoping.** Four rules this session were scoped by measurement rather than
  taste, and two would otherwise have retroactively invalidated imported real-run evidence.
- **A deferral whose gate has been met and not noticed is how a backlog rots** — F-053 and F-043
  were fixed *incidentally* at 8804bd7 and noticed only at triage, and F-010's gate had been met
  for eleven days.
