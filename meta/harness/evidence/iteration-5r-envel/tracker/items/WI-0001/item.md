---
id: WI-0001
type: work-item
title: Set up envelopes, put income into them, and see what is in each
status: done
priority: high
epic: EP-001
created: "2026-09-11T01:57:11Z"
updated: "2026-09-11T03:28:28Z"
branch: wi/WI-0001
outcome: delivered
merge-commit: 025240e494eb2593213870af5763094d6b1f4a2a
---

## Story

As a person budgeting my own money at a terminal, I want to create named envelopes and put
income into them, so that my money is divided up the way I have decided before I start spending
it.

## Acceptance criteria

- [x] AC1 — `envel new <name>` creates an envelope called `<name>`, prints to stdout a line that
      contains the name and says the envelope was created, and exits 0.
- [x] AC2 — `envel add <name> <amount>` adds `<amount>` of income to the envelope called
      `<name>`, prints to stdout a line that contains the envelope's name and the amount now in
      it, and exits 0.
- [x] AC3 — `envel list` prints to stdout one line per envelope, each line containing that
      envelope's name and the amount currently in it, the lines ordered alphabetically by name
      ignoring capitalisation, with no total line and no line for anything but an envelope, and
      exits 0.
- [x] AC4 — The three commands above are run as separate invocations of the tool, with the
      process exiting between them, and the listing still shows the envelope and the amount
      added. Nothing else is running between invocations.
- [x] AC5 — Adding income to an envelope that does not exist is refused, with a message naming
      the envelope, and no envelope is created as a side effect.
- [x] AC6 — Listing when no envelope has ever been created prints a line saying there are none
      and exits 0; it neither prints nothing nor fails.
- [x] AC7 — Creating an envelope whose name is already taken is refused: the existing envelope
      is left exactly as it was, including the amount in it, the message says the envelope
      already exists and names it, and the command exits non-zero. Nothing is emptied or reset.
- [x] AC8 — An amount is written with at most two decimal places. `12.5` is accepted and means
      12.50; `12.567` is refused with a message and nothing is recorded. Every amount the tool
      prints is shown with exactly two decimal places.
- [x] AC9 — No amount is rounded or truncated: after adding income of `0.01` to an envelope one
      hundred times in separate invocations, the listing shows `1.00` for that envelope.
- [x] AC10 — Adding income of `0`, or of a negative amount, is refused with a message, and the
      envelope's amount is unchanged.
- [x] AC11 — Envelope names are matched without regard to capitalisation: after creating
      `groceries`, adding income to `Groceries` adds it to that same envelope and the listing
      shows one envelope, not two. AC7 refuses the create of `Groceries` for the same reason.
- [x] AC12 — The listing shows an envelope's name exactly as it was typed when it was created,
      whatever capitalisation was used to refer to it afterwards.
- [x] AC13 — A name may contain any character, including spaces and punctuation: `eating out`
      and `car & bike` are both accepted. An empty name, and a name that begins or ends with a
      space, are refused with a message and no envelope is created.
- [x] AC14 — `envel` run with no subcommand, and `envel <word>` where `<word>` is not one of the
      subcommands this tool has, each print to stderr a usage message that lists the subcommands
      the tool does have, and exit non-zero. No envelope is created and no amount changes.
- [x] AC15 — A subcommand given the wrong number of arguments prints to stderr a usage message
      for that subcommand and exits non-zero, changing nothing: `envel new` with no name,
      `envel new a b`, `envel add groceries` with no amount, `envel add groceries 10 20`, and
      `envel list extra` are each refused this way.
- [x] AC16 — Every refusal this item specifies writes its message to stderr and exits non-zero,
      and every command that succeeds writes its output to stdout and exits 0. Checked case by
      case against the criteria that name them: refusals at AC5, AC7, AC8, AC10, AC13, AC14 and
      AC15; successes at AC1, AC2, AC3 and AC6.
