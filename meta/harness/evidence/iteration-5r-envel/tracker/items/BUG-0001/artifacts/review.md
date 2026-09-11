# Review — BUG-0001

## What I examined

- **The item's own record, in full:** `item.md` (six criteria, all ticked), `history.md` (seven rows,
  chaining `— → ready → awaiting-answer → ready → planned → in-progress → verifying → in-review`
  with no gap, the last row matching `item.md`), `journal.md` (509 lines, **seven** entries against
  seven history rows), `plan.md`, `impl-report.md`, `verify-report.md`, and `questions/Q-001.md`.
- **The diff, hunk by hunk**, at `git diff main...wi/BUG-0001` — `main` at `51a0a62`, branch head at
  `d710459`. Ten files: `envel/summary.py` (+56/−6), two test files (+124, no deletions), and seven
  files under `tracker/`. Every code hunk maps to a plan step: `left_column` to step 1, `row()`'s
  call to step 2, `balance_line` to step 3, `list_entries()`' two bracket lines to step 4, the two
  appended test classes to steps 5 and 6. The one deviation — three explicit `money.format_amount`
  calls in `row()` in place of the starred generator, because a fifth argument of a different shape
  cannot be mixed into it — is declared in `impl-report.md` `## Deviations from the plan` and is a
  *how* rather than a *what*. **Nothing in the diff serves neither a criterion nor a plan step.**
- **The nine ADRs the plan's `## Binding ADRs` section names**, for D13's completeness question, plus
  `ADR-0004`, `ADR-0005` and `ADR-0006`, which it does not name, to ask whether they are engaged.
- **Every `envel/*.py:<line>` citation in `docs/` — all 35 of them — resolved against the branch
  head**, one at a time, by printing the cited line beside the citing sentence. This is where this
  review's one finding came from, and it is the sweep `WI-0005/Q-009`'s answer performed for
  `envel/cli.py`; I repeated it for the module this item changed. Result: **one** is stale, and it is
  in the ADR this item's own `plan` wrote. Details under `## Findings`.
- **The claims audit, D12, by reading rather than by the gate.** The gate's own scope line is
  *"checked absolute claims: 0 document(s) in 0 path(s) differ from main (51a0a62) under docs"* — the
  scope is **empty**, because this branch wrote no document at all, which is correct for this change
  and is also exactly the empty-window shape F-066 warns about. So the read was done by hand over
  the documents the invalidation set names and over the sweep above, and the finding is the sweep's,
  not the gate's. Claims audited:
  - `docs/architecture/overview.md:93`, *"Amounts are printed with exactly two decimal places and no
    currency symbol"* — **holds**. **Set:** every place in `envel/` where cents become printed text.
    **Enumerated by:** `grep -n "format_amount" envel/summary.py` → 8 call sites (82, 83, 101, 102,
    103, 171, 238, 241), and `grep -rn "parse_amount\|:\.2f\|/ 100\|// 100\|% 100" envel/ --include=*.py`
    → nothing outside `money.py`. **Members:** the two this change added, at 82 and 238.
    **Falsifier:** a member building the amount string itself, which shows as a dropped trailing
    zero. I did not re-run the happy case `verify` ran; I ran the one that distinguishes them —
    `python3 -m envel entries g --month 2026-08` on a `100.01` shortfall printed `g was 100.01 short
    at the end of 2026-08`, and the whole magnitude printed `250.00`, not `250.0`. A hand-rolled
    `str(-cents / 100)` produces the first and not the second, so the example could have said no.
  - `docs/architecture/overview.md:33`, *"the only two places text and amounts meet: parse and
    format"* — **holds**. Same enumeration; **members** `money.parse_amount` (`money.py:20`) and
    `money.format_amount` (`money.py:42`), no third. **Falsifier:** a `cents // 100` outside
    `money.py`; `summary.py` is where one would have appeared, since both new helpers handle a sign,
    and the grep covers the package.
  - `docs/architecture/overview.md:31`, the `envel/summary.py` row, *"the reports, both of them"* —
    **holds**. `summarise()` and `list_entries()` are still the only two functions taking a `store`
    and a `month`; `envel/cli.py` is absent from the diff, so nothing new is dispatchable.
  - `docs/product/vision.md:73`, the v8 paragraph — **holds**, and this change is what made it true.
  - `docs/product/vision.md:48`, *"A correction that would take an envelope below zero is refused"* —
    **holds**, checked by triggering both refusals rather than by the diff's silence.
  - `ADR-0009` `## Consequences`, *"`summary` prints nothing and calls no `sys.exit`"* — **holds**.
    `grep -n "print(\|sys\.exit\|import sys" envel/summary.py` → no hit at all. **Falsifier:** a
    `print(` in the module; the two new functions are where one would have been, both existing to
    produce user-visible text.
  - `ADR-0008` `## Consequences`, *"nothing **derives** the carried-in figure from the other three"* —
    **holds**, and checked **at the boundary** rather than on a comfortable month: `left − (in −
    spent + moved)` equals `balance_before` for 2026-08 (`0`) and for 2026-09 (`-10001`, a negative
    carried-in figure, which is the case the whole bug is about).
  - `ADR-0012` `## Consequences`, *"Both surfaces are the same filtered sum bounded by a month"* —
    the **assertion holds** and its **second citation does not support it**. See `## Findings`.
