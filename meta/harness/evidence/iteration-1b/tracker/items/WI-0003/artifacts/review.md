# Review — WI-0003

## What I examined

- The full diff `main..wi/WI-0003` for `expenses/` — 90 changed lines across two modules — hunk by
  hunk, and the 200 lines of test added, read for what they assert rather than whether they pass.
- `item.md` (AC1–AC12, all ticked), `history.md` (eight rows), `journal.md` (six entries, read in
  full), `plan.md`, `impl-report.md`, `verify-report.md`, `refinement-qa.md`, and the one question
  with its `## Consequences`.
- `ADR-0003`, `ADR-0004`, `ADR-0005`, `ADR-0006`, `ADR-0007`, `docs/architecture/overview.md`
  (v3), read against the code for D12 — in particular `ADR-0004`'s three promises and its
  tie-break wording.
- Commands run during this review: `check-verify-freshness`, `check-commit-refs`,
  `validate-workspace`, a trial merge into a **detached** throwaway worktree with the project's
  test and lint commands on the merge result, and a re-run of the criteria's four worked examples.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every criterion checkbox ticked | **pass** | `grep -c '^- \[ \]' item.md` → 0; twelve `- [x] AC` |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | twelve rows, each naming a command and captured output. I re-ran AC4, AC5 and AC6 here and got the same three outputs |
| D3 | all declared gates passed on the **final** state of the code | **pass** | I ran the test command (exit 0, 96 tests) and the lint command (exit 0) at `7986250`, and again on the trial merge result |
| D4 | no open blocking question | **pass** | `Q-001` is `answered`, with `## Consequences` naming `ADR-0004`, `prd.md`, `vision.md` and four items |
| D5 | a journal entry per execution; history chains without a gap | **pass** | eight rows chain from `— → draft` to `verifying → in-review`, last row matches the item's status; six journal entries for six executions (`intake` and `implement` each produced two rows from one execution) |
| D6 | every design decision is in an ADR cited from the plan or journal | **pass, and the interesting case is a deliberate non-ADR** | `plan.md` § *Decisions and ADRs* cites five existing ADRs and records, with its reasoning, that **no new ADR was written**: the one consequential decision — which valid settlement is printed — was made by `refine` in the criteria, and duplicating it in an ADR would leave two documents with no way to tell which governs. Instead `overview.md` v3's decisions table gained a row pointing at the criteria. That is a real answer to D6, not an evasion |
| D7 | documents this change invalidated were updated, with a version bump and a change-log row | **pass** | `overview.md` v2 → v3 with a change-log row: `group.py` now owns net positions and the settlement, and the new decisions row. `prd.md` needed nothing: its description of what the tool derives already matched |
| D8 | every commit references the item ID | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → exit 0, three commits, run **before** the merge |
| D9 | merged into the trunk | **pass** | merged after this review and after the close — see § *Verdict* |
| D10 | verification postdates the last code change | **pass** | `check-verify-freshness` → exit 0: verified at `f6b37ed8`, branch at `79862502`, "only the record changed". Confirmed independently: `git diff --name-only f6b37ed..wi/WI-0003 -- expenses tests` is empty |
| D11 | the review record states what was examined | **pass** | this document, § *What I examined* |
| D12 | every claim in `docs/` about the behaviour this item touched is still true | **pass, with one clarification** | `ADR-0004`'s three promises are each borne out — `verify` checked them over 407 records, and I re-derived the `n - 1` argument against the loop: `amount = min(-debt, credit)` guarantees one of the two positions reaches zero, and both are deleted when they do. `ADR-0003` point 6 holds: `_who_owes_whom` calls `load` and never `save`, which I confirmed by reading its eleven lines. The clarification is Finding 1 |

## Findings

**1 — `ADR-0004` says ties are broken "by the person's name"; the code compares identity keys.**
This is not a contradiction and needs no question: `refine` recorded the choice in
`refinement-qa.md` Q4 and pinned it in the criteria, on the grounds that comparing raw spellings
would make the output depend on who typed a capital letter — the same reasoning `ADR-0005` already
applies to identity. The ADR is simply less specific than the code, which is the safe direction.
Recorded so a future reader comparing the two does not conclude they have found a defect.

