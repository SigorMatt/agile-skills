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
| `status` | always | `open` \| `answered` \| `deferred` \| `abandoned` |
| `created` | always | UTC ISO-8601 |
| `answered-at` | when `answered` or `deferred` | UTC ISO-8601, ≥ `created`. MUST be absent when `abandoned` — nothing arrived, so there is no time at which it did |
| `answered-by` | when `answered` or `deferred` | `answer-questions`, or `human` when escalated. MUST be absent when `abandoned` |
| `kind` | optional | `decision` (the default when absent) \| `sign-off` \| `elicitation` |

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
- **Options first; the recommendation last, and marked as ours.** The `- **Recommendation:**`
  line comes after every option, inside `## Options considered`, and nowhere else — not in
  `## Context`, not in `## Question`. A stakeholder who received eleven questions "every one with
  the preferred answer printed above the options" chose against the recommendation twice and
  wrote: *"I would rather have been asked plainly"* (F-063). A compliant persona would simply
  have been steered, and nobody would have known. The recommendation is worth having — it is the
  thinking the previous rule demands — but a reader must reach the options before they reach our
  preference, and must be able to see that the preference is ours.
- `## Answer` and `## Consequences` MUST be non-empty when `status: answered` or
  `status: deferred`. When `status: abandoned`, `## Answer` MUST be **empty** and
  `## Consequences` MUST be non-empty — see below.
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
- The orchestrator does **not** stop on a deferred question (the halt step reads `open`), and
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

### `status: abandoned` — the reply that never came

`deferred` records a reply of "not yet". `abandoned` records **no reply at all**: the question was
addressed to `human`, it stood open across `termination.silence.threshold_rounds` silent rounds,
and the engagement ended at E4 by silence (`ids-and-statuses.md` §3.5a). It is the pipeline's only
vocabulary for absence, and it is forced rather than chosen:

- leaving the question `open` is fatal rather than untidy where the question is a **blocking**
  one: the orchestrator halts on any outstanding ask, so an abandoned engagement's leftovers
  would halt the whole workspace for ever — the deadlock E4 exists to end would survive its own
  ending. A standing ask left open is not fatal any more (§3 rule 4a) and is still a lie in the
  record, because `open` asserts that a reply is expected on a question nobody will ever answer,
  in an engagement that has ended. Definition of Done DE5 also requires open questions closed or
  re-filed.
- `answered` and `deferred` are both lies. Each asserts that a reply arrived, and each requires a
  non-empty `## Answer` to back it. Using `deferred` for silence would destroy the one distinction
  F-028 created it to record.

The rules:

- **`## Answer` MUST be empty.** Writing anything there — a summary, a note that nobody replied, a
  reconstruction of what they would probably have said — is the exact fiction this status exists
  to prevent. The emptiness is the evidence.
- **`## Consequences` MUST be non-empty** and names files like any other consequence. It says what
  the pipeline did instead: the ending it was closed under (E4, with the round count and the
  threshold), the epic whose ending closed it, and the item's own class from §3.5a's table —
  delivered, dropped earlier, blocked earlier, orphaned in flight, or orphaned never started.
- **`answered-at` and `answered-by` stay unset.** No reply arrived, so there is no time and no
  author to record. The closing act is recorded by the epic's ending, which is where a fact about
  the engagement belongs.
- **Only `review-close` sets it, and only when declaring an ending.** No other skill, and never
  on its own account: abandonment is a fact about the engagement, not about one question (H-008).
  It was scoped to E4 alone when it was created, and that was a scoping decision rather than a
  claim about the word: a question could not then survive to any other ending, because every open
  question held the engagement short of rest. A **standing ask** can (§3 rule 4a), and the honest
  closure for one nobody replied to is the same one — no reply arrived, and the empty `## Answer`
  is the evidence. What distinguishes E4 from E3 is not this status appearing anywhere in the
  engagement; it is the **sign-off's** status and the waiting log's trailing run
  (`ids-and-statuses.md` §3.5a, ADR-0012 §4.1).
- **It is not open.** `next` does not stop on it, the orchestrator does not re-ask it, and no item
  resumes on the strength of it. It settled nothing, so no skill may cite it as a basis for a
  decision.
- **Outside E4 by silence, the record must show it was asked.** An abandoned elicitation
  satisfies Definition of Done DE8 at an ordinary ending only where the waiting log names it in a
  halt's `surfaced` column — `scripts/check-epic-signoff` reads it. Filing an elicitation and
  closing it in the same execution shows nobody anything, and that route exists (`review-close`
  may file one alongside the sign-off), so the evidence is asked for rather than assumed.

