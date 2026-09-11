---
title: Product vision — envelope budgeting from the command line
version: 10
status: current
updated: 2026-09-11T19:17:34Z
updated-by: review-close
updated-for: EP-001
---

# Product vision — envelope budgeting from the command line

## Who this is for

A person who budgets their own money and is comfortable at a terminal. They already think in
envelopes — this much for groceries, this much for fun — and they want the arithmetic kept for
them rather than being taught a method.

It is for one such person, on one machine — the stakeholder themselves, for their household
budget, and nobody else [src: EP-001/Q-001]. What they use today is a spreadsheet with a tab per
month; they said it works and is tedious [src: EP-001/Q-001]. That is the thing this tool is
measured against: it has to be quicker to type than a spreadsheet row, and it has to keep the
same figures.

## What it is for

Four things, in the order they happen:

1. Naming envelopes and putting income into them.
2. Recording a spend against the envelope it came out of.
3. Seeing what is left in each envelope.
4. Looking at a summary of a month.

And two more the stakeholder asked for once they saw the shape of it [src: EP-001/Q-005]: moving
an amount from one envelope to another, and correcting a spend that was already recorded. Moving
money is what they want to do when an envelope runs short, because they chose to have an
overspend refused rather than shown as a negative envelope [src: EP-001/Q-002]. Correcting is
what they want when they mistype, and they asked for the correction to replace the entry, so that
a summary of a past month shows the corrected figure and not both figures [src: EP-001/Q-005].

Refining the correction has since told us how far it reaches. What follows was decided by the
stakeholder, question by question; the citation on a sentence names the answer it came from. A
correction reaches an income as well as a spend — they declined a
negative income on the understanding that proper corrections were coming, and said so again when
asked [src: WI-0005/Q-005]. On a spend it reaches the amount, the date, the description and the
envelope it came out of, because *"if I typed the line wrong I want to fix the line"*
[src: WI-0005/Q-002]. A spend recorded twice can be removed outright, by a command that says what
it took out and what the envelope holds afterwards [src: WI-0005/Q-003]. A correction that would
take an envelope below zero is refused and says how short the envelope is, which is the overspend
rule of `EP-001/Q-002` applied to a second moment they had not been asked about
[src: WI-0005/Q-004]. Moving money between envelopes stays outside what a correction can touch,
which the stakeholder reaffirmed twice while settling the rest [src: WI-0005/Q-002;
WI-0005/Q-005].

A second round of refinement settled how far a correction reaches into an income, and the
stakeholder settled it against their own earlier sentence rather than leaving the choice to us. A
correction changes an income's amount and the envelope it went into, and stops there —
*"income has two of those and a spend has four, and that is the whole of the difference"*
[src: WI-0005/Q-006]. It does not set a date on an income: they declined to give income a date
when `envel add` was being refined [src: WI-0003/Q-003] and declined again to let it acquire one
through the correction command [src: WI-0005/Q-006], so which month an income counts in stays the
month it was typed in. An income recorded twice can be removed, by the same command that removes
a spend and without an extra flag, because the mistake they had in mind was the duplicate rather
than the shop [src: WI-0005/Q-007]. A removal that would leave an envelope short of what has
already been spent from it is refused with the shortfall named, which is the rule they gave at
[src: WI-0005/Q-004] reaching a moment that answer did not itself cover [src: WI-0005/Q-007].

A month that has already ended can still close short, and the stakeholder has said what the tool
does about it. It arises from two of their own decisions meeting: a spend counts in the month it
happened, because they asked to be able to date one [src: WI-0002/Q-001], while income counts in
the month it was typed and carries no date of its own [src: WI-0003/Q-003]. So typing last month's
shopping in after this month's income has been recorded can take that month's own closing figure
below zero, even though what the envelope holds today is right. Shown this, they kept the spend
and refused the minus sign: `envel entries` and `envel summary` say how short the month closed, in
words, rather than printing a negative — *"'Groceries was 250.00 short at the end of 2026-08'
tells me exactly what I need and still gives me the figure"* [src: BUG-0001/Q-001]. The figure
stays readable on purpose, because that is what they meant by the rule about a report adding up:
*"a figure I can read is what the adding-up rule was about; a minus sign in front of it is what I
don't want"* [src: BUG-0001/Q-001]. They declined the two alternatives that would have changed how
they work — refusing the backdated spend, and giving income a date, which they had declined at
[src: WI-0003/Q-003] and again at [src: WI-0005/Q-006].

