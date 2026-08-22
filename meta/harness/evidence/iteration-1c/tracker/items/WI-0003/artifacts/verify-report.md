# Verification report — WI-0003

Verified-commit: e8a82310b21ca9b46afc6571f287b35c8f71a64f

## Verdict

**Pass.** All nine acceptance criteria were checked independently, by deriving from each criterion
what would settle it and running that against the branch head before reading `impl-report.md`'s
evidence column. Every criterion passes. No defect was found and no bug item was filed.

One thing is worth reading before the table: **AC9's test is weaker than AC9's heading**, and this
verification says so and then checks the behaviour a stronger way. See `## Test sensitivity check`.

## Criteria

Every command was run from the repository root on branch `wi/WI-0003`, against data files under
`/tmp/v3/` that did not exist when their criterion started.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | a four-person ledger — `10.00` by Ana shared three ways, `7.77` by Cass shared three ways, `0.13` by Dan shared four ways — then `./expenses report` | `Ana is owed 4.03 / Ben owes 3.36 / Cass is owed 1.82 / Dan owes 2.49`, then `Ben pays Ana 3.36 / Dan pays Ana 0.67 / Dan pays Cass 1.82` | parsed the printed report and applied the payments to the printed balances: all four reach zero; `payments=3 nonzero=4 bound_ok=True` |
| AC2 | **pass** | the worked example built with five invocations, then `./expenses report … \| cat -A` | `Ana is owed 15.00$ / Ben is square$ / Cass owes 15.00$ / $ / Cass pays Ana 15.00$` | `cat -A` confirms the blank line is empty and there is no trailing whitespace; the output matches the criterion's quoted block exactly |
| AC3 | **pass** | the AC1 ledger, parsed | `balances sum: 0`, `paid total == received total: True`, `after payments, all zero: True` | checked on data with an indivisible split, not only on the worked example |
| AC4 | **pass** | `./expenses report` against a store with nobody and nothing; then a store where Ana paid `10.00` for her own lunch | `Nobody owes anybody`, `exit=0`; and `Ana is square / Ben is square / (blank) / Nobody owes anybody`, `exit=0` | both halves of the criterion: the sentence alone, and the sentence after the balances |
| AC5 | **pass** | the two expenses recorded in separate `bash -c` processes, `report` run in another | the AC2 output | each step is its own process, so nothing could be held in memory |
| AC6 | **pass** | `Ana`, `Ben`, `Cass`; one `10.00` expense paid by Ana shared by all three; `./expenses report` | `Ana is owed 6.66 / Ben owes 3.33 / Cass owes 3.33 / (blank) / Ben pays Ana 3.33 / Cass pays Ana 3.33` | matches the criterion's quoted block; `666 = 1000 - 334` and `333 + 333 = 666` by hand |
| AC7 | **pass** | registered `Cass`, `ana`, `Ben`, `Dan` in that order; `ana` paid `30.00` shared by `ana,Ben,Cass`; `./expenses report` | `ana is owed 20.00 / Ben owes 10.00 / Cass owes 10.00 / Dan is square` | normalised order, not registration order and not ASCII order (`ana` first); `Dan`, who shared in nothing, appears; `2000 - 1000 - 1000 = 0` |
| AC8 | **pass** | the worked example, then `./expenses add-person Dan`, then `./expenses report` | `Ana is owed 15.00 / Ben is square / Cass owes 15.00 / Dan is square / (blank) / Cass pays Ana 15.00` | the shares of the two recorded expenses did not change when a fourth person was registered |
| AC9 | **pass** | `cmp` before and after `report`; `diff` of two consecutive runs; and `stat -c 'inode=%i mtime=%Y size=%s'` before and after | `bytes unchanged: yes`, `repeatable: yes`, and `inode=6987881 mtime=1787351689 size=495` identical before and after — against `inode=6987886` after a deliberate `add-person`, which shows what a write looks like | the byte comparison the criterion names is satisfied; the inode and mtime check is stronger and is what actually establishes "never writes" |

