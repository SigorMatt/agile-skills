# `docs/` — version header, change log, and the ADR format

`docs/` is the workspace's long-lived knowledge: what the product is for, how it is built, and
why it is built that way. Where `tracker/` is a record of *work*, `docs/` is a record of
*conclusions*. A skill that learns something durable writes it here; a skill that needs a
decision looks here first.

Git already stores the diffs. The header and change log exist for a different reason: an agent
reading a document mid-run needs to know, from the document itself, how current it is and which
work item last touched it — without running `git log`, and without the answer depending on
whether the workspace is even a git repository yet.

---

## 1. Layout

```
docs/
├── product/
│   ├── vision.md            # why this exists, for whom
│   └── prd.md               # what it does, at product level
├── architecture/
│   ├── overview.md          # the shape of the system
│   └── adr/
│       ├── ADR-0001-<slug>.md
│       └── ADR-0002-<slug>.md
└── process/
    └── ways-of-working.md   # conventions this project adopted
```

`docs/product/vision.md` and `docs/architecture/overview.md` MUST exist once an epic has been
planned. The others are created when a skill has something to put in them; an empty placeholder
document is worse than a missing one, because it reads as an answer.

---

## 2. Header

Every file under `docs/` MUST start with this frontmatter:

```yaml
---
title: Architecture overview
version: 3
status: current
updated: 2026-08-16T10:20:03Z
updated-by: plan
updated-for: WI-0007
---
```

| Field | Required | Rules |
|-------|----------|-------|
| `title` | always | human-readable; matches the document's `# ` heading |
| `version` | always | integer, starts at `1`, incremented by **every** content change |
| `status` | always | `current` \| `superseded` \| `draft` |
| `updated` | always | UTC ISO-8601 of the change that produced this version |
| `updated-by` | always | the **skill name** that made the change |
| `updated-for` | always | the item ID the change was made for, or `—` for a change not tied to one |
| `supersedes` / `superseded-by` | when `status: superseded` | path to the replacing document |

---

## 3. Change log

Every document MUST end with:

```markdown
## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-08-16T10:20:03Z | plan | WI-0007 | Added the summary pipeline; recorded the sort contract |
| 2 | 2026-08-16T09:40:12Z | answer-questions | WI-0004 | Clarified that "line" means newline-terminated |
| 1 | 2026-08-15T16:02:00Z | plan | EP-001 | First version |
```

Rules:

- Newest first. The top row's `version` MUST equal the frontmatter `version`.
- Every content change adds a row **and** bumps `version`. A change without a row is invalid; a
  row without a bump is invalid.
- `what changed` describes the change in terms a reader can act on. "Updated" is not a
  description.
- Fixing a typo is a content change. The rule has no exceptions, because "is this worth a row?"
  is exactly the judgement that erodes a change log into uselessness.

---

## 4. Architecture Decision Records

`docs/architecture/adr/ADR-####-<slug>.md`. `<slug>` is lowercase, hyphen-separated, derived
from the title.

```markdown
---
title: Store counts as integers, not floats
version: 1
status: current
updated: 2026-08-16T10:18:44Z
updated-by: plan
updated-for: WI-0007
---

# ADR-0004 — Store counts as integers, not floats

- **Status:** proposed | accepted | superseded
- **Date:** 2026-08-16
- **Decided by:** plan (architect), for WI-0007
- **Supersedes:** — | ADR-0002

## Context

What forced a decision. The constraints that were actually in play, and what was read to
establish them.

## Options considered

- **A —** <option>. Cost: <...>. Risk: <...>.
- **B —** <option>. Cost: <...>. Risk: <...>.

## Decision

What was chosen, stated so that code can be checked against it.

## Consequences

What becomes easy, what becomes hard, and what would have to change to reverse this. If the
decision is hard to reverse, say so here — that is the fact a future reader most needs.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-16T10:18:44Z | plan | WI-0007 | First version |
```

Rules:

- An ADR MUST list at least two options, or state why the decision was forced. A record showing
  only the chosen path documents a conclusion, not a decision, and a later reader cannot tell
  whether the alternatives were considered or never noticed.
