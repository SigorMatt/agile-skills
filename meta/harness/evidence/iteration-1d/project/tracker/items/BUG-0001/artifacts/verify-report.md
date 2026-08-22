# Verification report — BUG-0001

Verified-commit: 758c0af9b29cdf769943c42f3a98a3f179f82523

## Verdict

**Pass.** Both acceptance criteria are met, on evidence gathered by running the commands here
rather than by reading `impl-report.md`. What settled each criterion was derived from the
criterion's own wording before the implementation report was opened. One documentation finding is
recorded below for `review-close`'s D12 audit; it blocks nothing and is not a defect in behaviour.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 — with the ledger location unwritable, each of `add-person`, `add-expense` and `repay` prints nothing on stdout, prints the failure on stderr, and exits non-zero; reproduced by the six steps | **pass** | BUG-0001's six steps, run here in a fresh `mktemp -d`, with stdout and stderr captured to separate files: `add-person Ana`, `add-person Ben`, `chmod 500 $V`, then `add-person Cara`, `add-expense --payer Ana --amount 10 --description x`, `repay --from Ana --to Ben --amount 5`, then `chmod 700 $V` and `people` | Steps 2: `exit=0`, `stdout=<<Added Ana.>>` and `<<Added Ben.>>`. Step 3: mode confirmed `500` via `stat -c %a`. Steps 4 and 5, all three commands: `exit=1`, `stdout=<<>>`, `stderr=<<error: cannot write the ledger at /tmp/tmp.tW1czC01a4/l.json: [Errno 13] Permission denied: '…l.json.<suffix>.tmp'>>`. Step 6: `exit=0`, `stdout=<<Ana\nBen>>` — no `Cara` | "Prints nothing" was checked byte-exactly, not by eye: a second run redirected stdout to a file and measured it, giving `stdout_bytes=0` for all three commands (`stderr_bytes=134` each, exit 1). A shell `$(...)` capture strips trailing newlines and would have shown a lone `\n` as empty; this does not |
| AC2 — a regression test covers all three commands against an unwritable location, asserting empty stdout, and fails if the success line is moved back before the save | **pass** | Three separate checks. **(a)** `python3 -m unittest tests.test_persistence.TestAFailedWriteSaysNothingOnStdout -v`. **(b)** read the test body: `RECORDING_COMMANDS` lists `add-person`, `add-expense` and `repay`, and the loop asserts `assertEqual(result.stdout, "")`, non-empty stderr and a non-zero exit per command under `subTest`. **(c)** the sensitivity check below — `print(line)` moved back above `store.save` in `main`, then the test re-run | **(a)** `Ran 1 test … ok`, exit 0 — and it **ran**, it was not skipped: `id -u` is `1000`, so the `skipIf(os.geteuid() == 0)` guard is inactive here and the full-suite run reports a bare `OK` with no skip count. **(c)** `FAILED (failures=3)`, one per command, with `AssertionError: 'Added Cara.\n' != ''`, `'Recorded 10.00 paid by Ana for x.\n' != ''` and `'Recorded Ana repaying 5.00 to Ben.\n' != ''` | The failing strings are exactly the three lines `item.md` quotes as the pre-fix actual behaviour, so the test fails against the defect it names and not against some other breakage |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` at `758c0af` → `Ran 116 tests in 2.993s / OK`, exit 0. Run here, on the branch head, before anything was touched |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses tests` → exit 0 |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → `checked 5 item(s), 13 document(s) / 0 errors, 0 warnings`, exit 0 |
| `every-criterion-independently-checked` | **pass** | Both rows of the criteria table cite commands run in this execution. AC1 rests on the six reproduction steps performed here and on a byte-exact re-run, not on `impl-report.md`'s account of them; AC2 rests on reading the test body and on sabotaging `main` and watching the test fail |
| `negative-cases-exercised` | **pass** | See the section below. AC1 is entirely a negative criterion and every part of it was triggered; three further error paths were exercised to check the contract change did not disturb them |
| `tests-would-fail-without-the-change` (advisory) | **pass** | The sensitivity check below, including the finding that the new test is the **only** guard among 116 |

## Negative and boundary cases exercised

1. **The directory holding the ledger is unwritable, for all three recording commands.** AC1's own
   condition, `chmod 500`. All three: `exit=1`, `stdout_bytes=0`, non-empty stderr. Then
   `chmod 700` and `people` → `Ana`, `Ben`; nothing was recorded, so "prints nothing" means
   "nothing happened" rather than "the output went elsewhere".
