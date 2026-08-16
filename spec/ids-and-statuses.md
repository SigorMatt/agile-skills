# Identifiers, item types, and the status graph

Normative. `scripts/validate-workspace` enforces every rule on this page.

## 1. Identifier formats

| Kind | Format | Example | Scope of uniqueness |
|------|--------|---------|---------------------|
| Epic | `EP-` + 3 digits | `EP-001` | whole workspace |
| Work item | `WI-` + 4 digits | `WI-0007` | whole workspace |
| Bug | `BUG-` + 4 digits | `BUG-0003` | whole workspace |
| Question | `Q-` + 3 digits | `Q-002` | the owning item only |
| Architecture decision | `ADR-` + 4 digits | `ADR-0004` | whole workspace |

Rules:

- Numbers MUST be sequential from `1`, zero-padded to the width above.
- An ID MUST NOT be reused, even if the artifact it named was abandoned. Abandoned items are
  set to `done` with an outcome of `dropped` (see `work-item.md`), never deleted. A reused ID
  would silently rewrite history in `git log --grep`.
- A question ID is scoped to its item, so `WI-0007/questions/Q-001.md` and
  `WI-0009/questions/Q-001.md` are different questions. A question is therefore cited as
  `WI-0007/Q-001` wherever the item is not already obvious from context.

### 1.1 Allocating the next ID

The next ID for a kind is **derived from the filesystem**: take the highest number currently
present across the workspace for that kind — including items already `done` — and add one.

There is deliberately no counter file. A counter is a second source of truth that drifts the
first time a run is interrupted between "increment the counter" and "create the directory",
and the drift is invisible. Derivation is idempotent and self-healing: re-deriving after a
crash gives the same answer as deriving before it. See `meta/adr/ADR-0003` for the full
argument.

Allocation MUST scan, in one pass:

- `tracker/items/*/` directory names, for `EP-`, `WI-`, `BUG-`;
- `tracker/items/*/questions/Q-*.md`, for that item's `Q-`;
- `docs/architecture/adr/ADR-*.md`, for `ADR-`.

## 2. Item types

Every tracked entity is a directory under `tracker/items/<ID>/`, whatever its type. One uniform
shape means one validator, one board generator, and one journal format.

| `type` | ID kind | What it is | Parent |
|--------|---------|-----------|--------|
| `epic` | `EP-` | A goal that groups work items. Holds the product-level narrative. | none |
| `work-item` | `WI-` | A unit of deliverable change with its own acceptance criteria. | an epic |
| `bug` | `BUG-` | A defect found against already-delivered behaviour. | an epic; and links the item it was found against |

A `work-item` MUST name an `epic`. A `bug` MUST name an `epic` and SHOULD name the work item
whose delivered behaviour it contradicts, via `found-in`.

## 3. Statuses

### 3.1 Statuses for `work-item` and `bug`

| Status | Meaning | Owning skill | Terminal |
|--------|---------|--------------|----------|
| `draft` | Created, but not yet proven to meet the Definition of Ready. | `refine` | no |
| `ready` | Meets the Definition of Ready. Needs a design and a plan. | `plan` | no |
| `planned` | A plan exists and has been recorded. Needs implementation. | `implement` | no |
| `in-progress` | Implementation has started. Also the resume point after an interruption. | `implement` | no |
| `verifying` | Implementation reports itself complete. Needs independent validation. | `verify` | no |
| `in-review` | Verified. Needs review against the Definition of Done, then closing. | `review-close` | no |
| `awaiting-answer` | A blocking question is open. No engineering may proceed. | `answer-questions` | no |
| `blocked` | A documented impasse that no skill can resolve. | none — a human must act | yes |
| `done` | Closed. Carries an `outcome`. | none | yes |

### 3.2 Statuses for `epic`

| Status | Meaning | Owning skill | Terminal |
|--------|---------|--------------|----------|
| `open` | Has child items that are not all `done`. | none — epics advance through their children | yes* |
| `awaiting-answer` | A blocking question about the epic's own scope is open. | `answer-questions` | no |
| `blocked` | Every child is blocked or awaiting a human. | none — a human must act | yes |
| `done` | Every child item is `done`, and the epic has been closed with an outcome. | none | yes, but reopenable — see §3.4 |

\* "Terminal" here means *the orchestrator never dispatches a skill against an open epic
directly*. An epic is closed by `review-close` as the final act of closing its last open child
item — the only place where the state of every sibling is already being examined.

### 3.3 Why `in-progress` exists as a distinct status

