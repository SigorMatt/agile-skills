---
id: WI-0002
type: work-item
title: Record income into an envelope and spending against it, and show what is left
status: awaiting-answer
priority: high
epic: EP-001
created: "2026-09-10T13:14:49Z"
updated: "2026-09-10T15:58:36Z"
depends-on:
  - WI-0001
branch: wi/WI-0002
---

## Story

As someone budgeting into envelopes, I want to record money going into an envelope and money
spent out of one, so that I can see what is left in each envelope without working it out myself.

## Acceptance criteria

Every criterion below is observed by running `envel` and reading its stdout, its stderr and its
exit status, which is the form WI-0001's criteria take. `envel` is the stakeholder's own choice of
command name (`WI-0001/Q-001`); the sub-command words `income` and `spend` are this refinement's,
taken from the stakeholder's own vocabulary in `IDEA.md` and recorded as an assumption in
`artifacts/refinement-qa.md`.

- [x] AC1 — `envel income groceries 400` records 400 as income into the envelope `groceries` and
      exits 0. There is no pool of unallocated money and no split for the tool to work out: the
      envelope is named at the moment the income is recorded (`EP-001/Q-002`). It writes nothing
      to stderr and one line to stdout, and what that line must carry is AC13. That the 400 was
      recorded is read from `envel list` afterwards: on a store where `groceries` held 0, it then
      writes a line containing both `groceries` and `400.00`
- [x] AC2 — `envel spend groceries 60` records 60 as spending against the envelope `groceries`,
      exits 0, and writes nothing to stderr. That the 60 was recorded is read from `envel list`
      afterwards: on a store where `groceries` held 400, it then writes a line containing both
      `groceries` and `340.00`
- [x] AC3 — `envel income groceries 400`, then `envel spend groceries 60`, each a separate
      invocation of the process with no other step in between: a third invocation, `envel list`,
      exits 0 and writes a line containing both `groceries` and `340.00`. A balance is what went
      in minus what went out; `envel list` is where it is seen (`WI-0002/Q-001`) and `340.00` is
      how it is written (`ADR-0006`)
- [x] AC4 — a recording command naming an envelope that does not exist is refused and creates
      nothing. On a store where only `groceries` exists, `envel income rent 100` and
      `envel spend rent 100` each exit non-zero, write at least one line to stderr containing
      `rent`, and a following `envel list` writes a line containing `groceries` and no line
      containing `rent`.
      Whether a name is an existing envelope is decided the way WI-0001 decides it, ignoring case
      and surrounding whitespace: with `groceries` holding at least 10,
      `envel spend Groceries 10` exits 0, writes nothing to stderr, and reduces the balance shown
      for `groceries` rather than reporting an unknown envelope (`WI-0001/Q-002`; `ADR-0004`)
- [x] AC5 — balances recorded in one invocation are shown unchanged by a later, separate
      invocation, with no manual step in between: after AC3's two invocations, a fourth
      invocation of `envel list` again writes a line containing both `groceries` and `340.00`
- [x] AC6 — recording a spend larger than the balance of its envelope is refused: with `groceries`
      at 340, `envel spend groceries 500` exits non-zero, writes at least one line to stderr
      containing `groceries`, records nothing, and `envel list` afterwards still writes a line
      containing both `groceries` and `340.00`. No envelope balance can become negative by this
      route (`EP-001/Q-003`)
- [x] AC7 — both recording commands accept an optional date for the transaction and default to
      today when it is omitted, so that a transaction typed a few days late carries the day it
      happened (`EP-001/Q-004`). The date is given as `--date YYYY-MM-DD`, and every invocation
      below is on a store where `groceries` holds at least 30:
      `envel spend groceries 10 --date 2026-08-31` exits 0 and writes nothing to stderr, and
      `envel spend groceries 10 --date 2026-13-01` and `envel spend groceries 10 --date 31/08/2026`
      each exit non-zero, write at least one line to stderr, and record nothing
- [x] AC8 — a spend of exactly the balance is recorded rather than refused: with `groceries` at
      340, `envel spend groceries 340` exits 0 and writes nothing to stderr, and `envel list`
      afterwards writes a line containing both `groceries` and `0.00`. Zero is not negative, and
      what `EP-001/Q-003` refuses is a balance going below zero
- [x] AC9 — an amount of zero, and a negative amount, are refused on both commands:
      `envel income groceries 0`, `envel spend groceries 0`, `envel income groceries -5` and
      `envel spend groceries -5` each exit non-zero, write at least one line to stderr, and record
      nothing — the line `envel list` writes for `groceries` afterwards is unchanged
