---
title: Product vision — shared expenses for a friend group
version: 5
status: current
updated: 2026-08-27T02:40:28Z
updated-by: review-close
updated-for: EP-001
---

# Product vision — shared expenses for a friend group

## Who it is for

One person in a group of friends who share costs — the one who ends up keeping track. They are
comfortable at a terminal on their own machine, and they are the only person who runs the tool.
The rest of the group are names in it, not users of it.

## What it is for

Answering "who owes whom" without doing the arithmetic — and answering it as **a list of
payments that settles the group**, not as a table of who is up and who is down. The stakeholder
was asked which they meant and chose the payments: *"The list of payments that settles it — that's
what actually saves us the arguing after a trip."* The arguing is the thing being removed, so a
report the group still has to interpret would miss the point.

The person records who paid for what and who shared it, and asks the tool for that list whenever
the group wants to settle up. What has been recorded is still there the next time the tool runs,
on that machine, without any service behind it. Letting the bank's CSV export supply the expenses
instead of typing them is part of what this product is for and **is not built** — see *Still
awaited* below [src: WI-0003; tracker/items/EP-001/questions/Q-004.md].

An expense is **split equally between the people named as sharing it** — *"Equal split, keep it
simple. If a bill's uneven we'll just enter it as separate expenses."* (`WI-0001/Q-001`). The
product deliberately has no per-person amounts and no weights: an uneven bill is two entries, not
one complicated one [src: WI-0001/Q-001; expenses/store.py]. Each expense also carries a **date
and a short description**, so that a list read back weeks later says what the money was for
(`WI-0001/Q-002`), and so that a bank row's own date and description survive the import.

A record made by mistake can be **deleted** (`WI-0001/Q-003`, WI-0004). It cannot be edited in
place: the stakeholder was offered both and chose deletion, so a correction is a delete and a
re-record [src: WI-0001/Q-003; expenses/cli.py].

## What it deliberately is not

- It is not a payments tool. It says what is owed; the group settles it themselves, elsewhere.
- It is not multi-user. There is one person, one machine, one local data store — no accounts, no
  sync, no sharing of the dataset.
- It is not online. No network access, no hosted service, no bank connection; the CSV export is a
  file the person already has.
- It is not a general finance tracker. It is about costs shared between named people, not about
  budgeting, categories or reporting over time.
- It has no graphical or web interface.

## Where this came from

The stakeholder's opening statement, recorded verbatim in the journal of EP-001. Three things it
left open were put back to them as questions on that epic. Two are now settled and one is not.
Three further questions were put to them on WI-0001, and all three are answered — they are what
the two paragraphs above record.

**Settled — what the answer looks like.** A list of payments that settles the group (EP-001/Q-002).
Net positions per person were offered and not chosen; they are out of scope for WI-0002 unless
the stakeholder asks for them later.

**Settled — the order.** WI-0001 (record people and expenses, on disk), then WI-0002 (the
settlement list), then WI-0003 (the CSV import). The stakeholder delegated the order —
*"Whatever you think is best on the order"* — and it was decided on the basis that WI-0002 is
what makes the tool answer the question it exists for. They also refused to drop any of the
three: *"I don't want to drop either one, the import's part of what I asked for too."* The
importer is therefore required for this product, not optional.

**Still awaited — the bank CSV layout.** The stakeholder replied *"I'll send you a sample later."*
No layout has been invented in its place, and WI-0003 is parked until a sample of the export, or
its header row with two or three example rows, arrives. Until then this product does everything
in it except read a bank file.

## Where this ended

The engagement that built this product ended on 2026-08-27 at an **impasse**, not at completion.
Asked whether they accepted what had been delivered, the stakeholder said no:

> No, not as it stands — the bank import was part of what I asked for and it isn't there.
> Everything else looks right. I'll send the file and then we can finish it.

(`EP-001/Q-004`.) So everything above is true of a product that is **incomplete by its own
stakeholder's judgement**. Recording people and expenses, deleting a mistake, and printing the
payments that settle the group all work and were accepted; the bank CSV import does not exist
[src: tracker/items/EP-001/questions/Q-004.md; README.md]. The thing that would finish it is the
sample of the export, which restarts WI-0003 and nothing else.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 5 | 2026-08-27T02:40:28Z | review-close | EP-001 | The engagement's ending recorded (DE4): a new *Where this ended* section carrying the stakeholder's refusal to accept the product without the bank CSV import, and the *What it is for* paragraph corrected so that a reader who stops there is not told the import works — it presented the CSV export as a way expenses arrive today, which no code does |
| 4 | 2026-08-27T02:17:05Z | implement | BUG-0001 | The two absolute claims about named code — that the product has no per-person amounts and no weights, and that a record cannot be edited in place — gained resolvable inline citations, each naming the stakeholder answer that decided it and the source file where it is visible. Neither claim changed, and no paragraph was removed; ADR-0009 records why the implementing skill made this edit |
| 3 | 2026-08-26T23:44:00Z | answer-questions | WI-0001 | WI-0001/Q-001, Q-002 and Q-003 answered by the stakeholder: expenses split equally between their named sharers, each expense carries a date and a description, and a mistaken record can be deleted but not edited — the last of which added WI-0004 to the epic |
| 2 | 2026-08-26T23:30:03Z | answer-questions | EP-001 | EP-001/Q-002 and Q-003 answered by the stakeholder and Q-001 decided under their deferral: the product answers with a settlement list, the delivery order is recorded, and the CSV import is required but awaiting a sample |
| 1 | 2026-08-26T23:21:56Z | intake | EP-001 | First version, from the stakeholder's opening statement |
