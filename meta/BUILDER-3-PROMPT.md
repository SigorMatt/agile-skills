# Builder session three — mission kickoff prompt

Location when adopted: meta/BUILDER-3-PROMPT.md. Paste everything below the line into Claude
Code at the repository root.

---

You are builder session three of **agile-skills** — the proven-kernel session. The full
four-entry queue has run: two E1 endings, one E3, all three dead paths, and a findings ledger
of 67 toolkit and 14 harness entries whose open items now have a distinct shape — the
machinery enforces the *document record* superbly and gives the *person* no seat in conflicts,
plus a set of gate-scope and budget-semantics defects that let green verdicts mean less than
they claim. Your mission: close that shape, then prove it with a dual regression gate.
ROADMAP §2's addendum (2026-08-29) is the honest baseline; your job is to make all three
conditions read positive.

Read first: meta/findings/FINDINGS.md in full (the open findings are the backlog),
meta/ROADMAP.md with its addendum, the iteration-3 and iteration-4 evidence for everything you
touch (meta/harness/evidence/iteration-3/, iteration-4/ — especially WI-0004's question
bodies and journal, and EP-001 review.md's Accepted gaps in iteration-4). All standing
discipline applies: CLAUDE.md, checkpoint write-ahead, small pushed commits, findings statuses
current with resolving multi-sha citations, must-fail fixtures for every enforcement change,
version bumps semver-honest, META-### continues, banked evidence and filed findings text
read-only (append corrections only).

## Cluster 1 — the person's seat in conflicts (F-062, F-065)

The queue's sharpest lesson: a contradiction between two stakeholder statements was detected
twice, named "false", and repaired unilaterally — the sim held a scripted one-line
reconciliation in reserve all engagement and nobody asked. Fix the class:

- A **cross-answer consistency obligation**: when a new answer, criterion, or sign-off
  condition touches a topic with a prior recorded human answer, the acting skill must either
  cite compatibility or file a question quoting both answers by ID and asking which wins.
  Repairing a stakeholder-sourced falsehood in docs without a question to its author becomes
  a refused move (hard gate where mechanical, contract rule where not — say which in the ADR).
- A **lint over the question/criteria record** for same-topic answers with conflicting
  content, so the escalation is checked rather than remembered. Topic matching may be
  citation-graph based (answers cited by conflicting claims) rather than semantic — design it,
  ADR it, and be honest in the ADR about what the lint can and cannot see.
- **F-065**: a "still holds" criterion is assessed against the criteria's text; the test suite
  is evidence for the answer, not its definition. Where domains don't intersect in tests, the
  non-intersection is stated and a covering case added or waived by name.

## Cluster 2 — gates that cannot pass vacuously (F-066, F-067)

- F-066: the claims gate's scope becomes explicit per context (item close: changed-since the
  item's base; ending: full set or named scope), and "checked nothing" is a failing verdict —
  F-033's rule applied to scope. The 4b regression depends on this.
- F-067: define the minimal legal repair for a true-but-unsourced ADR claim (append-only
  `## Corrections`, or an `accepted-unsourced` waiver citing the verifying review). The
  iteration-4 instance (ADR-0002 ×3) becomes the fixture and gets repaired through the new
  legal path.

## Cluster 3 — refine calibration, second pass (F-063, F-064)

Options before recommendation, recommendation marked as the team's preference (lintable
presentation rule); one open-elicitation question per item or per engagement (presence-
checkable). Small, contract-level, evidenced from two personas.

## Cluster 4 — harness semantics (H-010, H-011, H-012, H-013, H-014)

One rework, five findings: budgets bound work, not verdicts. Terminal workspace → epic-done
regardless of counter; closing turn budget-exempt; budget stops resumable when the engagement
is not at an ending (plain rerun with a larger --max-turns continues in place); first-job
derived from workspace state (no job=open at a populated workspace — H-013's sim-side fix
rides along in SKILL.md: describe the disk, never the frame); the driver owns its run
directory and console log from first output. Six-plus regression tests, harness commits
separate from toolkit commits.

## Cluster 5 — triage the riding tail

Every remaining open finding gets a decision: fix here (only if small and adjacent), defer
with a named gate, or reject with reason. No finding left status-stale. F-061 stays an
observation unless the 3b/4b runs give new evidence.

## Acceptance: the dual regression gate

- [ ] ./scripts/check green, including new fixtures: the cross-answer escalation refused-move
      case, the vacuous-scope failing case, the ADR legal-repair case, and the harness budget/
      first-job/closing-turn tests.
- [ ] **Regression 3b**: fresh project, iteration-3's config and probe INCLUDING the sign-off
      extension, unchanged. Expected: the planted contradiction is escalated — a question
      quoting both stakeholder answers by ID — and the sim's scripted reconciliation ("the
      multiline case wins; I over-spoke before") is finally elicited and recorded; the
      engagement ends through the gate. The sim saying its reserved line is the pass.
- [ ] **Regression 4b**: fresh project, iteration-4's config, unchanged. Expected: the boring
      run again — and this time the ending's own audit signs with zero new findings: the
      claims gate examines a real scope, nothing is legally unfixable, and the driver labels
      the completed engagement epic-done.
- [ ] Findings passes over both trails; anything new filed (F-068+/H-015+), nothing fixed
      silently.
- [ ] meta/FINAL-REPORT-3.md: what changed, versions bumped, what 3b and 4b proved, and the
      ROADMAP §2 verdict stated plainly — all three conditions, hold or not, with the evidence
      line for each. If all three hold, say "the kernel is proven" and stop; the gated tracks
      are the owner's to open. If any does not, say which, why, and what the next session's
      first unit is.

Budget guidance: clusters 1–2 and the regressions outrank everything; cluster 5 yields first
under quota pressure. The regressions are runs — launch them detached per harness/USAGE.md,
budget them generously (--max-turns 30), and treat their trails as read-only evidence the
moment they stop.

Begin: read the ledger's open findings, plan units in meta/plan.md, checkpoint, proceed.
