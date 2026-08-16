# Review — BUG-0002

## What I examined

- `item.md` — the seven criteria, both triggers, the control, `## Expected behaviour` with its
  quotations from WI-0001 AC10 and ADR-0005, and the `## Notes` observation about `--top`'s label
- `history.md` — four rows, checked against `pipeline.yaml`; `journal.md` — all four entries in
  full
- `artifacts/plan.md`, `impl-report.md`, `verify-report.md`; no questions were filed on this item
- `docs/architecture/adr/ADR-0007` (written for it), `ADR-0002`, `ADR-0005`, `ADR-0006`,
  `docs/architecture/overview.md` v3
- **the diff**, hunk by hunk: `git diff main..wi/BUG-0002 -- linecount.py tests/` — `linecount.py`
  +14/−5, `tests/test_linecount.py` +72/−0

Three code hunks, each traceable:

| hunk | serves |
|------|--------|
| `format_report` gains `empty="no files"`; the no-rows branch returns `f"{empty}\n"`; the docstring says the caller decides *why* there are no rows | AC1, AC3, AC4 — and ADR-0005's contract, which this extends rather than contradicts |
| `main` counts skipped files beside the stderr line it already printed | AC1, AC3 — and AC6 by leaving the line itself alone |
| `main`'s `if not rows:` branch asks *why*, with `elif top is None` below it | AC1–AC5 |

I checked the third hunk against the specific risk that it swallows WI-0002's `--top` behaviour:
the `elif top is None` and `else` arms are the previous code unchanged, and the slice, the total
and the `(all M files)` label are byte-identical to `main`.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | 7 of 7 `- [x]`; `validate-workspace` exit 0 |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | seven rows, each with the command `verify` ran and its output, on fixtures built under `/tmp/vbug2-9bJv/` rather than the item's own `/tmp/bug2*` folders. AC2 was decided with `cmp` on two stdout captures, which is the criterion's own test |
| D3 | the gates passed on the **final** state of the code | **pass** | last code commit `277c89c`; `verify` ran the suite at `e1e2985`, whose code tree is identical; I re-ran it on the merge result: 55 tests, exit 0 |
| D4 | no open blocking question | **pass** | `questions/` is empty — none was filed on this item |
| D5 | a journal entry per execution; history chains | **pass** | four rows chaining `— → ready → planned → in-progress → verifying → in-review` (the `verify` filing row, then `plan`, `implement` ×2, `verify`), the last matching `item.md`; four journal entries, one per execution |
| D6 | every design decision is an ADR, cited | **pass** | ADR-0007, cited by number in `plan.md`'s decision table, in the `plan` journal entry, and in the comment on the branch it governs. Four options costed, reversibility stated |
| D7 | documents the change invalidated were updated | **pass** | none needed updating, and the plan says why: the overview's line for `format_report` — "the caller may override the total and its label" — still reads true with one more optional parameter, and no boundary in that document changed. A version bump with no substantive change devalues every other one |
| D8 | every commit references the item ID | **pass** | `check-commit-refs` → exit 0, "all 3 commit(s) … name BUG-0002" |
| D9 | merged into the trunk | **pass** | `main` was at `558eaaa` = the merge base, so a fast-forward. Proved first on a throwaway branch: `git diff --stat wi/BUG-0002 HEAD` empty, 55 tests green. Then `git merge --ff-only`, suite re-run on `main` |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness` → exit 0: "verified at `e1e29850`; … only the record changed (5 file(s) under `tracker/` or `docs/`)" |
| D11 | `artifacts/review.md` exists and says what was examined | **pass** | this file |

## Findings

1. **The fix is one branch and it is in the right place.** The plausible wrong version — making
   the new sentence the general case for any empty result — is caught by five tests, three of them
   WI-0001's and WI-0002's own. `verify` mutated the code into that shape twice (the branch and the
   renderer's default) and both were rejected by the existing suite, which is the strongest
   evidence available that AC4 and AC5 are genuinely protected.
2. **`no files could be read` is a new interface, and it is recorded as one.** The tool's stdout
   vocabulary is now three shapes rather than two. Nothing in this project consumes that output
   programmatically, and ADR-0007's consequences say so plainly rather than assuming it away.
3. **The `unreadable` counter counts the right thing.** It increments only where a file was
   established to be a file and then failed to read — not where an entry could not be resolved
   (ADR-0006). That distinction is why a folder of symlink loops still prints `no files`, which
   `verify` exercised directly. Getting it wrong would have made the two bugs' fixes interfere.
4. **A coverage gap, accepted:** nothing in the suite asserts that a folder of *only* unresolvable
   entries prints `no files`. `verify` ran it by hand and it is correct; no criterion of this item
   covers it. Carried into `## Notes` rather than filed, because the behaviour is right and only
   the test is missing.
5. **Nothing else.** No duplicated rule, no swallowed error, no misleading name.

## Accepted gaps

Each is declared in `verify-report.md` `## Not verified, and why` or `impl-report.md` `## What I
did not do`, and each is written into `item.md`'s `## Notes`:

1. **No test for a folder of only unresolvable entries** (finding 4).
2. **No test for a folder mixing unreadable files with unresolvable entries** — `verify` ran it by
   hand and it matches plan assumption 2; the suite does not pin it.
3. **The wording `no files could be read`** is ADR-0007's choice and no criterion fixes it.
4. **No lint** (ADR-0003).
5. **Non-POSIX platforms**, and folders of more than a handful of unreadable files, are untested.

## Verdict

**Accepted, merged into `main`, and closed with outcome `delivered`.**

Seven criteria, each independently demonstrated; a three-hunk diff whose every line traces to a
plan step; one ADR for the decision the criteria left open, with four options costed. The fix does
not widen into BUG-0003's printing path, and it leaves `--top`'s label exactly as it found it —
the item's own notes asked whoever fixed this to check that and say so, and both `implement` and
`verify` did.

`EP-001` stays `open`: BUG-0003 is still `ready`, so DE1 is not met.