**What may and may not be done with it afterwards.** Never edit it: the general rule that a
question is never deleted and its `status` never reverted (§3, rule 6) applies here with no
exception, and it matters more here than anywhere else, because the empty `## Answer` is the whole
record of what happened. In particular, a stakeholder who comes back does **not** answer an
abandoned question — reopening the engagement is done through `tracker/requests/`, which returns
the epic `done → open` (`ids-and-statuses.md` §3.4), and the thing they need to be asked is filed
as a **new** question that cites this one. An abandoned question may be quoted, cited and counted;
it may not be revived.

An abandoned **sign-off** is the one abandonment with a further consequence, and it is what
distinguishes E4 from E3 in the record: `status: abandoned` with an empty `## Answer`, against
E3's `answered` or `deferred` with the stakeholder's words in it verbatim
(`ids-and-statuses.md` §3.5a). It does not satisfy DE7's *asked and answered* form; what it
satisfies is DE7's E4 form, *asked, and the ask stood unanswered for the threshold*
(`dor-dod.md` §4).

### `## Cross-answer check` — the section that stops a contradiction being settled privately

A stakeholder's answers are requirements, not document content. Two of them can contradict each
other, and when they do, the person who wrote both is the only one who can say which wins.

Iteration 3 is the whole argument. Part one, at refinement: *"The alignment marker decides
everything. Whatever the marker says, that's where the text sits in the cell — every row, every
column, no exceptions."* Part two, five turns later, as the condition on a sign-off: *"a cell
with a line break … should just sit top-left, plain, whatever the column marker says."* The
contradiction was **detected twice** — D12 found the earlier sentence, quoted with its citation,
now false in two documents — and repaired both times by rewriting the document. The stakeholder
had a one-sentence reconciliation ready the whole engagement and was never asked for it:
*"They fixed it as a problem with their document, not as a question for me. I would rather have
been asked"* (F-062, derived in `meta/adr/ADR-0008-cross-answer-consistency.md`).

So every human answer, at the moment a skill **consumes** it, records what it was checked
against:

```markdown
## Cross-answer check

Checked against: WI-0002/Q-001; WI-0002/Q-002.

- `WI-0002/Q-001` — **conflicts**: it says the marker decides "every row, every column, no
  exceptions"; this answer exempts a whole class of cell. Escalated as `WI-0004/Q-005`, which
  quotes both and asks which wins.
- `WI-0002/Q-002` — compatible: it is about column width, not about where text sits.
```

Rules:

- The section is REQUIRED on every question with `answered-by: human` that has reached
  `status: answered`. It is written by the skill that consumes the answer — the human writes
  `## Answer` and nothing else — so a reply sitting in the file before anything has read it is
  not a defect.
- `Checked against:` names the prior recorded human answers by ID, or `none` **with the reason**.
  `none` is a real result and the commonest one; what is not allowed is silence.
- Every named ID MUST resolve to a human answer in this workspace, and MUST carry a verdict:
  `compatible` (with why) or `conflicts`.
- A verdict of `conflicts` MUST be matched by a question addressed to `human` that **quotes both
  answers by ID** and asks which wins. Recording a conflict and then deciding it is the move
  ADR-0008 §3 refuses.
- Which prior answers belong in the list is the acting skill's judgement, and the ADR says so
  rather than pretending otherwise: a citation-graph topic key was measured against iteration 3's
  real record and produced 58 candidate pairs in a four-item engagement. What is mechanical is
  that the check happened, that its IDs resolve, and that a declared conflict was escalated.

`scripts/lint-answers` enforces all of the above. It also enforces the other half, over a diff:
**a claim in `docs/` sourced to a human answer may not be rewritten by the execution that
overtakes it.** If the sentence is false because the pipeline paraphrased badly, or because the
code changed, correcting it is an ordinary D12 repair and always was. If it is false because the
person has since said something incompatible, the document is not the thing that is wrong.

### `Under delegation:` — the answer that covers a whole category

A stakeholder who says *"you decide the technical details"* has answered a **category**, not a
question. That is a real answer and this protocol treats it as one: the skill decides inside the
category rather than asking again, because asking anyway tells them their answer was not heard.
What the protocol had no way to record is how far the licence was taken to reach. In one
engagement two such answers carried **38** `[assumed]` decisions across four items — among them
what happens to a file the tool does not recognise, and whether one broken rule file stops every
run — and exactly one of the 38 ever reached the person who gave the licence, because a reviewer
chose to put it in a sign-off (F-082).

So a decision taken under a delegation says so, in one line, beside the decision:

```markdown
**Under delegation:** WI-0001/Q-002 — output wording, exit codes and file layout.
```

- The ID is the recorded human answer that granted the licence: a question with
  `answered-by: human` — `answered` or `deferred`, since a deferral is a reply (§3 rule 7) — or a
  `tracker/requests/R-nnn.md`. It MUST resolve. A licence with no route back to whoever gave it
  is the whole of what the finding names.
- After it, **the category the licence is being taken to cover**, in words, so that its scope is
  something the record holds rather than something each later execution re-derives privately.
- It lives wherever the decision is recorded: in `artifacts/refinement-qa.md` beside the
  `[assumed]` tag, in `artifacts/plan.md` under `## Assumptions`, in the item's `## Notes` where
  the assumption is carried there. It may be a line of its own or a line under the assumption it
  belongs to; both are read.
- The **sign-off names every answer spent under** (below). That is the half that closes the loop:
  the person who wrote the blank cheque sees what was spent before they accept.

`scripts/lint-answers` reads the line — that the ID resolves, that a category is named, and at an
ending that every ID so spent is in front of its author. It cannot read whether the delegation
really reaches the decision taken under it, and it cannot see a delegation relied on and never
written down at all. Both are judgement, both are the acting skill's, and `dor-dod.md` R12 is
where that is written down as such rather than left to be inferred from a gate's silence.

### `kind: elicitation` — the one question that is not about our agenda

Every other question in this protocol is closed-form and comes from the team's list of things it
needs to know. That is correct and it has a blind spot the size of the product. Iteration 3's
stakeholder, in their closing note: *"What I never got asked about was anything I would have
thought to say myself."* Two real wants — a maximum column width, and trailing whitespace — sat
in that persona for the whole engagement, and no question ever created a vehicle for them
(F-064). It is the same structural gap `request.md` closed for mid-epic input, one layer earlier:
the stakeholder had somewhere to speak unprompted, and was never *asked* to.

An **elicitation** question is the vehicle. One per engagement, at least.

- `addressed-to` MUST be `human`; `blocking` MUST be `false`. It must not stop the loop — it is
  not a thing anyone is waiting on — and it must not be answered by anybody else. That sentence
  is now what executes: it is a **standing ask** (§3 rule 4a), so it is surfaced at every halt
  and causes none, and it holds neither the loop nor rest. It did not execute for its first three
  weeks — `next` stopped on any open human-addressed question and rest was held by any open
  question at all, so the one question declared to be nobody's to wait on put every ending out of
  reach, E1 included (F-104, ADR-0012).
- It is exempt from the two-options rule, and from it alone. *"What else matters to you here that
  we have not asked about?"* is not a choice between options and inventing two would defeat it.
  Every other body rule applies, including one topic per question and a place to write the answer.
- `intake` files it at the start of an engagement, where the answers are cheapest to act on, or
  `refine` files it on an item. If the engagement reaches rest without one, `review-close` files
  it alongside the sign-off. That last route exists so the rule cannot deadlock an engagement
  that forgot it — but an elicitation asked at the ending is worth much less than one asked at
  the beginning, and the record shows which happened.
- The answer is routed like any other: it becomes an item, a criterion, a `## Notes` entry, or an
  explicit "nothing to add" — and `## Consequences` says which, naming files.

`scripts/check-epic-signoff` enforces presence at the ending (`dor-dod.md` DE8): an engagement
does not end without at least one elicitation question, created no later than the sign-off
it is being asked alongside.

### `kind: sign-off` — the termination question

Almost every question is a `decision`: something the pipeline cannot settle by itself. One is
not. A **sign-off** is the moment the stakeholder is told what happened and asked whether they
accept it, and it is filed by `review-close` when the engagement reaches **rest** — before the
epic may reach *any* of its endings, not only closure (`ids-and-statuses.md` §3.5,
`dor-dod.md` DE7).

It obeys every rule above and adds six:

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
  only "yes" is theatre. **Accept-with-follow-ups carries the consequence it actually has**: the
  epic stays `open`, the follow-up is built like any other item, and a fresh sign-off is due at
  the next rest — never *"the engagement still closes as delivered, and the new work is opened"*,
  which a real sign-off printed, which this protocol's own status model forbids (an engagement
  ends only from rest, rest requires every child terminal, and the follow-up is created at
  `draft`), and which cost the stakeholder a second full cycle they had chosen the option to
  avoid: *"more process than I expected for one follow-up request"* (F-061).