- [x] AC17 — An amount is written as a plain decimal number, with no currency symbol and no
      thousands separator: `400`, `12.5` and `12.50` are accepted, and `£12.50`, `1,200`, `12.5x`
      and `abc` are each refused with a message with nothing recorded. A leading `-` is read as a
      negative amount and refused by AC10, not by this criterion. No amount the tool prints
      carries a currency symbol.

## Out of scope

- Recording spending, and anything that reduces an envelope's amount — that is `WI-0002`.
- Any summary or report — that is `WI-0003`.
- Renaming, deleting or merging envelopes. Moving money between them was asked for at
  `EP-001/Q-005` and is `WI-0004`, not this item.
- Creating an envelope and putting money in it in a single command (`envel new groceries 400`).
  Creating and funding are AC1 and AC2, two invocations.
- Flags and options of any kind on these three commands — they take positional arguments only,
  so there is no `--name`, no `-a`, and no global switch. If one is wanted later it is its own
  item.
- Any notion of where the data is stored and in what format. That is a design decision and
  belongs to `plan`; AC4 constrains only that it survives.

## Notes

- `refine` round 1's four questions are all answered and propagated. What each settled:
  - `WI-0001/Q-001` — option A: a create of a name already taken is refused, and nothing is
    emptied. AC7. Their reason: *"Nothing should ever be able to wipe money out of an envelope
    by accident."*
  - `WI-0001/Q-002` — option A: at most two decimal places in, exactly two out, and nothing
    rounded. AC8 and AC9. *"The figures have to add up."* How the amounts are held internally
    they left to us explicitly: *"How you keep it under the hood is yours to decide."*
  - `WI-0001/Q-003` — option A: zero and negative income are both refused. AC10.
  - `WI-0001/Q-004` — option A: names match case-insensitively, are shown as first typed, and
    are not restricted in what characters they may contain. AC11, AC12, AC13.
- `refine` round 2 filed no question. It settled the command surface — what is typed below
  `envel`, what goes to stdout and stderr, and what exit code follows — by assuming it rather
  than asking, and every one of those assumptions is recorded in
  `artifacts/refinement-qa.md` `## Round 2`. Assumed there, under **no delegation**:
  - the three subcommands are `new`, `add` and `list`, positional arguments only. A
    disagreement lands on AC1, AC2, AC3, AC14 and AC15 and costs the argument parser.
  - success goes to stdout and exits 0; every refusal goes to stderr and exits non-zero. AC16.
  - the listing is ordered alphabetically ignoring capitalisation and carries no total line.
    AC3.
  - listing with no envelopes prints a line saying so rather than printing nothing. AC6.
  - an amount is a plain decimal number, no currency symbol either way. AC17.
- Deliberately left **unconstrained** by `refine`, so that nobody mistakes the silence for a
  decision: whether two names differing only in *internal* whitespace (`eating out` against
  `eating  out`) are one envelope or two. AC11 settles capitalisation and AC13 settles what
  characters are allowed; neither says anything about this, and a disagreement lands on AC11.
- Also unconstrained: the exact wording of every message. The criteria say what a message must
  contain — the envelope's name, the amount — and not how it reads.
- Open **design** questions, routed to `plan` rather than to the stakeholder, because the answer
  would be the same whoever they were:
  - where the data is stored, in what format, and what the tool does when that file is missing,
    empty, or unreadable;
  - whether the store is written atomically, so that an interrupted run cannot leave a
    half-written file behind.
- `EP-001/Q-006` is answered: the command is `envel`, and AC1, AC2 and AC3 now say so. Their
  reason — *"Short is what matters if I'm typing it several times a day"* — is what the round 2
  subcommand assumption was taken against.
- `EP-001/Q-005` is answered: the stakeholder wants both moving money between envelopes and
  correcting a recorded spend. They were filed as `WI-0004` and `WI-0005` rather than added
  here, so this item's scope is unchanged by that answer.