- [x] AC10 — an argument that is not an amount at all is refused: `envel spend groceries abc` and
      `envel spend groceries ""` each exit non-zero, write at least one line to stderr, and record
      nothing. What else counts as an amount — a leading currency symbol, and more than two
      decimal places — is settled by AC17 and AC18
- [x] AC11 — a recording command missing an argument is refused: `envel income groceries` with no
      amount, and `envel spend` with neither envelope nor amount, each exit non-zero, write at
      least one line to stderr, and record nothing
- [x] AC12 — every one of WI-0001's acceptance criteria still holds after this item's change —
      `WI-0001` AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10 and AC11, each named so that
      each gets its own verdict. The assessment is a **read** of those eleven criteria's text
      against this item's behaviour, with WI-0001's named tests as evidence for the answer rather
      than as its definition. Six of the eleven are **waived by name**, because `WI-0002/Q-001`
      replaced the requirement each of them states: `WI-0001` AC2, AC3, AC5, AC7, AC8 and AC11 each
      say that a line of `envel list` contains an envelope's name and nothing else, and AC15 below
      says it now carries the balance too. Each of the six is marked `superseded` on `WI-0001`
      itself, and its verdict here is `waived — superseded by WI-0002/Q-001`, stated per criterion.
      A waiver does not drop what the criterion was protecting: the substance of all six is
      re-checked against the new line shape by AC15 and AC19.
      The remaining five — `WI-0001` AC1, AC4, AC6, AC9 and AC10 — are **not** waived and must each
      still hold as written; AC4, whose subject is the order of the lines and their byte-stability
      across two runs, is unaffected by a second column and is the one most likely to break in
      implementation (`spec/dor-dod.md`)
- [x] AC13 — a successful `envel income` or `envel spend` says what it recorded, on one line
      (`WI-0002/Q-003`). On a store where `groceries` holds 400, the invocation
      `envel spend groceries 12.50 --date 2026-08-31` exits 0, writes nothing to stderr, and
      writes exactly one line to stdout; that line contains all four of the substrings
      `groceries`, `12.50`, `2026-08-31` and `387.50` — the envelope, the amount, the date the
      transaction was filed under, and what is left in the envelope afterwards. The sentence those
      four are set in is `plan`'s to word, and the two-decimal form of the amount and the balance
      is `ADR-0006`'s
- [x] AC14 — with no `--date`, the date on AC13's line is today's: `envel spend groceries 10`, run
      on a store where `groceries` holds at least 10, writes one line to stdout containing today's
      date in the `YYYY-MM-DD` form of AC7 — the string `date +%F` prints when run alongside it.
      This is what makes AC7's "defaults to today" half observable in this item at all
      (`EP-001/Q-004`; `WI-0002/Q-003`)
- [x] AC15 — `envel list` shows what is left in every envelope: each line it writes carries the
      envelope's name and that envelope's balance (`WI-0002/Q-001`; `ADR-0006`). On a store where
      `groceries` holds 340 and `rent` holds 0, `envel list` exits 0, writes nothing to stderr, and
      writes exactly two lines to stdout — the first containing both `groceries` and `340.00`, the
      second containing both `rent` and `0.00`, in that order, which is `WI-0001` AC4's ordering
      rule unchanged. Running `envel list` twice in a row still produces byte-identical stdout
- [x] AC16 — an envelope that has had nothing put into it shows a zero balance rather than a blank
      or an error: `envel new petrol` on a store where `petrol` does not exist, then `envel list`,
      writes a line containing both `petrol` and `0.00` and exits 0
- [x] AC17 — a single leading `£` is accepted and ignored (`WI-0002/Q-002`; `ADR-0006`): on a store
      where `groceries` holds 0, `envel income groceries £12.50` exits 0, writes nothing to stderr,
      and `envel list` afterwards writes a line containing both `groceries` and `12.50`. The plain
      forms are accepted too — `envel income groceries 12`, `envel income groceries 12.5` and
      `envel income groceries 12.50` each exit 0 and write nothing to stderr
- [x] AC18 — an amount with more than two decimal places is refused rather than rounded
      (`WI-0002/Q-002`; `ADR-0006`): with `groceries` at 340, `envel spend groceries 12.345` and
      `envel income groceries 12.345` each exit non-zero, write at least one line to stderr, and
      record nothing — `envel list` afterwards still writes a line containing both `groceries` and
      `340.00`