All nine checkboxes in `item.md` were ticked after — and only after — the run above.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 87 tests`, `OK` |
| `lint-clean` | **pass** (weak by design) | `python3 -m compileall -q expenses expenses_tool tests` → exit 0; a syntax check (ADR-0007 clause 4) |
| `workspace-valid` | **pass** | `validate-workspace` → exit 0, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | the nine rows above, each a command this skill ran with its output quoted |
| `negative-cases-exercised` | **pass** | both empty cases (AC4), the indivisible split (AC6), a person who shared in nothing (AC7), a person registered after the fact (AC8), and repeated runs (AC9) |

## Negative and boundary cases exercised

- **An empty store and an empty settlement**, which are different code paths producing the same
  sentence (AC4).
- **An indivisible amount in a multi-expense ledger** (AC1/AC3's four-person case), not only the
  clean `10.00` of AC6 — this is where a rounding error would show as balances that do not sum to
  zero, and they summed to zero.
- **A ledger where the alphabetical order and the registration order differ** (`Cass`, `ana`,
  `Ben`, `Dan`), which checks ADR-0003's normalised sort rather than ASCII or insertion order.
- **A person registered after the expenses** (AC8), the report-side counterpart of WI-0002's
  snapshot.
- **A deliberate write, for contrast**, to establish what a changed file looks like when checking
  AC9.

## Test sensitivity check

Four behaviours were removed in turn, the suite re-run, and the code restored with
`git checkout -- expenses_tool` each time.

| what was broken | edit | result |
|-----------------|------|--------|
| the leftover penny is dropped instead of given out by name order | `shares` returns `base` for everyone | **FAILED (failures=32)** |
| balances recomputed from today's people rather than the stored sharers | `shares(…, data["people"])` | **FAILED (failures=6)** |
| the printed payments are not sorted | `reversed(settle.settle(…))` | **FAILED (failures=1)** |
| **the report writes the ledger back** | `store.save(path, data)` added to `cmd_report` | **OK — no test failed** |

**The fourth result is a finding about the criterion, not about the code.** AC9 asks that `cmp`
show the file "byte-for-byte unchanged", and a report that rewrote the file with identical content
would satisfy exactly that — so neither AC9's test nor AC9's literal wording can detect a write. I
therefore checked the behaviour a stronger way: `stat` reports the same inode, mtime and size
before and after `report`, while a deliberate `add-person` changes the inode (the atomic write of
ADR-0006 clause 5 replaces the file). Together with reading `cmd_report`, which contains no
`store.save` — `grep -n "store.save" expenses_tool/cli.py` finds it only in `cmd_add_person`
and `cmd_add_expense` — the behaviour AC9 is *about* holds.

This is recorded rather than fixed: amending a criterion is not this skill's job, and the behaviour
is correct today. It is flagged for `review-close` as a weakness in the criterion's construction,
and the honest summary is that AC9 passes on its own terms and passes a stricter test I ran myself.

## Defects found

None. No criterion failed.

The diff was read for unaccounted scope: `expenses_tool/settle.py` (new), three additions to
`cli.py`, two new test modules, and `README.md`, all named in `plan.md` steps 1–9, plus the
tracker files. `item.md`'s diff shows only `status`, `branch` and `updated`.

## Not verified, and why

- **Which settlement is printed when more than one is minimal.** The item leaves this
  unconstrained and ADR-0010 decides it; nothing here checks that the *particular* settlement is
  the one a different algorithm would produce, because no criterion asks.
- **Behaviour with a very large group.** Every check used three or four people. The item names this
  as unconstrained; nothing was measured.
- **Style, as opposed to syntax** — `compileall` only (ADR-0007 clause 4).
- **The AC9 insensitivity described above**, restated here so it is not buried: no automated test in
  this suite would fail if `report` began writing the file back with identical content.
- **A ledger containing an expense whose `shared_by` names somebody no longer in `people`.**
  ADR-0009 clause 5 says this cannot arise and nothing defends against it; `settle.balances` would
  add a key for that person and the report would show them. Not reachable through the tool, not
  tested, and recorded because a hand-edited file could produce it.
- **Concurrency**, unchanged from WI-0002: nothing here writes, so `report` is safe, but a report
  run while another process is mid-write is not something this suite examines.
