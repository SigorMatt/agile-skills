# Review — WI-0001

## What I examined

- **The record's mechanics.** `history.md` — eight rows, chaining without a gap from `— → draft`
  to `verifying → in-review`, the last row matching `item.md`. `journal.md` — seven entries
  (`intake`, `refine`, `answer-questions`, `refine`, `plan`, `implement`, `verify`), one for every
  actor the history names, in non-decreasing timestamp order. All four questions `answered`, each
  with a `## Consequences` section naming files that exist. All eight criteria ticked.
- **Verification freshness.** `check-verify-freshness WI-0001 wi/WI-0001` →
  *"verified at 5288776a; wi/WI-0001 has moved to 77a0ad4a but only the record changed (5 file(s)
  under tracker/ or docs/), so the verification still covers the code"*, confirmed by
  `git log --oneline --name-only 5288776..HEAD`, whose one commit touches only `tracker/`.
- **The diff, hunk by hunk:** `git diff main..HEAD` — `expenses` (17 lines),
  `expenses_tool/__init__.py`, `expenses_tool/cli.py` (106), `expenses_tool/store.py` (159),
  `tests/__init__.py`, `tests/test_store.py` (130), `tests/test_cli_people.py` (172), `README.md`
  (102), and the tracker files this pipeline writes.
- **The two declared-gap sections:** `verify-report.md` `## Not verified, and why` (five entries)
  and `impl-report.md` `## What I did not do` (four).
- **The trial merge:** `wi/WI-0001` into a throwaway branch off `main`, with `commands.test` and
  `commands.lint` run on the merge result.

Where each hunk earns its place:

| hunk | serves |
|------|--------|
| `expenses` — launcher, `sys.path` from `realpath` | plan step 1; ADR-0008 clauses 1–2 |
| `store.py` — `normalise`, `display`, `validate_name` | plan step 2; AC3, AC5, AC6; ADR-0003 |
| `store.py` — `load`, the exception classes | plan step 3; AC4, AC8; ADR-0006 clause 4 |
| `store.py` — `save`, temp file plus `os.replace` | plan step 4; AC3, AC5, AC7; ADR-0006 clause 5 |
| `store.py` — `add_person`, `list_people` | plan step 5; AC1, AC3, AC6 |
| `cli.py` — parser and `--data-file` parent | plan step 6; AC1, AC7; ADR-0004 |
| `cli.py` — `cmd_add_person`, `cmd_list_people`, `_refuse` | plan steps 7–8; AC1–AC5, AC8; ADR-0005 |
| `tests/test_store.py` | plan step 9 |
| `tests/test_cli_people.py` | plan step 10; one class per criterion, plus two usage-error tests declared as a deviation |
| `README.md` | plan step 11; AC7 points at the path it documents |

Nothing in the diff is unaccounted for. No hunk contradicts an ADR: `cli.py` holds every
user-visible string (ADR-0008 clause 3), `store.py` prints nothing and exits nothing, `main()`
returns rather than exits (clause 4), and money — which does not appear in this item — is
untouched, so ADR-0001 is not in play.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every criterion ticked | **pass** | `grep -c "^- \[x\] AC" item.md` → 8, and no `- [ ] AC` remains |
| D2 | every tick cites evidence in `verify-report.md` | **pass** | its `## Criteria` table has eight rows, each with the command `verify` ran and its quoted actual output — not a test name and not a reference to `impl-report.md` |
| D3 | gates passed on the final state of the code | **pass** | `implement` ran them on `1dd3f09`; `verify` re-ran them on `5288776`; this review ran them again on the trial merge result — `Ran 27 tests … OK`, `compileall` exit 0 |
| D4 | no open blocking question | **pass** | `Q-001` to `Q-004` all `status: answered`, each with `## Consequences` naming files that exist |
| D5 | a journal entry per execution; history chains | **pass** | seven journal entries against seven executions in the history; `validate-workspace` → 0 errors, which is where `history.gap` and `journal.execution.missing` would surface |
| D6 | design decisions in ADRs, cited | **pass** | ADR-0002 to ADR-0005 (from `answer-questions`) and ADR-0006 to ADR-0008 (from `plan`), all cited in `plan.md` `## Decisions and ADRs` and in the item's `## Notes` |
| D7 | documents the change invalidated are updated | **pass** | `docs/architecture/overview.md` was created at v1 by `plan` and describes exactly what was built; `docs/product/vision.md` reached v9 before the code existed. The implementation contradicted neither, so neither needed a further bump |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → *all 3 commit(s) on main..wi/WI-0001 name WI-0001* |
| D9 | merged into the trunk | **pass** | merged after this review was written and the item closed, per the skill's ordering; the merge commit is named in the journal entry for this execution |
| D10 | verification postdates the code | **pass** | `check-verify-freshness` as quoted above: the only commit after the verified one changes five files, all under `tracker/` |
| D11 | the review record says what was examined | **pass** | this document's `## What I examined`, including the per-hunk mapping table |
| D12 | claims in `docs/` about this behaviour are still true | **pass** | re-read `docs/architecture/overview.md` §"The pieces", §"The data" and §"The conventions every command follows" against the code: the three-layer split, the `{"schema": 1, "people": [...]}` envelope, the atomic write, the `--data-file` position and the exit-code table all match what `git diff` shows. One claim needed checking rather than remembering — "the launcher resolves its own real path so that a symlink on `PATH` still finds the package" — and `expenses` line 11 does exactly that, though no test exercises the symlink case (see `## Accepted gaps`) |