`planned` and `in-progress` share an owning skill. The distinction is not bureaucratic: it is
what makes an interrupted run recoverable. `planned` means no branch and no code exist yet, so
starting over is free. `in-progress` means a branch exists and partial work is on it, so the
skill MUST reconcile with what is already there rather than starting again. A single status
could not carry that difference, and the recovery behaviour would depend on the agent guessing.

### 3.4 A closed epic can be reopened

`done` is terminal for a `work-item` and a `bug`: once closed, that unit of work is finished,
and a later defect is a *new* item. An **epic** is different, and the difference is not
cosmetic. An epic states a goal. If a defect is later found in the behaviour that epic
delivered, the goal is no longer met — and the defect must be filed under that epic, because
that is the goal it violates.

So a `done` epic MAY return to `open`, by any skill, when a child item is filed against it after
it closed. The transition is recorded like any other, and the reason names the item that caused
it. When that item closes, `review-close` applies the epic Definition of Done again and may
close the epic again.

The alternative — forbidding it — was tried and produces a lie: `validate-workspace` reports
`epic.closed-with-open-children`, and the only ways to silence it are to file the bug under a
different epic (breaking the link between the defect and the goal it violates) or not to file it
at all. A methodology that makes "do not record the defect" the path of least resistance has
chosen the wrong invariant. This was found by an independent regression pass against a closed
epic, not by reasoning about it.

## 4. Legal transitions

Every row is the only legal way to reach that status. Any other transition is invalid and
`scripts/validate-workspace` reports it by reading `history.md`.

| From | To | Actor skill | Condition |
|------|----|-------------|-----------|
| — | `draft` | `intake` | item created from a refined idea |
| — | `ready` | `verify` | a bug filed with reproduction steps already satisfies the bug Definition of Ready |
| `draft` | `ready` | `refine` | Definition of Ready passes, or the human explicitly overrides |
| `ready` | `planned` | `plan` | design recorded and plan written |
| `planned` | `in-progress` | `implement` | branch created, work started |
| `in-progress` | `verifying` | `implement` | implementation gates pass and the report is written |
| `verifying` | `in-review` | `verify` | verification passes against the acceptance criteria |
| `verifying` | `in-progress` | `verify` | verification fails on this item's own acceptance criteria |
| `in-review` | `done` | `review-close` | Definition of Done passes and the change is merged |
| `in-review` | `in-progress` | `review-close` | review rejects the change with recorded reasons |
| *any non-terminal* | `awaiting-answer` | `implement`, `verify`, `plan`, `review-close` | that skill filed a blocking question |
| `awaiting-answer` | *the status it came from* | `answer-questions` | the blocking question is answered and its consequences are propagated |
| *any non-terminal* | `blocked` | any skill | a documented impasse no skill can resolve |
| `blocked` | *the status it came from* | any skill | a human recorded a resolution in the item |
| `open` | `done` | `review-close` | epic only: every child item is `done` |
| `done` | `open` | any skill | epic only: a defect was filed against the epic's delivered behaviour after it closed (§3.4) |
| *any* | `blocked` | any skill | epic only, or as above |

Notes:

- **`awaiting-answer` remembers where it came from.** The history entry MUST record the status
  being suspended, and `answer-questions` MUST restore exactly that status. Otherwise an item
  interrupted during `verify` would silently restart at `implement`, and the verification
  evidence already gathered would be quietly discarded.
- **`verifying → in-progress` is a rejection, not a bug.** A failure of *this item's own*
  acceptance criteria sends the item back. A defect in *previously delivered* behaviour is a
  new `bug` item instead, and this item continues. `verify`'s process defines the test.
- **Skills change statuses. Nothing else does.** A human editing `status:` by hand produces a
  history gap, and the validator reports it as `history.gap`.

## 5. Priority

`priority` MUST be one of `critical`, `high`, `medium`, `low`.

| Value | Rank | Meaning |
|-------|------|---------|
| `critical` | 1 | Blocks everything else; the epic cannot ship without it. |
| `high` | 2 | Required for the epic's stated outcome. |
| `medium` | 3 | Wanted, but the epic is coherent without it. |
| `low` | 4 | Opportunistic. |

Rank orders the orchestrator's choice of what to run next. The tie-break after rank is the
oldest `created` timestamp, and after that the lexicographically smallest ID — so the choice is
fully deterministic and two runs over the same workspace pick the same item. Randomness here
would make an interrupted run unreproducible, which is the one thing the whole design is
protecting.
