---
id: WI-0001
type: work-item
title: Add and list people, stored so they survive between runs
status: done
priority: high
epic: EP-001
branch: wi/WI-0001
outcome: delivered
created: "2026-08-21T18:38:55Z"
updated: "2026-08-21T19:38:37Z"
---

## Story

As someone keeping track of a friend group's shared costs, I want to add people to the group and
list who is in it, so that later expenses can name them and the group's membership is recorded
in one place rather than assumed.

## Acceptance criteria

Every criterion below is written against `python3 -m expenses <subcommand> [arguments]`, run from
the project root (ADR-0001, ADR-0006). "Exits non-zero" always means: a message on standard error,
an exit status other than `0`, and no Python traceback — standard error contains no line matching
`Traceback (most recent call last)`.

- [x] AC1 — `python3 -m expenses add-person "Sam Okafor"` prints `Added Sam Okafor.` on standard
  output and exits `0`. A name may contain spaces (ADR-0005).
- [x] AC2 — After that, `python3 -m expenses people` prints exactly one line, `Sam Okafor`, on
  standard output and exits `0`. A person is shown with the spelling first entered for them,
  stripped of surrounding whitespace (ADR-0005 point 4).
- [x] AC3 — Persistence: with the three commands run as three separate invocations of the
  process — `add-person Alice`, then `add-person Bob`, then `people` — the third prints `Alice`
  and `Bob` and exits `0`. Nothing is re-entered, and no state is passed between the invocations
  other than what the tool itself stored.
- [x] AC4 — `people` lists people in the order they were added, one per line, and prints nothing
  else on standard output. Adding `Carol`, `alice` and `Bob` in that order makes `people` print
  `Carol`, `alice`, `Bob`, in that order, on three lines.
- [x] AC5 — `python3 -m expenses people` when nobody has been added prints exactly
  `No one is in the group yet.` on standard output and exits `0` — not a traceback, not silence,
  not an error (ADR-0006 rule 2).
- [x] AC6 — Duplicate refused. With `Sam Okafor` in the group, each of
  `add-person "sam okafor"`, `add-person "  SAM OKAFOR  "` and `add-person "Sam  Okafor"` prints
  `Sam Okafor is already in the group.` on standard error and exits non-zero, and `people`
  afterwards still prints exactly one line. Two names denote the same person when their identity
  keys are equal — surrounding whitespace stripped, internal runs of whitespace collapsed to one
  space, the result case-folded (ADR-0005 point 3).
- [x] AC7 — A name that is empty or only whitespace is refused: `add-person ""` and
  `add-person "   "` each print `A name cannot be empty.` on standard error, exit non-zero, and
  add nobody.
- [x] AC8 — A name containing a comma or an equals sign is refused: `add-person "Anna,Karin"` and
  `add-person "a=b"` each print
  `A name cannot contain a comma or an equals sign; those are reserved.` on standard error, exit
  non-zero, and add nobody. Those two characters are reserved for naming several sharers and their
  amounts on one command line (ADR-0005 point 2).
- [x] AC9 — Accented letters are distinct. With `José` already added, `add-person "Jose"` exits
  `0`, and `people` then prints two lines (ADR-0005 point 3).
- [x] AC10 — Argument arity is checked, and each failure exits non-zero with a message on standard
  error:
  - `python3 -m expenses add-person` — no name at all — says a name is required;
  - `python3 -m expenses add-person Sam Okafor` — two arguments, the name unquoted — says the name
    must be a single argument and should be quoted, and adds nobody. It does **not** silently join
    the two words;
  - `python3 -m expenses people extra` — a listing command given an argument — says `people` takes
    no arguments (ADR-0006 rule 2).
- [x] AC11 — `python3 -m expenses no-such-command` and `python3 -m expenses` with no subcommand at
  all each exit non-zero with a message on standard error; the first names the unknown subcommand
  (ADR-0001, ADR-0006 rule 3).

## Out of scope

- Removing or renaming a person. Membership is add-only for this item, and for this epic — which
  is why the duplicate rule in AC6 matters: a person added by mistake cannot be taken out again.
- Any attribute of a person beyond the name used to refer to them.
- Anything to do with expenses, payments or balances; those are WI-0002, WI-0004 and WI-0003.
- Where and how the group is stored on disk. That is a design decision, not a requirement: this
  item asserts only that the data survives between invocations (AC3). See `## Notes`.
- Two people running the tool at the same time on the same file. `docs/product/vision.md` (v3)
  excludes multi-user use; no locking or conflict behaviour is specified or expected.

## Notes

### What was decided, and by whom

All four questions on this item are answered.