- An ADR is **never edited to change its decision**. It is superseded by a new ADR that cites
  it, and its `status` becomes `superseded` with `superseded-by` set. The change log records
  that transition. The point of the file is to preserve what was believed at the time.
- Every ADR MUST be referenced from at least one item's plan or journal. An ADR nobody cites is
  either unnecessary or, more often, a decision that was never actually applied.
- `## Consequences` MUST state reversibility. `plan`'s escalation rule (see `question.md` §1)
  turns on exactly that property, so leaving it implicit breaks a decision procedure elsewhere
  in the methodology.

---

## 4b. Correcting a standing ADR without superseding it

§4's supersession rule protects one thing: **what was decided**. It was written as though the
decision and the document were the same object, and they are not. A real run found the gap from
both sides in one week.

- Iteration 4's `lint-claims --all` flagged three `claim.unsourced` errors in a standing ADR. The
  reviewer read all three against the code and found them **true**. Adding a citation would have
  cleared them; adding a citation is an edit; superseding an accepted decision in order to write
  down where it came from is disproportionate. The reviewer recorded it honestly as an accepted
  gap, and the ledger acquired a permanent, known, unfixable lint error (F-067).
- Iteration 3's team hit the other side — one clause of a *justification* was false against the
  code while the decision itself was correct — and wrote themselves an ADR to authorise fixing
  it, because ours did not.

So: an ADR at `status: accepted` MAY be repaired in place, in exactly two ways, and every repair
is recorded as an entry in an **append-only `## Corrections` section**.

| Kind | What it may do | What makes it legal |
|------|----------------|--------------------|
| `provenance` | add a citation to an existing sentence | the sentence's assertion is **unchanged** — only its `[src: ...]` is new — and the citation resolves |
| `erratum` | replace a clause that was **false against the code** | the removed text is quoted **verbatim** in the entry, and the entry cites what establishes the truth: a command with its outcome, a named function, a criterion |

And one line that is not negotiable: **if a reader would have to change any code to satisfy the
new text, it is a new decision** and §4's supersession rule applies with full force. That is the
boundary between a correction and a rewrite, and it is the condition most likely to be stretched
under time pressure.

```markdown
## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-08-29T14:02:11Z | review-close | EP-001 | provenance | `## Decision` item 1: *"used exactly as given"* now cites [src: src/recall/store.py:31] and [src: run: RECALL_FILE=/tmp/x recall list → exit 0, reads /tmp/x]. The assertion is unchanged. |
| 2026-08-29T14:02:11Z | plan | BUG-0001 | erratum | `## Decision` item 4 said *"A column's width does not depend on its marker"*, which [src: run: printf … \| mdtab → a wider column] falsifies. Replaced with a clause naming what width does depend on. |
```

Rules:

- `## Corrections` is **append-only** and sits last, after `## Change log`. An entry is never
  edited or removed. A correction whose row says "fixed a wrong sentence" without quoting it
  destroys the evidence this section exists to keep.
- Every entry carries a resolving citation. A repair with no source is the shape that produced
  F-001.
- Every entry has a matching `## Change log` row and a `version` bump. The two sections answer
  different questions — the change log says *a version happened*, the corrections say *what a
  sentence used to say* — and neither substitutes for the other.
- A superseded ADR takes **no new correction**, and keeps every correction it already made. The
  rule is about the *act*, not the state: an ADR corrected while it was `accepted` and superseded
  afterwards is perfectly legal, and its `## Corrections` section stays exactly as it was — the
  section is append-only, so removing the entries to satisfy a state rule would destroy the
  evidence it exists to keep. `validate-workspace` therefore refuses a correction **dated at or
  after** the supersession, and nothing else.

  Reading it as a state rule was this section's own first defect, and a regression run found it
  within a day: an ADR that had been corrected and was then correctly superseded had *no valid
  state to be in*. The team renamed its heading to `## Corrections — closed on supersession`,
  wrote a paragraph saying plainly that the rename was a workaround, and then could not clear
  three true-but-unsourced claims in the same file, because §4b's repair route was shut for it.
  `review-close` ended that engagement with a forced hard gate (F-069). A rule nobody can satisfy
  is the F-050 mistake, and this is what it looks like when it is made in a fix for F-067.
