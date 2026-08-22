# Plan — BUG-0001 A failed ledger write still prints the success line on stdout

## Problem

All three recording commands print their success line before `main` attempts to save, so a run
whose save fails prints a success line on stdout and an error line on stderr and exits 1, having
recorded nothing [src: BUG-0001]. Nothing about the *data* is wrong — it is genuinely unchanged,
the exit code is genuinely non-zero, and the reason is genuinely on stderr, which is why no WI-0001
criterion catches it [src: BUG-0001]. What is wrong is that a caller reading stdout is told the
run succeeded. The fix is to change the handler contract so that the ordering lives in `main`
rather than in each command: a handler returns its success line and `main` prints it only after
`store.save` has returned [src: ADR-0011]. The constraint is the property this project has kept
since WI-0001 — every command is the same skeleton, so a fact like "a refusal changes no recorded
data" is true by construction rather than by being remembered in six places
[src: tracker/items/WI-0001/artifacts/plan.md] — and the change must leave `WI-0003`'s importer
inheriting the ordering rather than having to repeat it [src: WI-0003 AC1].

## Approach

Change `cmd_add_person`, `cmd_add_expense` and `cmd_repay` to build their line and `return` it
instead of printing it, change the four read-only handlers to return `None`, and move the single
`print` into `main` after the save. Then cover it with a regression test that reproduces the bug's
own steps in real processes and asserts stdout is empty.

Nothing outside `expenses/cli.py` changes: a handler is reached only through
`set_defaults(handler=...)` and the one call in `main`, and no test and no other module reads a
handler's return value [src: expenses/cli.py]. `store.py`, `model.py` and `debts.py` are untouched,
and no command's arguments, output or exit code changes on the success path [src: ADR-0011].

## Steps

1. **`expenses/cli.py` — the three mutating handlers return their line.** In `cmd_add_person`,
   `cmd_add_expense` and `cmd_repay`, replace the `print(...)` and the `return True` with a
   `return` of the same f-string, unchanged in wording. Annotate each `-> str | None`. Afterwards
   the three handlers contain no `print` call and the success wording is byte-identical to today's
   [src: expenses/cli.py].

2. **`expenses/cli.py` — the four read-only handlers return `None`.** `cmd_people`,
   `cmd_expenses`, `cmd_repayments` and `cmd_debts` keep printing their own rows exactly as they do
   and `return None` in place of `return False`; annotate them `-> str | None` too. Their rows are
   deliberately **not** routed through the return value — see `ADR-0011`'s decision, which rejects
   buffering them. Afterwards every handler in the module has the same signature.

3. **`expenses/cli.py` — `main` prints after the save.** Replace `changed = args.handler(...)` with
   `line = args.handler(...)`, and the `if changed:` block with: when `line is not None`, call
   `store.save(path, ledger)` inside the existing `try`, returning `EXIT_STORE` on `StoreError`
   exactly as now, and then `print(line)`. The `ValidationError` and load-failure paths are not
   touched. Afterwards no statement in `main` writes to stdout before `store.save` has returned
   [src: BUG-0001 AC1].

4. **`expenses/cli.py` — the module docstring states the contract.** The docstring already claims
   the order "resolve the ledger path, load, apply one change, save atomically, print, return 0"
   [src: expenses/cli.py]; after step 3 that is true. Add one sentence naming the handler contract
   — a handler returns the line to print after a successful save, or `None` — and cite `ADR-0011`,
   so the next person to add a command reads it where they are working.

5. **`tests/test_persistence.py` — the regression test.** Add one test that follows `BUG-0001`'s
   reproduction in real processes, using the file's existing `run` helper and its
   `@unittest.skipIf(os.geteuid() == 0, ...)` guard [src: tests/test_persistence.py]: create the
   ledger in a writable directory and `add-person Ana` and `add-person Ben`; `chmod` the directory
   to `S_IRUSR | S_IXUSR` with an `addCleanup` restoring `S_IRWXU`; then run each of
   `add-person Cara`, `add-expense --payer Ana --amount 10 --description x` and
   `repay --from Ana --to Ben --amount 5`, asserting for each that `stdout` is empty, `stderr` is
   non-empty, and the exit code is non-zero. Finally restore the permissions and run `people`,
   asserting `Cara` is absent — the bug's step 6, which is what makes "prints nothing" mean
   "nothing happened" rather than "the output moved". The test fails on today's code and fails
   again if the print is moved back before the save [src: BUG-0001 AC2].

   The writable-then-locked ordering is required, not incidental: `add-expense` and `repay` name
   people, and an unknown person is refused with exit 2 before any save is attempted
   [src: expenses/cli.py], so a test that locks an empty directory would pass without ever
   exercising the defect.

