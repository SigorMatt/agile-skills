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
- The top row **is** the header. Its `when`, `by` and `for` MUST equal the frontmatter's
  `updated`, `updated-by` and `updated-for`; a document that describes its own latest version
  two ways is wrong in one of them.
- `by` names a skill the pipeline declares, and `for` names an item in this workspace or the em
  dash. Never a person and never a model — the reason is `journal-and-history.md` §1.

### What is checked, and what is not

A row's `when`, `by` and `for` are the three fields `journal-and-history.md` §0 exists for: a
clock, a skill, and an item, self-reported, with nothing behind them. §0 now reaches this table,
and the honest split is worth stating rather than leaving a reader to assume the whole row is
guarded.

| Claim | Decided by |
|-------|-----------|
| the top row and the header agree | **[auto]** `validate-workspace` — `doc.changelog.header` |
| `when` is a UTC timestamp a clock could have produced | **[auto]** — `doc.changelog.when`, `doc.changelog.timestamp.*` |
| `by` is a skill this pipeline has | **[auto]** — `doc.changelog.actor` |
| `for` is an item in this workspace | **[auto]** — `doc.changelog.for` |
| that skill **was executing on that item** at that time | **[auto]** — `doc.changelog.no-execution`, matched against the named item's `journal.md`, while that item is not yet `done` |
| the version **number** is the right one | **[skill]** — a change may deserve one bump or none, and no program can say which |
| `what changed` describes what changed | **[skill]** — "Updated" passes every mechanical test there is |
| the named skill made **this** edit | **[skill]** — the check establishes that an execution of it was running, not that this edit was its work |

The execution match is asked only while the item the row names is **not yet `done`**, and the
line is deliberate: a row on a closed item is history, and demanding its repair is a demand to
rewrite a record rather than to improve one. It costs nothing that matters, because every skill
runs the validator and a row is written during the item's life — the next gate run after it is
written is inside the window. A row whose `for` is the em dash is matched against nothing, and
that is the price of the escape hatch (F-084).

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
| acceptance criterion | `[src: WI-0007 AC3]`, `[src: WI-0007 AC3 "sorted by descending line count"]` | the item declares that AC — and, when the citation quotes words, that AC still says them |
| question | `[src: WI-0007/Q-002]` | the question file exists |
| ADR | `[src: ADR-0004]` | an ADR with that number exists |
| commit | `[src: commit a1b2c3d]` | the commit is in this repository |
| command outcome | `[src: run: python3 -m pytest -q → exit 0, 14 passed]` | it records both the command and its outcome |

Several sources are separated by `;` inside one marker. `scripts/lint-claims` enforces both
rules and is a hard gate on `plan`, `implement` and `review-close`; `scripts/validate-workspace`
enforces the resolution rule over the whole workspace, at any time.

### A criterion's number is a position, not a name

`AC7` is where a criterion sits in a list. Renumbering that list is legal and cheap while an item
is being refined, and when it happens every standing `ITEM AC7` elsewhere silently starts pointing
at a different criterion. It still **resolves**, which is worse than failing: the gate reports
success. It has happened — one item's criteria were renumbered twice at `draft`, and two citations
in a sibling item were left naming criteria nobody had written when they were filed (F-094).

So the citation may carry the criterion's own **words**, quoted, and that is what a renumbering
cannot move:

- an **anchored** citation — `[src: WI-0002 AC7 "sorted by descending line count"]` — resolves
  only while AC7 still says those words. Comparison ignores whitespace, case and backticks, and
  the quoted text may be any run of the criterion, so quoting the distinctive half is enough. It
  fails loudly the moment the list moves under it.
- an **unanchored** citation is **refused** while the cited item is at `draft` or `ready` — the
  statuses at which `work-item.md` §2 still permits the criteria to be rewritten. There the number
  has not yet become an identity, and the message says so and quotes the criterion's opening words
  back so the anchor can be pasted in.

