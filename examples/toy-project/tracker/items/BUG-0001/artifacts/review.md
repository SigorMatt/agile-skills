# Review — BUG-0001

## What I examined

- `item.md` — the six criteria as they now stand (AC6 as `Q-002` scoped it), `## Summary`, the
  three reproduction blocks, `## Expected behaviour` with its quotations from WI-0001 AC7,
  `docs/product/vision.md` and ADR-0002, and both `## Notes` paragraphs recording amendments
- `history.md` — six rows, checked against `pipeline.yaml`; the second row is the one repaired by
  `--restamp-last`, and the clamp's fingerprints (`01:30:01`, `:02`, `:03`, `:04`) are visible on
  every row after it
- `journal.md` — all **eight** entries in full, including the two correction entries and the
  restamp record
- `artifacts/plan.md`, `impl-report.md`, `verify-report.md`; `questions/Q-001.md` and `Q-002.md`,
  both `answered`, and the three files each named in `## Consequences`
- `docs/architecture/adr/ADR-0006` (written for this item), `ADR-0002` (the boundary it must not
  disturb), `docs/architecture/overview.md` v3, `docs/product/vision.md` v1
- **the diff**, hunk by hunk: `git diff main..wi/BUG-0001 -- linecount.py tests/` — `linecount.py`
  +18/−3, `tests/test_linecount.py` +64/−0

The code diff is two hunks and both trace to plan step 1 and step 2:

| hunk | serves |
|------|--------|
| `list_files`: `try` / `except OSError` around `entry.is_file(...)`, plus the docstring naming ADR-0006 and stating that `os.scandir`'s own error still propagates | AC1, AC2, AC3 — and AC5 by where it is *not* placed |
| `tests/test_linecount.py`: `UnresolvableEntryTest` appended, four tests | AC1, AC2, AC3, AC5, AC6 |

Nothing else in `linecount.py` is touched: `count_lines`, `format_report`, `parse_top`,
`parse_args`, the sort key, `main`'s folder handler and its ADR-0002 per-file handler are
byte-identical to `main`. No hunk contradicts an ADR; ADR-0006 is the one that authorises this
change and the code cites it where it acts.

## Definition of Done

`spec/dor-dod.md` §3, criterion by criterion.

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | 6 of 6 `- [x]`, none left; `validate-workspace` exit 0 |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | six rows, each with the command `verify` ran and its quoted output, on fixtures built under `/tmp/vbug1-ZITq/` — deliberately not the `/tmp/bug1a…d` folders the earlier steps used |
| D3 | the gates passed on the **final** state of the code | **pass** | last code commit `06fc185`; `verify` ran the suite at `4bf2cba`, whose code tree is identical (`git diff --name-only` between them lists only `tracker/`); I re-ran it on the merge result: 50 tests, exit 0 |
| D4 | no open blocking question | **pass** | `Q-001` and `Q-002` both `answered`; neither was ever blocking. I opened all three files named across their `## Consequences` and confirmed each change is present — including AC6's scoped wording and the `## Notes` paragraph recording it |
| D5 | a journal entry per execution; history chains | **pass** | six rows chaining `— → ready → planned → in-progress → verifying → in-review`, the last matching `item.md`; eight journal entries covering `verify` (the filing), `plan`, `answer-questions` ×3, `implement`, `verify`. The two `plan` entries and the restamp entry are corrections, each saying what it corrects |
| D6 | every design decision is an ADR, cited | **pass** | ADR-0006, cited by number in `plan.md`'s decision table, in the `plan` journal entry, and in `list_files`'s docstring where the rule acts. Its four options are costed and its `## Consequences` states reversibility |
| D7 | documents the change invalidated were updated | **pass** | `docs/architecture/overview.md` v2 → v3 with a change-log row and the three-`OSError`-sites table, written by `plan` (as it must be — `implement` and `verify` may not write to `docs/`). `vision.md` needed no change: this fix makes its "a number, not a stack trace" claim true where it was false |
| D8 | every commit references the item ID | **pass** | `check-commit-refs BUG-0001 wi/BUG-0001` → exit 0, "all 4 commit(s) … name BUG-0001" |
| D9 | merged into the trunk | **pass** | `main` was at `f520c2d` = `git merge-base main wi/BUG-0001`, so a fast-forward. Proved first on a throwaway branch: `git diff --stat wi/BUG-0001 HEAD` empty, 50 tests green there. Then `git merge --ff-only`, with the suite re-run on `main` |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness BUG-0001 wi/BUG-0001` → exit 0: "verified at `4bf2cba5`; … has moved to `5743c3ed` but only the record changed (5 file(s) under `tracker/` or `docs/`)" |
| D11 | `artifacts/review.md` exists and says what was examined | **pass** | this file |

## Findings

1. **The fix is in the right place, and that is the whole review.** The plausible wrong version of
   this change is one `try` a few lines higher, wrapping `os.scandir` and swallowing the folder's
   own failure. `verify` mutated the code into exactly that shape and four tests caught it. I
   re-read the hunk against that risk and the placement is correct: the `try` is inside the loop,
   around the per-entry predicate only.
2. **`except OSError` is deliberately broad, and I accept it.** Plan assumption 2 argues that
   naming a subset of errnos would leave the next unlisted one as a fresh instance of this bug.
   The breadth is bounded by where it sits — one predicate call — so it cannot mask an error from
   anything else.
3. **Silence for an unresolvable entry is a real product decision, not an implementation detail.**
   A folder can now hold an entry the tool never mentions. ADR-0006 costs the alternative, AC1
   forces it for the loop case, and `verify` names it under `## Not verified, and why` as the one
   thing a reasonable person might want different. Accepted, and carried into `## Notes`.
4. **The record of this item is unusually long for an eleven-line fix**, and that is not padding:
   two of its eight journal entries exist because the workspace's clocks disagreed, and one
   because a criterion asked for something impossible. Each is a correction that says what it
   corrects. A reader can follow it.
5. **Nothing else.** No duplicated rule, no swallowed error, no name that says something untrue.

## Accepted gaps

Each is declared in `verify-report.md` `## Not verified, and why` or `impl-report.md` `## What I
did not do`, and each is written into `item.md`'s `## Notes` so it outlives the reports:

1. **Silence for unresolvable entries** (finding 3) — accepted, ADR-0006 records the alternative.
2. **No lint** (ADR-0003) — the eleven changed lines were read by a person and by no tool.
3. **Entries that are neither file, directory nor symlink** (a socket, a device node) — `is_file()`
   returns `False` for them without raising, so they are unaffected; untested.
4. **Non-POSIX platforms**, unchanged from WI-0001.
5. **BUG-0002's symptom is untouched** — a folder whose entries are *all* unresolvable still prints
   `no files`. Correctly left to BUG-0002, which is open; noted here so the connection is not lost.

## Verdict

**Accepted, merged into `main`, and closed with outcome `delivered`.**

Six criteria, each independently demonstrated on fixtures the verifier built himself; a two-hunk
diff with nothing unrequested; one ADR for the decision the criteria did not make; two questions
raised, answered from the record, and propagated into the criterion and the spec they concerned.
The defect this item fixes was found by an independent pass against a closed epic, and the fix
does not widen to absorb the two bugs found beside it.

`EP-001` stays `open`: BUG-0002 and BUG-0003 are still `ready`, so DE1 is not met. It will be
re-closed when they are, with its success measures re-run against the merged trunk.