- **`docs/` for a document the invalidation set does not name**, for D7's closing question: the eight
  documents outside the set, greppedded for any sentence about a printed balance, a minus, a summary
  column or a balance line — `grep -n "holds\|left \|negative\|minus\|short\|at the end of\|at the
  start of\|balance line\|summary row\|prints"` over each. `ADR-0003`, `ADR-0004` and `ADR-0005`
  returned nothing at all; `ADR-0002`, `ADR-0006`, `ADR-0007` and `ADR-0010` returned only sentences
  about stored `cents` and about entry signs, all still true and none about a printed balance.
  `ADR-0012` is the one that is not clean, and it is named below.
- **The trial merge result**, not only the branch: `git worktree add --detach`, `git merge --no-ff`,
  the suite and the lint run **inside** the worktree, then the worktree removed and `main` confirmed
  unmoved.
- **`tracker/project.yaml`** for the two commands, and `tests/` directly to settle one observation
  about where a new test class was appended.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every checkbox settled | **pass** | Six criteria, all `- [x]`; none `- [~]`, so no substitution and no wording question is owed. `grep -c "^- \[ \] AC" item.md` → 0 |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | Six rows in `## Criteria`, each with the command and its quoted output. I spot-re-ran two rather than reading them: AC1's listing and AC2's summary row reproduce exactly as quoted, and AC3's `exit=0` with 0 bytes on stderr reproduces. No row cites `impl-report.md` |
