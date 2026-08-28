---
title: Report an unusable target at the CLI boundary, with exit status 2
version: 2
status: current
updated: 2026-08-27T21:06:34Z
updated-by: answer-questions
updated-for: BUG-0004
---

# ADR-0006 — Report an unusable target at the CLI boundary, with exit status 2

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for BUG-0001
- **Supersedes:** —

## Context

Pointing `tidy` at a folder the process cannot read makes it die with an uncaught
`PermissionError` traceback and exit 1 [src: BUG-0001]. `tidy/cli.py` validates only
`os.path.isdir(folder)` before calling `build_plan`, and `build_plan`'s first act is
`os.scandir(folder)`, which raises [src: tidy/cli.py; src: tidy/planner.py]. Reproduced on
`main` after WI-0002 merged
[src: run: python3 -m tidy /tmp/bug1repro/unreadable → exit 1, PermissionError traceback].

Two things are already fixed and constrain the answer. `README.md` states the exit-status
contract — 0 on success including nothing to do, 2 when the named folder does not exist or is not
a folder, 1 when some file could not be moved while others were [src: README.md] — and the
current exit 1 contradicts it, because no file failed to move; nothing was even planned. And
ADR-0002 fixes the layering: `tidy/planner.py` decides and writes nothing, `tidy/apply.py`
executes and decides nothing, `tidy/cli.py` turns results into text and exit codes
[src: ADR-0002].

BUG-0001 deliberately left the number to this decision: its AC1 requires "a status the tool
documents", not a specific one [src: BUG-0001 AC1]. So there are two questions here — **which
status**, and **where the failure is caught** — and both are checkable against code once
answered.

## Options considered

**Which status.**

- **A — Exit 2, the status the tool already uses for an unusable target.** Cost: 2 stops meaning
  "the path is not a folder" and starts meaning "the folder you named cannot be used as a
  target", so `README.md`'s sentence has to be rewritten rather than extended
  [src: README.md; src: BUG-0001 AC2]. Risk: a script
  that distinguishes "no such folder" from "no permission" cannot; nobody has asked to, and the
  message on stderr says which it was.
- **B — A new status, 3, for "the folder exists but cannot be read".** Cost: a third number in a
  contract users must learn, for a case that is one line of prose away from the two that exist,
  and every future unusable-target condition then argues for its own code. Risk: the contract
  grows faster than the tool.

**Where it is caught.**

- **C — At the CLI boundary: wrap the `build_plan` call in `tidy/cli.py`.** Cost: `cli.py` gains
  one `try`/`except`. Risk: catching too broadly could turn a defect inside `build_plan` into a
  tidy message instead of a traceback — mitigated by `build_plan` doing nothing but filesystem
  reads, and by the message carrying the operating system's own reason.
- **D — Inside `tidy/planner.py`: catch and return an empty action list, or an action that
  represents the failure.** Cost: the planner acquires a second kind of return value, or an
  `Action` kind that means "the run failed", which every caller then has to interpret; `cli.py`
  still has to decide the exit status, so the decision does not actually move. Risk: it makes
  the planner responsible for how a failure is presented, which is the boundary ADR-0002 exists
  to hold [src: ADR-0002].
- **E — Pre-check with `os.access(folder, os.R_OK | os.X_OK)` before planning.** Cost: a second
  check that can disagree with the real one. Risk: time-of-check to time-of-use — the folder can
  become unreadable between the check and the scan, so the traceback comes back on the exact
  path the check was added to prevent, and now it is harder to find.

## Decision

**A and C.** `tidy/cli.py` wraps its `build_plan(folder)` call in `try`/`except OSError`. On
`OSError` it writes one line to stderr naming the folder and the operating system's reason,
writes nothing to stdout, and returns **2** — the same status the existing
`os.path.isdir` check already returns for a target that cannot be used
[src: tidy/cli.py; src: BUG-0001 AC1].

Three details are fixed here because each is checkable against code and each would otherwise be
decided silently in a plan step:

1. **The `except` clause catches `OSError`, not `PermissionError`.** An unreadable folder is the
   case BUG-0001 reproduces, but it is not the only way listing a directory fails — a mount that
   disappears, a name that stops being a directory between the `isdir` check and the scan, a
   filesystem returning `EIO`. Every one of them reaches the user as a traceback today, and
   narrowing the clause to `PermissionError` would leave them there while claiming the class was
   handled. `build_plan` performs filesystem reads and nothing else [src: tidy/planner.py], so an
   `OSError` out of it is a filesystem condition rather than a defect in this code.
2. **The message carries the operating system's own reason**, so it is honest for every member of
   that class rather than only for the permission one. Naming the folder is what BUG-0001 AC1
   requires; the reason is what makes the broader clause defensible.
3. **`README.md`'s exit-status paragraph is rewritten, not appended to** [src: BUG-0001 AC2]. The
   sentence becomes "2 when the folder you named cannot be used — it does not exist, is not a
   folder, or cannot be read", which states one rule instead of listing three cases.

`tidy/apply.py` is unchanged: `apply_plan` already lets nothing raise out of it, returning a
message per action that did not complete [src: tidy/apply.py].

## Consequences

What becomes easy: every way of failing to list the target folder now produces the same shape of
output — a line on stderr, an empty stdout, exit 2 — so a user or a script has one rule to learn
and `README.md` has one sentence to state [src: README.md; src: BUG-0001 AC1]. The traceback stops being part of the interface.

What becomes hard: distinguishing "no such folder" from "cannot read it" by exit status alone is
no longer possible. That distinction is available on stderr and nobody has asked for it as a
status; if someone does, it is option B, and it is additive.

A cost worth naming: a genuine defect inside `build_plan` that surfaces as an `OSError` is
reported as a filesystem condition rather than crashing loudly. Since ADR-0009 that cost is split
in two, and the halves are not equally loud. An `OSError` from `os.scandir` — or from anywhere
outside the per-entry guard — still arrives here and is reported as an unusable target, exit 2
[src: ADR-0009; src: tidy/cli.py]. One raised while interrogating a single entry no longer reaches
this handler at all: it becomes that entry's `leave` line and the run continues, exit unchanged
[src: ADR-0009; src: tidy/planner.py; src: BUG-0004]. So a defect in the guarded region surfaces
more quietly than an unusable target, not less. `build_plan` reads the filesystem and composes
strings, so the class of such defects is small, and the operating system's own reason — in the
stderr line here, in the `leave` text there — is what would give it away in either place.

**Reversibility: cheap, in both parts.** Moving to option B is changing one returned constant in
`tidy/cli.py`, one sentence in `README.md`, and one assertion in the regression test — no data on
disk, no change to any file the tool writes, no other module involved [src: tidy/cli.py; src: README.md]. Narrowing the `except`
clause from `OSError` to `PermissionError` is one word. Neither reversal touches
`tidy/planner.py` or `tidy/apply.py`, which is the property option C was chosen for.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-27T21:06:34Z | answer-questions | BUG-0004 | Answering BUG-0004/Q-001: the `## Consequences` cost paragraph said a defect inside `build_plan` surfacing as an `OSError` would be reported as an unusable target. ADR-0009 made that untrue for the per-entry guard, where such an error now becomes a `leave` line and the run exits 0. Restated as the two halves it has become; the decision is unchanged |
| 1 | 2026-08-27T19:19:39Z | plan | BUG-0001 | First version |
