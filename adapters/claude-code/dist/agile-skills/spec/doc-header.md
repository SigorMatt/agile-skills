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
- An ADR at `status: superseded` is **not** corrected. It records what was believed then, and it
  is no longer the document a reader acts on.
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

The absolute-claim rule is checked against **what an execution touched**, not against the whole
tree — the same scoping `dor-dod.md` applies to D7 and D12. A record written before this
convention existed is not retroactively invalid; the next execution that edits a document is the
one that must source what it writes.

---

## 5. Which skill writes what

| Document | Created by | Updated by |
|----------|-----------|-----------|
| `product/vision.md` | `intake` | `refine`, `answer-questions` |
| `product/prd.md` | `intake` or `refine` | `refine`, `answer-questions` |
| `architecture/overview.md` | `plan` | `plan`, `answer-questions` |
| `architecture/adr/*` | `plan` or `answer-questions` | the **decision**: superseded only (§4). The **document**: `## Corrections`, append-only, for provenance and errata (§4b) |
| `process/ways-of-working.md` | `plan` | `review-close`, `answer-questions` |

`implement` and `verify` do **not** write to `docs/`. If either concludes that a document is
wrong, that is a question (`question.md`), and `answer-questions` makes the edit. Otherwise the
authoritative record would be updated by the same execution that is trying to satisfy it, and
the check would be circular.

---

## Revisions

| # | Date | Change |
|---|------|--------|
| 1 | 2026-08-17 | Initial. |
| 2 | 2026-08-22 | §4a added: absolute claims about named code carry a resolvable `[src: ...]` citation (F-001). |
| 3 | 2026-08-29 | §4b added: a standing ADR is repaired in place through an append-only `## Corrections` section — `provenance` or `erratum`, never a change to what the code must do. §5's ADR row says which half is superseded-only (F-067). |
