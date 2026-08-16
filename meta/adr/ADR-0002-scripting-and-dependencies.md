# ADR-0002 — Scripting language and dependency policy

- **Status:** accepted
- **Date:** 2026-08-16
- **Unit:** META-003
- **Supersedes / superseded by:** —

## Context

`scripts/validate-workspace`, `scripts/board-gen` and the workspace helpers do not only run in
*this* repo. They are copied into the **consumer's project** by the adapter's installer, and
they are invoked there as quality gates — including from a `PreToolUse` hook, which must
succeed or fail deterministically without a human present.

The consumer's project may be a Node project, a Go project, or an empty directory. We cannot
assume a virtualenv, a package manager, a lockfile, or network access at gate time. A gate that
fails because `pyyaml` is missing is indistinguishable, to the agent running it, from a gate
that fails because the work is wrong — and that ambiguity would poison the whole "executable
gates over vibes" principle.

Three options were considered:

1. **Bash + `grep`/`sed`.** No parsing of structured data worth the name; validation of nested
   `skill.yaml` contracts would become unreadable regexes. Rejected.
2. **Python + PyYAML.** Correct YAML, but adds an install step to every consumer project and to
   every CI job that runs the gates. Rejected for the reason above.
3. **Python, standard library only, with a YAML *subset* reader we own.** Chosen.

## Decision

1. Every executable under `scripts/` and `adapters/` is **Python 3.9+, standard library only**.
   No third-party import may appear anywhere on the import path of a gate. There is no
   `requirements.txt`, and there is deliberately no place to add one.
2. YAML is read by `scripts/lib/miniyaml.py`, a reader for an explicitly documented **subset**:
   block mappings, block sequences, plain/quoted scalars, `|` and `>` block scalars with
   chomping indicators, single-line flow sequences and flow mappings, comments, and the
   `true`/`false`/`null` literals.
3. **Anything outside the subset is a hard error with a file and line number** — never a silent
   mis-parse. Anchors (`&`), aliases (`*`), tags (`!`), multiple documents, and tab indentation
   are all rejected explicitly. This is the load-bearing property: a reader that quietly
   mis-reads a contract is worse than no reader, because the gate would go green on a lie.
4. Because we own both the writer (the renderer) and the readers (the linters), the subset is
   sufficient by construction. If a spec ever needs a construct outside it, the subset is
   extended in `miniyaml.py` *and* in this ADR — not worked around in a caller.
5. `scripts/lib/selftest.py` is the reader's own gate. When PyYAML happens to be importable —
   as it is in this build environment, but not necessarily in a consumer's — the self-test
   additionally cross-checks every fixture and every repo YAML file against PyYAML, so
   divergence between "what we parse" and "what YAML means" is caught here rather than in the
   field. PyYAML's absence downgrades that cross-check to a skip; it never fails the run.

## Consequences

- Consumers run `python3 scripts/validate-workspace` with zero setup. That is the property
  that makes the gates credible as gates.
- We carry the maintenance of a ~350-line parser. Bounded, and paid for by the point above.
- The YAML we *emit* (rendered SKILL.md frontmatter, `pipeline.yaml`) must stay inside the
  subset. `scripts/lint-skills` enforces this by re-reading everything it writes.
- Node is present in this environment but is not used: adding a second language would double
  the "is it installed?" surface the whole ADR exists to remove.