- `scripts/validate-workspace` enforces the shape; it cannot enforce condition one. Whether the
  assertion really is unchanged is a judgement, and the entry is what makes it attributable.

---

## 4a. Claims and their provenance

A document under `docs/` is read by people and by skills that will act on it. Its most dangerous
sentences are the confident ones — an absolute statement about a named thing in the system,
written once and re-quoted thereafter. An independent audit of a real run found exactly that
failure: one wrong absolute justification reached shipped source comments, an ADR and the
architecture overview, and then **spread to a seventh document after the audit flagged it**,
because every skill that touched the area re-quoted the sentence rather than re-checking it.
Every machine-decidable gate held throughout; every gate resting on a human-style read did not.

So absolutes get sources.

- A paragraph that makes an **absolute claim** — `no`, `none`, `never`, `always`, `only`,
  `every`, `all`, `nothing`, `cannot`, `exactly`, `impossible`, `guaranteed` — about something
  named as code (a backticked identifier, call, constant, or a path) MUST carry at least one
  citation, written inline as `[src: ...]`.
- A citation MUST resolve. An unresolvable citation is worse than none: it is the appearance of
  evidence.
- Hedged prose is not the target. "Recursion was deferred" needs no citation; "`list_files`
  never recurses" does.

### Citation forms

| Form | Example | Resolves when |
|------|---------|---------------|
| workspace path | `[src: src/store.py]`, `[src: src/store.py:42]` | the file exists in the workspace |
| item | `[src: WI-0007]` | the item exists |
| acceptance criterion | `[src: WI-0007 AC3]` | the item exists and declares that AC |
| question | `[src: WI-0007/Q-002]` | the question file exists |
| ADR | `[src: ADR-0004]` | an ADR with that number exists |
| commit | `[src: commit a1b2c3d]` | the commit is in this repository |
| command outcome | `[src: run: python3 -m pytest -q → exit 0, 14 passed]` | it records both the command and its outcome |

Several sources are separated by `;` inside one marker. `scripts/lint-claims` enforces both
rules and is a hard gate on `plan`, `implement` and `review-close`; `scripts/validate-workspace`
enforces the resolution rule over the whole workspace, at any time.

The absolute-claim rule is checked against **what an execution touched, or what its plan named**
— its branch diff plus the invalidation set and deliverable documents its plan declared
(`dor-dod.md` D7) — and not against the whole tree. That is the same scoping `dor-dod.md` applies
to D7 and D12. A record written before this
convention existed is not retroactively invalid; the next execution that edits a document is the
one that must source what it writes.

It also does not apply to a document at `status: superseded`. The rule exists so that a confident
sentence **a reader will act on** points at something, and a superseded document is by
construction not one anybody acts on: `superseded-by` is mandatory and names what replaced it. It
is also the one document with no legal way to gain a citation, because §4b takes no new
corrections on it — so the rule would demand a repair it forbids, which is how a regression run
ended with a forced gate over three sentences that were every one of them true (F-069). Rule 1
still reads them: a citation that does not resolve is a broken pointer whatever the document's
status, and `lint-claims` prints how many documents rule 2 skipped and why rather than passing
over them in silence.

### Three claim kinds, three obligations

The citation is the obligation of **one** kind of claim, and it is discharged perfectly by
sentences that are false. What a sentence owes follows from **what would falsify it, and who
would be in a position to witness the falsification**, and in this pipeline that question has
exactly three answers (derived in ADR-0010 §4):

| Kind | The falsifier is… | So the obligation is… |
|------|-------------------|-----------------------|
| **cited fact** | a change to a **named** thing the sentence points at | *point at it* — the citation above, and it resolves |
| **quantified claim** | a change to, or the existence of, an **unnamed member** of the family the sentence quantifies over | *enumerate the family* |
| **engagement-state statement** | the **engagement's own act**, not any code change | *own it at the ending* |

A claim of **any** of the three kinds may additionally be sourced to a human-answered question.
That overlay is governed elsewhere and is unchanged by the kinds: it removes the "correct it"
move and substitutes "file the question", for every actor and every kind (`question.md` §2).

