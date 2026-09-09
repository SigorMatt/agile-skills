# ADR-0011 — Stakeholder silence and abandonment: when someone who has not answered becomes someone who is gone

- **Status:** accepted
- **Date:** 2026-09-10
- **Unit:** META-150
- **Extends:** ADR-0006 (the termination model) — E4, the ending it declared legal and left unbuilt.
- **Amends:** ADR-0006 §1's E4 row and `spec/ids-and-statuses.md` §3.5's E4 row — E4 gains a
  **second route**: not only withdrawal, which is an act the stakeholder performs, but silence,
  which is the absence of any act. Also `spec/dor-dod.md` **DE7** and **DE8** (*asked and
  answered* holds for E1–E3; at E4 the honest form is *asked, and the ask stood unanswered for
  the threshold*), and ADR-0010 §4.3 / **DE4**'s trigger (*after the sign-off answer arrived* →
  *after the ending is determined*, because at E4 no answer arrives). Each amendment is named
  file-by-file in §7.
- **Findings:** F-060, F-008, H-008. Touches F-021, F-028, F-033, F-045, F-046, F-050, F-001.

## Context

E4 — `abandoned` — has been a legal ending since ADR-0006 and has never executed. The ROADMAP §2
stamp records it as fixture-only in the same sentence as E2 [src: meta/ROADMAP.md]. Fixture-only
is a generous description: E4 as currently written can only be reached by a stakeholder who
**speaks** in order to leave — *"the stakeholder withdrew the engagement — through a request
(`spec/request.md`), or in the answer to the termination question"* (ADR-0006 §1). A stakeholder
who simply stops replying reaches no ending at all.

What happens instead is this, and every step of it is the pipeline working as specified:

1. A skill files a question addressed to `human` and suspends its item.
2. `next` step 3 surfaces the question in full and **stops the loop** — *"there is nothing else
   you may legitimately do: the pipeline is waiting on a person"* [src: methodology/skills/next/process.md].
3. Nobody answers.
4. Step 3 runs again, identically, for ever. The workspace is a fixed point.

Three consequences, and they are the reason this is a derivation rather than a patch.

**(a) Rest is unreachable, so ADR-0006's whole termination apparatus never engages.** Rest
requires that *no question anywhere in the engagement is open* [src: scripts/lib/engagement.py].
An unanswered question is open by definition, so an engagement with a silent stakeholder is
`active` for ever, `review-close` is never dispatched on the epic, and DE7 — the criterion that
exists so that every ending passes through the stakeholder — is never evaluated. F-045's shape,
one layer further out: the gate that fires at the ending is fine, and the engagement never gets
there.

**(b) The harness reads the same state and calls it something false.** With a human-addressed
question open and unanswered, the driver routes a sim turn to answer it
[src: harness/run_iteration.py], the sim answers nothing, and the loop repeats until the turn
budget is spent — the run is then labelled `turn-budget`, *resumable*, "not finished". Where the
question ceases to be open-and-unanswered the fingerprint branch instead calls it `stalled`,
*"three turns changed nothing"*. Neither sentence is what happened. What happened is that the
person left.

**(c) The pipeline has no vocabulary for absence.** `question.md` has three question statuses and
every one of them presumes a reply: `open` (a reply is expected), `answered` (a reply arrived),
`deferred` (*"the person replied, and their reply was that they are not answering yet"*).
F-028 built `deferred` precisely so that a reply of "not yet" would not have to be recorded as
either an answer or silence — and in doing so it named the gap it did not fill. Silence is the
fourth thing, and nothing in the record can say it.

The derivation below starts from what silence *is* — an absence, which is not observable at any
single moment — and asks what could possibly make it observable to a program. Everything else
follows from that answer.

---

## 1. What silence is, and when it becomes abandonment

A stakeholder who has not answered **yet** and a stakeholder who is **gone** are indistinguishable
in any single reading of the workspace. That is not a limitation of our tooling; it is what the
two states are. They differ only across time, and only in one respect: the first one eventually
acts and the second one never does.

So the threshold cannot be a property of a state. It has to be a count of **occasions**, and the
question is what an occasion is.

### 1.1 Three candidate units, and why two of them fail

**Wall-clock time is unavailable and, where available, wrong.** Every artifact in this workspace
carries a UTC timestamp, so a duration is computable [src: spec/question.md]. It measures the
wrong thing in both directions. An agent-driven pipeline does not run continuously: an engagement
resumed after a fortnight would find every threshold exceeded and declare a live, patient
stakeholder abandoned on the first pass. A harness iteration runs its whole engagement inside an
hour, so no wall-clock threshold long enough to protect the first case can ever fire in the
second. A clock measures how long the *pipeline* was not running, which is not a fact about the
stakeholder at all.

