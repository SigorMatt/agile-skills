# Roadmap

Status: living document. Owner: project owner. Last updated: 2026-08-21.
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