| D3 | the declared gates passed on the **final** state of the code | **pass** | Re-run by me on branch head `d710459`: `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 310 tests`, `OK`; `python3 -m compileall -q envel tests` → exit 0. And again on the **merge result** `50ff2a7`, inside the trial worktree: 310 tests `OK`, compileall exit 0 |
| D4 | no open **blocking** question | **pass** | `Q-001` is `status: answered`, `answered-by: human`. `Q-002`, filed by this execution, is `blocking: false` — nothing waits on it and `BUG-0001` closes over it by design |
| D5 | a journal entry per execution, history chains | **pass** | 7 entries, 7 history rows, in order: `review-close` (the filing), `plan`, `answer-questions`, `plan`, `implement` ×2, `verify`. No gap; the last row's `to` is `in-review`, matching `item.md` |
| D6 | every design-changing decision is in an ADR, cited from the plan or journal | **pass** | `ADR-0012` — *a balance is never printed with a minus sign; a shortfall is said in words* — cited from `plan.md` `## Decisions and ADRs`, which also records the two options rejected and why. `status: accepted`, `version: 1`, `updated-for: BUG-0001`. No decision in the diff is absent from it: the two helper shapes, the wording of both branches, the untouched sums and the kept transaction signs are all Decisions 1–5 |
| D7 | the invalidation set is disposed, updates carry a bump and a change-log row, **plus** the question the set cannot answer for itself | **pass, with a finding** | Twelve entries, twelve dispositions — see `## Invalidation set confirmation`. The one `to-update` (`overview.md` `## What is not decided yet`) is at `version: 10` with a change-log row stamped `2026-09-11T11:13:17Z`, actor `plan`, item `BUG-0001`. The two `owned-by-ending` rows were left untouched, and I confirmed independently that `plan`'s v10 edit did not reach `## Engagement state`. **The closing question is answered yes:** this change falsified `ADR-0012`, which the set does not name, for the structural reason `WI-0005/Q-009` identified. Filed as `BUG-0001/Q-002` |
| D8 | every commit on the branch references the item | **pass** | `check-commit-refs BUG-0001 wi/BUG-0001` → `all 4 commit(s) on main..wi/BUG-0001 name BUG-0001`, exit 0 |
| D9 | merged into the trunk | **pass** | Trial-merged clean at `50ff2a7` with the suite green on the result, trunk confirmed unmoved afterwards; the real merge follows this close, and its sha is recorded by `scripts/record-merge` |
| D10 | `verify` ran **after** the last code change | **pass** | `check-verify-freshness BUG-0001 wi/BUG-0001` → exit 0: *"verified at df2cf4d4; wi/BUG-0001 has moved to d710459e but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"*. Run, not assumed |
| D11 | `review.md` exists and states what was examined; every accepted gap carries an owner and an actionable disposition | **pass** | This file; `## What I examined` is first and is longer than the verdict. Two accepted gaps, both disposed — one `question-filed:`, one `no-owner` with the reason it is owed nothing |
| D12 | claims in `docs/` about the behaviour this item touched are still true | **pass, with a finding** | Eight claims audited by reading, each with its set, enumeration, members and falsifier, in `## What I examined`. Seven hold. The eighth — `ADR-0012` `## Consequences` — holds as an **assertion** and fails as a **citation**, and that is the finding. `lint-claims --context bug --changed-since main` → exit 0, over a scope its own output states as empty |
| D13 | the plan's `binding-adrs` list is **complete** | **pass** | The plan's section names nine: `ADR-0001`, `0002`, `0008`, `0009`, `0012` as binding, and `0003`, `0007`, `0010`, `0011` in the course of saying they are not — `verify` gave all nine a verdict. I asked the completeness question of the three it names nowhere. **`ADR-0004`** (invocation and shim): not engaged, nothing about invocation changed and `envel/__main__.py` is absent from the diff. **`ADR-0005`** (checks are stdlib-only): the change adds `import re` to `tests/test_entries.py`, which is the nearest thing to engagement in the diff — but `ADR-0005`'s `## Decision` is about *which commands run the checks* (`unittest discover`, `compileall`), not about what a test may import, and `re` is stdlib either way. Not engaged. **`ADR-0006`** (a spend carries the date it happened): the change reads an entry's month through the unchanged `entry_month`, and decides nothing about dating. Not engaged. No ADR is engaged and unnamed |

## Invalidation set confirmation

