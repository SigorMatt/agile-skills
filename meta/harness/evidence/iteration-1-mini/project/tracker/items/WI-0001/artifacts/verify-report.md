# Verification report — WI-0001

Verified-commit: a273c4ee483b6d8bedab0aedd3e671ffc6f17d9c
Verified-at: 2026-08-21T03:32:55Z
Branch: wi/WI-0001 (code at `fcf3cf4`; `a273c4e` on top touches `tracker/` only)

> **Third verification.** The second passed all eight criteria on `f994258`; `review-close` then
> rejected the item on four findings, one of them a direct AC8 violation, and unticked AC8. This
> pass re-derives all eight criteria against the new code — it carries no verdict forward — and
> takes up `review.md` `## For the next verification` explicitly, because that handover names the
> input class the previous sweep never reached.

## Verdict

**Pass — all eight acceptance criteria met on `a273c4e`.** Recommend `in-review`. **AC8 is ticked
again**, on evidence that now includes the input that disproved it.

The review's three actionable findings are confirmed fixed by running its own reproductions, not
by reading `impl-report.md`. The advisory sensitivity gate passes: ten mutations, ten red suites.

## Criteria

Every command was run by this skill against the branch head, in a throwaway store under the
git-ignored `.harness/`.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `python3 -m expenses --help`; `add-person Zoe`, `alice`, `Carol`; `people \| cat -A` | help lists `add-person` and `people` under `{add-person,people}`; listing → `Zoe$` / `alice$` / `Carol$`, exit 0 | `cat -A` shows name-plus-newline and nothing else. Added out of alphabetical order, so the output is insertion order and could not come from sorting |
| AC2 | **pass** | the three adds and the listing are four separate processes; `people` re-run again | `Zoe` / `alice` / `Carol`, exit 0, identical | Order preserved across the process boundary and not alphabetical, so "the same order" is genuinely asserted |
| AC3 | **pass** | `add-person ALICE`; `add-person "  Alice  "`; then `people` | `alice is already in the group; nothing was added`, exit 2, twice | Case-insensitive after stripping; the message names the **stored** spelling; the roster is unchanged. The kept spelling is the first entered (`alice`, lowercase) |
| AC4 | **pass** | `people` against an empty store, and against no store at all | `Nobody in the group yet.`, exit 0, both | Confirmed on stdout |
| AC5 | **pass** | `EXPENSES_STORE=.harness/w/a/b/s.json` with no ancestors: `people`, then `add-person Bob`, then `people` | read → exit 0 and `ls -d .harness/w` → `No such file or directory`; write → `Added Bob.`, exit 0, file and both parents created; fresh read → `Bob` | Read creates nothing; write creates the file and missing parents; no setup step |
| AC6 | **pass** | four damage modes × **both** commands, `sha256sum` before and after each: non-JSON; `[1,2,3]`; **`people` holding `123`**; undecodable bytes | all eight → exit 2, no traceback, each naming the path and the fault (`it is not valid JSON …` / `it is not an expenses store …` / **`its list of people contains int, which is not a name …`** / `it is not valid UTF-8 text …`); every hash identical | The third mode is `review.md` F1. It previously exited **0** on the read path printing `123` as a member, and **1** with a traceback on the write path |
| AC7 | **pass** | `add-person ""`, `add-person "   "`, `add-person` with no argument | `a name is required` (exit 2) ×2; argparse's `the following arguments are required: name` (exit 2) | Roster unchanged |
| AC8 | **pass** | a 28-case sweep capturing stdout, stderr and exit separately — 23 failing invocations and 5 succeeding — plus a driver forcing an unanticipated exception | **every** failure: non-zero exit, stdout empty, stderr non-empty, `Traceback` in neither stream. **every** success: exit 0, stdout non-empty, stderr empty. Backstop: `ZeroDivisionError` raised from `store.load` → exit code 2, stdout `''`, stderr `an internal error in expenses (ZeroDivisionError: nobody planned this). This is a bug in the tool, not something you did wrong.` | The sweep now includes the class that broke it: six junk element types (`123`, an object, a list, `null`, `1.5`, `true`) × both commands, all through a store that **passes** `load()`'s top-level check. See `## The finding that unticked AC8` |

All eight boxes are ticked in `item.md`, each on the evidence in its row. AC8's tick was cleared
by `review-close` and is restored here; nothing was ticked on `impl-report.md`'s authority.

## The finding that unticked AC8, re-checked

`review.md` F1's reproduction, run again against `a273c4e`:

```
$ EXPENSES_STORE=<store with {"version":1,"people":[123],"expenses":[]}>
$ python3 -m expenses people
cannot read <path>: its list of people contains int, which is not a name.
Nothing has been changed; fix or move the file and try again.          # exit 2
$ python3 -m expenses add-person Carol
<the same message>                                                      # exit 2
```

Previously: exit 0 printing `123`, and exit 1 with an `AttributeError` traceback. Both halves of
`ADR-0002` decision 6 are now satisfied on this input, from both commands, with the bytes left
alone. Repeated for `{"name":"Alice"}`, `["Alice"]`, `null`, `1.5` and `true` — same result.