`Q-001` — the human delegated the command surface ("whatever you think is best"). Decided as
**ADR-0001**: one-shot subcommands, `python3 -m expenses <subcommand> [arguments]`, exit `0` on
success and non-zero with a stated message on standard error on refusal, never a traceback.

`Q-003` — the human delegated the subcommand names too. Decided as **ADR-0006**: `add-person` and
`people` here, and by the same rule `add-expense` / `expenses`, `add-payment` / `payments`, and
`who-owes-whom`.

`Q-002` and `Q-004` — the human chose option B in both, recorded together as **ADR-0005**: a name
may contain spaces; `,` and `=` are refused inside one; and two names denote the same person when
their case-folded, whitespace-normalised forms are equal. Their reason for `Q-002` is the one to
keep in mind here: "I don't want two half-right versions of the same person messing up the
totals." ADR-0005 point 5 extends the identity rule to every place a person is named, which is the
architect's derivation rather than something the human said.

### Assumptions this refinement made without the human

The human was not present for this refinement pass — they answer asynchronously, in the question
files. Everything the Definition of Ready needed from them was already answered there, so nothing
new was escalated. What remained was detail they have twice declined to be asked about, so it was
decided here and marked `[assumed]` in `artifacts/refinement-qa.md`. None of it was confirmed by
them:

1. **The exact wording of every message** in AC1 and AC5 to AC8. Exact text is what makes those
   criteria decidable by someone with no context; the wording itself is cosmetic and changing it
   later is a criterion edit, nothing more.
2. **`people` lists in the order people were added** (AC4), rather than alphabetically. Insertion
   order is the one that needs no tie-break rule and no decision about how to sort names that
   differ in case or carry accents.
3. **`add-person` given two arguments is refused rather than joined** (AC10). Joining would make
   `add-person Sam Okafor` and `add-person "Sam Okafor"` equivalent, which is friendly; refusing
   is what makes a fat-fingered `add-person Sam Okafor Smith` visible instead of silently creating
   a third spelling of somebody.

If the human contradicts any of these later, each is a one-line change to this item and its
implementation.

### Left deliberately unconstrained (R10)

- **The storage location and file format** are not constrained by any criterion. AC3 asserts only
  that the data survives between invocations. `plan` decides where the file lives and what is in
  it, and records it as an ADR; that decision governs WI-0002, WI-0003 and WI-0004 too, since all
  four kinds of fact share one record (`docs/product/prd.md` v2). Left so by `refine`, on the
  grounds that it is a design decision with no observable consequence at this item's level.
- **The behaviour when the stored file exists but is unreadable or malformed** is not specified
  here. It is not a combination of this item's own behaviours — it is a property of whatever
  storage `plan` chooses — so it belongs to that decision. Left so by `refine`.

### Accepted gaps, recorded at close (review-close, 2026-08-21)

Delivered as `delivered`. `artifacts/review.md` carries the full Definition of Done table; these
are the gaps it accepted, repeated here because a gap that lives only in a report is a gap that
has been forgotten rather than accepted:

1. **A write that fails produces a Python traceback.** With the target directory unwritable,
   `add-person` exits non-zero but prints a traceback rather than a message. No criterion on this
   item covers it and no ADR decides it: `ADR-0001` point 3's no-traceback rule is written about
   refusals (an unknown person, a duplicate, a malformed amount) and `ADR-0007` point 5 covers a
   record that cannot be *read*, not one that cannot be *written*. `storage.save` is inherited
   unchanged by WI-0002 and WI-0004, so **the `plan` execution on WI-0002 should decide the
   write-failure behaviour** rather than a criterion being retrofitted here.
2. **The `~/.local/share/expenses/expenses.json` default path was never exercised**, because doing
   so would write to the real home directory of whoever runs the suite. The `EXPENSES_FILE` and
   `XDG_DATA_HOME` branches of the same resolution were both run live.
3. **Atomicity of the write is argued from construction, not demonstrated.** What was demonstrated
   is the consequence that matters: a record that cannot be read is never overwritten.
4. **`lint-clean` on this project is a syntax check, not a linter** (`ADR-0008`). Nothing checks
   style, dead code or types anywhere in this pipeline; review is the only thing standing there.

One correction to the record, from the same review: `artifacts/impl-report.md` says the record
file gets whatever permissions the umask allows, and `artifacts/verify-report.md` repeats it. Both
are wrong — `tempfile.mkstemp` creates at mode `0600` regardless of umask and `os.replace`
preserves it, so the file is `0600`. The behaviour is stricter than the reports claim, so the code
is fine; the two reports are left as written because they record what those executions believed,
and this note is the correction.
