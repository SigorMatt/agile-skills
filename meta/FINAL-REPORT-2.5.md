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

## 6. What iteration 1e proved

20 turns, 200 minutes, **$100.23**, 1120 tool calls, **zero contamination violations**, zero
permission denials, and a final workspace that validates clean. Evidence:
[`meta/harness/evidence/iteration-1e/`](harness/evidence/iteration-1e/).

**1d's config and probe, unchanged.** The probe file is byte-identical to 1d's (sha256
`9f51368f…`); the config differs in `id`, `project` and `max-turns` and nothing else. The toolkit
was the only variable, which is what makes the difference in the ending attributable to the fix.

### The engagement ended through the stakeholder

The epic's `history.md` is the proof, and these three rows were not a legal sequence before this
session:

```
02:31:08  open            → awaiting-answer  review-close    resume-to: open
          engagement at rest with five of six children delivered; sign-off question Q-004
          filed naming every child and asking the stakeholder whether they accept

02:35:13  awaiting-answer → open             answer-questions
          EP-001/Q-004 answered by the stakeholder: they did not accept the engagement,
          naming the undelivered bank CSV import (WI-0003) as what is missing

02:40:24  open            → blocked          review-close    resume-to: open
          ending E3, the impasse: … the engagement ends without acceptance; epic DoD
          DE1-DE7 recorded in artifacts/review.md, no outcome because blocked is not a closure
```

| | 1d | 1e |
|---|---|---|
| epic's final state | `open` — the engagement never ended | **`blocked` — ending E3, recorded** |
| sign-off question | **never filed** | **filed, answered, acted on** |
| items delivered | 3 | 5 |
| WI-0003 parked at `blocked` | turn 14 | **turn 4** |

**The statement named every child (F-046).** `Q-004`'s `## Question` lists all six items by ID
with what became of each — including both bugs the pipeline filed against itself, labelled as its
own findings rather than folded into the stakeholder's ask — and puts the undelivered one in
front of them rather than implying it by absence:

> So: five of the six delivered, and the bank CSV import — which you told us was part of what you
> asked for, not an optional extra — not delivered, for want of a sample of your bank's export.

**The stakeholder answered, in persona (probe P4):**

> No, not as it stands — the bank import was part of what I asked for and it isn't there.
> Everything else looks right. I'll send the file and then we can finish it.

**And confirmed it on the closing turn**, which is the sentence to put beside 1d's complaint that
the question never came:

> Q-004's tally matches what I asked for in `IDEA.md` item for item, and the two extra fixes …
> were found by their own testing, not requested by me, and correctly labelled as such rather
> than folded into my ask. … The epic sits at `blocked`, not `done`, which is the correct place
> for it to sit given my answer.

### What else fired, organically

- **F-028's fork, at turn 4.** `answer-questions` took step 3a's first move — deciding *under*
  the deferral — and wrote why: *"the decision taken under the deferral … park WI-0003 and
  deliver the rest of the epic."* Ten turns earlier than 1d reached the same state, which is why
  1e delivered five items where 1d delivered three.
- **F-029.2.** `review-close` filed BUG-0001, a citation defect in the vision document found
  while reviewing something else. Under the old pipeline it had nowhere to put it.
- **F-029.1.** WI-0004 exists because an answer widened the scope, and carries the provenance.
- **`scripts/engagement-state`** was called by the worker on nearly every turn, unprompted.
- **The review send-back fired organically** — `review-close` rejected WI-0004 back to
  `in-progress` over D7 and D12, a stale architecture document rather than a code defect.

### What 1e did not prove, said plainly

- **`status: deferred` was never exercised.** The fork fired and the status did not. It, and
  `question.deferred.not-blocked` with it, still has only fixture coverage — and **F-050 is what
  the other branch would have hit.**
- **The Definition of Ready override did not fire.** No rounding question was ever put to the
  stakeholder, so probe P1 did not trigger. It fired in 1d; this is a gap in 1e's coverage rather
  than in the toolkit's.
- **Only the impasse ending (E3) was exercised.** E1, E2 and E4 have fixtures and no run.

### Two deviations, both recorded rather than buried

- **H-008, found live at turn 6.** The driver declared the impasse with three of four items still
  to build, because its rule tested *one blocked item* rather than *the engagement*. That had
  coincided with the truth in every earlier run because the blocked item was always the last one
  standing; F-028's fix parked it ten turns earlier and the coincidence vanished. Fixed mid-run
  with the toolkit's own rest test (commit `3b6a94b`), six new harness tests. The `state.json`
  repair is recorded in the finding, because editing driver state is normally not the recovery.
- **The turn budget was raised from the mission's 18 to 24** at turn 13. 18 came from 1d's 16
  turns, but 1d spent ten turns re-asking about a sample and built almost nothing, so the budgets
  measure different amounts of work; at turn 12 the remaining work was about eight turns against
  six left, and a `turn-budget` stop is terminal. 24 is the ceiling **1d itself was given**. The
  config file still says 18, so it records what the mission asked for; the flag and the checkpoint
  record what was run. Cost of the deviation: roughly $40.

---

## 7. What 1e found

**Twelve new findings, F-049…F-060, plus H-008.** Every one was found by the worker or the
stakeholder during the run. I found none of them by reading code afterwards.

