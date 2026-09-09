# Definition of Ready and Definition of Done

Two checklists, each a gate on a status transition:

- **Definition of Ready (DoR)** gates `draft → ready`. `refine` owns it.
- **Definition of Done (DoD)** gates `in-review → done`. `review-close` owns it.

Every criterion is marked with how it is checked:

- **[auto]** — `scripts/validate-workspace` decides it. An agent's opinion is irrelevant.
- **[skill]** — the owning skill decides it, and MUST record the evidence in its journal entry
  under `**Gates:**`. "I checked" is not evidence; the quoted criterion and why it holds is.

A checklist result MUST be recorded criterion by criterion, not as a single verdict. A skill
that writes "DoR passed" without the per-criterion record has not applied the checklist, and a
reviewer cannot tell which criterion was the weak one.

---

## 1. Definition of Ready — `work-item`

| # | Criterion | Check |
|---|-----------|-------|
| R1 | `item.md` has all required frontmatter, and `type`, `epic` and `priority` are set | [auto] |
| R2 | `## Story` names a role, a capability, and an outcome ("so that …") | [skill] |
| R3 | At least one acceptance criterion exists, labelled `AC<n>`, as a checkbox | [auto] |
| R4 | **Every** acceptance criterion is decidable by observation — a command to run, an output to inspect, a file to check. No criterion contains an unmeasurable adjective ("fast", "clean", "user-friendly") without a stated threshold | [skill] |
| R5 | `## Out of scope` names at least one thing a reader could reasonably assume is included | [skill] |
| R6 | Every open question on this item is non-blocking | [auto] |
| R7 | The item is independently deliverable: nothing in `depends-on` is unfinished, or the dependency is recorded and the item is sequenced after it | [auto] |
| R8 | The refinement Q&A is recorded verbatim in `artifacts/refinement-qa.md`, including which answers came from the human and which were assumed, and that file declares `status: recorded` — an agenda for a conversation that has not happened yet does not satisfy this | [auto] |
| R9 | Estimated to be deliverable as one coherent change. If it is not, it was split, and this item is one of the parts | [skill] |
| R10 | Every combination of the behaviours this item introduces — its options, its flags, its modes — either has a stated behaviour in a criterion, or is named in `## Out of scope`, or is recorded in `## Notes` as deliberately unconstrained with who left it so | [skill] |

R10 was added after a real run found the checklist could not express what was wrong. An item
specified `--sort`, an earlier item had specified `--top`, and nothing anywhere said what the two
did *together*. Every other criterion passed: each individual criterion was decidable, the story
was complete, the scope was stated. `refine` correctly refused to record a Definition of Ready
override, because naming a criterion that was not failing would have been a false entry — and it
was right that none was failing. The gap was in the checklist. R10 does not force the
combination to be *decided*; it forces it to be **visible**, which is the difference between an
open question someone can find and one nobody knows exists.

### The override

The human MAY override DoR and force an item to `ready`. When they do:

- `refine` records the override in `artifacts/refinement-qa.md` under `## Override`, naming
  **which criteria** were not met and the human's stated reason.
- The history row's `reason` MUST begin with `DoR overridden:`.
- The item's `## Notes` MUST carry the unmet criteria, so `plan` and `implement` see the risk
  they inherited rather than discovering it.

An override is legitimate and expected sometimes. Silently passing an item that does not meet
the checklist is not, and is the thing this section exists to make impossible to do quietly.

---

## 2. Definition of Ready — `bug`

A bug enters at `ready`, so `verify` (or whoever files it) applies this checklist at filing
time and records the result in the filing journal entry.

| # | Criterion | Check |
|---|-----------|-------|
| RB1 | `## Steps to reproduce` is a numbered list runnable without further questions | [skill] |
| RB2 | `## Actual behaviour` quotes real output — command, output, exit code — not a paraphrase | [skill] |
| RB3 | `## Expected behaviour` cites the acceptance criterion, doc, or ADR it contradicts | [skill] |
| RB4 | `found-in` names the item that delivered the behaviour, when it is known | [auto] |
| RB5 | Acceptance criteria include a regression test, or `## Notes` records why one is impossible | [skill] |

---

## 3. Definition of Done — `work-item` and `bug`

