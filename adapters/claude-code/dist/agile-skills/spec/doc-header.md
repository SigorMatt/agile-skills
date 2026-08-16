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

## 5. Which skill writes what

| Document | Created by | Updated by |
|----------|-----------|-----------|
| `product/vision.md` | `intake` | `refine`, `answer-questions` |
| `product/prd.md` | `intake` or `refine` | `refine`, `answer-questions` |
| `architecture/overview.md` | `plan` | `plan`, `answer-questions` |
| `architecture/adr/*` | `plan` or `answer-questions` | superseded only |
| `process/ways-of-working.md` | `plan` | `review-close`, `answer-questions` |

`implement` and `verify` do **not** write to `docs/`. If either concludes that a document is
wrong, that is a question (`question.md`), and `answer-questions` makes the edit. Otherwise the
authoritative record would be updated by the same execution that is trying to satisfy it, and
the check would be circular.
