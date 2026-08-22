# Builder session two — final report

Mission: [`meta/BUILDER-2-PROMPT.md`](BUILDER-2-PROMPT.md). Backlog:
[`meta/findings/FINDINGS.md`](findings/FINDINGS.md). Units META-082 … META-101, all on `main`.

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

### Cluster 4 — refine calibration

| Finding | What it is now |
|---------|----------------|
| **F-023** | `refine` step 3 is a four-branch routing test applied *before* a question is filed: product stake → the human; already answered → do not re-ask; a standing deferral covers the **category** → decide and record it; implementation-only → `plan`. An exit criterion, so it is checkable |
| **F-020** | questions for one item in one round are presented as one ask — same frame in each `## Context`, the last one closing the round. One conversation, three artifacts |
| **F-027** | one decision per question, stated with its consequence. Not mechanised, deliberately |

### Cluster 5 — consumer readiness

| Finding | What it is now |
|---------|----------------|
| **F-002** + **F-047** | the tool that creates a required directory creates its `.gitkeep` — `workspace-init` **and** `new-item`. Proven by clone |
| **F-003** | `workspace-init` writes or extends `.gitignore` |
| **F-005** | the uninitialised state has its own exit code: 0 clean, 1 wrong, 2 usage, **3 not started** |
| **F-004** + **F-012** | USAGE §2 puts the check that works first; §4 carries the trust requirement with the stderr line quoted |
| **F-007** | `scripts/export` — three profiles, non-destructive, and a guard that separates a leak from a dangling citation |
| **F-009** | README positions against BMAD-METHOD, and says which one a reader should want |

### Found and fixed within the session

| Finding | Why it matters |
|---------|----------------|
| **F-024** | every `fixed (commit <sha>)` citation in this ledger pointed at an orphaned pre-amend commit — F-001's failure class in the file that tracks F-001. All corrected, the practice changed, and `scripts/check` now enforces it |
| **F-037**, **F-033**, **F-044**, **F-039**, **F-025**, **F-040**, **F-041** | defects 1d found in this session's own work. See §4 |
| **F-026**, **F-032** | `--help` on all ten entry points; a filed question must carry `## Answer` from the start |

---

## 2. Version bumps

| Contract | Was | Now | Why |
|----------|-----|-----|-----|
| `pipeline.yaml` | 0.1.0 | **0.3.0** | `suspendable` (F-013); orchestrator step 2 for requests (F-021) |
| `intake` | 0.1.1 | **0.2.0** | handles a routed request, including declining one (F-021); journalling through the tool (F-017) |
| `next` | 0.1.0 | **0.2.0** | routes requests before selecting work (F-021) |
| `refine` | 0.1.1 | **0.2.0** | the routing test as an exit criterion (F-023); grouped presentation (F-020, F-027); journalling through the tool (F-017) |
| `plan` | 0.1.1 | **0.2.0** | the `claims-are-sourced` gate (F-001) |
| `implement` | 0.1.0 | **0.2.1** | `claims-are-sourced` (F-001); journals at step 3 with its transition (F-015) |
| `verify` | 0.1.1 | **0.1.2** | journalling through the tool (F-017) |
| `review-close` | 0.1.2 | **0.3.1** | `claims-are-sourced` and the claim audit step (F-001); `epic-sign-off` (F-022); the epic commit rule (F-016) |
| `answer-questions` | 0.1.1 | **0.1.4** | the precondition (F-011); the epic commit rule (F-016); journalling through the tool (F-017) |

Specs changed, each with a `## Revisions` row: `journal-and-history.md` (§0),
`skill-contract.md` (§2.2, §2.3), `ids-and-statuses.md` (§4), `question.md` (§2),
`doc-header.md` (§4a), `dor-dod.md` (D12, DE6, DE7), `workspace-layout.md` (§5,
`tracker/requests/`), and the new `request.md`. `question.md` reached revision 4. Prompts:
worker-turn 4, sim-turn 2.

New scripts, all shipped by the adapter: `journal-entry`, `lint-claims`, `check-epic-signoff`,
`export`; new shared library `scripts/lib/claims.py`.

Spec prose files carried no version header, so rule 2 of the mission had no literal target; each
changed file gained a `## Revisions` table instead, dated and attributed to its finding.

---

## 3. The gate, and what it now covers

`./scripts/check` went from 6 steps to 13:

| # | Step | Added for |
|---|------|-----------|
| 1 | library self-test — **195 cases**, was 183 | root resolution (F-019), both escapes (F-044, F-037) |
| 2 | lint-skills | new rule `pipeline.status.unsuspendable` (F-013) |
| 3 | must-fail fixture — **63 codes**, was 44 | F-019, F-017, F-001, F-022, F-021, F-032 |
| 4 | rendered output is current | — |
| 5 | must-pass workspace | — |
| 6 | claim-provenance fixtures | F-001, F-037 |
| 7 | claim-provenance as the gate invokes it | F-001 — a preflight caught this path crashing while step 6 was green |
| 8 | epic sign-off gate refuses an unaccepted epic | F-022 |
| 9 | epic sign-off gate | F-022 |
| 10 | write-guard self-test — 30 cases | F-018 |
| 11 | findings citations resolve | F-024 |
| 12 | export profiles | F-007 |
| 13 | harness self-test — **47 tests**, was 29 | H-002…H-007, F-021 |

Every enforcement fix ships a fixture where the old failure is attempted and now blocked, and —
where a rule could be satisfied only vacuously — a fixture proving it *can* be passed:
`fixtures/sourced-claims/` and `fixtures/signed-off-epic/` exist for that reason. The first of
those now contains a paragraph that *describes a malformed citation by quoting it*, which is a
paragraph that could not have existed before F-037 was fixed.

---

## 4. What iteration 1d proved

16 turns, 148 minutes, **$71.75**, 837 tool calls, **zero contamination violations**, and it
stopped exactly where it was predicted to: `blocked-no-recourse`. Evidence:
[`meta/harness/evidence/iteration-1d/`](harness/evidence/iteration-1d/).

### The dead path executed

**`blocked` ran, for the first time in five runs.** Four earlier runs escaped it legitimately —
a deferral accepted, a channel never opened, and 1c's genuinely good move of finding a design that
needed no sample at all. 1d closed the last escape by having the stakeholder refuse every
alternative, and WI-0003's history row is the artifact the run existed to produce:

> `draft → blocked | refine | draft | DoR fails R4 and R10 on one input the workspace has never
> held: a sample of the stakeholder's bank CSV. All three questions on this item are answered and
> Q-003 settled that the shape comes from their file, so no question remains to ask and no skill
> may guess it`

`resume-to: draft` is recorded, an ADR forbids a fourth question, and the recovery is written
down. The stakeholder's own verdict, unprompted, on the closing turn is better evidence than my
reading of it: *"It did not build a generic importer, did not guess at my bank's columns, did not
stub anything out to 'unblock itself' — all things I would have said no to if they'd tried… That's
the honest version of stuck, not the giving-up version."*

The **Definition of Ready override** probe also fired for the first time (turn 5), and the review
send-back had already fired in iteration 1. All three of `meta/ROADMAP.md` §2.2's dead paths have
now executed.

### The fixes worked in a real run

| Fix | Evidence from 1d |
|-----|------------------|
| **F-001** claim provenance | `claims-are-sourced` **refused `plan`'s first attempt and passed after 12 citations were added** (turn 6). The gate shaped real prose, which no fixture could tell me. |
| **F-001** claim audit (step 9a) | `review-close` caught a false claim that had already reached **three documents** (turn 12) and corrected the overview to v6 — F-001's own scenario, caught earlier than the original. |
| **F-013** epic suspension | `EP-001 open → awaiting-answer, resume-to: open` on turn 2 — the move that was impossible before this session. |
| **F-014** pending-move gates | the worker observed `question.blocking.not-suspended` being correctly downgraded, and said so. |
| **F-017** honest headers | every timestamp is a `date -u` read; no fabricated headers anywhere in the trail. |
| **F-019** journal↔history | no `journal.status.unmatched` in the run — and when a corrupted row *did* appear (F-044) this is the check that exposed it. |
| **H-006** bounded turns | `turn-budget-exhausted` fired repeatedly at exactly three skills. Worker turns averaged **854s / 76 tools / $7.05**, against iteration 1's single turn at 3603s and 255 tool calls. |
| **H-007** closing turn | the impasse extension written *while configuring this run* fired on its first real occasion. |

### And it found 24 findings, eight of them mine

Every one was found by the worker or the stakeholder during the run. I found none of them by
reading code afterwards, which is the harness doing its job.

The two worst were both defects in work this session shipped, and both are now fixed:

- **F-037** — the citation rule made the append-only rule unsatisfiable. A journal entry
  correcting a malformed `[src: ...]` had to quote it; the linter read the quotation as a
  citation; and since no *appended* entry can remove a line the linter rejects, the worker had to
  rewrite an append-only entry — and recorded, in full, that it was violating
  `spec/journal-and-history.md` with no sanctioned exception. The record could not describe its
  own defect without reproducing it.
- **F-033** — `lint-claims` handed a file path treated it as the workspace root, found no `docs/`
  beneath it, and **exited 0 while printing "checked the whole tree"**: a gate reporting success
  when it examined nothing. The telling detail is that the worker built a working rule of thumb on
  top of the false pass.

---

## 5. What remains open

**38 fixed, 14 open, 1 rejected, 1 deferred.** Every `fixed` cites a commit, and `scripts/check`
step 11 now asserts each cited sha is actually in this repository's history — a check that exists
because all ten of my own citations were dangling until 1d's findings pass caught them (F-024).