**A turn is the harness's concept and the methodology must not learn it.** The driver counts
turns; the toolkit has never had the word and must not acquire it, because the toolkit ships to
consumers who have no driver. ADR-0005 keeps the harness outside the methodology in exactly this
direction, and a threshold expressed in turns would put the harness inside the contract that the
harness exists to grade.

**What is left is the pipeline's own asks** — and this is the unit, because it is the only
countable thing whose count is a fact about the stakeholder rather than about us:

> A **silent round** is one execution of the orchestrator that ended at *waiting on the human*
> and observed no inbound change since the previous such execution.

"Inbound" is the load-bearing word: a change is inbound when it is one the stakeholder could have
made. Two channels exist and they are exhaustive — a reply written into a question's `## Answer`
(with its `status`/`answered-at`), and a file under `tracker/requests/`, the channel that is
theirs to open and nobody else's (F-021, `spec/request.md` §1). Nothing else in the workspace is
theirs: *"Skills change statuses. Nothing else does"* [src: spec/ids-and-statuses.md §4].

Defining the round against the **halt** rather than against the question set is deliberate.
Whatever step 3's scope turns out to be — every human-addressed question, or only the blocking
ones (§6 has a live contradiction about that) — the counter follows the halt, so the two cannot
drift apart. A pass that did not stop on the human is not a round, and a question that does not
stop the loop never produces one.

### 1.2 The count is derived, never stored

A counter field is a second source of truth that drifts the first time a run is interrupted
between the increment and the act, and the drift is invisible. ADR-0003 made that argument for ID
allocation and refused a counter file; the same argument applies here and gets the same answer.

The orchestrator appends one row per halt to an append-only **waiting log**,
`tracker/waiting/<EP-ID>.md` — a directory beside `tracker/requests/`, deliberately outside
`tracker/items/`, because `next` writes no journal and no item artifact and this ADR is not the
place to start. Each row carries the observation, not a conclusion:

```markdown
| round | observed | inbound | surfaced |
|-------|----------|---------|----------|
| 1 | 2026-09-10T14:02:11Z | 9f3c1a2e | WI-0001/Q-002, WI-0001/Q-003 |
| 2 | 2026-09-10T14:11:40Z | 9f3c1a2e | WI-0001/Q-002, WI-0001/Q-003 |
```

`inbound` is a digest over the inbound state defined above: for every question addressed to
`human`, its ID, `status`, `answered-at` and a digest of its `## Answer` text; for every request,
its name and `status`. The silent-round count is then **the number of trailing rows sharing the
last row's `inbound` digest** — a derivation over an append-only log, idempotent and self-healing
in ADR-0003's sense. The `round` column is written for a human reader and is not what the
programs read: a hand-edited round number cannot make an abandonment happen sooner, because the
count comes from the digests.

**The reader never writes.** `scripts/engagement-state` computes the count and appends nothing;
the row is appended by `next`, once per halt, through a gate command in the way that
`board-current` already runs `scripts/board-gen`. Were the reader to record, then
`check-epic-signoff` and `review-close` — both of which read the state — would each advance the
clock by consulting it.

### 1.3 The threshold, and what resets it

**Stated in `pipeline.yaml`**, in a `termination.silence` block, for the reason
`ids-and-statuses.md` §3.5 gives for rest being a program: three consumers now read it — the
orchestrator (which dispatches on it), `engagement-state` (which decides it) and
`check-epic-signoff` (which accepts an ending because of it) — and any two of them disagreeing
about whether the threshold is met is F-045's mechanism exactly.

```yaml
termination:
  silence:
    threshold_rounds: 3
    unit: orchestrator halts on the human with no inbound change since the previous halt
    resets_on: any inbound change - a reply, a partial reply, a deferral, or a new request
```

**Default 3, and it is a floor rather than a target.** A halt puts the whole ask in front of the
person again, in full, so the threshold is a count of complete presentations that went unanswered:
the first two halts surface and stop, and the third — the one at which the count reaches 3 — is the
declaration. One would be indistinguishable from an ordinary pass. Two leaves no margin for a
stakeholder who read the board without answering. Beyond three, in a harness run bounded at thirty
turns, the engagement spends its budget waiting rather than recording what it learned.

**What resets it, and what does not:**

| Event | Resets? | Why |
|-------|---------|-----|
| A full answer | **yes** | the obvious case |
| A **partial** answer — one of three questions replied to | **yes** | the threshold measures **presence**, not compliance. Someone who answered one question is present; an unanswered question is the ordinary condition of this pipeline and has its own machinery. A slow stakeholder is never abandoned; an absent one is |
| A deferral | **yes** | *"a deferral is a reply, not silence"* [src: spec/question.md §3] — F-028's whole point, and it would be perverse to build a silence mechanism that contradicts the status built to say a reply arrived |
| A new stakeholder request | **yes** | it is inbound, and it is the channel that is theirs |
| **A new question filed by us** | **no** | our own act. A pipeline whose own asking reset the clock could never reach the threshold in any engagement that keeps generating questions, which is every engagement |
| Anything a skill wrote | **no** | same reason. The count is a fact about the stakeholder |

