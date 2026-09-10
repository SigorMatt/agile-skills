# Roadmap

Status: living document. Owner: project owner. Last updated: 2026-09-10.
Supersedes the roadmap sketch in meta/FINAL-REPORT.md §5 where they differ.

## 1. What this project is (positioning)

The product is the **enforcement kernel**: the tracker state machine, the
`transition` program that makes gate-before-status a property of software, the
hooks that deny bypass writes, the validators, the question/escalation protocol,
and the audit bar (a context-free reader reconstructs the run from the record
alone). Methodology content rides on the kernel; the kernel is what nobody
else ships.

Positioning against the incumbent (BMAD-METHOD, see F-009): they are
collaborate-and-facilitate — expert agent personas guiding a human through
workflows. We are **delegate-and-verify** — interrogate the human once at
refinement, run autonomously under enforced gates, escalate through a protocol,
leave an audit-grade record. Their "Dev Loop Automation" roadmap item shows
convergence toward our territory; our moat is that autonomy here is
*trustworthy by construction*, and the way to keep the moat is to harden the
kernel faster than anyone bolts automation onto instruction-shaped process.

The toy-project audit finding (F-001) is the thesis in one line: every
machine-decidable gate held; every gate resting on an instruction-style
human-judgment read did not. Everything on this roadmap serves widening the
first class and mechanizing the second.

## 2. The "proven kernel" gate

The kernel is **proven** when all three hold:

1. A full consumer run completes with **zero skill version bumps**.
2. The three dead paths — DoR override, `blocked`, both send-back
   transitions — have each executed at least once (any run type counts).
3. The F-001 fix (mechanical claim provenance + adversarial verification)
   has survived a real run: wrong or unsourced justifications were caught at
   entry, none propagated.

This gate controls the Codex adapter and all BMAD-derived content imports
(F-010). Until it holds, those items do not start.

## 3. Sequence

**Harness build (now — critical path).**
A harness builder session receives meta/harness/DESIGN.md,
meta/harness/PROJECT-QUEUE.md, and the mission prompt
(meta/harness/HARNESS-PROMPT.md), and delivers `harness/` per DESIGN §7:
provisioner, driver, simulated-human skill, turn prompts, usage doc — proven
by one mini end-to-end iteration against the real toolkit. Human testing is
replaced by the harness; there is no human-peer track.

**Cycle 1+ — automated hardening.**
Inputs: harness iterations over the throwaway queue
(meta/harness/PROJECT-QUEUE.md), personas and probe scripts varied per
DESIGN §3; the first iterations force the three dead paths. The standing
findings F-001..F-010 (including the peer-derived setup findings F-002..F-006,
evidence on file) are cycle-1 backlog regardless of source.
Output per cycle: owner reviews trails (project trail + SIM-LOG + iteration
log) with the assistant → findings appended (F-011+) → builder session when
warranted — priorities: F-001 (mechanical claim class), F-002/F-003 (installer
correctness), F-004/F-005/F-006 (docs/UX), F-007 (export script), F-009
(README positioning) — version bumps, re-render, toy-project regression per
scripts/check → next queue entry.
Coverage caveat (DESIGN §6): the harness does not provide naive-user or
interactive-UX coverage. Before the open-source release, at least one
fresh-eyes human install-and-run is required (recorded under F-009).

**Retro skill — pulled forward (was roadmap item 3).**
Built as soon as two hardening cycles exist to learn from: reads a completed
epic's trail, proposes contract changes as findings. It automates the loop the
owner will by then have executed by hand, and every subsequent cycle gets
cheaper. Deepening `plan` and `review-close` (was item 2) is not a separate
phase — it dissolves into hardening cycles, driven by trail evidence.

**Codex CLI adapter.** Gated on §2. The port doubles as an independent audit of
the adapter contract and of runtime leakage into methodology/.

**Content packs.** Gated on §2. Architecture: the kernel becomes
methodology-agnostic; our 8-skill pack is the reference pack; a BMAD-derived
pack (per-skill quarrying, full contract translation, honest gating, renamed,
MIT-attributed) is a candidate second pack. Rules in F-010.

**Sprint ceremonies, estimation, multi-item parallelism.** Last, unchanged:
"once single-item flow is boring." Parallelism additionally needs a real answer
to conflicting branches.

## 4. Decision log pointers

Full analyses behind this roadmap: BMAD review and quarry-don't-fork decision
(F-009, F-010), async interaction (F-008), harness architecture
(meta/harness/DESIGN.md), judgment-gate direction (F-001). The findings file
is the single backlog; this document only orders it.

## §2 stamp (2026-08-30) — proven, and confirmed against the final state

FINAL-REPORT-3 declared all three conditions positive at a1bd33c, with the stated
qualification that no run had touched the kernel's final state (4b predated F-073 and
META-131's five fixes). Confirmation run 4c closes that gap: same probe and persona as
iteration 4, fresh project, final kernel at 735095c (+5ef81b0 config), 28-step gate green.

