# Review — WI-0002

## What I examined

- **The record, in full.** `item.md`; `history.md` (six rows, `— → draft → ready → planned →
  in-progress → verifying → in-review`, chaining without a gap, last row matching the item's
  status); `journal.md` read end to end (seven entries — `intake`, `answer-questions`, `refine`,
  `plan`, two `implement`, `verify`); `plan.md`; `impl-report.md`; `verify-report.md`. WI-0002 has
  no questions of its own; the decisions it inherited come from `EP-001/Q-002` and
  `WI-0001/Q-001`, both `answered`.
- **The diff, hunk by hunk**, over `main..wi/WI-0002` (`git diff main..wi/WI-0002 --stat`, then
  the code, docs and tests separately). Each hunk mapped to a plan step below.
- **`docs/architecture/adr/ADR-0005`** in full, against `expenses/settle.py`, to check the code
  implements the decision rather than something adjacent to it.
- **The trial merge**, and the suite on the merge result — not on the branch.

### D12 — the claims, checked from their citations

Each absolute claim this item wrote or rewrote in `docs/` or `README.md` is listed with the thing
I opened to decide it. In no case did I decide from the sentence, from a neighbouring document,
or from the report that wrote it.

| claim | where | what I opened | verdict |
|---|---|---|---|
| "the layering is one-way: `cli.py` depends on `store.py`, `money.py` and `settle.py`, `store.py` depends on `money.py`, `settle.py` depends on neither of them, and nothing below `cli.py` imports `cli.py` or prints anything" | `overview.md` v3 | the import block of every file in `expenses/`, and `grep -rn "print(" expenses/` excluding `cli.py` | **true.** `settle.py` has no `import` statement at all; `store.py` imports only `json`, `os`, `pathlib`, `tempfile` and `expenses.money`; `cli.py` imports `settle` and `store`; the `print(` search outside `cli.py` returns nothing |
| "`positions()` gives each recorded person their net … and `settlement()` … matching the largest debt against the largest credit, breaking ties on the order people were recorded" | `overview.md` v3 | `ADR-0005` §Decision steps 1–5, then `expenses/settle.py` | **true.** The `max(pool, key=lambda entry: (entry[1], -recorded[entry[0]]))` is exactly ADR-0005 step 4 — largest amount, and among equal amounts the smaller recorded index |
| "It takes the dataset dictionary and returns plain data: no file, no print, no import of `store.py` or `cli.py`" | `overview.md` v3 | `expenses/settle.py`, all 60 lines | **true**, and stronger than claimed: it imports nothing whatsoever |
| "That is what lets every figure in the settlement be tested without touching a disk" | `overview.md` v3 | `tests/test_settle.py` | **true.** Its datasets are literals built by a local `dataset()` helper; there is no `tempfile`, no `pathlib`, no store |
| "`argparse` subcommands under two nouns … plus a third top-level command `settle` which takes no arguments" | `overview.md` v3 | `build_parser()` in `expenses/cli.py`, lines 48–54 | **true.** `commands.add_parser("settle", …)` followed by `set_defaults(action=None)` and no `add_argument` |
| "It does not move money: `settle` prints the payments and records nothing" | `overview.md` v3 | `settle_report` in `cli.py`, and `main()`'s handler dispatch | **true.** The handler calls `store.load` and `format_amount` and nothing else; `store.save` is the only writer in the project and is not on this path |
| "**`settle` only tells you.** It records nothing, marks nothing as paid, and leaves your data file exactly as it was" | `README.md` | the same handler, plus `verify-report.md`'s md5 evidence which I re-derived by reading the code path | **true** |
| "every success writes to stdout and exits 0; every refusal writes to stderr … and exits non-zero" — a **pre-existing** claim the new command has to keep true | `overview.md` | `main()` in `cli.py` | **still true.** `settle` returns through the same `try/except ExpensesError` that every other handler does, so a corrupt store refuses through the common path rather than a new one. This is the D12 case that matters: the claim was written for WI-0001 and nobody was obliged to recheck it, and adding a command is exactly what could have falsified it |

