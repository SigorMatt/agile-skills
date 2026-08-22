# Review — WI-0004

## What I examined

- The full diff `main..wi/WI-0004` for `expenses/` — 116 changed lines across three modules —
  hunk by hunk, and the 315 lines of test added or changed.
- `item.md` (AC1–AC15, all ticked), `history.md` (six rows), `journal.md` (five entries, read in
  full), `plan.md`, `impl-report.md`, `verify-report.md`, `refinement-qa.md`. The `questions/`
  directory is empty and always has been.
- `ADR-0003`, `ADR-0005`, `ADR-0006`, `ADR-0007`, `ADR-0010`, `ADR-0011`, `overview.md` (v4),
  `prd.md` (v2), `vision.md` (v3), and **`EP-001/item.md`** — its four success measures, because
  this is the epic's last child.
- **The epic's four success measures, each run end to end as a user would**, not read.
- `WI-0002/item.md` and `WI-0003/item.md` `## Notes` — to check the three gaps they handed here
  were actually closed, which is the one thing only a reviewer standing at the end can check.
- Commands run during this review: `check-verify-freshness`, `check-commit-refs`,
  `validate-workspace`, a trial merge into a **detached** throwaway worktree with tests and lint
  on the merge result, and the epic-measure run below.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every criterion checkbox ticked | **pass** | `grep -c '^- \[ \]' item.md` → 0; fifteen `- [x] AC` |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | fifteen rows, each naming a command and captured output. I re-ran AC5's before-and-after and AC8's overpayment here and got the same output |
| D3 | all declared gates passed on the **final** state of the code | **pass** | I ran the test command (exit 0, 115 tests) and lint (exit 0) at `a0b7f29`, and again on the trial merge result |
| D4 | no open blocking question | **pass** | this item has never had a question; the answer that created it is `EP-001/Q-001`, answered and propagated |
| D5 | a journal entry per execution; history chains without a gap | **pass** | six rows chain from `— → draft` to `verifying → in-review`, last row matches the item's status; five journal entries for five executions (`implement` produced two rows from one) |
| D6 | every design decision is in an ADR cited from the plan or journal | **pass** | `ADR-0011` is new and is cited in `plan.md` § *Decisions and ADRs* and in the `plan` journal entry; six earlier ADRs are cited rather than re-decided; three choices are `## Assumptions` with reversal costs |
| D7 | documents this change invalidated were updated, with a version bump and a change-log row | **pass** | `overview.md` v3 → v4 with a change-log row: payments in `group.py`, the standing rule that every balance goes through `net_positions`, and "what is not here yet" replaced by the complete record. `prd.md` needed nothing — its four kinds of fact are now all built, exactly as it describes them |
| D8 | every commit references the item ID | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → exit 0, three commits, run **before** the merge |
| D9 | merged into the trunk | **pass** | merged after this review and after the close — see § *Verdict* |
| D10 | verification postdates the last code change | **pass** | `check-verify-freshness` → exit 0: verified at `f3be13cb`, branch at `a0b7f292`, "only the record changed". Independently: `git diff --name-only f3be13c..wi/WI-0004 -- expenses tests` is empty |
| D11 | the review record states what was examined | **pass** | this document, § *What I examined* |
| D12 | every claim in `docs/` about the behaviour this item touched is still true | **pass, with one finding** | `ADR-0011` point 1's shape checked against a real record file, field by field; point 2 checked by reading `net_positions` — the fold is there and it is the only place; point 4 (a payment is never shown as an expense) checked by running both listings. The finding is D12-adjacent and is Finding 2 below, on `EP-001`'s own scope wording |

## Epic Definition of Done — EP-001

WI-0004 is the last child, so `spec/dor-dod.md` §4 applies. Every measure below was **run**, not
read; the transcript is in the journal entry on the epic.

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| DE1 | every child item is `done` | **pass** | WI-0001, WI-0002, WI-0003 are `done` and merged; WI-0004 is closed by this execution |
| DE2 | every child's `outcome` is recorded | **pass** | all four `outcome: delivered`; none was dropped |
| DE3 | each success measure addressed — met, or explicitly not met with the reason | **pass, all four met** | see the table below |
| DE4 | `docs/product/` reflects what was actually built | **pass, with Finding 2** | `vision.md` (v3) and `prd.md` (v2) describe four kinds of fact, seven subcommands, one file, one currency, no network — all of which is what exists. The one discrepancy is in the **epic's own** `## Out of scope`, not in `docs/product/`; recorded as Finding 2 |

### The four success measures, run

