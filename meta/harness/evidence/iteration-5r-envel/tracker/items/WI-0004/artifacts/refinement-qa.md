---
status: recorded
---

# Refinement Q&A — WI-0004 Move money between envelopes

`refine` rounds 1 and 2. One question was put to the stakeholder, in round 1; everything else on
this item was either already answered by something they had said, or decided here with its
authority named. This file is the record of which was which. The one question has since been
answered and propagated — `## Answers — round 1` below carries the reply verbatim — so
`status: recorded` describes a conversation that has happened rather than one that was only filed.
**Round 2 put no question to anybody**, and `## Round 2` at the end of this file says why that is
the honest outcome rather than a corner cut.

## Round 1 — the agenda this round came from

`WI-0004` was filed by `answer-questions` on 2026-09-11, out of the stakeholder's answer to
`EP-001/Q-005`. It had never been refined. The Definition of Ready was walked against `item.md`
as that skill left it:

| # | verdict before this round | note |
|---|---------------------------|------|
| R1 | pass | frontmatter complete; `type`, `epic`, `priority` and `arose-from` all set |
| R2 | pass | `## Story` names the role, the capability and the outcome, and the outcome is the stakeholder's own route out of a refused overspend |
| R3 | pass | five criteria, labelled and checkboxed |
| R4 | **fail** | AC1 names no command surface — *"There is an `envel` command that moves a given amount"* — and five things the tool will certainly do have no criterion at all: what a successful move prints, which stream anything goes to, a zero or negative amount, a move to and from the same envelope, and the wrong number of words on the line |
| R5 | pass, but one entry was self-contradictory | `## Out of scope` named three things. The first deferred correcting a move to `WI-0005` *"which the stakeholder scoped to spends"* — deferring to an item that does not cover it. Rewritten this round; see below |
| R6 | pass before this round | no questions existed. This round files one blocking question, so R6 fails **by this round's own act**, and that is what suspends the item |
| R7 | **fail** | `depends-on` was empty while `## Notes` said the dependency on `WI-0001` was real and was being withheld on purpose. Recorded this round |
| R8 | **fail** | this file did not exist |
| R9 | pass | one coherent change: one subcommand that reads the store, moves an amount and writes it back |
| R10 | **fail** | a move's date, a move's description, and the combinations either would create had no stated behaviour anywhere |
| R11 | pass | no criterion counts anything |
| R12 | n/a before this round | no assumption had been taken on this item yet. Four are taken now, every one under **no** delegation and saying so |

## What the draft asked `refine` to ask, and what happened to each

The draft named three open points. Only one of them survived contact with the record.

1. **"Whether a move shows up in the monthly summary as money in and money out, or is excluded
   from it."** — **Already answered; not re-asked.** The draft was written on 2026-09-11 at
   02:12Z, and `WI-0003/Q-001` put this very question to the stakeholder later the same day. They
   answered option **C**:

   > [human] C. "Spent" has to mean money that left the house, so moves don't belong in it — but
   > I won't use a report whose rows don't add up… A column of zeros costs me nothing; a number I
   > can't account for costs me an evening.

   `WI-0003` AC2, AC3 and AC6 carry it. Re-asking would have been the fastest way to lose their
   engagement. What it leaves behind for this item is a pair of **constraints**, recorded under
   `## Routed to plan` rather than put to anybody: a move has to be recorded so that `WI-0003`
   can tell it from a spend and from income, and so that one net figure per envelope per month
   can be computed from it.

2. **"Whether a move carries a date and a description, by symmetry with `WI-0002/Q-001` and
   `WI-0002/Q-002`."** — **Split, and the two halves went opposite ways.**
   - The **date** is `Q-001`, below. It is the one thing here that cannot be derived.
   - The **description** is decided, `[assumed]`, under **no delegation**; see below.

   Splitting it was not a formality. Folding two decisions into one question is how a question
   gets half-answered and half-recorded (F-027), and here the two halves do not even have the
   same kind of answer: one turns on a fact about their habits that only they hold, and the other
   turns on whether anything in this project would ever display the field.

