# Plan — BUG-0005 README does not say what tidy exits with when every move fails

## Problem

`README.md` lists three exit statuses and a reader uses that list to predict one. Its third clause
says 1 is what you get "when some file could not be moved while others were", and there is a run
whose status it does not let a reader predict: when every move fails and nothing lands, `tidy`
also exits 1 [src: BUG-0005]. The change is one paragraph of `README.md` plus one regression test
that pins the behaviour the paragraph will describe. **No production code changes**, and the
constraints on the edit are tight: the same paragraph is load-bearing for BUG-0001 AC2 (the
exit-2 clause covering does-not-exist, not-a-folder and cannot-be-read) and for WI-0003 AC12
(that paragraph naming `--rules`), so a rewrite that improves the third clause and drops either of
those breaks a criterion two closed items were verified against [src: BUG-0001 AC2;
src: WI-0003 AC12].

## Approach

Change the sentence, not the tool. `cli.main`'s last statement is
`return 1 if any(outcome.kind == "failed" for outcome in outcomes) else 0` — one predicate, no
count and no ratio — so 1 has always meant "at least one intended move failed" and the README's
"while others were" is a condition the code never evaluated [src: tidy/cli.py; src: ADR-0007].
ADR-0012 records the decision to keep three statuses and say what 1 means, rather than to add a
fourth status for the all-fail case, which is the alternative BUG-0005's `## Notes` names
[src: ADR-0012].

The edit is surgical: the paragraph's first two clauses and its closing sentence are kept
**verbatim**, and only the third clause is replaced. Doing it that way is what makes AC2
inspectable — a reviewer diffs one clause rather than re-deriving whether a rewritten paragraph
still satisfies two other items' criteria.

The test is a new class in `tests/test_cli.py` beside `FallbackExitStatusTests`, built the way
BUG-0005's own reproduction is built: a `recent/` folder at mode `0o500` so that every
destination's `os.makedirs` fails, two files that would move into it, `--apply`, and an assertion
that the status is 1 and both files are still where they were. It uses the probe-based skip that
`FallbackExitStatusTests.test_a_genuine_failure_alongside_a_fallback_still_exits_1` already uses —
write into the restricted folder and skip if the write succeeds — because that guard covers both
running as root and a filesystem that does not enforce the mode, which AC3 asks for
[src: tests/test_cli.py; src: BUG-0005 AC3].

## Steps

1. **Read the paragraph as it stands** so the edit in step 2 is against the current text, not
   against the version quoted in BUG-0005: `grep -n "Exit status" -A4 README.md`. The item's
   `## Actual behaviour` quotes the pre-WI-0003 wording; the live paragraph is at `README.md:35`
   and its exit-2 clause now names `--rules` as well [src: README.md].

2. **In `README.md`, replace the third clause only** [src: README.md; src: BUG-0005 AC2]. In the
   paragraph beginning "Exit status is 0 on success", the text
   `and 1 when some file could not be moved while others were.`
   becomes
   `and 1 when a file that was going to move could not be — whether that is one of them, some of them, or all of them.`
   Everything else in the paragraph is untouched: the 0 clause including "when there was nothing
   to do, and when some files were left where they are", the 2 clause including all four of
   does-not-exist, not-a-folder, cannot-be-read and the `--rules` file, and the closing sentence
   about one line on stderr and nothing on stdout. Afterwards `git diff README.md` shows one
   changed clause and no other line of that paragraph moved.

3. **Add `class AllMovesFailExitStatusTests(FolderTestCase)` to `tests/test_cli.py`**, placed
   immediately after `FallbackExitStatusTests` so the two exit-status reproductions read together
   [src: tests/test_cli.py; src: BUG-0005 AC3]. One test method,
   `test_a_run_in_which_every_move_fails_exits_1`. It must:
   - write two files that move into two different type folders under the same band — `photo.jpg`
     and `doc.pdf`, whose destinations are `recent/images/` and `recent/documents/`, the pair
     BUG-0005's reproduction uses;
   - create the band folder `recent` and set it to mode `0o500`, registering the restoring
     `chmod` with `addCleanup` **before** the mode is changed, exactly as
     `FallbackExitStatusTests` does, so a failing assertion cannot leave an undeletable tree;
   - skip via the probe guard — attempt to create a file inside the restricted folder, and
     `self.skipTest(...)` with the existing wording if that write succeeds;
   - run `--apply` and assert: status is 1; both files are still at the top level of the folder;
     neither destination exists; and stderr carries one `could not be moved`-class line per file
     naming it.

   The assertion is on the status and on where the files are — do not assert the exact stderr
   wording of the `makedirs` failure, which is the operating system's string and is already
   covered by `tests.test_cli`'s BUG-0004 and BUG-0002 cases.

4. **Run the suite and the linter** from the repository root: `python3 -m unittest discover -s
   tests -t . -q` and `python3 -m compileall -q tidy tests`, both exit 0. The new test must appear
   in the count — `python3 -m unittest tests.test_cli.AllMovesFailExitStatusTests -v` shows it as
   `ok` and not as `skipped` on this machine, which is what proves the guard did not swallow the
   case it exists to run.

