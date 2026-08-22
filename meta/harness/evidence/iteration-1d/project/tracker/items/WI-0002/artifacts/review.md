# Review — WI-0002

## What I examined

- `tracker/items/WI-0002/item.md` — the eleven acceptance criteria, the tick state, and the
  `## Notes` sections carrying `refine`'s decisions and the R10 combination table.
- `tracker/items/WI-0002/history.md` — all eight rows, checked for chaining and against
  `item.md`'s status.
- `tracker/items/WI-0002/journal.md` — all eight entries, read in full, one per skill execution
  the history implies.
- `tracker/items/WI-0002/artifacts/plan.md`, `impl-report.md`, `verify-report.md`,
  `refinement-qa.md`.
- `tracker/items/WI-0002/questions/Q-001.md` — `answered`, `answered-by: human`, four files named
  under `## Consequences`, each of which exists.
- **The diff, hunk by hunk:** `git diff main..wi/WI-0002` — `expenses/debts.py` (93 lines, new),
  four hunks in `expenses/cli.py` (the import, `NOBODY_OWES`, the subparser, `cmd_debts`),
  `tests/test_debts.py` and `tests/test_cli_debts.py` (new), and the overview's v5 edit.
- `docs/architecture/adr/` — `ADR-0001`, `ADR-0002`, `ADR-0003`, `ADR-0004`, `ADR-0006`,
  `ADR-0008`, `ADR-0009`, read for contradiction with what was built.
- Code the change reaches but does not contain: `expenses/model.py` (`normalise_name`,
  `format_amount`, `Ledger.from_dict`), `expenses/store.py` (`load`, and what it refuses).

### The claims I checked, and what I opened to check them (D12)

Each absolute claim the delivered work touched, decided by opening the thing it cites — not by
reading the sentence again.