3. **"Whether moving zero is refused, by symmetry with `WI-0001/Q-003`."** — **Decided**,
   `[assumed]`, under **no delegation**; see below.

## Questions put to the stakeholder — round 1

One question. It is framed as *question 1 of 1* and says so, and it names the two things this
round decided instead of asking, so they can see what was spent as well as what was asked.

| # | question | why it is theirs |
|---|----------|------------------|
| `Q-001` | Is a move datable the way a spend is — `--on YYYY-MM-DD`, today unless you say otherwise — or always dated when it is typed, the way income is? | **They have answered this shape of question twice and given opposite answers.** `WI-0002/Q-001`: a spend can be back-dated, because *"I will not always sit down with the receipts on the day, and a Saturday shop landing in the wrong month would make the monthly summary wrong."* `WI-0003/Q-003`: income cannot, because *"I put income in when it arrives — that's the one thing I'm never late on."* Both reasons are about their own habits with a particular kind of event. A move is a third kind, and neither answer reaches it; choosing which precedent applies would be us deciding which of their habits this one resembles. It is not cosmetic either: the summary's fourth column is per month [src: WI-0003 AC2 "the money moved into or out of it during that month"], so the date decides which report a move appears in, and under the no-date options a move in the wrong month cannot be corrected at all, because `WI-0005` is scoped to spends. |

## Decided here, and by what authority — round 1

Four decisions, plus two things that are conventions rather than decisions. **None of them is
taken under a standing delegation**: the stakeholder has never said *"whatever you think"* about
any category in this engagement, so every `[assumed]` below says so in terms and names where a
disagreement about it lands (R12).

- **The subcommand is `move`, as `envel move <from> <to> <amount>`.** `[assumed]`

  **Under no delegation.** Nothing the stakeholder has said names it. Every word below `envel` in
  this tool is ours — `new`, `add`, `list`, `spend` and `summary`, five of them, none ever put to
  them — and asking about the sixth would be inconsistent rather than careful. The **order** is
  the one every delivered subcommand already uses, the envelope's name before the amount
  [src: WI-0001 AC2 "`envel add <name> <amount>` adds `<amount>` of income to the envelope called"]
  [src: WI-0002 AC1 "the envelope first and the amount second, the same order as"], and it is the
  order the story reads in: move *from* here *to* there, this much. A disagreement lands on AC1
  and costs swapping two arguments.

  The real risk in this one is getting the pair backwards and moving money the wrong way, which
  is worse than a refusal because it succeeds. It is mitigated in the criteria rather than by a
  question: round 2 will require the success line to name which envelope the money left and which
  it arrived in, so a reversed pair is visible in the same breath as the mistake, and the repair
  is running the same command with the names swapped.

- **A move of zero, or of a negative amount, is refused with a message and nothing is moved.**
  `[assumed]`

  **Under no delegation.** The stakeholder set this rule once, for income, at `WI-0001/Q-003`.
  They were not asked about spending, so `WI-0002` AC6 took it on the same footing and it has
  since shipped and been verified
  [src: WI-0002 AC6 "Recording a spend of `0`, or of a negative amount, is refused"]. Assuming it
  a third time for a move is consistent with the two instances they can already see, and asking
  about the third instance of a rule they stated once would tell them their answer was not heard.
  A disagreement lands on one criterion and costs one comparison.

- **A move to and from the same envelope is refused**, with a message naming the envelope.
  `[assumed]`

  **Under no delegation.** Nobody has raised it. It moves nothing, so accepting it would write an
  entry that changes no balance, and it is far more likely to be a mistyped name than an
  intention. A disagreement lands on one criterion.

