---
title: Target Python 3.9+ and depend on nothing outside the standard library
version: 1
status: current
updated: 2026-08-21T02:26:10Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0001 — Target Python 3.9+ and depend on nothing outside the standard library

- **Status:** accepted
- **Date:** 2026-08-21
- **Decided by:** answer-questions (architect), for EP-001
- **Supersedes:** —

## Context

`EP-001/Q-004` asked the stakeholder which Python version the tool may rely on, and whether the
project may install developer dependencies such as `pytest`. Their answer was *"Whatever you
think is best — you know this better than I do."* That is a delegation, not a constraint, so the
architect decides and records it here rather than leaving the record silent.

What is actually in play:

- `docs/product/vision.md` (v1) says the product is **"Not a service. No server, no account, no
  sync between machines, no network access at all. The store is one file on one machine, and the
  tool installs nothing from the internet."**
- `tracker/items/EP-001/item.md` carries the matching success measure: *"The tool runs on a
  machine with a Python interpreter and no network access, and installs nothing from the
  internet."*
- `tracker/project.yaml` currently has `commands.test: null`, which `validate-workspace` reports
  as `project.commands.test-null`. Something must resolve that, and this is the decision it
  depends on.

The measure above is written about the *tool*. The question is whether it also binds
*contributors*: a test suite that needs `pip install pytest` means the repository as a whole
cannot be used on the machine the epic describes.

## Options considered

- **A — Standard library only, at runtime and in tests; tests written with `unittest`.**
  Cost: `unittest` is more verbose than `pytest`, so tests take slightly longer to write.
  Risk: low. Nothing about the project can break because an index is unreachable.
- **B — Standard library at runtime, `pytest` for development.**
  Cost: one network-dependent install step before anyone can run the tests.
  Risk: the "installs nothing from the internet" measure becomes true only of the shipped tool
  and false of the repository, which is the kind of half-truth a success measure exists to
  prevent.
- **C — No automated tests at all.**
  Cost: none up front.
  Risk: unacceptable. The whole product is arithmetic about people's money, and EP-001's third
  success measure ("the amounts net to zero, to the last minor unit") is a property that only a
  test suite can hold down over time.

## Decision

1. **Runtime:** the tool imports only the Python standard library. No third-party package may
   appear in an `import` statement in shipped code.
2. **Baseline:** CPython **3.9 or newer**. Code must not use syntax or standard-library APIs
   introduced after 3.9 (notably: no `match` statements, no PEP 604 `X | Y` annotations at
   runtime, no `tomllib`).
3. **Tests:** written with the standard library's `unittest`. The project's test command is

   ```
   python3 -m unittest discover -s tests -t .
   ```

   `plan` MUST write exactly that string into `tracker/project.yaml` as `commands.test` when it
   plans the first item, which clears the `project.commands.test-null` warning.
4. **Lint:** there is no linter in the standard library, so `commands.lint` stays `null` and the
   `no-lint-errors` gate is legitimately **skipped**, citing this ADR. This is a deliberate
   consequence of decision 1, not an oversight, and any skill recording that skip should say so.
5. **Build:** there is no build step; `commands.build` stays `null`. The tool is run from source.

3.9 is chosen as the floor because it is the oldest interpreter still plausibly present on a
machine the stakeholder would run this on, and nothing in the design needs anything newer.
Nothing prevents running on a much newer interpreter; the floor bounds what may be *used*.

## Consequences

- Easy: cloning the repository and running both the tool and its tests on any machine with a
  Python 3.9+ interpreter and no network access. The success measure holds end to end.
- Easy: `implement`'s `tests-pass` gate has a real command from the first item onwards.
- Hard: no `pytest` fixtures, parametrisation, or plugins. Table-driven cases must be written
  with `subTest`. No automated style enforcement, so review carries that load.
- Hard: no `dataclasses.slots`, no `zoneinfo`-free-lunch assumptions, no newer typing syntax.
- **Reversibility: high, in one direction only.** Raising the baseline (3.9 → 3.11) or adding a
  development dependency is a small change to this ADR plus `project.yaml`. *Removing* a
  dependency once tests are written against it is the expensive direction, which is why the
  restrictive option is the one taken first.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-21T02:26:10Z | answer-questions | EP-001 | First version, deciding EP-001/Q-004 after the stakeholder delegated the choice |