2. **The ledger file itself is read-only, the directory writable** (`chmod 400 l.json`) — a
   boundary AC1 does not name and worth knowing about. `add-person Cara` **succeeded**: `exit=0`,
   `stdout=Added Cara.`, and a later `people` listed `Ana`, `Ben`, `Cara`. This is correct, not a
   defect: `store.save` writes a temporary file in the directory and renames over the target, and
   POSIX `rename` needs write permission on the *directory*, not on the file being replaced. The
   location genuinely can be written, so nothing about AC1 or about WI-0001 AC9 is contradicted —
   the run reported success and a success is what happened. Recorded because a reader could
   otherwise expect mode 400 to protect a ledger, and it does not.
3. **A validation refusal, on the fixed code** — `add-person Ana` when Ana is already recorded.
   `exit=2`, `stdout_bytes=0`, stderr `error: 'Ana' is already recorded as 'Ana'; names match
   ignoring surrounding whitespace and case`. The handler now returns a line instead of printing
   one, so this path was worth re-triggering: it is unchanged.
4. **The ledger cannot be read** — `chmod 000` on the file, then `add-person Dee`. `exit=1`,
   `stdout_bytes=0`, stderr `error: cannot read the ledger at …: [Errno 13] Permission denied`.
   The load-failure path runs before any handler and was already correct; it still is.
5. **The success path and the four listings**, to check the plan's claim that the wording is
   byte-identical rather than take it on trust. `add-person Cara` → `Added Cara.`,
   `add-expense …` → `Recorded 10.00 paid by Ana for x.`, `repay …` → `Recorded Ana repaying 5.00
   to Ben.` — each compared with `[ "$a" = "…" ]` against the strings `item.md` quotes as the
   pre-fix output, and each matched exactly. `people`, `expenses`, `repayments` and `debts` all
   exit 0 and still print their own rows (`Ben owes Ana 8.33`, and so on), so returning `None`
   after printing did not silence them.

## Test sensitivity check

`print(line)` in `main` was moved back above the `try: store.save(...)` block — the literal thing
AC2 says the test must catch, and the shape the code had before this item.

- `python3 -m unittest tests.test_persistence.TestAFailedWriteSaysNothingOnStdout` →
  `FAILED (failures=3)`, one per command, with the three pre-fix success lines quoted verbatim in
  the assertion messages.
- `python3 -m unittest discover -s tests -t . -q` against the same sabotage → `Ran 116 tests`,
  `FAILED (failures=3)`. **Only** the new test failed; the other 115 passed. That is worth
  recording rather than treating as reassurance: nothing else in the suite constrains this
  behaviour, so the criterion rests entirely on the one test — which is exactly why AC2 asks for
  the test to be demonstrably sensitive, and it is.
- `git checkout -- expenses/cli.py` restored the file; `git diff` reports no change to it, and the
  full suite is green again (`Ran 116 tests … OK`).

## Defects found

None in behaviour. One documentation finding, routed to `review-close` rather than filed as a bug
or sent back, because no acceptance criterion of this item covers it and it is not behaviour
delivered by another item:

- **`docs/architecture/overview.md`'s opening paragraph is now stale.** It reads "The shape of the
  system as it stands after WI-0001 and WI-0002 were implemented … and this version is step 5 of
  WI-0002's plan re-checking that description against what was actually built". "This version" is
  now v7, written by `implement` for BUG-0001 under step 6 of *this* item's plan, so the sentence
  attributes the current version to the wrong item and the wrong plan step. The bullet v7 actually
  added — the `cli.py` handler contract — is accurate; it is the lede that was not updated when
  the version was bumped. This is precisely what D12 exists to catch, and the same audit produced
  v3 and v6 of this document [src: docs/architecture/overview.md]. Cost to fix: one sentence.

## Not verified, and why

- **The behaviour under `root`.** The regression test guards itself with
  `skipIf(os.geteuid() == 0)`, because root ignores directory permissions and the test would
  observe a successful save. This run was not root (`id -u` → `1000`), so the test executed and
  AC1's manual reproduction was real; but what the tool does when a genuinely unwritable location
  is encountered *as root* is not something either criterion asks for and is not checked. The plan
  names this risk and accepts it.
- **Filesystems where `rename` behaves differently** — network mounts, containers with unusual
  overlay semantics. Everything here was exercised on the local filesystem `mktemp -d` returns.
  Boundary case 2's result is a property of POSIX rename semantics and could differ elsewhere.
- **Whether the success line is correct for a *fourth* mutating command.** `ADR-0011`'s main
  argument is that WI-0003's importer inherits the ordering. WI-0003 is `blocked` and no import
  command exists, so that claim is checked only against the three commands that do exist.
- **`--help`, argparse usage errors, and the `EXPENSES_LEDGER` / XDG resolution paths** were not
  re-exercised. They are WI-0001's criteria, they touch no handler return value, and the diff does
  not reach them.
