---
id: WI-0004
type: work-item
title: Move money between envelopes
status: done
priority: medium
epic: EP-001
depends-on:
  - WI-0001
created: "2026-09-11T02:12:40Z"
updated: "2026-09-11T06:15:53Z"
arose-from: EP-001/Q-005
branch: wi/WI-0004
outcome: delivered
merge-commit: 162ecdccebb7532220f6a47034b300975d0d8912
---

## Story

As a person budgeting my own money at a terminal, I want to move an amount from one envelope to
another, so that when an envelope runs short I can take the money from somewhere I have decided
it can come from, and then record the spend.

## Acceptance criteria

- [x] AC1 — There is an `envel` command that moves a given amount from one named envelope to
      another named envelope, and it can carry a date: `envel move <from> <to> <amount>`, with an
      optional `--on <date>` after it — `envel move groceries fun 20 --on 2026-08-28`. The date is
      optional in exactly the way a spend's is, and the move is held against the date given rather
      than the day it was typed [src: WI-0004/Q-001]. Observed in a store of its own —
      `ENVEL_FILE` set to a path that does not exist [src: ADR-0003], the route the delivered item
      already uses to make a stored date checkable [src: WI-0002 AC8 "Observed in a store of its
      own"] — by creating two envelopes, adding income to one, and running
      `envel move groceries fun 20 --on 2026-08-28`: the move the store then holds carries
      `2026-08-28`. The store file is where this item's dates are read, because nothing this item
      delivers prints a move's date back; `WI-0003`'s summary is where it becomes visible without
      opening the file. The subcommand name `move` and the argument order are `[assumed]`, under no
      delegation (`artifacts/refinement-qa.md`); what the stakeholder settled is that a date may be
      given at all, and that `--on` is how it is given.
- [x] AC2 — After a move, the listing shows the source envelope reduced by exactly the amount
      moved and the destination envelope increased by exactly the amount moved, and no other
      envelope's amount changed.
- [x] AC3 — A move of more than the amount currently in the source envelope is refused, on the
      same rule the stakeholder set for an overspend in `EP-001/Q-002`: nothing is moved, and
      the message names the source envelope and what is left in it.
- [x] AC4 — A move naming an envelope that does not exist — as either side — is refused with a
      message naming that envelope, and nothing is moved.
- [x] AC5 — A move recorded in one invocation is still reflected in the listing in a later,
      separate invocation of the tool.

- [x] AC6 — A move given with no `--on` is dated today, the day it was typed. This is the same
      default a spend has [src: WI-0002 AC9 "A spend can be recorded with a date other than
      today, written as"], and it is what makes `--on` optional rather than required. Observed in
      the store of AC1, by running one move with no `--on` and one with `--on 2020-01-01`: the
      first carries today's date and the second carries `2020-01-01`.
- [x] AC7 — `--on` on a move accepts the full `YYYY-MM-DD` form and nothing else. `2026-08-28` is
      recorded; `28/8`, `08-28`, `yesterday` and anything else that is not that form are each
      refused with a message, with nothing moved and both envelopes' amounts unchanged. The form
      is the one already delivered for a spend and is not a new decision [src: WI-0002 AC11
      "`--on` accepts the full `YYYY-MM-DD` form and nothing else"].
- [x] AC8 — A date given with `--on` that is later than today is refused with a message saying the
      date is in the future; nothing is moved and both envelopes' amounts are unchanged. Today's
      own date is accepted, being the default of AC6. This too follows the delivered spend rule
      rather than deciding anything new [src: WI-0002 AC12 "A date given with `--on` that is later
      than today is refused"].

- [x] AC9 — A successful move prints to stdout a line that contains the source envelope's name,
      the destination envelope's name, the amount moved, and the amount now in each of the two
      envelopes, and exits 0. The two names appear in an order that says which envelope the money
      left and which it arrived in, so a pair typed the wrong way round is visible in the same
      breath as the mistake and is undone by running the same command with the names swapped. That
      a move reports the new amounts rather than leaving them to be read from the listing follows
      the delivered spend [src: WI-0002 AC7 "Recording a spend prints the envelope's new remaining
      amount"]. The wording of the line is deliberately unconstrained; what this criterion decides
      is that those four things are in it. `[assumed]`, under no delegation
      (`artifacts/refinement-qa.md`).
- [x] AC10 — A move of `0`, or of a negative amount, is refused with a message; nothing is moved
      and both envelopes' amounts are unchanged. This is the rule the stakeholder set for income
      [src: WI-0001/Q-003] and the one the delivered item already applies to a spend
      [src: WI-0002 AC6 "Recording a spend of `0`, or of a negative amount, is refused"], taken a
      third time here rather than put to them again. `[assumed]`, under no delegation
      (`artifacts/refinement-qa.md`).
- [x] AC11 — A move whose source and destination name the same envelope is refused with a message
      naming that envelope, and nothing is moved. `groceries` to `Groceries` is refused by this
      criterion too, because the tool matches a name without regard to capitalisation
      [src: WI-0001 AC11 "Envelope names are matched without regard to capitalisation"] and they
      are therefore one envelope. `[assumed]`, under no delegation
      (`artifacts/refinement-qa.md`).
- [x] AC12 — Every refusal this item specifies writes its message to stderr and exits non-zero,
      and a successful move writes its output to stdout and exits 0. It is the project's recorded
      convention [src: docs/architecture/overview.md] and the rule both delivered items already
      follow [src: WI-0001 AC16 "Every refusal this item specifies writes its message to stderr
      and exits non-zero"] [src: WI-0002 AC13 "Every refusal this item specifies writes its
      message to stderr and exits non-zero"]. This criterion is settled by reading the text of the
      criteria it names against what the tool does, with the test suite as the evidence for that
      reading rather than as its definition: refusals at AC3, AC4, AC7, AC8, AC10, AC11 and AC13;
      successes at AC1, AC2, AC6 and AC9. Where no executable case exercises a named criterion's
      stream and exit code together, say so in as many words and then either add a covering case
      or waive that criterion by name — do not read the criterion as satisfied by the absence of a
      test.
- [x] AC13 — `envel move` with no arguments, `envel move groceries` with only a source,
      `envel move groceries fun` with no amount, and `envel move groceries fun 20 extra` with a
      word beyond the amount each print a usage message for the subcommand to stderr and exit
      non-zero, with nothing moved — the same treatment the delivered subcommands already get
      [src: WI-0001 AC15 "A subcommand given the wrong number of arguments prints to stderr a
      usage message"]. The fourth of those is what makes the decision that a move carries no
      description observable: the word that would be a description on `envel spend` is an error
      here [src: WI-0002 AC10 "A spend can be recorded with a short description of what it was
      for"].

## Out of scope

- **Correcting or deleting a move once it has been recorded — and nowhere else covers it
  either.** The draft said this was *"the subject of `WI-0005`, which the stakeholder scoped to
  spends"*, which contradicted itself: `WI-0005` does not cover moves, so as the epic stands
  there is no command anywhere that repairs a move. Round 1 leaves that gap deliberately rather
  than widening either item, because a move is self-reversing — a wrong `envel move a b 20` is
  undone by `envel move b a 20` — and `WI-0003` AC2's fourth figure is a **net** number
  [src: WI-0003 AC2 "The moved figure is one net number, positive when more arrived than left"],
  so a mistake and its reversal cancel in the only place a move is ever displayed. What survives
  the reversal is the month a move is counted in, and that is exactly what `WI-0004/Q-001` was
  about. `Q-001` is now answered — a move carries `--on` (AC1 and AC6–AC8) — so a reversal can be
  dated into the month the mistake landed in, and the one consequence a reversal could not undo is
  no longer part of this gap. It is still a gap: nothing edits or deletes a recorded move, and the
  stakeholder named that cost themselves — *"I can fix a spend afterwards and I can't fix a move,
  so I need to be able to get it right when I type it"* [src: WI-0004/Q-001].
- A description on a move. `[assumed]`, under **no delegation** — see `## Notes`.
- Moving money into or out of anything that is not an envelope.
- Splitting one move across more than two envelopes in a single command.

## Notes

- This item exists because of the stakeholder's answer to `EP-001/Q-005`: they chose option C,
  both moving money and correcting entries, and said *"Moving money between envelopes is normal
  practice and I will need it the moment an envelope runs short, which is the same week I start
  using this."* It was filed by `answer-questions` under `spec/ids-and-statuses.md` §5 rather
  than folded into `WI-0001` or `WI-0002`, so that the scope change is visible on the board.
- ~~These criteria are a first draft and this item is **not** Ready.~~ **Superseded by round 2.**
  Round 1 wrote that sentence while `Q-001` was with the stakeholder. `refine` round 2 has since
  written the five criteria round 1 deferred and walked the Definition of Ready criterion by
  criterion; the verdicts are in this item's journal entry for round 2 and the reasoning is in
  `artifacts/refinement-qa.md` `## Round 2`. The three open points the draft listed remain
  disposed of — two were already answered or decidable, one was `Q-001`, which is answered.

- **`depends-on: WI-0001` is now recorded**, and recording it costs nothing: `WI-0001` is `done`.
  The draft deliberately left it out because the `runnable` rule would have frozen this item's own
  refinement until `WI-0001` was delivered; that reason has expired. The dependency is real —
  there is nothing to move money between until envelopes exist — and it is `WI-0001` alone.
  `WI-0002` is **not** a dependency: moving money needs envelopes, not spending, and no criterion
  here is written against anything `WI-0002` delivers.

- **`refine` round 1 filed one blocking question and rewrote no criterion.**
  - `WI-0004/Q-001` — is a move datable the way a spend is, or always dated when it is typed, the
    way income is? It is the one thing on this item that cannot be derived, because the
    stakeholder has answered this shape of question twice and given **opposite** answers, each
    with a reason about their own habits: `WI-0002/Q-001` (a spend can be back-dated, *"I will
    not always sit down with the receipts on the day"*) and `WI-0003/Q-003` (income cannot,
    *"I put income in when it arrives"*). A move is a third event and neither answer reaches it.
    It decides which month a move counts in, which is visible in `WI-0003`'s fourth column.

- **The draft's first open point is already answered, and was not re-asked.** It asked whether a
  move shows up in the monthly summary as money in and money out. The stakeholder settled exactly
  that at `WI-0003/Q-001`, after this item was filed: option C, a move is kept out of *spent* and
  shown as its own net figure — *"'Spent' has to mean money that left the house, so moves don't
  belong in it — but I won't use a report whose rows don't add up."* `WI-0003` AC2, AC3 and AC6
  carry it. Two consequences land on this item and are recorded for `plan` rather than asked:
  a move must be recorded so that `WI-0003` can tell it from a spend and from income, and it must
  be recorded in a way that lets one net figure per envelope per month be computed from it.

- **The draft's third open point is decided here rather than asked.** Moving zero, or a negative
  amount, is refused with a message and nothing is moved. `[assumed]`, under **no delegation** —
  the stakeholder set this rule for income at `WI-0001/Q-003` and were never asked about anything
  else, so `WI-0002` AC6 took it for a spend on the same footing and has since shipped and been
  verified [src: WI-0002 AC6 "Recording a spend of `0`, or of a negative amount, is refused"].
  Assuming it a third time is consistent rather than careless, and asking about the third instance
  of a rule they set once would tell them their answer was not heard. A disagreement lands on one
  criterion and costs one comparison.

- **Decided by round 1 rather than asked, each under no delegation**, on the same footing as every
  other word below `envel` in this tool — `new`, `add`, `list`, `spend` and `summary` are all
  assumed names and none was ever put to the stakeholder:
  - **The subcommand is `move`, as `envel move <from> <to> <amount>`** — source first, destination
    second, amount last, which is the order every delivered subcommand already uses (the
    envelope's name before the amount) and the order the story reads in. A disagreement lands on
    AC1 and costs swapping two arguments. The risk of getting it backwards is real and is
    mitigated by AC6 below rather than by a question: the success line says which envelope the
    money left and which it arrived in, so a reversed pair is visible in the same breath.
  - **A move to and from the same envelope is refused**, with a message naming the envelope. It
    changes nothing and is far more likely to be a mistyped name than an intention. A disagreement
    lands on one criterion.
  - **A description on a move is not built.** Nothing in this project would ever show one back —
    `WI-0006` is scoped to the spends recorded against an envelope, and `WI-0003` rules the
    individual entries out of the summary [src: EP-001/Q-003] — so it would be a note that can be
    written and never read. This is **not** read as contradicting `WI-0002/Q-002`, where the
    stakeholder asked for an optional description on a **spend**: that answer is about spends, and
    the reason they gave for it — *"I'll put one on the ones I might query later"* — presupposes
    something that queries, which exists for spends and does not for moves. It is in
    `## Out of scope` as well as here, so it is visible on the board rather than buried. A
    disagreement lands on AC1 and costs one optional word on the line.
  - **Success goes to stdout with exit 0 and every refusal to stderr with a non-zero exit**, and
    a wrong number of arguments prints the subcommand's usage. These are **not** assumptions but
    the project's delivered conventions [src: docs/architecture/overview.md]
    [src: WI-0001 AC16 "Every refusal this item specifies writes its message to stderr and exits
    non-zero"] [src: WI-0002 AC14 "`envel spend` with no arguments"]. Round 2 writes them into the
    criteria by citation rather than restating them as new decisions.

  The **wording** of every message stays deliberately unconstrained, exactly as `WI-0001` and
  `WI-0002` left it. A criterion will say what a message must contain — the envelope's name, what
  is left in it — and never how it reads.

- **Round 1's one question is answered, and this is what it settled.** `answer-questions` consumed
  the reply on 2026-09-11; the stakeholder's words are quoted verbatim in
  `artifacts/refinement-qa.md` `## Answers — round 1`.
  - `WI-0004/Q-001` — option **A**: a move is datable exactly the way a spend is. *"I move the
    money because of a shop I'm typing in late, so the move is late too. The thing that settles it
    for me is that I can fix a spend afterwards and I can't fix a move, so I need to be able to
    get it right when I type it."* AC1 now carries `--on`, and AC6, AC7 and AC8 are new: today by
    default, `YYYY-MM-DD` and nothing else, and a future date refused. All three are the delivered
    `envel spend` rules cited rather than re-decided.
  - **Neither `WI-0002/Q-001` nor `WI-0003/Q-003` was overturned.** Round 1 filed the question
    saying that whichever way the reply went, one prior answer would look like the precedent and
    the other would not, and that neither was being reversed. The reply chose the spend's rule and
    did not mention income; `envel add` is untouched and `WI-0003` AC8 still says income is dated
    when it is typed.
  - **The stakeholder's reason is worth keeping separate from the choice**, because it is a fact
    about this project rather than about their habits: a move cannot be corrected after the fact —
    `WI-0005` is scoped to spends — so the date has to be right at the moment it is typed. That is
    the argument `## Out of scope`'s self-reversing-move entry does not reach: a reversal cancels
    the amounts, but it cannot move a figure out of the month it was counted in without a second
    move dated into that month, which is precisely what `--on` now allows.
- **What `refine` round 2 still has to do is what round 1 said, minus AC1.** Round 1's bounded job
  was *"write AC1 from `Q-001`'s reply, append the five criteria listed above, and walk the
  Definition of Ready with R4, R6, R8 and R10 closed."* AC1 and the three date criteria are
  written; the five criteria round 1 listed — the success output, the streams and exit codes, zero
  and negative, a move to the same envelope, and the wrong number of words — are **not**, because
  every one of them is `refine`'s own `[assumed]` decision or a delivered convention rather than
  anything this question asked. Writing them is refinement's judgement taken in the open, not a
  propagation.
- **Numbering held.** AC1 was amended **in place** and AC6, AC7 and AC8 **appended**, so no
  criterion changed its number. `grep -rn 'WI-0004 AC' tracker docs` still finds nothing that
  cites this item's criteria by number.

- **Open design questions, routed to `plan` rather than to the stakeholder**, because the answer
  would be the same whoever they were:
  - whether a move is stored as one entry or as two, and how `WI-0003` tells a move from a spend
    and from income when it computes the fourth column;
  - in what order the refusals are checked when more than one applies at once — the same question
    `WI-0002` routed to `plan`, which settled it there by putting the envelope check first so that
    a message naming the envelope is always available;
  - what a move does with a stored entry naming an envelope that is no longer present — the same
    question `WI-0002` and `WI-0003` both routed to `plan`, and it should get the same answer.

- **No acceptance criterion was rewritten by round 1**, deliberately. AC1 is downstream of
  `Q-001` — whether the line carries `--on` is exactly what is being asked — and the criteria that
  round 1 can already write (the success output, the streams and exit codes, zero and negative, a
  move to the same envelope, the wrong number of words) would have to be numbered around it.
  Round 2 writes them once, from the reply. The renumbering obligation was discharged rather
  than assumed: `grep -rn 'WI-0004 AC' tracker docs` returns one line, and it is this sentence
  quoting its own command inside backticks — a mention rather than a citation
  (`spec/doc-header.md` §4a). Nothing anywhere cites this item's criteria by number, which is a
  reason to renumber carefully once rather than a licence to do it twice (F-094).

### Round 2 — what it decided, and what it left alone

- **Round 2 wrote the five criteria round 1 named and rewrote nothing else.** AC9 (the success
  line), AC10 (zero and negative), AC11 (a move to and from the same envelope), AC12 (streams and
  exit codes) and AC13 (the wrong number of words) are appended. Three of them are `refine`'s own
  `[assumed]` decisions taken in round 1 and carried into criteria here; two — AC12 and AC13 — are
  the project's delivered conventions written in by citation rather than decided again.
- **AC1 and AC6 were amended in place, and no criterion changed its number.** What was added to
  each is *how the stored date is observed*: a store of its own under `ENVEL_FILE` [src: ADR-0003],
  which is the route the delivered item already uses for exactly this
  [src: WI-0002 AC8 "Observed in a store of its own"]. Round 1's AC1 and the criteria
  `answer-questions` appended said what the date *means* without saying where a person with a
  terminal would look, and nothing this item delivers prints a move's date back — `WI-0003`'s
  summary is the first thing that does, and it is not delivered. That is an R4 repair rather than
  a change of meaning, and it is `refine`'s own judgement rather than anything the stakeholder
  said.
- **Renumbering was checked again, after the append.** `grep -rn 'WI-0004 AC' tracker docs` returns
  five lines, and every one of them is this item's own `item.md`, `journal.md` or
  `artifacts/refinement-qa.md` quoting that very command inside backticks — a mention rather than a
  citation (`spec/doc-header.md` §4a) [src: run: grep -rn 'WI-0004 AC' tracker docs → exit 0, 5
  lines, all of them the command quoted inside backticks]. Nothing anywhere cites this item's
  criteria by number, so the append moved nothing under anybody.

### Combinations, and where each one is settled (R10)

The behaviours this item introduces are one optional flag, `--on`, and seven ways to be refused.
Their combinations are disposed of as follows, and none of them is left for somebody to discover:

- **`--on` together with any refusal** — a bad date and a missing envelope on the same line, an
  overdraw and a future date, and so on. **Deliberately unconstrained here**, and routed to `plan`
  below: which refusal is reported when several apply is a design decision, and `WI-0002` routed
  the same question to `plan`, which settled it by putting the envelope check first so that a
  message naming the envelope is always available. Whichever order `plan` picks, each criterion's
  own requirement still holds — nothing is moved and neither envelope's amount changes — so the
  criteria are satisfiable under any of them. Left so by `refine` round 2.
- **`--on` together with the wrong number of positional words** — AC13's usage message. The flag
  does not change how many words `envel move` takes.
- **`--on` written with no date after it, or written twice.** **Deliberately unconstrained**:
  these are refusals produced by the tool's argument parsing rather than by anything this item
  decides, and `WI-0001` and `WI-0002` both left the same ground to the parser. What AC12 still
  requires of them is the stream and the exit code. Left so by `refine` round 2.
- **How an amount may be written** — `400`, `12.5`, `12.50` accepted; `£12.50`, `1,200` and `abc`
  refused. **Not restated here**, because it is tool-wide and already delivered
  [src: WI-0001 AC17 "An amount is written as a plain decimal number, with no currency symbol and
  no thousands separator"] [src: WI-0001 AC8 "An amount is written with at most two decimal
  places"]. `WI-0002` did not restate it either. Left so by `refine` round 2.
- **A back-dated move against the balance check of AC3.** AC3 reads *currently in the source
  envelope* — the balance now, not the balance on the date given. That is not a new decision: the
  delivered spend does the same [src: WI-0002 AC5 "Recording a spend larger than the amount
  currently in the envelope is refused"], and a back-dated spend is checked against the same
  present balance. Recorded here so that a reader does not have to infer it from AC3's one word.