| document | disposition | confirmed by |
|----------|-------------|--------------|
| `docs/product/vision.md` — the v8 short-month paragraph | `verified-still-true` | Reopened at `vision.md:73`. The paragraph claims the two commands say it in words rather than printing a negative; both do. `verify` also checked the capital `G` in its quotation of the stakeholder and correctly found it is inside a quotation of them, not a claim about output — I re-read the line and agree |
| `docs/product/vision.md` — the below-zero correction refusal | `verified-still-true` | Reopened at `vision.md:48`. Confirmed by `verify` triggering both refusals in a store whose past month had closed short, with the messages quoted; the subject is the current balance and `envel/envelopes.py` is absent from the diff |
| `docs/product/vision.md` — `## Engagement state`, four bullets | `owned-by-ending` | Untouched, and untouchable by this item: `git diff main...wi/BUG-0001 --name-only -- docs/` prints nothing |
| `docs/architecture/overview.md` — *"exactly two decimal places and no currency symbol"* | `verified-still-true` | Re-audited here as a D12 claim with its own falsifier, not accepted from the disposition — see `## What I examined` |
| `docs/architecture/overview.md` — *"the only two places text and amounts meet"* | `verified-still-true` | Re-audited here, same |
| `docs/architecture/overview.md` — *"the reports, both of them"* | `verified-still-true` | Re-audited here, same |
| `docs/architecture/overview.md` — `## What is not decided yet` | `to-update`, discharged by `plan` | `version: 10`; change-log row at `overview.md:135` stamped `2026-09-11T11:13:17Z`, actor `plan`, item `BUG-0001`; `git show 51a0a62 --stat -- docs/` shows the repair landed on `main` before the branch existed. Bump and row both present, as D7 requires |
| `docs/architecture/overview.md` — `## Engagement state` | `owned-by-ending` | Untouched. Checked independently of the claim: `git show 51a0a62 -- docs/architecture/overview.md` adds only the v10 change-log row and the `## What is not decided yet` rewrite, and no `## Engagement state` line appears in that diff |
| `ADR-0008` — Decision 3's `left` row and `## Consequences` | `verified-still-true` | Re-checked as arithmetic at the boundary, not as a read — see `## What I examined` |
| `ADR-0001` — `## Consequences`, the formatter sentence | `verified-still-true` | Same enumeration and falsifier as the `## Conventions` claim |
| `ADR-0009` — `## Consequences`, *"prints nothing and calls no `sys.exit`"* | `verified-still-true` | `grep -n "print(\|sys\.exit\|import sys" envel/summary.py` → no hit. `verify` noted its own grep on the bare word `print` matched four docstring hits and that the call form leaves nothing; I ran the call form |
| `ADR-0011` — Decision 3/5, the below-zero refusal | `verified-still-true` | Both refusals triggered, quoted in `verify-report.md`; `envel/envelopes.py` absent from the diff and `tests/test_corrections.py` unmodified and green |

**Did this change falsify a document the set does not name? Yes — `ADR-0012`, and it is filed.**

I read, one by one, every one of the eight documents under `docs/` that the set does not name,
grepping each for any sentence about a printed balance, a minus, a summary column or a balance line.
Seven are clean and the grep output is in `## What I examined`. The eighth is `ADR-0012`, this
item's own ADR, and what is false in it is not an assertion but a **citation**: `## Consequences`
cites `[src: envel/summary.py:173]` as the bounded sum, and on the branch head line 173 is
`if "description" in entry:`, inside `entry_line()`. Detail and remedy: `## Findings`, and
`BUG-0001/Q-002`.

The set **could not** have named it. An invalidation set lists documents a change could make false,
and a document the item's own `plan` writes *from* that change is not one of them — which is exactly
what `WI-0005/Q-009` wrote down, and exactly what it predicted would recur: *"Every later item whose
plan cites a line its own implementation then moves will land in the same place."* It has now
happened on two consecutive items. I have not tried to repair it by adding a row to the set:
`Q-009` measured that doing so after `verify` has run fails
`lint-documents --rule invalidation-set-is-disposed`, because the set is checked against a
verification report that cannot be rewritten on a closing item.

## Sections restated at the ending

`not an ending`. `BUG-0001` is a `bug` at an item close; no `## Engagement state` section was read
for repair, and none was written. `lint-documents --rule engagement-state-is-restated --item
BUG-0001 --context bug` reports *"NOT APPLICABLE — an item close is not an ending, and the sections
are the ending's"*, and the gate is journalled as not applicable rather than as passed.

## Findings

