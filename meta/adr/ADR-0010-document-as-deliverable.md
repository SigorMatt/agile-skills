# ADR-0010 — Document-as-deliverable: what a document is, who may change it, and what makes a claim in it checked

- **Status:** accepted
- **Date:** 2026-09-10
- **Unit:** META-145
- **Amends:** `spec/doc-header.md` §5 — the absolute *"`implement` and `verify` do not write to
  `docs/`"* does not survive this derivation and is replaced by a rule scoped to the **record**
  half of `docs/` (§3, §6/F-076). Also amends `spec/dor-dod.md` D7, D12, DE4 and DE6, which are
  re-cut against the claim taxonomy (§4) and the invalidation set (§5).
- **Extends, does not supersede:** ADR-0006 (which enumerated *item* authority; this does the
  same for *documents*) and ADR-0008 (whose refused move survives intact and is strengthened —
  §3, the `human-answer` overlay).
- **Findings:** F-053 (as the lifecycle-state input), F-057, F-058, F-076, F-087, F-092, F-093,
  F-095. Touches F-001, F-024, F-066, F-067, F-069, F-098.

## Context

Eight findings, filed across five runs by four different actors, are one design debt. Every one
of them is a question about a document that the methodology answers by reaching for a rule about
`docs/` as a *place*, when the thing that decides the case is what the sentence is *about*.

| Finding | The contradiction, in one line |
|---------|-------------------------------|
| F-057 | `BUG-0001`'s acceptance criteria were criteria **about a document**, and `spec/doc-header.md` §5 leaves no skill the pipeline dispatches on `planned` or `in-progress` allowed to fix it. |
| F-058 | `check-verify-freshness` excludes everything under `docs/` from the "did code change after verification" comparison [src: scripts/check-verify-freshness], so on an item whose delivered change *is* a document, the gate excludes the thing that was delivered. |
| F-076 | `implement`'s hard `claims-are-sourced` gate is a window over the documents this branch changed [src: methodology/skills/implement/skill.yaml], and §5 forbids `implement` to put anything in it. The gate is empty **by construction**, on every execution, in every engagement. |
| F-087 | D7 asks what a change invalidated, and it is a `review-close` criterion [src: spec/dor-dod.md] — so the question "what does this change make false?" is first asked after `implement` and `verify` have both passed. Two items were sent back and cleared by editing documents only. |
| F-092 | The Definition of Done asks that *new* decisions become ADRs (D6) and nothing asks whether the change obeys the ADRs that already exist. The same ADR was broken twice, four items apart. |
| F-093 | The product vision said the stakeholder had not yet been asked to accept the engagement. The pipeline's own closing turn made that false, and the item that owned the document was closed by the same turn. `review-close` edited the document and recorded that *"there was no send-back available that would not have been a fiction"*. |
| F-095 | A claim of the form "every X does Y" is audited by opening what it cites; what it cites is the family's shared fixture; the member that falsifies it is not cited. The same universal was audited **true** three times and was false. |
| F-053 | (Contributing, not settled here.) `outcome` and `status: done` cannot both be written, in either order — a dependent field the transition mechanism does not model. Its *class* is the half-written record: a state that takes two writes and a tool that offers one. |

Read together they say three things the current rules do not.

**(a) `docs/` is not one kind of thing.** The specs treat it as *record* — a statement about what
happened or was decided, which later work does not falsify — because that is what `docs/` was
when it held only a vision and an overview. But a document can also be a **deliverable**: a
statement about the product, which the next change can make false, and which an item can be
asked to produce. F-057 and F-058 are the same case seen from the skill's side and the gate's
side, and both fail because a single rule about a *directory* is being asked to decide a question
about a *sentence*.

**(b) The pipeline asks what a change touched and never asks what it falsified.** "Touched" is a
diff and the machinery is built on it — `--changed-since`, D7's scoping, `lint-claims`'s window.
"Falsified" is not a diff, has no owner, and is first asked at the last gate (F-087). This is why
F-076's gate is not merely empty but *empty in the right direction*: it looks where the change is
and the damage is somewhere else.

**(c) Some sentences are not about the product at all.** "The stakeholder has not yet been asked
to accept this engagement" is a claim about the **engagement**, and the only act that falsifies it
is the pipeline's own ending (F-093). No item owns it, because by the time it is false every item
is closed.

The derivation below runs the other way round from the rules. It enumerates the document kinds
and the events that change them, reads the authority table off that enumeration, and then asks
what an audit obligation must be for each of the three things a claim can be about. Where the
enumeration and the current specs disagree, the specs are wrong and this ADR says which line.

Vocabulary, fixed here and used throughout:

- A **record** document is a statement about what happened or what was decided. Later work does
  not falsify it; later work can only *add* to it. Its correction rules are already written
  (`doc-header.md` §4, §4b).
- A **deliverable** document is a statement about the product as it now is. Later work **can**
  falsify it, and an item can be asked to produce or repair it.
- The two are properties of **sentences**, not of files. One file holds both, and `docs/product/
  vision.md` demonstrably holds three (§1).

---

## 1. The document kinds

Every kind of document this pipeline writes, as they exist in a workspace
[src: spec/workspace-layout.md]. `R` = record, `D` = deliverable, `R+D` = the file holds both and
the distinction runs through it sentence by sentence.

