# `questions/Q-###.md` — the escalation protocol

A question is a **first-class artifact**, not a message. It has a file, an ID, a state, and a
recorded consequence. This is the mechanism that lets `implement` and `verify` be blocked by
something they must not decide, without either guessing or interrupting the human.

Location: `tracker/items/<ID>/questions/Q-###.md`, numbered per item.

---

## 1. Who may ask whom

| Skill | May ask the human directly | May file a question |
|-------|---------------------------|---------------------|
| `intake` | yes — it is a conversation | rarely; prefers to ask now |
| `refine` | yes — it is a conversation | rarely; prefers to ask now |
| `plan` | yes, as a last resort | yes |
| `implement` | **never** | yes |
| `verify` | **never** | yes |
| `review-close` | **never** | yes |
| `answer-questions` | yes, when it cannot answer from the record | it answers them |

`plan`'s preference order is fixed and MUST be followed in this order:

1. Answer it from existing documentation. Cite what you read.
2. Make a **reversible** assumption, record it in the plan under `## Assumptions`, and continue.
3. Ask the human — only when the decision is not reversible, or when it depends on intent that
   no document captures.

The reason `implement` and `verify` may never ask directly is not politeness. It is that a
question answered in chat leaves no artifact, so the next execution of the same skill — after a
restart, or on a sibling item — cannot see the answer and will ask again or guess differently.
Answers must land in documents, which is what `answer-questions` is for.

---

## 2. File format

```markdown
---
id: Q-001
item: WI-0007
from-skill: implement
addressed-to: architect
blocking: true
status: open
created: 2026-08-16T11:05:52Z
---

## Context

What I was doing, what I read, and where the record stops short. Enough that the answerer does
not have to re-derive it.

## Question

One question, stated so that it can be answered. If there is more than one, file more than one
question.

## Options considered

- **A —** <option>. Consequence: <what follows>.
- **B —** <option>. Consequence: <what follows>.
- **Recommendation:** <which, and why> — or `none, insufficient basis`.

## Answer

<!-- filled in by answer-questions -->

## Consequences

<!-- filled in by answer-questions: which documents, plans, or items changed as a result -->
```

### Frontmatter fields

| Field | Required | Rules |
|-------|----------|-------|
| `id` | always | `Q-###`, matching the filename, unique within this item |
| `item` | always | the owning item's ID; MUST match the containing directory |
| `from-skill` | always | the skill that filed it |
| `addressed-to` | always | `architect` \| `human` |
| `blocking` | always | `true` \| `false` |
| `status` | always | `open` \| `answered` \| `deferred` |
| `created` | always | UTC ISO-8601 |
| `answered-at` | when `answered` or `deferred` | UTC ISO-8601, ≥ `created` |
| `answered-by` | when `answered` or `deferred` | `answer-questions`, or `human` when escalated |
| `kind` | optional | `decision` (the default when absent) \| `sign-off` |

### Body rules

- `## Context` and `## Question` MUST be non-empty when the question is filed.
- `## Answer` and `## Consequences` MUST **exist** from the moment the question is filed, even
  though both are empty until it is answered. A question filed without them leaves the answerer
  with nowhere to write: a stakeholder in a real run received five questions that stopped at
  `## Options considered` and had to invent the structure of the record in order to reply
  (F-032).
- **One decision per question.** A question that folds two decisions together gets
  half-answered and half-recorded — a stakeholder who refused a scope change inside what read
  like an ordering question noted that the refusal could easily have been logged as "ordering
  answered" (F-027). Two decisions, two files.
- **Questions filed for one item in one round are presented as one ask.** The artifacts stay
  one-per-decision because provenance needs them, but the person reading three files should
  experience one conversation, not three. Each `## Context` opens with the same frame — the
  item, the round, and which of how many this is — and the last one says that is all of them for
  now. Without it, a stakeholder receiving `Q-004`…`Q-006` reported "three separate emails…
  for one work item" (F-020).
- `## Options considered` MUST list at least two options **or** state explicitly why the
  question is not a choice between options (e.g. a missing fact). A question filed without
  having thought about the answer pushes the whole cost of the thinking upstream, which is how
  a question protocol degrades into "ask the human everything".
- `## Answer` and `## Consequences` MUST be non-empty when `status: answered` or
  `status: deferred`.
- `## Consequences` MUST name **files**, not intentions. "Updated the plan" is not a
  consequence; "`artifacts/plan.md` step 3 rewritten; `item.md` AC2 amended; `docs/architecture/
  adr/ADR-0004.md` created" is. This is what makes the rule "downstream skills re-read
  artifacts, never the Q&A" actually enforceable.

### `status: deferred` — the answer that is neither an answer nor silence

A stakeholder said "I'll send you a sample later", three times, and the protocol had nowhere to
put it. Leaving the question `open` deadlocks the loop for ever; marking it `answered` claims a
thing was settled that was not. The worker in that run wrote it down exactly: *"the question
protocol has no way to represent a deferred answer without either deadlocking `next` or
overstating what was settled"* (F-028).

`deferred` is that third state. It means: **the person replied, and their reply was that they
are not answering yet.**

- `## Answer` carries what they actually said, verbatim. A deferral is a real thing they said
  and the record keeps it in their words.