| # | Criterion | Check |
|---|-----------|-------|
| D1 | Every acceptance criterion checkbox in `item.md` is ticked | [auto] |
| D2 | Every ticked criterion cites its evidence in `artifacts/verify-report.md` | [skill] |
| D3 | All of the item's declared quality gates passed on the final state of the code, not on an earlier one | [skill] |
| D4 | No open blocking question remains on the item | [auto] |
| D5 | `journal.md` has an entry for every skill execution, and `history.md` chains without a gap to the current status | [auto] |
| D6 | Every decision that changed the design is in an ADR, and the ADR is cited from the plan or journal | [skill] |
| D7 | Every entry in the plan's **invalidation set** carries a disposition, and every entry disposed `to-update` was updated, with a version bump and a change-log row. Plus the one question the set cannot answer for itself: did this change falsify a document the set does not name? The scope is what this change **touched or its plan named** — engagement-state sentences excluded, they are the ending's (DE4) | [skill] + [auto] |
| D8 | Every commit on the branch references the item ID, so `git log --grep <ID>` reconstructs the item's code history | [auto] |
| D9 | The change is merged into the trunk, and the branch's work is not left only on the branch | [auto] |
| D10 | `verify` ran **after** the last code change. A verification older than the code it verifies does not count | [auto] |
| D11 | The review record exists at `artifacts/review.md` and states what was examined, not only the verdict | [skill] |
| D12 | Every claim in `docs/` about the behaviour this item touched is **still true**, checked by reading it against the code — not by remembering whether this change invalidated it. Absolute claims this execution wrote carry a resolvable citation, and every **quantified** claim it audited carries, in its audit row, the set, how the set was enumerated with the command's output, the members by name, and a verdict per member — opening what the claim cites does not discharge it (`doc-header.md` §4a). **Engagement-state sentences are out of scope**: no item audit is charged with one | [skill] + [auto] |
| D13 | The plan's `binding-adrs` list is **complete** — the change engages no ADR the list does not name. Whether the change *conforms* to each listed ADR is `verify`'s verdict in `artifacts/verify-report.md`, not this criterion's | [skill] |

### D7 confirms against a set; it does not discover

D7 used to be scoped to what the execution *touched*. "Touched" is a diff, and every piece of
document machinery here is built on one — `--changed-since`, D12's scoping, `lint-claims`'s
window — so a document the branch never opens is invisible to all of it, and the first person to
ask about it was `review-close`, at the last gate, after `implement` and `verify` had both
passed. Two items in one banked engagement were sent back and cleared by editing documents only,
with no code change in either (F-087). In the sharper of the two, the plan had learned from its
predecessor and carried a step for the architecture overview, `implement` executed it faithfully,
and the document that failed was the product vision, which no step named.

"What does this change make false?" is answerable only by someone who knows what the change does,
and it is a design output rather than a check: it is the same act as "which documents constrain
this change", which `plan` already performs. So the **invalidation set** is a table in
`artifacts/plan.md` — one row per document at risk, with the sentence or section located
precisely enough to reopen, its claim kind (`doc-header.md` §4a), why this change would falsify
it, and a `disposition` of `to-update`, `verified-still-true`, `owned-by-ending` or
`question-filed:<ITEM>/Q-###`. Beside it the plan carries `deliverable-documents` (documents this
item is *asked* to produce or change, because a criterion is about them) and `binding-adrs` (D13).

`plan` emits the set, `implement` discharges every entry and may add entries — it is the actor
that discovers mid-change that a fourth document was falsified — `verify` checks that every entry
has a disposition and that the `verified-still-true` ones are true, and D7 **confirms**. The
"nothing else was falsified" answer is now a claim against an enumerated set, attributable to
whoever made it, rather than a memory. That every entry carries a disposition is a shape a script
decides; whether the set is **complete** is not, and never was — what changed is who is on the
hook and what they are answering against.

### D12 exists because D7 was not enough

D7 asks whether *this* change invalidated a document. Nothing asked whether something written
three items ago is still true. An independent audit of a real run found the consequence: a
factually wrong justification for a decision reached two comments in shipped source, an ADR and
an architecture overview — and then, after the audit raised it, **spread to a seventh document**,
because every skill that touched the area re-quoted the sentence rather than re-checking it.
Every machine-decidable gate held throughout; every gate resting on a human-style read did not.

D12 is scoped deliberately — the behaviour *this item touched*, not all of `docs/` — so it is a
real read of a few paragraphs rather than a ritual nobody performs.