| # | Kind | Where it lives | Audience | R / D |
|---|------|----------------|----------|-------|
| K1 | **Product docs** | `docs/product/vision.md`, `docs/product/prd.md` | the stakeholder, and every later skill needing intent | **R+D** — "who this is for" is record; "the tool writes to `~/.local/share`" is deliverable |
| K2 | **Architecture overview** | `docs/architecture/overview.md` | `plan`, `implement`, a future maintainer | **D** — it describes the system as it now is, and every change can falsify it |
| K3 | **Consumer ADRs** | `docs/architecture/adr/ADR-####-<slug>.md` | whoever proposes to re-decide | **R** for the decision (superseded-only, §4); **D** for the document's own justifying clauses (§4b's `erratum`) |
| K4 | **Process docs** | `docs/process/ways-of-working.md` | the team, this engagement's skills | **R+D** — a convention adopted is record; a statement that a command exists is deliverable |
| K5 | **Item artifacts** | `tracker/items/<ID>/artifacts/{refinement-qa,plan,impl-report,verify-report,review,retro}.md` | the next stage, then the retro and the audit | **R** — each is what one execution claimed at one moment. Re-running a skill **overwrites its own** artifact [src: spec/workspace-layout.md]; nothing else may |
| K6 | **Journals and history** | `tracker/items/<ID>/{journal.md,history.md}` | the reviewer, the retro, the ledger | **R**, strictly append-only |
| K7 | **Questions** | `tracker/items/<ID>/questions/Q-###.md` | the answerer, then everyone | **R** for `## Context`/`## Question`/`## Answer`; the `## Answer` of a *human*-answered question is a requirement owned by a person (ADR-0008) and is not any skill's to revise |
| K8 | **Engagement-state sentences** | today: loose inside K1, occasionally K2 | the stakeholder | neither. See below |
| K9 | **The toolkit's own ADRs** | `meta/adr/` — this file | the toolkit's builders, not a consumer | **R**. Cited by a form a consumer's `ADR-nnnn` collides with (F-098); out of scope here beyond naming the distinction |

**K8 is the kind the specs have no name for.** An *engagement-state statement* is a sentence in a
delivered document that asserts something about the state of the **engagement** rather than about
the product: "the stakeholder has not yet been asked to accept this", "this is the only remaining
gap", "nothing else is open", "three of four work items are delivered". It is not record — it is
falsified, routinely, and by the pipeline itself. It is not deliverable — no code change can make
it true or false, and no item's acceptance criteria can be written against it, because the thing
it describes outlives every item. It is a third kind, and giving it its own row is the whole of
F-093's fix (§4, §6).

Two consequences follow immediately.

**(a) K5 and K6 are already governed and stay governed.** Fixed names, one writer each, overwrite
only your own, append-only where it says append-only. Nothing in this ADR reaches them; naming
them matters because a rule about "documents" that does not say it excludes the journal is a rule
somebody will apply to the journal.

**(b) The `record`/`deliverable` line does not follow the directory, and the two existing gates
that assume it does are both wrong.** `check-verify-freshness` excludes `docs/` wholesale
[src: scripts/check-verify-freshness] (F-058). `doc-header.md` §5 forbids writes to `docs/`
wholesale (F-057, F-076). Both were right about the record half and neither was ever told there
was another half.

---

## 2. The lifecycle events that change a document

The complete list of what happens to a document in an engagement, with the verb each event is
capable of. **Create** = the file did not exist. **Extend** = new content, nothing prior made
false. **Correct** = existing content made true again. **Falsify** = the event makes an existing
sentence false without touching it. **Cite** = the event points at the document as evidence and
changes nothing.

| # | Event | Actor | Can create | Can extend | Can correct | Can falsify | Can cite |
|---|-------|-------|------------|------------|-------------|-------------|----------|
| L1 | Intake shapes the idea | `intake` | K1 | K1 | — | — | K1 |
| L2 | Refinement sharpens an item | `refine` | K1 (prd) | K1 | K1 | — | K1, K7 |
| L3 | **`plan` designs the change** | `plan` | K2, K3 | K2, K3, K4 | K2 | — | all |
| L4 | **`implement` makes the change** | `implement` | — | — | see §3 | **K1, K2, K3, K4** | all |
| L5 | Verification finds a document wrong | `verify` | — | — | **nothing** | — | all |
| L6 | Review corrects | `review-close` | — | K4 | K1, K2, K3(§4b), K4 | — | all |
| L7 | A human answer is propagated | `answer-questions` | K3 | K1, K2, K3, K4 | K1, K2, K3(§4b), K4 | — | all |
| L8 | **The engagement ends** | `review-close` | — | K8 | **K8** | **K8** | all |
| L9 | The retrospective is read | `retro` | K5 (its own `retro.md`) | — | — | — | all |

The three rows in bold are where the current specs are silent or wrong.

**L4 is the event the specs deny exists.** `implement` is the only actor whose *ordinary work*
falsifies a document, and it is the actor forbidden to touch one. That is not a balance of
concerns; it is a hole. The falsification happens on the branch, the repair is required by D7,
and the only execution present is the one that is not allowed. F-076's gate sits in exactly that
hole and looks into it.

**L5 can do nothing at all, and that is correct.** `verify` judges the change against criteria it
did not write. If it may also repair the document it is judging, the judgement is circular in the
strongest sense — stronger than for `implement`, because `implement` at least has a plan telling
it what to do. `verify` files a question; `answer-questions` (L7) makes the edit. This is the one
half of `doc-header.md` §5 that survives this ADR unchanged, and it survives *derived* rather
than asserted.

**L8 is a new event.** ADR-0006 gave the ending a status graph and a termination question. It did
not give it a document. The engagement's ending is the moment at which every K8 sentence in the
workspace either becomes true or becomes false, and it is the only moment at which any actor
knows which.