| claim | cited to | opened | verdict |
|-------|----------|--------|---------|
| `debts.py` "imports from `model` only, reads no file, prints nothing" | `ADR-0008`; `expenses/debts.py` | `expenses/debts.py` — imports are `dataclasses` and `expenses.model`; no `open`, no `print` | **true** |
| `debts.py` "raises nothing — every ledger the store can load has a debt report, including an empty one" | `ADR-0008`; `expenses/debts.py` | `expenses/debts.py` line 74, `expenses/model.py` `Ledger.from_dict`, `expenses/store.py` `load` | **false as written** — see finding F1 |
| "The remainder rule it applies has no branch on whether the payer is among the sharers" | `ADR-0009`; `expenses/debts.py` | `expenses/debts.py` — one `share = amount_minor // len(sharers)`, and `_add` returns early when debtor and creditor normalise equal; no payer-membership test anywhere | **true** |
| "`debts` takes no options of its own and writes nothing" | `WI-0002` AC1/AC4/AC5; `expenses/cli.py` | `expenses/cli.py` — the subparser adds no argument; `cmd_debts` returns `False`, and `main` saves only when a handler returns `True` | **true** |
| "`--file` is global and must appear before the subcommand; placed after it, `argparse` reports an unrecognised argument and exits 2" | `expenses/cli.py` | `expenses/cli.py`; and `verify-report.md` triggered it for `debts` specifically | **true** |
| "the debts are pairwise: nothing is re-routed between pairs, so a circle is printed" | `ADR-0006` | `expenses/debts.py` — the accumulator is keyed per unordered pair and no value is ever moved between keys; AC8's test asserts the printed circle | **true** |
| "`cli.py` … is the only module that writes to stdout or stderr. It does not exit: `main` returns the code" | `expenses/cli.py`; `expenses/__main__.py` | both files | **true** in the overview — but the `cli.py` module docstring still says the opposite of its second half; see finding F2 |
| `ADR-0009`'s worked consequence: `--payer Ana --amount 10.01 --shared-by Ben --shared-by Cara` reports `5.00` from each and the odd cent is Ana's | `WI-0002` AC3 | ran it: `Ben owes Ana 5.00` / `Cara owes Ana 5.00` | **true** |

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion checkbox ticked | **pass** | eleven `- [x]` in `item.md`, AC1–AC11; `validate-workspace` exit 0, which fails an unticked criterion on a delivered item |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | eleven rows in the report's `## Criteria`, each naming a command `verify` ran and quoting its actual output; `impl-report.md` is cited in none of them |
| D3 | the declared gates passed on the final state of the code, not an earlier one | **pass** | `implement`'s gates ran at `1d47123`, the last code commit; `verify` re-ran the suite, the lint and the validator itself at `c73f039`; this review re-ran the suite and the lint on the merge result — `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 115 tests`, `OK`; `python3 -m compileall -q expenses tests` → exit 0 |
| D4 | no open blocking question | **pass** | `Q-001` is the only question on the item and is `answered`; `validate-workspace` exit 0 |
| D5 | a journal entry per execution; history chains to the current status | **pass** | eight history rows, eight journal entries, each row's `from` equal to its predecessor's `to`, last row `verifying → in-review` matching `item.md`; `validate-workspace` exit 0 |
| D6 | every design-changing decision is in an ADR, cited from the plan or journal | **pass** | `ADR-0008` (pure module) and `ADR-0009` (the remainder when the payer does not share), both cited from `plan.md`'s `## Decisions and ADRs` and from the `plan` journal entry; the four smaller choices are recorded as reversible assumptions in `plan.md` with what reversing costs |
| D7 | documents the change invalidated were updated, with a version bump and a change-log row | **pass** | `docs/architecture/overview.md` v4 → v5 by `implement` (step 5 of the plan), change-log row present; this review adds v6 for finding F1, also with a row |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → exit 0, "all 4 commit(s) on main..wi/WI-0002 name WI-0002" |
| D9 | merged into the trunk | **pass** | trial-merged into a throwaway copy of `main` and tested green before closing; merged into `main` for real after the close, per the skill's ordering |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0002 wi/WI-0002` → exit 0: "verified at `c73f039b`; `wi/WI-0002` has moved to `9b007eb2` but only the record changed (5 file(s) under `tracker/` or `docs/`)". The last code commit is `1d47123`, which precedes `c73f039` |
| D11 | `review.md` exists and states what was examined | **pass** | this file; `## What I examined` is first and names the diff range, the artifacts, and the claims audited with what was opened for each |
| D12 | claims in `docs/` about the behaviour this item touched are still true; absolute claims carry a resolvable citation | **fail on one claim, corrected here** | the claims table above: seven of eight verdicts true, one false as written (F1). `docs/architecture/overview.md` is corrected to v6 and the sentence now says what the code supports. `lint-claims --changed-since main` → exit 0 |

## Findings

**F1 — `debts.py` does not "raise nothing", and three documents say it does.** The sentence is
"it … raises nothing — every ledger the store can load has a debt report, including an empty one",
written first in `ADR-0008` by `plan`, then copied into `docs/architecture/overview.md` v5 and
into `expenses/debts.py`'s own module docstring by `implement`. `Ledger.from_dict` checks that
the keys are present and not what their values hold, so a hand-edited ledger whose
`amount_minor` is the JSON string `"3000"` loads without a `StoreError` and then reaches
`share = expense.amount_minor // len(expense.sharers)`:

```
$ python3 -m expenses --file /tmp/rc/hand.json debts
Traceback (most recent call last):
  ...
  File ".../expenses/debts.py", line 74, in debts
    share = expense.amount_minor // len(expense.sharers)
TypeError: unsupported operand type(s) for //: 'str' and 'int'
$ echo $?
1
```

This is the D12 failure mode exactly — a confident sentence about named code that the code does
not support, re-quoted across documents rather than re-checked. Three things follow, and they are
deliberately different:

- **`docs/architecture/overview.md` is corrected**, to v6 with a change-log row. That is this
  skill's own gate to enforce and the project's own precedent — v3 was `review-close` correcting a
  false sentence for WI-0001.
- **`ADR-0008` is left as written.** Superseding or amending a recorded decision is not this
  skill's to do, and the sentence is a statement of design intent — the module defines no error
  path of its own — which is true of it. The overview now names the ADR as the place the
  unqualified wording lives, so a reader who starts there finds the qualification.
