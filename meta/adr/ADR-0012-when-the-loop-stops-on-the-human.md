# ADR-0012 — When the loop stops on the human: which questions halt it, and where the halt belongs

- **Status:** accepted
- **Date:** 2026-09-10
- **Unit:** META-162
- **Amends:** ADR-0006 §4 (rest) — condition 2, *"no question anywhere in the engagement is
  `open`"*, becomes *no question that anyone but the stakeholder can act on is open*. And
  ADR-0011 §4's derived boundary — *"a halt requires a question addressed to `human` that is
  `open`"* — which is **narrowed, not reversed**: a halt requires an **outstanding ask**, and §3
  below is the check ADR-0011 §1 invited rather than an assumption that it survives. Also
  `spec/question.md` §2's *"only `review-close` sets it, and only when declaring E4"* for
  `status: abandoned` (widened to any ending, same actor, same shape rules) and `spec/dor-dod.md`
  **DE8** (an accepting branch, with an evidence requirement DE8 has never had).
- **Findings:** F-097, F-104, F-011 (its unfixed half, filed here as **F-109**); **F-110**
  filed and deliberately not fixed (§3, check 4). Touches F-008,
  F-013, F-020, F-021, F-028, F-060, F-064.

## Context

Three rules ship today. No two of them agree.

| # | Rule | Where |
|---|------|-------|
| A | The loop stops where **any** question has `addressed-to: human` and `status: open`. `blocking` is not consulted. | `methodology/skills/next/process.md` step 3, `pipeline.yaml` `orchestrator.steps` 3 |
| B | An elicitation's `blocking` **MUST** be `false`: *"It must not stop the loop — it is not a thing anyone is waiting on."* | `spec/question.md` §2 |
| C | Rest requires that **no question anywhere** in the engagement is `open`, elicitations included. | `scripts/lib/engagement.py`, ADR-0006 §4 |

A wins, because A is the one that executes. The consequences are two filed findings and one
that was filed as fixed and is not.

**F-104.** `intake` files an elicitation at the start of every engagement, because DE8 requires
one and the answers are cheapest to act on early. Until somebody answers it, A halts the whole
workspace and C makes rest unreachable, so `review-close` is never dispatched on the epic and
**every ending is unreachable, E1 included**. The question defined as the one nobody is waiting
on is the question the pipeline waits on hardest.

**F-097.** Because A fires at step 3 — before anything is dispatched — the first human-addressed
question stops the loop, and every other item that could have stated its own question that round
waits behind it. A real run had exactly this and stepped outside the orchestrator to get past it:
`WI-0003`'s `refine` entry names its own trigger as *"the harness's batching rule (amendment
A)"* [src: examples/toy-project], and four questions that would have cost two stakeholder round
trips cost one. The workaround is declared, which is why it is visible; the thing worked around
is in the pipeline.

**F-011's unfixed half.** F-011 is recorded as fixed. It was fixed in `answer-questions`, whose
precondition now reads that a question is answerable when it is `addressed-to: architect` **or**
`addressed-to: human` with `## Answer` filled in — and whose own text says why: *"`next` stops on
any open human-addressed question, so an answered-but-unconsumed one stopped every subsequent
turn forever"* [src: methodology/skills/answer-questions/process.md]. That sentence is in the
past tense and it is present tense in the code. `next` was never changed. A reply the stakeholder
has already written is still, to rule A, a reason to stop and show it to them again — and the
harness carries a second workaround for it: *"Run `answer-questions` on each such item **first**,
before running `/next`"* [src: harness/prompts/worker-turn.md].

Two harness workarounds, in one prompt, for one sentence. That is the shape of this ADR's
subject: **rule A asks the wrong question.** It asks whether a question exists that is addressed
to a person. What the orchestrator needs to know is whether there is something **a person must do
before the pipeline can go on** — and, separately, whether there is anything **else** the
pipeline could be doing instead.

---

## 1. The four classes of open question, and who owns each