| measure | verdict | what I ran and saw |
|---------|---------|--------------------|
| Add three people, record two expenses, exit, start again, see balances accounting for both, with no re-entry | **met** | eight separate `python3 -m expenses` processes. The seventh printed both expenses with their shares; the eighth printed `Carol pays Alice 16.00` and `Bob pays Alice 4.00`. Nothing was re-entered |
| `who-owes-whom` prints a debtor, a creditor and an amount for every person with a non-zero position, such that the amounts settle every recorded expense | **met** | net positions were `Alice 20.00, Bob -4.00, Carol -16.00`; applying the two printed transfers left all three at `0.00`; every non-zero person appeared in the output |
| After a payment, the debt it covered is no longer reported; when payments cover every debt, the tool says everybody is settled up | **met** | `add-payment 4 --from Bob --to Alice` → `who-owes-whom` printed only `Carol pays Alice 16.00`, Bob's line gone and Carol's untouched. After `add-payment 16 --from Carol --to Alice` → `Everybody is settled up.` |
| Runs on stock CPython 3 with no third-party packages and no network access | **met** | `python3 -c "import expenses"` succeeds on CPython 3.12.3. Every import in the package is `json`, `os`, `pathlib`, `sys`, `tempfile` or an internal module — no third-party name anywhere. No `socket`, `urllib`, `http`, `requests`, `subprocess` or `asyncio` in the shipped package. And, run rather than reasoned: I replaced `socket.socket` with a class that raises, then ran **all seven subcommands** — every one exited `0`, so none opened a socket |

## Findings

**1 — the `payments` shape check is unasserted, and this is the third instance of one pattern.**
`verify` found it: deleting `storage._is_payment`'s use entirely passes all 115 tests, because
nothing feeds the tool a corrupt `payments` key. `ADR-0011` point 5 and `plan.md` step 1 both
require the check, and the code implements it correctly — `verify` fed it four malformed records
by hand and each was refused with the right message and left the file untouched.

What makes this worth more than a line is that `verify` named the pattern, correctly: **a plan
step with no criterion behind it is the thing that keeps producing these.** All three gaps this
item inherited had the same shape, and so does this one. Recorded in the item's `## Notes` and,
because it is a methodology observation rather than a code defect, restated in the epic's journal
where a reader of the whole epic will find it.

**2 — `EP-001`'s `## Out of scope` implies an expense may carry a description, and none does.**
The epic excludes "Receipts, attachments, photographs, or free-text expense history **beyond a
description**", which reads as though a description is inside the scope. Nothing was built:
`prd.md` (v2) § *The facts the tool holds* enumerates an expense as an amount, one payer and one
or more sharers and says "Nothing else", and WI-0002's refinement excluded a description citing
exactly that. So the product is coherent and the PRD governs — but the epic's own wording points
the other way, and a reader starting at the epic would expect a field that does not exist.

I am not treating this as an unmet success measure: none of the four mentions a description, and
all four are met. It is recorded here, in the epic's journal and in WI-0002's already-recorded
scope exclusion, as the one place the record contradicts itself. **It is also the single most
likely thing the human will ask for first**, which is worth knowing.

**3 — the diff is smaller than the item.** Four lines of arithmetic in `net_positions`, two
handlers, one shape check. `who-owes-whom`, `settle` and `shares_of` have an empty diff, which
was `plan.md`'s central claim and is the strongest evidence in this epic that `ADR-0011` point 2
was the right call: payments were added to a settlement algorithm without touching it.

**Nothing else.** Every hunk traces to a plan step and a criterion. The three deviations
`impl-report.md` declares are each justified — in particular `RefusalLeavesNoFileTest` being a
plain `TestCase`, which is forced by the criterion it serves and is explained in its docstring.
No hunk contradicts an ADR.

## Accepted gaps

Each is written into `item.md` § `## Notes` as well.

| gap | why it is acceptable | where it lands |
|-----|----------------------|----------------|
| The `payments` shape check is unasserted — Finding 1 | the code is correct and was probed; no criterion requires it; the fix is one test and the epic is closing | `item.md` § Notes; the pattern is in the epic's journal |
| A duplicate payment is indistinguishable from two real ones | inherent in the model — `ADR-0011` § *Consequences* — and no criterion covers it | `item.md` § Notes; `ADR-0011` |
| A hand-edited record can name somebody outside the group in a payment, and it is printed | same as for expenses (WI-0003 recorded it); the tool cannot write such a record | `item.md` § Notes |
| Atomicity of the write is argued, not demonstrated | unchanged since WI-0001; the consequence that matters was demonstrated again on four malformed files | `WI-0001/item.md` § Notes |
| `lint-clean` is a syntax check, not a linter | `ADR-0008`, a standing project condition; roughly 700 lines of Python shipped in this epic with review as the only style check | `ADR-0008`; `WI-0001/item.md` § Notes |
| The epic's scope wording implies a description field — Finding 2 | the PRD governs and is explicit; no success measure turns on it | `item.md` § Notes; the epic's journal |

## Verdict

**Accept, close, merge — and close the epic.** All twelve Definition of Done criteria pass, and
all four of the epic's success measures were demonstrated by running them. The trial merge into a
detached throwaway worktree of `main` was clean, 115 tests passed on the merge result, the trial
was discarded and `main` confirmed still at `fbc6085`. The item was closed while `wi/WI-0004` was
unmerged so `check-commit-refs` had a non-empty range, and only then was the branch merged.

Three findings, none blocking. The one worth carrying past this epic is not about the code: three
of the four gaps recorded across these four reviews arrived by the same route — a plan step or an
ADR clause with no acceptance criterion behind it — and nothing in the pipeline catches that
class. That belongs in the epic's record, and it is there.