`scripts/lint-claims --changed-since main` → `checked 1 document(s)`, `0 errors, 0 warnings`,
exit 0. That proves the citations resolve; the table above is the part it cannot do.

### The diff, mapped

| hunk | plan step | serves |
|---|---|---|
| `expenses/settle.py` (new, 60 lines, `positions` + `settlement`) | 1, 2 | AC3's arithmetic and AC1/AC3/AC4's pairing and order |
| `expenses/cli.py` — `settle` subparser, `settle_report`, `HANDLERS[("settle", None)]`, `settle` added to the import | 3 | AC1, AC2, AC5 |
| `tests/test_settle.py` (new, 162 lines) | 4 | the criteria at the function level |
| `tests/test_cli.py` — `SettleTestCase` and six AC-named classes | 5 | AC1–AC6 end to end |
| `README.md` — the `### settle` section, and the opening paragraph that said who-owes-whom was not in this version | 6 | AC6 |
| `docs/architecture/overview.md` v2 → v3 | 7 | D7 |
| `tracker/` | — | the record |

No hunk serves neither a criterion nor a plan step. Every deletion is in the two paragraphs that
said this behaviour did not exist yet.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | Every acceptance criterion checkbox ticked | **pass** | AC1–AC6 all `- [x]` in `item.md`; `validate-workspace` exit 0 |
| D2 | Every ticked criterion cites its evidence in `verify-report.md` | **pass** | Six rows in `## Criteria`, each with the command `verify` ran and its actual output — including `cat -A` for AC1's "exactly two lines", three separate stores for AC2, and a `cmp` for AC4. AC3's five properties are cited against positions `verify` recomputed from the raw stored JSON rather than from `expenses/settle.py`, which is what makes them capable of failing |
| D3 | Gates passed on the **final** state of the code | **pass** | `impl-report.md`'s gates ran at `b873060`; `verify` ran at `6b2fb40`; `git diff --name-only b873060..HEAD` returns only `tracker/` paths, so both postdate the last code change. I re-ran `python3 -m unittest discover -s tests -t .` myself on the merge result: `Ran 86 tests`, `OK` |
| D4 | No open blocking question | **pass** | `tracker/items/WI-0002/questions/` does not exist; no question anywhere in the workspace is `open` |
| D5 | A journal entry per execution; history chains | **pass** | Six history rows, seven journal entries — the extra being `answer-questions` at `draft → draft`, an execution that changed no status and correctly still journalled. Every row has its entry; the last row is `verifying → in-review` and `item.md` said `in-review` |
| D6 | Every design decision in an ADR, cited from plan or journal | **pass** | One decision was taken on this item — which settlement to print and in what order — and it is `ADR-0005`, cited from `plan.md` `## Decisions and ADRs`, from `overview.md` v3, from `README.md` and from `settle.py`'s own docstring. The three decisions `plan` did *not* make into ADRs are each listed in the same table with the document they were answered from, so the absence is accounted for rather than silent |
| D7 | Invalidated documents updated, with a version bump and change-log row | **pass** | `docs/architecture/overview.md` v2 → v3 with a change-log row dated `2026-08-27T00:35:17Z` by `implement` for WI-0002; the "What is coming" paragraph describing `settle.py` as unbuilt is gone, and the module is in the diagram, in the layering sentence and in a piece of its own. `README.md`'s opening paragraph no longer says who-owes-whom is out of this version. No other document made a claim this change falsified — checked in the D12 table |
| D8 | Every commit references the item ID | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → `all 7 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0 |
| D9 | Merged into the trunk | **pass** | Merged after this review was written and after the item was closed, in the order the procedure requires — `check-commit-refs` inspects the not-yet-merged range, so merging first would have made the gate refuse the close it gates. Trial merge into a throwaway branch off `main` first: clean, `Ran 86 tests`, `OK`, then discarded |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0002 wi/WI-0002` → *"verified at 6b2fb409; wi/WI-0002 has moved to 04e662c2 but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"*, exit 0. Run, not assumed |
| D11 | `review.md` exists and states what was examined | **pass** | This file; `## What I examined` is its first section |
| D12 | Claims in `docs/` about the touched behaviour still true; absolute claims carry a resolvable citation | **pass** | The eight-row table above, each row decided by opening the cited code. `lint-claims --changed-since main` → 0 errors, 0 warnings |

