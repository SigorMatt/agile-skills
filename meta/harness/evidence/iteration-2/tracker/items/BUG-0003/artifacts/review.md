# Review — BUG-0003

## What I examined

- `tracker/items/BUG-0003/item.md` — the four criteria and their tick state, `## Summary`,
  `## Steps to reproduce`, `## Expected behaviour` and `## Actual behaviour`.
- `tracker/items/BUG-0003/history.md` — five rows, `— → ready → planned → in-progress →
  verifying → in-review`; the chain has no gap and its last row matches `item.md`.
- `tracker/items/BUG-0003/journal.md` — all five entries, read in full: `verify`'s creation entry
  of 19:11:48Z, `plan` at 20:24:28Z, `implement`'s opening and closing entries at 20:25:17Z and
  20:27:54Z, and `verify` at 20:32:45Z. One entry per history row.
- `tracker/items/BUG-0003/artifacts/plan.md`, `impl-report.md` and `verify-report.md` — in that
  order, with `## What I did not do` and `## Not verified, and why` read as the declared gaps.
- `tracker/items/BUG-0003/questions/` — empty. No question was raised at any stage of this item.
- **The diff, hunk by hunk:** `git diff main..wi/BUG-0003 -- tidy tests`, three hunks in two
  files, plus `git log --oneline main..wi/BUG-0003` (five commits) and
  `git diff main..wi/BUG-0003 --stat` (nine files, the other seven under `tracker/` and `docs/`).
- **The behaviour, not only its description:** `python3 -m tidy --help` run in this execution
  (exit 0, output read whole), `python3 -m unittest discover -s tests -t . -q` (exit 0, `Ran 69
  tests ... OK`), and `python3 -m compileall -q tidy tests` (exit 0).
- **ADRs:** ADR-0008 in full, as the decision this item carries; ADR-0002 and ADR-0005 for the
  layering and the band table the change touches by reference; ADR-0001 and ADR-0004 for the
  stdlib and command constraints. ADR-0003, ADR-0006 and ADR-0007 concern `apply.py`'s move
  routes, which this diff does not reach.
- `docs/architecture/overview.md` v6 §"Where the remaining item will touch this", and
  `README.md` §"Where each file goes" — the standard AC2 names.

### The claims I audited, and what I opened to decide each (D12)

