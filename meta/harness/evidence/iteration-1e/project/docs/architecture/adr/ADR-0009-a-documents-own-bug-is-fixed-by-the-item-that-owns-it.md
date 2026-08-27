---
title: A document's own bug is fixed by the item that owns it
version: 1
status: current
updated: 2026-08-27T02:13:09Z
updated-by: plan
updated-for: BUG-0001
---

# ADR-0009 — A document's own bug is fixed by the item that owns it

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for BUG-0001
- **Supersedes:** —

## Context

BUG-0001 is a defect **in a document**. Two paragraphs of `docs/product/vision.md` make absolute
claims about backticked names and carry their source only in prose, so the claims linter reports
two errors over the whole tree while the trunk-scoped gate every skill actually runs reports none
[src: BUG-0001; docs/product/vision.md]. The item's acceptance criteria are therefore criteria
about a file under `docs/`: AC1 is the linter exiting 0, AC2 is that the two claims still say the
same thing, AC3 is the version bump and change-log row [src: BUG-0001 AC1; BUG-0001 AC2;
BUG-0001 AC3].

Every other item in this project delivers code, and its documents are updated alongside it. This
one delivers **only** a document edit, which makes a rule visible that nothing had tested before:
the methodology's own table of which skill writes which document lists `refine` and
`answer-questions` as the updaters of the product vision, and states that `implement` and
`verify` do not write to `docs/` at all — because otherwise "the authoritative record would be
updated by the same execution that is trying to satisfy it, and the check would be circular"
[src: .claude/agile-skills/spec/doc-header.md].

Read flatly, that sentence makes BUG-0001 unbuildable: no skill the pipeline dispatches on
`planned` or `in-progress` is allowed to touch the file the item is about. Read against its own
stated reason, it is aimed at a narrower thing — a skill that *concludes* mid-execution that a
document is wrong and edits it to suit itself. The two readings produce different pipelines, so
the choice has to be made here rather than discovered by whoever executes the plan.

The tension is not new in this project, only newly unavoidable. The same table lists `plan` and
`answer-questions` as the updaters of the architecture overview, and `implement` wrote versions 5
and 7 of it — for WI-0004 and for BUG-0002 — because the Definition of Done requires the
delivering item to leave `docs/` true, and at plan time the code the document describes does not
exist yet [src: docs/architecture/overview.md; .claude/agile-skills/spec/dor-dod.md]. Both were
reviewed and accepted [src: WI-0004; BUG-0002].

## Options considered

- **A — `implement` edits `docs/product/vision.md` as a numbered plan step, like any other file
  the item delivers.** Cost: a recorded departure from the writer table, which has to be argued
  for rather than assumed, and this ADR is that argument. Risk: the circularity the table warns
  about — the skill that must satisfy the linter is the skill that edits the file the linter
  reads. Bounded here by three things that do not depend on `implement`: the judgement that the
  document is wrong was made by `verify`, not by the executing skill [src: BUG-0001]; AC2 forbids
  removing or softening either claim, so the cheap way out is closed by a criterion
  [src: BUG-0001 AC2]; and AC1 is a program, not an opinion [src: BUG-0001 AC1].
- **B — `plan` makes the edit now, in this execution, and leaves `implement` an empty plan.**
  Cost: the writer table does not list `plan` for the vision either, so it departs from the same
  rule without even the excuse of executing a plan; and it collapses the item, because the
  criteria would already be met before the status that owns meeting them. Risk: verification
  would be checking the architect's own edit with no independent step between them, which is a
  sharper version of the circularity option A is accused of.
- **C — route the edit through `answer-questions`, the skill the table does authorise**, by
  having `implement` file a question and suspend the item. Cost: a round trip and a question with
  nothing in it — the answer is already written in BUG-0001's criteria, so the artifact would be
  a formality wearing the shape of an escalation. Risk: it teaches the pipeline that a question
  is a routing device rather than a thing somebody does not know, which is the failure the
  question protocol is built to prevent [src: .claude/agile-skills/spec/question.md].
- **D — set BUG-0001 to `blocked` as unbuildable under the writer table**, and record that the
  methodology has no path for a document-only defect. Cost: a real defect stays in the tree, and
  the epic carries a blocked child into its ending for a reason that is procedural rather than
  substantive. Risk: it is also not obviously wrong — but it spends the stakeholder's engagement
  on a rule about which skill holds the pen, which is not a thing they asked for.

## Decision

**A.** When an item's own acceptance criteria are criteria *about* a document, the skill that
executes the item's plan edits that document, and the writer table's prohibition is read as what
its stated reason describes: a skill may not edit `docs/` on a conclusion it reached itself
mid-execution. For BUG-0001 this means `implement` edits `docs/product/vision.md`, bumps it to
version 4 and adds the change-log row, on the branch, as numbered steps of the plan.

Two things follow, and they are what the work can be checked against:

1. **The judgement must already be recorded before the edit.** Here it is: `verify` filed
   BUG-0001 with reproduction steps and criteria, and `plan` designed the fix
   [src: BUG-0001; tracker/items/BUG-0001/artifacts/plan.md]. An `implement` execution that
   *discovers* a document is wrong still files a question and stops; nothing in this ADR changes
   that.
2. **The document's `updated-by` records the skill that actually made the change**, which will be
   `implement`, not the skill the table would have preferred. The front matter is evidence about
   what happened, not a claim about what was authorised
   [src: .claude/agile-skills/spec/doc-header.md].

## Consequences

Easy: a defect in a document can be planned, implemented, verified and reviewed exactly like a
defect in code, with the same gates and the same independent verification. The project stops
having two classes of work item, one of which no dispatchable skill may execute.

Hard: this is a recorded departure from a methodology rule, not a project convention filling a
gap, and it is only as visible as this file. Anyone reading the writer table alone will not find
it. It also leaves the narrower prohibition intact and therefore requires a judgement each time:
"did an independent record already establish that this document is wrong?" is the question that
separates this case from the one the rule forbids, and nothing checks it.

Reversibility: **cheap, and cheap in both directions.** Reversing it means moving the two edited
paragraphs into an `answer-questions` execution and deleting one plan step; no code changes, no
stored data changes, and no interface changes. The document itself would be identical either way
— only its `updated-by` and which journal carries the entry would differ.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-27T02:13:09Z | plan | BUG-0001 | First version |
