# ADR-0007 — `plan` may create scaffolding, and only scaffolding

- **Status:** accepted
- **Date:** 2026-08-27
- **Unit:** META-108
- **Findings:** F-034

## Context

`plan` is specified as producing no code (`spec/workspace-layout.md` §5; a `plan` commit changes
only `tracker/` and `docs/`). Its own self-check asks whether `commands.test` is *"a command you
have actually run in this project, or one you expect to work"* — because a plan that records a
gate command nobody has ever executed is F-001's class in the plan: a confident sentence with
nothing behind it.

In a real run those two rules met. The project had no `expenses/__init__.py` and no
`tests/__init__.py`, so `pytest` could not execute *at all* — not fail, not collect nothing;
error. `plan` created both files empty so that it could run the command before recording it, and
flagged what it had done under the plan's `## Risks`, correctly, as a rule it had bent (F-034).

The worker behaved well. The contract was wrong, and it was wrong in a way that leaves an agent
choosing between two rules with nothing to choose on.

## Options

1. **Drop the "have you run it" requirement.** `plan` records the command and `implement` finds
   out whether it works.
2. **Let `implement` create the scaffolding**, and let `plan` record the command unrun.
3. **Carve out scaffolding**: `plan` may create files that contain no behaviour, solely so that a
   declared gate command can execute, and must list them.

## Decision

**Option 3.**

1 and 2 are the same option wearing different hats: both end with a plan recording a gate command
that has never run. That is precisely the sentence-with-nothing-behind-it that the F-001 work
exists to eliminate, and it fails in the most expensive place — `implement` discovers the command
is wrong after building against it, and the round trip costs a whole turn.

The carve-out keeps the property that matters (*every command in the plan has been executed
here, once, by the skill that wrote it down*) and gives up a weaker one (*`plan` touches no file
outside `tracker/` and `docs/`*). The weaker rule was a proxy anyway: what "produces no code"
protects against is `plan` starting the implementation, and an empty package marker is not the
implementation starting.

### The bound, stated so that it can be applied

`plan` MAY create a file outside `tracker/` and `docs/` only when **all** of:

- a gate command the plan declares **cannot execute at all** without it — not "fails", not
  "reports nothing": errors out or does not run;
- the file contains **no behaviour**: an empty package marker, an empty test module, the minimum
  a tool requires to recognise the project. No function, no class, no branch, no assertion;
- it is listed in the plan under **`## Scaffolding`**, one line each, saying which command needed
  it;
- it satisfies no acceptance criterion. If deleting the file would make a criterion fail, it is
  implementation and `plan` may not write it.

Anything else remains forbidden, including the tempting middle case: a stub function with the
right signature and a `pass` body. That is a decision about the interface, and it belongs in the
plan as an interface, where `implement` will read it and a reviewer can argue with it — not in a
file where it will be silently kept.

## Consequences

- `spec/workspace-layout.md` §5 carries the carve-out, so "a `plan` commit changes only `tracker/`
  and `docs/`" stops being a rule the tools state and a run has to break.
- `plan`'s process gains `## Scaffolding` and a self-check question. It stays a **[skill]** rule:
  nothing mechanically distinguishes an empty package marker from a small implementation, and
  claiming otherwise would be exactly the over-claim this project keeps finding.
- The honest cost: this widens what `plan` may write, and the bound is prose. What makes it
  reviewable rather than a loophole is `## Scaffolding` — the files are listed, so a reviewer
  reads a list rather than a diff, and a plan that quietly writes code has to lie in a named
  section to do it.
