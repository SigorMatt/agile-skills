---
id: WI-0001
type: work-item
title: Roll a dice expression and show the result with its breakdown
status: done
priority: high
epic: EP-001
created: "2026-09-11T21:26:01Z"
updated: "2026-09-11T23:09:06Z"
branch: wi/WI-0001
outcome: delivered
merge-commit: c52c3a6473774c99267853ea3eb56beb9157db23
---

## Story

As someone who needs dice while sitting at a keyboard, I want to type a dice expression such as
`3d6+2` and be shown both the total and the individual die results that make it up, so that I can
use the number straight away and still see where it came from.

## Acceptance criteria

Round 2. All four questions this item was waiting on are answered by the stakeholder and
propagated: `EP-001/Q-001` (an interactive prompt; a session is one run of it), `EP-001/Q-002`
via ADR-0001 (one dice term with an optional integer modifier), `EP-001/Q-003` (plain text on a
terminal, nothing shared, nothing saved) and `WI-0001/Q-001` (what the breakdown contains).
`artifacts/refinement-qa.md` records the exchange verbatim and the Definition of Ready criterion
by criterion. AC1-AC6 keep their numbers from round 1 on purpose: ADR-0001 cites AC4 and AC5 by
number and by quoted words, and renumbering under a citation is F-094.

Every criterion below is observed by starting the tool, typing the given text at its prompt and
reading what is printed. Where a criterion says "the shown total", it means the number printed on
that roll's own output line.

- [x] AC1 — Started with no arguments, the tool prints a prompt and waits for input. Typing
      `3d6+2` and pressing enter prints a line carrying a total, and the prompt returns.
- [x] AC2 — That same line shows, in plain text, each of the three die results individually and
      the `+2` modifier separately, such that adding the three shown die results and the shown
      modifier gives the shown total. This is option A of `WI-0001/Q-001`, chosen by the
      stakeholder.
- [x] AC3 — Rolling `1d6` two hundred times yields at least three distinct face values, and no
      value outside 1-6. The two numbers were invented by refinement and nobody agreed to them;
      see `artifacts/refinement-qa.md` A1 for what licensed that (nothing) and where a
      disagreement lands.
- [x] AC4 — An expression the tool cannot interpret produces a message naming what it could not
      interpret, and no total, and the prompt is still there afterwards to take the next
      expression. Each of `3x6`, `d`, `3d`, `0d6`, `3d0`, `1d8+1d6`, `4d6kh3` and `hello` is
      rejected this way: `0d6` and `3d0` because ADR-0001's count and sides are positive
      integers, and `1d8+1d6` and `4d6kh3` because they are outside its grammar.
- [x] AC5 — The accepted expression is one dice term with an optional integer modifier,
      `[count]d<sides>[(+|-)modifier]`, per ADR-0001. Each of `d20`, `2d10`, `3d6+2` and `4d8-2`
      is rolled rather than rejected, and AC7 to AC9 say what each of them prints.
- [x] AC6 — Two expressions can be typed and rolled one after the other in the same run: typing
      `d20`, reading its line, then typing `3d6+2` prints a second line without the tool having
      been restarted.
- [x] AC7 — `d20` prints in the same shape as `3d6+2`: its one die result is shown individually
      alongside the total rather than the total being printed on its own, and the shown die result
      equals the shown total.
- [x] AC8 — `2d10` prints two die results individually and no modifier, and the two shown results
      add to the shown total. `4d8-2` prints four die results individually and a modifier of
      `-2`, and the four shown results minus 2 gives the shown total.
- [x] AC9 — `D20` and `3D6+2`, typed with a capital `D`, are rolled exactly as `d20` and `3d6+2`
      are. `  3d6+2  ` with leading and trailing spaces is rolled. `3 d 6`, with spaces inside
      the expression, is rejected by AC4's path.
- [x] AC10 — Typing `quit` at the prompt ends the program, and so does typing `exit`, and so does
      end-of-input (Ctrl-D on an empty line). In each case the process exit status is 0 and
      nothing further is printed that looks like a roll. These three words were chosen by
      refinement and nobody agreed to them; see `artifacts/refinement-qa.md` A3.
