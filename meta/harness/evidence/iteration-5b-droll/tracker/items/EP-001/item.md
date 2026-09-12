---
id: EP-001
type: epic
title: A command-line dice roller with a session history
status: open
priority: high
created: "2026-09-11T21:25:36Z"
updated: "2026-09-11T21:44:56Z"
---

## Goal

Someone who needs dice at a keyboard — running or playing a tabletop game, or just checking what
a handful of dice tends to do — can type a dice expression such as `3d6+2`, immediately see both
the total and how that total was arrived at, and look back over the rolls they have already made
without having written any of them down. The tool is an interactive prompt they start once and
keep open, typing rolls one after another and quitting when they are done for the night, so "the
current session" is one run of that prompt [src: EP-001/Q-001].

## Why now

Rolling by hand is fine until you want the arithmetic done for you, and a pocket calculator or a
`python -c` one-liner gives a number with nothing behind it: you cannot see which die came up
what, and the moment you press enter again the previous result is gone. Two things are missing
and neither is available anywhere today — the **breakdown**, which is what makes a surprising
total believable, and the **history**, which is what lets you answer "what did I roll a minute
ago?". Without them the tool is a worse calculator; with them it replaces the dice.

## Success measures

- Typing a dice expression at the prompt produces a total, printed, in one step.
- The expressions accepted are one dice term with an optional integer modifier — `d20`, `3d6+2`,
  `4d8-2` — as decided in ADR-0001 from the stakeholder's answer [src: ADR-0001].
- A result printed shows each individual die's face value alongside any modifier, in plain text,
  so a reader with a pen can re-add the components and get the printed total. This was intake's
  reading of "the breakdown" and is now the stakeholder's own requirement [src: WI-0001/Q-001].
- After making several rolls without leaving the prompt, the user can ask for and see those rolls
  listed in the order they were made, each with the expression that produced it and its total.
- An expression the tool cannot interpret produces a message identifying what it could not
  interpret, and no number.
- The tool is run with Python, which is the stakeholder's stated constraint.

## Scope

- Reading a dice expression typed by the user at the prompt and evaluating it with random die
  results.
- Presenting each result with a breakdown a person can check by hand.
- Recording the rolls made during the current session and showing them back on request.
- An interactive command-line prompt, in Python: started once, reading expressions one after
  another until the user quits [src: EP-001/Q-001].

## Out of scope

These are exclusions derived from what a reader would otherwise assume was included. The
stakeholder was invited to contradict any of them in `EP-001/Q-003`; their reply contradicted none
and bore on two of them, as annotated below. The unannotated ones remain derived rather than
stated [src: EP-001/Q-003].

- Keeping history across separate uses of the tool — saving rolls to a file, a database, or
  anywhere else that outlives the session. Confirmed, and named as a want for later rather than
  now: *"keeping the history for just the current session is fine; being able to save it across
  sessions would be nice someday but I don't need it now"* [src: EP-001/Q-003].
- Any interface that is not the command line: no GUI, no web page, no chat bot.
- Anything shared or networked: no rolls visible to another person, no multi-user session. The
  stated setting is the stakeholder and their gaming group on game night — *"nothing bigger than
  that"* — one person at one keyboard, which asks for nothing here [src: EP-001/Q-003].
- Game-system knowledge beyond dice arithmetic: no character sheets, no skill checks, no rule
  lookups, no damage types.
- Reproducible or seeded randomness, and any claim about the statistical quality of the generator
  beyond what Python's standard library provides.
- Packaging and distribution — publishing to an index, installers, or a versioned release.
