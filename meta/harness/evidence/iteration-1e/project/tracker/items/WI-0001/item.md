---
id: WI-0001
type: work-item
title: Record people and expenses from the command line, stored on disk
status: done
priority: high
epic: EP-001
created: "2026-08-26T23:22:36Z"
updated: "2026-08-27T00:19:29Z"
branch: wi/WI-0001
outcome: delivered
---

## Story

As someone who shares costs with friends, I want to add the people in my group and record each
expense with who paid it and who shared it, so that what we spent lives in one place instead of
in my head, and is still there tomorrow.

## Acceptance criteria

Every criterion below names a command and the observation that settles it, so that someone with
a terminal and no context reaches the same verdict. Commands are as recorded in `## Notes`.

- [x] AC1 — `python3 -m expenses person add Ana` exits 0; `python3 -m expenses person list` then
      exits 0 and its stdout contains a line for `Ana`. Running `person add Ana` a second time
      exits non-zero, writes a message naming `Ana` to stderr, and `person list` still shows
      `Ana` exactly once. `person add ana` after `person add Ana` exits 0, and `person list` then
      shows both.
- [x] AC2 — with `Ana`, `Ben` and `Cara` added, `python3 -m expenses expense add --amount 30
      --paid-by Ana --shared-by Ana,Ben,Cara` exits 0, and the expense is recorded with amount
      30.00, payer `Ana`, sharers `Ana`, `Ben` and `Cara`, and an equal share of 10.00 each, the
      three shares summing to exactly 30.00.
- [x] AC3 — `python3 -m expenses expense list` exits 0 and prints one entry per recorded expense,
      each showing that expense's amount, its payer, its sharers, its date and its description,
      in the order the expenses were recorded.
- [x] AC4 — after every command above has exited, running `python3 -m expenses person list` and
      `python3 -m expenses expense list` again in a new process prints byte-identical stdout to
      the previous run.
- [x] AC5 — `expense add --amount 30 --paid-by Ana --shared-by Ana,Dan`, with no person `Dan` in
      the group, exits non-zero, writes a message naming `Dan` to stderr, and leaves
      `expense list` printing byte-identical stdout to before the attempt. The same holds for
      `--paid-by Dan --shared-by Ana,Ben`, where the unknown name is the payer.
- [x] AC6 — each of `--amount 0`, `--amount -4`, `--amount abc`, `--amount 1.005`,
      `--shared-by ""`, `--shared-by Ana,Ana`, `--date 2026-13-01`, `--date yesterday`,
      `person add ""` and `person add "   "` exits non-zero, writes a message to stderr, and
      leaves both `person list` and `expense list` printing byte-identical stdout to before the
      attempt.
- [x] AC7 — `expense add --amount 12 --paid-by Ana --shared-by Ana,Ben` with neither
      `--description` nor `--date` exits 0 and records the expense with the current date and no
      description; `expense list` shows that entry carrying today's date. The two flags are
      independent: `--description taxi` alone, and `--date 2026-08-01` alone, each exit 0 and
      record the value given with the default for the other. `--description ""` records the same
      thing as omitting it.
- [x] AC8 — `expense add --amount 10 --paid-by Ana --shared-by Ana,Ben,Cara`, an amount that does
      not divide evenly by three, exits 0 and the three recorded shares sum to exactly 10.00.
      Running the same sequence of commands against a fresh empty store a second time prints
      byte-identical `expense list` output, so which sharer carries the extra unit is fixed by a
      rule rather than by chance. This criterion deliberately does not name which sharer that is.
- [x] AC9 — against an empty data store, `python3 -m expenses person list` exits 0 and its stdout
      contains `no people`, and `python3 -m expenses expense list` exits 0 and its stdout
      contains `no expenses`.

## Out of scope

- Working out who owes whom — that is WI-0002.
- Reading expenses from a bank CSV export — that is WI-0003.
- **Deleting** a person or an expense once recorded — that is now **WI-0004**, filed by
  `answer-questions` when the stakeholder answered `Q-003`. It stays out of *this* item: they
  said the timing was ours and that it *"doesn't need to hold up the who-owes-whom feature"*, so
  WI-0004 depends on WI-0002.
- **Editing** a person or an expense in place. Asked in `Q-003` alongside deletion and not
  chosen: *"being able to delete a mistake matters more to me than editing one"*. Nothing in the
  epic asks for it, so nothing is scheduled for it.
- Sharing the data with anyone else, or storing it anywhere but this machine.

## Notes