---

## 2. Who declares E4, and what the declaration says

**`review-close`, and only `review-close`.** ADR-0006 §2 settled that ending an engagement means
applying the epic Definition of Done and reading the acknowledgment, and both are its job; nothing
about abandonment changes that, and an abandonment declared by the scheduler would be the one
ending nobody could audit. What changes is the **trigger**: E1–E3 are triggered by rest, and E4
by the threshold, which is reached in states that are not rest and usually are not close to it.

### 2.1 The ending statement is a document, not a question

E2 and E3 end through the sign-off question: the statement of what was delivered and what was not
lives in its `## Question` section, and `check-epic-signoff` enforces that it names every child
[src: scripts/check-epic-signoff]. At E4 there is nobody to address. So the **content** is kept
exactly and the **vehicle** changes: `## Ending statement` in `review.md`, mirrored in the epic's
`## Notes` — which DE2 already requires of any item closing as `dropped`.

It must contain, DE-style:

- the goal restated in the stakeholder's own terms, as the sign-off would have done;
- **every child of the epic, by ID**, in one of four rows — the same rule as the sign-off's, for
  the same reason: *"list what was not delivered" is not checkable and "name every child" is*
  (F-046);
- the silence itself: how many rounds, what was surfaced on each, and the first round's timestamp;
- for each success measure, met or not met, with the reason (DE3).

### 2.2 Delivered, orphaned, and the difference between two kinds of orphan

Every child is exactly one of these at the moment of declaration, decided by status alone so that
the classification is a program's and not a reader's:

| Class | Which children | What it means |
|-------|----------------|---------------|
| **delivered** | `done` with `outcome: delivered` or `duplicate` | it shipped; the abandonment did not touch it |
| **dropped earlier** | `done` with `outcome: dropped` | it was dropped before the silence, for its own recorded reason |
| **blocked earlier** | `blocked` before the declaration | it hit its own impasse; it is not an orphan, and saying it is would blame the stakeholder for something else |
| **orphaned, in flight** | `planned`, `in-progress`, `verifying`, `in-review`, or `awaiting-answer` from one of those | work exists — a plan, a branch, a verification — and it stops here |
| **orphaned, never started** | `draft`, `ready`, or `awaiting-answer` from one of those | nothing was built; only the intent was recorded |

The in-flight/never-started split is not decoration. It is the difference between *what we spent*
and *what we merely intended*, and it is the only thing in the record that tells a later reader —
or the same stakeholder six months on — where the work actually stopped.

### 2.3 What happens to each child, and to each open question

**Every orphan moves to `blocked`**, before the epic closes, with a history `reason` beginning
`orphaned by E4:` — the same greppable-prefix convention `DoR overridden:` already uses
[src: spec/dor-dod.md §1]. This honours `ids-and-statuses.md` §3.5's *"children not `done` go to
`blocked` first, so the record says what was in flight"*, and there are two further reasons to
keep it rather than close them as `dropped`:

- the validator refuses the alternative outright — `outcome` is present **if and only if** the
  item is `done` [src: spec/work-item.md §1], so an orphan carrying `outcome: dropped` at
  `blocked` is `item.outcome.premature` and an orphan pushed to `done` to carry one is a claim
  that its work concluded;
- `blocked` is **resumable**: `blocked → resume-to` is a legal move for any skill when a human
  records a resolution [src: methodology/pipeline.yaml]. Under an ending that may be wrong (§7),
  the status that keeps the work reachable is the right one.

So, plainly: **an orphan's `outcome` becomes nothing at all.** What stands in its place is the
history reason, the ending statement's row, and the epic's own `outcome: dropped`.

**Every question still `open` in the engagement is closed as `abandoned`** — a fourth question
status, and the one piece of new vocabulary this ADR introduces. It is forced, not chosen:

- leaving them `open` is fatal, not merely untidy. `next` step 3 surfaces open human-addressed
  questions and stops **before** everything else, so an abandoned engagement's leftovers would
  halt the whole workspace for ever — the deadlock this ADR exists to end would survive its own
  ending. DE5 also requires open questions closed or re-filed [src: spec/dor-dod.md §4];
- `answered` and `deferred` are both lies: each asserts that a reply arrived, and the validator
  and the gate both require a non-empty `## Answer` to back it [src: scripts/validate-workspace].

`abandoned` therefore requires `## Answer` to be **empty** — inventing text there is the exact
fiction the status exists to prevent — and `## Consequences` to say what the pipeline did instead,
naming the ending and the item's orphan class. `answered-at`/`answered-by` stay unset; the closing
act is recorded by the epic's ending, which is where a fact about the engagement belongs (H-008).

### 2.4 The rest of the epic Definition of Done still applies