This is what makes a claim **checked**: a named execution recorded, in an **audit row**, *what
would have falsified the sentence and where that was looked for* — discharging the obligation of
its kind — so that a later reader can repeat the look without re-deriving what the sentence is
about. "I read it and it is true" is not a check; it records the verdict and destroys the method.

An **audit row** is one row per claim checked, in the artifact where that audit is recorded —
`artifacts/review.md`'s `## What I examined` at an item close or an ending,
`artifacts/verify-report.md` where `verify` audits. It names the sentence and carries the
evidence the sentence's kind owes.

### Quantified claims carry their enumeration

A claim over a family — *every adapter …*, *all three tiers …*, *no caller …*, *the only path …*
— is syntactically one of the absolutes rule 1 already detects, and semantically a different
object: **a citation cannot name the thing that falsifies it.** The citation names the general
case; the falsifier is a member the sentence does not name.

- The audit row for a quantified claim records (a) **the set** the quantifier ranges over,
  (b) **how the set was enumerated** — the command, glob or grep, with its output, so the
  enumeration is repeatable and its completeness is inspectable, (c) **the members**, by name,
  and (d) **the verdict per member**, or an explicit statement that the members were
  spot-checked and which ones.
- **Opening what the claim cites does not discharge a quantified claim.** "I opened the fixture"
  and "I enumerated the members" are different entries, and the row has room for both. The
  failure this exists for: the same universal was audited **true** three times, honestly, from
  the family's shared fixture, and was false in the one member nobody opened (F-095).
- Where a family genuinely cannot be enumerated, the legal move is to **weaken the sentence**
  until it is a cited fact — never to record the enumeration as done. A universal nobody can
  enumerate is a universal nobody can check.

`scripts/lint-claims` decides the **shape**: a sentence carrying a quantifier over a named set
has an enumeration entry in its audit row. Whether the enumeration is **complete** is a read, and
the row is what makes that read attributable rather than a verdict.

### Engagement-state sentences live in a delimited section

A sentence asserting the state of the **engagement** rather than the state of the product — "the
stakeholder has not yet been asked to accept this", "this is the only remaining gap", "three of
four work items are delivered" — is neither a record nor a deliverable. No code change makes it
true or false; the pipeline's own ending does. No item can own one, because the thing it
describes outlives every item, and by the time it is false every item is closed (F-093).

1. Every engagement-state sentence lives inside a **delimited section**: exactly one
   `## Engagement state` section per document, holding that document's engagement-state
   sentences and nothing else. One section per document, marked, so the set of them in a
   workspace is enumerable by a script rather than by a reading.
2. `intake` writes the initial one. Between then and the ending, **no execution writes one.** An
   execution whose change would falsify one records that entry in its plan's invalidation set
   with the disposition `owned-by-ending` (`dor-dod.md` D7) and moves on.
3. At the ending, and **after** the sign-off question is answered — the answer is itself part of
   the engagement's state — `review-close` restates **every** `## Engagement state` section in
   the workspace, from the ending it is recording. Not the ones it noticed: all of them. The job
   is bounded precisely because of rule 1.
4. **No item-level audit is charged with one.** `dor-dod.md` D7 and D12 exclude them and DE4
   owns them. An item asked to repair an engagement-state sentence has been handed a defect it
   is structurally unable to fix.

Three of those are mechanical — that the sections exist, that nothing but `intake` and an ending
wrote inside one, that the ending restated each. Whether a restated sentence is **true** is a
person's read of the ending and always will be. And one thing no gate sees at all: whether a
sentence that *is* an engagement-state sentence was written **into** the section rather than
loose in the body. Everything mechanical above rests on that, and F-093's own sentence was
written loose.

These mechanical halves are new with revision 5. They are `scripts/lint-claims`' and
`scripts/validate-workspace`'s to decide; a workspace whose scripts predate this revision has
only the read.

---

## 5. Which skill writes what

