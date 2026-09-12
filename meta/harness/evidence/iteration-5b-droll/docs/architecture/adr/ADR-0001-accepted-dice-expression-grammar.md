---
title: One dice term with an optional integer modifier
version: 2
status: current
updated: 2026-09-11T21:46:56Z
updated-by: answer-questions
updated-for: WI-0001
---

# ADR-0001 — One dice term with an optional integer modifier

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** answer-questions (architect), for EP-001
- **Supersedes:** —

## Context

`EP-001/Q-002` asked the stakeholder which dice expressions the tool must accept, and offered
three widening options: A, a single dice term with an optional modifier; B, sums of several
terms; C, B plus keep-highest, advantage, exploding dice and multiplication.

They replied: *"Just the usual — d20, 2d8+1, that kind of thing. Whatever's standard, don't
overthink it."*

That settles the **option** and leaves the **notation** open. Both expressions they named are
single dice terms — `d20` omits both the count and the modifier, `2d8+1` supplies both — so neither reaches
past option A, and *"don't overthink it"* rules out option C, whose whole cost is the thinking.
What it does not settle is the incidental notation inside "the usual": whether a count may be
omitted, whether a modifier may be negative, and what the bounds on the three numbers are. Those
are the details their answer hands to us, and they have to be written down somewhere a parser and
a test can both be checked against, because `WI-0001` AC5 requires one criterion per accepted
form before that item can be Ready [src: WI-0001].

**Under delegation:** EP-001/Q-002 — the notation inside standard single-term dice expressions:
whether the count may be omitted, the sign and presence of the modifier, and the bounds on the
count, the die size and the modifier.

## Options considered

- **A — the grammar below: `[count]d<sides>[(+|-)modifier]`, count and modifier optional.**
  Cost: one small parser, four or five criteria. Risk: a stakeholder who meant `1d8+1d6` by "the
  usual" has to type two rolls and add them; the cost of finding that out is one more roll-sized
  item later, not a rewrite, because a multi-term grammar contains this one.
- **B — the same, but requiring an explicit count, so `1d20` rather than `d20`.**
  Cost: the same parser, marginally simpler. Risk: it rejects `d20`, which is one of the two
  expressions the stakeholder actually typed in their answer. Refused on that ground alone.
- **C — accept sums of several terms now (option B of `EP-001/Q-002`), on the reading that "the
  usual" includes `1d8+1d6+3`.** Cost: an arithmetic parser rather than a pattern match, and
  roughly double the criteria. Risk: it spends the stakeholder's budget on a reading of their
  words that their own two examples do not support, and *"don't overthink it"* is evidence
  against it.

## Decision

An accepted expression is one dice term with an optional integer modifier:

```
expression := [count] "d" sides [ ("+" | "-") modifier ]
```

- `count` is a positive integer. When it is omitted the expression means one die, so `d20` and
  `1d20` are the same roll.
- `sides` is a positive integer, and is not defaulted or restricted to the familiar solids: `d3`
  and `d100` are as acceptable as `d20`.
- `modifier`, when present, is a non-negative integer preceded by `+` or `-`, and is added to or
  subtracted from the sum of the dice.

Anything that is not of this form is not accepted, and is reported by `WI-0001` AC4's error path
rather than rolled [src: WI-0001 AC4 "produces a message naming what it could not interpret"].

Two details are deliberately **not** decided here, because they are cheap to settle later and
neither changes what is built: the letter case of `d`, and whether surrounding or internal
whitespace is tolerated. They sit inside the same delegation and belong to `refine`, which is
about to write the criteria, or to `plan`.

## Consequences

- `WI-0001` can state one acceptance criterion per accepted form — a bare `d20`, a count with a
  positive modifier, a count with a negative modifier, a count with the modifier omitted — and one
  for the rejection path, which is what its AC5 asks for
  [src: WI-0001 AC5 "one dice term with an optional integer modifier"].
- The expression reader is a pattern match over three numbers rather than an arithmetic parser,
  which is the smaller half of `WI-0001`.
- **Reversible, at a cost that grows.** A multi-term grammar (`EP-001/Q-002` option B) contains
  this one, so widening later is additive for the parser. What is not free is the output shape:
  `WI-0001/Q-001` fixes a breakdown built around one dice group and one modifier, and a sum of
  several terms would need that line re-designed and re-agreed with the stakeholder. Widening
  before any code exists would have been cheaper than widening after; widening after is an item,
  not a rewrite.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-09-11T21:46:56Z | answer-questions | WI-0001 | Provenance: the two `WI-0001` acceptance-criterion citations now quote the criterion, because the item returned to `draft` where its numbering may still change |
| 1 | 2026-09-11T21:37:43Z | answer-questions | EP-001 | First version: the accepted expression grammar, decided from the stakeholder's answer to `EP-001/Q-002` and the delegation it carried |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-09-11T21:46:56Z | answer-questions | WI-0001 | provenance | `## Decision`'s last paragraph and `## Consequences`'s first bullet cited `[src: WI-0001 AC4]` and `[src: WI-0001 AC5]`. Both resolved when they were written, with `WI-0001` at `awaiting-answer`; both stopped resolving when the same execution returned the item to `draft`, where a bare `AC<n>` names nothing because the numbering may still change. Each citation now quotes the criterion's words. Neither assertion is changed. [src: run: python3 .claude/agile-skills/scripts/validate-workspace . → exit 1, claim.citation.unresolved on both markers] |