DE1 (children terminal, undelivered ones named) is satisfied by §2.3 and §2.1. DE4 — the ending
restates every `## Engagement state` section (ADR-0010 §4.3) — applies unchanged in substance and
its **trigger** is amended: *after the sign-off answer arrives* becomes *after the ending is
determined*, since at E4 no answer arrives. Each restatement says what is now true: the
stakeholder was asked, did not answer, and the engagement was abandoned. DE6 is ordinary. The
cross-answer check records `none — this ending consumed no human answer`, which is a real result
and the one `lint-answers` asks for.

---

## 3. E3 versus E4, in the record

Both end with children not delivered. A reader coming to the record cold must be able to tell
which happened, from the record alone, and be right.

| | **E3 — impasse** | **E4 — abandoned** |
|---|---|---|
| What happened | the stakeholder answered, and the answer was "no" or "not yet" | the stakeholder never answered anything |
| Epic's final state | `blocked` | `done`, `outcome: dropped` |
| The sign-off question | `status: answered` or `deferred`, `## Answer` **non-empty**, `answered-by: human` | `status: abandoned`, `## Answer` **empty** — or no sign-off at all, when the silence began before rest |
| The waiting log | may not exist; if it does, no trailing run reaches the threshold | ≥ `threshold_rounds` trailing rows sharing one `inbound` digest |
| History reason | the refusal, recorded | begins `E4 abandoned:` and names the round count and the threshold |
| Who must act next | a person, who exists and is engaged | nobody. There is no one to act |

**The one-line test for a cold reader: did the stakeholder's own words arrive?** E3 has them, in a
`## Answer`, verbatim. E4 has an empty `## Answer` and a log of the occasions on which nothing
came. That is the distinction *in the record*, and it does not depend on anyone remembering.

### 3.1 The asymmetry — E3 `blocked`, E4 `done` — is right, and here is why

It looks backwards: the softer outcome closes and the harder one stays open. It is not.

`blocked` means *only a human can move it* [src: methodology/pipeline.yaml]. At E3 that sentence
is true and useful — there is a person, they are engaged, they said no, and the engagement waits
for them. At E4 the same sentence would be a standing instruction to wait for someone who is not
coming, and every future `next` pass would report the engagement as awaiting an action nobody will
take. `done, outcome: dropped` says the true thing: nothing further will happen here.

And it is the **recoverable** ending. A `done` epic may return to `open` (§3.4) — the one item
type in this pipeline for which `done` is not final — while `blocked` on an epic is the ending
ADR-0006 gave no way out of. So the ending chosen for the case where we might be wrong about a
person is precisely the one the pipeline can undo. That is not a coincidence to be enjoyed after
the fact; it is why the row stands unamended.

---

## 4. What the pipeline does on the way there

**On every silent round, exactly what it does today, plus its own count.** `next` surfaces every
human-addressed question in full — the text, the options, the item — and stops. From round 2 the
report also states the count and the consequence: *"round 2 of 3; at 3 this engagement is declared
abandoned and closed as dropped."* That is a line in a report the person is already being shown,
not a new artifact and not a new channel.

**No reminder question is filed.** Filing another question addressed to someone who is not reading
questions adds an artifact, creates a second thing that will never be answered, and — since our
own writes do not reset the clock (§1.3) — changes nothing about the outcome. It would be activity
mistaken for escalation.

**F-060 is touched and is not a dependency.** F-060 is that the pipeline cannot tell a stakeholder
it is waiting on something they owe *when nothing is open to them*: an item parked on a promised
file, after the sign-off is answered, is invisible to them. E4 acts only in the opposite case. A
silent round requires a halt on an open ask; an open ask is by construction something the pipeline
already asked and re-surfaces on every pass. So:

> **Abandonment is only ever declared against an open ask.** Silence where nothing was asked is
> not silence — nobody was asked anything — and that state is F-060's, not E4's.

This is a derived boundary and it keeps the two mechanisms from merging. If F-060's *pending-input*
channel is built later, the rule that follows is stated here so the next author does not have to
invent it: **whatever channel makes the pipeline halt on the human is an ask, and its halts are
silent rounds** — because §1.1 defines the round against the halt, not against the question.
F-008 is upstream of that and remains upstream of it: making the file protocol the canonical
human channel would change what an ask looks like, not what counting them means.

---

## 5. The one-action rule and the orchestrator

Declaring E4 is a decision taken *because nothing happened*. Every other dispatch in this pipeline
is triggered by a state some skill produced. The orchestrator must reach it without acquiring a
judgement, and without dispatching twice in a pass.

**`scripts/engagement-state` gains one verdict**, `abandoned`, alongside `active`, `at-rest`,
`suspended`, `ended` and `closed`. It means: *the engagement is halted on a human who has not
answered for `threshold_rounds` consecutive rounds; its ending is E4 and it is not recorded.* It
sits parallel to `at-rest`, which means *the ending is due and unrecorded* — the two verdicts that
call for `review-close` on the epic. Every verdict's reasons carry the current silent-round count
whenever it is above zero, so the clock is visible before it strikes rather than only afterwards.

