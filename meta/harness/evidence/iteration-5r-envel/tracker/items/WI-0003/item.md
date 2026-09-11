---
id: WI-0003
type: work-item
title: Show a summary of a month
status: done
priority: medium
epic: EP-001
depends-on:
  - WI-0002
  - WI-0004
created: "2026-09-11T01:57:16Z"
updated: "2026-09-11T07:08:33Z"
branch: wi/WI-0003
outcome: delivered
merge-commit: ec1de8305f899680c9baccc28c3c9eda08d7d3ee
---

## Story

As a person budgeting my own money at a terminal, I want a simple summary of a month, so that I
can look back at what came in and what went out without reading every individual entry.

## Acceptance criteria

- [x] AC1 — The command is `envel summary`, and it prints a summary for a calendar month. The
      month is named as a **plain word**, never behind an option: `envel summary 2026-08`
      summarises August 2026, and `envel summary --month 2026-08` is refused as a wrong command
      line, per AC14 [src: WI-0003/Q-004]. The stakeholder chose the plain word and gave the reason: *"naming a
      month is the normal case, not the rare one, so it gets the short form. And I'd rather
      everything in this tool be typed the same way than have one command that's special"*
      [src: WI-0003/Q-004]. `summary` takes no argument other than the month. The subcommand name
      `summary` itself is still `[assumed]`, under no delegation
      (`artifacts/refinement-qa.md`); what the stakeholder settled is the shape of what follows
      it.
- [x] AC2 — The summary prints one row per envelope, and each row shows four figures for that
      envelope: the money put into it during that month, the money spent from it during that
      month, the money moved into or out of it during that month, and the amount left in it at
      the end of that month [src: WI-0003/Q-001]. A move is counted only in the third figure and
      never in the second: *"'Spent' has to mean money that left the house, so moves don't belong
      in it"* [src: WI-0003/Q-001]. The moved figure is one net number, positive when more
      arrived than left — an envelope that received 50.00 and gave away 20.00 in the month shows
      30.00 — which is `[assumed]`, under no delegation (`artifacts/refinement-qa.md`).
- [x] AC3 — The figures reconcile, and reconciling is the whole point of AC2's third figure:
      *"I won't use a report whose rows don't add up"* [src: WI-0003/Q-001]. For each envelope,
      money in, minus money spent, plus money moved, equals the change in that envelope's amount
      across the month. The amount left in a row is the envelope's own balance, which carries
      over from the previous month rather than starting at zero — so for an envelope with 50.00
      carried in, nothing added, 20.00 spent and 30.00 moved in, the row reads in 0.00, spent
      20.00, moved 30.00, left 60.00, and 50.00 + 0.00 − 20.00 + 30.00 = 60.00.
