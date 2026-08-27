# Verification report — WI-0002

Verified-commit: 6b2fb40989f413f09f0214bd76c74dab8a4e062a

Everything below was run by this skill against a checkout of `wi/WI-0002` at that commit, with
the working tree clean. No figure in this report is taken from `impl-report.md`; where the two
agree, they agree because both were run, and the two places where they differ are noted.

`git diff --name-only b873060..HEAD` returns only `tracker/` files, so the code at the verified
commit is identical to the code at `b873060`, the commit the implementation reported its gates
against. That is what makes the two sets of runs comparable rather than merely similar.

## Verdict

**Pass.** All six acceptance criteria are confirmed by commands this skill ran. No criterion is
`ambiguous`. No defect was found, in this item's behaviour or in behaviour delivered elsewhere,
so no bug item was filed and there is nothing to send back. WI-0002 goes to `in-review`.

## Criteria

Every store below is a scratch path under one `mktemp -d`, built from a path that did not exist,
with `EXPENSES_STORE` pointing at it — which is what the criteria themselves prescribe.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| **AC1** — three people, one 30 expense, exactly two lines | **pass** | `person add Ana`, `person add Ben`, `person add Cara`, `expense add --amount 30 --paid-by Ana --shared-by Ana,Ben,Cara`, then `python3 -m expenses settle > ac1.out`; then `wc -l < ac1.out`, `sort ac1.out`, `cat -A ac1.out` | exit `0`; `cat -A` → `Ben pays Ana 10.00$` / `Cara pays Ana 10.00$`; `wc -l` → `2`; `sort` → `Ben pays Ana 10.00` / `Cara pays Ana 10.00`; stderr empty | Exactly two lines, each newline-terminated, and the sorted pair is the pair the criterion names. `cat -A` is what establishes "exactly two lines" rather than "two lines and something else" |
| **AC2** — three ways to have nothing to settle | **pass** | three stores built separately — (a) a path never written to, (b) `person add Ana` + `person add Ben`, (c) those two plus `expense add --amount 10 --paid-by Ana --shared-by Ana` — then `python3 -m expenses settle` in each | (a) exit `0`, `cat -A` → `no payments needed$`; (b) exit `0`, `no payments needed$`; (c) exit `0`, `no payments needed$`; stderr empty in all three | All three, not one generalised to three. In case (a) the store file did not exist at all (`store exists: no`); in (c) every position is zero because the only sharer is the payer |
| **AC3** — five-person dataset, exact three lines and five stated properties | **pass** | `person add` ×5 in the order `Ana Ben Cara Dan Eve`, then the three `expense add` commands in the order the criterion gives, then `python3 -m expenses settle`; the properties then checked by a script *this skill wrote*, which recomputes every position from the raw stored JSON rather than calling `expenses/settle.py` | exit `0`; stdout as emitted → `Cara pays Ana 9.33` / `Dan pays Ana 6.00` / `Ben pays Ana 1.33`; sorted → `Ben pays Ana 1.33` / `Cara pays Ana 9.33` / `Dan pays Ana 6.00`; `wc -l` → `3`. Independent recomputation → positions `{Ana: 1666, Ben: -133, Cara: -933, Dan: -600, Eve: 0}`, summing to `0`; non-zero people `['Ana','Ben','Cara','Dan']`, count `4`; `lines: 3 | one fewer than non-zero: True`; `every amount > 0: True [933, 600, 133]`; `no name in both roles: True payers {'Dan','Cara','Ben'} receivers {'Ana'}`; `Eve position: 0 | Eve appears in output: False`; `each debtor's total paid == what they owe overall: True`; `sum of the three amounts: 1666 | Ana's credit: 1666 | equal: True` | Each of the five clauses is checked separately and against arithmetic derived from the stored dataset, not from the code under test. The stored shares were also read out — `{'Ana': 334, 'Ben': 333, 'Cara': 333}` on the 10.00 expense — which is what makes the 1666/-133/-933/-600 figures reproducible rather than asserted |
| **AC4** — byte-identical across two processes | **pass** | on AC3's store, `python3 -m expenses settle > ac4.run1`, then `python3 -m expenses settle > ac4.run2`, then `cmp ac4.run1 ac4.run2` | `cmp` printed nothing, `cmp EXIT=0` | Two separate `python3` processes, as the criterion requires, compared with `cmp` as the criterion names |
| **AC5** — the command changes nothing | **pass** | on AC3's store: `md5sum` of the data file, `python3 -m expenses settle`, `md5sum` again. Then `EXPENSES_STORE=$T/nested/does/not/exist.json python3 -m expenses settle`, with `test -e` on the path before and after | before `ad65189c9362a13c953dee6d87db2a49`, settle exit `0`, after `ad65189c9362a13c953dee6d87db2a49` — identical. Missing path: `path absent before`, exit `0`, stdout `no payments needed$`, `path still absent after`, and `no parent dir created` | Both halves of the criterion. The parent-directory check is this skill's addition: a command that created `$T/nested/` without creating the file would still satisfy the criterion as written, and it does not do that either |
| **AC6** — the README documents it | **pass** | `grep -n settle README.md`, then reading `sed -n '85,120p' README.md` | line 94 `$ python3 -m expenses settle`; the fenced example immediately below it shows `Ben pays Ana 10.00` / `Cara pays Ana 10.00`; the following paragraph states "it prints `no payments needed`" with its own worked example | All three clauses — the command named, an example of its output, and what it prints when there is nothing to settle — are present in a `### settle` section under "The commands" |

