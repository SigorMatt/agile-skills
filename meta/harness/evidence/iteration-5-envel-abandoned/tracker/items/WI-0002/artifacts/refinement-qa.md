---
status: recorded
---

# Refinement Q&A — WI-0002

`status: recorded`. Round 1's three questions were filed on 2026-09-10T14:39:19Z and the
stakeholder answered all three; `answer-questions` propagated the answers into `../item.md` on
2026-09-10T15:03:57Z, and this round records the exchange verbatim and closes the file. Round 2
asked nothing further: the three answers settled every decision that was the stakeholder's, and
what remains open is `plan`'s.

Everything below is what was actually said, in order. Nothing here is attributed to the
stakeholder that they did not say, and no hesitant answer has been tidied into a confident one.

## Round 1 — the questions put to the stakeholder, and their answers

Three questions, all blocking, all addressed to the human, filed as one ask
(`WI-0002/Q-001`…`Q-003`). Each was a decision that changes what the tool is for them.

**Q1 — where do you see what is left: does `envel list` show the balances, or does a separate
command?** (`WI-0002/Q-001`)

> `[human]` — "A — `envel list` shows the balances. The number is the whole reason I open the
> tool; I'm not going to type a second command to see it. Change the criteria on the earlier item,
> that's fine by me — I'm asking for it. I don't need a flag to hide the balances."

Asked because their own sentence — "record spending against an envelope, and see what's left in
each" (`IDEA.md`) — says they want to see it and not where, and because one of the two answers
**changes behaviour WI-0001 already delivered and verified**. They chose that one, in terms that
leave no doubt it was theirs to ask for: "I'm asking for it."

Three things followed, and each is on the item. AC15 and AC16 state the new behaviour. Six of
`WI-0001`'s eleven criteria — AC2, AC3, AC5, AC7, AC8 and AC11 — are marked `superseded` on that
item rather than rewritten, because it is `done` and a ticked box records an observation that was
genuinely made; AC12 waives those six by name and AC19 re-checks their substance against the new
line shape. The question told them "two of its acceptance criteria"; reading all eleven against
their answer gives six, and `WI-0001` AC4 — ordering and byte-stability — is not one of them. The
correction is recorded in `answer-questions`' journal entry, in `WI-0001`'s `## Notes` and in
AC12. It was not put back to them, because their authorisation was unqualified.

**Q2 — what may an amount look like when you type it, and what happens to `12.345`?**
(`WI-0002/Q-002`)

> `[human]` — "C. Take a `£` if I type one and ignore it, and refuse anything with more than two
> decimals rather than rounding it — same reason as the overspend, I don't want the tool storing a
> number I didn't type. It's one currency, pounds and pence, and that's not changing."

Asked because every command this item adds takes an amount and nothing fixed its shape, and
because one half of it is about their money rather than about parsing: rounding `12.345` silently
stores a number they did not type. They made the connection to `EP-001/Q-003` themselves.

AC17 and AC18 state it. Their answer settled the **input** and left the **output** open, and the
criteria could not be written without the output: `340`, `340.0` and `340.00` were three answers
to "the balance is 340". `answer-questions` decided that as `ADR-0006` — every printed amount and
balance carries exactly two decimal places — rather than asking, on the grounds that they had
already said pounds and pence and that digit count is a consequence of that sentence.

**Q3 — what does a successful `income` or `spend` print back?** (`WI-0002/Q-003`)

> `[human]` — "C — tell me what you recorded: the envelope, the amount, the date it went under,
> and what's left. One line, not three. Catching a fat-fingered amount or a wrong date while I'm
> still looking at the screen is worth the extra output."

Asked because the two mistakes this tool cannot otherwise catch — the right envelope with the
wrong amount, and the right amount with the wrong `--date` — are only visible if something is
printed at the moment of recording.

AC13 states the four facts the line carries and AC14 checks the default date against `date +%F`.
Their answer closed a gap round 1 had recorded as open: refinement had written into the item's
`## Notes` that AC7's "defaults to today" half was not observable through any command this item
delivers. It is now, and the note says so.

## Round 2 — nothing asked

No question was put to the stakeholder in this round. The routing test in step 3 was applied to
what is still open on this item and none of it is theirs: how a transaction is stored, the exact
wording of each message, and which refusal wins when two apply are all implementation decisions
whose answer would be the same whoever the stakeholder was, and they are in the item's `## Notes`
for `plan`. Inventing a question to fill a round would have cost them a round trip for nothing.

## Decided without the stakeholder, and on what authority

Each was checked against the routing test in `refine`'s step 3 before it was taken: is it product
stake, is it already answered, is it covered by a standing delegation, or is it a design decision
whose answer would be the same whoever the stakeholder was.

**There is still no standing delegation anywhere in this engagement.** It was checked again this
round against all nine recorded human answers, not assumed from round 1. The nearest thing,
`WI-0001/Q-001`'s "I'm not going to spend a round renaming things", is about the tool's own name
and is not read here as a licence over every word that follows it. So no `**Under delegation:**`
line can honestly be written for any entry below, and R12's other form applies to each: nothing
licensed it, and the entry says where a disagreement lands.

**A1 — the sub-command words are `income` and `spend`.** `[assumed]`