**2 — a hand-edited record can make the tool announce that everybody is settled when somebody is
not.** `verify` probed it and quoted the output: with a record whose positions sum to `-100`
(`Alice 0, Bob -100`), `who-owes-whom` prints `Everybody is settled up.` and exits `0`. This is
worse-sounding than what `plan.md` § *Risks* predicted ("a short, wrong settlement"), and it is
accepted rather than sent back for three reasons: no criterion covers it; the tool cannot produce
such a record itself, because `shares_of` sums to each expense's total; and `plan.md` explicitly
forbids `implement` from adding a guard on its own initiative, which it correctly did not. It is
now in `## Notes` with its actual output, so the next person to consider a validity check finds
what it would be worth.

**3 — two test-coverage gaps, both in correct code, neither a send-back.** `verify` found them by
mutation and confirmed the mechanism of the second directly:
- `net_positions`' ordering is documented in `plan.md` § *Assumptions* 1 as a contract — everybody,
  in the order added — and nothing asserts it. Sorting the result by amount passes the whole suite.
- `test_the_record_is_not_modified` (AC10) uses a record with **one** expense, so a rewrite that
  merely reorders the expenses list is invisible to it. `verify` showed the same mutation does
  change the bytes on a two-expense record.

I considered rejecting on the second, since a test that cannot fail is a maintenance liability.
Against it: AC10's assertion is correct and the behaviour is correct; the weakness is in a fixture,
not in the item's contract; and a rejection would cost a full round trip to strengthen coverage of
something no criterion requires. Both are accepted with an owner named — **WI-0004 extends
`net_positions` and adds a third record-writing command, so both gaps land naturally in its
refinement and plan.**

**4 — this loop's failure mode is a hang, not a wrong answer.** `verify` found that rounding the
transfer amount down to 10p makes the suite never finish, because the loop can no longer reduce a
position below the rounding step. That is a caught mutation and not a defect, but it is worth a
line in the record: anyone changing how `amount` is computed should know that getting it wrong may
not produce a failing test so much as a test run that never ends.

**Nothing else.** Every hunk traces to a plan step and a criterion. The three deviations
`impl-report.md` declares are each justified, and the first — the loop-termination guard — was the
right call and was declared at exactly the right level of detail: the plan forbade a guard that
*reports or refuses*, and this one neither reports nor refuses, it just stops. No hunk contradicts
an ADR. Nothing anticipates WI-0004.

## Accepted gaps

Each is written into `item.md` § `## Notes` as well.

| gap | why it is acceptable | where it lands |
|-----|----------------------|----------------|
| A hand-edited record whose positions do not sum to zero prints `Everybody is settled up.` — Finding 2 | no criterion covers it; the tool cannot write such a record; `plan.md` forbade guarding it here | `item.md` § Notes, with the actual output |
| `net_positions`' documented ordering is unasserted — Finding 3 | an internal contract, not a criterion; correct today | `item.md` § Notes, named for **WI-0004**, which extends the function |
| AC10's fixture holds one expense — Finding 3 | the criterion is satisfied and the code is right; the fixture is too small to catch a reordering rewrite | `item.md` § Notes, named for **WI-0004**, which adds another writing command |
| The `n - 1` bound is checked empirically, not proved | 407 records is strong evidence and `ADR-0004`'s argument is sound; I re-derived it against the loop during D12 | `verify-report.md` § *Not verified* |
| Provable minimality is not checked, and the settlement is sometimes larger than a human would find | `ADR-0004` explicitly does not promise it and the item excludes it | `ADR-0004`; `item.md` § Out of scope |
| `lint-clean` is a syntax check, not a linter | `ADR-0008`; a standing project condition | `ADR-0008`; `WI-0001/item.md` § Notes |

## Verdict

**Accept, close, and merge.** All twelve Definition of Done criteria pass. The trial merge into a
detached throwaway worktree of `main` was clean and `python3 -m unittest discover -s tests -t . -q`
passed on the merge result (96 tests, exit 0), as did lint; the trial was discarded and `main` was
confirmed still at `ea5b447`. The item was closed while `wi/WI-0003` was still unmerged, so
`check-commit-refs` had a non-empty range, and only then was the branch merged.

Four findings, none blocking. The two that matter are handed to WI-0004 by name, because that item
touches exactly the code they concern.
