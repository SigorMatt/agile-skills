---
title: Python 3, standard library only, run as a stdin-to-stdout filter
version: 1
status: current
updated: 2026-08-28T18:30:21Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0001 — Python 3, standard library only, run as a stdin-to-stdout filter

- **Status:** accepted
- **Date:** 2026-08-28
- **Decided by:** the stakeholder, answering `EP-001/Q-001`; recorded by answer-questions
  (architect), for EP-001
- **Supersedes:** —

## Context

`mdtab` had no source code, no build file, no dependency manifest and no test framework when this
was decided, and `tracker/project.yaml` carried `commands.test`, `commands.lint` and
`commands.build` all null [src: tracker/project.yaml]. Nothing on disk recorded what the tool
should be written in or how it was to be invoked, so `intake` escalated the choice rather than
inferring it [src: EP-001/Q-001].

The stakeholder answered: *"Python, and nothing I have to install first. Every machine I work on
already has Python on it, and I want to clone this and pipe a file through it the same minute.
The rest of how it's built is your call, not mine."* [src: EP-001/Q-001]

Two constraints follow from that sentence and one degree of freedom is explicitly delegated. The
constraints are the runtime (Python) and the absence of an install step. The delegation is
everything below them — module layout, entry point mechanics, test framework — which remains
`plan`'s to decide.

## Options considered

- **A — Python 3, standard library only.** Cost: no third-party libraries may be used, so any
  capability the tool needs must exist in the standard library or be written here; interpreter
  startup costs tens of milliseconds per invocation. Risk: low — the tool is a text filter, and
  the standard library covers reading stdin, writing stdout, and Unicode data.
- **B — Python 3 with third-party dependencies, installed via `pip`.** Cost: an install step
  before first use. Risk: directly contradicts "nothing I have to install first", so this option
  is not available.
- **C — Node.js, Rust or Go.** Cost: a runtime or a toolchain the stakeholder did not ask for.
  Risk: contradicts "Python". Not available.

## Decision

`mdtab` is written in Python 3 and uses only modules shipped with CPython. No third-party
runtime dependency may be introduced, and no install step may stand between cloning the
repository and piping a document through the tool: a checkout plus a working `python3` is the
whole prerequisite.

It is invoked as a filter that reads a markdown document on stdin and writes the rewritten
document on stdout. The exact entry point — a module, a script with a shebang, or both — is left
to `plan`, subject to the constraint above.

A test framework may be introduced only if it is not required in order to *run* the tool. A
developer-only test dependency does not breach "nothing I have to install first"; a runtime one
does. `plan` decides this when it fills `commands.test` [src: tracker/project.yaml].

The minimum Python 3 version is not fixed here. It is a decision `plan` makes once it knows which
standard-library facilities the width rule in [src: ADR-0002] needs, and it is cheap to revisit.

## Consequences

What becomes easy: distribution is `git clone`, and the tool runs on any machine with a Python 3
interpreter. Nothing has to be packaged, published or version-pinned for a user to run it.

What becomes hard: capabilities that would normally come from a library — notably Unicode
display-width measurement, which [src: ADR-0002] requires — must be built from what the standard
library exposes, or vendored as data. Performance is bounded below by interpreter startup, so
this design is a poor fit for invoking the tool once per file across thousands of files; a batch
mode would be a separate item under EP-001, not a change to this decision.

**Reversibility: low for the runtime, high for everything under it.** Changing away from Python
means rewriting the tool and its tests, and it would contradict an explicit stakeholder answer,
so it requires the stakeholder's authorisation. Relaxing "standard library only" is cheaper but
still visible to every user, because it introduces the install step the stakeholder ruled out.
Choices delegated to `plan` — entry point, module layout, test framework, minimum interpreter
version — are ordinary reversible design decisions.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-28T18:30:21Z | answer-questions | EP-001 | First version, recording the stakeholder's answer to Q-001 |
