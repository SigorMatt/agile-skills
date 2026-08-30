---
id: WI-0003
type: work-item
title: Delete a card
status: done
priority: medium
epic: EP-001
created: "2026-08-30T11:15:14Z"
updated: "2026-08-30T13:26:28Z"
depends-on:
  - WI-0001
arose-from: EP-001/Q-004
branch: wi/WI-0003
outcome: delivered
---

## Story

As someone studying a subject, I want to delete a card I no longer want, so that a card I entered
by mistake or no longer need stops coming up in my daily review.

## Acceptance criteria

- [x] AC1 — Running the tool's `delete` subcommand from a terminal with exactly one argument, the
      front side of an existing card typed exactly as it was entered, and answering `y` at the
      confirmation prompt AC2 describes, removes that card, prints a confirmation naming the front
      side of the card that was removed, and exits zero (`WI-0003/Q-001`, `ADR-0005`).
- [x] AC2 — Before removing anything, `delete` prints the card it is about to delete — its front,
      its back, the rung it has reached and the date it is next due, each as that card's record
      holds it in the card file — and then waits, having stated at the prompt which answers it
      takes: `y` to delete and `n` to keep. Answering `n` removes nothing, prints a message saying
      nothing was deleted, leaves the card file byte-identical to what it was before the command
      ran, and exits zero (`WI-0003/Q-002`, `ADR-0005`).
- [x] AC3 — After a confirmed deletion, the deleted card is never offered again in a review
      session: starting `review` on a calendar date on or after that card's stored due date offers
      every other due card and not that one, and the count the session states before the first
      card is one lower than the same session would have stated before the deletion. Every
      remaining card keeps its own front, back, rung and due date unchanged, which a reader can
      check by comparing the card file before and after the deletion.
- [x] AC4 — The deletion survives stopping and starting the tool: the card is absent from the
      stored file, not merely hidden, and reading that file with an ordinary text tool afterwards
      shows no record whose front side is the deleted card's. Deleting the only card in the file
      leaves a file the tool can still use: `review` run afterwards prints that nothing is due and
      exits zero, and `add` run afterwards adds a card and exits zero.
- [x] AC5 — Giving a front side that matches no card removes nothing: `delete` shows no
      confirmation prompt at all, prints a message naming the front side it did not find, exits
      non-zero, and leaves the stored file byte-identical to what it was before the command ran —
      including when the card file holds no cards, and when it does not exist (`ADR-0005`).
- [x] AC6 — Giving a front side that matches more than one card — which is possible because two
      cards may share a front (`WI-0001/Q-001`, `WI-0001` AC6) — lists every match before removing
      anything, each with both sides, its rung and its due date, numbered from 1 in the order the
      matches appear in the card file, and states at the prompt which answers it takes: the number
      of the card to remove, or `n` to remove nothing. Giving a number removes exactly that card,
      prints the AC1 confirmation, exits zero, and leaves every other match with its own front,
      back, rung and due date unchanged. Answering `n` removes nothing, leaves the card file
      byte-identical, and exits zero (`ADR-0005`).
- [x] AC7 — Input that the prompt in AC2 or the prompt in AC6 does not accept — anything other
      than what that prompt has just said it takes — removes nothing and asks the same question
      again, reprinting the card or the numbered list so that nobody is asked about text that has
      scrolled away, and saying what the prompt accepts. It is never counted as a yes and never as
      a no. The input stream ending at either prompt — Ctrl-D, or a piped input running out —
      removes nothing: the tool prints a message saying nothing was deleted, exits zero, and
      leaves the card file byte-identical.
- [x] AC8 — A card file the tool cannot parse stops `delete` before any card is shown and before
      any prompt: it prints a message naming the file and the line it stopped at, exits non-zero,
      and leaves the file byte-identical. This is the refusal `add` and `review` already make on
      the same file (`ADR-0007`, `WI-0002` AC14).
- [x] AC9 — Running `delete` with no argument, or with more than one argument, removes nothing:
      the tool prints a usage message naming the `delete` subcommand, exits non-zero, and leaves
      the card file byte-identical. Running `delete` with an argument that is empty or is only
      whitespace removes nothing and is AC5's no-match outcome, since no card's front side can be
      empty (`WI-0001` AC7).

## Out of scope

- Editing a card after it has been added. The stakeholder said explicitly that editing can wait
  (`EP-001/Q-004`), so it stays out of scope for this epic.
- Undoing a deletion, or a trash/archive from which a deleted card can be recovered. This was
  intake's exclusion and it has now been put to the stakeholder, who chose the confirmation over
  the trash — *"B — show me the card and ask first"* (`WI-0003/Q-002`). Deletion is permanent, by
  their decision rather than ours (`ADR-0005`).
- Deleting more than one card at a time, or deleting by a search or filter. AC6's several-match
  prompt removes exactly one card, the one chosen.
- Any way to skip the confirmation — no force flag, no quiet mode. The stakeholder accepted the
  prompt every time: *"One keystroke is worth it"* (`WI-0003/Q-002`). Adding a way round it later
  is their decision, not ours (`ADR-0005`).
- A command that lists or searches the cards. The stakeholder declined it in the same answer that
  chose front-side deletion — *"I don't need a numbered list for this"* (`WI-0003/Q-001`) — so it
  is not deferred work, it is out.
- Deleting a card from inside a review session. That was option C of `WI-0003/Q-001` and the
  stakeholder did not choose it, so `review` is untouched by this item: no key it accepts changes,
  and `WI-0002`'s criteria all still read true against the session after this item ships.

