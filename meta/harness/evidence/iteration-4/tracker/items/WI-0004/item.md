---
id: WI-0004
type: work-item
title: Delete a card that was added by mistake
status: done
priority: medium
epic: EP-001
created: "2026-08-29T13:18:40Z"
updated: "2026-08-29T13:58:30Z"
arose-from: EP-001/Q-005
branch: wi/WI-0004
outcome: delivered
---

## Story

As someone keeping a pile of flashcards, I want to delete a card I added by mistake, so that a
typo or a duplicate stops coming round in my daily review without my having to hand-edit the
store file.

## Acceptance criteria

Every criterion below is checked by running `recall` with `RECALL_FILE` pointing at a store the
checker controls, and by reading that file afterwards — the same way `WI-0001` AC5 and `WI-0003`
were checked. A card is named by the number `recall list` prints for it.

All ten criteria are settled. `AC2` was open until the stakeholder answered `Q-001` with
option C — *"just delete it and tell me what got deleted. I'm only ever going to run this right
after I typo'd something, I don't need a prompt in my way for that."* [src: WI-0004/Q-001] —
which fixes the command as acting immediately, with no confirmation prompt, and printing what it
removed.

- [x] AC1 — with a store holding cards 1, 2 and 3, `recall delete 2` exits 0 and prints one line
      on stdout naming the card it deleted; a later run of `recall list` prints cards 1 and 3
      and no card 2
- [x] AC2 — `recall delete <n>` acts immediately and never asks: run against a store holding
      cards 1, 2 and 3 with nothing on stdin — `recall delete 2 < /dev/null` — it exits 0 without
      waiting for input, writes nothing on stderr, and writes **exactly one line** on stdout,
      which contains the number `2`, card 2's question text, and card 2's answer text
      [src: WI-0004/Q-001]
- [x] AC3 — deleting a card leaves every other card untouched: after AC1's deletion, cards 1
      and 3 have the same `number`, `question`, `answer`, `due` and `interval` values in the
      store file as they had before, and no card is renumbered
- [x] AC4 — a card that has been deleted is never offered again: with a store holding one card
      due today, `recall delete 1` followed by `recall review` prints the nothing-is-due line and
      exits 0
- [x] AC5 — `recall delete 9` against a store with no card 9 exits non-zero, prints a message on
      stderr naming the number, prints nothing on stdout, and leaves the store file byte-identical
- [x] AC6 — `recall delete 1` with no store file at all exits non-zero, prints a message on
      stderr, and creates no file
- [x] AC7 — deleting the last remaining card leaves a store the tool still reads: `recall list`
      afterwards prints the nothing-stored line and exits 0, and `recall add` afterwards exits 0
- [x] AC8 — a wrong command line exits non-zero with a usage line on stderr and changes nothing
      on disk, for each of: `recall delete` with no argument, `recall delete 1 2`, `recall delete
      two`, and `recall delete 0`
- [x] AC9 — a store the tool cannot read is refused rather than repaired: `recall delete 1`
      against a file that is not valid JSON exits non-zero, reports it on stderr naming the path,
      and leaves the file byte-identical, as `ADR-0004` requires of every command
- [x] AC10 — `README.md` documents the command in its `## Commands` section, in the same form as
      `add`, `list` and `review`, including what happens when the number names no card

## Out of scope

- **Editing a card** after it is added. The stakeholder ruled on this in the same answer that
  asked for deletion: *"editing can wait"* [src: EP-001/Q-005]. It stays out of scope for
  EP-001.
- A command to see or change a card's schedule, and any statistics, streaks or retention
  reporting — both declined in the same answer [src: EP-001/Q-005].
- **Undoing a deletion**, a trash or archive state, and any way to get a deleted card's earned
  schedule back. A deletion is final; the store file is the only backup, and copying it is the
  user's business. Assumed by `refine`, not asked — but stated in `Q-001`'s context, and the
  stakeholder answered that question without objecting to it and gave the reason it does not
  bite for them: *"I'm only ever going to run this right after I typo'd something"* — a card
  deleted seconds after it was added has no earned schedule to lose [src: WI-0004/Q-001]. Still
  an assumption, not a decision they were asked for.
- Deleting more than one card in one invocation, deleting by matching the card's text, and
  deleting every card at once. `recall delete` takes one number.
- Any change to how `add`, `list` or `review` behave on a store that has never had a deletion.

## Notes

### Why this item exists

The stakeholder answered `EP-001/Q-005` with option B: they accepted the engagement and named
exactly one follow-up — *"the one thing from your list I actually want next is being able to
delete a card I added by mistake"* [src: EP-001/Q-005]. `EP-001`'s `## Out of scope` had
anticipated it: *"Editing or deleting cards after they are added … if the stakeholder wants it
now they can say so and it becomes a new item."*

