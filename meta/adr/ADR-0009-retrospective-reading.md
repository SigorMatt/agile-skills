# ADR-0009 — Retrospective reading: the team studying itself from the record it left

- **Status:** accepted
- **Date:** 2026-08-30
- **Unit:** META-133
- **Supersedes:** nothing. It extends ADR-0006 — which defined every legal *ending* of an
  engagement — with what happens after one, and it borrows ADR-0008's honesty structure for a
  gate whose subject is judgement.
- **Findings:** the whole ledger is this ADR's context. Directly: F-001 (a gate that rests on a
  judgement read does not hold), F-033 / F-066 (a gate that examined nothing is not a pass),
  F-062 (the marquee case a retro must be able to see), ROADMAP §3 (the retro skill, pulled
  forward).

## Context

This repository's own findings ledger was produced by a loop the owner ran by hand: a run
finished, the owner and the assistant read its trail, and what the reading found was appended to
`meta/findings/FINDINGS.md` as F-### entries with evidence pointers, a component, a direction and
an honest severity. Eighty-seven findings, seven builder sessions, and a kernel that ROADMAP §2
now calls proven — all of it came out of that loop. The loop is the most valuable thing in the
project and it is the one part of it that does not ship.

The retro skill is that loop, written down as a contract so that a consumer's own engagement can
run it. Two things follow immediately from taking that sentence literally, and they shape
everything below.

**A consumer has no harness.** Every reading the owner did had a SIM-LOG beside it: a second
record, written by the person the engagement was for, saying what they thought while it happened.
Nothing in a real engagement produces that. The retro's input is the workspace record and nothing
else — tracker, docs, questions, journals, history, the git log. If a finding is only visible in
the SIM-LOG, the retro cannot find it, and pretending otherwise would put the skill's calibration
on a foundation no consumer has.

**A consumer has no ledger.** The eighty-seven filed findings are this project's corpus and the
reason its findings are written the way they are. A consumer starts with none. So the quality bar
cannot be transmitted by example the way it was learned here; it has to be written into the
procedure itself. `process.md` carries the bar or the bar does not ship.

The evidence that this is worth doing is in the record already. Iteration 3's `WI-0004` journal
says, in the pipeline's own words, *"Fixed two false claims where the review named one"* — one of
them a sentence the stakeholder had written, quoted with `[src: WI-0002/Q-001]` on it, repaired
rather than escalated to its author. That became F-062, the structural finding that opened builder
session three. It is visible in the record with no SIM-LOG at all. So is the fact that
`docs/product/vision.md` had been sent back on the same two Definition-of-Done criteria twice,
which the same entry records in one line. A reader who knows what to look for can find both.

---

## 1. What a retro is, and what it is not

A **retro** is one execution of a `process-analyst` over one **ended** engagement, producing one
report. It is:

- **an audit of the record, not of the product.** It asks how the work went and what the trail
  says about the way the trail was made. Whether the software is any good was `verify`'s and
  `review-close`'s question and it was answered before the ending.
- **read-only over the engagement it studies.** This is a refusal, not a preference: an auditor
  that can edit its subject has no way to prove it did not edit the evidence into agreement with
  its conclusions. The retro's only writes are its own report and its own journal entry.
- **not a gate on anybody.** The stakeholder's engagement ended at sign-off (ADR-0006). Nothing
  the retro finds re-opens it, delays it, or is shown to the person before they are told the work
  is done. The retro is the team studying itself.

It is **not** a review, a post-mortem of an incident, or a quality report on the delivered
software, and it is not a second chance to litigate a decision the record shows was made and
journaled.

### 1.1 Read-only, stated as the boundary a lint can hold

The retro writes exactly two paths:

| Path | Kind |
|------|------|
| `tracker/items/<EP>/artifacts/retro.md` | new file — the report |
| `tracker/items/<EP>/journal.md` | append — the execution's own entry |

It appends no history row, because it changes no status. It files **no questions** — for the same
reason `next` files none, and one more: the engagement has ended, so a blocking question would
suspend an item that has nowhere to resume to, and a question addressed to the human would ask a
person who has already been told the work is finished. Its escalation channel is the report.

