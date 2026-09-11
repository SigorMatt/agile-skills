---
id: WI-0006
type: work-item
title: Look up what has been recorded against an envelope
status: done
priority: low
epic: EP-001
created: "2026-09-11T02:22:17Z"
updated: "2026-09-11T09:16:00Z"
arose-from: WI-0002/Q-002
branch: wi/WI-0006
outcome: delivered
merge-commit: b93e5259ecd9a7393d2e7aa12e23c5c4fb8608d4
---

## Story

As a person budgeting my own money at a terminal, I want to look at what has been recorded
against an envelope, so that I can find the entry I am wondering about and see what is behind the
envelope's balance instead of only seeing the balance itself.

## Acceptance criteria

Round 2. The command surface below — the subcommand name `entries`, the envelope as a plain word,
the month as a named option — is `[assumed]`, taken under the stakeholder's standing delegation at
`WI-0003/Q-004`
(**Under delegation:** `WI-0003/Q-004` — argument style and the naming of commands and options).
`artifacts/refinement-qa.md` records how the licence was spent, what was weighed against it, and
what a disagreement would cost.

- [x] AC1 — The command is `envel entries`. `envel entries` with nothing after it lists what was
      recorded across the envelopes during the calendar month today falls in; `envel entries
      groceries` lists what was recorded against that envelope; `--month <YYYY-MM>` names a month
      instead of today's, with or without an envelope, so that `envel entries groceries --month
      2026-08` and `envel entries --month 2026-08` are both accepted. A month is spelled the way
      `envel summary` already spells one
      [src: WI-0003 AC5 "four-digit year, hyphen, two-digit month"].
- [x] AC2 — Each entry the listing covers gets one line, and that line carries the entry's
      reference, the date it counts under (AC5), its kind — income, spend, or a move in or out
      (AC6) — the envelope it belongs to, its amount, and, for a spend that has one, its
      description
      [src: WI-0002 AC10 "A spend can be recorded with a short description of what it"]. Every amount is a plain
      decimal with two decimal places, no currency symbol and no thousands separator, which is the
      project's delivered output rule and not a new decision
      [src: WI-0001 AC8 "An amount is written with at most two decimal places"],
      [src: WI-0001 AC17 "No amount the tool prints carries a currency symbol"].
- [x] AC3 — The reference on a line is a number counted once across everything recorded, rather
      than within each envelope, so that a number on its own names at most one entry whichever
      envelope that entry sits in. That is the stakeholder's decision at [src: WI-0005/Q-008]:
      *"one number across everything … what I care about is copying one thing off the line in
      front of me and typing it back."* This item is where the number is created and printed;
      `WI-0005` consumes it [src: WI-0005/Q-001], and `WI-0005` AC1 says so from its side.
- [x] AC4 — A reference belongs to its entry and is not moved onto another. Recording further
      entries after a listing has been read leaves every reference that listing printed pointing
      at the same entry it pointed at before, and gives the new entries references none of the
      earlier ones had. The number is therefore a property the entry carries in the store
      [src: ADR-0002], not its position among the entries that happen to exist when the listing
      runs — which is what makes the stakeholder's *"a number I wrote down last week still means
      what it meant"* true once `WI-0005` can remove one.
- [x] AC5 — The date on a line is the day the money moved where the entry has one, and the day
      the entry was recorded where it has not. That is the rule the delivered summary already
      applies rather than a new one [src: envel/summary.py:27], and it is the stakeholder's
      asymmetry: income falls under the day it was typed because they declined to date it
      [src: WI-0003/Q-003], while a spend falls under its own date
      [src: WI-0002 AC9 "A spend can be recorded with a date other than today, written as"].
- [x] AC6 — A move between two envelopes appears as two lines, one against the envelope the money
      left and one against the envelope it arrived in, each naming its direction, because that is
      how a move is recorded [src: ADR-0007]. With an envelope named, only that envelope's line
      is shown; with none named, both are, and the two carry the same date and the same amount in
      opposite directions.
- [x] AC7 — The listing covers one calendar month: the month today falls in when `--month` is not
      given, and the named month when it is. An entry falls in the month of the date AC5 gives it
      [src: envel/summary.py:27], so a past month lists the same entries whenever it is run. This
      is the stakeholder's answer at [src: WI-0006/Q-002]: *"a month at a time, this month unless
      I name one, and named the same way as the summary."*
- [x] AC8 — Lines are ordered oldest first by the date of AC5, and two entries with the same date
      appear in the order they were recorded, which is the order the store holds them in
      [src: ADR-0002]. The order is therefore total: the same store and the same month produce
      the same listing on every run. This is `[assumed]` under **no** delegation — the ordering
      was named in advance in `artifacts/refinement-qa.md` before the stakeholder was asked
      anything, and a disagreement about it lands on this criterion and costs one amendment.
- [x] AC9 — With an envelope named, the listing opens with a line giving what that envelope held
      at the start of the month and closes with a line giving what it holds at the end of it, and
      the figures reconcile: the opening amount, plus the amounts on the lines between, equals the
      closing amount. That is the stakeholder's rule — *"a list I cannot add up costs me an
      evening whichever report it is on"* [src: WI-0006/Q-004] — applied the way the delivered
      summary already reconciles a month
      [src: WI-0003 AC3 "money in, minus money spent, plus money moved, equals the change in that"].
      The closing amount equals what `envel list` shows for that envelope when the month named is
      the month today falls in
      [src: WI-0001 AC3 "one line per envelope, each line containing that envelope's name and the amount currently in it"].
- [x] AC10 — With no envelope named, the listing covers the envelopes together, each line carrying
      the envelope it belongs to (AC2), and it prints **no** opening and closing figure: across
      ten envelopes there is no single balance for one to reconcile against, and the case the
      stakeholder described for this form is finding an entry rather than adding a column up —
      *"a 34.99 on the statement I cannot place"* [src: WI-0006/Q-003]. This is `[assumed]` under
      **no** delegation; a disagreement lands on this criterion and costs one amendment.
- [x] AC11 — A listing with nothing to show — an envelope with no entries in the month, or a month
      in which nothing was recorded at all — prints to stdout a line saying so and exits 0, rather
      than printing nothing or failing. It is a success and not a refusal, which is the treatment
      the delivered commands already give an empty answer
      [src: WI-0001 AC6 "Listing when no envelope has ever been created prints a line saying there"].
      With an envelope named, AC9's opening and closing lines are still printed, because an
      envelope with no entries in the month still has a balance.
- [x] AC12 — `envel entries nosuch` names an envelope that does not exist: it is refused with a
      message naming what was typed, nothing is printed on stdout, and the exit is non-zero, as
      the delivered commands already refuse one
      [src: WI-0002 AC3 "Recording a spend against an envelope that does not exist is refused"].
      The refusal is distinguishable from AC11's empty listing by the stream and the exit code
      alone. Envelope names are matched without regard to capitalisation
      [src: WI-0001 AC11 "Envelope names are matched without regard to capitalisation"].
- [x] AC13 — A month this command will not accept is refused with a message on stderr, nothing on
      stdout, and a non-zero exit, in two cases: a month later than the month today falls in
      (`--month 2027-03` run in September 2026), and text that is not four digits, a hyphen and a
      two-digit month in the range `01` to `12` (`--month 2026-8`, `--month august`,
      `--month 2026-13`, `--month 2026-08-01`). Both are the treatment the delivered summary
      already gives the same two cases
      [src: WI-0003 AC9 "A month **later than the month today falls in** is refused"],
      [src: WI-0003 AC12 "A month the tool cannot read is refused"], and the stakeholder's reason
      for the first is on the record: *"A page of figures with the wrong year at the top is
      exactly the sort of thing I'd read straight past, and I'd rather be stopped"*
      [src: WI-0003/Q-005]. Applying it to this command is `[assumed]` under **no** delegation and
      a disagreement lands on this criterion.
- [x] AC14 — The listing carries no running-balance column down the side — *"I don't need a
      running balance down the side"* [src: WI-0006/Q-004] — and `envel summary` prints exactly
      what it printed before this item: the same rows, the same four figures, no individual entry
      [src: WI-0003 AC6 "The summary prints no total line for the month and does not list individual spends"].
      The second half is read as well as run: `WI-0003`'s AC1 through AC14 are re-read against
      this item's behaviour, and the evidence that they still hold is that `WI-0003`'s delivered
      tests pass unchanged. Where nothing executable exercises both this command and the summary
      together, the non-intersection is stated and a case covering it is added rather than waived.
- [x] AC15 — Every refusal named above writes its message to stderr and exits non-zero, and every
      successful listing — AC11's nothing-to-show line included — writes its output to stdout and
      exits 0; it is the project's recorded convention
      [src: docs/architecture/overview.md] and the rule the delivered items already follow
      [src: WI-0001 AC16 "Every refusal this item specifies writes its message to stderr and exits non-zero"].
      A command line of the wrong shape — `envel entries groceries extra`, `envel entries --month`
      with nothing after it, `envel entries --for 2026-08` — prints the subcommand's usage to
      stderr and exits non-zero with nothing on stdout
      [src: WI-0001 AC15 "A subcommand given the wrong number of arguments prints to stderr a usage message for that subcommand and exits non-zero"].
      Checked case by case against the criteria that name them: refusals at AC12, AC13 and AC15;
      successes at AC1, AC2, AC9, AC10 and AC11.

## Out of scope

- Any change to the monthly summary of `WI-0003`. The stakeholder ruled the individual spends out
  of that report at `EP-001/Q-003` and said so again while asking for this command: *"It does not
  reopen the monthly summary — I still don't want individual spends in that"* [src: WI-0006/Q-001].
  AC14 is that exclusion made observable rather than silent.
- Searching or filtering entries by description, amount or date range.
- Listing more than one month in one invocation, or a range of dates. The stakeholder chose a
  month at a time and gave the reason: *"I don't want a command whose output gets longer every
  year I use it"* [src: WI-0006/Q-002]. Reaching an older month means naming it with `--month`.
- A running balance down the side of the listing — *"I don't need a running balance down the
  side"* [src: WI-0006/Q-004].
- An opening and closing figure on the listing that names no envelope. AC10 decides against it,
  and the decision is `refine`'s rather than the stakeholder's, recorded as such in
  `artifacts/refinement-qa.md`.
- Correcting or removing anything from this listing. `WI-0005` owns both, and this command prints
  the reference they are aimed with.

## Notes

- **This item was derived, not asked for. `refine` put that to the stakeholder in round 1 and they
  kept it** [src: WI-0006/Q-001], option A: *"You have not over-read me: I meant reading those
  notes back, and when I am checking a month against the statement I need to see what is behind an
  envelope's balance. Keep it small and keep it last."* It exists because of one phrase in their
  answer to `WI-0002/Q-002` — *"I'll put one on the ones I might query later"* — and that reading
  is now confirmed by them rather than inferred by us.
- **Round 1's four answers and what each settled:**
  - **Build it, small, and last** [src: WI-0006/Q-001]. Priority stays `low` by their instruction,
    not by our guess. See the sequencing note below, which is the one thing that complicates it.
  - **A month at a time** [src: WI-0006/Q-002], option B: the current month unless one is named,
    and named the way `envel summary` names one. Their reason: *"I work a month at a time and I
    don't want a command whose output gets longer every year I use it."* This is AC7 after round
    2's renumbering.
  - **The envelope is optional** [src: WI-0006/Q-003], option B: *"The case I actually have is a
    34.99 on the statement I cannot place, and that is precisely the moment I cannot name an
    envelope."* With `Q-002`'s answer, the bare command means *this month, across the envelopes*,
    which they describe as *"a page I can read"*. This is AC1 and AC10 after round 2's
    renumbering.
  - **Income and moves as well as spends** [src: WI-0006/Q-004], option B, with the kind named on
    the line and no running balance. They were explicit that the rule they gave about the monthly
    summary travels: *"a list I cannot add up costs me an evening whichever report it is on."*
    This is AC2, AC6 and AC14 after round 2's renumbering, and it is why the old `## Out of scope`
    bullet excluding income and moves is gone — we wrote that exclusion, and they have now overruled it.