---

## 3. The authority-and-obligation table

Kinds × events. Each cell says **who may write**, **whether they may write it at that event**,
and **which check they owe when they do**. The cells that say *nobody* are as load-bearing as the
ones that name an actor; F-057's whole complaint is a nobody-cell nobody had noticed writing
down.

### 3.1 The rule, stated once so the next case is decided rather than argued

> A skill may write a document sentence exactly when it is the skill that **causes the sentence's
> subject to change**, and only if it is **not** the skill whose work that sentence is the
> standard for. It owes, at that write, the audit obligation of the sentence's **claim kind**
> (§4), recorded in an audit row that names the sentence.

The second clause is `doc-header.md` §5's circularity argument, kept and sharpened: the objection
was never "`implement` writes prose". It is "the execution trying to satisfy a requirement must
not be the one that rewrites the requirement" — ADR-0008 §3's words, one turn earlier. That
objection is about a document's **record** half and says nothing about its deliverable half.

### 3.2 The table

`—` = this actor does not write this kind at this event. **nobody** = no actor may, and the row's
note says what the legal move is instead.

| Kind → | K1 product | K2 overview | K3 consumer ADR | K4 process | K8 engagement-state |
|---|---|---|---|---|---|
| **L1 `intake`** | **create + write.** Owes: §4a citation on every absolute; K8 sentences it writes are marked (§4.3) | — | — | — | **create.** The initial state statement, in the delimited section |
| **L2 `refine`** | **write.** Owes: §4a; ADR-0008 cross-answer check | — | — | — | nobody — *`refine` may not restate the engagement's state; it is not at the ending* |
| **L3 `plan`** | nobody — *a plan that needs the vision changed files a question* | **create + write.** Owes: §4a; §4.2 enumeration for any quantifier; **and the invalidation set (§5)** | **create.** Owes: §4a; two options or forced (§4) | **create + write.** Owes: §4a | nobody |
| **L4 `implement`** | **write, restricted.** Only entries in this item's invalidation set or deliverable set. Owes: §4a on what it writes, §4.2 on any quantifier, and an invalidation-set disposition per entry | **write, restricted.** Same restriction and same obligations | **§4b `erratum` only**, and only for a clause its own change falsified. Never the decision | **write, restricted.** Same restriction | **nobody** — *it may only record the entry as `owned-by-ending` (§4.3)* |
| **L5 `verify`** | nobody | nobody | nobody | nobody | nobody |
| **L6 `review-close`** (item close) | **correct.** Owes: §4a, §4.2, and the D7 confirmation against the invalidation set | **correct.** Same | **§4b `provenance` or `erratum`.** Owes: the entry's verbatim quote and resolving citation | **write.** Owes: §4a | nobody at an item close |
| **L7 `answer-questions`** | **write.** Owes: §4a; ADR-0008; `## Consequences` naming this file | **write.** Same | **create**, or §4b repair. Same | **write.** Same | nobody |
| **L8 `review-close`** (the ending) | **correct**, K8 sentences only | **correct**, K8 sentences only | nobody | nobody | **owner.** Owes: the ending's own statement, written after the sign-off is answered, restating every K8 sentence in the workspace |
| **L9 `retro`** | nobody | nobody | nobody | nobody | nobody |

### 3.3 The nobody-cells, said out loud

Six of them are deliberate and are the design:

1. **`verify` writes no document, ever.** The independence of the judge. It files a question
   (`spec/question.md`); `answer-questions` edits. Unchanged from `doc-header.md` §5.
2. **`retro` writes no document, ever.** It reads an ended engagement and writes only its own
   artifact [src: spec/retro.md]. A retrospective that edits the record it is reading has changed
   the run it observed.
3. **`plan` does not write `docs/product/`.** Design does not get to revise intent. If the plan
   requires the vision to change, that is a question, and the answer arrives through L7.
4. **Nobody writes a K8 sentence except `intake` (once, at the start) and `review-close` (at the
   ending).** This is F-093's fix and §4.3 is its mechanism.
5. **Nobody corrects a superseded consumer ADR.** `doc-header.md` §4b, unchanged, including its
   own hard-won correction that the rule tests the *act* and not the state (F-069).
6. **Nobody rewrites a claim sourced to a human answer because a later answer overtook it.**
   ADR-0008 §3's refused move, unchanged, and it overrides every "may write" cell above. An
   `implement` execution holding a legitimate invalidation-set entry that turns out to be one of
   the stakeholder's own sentences must stop and file the question, exactly as `review-close`
   must.

And one nobody-cell is a **residual gap this ADR does not close**, named here so that the later
units do not close it by accident and so that it is not discovered again as a finding:

7. **A false sentence discovered after the engagement is closed has no owner.** The epic is
   `done`, the retro is written, `engagement-state` says `closed`. ADR-0006's `done → open`
   reopening row exists for *delivered behaviour* and is triggered by a bug. A document defect is
   not delivered behaviour, and nothing in this model files a bug for prose. The honest position
   is that the legal move is a **new engagement or a bug filed against the delivered behaviour
   the sentence describes**, and if neither applies the sentence stays wrong until someone opens
   one. Written down rather than papered over.

### 3.4 What this replaces in `doc-header.md` §5

§5's table of "created by / updated by" stays, and its final paragraph — *"`implement` and
`verify` do **not** write to `docs/`"* — does not. It is replaced by:

> `verify` does not write to `docs/`. `implement` writes to `docs/` only within the invalidation
> set and deliverable set its plan declared (§5), never a sentence that is the standard its own
> work is judged against, and never a claim sourced to a human answer.

This is a real weakening of a real rule and §7 says what it costs.

---

## 4. The claim taxonomy

`doc-header.md` §4a has one obligation — an absolute about named code carries a resolving
citation — and applies it to every confident sentence. F-095 and F-093 are both cases where that
obligation is discharged perfectly and the sentence is false. So the obligation is not the wrong
one; it is one of three.

### 4.0 What decides the kinds, and why three

The obligation on a claim is derived from **what would falsify it, and who would be in a position
to witness the falsification**. That question has exactly three answers in this pipeline:

| The falsifier is… | Witnessed by | Therefore the obligation is… |
|---|---|---|
| a change to a **named** thing the sentence points at | whoever changes that thing — locatable from the sentence | *point at it*: the citation resolves |
| a change to, or the existence of, an **unnamed member** of a family the sentence quantifies over | nobody, from the sentence alone — the citation names the general case, and the member is what the sentence does not name | *enumerate the family*: the members, and how they were found |
| the **engagement's own act**, not any code change | only the actor performing that act, and only at the ending | *own it at the ending*: the sentence is written where its falsifier lives |

Not two, because collapsing the second into the first is precisely F-095 — the auditor opens the
citation, the citation is honest, the exception is in a member the sentence does not name — and
collapsing the third into either is F-093, where the audit passed and the falsifier was the
auditor's own next action. Not four, because there is no fourth kind of falsifier: a document
sentence in this workspace is about a named thing, about a set of things, or about the engagement.
A sentence about none of those is hedged prose, which §4a already excludes from the rule and this
ADR leaves excluded.

**And this yields the definition the methodology was missing:**

> A claim in a document is **checked** when a named execution recorded, in an audit row, *what
> would have falsified it and where that was looked for* — discharging the obligation of its kind
> — such that a later reader can repeat the look without re-deriving what the sentence is about.

Two things follow that are worth stating because both were violated in banked runs. "I read it
and it is true" is not a check: it records the verdict and destroys the method. And an audit that
opened only what the claim **cites** has not checked a quantified claim, because for that kind
the citation is by construction not where the falsifier is.

### 4.1 Cited fact

An assertion about something named as code — a backticked identifier, call, constant, or path.

- **Obligation:** `doc-header.md` §4a's citation, and it resolves. Today's rule, unchanged.
- **Audit row:** the sentence, the citation, and what was found when it was opened.
- **Enforcement:** `[auto]` for presence and resolution (`scripts/lint-claims`,
  `scripts/validate-workspace`); `[skill]` for whether the source supports the sentence —
  `lint-claims` says so in its own docstring and F-095 quotes it.

### 4.2 Quantified claim

A claim over a family: *every adapter…*, *all three tiers…*, *no caller…*, *the only path…*.
Syntactically these are already the absolutes §4a detects; semantically they are a different
object, because a citation cannot name the thing that falsifies them.

- **Obligation:** **member enumeration, recorded in the audit row.** The auditor states (a) the
  set the quantifier ranges over, (b) **how the set was enumerated** — the command, glob or grep,
  with its output, so the enumeration is repeatable and its completeness is inspectable, (c) the
  members, by name, and (d) the verdict per member, or an explicit statement that the members
  were spot-checked and which ones.
- The distinguishing rule, in one line: **opening what the claim cites does not discharge a
  quantified claim.** "I opened the fixture" and "I enumerated the members" are different entries
  in the audit and the row has room for both.
- Where an enumeration is genuinely infeasible (an open-ended family), the legal move is to
  **weaken the sentence** until it is a cited fact, not to record the enumeration as done. A
  universal nobody can enumerate is a universal nobody can check.
- **Enforcement:** `[auto]` that a sentence carrying a quantifier over a backticked set has an
  enumeration entry in the audit row (a shape check — the absolutes are already detected, so this
  hangs off machinery that exists). `[skill]` for whether the enumeration is complete. This is the
  same split as `lint-answers`'s obligation 1 (ADR-0008 §4) and it works for the same reason: it
  makes "I opened the fixture" a sentence an execution cannot write while passing its gates.

### 4.3 Engagement-state statement

A sentence asserting the state of the engagement itself.

- **Obligation:** **it is owned by the ending.** Concretely:
  1. Every K8 sentence lives inside a **delimited section** of its document — one section per
     document, marked, so that the set of such sentences in the workspace is enumerable by a
     script rather than by a reading.
  2. `intake` may write the initial one. Between then and the ending, **no execution may write
     one**, and an execution whose change would falsify one records the entry in its invalidation
     set with the disposition `owned-by-ending` and moves on. That disposition is the whole of
     what F-093's `implement` and `review-close` had no way to say.
  3. At the ending (L8), and **after** the sign-off question is answered — because the answer is
     itself part of the engagement's state — `review-close` restates every delimited section in
     the workspace. Not "corrects the ones it noticed": restates all of them, from the ending it
     is recording. That is a bounded, enumerable job precisely because of rule 1.
  4. No item-level audit (D7, D12) is charged with a K8 sentence. An item that fails D12 on one
     has been given a defect it is structurally unable to fix, which is F-057's shape.
- **Enforcement:** `[auto]` that the delimited sections exist and that the ending restated each
  one (both are file-shape questions over an enumerable set). `[auto]` that no execution other
  than `intake` and `review-close`-at-an-ending changed the delimited region — this is the same
  diff-over-a-marked-region test `lint-answers --changed-since` already performs for sourced
  claims (ADR-0008 §4 obligation 3). `[skill]` for whether the restated sentence is *true*, which
  is a person's read of the ending and always will be.