It follows that the retro cannot open a bug, cannot reopen the epic, and cannot correct a
document it finds to be wrong. If it finds a real defect in delivered behaviour it says so, in
the report, as a proposal for a human to act on. This is a real cost and it is accepted
deliberately: a retro that can create work for itself out of what it audits is indistinguishable,
in the record, from one re-litigating a decision it disagreed with.

---

## 2. When it runs

**After an ending, before the engagement is archived as fully closed.** Concretely, `next` gains
one orchestrator step, between "end an engagement that is over" and "report and stop":

> For each epic whose `scripts/engagement-state` verdict is `ended`, dispatch `retro` on it and
> stop.

Three consequences, each deliberate.

**The verdict comes from the script, not from the scheduler.** `engagement-state` gains a fifth
verdict, `closed` — *ended, and the retro report exists* — so `ended` now means *the ending is
recorded and the retro has not been written yet*. This is F-045's lesson applied a second time:
the orchestrator does not decide what "over" means, and it does not decide what "fully closed"
means either. One function, three consumers.

**The step terminates.** Writing the report changes the verdict from `ended` to `closed`, so the
epic cannot be dispatched here twice for the same reason. That is the same termination argument
step 6 makes, and it is why the report is written on *every* execution — including one that finds
nothing. An empty finding list is a result; a missing report is a loop.

**Nothing already valid becomes invalid.** `validate-workspace` does not require `retro.md`, no
gate depends on it, and no existing workspace — `examples/toy-project`, every fixture, every
banked run — changes verdict class or fails a check because the skill now exists. The retro is
*dispatched* automatically and *enforced* nowhere. It has to be that way: after the ending there
is nobody left to escalate a refusal to.

### 2.1 Why not earlier, and why not per item

A retro that runs during the engagement judges incomplete work, and — worse — changes the run it
is observing, because its output would be visible to the skills still executing. A retro per item
would produce a dozen small readings none of which can see the shape that only appears across
items: *the same document was sent back on the same two criteria twice* is not visible from
inside either item.

---

## 3. What it reads

The **record** is the input, and it is enumerated so that "I read the workspace" is a checkable
claim rather than a gesture:

| Source | What it carries |
|--------|-----------------|
| `tracker/items/*/history.md` | the timeline: every status change, its actor, its reason, every send-back and every suspension |
| `tracker/items/*/journal.md` | the reasoning: decisions with rationale, inputs actually read, gates with verdicts, commands with outcomes |
| `tracker/items/*/item.md` | criteria, their tick state, outcomes, `## Notes` and any accepted gap recorded there |
| `tracker/items/*/questions/*.md` | who was asked what, by whom, when, what came back, and what the cross-answer check said |
| `tracker/items/*/artifacts/*` | plan, impl-report, verify-report, review, refinement-qa — what each stage claimed |
| `tracker/requests/*.md` | what the stakeholder said on their own initiative |
| `docs/**` | the deliverable documents, their version headers and their change logs |
| `tracker/board.md`, `tracker/project.yaml` | the shape of the engagement and its commands |
| the git log | when work actually happened, and whether the commits match the record |
| the installed skill contracts | what each skill was *obliged* to do, needed to tell "the gate held" from "the worker was careful" |

The last row is the one worth defending. Without the contracts, the question *"did that gate pass
on the contract or on the worker's discipline?"* — one of the four readings the mission asks for —
cannot be answered at all, only guessed at. The contracts are installed in every consumer project
by construction, they are versioned, and the record names the version that acted in every journal
heading. So they are available, they are honest, and they are not part of the *record*: the retro
reads them as the yardstick, never as evidence about the engagement.

**Not read, ever:** anything outside the workspace and those contracts. No SIM-LOG, no harness run
directory, no `HARNESS-STATUS.md`, no upstream findings ledger, no conversation. Two of those are
absent in a consumer project; the ledger is absent on purpose, because a retro that has read the
answers is not measuring anything.

---

## 4. Two audiences, one report

The report has two jobs and they must not be allowed to blur, because they are read by different
people for different purposes and the second one leaves the project.

**Audience one — the team, about this engagement.** Observations about how *this* work went:
where a skill misled itself, where a question was late or went to the wrong addressee, where a
gate passed on discipline rather than on contract, where the trail cannot explain itself. This is
the section that is worth reading once and then never again.