- **A move carries no description.** `[assumed]`

  **Under no delegation**, and this is the one of the four worth arguing with, so here is the
  whole of the reasoning. Nothing in this project would ever show a move's description back:
  `WI-0006` is scoped to *"the spends recorded against an envelope"* [src: WI-0006], and the
  stakeholder ruled the individual entries out of the monthly summary at `EP-001/Q-003`. It would
  be a note that can be written and never read.

  It is deliberately **not** read as contradicting `WI-0002/Q-002`, where they asked for an
  optional description on a spend — *"I'll put one on the ones I might query later and skip it on
  the weekly shop"*. That answer is about spends, and the reason inside it presupposes something
  that queries, which exists for spends and does not for moves. Stretching it to cover moves
  would be the same move round 1 of `WI-0003` refused to make when it declined to read
  `WI-0002/Q-001` as covering income.

  Because this is a scope decision rather than a detail, it is recorded in the item's
  `## Out of scope` as well as in `## Notes`, so it is visible on the board rather than buried in
  a Q&A file. `Q-001` also names it to the stakeholder in as many words, so the decision reaches
  the person it was taken on behalf of in the same breath as the question. A disagreement lands on
  AC1 and costs one optional word on the line.

- **Success on stdout with exit 0, every refusal on stderr with a non-zero exit, and a usage
  message for the subcommand when the wrong number of words is given.** **Not** assumptions: they
  are the project's recorded conventions [src: docs/architecture/overview.md] and the stakeholder's
  own criteria on two delivered items
  [src: WI-0001 AC16 "Every refusal this item specifies writes its message to stderr and exits non-zero"]
  [src: WI-0002 AC14 "`envel spend` with no arguments"]. Round 2 writes them into the criteria by
  citation rather than restating them as new decisions.

- **The wording of every message stays deliberately unconstrained**, exactly as `WI-0001` and
  `WI-0002` left it. The criteria will say what a message must contain — the envelope's name,
  what is left in it — and never how it reads.

## The `## Out of scope` entry that contradicted itself

The draft's first exclusion read:

> Correcting or deleting a move once it has been recorded — that is the subject of `WI-0005`,
> which the stakeholder scoped to spends.

It defers to an item that it says in the same sentence does not cover this. As the epic stands
there is no command anywhere that repairs a move, and that is a real gap rather than a wording
slip.

Round 1 leaves the gap and rewrites the sentence to say so honestly, rather than widening
`WI-0005` or filing a new item. The reason is that a move is **self-reversing** — a wrong
`envel move a b 20` is undone by `envel move b a 20`, which needs no new command — and the only
place a move is ever displayed is `WI-0003`'s fourth figure, which is a **net** number
[src: WI-0003 AC2 "The moved figure is one net number, positive when more arrived than left"], so
a mistake and its reversal cancel there. What does **not** cancel is the month each of the two
lands in, and that is precisely what `Q-001` is about — which is why the cost is stated inside
`Q-001`'s options B and C rather than left for the stakeholder to discover.

## Routed to `plan`, not to the stakeholder

Recorded in `WI-0004` `## Notes` for `plan` to settle under its own preference order, because the
answer would be the same whoever the stakeholder was:

- whether a move is stored as one entry or as two, and how `WI-0003` tells a move from a spend
  and from income when it computes the fourth column. This is a **constraint** rather than an
  open choice in one respect: whatever the shape, `WI-0003` AC2 and AC3 have to be satisfiable
  from it, and that comes from the stakeholder's answer at `WI-0003/Q-001`;
- in what order the refusals are checked when more than one applies at once — the same question
  `WI-0002` routed to `plan`, which settled it by putting the envelope check first so that a
  message naming the envelope is always available;
- what a move does with a stored entry naming an envelope that is no longer present — the same
  question `WI-0002` and `WI-0003` both routed to `plan`, and it should get the same answer.

## Cross-answer check — round 1

No answer was consumed by this execution — round 1 asks, it does not propagate — so there is
nothing to check a reply against yet. `Checked against: none`, because this execution consumed no
human answer.

`Q-001` carries its own `## Cross-answer check` filed **with** the question, naming
`WI-0002/Q-001`, `WI-0003/Q-003`, `WI-0003/Q-001`, `EP-001/Q-002` and `EP-001/Q-005`.

The pair to watch is `WI-0002/Q-001` against `WI-0003/Q-003`, and it is unusual: the two prior
answers already point opposite ways, and **whichever way the reply goes one of them will look
like the precedent and the other will not**. Neither is being overturned by either outcome — a
move is a third kind of event — and the question says so explicitly so that the reply cannot be
recorded as a reversal of something they said about spends or about income. If the stakeholder
themselves frames their reply as changing one of those earlier answers, that is a conflict under
ADR-0008 §3 and it goes back to them quoting both, rather than being reconciled here.

