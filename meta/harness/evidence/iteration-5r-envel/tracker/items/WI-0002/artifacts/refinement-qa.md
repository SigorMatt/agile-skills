---
status: recorded
---

# Refinement Q&A — WI-0002

`status: recorded`, as of 2026-09-11: round 2's three replies arrived and `answer-questions`
propagated them, so both rounds of the conversation this file records are finished and quoted
verbatim. The field was `agenda` while round 2 was open — the sentence that stood here then said
it would go back to `recorded` when the round-2 replies were propagated, and this is that. No
question on this item is open.

Round 1's original opening, unchanged: round 1's two questions were put to the stakeholder, who answers
asynchronously in the question files; both came back between turns and `answer-questions`
consumed them on 2026-09-11. What is below is what was actually said — the answers are quoted
verbatim in `## Answers` and marked `human`. Round 1 is closed; the item is back at `draft` and
a second round of `refine` is what takes it to Ready.

## Round 1 — the agenda this round came from

`refine` walked `spec/dor-dod.md` §1 against `WI-0002` as `intake` left it:

- **R4** — AC1 names no observation (nobody knows what to type), and AC5 says in its own words
  that it is not decidable until `EP-001/Q-002` is answered.
- **R7** — the dependency on `WI-0001` was real and unrecorded. You cannot spend from an
  envelope that cannot be created, and AC2 is written against the listing `WI-0001` delivers.
  This round records it in `depends-on`.
- **R8** — this file did not exist.
- **R10** — the combinations nobody had stated: when a spend happened, whether it carries a
  description, and whether a zero or negative spend is accepted.

R1, R2, R3, R5, R9 and R11 passed; R6 passed before this round and fails now, by design,
because this round filed blocking questions. R12 is exercised below, in its "no licence" form.

## Questions put to the stakeholder — round 1, both answered

| # | Question | Why it is theirs | Status |
|---|----------|------------------|--------|
| Q-001 | Is a spend always dated today, or can I say when it happened? | It decides whether `WI-0003`'s monthly summary can be accurate for anything entered late, and there is no way to correct it afterwards. | `answered` |
| Q-002 | Does a spend carry a short description? | It decides what the tool can ever show them about their own past, and it interacts with option C of `EP-001/Q-003`. | `answered` |

Not asked here, because it was already open with the stakeholder and re-asking would have told
them their answer was not heard: what happens when a spend is larger than the envelope's
remaining amount — `EP-001/Q-002`, which AC5 named. It has since been answered: the spend is
refused, and AC5 is now the rule rather than a placeholder.

## Decided here, and by what authority

- **A zero or negative spend amount is refused, on whatever rule `WI-0001/Q-003` sets for
  income.** `[assumed]`

  **Under no delegation.** Nothing the stakeholder has said covers it. It is assumed rather than
  asked because it is the same decision they are already being asked in `WI-0001/Q-003`, in the
  same round, about the same kind of amount — and putting a near-identical question in front of
  them twice is how a question protocol degrades into noise. It is written as a criterion only
  once `Q-003` is answered, and if they want spends to behave differently from income, saying so
  in `WI-0001/Q-003` or in `EP-001/Q-001` lands the disagreement on `WI-0002` AC6 alone.

  **Still assumed, after the answer.** `WI-0001/Q-003` came back as option A — zero and negative
  income both refused — and AC6 now states that rule for spending. The stakeholder was asked
  about income and answered about income, so the *symmetry* is still this assumption and is not
  theirs. `WI-0002` `## Notes` says so, and `answer-questions` did not treat the answer as
  discharging it.

- **Recording a spend prints the envelope's new remaining amount.** `[assumed]`

  **Under no delegation.** Nothing licensed it; it is assumed because the alternative is a
  question about one line of output, and a stakeholder's attention is the scarcest thing in this
  loop. A disagreement lands on `WI-0002` AC7 and costs one line of code.

## Routed to `plan`, not to the stakeholder

Recorded in `WI-0002` `## Notes` for `plan` to settle under its own preference order:

- how a spend is stored alongside the envelope balances, and whether the balance is stored or
  derived by replaying entries;
- what the tool does when the store exists but a spend in it refers to an envelope that is no
  longer there.