The quoted text lives inside the marker, so it may contain neither `]` nor `;` — the first ends
the marker and the second separates sources. Quote a run of the criterion that has neither; there
is always one.

What this does **not** catch, said here rather than left to be discovered: an unanchored citation
to an item past `ready` still resolves by number alone, so a criterion edited later by
`answer-questions` propagating an answer can still move under it. Requiring an anchor everywhere
was measured and rejected — 84 existing citations across the examples, the fixtures and the banked
run evidence would have been invalidated retroactively, which §4a's own paragraph above forbids.
The anchor is how an author makes a citation durable; the refusal at `draft` and `ready` is where
the number is provably not one yet.

This is **F-077's disease and not F-077's cure.** There, a `path:line` citation resolved for ever
because the resolver asked whether the *file* existed; the fix bounds the line number by the
file's length. The same bound here — *does the item declare an AC7?* — was already in place, and
it is precisely the check being fooled. A bound cannot tell a moved target from a standing one;
only the target's own content can, which is why the citation has to carry some of it.

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

### The example has to be able to fail

An audit row is passed by an example the same way a gate is passed by an empty window, and it is
the same defect wearing different clothes. `scripts/lib/scope.py` calls that state
*out-of-scope-by-construction*: the comparison did not come up empty, it was never able to come
up otherwise. A claim audit reaches it through the example rather than through the scope — the
auditor picks what to open, and the natural thing to open is the case the sentence was written
from, which is the one case that cannot contradict it.

It has happened twice on one sentence. *"No column's width depends on its marker"* was audited
**holds**, honestly, by laying the same table out under all four markers — a table whose cells
were every one of them wider than any marker, so the rule the sentence denies never applied. The
unit test named for the claim had the same blind spot. The sentence was false, and the example
that shows it is one empty column. Its replacement then passed the item's own two reproduce
commands and was still false, and what caught it was a verifier choosing the boundary instead of
the happy path (F-088).

So the row carries a fifth thing, and it is the one that makes the other four mean something:

- **`Falsifier:`** — what a counterexample would look like, and **why the thing opened could have
  produced one**. Not "I checked and it holds": *the marker only governs a column whose widest
  cell is narrower than the marker itself, and column 3 of the fixture is one character wide, so
  a dependency would have shown here.*
- An absolute about a rule with a **threshold, a boundary or an exception** is checked **at** the
  boundary. The happy path is evidence for the sentence; only the boundary can be evidence
  against it.
- Where the falsifier cannot be produced at all — no member of the family can exhibit it, the
  boundary case does not exist — that is not a pass. It is the same answer §4a already gives for
  a family nobody can enumerate: **weaken the sentence** until it says what was actually checked.

`scripts/lint-documents` decides the **shape**: the label is present and says something. Whether
the example named could really have failed is a read, and it is the read this row exists to make
attributable. One thing it *can* decide is the degenerate case — an enumeration whose `Members:`
names nobody. That audit could not have found a counterexample, and it **passes with a mark**
rather than silently, on `scope.py`'s precedent exactly: a pass that is not an ordinary pass is
never spelled the same as one.

**Where that shape check runs, and where it does not.** It runs where the labelled form is
already gated — `propagated-claims-carry-their-obligation`, over the enumeration entries in an
answering question's `## Consequences`. It does **not** run over `review.md`'s
`## What I examined` or `verify-report.md`, which are the audit rows D12 and DE6 name: nothing
mechanical reads those, before this rule or after it. There the falsifier is an obligation the
skill discharges and records, exactly as the rest of D12's read is, and `dor-dod.md` marks it
`[skill]` for that reason. Under-claiming is the correct failure mode; a gate that overstates
its reach is worse than one that does not exist.

### Quantified claims carry their enumeration

A claim over a family — *every adapter …*, *all three tiers …*, *no caller …*, *the only path …*
— is syntactically one of the absolutes rule 1 already detects, and semantically a different
object: **a citation cannot name the thing that falsifies it.** The citation names the general
case; the falsifier is a member the sentence does not name.

