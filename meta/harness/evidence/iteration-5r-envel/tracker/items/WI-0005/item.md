---
id: WI-0005
type: work-item
title: Correct a spend that was already recorded
status: done
priority: medium
epic: EP-001
created: "2026-09-11T02:12:52Z"
updated: "2026-09-11T10:38:43Z"
arose-from: EP-001/Q-005
depends-on:
  - WI-0002
  - WI-0006
branch: wi/WI-0005
outcome: delivered
merge-commit: 996c336009b17d30bfdba8d565ab5b0b3eab1cfc
---

## Story

As a person budgeting my own money at a terminal, I want to correct a spend I have already
recorded, so that a mistyped amount does not stay in my figures and a summary I look at later
shows what I actually spent.

## Acceptance criteria

Round 3, and the round that reaches Ready. Both rounds of the stakeholder's answers are
propagated; round 3 asked them nothing further, walked the Definition of Ready against the
eighteen criteria their answers produced, and appended AC19 and AC20 for the two combinations
those answers left unconstrained. The command surface below — the subcommand
names `fix` and `remove`, the reference as a plain word, each correctable field as a named option — is `[assumed]`, taken under the
stakeholder's standing delegation at `WI-0003/Q-004`
(**Under delegation:** `WI-0003/Q-004` — argument style and the naming of commands and options).
`artifacts/refinement-qa.md` records it and what a disagreement would cost.

- [x] AC1 — `envel fix <ref>` names the entry to be corrected by the reference the stakeholder
      asked for at [src: WI-0005/Q-001] — a plain word after the subcommand, as `envel spend`
      takes its envelope. The reference is one number counted once across everything recorded,
      so that a number on its own names at most one entry whichever envelope that entry sits in
      [src: WI-0005/Q-008]; `envel fix 148 --amount 14.00` is a whole invocation and carries no
      envelope. The number an entry is given stays that entry's: nothing is renumbered when an
      entry is removed, and a number is not handed to a later entry [src: WI-0005/Q-008].
      `WI-0006` creates the number and prints it, and this item consumes it
      [src: WI-0005/Q-001]. A `<ref>` that matches no entry is refused with a message naming the
      reference, nothing is changed, and the listing
      [src: WI-0001 AC3 "one line per envelope, each line containing that envelope's name and the amount currently in it"]
      is identical before and after.
- [x] AC2 — `envel fix <ref> --amount <amount>` changes that entry's amount to `<amount>`, read
      and shown by the rules already delivered — at most two decimal places, nothing rounded, no
      currency symbol
      [src: WI-0001 AC8 "An amount is written with at most two decimal places"].
      It prints to stdout the entry's envelope and what that envelope holds afterwards, and
      exits 0.
- [x] AC3 — `envel fix <ref> --on <date>` changes a **spend's** date. `--on` accepts the full
      `YYYY-MM-DD` form and nothing else, and a date later than today is refused with a message,
      exactly as the delivered `envel spend` does
      [src: WI-0002 AC11 "accepts the full `YYYY-MM-DD` form and nothing else"],
      [src: WI-0002 AC12 "that is later than today is refused with a message saying the date is in the future"].
      On a refusal nothing is changed.
- [x] AC4 — `envel fix <ref> --description <text>` sets or replaces a spend's description, and
      `envel fix <ref> --description ""` removes one, after which the entry carries no
      description at all rather than an empty one. This is the half of `WI-0005/Q-002`'s answer
      the question said would be written into the criteria rather than asked about; it is
      `[assumed]` under no delegation and `artifacts/refinement-qa.md` says where a disagreement
      about it lands.
- [x] AC5 — `envel fix <ref> --envelope <name>` moves the spend to the envelope called `<name>`:
      the listing then shows that envelope reduced by the spend's amount and the envelope it came
      from increased by it, and no third envelope changed. A `<name>` no envelope has is refused
      with a message naming it and nothing is changed, as `envel spend` already refuses one
      [src: WI-0002 AC3 "Recording a spend against an envelope that does not exist is refused"].
      Names are matched without regard to capitalisation
      [src: WI-0001 AC11 "Envelope names are matched without regard to capitalisation"].
- [x] AC6 — The four options of AC2–AC5 may be given in any combination in one invocation, and
      `envel fix 7 --amount 14.00 --on 2026-09-06 --description "lunch" --envelope "eating out"`
      applies all four to entry `7`. `envel fix <ref>` with none of them prints a usage message
      for the subcommand to stderr, exits non-zero, and changes nothing
      [src: WI-0001 AC15 "A subcommand given the wrong number of arguments prints to stderr a usage message for that subcommand and exits non-zero"].