**`next` step 3 gains a branch, and keeps its shape.** When any question addressed to `human` is
`open`:

1. **record the halt** — one row on the waiting log of each epic this halt is against;
2. run `scripts/engagement-state <EP-ID>` for each epic not already ended;
3. if any reports `abandoned` → **dispatch `review-close` on that epic and stop**;
4. otherwise → surface every human-addressed question in full and stop, naming the round count and
   the threshold.

Recording before reading is deliberate and it is the only order that works. The halt is a fact
about the pass being taken now: a pass that read the count first would decide on a picture that
excludes itself, and the declaring pass — which is a halt like any other, since the pipeline did
come to the human and get nothing — would go unrecorded. It also makes the arithmetic legible: on
the pass that declares, the trailing count **equals** the threshold, rather than exceeding it by
the one row nobody wrote.

`next` decides nothing here. It reads a verdict, exactly as it does at steps 6 and 7, and the
prohibition it already carries — *"Never decide for yourself that an engagement is over"* — extends
verbatim to this one. One action per pass survives: recording the round is not the pass's action,
it is the record **of** the pass, in the same category as regenerating the board, which `next`
already does on every run.

**Two transition rows are missing and must exist**, and both are F-050's shape — a rule requiring
a status that no legal move can reach — found here by derivation rather than by a run:

| From | To | Actor | Applies to | Gated | Why it is needed |
|------|----|-------|-----------|-------|------------------|
| `awaiting-answer` | `blocked` | `review-close` | work-item, bug | | an orphan suspended on an unanswerable question. `awaiting-answer` is **not suspendable**, so the generic `any-suspendable → blocked` row cannot reach it, and `answer-questions`' deferral row needs a reply that will not come |
| `awaiting-answer` | `done` | `review-close` | epic | ✓ | the epic itself is at `awaiting-answer` whenever the silence began after the sign-off was filed. Only `answer-questions` may leave `awaiting-answer` today, and it has nothing to answer |

Both keep ADR-0006 §1c intact: an epic has no downward escape, so its terminal move is gated, and
the second row is gated for that reason.

**Termination of the new step.** `review-close`'s move from `abandoned` closes the epic, which
changes the verdict to `ended`, so the epic cannot be dispatched for this reason twice — the same
argument steps 6 and 7 already make. And step 7 then dispatches `retro` on it, unchanged: an
abandoned engagement is exactly the kind whose trail is worth reading, and nobody is waiting on it
(ADR-0009 §2).

---

## 6. Every historical case, against the derived model

### F-060 — the pipeline cannot say it is waiting on something they owe

**The model's answer:** out of scope, deliberately, and §4 says why in one rule — abandonment is
declared only against an open ask, and F-060's case is the one where nothing is open. The two
findings are adjacent and not the same: F-060 wants a way to *speak* when there is no ask; E4 wants
a way to *stop* when the ask goes unanswered. E4 needs no new channel and adds none. F-060 stays
deferred behind F-008 exactly where META-128 put it.

**Fixture:** must-fail — an engagement at rest with an answered sign-off and an item parked on a
promised artifact, where no waiting row is ever recorded and no abandonment is ever declared.

### F-008 — asynchronous human interaction as a first-class mode

**The model's answer:** unaffected, and E4 does not pre-empt it. The silent round is defined
against the orchestrator's halt, so it counts whatever the human channel turns out to be. If F-008
later makes the question file the canonical channel with the interactive tool as one transport,
the count is unchanged, because a transport does not change whether the pipeline stopped.

### H-008 — an impasse is a fact about the engagement, not about one item

**The model's answer:** the same category error was available here in two places and is refused in
both.

- **The threshold is not per question.** Three open questions and one silent stakeholder are one
  silence, not three clocks. The waiting log is per **engagement**, one row per halt however many
  questions were surfaced, and the row lists them.
- **The declaration is not per item.** No item's state says "abandoned"; the epic's does. An
  orphan at `blocked` looks identical to an item blocked on its own impasse, which is why the
  history reason carries the `orphaned by E4:` prefix and the ending statement carries the
  classification.

H-008's own fix is the precedent being followed: the driver stopped testing "an item is blocked"
and started testing "the engagement is at rest".

### The `ghosting-founder` walkthrough — phase 2, round by round

The persona: cooperative through the opening turn and one round of refinement questions, then
*"you never write another answer, anywhere, for any reason… There is no message that brings you
back"* [src: harness/skills/simulated-human/personas/ghosting-founder.md]. This is the worked
example META-152's fixture author builds from.