Every open question in a workspace is exactly one of these. The classification is a function of
three frontmatter fields and one section's emptiness, so it is a program's and not a reader's.

| Class | `addressed-to` | `blocking` | `## Answer` | Whose move is it? |
|-------|----------------|-----------|-------------|-------------------|
| **ours to answer** | `architect` | either | — | ours: `answer-questions` |
| **a reply to consume** | `human` | either | **written** | ours: `answer-questions` |
| **an outstanding ask** | `human` | `true` | empty | **theirs**, and we cannot go on without it |
| **a standing ask** | `human` | `false` | empty | theirs, and nothing waits on it |

Read off it directly:

> **The loop stops on the human when, and only when, an outstanding ask exists.**

Each of the other three classes is a case the loop must **not** stop on, and each is one of the
three defects in Context:

- *ours to answer* — never stopped the loop; step 4 already dispatches `answer-questions`.
- *a reply to consume* — F-011's unfixed half. Stopping here shows a person the answer they
  wrote. The remedy is not a new rule: it is that `next`'s dispatch condition becomes the same
  sentence as `answer-questions`' precondition 1, which already enumerates both answerable
  shapes. Two readings of one rule is one reading too many (F-045), and here the two readings
  were in two different files saying opposite things about the same question.
- *a standing ask* — F-104. `blocking: false` means *nothing waits on this*, and the only way to
  make that sentence true is to stop waiting on it.

**`blocking` is trustworthy here, and that is not an assumption.** The whole rule rests on the
field being right for the one kind of question that most needs it, and `validate-workspace`
already refuses an elicitation that is not `addressed-to: human` and not
`blocking: false` — `question.elicitation.addressed` — and refuses a sign-off that is not
`addressed-to: human` and `blocking: true`. The two ends of the range are pinned by an existing
gate; this ADR adds no new trust.

### 1.1 What a standing ask is for, since it no longer stops anything

It is surfaced. Every halt puts **every** open human-addressed question in front of the person in
full — that is what a halt has always done and this ADR does not change it — so a standing ask is
seen at every halt, and the waiting log's `surfaced` column records that it was
(`spec/workspace-layout.md` §1.4). What changes is that it no longer *causes* one.

This is the right relationship for the question the class was invented for. An elicitation asks
*"what else matters to you here that we have not asked about?"* (F-064). Holding an engagement
hostage to that question is not attentiveness; it is the pipeline demanding that the stakeholder
have something to say before it will do the work they asked for.

---

## 2. Where the halt belongs, and the one-action rule

Rule A also fires in the wrong **place**, and that half is F-097.

`next` dispatches **one** action per run and stops; the caller loops. That property is what makes
the pipeline observable and resumable, and F-097's accepted direction — *"a pass that lets every
currently-runnable item file the questions it can already state"* — is, read literally, several
actions in one pass. It would put a walk of the board, and a judgement about what each item could
ask, into the one component in the system that must hold no judgement.

It does not have to be read literally, because **the collect pass F-097 asks for already exists.
It is the loop.** Each runnable item is dispatched to its own owning skill, on its own pass, with
its own journal entry and its own gates; each files the questions it can state and suspends. What
stopped that from happening was not a missing mechanism. It was an ordering: the halt sat at step
3, above dispatch, so the loop stopped before the second item ever ran.

> **The halt is the orchestrator's last resort, not its first.** It moves below every step that
> dispatches work.

| | today | derived |
|---|-------|---------|
| 1 | validate | validate |
| 2 | route stakeholder requests | route stakeholder requests |
| 3 | **surface human questions — halt** | dispatch `answer-questions` (**any answerable question**) |
| 4 | dispatch `answer-questions` (architect only) | dispatch the status owner |
| 5 | dispatch the status owner | **surface human questions — halt** |
| 6 | end the engagement at rest | end the engagement at rest |
| 7 | retro | retro |
| 8 | report and stop | report and stop |

