# Builder session two — mission kickoff prompt

Location when adopted: meta/BUILDER-2-PROMPT.md. Paste everything below the line into Claude
Code at the repository root.

---

You are builder session two of **agile-skills**. Session one built the toolkit; the harness
then drove it through four real runs (a mini plus iterations 1, 1b, 1c) and produced a
trail-backed findings ledger. Your mission is to work that ledger: fix what is filed, bump what
you change, re-render, and prove the fixes against regression runs — leaving the kernel
measurably closer to the "proven" gate in `meta/ROADMAP.md` §2.

Read first, in this order: `meta/findings/FINDINGS.md` (the whole ledger — it is your backlog),
`meta/ROADMAP.md`, `meta/harness/FINAL-REPORT.md`, and skim the evidence for any finding before
touching its fix (`meta/harness/evidence/`). The standing discipline applies unchanged:
CLAUDE.md, checkpoint rule (write-ahead intent in `meta/CHECKPOINT.md`, small committed units,
push after commit, clean tree between units), journal + ADRs, restart protocol, context
hygiene. Continue the existing META-### numbering.

## Ground rules for this session

1. **Findings are the only backlog.** Every change traces to an F-### or H-### (or to a new
   finding you file first). No unprompted improvements — if you see something worth fixing that
   is not filed, file it, then decide with the priorities below whether it is in scope.
2. **Version discipline.** Any behavioral change to a skill bumps its version in `skill.yaml`
   (semver: fixes patch, contract changes minor). Spec changes bump the spec's version header.
   Update FINDINGS.md as you go: `fixing` when you start, `fixed (commit <sha>)` when proven.
   The final re-render must leave `./scripts/check` green.
3. **Fix the class, not the specimen.** F-017's fix is not "write better timestamps" — it is a
   mechanical source for every self-reported field. F-019's is not "don't cd" — it is scripts
   that resolve their own root plus a validator that detects record/status divergence. The
   ledger's Direction lines are starting points, not specifications; where you deviate, say why
   in an ADR.
4. **Firewall, adjusted for this session:** you MAY modify `methodology/`, `spec/`, `scripts/`,
   `adapters/`, and `harness/` — that is the mission. You may NOT touch the banked evidence
   (`meta/harness/evidence/**` is read-only history) or rewrite prior findings (append
   corrections; never edit filed text). Throwaway project workspaces under
   `~/agile-skills-throwaway/` from past runs are evidence too — regression runs use fresh
   projects.
5. **Verify by execution.** A finding is `fixed` only when a test, a validator run, or a
   regression iteration demonstrates the new behavior. For every enforcement fix, also
   demonstrate the *negative*: a fixture where the old failure is attempted and now blocked
   (the same must-fail discipline `scripts/check` already uses).

## The worklist, in priority order

**Cluster 1 — enforcement integrity** (the kernel's reason to exist):
- F-001 (mechanize the claim class: claim-provenance linting per its addendum — DE6 proved the
  check works when followed; make it unskippable), F-017 (mechanical sources for timestamps,
  versions, personas; validator rejects entries dated outside the git activity window),
  F-018 (write-guard matches the target, not the command string), F-019 (root-resolving
  scripts; no chained transitions; journal-status ↔ history cross-check).

**Cluster 2 — the acceptance loop** (the human's seat at the table):
- F-022 (epic sign-off gate: blocking human-addressed acceptance question before epic done),
  F-021 (stakeholder-initiated request artifact routed by `next`), F-013 (make an epic
  suspendable: fix the pipeline.yaml terminal-status contradiction its addendum documents).

**Cluster 3 — pipeline/spec correctness:** F-011, F-014, F-015, F-016.

**Cluster 4 — refine calibration:** F-020 (grouped presentation), F-023 (routing test:
product-stake to the human; implementation-only decided and recorded; honor standing
deferrals by category).

**Cluster 5 — consumer readiness:** F-002, F-003, F-004, F-005 (installer + docs), F-007
(scripts/export with profiles), F-009 (README positioning per its filed direction).

**Cluster 6 — harness:** H-002 (resumable stop classes; fix the --fresh hint), H-003
(provision --wipe or true-fresh semantics, documented), H-004 (answers-pending routes a sim
turn first), H-005 (killed-turn cost + stale-status handling), H-006 (bound skill executions
per worker turn), H-007 (sim gets a closing turn). Keep harness commits separate from toolkit
commits — two ledgers, two prefixes.

Work cluster by cluster; within a cluster, order as you judge. If the session cannot finish
everything, clusters 1–2 plus the regression gate below outrank everything else — stop there
cleanly rather than spreading thin (rule 8 of the original mission still applies: done and
proven beats broad and fragile).

## Acceptance: the regression gate

- [ ] `./scripts/check` green, including the new must-fail fixtures for every enforcement fix.
- [ ] **Iteration 1d** configured and run: copy iteration 1c's setup to `iteration-1d-expenses`
      (fresh project `expenses-1d`), with the probe extended so the stakeholder ALSO refuses
      every alternative to the sample ("no — just wait for my file; I don't want a
      name-the-columns version") while everything else stays 1c. Expected: the import item
      reaches `blocked` through the fixed machinery; the sign-off gate (F-022) fires and the
      sim answers it; the run ends `blocked-no-recourse` or epic-explicitly-not-accepted — and
      the trail shows honest timestamps (F-017) throughout. This one run is the regression
      test for clusters 1, 2, and 6 at once.
- [ ] A findings pass over 1d's trail: anything new is filed (F-024+/H-008+), nothing is fixed
      silently.
- [ ] FINDINGS.md statuses current; every `fixed` cites its commit; `meta/FINAL-REPORT-2.md`
      written last — what changed, version bumps, what 1d proved, what remains open, and an
      honest read of ROADMAP §2: which proven-gate conditions now hold.

When the checklist is green: stop. The owner reviews 1d's trail next; iteration 2 (`tidy`)
runs against your fixed toolkit only after that review.

Begin: read the ledger, plan your units in `meta/plan.md`, checkpoint, and proceed.