`scripts/lint-answers --item WI-0004` → exit 0.

## What round 1 has not settled

- `Q-001` was blocking and with the stakeholder; it is now `answered` and propagated —
  see `## Answers — round 1` below.
- **No acceptance criterion was rewritten**, deliberately. AC1 is downstream of `Q-001` — whether
  the line carries `--on` is exactly what is being asked — and the five criteria round 1 could
  already write (the success output, the streams and exit codes, zero and negative, a move to the
  same envelope, the wrong number of words) would have to be numbered around it. Round 2 writes
  them once, from the reply, rather than renumbering the list twice. The renumbering obligation
  was discharged rather than assumed: `grep -rn 'WI-0004 AC' tracker docs` returns one line, and
  it is `item.md` quoting this very command inside backticks — a mention rather than a citation
  (`spec/doc-header.md` §4a). Nothing anywhere cites this item's criteria by number.
- What this round *did* change in the item: `depends-on: WI-0001` in the frontmatter, which is
  R7; the self-contradictory `## Out of scope` entry, plus a second entry naming the description
  decision; and `## Notes`.
- Round 2 therefore has a bounded job: write AC1 from `Q-001`'s reply, append the five criteria
  listed above, and walk the Definition of Ready with R4, R6, R8 and R10 closed.


## Answers — round 1

The reply is the stakeholder's own words, copied from the `## Answer` section of
`questions/Q-001.md`, and marked `human`. `answer-questions` consumed it on 2026-09-11 and
propagated it into `WI-0004`'s criteria; the question's `## Consequences` section names the files.

- **Q-001 — whether a move can be back-dated.** `human`, option A:

  > A — datable, same as a spend. You've put your finger on it: I move the money because of a shop
  > I'm typing in late, so the move is late too. The thing that settles it for me is that I can fix
  > a spend afterwards and I can't fix a move, so I need to be able to get it right when I type it.

  Propagated to `WI-0004` AC1, which now carries the optional `--on <date>` and says the move is
  held against the date given rather than the day it was typed, and to three new criteria — AC6
  (today by default), AC7 (`YYYY-MM-DD` and nothing else) and AC8 (a future date refused). All
  three are the delivered `envel spend` rules cited to `WI-0002` AC9, AC11 and AC12 rather than
  decided again here: option A said *"all identical to `envel spend`"*, and that is what the
  stakeholder chose.

  The reply also gave a reason round 1 had not anticipated, and it is recorded in `WI-0004`
  `## Notes` because it is a fact about this project rather than about their habits: a move cannot
  be corrected afterwards, so the date has to be right when it is typed. `## Out of scope`'s
  self-reversing-move entry was amended to say so — a reversal cancels the amounts, but only a
  second move dated into the right month moves a figure out of the wrong one, and `--on` is what
  makes that possible.

## Cross-answer check — round 1, on the reply

Written by `answer-questions` on consuming the reply. `questions/Q-001.md` carries its own
`## Cross-answer check` with the IDs and a verdict for each; five verdicts, all `compatible`,
**no conflict**, so no question was filed under ADR-0008 §3.

The pair round 1 flagged came out the way it anticipated. `WI-0002/Q-001` (a spend can be
back-dated) is the answer this reply follows, and `WI-0003/Q-003` (income cannot) is the one it
does not — and **neither is overturned**, because a move is a third kind of event and the question
said so before the reply came. The stakeholder did not frame their reply as changing either
earlier answer, and nothing about `envel add` or `envel spend` moves as a result. `WI-0003` AC8
still says income is dated when it is typed.

`scripts/lint-answers --item WI-0004` → exit 0.

## What round 1's answer left for round 2

- **Nothing on this item is waiting on the stakeholder.** The only question ever filed here is
  `answered`.
- **AC1 is written, and so are the three criteria the reply itself specified** — AC6, AC7 and AC8.
  Round 1's stated reason for deferring AC1 was that whether the line carries `--on` was exactly
  what was being asked; the reply answers it, so the reason has expired.