## Findings

**None blocking.** Two observations, recorded because they are the kind of thing that is invisible
once an item is closed:

1. **`tests/test_settle.py`'s datasets hard-code shares that `store.py` computes.** `AC3`'s third
   expense is written as `[("Ana", 334), ("Ben", 333), ("Cara", 333)]` — the split ADR-0003's
   remainder rule produces today. If that rule ever changed, these literals would keep passing
   while describing a dataset the tool no longer writes. Not a defect and not worth a follow-up
   item: `tests/test_cli.py` builds the same five-person dataset with the real commands and
   asserts the same three output lines, so the end-to-end tests are the anchor and would fail
   first. I confirmed the literals match reality today by reading the stored JSON of a dataset
   built with the delivered commands: `{'Ana': 334, 'Ben': 333, 'Cara': 333}`.
2. **AC1's end-to-end test cannot see ADR-0005's tie-break**, because AC1 compares *sorted*
   stdout. `verify` found this by mutation — reversing the tie-break left
   `WI0002AC1SettleListsThePayments` green — and recorded it as a qualification rather than
   burying it. It is correct as it stands and I am not sending it back for it, but it is a real
   fact about which test is load-bearing, so it is carried into the item's `## Notes` rather than
   left in a verification report nobody will open again.

Nothing in the change contradicts an ADR. `settle.py`'s `max(pool, key=(amount, -recorded_index))`
is ADR-0005 step 4 exactly, and its worked examples — `Ben` before `Cara` on the AC1 dataset,
`Cara`/`Dan`/`Ben` on the AC3 dataset — are the output the delivered command actually produces.

## Accepted gaps

Each of these is declared in `verify-report.md` `## Not verified, and why` or `impl-report.md`
`## What I did not do`. All are accepted, and each is written into the item's `## Notes` so that
it survives the close.

| gap | why it is acceptable |
|---|---|
| **Lint checked nothing.** `commands.lint` is null | ADR-0004 is the record: the project installs nothing and the standard library ships no linter. Both `implement` and `verify` reported the gate as `skipped`, not as a pass, which is the behaviour the contract asks for. The cost is real and is now recorded on the item |
| **No test covers a dataset whose positions do not sum to zero**, though `settlement()`'s docstring claims it terminates on one | No delivered command can produce that state — `add_expense` refuses an unknown name and nothing deletes a person — so a test would need a hand-written file the tool would never write. `plan.md`'s third assumption declares it. It is an untested claim in a docstring and `review-close` should not read it as evidence, which is precisely what `verify` said |
| **`positions()` silently drops a name in an expense but absent from `data["people"]`** | Unreachable today, and named in three places — `plan.md` `## Risks`, `impl-report.md` `## What I did not do`, `verify-report.md` `## Defects found` — as WI-0004's to solve. Carried into `## Notes` so WI-0004's refinement meets it in this item's record too |
| **Scale is unexercised** | The item's `## Deliberately unconstrained` section says no threshold was ever set, by `refine`, deliberately. There is nothing to check against, and inventing one at review time would be a criterion nobody agreed |
| **The multi-creditor tie-break is not covered by any acceptance criterion** | AC1's and AC3's datasets each have exactly one creditor. `test_settle.py::test_two_creditors_are_paid_largest_credit_first` covers it and passes, but it is a test the implementation chose to write, not a criterion. Accepted: the rule is recorded in ADR-0005 and tested, just not AC-level. Carried into `## Notes` |

## Verdict

**Accept, merge, close as `delivered`.** All twelve Definition of Done criteria pass, each with
its own evidence. The change does what WI-0002 asked, in the way `plan` designed and ADR-0005
recorded; the trial merge into `main` was clean and its 86 tests green; and the record answers,
from the tracker, `docs/` and `git log` alone, what was built, who decided what, what was asked of
the stakeholder and what verification found. Five gaps are accepted and every one is now on the
item rather than only in a report.
