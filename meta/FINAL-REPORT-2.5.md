# Builder session 2.5 — final report

Mission: [`meta/BUILDER-2.5-PROMPT.md`](BUILDER-2.5-PROMPT.md). Backlog:
[`meta/findings/FINDINGS.md`](findings/FINDINGS.md). Units META-102 … META-112, all on `main`.

A compact session between builder two and iteration 2, with two jobs: derive the termination
model once so that the F-013 class stops recurring, and close the correctness findings that
would corrupt iteration 2's evidence.

---

## 1. The derivation, and what it decided

[`ADR-0006`](adr/ADR-0006-termination-model.md) is the centrepiece. Four findings — F-013,
F-029 (+F-042), F-045, F-046 — filed across three runs by two different actors, are one design
debt: **the status graph and the authority rules were derived from the happy path**, so every
non-happy ending finds a rule the methodology instructs a skill to break. Each was individually
fixable by adding one row or one exception, which is what made it a class rather than five bugs.

The derivation runs the other way round: start from the set of legal endings and the set of
events that change the item set, and read the status graph and the authority table off that
enumeration.

### The four endings

An **engagement** is one epic and every item whose `epic:` names it. It **ends** when no skill
can advance any item in it and none ever will without a person acting.

| | Ending | Epic's final state |
|---|--------|-------------------|
| E1 | delivered | `done`, `outcome: delivered` |
| E2 | delivered-partial | `done`, `outcome: delivered-partial` |
| E3 | impasse | `blocked` |
| E4 | abandoned by the stakeholder | `done`, `outcome: dropped` |

**No engagement ends, in any ending, without a blocking human-addressed question stating what
was delivered, what was not, and why.** F-022 built that as a *completion* gate; it is now a
**termination** gate, and the generalisation is not a widening — it is the discovery that
"completion" was never the right trigger.

### Four things the enumeration decided that I had not expected

1. **`blocked` means two different things.** For a work item it is a suspension: the engagement
   continues around it. For an epic it *is* the engagement, so there is nothing to continue.
   That single distinction is the whole of F-045 — the gate fired on `open → done`, and the run
   that needed it most never got there.
2. **DE1 was an entry condition for one ending out of four.** "Every child item is `done`"
   describes E1. What generalises is **terminal, and named**: every child has stopped, and every
   child that did not deliver appears by ID in the termination statement. That is strictly
   stronger than the rule it replaces — DE1 never required anyone to say *which* children
   delivered — and it dissolves **F-046** into a consequence rather than a separate fix.
   "List what was not delivered" cannot be checked; "name every child" can.
3. **An epic never escapes downward, so every terminal move it makes is a completion move.**
   `transition` refuses only a skill's `next_status`, for a good reason: do not trap a skill that
   is filing a question or sending an item back. That reasoning is about work in flight, and an
   epic has none. Without a per-transition `gated` flag, `open → blocked` would have run the
   acknowledgment gate and ignored its verdict — F-045 reappearing three feet to the left.
4. **F-029 had a third occurrence nobody had filed.** Listing the events that change the item set
   produces the authority table directly, and Definition of Ready **R9** instructs `refine` to
   split an item into two — which `refine` had no authority to do.

### The creation-authority table

> A skill may create an item exactly when it is the skill that **observes the need** for it, and
> only if it records **what caused the item to exist** in a citation that resolves.

| Actor | May create | At | Provenance |
|-------|-----------|----|-----------|
| `intake` | epic, work-item | `open`, `draft` | the vision, or a request `R-###` |
| `refine` | work-item | `draft` | the item it split (R9) |
| `answer-questions` | work-item | `draft` | the question whose answer widened scope |
| `verify` | bug | `ready` | `found-in`, or `arose-from` |
| `review-close` | bug | `ready` | `found-in`, or `arose-from` |
| `plan`, `implement`, `next` | — | — | — |

`plan` and `implement` are excluded **by the rule**, not by omission: `plan` observes
uncertainty, which is a question, and `implement` observes scope creep, which is a question too.

### Rest is a program, not a judgement

Every rule above turns on "the engagement is at rest", so `scripts/lib/engagement.py` decides it
and **both** consumers read the same function: `scripts/engagement-state`, which `next`'s new
orchestrator step 6 reads, and `check-epic-signoff`, which dates the acknowledgment against it.
The orchestrator and the gate disagreeing about whether an engagement is over is precisely how
F-045 happened.

---

## 2. Versions bumped