5. **Demonstrate AC1 by running the item's own reproduction**, not the test: build the folder from
   BUG-0005 `## Steps to reproduce`, run `python3 -m tidy <folder> --apply; echo "EXIT: $?"`,
   confirm `EXIT: 1` and that `find` shows both files unmoved, then read the amended paragraph and
   check it accounts for that run. Clean up with the `chmod 0700` the item's step 4 gives.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — the paragraph describes the exit code of a run in which no file moved | 2 | Step 5's run of BUG-0005 `## Steps to reproduce`: `EXIT: 1`, `find` shows `photo.jpg` and `doc.pdf` still at the top level, and the amended clause — "1 when a file that was going to move could not be — whether that is one of them, some of them, or all of them" — covers it without the reader inferring anything |
| AC2 — 0, 2 and the partial case still described correctly | 2 | `git diff README.md`: exactly one clause of the paragraph changed. The 2 clause is character-identical to the form BUG-0001 AC2 put it in, extended by WI-0003 with `--rules`, and the new 1 clause names the partial case first ("one of them") |
| AC3 — a regression test pins the all-fail exit 1, skipping under root or a non-enforcing filesystem | 3 | `tests.test_cli.AllMovesFailExitStatusTests.test_a_run_in_which_every_move_fails_exits_1` asserts `result.status == 1` with both files unmoved; `python3 -m unittest tests.test_cli.AllMovesFailExitStatusTests -v` reports `ok` here, and the probe guard makes it `skipped` where mode `0o500` is not enforced |

## Assumptions

- **A1 — the test lives in `tests/test_cli.py` rather than a new module.** It is a CLI-level
  reproduction asserting an exit status, which is what that module already holds, and it belongs
  beside `FallbackExitStatusTests` because the two are the exit-status pair
  [src: tests/test_cli.py]. Reversing it is moving one class to a new file with its imports: one
  file, no interface change, no data migration.
- **A2 — the fix is one sentence rather than a bulleted list of the three statuses.** A list would
  read better and is what a longer paragraph eventually wants, but it would rewrite text BUG-0001
  AC2 and WI-0003 AC12 are verified against, turning a one-clause diff into a paragraph a reviewer
  must re-check against two closed items. Reversing it is one paragraph edit in `README.md`, and
  the sentence this plan writes is the content that list would carry.
- **A3 — mode `0o500` on the band folder is the way to make every move fail.** It is what
  BUG-0005's reproduction uses and what the existing test uses for one file; the alternative,
  mocking `os.makedirs`, would test the code's reaction to a mock rather than to a filesystem.
  Reversing it is rewriting one test method, and the probe guard is what keeps it honest where the
  mode is not enforced.

## Decisions and ADRs

| decision | how it was made | where it is recorded |
|----------|-----------------|----------------------|
| Keep three exit statuses and state 1 as "at least one intended move failed", rather than adding a fourth status for the all-fail run | decided — the alternative is named in BUG-0005 `## Notes` and adding a number to a published contract is not an edit | **ADR-0012** (new), citing ADR-0006's rejection of the same growth for the unusable-target case and ADR-0007 for the predicate `cli.py` actually evaluates |
| No production code changes | documented — `cli.main`'s last statement already implements the predicate the new wording states, so there is nothing to change | ADR-0012 `## Decision`; `tidy/cli.py` |
| Only the third clause of the paragraph is replaced | assumed, and reversible | `## Assumptions` A2 |
| The regression test's location and construction | assumed, and reversible | `## Assumptions` A1 and A3 |

`tracker/project.yaml` already carries real commands — `commands.test` is
`python3 -m unittest discover -s tests -t . -q` and `commands.lint` is
`python3 -m compileall -q tidy tests`, both chosen by ADR-0004 and both run by this execution
[src: ADR-0004; src: tracker/project.yaml]. Nothing here changes the shape of the system, so
`docs/architecture/overview.md` is deliberately not touched: it describes modules and boundaries,
and this item moves neither.

## Scaffolding

none.

## Risks

- **The paragraph is load-bearing for two closed items, and the obvious rewrite breaks them.**
  BUG-0001 AC2 fixed the exit-2 clause's form and WI-0003 AC12 requires this paragraph to name
  `--rules`; a reviewer who rewrites the whole paragraph for readability satisfies AC1 and AC2
  while quietly invalidating two items' verification. Step 2 is written as a one-clause
  replacement for exactly this reason, and AC2's demonstration is a diff rather than a re-read.
- **The test can pass by being skipped.** A probe guard that skips on this machine would leave AC3
  demonstrated by a test that never ran. Step 4 requires the `-v` run showing `ok`, not the
  suite's aggregate, and `verify` should re-do that rather than trust the count.
- **`0o500` may not stop `os.makedirs` under an unusual `umask` or filesystem.** The guard covers
  it by skipping, but a run where the guard passes and the makedirs then succeeds would fail with
  a confusing assertion rather than skip. If that happens the test is wrong about the platform,
  not about the tool, and the fix is the guard, not the assertion.
- **`inf`-style edge readings of "a file that was going to move".** A `leave` line is not a file
  that was going to move, and the 0 clause already says so; if a reviewer reads the new clause as
  covering leaves, the wording needs one more word, not a code change [src: ADR-0009].

## Out of scope for this item

- **A fourth exit status for a total failure.** Considered and declined in ADR-0012; taking it
  later is a new item with a code change, not a re-read of this one.
- **Restructuring the exit-status paragraph into a list**, and any other readability work on
  `README.md`. See A2.
- **Anything in `tidy/`.** The behaviour is correct; only the description of it is incomplete
  [src: BUG-0005].
- **BUG-0006**, the other open record defect, which is about a citation in ADR-0008 and shares no
  file with this item [src: BUG-0006].