**The one-action rule is preserved, unamended, and this derivation needs no amendment to it.**
One action per pass, still; the halt is not a dispatch and never was. What the reordering changes
is only *which* pass halts: a pass that had work to do does the work, and the pass that halts is
the pass that had nothing else. Which is what "waiting on the human" was always supposed to mean.

Three things follow, and all three are improvements the reordering gets for free:

- **F-097 is fixed by ordering alone.** Two items with questions to state now cost two passes and
  one round trip, not two round trips — and `next` acquires no judgement about what could be
  asked, because it never asks that question. It dispatches; the skill decides.
- **A halt now means something.** Before, every pass with any open human question was a halt,
  including passes with a full queue of runnable work. Now a halt says *the pipeline has nothing
  left it can do by itself*, which is a fact about the stakeholder rather than about the
  scheduler's step order — and that is exactly what ADR-0011 counts (§3).
- **Step 5 and step 6 cannot both fire, and they cannot deadlock each other.** An engagement at
  rest has no outstanding ask by construction (§4), so it falls past the halt into the ending. An
  engagement with an outstanding ask is not at rest. The two are complementary, which is why the
  halt can sit above the ending without the ending becoming unreachable — the exact failure mode
  F-104 reports.

### 2.1 The cost of moving it, said here rather than in §7 because it is structural

`record-halt`'s condition was **sufficient** while the halt was step 3: any pass with an open
human-addressed question was a halting pass, so "an ask is open" and "this pass halted" were the
same statement. After the reordering they are not. A pass may have an outstanding ask **and**
dispatch work, and a row written on that pass would be a round that never happened — the count an
ending rests on, inflated by the pipeline's own busyness.

So `record-halt` is given the other half of the condition, and it is mechanical: it records
nothing, and says so, when anything is **dispatchable** — an open request, an answerable
question, or a runnable item. That is steps 2, 3 and 4's existence question, not their selection
question: whether work exists, never which work or in what order. The selection key stays the
orchestrator's alone.

It fails **open**: where something is dispatchable it prints what and exits 0, exactly as it
already does when no epic is halted. A defect there under-counts rounds and delays an E4; the
opposite direction would break the loop, and between the two the safe failure is the one that
waits longer for a person.

---

## 3. The ADR-0011 reconciliation — checked, not assumed

ADR-0011 §1.1 anticipated this ADR by name:

> *"Defining the round against the **halt** rather than against the question set is deliberate.
> Whatever step 3's scope turns out to be — every human-addressed question, or only the blocking
> ones (§6 has a live contradiction about that) — the counter follows the halt, so the two cannot
> drift apart. A pass that did not stop on the human is not a round, and a question that does not
> stop the loop never produces one."*

The unit brief's instruction was to check that claim rather than take it on trust. Checked, three
ways, and the verdict is split: **the counting claim survives; the boundary rule in §4 did not,
and is narrowed here.**

**Check 1 — against the code.** `silent_rounds()` takes a list of `WaitingRow` and returns the
trailing run of equal `inbound` digests. It never reads a question, a status or an addressee; it
cannot, since its only argument is rows. `next_round_number()` is the same. `append_halt()` takes
the digest and the surfaced list from its caller. So no arithmetic anywhere in the count reads
the question set, and changing which questions halt cannot change what a round is. The claim
holds where it was made [src: scripts/lib/engagement.py].

**Check 2 — against the shape of a round.** A round is *one halt with no inbound change since
the previous halt*. Both halves are untouched. `inbound_rendering()` digests **every**
human-addressed question whatever its status, plus every request — so a reply to a standing ask
still resets the clock, which is right, because the count measures presence and not compliance
(ADR-0011 §1.3). A stakeholder who answers only the elicitation is present, and the clock says
so. What the reordering changes is how many passes are halts, and ADR-0011 §7 already says in
plain words that the rate at which rounds accrue is set by whoever runs the loop and that no
program can check it. Fewer halts is a slower clock, not a different unit.

**Check 3 — against §4's boundary rule, which is where it fails.** ADR-0011 §4:

> *"**Abandonment is only ever declared against an open ask.** … A silent round requires a halt,
> and a halt requires an open ask."*

`spec/ids-and-statuses.md` §3.5a spells that out as *"a halt requires a question addressed to
`human` that is `open`"*, and `state()` implements it as `engagement.surfaced` — every open
human-addressed question. Under this ADR that sentence is **false**: a standing ask is open,
addressed to the human, and produces no halt at all. Left as written it would let the
`abandoned` verdict fire against a question nobody is waiting on, which is F-104's own defect
wearing the ending's clothes.

So it is narrowed to what §1.1's last clause already implied — *a question that does not stop the
loop never produces one* — and the narrowing is stated rather than inferred:

> **A halt requires an outstanding ask.** An engagement whose only open ask is a standing one
> accrues no rounds and is never declared abandoned over it.

**And that narrowing is exactly why rest had to change too.** If a standing ask accrues no
rounds, an engagement holding one can never reach E4 by silence; if it also holds rest (rule C),
it can never reach E1, E2 or E3 either. Repairing the halt without repairing rest does not fix
F-104, it converts a loop that halts for ever into a loop that idles for ever. That is the
constraint META-153b established by reading the code, and it is the reason §4 below exists.

**Check 4 — against §1.3's table, which turned up a defect this ADR does not fix.** The row
*"a new question filed by us — resets? **no** — our own act"* does not hold in the code.
`inbound_rendering()` emits one line per human-addressed question whatever its status, so filing
a question adds a line, moves the digest and restarts the count — while the same function's
docstring says *"a question **we** file changes no line here"* and `pipeline.yaml` says *"nothing
a skill writes is inbound"*. Proved by execution over a copy of
`fixtures/abandoned-engagement/right`: `EP-003`'s digest is `ee47bf97`, and adding one unanswered
human-addressed question to `WI-0008` moves it to `edd86dbe`. It is **filed as F-110 and not
fixed here** — it is a different rule from the one being derived, and its fix moves the digests
three banked fixtures assert. It is named in this section rather than only in the ledger because
this ADR makes it worse: the loop now dispatches between halts, so there is more room for a skill
to file a question between two of them.

**What is not amended.** §1.2 (the count is derived, never stored), §1.3's *substance* (any
inbound change resets, and only an inbound change does — F-110 is a defect against that rule, not
a change to it), §2
(who declares E4 and what the declaration says), §3 (E3 versus E4 in the record — the
discriminator is the **sign-off's** status and the waiting log's trailing run, neither of which
this ADR touches) and §5's transition rows all stand as written.

---

## 4. Rest, restated as the complement of the halt

ADR-0006 §4 condition 2 — *no question anywhere in the engagement is `open`* — was written when
every open question stopped the loop, and it meant, in that world, *nothing is outstanding*. It
no longer means that, so it is restated to say what it always intended:

> An engagement is at rest when: every child is at a terminal status; **no open question is
> anyone's to act on but the stakeholder's, non-blockingly** — that is, every open question in it
> is a standing ask; and no request is open.

Equivalently, and this is the form the code takes: an open question **holds** rest unless it is a
standing ask. Each of the other three classes holds rest for its own reason, and none of them is
an exception:

- *ours to answer* and *a reply to consume* — a skill can still advance them, so the engagement
  is not over. Both are drained by step 3 before the loop can reach the ending anyway.
- *an outstanding ask* — the pipeline is waiting on a person and must keep asking that, not file
  a sign-off asking a different question.

A standing ask holds nothing, because nothing is what it was declared to hold.

### 4.1 The deadlock's fourth site, and why it is not a fifth

Repairing the halt and rest together makes every ending **reachable**. It does not yet make one
**recordable**, and the site is `check-epic-signoff`:

- **DE5** requires open questions closed or re-filed at the ending.
- **DE8** requires a `kind: elicitation` question that was **answered** — and, since ADR-0011,
  accepts one that is `abandoned` with an empty `## Answer`, but only at E4 by silence.