- `## Question` MUST also name **every delegation this engagement spent**: each answer ID that
  an `**Under delegation:**` line cites, the category it was taken to cover, and the assumptions
  taken under it. Naming the IDs is the checkable half, for the same reason naming every child is
  — *"list what we assumed on your behalf"* cannot be checked and *"name every answer we spent"*
  can — and whether the assumptions listed beside them are the ones actually taken is the
  reviewer's. At E4 there is no sign-off and the same list goes into `artifacts/review.md`'s
  `## Ending statement`, which is where an ending's statement lives when there is nobody to
  address (§2, `ids-and-statuses.md` §3.5a). A stakeholder whose two answers carried 38
  assumptions was shown one of them (F-082).
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
3. **The orchestrator will not advance an item while a blocking question on it is open.** It
   will advance every **other** item, and a question addressed to the human is no exception —
   what a blocking question suspends is its own item. A skill that learns something invalidating
   a *different* item files a blocking question on that item; nothing else stops it.
4. **An outstanding ask stops the autonomous loop.** An **outstanding ask** is a question that is
   `addressed-to: human`, `status: open`, `blocking: true`, and whose `## Answer` is still empty:
   the pipeline is waiting on a person and cannot go on without them. The orchestrator records
   the halt on the engagement's waiting log, surfaces every open human-addressed question and
   stops; there is nothing else it can legitimately do — with one exception, and it is still not
   the orchestrator deciding anything. Where the halt is the one at which
   `scripts/engagement-state` reports `abandoned`, the orchestrator dispatches `review-close` on
   that epic instead of surfacing, and stops (`ids-and-statuses.md` §3.5a).

   It stops there **last**. The halt sits below every step that dispatches work, so the loop lets
   each runnable item state its own questions before it comes to the person, and one round trip
   carries them all instead of one per item (F-097, ADR-0012 §2).

4a. **A standing ask stops nothing.** A **standing ask** is `addressed-to: human`, `open`,
   `blocking: false`, with no reply — the elicitation is the one every engagement carries. It is
   surfaced at every halt, so the person sees it as often as anything else; it causes no halt,
   accrues no silent round, and does not hold the engagement short of rest. At the ending, one
   still unanswered is closed `abandoned` by `review-close` (§2).

4b. **A reply is not a reason to stop.** A question `addressed-to: human` whose `## Answer` has
   been filled in is **answerable**, not outstanding: `answer-questions` is dispatched to
   propagate it. The orchestrator once stopped on those too and showed the person the answer they
   had just written (F-011, F-109).
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
8. **Silence is not a reply, and it is recorded as such.** A question addressed to `human` that
   is never answered is closed `abandoned` by `review-close` when it declares E4, with an empty
   `## Answer` (§2). Nobody else may set it, it is set for no other reason, and it is set only on
   questions that were still `open` at the declaration — an already-`answered` or `deferred`
   question is untouched by the ending.

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
| 7 | 2026-08-29 | §2: `## Cross-answer check` — a consumed human answer records what it was checked against, and a declared conflict is put to its author rather than settled in a document (F-062). Derived in ADR-0008. |
| 8 | 2026-08-29 | §2: options before the recommendation, and the recommendation marked as ours (F-063); `kind: elicitation`, the one open question per engagement that is not about the team's agenda (F-064). |
| 9 | 2026-09-10 | §2: `status: abandoned` — the fourth question status, and the pipeline's only vocabulary for **absence**. `## Answer` MUST be empty, `## Consequences` names the ending and the item's orphan class, `answered-at`/`answered-by` stay unset, and only `review-close` sets it, only at E4. §3: rule 4 gains the orchestrator's `abandoned` branch, and new rule 8. Derived in ADR-0011 (F-060, F-028, H-008). |
| 10 | 2026-09-10 | §2: `kind: sign-off`'s accept-with-follow-ups option states the consequence it actually has — the epic stays `open`, the follow-up is built, a fresh sign-off follows — rather than an ending the status model forbids (F-061). |
| 11 | 2026-09-10 | §2: `**Under delegation:**` — a decision taken under a stakeholder's category answer names the answer that granted it and the category it is taken to cover, and the sign-off names every answer so spent (F-082). |
| 12 | 2026-09-10 | §2/§3: **which questions stop the loop.** An **outstanding ask** — `addressed-to: human`, `open`, `blocking: true`, `## Answer` empty — halts the orchestrator, and it halts last, below every dispatching step (F-097). A **standing ask** is surfaced and stops nothing, so the elicitation's own `blocking: false` finally executes (F-104); a question carrying a reply is answerable rather than a reason to stop (F-011, F-109). `status: abandoned` is set by `review-close` at **any** ending, not only E4, and outside E4 the waiting log must show the question was surfaced. Derived in ADR-0012. |
