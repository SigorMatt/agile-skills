# `item.md` — the tracked item

Every directory under `tracker/items/<ID>/` MUST contain exactly one `item.md`. It is the
item's identity card: what is wanted, how we will know it is done, and where it stands.

It is **not** a log. Nothing that happened goes here — that is `journal.md` and `history.md`.
The distinction matters when reading: `item.md` answers *what and why*, the logs answer *what
happened and when*.

## 1. Frontmatter

```yaml
---
id: WI-0007
type: work-item
title: Report a per-file line count in the summary
status: verifying
priority: high
epic: EP-001
created: 2026-08-16T09:12:04Z
updated: 2026-08-16T11:47:52Z
branch: wi/WI-0007
depends-on:
  - WI-0004
---
```

| Field | Required | Type | Rules |
|-------|----------|------|-------|
| `id` | always | string | MUST match the directory name and the format in `ids-and-statuses.md` |
| `type` | always | enum | `epic` \| `work-item` \| `bug`; MUST agree with the ID prefix |
| `title` | always | string | one line, ≤ 80 characters, imperative or declarative, no trailing period |
| `status` | always | enum | a status legal for this `type` (`ids-and-statuses.md` §3) |
| `priority` | always | enum | `critical` \| `high` \| `medium` \| `low` |
| `epic` | `work-item`, `bug` | ID | MUST name an existing epic. MUST be absent on an epic |
| `created` | always | timestamp | UTC ISO-8601 to the second; set once, never changed |
| `updated` | always | timestamp | bumped by every skill that writes the item |
| `branch` | once code exists | string | `wi/<ID>`; set by `implement` when it creates the branch |
| `outcome` | when `status: done` | enum | `delivered` \| `dropped` \| `duplicate` |
| `found-in` | `bug`, when known | ID | the work item whose delivered behaviour the bug contradicts |
| `depends-on` | optional | list of IDs | this item cannot start until those are `done` |
| `blocks` | optional | list of IDs | informational mirror of another item's `depends-on` |
| `relates-to` | optional | list of IDs | non-blocking association |

Rules that a validator enforces:

- Unknown frontmatter fields are an **error**, not a warning. A typo'd `piority:` that validated
  clean would leave the board silently wrong.
- `depends-on`, `blocks` and `relates-to` MUST reference items that exist. A dangling reference
  is an error.
- `depends-on` MUST NOT contain a cycle.
- `outcome` MUST be present if and only if `status` is `done`.
- `branch` MUST be present once `status` has ever been `in-progress` or later.
- `updated` MUST NOT be earlier than `created`, and MUST NOT be earlier than the timestamp of
  the last `history.md` entry.

## 2. Body — `work-item`

Required headings, in this order:

```markdown
## Story

As a <role>, I want <capability>, so that <outcome>.

## Acceptance criteria

- [ ] AC1 — <observable, testable statement>
- [ ] AC2 — <observable, testable statement>

## Out of scope

- <what a reader might reasonably assume is included, and is not>

## Notes

<optional context; links to docs; constraints discovered during refinement>
```

- **`## Story`** MUST state a role, a capability and an outcome. "so that" is where refinement
  usually finds the real requirement, which is why it is mandatory rather than encouraged.
- **`## Acceptance criteria`** MUST be a markdown checkbox list, at least one item, each
  labelled `AC<n>`. Each criterion MUST be decidable by observation — a command to run, an
  output to inspect, a file to look at. "Works well" is not a criterion; `refine` rejects it.
  - `verify` ticks a box only when it has evidence for it, and cites that evidence in
    `artifacts/verify-report.md`.
  - `review-close` MUST NOT close an item with an unticked box.
  - Once an item is past `ready`, criteria MUST NOT be edited except by `answer-questions`
    propagating an answer, or by `refine` on an item that was sent back. Every such edit is
    journaled with the reason. Silently loosening a criterion to make verification pass is the
    single most damaging thing a pipeline like this can do, so it is called out here rather
    than left to good taste.
- **`## Out of scope`** SHOULD be present. It is the cheapest defence against scope drift
  during `implement`, and its absence is a warning.

## 3. Body — `bug`

```markdown
## Summary

<one paragraph: what is wrong, observed where>

## Steps to reproduce

1. <exact command or action>
2. ...

## Expected behaviour

<what the acceptance criteria of the originating item, or the docs, say should happen>

## Actual behaviour

<what happens instead, verbatim: output, error text, exit code>

## Acceptance criteria

- [ ] AC1 — the steps above produce the expected behaviour
- [ ] AC2 — a regression test covers this case and fails without the fix

## Notes
```

- **`## Steps to reproduce`** MUST be a numbered list a reader can follow without asking
  anything. "Run the tests" is not a step; the exact command is.
- **`## Actual behaviour`** MUST quote real output rather than paraphrase it.
- A bug's `AC2` (a regression test) is required unless the item's `## Notes` records why the
  behaviour cannot be tested. `verify` checks this.

## 4. Body — `epic`

```markdown
## Goal

<one paragraph: the outcome for the user, not the implementation>

## Why now

<the problem this solves and the cost of not solving it>

## Success measures

- <observable signal that the goal was met>

## Scope

- <the shape of the work>

## Out of scope

- <deliberate exclusions>
```

An epic MUST NOT contain a hand-maintained list of its child items. Children are derived from
the `epic:` field of every item, and a second, hand-written list would drift from it within one
work item. `tracker/board.md` shows the real one.

## 5. Worked example

```markdown
---
id: WI-0007
type: work-item
title: Report a per-file line count in the summary
status: ready
priority: high
epic: EP-001
created: 2026-08-16T09:12:04Z
updated: 2026-08-16T09:58:11Z
---

## Story

As someone reviewing a directory of source files, I want the summary to show a line count for
each file, so that I can see which files dominate the total without opening them.

## Acceptance criteria

- [ ] AC1 — `wc-tool summarise <dir>` prints one row per regular file, with its line count
- [ ] AC2 — rows are sorted by descending line count, ties broken by filename ascending
- [ ] AC3 — a directory containing no regular files prints `no files` and exits 0
- [ ] AC4 — a path that does not exist prints an error to stderr and exits 2

## Out of scope

- Recursing into subdirectories; that is WI-0009.
- Counting anything other than newline-terminated lines.

## Notes

Refinement established that "line" means newline-terminated, and that a final line without a
trailing newline still counts — see `questions` on this item and `artifacts/refinement-qa.md`.
```
