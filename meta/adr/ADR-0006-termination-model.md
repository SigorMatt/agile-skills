# ADR-0006 — The termination model: how an engagement ends, and who may create work

- **Status:** accepted
- **Date:** 2026-08-27
- **Unit:** META-102
- **Supersedes:** patch-thinking on the F-013 class. F-013's own fix (ADR-less, META-087) stands
  and is re-derived here rather than reversed.
- **Findings:** F-013, F-029 (+F-042), F-045, F-046. Feeds F-028.

## Context

Four findings, filed across three runs by two different actors, are one design debt:

| Finding | The contradiction, in one line |
|---------|-------------------------------|
| F-013 | `intake`'s own instruction — "set the epic to `awaiting-answer` and stop" — was not a transition the state machine had. |
| F-029.1 | `answer-questions` accepted an answer that widened scope and had no way to record the implied work. |
| F-029.2 | `review-close`'s D12 audit found a defect belonging to a closed item and could not file it, because only `verify` may create a bug. |
| F-045 | The sign-off gate fires on `open → done`; an epic with a `blocked` child never reaches it, so the one ending where the stakeholder most needs to speak is the one ending that never asks. |
| F-046 | A bug the pipeline filed was never shown to the stakeholder, because nothing shows them anything except at closure. |

The shape is identical every time: **the status graph and the authority rules were derived from
the happy path**, and each non-happy path finds a rule the methodology instructs a skill to
break. Each was previously fixable by adding one row or one exception; that is what makes it a
class rather than five bugs, and adding a sixth exception is how the class survives.

The derivation below runs the other way round. It starts from the set of endings and the set of
events that change the item set, and reads the status graph and the authority table off that
enumeration. Where the enumeration and the current pipeline disagree, the pipeline is wrong.

Vocabulary: an **engagement** is one epic and every item whose `epic:` names it. The engagement
is the unit that begins with a raw idea and ends with a person being told what they got.

---

## 1. Every legal ending of an engagement

An engagement **ends** when no skill can advance any item in it and none ever will without a
person acting. That is one condition, and it is mechanical (§4). Four endings satisfy it.

| # | Ending | Epic's final state | Reached when |
|---|--------|-------------------|--------------|
| E1 | **delivered** | `done`, `outcome: delivered` | every child is `done`; every child's outcome is `delivered` or `duplicate`; the stakeholder accepted |
| E2 | **delivered-partial** | `done`, `outcome: delivered-partial` | every child is at a terminal status, at least one is not delivered (`blocked`, or `done`/`dropped`); the stakeholder accepted, with or without named follow-ups |
| E3 | **impasse** | `blocked` | every child is at a terminal status, at least one is not delivered, and the stakeholder did **not** accept — or deferred the acknowledgment. A person must act; the engagement is suspended, not closed |
| E4 | **abandoned by the stakeholder** | `done`, `outcome: dropped` | the stakeholder withdrew the engagement — through a request (`spec/request.md`), or in the answer to the termination question. Children not `done` go to `blocked` first, so the record says what was in flight when the plug was pulled |

Three consequences follow immediately, and each of them contradicts a rule that exists today.

**(a) `blocked` is an ending for an epic and a suspension for a work item.** A work item at
`blocked` sits inside an engagement that continues around it. An epic at `blocked` *is* the
engagement, and there is nothing around it. This is why E3 is an ending at all, and why F-045
could not be fixed by tightening the closure gate: the run it was filed from never reached
closure.

**(b) "Every child is `done`" (DE1) is a happy-path rule.** It is the entry condition for E1
only. E2, E3 and E4 all end with at least one child not `done`, and all three are legal. The
rule that generalises is **every child is at a terminal status** — `done` or `blocked` — with the
non-delivered ones *named*, which is a stronger requirement than DE1 ever made and is the one
F-046 was asking for.

**(c) An epic never escapes downward.** `transition` deliberately blocks a skill's hard gates
only on the move that declares its work complete, because trapping a skill that is trying to
file a question or send an item back is worse than letting it move (see `scripts/transition`, the
comment above `gating`). That reasoning is about *work in flight*. An epic has none: it advances
only through its children, so every move an epic makes out of `open` declares the engagement
finished. **For an epic, every terminal move is a completion move and must be gated.** Without
this, E3 is a hole exactly the size of F-045: `open → blocked` would run the sign-off gate and
ignore its verdict.

---

## 2. The termination gate

> No engagement ends, in any ending, without a blocking question addressed to the human that
> states what was delivered, what was not, and why.

F-022 built this as a **completion** gate. It generalises to a **termination** gate, and the
generalisation is not a widening of scope — it is the discovery that "completion" was never the
right trigger. The stakeholder's own words, from the run that ended at an impasse, are the
argument:

> "I expected that before anyone called this engagement finished, someone would ask me straight
> out whether I accept it as it stands — and I was ready to say no… That question never came."

Rules, each derived from an ending in §1:

1. **Trigger.** The question is filed when the engagement reaches **rest** (§4) — not when the
   last child closes. E1's rest and E1's closure coincide, which is why the narrower trigger
   looked sufficient for a year of happy paths.
2. **Content.** `## Question` names **every child of the epic**, each as delivered or not, each
   with one line of why. Naming every child is what makes F-046 mechanical: a bug the pipeline
   filed and never fixed is a child, so it is in the statement, so the stakeholder sees it. A
   sign-off that lists only the good news is the failure this rule exists to prevent, and
   "list what was not delivered" is not checkable while "name every child" is.
3. **Addressee and blocking.** `addressed-to: human`, `blocking: true`. Nobody accepts on the
   stakeholder's behalf, and an acknowledgment that does not stop the engagement is a formality.
4. **The answer selects the ending.** Accept → E1 or E2 by whether every child delivered. Do not
   accept → E3. Withdraw → E4. Defer → E3, with the deferral recorded (F-028; a deferred
   acknowledgment is not an acknowledgment, and pretending otherwise is the lie the deferral
   status exists to avoid).
5. **A "no" is as legal as a "yes".** The criterion is that the question was asked and answered,
   never that the answer was favourable. E3 exists so that a refusal has somewhere honest to go.