F2, re-checked: with `Al\x07ice` and `Bob` stored, `add-person Carol` exits **0** and `people`
lists all three. The error that blamed `Carol` for a control character it does not contain is
gone.

F3, re-checked in the code rather than the prose: `cli.main`'s backstop turns an arbitrary
exception into one line on stderr with a non-zero exit. `docs/architecture/overview.md` is at v2
with a change-log row, and its `cli` bullet now describes both handlers.

## Gates

| gate | enforcement | result | evidence |
|------|-------------|--------|----------|
| `tests-pass` | hard | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 23 tests`, `OK`, run on the branch head and again after the mutation sweep |
| `lint-clean` | hard | **skipped** | `commands.lint` is null by `ADR-0001` §4. Recorded as skipped, not passed |
| `workspace-valid` | hard | **pass** | `validate-workspace .` → `0 errors, 0 warnings` |
| `every-criterion-independently-checked` | hard | **pass** | Each row above names a command this skill ran and quotes real output; no row cites `impl-report.md` |
| `negative-cases-exercised` | hard | **pass** | 23 failing invocations across argument parsing, name rules, four store-damage modes and six junk element types, plus a forced internal exception |
| `tests-would-fail-without-the-change` | advisory | **pass** | Ten mutations, ten red suites, table below |

## Test sensitivity check

Each mutation applied to a backed-up copy, the named test run, the source restored. Afterwards
`git status --short` on `expenses/ tests/` was empty and the full suite green, so the tree this
report describes is the committed one.

| criterion | behaviour disabled | result |
|-----------|--------------------|--------|
| AC1 | `listing()` returns `sorted(...)` | exit 1 |
| AC2 | `store.save()` made a no-op | exit 1 |
| AC3 | `match_key` stops lowercasing | exit 1 |
| AC4 | the empty-group message removed | exit 1 |
| AC5 | `mkdir(parents=True)` removed | exit 1 |
| AC6 | a JSON parse error returns `empty()` | exit 1 |
| AC7 | the empty-name rejection removed | exit 1 |
| AC6/AC8 (F1) | the element-type check removed from `load()` | exit 1 |
| AC3 (F2) | `match_key` validates again | exit 1 |
| AC8 (F3) | the `except Exception` backstop removed | exit 1 |

The last three matter most: they are the three fixes this pass exists to check, and each one's
test provably goes red without it.

## Diff read against the plan

`fcf3cf4` is the only code change since the last verification: `store.load()` gains an
element-type loop; `match_key` becomes `name.strip().lower()`; `cli.main` gains an
`except Exception` backstop; `errors.py`'s docstring is corrected; four tests added;
`overview.md` → v2. Every hunk traces to F1, F2 or F3. No unrequested scope; F4 is untouched, as
the review recorded it should be.

One deviation is declared in `impl-report.md` and is real: `plan.md` step 5 specifies one
`except ExpensesError`, and there are now two handlers. AC8 covers the behaviour, the deviation is
declared rather than buried, and the plan's own AC8 mapping is what turned out to be insufficient.
Recorded, not raised as a defect.

## Defects found

**None.** No criterion of this item failed, so there is no send-back; no behaviour delivered by
another item failed, so no bug item was filed.

## Not verified, and why

- **`lint-clean` was skipped, not passed** (`ADR-0001` §4). Nothing mechanical checks dead code,
  unused imports or shadowed names. Already in `item.md` `## Accepted gaps`; this is the third
  consecutive pass where the two hand-found defects of that class (`match_key` dead, then
  `main`'s unused `out`/`err`) were found by a person reading a diff.
- **`store.save()`'s atomicity is still verified by inspection, not by test.** No process was
  killed mid-write. Unchanged, and in `## Accepted gaps`.
- **`expenses` list elements are still unvalidated.** F1's fix covers `people` only, which
  `impl-report.md` declares and hands to WI-0002. Nothing in this item reads that list, so it is
  not verifiable here — but it is the same latent crash, and it is named so WI-0002 inherits it as
  a known task rather than a surprise. The container type *is* checked: a store with
  `"expenses": 5` is rejected from both commands, exit 2, which this pass confirmed.
- **Concurrent writers** — unchanged, last writer wins, no criterion mentions it.
- **Disk-full and read-only-directory failures on the write path.** The read side's `OSError`
  wrapper was proven earlier by a `chmod 000` store; the write side's was not triggered, since
  filling a disk is not something this skill will do to its host.
- **`plan.md` lines 24–29 still carry the claim `review.md` F3 corrected elsewhere.**
  `impl-report.md` declares this deliberately and leaves it to `review-close` or `plan`. It is a
  record-accuracy question, not a behaviour one, and this skill has no standing to edit either
  artifact — flagged so it is not mistaken for an oversight.
- **A stored name today's rules would reject is listed rather than repaired or refused.** Not a
  gap in a criterion — no criterion covers it, and `impl-report.md` gives the reasoning — but it
  is behaviour a reader might expect to see checked, so it is named: `people` prints it, and
  `add-person` now works around it.
