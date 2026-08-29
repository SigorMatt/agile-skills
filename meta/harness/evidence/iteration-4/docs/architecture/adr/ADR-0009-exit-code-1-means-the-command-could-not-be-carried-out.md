---
title: Exit code 1 means the command could not be carried out, of which an unusable store is one case
version: 1
status: current
updated: 2026-08-29T13:34:39Z
updated-by: plan
updated-for: WI-0004
---

# ADR-0009 — Exit code 1 means the command could not be carried out, of which an unusable store is one case

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** plan (architect), for WI-0004
- **Supersedes:** —

## Context

`ADR-0005` fixed three exit codes: *"`0` on success. `2` when the command line itself is wrong —
an unknown command, the wrong number of arguments, or an empty card side. `1` when the command
line was fine and the store could not be used"* [src: ADR-0005].

`recall delete 9` against a readable store holding cards 1, 2 and 3 is neither failure. The
command line is well formed — one command name, one positional integer — and the store is
perfectly usable. It is a new third thing: a valid request the tool cannot carry out because
what it names is not there.

`refine` saw this and left it here rather than guessing: `AC5` and `AC6` say *non-zero*, which is
decidable, and the item's notes record that the value is `plan`'s and that `ADR-0005` may need
extending [src: WI-0004; src: WI-0004 AC5; src: WI-0004 AC6].

`ADR-0005` does not forbid this case — its exit-code section names only a wrong command line and
an unusable store, and never a request the tool understood but could not carry out
[src: ADR-0005]. So what follows widens a category rather than reversing a decision, and
`ADR-0005` is not superseded.

## Options considered

- **A — return `2`, folding it into "the command line was wrong".** Cost: `2` stops meaning
  "wrong on the command line's own terms". There is a precedent pulling this way — `ADR-0005`
  puts an empty card side under `2`, and that is an argument *value* rather than a syntax error
  [src: ADR-0005]. But an empty card side is wrong against every store that could exist, whereas
  `9` is wrong only against this one, and only until someone adds six more cards. Risk: the
  useful property that `2` can be decided without reading the user's data is lost, and the four
  cases `AC8` checks stop being one category [src: WI-0004 AC8].
- **B — widen `1` to "the command line was fine and the command could not be carried out",
  with the unusable store as one instance.** Cost: the README's one-line gloss for `1` has to be
  rewritten, and a caller reading only the code can no longer conclude "your store is broken"
  from `1` alone — the message distinguishes them. Risk: low; no existing command gains or loses
  a code, so no delivered criterion moves.
- **C — a third failure code, `3`, for "not found".** Cost: a fourth meaning in a scheme
  deliberately kept small, and every future failure then has to argue whether it is a `1` or a
  `3`. Risk: it buys a distinction nobody has asked for — this is a tool one person drives by
  hand, and the reader of the failure is the person who typed it [src: docs/product/vision.md].

## Decision

Option B. The scheme keeps three codes, and the line between `1` and `2` is drawn where it can
be checked:

- **`2` — the command line is wrong on its own terms.** Decidable by looking at the arguments
  alone, without opening the store: an unknown command, the wrong number of arguments, an empty
  card side, and an argument that is not a card number at all. `recall delete` with no argument,
  `recall delete 1 2`, `recall delete two` and `recall delete 0` are all `2`
  [src: WI-0004 AC8].
- **`1` — the command line was fine and the command could not be carried out.** Two instances
  today: the store could not be read or written, which is `ADR-0005`'s case and is unchanged
  [src: ADR-0005]; and a card number that names no card in the store, which is this item's.
  `recall delete 9` against a readable store exits `1`, reports it on stderr naming the number,
  and prints nothing on stdout [src: WI-0004 AC5].
- **A missing store file takes the same path as a number that names no card.** `load` treats a
  file that is not there as an empty document, so `recall delete 1` with no store finds no card 1
  and exits `1` for that reason, having created nothing [src: recall.py; src: WI-0004 AC6]. That
  is one code path rather than two, and it matches how `list` already treats a missing file as an
  empty pile [src: ADR-0004].
- **No existing behaviour changes.** `add`, `list` and `review` return exactly what they returned
  before this ADR; it adds a case, it does not reclassify one [src: recall.py].

## Consequences

What becomes easy: every future command that can fail to find what it was pointed at has a code
already, and the rule for choosing between `1` and `2` is mechanical — could you have known from
the command line alone?

What becomes hard: a script that wanted to distinguish "your store is broken" from "that card is
not there" has to read stderr rather than the exit code. Option C is what that script would need,
and it can be added later without disturbing this line, because `1` would simply narrow again.

The README's exit-code table states the old, narrower meaning of `1` and is made wrong by this
decision, so the item that carries this ADR updates it [src: README.md].

**Reversibility: high.** Nothing persists an exit code — no file, no state, no protocol. Changing
the scheme is a change to the command functions and one table in the README.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-29T13:34:39Z | plan | WI-0004 | First version: exit code 1 widened from "the store could not be used" to "the command could not be carried out", with the store case and a card number naming no card as its two instances; 2 stays decidable from the command line alone |