Two things are outside it. A **quantified** claim is not discharged by opening what it cites: the
citation names the general case and the falsifier is a member the sentence does not name, so the
audit row carries the enumeration instead (`doc-header.md` §4a). And an **engagement-state**
sentence is not D12's at all — nothing an item does makes it true or false, so an item that fails
D12 on one has been handed a defect it is structurally unable to fix. DE4 owns those (F-093,
F-095).

**The half of D12 that is now a program.** The read itself cannot be automated; what can be, and
now is, is the demand that the confident sentences point at something. `doc-header.md` §4a
requires an absolute claim about named code to carry a citation, and requires every citation to
resolve; `scripts/lint-claims` is a hard gate on `plan`, `implement` and `review-close`. That
does not make the claim true — it makes it *checkable in one hop*, by a reader who does not have
to reconstruct where the sentence came from. The sentence that propagated through seven documents
would have carried, from its first appearance, a pointer to the code it was wrong about.

### D13 asks whether the list is complete, not whether the change conforms

D6 asks that *new* decisions become ADRs. Nothing asked whether a change obeys the ADRs that
already exist, and the same ADR was broken twice, four items apart, each time caught only because
a reviewer happened to read the diff against it (F-092). The fix is split in two, deliberately.

`verify` decides **conformance**: for every ID in the plan's `binding-adrs`, `verify-report.md`
carries a row with a verdict of `conforms`, `violates` or `not-engaged`; a `conforms` verdict
quotes the clause of that ADR's `## Decision` it conforms to and names the file and line that
satisfies it; `not-engaged` is legal and says why the change does not touch the decision's
subject; `violates` is a send-back. That belongs to `verify` because judging a change against a
standard it did not write is `verify`'s whole contract, and because putting it at the close moves
the read one stage further from the person who could act on it.

D13 is the other half and the cheap one: did the plan name every ADR the change engages? Nothing
can decide that mechanically — it is the same shape as D7's closing question — and it is the half
that catches a plan which listed nothing at all.

### D3 and D10 are the two that get skipped

Both fail the same way: something is re-touched after the check, and the check is not re-run
because "it was only a small fix". D10 is machine-checkable — compare the verify report's
timestamp against the last commit on the branch — and `review-close` MUST perform that
comparison rather than assume. When it fails, the item goes back to `verifying`; it does not go
to `done` with a note.

---

## 4. Definition of Done — `epic`

| # | Criterion | Check |
|---|-----------|-------|
| DE1 | Every child item is at a **terminal** status (`done` or `blocked`), and every child that was not delivered is named in the termination question and in the epic's outcome | [auto] |
| DE2 | Every child item's `outcome` is recorded; dropped items say why in their `## Notes` | [auto] |
| DE3 | The epic's `## Success measures` are each addressed — met, or explicitly not met with the reason | [skill] |
| DE4 | `docs/product/` reflects what was actually built, not what was proposed. And the ending has restated **every** `## Engagement state` section in the workspace — all of them, not the ones it noticed — written **after the ending is determined**, because what is now true about the engagement is not settled until then (`doc-header.md` §4a) | [skill] + [auto] |
| DE5 | Open questions across all child items are closed, or re-filed against a follow-up item | [auto] |
| DE6 | Every claim in `docs/` about behaviour this epic delivered has been checked against the code **during this epic**, not merely at the moment it was written, each quantified claim by the enumeration its audit row owes rather than by opening what it cites (`doc-header.md` §4a). Every citation in the workspace resolves. **Engagement-state sentences are out of scope**: DE4 owns them | [skill] + [auto] |
| DE7 | The stakeholder was **asked** whether they accept the engagement as it stands, after it reached rest, and **answered** — in **every** ending, not only closure. At **E4 by silence** the form is *asked, and the ask stood unanswered for the threshold*: there is an ask addressed to the human, it was open across `termination.silence.threshold_rounds` silent rounds, and the waiting log shows them (`ids-and-statuses.md` §3.5a) | [auto] |
| DE8 | The stakeholder was asked, at least once in this engagement, an **open** question that was not about the team's agenda — a `kind: elicitation` question (`question.md` §2) — and it was **answered**. At **E4 by silence** the elicitation may end `abandoned` with an empty `## Answer`; the criterion is then that it was asked and went unanswered, never that it was skipped | [auto] |

### DE1 was an entry condition for one ending out of four

"Every child item is `done`" describes ending **E1** and nothing else. E2 (delivered-partial),
E3 (impasse) and E4 (abandoned) all end legitimately with at least one child not `done`
(`ids-and-statuses.md` §3.5), and a criterion that only E1 can satisfy is why the epic in a real
run sat `open` for ever with a `blocked` child, never reaching the gate that would have asked
the stakeholder anything (F-045).