- Condition 1 — a full consumer run, zero version bumps, ending audit signs with no new
  finding against the code: **holds.** 4c ended E1 delivered at turn 17/30; the audit's one
  finding was a documentation citation defect the claims gate caught by its own discipline
  and repaired legally (v5→v6, no code touched); three gaps disclosed pre-sign-off, none
  hidden. Evidence: meta/harness/evidence/iteration-4c/.
- Condition 2 — the three dead paths and the endings: **holds.** E1 (tidy twice-signed; 4b;
  4c), E3 (1e), DoR override (1d), blocked (1d), send-backs (organic, multiple runs).
  E2/E4 remain fixture-only, recorded as such.
- Condition 3 — the F-001 machinery survives real runs and its contracted form is not
  vacuous: **holds.** 3b escalated a planted stakeholder contradiction to its author
  (the reserved reconciliation elicited); 4b/4c ran lint-claims --all over the full document
  set with the degenerate scope a failing verdict; the named residual (resolution ≠ support)
  is recorded at F-001/F-066's addendum as the mechanization boundary, owned by D12/DE6.

**The kernel is proven. The gated tracks are open:** retro skill first (per §3), then the
Codex CLI adapter, then content packs under F-010's rules. New-finding cadence continues to
govern: any structural finding class re-closes the affected track until fixed.


## §3 stamp (2026-08-30) — the retro skill is built; the track is open, not finished

Builder session four delivered the first gated-track item (`meta/FINAL-REPORT-4.md`). `retro`
0.2.1 ships as the ninth skill: it reads an ended engagement's record — tracker, docs, questions,
journals, history, git log, and the installed contracts — and writes one report with an
engagement-local retrospective and a set of candidate toolkit findings marked `PROPOSED` for a
human to triage upstream. `next` dispatches it after an ending on `engagement-state`'s new
`closed`/`ended` distinction; it is read-only over the engagement it audits, and it gates nothing.