6. **`docs/architecture/overview.md` — record the contract.** Extend the `cli.py` bullet with the
   handler contract and the ordering guarantee, citing `ADR-0011`, and bump the version with a
   change-log row [src: .claude/agile-skills/spec/doc-header.md]. This is a shape statement rather
   than a detail: it is what `WI-0003`'s author needs in order to write the import command without
   rediscovering the ordering.

7. **Run the gates on the final state.** `python3 -m unittest discover -s tests -t . -q` and
   `python3 -m compileall -q expenses tests` [src: tracker/project.yaml], and tick both criteria in
   `item.md` only against that run.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — with the ledger location unwritable, each of `add-person`, `add-expense` and `repay` prints nothing on stdout, prints the failure on stderr, and exits non-zero | 1, 2, 3 | The new test in step 5, run for all three commands; and by hand, `BUG-0001`'s six reproduction steps, whose step 4 currently prints `Added Cara.` and afterwards must print nothing while `error: cannot write the ledger at …` still appears on stderr and the exit code is still 1 |
| AC2 — a regression test covers all three commands against an unwritable location, asserting empty stdout, and fails if the success line is moved back before the save | 5 | `python3 -m unittest discover -s tests -t . -q` passes on the fixed code; the same command fails the new test on the pre-fix code, which `implement` records by running it before step 1 or against a stash |

## Assumptions

None. The one thing that could have been assumed — that nothing outside `cli.py` depends on the
handler's `bool` return — was checked instead: a handler is reached only through
`set_defaults(handler=...)` and the single call in `main`, and no test references a handler or its
return value [src: expenses/cli.py].

## Decisions and ADRs

- **`ADR-0011` — a command handler returns its success line rather than printing it.** The handler
  contract becomes `str | None`. Recorded as an ADR rather than settled in this plan because it is
  the shape `WI-0003`'s import command will implement, and because three alternatives were worth
  naming: returning `(changed, line)`, buffering stdout in `main`, and saving before the handler
  runs. Reversibility is high — one file, no data migration, no change to any command's arguments
  or output on the success path.
- **Answered from the documents, not decided here:** that a failing save must still exit 1 with its
  reason on stderr and the data unchanged. WI-0001 already defines a refusal that way and
  `BUG-0001` records that all three already hold [src: BUG-0001]. This item changes stdout and
  nothing else.
- **Answered from the documents:** the success wording. It stays byte-identical, because
  `BUG-0001` quotes all three lines as the actual behaviour and asks only for their *timing*
  [src: BUG-0001].

## Risks

- **Running the tests as root ignores directory permissions**, and the new test would then observe
  a successful save rather than a failed one. `tests/test_persistence.py` already guards its two
  permission tests with `@unittest.skipIf(os.geteuid() == 0, ...)`; step 5 uses the same guard, so
  under root the test is skipped rather than passing vacuously [src: tests/test_persistence.py].
- **`store.save` fails at a different point than the test assumes.** It creates the parent with
  `mkdir(parents=True, exist_ok=True)` before opening the temporary file, and on an existing
  directory that call succeeds without write permission, so the failure is raised from
  `NamedTemporaryFile` — which is the `[Errno 13] … .tmp` message `BUG-0001` quotes
  [src: expenses/store.py; BUG-0001]. If a future change made `save` fail earlier, the test still
  holds: it asserts on stdout and the exit code, not on which line raised.
- **A later change re-unifies the read-only output into the return value**, buffering the listings
  and undoing option C's rejection without noticing. `ADR-0011` states the distinction and why, and
  step 4 puts it in the docstring where a command is added.
- **The fix is invisible on the success path**, so a reviewer cannot see it working from normal
  use. That is what step 5's before-and-after run is for: a regression test that never failed
  against the unfixed code is not evidence of anything.

## Out of scope for this item

- **Strengthening `CliTestCase.assertRefused` to also assert empty stdout.** Every validation
  refusal already prints nothing on stdout, so the assertion would pass today across every existing
  refusal test and would guard them all in future [src: tests/cli_harness.py]. It maps to no
  criterion of this item, and widening a shared assertion in a bug fix makes both changes harder to
  review. Recorded here so it is a visible opportunity rather than a lost thought.
- **Any change to the wording, the exit codes, or the stderr text.** `BUG-0001` asks for the
  success line to move, not to change [src: BUG-0001].
- **The `expenses`, `people`, `repayments` and `debts` listings' own output.** They print no
  success line and have no save to be ordered against [src: ADR-0011].
- **`WI-0003`'s import command**, which will implement this contract but is `blocked` on a CSV
  sample and is not this item's work [src: WI-0003].
