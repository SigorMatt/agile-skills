---
id: WI-0004
type: work-item
title: Delete a person or an expense recorded by mistake
status: done
priority: medium
epic: EP-001
created: "2026-08-26T23:42:32Z"
updated: "2026-08-27T01:44:25Z"
arose-from: WI-0001/Q-003
depends-on:
  - WI-0002
branch: wi/WI-0004
outcome: delivered
---

## Story

As the person keeping track of the group's costs, I want to delete a person or an expense I
recorded by mistake, so that a typo does not sit in every who-owes-whom answer for ever and I
never have to hand-edit the data file to get rid of it.

## Acceptance criteria

Every criterion below names a command and the observation that settles it, so that someone with
a terminal and no context reaches the same verdict. The commands are `person delete <NAME>` and
`expense delete <NUMBER>`, where `<NUMBER>` is the 1-based position printed by `expense list`
(see `## Notes`, D1 and D2). `TWO-EXPENSE STORE` below means, exactly, this sequence run against
an empty store:

    python3 -m expenses person add Ana
    python3 -m expenses person add Ben
    python3 -m expenses expense add --amount 30 --paid-by Ana --shared-by Ana,Ben \
        --date 2026-08-01 --description Taxi
    python3 -m expenses expense add --amount 10 --paid-by Ben --shared-by Ana,Ben \
        --date 2026-08-02

- [x] AC1 — deleting a person nobody's expenses name. With `Ana` and `Ben` added and no expenses
      recorded, `python3 -m expenses person delete Ben` exits 0 and its stdout is exactly
      `deleted Ben` followed by a newline; `python3 -m expenses person list` then exits 0 and its
      stdout is exactly `Ana` followed by a newline.

- [x] AC2 — deleting an expense, and the renumbering that follows. Against the TWO-EXPENSE STORE,
      `python3 -m expenses expense list` exits 0 and prints two lines whose first
      whitespace-separated fields are `1` and `2`, in that order, the rest of each line being what
      WI-0001 AC3 already requires. `python3 -m expenses expense delete 2` then exits 0 with
      stdout exactly `deleted expense 2` and a newline, and `expense list` afterwards prints
      exactly one line, beginning `1`, for the 30.00 taxi. Deleting that one too — `expense
      delete 1` — exits 0 and `expense list` afterwards prints exactly `no expenses`.

- [x] AC3 — deleting a person named in an expense is refused, and nothing changes. This is the
      stakeholder's decision on Q-001, option A. Against the TWO-EXPENSE STORE, in which `Ben` is
      the payer of one expense and a sharer in both:
      `python3 -m expenses person delete Ben` exits non-zero, prints nothing at all to stdout, and
      writes to stderr a message containing both `Ben` and `2` — the count of expenses naming him.
      The `md5sum` of the data file is byte-identical before and after, and `person list` still
      prints `Ana` and `Ben`. The same holds for `person delete Ana`, who is the payer of one
      expense and a sharer in both, with a message containing `Ana` and `2`. The message must
      name the count, not merely refuse: the stakeholder accepted the extra commands on the basis
      of being told what stands in the way.

- [x] AC4 — the refusal is about the expenses, not about the person. Against the TWO-EXPENSE
      STORE, running `expense delete 1` and then `expense delete 1` again (the second removing
      what the renumbering made expense 1) leaves no expenses; `python3 -m expenses person delete
      Ben` then exits 0 with stdout exactly `deleted Ben`, and `person list` prints exactly `Ana`.
      Without this criterion an implementation that refused every person-deletion would satisfy
      AC3.

- [x] AC5 — deletions survive the process exiting. After AC1's `person delete` and after AC2's
      first `expense delete`, running the corresponding listing in a **fresh** `python3 -m
      expenses` process prints stdout byte-identical to the listing run immediately after the
      deletion.