That sentence brackets a listing at either end of a month, and the stakeholder has now seen it in
both places. A listing of a month an envelope started short opens with the same words —
*"groceries was 250.00 short at the start of 2026-09"* [src: envel/summary.py:237] — and shown
that line as one of two wordings the pipeline had chosen for itself, they kept it: *"reads fine to
me"* [src: EP-001/Q-009]. The second wording, the `left` column of an `envel summary` row for a
month that closed short, reads `short 250.00` and is still the pipeline's own: offered the change,
they declined to spend a round on it and parked it with the rest of the monthly summary
[src: EP-001/Q-009].

An entry is named by a short reference the tool prints and the person types back, read off the
listing rather than remembered [src: WI-0005/Q-001] — off one envelope's entries, or off the
month's across the envelopes, because they later asked for the envelope to be optional for
exactly the case where they cannot name one [src: WI-0006/Q-003]. That is what makes
a correction possible at the moment they actually catch a mistake — *"a couple of days after the
month has ended with the statement in front of me"* — and it is the reason the listing itself is
work this tool needs rather than work nobody asked for.

That reference is one number counted once across everything recorded, rather than a number
counted within each envelope, so a number on its own names at most one entry whichever envelope
that entry sits in [src: WI-0005/Q-008]. The stakeholder chose it for the case they had already
described — a figure on a statement they cannot place, which is the moment the envelope is the
thing they do not know [src: WI-0006/Q-003] — and the number an entry is given stays that
entry's, so a number written down last week still means what it meant [src: WI-0005/Q-008].

That listing is the seventh thing the tool does, and the stakeholder confirmed they wanted it
when they were offered the chance to close it: *"I meant reading those notes back, and when I am
checking a month against the statement I need to see what is behind an envelope's balance"*
[src: WI-0006/Q-001]. It shows income, spends and moves together, with the kind named on the
line, so that the lines add up to the balance — they said the rule they had given about the
monthly summary travels, *"a list I cannot add up costs me an evening whichever report it is on"*
[src: WI-0006/Q-004]. It covers one month, the current one unless another is named, spelled the
way `envel summary` spells a month [src: WI-0006/Q-002], and the envelope is optional, because
the case they described is a figure on a statement they cannot place [src: WI-0006/Q-003].

The monthly summary is untouched by that, and the distinction is the stakeholder's own. They
refused individual spends in the summary at `EP-001/Q-003`, and repeated it while asking for the
listing: *"It does not reopen the monthly summary — I still don't want individual spends in
that"* [src: WI-0006/Q-001]. One report is four figures per envelope; the other is the entries
themselves, asked for by name.

The tool's job is to make those things quick to do and to remember them between runs. It is a
ledger with opinions about where money is allocated, not an adviser: it records what the person
decides and shows them the consequences.

An envelope's balance carries over. Money left in an envelope when a month ends is still in that
envelope when the next month starts, and the stakeholder named this as the point of budgeting
this way [src: EP-001/Q-001]. It is why the summary's **last** column is a balance rather than a
monthly remainder — the fourth of the four figures in a row
[src: WI-0003 AC2 "each row shows four figures for that"] — and it is the rule they said they
would least want us to get wrong. It was written as the third column, and was, until they asked
for a figure showing what had been moved between envelopes and put it ahead of the balance
[src: WI-0003/Q-001]. Only the place in the row moved; what the column is has not changed.

The command is `envel` [src: EP-001/Q-006].

Two constraints came from the stakeholder in their own words — "Python, no services" and "data
must survive between runs" — and they are treated as requirements rather than preferences. In
practice that means the tool starts, does one thing, and exits, leaving its data on the local
machine; nothing runs between invocations.

## What it deliberately is not