**F1 — `ADR-0012` `## Consequences` cites a line that resolves and does not support it.** Accepted
as a gap and made dispatchable as `BUG-0001/Q-002`; **not** a send-back. The sentence is:

> Both surfaces are the same filtered sum bounded by a month [src: envel/summary.py:68]
> [src: envel/summary.py:173], and neither is touched.

At `main` (`51a0a62`), line 173 is `def bounded_balance(store, name, within):`. On the branch head it
is `    if "description" in entry:`, inside `entry_line()` — the function that renders the **signed
transaction figure**, which is the one figure `ADR-0012` `## Decision` 4 exists to distinguish from a
balance. `bounded_balance` is now at `envel/summary.py:196`. The first citation, `:68`, is still
`left = sum(...)` and still supports; it sits above this change's first insertion.

Why it is a gap and not a rejection, stated so the reasoning can be checked:
- **The assertion is true.** Both surfaces *are* the same bounded sum and neither was touched —
  `verify` measured the identity directly, and `git diff` shows `figures()`, `bounded_balance()`,
  `balance_before()` and `balance_through()` unchanged. Nothing in `docs/` says something false
  about the code; one pointer lands in the wrong place.
- **No acceptance criterion of this item is about it**, so the send-back test — *does a criterion of
  this item say the behaviour should be different?* — answers no.
- **The remedy is not a decision anybody needs to take.** `WI-0005/Q-009` settled the policy for
  this exact shape, grounded in `spec/doc-header.md` §4b: repair in place, `provenance` row in an
  append-only `## Corrections` section, change-log row, version bump. Both of §4b's conditions hold.
- **`review-close` may not make the edit.** Its licence to write under `docs/` is for a correction
  *inside this item's invalidation set*, and `ADR-0012` is not in it. The owner of a document repair
  is `answer-questions`, which is why this is a question rather than prose.

Sending the item back would mean re-opening a branch, re-running `implement` and `verify`, to move
one number in a document, for a change that is otherwise correct and fully verified. Filing the
question costs one `answer-questions` execution and the orchestrator will dispatch it on the next
pass, because an architect-addressed open question is answerable.

**F2 — `tests/test_summary.py` now defines a test class below its `if __name__ == "__main__"`
block, so one way of running that module reports `OK` over 27 of its 32 tests.** Accepted,
`no-owner`. `grep -n '__main__' tests/*.py` puts the guard at line 345 of a 401-line file, with
`class AMonthThatClosedShort` at 349 — the only module of the three with a guard where the guard is
not last. `PYTHONPATH=. python3 tests/test_summary.py` → `Ran 27 tests` / `OK`;
`python3 -m unittest tests.test_summary` → `Ran 32 tests` / `OK`. The five invisible tests include
AC2's own and AC6's clamp test, so that path gives a green that hides this bug's regression tests.

Disposed `no-owner`, and the reason is not that it is small. **That path is not a supported way to
run this project's tests and has never been one:** `python3 tests/test_summary.py` fails at
`ModuleNotFoundError: No module named 'envel'`, as does every other test module, so the guard is
vestigial in all three; and `tracker/project.yaml` declares exactly one `commands.test`, which sees
all 32 and which `verify`, the `implement` gates and my own re-run all used. Nothing is owed while
that remains true. What would change it: anyone who makes direct execution work — a `conftest`-style
path shim, a `sys.path` insert, a documented `PYTHONPATH` recipe — inherits this, and this row is
the record for them. `AC5` would not have been breached by inserting the class above the guard, so
this was avoidable rather than forced.

**Nothing else.** The diff contains no unrequested scope, no duplicated rule, no swallowed error and
no name that says something untrue. The two helpers are each a single `return` over one branch, the
branch is `cents < 0` in both, and the boundary that branch turns on is asserted from both sides.

## Accepted gaps