So an engagement that reaches rest with a standing ask still open — which is now a state the
pipeline can be in, and before this ADR was not — must close it under DE5, and the only honest
closure for a question nobody replied to is `abandoned`, and DE8 refuses `abandoned` anywhere but
E4. **A rule requiring a state no legal move can reach:** F-013's shape from one side and F-050's
from the other, and this repo carries a `rule_obligations` gate because it has now written that
bug twice by hand. Finding it by derivation rather than by a run is the whole point of writing
this section before writing the code.

Two changes, both narrow, and both of them widen an existing mechanism rather than adding one.

**(a) `abandoned` is set at any ending, not only at E4.** ADR-0011 §2.3 already has
`review-close` closing every question still `open` as `abandoned` when it declares an ending; the
only thing amended is *which* ending. Every shape rule stands: `## Answer` MUST be empty because
the emptiness is the evidence, `## Consequences` names what the pipeline did instead,
`answered-at`/`answered-by` stay unset, and only `review-close` sets it. H-008's rule stands too
— a question is still never abandoned *on its own account*, because it is still only ever set as
part of declaring an ending. And ADR-0011 §3's E3/E4 test is untouched, because that test reads
the **sign-off's** status and the waiting log's trailing run, and neither is affected by what a
non-blocking question elsewhere in the engagement records.

**(b) DE8 gains an accepting branch, and an evidence requirement it has never had.** An
`abandoned` elicitation satisfies DE8 at any ending **provided the waiting log shows it was
surfaced to the person at least once**. This is a weakening and it is written down as one in §6.
What is traded for it is not nothing: DE8's old second half — *and it was answered* — is a
criterion the pipeline cannot compel, since only the stakeholder can satisfy it, and ADR-0011
already conceded exactly that for E4. What replaces it here is a half the pipeline **can** be
held to and never has been: *and we put it in front of them*. `review-close` is allowed to file
the elicitation alongside the sign-off precisely so the rule cannot deadlock an engagement that
forgot it, and that route was one halt away from being theatre — file it, close it, satisfy DE8,
and never show anybody anything. Now it is not, because the log is written by a different program
on a different pass.

The evidence exists by construction: rest files a sign-off, a sign-off is `blocking: true`, so
the ending is reached through at least one halt, and a halt surfaces every open human-addressed
question and records the list.

---

## 5. Every historical case, against the derived model

### F-104 — an unanswered elicitation deadlocks every ending

**The model's answer:** rule B is the rule and rules A and C follow it. A standing ask stops
nothing and holds nothing. Both loci the finding names are repaired in one sentence rather than
two, and the third locus it did not name — `record-halt`'s idea of what a halt is — follows from
the same predicate, in the same function, because all three now read
`engagement.outstanding_asks()`.

**Fixture:** must-pass — an engagement at rest whose only open question is a standing ask reports
`at-rest` and records no halt. Must-fail — the old predicate restored, which returns `active` and
writes a row.

### F-097 — the loop stops on the first human question

**The model's answer:** §2. The ordering, not a new pass, and the one-action rule is untouched.
The literal collect-askable-questions pass is rejected in §7 with its reason.

**Fixture:** must-pass — a workspace with an outstanding ask **and** a runnable item records no
halt, and names the item that is dispatchable instead. Must-fail — the dispatchable guard
removed, which records a round on a pass that had work to do.

### F-011 — `answer-questions`' precondition excluded the case the protocol depends on

**The model's answer:** the half that was fixed stays fixed. The half in `next` is *a reply to
consume* in §1's table, and it is repaired by making `next`'s dispatch condition the same
sentence as the precondition. Filed as **F-109** rather than reopening F-011, because F-011's own
status text is accurate about what it changed and a status that says "fixed" for one file and not
another is worth two entries, not one edit.

### F-020 — several separate questions for one item in one round

