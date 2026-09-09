# Builder session five — mission kickoff prompt

Location when adopted: meta/BUILDER-5-PROMPT.md. Paste into Claude Code at the repository
root: "Read meta/BUILDER-5-PROMPT.md and execute the mission below its divider."

---

You are builder session five of **agile-skills**. The kernel is proven (ROADMAP §2 stamp);
the retro skill exists and its first triage put 19 accepted findings (F-080..F-098) plus
F-099 into the ledger. Your mission: the document-as-deliverable derivation the ledger has
been circling, the E4 mechanism, and the accepted backlog — then stage (not run) the two
regression iterations that will grade this work.

Read first: meta/ROADMAP.md, meta/findings/FINDINGS.md — every entry with Status: open,
with special attention to F-080..F-099's provenance sections — meta/FINAL-REPORT-4.md §8,
and meta/adr/ADR-0006 + ADR-0008 as the house style for derivations. Standing discipline
applies unchanged (CLAUDE.md, checkpoint write-ahead, small pushed commits, findings
statuses with resolving citations, must-fail fixtures, semver bumps, META-### continues,
banked evidence and filed findings read-only).

## Execution model for this session (new, binding)

Work in SMALL UNITS, each executed by a DEDICATED SUB-AGENT via the Task tool. Your own
context is the orchestrator only: mission, plan, checkpoint, and per-unit verdicts. Per
unit: (1) checkpoint the intent; (2) dispatch a sub-agent with the unit's scope, the exact
files to read, the definition of done, and the obligation to commit AND push; (3) verify
the unit yourself cheaply — git log for the sha, ./scripts/check or the relevant fixture
run — before marking the checkpoint closed; (4) next unit. Do not pull unit work products
into your own context beyond what verification needs. Subscription limits can hit at any
moment: the checkpoint must always be accurate enough that a fresh session resuming with
the standard kickoff line loses at most the in-flight unit.

## Cluster 1 — the derivation: document-as-deliverable (centerpiece)

The last undefined region: what is a document in this pipeline, who may change it, when,
and what makes a claim in it checked? Do it the ADR-0006 way — enumerate, derive, then
re-check the historical findings as fixtures:

1. Enumerate the document kinds (product docs, architecture overview, ADRs, process docs,
   item artifacts, engagement-state sections of the vision) × the lifecycle events that
   change them (plan writes, implement's change falsifies, review corrects,
   answer-questions propagates, the ending records).
2. Derive an authority-and-obligation table — who may write which kind at which event, and
   which check they owe when they do — and a claim taxonomy (cited fact, quantified claim,
   engagement-state statement) with a distinct audit obligation per kind.
3. Settle these findings from the derived model, as fixtures: F-076 (implement's empty-by-
   construction claims window — assign checking to whoever the table says writes),
   F-087 (the invalidation-set becomes a plan output; the falsification question is asked
   where the change is made), F-093 (engagement-state sections are owned by the ending,
   not by any item), F-095 (quantified claims require member enumeration recorded in the
   audit row), and F-053's class as the lifecycle-state input. F-092 (ADR conformance as a
   criterion) belongs to the same table — plan lists the ADRs that bind it; a later gate
   decides each.
4. ADR it; update spec/doc-header.md, dor-dod.md, and the affected skill contracts from
   the derivation; every changed rule ships its must-fail fixture.

## Cluster 2 — the E4 mechanism (gates regression 5b)

Nothing can currently declare a stakeholder gone. Derive and build: a silence threshold
(measured in rest-time or unanswered rounds, stated in pipeline.yaml), the abandonment
decision owned by review-close (an ending statement listing delivered children and
orphaned ones by ID — DE-style, mirroring E2/E3), the E4 rows exercised end to end in
fixtures. Harness side: a sim job that legitimately declines to answer (scripted silence,
logged), and the driver recognizing "human silent past threshold, E4 declared" as a
terminal epic-done-class stop rather than a stall. Keep harness commits separate.

## Cluster 3 — enforcement mechanics (small, mostly script-level)

F-091 is the anchor: transition owns the **Gates:** verdicts the way it owns **Status:**
(the runner writes what ran; the worker supplies evidence sentences). Then F-080 (fourth
gate verdict + contract-vs-bullet comparison), F-081 (a sanctioned place for the merge
sha created after the closing entry), F-083 (outcome/status ordering made legal), F-084
(doc version rows matched against executions), F-094 (criterion citations survive
renumbering), F-096 (substituted-verification ticks carry a mark), F-099 (evidence-to-
ledger citation resolution — expect its first run to surface more phantoms; tombstone or
correct each, honestly).

## Cluster 4 — ending contracts

F-085 (review-close's gate list gains an epic-subject column: "skipped, an epic has no
branch" becomes the contract's answer), F-086 (DE1–DE6 applied before the sign-off is
filed; DE7 alone waits for the reply), F-061 (option B's consequence line tells the
truth: the epic stays open, the follow-up is built, a fresh sign-off follows — the
truth-in-labeling fix, one sentence in spec/question.md §2).

## Cluster 5 — planning/criteria and stakeholder protocol

F-089 (criteria name artifacts rather than counting them; wanted counts are measured
first), F-090 (an accepted gap naming an owner becomes dispatchable — an open question at
acceptance time), F-088 (audit examples must be able to falsify; the audit row records
why), F-082 (a consumed delegation records the category it is taken to cover; the
sign-off surfaces assumptions taken under delegations), F-097 (a collect-askable-questions
pass before the loop stops on the human — design carefully against the one-action rule;
ADR the resolution).

## Cluster 6 — triage the rest

Every remaining open finding gets a decision: fix here only if small and adjacent, defer
behind a named gate, or reject with reason. No status left stale.

## Staging the regressions (do NOT run them)

Two iterations are staged by the owner alongside this mission (queue entries, configs,
probes, personas for iteration-5-envel and iteration-5b-droll). Your acceptance includes
verifying they are runnable — provision each in a throwaway path, validate, tear down —
but the runs themselves are the owner's to launch, because iteration 5 is a HELD-OUT
calibration engagement: its trail must be reviewed by the owner before anyone reads the
retro's report on it. Do not run iteration 5, do not read its probe beyond what staging
verification requires, and say in the final report that you did not.

## Acceptance

- [ ] ./scripts/check green; every enforcement change carries its must-fail fixture; the
      derivation's historical cases (F-076/F-087/F-093/F-095/F-053-class) run as fixtures.
- [ ] E4 executes end to end in fixtures and harness tests (the run itself is 5b's job).
- [ ] Findings statuses current; F-099's sweep results handled honestly.
- [ ] Both regression configs provision-verified and torn down.
- [ ] meta/FINAL-REPORT-5.md: the derivation's decisions, what each cluster changed,
      versions bumped, the F-099 sweep's yield, explicit confirmation that iteration 5
      was not run or read, and the recommended launch order (expected: iteration 5 →
      owner review → retro comparison → 5b).

Budget guidance: cluster 1 and 2 outrank everything; cluster 6 yields first. If limits
hit, the checkpoint recovers you; resume with the standard kickoff line.

Begin: read, plan units in meta/plan.md (one line each — unit, sub-agent scope, gate),
checkpoint, dispatch.