- [x] AC6 — the settlement follows the deletion, and the refusal keeps it correct. Against a
      store holding `Ana`, `Ben` and one 30.00 expense paid by `Ana` shared by both,
      `python3 -m expenses settle` exits 0 and prints exactly `Ben pays Ana 15.00`. After
      `expense delete 1` it exits 0 and prints exactly `no payments needed`. Against the same
      store before that deletion, `person delete Ben` is refused per AC3 and `settle` afterwards
      prints `Ben pays Ana 15.00` byte-identically to before the attempt — so no sequence of
      commands leaves `settle` computing over an expense that names somebody `person list` does
      not show.

- [x] AC7 — deleting something that is not there is refused and changes nothing. Against the
      TWO-EXPENSE STORE, each of `person delete Nobody`, `person delete ana` (the group holds
      `Ana`, and names are compared exactly per WI-0001 AC1), `person delete ""`,
      `expense delete 3`, `expense delete 0`, `expense delete -1` and `expense delete abc` exits
      non-zero, writes a message to stderr, prints nothing to stdout, and leaves the data file's
      `md5sum` unchanged. Against an **empty** store, `person delete Ana` and `expense delete 1`
      each exit non-zero, write a message to stderr, and create no data file.

- [x] AC8 — `README.md` documents both commands, checked by reading the file for four things,
      each of which is present or is not: (a) it contains the literal string `person delete` and
      the literal string `expense delete`, each with a worked example showing the command and the
      line it prints; (b) its `expense list` sample output has every line beginning with the
      position number, so the sample matches what AC2 requires the command to print; (c) it
      states in a sentence that deleting a person named in a recorded expense is refused, and
      that the expenses must be deleted first; (d) it says that the numbers renumber after a
      deletion. A reader who has not seen this item can tell from the README alone what these two
      commands do and what they refuse to do.

## Out of scope

- **Editing** a person or an expense in place. The stakeholder was asked about correcting and
  removing together and chose removal: *"if I have to pick — being able to delete a mistake
  matters more to me than editing one"* (`WI-0001/Q-003`). Editing was not asked for and is not
  in this item; a correction is made by deleting and re-recording.
- Undoing a deletion, or any form of history of what was deleted.
- Deleting the whole data store, or a "start again" command.
- **A flag that deletes a person together with their expenses.** The stakeholder was offered
  exactly this as option D of `Q-001` — `person delete Ben --and-their-expenses` — and chose
  option A instead. There is no bulk escape hatch in this item, and adding one later is a new
  item and a new conversation, not a convenience somebody notices is missing.
- **Any confirmation prompt.** `person delete` and `expense delete` do what they are told and
  print what they did. Nothing in this tool is interactive (D3 in `## Notes`), and the safety
  the stakeholder asked for is AC3's refusal, not a `y/n`.
- **A stable identifier for an expense.** `expense delete` takes the position printed by
  `expense list` and nothing else; the numbers renumber after a deletion and mean "the Nth line
  of the listing you are looking at" (D2 in `## Notes`). Nothing here is scriptable against a
  handle that outlives a listing.

## Notes

- **Where this item came from.** `WI-0001/Q-003` asked the stakeholder whether records could be
  corrected or removed once recorded, and offered three options: never (append-only), inside
  WI-0001, or as its own item after WI-0002. Their reply: *"Hadn't really thought about it, but
  if I have to pick — being able to delete a mistake matters more to me than editing one.
  Timing's up to you, doesn't need to hold up the who-owes-whom feature."* That is option C
  narrowed to deletion, and this item is it. `answer-questions` filed it rather than widening
  WI-0001, per `spec/ids-and-statuses.md` §5.
- **Why it depends on WI-0002 rather than only on WI-0001.** The stakeholder said the timing was
  ours and that this must not hold up the who-owes-whom feature. `depends-on: WI-0002` is that
  sentence made mechanical: the orchestrator will not start this item until the settlement list
  is delivered. It is not a technical dependency — deletion only needs WI-0001's data store.
