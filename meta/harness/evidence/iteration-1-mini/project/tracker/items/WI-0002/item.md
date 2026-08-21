---
id: WI-0002
type: work-item
title: Record an expense paid by one person and shared by several
status: awaiting-answer
priority: high
epic: EP-001
created: "2026-08-21T02:03:44Z"
relates-to:
  - WI-0001
updated: "2026-08-21T03:51:28Z"
---

## Story

As a member of the friend group, I want to record that one person paid an amount that a named
set of people shared, so that the group's spending is captured as it happens rather than
reconstructed later.

## Acceptance criteria

- [ ] AC1 — a command records an expense with an amount, the person who paid it, and the people
      who shared it, and the expense survives into a later run of the tool. The expense is
      **divided equally** among its sharers: nothing in the command or in the stored record
      carries a per-person amount, weight or percentage. (EP-001/Q-001.)
- [ ] AC2 — the sharers are exactly the people named. Giving **no** sharers records the expense
      as shared by everyone in the group at that moment, the payer included, with no flag and no
      names typed; there is also an explicit way to say "everyone" that means the same thing.
      Naming sharers explicitly records exactly those people and nobody else. The sharer set is
      fixed when the expense is recorded, so adding a person to the group afterwards does not
      change who shared it. (WI-0002/Q-002, ADR-0003.)
- [ ] AC3 — recording an expense whose payer, or any of whose sharers, is not a person in the
      group fails with a message naming the unknown person, exits non-zero, and records nothing.
      Names are matched by the same rule as WI-0001 AC3: case-insensitively, after surrounding
      whitespace is stripped.
- [ ] AC4 — a command lists the expenses recorded so far, one expense per line, showing for each
      one the amount, the payer, the sharers, the date and the description where one was given.
      The amount is shown in the same two-decimal text form the recording command accepts
      (`12.50`, not `1250` and not `12.5`), and each sharer is shown in the spelling stored on
      the roster, not the spelling typed into this command. The exact column layout is `plan`'s
      to choose; what is fixed is that all five fields are present and identifiable.
      **The order the expenses come out in is not yet decided** — it is WI-0002/Q-005, open to
      the stakeholder, and this criterion is not decidable until that is answered.
- [ ] AC5 — an amount is accepted when it is a positive number with **at most two decimal
      places**: `12`, `12.5` and `12.50` are all accepted and `12.5` and `12.50` mean the same
      amount. An amount with more than two decimal places, such as `12.345`, is **rejected** with
      a message saying so — it is never rounded — as are zero, a negative amount and anything
      that is not a number. Every rejection exits non-zero and records nothing.
      (WI-0002/Q-003.) **What counts as a number here**, so that the criterion is decidable:
      digits, optionally followed by a single `.` and one or two more digits. A leading `+` or
      `-`, a currency symbol (`£12`), a thousands separator (`1,200`), an exponent (`1e3`),
      whitespace inside the number, and an empty value are all "not a number" and are rejected
      with the same non-zero exit. Assumed by `refine`, not stated by the stakeholder.
- [ ] AC6 — an expense may carry a **description**, and it is optional: recording one without a
      description succeeds and the listing shows the expense with the description column empty
      rather than failing or inventing text. (WI-0002/Q-001.) A description may contain any
      printable character — commas, punctuation, non-ASCII text — and is rejected, non-zero and
      recording nothing, if it contains a **control character**, for the same reason `ADR-0006`
      decision 5 gives for names: AC4 prints one expense per line, and a newline or an escape
      sequence in a description makes the listing unreadable or lets it overwrite what the
      terminal has already drawn. Assumed by `refine` from that ADR's reasoning, not stated by
      the stakeholder.
- [ ] AC7 — an expense may carry a **date**, given by the person recording it, so that an expense
      from several days ago can be entered with the day it happened. The format is `YYYY-MM-DD`.
      When no date is given, today's local date is recorded. A date that is not a valid
      `YYYY-MM-DD` calendar date — `2026-13-01`, `21/08/2026`, `yesterday` — is rejected with a
      message showing the expected format, exits non-zero, and records nothing.
      (WI-0002/Q-001.)
- [ ] AC8 — when sharers are named explicitly and the payer is not among them, the expense is
      still recorded and the command still exits zero, but a note is printed on stderr saying
      that the payer is not sharing this expense and is owed the whole amount.
      (WI-0002/Q-002, ADR-0003 decision 4.)
- [ ] AC9 — listing expenses when none have been recorded succeeds, exits zero, and prints a
      message saying there are none, rather than failing or printing nothing. This is the same
      shape as WI-0001 AC4's empty-roster message, and it is assumed by `refine` from that
      precedent rather than stated by the stakeholder; it is put to them inside WI-0002/Q-005 so
      they can reject it in the same breath as the ordering question.
- [ ] AC10 — no failure in this item's commands prints a Python traceback. Every failure prints
      a message on **stderr** naming what was wrong and exits non-zero, every success prints on
      **stdout** and exits zero, and **no failure changes the store's bytes** — checked by
      comparing the file before and after. When more than one thing is wrong in the same
      invocation, the message names at least the first fault in this order: the amount, then the
      date, then the payer, then the sharers. A store that exists but cannot be read or parsed is
      fatal to **both** of this item's commands, naming the path, per `ADR-0002` decision 6 —
      **including a store whose `expenses` list holds an element that is not an expense record**,
      which is the check `store.load()` does not yet make and which WI-0001 handed to this item
      (`tracker/items/WI-0001/artifacts/review.md` F6). This criterion is WI-0001 AC8 restated
      for this item's commands, because EP-001's fourth success measure is about the whole tool
      and each item can only test its own surface. The validation order is assumed by `refine`;
      the rest follows from decisions already recorded.