### 4.4 The `human-answer` overlay

A claim of **any** of the three kinds may additionally carry the marker `[src: <ITEM>/Q-nnn]`
(written here as a form, not as a citation) where that
question is human-answered. ADR-0008 governs it and this ADR does not touch it: the overlay
removes the "correct it" move and substitutes "file the question", regardless of kind, for every
actor including the ones §3 newly permits to write. Stated here so that a reader deriving
`implement`'s new authority from §3 alone cannot miss it.

---

## 5. The invalidation set

**Derived claim: the set of documents a change invalidates is an output of `plan`, and the
falsification question is asked where the change is made.**

F-087's mechanism, restated from the model: "touched" is a diff and "falsified" is not. Every
piece of document machinery in the pipeline is scoped to a diff — `--changed-since`, D7's
scoping, `lint-claims`'s window — so a document the branch never opens is invisible to all of it,
and the first question anybody asks about it is D7, at the last gate, after `implement` and
`verify` have both passed. WI-0004 is the sharp case: its plan had learned from WI-0003 and
carried a step for the architecture overview, `implement` executed it faithfully, and the
document that failed was the product vision, which no step named.

Three properties decide where the question belongs.

1. **It is answerable only by someone who knows what the change does.** That is `plan`, which has
   just designed it, or `implement`, which is making it. It is not `review-close`, which is why
   `review-close` discovers rather than confirms.
2. **It is a design output, not a check.** "Which sentences does this change make false" is the
   same act as "which documents constrain this change", and `plan` already performs the second —
   it reads `docs/architecture/overview.md` and `docs/architecture/adr/`
   [src: methodology/skills/plan/skill.yaml].
3. **The cost of asking it late is a full cycle.** Twice, in one banked engagement, with no code
   change in either.

So: `plan` emits it, `implement` discharges it, `verify` checks the disposition, `review-close`
confirms it.

### 5.1 What the invalidation set contains

A table in `artifacts/plan.md`, one row per entry, four kinds of entry:

| Column | Content |
|--------|---------|
| `document` | the path |
| `what` | the sentence or the section at risk, quoted or located precisely enough to reopen |
| `kind` | `cited-fact` \| `quantified` \| `engagement-state` (§4) |
| `why` | what about this change would make it false |
| `disposition` | `to-update` \| `verified-still-true` \| `owned-by-ending` \| `question-filed:<ITEM>/Q-###` |

Plus two lists that belong to the same act and are cheaper to keep beside it than to keep
separately:

- **`deliverable-documents`** — documents this item is *asked to produce or change*, because an
  acceptance criterion is about them. Empty for most items and non-empty for exactly the items
  F-057 and F-058 are about.
- **`binding-adrs`** — the ADRs that constrain this change, by ID (§6/F-092).

`plan` fills `document`/`what`/`kind`/`why` and leaves `disposition` open, seeding it from the
documents its own steps cite and from the documents that describe the behaviour the item's
criteria name. `plan` cannot be complete and this ADR does not claim it can — completeness is
what the downstream consumers are for.

### 5.2 Who consumes it

| Consumer | What it does with the set |
|----------|---------------------------|
| `implement` | Closes every entry with a disposition, and **may add entries** — it is the actor that discovers, mid-change, that a fourth document was falsified. Its authority to write (§3, L4) is bounded by this set plus `deliverable-documents`, so the set is simultaneously its obligation and its licence |
| `verify` | Checks that every entry has a disposition and that `verified-still-true` entries are true, by reading. It repairs nothing (§3, L5); a false entry is a send-back or a question |
| `review-close` | **D7 becomes a confirmation:** every entry disposed, plus one question — did this change falsify a document the set does not name? A `no` is now a claim against an enumerated set rather than a memory |
| `check-verify-freshness` | Excludes from the "record only" exemption every path in `deliverable-documents` (§6/F-058) |
| the `claims-are-sourced` window | Its scope on `implement` is the branch diff **plus** the set — which is what stops the window being empty by construction (§6/F-076) |

---

## 6. Every historical case, against the derived model

Each is a fixture in META-148. The derivation has to re-decide the cases that produced it, or it
is a story rather than a model.

### F-076 — the claims gate examines an empty window by construction

The two answers ROADMAP §3 named were: *either `doc-header.md` §5 holds and the gate does not
belong on `implement`, or §5 does not hold.*

**Answer chosen: §5 does not hold, and the gate stays on `implement`.**

Why this way round and not the other:

- §5 is an **absolute over a directory** justified by an argument about **circularity**. §3.1
  shows the argument survives in full for the record half and has nothing to say about the
  deliverable half. A rule whose justification covers a subset of its scope is over-broad, and
  the over-broad part is exactly the part that produced F-057, F-058 and F-076.
- The practice already contradicts it, and did so through a legitimate path: a D7/D12 send-back
  had `implement` edit `docs/product/vision.md` [src: meta/findings/FINDINGS.md]. A rule the
  pipeline instructs skills to break is F-013's class, and ADR-0006 settled that such a rule is
  the defect, not the run.
- Removing the gate instead would leave `implement` — the one actor whose ordinary work falsifies
  documents — with no document obligation whatsoever, and would move the whole of D7 onto
  `review-close`, which is the arrangement F-087 filed as a defect.

What therefore has to change:

1. `doc-header.md` §5's final paragraph is replaced by §3.4's rule.
2. `implement`'s `claims-are-sourced` window becomes the branch diff **plus the invalidation set
   and the deliverable documents** — a scope that can contain something, on an item that has
   documents in it.
3. `scripts/lib/scope.py` gains the **fourth state** F-076's first direction asks for:
   *out-of-scope-by-construction* — the window is well formed, this execution touched nothing in
   it, **and nothing this execution was permitted to do could have put anything in it.** It
   prints and journals as its own sentence, never as "passed". F-066's three states modelled
   "real and empty" as an honest pass *because the comparison could have found something*
   [src: scripts/lib/scope.py]; that justification is exactly what fails here, and the fourth
   state is where the failure goes. With change 2 in place this state should be rare; it must
   still exist, because the next rule that empties a window by construction will not announce
   itself either.

Fixture: must-fail — an `implement` execution whose plan declares an invalidation-set entry under
`docs/`, whose gate window excludes it, and whose journal records a pass.

### F-087 — the invalidation set

**The model's answer:** §5 in full. The set is a `plan` output; `implement` discharges it and may
extend it; `verify` checks dispositions; `review-close`'s D7 confirms against an enumerated set
instead of discovering. The falsification question is asked where the change is made.

**What has to change:** `plan` gains the output and an exit criterion; `implement` gains the
disposition obligation; `verify` gains the disposition check; D7 is rewritten as a confirmation
against the set, and its scoping sentence — "what this change touched" — becomes "what this
change touched or its plan named".

Fixture: must-fail — a plan with no invalidation set on an item whose steps cite a document;
must-fail — an entry left with no disposition at `in-review`.

### F-093 — engagement-state sections are owned by the ending

**The model's answer:** §4.3. K8 is a third claim kind; its sentences live in delimited sections;
`intake` writes the first; nothing writes one mid-engagement; `review-close` restates every one at
the ending, after the sign-off is answered. No item-level audit is charged with one.

Both corrections in the banked run were *declared and defensible and authorised by nothing*. The
model authorises one of them — `review-close`'s, at the ending — and makes the other unnecessary:
`answer-questions` was correcting a second sentence beyond its answer's scope because nobody else
was going to.

**What has to change:** the delimiter convention in `doc-header.md`; the `owned-by-ending`
disposition in the invalidation set; `review-close`'s ending contract gains the restatement; DE4
gains it as a criterion; D7/D12 are scoped to exclude K8 explicitly, because "exclude the
engagement-state sentences" is a rule a reader will otherwise not infer.

Fixture: must-pass — an ending that restates a section whose sentence its own sign-off falsified.
Must-fail — an item execution that edits a delimited section.

### F-095 — quantified claims require member enumeration

**The model's answer:** §4.2. A quantifier is its own claim kind; opening the citation does not
discharge it; the audit row carries the set, the enumeration method with its output, the members
and a per-member verdict; an unenumerable universal is weakened rather than recorded as checked.

Note what this says about the banked case: all three item-level audits were honest and all three
were *insufficient by construction*, and the ending's audit found the falsifier only because its
scope was the whole document set rather than because it read better. A model that made those
three audits look negligent would be the wrong model.

**What has to change:** `doc-header.md` §4a gains the second obligation; D12's audit row gains the
enumeration columns; `verify` and `review-close` gain the obligation where they audit;
`lint-claims` gains the shape check on quantified sentences.

Fixture: must-fail — a universal audited `true` with an audit row that names only the shared
fixture. Must-pass — the same claim with the enumeration recorded and one member marked as the
exception.

### F-053 — its class is the lifecycle-state input

Not fixed here. What it contributes is the constraint that the model must satisfy, and it is
this: **a document's state and an item's state are two different state machines, and neither may
be derived from the other.**

- A document's machine advances on **content change**: `version` bumps, a change-log row is
  appended, `status` moves `draft`→`current`→`superseded` [src: spec/doc-header.md]. Its unit is
  the edit.
- An item's machine advances on **execution**: `draft`→…→`done`, gated, with a history row and a
  journal entry [src: methodology/pipeline.yaml]. Its unit is the skill run.
- The only legitimate coupling is the **audit row**, which names both: the item the change was
  made for (`updated-for`) and the document version it produced.

F-053's mechanism is the half-written record — a state requiring two writes, and a tool offering
one, so every path through it passes through an invalid workspace. The document machine has the
same shape and this ADR must not add another instance of it: the content edit, the `version` bump
and the change-log row are **one act**, and the same is true of the audit row and the disposition
it closes. Where a later unit adds a tool for a document write, it writes all of them or it is
F-053 again in `docs/`.

The corollary is F-058's diagnosis in one sentence: `check-verify-freshness` decides a document's
kind from **its directory**, which is a proxy for the item's state machine, and gets it wrong for
exactly the items where the two machines disagree.

### F-092 — ADR conformance

**The model's answer:** it is a cell in §3's table and a list in §5's plan output.

- `plan` lists `binding-adrs` — the ADRs its steps are constrained by, by ID. It already reads
  `docs/architecture/adr/` for the purpose of not silently re-deciding
  [src: methodology/skills/plan/skill.yaml]; naming what it read is the whole addition.
- **`verify` decides each one.** It is the gate, and "decides" means concretely: for every ID in
  `binding-adrs`, `verify-report.md` carries a row with a verdict of `conforms`, `violates` or
  `not-engaged`; a `conforms` verdict **quotes the clause of that ADR's `## Decision` it is
  conforming to** and names the file and line in the change that satisfies it; a `violates`
  verdict is a send-back. `not-engaged` is legal and must say why the change does not touch the
  decision's subject.