- [x] AC7 — After a correction, the listing shows the envelopes the entry touched as though the
      corrected values had been recorded when the entry was first made, and no other envelope's
      amount changed.
- [x] AC8 — A summary of a month that already contained the spend
      [src: WI-0003 AC2 "each row shows four figures for that"]
      shows the corrected figure, and the corrected spend appears in exactly one month's summary
      — the month of its date after the correction, not also the month it had before.
- [x] AC9 — A correction that would take an envelope below zero is refused: nothing is changed,
      and the message names the envelope, the amount it holds and how much short of the corrected
      figure that leaves it. The listing never shows a negative amount for any envelope, which is
      the rule the delivered spend already keeps
      [src: WI-0002 AC5 "The listing never shows a negative amount for any envelope"].
- [x] AC10 — `--amount 0` and a negative `--amount` are each refused with a message and nothing
      is changed — the same rule the delivered commands keep for a spend and for income
      [src: WI-0002 AC6 "Recording a spend of `0`, or of a negative amount, is refused with a message"].
- [x] AC11 — `envel remove <ref>` removes a recorded spend. It prints to stdout what it removed —
      the envelope, the date and the amount — and what that envelope holds afterwards, exits 0,
      and asks nothing: no prompt, no confirmation, no `--yes`. That is the stakeholder's
      instruction at [src: WI-0005/Q-003]: *"Don't make it stop and ask me to confirm; just say
      plainly what went and what the envelope holds now."*
- [x] AC12 — `envel remove <ref>` with a `<ref>` that matches no entry is refused with a message
      naming the reference, and nothing is changed.
- [x] AC13 — `envel fix <ref>` and `envel remove <ref>` given the reference of a **move** entry
      are each refused with a message saying a move cannot be corrected or removed, and nothing is
      changed. This is the stakeholder's own boundary, stated twice while answering this item
      [src: WI-0005/Q-002], [src: WI-0005/Q-005].
- [x] AC14 — A correction or a removal made in one invocation is still reflected in the listing
      and in a month's summary in a later, separate invocation of the tool, with the process
      exiting between them.
- [x] AC15 — Every refusal named above writes its message to stderr and exits non-zero, and every
      success writes its output to stdout and exits 0 — the project's recorded convention
      [src: docs/architecture/overview.md] and the rule the delivered items already follow
      [src: WI-0002 AC13 "Every refusal this item specifies writes its message to stderr and exits non-zero"].
      Checked case by case against the criteria that name them: refusals at AC1, AC3, AC5, AC6,
      AC9, AC10, AC12, AC13, AC16, AC18 and AC19; successes at AC2, AC4, AC5, AC7, AC11, AC16,
      AC17 and AC20.
- [x] AC16 — `envel fix <ref>` on the reference of an **income** changes its amount with
      `--amount` and the envelope it went into with `--envelope`, and nothing else. That is the
      stakeholder's answer at [src: WI-0005/Q-006]: *"income has two of those and a spend has
      four, and that is the whole of the difference."* `--on` and `--description` given for an
      income reference are each refused with a message saying an income carries no date and no
      description, and nothing is changed — an income entry records its reference, the envelope,
      the amount and the moment it was typed, and nothing else
      [src: envel/envelopes.py:107], which is the shape the stakeholder chose at
      [src: WI-0003/Q-003] and declined to reopen here. `--amount` and `--envelope`
      behave on an income exactly as AC2 and AC5 specify them on a spend, including the refusal
      of an envelope no envelope has, and `--amount 0` or a negative `--amount` stays refused by
      AC10.
- [x] AC17 — `envel remove <ref>` removes a recorded income, by the same subcommand as AC11, with
      no extra option and no flag: `envel remove 12` on an income reference behaves as
      `envel remove 12` on a spend reference. It prints to stdout what it removed — the envelope
      and the amount — and what that envelope holds afterwards, exits 0, and asks nothing. The
      stakeholder's answer at [src: WI-0005/Q-007]: *"spends and income, one command … the
      command telling me what it took out is enough. No flag."*
