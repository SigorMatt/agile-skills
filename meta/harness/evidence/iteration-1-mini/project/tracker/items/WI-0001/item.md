---
id: WI-0001
type: work-item
title: Keep a roster of people that survives between runs
status: done
priority: critical
epic: EP-001
branch: wi/WI-0001
created: "2026-08-21T02:03:44Z"
updated: "2026-08-21T03:44:12Z"
outcome: delivered
---

## Story

As a member of the friend group, I want to add people to the group and see who is in it, so
that later expenses can name them and the list is still there the next time I run the tool.

## Acceptance criteria

- [x] AC1 — the tool offers a command that adds one named person to the group and a command that
      lists the people in it, and both appear in the tool's top-level `--help` output. When the
      group is non-empty the listing prints one person per line, their name and nothing else, in
      the order they were added; it exits zero.
- [x] AC2 — after adding people, exiting the process, and running the listing command again in a
      **fresh** process, the same people are listed, in the same order
- [x] AC3 — adding a person whose name matches one already in the group prints an error naming
      that person, exits non-zero, and leaves the roster exactly as it was. Names are matched
      **case-insensitively**, after surrounding whitespace is stripped, so `alice`, `Alice` and
      ` Alice ` are the same person; the spelling kept and listed is the one entered first.
      (WI-0001/Q-001.)
- [x] AC4 — listing people when none have been added yet succeeds, exits zero, and prints a
      message saying the group is empty, rather than failing or printing nothing
- [x] AC5 — on a machine where the store does not yet exist, adding a person creates it — the
      file and any missing parent directories — with no separate setup or initialise step, and
      the person is listed by a subsequent run. Commands that only read succeed against a
      missing store and report an empty group. (WI-0001/Q-002, ADR-0002.)
- [x] AC6 — when the store file exists but cannot be read or parsed, every command — reading or
      writing — prints an error naming the file's path and what was wrong with it, exits
      non-zero, and leaves the file's bytes on disk unchanged. In particular, adding a person to
      a damaged store must not overwrite it with a fresh one. (WI-0001/Q-002, ADR-0002.)
- [x] AC7 — adding a person with an empty name, or a name that is only whitespace, is rejected
      with a message saying a name is required, exits non-zero, and leaves the roster unchanged.
      Adding with no name argument at all does the same.
- [x] AC8 — no failure in this item's commands prints a Python traceback. Every failure prints a
      one-line message on **stderr** naming what was wrong and exits non-zero, and every success
      prints on **stdout** and exits zero. This is EP-001's fourth success measure, tested here
      because this item introduces the file I/O that produces most of the failures.

## Out of scope

- Removing or renaming a person.
- Any attribute of a person other than the name they are known by (no email, no phone, no
  avatar).
- Recording expenses; that is WI-0002.

## Notes

Where the store lives on disk is now decided: a single JSON file at
`$XDG_DATA_HOME/expenses/store.json`, defaulting to `~/.local/share/expenses/store.json`,
overridable by the `EXPENSES_STORE` environment variable so that tests can exercise a real store
without touching the developer's own. It is per-user, not per-directory, so the roster is the
same whatever directory the tool is run from. Writes go to a temporary file in the same directory
and are renamed over the store, so an interrupted run cannot produce the damaged file AC6 has to
report. The full decision, its alternatives and its reversibility are in
`docs/architecture/adr/ADR-0002-one-store-file-per-user.md`; that ADR is the authority, and this
paragraph is a summary of it.

`EXPENSES_STORE` is a testing and escape-hatch mechanism, not a way to keep several friend groups
apart — the stakeholder said there is only one group (EP-001/Q-003) — and the help text must not
present it as one.

This item is the foundation for WI-0002 and WI-0003, which both read the same store; whatever
module owns reading, writing, creating and validating it is written here and used by both.

## Accepted gaps