- **`review-close` checks the list is complete**, not each entry — one D-criterion asking whether
  the change engages an ADR that `binding-adrs` does not name. That is the cheap half and it is
  the half that catches a plan which listed nothing.

Why `verify` and not `review-close`: `verify` is the stage whose entire contract is judging a
change against a standard it did not write, it already reads the branch, and it already carries
the closest analogue — `a-criterion-about-criteria-is-read`, which is the same move (read a
sentence's text against the new behaviour, tests as evidence and not as definition)
[src: methodology/skills/verify/skill.yaml]. Putting it on `review-close` puts it after the
merge-shaped gates and one stage further from the person who could fix it. Both banked violations
were caught by a reviewer reading the diff against the ADR; the model moves that read one stage
earlier and makes it a row rather than a virtue.

**What has to change:** `plan` output; `verify` gate and report section; one new D-criterion.

Fixture: must-fail — a plan naming an ADR whose verdict row is missing from the verify report;
must-fail — a `conforms` row quoting no clause.

### F-057 — a defect whose fix is a document

**The model's answer:** the item declares the document in `deliverable-documents` (§5.1), and §3's
L4 row permits `implement` to write it. The nobody-cell is gone, and it is gone by derivation
rather than by an exception — `implement` causes the sentence's subject to change (it *is* the
subject), and the sentence is not the standard its own work is judged against, because the
standard is the acceptance criterion in `item.md`.

The worker's own two options were *"an exception in §5 for items whose criteria are about a
document, or a dispatchable owner for such items"*. The model takes the first and generalises it:
not an exception for that item shape, but the recognition that §5's scope was always wrong.

Fixture: must-pass — an item whose AC is about `docs/product/vision.md`, planned with the
document in `deliverable-documents`, implemented, verified, closed, with no send-back and no ADR
written to authorise it.

### F-058 — the freshness gate treats `docs/` as record

**The model's answer:** the exemption is not "under `docs/`". It is "not in this item's
`deliverable-documents`". `check-verify-freshness`'s reasoning is right and its predicate is a
proxy: `verify` and `review-close` must commit their own records, those commits move the head,
and a record-only change does not invalidate a verification of the code
[src: scripts/check-verify-freshness]. Everything in that sentence holds for record documents and
none of it holds for a document that is the deliverable — a change to which is exactly what D10
exists to catch.

**What has to change:** the gate takes the item's `deliverable-documents` (from the plan) and
subtracts them from the exemption, so a post-verification edit to a delivered document sends the
item back to `verifying` like any code change.

Fixture: must-fail — an item with `docs/product/vision.md` in `deliverable-documents`, verified,
then edited, then closed.

---

## Enforcement boundary — what a script can decide, and what stays judgement

Stated plainly, per obligation, because this project's thesis is that instruction-shaped gates do
not hold (ROADMAP §1, F-001) and an ADR that hides which of its own rules are instructions is
worse than one that says so.

| # | Obligation | `[auto]` | `[skill]` | Neither, today |
|---|-----------|---------|-----------|----------------|
| 1 | A cited fact carries a resolving citation | ✅ `lint-claims`, `validate-workspace` | — | — |
| 2 | The citation **supports** the sentence | — | ✅ D12's read | — |
| 3 | A quantified sentence's audit row carries an enumeration entry with a repeatable method | ✅ shape check, on machinery that already detects the absolutes | — | — |
| 4 | The enumeration is **complete** | — | ✅ | — |
| 5 | A quantified sentence was recognised **as** quantified | ⚠️ partial — the absolute-word list catches most (`every`, `all`, `no`, `only`), and a universal phrased without one ("each handler validates its input") is caught by nothing | ✅ for the rest | — |
| 6 | K8 sentences sit inside delimited sections | ✅ shape | — | — |
| 7 | Only `intake` and the ending wrote inside a delimited section | ✅ diff over a marked region, the `lint-answers --changed-since` mechanism | — | — |
| 8 | The ending restated **every** delimited section | ✅ enumerable set, presence per section | — | — |
| 9 | The restated K8 sentence is **true** | — | ✅ | — |
| 10 | A K8 sentence was **written** as a K8 sentence, and not as ordinary prose outside the section | — | ✅ the author's judgement at the moment of writing | ⚠️ this is the load-bearing gap in §4.3 and it should be said first, not last: everything mechanical about K8 rests on the sentence having been put in the right place by the skill that wrote it. A K8 sentence written loose in the body is invisible to obligations 6–8, and F-093's own sentence was written loose |
| 11 | The plan carries an invalidation set with the required columns | ✅ shape | — | — |
| 12 | The set is **complete** — it names every document the change falsifies | — | ✅ `plan`, `implement`, `review-close`'s D7 confirmation | ⚠️ nothing can decide this, and D7 was never able to either. What changes is that the answer is now a claim against an enumerated set, attributable, instead of a memory |
| 13 | Every entry carries a disposition at `in-review` | ✅ shape | — | — |
| 14 | A `verified-still-true` disposition is **true** | — | ✅ `verify` | — |
| 15 | `binding-adrs` has a verdict row per ID in the verify report | ✅ shape, IDs cross-checked against the plan | — | — |
| 16 | A `conforms` verdict is correct | — | ✅ | — |
| 17 | `binding-adrs` is **complete** | — | ✅ `review-close`'s completeness criterion | ⚠️ same shape as 12 |
| 18 | The freshness exemption subtracts `deliverable-documents` | ✅ `check-verify-freshness` | — | — |
| 19 | `implement` wrote only inside its invalidation set and deliverable set | ✅ diff under `docs/` against the plan's set | — | — |
| 20 | The claims window was not out-of-scope-by-construction | ✅ `scope.py`'s fourth state | — | — |