- Not multi-user and not shared. One person, one set of envelopes, one machine.
- Not connected to anything: no server, no sync, no bank import, no network.
- Not an adviser: no forecasts, no goals, no recommendations about how money should be split.
- Not a general finance tool: one currency, no conversion, no investments, no tax.
- Not a screen to sit in: no graphical, web or full-screen terminal interface.

## Engagement state

- The engagement has ended, and the ending is **E1, delivered**. Seven items were opened under
  `EP-001` [src: EP-001] and each closed with `outcome: delivered`: `WI-0001` [src: WI-0001],
  `WI-0002` [src: WI-0002], `WI-0003` [src: WI-0003], `WI-0004` [src: WI-0004], `WI-0005`
  [src: WI-0005], `WI-0006` [src: WI-0006] and `BUG-0001` [src: BUG-0001], the last of them a
  defect the pipeline found in its own delivered behaviour rather than one the stakeholder
  reported.
- The stakeholder was asked whether they accept the engagement as it stands, at `EP-001/Q-009`
  [src: EP-001/Q-009], once it had reached rest, and they answered: *"Ship it as it stands"*
  [src: EP-001/Q-009]. That reply is what determined this ending.
- Thirty-five questions were filed across the engagement and each is `answered`. None was
  deferred and none was abandoned, so nothing in this record stands on an ask that went
  unanswered [src: EP-001].
- What the stakeholder parked is further work, not product: the monthly summary, including the
  one wording change the sign-off put in front of them [src: EP-001/Q-009]. Everything this
  document describes, `envel summary` among it, was built and shipped.
- `review-close` restated this section when it recorded the ending, on 2026-09-11. Nothing
  rewrites it now; a further round of work would begin with a request under `tracker/requests/`,
  which reopens the epic.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 10 | 2026-09-11T19:17:34Z | review-close | EP-001 | `## Engagement state`: restated at the ending, which is **E1, delivered**. The four sentences it held were written by `intake` at the start and each had become false: the engagement has not just begun, the first round of questions was answered on 2026-09-11, and the stakeholder has now been asked to accept the engagement and has done so at `EP-001/Q-009`. Restated from the ending rather than repaired along the way, which is why they stood false for the whole engagement — they are the ending's to write and nobody else's (`spec/doc-header.md` §4a). This is the only section of this document this execution touched; the product prose above it is unchanged, including the paragraph version 9 added under `EP-001/Q-009`. |
