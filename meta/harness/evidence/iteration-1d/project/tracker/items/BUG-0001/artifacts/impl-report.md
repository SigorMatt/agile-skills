# Implementation report — BUG-0001

## What was built

`ADR-0011`'s handler contract, executed on `expenses/cli.py`, plus the regression test that
holds it and one paragraph of documentation.

A command handler now returns `str | None` rather than `bool`. The three recording commands —
`cmd_add_person`, `cmd_add_expense`, `cmd_repay` — build the same success line they built
before and `return` it instead of printing it; none of the three contains a `print` call any
more. The four listings — `cmd_people`, `cmd_expenses`, `cmd_repayments`, `cmd_debts` — keep
printing their own rows exactly as they did and return `None`. `main` reads:

```python
line = args.handler(args, ledger)          # ValidationError → stderr, exit 2, as before
if line is not None:
    store.save(path, ledger)               # StoreError → stderr, exit 1, as before
    print(line)                            # only reachable when save returned
```

So no statement in `main` writes to stdout before `store.save` has returned. The success wording
is byte-identical to before for all three commands, and nothing changes on the success path: the
observable difference is confined to the failing-write path, which is the defect.

Nothing outside `cli.py` changed. `store.py`, `model.py` and `debts.py` are untouched, and the
plan's check that no other module or test reads a handler's return value held — all 116 tests
pass unaltered.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — with the ledger location unwritable, each of `add-person`, `add-expense` and `repay` prints nothing on stdout, prints the failure on stderr, and exits non-zero | `main` prints the returned line only after `store.save` returns, so the `StoreError` path returns `EXIT_STORE` before anything reaches stdout (plan steps 1–3) | Two independent runs. **(a)** `tests.test_persistence.TestAFailedWriteSaysNothingOnStdout.test_every_recording_command_prints_nothing_when_the_save_fails`, which asserts `stdout == ""`, non-empty stderr and a non-zero exit for all three commands via `subTest`. **(b)** BUG-0001's own six reproduction steps by hand, stdout and stderr captured separately: step 4 printed `stdout=[] exit=1` with `error: cannot write the ledger at /tmp/tmp.4FTOMeznc0/l.json: [Errno 13] Permission denied: '…l.json.y6zqlo24.tmp'` on stderr, and the same for `add-expense --payer Ana --amount 10 --description x` and `repay --from Ana --to Ben --amount 5`. Step 6 (`chmod 700`, then `people`) printed `Ana` and `Ben` and no `Cara`. Before the fix, step 4 printed `Added Cara.` — see AC2's before-run |
| AC2 — a regression test covers all three commands against an unwritable location, asserting empty stdout, and fails if the success line is moved back before the save | The new test class in `tests/test_persistence.py`, written and run **before** the fix so that its failure against the defect is on the record | `python3 -m unittest tests.test_persistence.TestAFailedWriteSaysNothingOnStdout -v` against the unfixed code at `17ca1fa`: `FAILED (failures=3)`, one per `subTest`, with `AssertionError: 'Added Cara.\n' != ''`, `AssertionError: 'Recorded 10.00 paid by Ana for x.\n' != ''` and `AssertionError: 'Recorded Ana repaying 5.00 to Ben.\n' != ''` — the three lines BUG-0001 quotes as the actual behaviour. Against the branch head, `python3 -m unittest discover -s tests -t . -q` → `Ran 116 tests … OK`, exit 0. Moving the `print(line)` back before `store.save` reproduces those three failures exactly, because that is the state it was run against |

Both criteria are left **unticked** in `item.md`; see the deviation below.

## Deviations from the plan

1. **Step 7's instruction to tick both criteria in `item.md` was not carried out.** The plan says
   to "tick both criteria in `item.md` only against that run". `spec/work-item.md` says
   "`verify` ticks a box only when it has evidence for it, and cites that evidence in
   `verify-report.md`" — ticking is the verifier's act, and a box `implement` ticked would tell
   `verify` that something had already been confirmed by someone independent, which is the one
   thing this pipeline arranges for it not to mean. The evidence the plan wanted recorded is in
   the table above instead, which is what `verify` reads. This changes no code and no criterion;
   it moves one act to the skill the spec assigns it to.
2. **Step 5's assertion about `Cara` was made stronger than written.** The plan says to assert
   that `Cara` is absent from the `people` listing after the permissions are restored. The test
   asserts the full listing equals `["Ana", "Ben"]`, which entails `Cara`'s absence and also
   catches a ledger that lost or reordered what was already recorded. No plan step is skipped.
3. **The docstring sentence of step 4 is a short paragraph rather than one sentence.** It states
   the contract, cites `ADR-0011`, and adds the listings' exception, because a reader adding a
   command needs to know that returning `None` after printing rows is deliberate rather than an
   oversight — which is the misreading `ADR-0011` names as option A's own risk.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → `Ran 116 tests in 3.002s / OK`, exit 0, on the branch head `d727aba` |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses tests` → exit 0 |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → `checked 5 item(s), 13 document(s) / 0 errors, 0 warnings` |
| `every-criterion-has-a-test` | **pass** | AC1 → `TestAFailedWriteSaysNothingOnStdout.test_every_recording_command_prints_nothing_when_the_save_fails`, plus the by-hand reproduction quoted above. AC2 → the recorded pre-fix run of that same test, `FAILED (failures=3)`. Neither criterion rests on reading the code |
| `commits-reference-the-item` | **pass** | `check-commit-refs BUG-0001 wi/BUG-0001` → `all 2 commit(s) on main..wi/BUG-0001 name BUG-0001`, exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main..HEAD` is three files. `expenses/cli.py`: the docstring paragraph (step 4), seven signature changes and three `return`s (steps 1–2), and `main`'s rename plus the moved `print` (step 3). `tests/test_persistence.py`: one added class (step 5). `docs/architecture/overview.md`: the `cli.py` bullet, the header version and one change-log row (step 6). No hunk traces to anything else |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → `0 errors, 0 warnings`, exit 0 |

## What I did not do

- **The AC boxes in `item.md` are unticked.** Deliberate, per deviation 1 — `verify` ticks them.
- **`CliTestCase.assertRefused` was not strengthened to assert empty stdout.** The plan lists this
  under "Out of scope for this item" and it stays there: it maps to no criterion of BUG-0001, and
  every validation refusal already prints nothing on stdout, so the assertion would guard future
  changes rather than fix anything today. It remains a visible opportunity in the plan.
- **No wording, exit code or stderr text was changed**, and no listing's output was touched. The
  three success lines are byte-identical to before; only their timing moved.
- **The in-process harness (`tests/cli_harness.py`) was not used for the regression test.** The
  defect is about what a process writes to stdout when a write to the filesystem fails, and
  BUG-0001's reproduction is stated in real processes; `test_persistence.py`'s `run` helper and
  its `skipIf(os.geteuid() == 0)` guard are what the plan named, so under root the test is skipped
  rather than passing vacuously. It was not run as root here — it failed three times before the
  fix and passes after, so it executed.
- **`WI-0003`'s import command** is not touched. It is `blocked` and will inherit this contract.
