---
status: recorded
---

# Refinement Q&A — WI-0003

`status: recorded`, as of 2026-09-11: both rounds' replies have arrived in the question files and
`answer-questions` has propagated them, so the conversations this file records have happened and
are quoted verbatim in `## Answers — round 1` and `## Answers — round 2`, marked `human`. The
field was `agenda` while questions stood unanswered; none does now. Round 1 did not take the item
to Ready — AC1 and AC5 had no command surface — and round 2 did not either, because it asked
rather than wrote. Round 2's answers give AC1, AC5 and AC9 their content, and `refine` round 3 is
what walks the Definition of Ready against them.

## Round 1 — the agenda this round came from

`refine` walked `spec/dor-dod.md` §1 against `WI-0003` as `intake` and `answer-questions` left
it. Five criteria fail:

- **R4** — five of the six acceptance criteria are not decidable by someone with a terminal.
  AC1 says only *"There is an `envel` command that prints a summary for a calendar month"* — no
  command, and no way to name a month. AC5 says a month can be named without saying how. AC2 says
  *"one row per envelope"* without saying which envelopes, and its three figures have no stated
  treatment of a transfer. AC4 says a summary *"says so"* without naming the stream or the exit
  code. Only AC3 and AC6 are decidable as written — AC3 because it carries a worked example
  (50.00 in, 0.00 added, 20.00 spent, 30.00 left), which is exactly what makes it checkable.
- **R7** — the dependency on `WI-0002` is real and unrecorded. There is no such thing as *"the
  money spent from it during that month"* until spending exists, and AC3's reconciliation cannot
  be demonstrated at all against a tool that only takes income in. This round records it.
- **R8** — this file did not exist.
- **R10** — four combinations the item introduces have no stated behaviour: a transfer between
  envelopes in the in/spent columns; an envelope with no activity in the month, including one
  created after that month ended; a month named in a form the tool cannot read; and a month in
  the future. The first two are asked below; the second two are decided below.
- **R6** passed before this round and fails now, by design, because this round files three
  blocking questions.

R1, R2, R3, R5, R9, R11 and R12 pass. The item's own `## Notes` had already named three things
as *"`refine`'s to ask"*, and this round disposes of all three: two are asked, and the third —
how a month is named on the command line — is **not** asked, for the reason under
*Deliberately not asked* below.

## Questions put to the stakeholder — round 1, all three answered

All three are one ask about one thing: what the three numbers in a row actually mean.

| # | Question | Why it is theirs | Status |
|---|----------|------------------|--------|
| Q-001 | Does a move between envelopes count as money in and money out, or is it excluded from those columns? | `EP-001/Q-003` chose what the summary shows *before* moving money existed as a thing the tool would do — they asked for that at `EP-001/Q-005`, and it is `WI-0004`. The answer changes what every number in the report means, and they said a move is routine, not rare. | `answered` |
| Q-002 | Does every envelope get a row, or only those with activity in that month — and what about one created after the month ended? | It is what they see every time they run the command, and it decides whether a past month's summary is a fixed document or one that grows a line each time they make an envelope. | `answered` |
| Q-003 | Can income carry a date, the way a spend now can? | Found by reading their own answers against what is built. `envel add` is shipped and stamps income with the moment it was typed, so the summary's first column is keyed to when they sat at the terminal. Their argument for dating spends — *"a Saturday shop landing in the wrong month would make the monthly summary wrong"* — applies to a payslip word for word, and they told us at `EP-001/Q-004` that calendar months matter because *"calendar months are what my payslips and statements use."* | `answered` |

## Deliberately not asked

- **How a month is named on the command line.** The item's `## Notes` listed it as `refine`'s to
  ask, and this round is deliberately not asking it, because it is already open with the
  stakeholder in another form. `WI-0002/Q-003` asks whether an optional date is a named option or
  a plain word, and `WI-0002/Q-004` asks which date forms the tool accepts. A month is a date with
  the day taken off; whatever they answer there settles the shape of this one, and asking again
  would be putting a near-duplicate question in front of them in the same round. Round 2 of this
  item writes AC1 and AC5 from those two answers.

  If their answers somehow leave the month ambiguous — for example if they choose a day-first
  short form, where `9/2026` and `2026/9` are both plausible — that is a real question and round 2
  files it. It is not one yet.

- **Whether a spend's description appears in the summary.** Answered: `EP-001/Q-003` ruled the
  individual spends out, and the item's `## Notes` already records it.

