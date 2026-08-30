---
title: A single-user command-line tool is the delivery surface
version: 1
status: current
updated: 2026-08-30T11:13:36Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0001 — A single-user command-line tool is the delivery surface

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** answer-questions (architect), for EP-001, on the stakeholder's answer to
  `EP-001/Q-001`
- **Supersedes:** —

## Context

Nothing existed on disk when this was decided: the repository holds a tracker and docs and no
product code, so no language, framework or existing interface constrained the choice
[src: EP-001]. The surface decides how every acceptance criterion on WI-0001 and WI-0002 is
written and checked, and changing it later means rewriting the product rather than adjusting it,
so `intake` escalated it rather than assuming [src: EP-001/Q-001].

The stakeholder answered, in their own words: *"A. Command-line is fine — it's just me, once a
day at a terminal, running through vocab."* [src: EP-001/Q-001]

Two further sentences of theirs bear on this decision. On storage: the card data *"needs to live
in a file on my machine that survives a reboot"* [src: EP-001/Q-004]. On technology: *"As for how
it's actually built — whatever you think is best."* [src: EP-001/Q-004]

## Options considered

- **A — A command-line tool** invoked per action (`add`, `review`), reading and writing a file on
  the local machine. Cost: lowest of the three; each criterion becomes a command with output a
  reader can check. Risk: no interface beyond a terminal, so a later change of mind about the
  surface is a rewrite of everything above the storage layer.
- **B — A local web page** served by the tool and opened in a browser. Cost: substantially more
  work, and every criterion has to be checked through a browser rather than by reading output.
  Risk: the review loop arrives later.
- **C — A full-screen terminal application** driven by the keyboard. Cost: between A and B, and
  harder to test than A. Risk: the same scheduling and storage work underneath, spent on a
  surface the stakeholder did not ask for.

## Decision

The tool is a command-line program, run in a terminal by one person on one machine
[src: EP-001/Q-001]. Its state lives in a file on that machine, and it must survive a reboot of
the machine, not merely an exit of the program [src: EP-001/Q-004].

The choice of implementation language, storage file format and packaging is delegated to `plan`,
which the stakeholder authorised explicitly [src: EP-001/Q-004]. `plan` records that choice as
its own ADR; it is not settled here.

Two constraints on the surface follow from the stakeholder's stated failure modes, and both are
recorded here because they bind whatever `plan` chooses: losing recorded progress is a failure of
the product, and a review session that takes more than a couple of minutes to get through is a
failure of the product [src: EP-001/Q-004]. The second is in tension with the stakeholder's
instruction that a session shows every due card with no cap [src: EP-001/Q-003]; that tension is
open with them as `EP-001/Q-005` and is not resolved here [src: EP-001/Q-005].

## Consequences

Easy: acceptance criteria on WI-0001 and WI-0002 can name a command and the output it must
produce, so a reader with a terminal and no context can decide them [src: WI-0001]
[src: WI-0002]. Checking that "progress persists" needs only the stored file, inspected outside
the tool [src: WI-0001].

Hard: there is no interface for anyone not at a terminal, and no path to a second device — both
already out of scope on the epic [src: EP-001].

Reversibility: **partial, and asymmetric.** The scheduling and storage decisions in
`ADR-0002-scheduling-binary-ladder.md` are independent of the surface and survive a change of
mind [src: docs/architecture/adr/ADR-0002-scheduling-binary-ladder.md]. The surface itself is not
cheaply reversible: moving to a browser or a full-screen terminal application replaces every
interaction and every acceptance criterion written against it, while leaving the stored data
intact [src: WI-0001] [src: WI-0002].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T11:13:36Z | answer-questions | EP-001 | First version: records the stakeholder's answer to Q-001 and the delegation of technology choice from Q-004. |