- **The title changed with `Q-004`'s answer.** It was *"Look up the spends recorded against an
  envelope"*, which stopped being what the item is the moment income and moves came in. The story
  and AC1 changed with it.
- **Round 2 settled the two things round 1 left open, and neither went back to the stakeholder.**
  - **How a single month's listing adds up** is AC9 and AC10. With an envelope named, an opening
    and a closing line bracket the entries and the three reconcile, which is the arrangement
    `refine` put in front of the stakeholder in `Q-004`'s own `## Cross-answer check` — *"we would
    handle that by printing the carried-in figure as an opening line, the way `WI-0003` AC3
    already reconciles a month"* — before they answered `Q-004`. With no envelope named there is
    no opening or closing figure, because there is no single balance for one to reconcile
    against; that half is `refine`'s own and is recorded as `[assumed]` under no delegation.
  - **Whether the reference is per-envelope or global** was answered by the stakeholder on
    `WI-0005` while this item waited: *"one number across everything"* [src: WI-0005/Q-008]. AC3
    is that answer, and AC3 also puts the reference's creation on this item, which is where
    `WI-0005`'s own round 2 concluded it belongs [src: WI-0005/Q-001]. Round 1's AC2 had
    attributed the reference to `WI-0005` and was the wrong way round; AC3 corrects it. That
    discharges the instruction `WI-0005`'s `## Notes` left for this round — *"`WI-0006`'s own
    round 2 has to make creating the reference one of its criteria"* — and the sentence there
    saying AC2 is the wrong way round is now spent. `refine` on this item does not edit
    `WI-0005`'s own notes, so this is where a reader of either item finds it.