## Findings

Two, neither of them a send-back:

1. **`store.save` is not wrapped, so an unwritable `--data-file` path produces a traceback rather
   than a refusal.** `cmd_add_person` catches `DataFileError` around `load` but nothing around
   `save`, so `mkstemp` raising `PermissionError` reaches the user as a Python traceback. This is
   the behaviour the item's `## Notes` records as deliberately unconstrained by `refine`, and
   `impl-report.md` declares it plainly, so it is an accepted gap rather than a defect — but it is
   the one place the tool falls short of ADR-0005 clause 2's shape for a refusal, and it is now
   written into the item's `## Notes` so that it survives this item being closed.
2. **`except BaseException` in `save` is broad, and correct here.** It exists to delete the
   temporary file on `KeyboardInterrupt` as well as on an error, and it re-raises immediately, so
   nothing is swallowed. Noted rather than raised as a finding, because a reader skimming for
   bare-except smells will stop at it: the comment above it explains why, and AC7's
   "exactly one new file in `$HOME`" is what would catch a regression.

Nothing else in the diff would be uncomfortable to maintain. The message strings live in one
module, the identity rule is defined once and reused by both the duplicate check and the sort, and
the data-file guard clauses each produce a distinct, specific `reason` rather than a single
catch-all.

## Accepted gaps

Each is recorded in the item's `## Notes` under "Accepted gaps at close", so it outlives this
report:

- **An unwritable `--data-file` path produces a traceback**, not a refusal. Finding 1 above.
- **The optional `PATH` install is unexercised.** Every criterion runs `./expenses` from the
  repository root, so the symlink path ADR-0008 clause 2 exists to support has no test.
  `plan.md` `## Risks` calls this the most likely way a real user's first run fails.
- **`commands.lint` is a syntax check, not a style linter.** `compileall` proves the files parse.
  No style linter is installed and none can be installed here (ADR-0007 clause 4).
- **Crash-during-write atomicity rests on `os.replace`'s documented behaviour**, not on a test;
  killing the process mid-write is not something this suite can arrange.
- **Non-ASCII names are covered by a unit test only** (`José` and `Jose` stay distinct), not
  through the command line.
- **`argparse`'s usage wording is unchecked.** Its exit code 2 is asserted; the text is not, which
  is what the item's R10 note says.

None of these contradicts a criterion. All six are things nobody asked for or things the record
already says are unconstrained — which is why they are accepted rather than sent back.

## Verdict

**Accepted.** The change does what WI-0001's criteria say, in a shape this project should live
with, and the record supports reconstructing it: what was asked (`item.md`, `refinement-qa.md`),
who decided what (seven journal entries, eight ADRs), what was built (`plan.md`,
`impl-report.md`), what was checked and how (`verify-report.md`, with commands and output), and
what remains unchecked (six accepted gaps, now in the item's `## Notes`).