- [x] AC11 — After a rejected expression the tool still works: typing `3x6`, reading the message,
      then typing `3d6+2` prints a normal roll line. A rejected expression does not end the
      session and does not change what a later roll prints.

## Out of scope

- Remembering anything between one roll and the next, and any way of asking for that list —
  that is `WI-0002`.
- Any expression form outside ADR-0001's grammar: sums of several dice terms, keep-highest or
  keep-lowest, advantage, exploding dice and multiplication are all out [src: ADR-0001].
- Choosing or configuring the random number generator.

## Notes

The stakeholder's words were: "A little command-line dice roller: I type something like `3d6+2`,
it rolls and shows the result and the breakdown." `3d6+2` is the only expression they gave, and
"the breakdown" is their word rather than a term this project has defined. Refinement put it back
to them as `WI-0001/Q-001` and they chose option A — *"the total plus the individual dice, plain
text. That's all I need to believe the number."* AC2 is now their requirement rather than intake's
reading of it.

**Deliberately unconstrained, and who left it so (Definition of Ready R10).** The upper bound on
the count and the die size is not constrained by any criterion: `100d1000` is inside ADR-0001's
grammar and the tool rolls it. Refinement left it unconstrained under the delegation
`EP-001/Q-002` granted, on the reading that a bound nobody asked for is a rule somebody has to
discover. Where the combination of a capital `D` and a modifier is concerned, AC9 names `3D6+2`
rather than leaving the combination to be inferred.

**The shape of the printed line, routed to `plan` rather than to the stakeholder.** `WI-0001/Q-001`
told the stakeholder that the exact spacing and punctuation of the breakdown was ours to settle,
and asked only what information is present. Their answer added *"plain text"* and settled nothing
further, so the layout — separators, brackets, where the total sits — is `plan`'s, by the same
test that routed the error stream there. AC2 constrains the information, not the punctuation.

**The expression grammar, and the licence it was decided under.** AC5 and the exclusions above
come from ADR-0001, which the architect wrote from the stakeholder's answer to `EP-001/Q-002`.
That answer chose the option; the notation inside it was left to us in the same sentence.

**Under delegation:** EP-001/Q-002 — the notation inside standard single-term dice expressions:
whether the count may be omitted, the sign and presence of the modifier, and the bounds on the
count, the die size and the modifier. Spent in ADR-0001 for the grammar itself, and in round 2 of
refinement for the three things ADR-0001 left open: the letter case of `d` (AC9), the treatment of
whitespace (AC9) and the absence of an upper bound on the count and the die size (the R10 note
above). `artifacts/refinement-qa.md` round 2 carries each as an `[assumed]` answer.

**Open design question, routed to `plan` rather than to the stakeholder.** Which stream an error
message is written to, and what exit code accompanies it. The answer would be the same whoever
the stakeholder was, so it is not theirs to spend attention on. `EP-001/Q-001` is now answered —
the tool is one long-lived prompt, not a process per roll — so the question narrows to which
stream the prompt writes an error message on. The exit code is no longer part of it: AC10 fixes
it at 0 for the three ways a session is ended deliberately, which is the only exit this item
produces. `plan` settles the stream under its own preference order and records it. See
`artifacts/refinement-qa.md` A2.

**Assumption taken under no licence.** AC3's `200` and `3` were invented by refinement. The one
delegation the stakeholder has since granted — `EP-001/Q-002`, *"whatever's standard, don't
overthink it"* — covers the notation of a dice expression and does not reach how many times a die
is rolled in a test or how varied the result has to be, so nothing covered this. It is recorded
under Definition of Ready R12's second branch in `artifacts/refinement-qa.md` A1, with where a
disagreement about it would land.

**A second assumption taken under no licence.** AC10's `quit`, `exit` and end-of-input were
chosen by refinement. The stakeholder said only *"close it when we're done for the night"*, which
names no input, and the one delegation they granted is about dice notation and does not reach a
command word. Recorded under R12's second branch in `artifacts/refinement-qa.md` A3, with where a
disagreement about it would land.
