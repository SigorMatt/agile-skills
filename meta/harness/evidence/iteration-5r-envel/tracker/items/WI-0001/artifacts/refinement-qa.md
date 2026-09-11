---
status: recorded
---

# Refinement Q&A — WI-0001

`status: recorded`. Two rounds. Round 1 put four questions to the stakeholder, who answers
asynchronously in the question files; all four came back and `answer-questions` consumed them on
2026-09-11. Round 2 asked nothing: what was left was the command surface, and this file records
why that was decided here instead of being sent to them, and exactly what was decided. What is
below is what was actually said — the answers are quoted verbatim in `## Answers`, and every
decision taken without an answer is marked `[assumed]` and says what licensed it.

## Round 1 — the agenda this round came from

`refine` walked `spec/dor-dod.md` §1 against `WI-0001` as `intake` left it, and these are the
criteria that failed:

- **R4** — none of AC1, AC2 or AC3 names an observation. "There is a command that creates an
  envelope" cannot be handed to someone with a terminal: they do not know what to type, what it
  should print, or what exit code to expect.
- **R8** — this file did not exist.
- **R10** — the behaviours this item introduces have combinations nobody had stated: a name that
  already exists, an amount of zero or a negative one, how a number is written and shown back,
  and whether two spellings of a name are one envelope or two.

R1, R2, R3, R5, R7, R9 and R11 passed; R6 passed before this round and fails now, by design,
because this round filed blocking questions. R12 is exercised below, in its "no licence" form.

## Questions put to the stakeholder — round 1, all four answered

| # | Question | Why it is theirs | Status |
|---|----------|------------------|--------|
| Q-001 | What happens when you create an envelope whose name already exists? | One of the plausible answers destroys a balance the tool exists to keep. | `answered` |
| Q-002 | How are amounts written, and how are they shown back? | It decides whether the figures can be made to add up exactly, and it is visible in every line of output. | `answered` |
| Q-003 | Are zero and negative income amounts accepted? | A negative income is a correction route arriving by the back door, and corrections are an open scope question (`EP-001/Q-005`). | `answered` |
| Q-004 | Are envelope names matched exactly, or is `Groceries` the same envelope as `groceries`? | Getting it wrong splits one envelope into two with half the money in each, and it shows in their own listing. | `answered` |

Two further things `WI-0001` needed were **not** asked here, because they were already open with
the stakeholder on the epic and re-asking would have told them their answer was not heard. Both
have since been answered:

- the command the tool is invoked as — `EP-001/Q-006`: it is `envel`, now in AC1, AC2 and AC3;
- whether correcting a mistake, or moving money between envelopes, is in this first version —
  `EP-001/Q-005`: both are, and they were filed as `WI-0004` and `WI-0005` rather than added to
  this item, so this item's scope is unchanged.

## Decided in round 1, and by what authority

- **The order envelopes are listed in** — alphabetical by name. `[assumed]`

  **Under no delegation.** The stakeholder has given no answer that covers this category; there
  is no standing "you decide" to spend. It is assumed because the alternative is asking a fifth
  question about something that changes nothing about what the tool can do, and a stakeholder's
  attention is the scarcest thing in this loop. If they disagree, the disagreement lands on
  `WI-0001` AC3 and costs one line of code and one criterion — which is the whole reason it was
  judged safe to assume rather than ask.

- **Listing when no envelopes exist** — prints a line saying there are none and exits 0, rather
  than printing nothing or failing. `[assumed]`

  **Under no delegation**, on the same basis as above: nothing licensed it, it is assumed
  because silence and an error are both worse than a sentence, and a disagreement lands on
  `WI-0001` AC6 alone.

## Routed to `plan`, not to the stakeholder

These would have the same answer whoever the stakeholder was, so they are design and they are
recorded in `WI-0001` `## Notes` for `plan` to settle under its own preference order:

- where the data is stored, in what format, and what happens if that file is missing, empty or
  unreadable;
- whether the store is written atomically, so an interrupted run cannot leave a half-written
  file.

## Answers

All four answers below are the stakeholder's own words, copied from the `## Answer` section of
the question file named. They are marked `human`; the two entries under *Decided in round 1*
above remain `[assumed]` and nothing in that round licensed them.