- **Why `medium` and not `high`.** `spec/ids-and-statuses.md` §6 reserves `high` for what the
  epic's stated outcome requires. EP-001's goal and its success measures are about recording
  costs and answering who owes whom; they are coherent without deletion. The stakeholder's own
  framing — *"if I have to pick"* — is a want, not a requirement.
- **What refinement had to settle is now settled.** The bullet that stood here listed three
  things — what the commands are called and how a person or an expense is named; whether the
  refusal is the right rule; and whether "already settled" means anything for an expense. All
  three are closed: the first two by D1 and D2 below and by the stakeholder's answer to Q-001,
  the third by reading (`settle` writes nothing and marks nothing as paid, so no such state
  exists — WI-0002 AC5 and WI-0002's `## Out of scope`).
- The whole epic is constrained to python3 and its standard library, with no network and no
  external services (see EP-001).

### How this item got here — read this before changing anything above

- **The stakeholder decided what deleting a person does to that person's expenses**
  (`questions/Q-001.md`, answered 2026-08-27T01:00:12Z). They chose **option A**: *"Go with A —
  refuse and tell me what's in the way. I'd rather do a couple extra commands than have expenses
  vanish or numbers quietly go wrong because I mistyped a name."* AC3 is that decision, and AC4
  is its other half. They were offered a `--and-their-expenses` bulk flag (option D) and declined
  it; that is in `## Out of scope` rather than merely absent.
- **Refinement ran twice.** The first execution could not finish — the question above was open
  against a stakeholder who was not in the session — and left an agenda rather than a
  half-refined item. `answer-questions` propagated the answer; the second execution installed the
  criteria and recorded the Definition of Ready verdict. Both are in
  `artifacts/refinement-qa.md`, now `status: recorded`, with every gap and who it was routed to.
- **The Definition of Ready passes on all ten criteria and was not overridden.** R4 and R10 were
  the two that failed on entry; the criteria above and the combination map below are what closed
  them. There is no `## Override` section on this item because nothing was waived.
- **Inherited from WI-0002's close, and now load-bearing:** `expenses/settle.py`'s `positions()`
  keys on `data["people"]` and silently ignores a name that appears in an expense but not in that
  list [src: tracker/items/WI-0002/artifacts/review.md]. AC3 is what stops the tool ever reaching
  that state: it makes "every name in a stored expense is a person `person list` shows" an
  invariant enforced where data is written. AC6 is the criterion that checks it from the reading
  side. Option C of Q-001 — delete the person, leave the expenses — is the one that would have
  walked into it, and it is the option the stakeholder was advised against and did not choose.

### The four decisions refinement took without asking

Each is `[assumed]`: refinement decided it and the stakeholder was **not** asked. Q-001's
`## Context` pointed them at `artifacts/refinement-qa.md` and invited them to object to anything
decided in their name; they answered Q-001 without objecting, which is as much endorsement as
this protocol can honestly record and is not the same as their having chosen these. The full
reasoning and the rejected alternatives are in that file; `plan` may propose a change to any of
them with a recorded reason, but may not change one quietly.

- **D1 — the commands are `person delete <NAME>` and `expense delete <NUMBER>`.** `<noun>
  <verb>` is the surface WI-0001's A1 fixed; `delete` is the stakeholder's own word. `remove`
  and `rm` were considered and rejected.
- **D2 — an expense is named by its 1-based position in `expense list`, and `expense list` gains
  a leading number column to print it.** An expense carries no identifier today, so a handle had
  to be invented; a stored opaque id and attribute-matching were both considered and rejected.
  The numbers are positions, not identities: after a deletion the rest renumber.
- **D3 — deletion does not ask for confirmation** (see `## Out of scope`).
- **D4 — a successful deletion prints one line naming what went, and exits 0**, the same shape as
  every other success in this tool. The exact wording is fixed in AC1, AC2 and AC4 so that
  `verify` has something to compare against rather than a judgement to make.

### What D2 costs elsewhere, for `plan` to reconcile rather than discover

Adding the number column changes output that WI-0001 already delivered and that its tests and the
README pin down. None of it breaks a WI-0001 acceptance criterion — AC3 requires each entry to
show its amount, payer, sharers, date and description in recorded order, which a leading number
does not disturb — but three things must be updated with this item rather than left to fail:

- `tests/test_cli.py`, `AC3ExpenseListShowsEveryField.test_expenses_are_listed_in_the_order_they_were_recorded`,
  reads the amount as `line.split()[1]`, which becomes the date once a number is prepended.
- `README.md` §`expense list` shows sample output with no number column (AC8 covers replacing it).
- WI-0002's settlement output is untouched by D2; `settle` prints payments, not the expense
  listing.

### Every combination this item introduces, and where each is stated — DoR R10

Two commands, no flags, so the combinations are the two targets against the states the store can
be in. Present in a criterion: person-deletion × their expenses present (AC3) and absent (AC1,
AC4); expense-deletion × the listing that follows, including the last expense going (AC2);
either deletion × a fresh process (AC5); either deletion × `settle` (AC6); either deletion × a
target that is not there, and × an empty store (AC7); expense-deletion × the numbering it
invalidates (AC2, D2). Named in `## Out of scope` rather than specified: deletion × a
confirmation prompt, deletion × an undo, person-deletion × cascading to expenses (option D), and
expense-deletion × a handle that survives renumbering. Nothing is left deliberately
unconstrained.

### What review accepted as gaps, at close

`review-close` accepted these declared gaps rather than sending the item back. They are written
here because once an item is `done` nobody opens its verification report again, and a gap that
lives only in a report stops being true without anyone noticing.

- **`lint-clean` checked nothing on this item, at any stage.** `commands.lint` is `null`
  [src: tracker/project.yaml], so no tool examined this diff for style, unused imports or dead
  code — only human reading did. ADR-0004 is the standing decision behind that; it is
  project-wide and not something this item introduced. Recorded as `skipped` by `implement`, by
  `verify` and by this review, never as a pass.
- **AC8(c) and AC8(d) are verified by reading only.** The test class
  `WI0004AC8TheReadmeDocumentsBothCommands` pins AC8(a)'s two literal command strings, the two
  output lines, and AC8(b)'s numbered sample. It asserts nothing about the sentence stating that
  deleting a person named in an expense is refused, or the sentence stating that the numbers
  renumber. Deleting either sentence from `README.md` would leave the suite green.
- **No criterion pins the refusal message strings.** AC3 requires only that the message contain
  the name and the count; `Ben is named in 2 expense(s); delete those first` is the plan's choice
  [src: tracker/items/WI-0004/artifacts/plan.md]. The same is true of
  `there is no expense <n>`, `<name> is not in the group` and
  `expense '<n>' is not a positive whole number`, which no criterion constrains at all. A rewrite
  that kept the name and the count would pass every test and every criterion.
- **`expense delete` refuses a positive whole number written with leading zeros.**
  `cli.POSITION_RE` is `^[1-9]\d*$`, so `expense delete 01` is refused with
  `expense '01' is not a positive whole number` — a message that is true of the *form* and false
  of the *value* [src: expenses/cli.py]. No criterion covers it, `expense list` never prints such
  a number, and it fails safe. Recorded rather than fixed; see finding F2 of
  `artifacts/review.md`.
- **`naming_expenses` returns `(position, expense)` pairs and only `len()` of the result is
  read.** The shape is the architect's, fixed in `plan.md`'s `## Approach`, and it is what a
  future message naming *which* expenses stand in the way would need. It is not an oversight and
  must not be quietly narrowed [src: tracker/items/WI-0004/artifacts/review.md].
- **Nothing was tested on any other platform, against any older stored dataset, or under
  concurrent use.** No older dataset exists — `store.VERSION` is unchanged by this item — and the
  product is one person at one terminal on one machine [src: docs/product/vision.md].