- `## Consequences` carries what the pipeline did **instead** — which is the whole point of the
  status, and why `deferred` is not just `open` with a nicer name. It MUST name files, like any
  other consequence.
- `answered-at` and `answered-by` are set, because a reply arrived.
- The orchestrator does **not** stop on a deferred question (`next` step 3 reads `open`), and
  the question is not re-asked. It is not open.

**What happens to the item is decided, not left to taste.** The architect has two moves and
must take one:

1. **Decide it under the deferral.** If the record plus the deferral is enough to choose — the
   deferral itself often *is* an answer, e.g. "proceed without it" — the question becomes
   `answered`, citing the deferral as the basis. This is not a deferred question at all, and
   calling it one would understate what was settled.
2. **Record the deferral and stop.** If no decision can be taken without the missing thing, the
   question becomes `deferred` and the item moves `awaiting-answer → blocked` with the
   `resume-to` it already carries, and `## Consequences` says what would unblock it. A blocking
   question that is deferred leaves the item at `blocked`, never at its old status: resuming
   would be a claim that the work can proceed, which is the guess the whole protocol exists to
   prevent.

**On an epic, move 2 parks nothing.** `blocked` on an epic is not a suspension — it *is* the
impasse ending of the engagement, reached only through `review-close` and only after the
stakeholder has been asked (`ids-and-statuses.md` §3.5). So a deferred blocking question on an
epic returns the epic to `open`, and `## Consequences` says what the engagement is doing
meanwhile. That is not the resumption move 2 forbids: `open` is where an engagement lives, not
where it works, and an epic advances only through its children, so nothing proceeds on the
strength of the missing thing. If the children can still move, they move; when they cannot, the
engagement comes to rest, the orchestrator dispatches `review-close`, and the deferral is part of
what the stakeholder is shown at the ending.

Writing move 2 for every item type was legal to write and impossible to execute: the validator
required `blocked` and the transition table permitted no move that reached it, so an epic-level
deferral produced a workspace no legal move could repair (F-050). The scope now lives in
`pipeline.yaml`'s `rule_obligations` and is checked against the transition table
(`ids-and-statuses.md` §4).

A **non-blocking** question that is deferred changes nothing about the item; it simply stops
being asked.

`validate-workspace` enforces the pairing on the item types that can be parked:
`question.deferred.not-blocked` fires when a **work item or bug** carries a deferred blocking
question and is not at `blocked` (or already closed).

A deferred **sign-off** (below) is the one deferral with a further consequence: the engagement
does not end, because the acknowledgment did not happen. The honest record is E3, the impasse
(`ids-and-statuses.md` §3.5).

### `kind: sign-off` — the termination question

Almost every question is a `decision`: something the pipeline cannot settle by itself. One is
not. A **sign-off** is the moment the stakeholder is told what happened and asked whether they
accept it, and it is filed by `review-close` when the engagement reaches **rest** — before the
epic may reach *any* of its endings, not only closure (`ids-and-statuses.md` §3.5,
`dor-dod.md` DE7).

It obeys every rule above and adds five:

- `addressed-to` MUST be `human` and `blocking` MUST be `true`. Nobody accepts on the
  stakeholder's behalf, and an acceptance question that does not stop the epic is a formality.
- `## Context` MUST restate **the goal in the stakeholder's own terms** — from the epic's
  `## Goal` and the vision, not from the tracker's vocabulary — so the answer is about the
  outcome rather than about the tickets.
- `## Question` MUST **name every child item of the epic**, by ID, each marked delivered or not
  delivered with one line of why — and then ask plainly whether the stakeholder accepts the
  engagement as it stands.
- `## Options considered` MUST offer at least: accept as complete; accept with named follow-up
  items; do not accept, with what is missing. That is a real choice, and a sign-off that offers
  only "yes" is theatre.
- Exactly one sign-off is due per **rest**. If the engagement re-enters rest after further work,
  the acknowledgment is due again, because the previous one accepted something else.

**Naming every child is the rule, and it is deliberate.** "List what was not delivered" is not
checkable and "name every child" is, so the gate can enforce it. It is also what closes the
second half of the gap: a bug the pipeline filed and never fixed is a child of the epic, so it
appears in the statement whether or not anyone remembered it. The stakeholder in the run that
produced this rule found one for themselves afterwards — *"there's also a bug sitting at
`planned`… that I was never told about"* (F-046).