6. **Asked once per rest.** If the engagement re-enters rest after new work (a follow-up item, a
   reopened epic), the acknowledgment is due again, because it would otherwise be an acceptance
   of something the stakeholder has not seen. This is the existing staleness rule
   (`check-epic-signoff`'s "filed after the last child closed") restated against rest.

**Who ends an engagement.** Only `review-close`. Ending requires applying the epic Definition of
Done and reading the acknowledgment, and both are already its job. So the generic
`any-suspendable → blocked` transition — actor `any` — stops applying to epics, and an epic
reaches `blocked` only through `review-close`, gated. An epic-level *question* may still suspend
the epic from anywhere (F-013's fix); an epic-level *ending* may not.

---

## 3. Mid-flight events that change the item set, and the creation authority they imply

An engagement's item set is not fixed at intake. Enumerating the events that change it produces
the authority table directly — which is the point, because F-029 is what happens when the table
is written from the happy path and the events are discovered afterwards.

| Event | Who observes it | What must be created | Provenance |
|-------|-----------------|----------------------|------------|
| The raw idea is refined into work | `intake` | the epic at `open`, work items at `draft` | `docs/product/vision.md` |
| The stakeholder speaks unprompted | `intake`, routed by `next` step 2 | a work item at `draft`, or a decline recorded on the request | the request `R-###` |
| Refinement finds the item is two items (DoR **R9**) | `refine` | the sibling work item at `draft` | the item being split |
| An answer widens the scope (**F-029.1**) | `answer-questions` | a work item at `draft` | the question `<ITEM>/Q-###` |
| Verification finds a defect in *delivered* behaviour | `verify` | a bug at `ready` | the item it was found against |
| Review finds a defect belonging to another item (**F-029.2**) | `review-close` | a bug at `ready` | the item under review |
| A defect is found after the epic closed | any skill | a bug at `ready`, and the epic reopens | the bug |

Read off it:

| Actor | May create | At | Provenance it must record |
|-------|-----------|----|---------------------------|
| `intake` | epic, work-item | `open`, `draft` | the vision, or a request `R-###` |
| `refine` | work-item | `draft` | the item it split (`arose-from`) |
| `answer-questions` | work-item | `draft` | the question whose answer widened scope (`arose-from`) |
| `verify` | bug | `ready` | `found-in`, and `arose-from` |
| `review-close` | bug | `ready` | `found-in` where known, and `arose-from` |
| `plan`, `implement`, `next` | — | — | — |

**The rule, stated once so that the next case is decided rather than argued:**

> A skill may create an item exactly when it is the skill that **observes the need** for it, and
> only if it records **what caused the item to exist** in a citation that resolves. Nothing may
> create an item past `draft` (a bug at `ready` is the one exception, and it is not one: a bug
> filed with reproduction steps has *already satisfied* its Definition of Ready — `dor-dod.md`
> §2 — so `ready` is where it is born, not a status it skipped to).

`plan` and `implement` are excluded by the same rule, not by an exception: neither observes a
*need for new work*. `plan` observes uncertainty, which is a question; `implement` observes
scope creep, which is a question too. `next` observes nothing — it knows no engineering.

**Provenance is a new required field**, `arose-from`, because the authority table is only
enforceable if the creating skill's claim is checkable. Without it "who may create" degrades
into "who says they may", and an item created for no recorded reason is indistinguishable from
one invented to make a gate pass.

---

## 4. Rest, mechanically

Every rule above turns on "the engagement is at rest", so rest must be a program, not a
judgement — this is F-001's thesis applied to the derivation itself. An engagement is at rest
when **all** of:

1. every child of the epic is at a terminal status (`done` or `blocked`);
2. no question anywhere in the engagement — on the epic or on any child — is `open`;
3. no request in `tracker/requests/` is `open`.

`scripts/engagement-state <EP-ID>` decides it and prints why. `next` reads it rather than judging
it, and `check-epic-signoff` reads it to date the acknowledgment. Two consumers, one
implementation, no possibility of the orchestrator and the gate disagreeing about whether an
engagement is over — which is the disagreement that produced F-045 in the first place.

The orchestrator gains exactly one step, between "dispatch the status owner" and "report and
stop": **if the engagement is at rest and the epic is still `open`, dispatch `review-close` on
the epic.** It terminates because both of `review-close`'s legal moves from there —
`open → awaiting-answer` to ask, and `open → done`/`open → blocked` to end — leave `open`.

That step is where 1d stopped and reported. The whole of F-045 is that the pipeline had no name
for the state it was in, so it printed a board and called it a day.

---

## 5. Every historical contradiction, against the derived model

Each is a fixture in META-107. This is the list the fixtures must cover, and the reason the
derivation is not self-congratulatory: it has to re-decide the cases that produced it.

| Case | The derived model's answer | Fixture |
|------|---------------------------|---------|
| **F-013** — a blocking question on an epic at `open` | Legal. `open` is terminal (the pipeline does not advance it) and suspendable (a person's question may stop it). Unchanged from META-087, now derived rather than patched. | must-pass: an epic suspended at `awaiting-answer` with `resume-to: open` |
| **F-029.1** — an answer widens scope | `answer-questions` creates a work item at `draft` with `arose-from: <ITEM>/Q-###` | must-pass; and must-fail without the provenance |
| **F-029.2** — review finds someone else's defect | `review-close` creates a bug at `ready` with `arose-from` and `found-in` | must-pass; and must-fail for `plan` attempting the same |
| **F-045** — the run ends at an impasse | E3. Rest is reached, `review-close` is dispatched on the epic, the acknowledgment is filed, the answer is "no", the epic goes to `blocked` — gated | must-fail: an epic at `blocked` with no answered acknowledgment |
| **F-046** — a filed bug nobody showed the stakeholder | It is a child, so §2 rule 2 puts it in the statement by name | must-fail: an acknowledgment that omits a child |

---

## 6. What this costs, said plainly

- **A version bump on almost everything.** `pipeline.yaml`, `review-close`, `answer-questions`,
  `next`, `refine`, `verify`, and four spec files. ROADMAP §2 condition 1 ("a full consumer run
  with zero version bumps") moves further away, not closer. That is the honest read: this
  session is hardening, and the thermometer says so.
- **A new required frontmatter field.** `arose-from` on items created by `refine`,
  `answer-questions`, `verify` and `review-close`. Existing workspaces do not carry it; the rule
  is scoped to the creation row's actor, so items created by `intake` — every item in every
  banked run — are unaffected.
- **One more script.** `scripts/engagement-state`. The alternative was the same rest test written
  twice, in `next`'s prose and in the gate's code, which is the arrangement that produced F-045.
- **Two rules that remain instructions.** "Name every child with one line of why" is checkable
  for *naming* and not for *why*; and whether an acknowledgment is honestly shaped is a person's
  read of it. Both are stated where a reader can see the limit rather than claimed as mechanical.

## Alternatives rejected

- **Fix F-045 alone by letting the closure gate fire on `blocked`.** The sixth exception. It
  leaves F-029 untouched and leaves the next non-happy ending — abandonment — to find the next
  contradiction.
- **Make `open` non-terminal and give the epic an owning skill.** Then `next` dispatches
  `review-close` on the epic on every pass, and the epic competes with its own children for the
  selection key. Rest is the condition that makes epic dispatch correct exactly once.
- **Close the epic as `done` on an impasse, with an outcome saying "not accepted".** It reads
  fine and it is a lie: in the run this was derived from the stakeholder said "I'll send the file
  and then we can finish it". `done` would have closed a thing they had just said was not
  finished.
- **Let any skill create any item, and check provenance only.** Provenance answers *why*; the
  authority table answers *who*, and the two failures are different. `implement` filing its own
  follow-up work with a citation is still `implement` widening its own scope.