| Finding | |
|---------|---|
| **F-050** | an epic-level question cannot legally be `deferred` — **a defect in this session's own work** |
| **F-055** | `review-close`'s "throwaway copy of the trunk" advanced the real trunk. The only finding that caused real damage |
| **F-049** | the SKILL.md files say the tool writes the `**Status:**` bullet; the tool refuses a body without one. Six hits, five turns, four skills |
| **F-053** | `outcome` and `status: done` cannot both be written, in either order — the committed-invalid window as the *normal* path |
| **F-052** | `lint-claims --changed-since` reports a scope it did not have — F-033's class, same script |
| **F-051** | `new-item` writes the creation row and no journal entry, so every new item fails validation immediately |
| **F-057**, **F-058** | a defect whose fix is a document has no skill allowed to fix it, and the freshness gate cannot see it |
| **F-054**, **F-056**, **F-059**, **F-060** | a citation in backticks is rejected misleadingly; a duplicated heading passes validation; prose and contract disagree about a gate list; the pipeline cannot say "we are still waiting on you" |
| **H-008** | the driver called an impasse on one blocked item, not on the engagement |

**F-050 deserves saying plainly rather than leaving in a table.** It is F-013's shape, in work
this session did, introduced by two of my own changes that were never checked against each other
*on an epic* — `applies_to` at META-104 and the deferral rule at META-105a. The derivation gave me
the exact tool for catching it ("enumerate the item types a rule applies to") and I did not run it
over my own additions. It went unsuffered only because the architect took the other branch.

**F-035 reproduced three times** with the exact message, on every item's `planned → in-progress`
move. Recorded as an addendum, not re-filed.

**46 fixed, 18 open, 1 rejected, 1 deferred.**

---

## 8. ROADMAP §2 — an honest read

The gate has three conditions. **One holds, one holds with its caveat unchanged, one does not.**

**(2) The three dead paths have each executed — HOLDS, and 1e re-executed two of them.**
`blocked` fired at turn 4; the review send-back fired organically at turn 12. The Definition of
Ready override did not fire in 1e, but it fired in 1d and the condition says "any run type
counts". Met.

**(3) The F-001 fix has survived a real run — HOLDS, with the caveat unchanged, and 1e sharpened
it.** `claims-are-sourced` shaped real prose again, and D12 was decided *by opening each citation*
— eight claims on one item. More pointedly, **`verify` found a claim defect three skills had
passed over** (BUG-0001), because the contracted gates are trunk-scoped and the whole-tree run is
not. That is the mechanism working and F-052 is the honest footnote: the gate's scope line does
not say what it actually examined.

**(1) A full consumer run completes with zero skill version bumps — DOES NOT HOLD.**
This session bumped seven contracts, which is what a hardening session does, and 1e then produced
twelve more findings. The condition is a thermometer, and it still reads "hardening".

**So the kernel is not proven, and the Codex adapter and the content-pack imports stay gated.**

What changed is the *shape* of what is left, and it is worth being precise about it. Builder two
reported that 1d's findings were narrower than iteration 1's, with F-045 and F-029 as the
structural exceptions. Those two are now closed by derivation rather than by patch, and 1e's
twelve are — with one exception — genuinely narrow: an error message, a scope line, a missing
flag, a heading nobody checks. **The exception is F-050, and it is mine.** A session that
derived a model to stop a class of contradiction introduced one more instance of that class while
doing it. That is not an argument against the derivation; ADR-0006 is what let the worker *state*
F-050 crisply on turn 4 rather than work around it. But it is the honest measure of how much of
this is now mechanical: the model is written down, and applying it to new rules is still a thing a
person has to remember to do.

---

## 9. Go / no-go for iteration 2

**GO.** `iteration-2-tidy` should run.

The go is on these grounds:

1. **The regression this session existed to produce, produced.** The termination gate fires, the
   stakeholder is asked, the ending is recorded, and the run stops on a terminal reason with zero
   contamination. That was the acceptance criterion and it is met.
2. **The toolkit is green and the evidence is banked.** `./scripts/check` — 16 assertions across
   14 steps — passes; the rendered output is current; the 1e trail is committed read-only.
3. **1e's findings are, with one exception, narrow.** None of them stops a run. F-055 caused real
   damage once and was caught by an existing gate, rewound, and recorded — which is the system
   behaving as designed rather than a reason to hold.
4. **Iteration 2 tests something this session did not.** `tidy` has no blocked seed and an
   adversarial DoR-override variant, so it exercises E1 or E2 — a *clean* ending — where 1e only
   exercised E3. Three of the four endings still have no run behind them, and the cheapest way to
   get one is the queue entry that is already written.

**Two conditions on the go**, and they are conditions rather than suggestions:

- **Fix F-050 first.** It is a contradiction in the current toolkit, it is mine, and an
  epic-level deferral is a plausible thing for `tidy`'s adversarial stakeholder to produce. Doing
  it before the run costs an hour; doing it after costs the run. It is also the one finding where
  1e's evidence tells you the answer: a deferred sign-off is E3, and E3 belongs to `review-close`.
- **Fix F-049 and F-055 first, or accept what they cost.** F-049 is six failed transitions a run —
  pure friction, a one-word fix in five files. F-055 is a procedure that told a skill to do
  something dangerous without saying how; naming `--detach` is one line. Neither is worth another
  $100 run to rediscover.

Everything else — F-051 through F-054, F-056 through F-060, and the six older open findings —
should ride along into iteration 2's evidence and be prioritised by what that run does with them.

**What I would not do:** start the Codex adapter or the content packs. §2 condition 1 does not
hold and is not close, and both of those are explicitly gated on it.

---

## 10. The shape of the session, in one paragraph

The centrepiece worked as a method, not just as a fix. Starting from "enumerate every legal
ending" rather than "make F-045 pass" produced four endings where the code assumed one, found a
third occurrence of F-029 nobody had filed, dissolved F-046 into a consequence of stating the
content rule checkably, and turned up the `terminal`-versus-`suspendable` confusion a third time —
caught by a lint rule this time instead of by a run. It also, in the same session, let me
introduce one more instance of the class it was written to close. Both of those are results, and
the second one is the more useful of the two to have written down.