- **What plan has to honour for AC4.** The stakeholder's promise is that a number written down
  last week still means what it meant, and `WI-0005` will be able to remove an entry
  [src: WI-0005/Q-007]. A reference derived from an entry's position in the store would break
  that the first time a removal happened, and the break would be invisible until somebody typed
  an old number. AC4 states the observable half — recording more entries moves nobody's
  reference — and this note states the half `plan` has to design for: the number is stored with
  the entry [src: ADR-0002] rather than computed when the listing runs.
- **Sequencing: `WI-0005` needs this item, and the stakeholder asked for this one last.** At
  `WI-0005/Q-001` they chose a printed reference and said *"That does mean the listing command has
  to exist, and I am saying yes to that separately"*; here they said *"keep it last"*. The two are
  not in conflict — *last* is about size and priority, and the dependency is a fact about the
  order the work has to be done in — but they cannot both be honoured naively, because
  `WI-0005`'s AC1 cannot be demonstrated until something prints a reference. Deciding the order is
  `refine`'s and `next`'s, and it is now settled: `WI-0005` records `depends-on: WI-0002,
  WI-0006`, so this item is built first and `WI-0005` after it. *Last* is honoured as size and
  priority — this item stays `low` and its criteria are one command — and the dependency is
  honoured as order. Both sentences are on the record here and on `WI-0005`.
- Depends on `WI-0002` for there to be entries to list, and on `WI-0001` for envelopes; not
  recorded in the frontmatter yet, for the reason given on `WI-0004` — it would freeze this
  item's own refinement behind delivery that is already `done`.