| 9 | 2026-09-11T19:11:25Z | answer-questions | EP-001 | `## What it is for`: one paragraph added, recording what the stakeholder settled at `EP-001/Q-009`. The sign-off named two printed sentences as ours rather than theirs; their reply settles one and parks the other. The opening line of a listing for a month an envelope started short — *"groceries was 250.00 short at the start of 2026-09"* — is now theirs, kept in their own words [src: EP-001/Q-009], and the `left` column's `short 250.00` is recorded as still the pipeline's own rather than quietly promoted to theirs. Nothing already in the document was rewritten. In particular the paragraph sourced to `BUG-0001/Q-001` about a month closing short stands as they gave it — this answer approves a second place that rule is printed, it does not reinterpret the rule — and the summary paragraphs sourced to `EP-001/Q-003` and `WI-0006/Q-001` stand untouched, because their sentence *"I asked for it at the start and I've changed my mind"* is them overtaking their own earlier want and is theirs to have said, not ours to edit into the record of what they wanted then. `## Engagement state` was left untouched — it belongs to the ending. |
| 8 | 2026-09-11T11:07:09Z | answer-questions | BUG-0001 | `## What it is for`: one paragraph added, recording what the stakeholder settled at `BUG-0001/Q-001` — a month that has already ended can close short, and the shortfall is said in words on the closing line of `envel entries` and in the `left` column of an `envel summary` row rather than printed as a minus. Their condition that the figure stay readable is quoted with it, and the two alternatives they declined are named with the answers that declined them [src: WI-0003/Q-003] [src: WI-0005/Q-006]. Nothing already in the document was rewritten: the paragraph sourced to `WI-0005/Q-004` about a below-zero correction being refused is about what an envelope holds now, which this answer does not touch, and the paragraph sourced to `WI-0006/Q-004` about the lines adding up stands as they gave it — this answer is the stakeholder reconciling it with their own no-minus rule, not us reinterpreting it. `## Engagement state` was left untouched — it belongs to the ending. |
| 7 | 2026-09-11T08:22:40Z | implement | WI-0006 | `## What it is for`: the sentence about the printed reference said it is *"read off a listing of an envelope's entries"*, which was our paraphrase of the example in front of the stakeholder at `WI-0005/Q-001` [src: WI-0005/Q-001] — `envel spends groceries`, before the envelope was optional. This item delivers the listing, and the envelope is optional because they asked for it to be [src: WI-0006/Q-003], so the clause now names both forms. Their two answers are not in conflict and neither was reinterpreted: `Q-001` settled that there is a printed reference, `Q-003` settled whether an envelope must be named. Nothing else was rewritten — in particular the paragraph sourced to `WI-0006/Q-004` about the lines adding up stands as they gave it, and the decision that the all-envelopes form prints no opening and closing figure is `refine`'s, recorded at [src: WI-0006 AC10 "it prints"] under no delegation rather than written in here as though it were theirs. `## Engagement state` was left untouched — it belongs to the ending. |
| 6 | 2026-09-11T07:49:39Z | answer-questions | WI-0005 | `## What it is for`: two paragraphs added, recording what the stakeholder's three round-2 answers on `WI-0005` settled — a correction reaches an income's amount and its envelope and does not set a date on one (`Q-006`), an income recorded twice can be removed by the same command as a spend (`Q-007`), and the reference is one number counted once across everything recorded rather than within an envelope (`Q-008`). Nothing already in the document was rewritten: the sentence sourced to `WI-0005/Q-005` about corrections reaching income still says what it said, and the `WI-0005/Q-001` paragraph about the printed reference is untouched — `Q-008` decides what the number counts, not whether there is one. `## Engagement state` was left untouched — it belongs to the ending. |
| 5 | 2026-09-11T07:33:50Z | answer-questions | WI-0006 | `## What it is for`: two paragraphs added for the listing the stakeholder confirmed at `WI-0006/Q-001` — what it shows (`Q-004`), the month it covers (`Q-002`), the optional envelope (`Q-003`), and their own statement that it does not reopen the monthly summary. Nothing already in the document was rewritten; the sentence sourced to `EP-001/Q-003` about the summary stands, and the new paragraph quotes their restatement of it rather than editing it. `## Engagement state` was left untouched — it belongs to the ending. |
| 4 | 2026-09-11T07:28:24Z | answer-questions | WI-0005 | `## What it is for`: two paragraphs added, recording what the stakeholder's five answers on `WI-0005` settled about how far a correction reaches — income as well as spends (`Q-005`), the amount, date, description and envelope of a spend (`Q-002`), removing a spend outright (`Q-003`), a below-zero correction refused with the shortfall named (`Q-004`), and a short printed reference as the way an entry is named (`Q-001`). Nothing already in the document was rewritten: the sentence sourced to `EP-001/Q-005` still says what it said, and these paragraphs sit after it. `## Engagement state` was left untouched — it belongs to the ending. |
| 3 | 2026-09-11T06:38:45Z | implement | WI-0003 | `## What it is for`: the balance is the summary's **last** column, the fourth of four, and not the third. It was the third when this was written and `WI-0003/Q-001` put the moved figure ahead of it [src: WI-0003/Q-001]; the claim the sentence makes — that the column is a balance and not a monthly remainder — is what this item delivers and is unchanged, so only the ordinal was repaired. `## Engagement state` was left untouched — it belongs to the ending. |
| 2 | 2026-09-11T02:15:30Z | answer-questions | EP-001 | The stakeholder's first round of answers propagated: who it is for and what they use today are now known rather than unknown (`Q-001`); balances carry over between months (`Q-001`); moving money and correcting a spend are in scope (`Q-005`); an overspend is refused rather than shown negative (`Q-002`); the command is `envel` (`Q-006`). `## Engagement state` was left untouched — it belongs to the ending. |
| 1 | 2026-09-11T01:59:19Z | intake | EP-001 | First version: who the tool is for, the four things it does, what it deliberately is not, and the engagement's opening state. |