All six boxes are ticked in `item.md` on this evidence.

## Gates

| gate | result | evidence |
|---|---|---|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` on the verified commit → `Ran 86 tests in 0.781s`, `OK`, exit `0`. Re-run after every mutation below was reverted → `Ran 86 tests in 0.797s`, `OK` |
| `lint-clean` | **skipped** | `commands.lint` is `null` in `tracker/project.yaml`; ADR-0004 records why (the project installs nothing and the standard library ships no linter). The gate checked nothing, so it is not recorded as a pass. What that leaves unchecked is in `## Not verified, and why` |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → `checked 7 item(s), 7 document(s)`, `0 errors, 0 warnings`, exit `0` |
| `every-criterion-independently-checked` | **pass** | The `## Criteria` table: every row is a command this skill ran with the output it actually produced. AC3's properties were checked against positions recomputed from the raw JSON by a script written here, specifically so that the check does not inherit a bug from `expenses/settle.py` |
| `negative-cases-exercised` | **pass** | AC2's three empty/zero conditions were each *created* and run, not reasoned about; AC5's missing-file condition was created by pointing `EXPENSES_STORE` at `$T/nested/does/not/exist.json` and the absence re-checked afterwards. See `## Negative and boundary cases exercised` |
| `tests-would-fail-without-the-change` (advisory) | **pass, with one qualification** | Six mutations, each reverted; see `## Test sensitivity check`. The qualification concerns AC1 and is recorded there |

## Negative and boundary cases exercised

| condition | how it was produced | what happened |
|---|---|---|
| No store file at all | `EXPENSES_STORE` set to a scratch path never written to; `test -e` confirmed absent first | exit `0`, stdout exactly `no payments needed`, stderr empty |
| People recorded, no expenses | `person add Ana`, `person add Ben`, nothing else | exit `0`, stdout exactly `no payments needed` |
| Every position zero with an expense present | `expense add --amount 10 --paid-by Ana --shared-by Ana` — payer is the only sharer | exit `0`, stdout exactly `no payments needed`. The non-trivial one: there is data, and the answer is still nothing |
| A person whose position is zero among people whose positions are not | `Eve` in AC3's dataset — added, never paid, never shared | absent from all three output lines, confirmed by string search over the stdout |
| Two debts exactly equal | AC1's `Ben` and `Cara`, both `-1000` | the tie is broken by recorded order: emitted order was `Ben` then `Cara`, which is the order they were added. This is ADR-0005's rule observed in output rather than read in the source |
| A path whose parent directories do not exist | `EXPENSES_STORE=$T/nested/does/not/exist.json` | exit `0`, `no payments needed`, the file still absent **and** `$T/nested` never created |

## Test sensitivity check

Each mutation was applied to the working tree, the suite run, and the change reverted with
`git checkout`. `git status --porcelain` was empty afterwards and the full suite returned to
`Ran 86 tests ... OK`.