- **Q-001 — a create of a name already taken.** `human`, option A:

  > A — refuse and tell me it already exists. I will be setting these up by hand, eight or ten
  > of them, so the second run of a create is a mistake and I want to hear about it. Nothing
  > should ever be able to wipe money out of an envelope by accident.

  Propagated to `WI-0001` AC7. They chose the option `refine` recommended, and gave a reason
  `refine` had not thought of — that they will be creating eight or ten envelopes by hand, so a
  repeated create is a mistake rather than a re-run.

- **Q-002 — how amounts are written and shown.** `human`, option A:

  > A. One currency, cents exactly, two decimal places both ways — `12.5` meaning 12.50 is fine.
  > I do not want anything rounded off; the figures have to add up. How you keep it under the
  > hood is yours to decide.

  Propagated to `WI-0001` AC8 and AC9, and recorded on `EP-001` `## Notes` as a rule that holds
  across every item. The last sentence is a delegation of the **internal representation** only —
  it licenses `plan` to choose how amounts are held, and it licenses nothing about what is
  accepted or printed, which they specified.

- **Q-003 — zero and negative income.** `human`, option A:

  > A — refuse both. Putting income in should only ever mean more money going in. I have asked
  > for proper corrections and for moving money between envelopes in the epic's Q-005, so there
  > is no need for a back door through a negative income.

  Propagated to `WI-0001` AC10, and to `WI-0002` AC6 — which `refine` had written against this
  question by symmetry — where it replaces a placeholder. They answered it having already
  answered `EP-001/Q-005`, and said so, which is why the correction route is `WI-0005` and not a
  negative income.

- **Q-004 — how names are matched.** `human`, option A:

  > A. "Groceries" and "groceries" are the same envelope — the same money split across two of
  > them is exactly the mess I want to avoid. Show it back the way I first typed it, and don't
  > go restricting what characters I can use; my names are things like "groceries", "car" and
  > "eating out".

  Propagated to `WI-0001` AC11, AC12 and AC13, and recorded on `EP-001` `## Notes`. They took
  option A and pushed back on the character restriction that option C offered, so AC13 refuses
  only the empty name and a leading or trailing space, which is what option A itself said.

## Round 2 — the command surface, and why nothing was asked

Round 1 closed with one criterion still failing and named it: *"R4 still fails: none of AC1, AC2
or AC3 names what to type below `envel`, what it prints, or what exit code it gives. The
stakeholder settled the behaviour; nobody has settled the surface."* That is round 2's whole
agenda. R10 was re-walked at the same time and produced three gaps of its own — an unknown
subcommand, a wrong argument count, and what a badly written amount does — which are AC14, AC15
and AC17.

**No question was filed.** `refine`'s step 3 test was applied to the surface and it does not
reach the stakeholder:

- It is not **product stake**. The subcommand a verb is spelled with changes nothing about what
  the tool is for, what it promises, what counts as correct, or what happens to their money. It
  is squarely in the category step 3 names as a standing deferral's — *"what things are called,
  the exact wording of output, exit codes, file layout"*.
- It is **not already answered**, and it is **not under a standing delegation**: nothing the
  stakeholder has said licenses it. `WI-0001/Q-002`'s *"How you keep it under the hood is yours
  to decide"* is the internal representation of an amount and nothing wider, and round 1 already
  read it that way.
- So it is **implementation-only**, and the step 3 route for that is to decide it and leave it
  visible. Routing it to `plan` instead was rejected for one reason: R4 is a hard gate on *this*
  skill, and an acceptance criterion that says "there is some subcommand that creates an
  envelope" is not decidable by someone with a terminal and no context.

What the stakeholder *has* said that bears on it is `EP-001/Q-006`: they picked `envel` over
`envelope` because *"Short is what matters if I'm typing it several times a day."* That is a
stated preference to apply, not a licence to spend, and it is what the verbs below were chosen
against.

The honest summary is the one R12 asks for: **five decisions were taken here under no
delegation**, they are each cheap to reverse, and each entry says where a disagreement lands.
`review-close` names assumed answers in the sign-off, which is where the stakeholder sees them.

## Decided in round 2, and by what authority