Twelve of the twenty are decidable by a script; six are judgement with a mechanical shell that
makes the judgement **attributable**; and three — 10, 12 and 17 — are places where the model
depends on someone doing something no gate can see. Obligation 10 is the one to watch: it is the
foundation of the K8 mechanism and it is the one obligation in this ADR with no mechanical half at
all. If §4.3 fails in a later run, that is where it will fail.

---

## 7. What this costs, said plainly

- **A rule is weakened, not tightened.** `implement` may now write to `docs/`. That is a real loss
  of a real protection, and the compensating controls — the write must be inside a set the plan
  declared, the record half is still forbidden, ADR-0008's refused move still overrides, and
  obligation 19 checks the diff against the set — are three shape checks and a contract rule
  standing where one absolute stood. If a later run finds `implement` widening its own scope
  through `docs/`, this section is where it was predicted.
- **`plan` grows an output nobody can complete.** The invalidation set is a guess made by the
  actor furthest from the change's consequences, and its completeness is obligation 12, which
  nothing decides. The honest claim is narrow: the question moves from the last gate to the first
  stage that can act on it, and being wrong about it becomes attributable.
- **A version bump on almost everything, again.** `plan`, `implement`, `verify`, `review-close`,
  `intake`, `answer-questions`; `spec/doc-header.md`, `spec/dor-dod.md`, `spec/workspace-layout.md`;
  `scripts/lib/scope.py`, `scripts/lint-claims`, `scripts/check-verify-freshness`,
  `scripts/validate-workspace`. ROADMAP §2's "a full consumer run with zero version bumps" moves
  further away. This is the second consecutive derivation of which that is true and the thermometer
  should be read rather than explained.
- **Every audit gets longer.** A quantified claim now costs an enumeration with its command and
  its output, per claim, per audit. The failure mode of a gate that is too expensive is that it
  gets performed as ritual — F-095's three audits were not ritual, they were honest and
  insufficient, and an enumeration performed as ritual would be worse than what they did. §4.2's
  escape hatch (weaken the sentence) exists for this reason and it will be under-used.
- **The ending grows work at the worst moment.** `review-close` at an ending must now restate every
  delimited section in the workspace, after the sign-off answer arrives, in the same turn that
  ADR-0006 already loaded with the termination gate. It is bounded and enumerable; it is still one
  more thing at the moment when everyone wants to be finished.
- **Three obligations stay judgement, and two of them are completeness.** Said in the enforcement
  table rather than buried.
- **A residual gap ships unfixed.** §3.3 item 7: a false sentence found after the engagement is
  closed has no owner. Named, not solved.

## 8. Alternatives rejected

- **Keep §5 and remove `implement`'s claims gate.** The other branch of F-076's two-way question.
  Rejected: it leaves F-057's nobody-cell open, leaves F-058 undecidable, and moves the entire
  document obligation onto `review-close` — the arrangement F-087 was filed against. It also
  requires believing that the actor whose work falsifies documents should have no obligation
  toward them.
- **An exception in §5 for items whose acceptance criteria are about a document.** F-057's own
  first option, and the smallest possible fix. Rejected as the sixth-exception move ADR-0006
  names: it decides F-057, leaves F-058 to be decided separately, leaves F-076's gate empty on
  every ordinary item, and says nothing about F-087 or F-093. The class survives an exception; it
  does not survive an enumeration.
- **A dispatchable owner for document-shaped items** — a `document` item type, or a
  `write-the-docs` skill. F-057's second option. Rejected: it makes the document deliverable a
  *different kind of work* rather than ordinary work with a different artifact, which duplicates
  the whole DoR/DoD apparatus for a case that differs only in what a criterion points at. It also
  gets F-093 wrong in a new way, by implying an item could own an engagement-state sentence.
- **Treat every document as record, and forbid any falsification.** Rejected: an architecture
  overview that may not be falsified is an architecture overview that may not describe the system.
  This is the F-050 mistake — a rule nobody can satisfy.
- **Ask "what did this falsify?" at `verify` instead of at `plan`.** Rejected: `verify` may not
  repair (§3, L5), so the answer arrives one stage after the last actor able to act on it. It
  would replace one late discovery with a slightly earlier one and keep the send-back.
- **Make the ending's K8 restatement a full re-read of `docs/` rather than of delimited sections.**
  Rejected on the ADR-0008 §5 argument, measured there: a gate that demands an unbounded
  reconciliation at the ending gets switched off, and a gate that gets switched off is worse than
  none. Delimiting the sections is what makes the ending's job finite.
- **Four claim kinds — split `cited fact` into "about code" and "about a document".** Rejected:
  the falsifier and the witness are the same in both cases (whoever changes the named thing), so
  the obligation is the same, so it is one kind. §4.0's test is what keeps the taxonomy from
  growing by analogy.
- **Give the toolkit's own `meta/adr/` the same machinery.** Rejected as out of scope, and noted:
  this file's citations resolve as workspace paths but no gate reads `meta/adr/` today
  [src: scripts/lint-claims], so every citation above was checked by hand. F-024 is in this ledger
  because a citation nobody checks is the appearance of evidence, and F-098 is open on the citation
  form itself.
