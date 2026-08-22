---
id: WI-0002
type: work-item
title: Record an expense paid by one person and shared by several
status: done
priority: critical
epic: EP-001
branch: wi/WI-0002
created: "2026-08-21T21:07:03Z"
updated: "2026-08-21T22:26:50Z"
outcome: delivered
---

## Story

As the person keeping the group's books, I want to record that one friend paid a given amount
for something and that a named subset of the group shared in it, so that the debt this created
is captured at the moment it happens rather than reconstructed from memory later.

## Acceptance criteria

Every criterion is checked from the repository root against `$T`, a data file that does not exist
when the criterion starts (ADR-0004). Where a criterion needs people, they are registered first
with `./expenses add-person … --data-file "$T"` (WI-0001).

A recorded expense is **rendered** in exactly one form, used by both the confirmation and the
listing:

```
<YYYY-MM-DD> <amount> <description> — paid by <payer>, shared by <sharer>, <sharer>, …
```

with the amount to exactly two decimal places and no currency symbol, and the sharers in trimmed
case-folded name order (ADR-0003 clause 4), separated by a comma and a space.

- [x] AC1 — with `Ana`, `Ben` and `Cass` registered,
      `./expenses add-expense --paid-by Ana --amount 30.00 --description dinner --shared-by Ana,Ben,Cass --date 2026-08-14 --data-file "$T"`
      prints exactly `Added 2026-08-14 30.00 dinner — paid by Ana, shared by Ana, Ben, Cass` on
      stdout, nothing on stderr, and exits 0. The command has no option for a per-person amount:
      passing `--share-amount 10.00` is a usage error and exits 2, so an uneven split can neither
      be recorded nor silently ignored (WI-0002/Q-001)
- [x] AC2 — with `Ana`, `Ben` and `Cass` registered,
      `./expenses add-expense --paid-by Ana --amount 9.00 --description taxi --data-file "$T"`
      with no `--shared-by` records the expense as shared by all three: the confirmation reads
      `… — paid by Ana, shared by Ana, Ben, Cass`. The sharers are fixed at the moment of
      recording, so registering `Dan` afterwards and running `./expenses list-expenses` again
      still shows that expense shared by `Ana, Ben, Cass`
- [x] AC3 — recorded expenses survive the process exiting, and are listed in date order: after two
      expenses are recorded in separate invocations — `--date 2026-08-14` and `--date 2026-08-02` —
      a later `./expenses list-expenses --data-file "$T"` prints exactly two lines, the
      `2026-08-02` one first, each in the rendered form above, and exits 0. Two expenses with the
      same date print in the order they were recorded. `./expenses list-expenses` against a data
      file with no expenses prints exactly `No expenses recorded yet` on stdout and exits 0
      (ADR-0005 clause 4)
- [x] AC4 — naming someone who is not registered is refused and records nothing: with only `Ana`
      registered, both `--paid-by Dan …` and `--paid-by Ana … --shared-by Ana,Dan` print exactly
      `Unknown person: Dan` on stderr, print nothing on stdout, exit 1, and leave `$T` byte-for-byte
      unchanged. A sharer named in a different case (`--shared-by ana`) is **not** unknown: it
      resolves to the registered `Ana` (ADR-0003)
- [x] AC5 — an amount that is not a positive number with at most two decimal places is refused:
      `--amount 0`, `--amount -5`, `--amount abc` and `--amount 1.005` each print exactly
      `Amount must be a positive number with at most two decimal places: <value>` on stderr, exit
      1, and record nothing. `--amount 30` and `--amount 30.5` are accepted, and the expense they
      record renders as `30.00` and `30.50`
- [x] AC6 — the recording command accepts `--date YYYY-MM-DD` and stores that date; run without
      `--date` it stores the current date on the machine running it, **read from that machine's own
      clock and timezone**, so the rendered line begins with the output of `date +%F` — the local
      date, not `date -u +%F` — and the expense is otherwise indistinguishable from one where that
      date was typed. A `--date` value that is not a calendar date in `YYYY-MM-DD` form
      — `2026-13-01`, `14/08/2026`, `today` — prints exactly
      `Date must be a calendar date in YYYY-MM-DD form: <value>` on stderr, exits 1, and records
      nothing (WI-0002/Q-002)