- [x] AC18 — Removing an income, correcting one downwards, or moving one to another envelope
      with `--envelope`, where the change would leave an envelope holding less than the spends
      already recorded against it, is refused: nothing is changed, and
      the message names the envelope, the amount it holds and how much short the change would
      leave it — AC9's rule, reaching a removal and a change of envelope as well as a change of
      amount. `envel fix <income-ref> --envelope <name>` takes the income's whole amount out of
      the envelope it went into, so it is the one correction on an income that can take an
      envelope below zero without any figure being reduced. This is the rule
      [src: WI-0005/Q-007] said would be applied unchanged rather than asked about again, and it
      is the stakeholder's own at [src: WI-0005/Q-004]: *"No negative envelopes anywhere in this
      tool, and that includes here."*
- [x] AC19 — A refused invocation of `envel fix` changes **nothing at all**, including the parts
      of it that would have been accepted on their own. `envel fix <income-ref> --amount 20.00
      --on 2026-09-01` is refused by AC16 for the `--on`, and afterwards the entry's amount is
      what it was before the invocation: the line `envel entries` prints for that reference is
      identical before and after, and so is `envel list`. The same holds wherever a refusal named
      at AC1, AC3, AC5, AC6, AC9, AC10, AC13, AC16 or AC18 is reached while other options are
      given in the same invocation. This is `[assumed]` under **no** delegation: it is the rule
      every delivered refusal in this tool already keeps, in the words the stakeholder reads —
      *"Nothing has been changed."* [src: envel/envelopes.py:101] — carried to an invocation that
      asks for more than one change at once. If they would rather have the acceptable parts
      applied and only the rest refused, the disagreement lands on this criterion and on AC6 and
      costs one amendment to each; nothing else depends on it.
- [x] AC20 — The listing the reference is read off shows the change. After
      `envel fix <ref> --amount 14.00`, `envel entries --month <the entry's month>` prints that
      reference's line carrying `14.00`, with the rest of the line as it was
      [src: WI-0006 AC2 "Each entry the listing covers gets one line, and that line carries the entry's"];
      after `envel fix <ref> --on <a date in another month>` that line is absent from the month
      the entry was in and present, once, in the month of its new date
      [src: WI-0006 AC7 "The listing covers one calendar month"]; after
      `envel fix <ref> --envelope <name>` the line names `<name>`; and after `envel remove <ref>`
      no line of any month carries that reference. With an envelope named, the opening and closing
      figures still bracket the lines between them
      [src: WI-0006 AC9 "the figures reconcile: the opening amount, plus the amounts on the lines between, equals the"].

## Out of scope

- Correcting or removing a move between envelopes. `WI-0004` covers moves, and the stakeholder
  reaffirmed the exclusion twice while answering this round: *"a move stays unfixable, exactly as
  I decided before"* [src: WI-0005/Q-002], and *"Not moves — that stays as I decided it"*
  [src: WI-0005/Q-005]. AC13 is that exclusion made observable rather than silent.
- Keeping a history of corrections, or being able to see what an entry used to say. The
  stakeholder chose against it explicitly [src: EP-001/Q-005].
- The command that lists an envelope's entries, and the reference it prints. `AC1`'s `<ref>` is
  read off that listing, and both belong to `WI-0006`, which this item now depends on
  [src: WI-0005/Q-001].
- Reopening the refusal of a zero or negative income at `envel add`. Correction is the route the
  stakeholder wanted instead [src: WI-0001/Q-003], and AC10 keeps that refusal standing here too.
- Giving an income a date. Correcting one cannot set a date: `--on` is refused on an income
  reference at AC16, because the stakeholder settled it that way at [src: WI-0005/Q-006] —
  *"I am not giving income a date by the back door after turning it down two rounds ago"* — which
  leaves their `WI-0003/Q-003` answer standing. They also refused the separate dated-income item
  that `Q-006`'s option D offered: *"I am not leaving a dated-income item sitting on the board
  either — that is D and it is a nice-to-have, not this round."* So no item was filed for it, and
  which month an income counts in stays the month it was typed in
  [src: WI-0003 AC2 "each row shows four figures for that"].
- Correcting or removing a **description** on an income. An income entry has none to correct
  [src: envel/envelopes.py:107], and AC16 refuses `--description` on one rather than inventing the
  field.
- Changing what **kind** of entry something is. Nothing here turns a spend into an income or an
  income into a spend: `envel fix` reaches the fields AC2–AC5 and AC16 name and no others, and a
  spend typed in where income was meant is put right by removing it (AC11) and typing the income.
  `refine`'s decision, not the stakeholder's — they have never been asked, and if they want it the
  disagreement lands on a new criterion rather than on one of these.