What generalises is **terminal, and named**: every child has stopped, and every child that did
not deliver appears by ID in the termination question and in what the epic records as its
outcome. That is strictly stronger than the rule it replaces — DE1 never required anyone to say
*which* children delivered — and it is what makes F-046 mechanical. A bug the pipeline filed and
never fixed is a child of the epic, so it is named, so the stakeholder sees it. "List what was
not delivered" cannot be checked; "name every child" can.

An epic that closes with an undelivered child MUST carry `outcome: delivered-partial` or
`dropped`. Closing one as `delivered` is overclaiming and the validator refuses it.

DE6 is the epic-level counterpart of D12, and it is where a claim that no single item touched
gets caught. Treat it the way a regression pass treats behaviour: the run that found three real
defects in delivered code existed because someone re-checked behaviour nobody had changed. Prose
deserves the same, and in the run that produced this rule, every uncorrected finding lived in
prose.

DE3 is the criterion that stops a pipeline from mistaking "all the tickets are closed" for
"the goal was achieved". If a success measure was not met, closing the epic is still allowed —
saying so is what is mandatory.

### A criterion about other criteria is read against their text

`WI-0004`'s AC5 in a real run: *"every acceptance criterion of WI-0001..0003 still holds, named
tests pass unmodified."* It passed. The reasoning recorded for it was that no test and no fixture
contains a `<br>`, so nothing executable exercises both the old rule and the new exception — and
that is true, and it is not what the criterion says. On the page, the criteria contradicted each
other: one said the alignment marker governs *"every row, every column, no exceptions"*, the new
one exempted a class of cell. A coverage gap laundered a semantic conflict (F-065).

So a criterion of that shape — one whose subject is other criteria rather than behaviour — is
assessed like this, and `verify` records it this way:

1. **Name them.** The criteria it covers are listed by ID (`WI-0001 AC3`, not "the earlier
   criteria"). A criterion that cannot name its own subject is not decidable and R4 already
   refuses it.
2. **Read each one's text against the new behaviour** and say, per criterion, whether the
   sentence is still true. This is the assessment. It is a read, and it is the thing the
   criterion actually asks for.
3. **Run the tests as evidence *for* that answer, never as its definition.** "The suite is green"
   answers a different question, and answering the easier question is how this criterion fails.
4. **State non-intersection when it exists.** If nothing executable exercises the old criterion
   and the new behaviour together, say so in those words, and then either add a case that does,
   or waive it **by name** — which criterion, and why a covering case is not worth writing. A
   waiver somebody signed is a decision; an unremarked gap is a hole.

If step 2 finds that a criterion's sentence is no longer true, that is not a criterion to
rewrite. It is a contradiction between what was agreed then and what is being built now, and
`ADR-0008` says where it goes: cite compatibility, or ask the person who agreed to both.

### DE7 is about asking, not about being told yes — in every ending

DE3 and DE4 both ask whether the record says the goal was met. DE7 asks something the record
cannot answer on its own: whether the person who wanted it agrees. A record only holds what the
stakeholder said when last consulted, so an epic can satisfy every other criterion while nobody
has spoken to them since refinement — which is what happened, twice, in consecutive runs.

**DE7 is a termination criterion, not a completion criterion.** It was written as the latter and
the difference cost a whole run: the gate fired on `open → done`, an epic with a `blocked` child
never reaches `done`, and so the one ending where the stakeholder most needed to speak was the
one ending that never asked them (F-045). The stakeholder in that run went looking for the
question and recorded that it never came.

So the trigger is **rest**, not closure (`ids-and-statuses.md` §3.5): every child terminal, no
question open anywhere in the engagement, no request open. At rest, `review-close` files a
`kind: sign-off` question on the epic (`question.md` §2), suspends the epic to
`awaiting-answer`, and stops. `scripts/check-epic-signoff` is the gate; it requires the
acknowledgment to have been filed **after the engagement reached rest** — an acceptance obtained
halfway through is an acceptance of something else — and it requires the question to **name
every child item**, so that what was not delivered is in front of the stakeholder rather than
implied by its absence.

A "no" ends the engagement just as legitimately as a "yes": the epic goes to `blocked` with the
impasse recorded (E3), or closes with an outcome that says what was and was not delivered. The
criterion is that the question was asked and answered, never that the answer was favourable.

### DE7 and DE8 at E4 by silence: asked, not answered

*Asked and answered* holds for E1, E2, E3 and E4 by withdrawal. At **E4 by silence** the second
half cannot hold by construction: the ending exists precisely because no answer came
(`ids-and-statuses.md` §3.5a). So for that one ending the honest form of DE7 is **asked, and the
ask stood unanswered for the threshold** — there was a question addressed to the human, it was
open across `termination.silence.threshold_rounds` silent rounds, and the waiting log records
each of them. DE8's elicitation may likewise end `abandoned` with an empty `## Answer`.

This is a weakening of the criterion that exists because two consecutive runs closed an epic
without asking anyone (F-022), so it deserves the suspicion it will get. Three things bound it,
and they are stated here rather than assumed:

- **E4 is the only ending where it is relaxed.** Every other ending still requires a reply.
- **The relaxation is decided by the pending move**, not by the skill's account of itself — the
  same arrangement by which `--resolving` already decides the deferral branch (F-033).
- **The gate still requires an ask to have existed and to have gone unanswered for the full
  count.** "Nobody was asked" fails DE7 at E4 exactly as it fails it everywhere else; what E4
  permits is an ask with an empty `## Answer`, never a missing ask.

What replaces the answer in the record is not nothing: it is the `## Ending statement`, which
says to a reader what the sign-off would have said to the stakeholder — the goal in their terms,
every child by ID with its class, the rounds and what was surfaced on each, and each success
measure met or not met.

**DE4's trigger changes with it.** ADR-0010 §4.3 set it as *after the sign-off answer arrived*,
because the answer is itself part of the engagement's state. At E4 no answer arrives, so a
trigger that waits for one can never fire and DE4 would be unsatisfiable in the ending that most
needs restating. The trigger is therefore **after the ending is determined** — which is the same
moment in E1, E2, E3 and E4 by withdrawal, since the answer is what determines those endings, and
is a moment that exists at E4 by silence. **This amends ADR-0010 §4.3**, and is recorded here
rather than left for the two ADRs to disagree about quietly: ADR-0011 §2.4 is the amending
derivation, and where the two texts differ ADR-0011's is the later and governing one.

---

## Revisions

| # | Date | Change |
|---|------|--------|
| 1 | 2026-08-17 | Initial. |
| 2 | 2026-08-22 | D12 and DE6 gain their mechanical half: claim provenance, enforced by `scripts/lint-claims` (F-001). |
| 3 | 2026-08-22 | DE7 added: the stakeholder is asked to accept the epic, after the last child closed, and answers (F-022). |
| 4 | 2026-08-27 | R8 reads `refinement-qa.md`'s `status` field rather than the filename: an `[auto]` check that only tests existence is trusted and wrong (F-031). |
| 5 | 2026-08-27 | DE1 generalised from "every child `done`" to "every child terminal, and every undelivered child named" (F-045, F-046); DE7 generalised from a completion gate to a **termination** gate, triggered by rest. Derived in ADR-0006. |
| 6 | 2026-08-29 | A criterion whose subject is other criteria is read against their **text**, with the suite as evidence rather than as the definition, and non-intersection stated or waived by name (F-065). DE8 added: an engagement is asked at least one open question that is not about the team's agenda (F-064). |
| 7 | 2026-09-10 | D7 becomes a **confirmation** against the invalidation set `plan` emits: every entry disposed, plus "did this change falsify a document the set does not name?", scoped to what the change touched **or its plan named** (F-087). D12 and DE6 gain the member enumeration a **quantified** claim owes and exclude **engagement-state** sentences; DE4 gains the ending's restatement of every delimited `## Engagement state` section, after the sign-off answer (F-095, F-093). D13 added: the plan's `binding-adrs` list is complete, `review-close`'s to check, each ADR's conformance verdict `verify`'s to decide (F-092). Derived in ADR-0010. |
| 8 | 2026-09-10 | DE7 and DE8 gain their **E4 by silence** form — *asked, and the ask stood unanswered for the threshold* — the one ending where *answered* cannot hold, bounded by three named compensating controls. **DE4's trigger is amended from *after the sign-off answer arrived* to *after the ending is determined***, because at E4 no answer arrives and the old trigger could never fire; **this amends ADR-0010 §4.3**, and ADR-0011 §2.4 is the governing derivation. Derived in ADR-0011 (F-060, F-022, F-033). |