Recorded by `review-close` on 2026-08-21, extended at each of its three executions. Each was
declared by `verify` or `implement`, or found in the diff, judged acceptable, and written here
rather than left in `artifacts/review.md`, because nobody reads a review report after an item
closes. The reasoning for each is in `artifacts/review.md` `## Accepted gaps` and `## Findings`.

Two bullets that stood here have been **struck** rather than carried, because an accepted gap that
has since been closed misleads exactly as much as an unrecorded one:

- *"the two default store-path branches have never been executed"* — the second verification
  executed both, against a scratch `HOME` and `XDG_DATA_HOME`, and both match `ADR-0002`
  decisions 1–2.
- *"the write path's `OSError` wrapper was never triggered"* — the third review triggered it: a
  read-only parent directory gives `cannot write <path>: Permission denied`, exit 2, no traceback,
  and an `EXPENSES_STORE` pointing at a directory gives the read-side equivalent on both commands.

- **A bare `python3 -m expenses`, with no subcommand, prints the whole help to stderr and exits
  2.** No criterion and no plan step specifies this; AC8 is scoped to this item's two commands.
  It exits non-zero with no traceback and is pinned by
  `tests/test_cli.py::test_no_command_at_all_fails_cleanly`, so it is deliberate. If the intended
  behaviour is a one-line error instead, that is a change someone must ask for.
- **No static analysis runs on this project at all.** `tracker/project.yaml` has
  `commands.lint: null` by `ADR-0001` §4, so the `lint-clean` gate is skipped on every item, not
  passed. Unused imports, dead functions, unreachable branches and shadowed names are caught by
  nothing mechanical. **Three** defects of exactly that class were found in this one item by a
  person reading a diff — the dead `match_key()`, the never-passed `out`/`err`, and a `# noqa`
  comment naming a rule no tool here enforces. This is an epic-level decision to revisit, and it
  is handed to EP-001's closure rather than to another item.
- **`ADR-0002` decision 7's atomic write is verified by inspection, not by test.** No process was
  killed mid-write. `store.save()` does create its temporary file in the store's own directory,
  which is the part that matters, but nothing would catch that changing.
- **`cli.main` carries `out` and `err` parameters that no caller passes.** `plan.md` step 5
  declares `main(argv=None) -> int`; the implementation adds two stream parameters, and
  `__main__.py` and every caller leave them at their defaults, so half of each `if … is None`
  branch is never taken. One test now drives them, which makes them exercised but still unused by
  any caller. Inert and cheap, so it is kept. Recorded by `review-close` on 2026-08-21
  (`review.md` F4, second execution).
- **Two processes adding a person at the same time can lose one of them.** The store is read and
  written whole, so the last writer wins. Nothing claims otherwise and no criterion mentions it;
  it is unreachable for one person at a terminal and is a real limit of the design.
- **A name that today's rules would reject, put into the store by hand, is listed verbatim.**
  `store.load()` guarantees every roster entry is a string; it deliberately does not guarantee the
  entry would pass `normalise()`. So a hand-edited `""` makes `people` print a blank line, and
  `"Al\nice"` makes it print across two lines — the very thing `ADR-0006` decision 5 bans control
  characters to prevent. The tool cannot create such a store: `normalise()` rejects both at the
  only point a name enters the roster, and the fix for `review.md` F2 was specifically about not
  re-validating the stored side. Rejecting these on read would make a hand-edited store unusable
  rather than merely odd, and repairing them would edit a user's file unasked — both stricter than
  `ADR-0002` decision 6 asks for. Recorded by `review-close` on 2026-08-21 (`review.md` F5).