| gap | owner | disposition |
|-----|-------|-------------|
| **F1** — `ADR-0012` `## Consequences`' `[src: envel/summary.py:173]` resolves to `if "description" in entry:` and no longer supports the sentence. Repair to `:196` under `WI-0005/Q-009`'s settled policy: a `provenance` row in a new append-only `## Corrections` section, a `## Change log` row, and `version: 1 → 2`. `review-close` may not make this edit — its licence to write under `docs/` covers a correction inside this item's invalidation set, and `ADR-0012` is not in it | `answer-questions` | `question-filed:BUG-0001/Q-002` |
| **F2** — a test class sits below `test_summary.py`'s `__main__` guard, so `PYTHONPATH=. python3 tests/test_summary.py` reports `OK` over 27 of its 32 tests. Nothing is owed, and not because it is small: direct execution of a test module is **not a supported path in this project** and fails at `ModuleNotFoundError: No module named 'envel'` for every module, so the guard is vestigial in all three that have one; `tracker/project.yaml` declares exactly one `commands.test`, which sees all 32 and which `verify`, the `implement` gates and my own re-run all used. What would change it: anyone who makes direct execution work inherits this, and this row is their record | `none` | `no-owner` |
| **`verify`'s declared gap** — the stakeholder never saw the summary column's `short 250.00` wording, nor the opening line's `was … short at the start of`; `plan` recorded both as assumptions *not under delegation*. `human` owns the approval, but it is not `BUG-0001`'s to obtain and filing a question here would ask them the same thing twice: `EP-001`'s sign-off must name every answer spent under delegation, and that is where printed prose reaches them. `plan`'s `## Risks` says so, `verify` put it in `## Not verified, and why`, and this is the third place it is written so the ending cannot miss it | `none` | `no-owner` |
| **`verify`'s declared gap** — `ADR-0012`'s rule binds three call sites and nothing enforces it; a future report printing a bounded balance without `balance_line` or `left_column` reintroduces this bug with no failing test. All three existing call sites are confirmed, so no work is outstanding on any current code path, and enforcing it mechanically would be a new decision rather than a gap in this change. Named in `ADR-0012` `## Risks` | `none` | `no-owner` |

`verify`'s remaining two declared gaps — the step-7 store probe, and nothing checked on a second
machine or across a restart — are examined and accepted with nothing owed: AC2 *names* the probe, so
making it is what verifying AC2 means, and no criterion of this item names a restart or a second
machine, so no criterion is `substituted` and no wording question is due.

## Verdict

**Accepted, and merged. `BUG-0001` closes as `delivered`.**

The change does what the stakeholder asked for at `Q-001` and nothing else: a month that closed
short says so in words, the figure stays readable, and the arithmetic behind it is untouched — which
I checked at the boundary and by introducing the clamp the criterion forbids, not by reading that it
was absent. Six criteria, each with a command behind it. The record chains, every execution has an
entry, and the verification postdates the last code change.

Two gaps accepted rather than sent back, both disposed, one of them dispatchable as a question that
will fall due on the next orchestrator pass. The one that matters is not in the code: it is a
citation in this item's own ADR that now points at the wrong line — the second occurrence in two
consecutive items of a defect whose policy was settled at `WI-0005/Q-009` and whose recurrence that
answer predicted in writing. The policy holds; what the engagement should take from the recurrence
is that `path:line` as a citation form has now cost three reviews, which `Q-009` sent to the
retrospective and which `Q-002` records with a count.

One thing the epic's ending should carry, and it is not a defect of this item: `EP-001`'s success
measure is *"No envelope ever shows a negative amount"*, unqualified, while `ADR-0012` draws a
distinction the measure does not — a balance is worded, a transaction figure keeps its sign. After
this change a reader of `envel summary` can still see `moved -100.00`, and of `envel entries` a
spend's `-250.00`. The stakeholder chose that with the entry line printed verbatim in front of them,
so nothing here is wrong; but whoever closes `EP-001` should say it in those terms rather than let
the measure read as unqualified. `verify` raised it, and this review carries it forward.
