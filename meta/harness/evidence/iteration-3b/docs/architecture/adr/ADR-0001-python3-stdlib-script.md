---
title: The filter is a single Python 3 script using only the standard library
version: 2
status: current
updated: 2026-08-29T23:52:30Z
updated-by: review-close
updated-for: EP-001
---

# ADR-0001 — The filter is a single Python 3 script using only the standard library

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** answer-questions (architect), for EP-001
- **Supersedes:** —

## Context

The repository holds the pipeline's tracker and docs and nothing else — no source, no build
file, no dependency manifest — so nothing in the project constrained what this tool is written
in. `intake` filed EP-001/Q-002 to the stakeholder rather than guessing.

The stakeholder answered [src: EP-001/Q-002]:

> It is me, at my own machine, piping a file through it from my editor before I commit — so it
> has to be a thing I can just run, with no build step and nothing to install first. Your first
> suggestion is right: a plain script that runs on what is already there. I have opinions about
> languages but they are not worth much here, so take that decision yourselves.

That fixes the shape of the product — a script, invoked from an editor's "filter buffer through
command", no build step, no install step — and explicitly delegates the choice of language to
us. So the decision is ours to take and to record, which is what this ADR does.

The constraints it leaves are: runnable directly from a shell with no compilation; no
third-party package to fetch; present on an ordinary Linux developer machine already; and cheap
enough to start that it is invisible when a buffer is piped through it on every save.

## Options considered

- **A —** A single Python 3 script, standard library only, executable via `python3 mdtab` or a
  shebang. Cost: assumes a Python 3 interpreter is on the machine, and pays a few tens of
  milliseconds of interpreter startup. Risk: low — the startup cost is imperceptible for an
  editor filter, and the stated environment is the stakeholder's own development machine, where
  Python 3 is near-universal on Linux and macOS.
- **B —** A POSIX shell script driving `awk`. Cost: nothing to install anywhere a shell exists,
  and the fastest to start. Risk: high for this problem — column-width bookkeeping, fence-state
  tracking and byte-exact passthrough in `awk` are hard to write and harder to read, and the
  tests would be shell too, so the whole record of correctness gets less legible.
- **C —** A Perl 5 script. Cost: comparable ubiquity on Linux and a genuinely good fit for a text
  filter. Risk: fewer people can read or change it than Python, and this project's whole value is
  that the stakeholder can open the file and see what it does.
- Node.js and a compiled Go/Rust binary were the alternatives `intake` offered as options B and
  C of EP-001/Q-002. The stakeholder's answer rules both out: one needs an install, the other a
  build step.

## Decision

The tool is one Python 3 script, using only the standard library, that reads standard input and
writes standard output. It is run as `python3 mdtab.py` or, via its shebang, as `./mdtab.py`
[src: mdtab.py; src: run: printf '| a | b |\n|:-|-:|\n| xx | y |\n' | ./mdtab.py -> exit 0, table aligned].

- No third-party runtime dependency, and no dependency manifest.
- No build step, no packaging step, and no installation step.
- Tests are written with `unittest` from the standard library, so the test command needs
  nothing installed either.
- Minimum interpreter version: Python 3.8. Nothing in the problem needs anything newer, and 3.8
  is old enough to be present wherever `python3` is.

## Consequences

Easy: the stakeholder can copy one file onto a machine and pipe text through it. Reading and
changing the tool needs no toolchain. There is no supply chain and no lockfile to keep current.
Testing needs no runner to be chosen or installed.

Hard: the tool inherits Python's interpreter startup, so it is the wrong choice if it ever has to
run per-keystroke rather than per-save. It also assumes `python3` is present, which is an
assumption, not something we verified on the stakeholder's machine — if it turns out to be false,
that is the fact that reverses this decision.

Reversibility: **high, while the project is small.** The tool is a few hundred lines of text
manipulation with no dependencies and no persistent state, so a port to another language is a
rewrite of one file, and the acceptance criteria and tests describe behaviour rather than
implementation. Nothing else in the project will be built on the choice.

Follow-on: `plan` must set `commands.test` in `tracker/project.yaml`, which is still null, to
the `unittest` invocation this decision implies. That is `plan`'s field to fill
(`tracker/project.yaml` comment), so this execution leaves it null rather than pre-empting it.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-29T23:52:30Z | review-close | EP-001 | Provenance only, in `## Corrections`: the `## Decision` sentence's *"using only the standard library"* absolute now carries a citation. The decision is unchanged; the claim was verified true against the code before the citation was added [src: mdtab.py] |
| 1 | 2026-08-29T21:21:34Z | answer-questions | EP-001 | First version, recording the language and runtime decision the stakeholder delegated in EP-001/Q-002 |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-08-29T23:52:30Z | review-close | EP-001 | provenance | `## Decision`, first sentence — *"The tool is one Python 3 script, using only the standard library, that reads standard input and writes standard output"* — made an absolute claim (*only*) about `./mdtab.py` and carried no citation, which `lint-claims --context epic` reports as `claim.unsourced` at line 58. The assertion is **unchanged**; it was read against the code and is true: `mdtab.py` imports `re`, `sys` and `unicodedata` and nothing else [src: mdtab.py], and all three are standard-library modules [src: mdtab.py], it is the only `.py` file at the repository root [src: run: find . -maxdepth 1 -name '*.py' -> ./mdtab.py], there is no dependency manifest [src: run: ls requirements.txt pyproject.toml setup.py Pipfile -> all absent], and it is mode 100755 with a `#!/usr/bin/env python3` shebang so the `./mdtab.py` form works [src: run: printf '| a | b |\n|:-|-:|\n| xx | y |\n' | ./mdtab.py -> exit 0, table aligned]. Found by the epic-scope audit, not by any item's window: no work item ever edited this document, so `--changed-since main` could not have seen it (F-066). Repaired in place rather than recorded as an accepted gap, per `spec/doc-header.md` §4b — no code would change to satisfy the new text |