- Undoing a correction, or reversing a removal. There is nothing to undo it from: the stakeholder
  chose against keeping a history of corrections [src: EP-001/Q-005], so a removed entry is gone
  and a corrected figure is the only figure. AC11's printing of what it took out is what they
  asked for in its place [src: WI-0005/Q-003].

## Notes

- This item exists because of the stakeholder's answer to `EP-001/Q-005`, option C: *"I mistype
  things in the spreadsheet most weeks, so being able to correct a spend I already recorded
  matters to me more than keeping a perfect history of my own typos — if I fix an entry, a past
  summary should just show the corrected figure."* AC5 and the second `## Out of scope` bullet
  are that sentence: the correction replaces the entry rather than being recorded beside it.
  Filed by `answer-questions` under `spec/ids-and-statuses.md` §5 so that the scope change is
  visible on the board rather than living in a question file.
- **Round 1's five answers are in, and this is what they settled.** Each is the stakeholder's own
  decision, quoted verbatim in the question it answers and in `artifacts/refinement-qa.md`:
  - **How an entry is named — a short reference number** [src: WI-0005/Q-001], option A. Their
    reason: *"I find these mistakes a couple of days after the month has ended with the statement
    in front of me, so an option that only reaches the last spend, or a number that scrolled off
    the screen a week ago, is no use to me."* This is AC1, and it is the answer that ties this
    item to `WI-0006` — see the dependency note below.
  - **Which parts of a spend are correctable — all four** [src: WI-0005/Q-002], option C,
    including the envelope: *"with ten envelopes, putting the Saturday shop against 'eating out'
    instead of 'groceries' is a mistake I will certainly make."* This is AC2 to AC6, one option per
    part; round 2's renumbering is why this line no longer says AC3.
  - **A spend can be removed, by its own command, reporting what it took out**
    [src: WI-0005/Q-003], option B, and without a confirmation prompt. This is AC11 and AC12 after
    round 2's renumbering.
  - **A correction below zero is refused and says how short the envelope is**
    [src: WI-0005/Q-004], option C: *"No negative envelopes anywhere in this tool, and that
    includes here."* This is AC9, and AC18 after `Q-007` carried it to a removal.
  - **Corrections reach income as well as spends** [src: WI-0005/Q-005], option B, because the
    negative income was refused on the understanding that corrections were coming. Round 2's
    `Q-006` and `Q-007` settled how far that reaches, so it is now AC16, AC17 and AC18,
    and it is why the `## Out of scope` bullet that excluded income is gone.
- **Dependency on `WI-0006`, now recorded.** `depends-on` names `WI-0006` and `WI-0002` from
  round 2. The stakeholder settled the order themselves: *"That does mean the listing command has
  to exist, and I am saying yes to that separately"* [src: WI-0005/Q-001]. The reference belongs
  to `WI-0006`, which creates it and prints it; this item consumes it, and AC1 says so. That is
  also why `## Out of scope` now excludes the reference itself — round 1's draft had this item
  creating it, which would have made the two items circular, each waiting for the other.
  Round 2 recorded that `WI-0006` still had to make creating the reference one of its criteria.
  **That is now done**: `WI-0006` AC3 owns the number and names this item as its consumer, and
  `WI-0006` is `done` and merged [src: WI-0006 AC3 "The reference on a line is a number counted once across everything recorded"].
- **`WI-0006` was built before this item, and *"keep it small and keep it last"* was kept.**
  Their instruction at [src: WI-0006/Q-001] was about size and priority, and it was honoured:
  `WI-0006` stayed at priority `low` and small. What the dependency changed was the order the two
  were *built* in, which their `Q-001` answer here decided. `WI-0006` is now `done`, so this item
  is the last one left in the epic and R7's dependency is satisfied rather than merely sequenced.