- [x] AC4 — A month for which there is no row to print — a month that ended before any envelope
      existed — prints to stdout a line saying so, and exits 0, rather than an error or empty
      output. It is a success and not a refusal: the month was readable and the answer is that
      there is nothing in it [src: WI-0001 AC6 "Listing when no envelope has ever been created prints a line saying there
      are none"]. A month in
      which envelopes existed but nothing happened is **not** this case: it prints their rows
      with zeros, per AC7. This case is reached only for a month the command accepts at all: a
      month later than the one today falls in is refused before any row is considered, per AC9
      [src: WI-0003/Q-005].
- [x] AC5 — Run as `envel summary` with nothing after it, the command summarises the calendar
      month that today falls in. Run as `envel summary 2026-08`, it summarises that month
      instead; a month that has ended is still reachable after it has ended. A month is written
      `YYYY-MM` — four-digit year, hyphen, two-digit month — which is the date form this project
      already accepts with the day taken off [src: WI-0002 AC11 "`--on` accepts the full
      `YYYY-MM-DD` form and nothing else"], and no other spelling of the digits was offered or
      chosen [src: WI-0003/Q-004].
- [x] AC6 — The summary prints no total line for the month and does not list individual spends.
      Its content is the four columns of AC2 and nothing else. The two exclusions are the
      stakeholder's own [src: EP-001/Q-003] and the fourth column does not disturb them: they
      chose it knowing the report was meant to stay small [src: WI-0003/Q-001].
- [x] AC7 — The summary shows a row for every envelope that existed by the end of the month
      being summarised, and for no others [src: WI-0003/Q-002]. An envelope with no activity in
      that month still gets a row: 0.00 in, 0.00 spent, 0.00 moved, and its carried-over balance
      under what is left. An envelope created after that month ended gets no row, so a past
      month's summary prints the same rows whenever it is run — *"August's report should say the
      same thing in November as it did in September"* [src: WI-0003/Q-002].
- [x] AC8 — A month's money-in figure is the income **recorded** during that month. Income
      carries no date of its own, so income entered late falls in the month it was typed rather
      than the month it arrived — the opposite of a spend, which is held against its own date
      [src: WI-0002 AC9 "A spend can be recorded with a date other than today, written as"]. The
      asymmetry is the stakeholder's decision at `WI-0003/Q-003` and not an oversight: *"I put
      income in when it arrives — that's the one thing I'm never late on."* `envel add` is
      unchanged by this item.

- [x] AC9 — A month **later than the month today falls in** is refused: nothing is printed, a
      message saying that month has not happened yet goes to stderr, and the command exits
      non-zero [src: WI-0003/Q-005]. `envel summary 2027-03`, run in September 2026, is refused;
      `envel summary 2026-09`, the month today falls in, is **not** refused even though most of
      it may not have happened yet — the rule is *later than the current month*, not *later than
      today*. The stakeholder chose refusal over printing: *"A page of figures with the wrong
      year at the top is exactly the sort of thing I'd read straight past, and I'd rather be
      stopped"* [src: WI-0003/Q-005]. The stream and the exit code are the project's delivered
      convention rather than a new decision [src: WI-0001 AC16 "Every refusal this item specifies
      writes its message to stderr and exits non-zero"].

- [x] AC10 — The rows are ordered alphabetically by envelope name, ignoring capitalisation — the
      same order the delivered listing already prints and not a new decision
      [src: WI-0001 AC3 "the lines ordered alphabetically by name ignoring capitalisation"]. Two
      envelopes whose names differ only in capitalisation are one envelope
      [src: WI-0001 AC11 "Envelope names are matched without regard to capitalisation"], so the ordering has no tie to break.
- [x] AC11 — Every figure the summary prints is a plain decimal with exactly two decimal places
      and no currency symbol and no thousands separator — `0.00`, `20.00`, `1200.00` — which is
      the project's delivered output rule and not a new decision [src: WI-0001 AC8 "An amount is written with at most two
      decimal places"] [src: WI-0001 AC17 "No amount the tool prints carries a currency symbol"].
      AC3's worked example is written in that form.
- [x] AC12 — A month the tool cannot read is refused: `2026-8`, `08-2026`, `august`, `2026-13`,
      `2026-08-01` and anything else that is not four digits, a hyphen and a two-digit month in
      the range `01`–`12` are each refused with a message, nothing is printed on stdout, and no
      row is computed. This is `refine`'s own decision, `[assumed]` under **no delegation**
      (`artifacts/refinement-qa.md`), on the treatment the project already delivers for text it
      cannot read as a date [src: WI-0002 AC11 "`--on` accepts the full `YYYY-MM-DD` form and
      nothing else"]. A disagreement lands on this criterion alone.
- [x] AC13 — Every refusal this item specifies writes its message to stderr and exits non-zero,
      and every successful summary — including AC4's nothing-to-print line — writes its output to
      stdout and exits 0. It is the project's recorded convention
      [src: docs/architecture/overview.md] and the rule the delivered items already follow
      [src: WI-0001 AC16 "Every refusal this item specifies writes its message to stderr and
      exits non-zero"]. Checked case by case against the criteria that name them: refusals at AC9,
      AC12 and AC14; successes at AC1, AC2, AC4, AC5, AC6, AC7 and AC8.
- [x] AC14 — A command line of the wrong shape is refused with a usage message for the subcommand
      on stderr and a non-zero exit, and nothing is printed on stdout:
      `envel summary --month 2026-08` (an option, where this subcommand takes none),
      `envel summary 2026-08 extra` (a word beyond the month), and any other extra word. It is
      the same treatment the delivered subcommands already get [src: WI-0001 AC15 "A subcommand
      given the wrong number of arguments prints to stderr a usage message for that subcommand
      and exits non-zero"] [src: WI-0002 AC14 "`envel spend` with no arguments"].

## Out of scope

- Any period other than a month — no weekly, quarterly or yearly view, and no arbitrary date
  range.
- A total line across all envelopes for the month, and a listing of the individual spends under
  each envelope. The stakeholder ruled both out at `EP-001/Q-003`.
- Projecting forward — asking what would be left in each envelope if nothing more were spent
  this month. It is the one honest use a future-month summary would have had, and the stakeholder
  ruled it out of this round when they chose to refuse future months: *"The 'what if I stop
  spending now' idea is a nice-to-have, not this round — don't build it in"* [src: WI-0003/Q-005].
- Charts, graphs, colour, and any output that is not plain text.
- Comparison between months, trends, or averages.

## Notes

- AC5 and AC6 were placeholders and are no longer. `EP-001/Q-003` settled what the summary
  shows — option A, *"One row per envelope showing what went in that month, what was spent, and
  what is left"*, with no total line and no individual spends — and `EP-001/Q-004` settled the
  period — option A, calendar months, the current one by default and an earlier one on request.
  AC2, AC5 and AC6 are those two answers; AC1 names the command settled at `EP-001/Q-006`.
- AC3's carry-over sentence comes from the stakeholder's answer to `EP-001/Q-001`: *"money left
  in an envelope at the end of a month stays in that envelope; rolling over is the whole point
  of doing it this way."* It is what makes the third column a balance rather than a monthly
  remainder, and it is the one thing in this item they said they would not want us to get wrong.
- A spend carries the date it happened on, not the date it was typed in: the stakeholder chose
  "today unless I say otherwise" at `WI-0002/Q-001`, and gave this summary as their reason —
  *"a Saturday shop landing in the wrong month would make the monthly summary wrong."* So the
  month a spend falls into is decided by its own date, and a spend entered late still counts in
  the month it happened in. `WI-0002` AC9 is that rule on the recording side.
- A spend may carry a short description (`WI-0002/Q-002`), and this summary does not show it:
  the stakeholder ruled the individual spends out of this report at `EP-001/Q-003`.
- **`refine` round 1** walked the Definition of Ready and found R4, R6, R7, R8 and R10 failing.
  It filed three blocking questions, recorded the missing dependency, and rewrote no criterion.
  The full record is `artifacts/refinement-qa.md`.

- `depends-on: WI-0002` was added by that round, and it is the R7 failure. There is no such thing
  as *"the money spent from it during that month"* until spending exists, and AC3's reconciliation
  cannot be demonstrated at all against a tool that only takes money in. `WI-0002` in turn depends
  on `WI-0001`, which is `done`, so naming `WI-0002` alone is enough. The consequence is
  deliberate and is written here rather than left for a later reader to discover: the orchestrator
  dispatches nothing on an item whose `depends-on` is unfinished, so this item does not move again
  until `WI-0002` is `done` — including the round that consumes the answers below.

- The three questions round 1 put to the stakeholder, all open:
  - `WI-0003/Q-001` — does a move between envelopes count as money in and money out, or is it
    excluded from those columns? `EP-001/Q-003` chose what the summary shows before moving money
    existed as a thing the tool would do.
  - `WI-0003/Q-002` — does every envelope get a row, or only those with activity that month, and
    what about one created after the month ended?
  - `WI-0003/Q-003` — can income carry a date the way a spend now can? `envel add` is shipped and
    stamps income with the moment it was typed, so this summary's first column is keyed to when
    they sat at the terminal rather than to when they were paid. Their own argument at
    `WI-0002/Q-001` applies to a payslip word for word. This one may imply work on a delivered
    command, and routing that is `answer-questions`' to decide, not this round's.

- **Not asked, deliberately: how a month is named on the command line.** It was listed above as
  `refine`'s to ask and it is already open with the stakeholder in another form —
  `WI-0002/Q-003` (is an optional date a named option or a plain word) and `WI-0002/Q-004` (which
  date forms are accepted). A month is a date with the day taken off. Round 2 writes AC1 and AC5
  from those two answers; if they leave the month genuinely ambiguous, round 2 files that as its
  own question.

- Decided by round 1 rather than asked, each with its authority in `artifacts/refinement-qa.md`:
  the subcommand is `summary`; a month the tool cannot read is refused with a message and nothing
  printed; a month in the future is summarised like any other and is simply empty — all three
  `[assumed]` under **no delegation**, each landing on one criterion. Row ordering and the
  stream-and-exit-code rule are **not** assumptions but the project's delivered conventions
  [src: WI-0001 AC3 "the lines ordered alphabetically by name ignoring capitalisation"]
  [src: WI-0001 AC16 "Every refusal this item specifies writes its message to stderr and exits
  non-zero"].

- Open **design** questions, routed to `plan` rather than to the stakeholder, because the answer
  would be the same whoever they were:
  - how a month's figures are computed from the stored entries, and whether anything is
    precomputed;
  - how the third column, the balance at the end of a month, is derived for a month that is not
    the current one;
  - what the summary does with an entry naming an envelope that is no longer present — the same
    question `WI-0002` routed to `plan`, and it should get the same answer.

- A constraint from the stakeholder that is `WI-0005`'s to satisfy rather than this item's, and is
  recorded here so `plan` sees it: *"if I fix an entry, a past summary should just show the
  corrected figure"* [src: EP-001/Q-005].

- **No acceptance criterion was rewritten by round 1**, deliberately. Five of the six are
  downstream of something pending — AC1 and AC5 on the command surface, AC2, AC3 and AC4 on the
  three questions above — so round 2 writes them once, from the answers, rather than renumbering a
  list twice.

- **Round 1's three answers are in, and this is what they settled.** `answer-questions` consumed
  them on 2026-09-11; the stakeholder's words are quoted verbatim in
  `artifacts/refinement-qa.md` `## Answers — round 1`.
  - `WI-0003/Q-001` — option **C**: a move is kept out of *spent* and shown as a fourth figure.
    *"'Spent' has to mean money that left the house, so moves don't belong in it — but I won't use
    a report whose rows don't add up… A column of zeros costs me nothing; a number I can't account
    for costs me an evening."* AC2, AC3 and AC6 now say so. This is the one answer that pulls
    against something they said earlier — `EP-001/Q-003` asked for a small report — and they
    reconciled it themselves, in the reply, after the question named the tension.
  - `WI-0003/Q-002` — option **C**: every envelope that existed by the end of that month, zeros
    for untouched ones, nothing for envelopes made later. *"August's report should say the same
    thing in November as it did in September."* AC7 is new and says so, and AC4 was rewritten
    because their answer changes what the empty case is.
  - `WI-0003/Q-003` — option **B**: income is dated when it is typed, and `envel add` is not
    reopened. *"I'm not paying for rework on a command that already works for a case I don't have;
    if it turns out to bite me after a couple of months, I'll tell you then."* AC8 is new and
    states the rule and the asymmetry with a spend. **No item was filed**: options A and C would
    each have created one, and B declines both.
- **The limitation the stakeholder knowingly accepted, recorded once so nobody re-derives it as a
  defect.** Income entered later than the month it arrived in is counted in the month it was
  typed, and there is no way to correct it — `WI-0005` is scoped to spends. They were shown this
  as option B's cost and took it anyway, on their own habit, and said what they would do if it
  turns out to matter. Anyone who later finds a payslip in the wrong month is looking at AC8
  working as specified, not at a bug; the route back is a new request from them, not a fix.
- **One thing the answers did not settle, decided here rather than asked.** `Q-001`'s option C
  said *"moved in or out"* without saying whether that is one figure or two. It is one net
  number, positive when more arrived than left — `[assumed]`, under no delegation. Two figures
  would be a fifth column on a report they have twice asked to stay small, and net is what makes
  AC3's row add up in one subtraction. A disagreement lands on AC2 and AC3 and costs one column.
- **Round 1 deferred the criteria rewrite to round 2; `answer-questions` did it instead, and here
  is why.** Round 1's reason was that five of six criteria were downstream of something pending,
  so round 2 should write them once rather than renumbering twice. Three of those answers are now
  in, and AC2, AC3, AC4 and AC6 were amended **in place** with AC7 and AC8 **appended**, so no
  criterion changed its number and every `WI-0003 AC<n>` citation still resolves. The reason not
  to wait is specific to this item: `depends-on: WI-0002` means the orchestrator dispatches
  nothing here until `WI-0002` is `done`, which is several items away — so an answer left in a
  question file would have sat unpropagated for the whole of that, and `item.md` would have gone
  on saying three columns to everyone who read it.
- **What `refine` round 2 still has to do.** AC1 and AC5 are untouched and still fail R4: nobody
  has said what is typed to get a summary or how a month is named on the command line. Round 1
  left that to round 2 on the grounds that the two `WI-0002` questions about date syntax would
  settle it, and **those are now answered** — `WI-0002/Q-003` (the description is a plain word,
  the date is `--on`) and `WI-0002/Q-004` (`YYYY-MM-DD` and nothing else). Round 2 has what it
  needs to write AC1 and AC5, or to file its own question if a month still reads two ways.
  `answer-questions` deliberately did not write them: they are not what any question on this item
  asked, and deriving a command surface from someone else's answer is refinement's judgement to
  make in the open, not a propagation.

- **`refine` round 2 filed two blocking questions and rewrote no criterion.** Both are about the
  line you type to get a summary, and they are one ask. The full record of the round is
  `artifacts/refinement-qa.md` `## Round 2`.
  - `WI-0003/Q-004` — is a month named as a plain word (`envel summary 2026-08`) or behind an
    option (`envel summary --month 2026-08`)? Round 1 left AC1 and AC5 waiting on
    `WI-0002/Q-003` and `WI-0002/Q-004`, expecting those two answers to settle this. They settle
    **half** of it: a month is written `2026-08` and there is no argument about the digits
    [src: WI-0002/Q-004]. They do not settle the shape, because the reason the stakeholder gave
    at `WI-0002/Q-003` — the cheap form goes to the thing you type often — was resolving a
    contest between *two* optional things at the end of the `spend` line, and `summary` has only
    one. Applying it here means guessing how often they name a month, which is a fact about them.
  - `WI-0003/Q-005` — is a month that has not happened yet refused, or printed? **This is a
    question round 1's own assumption can no longer answer**, and the reason is recorded below.

- **Round 1's future-month assumption is withdrawn, pending `Q-005`.** Round 1 decided, under no
  delegation, that *"a month in the future is summarised like any other, and is simply empty"*,
  on the grounds that a future month holds no entries and so falls into AC4's empty case. The
  stakeholder's answer to `WI-0003/Q-002` made that false: AC7 gives a row to every envelope that
  existed by the end of the month summarised, and every envelope that exists today existed by the
  end of any future month. So `envel summary 2027-03` prints every envelope, zeros in the three
  activity columns and today's balance under what is left — a page that looks exactly like a real
  report for a month that has not happened. The assumption is not quietly corrected and it is not
  re-decided here; it is put to the stakeholder as `Q-005`, because what it turns on is something
  they have twice told us matters to them — *"stop me rather than take something I didn't mean"*
  [src: WI-0002/Q-005] — applied to a command that, unlike the one they said it about, records
  nothing.

- **What round 2 did not change.** No acceptance criterion was rewritten. AC1 and AC5 still say
  what round 1 left them saying, and round 3 writes them once from both replies rather than
  renumbering the list twice while `WI-0003 AC<n>` citations point into it — `grep -rn 'WI-0003
  AC' tracker docs` finds four, every one of them naming **AC8** and every one anchored to its
  opening words, in `ADR-0002`, `ADR-0006` and `WI-0002`'s two reports. Each was re-read against
  the criterion it now points at and still resolves. Everything round 1 and `answer-questions` settled stands untouched: the
  four columns, the reconciliation, which envelopes get a row, and income dated when it is typed.

- **Round 2's two answers are in, and this is what they settled.** `answer-questions` consumed
  them on 2026-09-11; the stakeholder's words are quoted verbatim in
  `artifacts/refinement-qa.md` `## Answers — round 2`.
  - `WI-0003/Q-004` — option **A**: the month is a plain word, `envel summary 2026-08`, and there
    is no `--month`. *"Naming a month is the normal case, not the rare one, so it gets the short
    form. And I'd rather everything in this tool be typed the same way than have one command
    that's special."* AC1 and AC5 now say so, and they are the two criteria round 1 and round 2
    both left standing. This is the stakeholder answering the command surface directly, not
    `answer-questions` deriving one from an answer given about another item — which is the thing
    round 1 declined to do, and the reason it declined no longer applies.
  - `WI-0003/Q-005` — option **A**: a month later than the current one is refused, with a message
    saying why. *"A page of figures with the wrong year at the top is exactly the sort of thing
    I'd read straight past, and I'd rather be stopped."* AC9 is new and says so; AC4 was amended
    to say that its empty case is reached only for a month the command accepts. The "what if I
    stop spending now" projection was ruled out in the same breath — *"a nice-to-have, not this
    round — don't build it in"* — and is now in `## Out of scope`. **No item was filed**: the
    stakeholder declined the only work this answer could have implied.
- **Round 1's withdrawn future-month assumption is now closed, by the stakeholder rather than by
  us.** Round 1 assumed a future month was *"summarised like any other, and is simply empty"*;
  AC7 falsified that; round 2 withdrew it and asked. The answer is the opposite of the
  assumption, which is the case the withdrawal existed for. Nothing in the record now carries
  that assumption.
- **AC1 and AC5 are no longer the R4 failure, and nothing on this item is now waiting on the
  stakeholder.** What is left for `refine` round 3 is to walk the Definition of Ready again with
  R4, R6 and R10 closed, and to decide whether the one remaining round-1 assumption that still
  has no criterion — *a month the tool cannot read is refused, with a message, and nothing is
  printed* — is written onto AC5 or left as it is. `answer-questions` deliberately did not write
  it: no question asked it, it is `refine`'s own `[assumed]` decision under no delegation, and
  putting an assumption into a criterion is refinement's judgement taken in the open rather than
  a propagation.
- **Numbering held again.** AC1, AC4 and AC5 were amended **in place** and AC9 **appended**, so
  no criterion changed its number. `grep -rn 'WI-0003 AC' tracker docs` finds four citations,
  every one naming **AC8** and every one anchored to its opening words; AC8 is untouched by this
  execution, so all four still resolve.

- **`refine` round 3 took this item to Ready and asked the stakeholder nothing.** Its full record
  is `artifacts/refinement-qa.md` `## Round 3`. Three Definition-of-Ready criteria were failing
  and none of them was theirs.
  - **R7** — `depends-on: WI-0004` is now recorded, and it is the same argument round 1 made for
    `WI-0002`. There is no such thing as *"the money moved into or out of it during that month"*
    until moving money exists, and AC3's worked example — 50.00 carried in, 20.00 spent, 30.00
    moved in, 60.00 left — cannot be observed at all against a tool with no `envel move`. Round 1
    could not see this: it recorded `WI-0002` as the dependency before the stakeholder's answer to
    `Q-001` had put a **moved** column in the report. The consequence is deliberate and is written
    here rather than left for a later reader: the orchestrator dispatches nothing on an item whose
    `depends-on` is unfinished, so this item does not move again until `WI-0004` is `done`.
    `WI-0004` depends only on `WI-0001`, which is `done`, so nothing is circular and nothing else
    is held up.
  - **R4** — AC1 said `--month` was *"not accepted"* without saying what that looks like, and AC4
    said a summary *"says so"* without naming a stream or an exit code. Both were round 1's
    wording and both are now decidable: AC1 points at AC14, and AC4 names stdout and exit 0.
  - **R10** — five combinations this item introduces had no stated behaviour anywhere: a month in
    a form the tool cannot read; an option given to a subcommand that takes none; a word beyond
    the month; the order the rows come out in; and how a figure is written. AC10 to AC14 are new
    and cover all five.
- **What round 3 added, and on whose authority.** AC10, AC11, AC13 and AC14 are the project's
  **delivered conventions** cited rather than new decisions — the listing's ordering, two decimal
  places and no currency symbol, stdout/stderr and the exit code, and the usage message for a
  wrong command line. AC12 is the one genuine assumption, and it is round 1's own, now written
  onto a criterion: a month the tool cannot read is refused with a message and nothing printed,
  `[assumed]` under **no delegation**. It is the last of round 1's four assumptions to reach a
  criterion.
- **Numbering held a third time.** AC1 and AC4 were amended **in place** and AC10 to AC14
  **appended**, so no criterion changed its number. `grep -rn 'WI-0003 AC' tracker docs` finds
  seven citations from outside this item's own prose — four naming **AC8** and three naming
  **AC2** — every one anchored to its criterion's words, and neither AC2 nor AC8 was touched by
  this round.
- **Deliberately unconstrained, and left so by `refine` round 3.** `[assumed]`, **under no
  delegation** — nothing the stakeholder has said covers any of these, and each is recorded here
  rather than decided because a reasonable implementation may settle it either way without
  surprising them. `plan` may settle any of them and should say so if it does.
  - **Which message is printed when more than one refusal applies at once** — `envel summary
    2027-13` is both unreadable (AC12) and later than this month (AC9), and `envel summary
    --month 2027-13` adds AC14. Every criterion involved is satisfied by any of the three: the
    summary is refused, nothing goes to stdout, the exit is non-zero. A disagreement lands on
    whichever of AC9, AC12 and AC14 is read as promising its own message first, and costs the
    order of a few checks. This is the same thing `WI-0002` left open and `plan` settled there by
    putting the envelope check first.
  - **The wording of every message**, exactly as `WI-0001` and `WI-0002` left it. The criteria say
    what a message must contain — that the month has not happened yet, that the month cannot be
    read, the usage of the subcommand — and never how it reads.
  - **Whether the four figures are labelled, and how the columns are headed.** AC2 fixes what the
    four figures are and AC6 fixes that nothing else is on the page; neither says whether there is
    a header line. A disagreement lands on AC6 and costs one line of output.

- **Still `[assumed]` and still ours after round 3**: the subcommand `summary` (AC1), an
  unreadable month refused with a message and nothing printed (now AC12), and *"moved in or out"*
  as one net figure rather than two (AC2 and AC3). All three are under **no delegation**, and each
  now names the criterion a disagreement lands on. The future-month assumption is **no longer** on this list: it was
  `Q-005`, and `Q-005` is answered — a future month is refused, which is the stakeholder's
  decision at AC9 and not ours.
