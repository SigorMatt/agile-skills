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
| D7 | Documents the change invalidated have been updated, with a version bump and a change-log row | [skill] |
| D8 | Every commit on the branch references the item ID, so `git log --grep <ID>` reconstructs the item's code history | [auto] |
| D9 | The change is merged into the trunk, and the branch's work is not left only on the branch | [auto] |
| D10 | `verify` ran **after** the last code change. A verification older than the code it verifies does not count | [auto] |
| D11 | The review record exists at `artifacts/review.md` and states what was examined, not only the verdict | [skill] |
| D12 | Every claim in `docs/` about the behaviour this item touched is **still true**, checked by reading it against the code — not by remembering whether this change invalidated it. Absolute claims this execution wrote carry a resolvable citation (`doc-header.md` §4a) | [skill] + [auto] |

### D12 exists because D7 was not enough

D7 asks whether *this* change invalidated a document. Nothing asked whether something written
three items ago is still true. An independent audit of a real run found the consequence: a
factually wrong justification for a decision reached two comments in shipped source, an ADR and
an architecture overview — and then, after the audit raised it, **spread to a seventh document**,
because every skill that touched the area re-quoted the sentence rather than re-checking it.
Every machine-decidable gate held throughout; every gate resting on a human-style read did not.

D12 is scoped deliberately — the behaviour *this item touched*, not all of `docs/` — so it is a
real read of a few paragraphs rather than a ritual nobody performs.

**The half of D12 that is now a program.** The read itself cannot be automated; what can be, and
now is, is the demand that the confident sentences point at something. `doc-header.md` §4a
requires an absolute claim about named code to carry a citation, and requires every citation to
resolve; `scripts/lint-claims` is a hard gate on `plan`, `implement` and `review-close`. That
does not make the claim true — it makes it *checkable in one hop*, by a reader who does not have
to reconstruct where the sentence came from. The sentence that propagated through seven documents
would have carried, from its first appearance, a pointer to the code it was wrong about.

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
| DE4 | `docs/product/` reflects what was actually built, not what was proposed | [skill] |
| DE5 | Open questions across all child items are closed, or re-filed against a follow-up item | [auto] |
| DE6 | Every claim in `docs/` about behaviour this epic delivered has been checked against the code **during this epic**, not merely at the moment it was written. Every citation in the workspace resolves | [skill] + [auto] |
| DE7 | The stakeholder was **asked** whether they accept the engagement as it stands, after it reached rest, and answered — in **every** ending, not only closure | [auto] |
| DE8 | The stakeholder was asked, at least once in this engagement, an **open** question that was not about the team's agenda — a `kind: elicitation` question (`question.md` §2) — and it was answered | [auto] |

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
