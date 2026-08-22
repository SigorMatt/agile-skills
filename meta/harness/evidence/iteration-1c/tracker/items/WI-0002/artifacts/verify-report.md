# Verification report — WI-0002

Verified-commit: c59b1342471b8c9c6dc1edfe2013d6171d8f544b

## Verdict

**Pass.** All nine acceptance criteria were checked independently: what would settle each one was
derived from the criterion's own wording and run as shell commands against the branch head, before
`impl-report.md`'s evidence column was read. Every criterion passes. No defect was found in this
item's behaviour and no bug item was filed — including against WI-0001, whose delivered behaviour
this item extended.

## Criteria

Every command was run from the repository root on branch `wi/WI-0002`, against a data file under
`/tmp/v2/` that did not exist when its criterion started; the people each criterion needs were
registered first with `add-person`.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `./expenses add-expense --paid-by Ana --amount 30.00 --description dinner --shared-by Ana,Ben,Cass --date 2026-08-14 --data-file $T`; then the same with `--share-amount 10.00` | `exit=0`, `stdout=[Added 2026-08-14 30.00 dinner — paid by Ana, shared by Ana, Ben, Cass]`, `stderr=[]`; `share-amount exit=2` | the rendering matches the item's form exactly; a per-person amount is rejected by the parser, not ignored |
| AC2 | **pass** | record `taxi` with **no** `--shared-by`; then `add-person Dan`; then `list-expenses` | `Added 2026-08-14 9.00 taxi — paid by Ana, shared by Ana, Ben, Cass`; after Dan: `2026-08-14 9.00 taxi — paid by Ana, shared by Ana, Ben, Cass` | the sharers did not change when a fourth person was registered — the snapshot ADR-0009 clause 3 requires |
| AC3 | **pass** | two expenses recorded in separate invocations (the later date first, the second from a new shell), then `list-expenses` from a third; and `list-expenses` against a path that does not exist | `2026-08-02 9.00 taxi — paid by Ben, shared by Ana, Ben` then `2026-08-14 30.00 dinner — paid by Ana, shared by Ana, Ben`, `exit=0`; and `No expenses recorded yet`, `exit=0` | date order, not record order; the empty case is stdout and 0 |
| AC4 | **pass** | `--paid-by Dan …`; `--shared-by Ana,Dan`; then `--paid-by ana --shared-by ana,BEN` | `payer exit=1 stdout=[] stderr=[Unknown person: Dan]`; `sharer exit=1 stderr=[Unknown person: Dan]`; `cmp` reports the file unchanged; the case-different run printed `Added 2026-08-14 30.00 dinner — paid by Ana, shared by Ana, Ben` and `exit=0` | the unknown name is echoed as typed; a case-different sharer resolves to the stored spelling |
| AC5 | **pass** | `--amount` of `0`, `-5`, `abc`, `1.005`; then `30` and `30.5` | four × `exit=1` with `stderr=[Amount must be a positive number with at most two decimal places: <value>]`; then the listing shows `30.00` and `30.50` | `1.005` is refused, not rounded — the behaviour ADR-0001 depends on |
| AC6 | **pass** | record with no `--date`; then `--date` of `2026-13-01`, `14/08/2026`, `today` | `Added 2026-08-22 30.00 dinner …` while `date +%F` = `2026-08-22` and `date -u +%F` = `2026-08-21`; three × `exit=1` with `stderr=[Date must be a calendar date in YYYY-MM-DD form: <value>]` | this is the criterion `plan` stopped on: the local date is used, and on this machine it is provably not the UTC date |
| AC7 | **pass** | omit `--description`; then `--description "   "` | `missing --description exit=2`; `blank exit=1 stdout=[] stderr=[An expense needs a description]` | usage error versus refusal, as ADR-0005 clause 3 separates them |
| AC8 | **pass** | `--shared-by Ana,ana`; then `--shared-by ""` | `exit=1 stderr=[Ana is named twice in --shared-by]`; `exit=1 stderr=[--shared-by must name at least one person]`; `cmp` reports the file unchanged | the duplicate message names the *stored* spelling |
| AC9 | **pass** | one refusal from each of AC4–AC8 against a store already holding one expense, comparing `list-expenses` output and the file's bytes after each | five × `exit=1 listing and bytes unchanged` | "records nothing" is observable from outside, not inferred from the code |