- **What the summary does about corrections (`WI-0005`).** Answered at `EP-001/Q-005` — *"if I
  fix an entry, a past summary should just show the corrected figure"* — and it is a constraint on
  `WI-0005`, not a question for this item. Recorded in `## Notes` so `plan` sees it.

## Decided here, and by what authority

Four things, decided rather than asked because the answer would be the same whoever the
stakeholder was, or because a delivered convention already settles it.

- **The subcommand is `summary`, as `envel summary`.** `[assumed]`

  **Under no delegation.** Nothing the stakeholder has said names it. It is assumed on the same
  footing as `WI-0001`'s `new`, `add` and `list` and `WI-0002`'s `spend`: the words below `envel`
  have been ours throughout, and asking about the fifth while never having asked about the first
  four would be inconsistent rather than careful. A disagreement lands on `WI-0003` AC1 and costs
  the name of one subparser.

- **A month the tool cannot read is refused, with a message, and nothing is printed.** `[assumed]`

  **Under no delegation.** Every other malformed input in this tool is already refused this way,
  built and verified [src: WI-0001 AC17 "each refused with a message with nothing recorded"]
  [src: WI-0001 AC13 "are refused with a message and no envelope is created"], and the
  alternative — quietly summarising the current month instead — would show them a report they did
  not ask for under a heading they did not type. A disagreement lands on one criterion.

- **A month in the future is summarised like any other, and is simply empty.** `[assumed]`

  **Under no delegation.** It is assumed rather than asked because there is nothing to protect:
  a future month contains no entries, so the answer is AC4's *"a month in which nothing was
  recorded"* case and no separate rule is needed. If `WI-0002/Q-005` comes back allowing spends
  to be dated forward, a future month can hold something and this decision still reads correctly —
  it summarises whatever is there. A disagreement lands on one criterion.