Nothing licensed this. The basis is the stakeholder's own vocabulary: they wrote "put income into
them, record spending against an envelope" (`IDEA.md`), and these are those two words. If they
want different words, that is a change to AC1 and AC2 and lands on this item as a send-back to
`refine`. Round 1's three questions quoted commands like `envel spend groceries 12.50` at them and
they answered all three without objecting to the words, which is not a confirmation and is worth
recording as the exposure it closes.

**A2 — the date is given as `--date YYYY-MM-DD`.** `[assumed]`

Nothing licensed this either. `EP-001/Q-004` settled that a date is optional and defaults to today
and says nothing about its form. Taken rather than asked because the alternatives are worse for
the stakeholder rather than merely different: `10/9` is ambiguous between two readings that are
both plausible for a person in the UK typing about the same fortnight, and a criterion written on
an ambiguous format is not decidable at a terminal (R4). `YYYY-MM-DD` sorts, is unambiguous, and
is what the monthly summary in WI-0003 will group on. A disagreement lands as a change to AC7.
Their answer to Q3 has the tool print the date back, so the form is now something they will see on
every recording rather than something they meet only in a manual — which makes a disagreement
about it cheap and early.

**A3 — a recording command against a name that is not an envelope is refused, and never creates
the envelope.** `[assumed]`, written into AC4.

The record is close to explicit. They chose to be told rather than to end up with two envelopes —
"I'd rather be told it already exists than end up with two" (`WI-0001/Q-002`) — and the failure
this prevents is the same one: `envel spend gorceries 12.50` silently creating `gorceries` is
exactly ending up with two. Not asked, because the answer would be the same whoever the
stakeholder was once that preference is on the record. If they want implicit creation, it is a
change to AC4.

**A4 — a spend of exactly the balance succeeds, and leaves zero.** `[assumed]`, written as AC8.

Their words are "I don't want an envelope going negative" (`EP-001/Q-003`). Zero is not negative.
Written as a criterion rather than left silent so that the boundary is visible: an implementation
that refuses `spend 340` on a balance of 340 would be defensible against the prose and wrong
against this.

**A5 — a zero or negative amount is refused on both commands.** `[assumed]`, written as AC9.

Nothing licensed this. A negative income is a spend written backwards and a negative spend is
income written backwards; allowing either gives two ways to record the same movement and makes
WI-0005's correction command ambiguous about what it is correcting. A zero-amount transaction
changes no balance and would still appear in WI-0003's monthly summary. Refusing both is the
narrow choice, and widening it later costs nothing. A disagreement lands as a change to AC9.

**A6 — a date in the future is accepted.** `[assumed]`, recorded in the item's `## Notes` as
deliberately unconstrained rather than as a criterion.

`EP-001/Q-004` is about catching up on days already past and says nothing about a future date.
Refusing one would be a rule they never asked for; accepting it is the absence of a rule. Recorded
so that `verify` finds a decision rather than a gap.

**A7 — an envelope with nothing in it shows `0.00` rather than a blank, a dash or nothing at
all.** `[assumed]`, written as AC16, and new in round 2.

Nothing licensed this. Their answer to Q1 says `envel list` shows the balances and says nothing
about an envelope that has never had money in it, which is the state every envelope is in for the
first few seconds of its life. Three renderings were possible — `0.00`, an empty column, or the
envelope omitted from the listing — and the last two are both defensible readings of "show me the
balances" that would have surprised them. `0.00` was taken because it is the only one under which
`envel list` still answers "what are my envelopes called", which is what the command did before
this item and what `WI-0001` AC6's empty-store case still assumes. A disagreement lands as a
change to AC16.

**A8 — `envel new` stays silent.** `[assumed]`, recorded here rather than as a criterion.

Q3's option A described the quiet tool as "the way `envel new` does today", and they chose C — for
the two commands the question was about. Nothing they said extends the change to `envel new`, and
nothing they said protects its silence either: `WI-0001` AC1 constrains only its stderr and its
exit status, and that criterion is the pipeline's rather than theirs. Left as it is, because
changing a command this item does not otherwise touch on the strength of an answer about two other
commands would be widening their answer. If they want `envel new` to confirm too, it is a new
question and a change to `WI-0001`'s behaviour, exactly as Q1 was.

## Routed to `plan`, not to a person

Three decisions were identified as implementation-only and written into the item's `## Notes`
instead of being asked: how a transaction is stored and how a `version: 1` store from WI-0001
becomes what this item needs; the exact wording of every message this item adds; and which refusal
wins when more than one applies. The answer to each would be the same whoever the stakeholder was,
and `refine`'s step 3 says that makes them `plan`'s.

Round 2 added a fourth thing for `plan`, which is not a decision but a constraint it has to see:
AC17's `£` is a non-ASCII character and `BUG-0001` is open against the tool's handling of exactly
those on the way in. The item's `## Notes` says why this is not a `depends-on` and what `plan` may
not do.

## Definition of Ready — where this item stands

All twelve criteria pass. The per-criterion evidence is in this execution's journal entry.

R6 and R8, the two that failed by construction at the end of round 1, are the two this round
cleared: the three blocking questions are `answered`, and this file now says `recorded` because
the conversation happened. R4, which failed on AC1, AC3 and AC10 naming a question rather than a
value, passes: all three now name a value, and the seven criteria added since name theirs.