All nine checkboxes in `item.md` were ticked after — and only after — the run above.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 62 tests in 3.940s`, `OK`, run by this skill on the branch head |
| `lint-clean` | **pass** (weak by design) | `python3 -m compileall -q expenses expenses_tool tests` → exit 0; ADR-0007 clause 4 records that this is a syntax check |
| `workspace-valid` | **pass** | `validate-workspace` → exit 0, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | the nine rows above, each a command this skill ran with its output quoted |
| `negative-cases-exercised` | **pass** | AC4, AC5, AC6, AC7, AC8 and AC9 are all negative cases and were triggered; plus the two boundary cases below |

## Negative and boundary cases exercised

- **A data file written before `expenses` existed.** `{"schema": 1, "people": ["Ana"]}` →
  `No expenses recorded yet`, exit 0. WI-0001's files still work, which is what ADR-0006 clause 2
  promises and what nothing else in this item would have caught.
- **A hand-edited file with a fractional `amount_pence`.** `30.5` →
  `Cannot read /tmp/v2/frac.json: one of its expenses has an amount that is not a whole number of
  pence`, exit 1. ADR-0001 clause 1 says no float ever holds an amount; without this guard the
  file would load and WI-0003 would compute a balance from it.
- **`--share-amount`**, the option that must not exist, → exit 2 with nothing recorded.
- **A case-different sharer** (`--shared-by ana,BEN`) → accepted and stored under the registered
  spellings, which is the other half of AC4 and the case an over-strict implementation gets wrong.
- **Five refusal paths against a non-empty ledger** (AC9), each compared by bytes as well as by
  output.

## Test sensitivity check

Four behaviours were removed in turn, the suite re-run, and the code restored with
`git checkout -- expenses_tool` each time. Two of the four needed a second attempt: my first
edit for the amount case did not match anything in the file, and the suite passed — which is
exactly the false negative this step exists to catch, and is recorded here rather than quietly
re-run.

| what was broken | edit | result |
|-----------------|------|--------|
| the sharers are re-resolved at listing time instead of snapshotted | `list_expenses` overwrites `shared_by` from `data["people"]` | **FAILED (failures=1)** — AC2's test |
| a third decimal place is truncated instead of refused | `_AMOUNT` regex allows trailing digits | **FAILED (failures=4)** |
| the default date becomes UTC | `today()` returns `datetime.now(timezone.utc).date()` | **FAILED (failures=2)** |
| the save happens before validation | `store.save(path, data)` replaced by `pass` | **FAILED (failures=11, errors=6)** |

Each touches a different criterion group (AC2, AC5, AC6, AC1/AC3/AC9), and each produced failures.

## Defects found

None. No criterion of this item failed.

**One thing was examined and deliberately not filed as a bug.** `implement` changed an existing
WI-0001 unit test (`tests/test_store.py::test_a_missing_file_is_an_empty_store`) because
`empty_data()` now carries an `expenses` key. I checked whether that was WI-0001 behaviour being
altered: it is not. No WI-0001 acceptance criterion mentions the dict's shape, all of WI-0001's
end-to-end tests pass untouched on this branch, and a WI-0001-era data file still loads — which I
verified directly, not by reading the report. The change is an extension, and two tests were added
alongside it to pin exactly that compatibility.

The diff was read for unaccounted scope: nine source, test and documentation files, all named in
`plan.md` steps 1–12, plus the tracker files. `item.md`'s diff shows only `status`, `branch`
and `updated` — no criterion was touched by `implement`.

## Not verified, and why

- **Style, as opposed to syntax.** `commands.lint` is `compileall`; nothing here says anything
  about naming, unused imports or dead code (ADR-0007 clause 4).
- **An unwritable `--data-file` path.** Unchanged from WI-0001, where it is a recorded accepted
  gap: `add-expense` writes through the same `store.save`, so it inherits the traceback. No
  criterion covers it.
- **A description containing ` — ` or a comma.** The item's `## Notes` records this as
  deliberately unconstrained; the rendered line becomes ambiguous to a parser, and nothing in this
  epic parses it. Not tested, by design.
- **Two people whose names differ only by an accent.** ADR-0003 declined accent-folding, so
  `--shared-by José,Jose` is not a duplicate and would record a two-way split between two people
  the stakeholder may consider one. Follows from a recorded decision; no criterion covers it.
- **The listing at scale.** Every check here used one or two expenses. Nothing establishes what a
  hundred expenses look like, and no criterion asks.
- **Concurrent invocations.** Two `add-expense` processes writing the same file at once could
  lose one record: each loads, appends and replaces. Nothing in the epic mentions concurrency —
  it is one person at one terminal (`docs/product/vision.md`) — and no criterion covers it, but a
  reader should know it was considered and not checked.