- The audit row for a quantified claim records (a) **the set** the quantifier ranges over,
  (b) **how the set was enumerated** — the command, glob or grep, with its output, so the
  enumeration is repeatable and its completeness is inspectable, (c) **the members**, by name,
  (d) **the verdict per member**, or an explicit statement that the members were
  spot-checked and which ones, and (e) **the falsifier** — what a member that made the sentence
  false would look like, and why the members examined could have exhibited one.
- **Opening what the claim cites does not discharge a quantified claim.** "I opened the fixture"
  and "I enumerated the members" are different entries, and the row has room for both. The
  failure this exists for: the same universal was audited **true** three times, honestly, from
  the family's shared fixture, and was false in the one member nobody opened (F-095).
- Where a family genuinely cannot be enumerated, the legal move is to **weaken the sentence**
  until it is a cited fact — never to record the enumeration as done. A universal nobody can
  enumerate is a universal nobody can check.

The five parts are written as labels, nested under the audit row's own entry, so that the entry
can be found by the reader who needs it and by the script that checks it is there:

```markdown
- `docs/architecture/overview.md` — the rendering sentence added
  - **Enumeration:** "every adapter writes through `render_all()`"
    - **Set:** the adapters under `adapters/`
    - **Enumerated by:** `ls -d adapters/*/` → `one/`, `two/`
    - **Members:** `one`, `two`
    - **Verdict:** both call `render_all()`; true of each
    - **Falsifier:** an adapter with its own `open(...).write(...)`; `two` was written before
      `render_all()` existed and is where one would be, so it was read line by line
```

`scripts/lint-documents` decides the **shape**: a sentence carrying a quantifier over a named set
has an enumeration entry, with those five labels, in its audit row. Whether the enumeration is
**complete**, and whether the falsifier named could really have appeared, are reads, and the row
is what makes those reads attributable rather than a verdict. Without the labels nothing
mechanical can tell *"I opened the fixture"* from *"I enumerated the members"*, and telling those
two apart is the whole of the failure this rule exists for.

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

These mechanical halves are `scripts/lint-documents`' to decide (revision 6); a workspace whose
scripts predate it has only the read.

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
| 6 | 2026-09-10 | §4a: the four parts of a quantified claim's enumeration are written as labelled entries — `Enumeration:` carrying `Set:`, `Enumerated by:`, `Members:` and `Verdict:` — because a shape check needs the parts to be findable, and without a label nothing mechanical distinguishes opening what a claim cites from enumerating what it quantifies over. `scripts/lint-documents` decides that shape and the eight obligations of ADR-0010's enforcement table that had no implementation. |
| 7 | 2026-09-10 | §3: `journal-and-history.md` §0 reaches the change log — the top row and the header must agree, `by` and `for` must resolve, `when` must be a time a clock could have produced, and the row is matched against the journal of the item it names while that item is not yet `done`. The `[auto]`/`[skill]` table says plainly which half of a version row is decidable: the version number and the description of the change are not (F-084). |
| 8 | 2026-09-10 | §4a: a criterion's number is a position, not a name. An `ITEM ACn` citation may quote the criterion's own words, and an anchored citation is checked against them; an unanchored one is refused while the cited item is at `draft` or `ready`, the statuses at which the list may still be rewritten. What it does not catch, and why an anchor is not required everywhere, is stated with it. F-077's disease, not F-077's cure — the bound it added was already in place here and is the check being fooled (F-094). |
| 9 | 2026-09-10 | §4a: an audit row's example must be **able to fail**, and the row says why it could — a fifth label, `Falsifier:`, on the enumeration entry, plus the rule that an absolute about a rule with a boundary is checked **at** the boundary. This is `scope.py`'s out-of-scope-by-construction reached through the example rather than through the scope: the same sentence was audited *holds* twice from cases in which the rule it denies never applied (F-088). An enumeration whose `Members:` names nobody passes **with a mark**, on the same precedent. |