The epic goes to `awaiting-answer` with `resume-to: open` and the run stops. The answer then
selects the ending: accept → the epic closes with `delivered` or `delivered-partial`; do not
accept → the epic goes to `blocked`, the impasse, with what would unblock it recorded; withdraw
→ the epic closes as `dropped`. Every one of those is a legitimate end, and what is no longer
possible is ending while never having asked.

Why this is a rule rather than good manners: two consecutive automated runs closed an epic with
no question ever addressed to the human. Every Definition of Done gate passed, correctly — they
check the record, and the record only holds what the stakeholder said when last consulted. In one
of those runs a mid-epic redesign had received explicit consent three items earlier; closure
itself still asked nothing (F-022). The fix built then gated *closure*, so the next run — which
ended at an impasse instead — never reached the gate at all, and the stakeholder wrote down that
the question never came (F-045). Rest, not closure, is the trigger.

---

## 3. Protocol

```
                    filed (blocking: true)
   implement  ─────────────────────────────►  item.status = awaiting-answer
   verify                                     history resume-to = <suspended status>
   review-close                                          │
                                                         ▼
                                              answer-questions is dispatched
                                                         │
                          ┌──────────────────────────────┴───────────────────────┐
                          ▼                                                      ▼
             answerable from the record                        not answerable from the record
             → write Answer + Consequences                     → re-address to human, keep open,
             → update the named artifacts                        surface it and stop the loop
             → status = answered                                          │
             → item returns to resume-to                                  ▼
                                                              human answers in the file
                                                              → answer-questions propagates
```

Rules:

1. **A blocking question suspends the item.** The filing skill sets `status: awaiting-answer`
   and writes a history row whose `resume-to` is the status being suspended. It then stops. It
   MUST NOT continue on a guess "to save time" — the guess is exactly what the protocol exists
   to prevent.
2. **A non-blocking question does not suspend anything.** The item continues. The question is
   still filed, still answered, and still shows on the board. Use it for "this should be
   written down somewhere" rather than "I cannot proceed".
3. **The orchestrator will not advance an item while a blocking question on it is open.**
4. **A question addressed to `human` stops the autonomous loop.** The orchestrator surfaces it
   and stops; there is nothing else it can legitimately do.
5. **Answers propagate into artifacts.** `answer-questions` MUST update the authoritative
   documents — the plan, the item's acceptance criteria, an architecture doc, a new ADR — and
   list them under `## Consequences`. An answer that exists only inside the question file has
   not been propagated, and the next skill will not see it.
6. **The question is never deleted, and its `status` is never reverted.** A superseded answer is
   handled by filing a new question that cites the old one.
7. **A deferral is a reply, not silence.** `status: deferred` records that the person answered
   and their answer was "not yet". The loop does not stop on it and the item does not resume:
   a deferred *blocking* question leaves a work item or a bug at `blocked` with what would
   unblock it written down, and returns an **epic** to `open`, where the engagement waits to be
   ended through the stakeholder rather than parked by the answerer (§2, F-050).

---

## 4. When to escalate to the human

`answer-questions` escalates — sets `addressed-to: human` — only when at least one holds:

- The answer depends on **intent** that no document records (what the user actually wants).
- The answer is **not reversible** — it commits the project to something expensive to undo.
- The answer would **contradict** an existing ADR or product doc, which only the human can
  authorise.
- The record is **genuinely silent** and any choice would be a coin flip with material
  consequences.

It MUST NOT escalate merely because answering is effortful. An architect who forwards every
question is not doing the job, and the human's attention is the scarcest resource in the loop.
Every escalation MUST state, in `## Context`, which of the four conditions above applies.

---

## Revisions

| # | Date | Change |
|---|------|--------|
| 1 | 2026-08-17 | Initial. |
| 2 | 2026-08-22 | §2: the optional `kind` field, and `kind: sign-off` — the stakeholder acceptance question an epic cannot close without (F-022). |
| 3 | 2026-08-22 | §2: `## Answer` and `## Consequences` must exist from the moment a question is filed (F-032). |
| 4 | 2026-08-22 | §2: one decision per question (F-027); questions for one item in one round are presented as one ask (F-020). |
| 5 | 2026-08-27 | §2: `status: deferred` — the reply that is neither an answer nor silence, and what it does to the item (F-028). `kind: sign-off` becomes the **termination** question: triggered by rest rather than by closure, and it must name every child item (F-045, F-046). Derived in ADR-0006. |
| 6 | 2026-08-27 | §2: what a deferral does to an **epic** — it returns the epic to `open`, because `blocked` on an epic is the impasse ending and only `review-close` reaches it. Move 2 as written was impossible to execute on an epic (F-050). |