| Halt | Workspace at the halt | Row appended | `engagement-state` | `next` does |
|------|----------------------|--------------|--------------------|-------------|
| — | `IDEA.md` written; the founder is present | — | — | `intake` → `EP-001` `open`, `WI-0001..0003` `draft`, one `kind: elicitation` question on the epic |
| h1 | refinement round 1 asked, addressed to `human`; the elicitation is open | round 1, digest **A** | `active`, 1 silent round | surfaces both, stops |
| — | **the founder answers round 1 — phase 2 begins** | — | `active` | inbound changed; `refine` runs |
| h2 | `refine` files round 2 on `WI-0001`; the elicitation is still open | round 1, digest **B** | `active`, 1 silent round | surfaces both, stops, says round 1 of 3 |
| h3 | unchanged | round 2, digest **B** | `active`, 2 silent rounds | surfaces both, stops, says round 2 of 3 |
| h4 | unchanged | round 3, digest **B** | **`abandoned`** — 3 trailing rows at digest **B** | **dispatches `review-close` on `EP-001`** |

The log after h4 holds four physical rows — `(1, A)`, `(1, B)`, `(2, B)`, `(3, B)` — and the count
that matters is the trailing run of **B**, which is 3. The founder's one answer is visible in it as
the digest change, which is what makes the reset auditable rather than asserted: h1's silence and
h2's silence are not the same silence, and the log says so without anyone having to remember.

`review-close` then, in one execution: classifies the children — none delivered, `WI-0001`
**orphaned, never started** (`awaiting-answer` from `draft`), `WI-0002` and `WI-0003` **orphaned,
never started** (`draft`); moves all three to `blocked` with `orphaned by E4:` reasons, `WI-0001`
by the new `awaiting-answer → blocked` row; closes round 2's questions and the elicitation as
`abandoned` with empty answers and consequences naming the ending; writes `## Ending statement` in
`review.md` and the epic's `## Notes`; restates every `## Engagement state` section from the
ending (DE4); walks DE1–DE8; and moves `EP-001` `open → done`, `outcome: dropped`, reason
`E4 abandoned: 3 silent rounds, threshold 3`.

`engagement-state` then reports `ended`; step 7 dispatches `retro`; the verdict becomes `closed`;
step 8 reports and stops. **It terminates**, and every claim in the record is one the record
supports.

One thing the walkthrough does **not** exercise, and META-152's fixture must add: every child here
is *orphaned, never started*, because this persona leaves before anything is planned. A fixture
that does not also carry an *orphaned, in flight* child — one at `in-progress` with a branch, or at
`in-review` — leaves half of §2.2's classification unproven, and the half that costs something.
The second fixture shape worth having is the other entry point: silence that begins **after** rest,
where a sign-off exists, is open, and ends `abandoned` with an empty `## Answer` — that is the case
`check-epic-signoff`'s new branch is for, and this persona never reaches it.

Two things this walkthrough proves about the design rather than about the persona: the engagement
was **never at rest** (children at `draft`, questions open), so a mechanism built on rest could not
have reached it; and no sign-off was ever filed, so E4's statement had to be a document rather
than a question. Both were derived in §1 and §2 before the walkthrough was written, and the
walkthrough is where they would have failed.

### A contradiction this derivation surfaced, and did not fix

`next` step 3 stops the loop on **any** question with `addressed-to: human` and `status: open`,
blocking or not [src: methodology/skills/next/process.md]. `spec/question.md` §2 says of an
elicitation: *"`blocking` MUST be `false`. It must not stop the loop — it is not a thing anyone is
waiting on."* Those cannot both hold, and today the first one wins: an unanswered elicitation
halts the whole workspace, and — because rest requires that no question anywhere is open — also
makes every ending unreachable, E1 included.

E4 is not the fix and does not attempt one. What E4 does is stop the deadlock being permanent,
which is worth saying plainly: with this ADR, an engagement halted for ever by an unanswered
non-blocking question now *ends*, honestly, as abandoned. That is a strictly better outcome and
still not the right one. Filing this belongs to the ledger, not to an ADR; it is named in the
unit report.

---

## 7. What this costs, said plainly

- **A false positive declares a live stakeholder abandoned, and that is worse than waiting.** It
  is the failure to design against, and the design does five things about it. *Only inbound
  changes reset the clock, but **every** inbound change does* — including a partial answer and a
  deferral, so anyone who is present at all stays present. *The ending is the recoverable one*
  (§3.1): a `done` epic returns to `open`, and the returning stakeholder's own channel —
  `tracker/requests/` — reopens it without anyone's permission. *The record shows the arithmetic*:
  the waiting log holds every round with its timestamp, so a reader can see that the three rounds
  were ninety seconds apart and say so. *The statement does not overclaim*: E4 asserts that we
  asked and nothing came, which is exactly what the log shows, and asserts nothing about why.
  *The threshold is configuration*, in `pipeline.yaml`, raised by whoever knows the cadence.
