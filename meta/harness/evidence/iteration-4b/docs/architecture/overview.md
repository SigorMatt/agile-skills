---
title: Architecture overview
version: 9
status: current
updated: 2026-08-30T05:13:11Z
updated-by: implement
updated-for: BUG-0001
---

# Architecture overview

## The shape of it

`recall` is a command-line program with no server, no daemon and no network access. A person
types a subcommand, the process does one thing, writes to standard output or standard error, and
exits with a code that says whether it worked [src: ADR-0001]. All of its state is one JSON file
under the person's home directory [src: ADR-0004]. A card in that file carries its two sides, its
position on the interval ladder, the day it is next due [src: ADR-0002], and — once it has been
reviewed — how it went last time [src: ADR-0006].

```
bin/recall            launcher: puts the repo root on sys.path and calls recall.cli.main
recall/
  __main__.py         so `python3 -m recall` works too
  cli.py              argument parsing, exit codes, and what is printed
  deck.py             the deck and its cards as values; no file access
                      — selects the due cards; the interval ladder and the arithmetic
                        deciding when a card is next seen belong here
  store.py            reading and writing the one JSON file; no printing
tests/                unittest, invoking bin/recall as a subprocess
docs/                 this, the vision, and the ADRs
```

## Why it is split that way

Three layers, and the boundary between each pair is a rule about what that layer may not do:

- **`store.py` never prints and never decides policy.** It reads the file, or raises; it writes
  the file atomically, or raises. Keeping it silent is what lets the same load path serve all four
  subcommands — `add`, `list`, `review` and `delete` — without each of them re-deriving what a
  corrupt file means [src: recall/cli.py]. BUG-0001 gave it a second thing to classify and not to
  print: a refusal by the *operating system* — a directory that cannot be written, something
  sitting where the deck or its directory belongs — is caught at both of `store`'s boundaries and
  raised as `DeckInaccessible`, carrying the deck's own path and a reason that names whatever is
  in the way, so `cli` reads no `errno` and no exception filename and never learns that a write
  goes through a temporary file [src: ADR-0010; recall/store.py]. The outcomes of a load are
  therefore **three** rather than two: absent (an empty deck), unreadable (the contents are not a
  deck), and inaccessible (the operating system refused). Only the first is a normal state, and
  only `FileNotFoundError` produces it [src: recall/store.py; ADR-0004].
- **`deck.py` never touches the filesystem.** Cards, and the operations on them, as plain values.
  It is where the scheduling rule belongs, and WI-0003 put it there
  [src: ADR-0002; recall/deck.py]; keeping the module free of I/O is what
  lets that arithmetic be tested without a temporary directory. The ladder's four numbers exist
  there once and nowhere else, so changing them is editing one constant [src: ADR-0008]. WI-0004
  added selecting a card by its question side and removing it, and they are there for the same
  reason and in the same shape as the due-card selector: `positions_matching` returns positions
  and decides nothing about what to do with them, and `remove` constructs no card, so no
  survivor's rung, due date or order can move [src: recall/deck.py; WI-0004 AC11].
- **`cli.py` owns everything a person sees**: argument shapes, messages, and exit codes. It is
  the only layer that knows a terminal exists — and, since `review`, the only one that reads
  standard input. It now holds **two** prompt shapes, and they differ deliberately. A sitting is a
  conversation [src: ADR-0001], so `cli.py` alone holds the loop that prompts, waits, and re-asks
  when the answer is not one it recognises [src: WI-0002 AC3]; `deck.py` is handed a grade and
  never learns where it came from. A deletion asks once instead: it shows the card, reads a single
  line, and treats anything that is not a yes as a cancellation, because there the safe default
  exists and is the one the guard was asked for
  [src: ADR-0009; WI-0004/Q-002; recall/cli.py]. `cli.py` is also where the sitting says, after
  each answered card, when that card is next due
  [src: ADR-0007; tracker/items/WI-0003/artifacts/plan.md] — the sentence is `cli.py`'s and the
  date is `deck.py`'s, so the ladder's numbers never reach the layer that prints them.

The split is not free — three modules for a tool this size is more structure than the first item
strictly needs. It is here because WI-0002 and WI-0003 both add behaviour to the middle layer and
neither adds anything to the bottom one, and retrofitting the boundary later would mean moving
file access out of code that had grown around it.

## The two properties everything else serves

The stakeholder named the two ways this tool would fail them [src: EP-001/Q-001], and both are
architectural rather than cosmetic:

1. **Progress is not lost.** Hence one file the person can copy; hence writes that go through a
   temporary file and `os.replace`, so an interrupted write leaves the previous deck intact; and
   hence a deck that cannot be parsed is reported and left alone rather than replaced with an
   empty one [src: ADR-0004; WI-0001 AC8]. A field whose value is outside what the tool can act
   on counts as unparseable and is refused rather than silently corrected; that covers a card's
   recorded grade [src: ADR-0006] and, since WI-0003, its ladder position
   [src: ADR-0008; recall/store.py].
2. **A sitting does not drag on.** This is now settled, and it is settled by *not* constraining
   it. Asked whether a sitting should cap how many cards it presents, the stakeholder chose no
   cap and said how they would handle a large pile instead — they will stop part-way
   [src: WI-0002/Q-001]. So the design owes them two things rather than a limit: a sitting shows
   everything that is due [src: WI-0002 AC11], and one abandoned half-way keeps the answers
   already given [src: WI-0002 AC9]. That second obligation is why `review` saves the deck after
   every graded card rather than once at the end [src: tracker/items/WI-0002/artifacts/plan.md],
   which makes property 2 a consequence of property 1 rather than a trade against it.

## What is deliberately absent

- No database, no ORM, no configuration file, no environment variable of the tool's own
  [src: ADR-0004].
- No third-party runtime dependency [src: ADR-0003].
- No network access of any kind, and no second machine — the epic excludes syncing
  [src: docs/product/vision.md].
- No installation step; `bin/recall` on `PATH` is the whole of it [src: ADR-0005].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 9 | 2026-08-30T05:13:11Z | implement | BUG-0001 | No design change: version 8 was written at plan time and described the refusal classifier and the three load outcomes as things BUG-0001 would do. They are now built exactly as recorded, so the clause is restated as description rather than intent, names `DeckInaccessible`, and cites the code alongside the decision |
| 8 | 2026-08-30T05:05:46Z | plan | BUG-0001 | Records the shape BUG-0001's plan fixes: an operating-system refusal on the deck file is classified by `store` and raised as a deck-level exception, so `cli` reports it without reading `errno`, and a load now has three outcomes — absent, unreadable, inaccessible — where the text described two. Written at plan time, so it states what the design commits to rather than what is built |
| 7 | 2026-08-30T04:56:43Z | review-close | WI-0004 | D12 repair found in review: the `store.py` bullet said the load path serves "`add`, `list` and, later, `review`" — written when `review` was unbuilt, carried forward as a known-stale sentence by WI-0003's review, and made staler by this item, which gave it a fourth caller. It now names all four subcommands and cites `recall/cli.py`. Re-wrapped one line the previous version left over the file's width |
| 6 | 2026-08-30T04:46:40Z | implement | WI-0004 | No design change: version 5 was written at plan time and described the two prompt shapes and `deck.py`'s new selector and removal as things WI-0004 would do. They are now built exactly as recorded, so both clauses are restated as description rather than intent and cite the code alongside the decision |
| 5 | 2026-08-30T04:37:28Z | plan | WI-0004 | Records the shape WI-0004's plan fixes: `cli.py` now holds two prompt shapes rather than one — a sitting's re-asking loop and a deletion's single question where anything but a yes cancels — and `deck.py` gains selecting a card by its question side and removing it. Written at plan time, so it states what the design commits to rather than what is built |
| 4 | 2026-08-30T04:20:00Z | implement | WI-0003 | No design change: version 3 was written at plan time and described the ladder in `deck.py` and the refused out-of-range rung as things WI-0003 would do. They are now built exactly as recorded, so the two clauses are restated as description rather than intent, and cite the code instead of the plan |
| 3 | 2026-08-30T03:50:43Z | plan | WI-0003 | Records the shape WI-0003's plan fixes: the ladder and its arithmetic in `deck.py` with the four numbers in one constant, the next-due line `cli.py` prints after each answered card, and a stored ladder position outside the ladder refused like any other unreadable field. Written at plan time, so it states what the design commits to rather than what is built |
| 2 | 2026-08-30T02:38:36Z | plan | WI-0002 | Property 2 is no longer open: the stakeholder refused a cap, so the design owes them a complete sitting and a resumable one instead of a limit. Records `cli.py` as the only reader of standard input, the two card-level operations `review` adds to `deck.py`, and the `grade` field from `ADR-0006` |
| 1 | 2026-08-30T01:50:30Z | plan | WI-0001 | First version, written while planning the first item |