| # | behaviour disabled | how | what failed |
|---|---|---|---|
| M1 | ADR-0005's tie-break (AC1) | in `settle.py`, `(entry[1], -recorded[entry[0]])` → `(entry[1], recorded[entry[0]])`, reversing which of two equal debts is matched first | `FAILED (failures=2)` — `test_settle.SettlementTest.test_ac1_tie_between_two_equal_debts_goes_to_whoever_was_recorded_first` and `::test_ac1_reversing_the_recorded_order_reverses_the_payments` |
| M2 | the nothing-to-settle message (AC2) | in `cli.py`, `no payments needed` → `nothing to do` | `FAILED (failures=4)` — all three of `WI0002AC2NothingToSettle`, plus `WI0002AC5SettleChangesNothing::test_settle_creates_no_data_file_where_none_exists`, which also asserts the string |
| M3 | the position arithmetic (AC3) | in `settle.py`, `net[name] -= share` → `net[name] -= 0`, so shares stop being subtracted | `FAILED (failures=11, errors=6)` — including every one of `WI0002AC3TheListSettlesTheGroupExactly`'s six tests and `test_settle.PositionsTest::test_ac3_dataset_gives_the_positions_the_criterion_names` |
| M4 | determinism across processes (AC4) | in `cli.py`'s handler, `if os.getpid() % 2: payments = list(reversed(payments))` — same content, process-dependent order | `WI0002AC4TheSameDataPrintsTheSameBytes` → `FAILED (failures=1)` on three consecutive runs. The mutation leaves sorted output unchanged, so it isolates determinism from content |
| M5 | the read-only property, weakly (AC5) | in `cli.py`'s handler, `open(store.store_path(), "a").write("")` | `FAILED (failures=1)` — only `test_settle_creates_no_data_file_where_none_exists`. The md5 test did **not** fail, correctly: appending nothing changes no bytes |
| M5b | the read-only property, actually (AC5) | the same line writing `"\n"` instead | `FAILED (failures=2)` — both `test_the_data_file_is_unchanged_across_a_settle_run` and `test_settle_creates_no_data_file_where_none_exists`. This is what establishes the md5 test is sensitive; M5 alone would not have |
| M6 | the README section (AC6) | deleted `### settle` through to `## When something is wrong` from `README.md` | `FAILED (failures=3)` — all three of `WI0002AC6TheReadmeDocumentsTheCommand` |

**The qualification on AC1.** The mutation M1 does *not* fail `WI0002AC1SettleListsThePayments`,
the end-to-end test — because AC1 asks that stdout's two lines *sorted* be the two named lines,
and reversing a tie between two equal debts leaves the sorted pair identical. So the criterion as
written cannot distinguish the two orders, and the rule ADR-0005 fixes is pinned only by the two
function-level tests M1 did fail. This is not a defect: AC1 says what it says, the behaviour is
correct, and the tie-break is separately tested. It is recorded because a later change to
ADR-0005's tie-break would go undetected by AC1's own end-to-end test, and whoever makes that
change should know which test is actually load-bearing.

## Defects found

None — neither in this item's behaviour nor in behaviour delivered by another item. No bug item
was filed by this execution.

Two things were looked at specifically because they would have been defects if they had gone the
other way, and are recorded so the absence is auditable:

- **`positions()` silently ignores a name that is in an expense but not in `data["people"]`**
  (`if payer in net` / `if name in net` in `expenses/settle.py`). No delivered command can produce
  that dataset — `add_expense` refuses an unknown name and nothing deletes a person — and the
  implementation report's `## What I did not do` declares it, as does `plan.md`'s `## Risks`, both
  naming WI-0004 as where it must be solved. Declared, reachable only by hand-editing, covered by
  no criterion of this item: not a defect here.
- **The diff against the plan holds nothing unaccounted for.** `git diff main..wi/WI-0002 --stat`
  → `expenses/settle.py` (new, steps 1–2), `expenses/cli.py` (step 3), `tests/test_settle.py` and
  `tests/test_cli.py` (steps 4–5), `README.md` (step 6), `docs/architecture/overview.md` (step 7),
  and `tracker/` files. Every deletion is in the two paragraphs that said who-owes-whom was not
  built yet. No hunk implements behaviour no step asked for.

## Not verified, and why

- **Lint.** `commands.lint` is `null`, so nothing checked style, dead code, unused imports or
  shadowing anywhere in this change. ADR-0004 is the record of that choice; what it leaves
  unchecked is exactly what a linter would have caught, and this item's evidence rests entirely on
  behaviour instead.
- **The unsettled-dataset case.** `settlement()`'s docstring claims it terminates on a hand-edited
  dataset whose positions do not sum to zero, settling it as far as it can. No delivered command
  can produce that state and no criterion of this item covers it, so this skill did not construct
  one by hand. The claim is untested here, by both the implementation's declaration and this
  skill's judgement — it is not evidence, and `review-close` should not read it as such.
- **Scale.** Nothing was run against a large group or a long history. The item's
  `## Deliberately unconstrained` section says no threshold was ever set, so there is nothing to
  check against; the largest dataset exercised here is five people and three expenses, which is
  AC3's.
- **The two ADR-0005 shapes with more than one creditor.** AC1's and AC3's datasets each have a
  single creditor, so the creditor-side tie-break is not exercised by any acceptance criterion.
  `tests/test_settle.py::SettlementTest::test_two_creditors_are_paid_largest_credit_first` covers
  it and passes, but that is a test the implementation chose to write, not a criterion this skill
  can hold the item to. Recorded so nobody later mistakes AC-level coverage for rule-level
  coverage.
- **`git diff` review is coverage of the change, not of the untouched code.** Nothing was verified
  about `store.py` or `money.py` beyond their being unmodified on this branch. BUG-0001 and
  BUG-0002 remain open against WI-0001's behaviour and were not re-examined here.