| Contract | Was | Now | Why |
|----------|-----|-----|-----|
| `pipeline.yaml` | 0.3.0 | **0.4.0** | transitions declare `applies_to`, `gated` and `provenance`; the epic ending rows; the deferral row; orchestrator step 6 |
| `review-close` | 0.3.1 | **0.4.0** | it ends engagements: dispatched on an epic at rest, the four endings, and the authority to file a bug it found |
| `next` | 0.2.0 | **0.3.0** | orchestrator step 6, read from `engagement-state` rather than judged |
| `answer-questions` | 0.1.4 | **0.2.0** | the deferral fork (F-028); creating the work an answer implied (F-029) |
| `plan` | 0.2.0 | **0.3.0** | the `## Scaffolding` carve-out (F-034, ADR-0007) |
| `refine` | 0.2.0 | **0.2.1** | the authority and provenance for an R9 split |
| `verify` | 0.1.2 | **0.1.3** | `found-in` named as provenance |

Specs, each with a `## Revisions` row: `ids-and-statuses.md` (§3.5 the endings, §4 the transition
table, **new §5** creation authority), `work-item.md` (**new** revisions table: `arose-from`,
`delivered-partial`), `dor-dod.md` (DE1, DE7, R8), `question.md` (`status: deferred`, `kind:
sign-off` as the termination question), `workspace-layout.md` (§1.3 `refinement-qa.md`'s status
field, §5 the scaffolding carve-out), `skill-contract.md` (§2.3 the committed-invalid window).

New: `scripts/engagement-state`, `scripts/lib/engagement.py`, both shipped by the adapter.
New ADRs: [ADR-0006](adr/ADR-0006-termination-model.md),
[ADR-0007](adr/ADR-0007-plan-and-scaffolding.md).

---

## 3. The gate

`./scripts/check` went from 13 assertions to 16, across 14 numbered steps. Three are new:

| Step | What it asserts | For |
|------|-----------------|-----|
| **the termination gate at every ending** | `check-epic-signoff` over `fixtures/ended-engagement`: five epics, one per verdict it has to reach, plus `engagement-state`'s own two | F-045, F-046 |
| **pipeline invariants refuse each injected fault** | `methodology/` copied to a temp tree, one defect reintroduced into `pipeline.yaml` at a time, the expected finding code asserted — five faults | F-013, F-029, F-045 |
| **the derived model, by execution** | twelve cases against a workspace built by the real tools: creation authority refused and permitted through `new-item`, an epic suspended, and **an engagement refused an ending while nobody had asked the stakeholder** | F-013, F-029, F-045 |

The last one is the session in a line. `review-close` moving an epic `open → blocked` with no
acknowledgment on file is refused by a hard gate, not by anyone's discipline.

F-013's own defect is now a mechanical must-fail case rather than a sentence saying somebody once
flipped the value back and watched.

---

## 4. The correctness batch

| Finding | What it is now |
|---------|----------------|
| **F-028** | `status: deferred` — the reply that is neither an answer nor silence. `answer-questions` step 3a is **two moves, take one**: decide under the deferral (the question is `answered`, quoting it), or record `deferred` and park the item at `blocked` with what would unblock it. Enforced by `question.deferred.not-blocked` and by a gate that asks which move was taken |
| **F-031** | DoR R8 reads `refinement-qa.md`'s `status: agenda \| recorded` field, not the filename. An `[auto]` criterion that checks the wrong thing is worse than a manual one, because nobody re-reads it |
| **F-034** | ADR-0007: `plan` may create behaviour-free scaffolding a declared gate command needs in order to execute, listed under a required `## Scaffolding` heading. A stub function with a `pass` body is explicitly **not** scaffolding |
| **F-038** | `spec/skill-contract.md` §2.3 states the window *and* the obligation it creates: a skill MUST NOT end an execution while the validator reports errors — fix them, or name each and why it is not yours |

F-044, F-025, F-047, F-032 and F-039 were already fixed by builder two; the mission listed them
conditionally and none was still open.

### Found within the session

`scripts/check`'s "findings citations resolve" step matched `commit <sha>` and not
`commits a, b, c`. Every citation this session wrote is plural — a fix derived across seven units
cites seven commits — so the step reported PASS having checked the sixteen old singular citations
and none of the new ones. That is **F-024 verbatim, inside the step that exists to catch it**.
Fixed: 17 cited → 24, all resolving.

---

## 5. Riding along open, on purpose

**F-008, F-030, F-035, F-036, F-043, F-048** — UX and low-severity items the mission said to
leave. Their statuses are honest and iteration 2+ evidence will prioritise them naturally. Scope
discipline outranks completeness in a .5 session.

**45 fixed, 6 open, 1 rejected, 1 deferred.**

---
