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
| `merge-commit` | after the merge, on a delivered item | sha | the merge that put `branch` on the trunk; written by `scripts/record-merge`, never by hand |
| `outcome` | when `status: done` | enum | `delivered` \| `dropped` \| `duplicate`; and `delivered-partial`, **epics only** |
| `found-in` | `bug`, when known | ID | the work item whose delivered behaviour the bug contradicts |
| `arose-from` | when the creating skill is not `intake`, unless a bug's `found-in` covers it | citation | what caused this item to exist: `<ITEM>`, `<ITEM>/Q-###`, or `R-###` (`ids-and-statuses.md` §5) |
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
- `outcome: delivered-partial` is legal on an **epic** only. It records ending E2
  (`ids-and-statuses.md` §3.5): the engagement closed with the stakeholder's acceptance and with
  at least one child not delivered. An epic that closes with a child at `blocked` and an outcome
  of `delivered` is overclaiming, and the validator says so (`epic.outcome.overclaims`).
- `arose-from` MUST be present when the item's creation row names an actor other than `intake`
  — except on a bug that carries `found-in`, which already names what caused it — and MUST
  resolve to an item, a question file, or a request file that exists. It is the enforceable half
  of the creation-authority table: it says *why* an item exists, where the actor on the creation
  row says *who* recorded it.
- `branch` MUST be present once `status` has ever been `in-progress` or later.
- `merge-commit` is legal on a `work-item` or `bug` that is `done` with `outcome: delivered` and
  a `branch`, and nowhere else. It records the one fact about a close that is **created after
  the record of it**: the close must precede the merge, because `commits-reference-the-item`
  reads the commits not yet on the trunk and merging empties that range, so the closing journal
  entry is written before the merge commit exists and cannot name it (F-081). `scripts/record-merge`
  writes the field afterwards and writes nothing git has not confirmed — that the sha resolves,
  that it has two or more parents, that it is an ancestor of the trunk, and that it contains the
  item's branch. `validate-workspace` asks the same four questions again on every run, because a
  recorded merge that never happened is worse than an unrecorded one (F-035).
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
  - A criterion is in one of **three** states, and the third is the point of this paragraph:

    | Mark | Means |
    |------|-------|
    | `- [ ]` | not settled |
    | `- [x]` | settled **by the observation the criterion names** |
    | `- [~]` | settled by a **substitution** — the environment could not perform that observation, so something else was observed in its place |

    Some criteria name an observation no execution here can make: a machine restart, a second
    device, a year elapsing. The skill's honest choices are a tick with the substitution declared,
    or an `ambiguous` that costs a round trip on a criterion whose content is decidable — and a
    real run took the tick, declared the substitution in four artifacts, and spelled the box
    `- [x]`, identically to the seven settled directly. Every reader downstream then had to
    re-derive the qualification from prose (F-096). `- [~]` is that mark, where the criterion is.

    A `- [~]` is **settled**: it satisfies D1, `review-close` closes on it, and
    `validate-workspace` exits 0 — and says so in a warning of its own
    (`item.criteria.substituted`) on every run, because a pass that is not an ordinary pass must
    not be spelled the same as one.

    A `- [~]` MUST name, on the criterion itself, a question **on this item**, as
    `[src: <ITEM>/Q-nnn]` (`item.criteria.substitution.unasked`). A criterion the environment
    cannot execute is still the stakeholder's wording, and the substitution is the moment to put
    that wording back to them — while the engagement can still act on the answer, rather than
    disclosing it at sign-off. The question need not be **answered**: the obligation is to ask in
    time, and an open question already holds the engagement short of rest
    (`ids-and-statuses.md` §3.5).

    `verify` writes `- [~]`, and no other skill does — it is the skill that decides a criterion
    against evidence, and the mark is one of its verdicts (`verify`'s step 3). That is a
    `[skill]` rule: nothing here decides *which* skill edited a line.
  - A criterion **names** the artefacts it constrains; it does not count them. *"The suite runs
    unchanged"*, *"exactly one of its 65 tests changes"* and *"exactly `2 + max`"* are the natural
    way to write a regression guard and all three are false the moment the item touches what they
    count — each of those three had to be amended after the code existed (F-089). Name the test,
    the file, the case. Where a count is genuinely wanted, **measure it before writing the
    criterion** and carry the measurement on the criterion as a command-outcome citation,
    `[src: run: python3 -m unittest discover → exit 0, 65 tests]`, so the number has a provenance
    a reader can repeat. `dor-dod.md` R11 is the checklist entry, and it is `[skill]`: nothing
    here can tell a count of project artefacts from a count in the tool's own output.
  - A criterion's **number is not its name**. `AC7` is a position in a list, and the list may
    legally be renumbered while the item is being refined — so a citation elsewhere that says
    `AC7` goes on resolving against whatever moved into that position. `doc-header.md` §4a says
    what a citation must carry to survive that, and what the gate can and cannot tell (F-094).
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

---

## Revisions

| # | Date | Change |
|---|------|--------|
| 1 | 2026-08-27 | §1: `arose-from` provenance for items a skill other than `intake` created (F-029); `outcome: delivered-partial` for an epic that ended at E2 (F-045). Derived in ADR-0006. |
| 2 | 2026-09-10 | §1: `merge-commit` — the sanctioned home for a sha the closing entry could not name, written by `scripts/record-merge` after the merge and re-checked against git on every validation (F-081, F-035). |
| 3 | 2026-09-10 | §2: a criterion's number is a position, not a name — the anchored citation form and its limits are in `doc-header.md` §4a (F-094). The third criterion state `- [~]` — settled by a **substitution**, not by the observation the criterion names. It is a legal close that says so in its own words, and it owes the stakeholder a question on this item while the engagement can still act on the answer (F-096). |
| 4 | 2026-09-10 | §2: a criterion **names** the artefacts it constrains rather than counting them, and a wanted count is measured first and carried as a command-outcome citation (F-089, `dor-dod.md` R11). |