| claim | where | what I opened | verdict |
|-------|-------|---------------|---------|
| "`cli.py` holds the `--help` text as prose and imports nothing from `rules.py`" | `docs/architecture/overview.md`:102 | `tidy/cli.py` — `grep -n "^from\|^import" tidy/cli.py` → five imports: `argparse`, `os`, `sys`, `.apply`, `.planner` | **true** |
| "a band name that `DEFAULT_BANDS` declares and the help output omits should be a test failure" | `docs/architecture/overview.md`:105 | `tests/test_cli.py`:39-41 — the loop is `for band, _bound in DEFAULT_BANDS: self.assertRegex(result.stdout, r"\b%s\b" % re.escape(band))`, so a declared band absent from the output fails the assertion | **true**, and `verify` demonstrated it by adding a third band |
| "`tests/test_cli.py` contains an import of `DEFAULT_BANDS` used in an assertion over the help output" | ADR-0008 `## Decision` | `tests/test_cli.py`:14 (`from tidy.rules import DEFAULT_BANDS`) and :40 (used in the assertion above) | **true** |
| "Both rule tables are in README.md" — the epilog's own claim, and AC2's standard | `tidy/cli.py` epilog; `README.md` §"Where each file goes" | `README.md`:42-52 (`### The band: how old the file is`) and :54-67 (`### The type folder, inside the band`) — two tables, no third | **true** |
| "`tests/` holds four test modules and two helpers, and `python3 -m unittest ... -q` runs **37 tests** and exits 0" | ADR-0004 `## Consequences`, the "superseded by fact" note | `ls tests/` — four test modules and two helpers, still true; `python3 -m unittest discover -s tests -t . -q` → `Ran 69 tests ... OK` | **module count true, test count false — corrected in this execution.** See Finding 1 |
| "`python3 -m tidy --help` still tells the reader that a destination is 'chosen by file type'" | ADR-0008 `## Context` | `python3 -m tidy --help` on the branch — it no longer says this | **false as present tense, deliberately left.** See Finding 2 |

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion checkbox ticked | **pass** | `item.md` AC1-AC4 all `[x]`; `validate-workspace .` → exit 0, 0 errors 0 warnings, which is the `[auto]` decision |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | Four rows in `## Criteria`, each naming a command `verify` ran and quoting its real output: AC1 the four word-boundary counts (`\brecent\b` 1, `\bold\b` 2, `\bmodified\b` 1, `\bage\b` 0), AC2 `grep -c 'extension-to-folder'` → 0, AC3 the grep WI-0001's verification recorded, AC4 the full-revert run and an AST extraction of the test's literals. No row's evidence is `impl-report.md` |
| D3 | gates passed on the **final** state of the code | **pass** | Re-run by me on branch head `7a8d9f9`: tests exit 0 `Ran 69 tests ... OK`, `compileall` exit 0. And again on the **trial merge result** `4420b83`, with `PYTHONDONTWRITEBYTECODE=1` and no stale bytecode: exit 0, `Ran 69 tests ... OK`, `compileall` exit 0. No code file has changed since `46e5fd0`; everything after it is `tracker/` and `docs/` |
| D4 | no open blocking question | **pass** | `tracker/items/BUG-0003/questions/` is empty; no skill raised one at any stage. `validate-workspace` exit 0 |
| D5 | a journal entry per skill execution, history chains without a gap | **pass** | Five history rows, five journal entries, matched one to one by timestamp and actor; the last row's `to` is `in-review`, which is `item.md`'s status. `validate-workspace` exit 0 |
| D6 | every design decision in an ADR, cited from the plan or journal | **pass** | One decision was taken: ADR-0008 (the help text stays prose, guarded by a test that reads `DEFAULT_BANDS`). Cited from `plan.md` `## Approach` and `## Decisions and ADRs`, and from `plan`'s and `implement`'s journal entries. The four smaller choices are in `plan.md` `## Assumptions`, each with what reversing costs — correctly not ADRs: none of them changes an interface, a data format or a layer |
| D7 | documents the change invalidated updated, with a version bump and a change-log row | **pass, after this execution corrected one** | `plan` wrote ADR-0008 v1 and took `docs/architecture/overview.md` v5 → v6, each with its change-log row. ADR-0004's test count was invalidated by this item and by three before it; corrected here to v3, `updated-for: BUG-0003`, with a change-log row — Finding 1 |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs BUG-0003 wi/BUG-0003` → exit 0, "all 5 commit(s) on main..wi/BUG-0003 name BUG-0003", re-run after this execution's own commit |
| D9 | merged into the trunk | **pass** | Trial-merged into a **detached** worktree at `main` (`4420b83`), suite green on the merge result, trial discarded, and `git rev-parse main` returned `b76b27c` both before and after — unmoved. The real merge follows this transition, because the order is forced: `check-commit-refs` reads `main..wi/BUG-0003` and merging first empties that range. The merge commit sha is recorded in `## Verdict` |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness BUG-0003 wi/BUG-0003` → exit 0: verified at `f575fc9`, branch has moved to `7a8d9f9` but "only the record changed" — the moves are `bfdaec1` (the verification report) and `7a8d9f9` (this execution's ADR-0004 correction), both under `tracker/` or `docs/`. `git diff f575fc9..7a8d9f9 -- tidy tests` is empty |
| D11 | `review.md` exists and states what was examined | **pass** | This file; `## What I examined` is first and names every artifact, the diff range, the commands re-run, and the six claims audited with what was opened for each |
| D12 | claims in `docs/` about the behaviour this item touched are still true, checked against the code | **pass, with one correction and one deliberate exception** | The table under `## What I examined`: four claims verified true by opening the code they cite, one found false and corrected (Finding 1), one left as a dated `## Context` (Finding 2). `lint-claims --changed-since main` → exit 0, 1 document |

## Findings

**1. ADR-0004's "runs 37 tests" had been false since WI-0002. Corrected here, and the shape of
the claim changed so it stops going stale.**

`ADR-0004` `## Consequences` carried "`tests/` holds four test modules and two helpers, and
`python3 -m unittest discover -s tests -t . -q` runs 37 tests and exits **0**". The module count
is still true — `ls tests/` gives `test_apply.py`, `test_cli.py`, `test_planner.py`,
`test_rules.py`, `cli_support.py`, `support.py`. The test count is not: the command reports `Ran
69 tests ... OK`. It was written by WI-0001's review as a D12 correction of its own, and WI-0002,
BUG-0001 and BUG-0002 each added tests without anyone noticing it had gone false again; this item
made it 69.

