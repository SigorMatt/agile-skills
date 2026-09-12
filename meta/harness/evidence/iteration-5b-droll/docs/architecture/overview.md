---
title: Architecture overview — droll
version: 3
status: current
updated: 2026-09-11T22:52:59Z
updated-by: review-close
updated-for: WI-0001
---

# Architecture overview — droll

## Shape

droll is one process with one loop. It is started, it reads a line, it prints a line, and it
repeats until the person quits [src: EP-001/Q-001]. There is no server, no file it reads or
writes, no configuration and no state that outlives the process — the history `WI-0002` will add
lives in memory for the duration of one run [src: EP-001/Q-003].

The design is a pipeline of three pure steps wrapped in one impure loop:

```
line of text ──▶ parse ──▶ DiceExpression ──▶ roll ──▶ RollResult ──▶ format ──▶ line of text
                  │                                                                  ▲
                  └────────── rejected ──────────▶ error line ───────────────────────┘
```

Three of the six files under `droll/` reach the outside world, and two of the three reach it in
more than one way. `droll/__main__.py` names the real streams
[src: droll/__main__.py:10]. `droll/cli.py` reads and writes the streams it was handed, **and**
names `random.randint` as the default it hands on to `roll`
[src: droll/cli.py:5; droll/cli.py:15]. `droll/roller.py` calls the generator it was handed, and
names the same default [src: droll/roller.py:6; droll/roller.py:24]. `droll/expression.py` and
`droll/formatting.py` are functions of their arguments, and `droll/__init__.py` is empty
[src: droll/expression.py; droll/formatting.py]. That is what makes the acceptance criteria checkable by
a test that does not drive a terminal: a test hands the loop two strings and a known sequence of
faces, and everything in between is arithmetic.

## Components

| Module | Holds | Depends on |
|--------|-------|------------|
| `droll/expression.py` | the accepted grammar: the parsed form, and the function that turns a line of text into one or rejects it | nothing |
| `droll/roller.py` | the outcome of a roll, and the function that produces one from a parsed expression | `expression`, `random` |
| `droll/formatting.py` | how a roll and a rejection are rendered as one line of plain text | `roller` |
| `droll/cli.py` | the prompt loop: read, dispatch, write, repeat; and the ways a session ends | all three above, and `random` for the default it hands to `roll` |
| `droll/__main__.py` | the entry point, so that `python3 -m droll` starts a session | `cli` |

The dependency arrows run one way, down the table. `formatting` knows about a rolled result and
not about streams. `cli` owns the streams and calls `parse`, but what is accepted and what is not
lives in `expression` and is not restated anywhere else [src: droll/expression.py].

## The seams, and why they are where they are

- **Parsing is separated from rolling** because the grammar is a decision with its own record
  [src: ADR-0001] and it is the half that has to reject as precisely as it accepts. Eight named
  inputs are rejected and four are accepted [src: WI-0001 AC4 "produces a message naming what it
  could not interpret"], which is a table-driven test against one function rather than a session
  transcript.
- **Rolling takes its randomness as an argument**, defaulting to the standard library's. The
  vision declines any claim about statistical quality, reproducibility or seeding
  [src: docs/product/vision.md], so nothing here configures a generator; the argument exists so a
  test can substitute a known sequence and assert on an exact printed line.
- **Formatting is its own function** because `WI-0002` re-renders rolls that have already
  happened. If rendering were inlined into the loop, the history listing would have to reproduce
  it and the two could drift apart — which is precisely what the stakeholder's *"one shape for
  every roll"* rules out [src: WI-0001/Q-001].
- **The loop takes its streams as arguments** rather than reaching for `sys.stdin` and
  `sys.stdout`. `__main__.py` supplies the real ones. This is what lets a test drive a whole
  session, which is the only way several of the criteria are observable at all — AC6 and AC11 are
  about what happens across two inputs in one run
  [src: WI-0001 AC6 "without the tool having been restarted"].

## Conventions this project has adopted

- **No third-party dependency**, for the product or for the tooling that checks it. Tests are
  `unittest`; the lint command is a compile check, with limits stated in its record
  [src: ADR-0002].
- **One stream.** The prompt, roll lines and rejection messages are all written to standard
  output [src: ADR-0003].
- **Started as a module**: `python3 -m droll`. There is no installed console script and no
  packaging metadata yet; adding either is additive and changes nothing below `cli`
  [src: tracker/items/WI-0001/artifacts/plan.md].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-09-11T22:52:59Z | review-close | WI-0001 | Review's D12 audit: `## Shape` said the three files that reach the outside world *"each touches one part of it"* and assigned the generator to `roller` alone, but `droll/cli.py:5` imports `random` and `droll/cli.py:15` defaults `randint` to `random.randint` - the very line the sentence cited as its source. `## Components` compounded it: `roller`'s `Depends on` cell named `random` and `cli`'s, for the identical construct, did not. Both now say what the six files actually do. No code changed |
| 2 | 2026-09-11T22:12:18Z | implement | WI-0001 | Two sentences the implementation falsified, repaired against the code: `## Shape` said only the loop touches the outside world, which the injected-but-defaulted `randint` and `__main__.py`'s naming of the real streams both contradict; `## Components` said `cli` does not know about the grammar, and `cli` imports `parse`. Both now say what is true and name where it is checkable |
| 1 | 2026-09-11T21:58:28Z | plan | WI-0001 | First version: the one-process, one-loop shape, the four modules and the entry point, and the three seams that make WI-0001's criteria observable |