- [x] AC7 — a description is required and may not be blank: omitting `--description` is a usage
      error and exits 2; `--description "   "` prints exactly `An expense needs a description` on
      stderr, exits 1, and records nothing
- [x] AC8 — a `--shared-by` list that names the same person twice, or names nobody, is refused
      before anything is recorded: `--shared-by Ana,ana` prints exactly
      `Ana is named twice in --shared-by` on stderr and `--shared-by ""` prints exactly
      `--shared-by must name at least one person` on stderr; both exit 1 and leave `$T`
      byte-for-byte unchanged
- [x] AC9 — every refusal above leaves the recorded history intact: after each of AC4, AC5, AC6,
      AC7 and AC8's refusals, `./expenses list-expenses --data-file "$T"` prints exactly what it
      printed before the refused command was run

## Out of scope

- Unequal shares of one expense — one sharer owing more of a bill than another, whether stated
  as an amount or as a weight. The stakeholder settled this in WI-0002/Q-001 ("Equal is fine for
  now"); if it is wanted later it is a new item, not a change to this one.
- Editing or deleting an expense after it is recorded; the epic excludes it.
- Computing balances or reporting who owes whom; that is WI-0003.
- Importing expenses from a file; that is WI-0004.
- Recording a settlement payment between two people; the epic excludes it.
- Any way to filter, search or total the expense list. `list-expenses` prints every expense
  recorded, in date order, and nothing else — no `--since`, no `--person`, no sum. The totals are
  WI-0003's report.
- Attaching anything to an expense beyond the five things AC1 names: no category, no receipt, no
  note, no currency.

## Notes

WI-0002/Q-001 is answered: shares are always equal. The stakeholder chose option A — "Equal is
fine for now — most of the time we're just splitting a bill evenly. Don't need per-person
amounts." An expense therefore stores the payer, the amount, a description and the list of
sharers, and nothing else about how the amount divides. AC1 and the out-of-scope list above were
amended by `answer-questions` to say so.

How the amount divides when it does not divide evenly is fixed by ADR-0001 (integer pence,
largest-remainder by name order); WI-0002 stores the amount, WI-0003 does the arithmetic.

**WI-0002/Q-002 is answered: every expense carries a date.** The stakeholder chose option B in
their own words — "Yeah, give expenses a date. If I don't type one, just use today's date." So:

- an expense stores a date as well as its payer, amount, description and sharers (AC1);
- `--date YYYY-MM-DD` sets it and omitting it means today, on the machine running the command
  (AC6). There is no such thing as a dateless expense, which is what makes the expense list
  readable in the order things happened and keeps WI-0004's imported rows from all looking alike;
- an imported expense takes its date from its own row rather than from the day of the import
  (WI-0004 AC2 and `## Notes`). Which column that is, and in what format, is part of the CSV
  sample still outstanding on WI-0004.

Dates are stored and printed as `YYYY-MM-DD`. Nothing in this epic filters or sorts by date —
WI-0003's report is over the whole history and says so — so the date is recorded information, not
a query dimension.

Two decisions made for WI-0001 bind this item and were not re-decided here: **ADR-0002** fixes the
command surface (`./expenses <subcommand>`, verb-noun; `add-expense` and `list-expenses` are the
reserved names) and **ADR-0005** fixes output and exit codes (confirmation on stdout with 0, a
refusal on stderr with 1 and nothing stored). `refine` still has to pin this item's exact
subcommand arguments and its exact messages; it does not get to re-choose the conventions.

### Decided during refinement, and by whom

`refine` fixed the following, because a criterion cannot be checked against a convention. All are
recorded as `[assumed]` in `artifacts/refinement-qa.md`. The authority is the surface and output
conventions the stakeholder delegated for WI-0001 (Q-004, "whatever you think is best here"),
which `answer-questions` recorded as **ADR-0002 and ADR-0005 and stated as binding on this item**
— not a fresh delegation invented here.

- **The command and its options.** `add-expense` and `list-expenses`, the names ADR-0002 clause 3
  reserved. Options are `--paid-by`, `--amount`, `--description`, `--shared-by`, `--date` and
  `--data-file`; `--paid-by` and `--shared-by` are the spellings WI-0004 AC6 already commits to.
- **One rendering for an expense**, shown above and used by both the confirmation and the listing.
  Two renderings would drift, and `verify` would have two strings to check for every behaviour.
- **The amount grammar.** A decimal number, optional decimal point, at most two places, no
  currency symbol and no thousands separator. `30`, `30.5` and `30.00` are the same amount; `1.005`
  is refused rather than rounded, because rounding at input would silently change what someone owes
  and ADR-0001 fixes rounding as a property of the *split*, not of the input.
- **Sharers are fixed at the moment of recording (AC2).** With `--shared-by` omitted the tool
  expands "everyone currently registered" into an explicit list and stores that. The alternative —
  storing "everyone" and resolving it at report time — would silently change who shared last
  month's dinner when a new friend is registered. AC2's own wording ("shows that explicitly rather
  than leaving it implied"), written at intake, is read as requiring the snapshot.
- **A person named twice in `--shared-by` is refused, not de-duplicated (AC8).** Deduplicating
  silently is the same failure mode the stakeholder rejected for the CSV import — "I don't want it
  silently doubling up" (WI-0004/Q-003) — read in reverse: a list they typed wrongly should be
  reported, not quietly repaired.
- **The exact refusal messages** in AC4 to AC8. `Unknown person: Dan` and the amount message follow
  the examples ADR-0005 clause 2 itself gives.
- **The date with no `--date` is the machine's *local* date** (WI-0002/Q-003, amended after
  `plan` found that AC6's original check clause said `date -u +%F` and contradicted its own first
  half on any machine that is not on UTC). The stakeholder's words settle it — "just use today's
  date" — and today on their laptop is what their bank statement will also show.
- **The listing order.** Date ascending, ties in the order recorded. Sorting needs a total order
  or the output cannot be compared, and date is the only field a reader would expect to sort by.

### Left deliberately unconstrained (R10)

Recorded so the gaps are visible rather than absent, per `spec/dor-dod.md` R10. Left by `refine`.

- **`argparse`'s usage-error wording**, as on WI-0001. Its exit code 2 is fixed by ADR-0005 clause
  3 and is asserted in AC1 and AC7; the text is not.
- **An expense shared by exactly one person.** Allowed, and it records a share equal to the whole
  amount. No criterion covers it because nothing about it differs from AC1 — the arithmetic is
  WI-0003's, and ADR-0001 handles `n = 1` without a special case.
- **A description containing the em dash or a comma.** It is stored and printed verbatim, so a
  description containing ` — ` makes the rendered line ambiguous to a *parser*. Nothing in this
  epic parses that output, and the stakeholder reads it, so no criterion constrains it.
- **How an expense is stored inside the data file.** ADR-0001 requires the amount to be held as a
  whole number of pence and ADR-0006 clause 2 gives it a new top-level key; which key and which
  field names is `plan`'s, and no criterion inspects the file's internals.

Two cases cannot arise and so have no criterion: an expense with no sharers when `--shared-by` is
omitted (the payer must be registered, so at least one person always is), and a `--shared-by` name
that differs only in case from a registered person being treated as unknown (AC4 states the
opposite explicitly).

### Accepted gaps at close

Recorded by `review-close` so that they outlive this item's closure. None contradicts a criterion;
each is either behaviour the record already calls unconstrained, or something no criterion asked
for. `artifacts/review.md` has the reasoning.

- **An unwritable `--data-file` path produces a Python traceback**, inherited from WI-0001 where it
  is already an accepted gap: `add-expense` writes through the same `store.save`.
- **A description containing ` — ` or a comma** makes the rendered line ambiguous to a parser.
  Nothing in this epic parses that output; the stakeholder reads it.
- **Two names that differ only by an accent are two people** (ADR-0003 declined accent-folding), so
  `--shared-by José,Jose` is not a duplicate and records a two-way split.
- **`argparse`'s usage wording is unchecked** — only its exit code 2 is asserted.
- **The listing at scale is unexamined.** Every check used one or two expenses.
- **Two `add-expense` processes running at once could lose a record**, because each loads, appends
  and replaces the whole file. Nothing in the epic mentions concurrency — it is one person at one
  terminal — and no criterion covers it. New in this item, and the most likely of these to matter
  if the tool is ever scripted.