### Decided during refinement without asking, and on what authority

Recorded in full in `artifacts/refinement-qa.md`. In short: the command is `recall delete <n>`,
taking exactly one positional argument, the card number `recall list` prints — decided under the
stakeholder's standing deferral on `WI-0001/Q-002` (*"whatever you think is best"*, which
answers the category of naming, output wording, exit codes and file layout) together with
`ADR-0005`, which fixed the positional-only argument surface and the stream split.

### Open design questions, left for `plan` — not for the stakeholder

1. **Whether a deleted card's number is ever reused.** `ADR-0004` derives the next card number
   from the largest `number` present, and weighed that against a premise this item removes: it
   recorded the reuse cost as low *"because nothing in the epic deletes a card"* [src: ADR-0004].
   It now does. Delete the highest-numbered card and the next card added takes its number, so one
   number can name two different cards over the life of a store. `ADR-0004` is left as written —
   an ADR records what was believed when it was decided — so `plan` must weigh its option F
   against its option G again here rather than reading that risk line as settling it. **No
   criterion above constrains this either way**, deliberately: it is visible here rather than
   decided, which is what R10 asks for. `refine` left it open.
2. **Which exit code a number that names no card gets.** `ADR-0005` assigns `2` to a wrong
   command line and `1` to a usable command line against a store that cannot be used; `recall
   delete 9` against a readable store holding cards 1–3 is neither. AC5 and AC6 therefore say
   *non-zero* — which is decidable — and leave the value to `plan`, which may need to extend
   `ADR-0005`. `refine` left it open.
3. **Whether the store's `version` changes.** Deleting removes a card object and adds no field,
   so nothing in `ADR-0004` or `ADR-0007`'s schema changes shape; `plan` should confirm that and
   say so rather than bumping it by reflex. `refine` left it open.

### Accepted gaps, recorded at close by `review-close`

Six things were accepted rather than fixed. They are here, not only in the reports, because
nobody reopens a closed item's reports.

1. **`ADR-0004` still says "nothing in the epic deletes a card".** The epic now does, and the
   number reuse that option F called a hand-editing curiosity is reachable from the command line.
   The sentence sits in `## Options considered`, which is a record of the reasoning at the time,
   and `ADR-0008` was written to re-weigh exactly that premise and kept option F — so this was
   decided, not overlooked. What remains is that the link runs one way: `ADR-0008` cites
   `ADR-0004`, and `ADR-0004`, marked `status: current`, points nowhere. The fix is a forward
   pointer with a version bump and a change-log row, which is an architect's call
   [src: docs/architecture/adr/ADR-0004-card-store-schema-and-write-protocol.md; src: ADR-0008].
2. **`artifacts/impl-report.md` overstates its mutation evidence.** It attributes its mutation A
   to `AC5` and lists `AC5` among the tests its mutations turned red; re-running that mutation
   turns red only `AC6`'s test. `AC5`'s delivered behaviour is correct and was demonstrated
   directly. The defect is in the report's evidence section, not the code
   [src: tracker/items/WI-0004/artifacts/verify-report.md].
3. **`AC5`'s test cannot tell a correct implementation from a crashing one**, which is why the
   point above went unnoticed. `test_a_number_that_names_no_card_is_refused_and_changes_nothing`
   passes against code that raises `TypeError`: a traceback exits non-zero, the crash precedes the
   stdout write, a spurious `save` of an unmodified document is byte-identical, and
   `assertIn("9", stderr)` is satisfied by the traceback's line numbers. The narrow fix is to
   assert the message — `there is no card 9` — or to assert that `Traceback` is absent
   [src: tracker/items/WI-0004/artifacts/verify-report.md].
4. **`AC3` was exercised only on a two-survivor store.** `delete_card` pops by index so position
   should be irrelevant, but the evidence for that is the design, not a run
   [src: tracker/items/WI-0004/artifacts/plan.md].
5. **Argument shapes no criterion names** — `01`, `+1`, `" 1"`, `1.0`, and digits from other
   scripts — are refused with exit `2` by `_card_number`, as the plan's declared assumption said
   they would be, but only the shapes `AC8` names were exercised
   [src: tracker/items/WI-0004/artifacts/plan.md].
6. **Concurrent invocations, an interrupted write, and a filesystem failing mid-write** are
   unverified. `ADR-0004`'s write protocol is inherited unchanged and no criterion here touches
   it [src: ADR-0004].

### Not a work item

The stakeholder declined, explicitly, to treat the one gap disclosed at sign-off as work: a
hand-edited store containing the JSON number `1.0` where `1` is expected is read rather than
refused. *"That `1.0` thing in the store file doesn't bother me — I'm not hand-editing it often
enough to hit it."* [src: EP-001/Q-005] No item covers it and none should.