- **The `expenses` list's elements are unvalidated, and WI-0002 inherits the obligation.**
  `store.load()`'s element-type check covers `people` only, so
  `{"version":1,"people":["Alice"],"expenses":[42]}` loads cleanly and `people` exits 0. That is
  correct today — nothing in this item reads that list — but it is the same latent crash one item
  away. It was **not** filed as a bug, because a bug's Definition of Ready (`spec/dor-dod.md` §2,
  RB3) needs an expected behaviour citing something it contradicts, and nothing yet says what an
  expense record *is*; the bug would have to invent the schema WI-0002's plan owns.
  **WI-0002 must extend `store.load()`'s check when it defines that shape.** Recorded by
  `review-close` on 2026-08-21 (`review.md` F6).
- **AC8 says "a one-line message" and `argparse`'s failures are two lines.** `add-person` with no
  argument prints a usage line and then
  `python3 -m expenses add-person: error: the following arguments are required: name`.
  `plan.md` step 5 chose `argparse`'s own error handling deliberately and `verify` flagged the
  wording. The reading applied, and it is a decision rather than an oversight: **the message
  naming what was wrong is one line**, and `argparse`'s usage line precedes it as a hint. AC8's
  own sentence gives its purpose — EP-001's fourth success measure, no traceback, stderr,
  non-zero exit — and all three hold. The criterion was not edited. If strictly one line of
  stderr is wanted, that is a change someone must ask for. Recorded by `review-close` on
  2026-08-21 (`review.md` F7).
- **`cli.main`'s catch-all backstop is a design decision recorded in an architecture overview
  rather than in an ADR.** It changed the architecture's central claim about how AC8 is
  guaranteed — `overview.md` v1 said the property fell out of the layering, and it did not. It is
  captured in `overview.md` **v2** with a change-log row, the rationale, the rejected alternative
  and the counter-example, which is substantively what an ADR carries; but D6 asks for an ADR.
  `implement` could not have written one — ADRs are the architect's artifact. **A later `plan`
  execution should decide whether to promote it.** Recorded by `review-close` on 2026-08-21
  (`review.md` F8).
- **`plan.md`'s paragraph at lines 24–29 states a claim that is now false**, and it was left in
  place on purpose. It says AC8 is *"made true by construction"* by a single
  `except ExpensesError`; `review.md` F3 disproved that. `review-close` appended a `## Correction`
  section to the end of `plan.md` rather than editing the paragraph, so that the evidence of what
  the plan believed survives alongside the correction. `docs/architecture/overview.md` v2 is the
  current authority on how AC8 is guaranteed.

## Deliberately unconstrained

Recorded per the Definition of Ready **R10**, so that these are open questions someone can find
rather than gaps nobody knows exist. Each names who left it open.

- **What characters a person's name may contain.** AC7 forbids empty and whitespace-only names
  and AC3 fixes how two names are compared, but nothing constrains commas, digits, punctuation or
  non-ASCII characters, and any of them is accepted. Left open by `refine` on 2026-08-21, not by
  the stakeholder. It is left open deliberately rather than decided because the one thing that
  would force a decision — whether WI-0002 takes its sharers as a comma-separated list or as a
  repeated flag — is `plan`'s to decide, and constraining names here on a guess about that would
  couple this item to a design that does not exist yet. **`plan` must settle it**: if the sharer
  syntax makes a character unusable in a name, this item's validation has to reject that character
  at the point a person is added, not leave WI-0002 to discover it.
- **The tool's invocation name and the exact spelling of its two commands.** AC1 constrains only
  that they exist, that they are discoverable from `--help`, and what they print. Assumed by
  `refine`, not stated by the stakeholder; `plan` owns the naming, and AC1 stays true whatever it
  chooses.
- **How many people the roster may hold, and how large a store may get.** Nothing sets a limit and
  no criterion depends on one. Left open by `refine`: the stakeholder described a friend group,
  and a limit nobody asked for is a failure mode nobody wanted.
- **Permission and other OS errors** — an unwritable directory, a read-only store, a full disk.
  These are not enumerated as separate criteria; AC8 covers all of them by requiring a named
  message and a non-zero exit rather than a traceback, which is the behaviour the stakeholder
  actually cares about.
