# Builder session two — final report

Mission: [`meta/BUILDER-2-PROMPT.md`](BUILDER-2-PROMPT.md). Backlog:
[`meta/findings/FINDINGS.md`](findings/FINDINGS.md). Units META-082 … META-101, all on `main`.

> **Draft — iteration 1d is running.** §4 and §6 are written once it stops. Everything else is
> final.

---

## 1. What changed, by cluster

### Cluster 1 — enforcement integrity

| Finding | What it was | What it is now |
|---------|-------------|----------------|
| **F-001** | judgement gates don't hold; a wrong claim reached seven documents | absolute claims about named code carry a resolvable `[src: ...]` citation; `scripts/lint-claims` is a **hard** gate on `plan`, `implement`, `review-close`; `validate-workspace` enforces resolution workspace-wide |
| **F-017** | skills invent timestamps, versions and personas | `scripts/journal-entry` owns the heading — clock and installed `skill.yaml`; `transition --journal-body-file` writes row and entry together; the validator rejects a time no clock produced |
| **F-018** | the write guard matched the command string, not the target | the Bash branch resolves real write targets; 30 cases, 15 must-deny and 15 must-allow |
| **F-019** | a failed transition mid-chain left record and status divergent, undetectably | scripts find their own root; a transition is a checkpoint, never chained; `journal.status.unmatched` makes the blind direction visible |

### Cluster 2 — the acceptance loop

| Finding | What it was | What it is now |
|---------|-------------|----------------|
| **F-013** | a blocking question on an epic was unrepresentable | statuses declare `suspendable` separately from `terminal`; an epic at `open` is both terminal and suspendable |
| **F-022** | an epic closed without ever asking the stakeholder | `kind: sign-off`, epic DoD **DE7**, and `scripts/check-epic-signoff` as a hard gate that also refuses a *stale* sign-off |
| **F-021** | the stakeholder could only speak when spoken to | `tracker/requests/R-###.md` (`spec/request.md`), routed by `next` at orchestrator step 2 — before it selects work |

### Cluster 3 — pipeline/spec correctness

| Finding | What it is now |
|---------|----------------|
| **F-011** | `answer-questions`' precondition defines *answerable* and names the human-answered case; the harness workaround is deleted |
| **F-014** | `transition` declares the pending move; the validator downgrades — visibly, with a count — only the findings that move resolves |
| **F-015** | `implement` moves to `in-progress` and journals in one command; the skill writes two entries because it makes two transitions |
| **F-016** | an epic-level record commit belongs on the trunk; `check-commit-refs` diagnoses the case instead of only reporting it |

### Cluster 6 — the harness

| Finding | What it is now |
|---------|----------------|
| **H-002** | stops are `RESUMABLE` or `TERMINAL`; a resumable stop clears on a plain rerun, as USAGE §9 always promised |
| **H-003** | `provision.py --wipe`, with two refusals; USAGE §3 says which flag means what |
| **H-004** | the loop re-scans before a scheduled worker turn and gives it to the sim when answers are pending |
| **H-005** | a killed turn's cost is `unknown`, not `$0.00`; a status file older than the turn is not that turn's status |
| **H-006** | a worker turn stops after `worker-skills-per-turn` skill executions |
| **H-007** | the sim gets one closing turn before `epic-done` — and, by addendum, before `blocked-no-recourse` |

### Filed during the session

| Finding | Why |
|---------|-----|
| **F-024** | every `fixed (commit <sha>)` citation in this ledger pointed at an orphaned pre-amend commit. F-001's failure class, in the file that tracks F-001. All ten corrected; the mechanical check is open |

---

## 2. Version bumps

| Contract | Was | Now | Why |
|----------|-----|-----|-----|
| `pipeline.yaml` | 0.1.0 | **0.3.0** | `suspendable` (F-013); orchestrator step 2 for requests (F-021) |
| `intake` | 0.1.1 | **0.2.0** | handles a routed request, including declining one (F-021); journalling through the tool (F-017) |
| `next` | 0.1.0 | **0.2.0** | routes requests before selecting work (F-021) |
| `refine` | 0.1.1 | **0.1.2** | journalling through the tool (F-017) |
| `plan` | 0.1.1 | **0.2.0** | the `claims-are-sourced` gate (F-001) |
| `implement` | 0.1.0 | **0.2.1** | `claims-are-sourced` (F-001); journals at step 3 with its transition (F-015) |
| `verify` | 0.1.1 | **0.1.2** | journalling through the tool (F-017) |
| `review-close` | 0.1.2 | **0.3.1** | `claims-are-sourced` and the claim audit step (F-001); `epic-sign-off` (F-022); the epic commit rule (F-016) |
| `answer-questions` | 0.1.1 | **0.1.4** | the precondition (F-011); the epic commit rule (F-016); journalling through the tool (F-017) |

Specs changed, each with a `## Revisions` row: `journal-and-history.md` (§0),
`skill-contract.md` (§2.2, §2.3), `ids-and-statuses.md` (§4), `question.md` (§2),
`doc-header.md` (§4a), `dor-dod.md` (D12, DE6, DE7), `workspace-layout.md` (§5,
`tracker/requests/`), and the new `request.md`. Prompts: worker-turn 4, sim-turn 2.

Spec prose files carried no version header, so rule 2 of the mission had no literal target; each
changed file gained a `## Revisions` table instead, dated and attributed to its finding.

---

## 3. The gate, and what it now covers

`./scripts/check` went from 6 steps to 11:

| # | Step | Added for |
|---|------|-----------|
| 1 | library self-test | — (4 new root-resolution cases, F-019) |
| 2 | lint-skills | — (new rule `pipeline.status.unsuspendable`, F-013) |
| 3 | must-fail fixture — **62 codes**, was 44 | F-019, F-017, F-001, F-022, F-021 |
| 4 | rendered output is current | — |
| 5 | must-pass workspace | — |
| 6 | claim-provenance fixtures | F-001 |
| 7 | claim-provenance as the gate invokes it | F-001 (a preflight caught this path crashing while step 6 was green) |
| 8 | epic sign-off gate refuses an unaccepted epic | F-022 |
| 9 | epic sign-off gate | F-022 |
| 10 | write-guard self-test — 30 cases | F-018 |
| 11 | harness self-test — 47 tests, was 29 | H-002…H-007, F-021 |

Every enforcement fix ships a fixture where the old failure is attempted and now blocked, and —
where a rule could be satisfied only vacuously — a fixture proving it *can* be passed:
`fixtures/sourced-claims/` and `fixtures/signed-off-epic/` exist for that reason.

---

## 4. What iteration 1d proved

_To be written when the run stops._

---

## 5. What remains open

_To be written with §4._

---

## 6. ROADMAP §2 — an honest read

_To be written with §4._
