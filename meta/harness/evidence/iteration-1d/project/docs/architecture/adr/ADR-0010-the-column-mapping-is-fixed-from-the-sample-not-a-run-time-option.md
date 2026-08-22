---
title: The importer is written to the stakeholder's own export; the column mapping is not a run-time option
version: 1
status: current
updated: 2026-08-22T03:33:27Z
updated-by: answer-questions
updated-for: WI-0003
---

# ADR-0010 — The importer is written to the stakeholder's own export; the column mapping is not a run-time option

- **Status:** accepted
- **Date:** 2026-08-22
- **Decided by:** the stakeholder, answering `WI-0003/Q-003`; recorded, with the consequences
  they did not state, by answer-questions (architect), for WI-0003
- **Supersedes:** —

## Context

The importer has to learn four things about the CSV it reads: which column carries the date,
which carries the amount, which becomes the description, and how the date and the amount are
written [src: WI-0003/Q-001]. None of them is derivable from anything in this workspace, and
`ADR-0002` deliberately refused to widen what the hand-entry command accepts in order to make
the import easier, so normalising whatever the bank writes is this item's job
[src: ADR-0002; WI-0001 AC6].

The sample of the stakeholder's export had been asked for twice — `EP-001/Q-002`, then
`WI-0003/Q-001` — and deferred twice with the same sentence, "I'll send you a sample later"
[src: WI-0003/Q-001]. `refine` therefore stopped asking for the fact and asked for the choice
underneath it: **where should the importer learn the file's shape from?** It offered a sample
sent now (A), a fixed format the stakeholder converts their export into before importing (B),
and the mapping given as options at import time (C), and recommended **C** on the ground that it
takes the sample off the critical path without guessing anything [src: WI-0003/Q-003].

`ADR-0007` already settled what the command *does* with a row — the payer, the sharers and an
optional date range are named at import time — and said explicitly that it did not settle how a
row is *read* [src: ADR-0007]. This decision is the other half.

## Options considered

- **A — the importer is written against a sample of the stakeholder's real export.** The column
  mapping, the delimiter, the date format and the amount convention become fixed facts in the
  acceptance criteria. Cost: nothing can be written until the sample exists, and it has already
  been deferred twice. Risk: the item waits on an input the pipeline cannot produce for itself.
  Benefit: the smallest command of the three and the one that needs no thought at the moment it
  is used — the person types the payer, the sharers and the range, and nothing else.
- **B — a fixed format the stakeholder converts their export into.** A comma-separated file with
  `date`, `description` and `amount` headers, dates as `YYYY-MM-DD`, amounts as plain signed
  numbers. Cost: spreadsheet work at every import. Risk: it trades the retyping the idea asked
  to stop for a different manual chore. Benefit: buildable with nothing further from anyone.
- **C — the mapping given as options at import time** (`--date-column`, `--amount-column`,
  `--description-column`, `--date-format`), with the delimiter detected and an amount normaliser
  accepting a stated list of forms. Cost: five more options, a normaliser with its own tests, and
  the person has to read their own header row. Risk: the largest item of the three. Benefit: the
  sample stops being on the critical path and nothing is guessed.
- **D — drop the import.** Listed in `Q-003` only to be rejected; `EP-001/Q-001` settled that the
  import ships and is not optional [src: EP-001/Q-001].

## Decision

**A**, against `refine`'s recommendation, on the stakeholder's explicit instruction:

> "No — just wait for my file. I don't want a name-the-columns version." [src: WI-0003/Q-003]

That is a rejection of C by name and, by "just wait for my file", a rejection of B as well: they
intend to hand over their export as it is rather than convert it or describe it. So:

1. **The importer is written against the stakeholder's actual export.** Once the sample exists,
   its column names, delimiter, quoting, date format and amount convention are written into
   WI-0003's acceptance criteria as fixed, testable facts, and the sample itself becomes the
   fixture the tests read.
2. **The import command gains no column-mapping options.** Its arguments remain the file path,
   the payer, the sharers and the optional date range that `ADR-0007` settled — nothing more.
3. **Nothing about the file's shape is guessed in the meantime.** No parser, no dialect, no
   default header. This is the standing prohibition `Q-001` was filed to protect and the answer
   does not lift it.

Two things the answer did not say, decided here so that `refine` and `plan` do not each decide
them differently:

- **Where the sample goes when it arrives:** `tracker/items/WI-0003/artifacts/bank-sample.csv`.
  The stakeholder answers in files, so the file needs a place to land that a fresh session will
  look in without being told. Any CSV under `tracker/items/WI-0003/artifacts/` counts; that path
  is the one the record names.
- **Asking a fourth time is now forbidden.** They were asked three times and have answered the
  third: they know what is wanted and have said they will send it. A further question would
  spend their attention on something already settled. What replaces it is a status — see below.

## Consequences

- **WI-0003 cannot be refined, planned or implemented until the sample is on disk.** Under A
  there is no work that can start early: every remaining acceptance criterion — AC1's mapping,
  AC3's "a row the tool cannot turn into an expense", AC4's "not the expected shape at all",
  AC5's duplicate detection — is a statement about a file nobody has seen.
- **The item is therefore a documented impasse that no skill can resolve, and a human must act**
  [src: .claude/agile-skills/spec/ids-and-statuses.md]. The next `refine` execution dispatched on it must **not**
  file a fourth question: if no CSV exists under `tracker/items/WI-0003/artifacts/`, it records
  the impasse and moves the item to `blocked`. When the sample lands, any skill may move it back
  to `draft` and refinement resumes [src: .claude/agile-skills/spec/ids-and-statuses.md].
- **The rest of the epic is unaffected.** `BUG-0001` is `ready` and runnable, and WI-0001 and
  WI-0002 are `done`. Blocking WI-0003 stops one item, not the pipeline.
- **The epic cannot close while this item is blocked.** `EP-001/Q-001` settled that the import
  ships, so the goal is not met without it, and the epic stays `open`.
- **`ADR-0007` is unaffected and is now complete in its pairing.** It says what the tool does
  with a row; this says how a row is read. Between them the command is fully specified except for
  the file's shape.
- **AC5 stays undecided and is now genuinely blocked on the sample rather than on the choice.**
  Whether a second import of the same file skips rows already imported or adds them again depends
  on what identifies a row, which the sample settles. `refine` still expects to decide it toward
  skipping, and to report how many rows were skipped, because WI-0001 shipped with no way to
  delete an expense [src: tracker/items/WI-0003/artifacts/refinement-qa.md].
- **Reversibility.** High, and cheap in one direction only. If the sample never arrives, C is
  still available and nothing built so far would have to be undone — the cost of having waited is
  the waiting itself. Going the other way is also cheap: an importer built for A can later grow
  the C options additively, since a fixed mapping is a default the options override. What is not
  reversible is time: this item now waits on something outside the workspace, and the record says
  so rather than pretending the wait is progress.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-22T03:33:27Z | answer-questions | WI-0003 | Created, recording the stakeholder's answer to `WI-0003/Q-003` — option A, the importer is written to their own export and gains no column-mapping options — and the consequences that answer left open: where the sample lands, that no fourth question may be filed, and that WI-0003 is an impasse until it arrives. |