This is the D12 failure mode with a twist worth naming: the sentence was corrected once and then
went stale again, because what it asserts is a **number that every item changes**. So the fix is
not only the arithmetic. ADR-0004 v3 now makes the standing claim the *exit status* — the thing
the ADR is actually about — and marks the count as a dated measurement taken while closing
BUG-0003, with a paragraph recording that three items falsified the old form without notice.
`updated-for: BUG-0003`, version 2 → 3, change-log row written, `lint-claims --changed-since
main` → exit 0.

Not a send-back: the claim is not about this item's delivered behaviour, and the correction is
one document with no code consequence. It is D7 and D12 discharged, which is this skill's job.

**2. ADR-0008's `## Context` says the help text "still tells the reader ... chosen by file type",
which BUG-0003 has now made false. Left as written, deliberately.**

An ADR's `## Context` is the dated statement of the problem that forced the decision; it is
signed, timestamped and names the item it was written for. Rewriting it into the past tense after
the fix would edit the reasoning rather than correct a fact, and a reader who reaches ADR-0008
through `git log` or through the overview arrives with BUG-0003 already in hand. Recorded here so
that the exception is visible rather than an omission — the distinction that matters is between a
document that *asserts* current behaviour (ADR-0004's note, Finding 1) and one that *narrates*
why a decision was taken.

**3. Every hunk in the diff serves a criterion. Nothing is unrequested.**

Three hunks, and the mapping is one to one:

- `tidy/cli.py` `description` — AC1 (age takes part in choosing the destination). The word `type`
  survives as "what kind of file it is", which is what keeps the sentence true rather than merely
  different.
- `tidy/cli.py` `epilog` — AC1 (names `recent` and `old`, says the band comes from "when the file
  was last modified") and AC2 ("Both rule tables are in README.md"; `extension-to-folder` is
  gone). Its first and last sentences are byte-identical to `main`, which is what keeps AC3's
  four substrings alive — I checked that against the diff rather than against the report.
- `tests/test_cli.py` — AC4: `import re`, `from tidy.rules import DEFAULT_BANDS`, the module
  docstring's coverage list, one traceability comment on the existing help test whose assertions
  are untouched, and the new test.

No production module other than `cli.py` is touched; `planner.py`, `rules.py` and `apply.py` are
byte-for-byte `main`. Nothing contradicts an ADR: ADR-0002's "destinations are decided in
`planner.py` alone" is untouched because no destination logic moved, and ADR-0008 is this diff's
own decision, honoured exactly — `cli.py` imports nothing from `rules.py`, and the coupling lives
in the test.

**4. The word boundary is load-bearing, and I measured it rather than reading it.**

On the **delivered** help text, `grep -c 'old'` matches 7 lines and `grep -c '\bold\b'` matches 2;
`plan` recorded the same measurement against the **broken** text, where the counts are 5 and 0. So
`assertIn("old", stdout)` would have passed against the exact wording this bug was filed about.
The delivered test uses `assertRegex` with `\b...\b` and `re.escape` on the band name. This is the
single detail that decides whether the regression test guards anything, it is invisible to a
reader who only reads the assertion, and it is documented in the test's own docstring where the
next person to edit it will meet it.

**5. A maintainability note on the age assertion, accepted rather than sent back.**

The band loop uses `assertRegex`, so a failure prints the pattern and the text. The age check is
`assertTrue(any(re.search(...) for word in (...)))`, so its failure message is `False is not
true` — a future maintainer sees that something failed but not what was expected, and the
four-word vocabulary is only in the source. `assertRegex(result.stdout, r"\b(modified|age|aged|
older)\b")` would fail with the pattern in the message. This is a diagnostic-quality point, not a
correctness one: the assertion is correct, the vocabulary is explained by the comment above it,
and changing it now would be a change no criterion asked for on a file that has been verified.
Recorded here and in `item.md` `## Notes` so that whoever next touches this test finds it.

**6. `verify`'s AC4 finding: I take the same reading, for the reason it gave, and accept the gap.**

`verify` measured that reverting `description` alone, while keeping the new epilog, leaves the
suite green — so under the strict reading of AC4 ("fails when the **description** is reverted",
where `description` is the argparse argument the item's `## Summary` names by line number) the
delivered test does not satisfy the criterion; under the loose reading (the tool's description of
itself) it does. I checked the three artifacts it cites rather than accepting the summary of them:
this item's journal entry of 19:11:48Z glosses AC4 as guarding "the claim rather than the
wording", AC1's own checkable clause says "grepping the help **output**", and `plan.md`'s AC
mapping reads it the same way. None of the three supports the strict reading, and the criterion's
author is the same skill that wrote the gloss.

So AC4 stands as met. The residual hole is real and narrow — a future edit that reverts the
description while leaving the epilog correct would leave the help text self-contradictory with no
test objecting — and it is accepted rather than filed: it is not defective delivered behaviour
(the text is right today), it is not a failure of this item's criteria under the reading the
record supports, and widening the guard means asserting something about the description
specifically, which is a decision about the *criterion*, not a defect in the code. It goes into
`item.md` `## Notes` with the measurement, so whoever widens it later finds the experiment rather
than repeating it.

Worth saying plainly, because it is the best thing in this item's record: `verify` took the
reading that made the criterion pass, and then wrote down the experiment that would have failed
it. That is what made this finding reviewable at all.

**7. `check-commit-refs` reported a false failure again, exactly as predicted. Still a toolkit
defect, still not this item's.**

At `implement`'s `planned → in-progress` transition the branch had just been created and held zero
commits, so `main..wi/BUG-0003` was empty; the script read the empty range as "already merged into
`main`" and advised rewinding a merge that never happened. It is recorded in `impl-report.md`
`## What I did not do` item 3, it was recorded as latent in BUG-0002's review as Finding 5, and it
has now fired at the moment the pipeline creates every branch. Nothing was lost — the gate does
not block that move, and it exits 0 on this branch now (five commits) — but it is a false failure
in a hard gate's output, which teaches readers to skim gate results. It belongs to the methodology
under `.claude/agile-skills/`, not to the `tidy` product, so there is no item in this tracker it
could be filed against; it goes to the toolkit's owner through the same channel as the last two
sightings.

## Accepted gaps

Each is now in `item.md` `## Notes`, because a gap that lives only in a report stops being read
the moment the item closes.

| gap | source | disposition |
|-----|--------|-------------|
| reverting `description` alone leaves the suite green — the strict reading of AC4 | `verify-report.md` `## Defects found`; this review, Finding 6 | **accepted** — the record settles the reading; the measurement is preserved for whoever widens the guard |
| the extension table (`DEFAULT_RULES`) is unguarded in the direction the bands now are | `impl-report.md` 1; ADR-0008 `## Consequences` | **accepted** — the help text names no extensions, so there is nothing to compare; ADR-0008 says what should happen if a later item makes it list them |
| the age assertion's failure message names nothing | this review, Finding 5 | **accepted** — diagnostic quality, not correctness; no criterion asked for it and the file is verified |
| `--help` exercised under this environment's locale only | `verify-report.md` `## Not verified` | **accepted** — the strings are ASCII and `argparse` does not translate them, which is an inference and is labelled as one |
| whether the wording is *good*, as opposed to true and complete | `verify-report.md` `## Not verified` | **accepted** — `plan` was asked to settle the wording and did; no criterion constrains readability |
| the rest of `README.md` was not audited | `verify-report.md` `## Not verified` | **already recorded** — BUG-0005 is open against a different part of the same file |
| `check-commit-refs`' false failure on an empty branch | `impl-report.md` 3; BUG-0002 `review.md` Finding 5 | **not this project's** — a defect in the methodology under `.claude/agile-skills/`, reported to its owner; no tracker item can hold it |

## Verdict

**Accepted, merged and closed. `outcome: delivered`.**

All four acceptance criteria are met and independently evidenced, and every Definition of Done
criterion passes with its own evidence. The change is three hunks in two files, each traceable to
a criterion, with no production module touched but `cli.py` and no behaviour changed — no
destination, no exit status, no output line. The record is complete enough that a reader holding
only `tracker/`, `docs/` and `git log --grep BUG-0003` can say what was built, why the text went
stale without anyone editing it, which skill decided what, that no question was raised at any
stage, and what verification found including the one thing it could not settle cleanly.

One document was corrected on the way through: ADR-0004's test count, false since WI-0002 and
re-shaped so the standing claim is the exit status rather than a number every item moves. Six
gaps are accepted with reasons and all six now live in `item.md` `## Notes`. No bug was filed
against this project; the one defect this execution saw belongs to the methodology, not to
`tidy`.

Merged into `main` as `da060557fc68cd8d7443c9509e469fc70c126585`, after the item was closed — that order is required, because
`check-commit-refs` reads `main..wi/BUG-0003` and merging empties the range. The suite was re-run
on `main` after the merge: exit 0, `Ran 69 tests ... OK`.