| Document | Created by | Updated by |
|----------|-----------|-----------|
| `product/vision.md` | `intake` | `refine`, `answer-questions` |
| `product/prd.md` | `intake` or `refine` | `refine`, `answer-questions` |
| `architecture/overview.md` | `plan` | `plan`, `answer-questions` |
| `architecture/adr/*` | `plan` or `answer-questions` | the **decision**: superseded only (§4). The **document**: `## Corrections`, append-only, for provenance and errata (§4b) |
| `process/ways-of-working.md` | `plan` | `review-close`, `answer-questions` |

The table is the ordinary path. The rule underneath it, which decides the cases the table does
not list, is this (derived in ADR-0010 §3):

> `verify` does not write to `docs/`. `implement` writes to `docs/` only within the invalidation
> set and deliverable set its plan declared (`dor-dod.md` D7), never a sentence that is the
> standard its own work is judged against, and never a claim sourced to a human answer.

**`verify`'s half is derived, not asserted.** `verify` judges a change against criteria it did
not write. An execution that may also repair the document it is judging has made the judgement
circular — more so than for `implement`, which at least has a plan telling it what to write. So
`verify` writes no document, ever: if it concludes a document is wrong, that is a question
(`question.md`), and `answer-questions` makes the edit. `retro` writes no document either, for
the neighbouring reason — a retrospective that edits the record it is reading has changed the run
it observed.

**`implement`'s half is what changed, and it is a real weakening of a real rule.** The
circularity objection was never "`implement` writes prose"; it is that *the execution trying to
satisfy a requirement must not be the one that rewrites the requirement*. That objection is about
a document's **record** half — a statement about what happened or was decided, which later work
can only add to — and it says nothing about its **deliverable** half, a statement about the
product as it now is, which the next change can make false and which an item can be asked to
produce. The two are properties of sentences, not of files, and one file holds both. `implement`
is the only actor whose ordinary work falsifies a deliverable sentence, and forbidding it to
repair one left that repair with no owner: an item whose acceptance criterion is *about* a
document had no skill the pipeline dispatches that was allowed to deliver it (F-057), and
`implement`'s claims gate examined a window that was empty by construction on every execution
(F-076).

So `implement` may write a deliverable sentence, bounded three ways, and every bound is checkable:

- the write is inside the **invalidation set** or the **deliverable documents** its plan declared
  (`dor-dod.md` D7) — a diff under `docs/` against that set is decidable by a script;
- it is never a sentence that is the standard its own work is judged against — that standard is
  the item's acceptance criteria, not the document it delivers;
- a claim sourced to a human answer is not `implement`'s to rewrite, whatever the set says. It
  files the question, exactly as `review-close` must (`question.md` §2).

The same directory-as-proxy error appears in the freshness comparison, which exempts `docs/`
wholesale and so excludes the delivered thing on an item whose deliverable is a document (F-058).

---

## Revisions

| # | Date | Change |
|---|------|--------|
| 1 | 2026-08-17 | Initial. |
| 2 | 2026-08-22 | §4a added: absolute claims about named code carry a resolvable `[src: ...]` citation (F-001). |
| 3 | 2026-08-29 | §4b added: a standing ADR is repaired in place through an append-only `## Corrections` section — `provenance` or `erratum`, never a change to what the code must do. §5's ADR row says which half is superseded-only (F-067). |
| 4 | 2026-08-30 | §4b: a superseded ADR takes no **new** correction and keeps the ones it made — the rule is about the act, not the state, and as a state rule it described a document that could not exist. §4a: rule 2 does not read a superseded document, which has no legal way to gain a citation (F-069). |
| 5 | 2026-09-10 | §5's absolute — "`implement` and `verify` do **not** write to `docs/`" — is replaced by a rule scoped to the record half: `verify` writes no document (now **derived**, not asserted), `implement` writes only inside the invalidation set and deliverable documents its plan declared (F-076, F-057; the freshness gate's `docs/` exemption is the same directory-as-proxy error, F-058). §4a: the citation is one obligation of three — a **quantified** claim is discharged by member enumeration recorded in the audit row, never by opening what it cites (F-095), and **engagement-state** sentences live in a delimited `## Engagement state` section owned by the ending (F-093). Derived in ADR-0010. |