## Answers

Both answers below are the stakeholder's own words, copied from the `## Answer` section of the
question file named, and marked `human`. The two entries under *Decided here* remain
`[assumed]`.

- **Q-001 — when a spend happened.** `human`, option B:

  > B. Today unless I say otherwise. I will not always sit down with the receipts on the day,
  > and a Saturday shop landing in the wrong month would make the monthly summary wrong.

  Propagated to `WI-0002` AC8 and AC9, and to `WI-0003` `## Notes` — their reason is a statement
  about the summary, so it belongs where the summary is specified as well as where the date is
  recorded. They chose the option `refine` recommended, for the reason `refine` gave.

- **Q-002 — whether a spend carries a description.** `human`, option B:

  > B — optional. I'll put one on the ones I might query later and skip it on the weekly shop.
  > Don't make me type something every time.

  Propagated to `WI-0002` AC10. The phrase *"the ones I might query later"* implies something no
  item covered — nothing in this epic lets them query a spend, because `EP-001/Q-003` ruled the
  individual spends out of the monthly summary — so `WI-0006` was filed at `draft` under
  `spec/ids-and-statuses.md` §5, with `## Notes` saying it was derived rather than asked for and
  that `refine` must confirm or close it.

## What round 1 did not settle

`refine` round 2 is what takes this item to Ready. R4 still fails: nobody has settled what to
type below `envel`, how a date is written on the command line, or what the command prints. Two
further things these answers opened are listed in `WI-0002` `## Notes` for round 2 — what an
unreadable or future date does, and whether a description is bounded — and neither was guessed
here.

---

## Round 2 — the agenda this round came from

`refine` walked `spec/dor-dod.md` §1 against `WI-0002` as round 1 and `answer-questions` left it.
Two criteria fail, and both fail on the same missing thing — the command surface for recording a
spend:

- **R4** — four criteria are not decidable by someone with a terminal, because nobody has said
  what is typed. AC1 says only *"There is an `envel` command that records a spend"*; AC7 says the
  command prints the new remaining amount without saying what command; AC9 says a spend *"can be
  recorded with a date other than today"* without saying how a date is written; AC10 says the
  same of a description.
- **R10** — three combinations the item introduces have no stated behaviour: a date and a
  description given together, a date the tool cannot read, and a date in the future. The last two
  were carried into `## Notes` by round 1 rather than guessed, which was right; this round has to
  close them or record who left them open.

R1, R2, R3, R5, R9, R11 and R12 pass. R7 passes for the first time — `WI-0001` reached `done` at
`2026-09-11T03:28:08Z`, which is what made this item runnable at all. R8 is `agenda` while this
round is open. R6 passed before this round and fails now, by design, because this round files
three blocking questions.

## Questions put to the stakeholder — round 2, all three answered

The stakeholder is not in this session and answers asynchronously in the question files. All
three are one ask about one thing: the line you type to record a spend.

| # | Question | Why it is theirs | Status |
|---|----------|------------------|--------|
| Q-003 | Are the optional date and description named options (`--on`, `--note`), extra plain words in a fixed order, or a mixture? | It is what they type several times a day, and `WI-0001` deliberately gave the first three commands no options at all — so introducing one is a visible change to the surface they use, not an internal detail. | `answered` |
| Q-004 | Which ways of writing a date does the tool accept, and if a short form like `7/9` is wanted, which reading is theirs? | `7/9` is the 7th of September or the 9th of July depending on where a person lives, and we have not been told where they live. Guessing it would silently misfile spends into the wrong month — the exact failure their `Q-001` answer was given to prevent. | `answered` |
| Q-005 | Is a date in the future refused, recorded, or recorded with a warning? | The same keystrokes are a mistyped year and a direct debit they know is coming, and the tool cannot tell which. Their money moves either way, and correcting a recorded spend is `WI-0005` and is not built. | `answered` |

Not asked, because they have already answered it and re-asking would tell them their answer was
not heard: whether a spend can be dated at all (`WI-0002/Q-001`), and whether a description is
optional (`WI-0002/Q-002`).

## Decided here, and by what authority — round 2