- [x] AC19 — the substance of the six `WI-0001` criteria AC12 waives survives the new line shape,
      each checked in its new form on a store that starts empty. `envel new Groceries`, then
      `envel list`: exactly one line, containing `Groceries` with that capitalisation and `0.00`
      — `WI-0001` AC7's substance, and the reason it matters is `WI-0001/Q-002`. `envel new
      "eating out"`, then `envel list`: a line containing `eating out` — AC8's. `envel new a`,
      `envel new b`, then `envel list`: exactly two lines, the first containing `a` and the second
      containing `b` — AC3's. `envel new groceries`, then `envel new "  groceries  "` which exits
      non-zero, then `envel list`: exactly one line, containing `groceries` and no leading space —
      AC5's and AC11's. `WI-0001` AC2's substance is AC15's and is not repeated here

## Out of scope

- The monthly summary; that is WI-0003.
- Moving money between envelopes; that is WI-0004. It is what the stakeholder does when AC6
  refuses a spend, so the two are close, but it is a separate command and a separate item.
- Correcting or removing a transaction after it has been recorded; that is WI-0005.
- **Listing the individual transactions recorded against an envelope.** A reader could reasonably
  assume that a tool which records transactions can show them back, and this item does not: it
  shows a balance. Reading the movements is what the monthly summary is for (WI-0003), and
  correcting one is WI-0005.
- **Any notion of more than one currency.** Amounts are numbers in the one currency the person
  budgets in — pounds and pence, and the stakeholder has said it is not changing
  (`WI-0002/Q-002`). Nothing converts, and nothing is labelled with a currency in the store.
- **A flag that turns the balances off.** `WI-0002/Q-001` offered one and the stakeholder declined
  it: "I don't need a flag to hide the balances." `envel list` shows them, always, and there is no
  way back to the names-only listing except by asking for one.
- **Rounding an over-precise amount.** AC18 refuses `12.345`; nothing here rounds it to `12.35` or
  to `12.34` (`WI-0002/Q-002`).

## Notes

**Answered by the stakeholder before this refinement, and written into the criteria above:**

- Income goes straight into a named envelope, with no pool and no split (`EP-001/Q-002`, AC1):
  "Money comes in a few times a month and I decide the split there and then, envelope by envelope.
  I don't want the tool holding a pool or working out splits for me."
- A spend larger than its envelope is refused rather than recorded (`EP-001/Q-003`, AC6):
  "I don't want an envelope going negative; the whole point is that the number is the truth."
- A transaction carries an optional date and defaults to today (`EP-001/Q-004`, AC7): "Normally
  I'll be typing it the same day and want to type nothing extra, but I do catch up after a few days
  and those need to land on the day they happened."
- Two names are the same envelope when they differ only in case or in surrounding whitespace
  (`WI-0001/Q-002`, AC4), and the tool is called `envel` (`WI-0001/Q-001`).

**Answered by the stakeholder — refinement round 1's three questions, all now closed.** Each was
propagated into the criteria above by `answer-questions`; `artifacts/refinement-qa.md` still says
`agenda` and is `refine`'s to record verbatim and close in round 2.

- `WI-0002/Q-001` — **option A**: `envel list` shows the balances, and no second command and no
  flag. "The number is the whole reason I open the tool; I'm not going to type a second command to
  see it. Change the criteria on the earlier item, that's fine by me — I'm asking for it. I don't
  need a flag to hide the balances." AC15 and AC16 are new and are where the behaviour is stated;
  AC3, AC5, AC6, AC8, AC9 and AC4 now name `envel list` as the place a balance is read; AC12 names
  the six criteria of `WI-0001` this replaces, and `WI-0001`'s own criteria are marked
  `superseded` where it does.
- `WI-0002/Q-002` — **option C**: a leading `£` is accepted and ignored, and more than two decimal
  places is refused rather than rounded. "Same reason as the overspend, I don't want the tool
  storing a number I didn't type. It's one currency, pounds and pence, and that's not changing."
  AC17 and AC18 are new; AC10 now points at them; `ADR-0006` records the decision and the one
  thing their answer left open, which is how many digits a printed amount carries.
- `WI-0002/Q-003` — **option C**: a successful recording prints one line saying what was recorded
  — the envelope, the amount, the date it was filed under, and what is left. "One line, not three.
  Catching a fat-fingered amount or a wrong date while I'm still looking at the screen is worth
  the extra output." AC13 and AC14 are new; AC1 now points at AC13 rather than deferring.

**AC17's `£` meets BUG-0001, and `plan` needs to see it.** `£` is not an ASCII character, and
`BUG-0001` is open against exactly that: under a non-UTF-8 locale the tool raises
`UnicodeEncodeError` out of the argv path and prints a traceback (`ADR-0005` measures the
interpreter's encodings under that locale). AC17 is checkable as written, because it says nothing
about the locale and the ordinary one is UTF-8 — so this item does **not** gain a `depends-on`
and is not sequenced behind the bug. What `plan` must not do is parse the amount by reaching past
whatever boundary `BUG-0001` establishes: the two items touch the same argument-decoding path and
the fix for one has to hold for the other. Recorded here rather than as a criterion because there
is no observation to state that AC17 does not already state.

**Open design questions, routed to `plan` and not to the stakeholder.** The answer to each would
be the same whoever the stakeholder was.

- **How a transaction is stored, and whether the store keeps movements or only a running
  balance.** WI-0003 summarises a month from the movements and WI-0005 corrects one of them, so
  both need the movements to exist; this item only needs the balance. `plan` decides the shape,
  and it also decides how a `version: 1` store written by WI-0001 becomes whatever this item needs
  (`ADR-0003` fixes the file, not its contents).
- **The exact wording of every message this item adds**, on stdout and on stderr. The criteria fix
  the stream, the exit status and, where it matters, the substrings that must appear; they
  deliberately do not fix the sentence. This is the same disposition WI-0001 made under plan
  assumption P1. Two things are no longer `plan`'s and were not before `WI-0002/Q-003` was
  answered: **which four facts** a successful recording puts on the screen (AC13) and **how many
  decimal places** a printed amount or balance carries (`ADR-0006`). The sentence they sit in is
  still `plan`'s.
- **Which refusal wins when more than one applies** — `envel spend nosuch -5`, say, is both an
  unknown envelope and a bad amount. Any one refusal satisfies AC4, AC9 and AC10 as written; the
  order is `plan`'s and no criterion constrains it.

**Deliberately unconstrained, and by `refine`:**

- **A date in the future.** `EP-001/Q-004` is about catching up on days already past, and says
  nothing about `--date 2027-01-01`. AC7 accepts any well-formed date and this item does not refuse
  a future one. If the stakeholder wants a future date refused, that is a change to AC7 and lands
  on this item as a send-back to `refine`.
- **AC7's "defaults to today" half is now observable in this item, and the gap that was recorded
  here is closed.** Refinement noted that nothing in this item showed a transaction's date, so
  whether the default really was *today* could not be checked before WI-0003. `WI-0002/Q-003`'s
  answer prints the date back on every successful recording, which makes it checkable here; AC14
  is the criterion that checks it. Nothing was widened to achieve this — it falls out of an answer
  the stakeholder gave for a different reason.

**R10 — combinations.** This item introduces two commands, `income` and `spend`, one option,
`--date`, which both take, and one changed command, `envel list`, which gains a balance column and
takes no option at all (see `## Out of scope`). The pairs that exist are covered or named: each
command with an amount
and no date (AC1, AC2), each with a well-formed date (AC7), each with a malformed date (AC7), each
against an unknown envelope (AC4), each with a zero or negative amount (AC9), each with a
non-numeric amount (AC10, stated on `spend`; the parsing is shared and `plan` owns the shape), and
each with an argument missing (AC11). `spend` has one dimension `income` does not — the balance it
is measured against — and its three cases are covered: below it (AC2), exactly it (AC8), above it
(AC6). The combination of `--date` with a refusal is named above as `plan`'s, since a refused
command records nothing whatever date it was given.

