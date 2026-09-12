---
id: WI-0002
type: work-item
title: Keep the rolls made during a session and show them back
status: awaiting-answer
priority: medium
epic: EP-001
created: "2026-09-11T21:26:01Z"
updated: "2026-09-11T23:14:01Z"
depends-on:
  - WI-0001
---

## Story

As someone making a series of rolls, I want the tool to remember the rolls I have made in this
session and show them to me on request, so that I can answer "what did I roll a minute ago?"
without having written anything down.

## Acceptance criteria

These are what intake could already state; `refine` is expected to sharpen them. `EP-001/Q-001`
is now answered: a session is one run of an interactive prompt, so the history is what has been
rolled since the tool was started and the history is asked for by typing something at that same
prompt [src: EP-001/Q-001].

- [ ] AC1 — After making several rolls, there is something the user can type at the prompt that
      lists those rolls. Refinement settles what that input is.
- [ ] AC2 — The listing shows, for each roll, the expression that was rolled and the total that
      came out of it, in the order the rolls were made.
- [ ] AC3 — A roll that was rejected as uninterpretable does not appear in the history.
- [ ] AC4 — Asking for the history before any roll has been made produces a message saying there
      are none, not an error and not an empty screen.
- [ ] AC5 — A session is one run of the prompt: the history holds the rolls made since the tool
      was started, quitting ends it, and nothing is written to disk to be read back by a later
      run [src: EP-001/Q-001] [src: EP-001/Q-003].

## Out of scope

- Saving the history anywhere that outlives the session — see `EP-001`'s out-of-scope list.
- Re-rolling, editing or deleting an entry in the history.
- Statistics over the history (averages, distributions, totals across rolls).

## Notes

The stakeholder's words were: "It should remember the rolls from the current session so I can see
a history." "Current session" is their phrase and was the thing `EP-001/Q-001` asked about. They
answered it: *"A — the open prompt. I fire it up, keep typing rolls one after another, and close it when
we're done for the night."* AC5 is that answer.

This item depends on `WI-0001` because there is nothing to remember until rolling works. That
dependency, not a stated preference, is why `WI-0001` is the higher priority of the two — the
stakeholder gave no ordering.

## Notes — refinement round 1

Refinement round 1 ran on 2026-09-11 and **suspended on `Q-001`**, which is with the stakeholder.
The acceptance criteria above are still intake's and have deliberately **not** been rewritten:
`AC2` is the subject of the open question, and rewriting the list around a guess is what the
question exists to prevent. The whole list is rewritten in round 2, once the answer is in.
`artifacts/refinement-qa.md` carries the Definition of Ready criterion by criterion — R4, R6, R8
and R10 currently fail — and the full reasoning for everything below.

**Decided by refinement, under no licence from the stakeholder** (Definition of Ready R12, second
branch; reasoning and landing places in `artifacts/refinement-qa.md`):

- **D1** — the input that asks for the history is the word `history`, typed on its own, case
  ignored as `quit` and `exit` already are [src: droll/cli.py:34]. It is not a valid expression
  under ADR-0001, so it cannot collide with a roll. Named to the stakeholder in `Q-001`'s
  `## Context` so they can contradict it for free.
- **D2** — typing `history` does not itself add an entry to the history; only accepted rolls do.
- **D3** — no cap: the whole session's rolls are kept. No criterion will name a number.

**Open design question, routed to `plan` rather than to the stakeholder:** the layout of the
listing — indentation, whether entries are numbered, how columns line up, what separates entries.
This is the same call `WI-0001/Q-001`'s answer left open for a single roll line, applied to a
list. A second one goes with it: how the rolls are held in memory, which no criterion can see.

**Behaviour combinations this item introduces** (Definition of Ready R10), so that none of them is
discovered rather than decided:

- `history` with rolls in the session — the main path, and what `Q-001` settles the shape of.
- `history` before any roll — has a criterion already (`AC4`), and its wording is rewritten in
  round 2 to say what is observed.
- `history` in a session where every input so far was rejected — the same case as the one above,
  because a rejected expression is not an entry (`AC3`). Round 2 makes that explicit rather than
  leaving a reader to compose `AC3` and `AC4` themselves.
- `history` twice in a row — D2: the second listing is identical to the first.
