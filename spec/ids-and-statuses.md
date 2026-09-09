# Identifiers, item types, and the status graph

Normative. `scripts/validate-workspace` enforces every rule on this page.

## 1. Identifier formats

| Kind | Format | Example | Scope of uniqueness |
|------|--------|---------|---------------------|
| Epic | `EP-` + 3 digits | `EP-001` | whole workspace |
| Work item | `WI-` + 4 digits | `WI-0007` | whole workspace |
| Bug | `BUG-` + 4 digits | `BUG-0003` | whole workspace |
| Question | `Q-` + 3 digits | `Q-002` | the owning item only |
| Architecture decision | `ADR-` + 4 digits | `ADR-0004` | whole workspace |

Rules:

- Numbers MUST be sequential from `1`, zero-padded to the width above.
- An ID MUST NOT be reused, even if the artifact it named was abandoned. Abandoned items are
  set to `done` with an outcome of `dropped` (see `work-item.md`), never deleted. A reused ID
  would silently rewrite history in `git log --grep`.
- A question ID is scoped to its item, so `WI-0007/questions/Q-001.md` and
  `WI-0009/questions/Q-001.md` are different questions. A question is therefore cited as
  `WI-0007/Q-001` wherever the item is not already obvious from context.

### 1.1 Allocating the next ID

The next ID for a kind is **derived from the filesystem**: take the highest number currently
present across the workspace for that kind — including items already `done` — and add one.

There is deliberately no counter file. A counter is a second source of truth that drifts the
first time a run is interrupted between "increment the counter" and "create the directory",
and the drift is invisible. Derivation is idempotent and self-healing: re-deriving after a
crash gives the same answer as deriving before it. See `meta/adr/ADR-0003` for the full
argument.

Allocation MUST scan, in one pass:

- `tracker/items/*/` directory names, for `EP-`, `WI-`, `BUG-`;
- `tracker/items/*/questions/Q-*.md`, for that item's `Q-`;
- `docs/architecture/adr/ADR-*.md`, for `ADR-`.

## 2. Item types

Every tracked entity is a directory under `tracker/items/<ID>/`, whatever its type. One uniform
shape means one validator, one board generator, and one journal format.

| `type` | ID kind | What it is | Parent |
|--------|---------|-----------|--------|
| `epic` | `EP-` | A goal that groups work items. Holds the product-level narrative. | none |
| `work-item` | `WI-` | A unit of deliverable change with its own acceptance criteria. | an epic |
| `bug` | `BUG-` | A defect found against already-delivered behaviour. | an epic; and links the item it was found against |

A `work-item` MUST name an `epic`. A `bug` MUST name an `epic` and SHOULD name the work item
whose delivered behaviour it contradicts, via `found-in`.

## 3. Statuses

### 3.1 Statuses for `work-item` and `bug`

| Status | Meaning | Owning skill | Terminal |
|--------|---------|--------------|----------|
| `draft` | Created, but not yet proven to meet the Definition of Ready. | `refine` | no |
| `ready` | Meets the Definition of Ready. Needs a design and a plan. | `plan` | no |
| `planned` | A plan exists and has been recorded. Needs implementation. | `implement` | no |
| `in-progress` | Implementation has started. Also the resume point after an interruption. | `implement` | no |
| `verifying` | Implementation reports itself complete. Needs independent validation. | `verify` | no |
| `in-review` | Verified. Needs review against the Definition of Done, then closing. | `review-close` | no |
| `awaiting-answer` | A blocking question is open. No engineering may proceed. | `answer-questions` | no |
| `blocked` | A documented impasse that no skill can resolve. | none — a human must act | yes |
| `done` | Closed. Carries an `outcome`. | none | yes |

### 3.2 Statuses for `epic`

| Status | Meaning | Owning skill | Terminal |
|--------|---------|--------------|----------|
| `open` | The engagement is running: children exist and are not all finished. | none — epics advance through their children | yes* |
| `awaiting-answer` | A blocking question about the epic's own scope, or the termination question (§3.5), is open. | `answer-questions` † | no |
| `blocked` | The **impasse ending**: the engagement cannot proceed and the stakeholder has been told. Only a person can move it. | none — a human must act | yes |
| `done` | The engagement ended and was closed with an `outcome`. | none | yes, but reopenable — see §3.4 |