**The model's answer:** unaffected in its substance and better served in practice. F-020's fix is
a presentation convention — one item's questions in one round open with the same frame and the
last says that is all of them. The reordering makes *"which of how many this is"* a larger and
truer number: a round now carries every question every runnable item could state, so a
stakeholder who would have received two emails on Monday and two on Tuesday receives one
conversation. Nothing in the convention changes.

### F-021 — the stakeholder has no channel for unsolicited input

**The model's answer:** unaffected. `tracker/requests/` is step 2 and stays first; a request
outranks everything including the halt, and a stakeholder speaking unprompted is inbound, so it
resets the clock (ADR-0011 §1.3).

### F-028 — a deferred answer has no representation

**The model's answer:** unaffected, and its rule is the precedent for §4.1(a). `deferred` records
that a reply arrived and was *"not yet"*; `abandoned` records that none arrived. Widening
`abandoned` to any ending does not touch that distinction, because the distinction is about
whether `## Answer` has the person's words in it, and both statuses' rules on that section are
unchanged.

### F-060 / F-008 — the pipeline cannot say what it is waiting for; async as a first-class mode

**The model's answer:** both stay deferred, F-060 behind F-008, exactly where META-128 put them
and where ADR-0011 §6 re-decided them. This ADR gets adjacent to F-060 in one respect and stops
short of it deliberately: `next`'s report now names every outstanding and standing ask on
**every** pass, including passes that dispatch, so a reader can see what is pending without the
loop having to stop to tell them. That is a line in a report, not a channel — it says nothing to
anybody who is not already reading the run's output, which is precisely F-060's complaint. F-060
wants a way to speak when no ask is open; here an ask **is** open and the only change is that we
stopped confusing "showing you this" with "stopping for this".

### F-013 / F-050 — a rule requiring a status no legal move can reach

**The model's answer:** §4.1 is that shape found by derivation, in DE5 against DE8, and fixed
before it shipped. It is recorded here because the class is what ADR-0006 exists to close, and
the third instance of a class is evidence that the check for it belongs somewhere mechanical —
`pipeline.yaml`'s `rule_obligations` covers status rules and does not cover Definition-of-Done
criteria, and nothing in this ADR changes that.

---

## 6. What this costs, said plainly

- **The pipeline now keeps building while the stakeholder is unanswered.** This is the reordering
  seen from its worst side: an outstanding ask on `WI-0001` no longer stops `WI-0002` from being
  planned, implemented and verified. If the pending answer would have invalidated `WI-0002`, that
  work is now spent before anyone knows. The machinery for that case exists and is not new — a
  skill that learns something invalidating files a **blocking** question on the item it
  invalidates, which suspends it (`spec/request.md` §1, `intake` step 0) — but it is machinery
  somebody has to use, and the old behaviour was a blunt instrument that protected against it by
  accident. The trade is deliberate: the old protection cost one stakeholder round trip per item
  in **every** engagement, and this cost is paid only where an answer turns out to invalidate
  work nobody suspended.
- **A silent round is a scarcer thing, so E4 by silence arrives later.** The clock only runs on
  passes with nothing else to do. An engagement with a long queue and an absent stakeholder works
  through the queue first and is declared abandoned afterwards. That is the right ordering — it
  is not waiting on them while it works — and it means an abandonment that took three passes
  before this change may take thirty afterwards. ADR-0011 §7 already says the rate is the
  operator's to calibrate and no program can check it; this makes that sentence matter more.
- **`record-halt`'s condition is no longer sufficient by itself**, and the half that replaces it
  is a second reading of steps 2–4's existence question (§2.1). It is one implementation in
  `scripts/lib/engagement.py` read by one caller, which is the F-045 remedy applied in advance,
  but it is a place where the scheduler's world model is now consulted by something that is not
  the scheduler.
- **DE8 is weakened, for the second time, and by the same argument.** ADR-0011 relaxed *asked and
  answered* to *asked and unanswered* at E4; this relaxes it at every ending. Any weakening of a
  criterion that exists because a stakeholder held two real requirements for a whole engagement
  and was never given a vehicle (F-064) deserves suspicion. The compensating control is in
  §4.1(b) and it is a real one — DE8 now requires evidence that the question reached the person,
  which it never did — but the criterion is softer than it was and saying otherwise would be
  spin.