- **Refinement is complete and the item is Ready.** The stakeholder answered all three of round
  1's questions — `Q-001` (how an expense divides), `Q-002` (does an expense carry a description
  and a date), `Q-003` (can records be corrected or removed) — and refinement resumed, asked
  nothing further, and wrote the criteria above. The whole exchange, both rounds, is in
  `artifacts/refinement-qa.md` at `status: recorded`, including a table of the questions round 2
  considered asking and why each was refinement's own to settle instead.
- **Settled by the stakeholder, in their own words.** These three are not assumptions; they were
  asked and answered, and the verbatim replies are in the question files.
  - **An expense divides equally between the people named as its sharers.** *"Equal split, keep
    it simple. If a bill's uneven we'll just enter it as separate expenses."* (`Q-001`) A 30
    dinner shared by three is 10 each. There is no per-person amount and no weighting; an uneven
    bill is recorded as two or more expenses. This is what every number the tool prints means,
    including WI-0002's settlement list.
  - **An expense also carries a description and a date.** *"Yeah, add both — description and
    date. I'll want to know what a charge was for when I'm looking back over the list."*
    (`Q-002`, option C) The description is optional and the date defaults to the day the expense
    is recorded, which is what option C offered and what they accepted. Neither field takes part
    in any arithmetic: they exist for reading the list back, and they give WI-0003's importer
    somewhere to put the bank row's own date and description.
  - **Deletion is wanted, later, as its own item.** *"if I have to pick — being able to delete a
    mistake matters more to me than editing one. Timing's up to you, doesn't need to hold up the
    who-owes-whom feature."* (`Q-003`) Filed as WI-0004; see `## Out of scope`.
- **Settled by refinement in round 2 — the stakeholder was not asked.** Full reasoning in
  `artifacts/refinement-qa.md` as A8–A12. `--date` takes `YYYY-MM-DD`; anything else is a
  refusal, and a future date is accepted rather than second-guessed. An omitted `--date` means
  the day the expense is recorded, and `--description ""` means the same as omitting it. The
  empty listings print `no people` and `no expenses` and exit 0 — those exact strings are fixed
  so AC9 is decidable, and `plan` may print more around them but must keep them. Listings print
  in the order things were recorded, which AC4 forces anyway. A name that strips to nothing is a
  refusal.
- **Settled by refinement, not by the stakeholder — they were not asked.** These are the calls a
  team makes for itself, and they are recorded here so `plan`, `implement` and `verify` inherit a
  decision rather than a gap. Full reasoning for each is in `artifacts/refinement-qa.md` under
  "What refinement settled without asking".
  - The command surface is `python3 -m expenses person add|list` and
    `python3 -m expenses expense add|list`, with
    `expense add --amount <AMOUNT> --paid-by <NAME> --shared-by <NAME>[,<NAME>...]`
    `[--description <TEXT>] [--date <YYYY-MM-DD>]` — the last two flags added by `Q-002`'s
    answer. `plan` may propose a change with a recorded reason before this item is planned, but
    not silently: the acceptance criteria will be written against it.
  - Success writes to stdout and exits 0; a refusal writes to stderr, changes nothing on disk,
    and exits non-zero.
  - A person is identified by their name as typed, whitespace-stripped, compared exactly — `Ana`
    and `ana` are two people. Adding a name already in the group is a refusal.
  - An amount is a decimal with at most two decimal places and must be greater than zero. `12`,
    `12.5` and `12.50` mean the same thing; `0`, `-4`, `abc` and `1.005` are refusals. No
    currency is named and none is converted (EP-001 excludes conversion).
  - `--shared-by` must name at least one person. The payer need not be among the sharers. The
    same name twice in one sharer list is a refusal.
  - The shares of an expense sum to exactly the amount paid — no fraction of a unit created or
    lost. With the equal split now settled by `Q-001`, this is the statement that an amount which
    does not divide evenly by the number of sharers still has to add up: 10 shared by 3 is
    3.34/3.33/3.33 and not 3.33 three times. Which sharer absorbs the remaining unit is below.
- **Open design questions for `plan`** — no stakeholder stake in any of them, so none was asked:
  - Which sharer absorbs an indivisible remainder in an equal split. The only constraint is that
    the rule be deterministic, so the same data always produces the same shares. Record it as an
    ADR; WI-0002's AC4 depends on it.
  - Where the data store lives and what format it is in. No acceptance criterion names a path —
    AC4 is about running the listing commands again in a fresh process — but the location must be
    documented, because EP-001's success measures require a person to never hand-edit a data file.
  - What a date looks like on disk and how `--date` is validated, now that expenses carry one.
    Nothing rests on a particular choice; refusing an unparseable date per the rule above is the
    only requirement.
- The whole epic is constrained to python3 and its standard library, with no network and no
  external services, from the stakeholder's own statement (see EP-001).