- **`expenses/debts.py`'s docstring is left as written**, and accepted as a gap below. It is
  source, so changing it now would put a code commit after the verification and send the item back
  to `verifying` under D10 for one sentence — a worse trade than recording it.

**F2 — the behaviour behind F1 is a defect, and it belongs to WI-0001, not here.** The same
hand-edited ledger breaks the `expenses` and `repayments` listings through `format_amount`, at
`expenses/cli.py` line 192, with the same `TypeError` and the same traceback to the terminal.
`store.py`'s own docstring says "a file that cannot be read, written or parsed raises StoreError",
and `load` catches `AttributeError`, `KeyError` and `TypeError` around `Ledger.from_dict` — so
refusing a mis-shaped ledger cleanly is the recorded intent, and value types slip through the
guard. The right record for it is a bug item with `found-in: WI-0001`, and **this skill could not
file one**: `pipeline.yaml`'s only `null → ready` transition names `verify` as its actor, and the
only `null → draft` transition names `intake`, so a bug filed by `review-close` would fail
`validate-workspace` as an illegal transition. `review-close`'s own SKILL.md tells it to file a
bug item in this situation, so the contract and the pipeline disagree. It is recorded here and in
this turn's harness status instead, and it is neither a defect in WI-0002's delivery nor a reason
to hold the item open — `debts` is no more exposed than the commands WI-0001 shipped.

**F3 — no finding in the change itself.** Every hunk maps to a plan step and to a criterion:
`debts.py` is plan step 1 (AC1–AC11), `tests/test_debts.py` step 2 (AC3, AC9), the four `cli.py`
hunks step 3 (AC1, AC4), `tests/test_cli_debts.py` step 4 (all eleven), and the overview edit step
5. Nothing in the diff contradicts an ADR. The two things worth saying about the code, both
positive: the signed-per-pair accumulator makes AC6's direction reversal and AC7's "never a
`0.00` line" fall out of the arithmetic instead of being special cases, and the ordering tests use
people whose display forms and case-folded forms sort *differently*, so they would fail against a
sort on the printed names — the trap both `implement` and `verify` record hitting and fixing.

## Accepted gaps

Each of these is also written into `item.md`'s `## Notes`, so it survives this item closing.

1. **`expenses/debts.py`'s module docstring still says "raises nothing — every ledger the store
   can load has a debt report".** Reason for accepting: correcting it is a code change after
   verification, which D10 would rightly send back to `verifying`; the overview, which is where a
   reader looks first, now carries the qualification. Whoever next opens `debts.py` for a code
   reason should fix the sentence in the same commit.
2. **`expenses/cli.py`'s module docstring still says the module is "the only one that exits".**
   Inherited from WI-0001, false since `main` returns an `int`, corrected in the overview at v3 and
   flagged by `implement` and by `verify` on this item without being fixed. Same reason as 1, and
   the same instruction: whoever touches `cli.py` next fixes it.
3. **Scale is unverified.** `verify` checked AC3's identity on thirteen small ledgers, not on a
   generated large one. No criterion states a size and `ADR-0003` puts scale outside this
   project's frame.
4. **The default ledger location was not exercised for `debts`.** Every check used `--file`.
   `debts` shares the one `store.resolve_path` call every command uses, and the default path is
   WI-0001 AC9's territory, verified there.
5. **Concurrency and terminal rendering were not tested.** No criterion mentions either, and
   `ADR-0003`'s single-process, single-file model does not claim the first.

## Verdict

**Accepted, and closed as `delivered`.** All eleven acceptance criteria are ticked, each against a
command `verify` ran itself; the Definition of Done passes on every criterion except D12, whose
single false claim is corrected in this execution rather than carried forward. The suite is green
on the merge result — 115 tests, exit 0 — and `wi/WI-0002` merges into `main` cleanly.

`EP-001` stays `open`: BUG-0001 is `ready` and WI-0003 is `draft`, so this was not the epic's last
child and the stakeholder sign-off question DE7 requires is not due yet.
