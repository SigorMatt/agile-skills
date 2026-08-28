# Implementation report — BUG-0005

## What was built

One clause of `README.md` and one regression test. No production code changed, which is what the
plan predicted: `cli.main`'s last statement is
`return 1 if any(outcome.kind == "failed" for outcome in outcomes) else 0`, a single predicate with
no count and no ratio, so 1 has always meant "at least one intended move failed" and the README's
"while others were" was a condition the code never evaluated.

**`README.md:38-40`** — the third clause of the exit-status paragraph now reads:

> and 1 when a file that was going to move could not be — whether that is one of them, some of
> them, or all of them.

replacing:

> and 1 when some file could not be moved while others were.

**`tests/test_cli.py`** — a new `AllMovesFailExitStatusTests`, placed immediately after
`FallbackExitStatusTests`, with one method
`test_a_run_in_which_every_move_fails_exits_1`. It writes `photo.jpg` and `doc.pdf`, creates the
band folder `recent/` and sets it to mode `0o500` so that both destinations' `os.makedirs` fail,
probes the restricted folder and skips if the write succeeds, runs `--apply`, and asserts the
status is 1, both files are still at the top level, neither `recent/images` nor `recent/documents`
was created, and stderr carries exactly two failure lines, one naming each file.

The test count went from 157 to 158.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| **AC1** — the paragraph describes the exit code of a run in which no file moved | The clause now names the all-fail case explicitly ("or all of them") instead of requiring the reader to infer it from a condition that excludes it | The item's own `## Steps to reproduce`, run on this branch: `python3 -m tidy .harness/rc/allfail --apply; echo "EXIT: $?"` printed two `could not create the folder for …; <file> was left where it is` lines and `EXIT: 1`; `find .harness/rc/allfail -type f` then listed `doc.pdf` and `photo.jpg`, both still at the top level. Both files were going to move — the run printed `move doc.pdf -> recent/documents/doc.pdf` and `move photo.jpg -> recent/images/photo.jpg` — neither could, and the amended clause's "all of them" is that run. Cleaned up with the item's step 4 |
| **AC2** — 0, 2 and the partial case still described correctly | Only the third clause was replaced; the rest of the paragraph is character-identical | `git diff main..wi/BUG-0005 -- README.md` → 5 lines changed, all inside the third clause and the reflow it forced. The 0 clause ("including when there was nothing to do, and when some files were left where they are") and the 2 clause (does-not-exist, not-a-folder, cannot-be-read, and the `--rules` file) are untouched lines in the diff, and the closing sentence "Anything that stops the run before it starts gets one line on stderr saying so, and nothing on stdout." is unchanged in wording — it moved across a line boundary only because the new clause is longer. The partial case is still described, and is now first in the new clause: "one of them" |
| **AC3** — a regression test pins the all-fail exit 1, skipping rather than failing where mode `0o500` is not enforced | `tests.test_cli.AllMovesFailExitStatusTests.test_a_run_in_which_every_move_fails_exits_1` | `python3 -m unittest tests.test_cli.AllMovesFailExitStatusTests -v` → exit 0, `test_a_run_in_which_every_move_fails_exits_1 … ok` — **`ok`, not `skipped`**, so the guard did not swallow the case on this machine. The guard itself is the probe `FallbackExitStatusTests` uses verbatim: open a file inside the `0o500` folder, and `skipTest` with the existing wording if that write succeeds, which covers both root and a non-enforcing filesystem. **Mutation-checked**: with `cli.main`'s final statement temporarily replaced by `return 0`, the test failed with `AssertionError: 0 != 1` at the `self.assertEqual(result.status, 1)` line; `tidy/cli.py` was restored from a copy and `git status --porcelain tidy/cli.py` then reported no changes |

## Deviations from the plan

Two, both about wording rather than substance.

1. **The stderr assertion matches `was left where it is`, not `could not be moved`.** Plan step 3
   asks for "one `could not be moved`-class line per file". An all-fail run under a `0o500` band
   folder fails at `os.makedirs`, not at the move, so the line `tidy/apply.py` emits is
   `could not create the folder for %s: %s; %s was left where it is` — the string
   `could not be moved` never appears. The test asserts what the plan asked for in substance: one
   failure line per file, naming it, without asserting the operating system's message. The plan
   explicitly forbids asserting that message, so this is the reading that satisfies both halves of
   the step.

2. **`tests/test_cli.py`'s module docstring gained `and BUG-0005 AC3`.** The plan does not mention
   it. The docstring is the module's list of which criteria it covers, and leaving it out would
   have made it false the moment the class landed. One line, no behaviour.

Not a deviation, but worth stating: the replacement clause is the plan's text **verbatim**,
including its internal em dash. That dash sits inside a sentence whose top-level clauses are also
separated by em dashes, which a reader could briefly misread as a fourth exit-code clause opening.
It resolves immediately — "whether" cannot begin one — and re-litigating the architect's chosen
wording is not this skill's job, so it went in as written. Recorded here so `verify` and
`review-close` can take their own view with the observation in front of them rather than having to
notice it.

## Gates

All run on `05be040`, the head of `wi/BUG-0005` at the time and the branch's only code commit,
after the last change. The tracker commit that carries this report and the journal entries sits
on top of it, so `main..wi/BUG-0005` is two commits and the code diff is unchanged by the second.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 158 tests in 0.167s / OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 10 items, 14 documents, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | AC3 is `AllMovesFailExitStatusTests.test_a_run_in_which_every_move_fails_exits_1`, shown `ok` under `-v` and shown failing under a mutation. AC1 and AC2 are claims about a paragraph, so their evidence is a reproducible command and its output rather than a test function: AC1 is the item's own `## Steps to reproduce` run above, whose `EXIT: 1` the amended clause must account for, and AC2 is `git diff main..wi/BUG-0005 -- README.md` showing one clause changed. Neither is demonstrated by reading the code |
| `commits-reference-the-item` | **pass** | `check-commit-refs BUG-0005 wi/BUG-0005` → exit 0, `all 1 commit(s) on main..wi/BUG-0005 name BUG-0005` |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main..wi/BUG-0005 --stat` → `README.md 5 +++--`, `tests/test_cli.py 52 +++…`. Every hunk traces to a plan step: the README hunk is step 2, the test class is step 3, and the docstring line is deviation 2 above. Nothing under `tidy/` is touched, which the plan requires |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0, `checked no documents changed since main`. The gate is scoped to headed documents under `docs/`, and this branch changes none — `README.md` is not one of them. It is a genuine pass on an empty set, not a skip |

## What I did not do

- **Nothing in `tidy/`.** The behaviour is correct and the plan forbids touching it. `tidy/cli.py`
  was temporarily mutated to prove the new test fails without the behaviour, and restored; the
  branch diff contains no production file.
- **No fourth exit status** for a total failure. ADR-0012 declined it and it is on the item's
  out-of-scope list.
- **No restructuring of the exit-status paragraph into a list**, per assumption A2 — the readable
  rewrite is the one that would quietly invalidate BUG-0001 AC2 and WI-0003 AC12.
- **`docs/architecture/overview.md` was not touched**, following the plan: no module or boundary
  moved.
- **BUG-0006 was not touched.** It is the other open record defect and shares no file with this
  item.
- **The item's three AC checkboxes are still unticked.** Ticking them is `verify`'s call, not
  this skill's.
