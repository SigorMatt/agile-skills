---
id: BUG-0001
type: bug
title: A failed ledger write still prints the success line on stdout
status: done
priority: medium
epic: EP-001
created: "2026-08-22T02:27:53Z"
updated: "2026-08-22T04:00:22Z"
found-in: WI-0001
branch: wi/BUG-0001
outcome: delivered
---

## Summary

All three recording commands — `add-person`, `add-expense` and `repay` — print their success
line to stdout **before** `main` attempts to save the ledger. When the save then fails, the run
emits a success message and an error message together and exits 1. Nothing was recorded, so the
user is told two contradictory things about the same run; a script reading stdout is told the
wrong one. Found while verifying WI-0001 on branch `wi/WI-0001` at commit
`49dd2a0cffdabf33fd4976f9d93bfc62edbc591f`.

The module docstring of `expenses/cli.py` states the intended order as "resolve the ledger path,
load, apply one change, save atomically, print, return 0" — the code does the print and the save
the other way round, so this is a slip against the stated design rather than a choice.

## Steps to reproduce

1. `V=$(mktemp -d)`
2. `python3 -m expenses --file $V/l.json add-person Ana` — succeeds, exit 0
3. `chmod 500 $V` — make the directory unwritable
4. `python3 -m expenses --file $V/l.json add-person Cara`
5. Repeat step 4 with `add-expense --payer Ana --amount 10 --description x` and with
   `repay --from Ana --to Ben --amount 5` (after adding Ben in a writable state) — all three
   behave the same way.
6. `chmod 700 $V; python3 -m expenses --file $V/l.json people` — confirms nothing was recorded.

## Expected behaviour

A run that records nothing says nothing on stdout about having recorded something. The success
line belongs after the save, so it is printed only when the save succeeded. WI-0001 AC9 requires
that a location that cannot be written is refused, and the head of WI-0001's criteria defines a
refusal as a stderr message, a non-zero exit code, and no change to the recorded data — all three
of which do hold today. The contradiction on stdout is what is wrong.

## Actual behaviour

Step 4, verbatim:

```
error: cannot write the ledger at /tmp/tmp.jwFdK2yluI/l.json: [Errno 13] Permission denied: '/tmp/tmp.jwFdK2yluI/l.json.fh365i1x.tmp'
Added Cara.
```

exit code `1`. With stderr discarded, the run prints only `Added Cara.` and exits 1. The other
two commands print `Recorded 10.00 paid by Ana for x.` and `Recorded Ana repaying 5.00 to Ben.`
under the same conditions.

`python3 -m expenses --file $V/l.json people` afterwards prints only `Ana` and `Ben`: the data is
genuinely unchanged, which is why no WI-0001 criterion catches this.

## Acceptance criteria

- [x] AC1 — with the ledger location unwritable, each of `add-person`, `add-expense` and `repay`
      prints nothing on stdout, prints the failure on stderr, and exits non-zero. Reproduced by
      the six steps above
- [x] AC2 — a regression test covers all three commands against an unwritable location, asserting
      empty stdout, and fails if the success line is moved back before the save

## Notes

- **Why this is a bug item and not a send-back to WI-0001.** `verify`'s rule is that a send-back
  is for a failure of the item's *own* acceptance criteria. WI-0001's criteria define "refused" as
  three things — a stderr message, a non-zero exit, and unchanged data — and all three hold here.
  No criterion of WI-0001 constrains stdout on a failed write, so WI-0001 is not failing; this is
  behaviour nobody specified. Recording it as its own item keeps WI-0001's verdict honest and
  keeps the defect from disappearing.
- **The fix is small and local:** move the `print(...)` in `cmd_add_person`, `cmd_add_expense` and
  `cmd_repay` to after a successful save in `main`, or have the handlers return the line for
  `main` to print once the save has returned. The second shape keeps the "every command is the
  same skeleton" property that `tracker/items/WI-0001/artifacts/plan.md` sets out.
- The same ordering makes a `StoreError` on **load** behave correctly already, because `load` runs
  before any handler.

- **Gaps accepted at review, recorded here so they outlive this item.** `review-close` accepted
  each of these rather than sending the item back; none is covered by an acceptance criterion.
  - **Neither criterion is verified under `root`.** The regression test guards itself with
    `skipIf(os.geteuid() == 0)` because root ignores directory permissions, and verification ran
    as uid 1000. What the tool does when a genuinely unwritable location is met as root is
    unchecked, by both the test and the manual reproduction. Accepted: the guard is the honest
    option — without it the test would pass vacuously as root, which is worse than skipping — and
    the tool is a local command-line tool for one person's friend group.
  - **The claim that `WI-0003`'s importer inherits the ordering is unverified**, because no import
    command exists yet. It is `ADR-0011`'s main argument for changing the contract rather than
    moving three `print` calls, and it can only be checked when WI-0003 is built. WI-0003's
    implementer should confirm it rather than assume it.
  - **`CliTestCase.assertRefused` still does not assert empty stdout.** `BUG-0001`'s plan lists
    this under "Out of scope" and review agrees it was right to leave alone — widening a shared
    assertion inside a bug fix would have made both changes harder to review. It remains worth
    doing: every validation refusal already prints nothing on stdout, so the assertion would pass
    today and would guard every refusal test in future. Noted here rather than in a closed item's
    plan so that it is still findable.
  - **A ledger file at mode 400 in a writable directory is still overwritten.** Exercised during
    verification: `add-person` succeeds and records, because `store.save` renames a temporary file
    over the target and POSIX `rename` needs permission on the directory, not on the file. This is
    correct behaviour for an atomic write and contradicts no criterion, but a reader could
    reasonably expect mode 400 to protect a ledger, and it does not.