**Audience two — upstream, about the toolkit.** Candidate findings in the ledger's own format,
explicitly marked `PROPOSED`, each with evidence pointers into this engagement's record, for a
human to triage into the upstream ledger. This is the community feedback engine of the
open-source era: every consumer's retro can generate upstream findings, and none of them can file
one directly.

They are separated **in the document, by section**, not merely in tone, because the second
section is meant to be lifted out and sent somewhere. A proposal that only makes sense beside a
paragraph in the first section is not exportable and therefore not a proposal.

A third section, **the positive record**, is not decoration. This project's ledger keeps
"Positive record" sections for the same reason: a reading that only reports faults cannot
distinguish a run that went well from a reading that was lazy, and the fixes worth keeping are
the ones a later run can be shown to have benefited from.

### 4.1 A proposal is not a finding

Proposals carry a local ID (`P-1`, `P-2`, …), never an `F-###`. Allocating a number in the
upstream sequence from inside a consumer's workspace would collide with every other consumer
doing the same. `PROPOSED` is stated in the entry, not implied by its section — the block is
designed to be copied out, and a copied block that has lost the word is a finding nobody filed.

---

## 5. The classification, and the failure mode it exists to prevent

Every entry in the proposals section carries exactly one **classification**, from a closed set:

| Classification | Means | Exportable? |
|----------------|-------|-------------|
| `toolkit-defect` | a skill, spec rule, or script would mislead **any** engagement that reached this situation | yes — this is the class upstream wants |
| `project-circumstance` | this engagement's own difficulty: the domain, the codebase, the stakeholder changing their mind, a flaky test | no — recorded, not proposed |
| `observation` | a fact about how the work went that is neither a defect nor a circumstance | no |

**The failure mode to design against is misclassifying "this project was hard" as "the skill is
broken."** It is the failure mode because it is the cheap one: a retro that reads a difficult
engagement finds friction everywhere, and every piece of friction can be phrased as a complaint
about a tool. A ledger that fills with those stops being read, and then the real defects arrive
into a channel nobody is reading — which is the same death F-062's ADR predicted for a gate that
demands fifty-eight reconciliations.

Nothing mechanical can decide the classification. What can be made mechanical is that the
distinguishing work was *done and written down*, so that a wrong call is attributable rather than
absent — ADR-0008 §4's move, applied again. Two required fields on every `toolkit-defect`:

- **`Counterfactual:`** — what a *different* engagement, on a different subject, would hit here.
  A proposal whose counterfactual can only be stated in this project's own subject matter is a
  `project-circumstance` by construction, and writing the sentence is what exposes that.
- **`Recurrence:`** — did it happen more than once in this engagement, and where. One occurrence
  is allowed to be a finding — most of this ledger's are — but "once" and "four times" are
  different severities and the reader is entitled to know which.

And one rule with no exception: **the class, not the specimen.** A proposal is written about the
rule that failed, not about the sentence that failed it. `"WI-0004's AC5 was checked against the
test suite"` is a specimen; `"a criterion about other criteria is satisfiable by a coverage gap"`
is the finding, and it is the one that became F-065.

---

## 6. Evidence: one citation vocabulary, reused

**Every observation and every proposal cites its evidence, and an uncited one is a refused
write.** The project has said this about documents since F-001; a retro whose observations are
uncited is asking to be believed about a record the reader is holding.

The citation forms are the ones `spec/doc-header.md` §4a already defines and
`scripts/lib/claims.py` already resolves — a workspace path, an item, `ITEM ACn`, `ITEM/Q-nnn`,
an ADR number, a commit sha, and `run: <command> → <outcome>`. Nothing new is invented, which
means the retro's citations are checked by the resolver that checks everything else. One
vocabulary, one resolver, and a citation that stops resolving is caught by the same code path
that catches it in an ADR.

Two forms matter enough to name: a `tracker/...` path with a line number is how a journal
sentence is cited, and `<ITEM>/Q-nnn` is how an exchange with a person is. Both resolve today.

The known limit is F-001's own residual, recorded at the 2026-08-30 addendum: **a citation that
resolves is not a citation that supports the sentence.** `lint-retro` inherits that boundary
exactly and claims nothing beyond it.

---

## 7. Non-vacuity: a retro that read nothing is not a clean retro