- [ ] AC11 — naming the same person twice in one sharer list — `alice` and `Alice`, or the same
      spelling repeated — records them **once**, not twice, so their share is not doubled. The
      expense is still recorded and the exit status is still zero, and a note on stderr says the
      duplicate was ignored. This follows from WI-0001 AC3, which already decides that `alice`
      and `Alice` are one person, so naming them twice names one person twice; the stderr note
      follows AC8's precedent of making a surprising-but-legitimate outcome visible. Resolved by
      `refine` from the record rather than escalated, per `spec/question.md` §4.

## Out of scope

- Editing or deleting an expense after it has been recorded.
- Computing balances or who owes whom; that is WI-0003.
- Attaching receipts, images, or files to an expense.

## Notes

All three of this item's open questions have been answered by the stakeholder, and the answers
are in the criteria above rather than here:

- Shares are always **equal** (EP-001/Q-001).
- An expense carries an optional description and an optional, user-settable date defaulting to
  today (WI-0002/Q-001).
- Amounts allow at most two decimal places and more is rejected, never rounded (WI-0002/Q-003).
- Sharers are exactly who you name; naming nobody means everyone (WI-0002/Q-002, ADR-0003).

**Three things are open with the stakeholder**, filed by the second `refine` pass on
2026-08-21 and blocking this item at `awaiting-answer`:

- **WI-0002/Q-004 — the ADR-0003 confirmation.** The stakeholder's answer to WI-0002/Q-002 was
  *"If I paid and it's shared by all of us, include me automatically"* — conditional on the
  everyone case, which AC2's default covers exactly. It does not say what should happen when
  sharers **are** named explicitly and the payer is left off. ADR-0003 decides that such a list
  means literally what it says, and adds AC8's stderr note as the guard. If the stakeholder
  actually meant "include me whatever list I give", ADR-0003 must be superseded **before any
  expenses are stored** — afterwards the data cannot distinguish "did not share" from "forgot to
  type my own name", and the change becomes irreversible. `## Notes` has asked for this
  confirmation since the first answers landed and nothing could act on it, because `refine` is
  the only skill on this item that may ask; it is now asked.
- **WI-0002/Q-005 — the order the expense listing comes out in.** AC4 cannot be decided without
  it, and the stakeholder's own *"I'm usually catching up days later"* is what makes entry order
  and date order routinely differ. AC9's empty-listing message is put to them in the same
  question as an assumption they can reject.
- **WI-0002/Q-006 — whether a date in the future is accepted, rejected, or noted.** AC7 is silent
  and a mistyped year is invisible in the totals, because nothing downstream reads the date.

Nothing has been guessed on their account. Where this pass decided something itself it is marked
in the criterion as assumed by `refine` and recorded in `artifacts/refinement-qa.md`.

The amount is money, and AC5 forbids silent rounding, so it must not be held as a binary float.
Store and compute in **integer minor units** (pence), converting once at the boundary; that is
also what makes WI-0003's "net to zero, to the last minor unit" criterion achievable.

Depends on WI-0001 for the roster and for the store module described in
`docs/architecture/adr/ADR-0002-one-store-file-per-user.md`. Python 3.9+, standard library only,
per `docs/architecture/adr/ADR-0001-python-baseline-and-no-dependencies.md`.

## Deliberately unconstrained

Recorded per the Definition of Ready **R10**, so that these are open questions someone can find
rather than gaps nobody knows exist. Each names who left it open. This follows the same practice
WI-0001 used.

- **The spelling of the commands and their flags** — how you write "everyone" rather than listing
  names, whether sharers are `--with alice --with bob`, what the recording and listing commands
  are called. `ADR-0006` decisions 2–3 already fix all of this for the whole tool; AC1–AC4
  constrain only what must be possible and what must be printed, so they stay true whatever the
  ADR's spellings turn out to be in practice. Left to `plan` and `ADR-0006` by `refine`.
- **How large an amount may be, how long a description may be, and how many expenses the store
  may hold.** Nothing sets a limit and no criterion depends on one. Left open by `refine`, on the
  same reasoning WI-0001 used for the roster's size: the stakeholder described a friend group,
  and a limit nobody asked for is a failure mode nobody wanted.
- **Currency.** Amounts are bare numbers with no symbol and no unit anywhere — in the command, in
  the store, or in the listing. The stakeholder has never mentioned currency and the group
  presumably uses one. Assumed by `refine`; if a second currency ever appears, every stored
  amount becomes ambiguous, so it is named here rather than left silent.
- **Whether two expenses may be identical** — same amount, payer, sharers, date and description.
  Nothing forbids it and nothing deduplicates it, which is correct for a group that buys the same
  round twice. Left explicitly unconstrained by `refine` so that nobody later mistakes it for an
  oversight and adds a uniqueness rule.
- **What happens to an expense naming a person who is later removed from the group.** Removing a
  person is in WI-0001's `## Out of scope` and is not possible today, so the combination is
  unreachable. Named by `refine` because it becomes real the moment removal is built, and
  `ADR-0003` decision 3 (the sharer set is fixed at recording time) is the decision that will
  govern it.

**Combinations that are specified rather than left open**, listed so R10's check is visible:

- *No sharers given, in an empty group* — unreachable: AC3 rejects the command first, because an
  empty group cannot contain the payer.
- *An explicit sharer list containing only the payer* — the payer is among the sharers, so AC8's
  note does not fire and the payer shares the whole expense with themselves. Follows from AC2 and
  AC8 as written.
- *The everyone shorthand and an explicit name list given together* — not yet stated. `plan` must
  either reject the combination or define it when it settles the flag spellings; naming it here is
  what R10 asks for.
- *Several inputs invalid at once* — AC10 fixes the reporting order.
- *A damaged store, on either command* — AC10, via `ADR-0002` decision 6.