- **The three subcommands are `new`, `add` and `list`, with positional arguments only** —
  `envel new <name>`, `envel add <name> <amount>`, `envel list`. `[assumed]`

  **Under no delegation.** Chosen against `EP-001/Q-006`'s stated preference for short things
  typed several times a day, and for a verb set the rest of the epic can extend without
  collision: `WI-0002` needs a spend, `WI-0004` a move, `WI-0003` a summary, and none of those
  is `new`, `add` or `list`. `add` is unambiguous because `new` is what creates. A disagreement
  lands on AC1, AC2, AC3, AC14 and AC15 and costs the argument parser and five criteria; no
  stored data and no behaviour depends on it.

- **Success to stdout and exit 0; every refusal to stderr and exit non-zero.** `[assumed]`
  AC16, and the exit codes now written into AC1, AC2, AC3, AC14 and AC15.

  **Under no delegation.** It is the ordinary convention for a tool at a terminal, and the
  stakeholder had already produced half of it themselves without being asked: their answer to
  `Q-001` is what made AC7 exit non-zero. A disagreement lands on AC16 alone.

- **The listing carries no total line.** `[assumed]` AC3.

  **Under no delegation**, but not out of nowhere: at `EP-001/Q-003` they refused a total line on
  the monthly summary — *"I don't need a total line for the month"* — which is the nearest thing
  they have said about a total anywhere. This reads that preference across to the listing rather
  than asking again. It is an inference from an answer and not the answer itself, so it is
  `[assumed]`. A disagreement lands on AC3.

- **An amount is a plain decimal number, with no currency symbol and no thousands separator,
  either accepted or printed.** `[assumed]` AC17.

  **Under no delegation.** Their *"One currency, cents exactly"* at `Q-002` settles that there is
  no currency to choose between, which is why a symbol carries no information; it does not
  itself say that a symbol is refused. A disagreement lands on AC17 alone and is a change to the
  amount parser.

- **The exact wording of every message is left open on purpose**, and the criteria constrain only
  what a message must *contain*. `[assumed]`

  **Under no delegation**, and recorded because the silence is deliberate rather than an
  oversight. A disagreement lands nowhere in this item: no criterion quotes a message.

## Left deliberately unconstrained in round 2 (R10)

- Whether two names differing only in **internal** whitespace — `eating out` against
  `eating  out` — are one envelope or two. AC11 settles capitalisation, AC13 settles which
  characters are allowed, and neither reaches this. Left open by `refine`, which judged it too
  thin to spend a stakeholder round trip on and too arbitrary to assume quietly; `WI-0001`
  `## Notes` records it so that whoever hits it can see it was seen. A decision later lands on
  AC11.

## Cross-answer check — round 2

`scripts/lint-answers --item WI-0001` is the gate; this is the read behind it. Round 2 recorded
no new stakeholder answer, so what was checked is each criterion written this round against the
stakeholder's existing answers.

Checked against: `EP-001/Q-006`; `EP-001/Q-003`; `WI-0001/Q-001`; `WI-0001/Q-002`;
`WI-0001/Q-003`; `WI-0001/Q-004`.

- `EP-001/Q-006` — compatible, and it is the answer the subcommand choice was made against
  rather than one it might contradict: it fixes the program's name and says shortness is what
  they value. `new`, `add` and `list` do not disturb `envel`.
- `EP-001/Q-003` — compatible. They refused a total line on the monthly summary; AC3 gives the
  listing no total line either. If they had wanted one in the listing, this would be the answer
  that said so, and it says the opposite.
- `WI-0001/Q-001` — compatible. AC16's rule that refusals exit non-zero is the general form of
  what AC7 already said on their instruction.
- `WI-0001/Q-002` — compatible, and read narrowly. They fixed what is accepted (`12.5`) and what
  is printed (two decimal places); AC17 adds only that the number carries no symbol and no
  separator, and AC8's rule is untouched. Their delegation in the same answer covers the
  internal representation and is not spent here.
- `WI-0001/Q-003` — compatible. AC17 explicitly does **not** take over the refusal of a negative
  amount: a leading `-` is read as a negative amount and refused by AC10, which is their answer,
  rather than being refused as a malformed number, which would have quietly restated their
  decision as a parsing rule.
- `WI-0001/Q-004` — compatible. AC14 and AC15 constrain what the *tool* does with a word that is
  not a subcommand and with a wrong argument count; neither restricts what characters a name may
  contain, which is the thing they pushed back on.

No contradiction was found, so nothing was put back to them, and no recorded sentence of theirs
was edited.