- **The five criteria round 1 listed for round 2 are still round 2's**: the success output, the
  streams and exit codes, zero and negative, a move to and from the same envelope, and the wrong
  number of words. Every one of them is `refine`'s own `[assumed]` decision or a delivered
  convention, and none was asked in `Q-001`. `answer-questions` deliberately did not write them —
  putting an assumption into a criterion is refinement's judgement taken in the open, not a
  propagation, and it is the same line drawn on `WI-0003` this round.
- **Round 2's job is therefore the five criteria and the Definition of Ready** — R4, R6, R8 and
  R10 walked again with the date question closed.

---

## Round 2 — the agenda, and why it asked nothing

Round 1 left round 2 a bounded job, in its own words: *"write AC1 from `Q-001`'s reply, append the
five criteria listed above, and walk the Definition of Ready with R4, R6, R8 and R10 closed."*
`answer-questions` had already written AC1 and the three date criteria when it propagated the
reply, so what was left was the five criteria and the checklist.

**No question was put to the stakeholder this round, and that is a decision rather than an
omission.** Every one of the five is either a decision round 1 had already taken and recorded with
its authority named, or a convention this project has already delivered twice. Applying step 3's
test to each in turn:

| the criterion round 2 wrote | who it belongs to, and why |
|---|---|
| AC9 — what a successful move prints | **Ours.** Round 1 decided the success line must name both envelopes, as the mitigation for getting the argument pair backwards. The *wording* stays unconstrained, exactly as `WI-0001` and `WI-0002` left theirs. No product stake: the stakeholder's answers say nothing about output wording anywhere in this engagement |
| AC10 — zero and a negative amount | **Already answered, for the third time.** They set this rule for income at `WI-0001/Q-003`; `WI-0002` AC6 took it for a spend and has shipped and been verified. Asking about the third instance of a rule they stated once would tell them their answer was not heard (step 3) |
| AC11 — a move to and from the same envelope | **Ours.** Round 1 decided it. It moves nothing, so the only thing at stake is whether a mistyped name is refused or silently written as a no-op |
| AC12 — streams and exit codes | **Not a decision at all.** It is the project's recorded convention and the stakeholder's own criteria on two delivered items, written in by citation |
| AC13 — the wrong number of words | **Not a decision at all**, for the same reason — `WI-0001` AC15 already governs it for every subcommand |

**What round 2 did *not* do was invent a question to have one.** The temptation was real: this is
the last point at which asking is cheap, and AC9 and AC11 are decisions taken on the stakeholder's
behalf. But round 1 had already put the whole of that list to them inside `Q-001` — the question
names the two things round 1 decided instead of asking, in as many words — and their reply engaged
with the date and said nothing about the rest. Asking again, in a second round trip, about
decisions they had already been shown and had not objected to, is the failure step 3 names from the
other side.

### The two `[assumed]` decisions that round 2 turned into criteria

Both were taken in round 1 and are reproduced here only so that the criteria they justify have
their authority beside them. **Neither is taken under a standing delegation**, because the
stakeholder has never granted one in this engagement — there is no *"whatever you think is best"*
anywhere in the record — so each says so and names where a disagreement lands (R12).

- **AC9 — the success line names both envelopes and both new amounts.** `[assumed]`, under **no
  delegation**. A disagreement lands on AC9 alone and costs one line of output.
- **AC11 — a move to and from the same envelope is refused.** `[assumed]`, under **no
  delegation**. A disagreement lands on AC11 alone and costs one comparison.

AC10 is `[assumed]` too, and is round 1's third-instance argument rather than a fresh decision; it
is recorded above and in `## Decided here, and by what authority — round 1`.

### The one thing round 2 changed that nobody asked for

**AC1 and AC6 gained an observation route, in place.** They said what a move's date *means* and not
where anybody would look to see it, and nothing this item delivers prints a move's date back. The
first thing that would is `WI-0003`'s summary, which is not delivered and which this item does not
depend on — so a person with a terminal could not have decided either criterion. The repair is the
one the delivered item already uses for exactly this situation: a store of its own under
`ENVEL_FILE` [src: ADR-0003], read directly [src: WI-0002 AC8 "Observed in a store of its own"].