**What is proven, by execution.** The pipeline dispatch works end to end on a real ended
engagement, the read-only boundary held in four independent runs, and the skill found a live
defect in the current kernel that nothing else had (**F-076**) plus the mechanism behind a finding
this ledger had been holding open (**F-061**'s addendum).

**What is not proven: recall.** Against a ground-truth subset written down before the runs, the
first honest reading rediscovered **one of five** workspace-visible findings outright, two more in
part, and missed two. A procedure fix afterwards raised that sharply, and the report says in three
places that the fix was made after reading the miss and is therefore not a measurement.

**The track stays open.** The next step is the one thing no banked record can test: run `retro`
inside a live harness iteration, where the product source and the commit history are present, and
read its report as part of that iteration's findings pass. A held-out engagement — banked, ground
truth written, the skill unchanged afterwards — is what a real recall number would take.

**Still gated behind this, in order:** the Codex CLI adapter, then content packs under F-010's
rules. Neither is opened by this session. The new-finding cadence continues to govern: F-076 has
joined the *document-as-deliverable* class (F-057, F-058) and sharpened it into a question with
two answers that cannot both be right.


## §4 stamp (2026-09-10) — the undefined region is defined; nothing in it has met a stakeholder

Builder session five delivered `meta/FINAL-REPORT-5.md`: three ADRs, eight of nine skill contracts
bumped, five new programs, two new fixture trees, fifteen new `./scripts/check` steps, and sixteen
new ledger entries. `./scripts/check` is green at 45 steps; `fixtures/broken-workspace` is 108
codes; the self-test is 356 cases; the harness is 110 tests; the ledger is 133 entries, every one
carrying a current status.

**What this session settled.**

- **Document-as-deliverable (ADR-0010).** The last undefined region of the methodology has a
  model: record and deliverable are properties of **sentences**, not of files; one rule generates a
  nine-actor × five-kind authority table whose *nobody*-cells are as load-bearing as its named
  ones; three claim kinds carry three distinct audit obligations; the invalidation set becomes a
  `plan` output, so *"what does this change make false?"* is asked at the first stage that can act
  on it instead of at the last gate. `spec/doc-header.md` §5's absolute — *"`implement` and
  `verify` do not write to `docs/`"* — is a real rule deliberately weakened, with the compensating
  controls and the predicted failure mode written into the ADR. Eight `[auto]` obligations became
  commands in `scripts/lint-documents`. F-057, F-058, F-076, F-087, F-092, F-093 and F-095 are
  fixed; F-053's class supplied the lifecycle input.
- **E4 is reachable (ADR-0011).** A stakeholder who simply stops answering can now be recorded as
  gone: a **silent round** (an orchestrator halt on the human with no inbound change since the
  previous one), counted as the trailing run of digests over an append-only log, threshold 3 in
  `pipeline.yaml`, declared by `review-close` and by nobody else, with an ending statement naming
  delivered and orphaned children by ID. Wall-clock and turns were both rejected with reasons.
- **Which questions stop the loop (ADR-0012).** The halt requires an **outstanding ask** and it
  happens **last**, below every dispatching step; a **standing ask** is surfaced, causes no halt,
  holds no rest and accrues no round. The one-action rule is preserved unamended. A fourth
  deadlock site (DE5/DE8/`abandoned`) was found by derivation and fixed.
- **The accepted backlog.** All nineteen retro-derived findings F-080 … F-098 are decided, and
  every remaining entry in the ledger carries a current status. **No entry says only *open*.**
- **The ledger can be read.** `./scripts/check` step 17b resolves every finding number cited in
  any git-tracked file, and step 17c requires every entry to carry a status and the header to say
  which one is current. The obvious `grep 'Status: open'` was measured wrong in both directions
  and blind to one form; that is F-112, filed and fixed in the unit whose subject it was.

**What this session did NOT settle, and it is the larger half.**

- **No live run has produced an E4.** The whole mechanism is fixtures and unit tests.
- **Nothing in the document model has met a live workspace.** It is derived, specified, enforced
  and fixtured, and no engagement has ever run under it.
- **The eight new commands decide LESS than the `manual_check` prose they replaced**, on purpose,
  each saying so in its own gate description.
- **ADR-0010 obligation 10 is claimed by nothing** — whether a sentence that *is* an
  engagement-state claim was written **inside** its delimited section rather than loose in the
  prose — and the whole K8 mechanism rests on it. Filed as F-102, *known, derived and accepted*.
- **`retro`'s recall is still unmeasured.** §3 said the honest way to get a number is a held-out
  engagement. It is staged and unrun.

**What is now open.**

- **21 findings** — 17 deferred behind a named gate, 2 known-derived-and-accepted (F-102,
  F-103), 1 open-unstarted-and-sequenced with its gate met (F-010), 1 re-gated on scope (H-015).
  Every gate is written down and **none has been taken.** The named units, in the order the ledger gives them: the ADR-0010 amendment (F-100 then
  F-101); `check-epic-signoff` (F-106 then F-105); `engagement.py` (F-110 with F-107); the
  citation-form sweep (F-098, one unit, before release); the next harness change window (H-015,
  H-020's residual, H-021); and `new-item`'s write-both-or-neither shape (F-051 with F-036).
- **§2's condition 1 is further away than when it was stamped.** *A full consumer run with zero
  skill version bumps* has now been contradicted by three consecutive derivations, this one moving
  eight of nine contracts. ADR-0010 §7 says to read that as a thermometer rather than explain it,
  and this stamp does so: **the kernel is proven and it is not yet stable.** §2's stamp is not
  withdrawn — its three conditions were met against the kernel of 2026-08-30 and nothing here
  unmakes that — but a re-confirmation run is owed once this session's work has been exercised.

**A correction this document owed itself.** **F-010's gate has been met since 2026-08-30.** Its
gate *is* §2, whose stamp that day declared all three conditions positive and named F-010 in the
sentence that opened the tracks. The finding nonetheless read `deferred (gated)` for eleven days,
and META-128's triage that same day recorded it as *already gated on ROADMAP §2* without checking
whether §2 had been stamped. F-010 is **open, unstarted and sequenced** — not deferred — under its
own *quarry, don't fork* rules, behind the retro track and the Codex CLI adapter in §3. Nothing
about it is reclassified as a defect; it never was one.

**The gated tracks, precisely.** §2 is met, so nothing is gate-blocked. §3's order stands: the
retro track (open, not finished — its recall is the open question), then the **Codex CLI adapter**,
then **content packs** under F-010's rules. None of the three was opened by this session. The
new-finding cadence continues to govern.

**The next step is not a build.** Run the two staged regressions, in this order, for these
reasons:

1. **Iteration 5 (`envel`, `pragmatic-manager`)** — targets **E2 delivered-partial**, never
   executed, and is the **held-out retro calibration** FINAL-REPORT-4 §8 asked for, with the
   product source tree and git history present. It runs first because it is the only step whose
   value is destroyed by anything happening before it.
2. **The owner reviews that trail independently and writes the findings down** — before reading
   the retro's report. FINAL-REPORT-4 §4.2 is the precedent for why the order is the whole point.
3. **Read the retro's report and score it** against step 2's list. This would be the first recall
   number for `retro` that is honest to quote.
4. **Iteration 5b (`droll`, `ghosting-founder`)** — the first live test of the E4 mechanism, and a
   normal findings pass. It runs last because it is the step most likely to produce a toolkit
   change, and a toolkit change before step 3 contaminates the calibration.

**Iteration 5 was neither run nor read by this session.** `run_iteration.py` was never invoked in
any mode; `harness/runs/` is `diff`-identical to its nineteen-entry baseline; the held-out probe's
existence was established by `os.path.isfile` and `getsize` only. Both configs were
provision-verified in a scratch root outside the repository, 10/10 rules each, and torn down.