- **Round 2's three answers are in, and this is what they settled.** Each is the stakeholder's
  own decision, quoted verbatim in the question it answers and in `artifacts/refinement-qa.md`:
  - **Correcting an income reaches its amount and its envelope, and stops there**
    [src: WI-0005/Q-006], option B. Their reading of their own *"in the same way as a spend"*:
    *"anything I can type wrong when I put it in, I can put right; income has two of those and a
    spend has four, and that is the whole of the difference."* This is AC16. It leaves their
    `WI-0003/Q-003` answer standing — round 2 filed the collision rather than reconciling it, and
    the stakeholder resolved it in favour of the older sentence.
  - **An income can be removed by the same command as a spend, with no flag**
    [src: WI-0005/Q-007], option B: *"a payslip entered twice is money I do not have sitting in
    an envelope, and inventing a fake spend to cancel it would be worse than the mistake."* This
    is AC17. They also read their own `WI-0001/Q-001` sentence for us — *"what I said about not
    wiping money out by accident was about an envelope disappearing under me, not about me
    removing an entry I asked it to remove"* — which is why AC17 asks nothing before acting.
  - **The reference is one number counted once across everything recorded** [src: WI-0005/Q-008],
    option A: *"what I care about is copying one thing off the line in front of me and typing it
    back."* This is AC1, and they said explicitly that the per-envelope `7` in their round-1
    answer was our example rather than their decision.
- **What the reference answer meant for `WI-0006`, and how it landed.** `Q-008` was answered on
  this item and the work fell on `WI-0006`, which is where the number is created and printed.
  This item cannot edit a sibling's criteria, so round 2 recorded the two obligations here and in
  `docs/product/vision.md` (v6), and `WI-0006`'s own round 3 took them up: its AC3 says the number
  is counted once across everything recorded and that this item consumes it, and its AC4 says a
  reference is not moved onto another entry — which is what makes AC1's *"nothing is renumbered
  when an entry is removed"* deliverable rather than hopeful
  [src: WI-0006 AC4 "A reference belongs to its entry and is not moved onto another"]. The
  delivered store carries the counter that does it [src: ADR-0010], and `envel entries` prints
  the number first on every line [src: envel/summary.py:144].
- **R9: not split.** With the reference belonging to `WI-0006`, what is left here is `envel fix`
  and `envel remove` — two subcommands over one piece of machinery: find an entry by its
  reference, change or drop it, and re-check the same balance invariant
  [src: WI-0002 AC5 "The listing never shows a negative amount for any envelope"]. Splitting them
  would put the invariant in two items. Recorded in `artifacts/refinement-qa.md` with the
  reasoning, because R9 was left `unresolved` in round 1 pending exactly these answers.
- **Round 3 asked the stakeholder nothing, and this is why.** Every gap it found was a reading of
  a convention this tool already delivers and already prints in the messages they see, not a
  choice about what the software is for. Two were written as criteria: AC19, that a refused
  invocation applies none of itself, and AC20, that `envel entries` shows the change. Both are
  `[assumed]` under **no** delegation and each says on its own line where a disagreement lands.
  Round 3 also stopped short of the one thing it could have invented a question about — whether a
  correction should be applied in part — because the stakeholder has never asked for partial
  application anywhere and eight delivered refusals say *"Nothing has been changed."*
- **Which figure the below-zero rule is about, observed rather than assumed.** AC9 and AC18 are
  about what an envelope *holds* — the figure `envel list` prints — and not about the
  month-bounded opening figure `envel entries <envelope>` prints, which can already be negative in
  the delivered tool with no correction in sight. A store with an August spend and September
  income shows it: `envel entries groceries` prints `groceries held -42.30 at the start of 2026-09`
  while `envel list` prints `groceries  45.20`
  [src: run: ENVEL_FILE=<a fresh store> python3 -m envel entries groceries → exit 0, opening line `groceries held -42.30 at the start of 2026-09`].
  That falls out of the stakeholder's own pair of decisions — a spend carries its own date
  [src: WI-0002/Q-001] and an income does not [src: WI-0003/Q-003] — and they said what happens if
  it ever costs them something: *"If a payslip in the wrong month ever actually costs me something
  I will come and tell you"* [src: WI-0005/Q-006]. It is written here so that whoever implements
  AC9 and AC18 checks `envel list`'s figure and does not invent a second check over a bounded sum.

- **What round 3 changed and did not.** It amended AC16's source citation, which the code had
  moved under when `WI-0006` added the reference counter [src: ADR-0010], and AC18's text, which
  named two of the three ways an income correction can take an envelope below zero. It appended
  rather than inserted criteria, because `ADR-0010` cites this item's AC1 twice by number and
  AC15 lists nine criteria by number; a renumbering would leave all of them pointing at whatever
  moved into the slot. No criterion was rewritten to match anything that has been built — there
  is no branch for this item yet.
