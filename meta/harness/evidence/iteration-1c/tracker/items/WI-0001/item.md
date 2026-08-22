---
id: WI-0001
type: work-item
title: Add and list the people who share expenses
status: done
priority: critical
epic: EP-001
branch: wi/WI-0001
created: "2026-08-21T21:07:03Z"
updated: "2026-08-21T22:05:54Z"
outcome: delivered
---

## Story

As the person keeping the group's books, I want to register each friend in the tool and see the
list back, so that expenses can name who paid and who shared without me retyping names and
without a typo silently creating a fourth person.

## Acceptance criteria

Every criterion below is checked from the repository root. `$T` is a path that does not exist at
the start of the criterion, so each one starts from an empty data store (EP-001 SM1, ADR-0004).

- [x] AC1 — `./expenses add-person Ana --data-file "$T"` prints exactly `Added Ana` on stdout,
      prints nothing on stderr, and exits 0. A following
      `./expenses list-people --data-file "$T"` prints exactly `Ana` on stdout and exits 0
      (ADR-0002 fixes the commands, ADR-0005 the output and the exit codes)
- [x] AC2 — the list survives the process exiting: the two commands in AC1 are separate
      invocations, and a third invocation of `./expenses list-people --data-file "$T"`, run later
      and from a new shell, still prints `Ana`
- [x] AC3 — with `Ana` already registered in `$T`, `./expenses add-person " ana " --data-file "$T"`
      creates no second entry: it prints exactly `Ana is already registered` on stderr, prints
      nothing on stdout, exits 1, leaves `$T` byte-for-byte unchanged, and a following
      `./expenses list-people --data-file "$T"` prints exactly one line, `Ana`. Two names are the
      same person when they are equal after trimming surrounding whitespace and case-folding
      (ADR-0003)
- [x] AC4 — `./expenses list-people --data-file "$T"` with `$T` not existing prints exactly
      `No one is registered yet` on stdout, exits 0, and does not create `$T` (ADR-0004 clause 3;
      ADR-0005 clause 4: nothing to show is not an error)
- [x] AC5 — a name that is empty, whitespace-only, or contains a comma is refused, and refusing
      changes nothing: `./expenses add-person "" --data-file "$T"` and
      `./expenses add-person "   " --data-file "$T"` each print exactly
      `A person's name cannot be blank` on stderr; `./expenses add-person "Smith, Jr" --data-file "$T"`
      prints exactly `A person's name cannot contain a comma` on stderr. Each prints nothing on
      stdout, exits 1, and leaves the output of `./expenses list-people --data-file "$T"` exactly
      as it was before (ADR-0003 clause 3, ADR-0005 clause 2)
- [x] AC6 — after `Cass`, `ana` and `" Ben "` are added in that order,
      `./expenses list-people --data-file "$T"` prints exactly three lines — `ana`, `Ben`, `Cass`,
      in that order. Each name is shown as it was first typed with surrounding whitespace removed,
      and the order is by the trimmed case-folded name (ADR-0003 clause 4, ADR-0005 clause 5)
- [x] AC7 — with `HOME` set to an empty directory and no `--data-file` given,
      `./expenses add-person Ana` exits 0 and creates exactly one new file directly in `$HOME`, at
      the path the README documents as the default; `./expenses list-people` with the same `HOME`
      then prints `Ana` (ADR-0004 clauses 1 and 2)
- [x] AC8 — a data file that exists but cannot be read as the tool's own format is refused rather
      than overwritten: with `$T` containing the bytes `not a data file`, each of
      `./expenses list-people --data-file "$T"` and `./expenses add-person Ana --data-file "$T"`
      prints a message on stderr that names `$T`, prints no Python traceback, exits 1, and leaves
      `$T` byte-for-byte unchanged (ADR-0005 clause 2)

## Out of scope

- Removing or renaming a person; the epic excludes editing and deleting.
- Any attribute of a person beyond their name (no email, no phone, no bank details).
- More than one group of people in the same data store. `--data-file` is not a group feature:
  nothing in the tool knows that a second file exists, and no command spans two of them
  (ADR-0004).
- Any way to see a person's expenses or balance from these commands; `list-people` prints names
  and nothing else. Balances are WI-0003's report.

## Notes

Intake wrote the first version of these criteria from the stated idea alone, deliberately leaving
"a documented command" unpinned. WI-0001/Q-001 to Q-004 put the four gaps to the stakeholder, who
answered all four by delegating the substance back — "whatever you think is best" — within one
binding constraint of their own: a typo like `ana` for `Ana` must not quietly create a second
person, and the data must be a file on their own laptop with no server, account or cloud.

`answer-questions` therefore decided, and the decisions are recorded where the whole epic can
read them rather than only here:

- **ADR-0002 — the command-line surface.** One executable file named `expenses` at the repository
  root, invoked `./expenses <subcommand>` in every criterion and worked example, with an optional
  `PATH` install documented for daily use. Subcommands are verb-noun: `add-person`, `list-people`
  here, and `add-expense`, `list-expenses`, `report`, `import-csv` reserved for the later items.
- **ADR-0003 — who counts as the same person.** Trim, case-fold, compare; store and print the
  name as first typed; refuse empty, whitespace-only and comma-containing names. Accents and
  internal spacing are *not* normalised, because merging two people who really are distinct
  cannot be undone in an epic with no editing or deleting.
- **ADR-0004 — where the data lives.** `~/.expenses.json` by default, `--data-file PATH` for one
  run. The override exists so that every check in this epic — all of which start "from an empty
  data store" — can be run without writing to the stakeholder's real ledger.
- **ADR-0005 — output and exit codes.** Confirm on success (stdout, 0); refuse on stderr with
  exit 1 and change nothing; `argparse`'s exit 2 for a usage error; "nothing to show" is stdout
  and 0, not an error.

AC5, AC6 and AC7 are new, added by `answer-questions` when those answers were propagated. They
state behaviour the decisions above create — the refusals, the listing order, and the data file
option — which nothing else in the item would have made checkable.

ADR-0002 and ADR-0005 bind WI-0002, WI-0003 and WI-0004 as well: this item is where the surface
and the conventions were settled, and the later items extend them rather than re-choosing.

### Decided during refinement, and by whom

`refine` fixed four things the ADRs left at the level of a convention, because a criterion cannot
be checked against a convention. All four are recorded as `[assumed]` in
`artifacts/refinement-qa.md`, under the stakeholder's standing delegation in Q-004 ("whatever you
think is best here"):

- **The exact refusal messages** — `A person's name cannot be blank` and `A person's name cannot
  contain a comma` (AC5). ADR-0005 fixed the stream and the exit code but not the words.
- **Where `--data-file` goes on the command line** — after the subcommand, as in
  `./expenses add-person Ana --data-file "$T"`. ADR-0004 requires every subcommand to accept it;
  which side of the subcommand it sits on is `argparse` mechanics, and pinning one form is what
  makes the criteria runnable.
- **AC8, an unreadable data file.** Nothing said what happens when the file exists but is not the
  tool's format. Left open, the natural implementation overwrites it — destroying a ledger that
  cannot be reconstructed, in an epic with no undo. AC8 requires a refusal instead.
- **AC7 does not quote the default filename.** It requires exactly one new file directly in
  `$HOME` at the path the README documents, so `plan`'s choice of storage format (and therefore of
  extension, ADR-0004 clause 4) cannot invalidate a criterion.

### Left deliberately unconstrained (R10)

Recorded here so that the gaps are visible rather than absent, per `spec/dor-dod.md` R10. Both
were left by `refine`, not by the stakeholder:

- **The wording of a usage error** — an unknown subcommand, a missing name, a second positional
  argument. ADR-0005 clause 3 fixes the exit code at 2 by adopting `argparse`'s own behaviour, and
  the message is therefore `argparse`'s. No criterion checks its text.
- **A `--data-file` path that cannot be created or written** — an unwritable directory, a path
  that is itself a directory. ADR-0005 clause 2 says what this *should* look like (a message on
  stderr, exit 1) and `plan` is free to implement exactly that, but no criterion checks it: the
  case needs a permission-controlled fixture to reproduce, and it is not one the stakeholder can
  hit with the documented default.

Every other combination this item introduces is covered: `--data-file` with each subcommand
(AC1, AC3, AC4, AC5, AC8) and without it (AC7); normalisation with listing (AC3, AC6); every
refusal with persistence (AC3, AC5, AC8 all require the stored file to be unchanged).

### Accepted gaps at close

Recorded by `review-close` so that they outlive this item's closure. None contradicts a
criterion; each is either behaviour the record already calls unconstrained, or something no
criterion asked for. `artifacts/review.md` has the reasoning.

- **An unwritable `--data-file` path produces a Python traceback, not a refusal.** `cmd_add_person`
  does not wrap `store.save`, so a `PermissionError` from `mkstemp` reaches the user raw. This is
  the one place the tool falls short of ADR-0005 clause 2's shape for a refusal.
- **The optional `PATH` install is unexercised.** Every criterion runs `./expenses` from the
  repository root, so the symlink case ADR-0008 clause 2 exists to support has no test. `plan.md`
  `## Risks` calls it the most likely way a real user's first run fails.
- **`commands.lint` is a syntax check.** `compileall` proves the files parse; no style linter is
  installed or installable here (ADR-0007 clause 4).
- **Atomicity rests on `os.replace`'s documented behaviour**, not on a test that kills the process
  mid-write.
- **Non-ASCII names are covered by a unit test only**, not through the command line.
- **`argparse`'s usage wording is unchecked** — only its exit code 2 is asserted, as the R10 note
  above says.
