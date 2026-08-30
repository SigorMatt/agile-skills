---
title: Architecture overview
version: 4
status: current
updated: 2026-08-30T00:23:48Z
updated-by: plan
updated-for: WI-0003
---

# Architecture overview

## The shape of the system

One executable Python 3 file, read from standard input, written to standard output, with no
arguments, no configuration and no dependency outside the standard library [src: ADR-0001]. There
is no package, no build step and nothing to install: the stakeholder runs it from their editor
against a buffer before committing [src: EP-001/Q-002].

```
stdin (bytes)
  │  decode utf-8, errors=surrogateescape
  ▼
split into lines, keeping each line's own ending
  │
  ▼
scan ── fenced code block?  ──────────► copy the line
  │
  ├── part of a uniformly indented run of |…| lines? ──► collect a candidate block
  │                                                          │
  │                        well-formed table? ── no ─────────┴─► copy the block, byte for byte
  │                                    │ yes
  │                                    ▼
  │                        measure columns, compose rows
  ▼
join, encode utf-8 errors=surrogateescape, write to stdout (bytes)
```

Everything in the middle column is a copy. The tool's default is to do nothing, and every rule
that recognises something is a narrow exception to that default — which is the product's first
property, not an implementation preference [src: docs/product/vision.md].

## Why bytes at the edges

The strongest promise the tool makes is that anything that is not a table comes back exactly as
it went in [src: EP-001/Q-001], and that promise has to survive input the tool cannot interpret.
Decoding with `surrogateescape` and encoding back the same way lets an arbitrary byte sequence
round-trip through a `str` pipeline unchanged, so a document that is not valid UTF-8 is copied
rather than rejected halfway through [src: WI-0001 AC6]. The alternative — operating on `bytes`
throughout — would push the same problem into every width and cell-splitting function for no gain.

## The rule documents

A reader deciding whether the code is right should read these, in this order, and not the code:

- **ADR-0003** — what counts as a table, and what one looks like coming back. Eleven numbered
  decisions, each a test [src: ADR-0003]. Its decision 9 fixes the shape of a content cell but not
  where a marked column's padding sits inside it; it carries a `## Corrections` entry saying so.
- **ADR-0007** — which side of the text the padding goes, per the column's alignment marker; that
  an odd centring remainder falls to the right; and that a cell containing a line break is exempt
  from its column's marker. It supersedes ADR-0005, carrying every other decision in it forward
  unchanged [src: ADR-0007]. ADR-0005 remains readable as what was believed before the stakeholder
  narrowed it [src: ADR-0005].
- **ADR-0008** — the edges of that exemption: which written forms of a break tag make a cell
  exempt, that a trailing backslash does not, and that an exempt cell is still padded out to its
  column's width [src: ADR-0008].
- **ADR-0009** — where the exemption is applied in the code: per cell inside `compose_row`, not by
  rewriting a column's alignment [src: ADR-0009].
- **ADR-0004** — what a delimiter row that carries an alignment marker is composed as: the colons
  the input had, at the ends it had them at [src: ADR-0004].
- **ADR-0001** — the runtime, and why there is no framework in this repository [src: ADR-0001].
- **ADR-0006** — how a test method is named, so that one item's coverage check cannot be broken by
  a later item's tests [src: ADR-0006].

ADR-0002 is superseded by ADR-0003 and records what was believed before the stakeholder answered
WI-0001's round 1 [src: ADR-0002].

## Layout

| path | what lives there |
|------|------------------|
| `mdtab.py` | the filter: recognition, measurement, composition, and `main()` |
| `tests/` | `test_mdtab.py`, one `unittest` method per acceptance criterion, named `test_<item>_ac<n>_<slug>` for the criterion it covers [src: ADR-0006] |
| `tests/fixtures/` | input and expected-output documents, compared byte for byte. `not_utf8.markdown` is not named `.md` on purpose - it is deliberately invalid UTF-8, and the pipeline's own markdown walkers decode every `.md` file in the repository without an error handler |
| `tracker/`, `docs/` | the record; no code |

`tracker/project.yaml` names the commands: `commands.test` runs the suite with `unittest`
discovery, `commands.lint` byte-compiles the project's Python outside `.claude/`. Neither
installs anything.

## What the shape does not include

No package directory, no `setup.py` or `pyproject.toml`, no entry-point script, no configuration
file, no logging, and no reading or writing of files by path. Each of those would be a thing to
install or configure before the tool could be run, which is the one property the stakeholder
stated about how it must work [src: EP-001/Q-002].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 4 | 2026-08-30T00:23:48Z | plan | WI-0003 | The rule-document list is brought up to date: ADR-0007 replaces ADR-0005 as the current statement of where a marker puts cell text, and ADR-0008 and ADR-0009 are added — the edges of the multiline-cell exemption, and where it is applied in the code |
| 3 | 2026-08-29T22:41:48Z | plan | WI-0002 | The rule-document list now names ADR-0005, which decides where a marker puts cell text, and ADR-0006, which names test methods per item; the layout table states the test-naming convention |
| 2 | 2026-08-29T22:01:03Z | implement | WI-0001 | Layout table corrected against the code as built: one test module rather than one per criterion group, and why the non-UTF-8 fixture is not named `.md` |
| 1 | 2026-08-29T21:47:00Z | plan | WI-0001 | First version, written while planning the first item |