- **A version bump on almost everything, a fourth consecutive time.** `pipeline.yaml`, `next`,
  `review-close`, `scripts/lib/engagement.py`, `record-halt`, `check-epic-signoff`,
  `spec/ids-and-statuses.md`, `spec/question.md`, `spec/dor-dod.md`. ROADMAP §2 condition 1 — a
  full consumer run with zero version bumps — moves further away again.
- **Two harness workarounds become dead code, and this ADR does not remove them.** The worker
  turn prompt's *"run `answer-questions` first"* and its batching amendment A both become
  unnecessary. Deleting them is a harness change and no harness run is in flight; it is named
  here so the next person to open that file knows why the paragraphs are there and what they may
  now be tested against.
- **One obligation has no mechanical half at all**, and it is the one the reordering created:
  nothing can prove that the pass which wrote a waiting row was a pass that actually halted.
  Obligation 4 in the table below.

---

## Enforcement boundary — what a script can decide, and what stays judgement

Per obligation, because this project's thesis is that instruction-shaped gates do not hold
(ROADMAP §1, F-001) and an ADR that hides which of its own rules are instructions is worse than
one that says so.

| # | Obligation | `[auto]` | `[skill]` | Neither, today |
|---|-----------|---------|-----------|----------------|
| 1 | The four classes are computed from the record, not judged | ✅ three frontmatter fields and one section's emptiness, in `engagement.py` | — | — |
| 2 | A standing ask stops nothing: it does not halt the loop, hold rest, or accrue a round | ✅ one predicate, three consumers — `record-halt`, `state()`'s rest and `state()`'s abandonment trigger | — | — |
| 3 | `blocking` is honest on the questions the rule turns on | ✅ `question.elicitation.addressed` and `question.signoff.addressed` pin both ends of the range | ✅ whether an ordinary question's author judged blocking correctly | — |
| 4 | A waiting row is written only by a pass that actually halted | ⚠️ **partial and newly so.** The necessary half is checked — an outstanding ask exists, and nothing is dispatchable (§2.1). The sufficient half is not: nothing can prove the caller had reached step 5 | ✅ `next`'s self-check | ⚠️ this is the obligation the reordering created and the one to watch. If the silence clock misbehaves in a later run, it will misbehave here |
| 5 | The halt sits below every dispatching step | — | ✅ `next` executes `pipeline.yaml`'s `orchestrator.steps` in order | ⚠️ nothing reads a skill's prose and confirms it follows a numbered list. `record-halt`'s guard is the closest thing: a pass that halted early records nothing and says why |
| 6 | An engagement at rest has no outstanding ask | ✅ complementary by construction — both derive from the same predicate | — | — |
| 7 | `next` dispatches `answer-questions` on every answerable question | — | ✅ the skill's step 3 | ⚠️ the condition is now identical in two files by intent; nothing checks that they stay identical |
| 8 | A question still open at an ending is closed `abandoned`, with an empty `## Answer` | ✅ shape, unchanged from ADR-0011 (`question.abandoned.*`) | ✅ that `review-close` closed **all** of them | — |
| 9 | DE8's elicitation was surfaced to the person | ✅ the waiting log's `surfaced` column names it | — | — |
| 10 | DE8's elicitation was a **good** question | — | — | ⚠️ unchanged from F-064's own note: presence is checkable, quality is not |
| 11 | Work dispatched past an outstanding ask is not invalidated by the pending answer | — | ✅ the skill that learns something invalidating files a blocking question | ⚠️ nothing can see an invalidation nobody noticed. This is §6's first cost with a number on it |