Round 1's three answers added a third dimension to the amount — its **shape as typed** — and its
pairs are covered: a leading `£` on `income` (AC17), more than two decimal places on both commands
(AC18), zero and negative on both (AC9), non-numeric and empty on `spend` (AC10), and absent
altogether (AC11). They also added the recording line itself, whose pairs with `--date` are both
covered: with a date given (AC13) and with it omitted (AC14). And they changed `envel list`, whose
cases are an envelope with money in it, one with nothing in it and the ordering of the two (AC15),
a freshly created envelope (AC16), and a store with no envelopes at all — which is `WI-0001` AC6,
not waived, and named in AC12 as one of the five that must still hold.

**R11 — nothing here counts a project artefact.** No criterion states a number of tests, files or
criteria. AC12 names WI-0001's eleven criteria individually rather than counting them, which is
what R11 asks for and what makes each one get its own verdict. Several criteria do count something
— AC1, AC13 "one line to stdout", AC15 and AC19 "exactly two lines", AC13 "all four of the
substrings" — and every one of those counts a line of the **tool's own output** on a store this
item's own text fixes. That is the case `spec/dor-dod.md` R11 names as not being what it is about
("prints one row per file"): the number cannot drift as the project grows, because it is a
property of a run rather than of the repository.

**R9 — one item or two?** Income in, spending out and a balance are one coherent change: they are
one store shape, one lookup rule and one arithmetic, and the balance is not observable without the
two recording commands. Splitting them would produce an item whose criteria could not be checked
without the other item's code. Judged one item by `refine`; the stakeholder was not asked, because
the answer would be the same whoever they were.
