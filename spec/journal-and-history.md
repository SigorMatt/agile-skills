# `journal.md` and `history.md` — the append-only record

These two files are what makes a run auditable. Between them they answer, for any item:
**what happened, in what order, why, and which skill decided it** — R4's quality bar.

They are split because they answer different questions at different resolutions. `history.md`
is the timeline a manager scans: six columns, one line per state change. `journal.md` is the
detail a reviewer reads when a line in that timeline looks wrong.

Both are **append-only**. Never reorder, never rewrite, never tidy. A wrong entry is corrected
by a later entry that says what was wrong; a rewritten entry destroys the only evidence that
anything went wrong at all.

There is exactly **one** sanctioned exception, and it exists because appending genuinely cannot
fix the situation it addresses: when an earlier entry was stamped with a wrong clock, the last
one is legitimately earlier than the one before it, the item can never move again, and no later
entry can repair the pair. The tool that owns the file may restamp that single `when`, to a value
not earlier than its predecessor, and the caller MUST journal it as a correction naming the old
value, the new value, and the reason. Nothing else may be changed, and nothing else may be
touched. The exception applies to **both** files — `history.md`'s last row and `journal.md`'s
last entry heading — and each has one tool that may perform it. If you find yourself wanting a
second exception, you want a journal entry instead.

---

## 0. Every self-reported field comes from a machine

A record is auditable because each claim in it can be checked against something. A test result
has an exit code behind it; a decision has an artifact; a commit has a sha. **Timestamps,
skill versions and personas have nothing behind them** — which is exactly why, in four real
runs, they were the fields that got invented. One run stamped its final eleven entries across a
leisurely next morning for work that had finished in minutes the night before; another recorded
a skill version two patches below the one that was installed. Both records would pass a reading;
neither describes what happened.

So, normatively:

- A timestamp MUST be **read from a clock at the moment it is written**. It MUST NOT be
  estimated, inferred from surrounding entries, or chosen to look plausible. An agent that
  cannot run a clock cannot write a record entry — that is a stop, not a licence to guess.
- The heading fields of a journal entry — timestamp, skill name, version, persona — MUST come
  from a mechanical source: the clock, and the acting skill's own installed contract. They are
  not fields a worker types.
- The tools exist so that this is cheap rather than disciplined: the entry heading is written by
  the journal-entry tool, and the tool that appends a history row writes the matching entry when
  asked to, so the row and the entry cannot disagree about what moved or when.
- A validator MUST reject a recorded time that no clock could have produced — one in the future,
  or one outside the window in which the workspace's repository shows any activity at all.

---

## 1. `history.md`

A markdown table. The header and separator are written once when the file is created; every
transition appends exactly one row.

```markdown
# History — WI-0007

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-16T09:12:04Z | — | draft | intake | — | created from idea refinement for EP-001 |
| 2026-08-16T09:58:11Z | draft | ready | refine | — | Definition of Ready passed, 4 questions resolved |
| 2026-08-16T10:20:03Z | ready | planned | plan | — | plan.md written; ADR-0002 recorded |
| 2026-08-16T10:41:27Z | planned | in-progress | implement | — | branch wi/WI-0007 created |
| 2026-08-16T11:05:52Z | in-progress | awaiting-answer | implement | in-progress | Q-001 blocking: tie-break order undefined |
| 2026-08-16T11:19:40Z | awaiting-answer | in-progress | answer-questions | — | Q-001 answered; AC2 updated |
| 2026-08-16T11:47:52Z | in-progress | verifying | implement | — | gates green; impl-report.md written |
```

| Column | Rules |
|--------|-------|
| `when` | UTC ISO-8601 to the second. MUST be ≥ the previous row's `when`. |
| `from` | The previous row's `to`. On the first row it MUST be `—`. |
| `to` | A status legal for this item's `type`. |
| `actor` | The **skill name** that made the change. Never a person, never a model. |
| `resume-to` | The status to return to. MUST be a status on a transition *into* `awaiting-answer` or `blocked`; MUST be `—` otherwise. |
| `reason` | One line. MUST say what caused the change, not restate it. `"moved to verifying"` is not a reason; `"gates green; impl-report.md written"` is. |

Validation rules:

- `from` MUST chain: row *n*'s `from` equals row *n−1*'s `to`. A break is reported as
  `history.gap` and means something changed `status` without going through a skill.
- The last row's `to` MUST equal the item's current `status` in `item.md`.
- Every transition MUST be legal per `ids-and-statuses.md` §4, with a matching `actor`.
- A row whose `to` is `done` MUST be the last row **for a `work-item` or a `bug`**. An epic may
  be reopened (`ids-and-statuses.md` §3.4), so a `done → open` row may follow one on an epic;
  nothing else may.
- Timestamps MUST be non-decreasing. The tool that appends a row is responsible for this: it
  MUST stamp the row no earlier than the previous row, and MUST say so when it has had to.
  One artifact stamped by hand with a local time labelled `Z` would otherwise make every
  subsequent row on that item look out of order, and the item would be unable to move at all.