Seven of the eleven are decidable by a script, two are judgement with a mechanical shell, and
four carry a ⚠️ — three of them created by this ADR rather than inherited. Obligation 4 is the one
to watch, for the same reason ADR-0011's obligation 10 was: it is the premise the counting rests
on, and it went from checkable to partly checkable in exchange for F-097.

---

## 7. Alternatives rejected

- **Strike `spec/question.md` §2's sentence instead, and let every human question stop the
  loop.** The other way to resolve a contradiction, and F-104's Direction names it as a real
  option: then `blocking: false` on an elicitation is a label with no behaviour behind it. It is
  rejected because it makes DE8 — one elicitation per engagement, filed at intake, where the
  answers are cheapest — into a mechanism that halts every engagement at its first pass until
  somebody replies. The rule that would have to give is the one added most recently and for the
  best-evidenced reason (F-064). And it would leave F-097 entirely unaddressed.
- **A literal collect-askable-questions pass**, as F-097's Direction proposes: walk the board,
  let every currently-runnable item file what it can state, then halt. Rejected: it is several
  actions in one pass, and the judgement about what an item "can already state" is engineering
  judgement inside the scheduler — applied to every item, appearing in no journal, findable by
  nobody afterwards. The loop already does this correctly, one item and one journal entry at a
  time, and only the step order stopped it.
- **Keep the halt at step 3 and exempt only non-blocking questions.** The smallest change that
  fixes F-104. Rejected because it leaves F-097 exactly as filed, and because the two findings
  are the same sentence read twice: one asks *which* questions stop the loop and the other asks
  *when* it stops. Fixing one and not the other leaves the harness's amendment A in place as the
  only way to run the pipeline as designed.
- **Repair `next` step 3 and leave rest alone.** Explicitly refused: rest counts elicitations
  too, so the loop would run and the engagement would still have no reachable ending. This moves
  the deadlock rather than removing it, and §3 shows the same argument reaching the silence clock
  and §4.1 shows it reaching DE8. A deadlock with three sites is not repaired at one of them.
- **Let `record-halt` fail non-zero when something is dispatchable.** Stricter, and it turns a
  library defect into a stopped pipeline: `silence-is-recorded` is a hard gate with
  `on_failure: stay`, so a false positive would mean the loop can neither dispatch nor halt.
  Failing open under-counts rounds and delays an ending; failing closed stops the engagement. The
  safe failure is the one that waits longer for a person (§2.1).
- **Have `next` decide for itself whether the pass halted, without a guard.** The status quo,
  and it is exactly the arrangement that produced the two harness amendments: a rule written only
  in prose is a rule the runner may reasonably read past. The guard does not decide *which* work
  to do — that stays the selection key's — only whether any exists.
- **A third question status for "asked, shown, and never answered while the person was
  present".** Considered for §4.1(a), and it is one status too many. `abandoned`'s whole content
  is *no reply arrived, and the empty `## Answer` is the evidence*, which is true in both cases;
  the E4-only restriction was a scoping decision made when a question could not survive to any
  other ending, not a claim about what the word means. A new status would also grow a branch in
  `validate-workspace`, `check-epic-signoff`, `is_open` and the board for a distinction no
  consumer would read.
- **Let the epic close with the standing ask left `open`.** Cheaper than widening `abandoned`,
  and under this ADR it is no longer *fatal* — a standing ask on a closed epic halts nothing. It
  is still a lie in the record: `open` asserts that a reply is expected, on a question nobody will
  ever answer, in an engagement that has ended. ADR-0011 refused the same shape for the same
  reason at E4.
- **Require a standing ask to be answered before rest.** It restores C's effect with a nicer
  name, and it is F-104 again: an engagement cannot end because a person declined to volunteer
  something.
- **Count a dispatching pass as a silent round if an outstanding ask is open on it.** It would
  keep the clock running at its old rate and preserve `record-halt`'s sufficiency. Rejected: it
  says the pipeline was waiting on a person during a pass in which it was doing the work they
  asked for, which is false, and it would let a busy engagement with a slow-but-present
  stakeholder accrue three rounds while nobody was asked anything twice.