| Open | |
|------|---|
| **F-045** | the epic sign-off gate does not fire on a run that ends in an impasse — **the most important one** |
| **F-028** | a deferred answer has no representation, and it undermines the F-011 fix |
| **F-029** (+F-042) | three skills need to create items and only two may — F-013's shape again |
| **F-031** | an `[auto]` Definition of Ready check that only tests file existence — F-001's class in a machine-decidable gate |
| **F-030** | `priority` is doing two jobs, so the board lies about what matters |
| **F-034**, **F-048** | `plan` writes source files to run its own gates; `plan` wrote a step telling `implement` to break a spec rule |
| **F-035**, **F-036**, **F-043** | `check-commit-refs` reports a merge that never happened; `new-item` leaves the workspace invalid silently; `--outcome` is unreachable in practice |
| **F-038** | a transition can leave the tracker committed-invalid — documented behaviour, undocumented window |
| **F-046** | a bug the pipeline filed is never shown to the stakeholder |
| **F-008** | async human interaction as a first-class mode — still deferred, still working at the prompt level |
| **F-010** | BMAD-derived imports — deliberately gated on §2 |

Two of these deserve saying plainly rather than leaving in a table.

**F-045 is the honest limit of this session's acceptance work.** F-022's gate fires on
`open → done`, and an epic with a blocked child never gets there — so 1d, the run built to
regression-test the acceptance loop, never evaluated it. The stakeholder went looking for the
question and wrote down that it never came: *"if this had ended with a report calling it 'done,'
I'd have had no record of ever being asked, and that's the part I'd have pushed back on hardest."*
The mechanism is proven by fixtures and by demonstration. The larger claim — that a stakeholder
gets a say at the end of an engagement — is **not yet true**, and I have not claimed it.

**F-028 is the same shape against F-011.** The rewritten precondition treats a non-empty
`## Answer` as answerable, and a deferral — "I'll send you a sample later", said three times — is
non-empty. Right for the case it addresses, blind to one the same run produced within minutes.

### Two limits of the fixes that *are* claimed

- **F-001's judging half is still an instruction.** The provenance half is a program: citations
  must exist and must resolve, enforced by a hard gate. The half that asks whether a citation
  *supports* its sentence is `review-close` step 9a — and instructions are precisely what F-001
  says do not hold. What changed is that it now has a mechanically guaranteed input and a much
  narrower question. It did catch a real three-document claim in 1d, which is more than the
  original did.
- **F-017 catches a version that is too high, not one that is too low.** A validator cannot tell
  a legitimately old entry from a fabricated low version, because the record is meant to span
  upgrades. The low case is prevented at the point of writing (the script reads the file), not
  detected at rest. A worker that ignores the script and hand-writes an old version string is not
  caught.

---

## 6. ROADMAP §2 — an honest read

The gate has three conditions. **One holds, one holds with a caveat, one does not.**

**(2) The three dead paths have each executed — HOLDS.**
The Definition of Ready override fired in 1d turn 5; the review send-back fired three times in
iteration 1; `blocked` fired in 1d turn 14 with a recovery path recorded. This condition is met,
and 1d is what met it.

**(3) The F-001 fix has survived a real run — HOLDS, with the caveat above.**
`claims-are-sourced` refused real prose and passed once cited; the claim audit caught a claim that
had spread to three documents. Wrong or unsourced justifications *were* caught at entry. The
caveat is that "the F-001 fix" now means two things, and only the provenance half is mechanical.
I would call this condition met for the half that was mechanised and unproven for the half that
was not.

**(1) A full consumer run completes with zero skill version bumps — DOES NOT HOLD, and is
further away than before.**
This session bumped every skill, which is expected — that is what a hardening session does. But
1d then produced 24 more findings, and fixing them will bump more. The condition is not a
criticism of the run; it is a thermometer, and it reads "still hardening". Nothing in five runs
has yet gone start-to-finish without the toolkit needing a change.

**So: the kernel is not proven, and the Codex adapter and the content-pack imports stay gated.**
That is the right answer. What did change is the shape of what remains: the findings 1d produced
are narrower than the ones iteration 1 produced — `--outcome` is undocumented, a gate's message is
misleading, a field does two jobs — rather than structural contradictions like "this escalation
cannot be represented". F-045 and F-029 are the two exceptions, and both are the *same* structural
shape as F-013: an instruction the state machine cannot carry out.

### Recommended next

1. **F-045**, then **F-029** — the two remaining structural contradictions. Both are cheap.
2. **F-028** — the deferral status, which blocks nothing today and will block the moment a
   stakeholder says "later" and means it.
3. **Iteration 2** (`tidy`) against the fixed toolkit, per the owner's review of 1d's trail.
4. The retro skill, once there are two hardening cycles to learn from — 1d is the second.