F-033 and F-066 are the same finding twice — a gate exits 0 having examined nothing — and both
were found in this project's own scripts. A skill whose entire job is *reading* is the most
exposed thing yet written to that failure, and it fails silently: a report with an empty
observations list is exactly what a diligent retro of a flawless engagement produces, and exactly
what a retro that opened no files produces.

So the report declares its own scope, in a `## What was read` section that names the items, the
journal entries, the questions and the documents actually opened — and `lint-retro` refuses a
report whose declared scope is degenerate: fewer items than the engagement has, or no journal
entry at all. The scope is checked against the workspace, not taken on trust, for the same reason
`--changed-since` refuses a window that could not have contained anything.

This is the one place where the retro's own honesty is machine-checkable, and it is worth more
than any check on its conclusions.

---

## 8. What `lint-retro` can and cannot see

Stated plainly, because a gate whose limits are not written down gets trusted for things it does
not do.

**It can see:**

- that the report exists at the contracted path, with the required sections, for an engagement
  that has ended;
- that `## What was read` names a scope that exists in the workspace and is not degenerate (§7);
- that every observation and every proposal carries at least one citation, and that every
  citation resolves;
- that every proposal carries a classification from the closed set, a severity, a component, a
  symptom, a direction, and `PROPOSED` in its own text;
- that every `toolkit-defect` proposal carries `Counterfactual:` and `Recurrence:`, and names a
  component that is a real part of the toolkit;
- that the report changed nothing else — the retro's execution touched only the two paths of
  §1.1.

**It cannot see:**

- **whether an observation is true.** It resolves the citation; it does not read the cited text
  and judge whether it supports the sentence (§6, F-001's residual).
- **whether a classification is right.** The misclassification failure mode of §5 is judgement.
  The defence is that the counterfactual must be *written*, so the wrong call is in the record
  with a name on it instead of being an absence.
- **whether the retro found everything.** Recall cannot be measured from inside: the report is
  the only thing the lint has, and a retro that missed a finding produces a report identical in
  shape to one that found it. This is why the skill's calibration is established by a
  ground-truth test against engagements whose findings are already known (META-140) rather than
  by a gate, and why that test is a **reading**, not a pass/fail.
- **whether a proposal duplicates one already filed upstream.** The retro has not read the
  upstream ledger (§3) and must not: a triager de-duplicates, which is the job the word
  `PROPOSED` hands them.

---

## 9. Persona

`process-analyst`, added to `spec/skill-contract.md`'s persona enum by this ADR. The existing
enum has six roles and every one of them was on the team: `reviewer` reviewed this work,
`architect` decided it, `qa-engineer` verified it. The retro's whole standing rests on not having
been one of them — it reads a record it did not write, it has no work of its own to defend, and
it is the one role in the system whose subject is the process rather than the product. Reusing
`reviewer` would put the person who signed the engagement off in charge of judging how it went.

---

## Alternatives rejected

- **Let the retro file bugs and findings directly.** Rejected: §1.1. It makes the auditor a
  participant, and the record loses the ability to distinguish an audit from a second review.
- **Gate the ending on the retro** — the epic does not reach `done` until the retro is written.
  Rejected: it makes the stakeholder wait on the team's bookkeeping, and it inverts ADR-0006,
  where the ending *is* the stakeholder's answer. It also has no escalation path when the retro
  cannot be produced.
- **Put the proposals in a separate file** from the engagement-local report. Rejected: two files
  means two things to find and one of them will drift. The export boundary is a section heading,
  and §4's rule — a proposal that only makes sense beside the observations is not a proposal —
  keeps the section liftable without a second file.
- **Give the retro the SIM-LOG when one exists.** Rejected: it would calibrate the skill on an
  input no consumer has, and every measurement taken with it would overstate what the skill can
  do in the field. The harness's own iterations are read by the retro exactly as a consumer's
  engagement is (META-140), which is the only way the numbers mean anything.
- **A model-graded check on classification correctness.** Rejected for F-001's reason, the same
  way ADR-0008 rejected semantic conflict detection: a judgement gate wearing a program's
  clothes. If it is judgement it belongs in a contract, where its failures are attributable.
- **Number proposals as `F-###`.** Rejected: §4.1. Every consumer would allocate the same
  numbers.
