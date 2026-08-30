---
id: WI-0001
type: work-item
title: Add a flashcard and have it survive a restart
status: done
priority: critical
epic: EP-001
created: "2026-08-30T11:04:20Z"
updated: "2026-08-30T12:17:47Z"
branch: wi/WI-0001
outcome: delivered
---

## Story

As someone studying a subject, I want to write down a question and its answer as a flashcard,
so that the thing I want to remember is captured in the tool instead of in my head.

## Acceptance criteria

- [x] AC1 — Running the tool's `add` subcommand from a terminal with exactly two arguments, the
      front side first and the back side second, each one line of text, adds one card, prints a
      confirmation naming the front side of the card that was added, and exits zero.
- [x] AC2 — After the process that ran AC1 has exited and the machine has been restarted, reading
      the card file with an ordinary text tool shows that card, with both sides byte-identical to
      the two arguments that were given.
- [x] AC3 — Adding three cards with different front sides keeps all three: reading the card file
      afterwards shows three separate records, none has overwritten another, and each carries its
      own front, its own back and its own scheduling state.
- [x] AC4 — The record written for a newly added card carries a due date equal to the calendar
      date on which it was added, read from the card file with an ordinary text tool. (What that
      date then causes a review session to do is WI-0002's, not this item's.)
- [x] AC5 — The card data lives in a file on the local machine, at a path stated in the project's
      documentation, and both sides of every card and its scheduling state can be read out of
      that file with an ordinary text tool while the tool is not running — no part of a card or
      its schedule is compressed, binary, or otherwise encoded such that it has to be decoded to
      be seen (`WI-0001/Q-002`, `ADR-0004`).
- [x] AC6 — Running `add` with a front side exactly equal to an existing card's front side adds a
      second, distinct card rather than refusing or replacing the first: the card file afterwards
      holds both, each with its own back side and its own scheduling state; the tool prints a
      warning saying a card with that front already exists, in addition to the AC1 confirmation;
      and it exits zero (`WI-0001/Q-001`).
- [x] AC7 — Running `add` where either argument is empty or contains only whitespace adds
      nothing: the tool prints a message naming which side was empty, exits non-zero, and the
      card file is byte-identical to what it was before the command ran (or still does not exist,
      if it did not before). This check happens before AC6's duplicate check, so an empty back
      side with a duplicate front is refused by this criterion and prints no duplicate warning.
- [x] AC8 — Running `add` when the card file does not yet exist creates it at the documented path
      and writes the card, rather than failing: after the first ever `add`, AC1 and AC2 hold.

## Out of scope

- Editing a card once it has been added. The stakeholder said editing can wait
  (`EP-001/Q-004`).
- Deleting a card. The stakeholder asked for it and it is WI-0003, not this item.
- Any grouping of cards: decks, tags, categories.
- Editing the card file by hand. The stakeholder declined it in the same breath as asking to be
  able to read it — *"I'm not asking to hand-edit it — that's a different thing"* (`WI-0001/Q-002`)
  — so the tool may rewrite or reformat the file whenever it saves and promises nothing about the
  result of an external edit (`ADR-0004`).
- Listing the cards that exist, or any command for finding a card. Nothing asks for one and
  nothing here needs one.
- Card content other than one line of text per side: no images, audio or formatting
  (`EP-001/Q-004`).
- Showing, reviewing or rescheduling cards — that is WI-0002. This item only records that a new
  card is due on the day it was added; the rule that moves that date afterwards is
  `ADR-0002-scheduling-binary-ladder.md`.

## Notes

The four questions this item was waiting on at intake have been answered by the stakeholder, and
the criteria above have been rewritten from their answers. What each answer settled:

- **The surface is a command line** (`EP-001/Q-001`): *"Command-line is fine — it's just me, once
  a day at a terminal, running through vocab."* Recorded as
  `docs/architecture/adr/ADR-0001-command-line-delivery-surface.md`.
- **A card is a front and a back, one line of text each** (`EP-001/Q-004`): *"A card's just a
  front and a back, one line of text each — nothing fancy."* That is AC1, and it answers the
  question intake left open about whether a card carries anything beyond a question and an answer.
- **Storage is a file on the machine that survives a reboot** (`EP-001/Q-004`): *"It needs to live
  in a file on my machine that survives a reboot."* AC2 and AC5 are written against that sentence
  — AC2 now says the machine is restarted, not merely the tool, because that is what they asked
  for.
- **A new card is due the day it is added** — the architect's inference from `EP-001/Q-003`'s
  due-date rule, not the stakeholder's words. Recorded with its basis in
  `docs/architecture/adr/ADR-0002-scheduling-binary-ladder.md`.

`refine` ran on this item on 2026-08-30 and suspended it at `awaiting-answer` with two blocking
questions to the stakeholder. **Both are now answered** and `answer-questions` has taken them into
the criteria above. `tracker/items/WI-0001/artifacts/refinement-qa.md` is the record of that
conversation and is now at `status: recorded`.

What the stakeholder's two answers settled:

- **A duplicate front side is added, with a warning** (`WI-0001/Q-001`): *"C — add it and warn me.
  I don't want it refusing a second meaning of a word, and a warning is enough to catch a typo."*
  That is AC6, which is new, and it is why AC3 now speaks of three cards with **different** fronts
  — the two criteria cover the two cases separately rather than one of them silently.
- **The card file is readable text that the tool owns** (`WI-0001/Q-002`): *"B. I want to be able
  to open it and see my cards are still there, but I'm not asking to hand-edit it — that's a
  different thing."* AC5 was intake's own promise, written ahead of their decision and flagged at
  the time as something to put to them; their answer confirms it, so AC5 stands and is now
  sharpened to say what "readable" excludes. Hand-editing is out of scope above. The commitment is
  recorded as `docs/architecture/adr/ADR-0004-card-file-is-readable-text-owned-by-the-tool.md`,
  because it binds every later version and not only the first.

One consequence reaches beyond this item: because two cards may share a front side, deleting a
card by typing its front (`WI-0003/Q-001`) can match more than one. That is WI-0003's to settle
and it is not a gap here — AC6 requires the two cards to be separate records, which is what makes
any resolution there possible.

Settled by `refine` under the stakeholder's standing deferral *"as for how it's actually built —
whatever you think is best"* (`EP-001/Q-004`), and **not** put to them, because that answer covers
the category and re-asking would ignore it. Each is reversible, each is recorded with its basis in
the Q&A file, and each is now written into a criterion rather than living only in this section:

- The add operation is a subcommand named `add`, with the front and the back given as two
  arguments, front first — one line of typing, no prompt. That is AC1. The executable's own name
  is still `plan`'s, which is why no criterion names it.
- A card with an empty or whitespace-only side is refused with a message naming which side, a
  non-zero exit, and nothing written. That is AC7, which also fixes its precedence over AC6 —
  validation first, so an empty back with a duplicate front is refused and prints no duplicate
  warning. Nobody stated that order and two criteria could otherwise both claim the case.
- The card file is created on first use rather than having to exist already. That is AC8. It is
  the same deferral and it was previously unstated anywhere, which made AC1 undecidable on a clean
  machine — the commonest way anyone will first run this.
- The confirmation names the card that was added, so a mistyped front is visible at once. AC1
  requires it to name the front side; the exact wording is `plan`'s and `implement`'s.

**Deliberately left unconstrained, by `refine`, under the same deferral:** what the tool does when
`add` is given the wrong number of arguments. It gets a usage message and a non-zero exit, which is
what every command-line tool does and what the stakeholder delegated; which message, and whether
the usage text is printed on stdout or stderr, is `plan`'s and `implement`'s. It is named here
rather than as a criterion because no observation of it would tell anyone whether this item
delivered what was asked for.

Definition of Ready: **all ten criteria pass**, criterion by criterion, and the evidence is in this
item's journal entry for the `refine` execution of 2026-08-30 that moved it to `ready`. The two
that were failing when the item resumed have been repaired here — R4, by rewriting AC1 to name the
`add` subcommand and its two arguments and by rewriting AC2 to AC4 to name the observation that
settles each, and R10, by turning the empty-side assumption into AC7 with its precedence over AC6
stated, adding AC8 for the file that does not exist yet, and naming the argument-count case above
as deliberately unconstrained. Nothing here is a Definition of Ready override: no criterion was
waived and the stakeholder was not asked to waive one.

`EP-001/Q-005` has been answered and never blocked this item: it was about how many cards a review
session shows, which is WI-0002's concern.

### Carried out of review, 2026-08-30

`review-close` accepted this item and merged it. Four things survive it, recorded here because
once an item is `done` nobody reads its reports again. The full reasoning is in
`tracker/items/WI-0001/artifacts/review.md`.

- **AC2's machine restart was never performed.** No machine can be restarted inside a pipeline
  run. What was accepted in its place: a separate process read the file's exact bytes after the
  writing process had exited, and `strace -f -e trace=fsync,rename` on a real `add` shows
  `fsync` → `rename` → `fsync`, so the file and its directory entry are both flushed before the
  command exits. The criterion is ticked on that substitution, which `plan`, `implement` and
  `verify` each declared. If anyone reads AC2 as requiring a literal reboot, the wording is what
  needs revisiting with the stakeholder — the implementation is not what would change.
- **Two `recall` processes writing at the same moment are unexercised.** No criterion mentions
  concurrency and `ADR-0001` fixes the tool as single-user. The rename-based save makes a torn
  file unlikely, not impossible.
- **A filesystem with no directory `fsync`, and non-UTF-8 arguments, are unexercised.**
  `store._fsync_directory` swallows the error, so a save on such a filesystem completes with a
  weaker durability guarantee than `ADR-0008` describes. No criterion names either case.
- **`cli.main()` does not dispatch on the subcommand it parsed** — it calls `add()`
  unconditionally, which is correct while `add` is the only one registered and `argparse` refuses
  the rest with exit `2`. WI-0002 adds the second subcommand and must change that line; left as
  it is, a `review` command would silently run `add`. Recorded for WI-0002's plan, not filed as a
  defect against this item, because nothing this item promised is affected.