This is an R4 repair, not a change of meaning, and it is worth being explicit that it is
`refine`'s own judgement: `answer-questions` propagated the stakeholder's choice faithfully and
correctly, and propagation is not the same job as making a criterion decidable. Nothing about what
the stakeholder chose has been altered.

## Cross-answer check — round 2

**`Checked against: none`** — and the reason matters, because the result looks the same as an
omission. Round 2 consumed **no** human answer: the only question ever filed on this item is
`Q-001`, `answer-questions` consumed it on 2026-09-11, and its own `## Cross-answer check` carries
five verdicts, all `compatible`. Round 2 wrote criteria out of decisions that were already in the
record with their authority named, so there is no new statement of the stakeholder's to hold
against their prior ones.

One thing was nevertheless read across, because R10 asked for it and the answer could have gone
badly: **AC3's balance check against the back-dating the reply introduced.** A move is now datable,
and AC3 refuses a move larger than what is *currently* in the source envelope. Those could have
contradicted each other — a back-dated move might have been expected to check the balance as it
stood on that date. They do not, and the reason is that the delivered spend behaves the same way
[src: WI-0002 AC5 "Recording a spend larger than the amount currently in the envelope is
refused"], and the stakeholder's reply to `Q-001` asked for a move to be *"datable, same as a
spend"*. Reading it any other way would be us extending their answer past what it says. It is
recorded in `## Notes` rather than left implicit in AC3's one word.

`scripts/lint-answers --item WI-0004` → exit 0.

## Definition of Ready — round 2's walk

| # | verdict | evidence |
|---|---------|----------|
| R1 | pass | `validate-workspace` → exit 0; `type`, `epic`, `priority` and `arose-from` all set |
| R2 | pass | `## Story` names the role (a person budgeting their own money at a terminal), the capability (move an amount from one envelope to another) and the outcome (*"so that when an envelope runs short I can take the money from somewhere I have decided it can come from"*) |
| R3 | pass | thirteen criteria, each labelled `AC<n>` and checkboxed; `validate-workspace` → exit 0 |
| R4 | pass — **was failing at the start of round 1** | Every criterion now names a command and an observable outcome. The two that did not are repaired: AC1 and AC6 said what a date means without saying where it is seen, and now name the store under `ENVEL_FILE`. No criterion contains an unmeasurable adjective; the message *wording* is deliberately unconstrained and each criterion says what a message must **contain** instead |
| R5 | pass | `## Out of scope` names four things, and the first — that nothing anywhere repairs a recorded move — is something a reader would reasonably assume `WI-0005` covered, which is exactly why round 1 rewrote it to say so |
| R6 | pass — **was failing during round 1 by round 1's own act** | `Q-001` is `answered`; no question on this item is open. `validate-workspace` → exit 0 |
| R7 | pass — **was failing at the start of round 1** | `depends-on: WI-0001`, recorded in round 1, and `WI-0001` is `done` |
| R8 | pass — **was failing at the start of round 1** | this file exists and declares `status: recorded`, and the conversation it records has happened |
| R9 | pass | one coherent change: one subcommand that reads the store, validates, writes two amounts back, and prints a line |
| R10 | pass — **was failing at the start of round 1** | The behaviours are one flag and seven refusals. `## Notes` `### Combinations` disposes of every combination: `--on` with each refusal is **deliberately unconstrained** and routed to `plan` with who left it so; `--on` with the wrong number of words is AC13; `--on` malformed at the parser is **deliberately unconstrained** with AC12 still binding its stream and exit code; how an amount is written is delivered and cited, not restated; and the back-dating-versus-balance combination is stated outright |
| R11 | pass | No criterion counts anything. AC12 names the criteria it covers by ID — AC3, AC4, AC7, AC8, AC10, AC11, AC13 and AC1, AC2, AC6, AC9 — rather than saying *"every refusal above"* or a number of them, and it says the assessment is a read of their text with the suite as evidence rather than as definition (step 6a) |
| R12 | pass | Four `[assumed]` decisions stand on this item — the subcommand name and argument order, zero and negative, the same-envelope refusal, and no description — plus AC9's success line. **Every one says `under no delegation`** and names where a disagreement lands. There is no standing delegation in this engagement to spend: `lint-answers --item WI-0004` reports `0 delegation(s) spent` |

**No override.** Every criterion passes on its own terms, so there is nothing for the stakeholder
to override and no `## Override` section.

## How each criterion is decided — round 2

The `criteria-are-decidable` gate asks for the command or the artifact, and the verdict that
follows, for every criterion. Throughout, *the store* means a store of this item's own —
`ENVEL_FILE` pointed at a path that does not exist [src: ADR-0003] — so that nothing under test
touches a real budget, and *the listing* means `envel list`
[src: WI-0001 AC3 "one line per envelope, each line containing that envelope's name and
      the amount currently in it"].

| AC | what to run or inspect | verdict |
|----|------------------------|---------|
| AC1 | in the store: `envel new groceries`, `envel new fun`, `envel add groceries 100`, then `envel move groceries fun 20 --on 2026-08-28`; then open the store file | **pass** if the command is accepted and the move the store holds carries `2026-08-28`; **fail** if it is refused, or the stored move carries the day the command was run |
| AC2 | the listing, before and after the AC1 move | **pass** if `groceries` fell by exactly 20.00, `fun` rose by exactly 20.00, and every other envelope's amount is byte-identical between the two listings; **fail** otherwise |
| AC3 | in the store of AC1: `envel move groceries fun 1000` against a `groceries` holding less | **pass** if it exits non-zero, the message contains `groceries` and the amount left in it, and the listing is unchanged; **fail** if the move succeeds or the message omits either |
| AC4 | `envel move nosuch fun 10` and `envel move groceries nosuch 10` | **pass** if each is refused with a message containing the missing name and the listing is unchanged; **fail** if either succeeds, or the message names the wrong envelope |
| AC5 | the AC1 move in one invocation; `envel list` in a separate later invocation of the tool | **pass** if the later listing shows both amounts as the move left them; **fail** if the store is only in memory |
| AC6 | in the store: one `envel move groceries fun 1` with no `--on` and one with `--on 2020-01-01`; open the store file | **pass** if the first carries today's date and the second carries `2020-01-01`; **fail** otherwise |
| AC7 | `envel move groceries fun 1 --on` each of `28/8`, `08-28`, `yesterday`, and once with `2026-08-28` | **pass** if the three malformed dates are each refused with a message and the listing is unchanged, and the well-formed one is accepted; **fail** if any malformed form is accepted or a refusal moves money |
| AC8 | `envel move groceries fun 1 --on <tomorrow>`, then the same with today's date | **pass** if tomorrow is refused with a message saying the date is in the future and the listing is unchanged, and today is accepted; **fail** otherwise |
| AC9 | stdout of the AC1 move | **pass** if the line contains `groceries`, `fun`, the amount moved, and the amount now in each of the two, and the command exits 0; **fail** if any of the four is absent |
| AC10 | `envel move groceries fun 0` and `envel move groceries fun -5` | **pass** if each is refused with a message and the listing is unchanged; **fail** if either is recorded |
| AC11 | `envel move groceries groceries 10` and `envel move groceries Groceries 10` | **pass** if each is refused with a message containing the envelope's name and the listing is unchanged; **fail** if either is accepted, including as a no-op that writes an entry |
| AC12 | for each criterion AC12 names: capture stdout, stderr and the exit code of the case that criterion specifies | **pass** if every refusal wrote to stderr and exited non-zero and every success wrote to stdout and exited 0, **and** every named criterion had an executable case; **fail** if any stream or code is wrong. Where a named criterion has no case that exercises both, that is neither pass nor fail until the case is added or the criterion is waived by name, in writing |
| AC13 | `envel move`, `envel move groceries`, `envel move groceries fun`, `envel move groceries fun 20 extra` | **pass** if each prints a usage message for `move` to stderr, exits non-zero, and leaves the listing unchanged; **fail** if any is accepted — the fourth in particular, which would mean a bare fourth word was being read as a description |