- **The rows are ordered alphabetically by envelope name ignoring capitalisation, output goes to
  stdout with exit 0, and every refusal goes to stderr with a non-zero exit.** Not an assumption:
  both are the project's recorded conventions [src: docs/architecture/overview.md] and their own
  criteria on the delivered item [src: WI-0001 AC3 "the lines ordered alphabetically by name
  ignoring capitalisation"] [src: WI-0001 AC16 "Every refusal this item specifies writes its
  message to stderr and exits non-zero"]. Round 2 writes them into the criteria by citation rather
  than restating them as new decisions.

  The **wording** of every message and every column heading stays deliberately unconstrained, as
  `WI-0001` `## Notes` left it. The criteria will say what a row must contain — the envelope's
  name and the three figures — and not how it reads.

## Routed to `plan`, not to the stakeholder

Recorded in `WI-0003` `## Notes` for `plan` to settle under its own preference order:

- how a month's figures are computed from the stored entries — whether by filtering the entry log
  on each run or by keeping anything precomputed;
- how the third column, the balance at the end of a month, is derived for a month that is not the
  current one;
- what the summary does with an entry in the store that names an envelope no longer present —
  the same question `WI-0002` routed to `plan`, and it should get the same answer.

## Cross-answer check

No answer was consumed by this execution, so there is nothing to check a reply against yet. Each
of the three questions carries its own `## Cross-answer check` section, filed **with** the
question rather than after it, naming the prior answers the reply will have to coexist with:
`EP-001/Q-001`, `EP-001/Q-002`, `EP-001/Q-003`, `EP-001/Q-004`, `EP-001/Q-005`, `WI-0001/Q-002`
and `WI-0002/Q-001`.

`Q-003`'s is the one to watch. `WI-0002/Q-001` is an answer about **spending**, and it is
deliberately not read as covering income — stretching it would be answering `Q-003` on the
stakeholder's behalf. If they answer "no" there, that is a decision about income and not a
reversal of what they said about spends, and it must be recorded that way rather than smoothed
over.

`scripts/lint-answers --item WI-0003` → exit 0.

## What round 1 has not settled

The three questions above, and AC1 and AC5's command surface, which waits on `WI-0002/Q-003` and
`WI-0002/Q-004`. **No acceptance criterion was rewritten by this execution**, deliberately: five
of the six are downstream of something pending, and rewriting them now would mean guessing, then
renumbering the list again in round 2. `grep -rn 'WI-0003 AC' tracker docs` → exit 1, no matches,
so nothing outside this item points into the list — but that is a reason to renumber carefully
once, not a licence to do it twice (F-094).

What this round *did* change in the item: `depends-on: WI-0002` in the frontmatter, which is R7,
and `## Notes`.

---

## Answers — round 1

All three replies are the stakeholder's own words, copied from the `## Answer` section of the
question file named, and marked `human`. `answer-questions` consumed them on 2026-09-11 and
propagated each into `WI-0003`'s criteria; the per-question `## Consequences` sections name the
files.

- **Q-001 — a move between envelopes, in the summary's columns.** `human`, option C:

  > C. "Spent" has to mean money that left the house, so moves don't belong in it — but I won't
  > use a report whose rows don't add up, I've spent years chasing that in the spreadsheet. A
  > column of zeros costs me nothing; a number I can't account for costs me an evening.

  Propagated to `WI-0003` AC2 (four figures, a move in the third and never the second), AC3 (the
  reconciliation rewritten with the moved figure and a worked example that adds up) and AC6 (*the
  four columns of AC2*, which would otherwise have contradicted AC2 outright). They chose against
  `refine`'s recommendation of B, and gave the reason B was wrong for them.

- **Q-002 — which envelopes get a row.** `human`, option C:

  > C. August's report should say the same thing in November as it did in September — that's the
  > whole reason I check it against a statement. Envelopes I didn't touch still get their row;
  > that's where the rolled-over money is sitting.

  Propagated to `WI-0003` AC7, which is new, and to AC4, which had to be rewritten: with rows of
  zeros for untouched envelopes, *"a month in which nothing was recorded"* is no longer the empty
  case, and the honest empty case is a month that ended before any envelope existed.

- **Q-003 — whether income can carry a date.** `human`, option B:

  > B. I put income in when it arrives — that's the one thing I'm never late on, because it's the
  > bit I enjoy. I'm not paying for rework on a command that already works for a case I don't
  > have; if it turns out to bite me after a couple of months, I'll tell you then.

  Propagated to `WI-0003` AC8, which states that a month's money-in figure is the income recorded
  in that month and names the asymmetry with a spend as their decision. **No item was filed.**
  Options A and C would each have implied one — new work on the delivered `envel add` — and B is
  a refusal of both; filing it anyway would have put work on the board that they had just
  declined. The limitation they accepted, and what they said they would do about it, is in
  `WI-0003` `## Notes`.

## Cross-answer check — round 1, on the replies

Written by `answer-questions` on consuming the three replies. Each question file carries its own
`## Cross-answer check` with the IDs and a verdict for each; eleven verdicts, all `compatible`,
**no conflict**, so no question was filed under ADR-0008 §3.

Two of them were close enough to be worth recording here rather than only in the question files:

- `Q-001` against `EP-001/Q-003`. They had asked for a small report and this answer adds a column
  to it. It is not a conflict because the question named that tension in as many words and they
  answered it directly — *"A column of zeros costs me nothing"* — so the reconciliation is
  theirs. What `EP-001/Q-003` actually ruled out, a total line and a list of individual spends,
  is untouched and still in AC6.
- `Q-003` against `WI-0002/Q-001`. The watch round 1 filed with the question was exactly this,
  and it came out the way the watch anticipated: the answer is B, which is a decision about
  **income**, and `WI-0002/Q-001` remains their decision about **spending**. Neither was read as
  covering the other, and AC8 records the asymmetry as chosen rather than as an oversight.

`scripts/lint-answers --item WI-0003` → exit 0.

## What round 1's answers left for round 2

- **AC1 and AC5 still have no command surface, and this is now round 2's whole remaining R4
  failure.** Round 1 left them waiting on `WI-0002/Q-003` and `WI-0002/Q-004`; both are now
  answered — the description is a plain word, the date is `--on`, and a date is `YYYY-MM-DD` and
  nothing else. Round 2 has what it needs to write them, or to file its own question if a month
  named on the command line still reads two ways. `answer-questions` did not write them:
  deriving a command surface from answers given about a different item is refinement's judgement,
  taken in the open, not a propagation.
- **The criteria round 1 deferred have been written**, by `answer-questions` rather than by round
  2, and `WI-0003` `## Notes` records why: `depends-on: WI-0002` means nothing is dispatched on
  this item for several items yet, so waiting would have left `item.md` saying *three columns* to
  every reader in the meantime. AC2, AC3, AC4 and AC6 were amended in place and AC7 and AC8
  appended, so nothing renumbered — the cost round 1 was avoiding did not arise.
- **Still `[assumed]` and still ours**, unchanged by these replies: the subcommand `summary`, an
  unreadable month refused, a future month summarised as empty, and — new with `Q-001`'s answer —
  that *"moved in or out"* is one net figure rather than two.

---

## Round 2 — the agenda this round came from

Round 2 opened with `WI-0002` `done`, which is what made this item dispatchable again, and with
one stated job: *"AC1 and AC5 are untouched and still fail R4: nobody has said what is typed to
get a summary or how a month is named on the command line"* (`## What round 1's answers left for
round 2`, above). Walking the Definition of Ready against the item as `answer-questions` left it
found that job, and one thing nobody had listed.

| # | verdict before this round | note |
|---|---------------------------|------|
| R1 | pass | frontmatter complete; `type`, `epic`, `priority` all set |
| R2 | pass | `## Story` names the role, the capability and the outcome, unchanged since intake |
| R3 | pass | eight criteria, labelled and checkboxed |
| R4 | **fail** | AC1 and AC5 name no command surface. `envel summary` is assumed; how a month is written on the line is not settled |
| R5 | pass | `## Out of scope` names four things, including a total line and the individual spends, which a reader could reasonably assume were included |
| R6 | pass before this round | `Q-001` to `Q-003` all `answered`. This round files two blocking questions, so R6 fails **by this round's own act** and is what suspends the item |
| R7 | pass | `depends-on: WI-0002`, now `done` |
| R8 | pass | this file, `status: recorded`, carrying round 1 in full |
| R9 | pass | one coherent change: one subcommand that reads the store and prints a table |
| R10 | **fail** | the future-month case, below. Round 1 recorded a behaviour for it; AC7 now contradicts that behaviour, so the combination is neither stated nor honestly unconstrained |
| R11 | pass | no criterion counts a project artefact. AC2's *"four figures"* counts columns of the tool's own output, which R11 is not about |
| R12 | pass | four `[assumed]` entries, each saying in terms that it was taken under **no** delegation and where a disagreement lands; no standing licence is relied on anywhere in this item |

## The R10 failure round 2 found, and why it became a question rather than a fix

Round 1 decided, under no delegation:

> **A month in the future is summarised like any other, and is simply empty.** `[assumed]`
>
> It is assumed rather than asked because there is nothing to protect: a future month contains no
> entries, so the answer is AC4's *"a month in which nothing was recorded"* case and no separate
> rule is needed.

The premise was true when it was written and the stakeholder's reply to `Q-002` falsified it. AC7
now reads *"a row for every envelope that existed by the end of the month being summarised"*, and
every envelope that exists today existed by the end of any month still to come. So the output for
`envel summary 2027-03` is not empty: it is every envelope, zeros in the in, spent and moved
columns, and today's balance under what is left — indistinguishable on the page from a real
report.

Two moves were available and only one of them is legal here. Re-deciding it — *"a future month is
refused"*, say, on the strength of `WI-0002/Q-005` — would be answering on the stakeholder's
behalf using an answer they gave about **recording a spend**, which is a decision about their
file rather than about a report, and stretching it is exactly the move round 1 refused to make
with `WI-0002/Q-001` on income. So the assumption is **withdrawn** and the case is put to them as
`Q-005`. What is recorded, and is not a guess, is that round 1's answer is no longer available.

## Questions put to the stakeholder — round 2

Two questions, presented as one ask. Neither is a re-ask: `Q-004` is the item's own recorded
remaining R4 failure, and `Q-005` is new and arises from the interaction of two of their own
answers.

| # | question | why it is theirs |
|---|----------|------------------|
| `Q-004` | Is a month named as a plain word — `envel summary 2026-08` — or behind an option, `--month 2026-08`? | It is what they type every time they use the feature they asked for in their opening sentence. The last time this skill asked them the same shape of question, at `WI-0002/Q-003`, they chose option C, which was neither of the two obvious answers, and they gave a reason keyed to their own typing habits. That reason does not reach this case (below), so applying it would be guessing about them rather than following them. |
| `Q-005` | Is a month that has not happened yet refused, or printed? | It is a policy about being stopped rather than handed something they did not mean, which they have stated twice in their own words, applied to a command that — unlike the one they stated it about — records nothing. And our own earlier answer to it is no longer available. |

## Why `WI-0002/Q-003` and `WI-0002/Q-004` did not settle `Q-004`, in detail

Round 1 said it was not asking about the command surface because *"a month is a date with the day
taken off; whatever they answer there settles the shape of this one"*, and set a condition for
round 2 to file anyway: *"if their answers somehow leave the month ambiguous — for example if they
choose a day-first short form, where `9/2026` and `2026/9` are both plausible."*

That specific ambiguity did **not** happen. `WI-0002/Q-004` came back **A** — *"the full
`2026-09-07` and nothing else"* — so a month is `2026-08` and no digit is in doubt. Half of
round 1's expectation is met and is used rather than re-asked.

The other half is not met, and the reason is structural rather than a matter of taste.
`WI-0002/Q-003` asked which of **two** optional trailing things on `envel spend` — a description
and a date — should get the bare-word slot, since only one of them could. They answered by ranking
them on frequency: *"The description is the bit I'll actually type, so make that the cheap one,
and put the longer spelling on the date since I'll hardly ever give one."* On `envel summary`
there is exactly one optional thing, so there is no contest to resolve, and what is left of their
rule is a bare frequency question — how often do they name a month? — which is a fact about their
habits that only they hold. The evidence in the record points both ways and is set out in
`Q-004`'s `## Context`.

This is `refine`'s step 3 applied honestly rather than conveniently: the answer would **not** be
the same whoever the stakeholder was, which is the test for routing it to `plan` instead, and
`WI-0002/Q-003` is direct evidence that this stakeholder has a non-obvious preference in exactly
this category.

## Decided here, and by what authority — round 2

Nothing new was decided this round, and that is itself the decision worth recording. Round 1's
four entries under `## Decided here, and by what authority` were re-read against the item as
`answer-questions` left it:

- **The subcommand is `summary`.** `[assumed]`, **under no delegation** — unchanged, and still on
  the same footing as `new`, `add`, `list` and `spend`, all four of which are now delivered under
  assumed names. A disagreement lands on AC1.
- **A month the tool cannot read is refused, with a message, and nothing is printed.**
  `[assumed]`, **under no delegation** — unchanged, and now standing on delivered behaviour
  rather than on planned behaviour: `WI-0002` AC11 shipped exactly this treatment for a date
  [src: WI-0002 AC11 "accepts the full `YYYY-MM-DD` form and nothing else"]. A disagreement lands
  on one criterion.
- **"Moved in or out" is one net figure rather than two.** `[assumed]`, **under no delegation** —
  unchanged. A disagreement lands on AC2 and AC3 and costs one column.
- **A month in the future is summarised like any other, and is simply empty.** **Withdrawn.** See
  `## The R10 failure round 2 found` above; it is now `Q-005`.

Row ordering and the stream-and-exit-code rule remain **not** assumptions but the project's
delivered conventions [src: WI-0001 AC3 "the lines ordered alphabetically by name ignoring
capitalisation"] [src: WI-0001 AC16 "Every refusal this item specifies writes its message to
stderr and exits non-zero"], and `WI-0002` AC13 has since delivered the second of them again.

## Cross-answer check — round 2

No answer was consumed by this execution — round 2 asks, it does not propagate — so there is
nothing to check a reply against yet. `Checked against: none`, because this execution consumed no
human answer.

Each of the two questions carries its own `## Cross-answer check` section, filed **with** the
question rather than after it, naming the prior answers the reply will have to coexist with:
`Q-004` against `WI-0002/Q-003`, `WI-0002/Q-004`, `EP-001/Q-004` and `EP-001/Q-006`; `Q-005`
against `WI-0002/Q-005`, `WI-0003/Q-002`, `EP-001/Q-003` and `EP-001/Q-004`.

`Q-005`'s is the one to watch, and it is the same shape as round 1's watch on `Q-003`.
`WI-0002/Q-005` is an answer about **recording** a spend, and it is deliberately not read as
covering a report. If the stakeholder answers B or C there, that is a decision about summaries
and not a reversal of what they said about spends, and it must be recorded that way rather than
smoothed over.

`scripts/lint-answers --item WI-0003` → exit 0.

## What round 2 has not settled

- `Q-004` and `Q-005` were both blocking and both with the stakeholder; both are now
  `answered` and propagated — see `## Answers — round 2` below.
- **No acceptance criterion was rewritten**, deliberately. AC1 and AC5 are downstream of `Q-004`
  and AC4 is downstream of `Q-005`; writing them now would mean guessing two answers and then
  renumbering the list again in round 3. The renumbering obligation was discharged rather than
  assumed: `grep -rn 'WI-0003 AC' tracker docs` → exit 0, and every citation it finds names
  **AC8** and no other criterion — `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md`
  `## Corrections`, `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md`
  line 38, and two rows of `WI-0002`'s review and verification reports quoting them. All four are
  anchored, `[src: WI-0003 AC8 "A month's money-in figure is the income"]`, and AC8 still opens
  with exactly those words, so each resolves to the criterion its author meant (F-094). Round 1's
  note that the grep found nothing is true of round 1 and is now out of date: `WI-0002`'s ADR
  work cited AC8 in between.
- Round 3 therefore has three things to write and no more: AC1 and AC5 from `Q-004`, AC4 from
  `Q-005`, and the Definition of Ready walked again with R4, R6 and R10 closed.


## Answers — round 2

Both replies are the stakeholder's own words, copied from the `## Answer` section of the question
file named, and marked `human`. `answer-questions` consumed them on 2026-09-11 and propagated each
into `WI-0003`'s criteria; the per-question `## Consequences` sections name the files.

- **Q-004 — how a month is named on the command line.** `human`, option A:

  > A — `envel summary 2026-08`. Your reading of me is right: naming a month is the normal case,
  > not the rare one, so it gets the short form. And I'd rather everything in this tool be typed
  > the same way than have one command that's special.

  Propagated to `WI-0003` AC1, which now names the command and states that the month is a plain
  word and that `--month` is not accepted, and to AC5, which now shows both invocations and fixes
  the month's spelling as `YYYY-MM`. This is the one thing round 1 and round 2 both left standing,
  and it is now settled by the stakeholder directly rather than derived from an answer they gave
  about `WI-0002`. They chose **with** `refine`'s recommendation and, unusually, confirmed the
  reasoning behind it — that naming a month is the common case — which is the fact about their
  own habits the question said we could not supply.

- **Q-005 — a month that has not happened yet.** `human`, option A:

  > A — refuse it, and say why. A page of figures with the wrong year at the top is exactly the
  > sort of thing I'd read straight past, and I'd rather be stopped. The "what if I stop spending
  > now" idea is a nice-to-have, not this round — don't build it in.

  Propagated to `WI-0003` AC9, which is new and states the refusal, the *later than the current
  month* boundary, and the stream and exit code; to AC4, which now says its empty case is reached
  only for a month the command accepts; and to `## Out of scope`, which now names the forward
  projection they declined. **No item was filed.** The only work this answer could have implied
  is the projection, and the reply is an explicit refusal of it — filing it would put work on the
  board they had just declined, which is the same reasoning that applied to `Q-003` in round 1.

  This answer closes round 1's withdrawn assumption in the opposite direction from the assumption
  itself. Round 1 had decided a future month was *"summarised like any other, and is simply
  empty"*; the stakeholder refuses it outright. Withdrawing rather than quietly correcting is what
  put the question in front of them, and had round 2 not withdrawn it, the tool would have shipped
  a page of plausible figures under a heading they have just told us they would read straight
  past.

## Cross-answer check — round 2, on the replies

Written by `answer-questions` on consuming the two replies. Each question file carries its own
`## Cross-answer check` with the IDs and a verdict for each; eight verdicts, all `compatible`,
**no conflict**, so no question was filed under ADR-0008 §3.

Two are worth recording here rather than only in the question files:

- `Q-004` against `WI-0002/Q-003`. That answer put the cheap form on the description and `--on`
  on the date, with the reason *"the description is the bit I'll actually type, so make that the
  cheap one"*. This answer puts the cheap form on the month. It is not a conflict and not even a
  tension: the rule they stated is *the thing you type often gets the short form*, and they have
  now told us the month is a thing they type often. `--on` on `envel spend` is untouched.
- `Q-005` against `WI-0002/Q-005`. The watch round 2 filed with the question was exactly this,
  and it came out the way the watch anticipated — but in the direction that needed no
  reconciliation. They refused a future date on a spend because it writes something into the
  file, and they have now refused a future month on a summary, which writes nothing, for a
  different reason: not that it would corrupt the record but that they would misread the output.
  Two decisions, one habit, no contradiction, and `WI-0002/Q-005` is not being read as having
  covered this.

`scripts/lint-answers --item WI-0003` → exit 0.

## What round 2's answers left for round 3

- **Nothing on this item is waiting on the stakeholder.** All five questions ever filed here are
  `answered`.
- **The criteria round 2 deferred have been written**, by `answer-questions` rather than by round
  3: AC1, AC4 and AC5 amended in place and AC9 appended, so nothing renumbered. The reason is the
  one round 2 gave for deferring them — that writing them would have meant guessing two answers —
  and it no longer applies, because the answers are in and they are answers about exactly these
  criteria. Round 3's remaining job is the Definition of Ready itself, not the writing.
- **One round-1 assumption still has no criterion**: *a month the tool cannot read is refused,
  with a message, and nothing is printed*. `answer-questions` deliberately did not write it onto
  AC5 while it was there. No question asked it, it is `refine`'s own `[assumed]` decision under no
  delegation, and putting an assumption into a criterion is refinement's judgement taken in the
  open — the same line round 1 drew when it declined to derive a command surface.
- **Still `[assumed]` and still ours after round 2's answers**: the subcommand `summary`, an
  unreadable month refused, and *"moved in or out"* as one net figure. The future-month assumption
  is off this list for good; it is AC9, and AC9 is the stakeholder's.


---

## Round 3 — the agenda this round came from

Round 3 opened with both of round 2's questions answered and propagated, and with the hand-over
`answer-questions` left: *"Round 3's remaining job is the Definition of Ready itself, not the
writing."* That turned out to be true of the two criteria round 2 had deferred and false of the
checklist as a whole. `spec/dor-dod.md` §1 was walked against `item.md` as `answer-questions` left
it, criterion by criterion:

| # | verdict before this round | note |
|---|---------------------------|------|
| R1 | pass | frontmatter complete; `type`, `epic` and `priority` set |
| R2 | pass | `## Story` names the role, the capability and the outcome |
| R3 | pass | nine criteria, each labelled and a checkbox |
| R4 | **fail** | two criteria were not decidable. AC1 said `envel summary --month 2026-08` *"is not accepted"* without saying what a reader would observe; AC4 said a summary *"says so"* without naming a stream or an exit code. Both are round 1's wording, surviving two rounds because every round since was about something else. |
| R5 | pass | `## Out of scope` names five things, including the forward projection the stakeholder ruled out at `Q-005` |
| R6 | pass | no question on this item is open |
| R7 | **fail** | `depends-on` named `WI-0002` and not `WI-0004`. See below — this is the round's real finding. |
| R8 | pass | this file, `status: recorded`, with both rounds' answers verbatim |
| R9 | pass | one command, one report; nothing here is two items |
| R10 | **fail** | five combinations with no stated behaviour anywhere: an unreadable month, an option on a subcommand that takes none, a word beyond the month, the order of the rows, and how a figure is written |
| R11 | pass | no criterion counts anything this item may move; AC3's figures are the tool's own output, not a count of project artefacts |
| R12 | pass | every `[assumed]` entry says plainly that nothing licensed it and where a disagreement lands. No standing delegation exists on this project — the stakeholder has answered every question put to them by choosing an option, and has never said *"whatever you think"* about a category. |

**Nothing on this agenda was the stakeholder's**, so round 3 filed no question. Applying `refine`
step 3's test to each failure: R4's two gaps are the wording of criteria about behaviour they have
already chosen; R7 is a scheduling fact derived from their own answer at `Q-001`; and four of
R10's five combinations are the project's delivered conventions, with the fifth being round 1's
own assumption. Asking would have been asking them to confirm what they have already said.

## The R7 failure, and why it is the round's real finding

`depends-on` named `WI-0002` alone, and round 1's reasoning for that is quoted in `item.md`:
*"There is no such thing as 'the money spent from it during that month' until spending exists."*
The identical argument now applies to `WI-0004`, and round 1 could not have seen it — it recorded
the dependency **before** the stakeholder's answer at `WI-0003/Q-001` put a fourth, **moved**
column in the report.

It is not a theoretical gap. AC3's worked example is a required observation, not an illustration:
*"for an envelope with 50.00 carried in, nothing added, 20.00 spent and 30.00 moved in, the row
reads in 0.00, spent 20.00, moved 30.00, left 60.00."* There is no way to produce a non-zero
**moved** figure against a tool that has no `envel move`, so AC2's third figure and AC3's
reconciliation cannot be demonstrated at all until `WI-0004` ships. Delivering this item first
would mean a column that is always `0.00` and two criteria nobody could check.

So `depends-on: WI-0004` is recorded, with the consequence written into `item.md` `## Notes`
rather than left to be discovered: the orchestrator dispatches nothing on an item whose
`depends-on` is unfinished, so `WI-0003` does not move again until `WI-0004` is `done`. `WI-0004`
depends only on `WI-0001`, which is `done`, so there is no cycle. This reorders the board and it
is a mechanical consequence of a criterion, not a judgement about what matters more — the
stakeholder had already put moving money early on their own account: *"I will need it the moment
an envelope runs short, which is the same week I start using this"* [src: EP-001/Q-005].

## Decided here, and by what authority — round 3

Five criteria were added and two amended. Only one of the seven is a decision; the rest are
citations.

- **AC1, amended.** `--month` is now refused *as a wrong command line, per AC14* rather than
  merely *"not accepted"*. Not a decision — it is the stakeholder's answer at `Q-004` pointed at
  the criterion that says what a refusal looks like here.
- **AC4, amended.** The nothing-to-print case now prints to stdout and exits 0, cited to the
  delivered empty-listing behaviour [src: WI-0001 AC6 "Listing when no envelope has ever been
  created prints a line saying there are none"]. Not a decision: an empty month is a successful
  answer to a readable question, and the project already treats an empty listing that way.
- **AC10 — row ordering.** **Not** an assumption: the project's delivered convention
  [src: WI-0001 AC3 "the lines ordered alphabetically by name ignoring capitalisation"]. The
  criterion also records why there is no tie to break, citing `WI-0001` AC11.
- **AC11 — how a figure is written.** **Not** an assumption: two decimal places and no currency
  symbol are delivered [src: WI-0001 AC8 "An amount is written with at most two decimal places"]
  [src: WI-0001 AC17 "No amount the tool prints carries a currency symbol"]. It is written down
  because AC3's worked example is in that form and a reader should not have to infer it.
- **AC12 — a month the tool cannot read.** `[assumed]`, **under no delegation**. This is round 1's
  own decision, taken under no delegation then and unchanged since, finally reaching a criterion:
  *"a month the tool cannot read is refused, with a message, and nothing printed."* Round 3 made
  it decidable by naming the forms — `2026-8`, `08-2026`, `august`, `2026-13`, `2026-08-01` — and
  the accepted range `01`–`12`, which is the part that was never written down. A disagreement
  lands on AC12 alone and costs one parser rule. `answer-questions` deliberately declined to write
  this one, twice, on the grounds that putting an assumption into a criterion is refinement's
  judgement taken in the open; this is refinement taking it.
- **AC13 — streams and exit codes.** **Not** an assumption: the project's recorded convention
  [src: docs/architecture/overview.md] and the delivered rule [src: WI-0001 AC16 "Every refusal
  this item specifies writes its message to stderr and exits non-zero"]. Written case by case
  against the criteria that name them, in the shape `WI-0002` AC13 already uses.
- **AC14 — a wrong command line.** **Not** an assumption: the delivered treatment
  [src: WI-0001 AC15 "A subcommand given the wrong number of arguments prints to stderr a usage
  message for that subcommand and exits non-zero"] [src: WI-0002 AC14 "`envel spend` with no
  arguments"]. It is what makes AC1's *"`--month` is refused"* observable, and it is where the
  extra-word case lives.

## Left deliberately unconstrained by round 3

Recorded in `item.md` `## Notes` so that nobody mistakes the silence for a decision, each
`[assumed]` under **no delegation**:

- which message is printed when more than one refusal applies at once — `envel summary 2027-13` is
  both unreadable and in the future, and every criterion involved is satisfied by any of the
  messages;
- the wording of every message, exactly as `WI-0001` and `WI-0002` left it;
- whether the four figures carry a header line. AC2 fixes what they are and AC6 fixes that nothing
  else is on the page; neither says whether there is a heading.

## Cross-answer check — round 3

`Checked against: none — this execution consumed no human answer.` Round 3 asked nothing and
recorded no reply; every answer this item holds was consumed by `answer-questions` in earlier
executions, and each carries its own `## Cross-answer check` with its verdicts. Round 3 re-read
`Q-001` through `Q-005` while writing the criteria and found nothing it had to reconcile: AC10 to
AC14 are conventions and one prior assumption, and none of them touches a sentence the stakeholder
wrote.

`scripts/lint-answers --item WI-0003` → exit 0.

## What round 3 leaves

- **The item is Ready.** All twelve Definition-of-Ready criteria pass, none by override.
- **It is not runnable yet**, and that is R7 working rather than failing: `WI-0004` must be `done`
  first. The next thing the orchestrator can do on this epic is `WI-0004`.
- **Three assumptions are still ours and none has been shown to the stakeholder**: the subcommand
  name `summary`, the unreadable-month rule at AC12, and the net **moved** figure at AC2 and AC3.
  Each names the criterion a disagreement lands on. `review-close` names assumptions spent under a
  delegation in the sign-off; these were spent under none, which is worth saying out loud here
  because it means the only route to the stakeholder for them is somebody choosing to raise them.
- **`plan` has four things routed to it**, three from earlier rounds and one from this one: how a
  month's figures are computed from the stored entries; how an end-of-month balance is derived for
  a month that is not the current one; what the summary does with an entry naming an envelope that
  is no longer present; and the order in which the refusals of AC9, AC12 and AC14 are checked.