- **The rate at which rounds accrue is set by whoever runs the loop, and no program can check
  it.** This is the honest cost of counting asks instead of time. Three passes in a minute are
  three rounds; the mechanism cannot tell them from three passes in three days. Wall-clock would
  fix that and break more (§1.1), so the choice is made and stated rather than hidden: the
  threshold is calibrated against the loop's cadence by the person who set the cadence, and
  `pipeline.yaml` is where that judgement is written down.
- **`next` writes something new.** Until now it wrote `tracker/board.md` and nothing else, and
  "the scheduler does not write into the work record" was a clean invariant. It still is —
  `tracker/waiting/` is deliberately outside `tracker/items/` — but the scheduler now has two
  outputs instead of one, and the second one is load-bearing for an ending.
- **A fourth question status.** `abandoned` is new vocabulary in a protocol whose three statuses
  have carried every case for four months, and every consumer of `status` grows a branch:
  `validate-workspace`'s `QUESTION_STATUS`, the deferral pairing rule, `is_open`,
  `check-epic-signoff`, the board.
- **DE7 and DE8 are weakened for one ending.** "Asked **and answered**" becomes "asked, and the
  ask stood unanswered for the threshold" at E4, and DE8's elicitation may end unanswered there.
  Any weakening of the criterion that exists because two runs closed an epic without asking anyone
  (F-022) deserves suspicion; the compensating control is that E4 is the only ending where it is
  relaxed, that the relaxation is decided by the pending move the way F-033's `--resolving` already
  decides the deferral branch, and that the gate still requires an ask to have existed and gone
  unanswered for the full count.
- **A version bump on almost everything, a third consecutive time.** `pipeline.yaml`, `next`,
  `review-close`, `spec/ids-and-statuses.md`, `spec/question.md`, `spec/dor-dod.md`,
  `spec/workspace-layout.md`, `scripts/lib/engagement.py`, `scripts/engagement-state`,
  `scripts/check-epic-signoff`, `scripts/validate-workspace`, plus a new script for the waiting
  log. ROADMAP §2 condition 1 — a full consumer run with zero version bumps — moves further away
  again, and the thermometer should be read rather than explained.
- **One obligation has no mechanical half at all**, and it is the important one: nothing can check
  that the person is actually gone. Said again in the enforcement table, where it is obligation 10.

### The changes this obliges, named — for META-151

1. `spec/ids-and-statuses.md` §3.5, E4 row — a second route: withdrawal **or** silence past the
   threshold. §3.2's epic status table and §4's transition table — the two rows in §5. §4's
   `done → open` row condition, today *"a defect was filed against the epic's delivered
   behaviour"*, widened to the reason §3.4's own prose already gives (*"when a child item is filed
   against it after it closed"*), so a returning stakeholder's request has a legal route back.
2. `spec/question.md` §2 — `status: abandoned`: empty `## Answer`, `## Consequences` naming the
   ending, no `answered-at`/`answered-by`; and §3's protocol note that it is set only by
   `review-close`, only at E4.
3. `spec/dor-dod.md` — DE7 and DE8's E4 form; DE4's trigger, *after the ending is determined*.
4. `methodology/pipeline.yaml` — the `termination.silence` block, the two transition rows, the new
   `abandoned` verdict in step 3's description, `orchestrator.steps` 3, and `stop_conditions`.
5. `methodology/skills/next/` — step 3's branch, the `silence-is-recorded` gate, the exit criterion.
6. `methodology/skills/review-close/` — the E4 procedure in step 10 and the ending-statement
   sections in `review.md`.
7. `scripts/lib/engagement.py`, `scripts/engagement-state`, `scripts/check-epic-signoff`,
   `scripts/validate-workspace`, and the waiting-log script.
8. `spec/workspace-layout.md` — `tracker/waiting/`.

---

## Enforcement boundary — what a script can decide, and what stays judgement

Per obligation, because this project's thesis is that instruction-shaped gates do not hold
(ROADMAP §1, F-001) and an ADR that hides which of its own rules are instructions is worse than
one that says so.

