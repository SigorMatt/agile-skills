---
title: The CSV import takes its payer, its sharers and its date range from the command line
version: 1
status: current
updated: 2026-08-22T02:52:26Z
updated-by: answer-questions
updated-for: WI-0003
---

# ADR-0007 — The CSV import takes its payer, its sharers and its date range from the command line

- **Status:** accepted
- **Date:** 2026-08-22
- **Decided by:** the stakeholder, answering `WI-0003/Q-002`; recorded, with the consequences
  they did not state, by answer-questions (architect), for WI-0003
- **Supersedes:** —

## Context

A bank row knows a date, an amount and a merchant. It does not know who shared the expense, and
it only implicitly knows who paid — presumably the account holder [src: WI-0003/Q-002]. Something
has to supply what the file does not carry, and what that something is changes the shape of the
command and what the person types when they run it.

Two recorded decisions bear on this. An expense is split **equally** among whoever shared it
[src: ADR-0002], so the rule only ever has to name *who*, never in what proportion. And WI-0001
shipped with no edit and no delete [src: WI-0001], so an import that records the wrong thing
cannot be undone from the tool — which is why the cheapest option, "import everything as paid by
me and shared by everyone", is also the most dangerous.

`refine` put four options to the stakeholder and recommended B [src: WI-0003/Q-002].

## Options considered

- **A — everything imported is paid by the account holder and shared by everyone recorded.**
  Cost: one run over a full month's statement puts personal spending permanently into the group's
  books, with no way to remove it. Benefit: the simplest possible command.
- **B — the payer and the sharers are named once for the whole import, with a way of limiting
  which rows are taken.** Cost: a mixed export still needs the limit to be set correctly.
  Benefit: one non-interactive command, testable with nobody at the keyboard, and it does not
  assume every line of a statement is group spending.
- **C — the import asks row by row.** Cost: interactive, slow on a large file, harder to test,
  and closer to the typing this item exists to avoid. Benefit: handles a mixed export honestly
  with no filtering.
- **D — the CSV carries the sharing, because columns are added before importing.** Cost: the
  export has to be hand-edited every time, which is the thing this item exists to avoid.
  Benefit: precise and scriptable.

## Decision

**B.** The stakeholder chose it and said what the limit should be:

> "B — let me say who paid and who it's shared with when I run the import, and let me limit it to
> a date range. That's basically what a trip looks like anyway." [src: WI-0003/Q-002]

So the import command takes, besides the path of the file:

1. **the payer** — one person, who must already be recorded [src: WI-0001 AC1];
2. **the sharers** — the people the imported expenses are shared by, applied identically to every
   row the import covers, split equally [src: ADR-0002];
3. **a date range** — an optional pair of bounds, compared against **each row's own date**, not
   against today [src: WI-0001 AC7].

Of the four, only C would have changed this item from "run a command" into "sit with the tool",
and the stakeholder was asked explicitly and did not choose it. The import therefore stays
non-interactive, which is what lets `verify` exercise it from a test.

Two details the answer did not state, decided here so that `refine` and `plan` do not each decide
them differently:

- **The range is optional; omitting it imports every row in the file.** The stakeholder asked to
  be *allowed* to limit the import, not to be required to. Making it mandatory would refuse the
  case where the file is already only the trip.
- **A row whose date falls outside the range is skipped silently, and is not an error.** Filtering
  is the point of the range; a skipped row is not a row the tool failed to understand, and
  reporting it on stderr would drown AC3's genuine failures [src: WI-0003 AC3].

## Consequences

- **The command is non-interactive and fully specified by its arguments**, so it can be tested
  end to end without a person, and two runs with the same arguments over the same file do the
  same thing — which is what AC5's re-import question will be decided against
  [src: WI-0003 AC5].
- **Every expense created by one import run shares one payer and one set of sharers.** A
  statement covering two different groups needs two runs with two ranges. That is the cost of B
  and the stakeholder accepted it.
- **The no-delete hazard is reduced, not removed.** A wrong range still records expenses that
  cannot be removed from the tool [src: WI-0001]. This is worth a warning in the eventual plan,
  and is the strongest argument for `refine`'s expectation that a re-import should skip rows it
  has already imported [src: tracker/items/WI-0003/artifacts/refinement-qa.md].
- **This decision is independent of the CSV's shape.** It says what the tool does with a row, not
  how a row is read. `WI-0003/Q-001` — the sample of the stakeholder's export — is still
  unanswered in substance, and this ADR does not unblock it: the mapping from columns to a date,
  an amount and a description remains undecidable.
- **The flag names are not fixed here.** `plan` chooses them, against the CLI conventions already
  in the code [src: docs/architecture/overview.md].
- **Reversibility.** Nothing stored depends on this: imported expenses are ordinary expenses
  [src: WI-0003 AC2]. Adding an interactive mode (option C) later is additive. Reversing to A
  would be a change to the command's arguments only.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-22T02:52:26Z | answer-questions | WI-0003 | Created, recording the stakeholder's answer to `WI-0003/Q-002` and the two details that answer left open. |