## Notes

Filed by `answer-questions` from the stakeholder's answer to `EP-001/Q-004`, in which they wrote:
*"I want to be able to delete a card; editing can wait."* Deletion was listed as out of scope on
EP-001 at intake — an inference, not their words — and their answer contradicted it, so the work
is recorded here rather than being folded into WI-0001 where it would be invisible on the board.

`refine` ran on this item twice. The first execution suspended it at `awaiting-answer` with two
blocking questions; `answer-questions` consumed both answers and returned it to `draft` with one
Definition of Ready failure left — AC1 and AC2 named no command. This second execution repaired
that and finished the item. `tracker/items/WI-0003/artifacts/refinement-qa.md` is the whole
record, at `status: recorded`, and Round 2 there holds what this execution decided.

What the stakeholder's two answers settled:

- **A card is named for deletion by its front side** (`WI-0003/Q-001`): *"A — by typing the front
  side. I don't need a numbered list for this."* That is AC1. The second half of the sentence is a
  decision against the listing command, not a deferral of it, so no item is filed for one and it is
  now an explicit exclusion above.
- **The tool shows the card and asks before removing it** (`WI-0003/Q-002`): *"B — show me the card
  and ask first. One keystroke is worth it to not lose a month of progress by fat-fingering a
  delete."* That is AC2, and it settles the undo exclusion this item carried as ours: they chose
  the confirmation over the recoverable trash, so deletion being permanent is now their decision.

Both are recorded together, with the reasoning, in
`docs/architecture/adr/ADR-0005-deleting-a-card-names-it-by-front-side-and-confirms.md`, which also
records the two cases they delegated: a front matching nothing (AC5) and a front matching several
cards (AC6).

**Assumed under the stakeholder's standing deferral** *"as for how it's actually built — whatever
you think is best"* (`EP-001/Q-004`), and not put to them. All of it is terminal wording and
keystrokes, all of it is reversible without migrating anything stored, and all of it is written up
in Round 2 of the Q&A:

- the operation is a subcommand named `delete` taking one argument, matching `add` and `review`;
- the confirmation takes `y` and `n`, matching the outcome prompt of `WI-0002`'s review session,
  and the prompt says so;
- the several-match prompt numbers the listed matches from 1 in card-file order and takes that
  number, or `n`; the numbers exist only inside that prompt and are not an identifier the person
  can use anywhere else, which is what `WI-0003/Q-001` declined;
- an unrecognised answer re-asks the same question (AC7), copying `WI-0002` AC13;
- the input stream ending means "delete nothing" rather than "delete" (AC7). `WI-0002`'s session
  treats it as a clean quit; here the same reflex has to be the safe outcome, because the
  irreversible act is the one being confirmed.

**Sequencing.** This item now declares `depends-on: WI-0001`, which is the plain truth — `delete`
reads and rewrites the card file WI-0001 defines and writes — and WI-0001 is `done`, so nothing is
held up by saying so. The first `refine` execution recorded this as a risk in prose because the
field was empty; the field is the better place for it. The other half of that risk is gone: option
C of `Q-001` would have made this item need WI-0002's session as well, and the stakeholder did not
choose it.

**Definition of Ready: all ten criteria pass**, per-criterion in this execution's journal entry.
Nothing here is a Definition of Ready override; no criterion was waived and the stakeholder was
asked for nothing they had not already answered.

Priority is `medium`: it is real work the stakeholder asked for, and it is not on the path to the
first useful version, which is WI-0001 followed by WI-0002 — both now `done`.

**Gaps accepted at the close** (`artifacts/review.md` `## Accepted gaps`, recorded here because
nobody reads a verification report after an item closes):

- `delete` was never run against the **default** card-file location — every test and every
  verification run set `RECALL_CARD_FILE`. It calls the same `store.card_file_path()` as `add` and
  `review`, which `tests/test_store.py` covers and this item did not touch.
- **Two processes writing at once** can still lose one of them: `delete` reads, waits at the prompt
  for as long as the person likes, then writes back the list it read. `ADR-0008`'s atomic rename
  means the loser is overwritten rather than the file corrupted. This is the whole tool's gap,
  accepted at `WI-0002`'s close, and it belongs to `recall/store.py` for every subcommand at once
  if it is ever taken on.
- **No unicode-normalisation case** was constructed. Front matching is exact equality
  (`plan.md` assumption 2), so a front differing only by normalisation form does not match; case
  and surrounding whitespace are covered by `NoMatchTests.test_a_near_miss_is_not_a_match`.
- **`Ctrl-D` was never pressed at a real terminal.** A closed pipe stands in for it, which is the
  same evidence `WI-0002` AC11 rests on.
- **The prompt does not wrap**, so a long side runs past a narrow terminal's edge. No criterion
  constrains the width; if it ever matters it is a new item.
- **AC4's "survives stopping and starting" is separate subprocess invocations**, not a reboot —
  the same limit `WI-0001` recorded for its AC2.

**Documentation repaired at the close**, as D7 and D12 obligations rather than as defects in the
code: `docs/architecture/overview.md` v5 (the two sentences saying `delete` was not yet started,
and a claim since v1 that `recall/store.py` *"appends or removes"* — it offers only `load` and
`save`, and both the append and the remove are in `recall/cli.py`) and
`docs/architecture/adr/ADR-0005-…` v2 (one `erratum`: its `## Consequences` said this item declared
no `depends-on`, which the second `refine` execution falsified).