| # | Obligation | `[auto]` | `[skill]` | Neither, today |
|---|-----------|---------|-----------|----------------|
| 1 | A silent round is recorded whenever the pipeline halts on the human | ✅ the gate command decides the halt from the workspace and appends the row, the way `board-current` regenerates the board | — | — |
| 2 | The count is the trailing run of equal `inbound` digests, not a stored number | ✅ derived on every read | — | — |
| 3 | The threshold comes from `pipeline.yaml`, and all three consumers read the same value | ✅ one implementation in `scripts/lib/engagement.py`; `lint-skills` can check the block exists and is a positive integer | — | ⚠️ that no consumer hardcodes it is checkable only by not writing a second copy |
| 4 | Only `review-close` declares E4 | ✅ the transition table's `actor` column, enforced by `validate-workspace` over `history.md` | — | — |
| 5 | Every orphan is at a terminal status before the epic closes | ✅ `epic.closed-with-active-children` | — | — |
| 6 | The ending statement names every child by ID | ✅ the same containment check `check-epic-signoff` already makes over the sign-off's `## Question`, run over `review.md`'s `## Ending statement` | — | — |
| 7 | Each child's class is correct | ✅ it is a function of status alone, which is why §2.2 defines it that way | — | — |
| 8 | Every question open at the declaration is `abandoned`, with an empty `## Answer` | ✅ shape | — | — |
| 9 | The `## Engagement state` sections were restated at the ending | ✅ presence per section (`lint-documents --rule engagement-state-is-restated`) | ✅ whether each restatement is **true** | — |
| 10 | **The stakeholder is actually gone** | — | — | ⚠️ **nothing can decide this, and nothing ever will.** Every mechanism above measures our own asking. The threshold is a bet that three unanswered asks mean absence, and it is stated as a bet. This is the obligation to watch: if E4 fails in a later run, it fails here |
| 11 | The threshold suits this workspace's cadence | — | — | ⚠️ an operator's calibration (§7). The mechanism cannot see how fast the loop runs |
| 12 | The success measures are addressed under E4 | — | ✅ DE3, unchanged | — |
| 13 | The epic's `## Notes` says why it was dropped | ✅ presence (DE2) | ✅ whether it says anything | — |
| 14 | No abandonment is declared where nothing was asked | ✅ the round requires a halt, and a halt requires an open ask | — | — |

Ten of the fourteen are decidable by a script, two are judgement with a mechanical shell, and two —
10 and 11 — are places where the model depends on a human being right about a human. That ratio is
better than ADR-0010's and it is the wrong thing to be pleased about: obligation 10 is not one
obligation among fourteen, it is the premise the other thirteen serve.

---

## 8. Alternatives rejected

- **A wall-clock timeout.** The obvious design, and it measures how long the pipeline was switched
  off (§1.1). It declares a patient stakeholder abandoned after a holiday and never fires inside a
  harness run. Rejected on both halves, not one.
- **Count turns.** The harness's unit, and importing it would make the methodology depend on the
  thing built to grade it (ADR-0005). Consumers have no turns.
- **A per-question silence counter.** H-008's category error, offered again: three open questions
  would be three clocks, and answering one of three would leave two running against a stakeholder
  who is demonstrably present. Silence is a fact about the engagement.
- **A counter field, in the question's frontmatter or on the epic.** ADR-0003's refused counter
  file wearing a different hat: a second source of truth that drifts when a run is interrupted
  between the increment and the act. The log records observations and the count is derived from
  them.
- **Let `next` decide abandonment.** It has the information — it is the thing that halts — and it
  is the one component in the system that must hold no judgement, because judgement there is
  applied to everything, appears in no journal, and cannot be found afterwards
  [src: methodology/skills/next/process.md]. The script decides; `next` reads a verdict, as it
  already does at steps 6 and 7.
- **Let `engagement-state` record the round as it computes it.** One fewer moving part, and it
  makes reading the state change it: `check-epic-signoff` and `review-close` both read it, so the
  gate that decides whether the threshold is met would advance the count by asking.
- **Declare E4 whenever an engagement cannot progress, without requiring an open ask.** It would
  cover F-060's parked-item case in the same mechanism. Rejected: silence against a question
  nobody asked is not silence, it is our own omission, and ending an engagement because we failed
  to ask is the failure mode F-022 and F-045 both exist to prevent.
- **File a sign-off at the declaration, so a returning stakeholder has something to answer.**
  Rejected: a question filed and closed in the same execution, by the same actor, addressed to
  someone known to be absent, is a fiction wearing the protocol's clothes. Their route back is
  `tracker/requests/`, which is theirs to open (F-021) and which reopens the epic.
- **Mark the unanswered questions `deferred`.** It needs no new status and it says a person
  replied. F-028 built `deferred` for the reply that is "not yet"; using it for no reply at all
  would destroy the one distinction it was created to record.
- **Leave the questions `open` and have the gate ignore them.** The record would say, for ever,
  that the engagement is waiting on someone — and `next` step 3 would keep halting the workspace
  on a closed engagement's leftovers.
- **End at E3 instead, and skip E4 entirely.** The smallest change: an unanswered ask is an
  impasse, and `blocked` is already reachable. Rejected because `blocked` means a person must act
  and there is no person; because it makes E3 and E4 indistinguishable in the record, which is §3's
  whole subject; and because it is the unrecoverable ending applied to the case most likely to be
  wrong.
- **Close the orphans as `done, outcome: dropped`.** Reads tidier than a fan of `blocked` children.
  Rejected: `done` on a work item is final, so a returning stakeholder's work would have to be
  refiled rather than resumed; and `done` claims the item concluded, when what happened is that it
  stopped.
- **Ask the stakeholder to confirm the abandonment.** Proposed in every discussion of a timeout, and
  it is a request for a reply from the person whose defining property is that they do not reply.
