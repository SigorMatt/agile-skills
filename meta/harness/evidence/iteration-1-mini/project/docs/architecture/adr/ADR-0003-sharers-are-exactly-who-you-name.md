---
title: The sharers of an expense are exactly who you name, with "everyone" as the default
version: 1
status: current
updated: 2026-08-21T02:32:00Z
updated-by: answer-questions
updated-for: WI-0002
---

# ADR-0003 — The sharers of an expense are exactly who you name, with "everyone" as the default

- **Status:** accepted
- **Date:** 2026-08-21
- **Decided by:** answer-questions (architect), for WI-0002
- **Supersedes:** —

## Context

`WI-0002/Q-002` asked whether the payer of an expense is automatically one of the people sharing
it (option **B**), or whether the list of sharers is exactly the people who share, so that a
payer left off the list paid for other people entirely (option **A**). The recommendation was
**A**, on the grounds that WI-0002's AC2 already promises a "shared by everyone" shorthand, which
removes most of B's typing saving.

The stakeholder answered: *"If I paid and it's shared by all of us, include me automatically —
most of the time I'm one of the people splitting it too."*

That sentence is **conditional**, and the condition is the everyone case: *if* the expense is
shared by all of us. It settles the common case beyond doubt and says nothing directly about the
uncommon one — an explicit list of sharers that happens not to include the payer. The two
readings diverge materially:

- Under **A**, `expense 30 --paid-by alice --shared-by bob,carol` charges Bob and Carol 15 each
  and Alice nothing. "I bought the taxi for you two, I walked home" is expressible.
- Under **B**, the same command charges all three 10 each, and paying for other people without
  sharing becomes inexpressible without a special flag.

A wrong choice here does not crash anything; it silently produces different money. That is why it
was asked before anything was built, and why the residual ambiguity is recorded here rather than
resolved by picking whichever letter reads closest to the stakeholder's phrasing.

## Options considered

- **A — The sharers you list are exactly the sharers, and an omitted list means everyone.**
  Cost: in the rare explicit-list case you must type your own name to be included.
  Risk: forgetting to is a silent error that produces wrong money — the exact risk option **C**
  of the original question proposed to guard with a warning.
- **B — The payer is always among the sharers, whatever list is given.**
  Cost: a special flag, or nothing, for "I paid for other people and did not share".
  Risk: "shared by Bob and Carol" quietly means three people share. For a tool whose output is
  disputed at a table, a command that does not mean what it says is the worse failure. It also
  removes a capability rather than adding a keystroke, and removed capability is the harder thing
  to notice missing.
- **C — B, but reachable only through an explicit `--everyone` and never implicit.**
  Cost: the stakeholder's common case needs a flag on every expense.
  Risk: directly contradicts *"I don't want an extra setup step"*-style economy the stakeholder
  has shown twice (here and in `WI-0001/Q-002`).

## Decision

1. **The sharers of an expense are exactly the people named.** No name is added implicitly.
2. **When no sharers are given at all, the expense is shared by everyone currently in the
   group — the payer included.** This is the default, requiring no flag and no names, and it is
   what the stakeholder asked for: the common case costs zero typing and includes them
   automatically. An explicit way to say the same thing (`--shared-by everyone`, or the
   equivalent the CLI settles on) is also accepted, per WI-0002 AC2.
3. **The sharer set is fixed when the expense is recorded.** Adding a person to the group later
   does not retroactively change who shared an earlier expense, even one recorded with the
   default. Otherwise every past expense would silently re-divide the moment a new friend is
   added.
4. **If an explicit sharer list is given and the payer is not in it, the tool prints a note on
   stderr** saying that the payer is not sharing this expense and is therefore owed the whole
   amount. The expense is still recorded and the exit status is still zero: this is a legitimate
   thing to do, not an error. The note exists so that the silent error in option A's risk column
   becomes a visible one.
5. **Shares are equal** among whoever the sharers turn out to be, per `EP-001/Q-001`.

Decisions 1–3 follow from the stakeholder's answer for the case they described. Decision 4 is the
architect's, and it is the mitigation that makes choosing A over B defensible.

## Consequences

- Easy: the common case — "I paid, we all split it" — is the shortest command the tool has, with
  no names and no flags.
- Easy: "I paid for these two and did not share" stays expressible, and now announces itself.
- Easy: every command means literally what it says, which matters when the output is read aloud
  to the people it charges.
- Hard: a user who explicitly lists sharers and forgets themselves gets the wrong answer unless
  they read stderr. Decision 4 mitigates but does not eliminate this.
- **Open, and flagged for the stakeholder rather than buried here:** their answer was conditional
  on "shared by all of us", so decisions 1 and 4 cover a case they did not speak to. If they
  actually meant "include me whatever list I give", that is option **B** and this ADR must be
  superseded. `tracker/items/WI-0002/item.md` says so in `## Notes` where the implementer will
  see it.
- **Reversibility: high.** Switching to B is a change to one function that resolves a sharer list,
  plus this ADR, plus WI-0002's AC2 and AC6 — provided it happens before a store full of expenses
  exists. Afterwards it is not reversible at all without knowing, for each recorded expense,
  whether the payer was omitted deliberately: the stored data cannot distinguish "Alice did not
  share" from "Alice forgot to type her name". That asymmetry is the reason decision 4 exists,
  and the reason this is worth confirming early.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-21T02:32:00Z | answer-questions | WI-0002 | First version, deciding WI-0002/Q-002 where the stakeholder's answer covered only the everyone case |