### Why `actor` is a skill and not a person

A run is executed by an agent playing several roles. Recording "the agent" tells a reader
nothing; recording `verify` tells them which contract was in force, which inputs were required,
and which gates should have run. When a run goes wrong, this column is the first thing that
localises the fault to a skill — which is the whole debugging loop the vision asks for.

---

## 2. `journal.md`

One entry per **skill execution**, appended when that execution finishes — including when it
finishes by failing or by escalating. An execution that produced no entry is indistinguishable
from an execution that never happened.

### 2.1 Entry format

```markdown
## 2026-08-16T11:47:52Z — implement v0.1.0 — developer

- **Item:** WI-0007
- **Trigger:** status `in-progress`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0007/item.md`
  - `tracker/items/WI-0007/artifacts/plan.md`
  - `docs/architecture/overview.md` (v3)
- **Decisions:**
  - Sorted with a stable sort so AC2's tie-break falls out of the comparator rather than a
    second pass. Rationale: one comparison function is the only place the order is defined.
  - Did not extract a shared formatter yet — one caller, so it would be speculative.
- **Questions raised:** `Q-001` (blocking, to architect) — answered before this entry
- **Commands:**
  - `python3 -m pytest tests/ -q` → exit 0, 14 passed
  - `python3 -m ruff check .` → exit 0
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m pytest -q`, exit 0)
  - `no-lint-errors` → **pass** (`python3 -m ruff check .`, exit 0)
  - `acceptance-criteria-addressed` → **pass** (AC1–AC4 each mapped to a test in impl-report.md)
- **Artifacts:**
  - `tracker/items/WI-0007/artifacts/impl-report.md` (new)
  - commit `a1b2c3d` on `wi/WI-0007`
- **Status:** `in-progress` → `verifying`
- **Result:** Implementation complete; handing to verification.
```

### 2.2 Required elements

The heading MUST be:

```
## <timestamp> — <skill-name> v<skill-version> — <persona>
```

and the entry MUST contain these bullets, with these exact labels:

| Bullet | Content |
|--------|---------|
| `**Item:**` | the item ID this execution acted on |
| `**Trigger:**` | the status that made this skill runnable, and what dispatched it |
| `**Inputs read:**` | every artifact actually read. Not the contract's list copied out — what was read |
| `**Decisions:**` | each decision with its rationale. Empty is legal only as the literal `none` |
| `**Questions raised:**` | question IDs filed by this execution, or `none` |
| `**Commands:**` | every command run, with its exit code or outcome. `none` is legal |
| `**Gates:**` | every gate in the contract, each `pass` / `fail` / `skipped`, with the evidence |
| `**Artifacts:**` | every file created or updated, and any commit produced |
| `**Status:**` | `from` → `to`, matching the history row this execution appended |
| `**Result:**` | one or two sentences a reader can stop at |

Rules:

- Entries MUST be in non-decreasing timestamp order.
- A gate listed in the skill's contract MUST appear under `**Gates:**`, even when it was
  skipped — with the reason it was skipped. A silently omitted gate is the failure this format
  exists to prevent: an execution that reports success while never having run the check.
- `**Decisions:**` MUST record the rationale, not only the choice. "Used a stable sort" is a
  fact; "used a stable sort so the tie-break lives in one comparator" is a decision. A reader
  auditing the run needs to know whether the reasoning was sound, not merely what happened.
- A failed execution still writes an entry, with the failing gate, what was tried, and the
  status it moved the item to (`blocked`, `awaiting-answer`, or unchanged).
- The entry MUST be written by the journal-entry tool, which owns the heading (§0). An entry
  that accompanies a status change is written by the transition tool in the same invocation, so
  that `**Status:**` states the move that was actually made rather than the move that was
  intended. An entry that accompanies no status change is written on its own, and its
  `**Status:**` says `X` → `X` (unchanged).

### 2.3 Journals on epics

An epic's `journal.md` records executions that acted on the *epic*: `intake` creating it and
its first items, `answer-questions` making a decision that changed the epic's scope, and
`review-close` closing it. Item-level detail stays on the item.

---

## 3. What a reader should be able to do

Given only these files, a reader who was not present MUST be able to answer:

1. What was asked for, and how did the understanding of it change over time?
2. Which skill made each decision, and on what basis?
3. What was run, and what did it produce?
4. Which gates passed, which failed, and what happened next?
5. Where did work stop, and what is it waiting on?

If any of those cannot be answered from the record, the record is defective — not the reader.
That is the test `examples/toy-project/AUDIT.md` applies to a real run.

---

## Revisions

| # | Date | Change |
|---|------|--------|
| 1 | 2026-08-17 | Initial. |
| 2 | 2026-08-22 | §0 added: every self-reported header field comes from a machine, timestamps are read from a clock and never estimated, and the restamp exception now covers `journal.md` as well as `history.md` (F-017). |
