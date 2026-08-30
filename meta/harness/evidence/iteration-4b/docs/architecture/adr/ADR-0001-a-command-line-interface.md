---
title: A command-line interface, one executable with subcommands
version: 1
status: current
updated: 2026-08-30T01:36:58Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0001 — A command-line interface, one executable with subcommands

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** the stakeholder, answering `EP-001/Q-002`; recorded by answer-questions (architect), for EP-001
- **Supersedes:** —

## Context

Every acceptance criterion on WI-0001, WI-0002 and WI-0003 was written to say what must be true
rather than what to type, because the shape of the interface was undecided and no criterion can
say "run X and see Y" until it is [src: WI-0001; WI-0002; WI-0003]. Intake filed that as
`EP-001/Q-002` and suspended the epic on it [src: EP-001/Q-002].

The repository is empty and nothing pre-existing constrains the choice; `tracker/project.yaml`
records no test, lint or build command [src: tracker/project.yaml].

The stakeholder answered: *"A command-line tool — I'm doing this at a terminal once a day, so
option A works fine."* [src: EP-001/Q-002]. Their answer to the elicitation question says the
same thing from the other side: *"It's just me, learning vocabulary, at a terminal, once a day —
nothing fancier than that."* [src: EP-001/Q-001].

## Options considered

These are the three options the question put to the stakeholder [src: EP-001/Q-002].

- **A — A command-line tool.** Subcommands typed at a terminal; the process exits when done.
  Cost: lowest of the three; every criterion becomes a command with an exit code. Risk: the
  review sitting is a sequence of prompts rather than a screen, and it only works where there is
  a terminal.
- **B — A local web app.** Cost: roughly doubles each item — a server process, a front end, and
  a way to start it. Risk: criteria become hard to check without browser automation.
- **C — A full-screen terminal application.** Cost: a terminal-UI library and a redraw loop.
  Risk: the hardest of the three to verify automatically.

## Decision

**A.** The tool is a command-line program: a single executable, invoked with a subcommand, that
does one thing and exits.

Fixed here, because acceptance criteria have to name an invocation:

1. **One entry point** — a single command, named `recall`, after the project.
2. **Subcommands** — `recall add`, `recall list`, `recall review`. WI-0004 adds one for
   removing a card. The subcommand is the first positional argument.
3. **`add` takes its two sides as options**, not as a prompt: `recall add --question <text>
   --answer <text>`. This is the clause that makes WI-0001 checkable without driving a prompt,
   and it is why the interface is being fixed at all. An interactive prompt as a *fallback* when
   the options are absent is left to `plan`; the option form must exist either way.
4. **`review` is interactive**, because a review sitting is a conversation: it shows a question,
   waits, shows the answer, and asks how it went. It reads from standard input, so it can be
   driven by a here-document in a test.
5. **Exit codes carry the outcome** — `0` for success, non-zero for a refused or failed
   operation, with the reason written to standard error.

Not decided here, and left to `plan`: the implementation language, the runtime, the storage
file's format and location, and the exact wording of any message.

## Consequences

- `refine` can now rewrite the criteria on WI-0001, WI-0002 and WI-0003 in terms of concrete
  invocations, which is what the Definition of Ready needs from them.
- Verification is cheap: a criterion becomes a command, an exit code and some text on a stream.
- The daily sitting is a scrolling prompt rather than a screen. The stakeholder chose that
  knowingly; the question named the consequence.
- **Reversibility: high for the surface, low for the paradigm.** Renaming a subcommand or adding
  a prompt fallback is a small change. Moving to option B or C after WI-0001 to WI-0003 are built
  would discard the whole interface layer and every criterion written against it, though the
  storage and scheduling would survive. That is why the paradigm was put to the stakeholder
  rather than assumed.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T01:36:58Z | answer-questions | EP-001 | First version, recording the stakeholder's answer to `EP-001/Q-002` |