Four things round 1 left open are settled here rather than asked, because the answer would be the
same whoever the stakeholder was, or because a decision they have already made covers it.

- **The subcommand is `spend`: `envel spend <envelope> <amount>`, with the envelope first and the
  amount second.** `[assumed]`

  **Under no delegation.** Nothing the stakeholder has said names it. It is assumed rather than
  asked because `WI-0001` round 2 assumed `new`, `add` and `list` on the same footing, and asking
  about the fourth word while never having asked about the first three would be inconsistent
  rather than careful. The argument *order* follows `envel add <name> <amount>`, which they have
  now used. A disagreement lands on `WI-0002` AC1 and costs the name of one subparser.

- **An unreadable date is refused, with a message, and nothing is recorded.** `[assumed]`

  **Under no delegation.** No answer of theirs covers it. It is assumed rather than asked because
  every other malformed input in this tool is already refused this way and the behaviour is
  built and verified — a badly written amount [src: WI-0001 AC17 "each refused with a message
  with nothing recorded"], an empty envelope name [src: WI-0001 AC13 "are refused with a message
  and no envelope is created"] — and the alternative, quietly falling back to today, would record
  a spend on a date they did not type. A disagreement lands on one criterion of `WI-0002`.

  This is **not** the same question as `Q-005`. That one asks about a date the tool reads
  perfectly well and might still refuse on policy; this one is about text that is not a date.

- **A description has no length limit and no restriction on what characters it may contain.**
  `[assumed]`

  **Under no delegation.** The nearest thing to a licence is `WI-0001/Q-004`, where they chose
  not to restrict what characters an envelope *name* may contain — but that was about names, and
  reading it as covering descriptions would be taking an answer further than it was given. It is
  assumed because an unbounded free-text field is the least surprising answer and a limit is the
  thing that would have to be justified. A disagreement lands on one criterion.

- **A spend's output goes to stdout with exit 0 and every refusal to stderr with a non-zero
  exit.** Not an assumption: it is the project's recorded convention
  [src: docs/architecture/overview.md] and their own criterion on the delivered item
  [src: WI-0001 AC16 "Every refusal this item specifies writes its message to stderr and exits
  non-zero"]. This round writes it into `WI-0002`'s criteria by citation rather than by restating
  it as a new decision.

  The **wording** of every message stays deliberately unconstrained, exactly as `WI-0001`
  `## Notes` left it. The criteria will say what a message must contain — the envelope's name,
  the amount left — and not how it reads.

## Cross-answer check — round 2

No new answer was consumed by this execution, so there is nothing to check a reply against yet.
What was done instead: each of the three questions carries its own `## Cross-answer check`
section, filed **with** the question rather than after it, naming the prior answers the reply
will have to coexist with — `WI-0002/Q-001`, `WI-0002/Q-002`, `EP-001/Q-001`, `EP-001/Q-002`,
`EP-001/Q-004` and `EP-001/Q-006`. `Q-005`'s is the one to watch: `EP-001/Q-002` says they would
rather be stopped than surprised, and an answer of B or C there would be a preference about dates
rather than a reversal of that — which needs saying rather than smoothing over.

`scripts/lint-answers --item WI-0002` → exit 0.

## What round 2 has not settled

The three questions above. Until they are answered, AC1, AC7, AC9 and AC10 stay as round 1 left
them: **no criterion was rewritten by this execution**, deliberately. Rewriting them now would
mean either guessing the answers or renumbering the list twice, and a citation elsewhere naming
`WI-0002 AC7` goes on resolving against whatever moves into that position (DoR R11's neighbour,
F-094). Round 3 rewrites them once, from the replies.

## Answers — round 2

All three replies are the stakeholder's own words, copied from the `## Answer` section of the
question file named, and marked `human`. `answer-questions` consumed them on 2026-09-11 and
propagated each into `WI-0002`'s criteria; the per-question `## Consequences` sections name the
files.

- **Q-003 — how the date and the description are typed.** `human`, option C:

  > C. The description is the bit I'll actually type, so make that the cheap one, and put the
  > longer spelling on the date since I'll hardly ever give one. I don't want to be typing
  > `--note` on the weekly shop.

  Propagated to `WI-0002` AC1 (`envel spend <envelope> <amount>`), AC9 (`--on <date>`) and AC10
  (the description as a plain word, with both givable together or either alone). They chose the
  option `refine` recommended, for the reason `refine` gave, and said so in their own terms.

- **Q-004 — how a date is written.** `human`, option A:

  > A — the full `2026-09-07` and nothing else. I don't want a short form; a spend in the wrong
  > month is exactly the thing I'm trying to get away from, and I'm only typing a date on the odd
  > occasion anyway. For the record, if you ever do add one, `7/9` means the 7th of September to
  > me.

  Propagated to `WI-0002` AC11, which names the accepted form and says that everything else is
  refused with nothing recorded. The last sentence is not a request and nothing was built from
  it: it is recorded in `WI-0002` `## Notes` so that whoever adds a short form, if anyone ever
  does, has their reading without asking again. This is also what makes round 2's
  *unreadable date* assumption concrete — that decision said text the tool cannot read is
  refused, and this answer says which text that is.

- **Q-005 — a date in the future.** `human`, option A:

  > A — refuse it. I record money that has gone, not money that is going to go; a direct debit
  > gets entered the day it leaves. Same reasoning as the overspend: stop me rather than take
  > something I didn't mean.

  Propagated to `WI-0002` AC12. The watch round 2 filed with this question does not arise: it
  was that an answer of B or C would be a preference about dates rather than a reversal of
  `EP-001/Q-002`, and the answer is A, which they themselves tied back to that decision.

## Cross-answer check — round 2, on the replies

Written by `answer-questions` on consuming the three replies. Each question file carries its own
`## Cross-answer check` with the IDs and a verdict for each; the verdicts are `compatible` across
the board and **no conflict was found**, so no question was filed under ADR-0008 §3.

What is worth recording once, here, is *why* there was no conflict to settle: on the two places
where a prior answer of theirs pulled the other way — `EP-001/Q-006`'s *"Short is what matters if
I'm typing it several times a day"* against `Q-003`'s spelling and `Q-004`'s ten-character date —
the stakeholder reconciled it themselves, in the reply, by saying how far that preference
reached. Nobody had to decide it on their behalf, which is the move ADR-0008 exists to prevent.

`scripts/lint-answers --item WI-0002` → exit 0.

## What round 2's answers left for round 3

Nothing was left open by the replies, and no new question arose from them. `refine` round 3 walks
the Definition of Ready against the criteria as `answer-questions` amended them — AC1, AC9 and
AC10 in place, AC11 and AC12 appended — and confirms or challenges them. It does not have to
write them: the reason round 2 deferred the rewrite was the risk of guessing or of renumbering
twice, and `WI-0002` `## Notes` records that neither cost applied once the answers were in.

Still `[assumed]` and still nobody's but ours, unchanged by these replies: the subcommand name
`spend`, the unbounded description, and AC6's symmetry between a zero-or-negative spend and the
same rule for income.

---

## Round 3 — the agenda this round came from

`refine` walked `spec/dor-dod.md` §1 against `WI-0002` as `answer-questions` left it, with all
five questions answered and the criteria carrying the answers. Two criteria fail, and **no
question is put to the stakeholder**: neither failure is theirs.

- **R4** — three criteria state a behaviour nobody can check. AC8, AC9 and AC10 are about a
  spend's date and its description, and **nothing this item delivers prints either of them
  back**: the listing shows names and amounts [src: WI-0001 AC3 "one line per envelope, each
  line containing that envelope's name and the amount currently in it"], and the only readers of
  a spend's date and description are `WI-0003`'s summary and `WI-0006`'s lookup, neither built.
  A criterion nobody can settle is the failure R4 exists for, and it would have reached `verify`,
  who cannot ask anyone anything. Separately, no criterion said which stream a message goes to or
  what the command exits with — round 2 recorded the convention and said it would write it "by
  citation", and then deliberately rewrote no criterion, so it never landed.
- **R10** — four combinations this item's two options introduce have no stated behaviour: a
  refusal when more than one refusal applies at once, an empty or whitespace-only description,
  `--on` given twice, and `envel spend` given the wrong number of words.

R1, R2, R3, R5, R7, R8, R9, R11 and R12 pass. R6 passes for the first time since round 1: every
question on this item is `answered`.

## Questions put to the stakeholder — round 3

**None.** Both failing criteria are ours. R4's gap is about how a criterion is *checked*, not
about what the tool does — the behaviour it describes is exactly what the stakeholder chose at
`WI-0002/Q-001` and `WI-0002/Q-002`, and asking them how to observe it would be asking them to do
our job. R10's four combinations are each one line of behaviour with no stake in their money.
Three rounds have asked them nine questions on this item and its epic; a fourth round asking
nothing is the right outcome, not a gap.

## Decided here, and by what authority — round 3

- **A spend's date and description are read from the store file, and the criteria say so.**
  Not an assumption about the product: the behaviour was settled by the stakeholder, and this is
  a decision about the observation that settles a criterion. The store is one JSON document whose
  entries carry the envelope, the amount and when it was recorded [src: ADR-0002], at a path
  `ENVEL_FILE` names when it is set [src: ADR-0003] — so a person with a terminal, a fresh
  `ENVEL_FILE` and one envelope can open the file and see which date is on which spend. AC8 spells
  out that setup so the observation is repeatable, and says plainly why the file is the reader:
  nothing this item delivers prints a date back.

  **Which field holds the date is not decided here** and is still `plan`'s, in `## Notes`:
  `ADR-0002`'s `at` is *"when the tool recorded the entry"*, and a spend dated `--on` needs its
  own date or a redefinition of that field. The criteria are written so that either choice
  satisfies them — they say the entry *carries* the date, not what it is called.

- **Streams and exit codes are written into a criterion, AC13.** Not an assumption at all: it is
  the project's recorded convention [src: docs/architecture/overview.md] and the delivered item's
  own criterion [src: WI-0001 AC16 "Every refusal this item specifies writes its message to
  stderr and exits non-zero"]. Round 2 said it would write this by citation and then rewrote no
  criterion, so this round did it. The **wording** of every message stays unconstrained, as
  `WI-0001` left it.

- **A `spend` given the wrong number of words is refused like any other subcommand, AC14.**
  Not an assumption: [src: WI-0001 AC15 "A subcommand given the wrong number of arguments prints
  to stderr a usage message for that subcommand and exits non-zero"] is delivered and verified
  behaviour, and `spend` is a subcommand. What is new is only that this item has a third and
  fourth word to get wrong.

- **Four combinations left deliberately unconstrained.** `[assumed]`, **under no delegation** —
  nothing the stakeholder has said covers any of them, and each is recorded in `WI-0002`
  `## Notes` with where a disagreement lands, which is what R10 asks for. They are left rather
  than decided because deciding them would be inventing requirements: which of several
  simultaneous refusals is printed, what an empty or whitespace-only description means, and what
  `--on` twice does are all cases a reasonable implementation may settle either way without
  surprising anyone, and `plan` is closer to them than this round is.

## Cross-answer check — round 3

Checked against: none — **this round consumed no answer.** No question was put to the stakeholder
and none came back; every answer on this item was consumed by `answer-questions` on 2026-09-11,
which wrote the check for each in the question files and again in `## Cross-answer check —
round 2, on the replies` above. Nothing here re-reads them.

The criteria this round wrote were checked against those answers all the same, in the one
direction that matters: AC13 and AC14 are new behaviour, and neither touches the date, the
description, the amount rules or the refusals the stakeholder chose. AC8, AC9 and AC10 gained an
observation and lost no promise — the sentences the stakeholder's answers produced are still
there, word for word, with the way to check them added after.

`scripts/lint-answers --item WI-0002` → exit 0.

## What round 3 has not settled

Nothing that stops the item being Ready, and two things a reader should know:

- **The four unconstrained combinations**, above and in `## Notes`. R10 asks that they be
  visible, not that they be decided, and they are visible.
- **The three `[assumed]` decisions rounds 1 and 2 took**, all still ours and all still under no
  delegation: the subcommand `spend`, an unbounded description, and AC6's symmetry between a
  zero-or-negative spend and the same rule for income. A disagreement with any of them lands on
  one criterion each.