† The **owning skill** is the one the orchestrator dispatches, and for `awaiting-answer` it is
always `answer-questions`. It is not the only skill that may move an epic out of the status: at
E4 by silence there is nothing to answer, so `review-close` leaves `awaiting-answer` directly
(§3.5a, and §4's row). Ownership answers *who is dispatched*; the transition table answers *who
may move it*, and the two are different questions.

\* "Terminal" here means *the orchestrator never dispatches a skill against an open epic while
the engagement is running*. There are exactly two exceptions, both mechanical rather than
judgement calls, and both are the same verdict read from the same program: when
`scripts/engagement-state` reports **at-rest** (§3.5) or **abandoned** (§3.5a), the orchestrator
dispatches `review-close` on the epic to end it. Otherwise an epic advances only through its
children.

### 3.3 Why `in-progress` exists as a distinct status

`planned` and `in-progress` share an owning skill. The distinction is not bureaucratic: it is
what makes an interrupted run recoverable. `planned` means no branch and no code exist yet, so
starting over is free. `in-progress` means a branch exists and partial work is on it, so the
skill MUST reconcile with what is already there rather than starting again. A single status
could not carry that difference, and the recovery behaviour would depend on the agent guessing.

### 3.4 A closed epic can be reopened

`done` is terminal for a `work-item` and a `bug`: once closed, that unit of work is finished,
and a later defect is a *new* item. An **epic** is different, and the difference is not
cosmetic. An epic states a goal. If a defect is later found in the behaviour that epic
delivered, the goal is no longer met — and the defect must be filed under that epic, because
that is the goal it violates.

So a `done` epic MAY return to `open`, by any skill, when a child item is filed against it after
it closed. The transition is recorded like any other, and the reason names the item that caused
it. When that item closes, `review-close` applies the epic Definition of Done again and may
close the epic again.

The alternative — forbidding it — was tried and produces a lie: `validate-workspace` reports
`epic.closed-with-open-children`, and the only ways to silence it are to file the bug under a
different epic (breaking the link between the defect and the goal it violates) or not to file it
at all. A methodology that makes "do not record the defect" the path of least resistance has
chosen the wrong invariant. This was found by an independent regression pass against a closed
epic, not by reasoning about it.

### 3.5 An engagement ends, and every ending passes through the stakeholder

An **engagement** is one epic and every item whose `epic:` names it. It **ends** when no skill
can advance any item in it and none ever will without a person acting. Four endings satisfy
that, and all four are legal:

| # | Ending | Epic's final state | Reached when |
|---|--------|-------------------|--------------|
| E1 | **delivered** | `done`, `outcome: delivered` | every child is `done` and delivered (or `duplicate`); the stakeholder accepted |
| E2 | **delivered-partial** | `done`, `outcome: delivered-partial` | every child is terminal, at least one was not delivered; the stakeholder accepted, with or without named follow-ups |
| E3 | **impasse** | `blocked` | every child is terminal, at least one was not delivered, and the stakeholder did not accept — or deferred the acknowledgment |
| E4 | **abandoned** | `done`, `outcome: dropped` | the stakeholder is gone, by **either** of two routes — **withdrawal**, an act they perform (through a request, or in the answer to the termination question); or **silence**, the absence of any act (§3.5a). Children not `done` go to `blocked` first, so the record says what was in flight |

**Rest** is the mechanical trigger for E1, E2, E3 and for E4 by **withdrawal** — a withdrawal is
an act the stakeholder performs, so it arrives as an answer or a request and brings the
engagement to rest like any other reply. E4 by **silence** has a different trigger and §3.5a
states it, because an engagement nobody is answering never reaches rest at all. Both triggers are
one program — `scripts/engagement-state <EP-ID>` — because the orchestrator and the termination
gate must not be able to disagree about whether an engagement is over. An engagement is at rest
when all of:

1. every child of the epic is at a terminal status (`done` or `blocked`);
2. no question anywhere in the engagement — epic or child — is `open`;
3. no request in `tracker/requests/` is `open`.

At rest, and while the epic is still `open`, the orchestrator dispatches `review-close` on the
epic. `review-close` then does one of two things, and both leave `open`, so the step terminates:
it files the **termination question** (`question.md` §2, `kind: sign-off`) and suspends the epic
to `awaiting-answer`; or, the acknowledgment already being answered, it records the ending.

**No engagement ends, in any ending, without the stakeholder having been asked.** In E1, E2, E3
and E4 by withdrawal that ask is a blocking question addressed to the human stating what was
delivered, what was not, and why, and it was **answered**. At E4 by silence it is the ask that
went unanswered for the threshold, and the ending statement states the same things to a reader
instead (§3.5a). `dor-dod.md` DE7 is that rule as a criterion and `scripts/check-epic-signoff` is
the gate. A refusal ends the engagement just as legitimately as an acceptance — E3 exists so that
"no" has somewhere honest to go. What is not legal, in any ending, is ending while never having
asked.

**Only `review-close` ends an engagement.** Ending means applying the epic Definition of Done and
reading the acknowledgment — or, where none arrived, recording that none did — which is already
its job. An epic-level *question* may suspend the epic from anywhere (§4, and the F-013 note); an
epic-level *ending* may not.

### 3.5a E4's second route: silence, counted in the pipeline's own asks

A stakeholder who has not answered **yet** and a stakeholder who is **gone** are the same reading
of the workspace. They differ only across time, so the threshold is a count of occasions, not a
property of a state.

A **silent round** is one execution of the orchestrator that ended at *waiting on the human* and
observed **no inbound change** since the previous such execution. A change is **inbound** when it
is one the stakeholder could have made, and exactly two channels are theirs: a reply written into
a question's `## Answer` (with its `status` and `answered-at`), and a file under
`tracker/requests/` (`spec/request.md` §1). Nothing else in the workspace is theirs — §4's last
note says skills change statuses and nothing else does — so nothing else counts.

The round is defined against the **halt**, not against the question set: a pass that did not stop
on the human is not a round, and a question that does not stop the loop never produces one.

**The count is derived, never stored.** The orchestrator appends one row per halt to the
engagement's append-only waiting log, `tracker/waiting/<EP-ID>.md`
(`workspace-layout.md` §1.4). The silent-round count is **the number of trailing rows sharing the
last row's `inbound` digest**. A counter field would be a second source of truth that drifts the
first time a run is interrupted between the increment and the act, which is the argument ADR-0003
made against a counter file, and it gets the same answer here.

**The reader never writes.** `scripts/engagement-state` computes the count and appends nothing;
the row is appended by `next`, once per halt. Were the reader to record, `check-epic-signoff` and
`review-close` — both of which read the state — would each advance the clock by consulting it.

**The threshold lives in `methodology/pipeline.yaml`**, as `termination.silence.threshold_rounds`,
default **3**. It is stated there for the same reason rest is a program: three consumers read it —
the orchestrator, `engagement-state` and `check-epic-signoff` — and any two of them disagreeing
about whether the threshold is met is F-045's mechanism exactly.

**Any** inbound change resets the count, and only an inbound change does. A full answer, a
**partial** answer, a **deferral** and a new request all reset it, because the count measures
**presence**, not compliance: a slow stakeholder is never abandoned, an absent one is, and *"a
deferral is a reply, not silence"* (`question.md` §3) would be contradicted by any other reading.
A question **we** file resets nothing, and neither does anything else a skill writes — a pipeline
whose own asking reset the clock could never reach the threshold in any engagement that keeps
generating questions, which is every engagement.

At the threshold, `scripts/engagement-state <EP-ID>` reports the verdict **`abandoned`**: *the
engagement is halted on a human who has not answered for `threshold_rounds` consecutive rounds;
its ending is E4 and it is not recorded.* It sits parallel to `at-rest`, and like `at-rest` it is
the orchestrator's cue to dispatch `review-close` on the epic — which then declares E4 and closes
it. The orchestrator records the halt **before** it reads the verdict, so the declaring pass is
itself counted and the trailing run **equals** the threshold rather than exceeding it by the row
nobody wrote. `next` decides nothing here: it reads a verdict, as it already does at steps 6
and 7.

**Abandonment is only ever declared against an open ask.** A silent round requires a halt, and a
halt requires a question addressed to `human` that is `open`. Silence where nothing was asked is
not silence — nobody was asked anything — and ending an engagement because *we* failed to ask is
the failure DE7 exists to prevent (F-022, F-045). Whatever channel later makes the pipeline halt
on the human is an ask, and its halts are silent rounds.

**What the declaration looks like.** There is nobody to address, so the statement the sign-off
would have carried becomes a document: `## Ending statement` in the epic's `artifacts/review.md`,
mirrored in the epic's `## Notes`. It restates the goal in the stakeholder's own terms, names
**every** child of the epic by ID with its class, records the silence itself — how many rounds,
what was surfaced on each, and the first round's timestamp — and addresses each success measure.
Naming every child is the rule for the same reason the sign-off has it: *"list what was not
delivered"* is not checkable and *"name every child"* is (F-046).

Each child is exactly one class, decided by status alone so the classification is a program's:

| Class | Which children |
|-------|----------------|
| **delivered** | `done` with `outcome: delivered` or `duplicate` |
| **dropped earlier** | `done` with `outcome: dropped` |
| **blocked earlier** | `blocked` before the declaration — its own impasse, not an orphan |
| **orphaned, in flight** | `planned`, `in-progress`, `verifying`, `in-review`, or `awaiting-answer` from one of those |
| **orphaned, never started** | `draft`, `ready`, or `awaiting-answer` from one of those |

Every orphan moves to `blocked` before the epic closes, with a history `reason` beginning
`orphaned by E4:` — the greppable-prefix convention `DoR overridden:` already uses. An orphan
takes **no `outcome` at all**: `outcome` is present if and only if the item is `done`
(`work-item.md` §1), so an orphan carrying one at `blocked` is invalid and an orphan pushed to
`done` to carry one is a claim that its work concluded. `blocked` is also the resumable status,
which under an ending that may be wrong is the right one.

Every question still `open` in the engagement is closed as `abandoned` (`question.md` §2).

**E3 and E4 are distinguishable from the record alone, and the test is one line: did the
stakeholder's own words arrive?** E3 has them verbatim in a `## Answer`, and the epic is
`blocked`. E4 has an empty `## Answer` — or no sign-off at all, where the silence began before
rest — a waiting log whose trailing run reaches the threshold, a history reason beginning
`E4 abandoned:` naming the round count and the threshold, and the epic at `done`,
`outcome: dropped`.

That asymmetry is deliberate. `blocked` means *a human must act*, which at E4 would be a standing
instruction to wait for someone who is not coming; and `done` on an epic is the one state in this
pipeline that reopens (§3.4), so the ending most likely to be wrong about a person is the only
one the pipeline can undo. The returning stakeholder's route back is `tracker/requests/`, which is
theirs to open and which reopens the epic.

**What no program can decide, said here rather than implied:** whether the person is actually
gone. Every mechanism above measures our own asking. The threshold is a bet that
`threshold_rounds` unanswered asks mean absence, and the rate at which rounds accrue is set by
whoever runs the loop — three passes in a minute are three rounds, and nothing can tell them from
three passes in three days. `pipeline.yaml` is where that calibration is written down.

The derivation, including the alternatives rejected, is `meta/adr/ADR-0011`.

### 3.6 An ending is not the same as being closed

`scripts/engagement-state` distinguishes them, and the distinction is what makes the
retrospective a step rather than a habit:

| Verdict | Means |
|---------|-------|
| `ended` | the ending is recorded on the epic, and `artifacts/retro.md` does not exist yet |
| `closed` | ended, **and** the engagement has read its own trail |

At `ended`, the orchestrator dispatches `retro` on the epic once. **Nobody is waiting on it.**
The stakeholder's engagement ended at sign-off and they have already been told the work is
finished; the retrospective is the team studying itself before the engagement is archived. It
therefore gates nothing: no workspace is invalid for lacking a report, no Definition of Done
criterion mentions one, and an engagement that never runs it is ended and unread rather than
broken.

The step terminates for the same reason §3.5's does: writing the report changes the verdict, so
the epic cannot be dispatched for this reason twice. `retro` writes exactly two things — the
report and its own journal entry on the epic — and changes no status; the format is
[`retro.md`](retro.md) and the derivation is `meta/adr/ADR-0009`.

The full derivation of the endings, including the ones that were rejected, is
`meta/adr/ADR-0006`.

## 4. Legal transitions

Every row is the only legal way to reach that status. Any other transition is invalid and
`scripts/validate-workspace` reports it by reading `history.md`.

`applies_to` says which item types the row is legal for; a row with no `applies_to` applies to
all three. **Gated** rows are the ones a skill's hard gates refuse — see the note below.

| From | To | Actor skill | Applies to | Gated | Condition |
|------|----|-------------|-----------|-------|-----------|
| — | `draft` | `intake` | work-item | | item created from a refined idea, or from a routed request |
| — | `draft` | `refine` | work-item | | the item being refined is two items, and this is one of the parts (DoR R9) |
| — | `draft` | `answer-questions` | work-item | | an answer widened the scope and implied work nobody has recorded |
| — | `ready` | `verify` | bug | | a bug filed with reproduction steps already satisfies the bug Definition of Ready |
| — | `ready` | `review-close` | bug | | review found a defect belonging to another item |
| — | `open` | `intake` | epic | | epic created from the raw idea |
| `draft` | `ready` | `refine` | work-item, bug | ✓ | Definition of Ready passes, or the human explicitly overrides |
| `ready` | `planned` | `plan` | work-item, bug | ✓ | design recorded and plan written |
| `planned` | `in-progress` | `implement` | work-item, bug | | branch created, work started |
| `in-progress` | `verifying` | `implement` | work-item, bug | ✓ | implementation gates pass and the report is written |
| `verifying` | `in-review` | `verify` | work-item, bug | ✓ | verification passes against the acceptance criteria |
| `verifying` | `in-progress` | `verify` | work-item, bug | | verification fails on this item's own acceptance criteria |
| `in-review` | `done` | `review-close` | work-item, bug | ✓ | Definition of Done passes and the change is merged |
| `in-review` | `in-progress` | `review-close` | work-item, bug | | review rejects the change with recorded reasons |
| *any suspendable* | `awaiting-answer` | any skill | all | | that skill filed a blocking question |
| `awaiting-answer` | *the status it came from* | `answer-questions` | all | | the blocking question is answered and its consequences are propagated |
| `awaiting-answer` | `blocked` | `answer-questions` | work-item, bug | | the answer was **deferred**: the stakeholder said "later" and no decision can be taken without it (`question.md` §2) |
| `awaiting-answer` | `blocked` | `review-close` | work-item, bug | | E4 (§3.5a): an orphan suspended on a question that will never be answered. `awaiting-answer` is not suspendable, so the generic impasse row cannot reach it, and the deferral row above needs a reply that is not coming |
| *any suspendable* | `blocked` | any skill | work-item, bug | | a documented impasse no skill can resolve |
| `blocked` | *the status it came from* | any skill | all | | a human recorded a resolution in the item |
| `open` | `done` | `review-close` | epic | ✓ | the engagement ended at E1, E2 or E4 (§3.5): the epic Definition of Done passes and the stakeholder answered the termination question — or, at E4 by **silence** (§3.5a), the ask stood unanswered for the threshold and the ending statement stands in the sign-off's place |
| `awaiting-answer` | `done` | `review-close` | epic | ✓ | the engagement ended at E4 by **silence** (§3.5a) while the epic was suspended — the sign-off was filed and the threshold was reached before it was answered. Only `answer-questions` may otherwise leave `awaiting-answer`, and it has nothing to answer |
| `open` | `blocked` | `review-close` | epic | ✓ | the engagement ended at E3 (§3.5): the impasse, with the stakeholder having been asked |
| `done` | `open` | any skill | epic | | a **child item was filed against the epic after it closed** (§3.4) — a defect in what it delivered, or work routed from a stakeholder request that arrives after the ending. Either way the goal is no longer met |


Notes:

- **An epic never escapes downward, so every terminal move it makes is gated.** A skill's hard
  gates refuse only the move that declares its work complete; every other move is reported and
  allowed, because trapping a skill that is trying to file a question or send an item back is
  worse than letting it move. That reasoning is about *work in flight*. An epic has none — it
  advances only through its children — so every one of its terminal moves — `open → done`,
  `open → blocked`, and `awaiting-answer → done` — declares the engagement finished, and all
  three are refused while the termination gate fails. Without this, the impasse ending would run
  the acknowledgment gate and ignore its verdict, which is F-045 by a different route
  (ADR-0006 §1c).
- **Terminal and suspendable are different questions.** `terminal` asks whether the pipeline
  advances an item out of this status by itself; `suspendable` asks whether a blocking question
  or an impasse may stop an item here. An epic at `open` is terminal — it advances only through
  its children — and suspendable, because an epic-level question is precisely the case that must
  be able to stop it. `done` and `blocked` are neither. Conflating the two made the escalation
  path the methodology documents impossible to execute: `intake`'s own instruction is "set the
  epic to `awaiting-answer` and stop", and two separate runs found that the transition was
  refused, leaving a skill to choose between recording a blocking question as non-blocking — a
  lie the record carries forever — and leaving the workspace failing validation (F-013).
- **`awaiting-answer` remembers where it came from.** The history entry MUST record the status
  being suspended, and `answer-questions` MUST restore exactly that status. Otherwise an item
  interrupted during `verify` would silently restart at `implement`, and the verification
  evidence already gathered would be quietly discarded.
- **`verifying → in-progress` is a rejection, not a bug.** A failure of *this item's own*
  acceptance criteria sends the item back. A defect in *previously delivered* behaviour is a
  new `bug` item instead, and this item continues. `verify`'s process defines the test.
- **A rule elsewhere that names a status must declare the move that satisfies it.** The
  validator enforces several rules of the shape *"this item must be at one of these statuses"*.
  Such a rule is enforceable only for the item types some skill may legally move there, so the
  scope is not the rule's to decide: `methodology/pipeline.yaml` carries a `rule_obligations`
  block naming, per rule, the item types it applies to and the transition that satisfies it.
  `validate-workspace` reads that scope, and `lint-skills` checks it against this table in both
  directions — a rule scoped wider than the moves that satisfy it, and a move narrowed while the
  rule still claims the item type. The first of those had already happened when the registry was
  written: a deferred question required its item to be at `blocked`, the deferral row above is
  scoped to work items and bugs, and an epic-level deferral therefore produced a workspace no
  legal move could repair (F-050).
- **Skills change statuses. Nothing else does.** A human editing `status:` by hand produces a
  history gap, and the validator reports it as `history.gap`.

## 5. Creation authority and provenance

An engagement's item set is not fixed at intake, and the skills that discover new work are not
the same as the skills that were given permission to record it. Two runs found the same
contradiction from opposite ends: an answer that widened scope with nowhere to record the
implied work, and a review that found a defect belonging to a closed item and could not file it
(F-029, F-042). The table below is derived from the events that change the item set rather than
from the happy path; the derivation is `meta/adr/ADR-0006` §3.

**The rule:** a skill may create an item exactly when it is the skill that **observes the need**
for it, and only if it records **what caused the item to exist** in a citation that resolves.

| Actor | May create | At status | Provenance it MUST record |
|-------|-----------|-----------|---------------------------|
| `intake` | `epic`, `work-item` | `open`, `draft` | `arose-from: R-###` when the item came from a stakeholder request; otherwise the vision it refined |
| `refine` | `work-item` | `draft` | `arose-from: <ITEM>` — the item it split (DoR R9) |
| `answer-questions` | `work-item` | `draft` | `arose-from: <ITEM>/Q-###` — the question whose answer widened the scope |
| `verify` | `bug` | `ready` | `found-in`, or `arose-from: <ITEM>` when the behaviour it contradicts is not one item's |
| `review-close` | `bug` | `ready` | `found-in`, or `arose-from: <ITEM>` — the item under review |
| `plan`, `implement`, `next` | — | — | — |

`plan` and `implement` are excluded by the rule rather than by omission. Neither observes a need
for *new work*: `plan` observes uncertainty, which is a question, and `implement` observes scope
creep, which is a question too. `next` observes nothing — it reads statuses, not content.

Nothing may create an item past `draft`. A `bug` at `ready` is not an exception: a bug filed
with reproduction steps has already satisfied its Definition of Ready (`dor-dod.md` §2), so
`ready` is where it is born rather than a status it skipped to.

Every item whose creation row names an actor other than `intake` MUST carry provenance, and
`arose-from` MUST resolve — to an item that exists, a question file that exists, or a request
file that exists. On a **bug**, `found-in` satisfies the requirement on its own: it already names
the delivered behaviour the bug contradicts, which is what caused the bug to exist, and demanding
a second field that says the same thing would be bureaucracy.

Without provenance, "who may create" degrades into "who says they may", and an item created for
no recorded reason cannot be told apart from one invented to make a gate pass.
`validate-workspace` reports `item.arose-from.missing` and `item.arose-from.unresolved`.

## 6. Priority

`priority` MUST be one of `critical`, `high`, `medium`, `low`.

| Value | Rank | Meaning |
|-------|------|---------|
| `critical` | 1 | Blocks everything else; the epic cannot ship without it. |
| `high` | 2 | Required for the epic's stated outcome. |
| `medium` | 3 | Wanted, but the epic is coherent without it. |
| `low` | 4 | Opportunistic. |

Rank orders the orchestrator's choice of what to run next. The tie-break after rank is the
oldest `created` timestamp, and after that the lexicographically smallest ID — so the choice is
fully deterministic and two runs over the same workspace pick the same item. Randomness here
would make an interrupted run unreproducible, which is the one thing the whole design is
protecting.

---

## Revisions

| # | Date | Change |
|---|------|--------|
| 1 | 2026-08-17 | Initial. |
| 2 | 2026-08-22 | §4: statuses declare `suspendable` separately from `terminal`, so an epic at `open` can be suspended by a blocking question or an impasse (F-013). |
| 3 | 2026-08-27 | §3.5: the four endings of an engagement, rest as the mechanical trigger, and the rule that every ending passes through the stakeholder (F-045, F-046). §4: transitions declare `applies_to`; the epic ending rows; the deferral row; an epic's terminal moves are gated. New §5: creation authority and `arose-from` provenance (F-029, F-042). Derived in ADR-0006. |
| 4 | 2026-08-27 | §4: a rule elsewhere that requires an item to be at a status declares the move that satisfies it, in `pipeline.yaml`'s `rule_obligations`; the scope is checked against this table rather than remembered (F-050). |
| 5 | 2026-08-30 | New §3.6: an ending is not the same as being closed. `engagement-state` gains the `closed` verdict, the orchestrator dispatches `retro` on `ended`, and the retrospective gates nothing (ADR-0009). |
| 6 | 2026-09-10 | §3.5: E4 gains a **second route** — silence, not only withdrawal — and rest stops being the trigger for it. New §3.5a: the silent round, the derived count over `tracker/waiting/<EP-ID>.md`, `termination.silence.threshold_rounds`, the `abandoned` verdict, the ending statement, the child classification and the orphan's move to `blocked` with no `outcome`. §3.2: ownership answers *who is dispatched*, not *who may move it*. §4: two new rows — `awaiting-answer → blocked` (`review-close`, work-item/bug) and `awaiting-answer → done` (`review-close`, epic, gated), both F-050's shape found by derivation; the `done → open` condition widened to §3.4's own prose, *a child item filed against the epic after it closed*, so a returning stakeholder has a legal route back. Derived in ADR-0011 (F-060, F-008, H-008). |
