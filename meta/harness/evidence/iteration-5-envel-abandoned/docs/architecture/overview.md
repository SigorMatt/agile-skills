---
title: Architecture overview
version: 3
status: current
updated: 2026-09-10T15:28:26Z
updated-by: implement
updated-for: WI-0002
---

# Architecture overview

## What this is

`envel` is a command-line program that keeps one person's envelope budget on their own machine
[src: docs/product/vision.md]. It is a program that starts, reads a file, does one thing, writes
the file and exits. There is no process that stays running, nothing listening on a port, and
nothing it talks to over a network [src: EP-001/Q-001].

This document describes the shape the system is built to. It was written for WI-0001 before the
code existed, naming the modules the plan called for; the implementation of WI-0001 has since
written them, and the rows below now cite the files rather than the design
[src: commit 34b69df]. WI-0002 added the money — two recording commands, a balance on the
listing, and a fifth module to hold the rules that decide them [src: WI-0002; ADR-0007].

## The shape

Five pieces, in a straight line from the terminal to the file:

| piece | what it is responsible for |
|-------|---------------------------|
| `bin/envel` | the executable the person types. Puts the repository root on `sys.path` and calls `main` [src: bin/envel:9; bin/envel:11]. Eleven lines, of which two are statements about the tool [src: ADR-0002] |
| `envel/cli.py` | reads `argv`, dispatches to `new`, `list`, `income` or `spend`, writes to stdout and stderr, and returns the process exit status [src: envel/cli.py:42]. It reads the one option the tool has, `--date`, by hand rather than through `argparse` [src: envel/cli.py:104; tracker/items/WI-0002/artifacts/plan.md] |
| `envel/envelopes.py` | the domain rules: `identity` and `display` [src: envel/envelopes.py:29], `find` and `add` [src: envel/envelopes.py:48], and `listing`, which fixes the order envelopes are printed in [src: envel/envelopes.py:60; ADR-0004] |
| `envel/movements.py` | the money rules: `parse_amount` and `format_amount` [src: envel/movements.py:50; envel/movements.py:68; ADR-0006], `parse_date` and `today` [src: envel/movements.py:77], and `balances`, which computes what is left in each envelope from the movements rather than reading a stored total [src: envel/movements.py:97; ADR-0007] |
| `envel/store.py` | `store_path` resolves where the file is [src: envel/store.py:28], `load` and `save` move the document [src: envel/store.py:40; envel/store.py:79; ADR-0003] |

The dependency direction is one-way. `cli` imports the other three [src: envel/cli.py:14];
`movements` imports `envelopes` for the identity rule and does not import `store`
[src: envel/movements.py:13]; `envelopes` imports nothing of this project's and touches no
filesystem; and `store` names no envelope rule and no money rule. The reason to hold that line is
that the domain rules are the part later items keep adding to — transfers, corrections, a monthly
summary [src: docs/product/vision.md] — and they are the part worth being able to test without a
filesystem, which `tests/test_movements.py` is
[src: run: python3 -m unittest tests.test_movements -v 2>&1 | tail -3 → OK, 19 tests, no
temporary directory and no subprocess].

## State

There is one piece of state: a JSON document holding the store-format version, the envelopes in
creation order, and the movements — the income and the spending — in the order they were recorded
[src: ADR-0007; envel/store.py:25]. The version is 2; a document written at version 1, before
there were movements, is upgraded when it is read and the file is not rewritten
[src: envel/store.py:65]. Its location comes from `ENVEL_FILE` when that is set, and otherwise
from the XDG data directory [src: ADR-0003].

An envelope's balance is not in that document. It is computed from the movements every time it is
needed [src: envel/movements.py:97; tracker/items/WI-0002/artifacts/plan.md], so the movements are the only
thing that can be wrong. A store file that is absent means an empty store rather than
an error, which is what lets the tool be run for the first time [src: WI-0001 AC6 "run before any
envelope has ever been created exits 0"].

Writes replace the file atomically, so an interrupted run leaves either the old store or the new
one [src: ADR-0003].

## Conventions

- Python 3, standard library only, for the runtime and for the checks [src: ADR-0001].
- Tests are `unittest`, under `tests/`, run with `python3 -m unittest discover -s tests -t .`
  [src: ADR-0001; run: python3 -m unittest discover -s tests -t . → exit 0, 69 tests, OK]. The
  end-to-end ones invoke `envel` as a subprocess through a `PATH` with `bin/` in front of it and
  `ENVEL_FILE` pointing into a temporary directory of that case's own
  [src: tests/test_cli.py:35], which is how a criterion about "before any envelope has ever been
  created" is observed without touching a real store [src: WI-0001].
- An exit status of 0 means the command did what was asked. A non-zero status means it did not,
  and stderr says why.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-09-10T15:28:26Z | implement | WI-0002 | A fifth row, `envel/movements.py`, and the `envel/cli.py` row now names four commands; the dependency-direction sentence enumerates four modules rather than three; `## State` says the document holds the movements at version 2 and that a balance is computed rather than stored; the `envel/store.py` line citations and the end-to-end helper's citation moved, and the test count in the recorded run is 69 |
| 2 | 2026-09-10T13:57:38Z | implement | WI-0001 | The four rows of `## The shape` and the dependency-direction sentence now cite the files WI-0001 wrote, instead of the design that called for them; the test convention cites the run |
| 1 | 2026-09-10T13:44:29Z | plan | WI-0001 | First version: the four pieces, the one-way dependency direction, the single JSON store, and the standard-library-only convention |
