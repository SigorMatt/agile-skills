# Review — WI-0004

This item has been reviewed twice. The first review, at `e50dc4f`, **rejected** it on Definition
of Done D7 and D12. That review is kept in full as an appendix at the end of this file, including
its correction about a trial merge that briefly advanced `main`. This is the second review, of
`2c96f8e`, and it is a close.

## What I examined

- `tracker/items/WI-0004/item.md` — the eight criteria (all `[x]`, none `[ ]`), `## Out of scope`,
  D1–D4, and the `## Notes` this review added at close.
- `tracker/items/WI-0004/history.md` — eleven rows, read as a chain: every `from` equals the
  previous `to`, the first is `—`, and the last row's `to` (`in-review`) matched `item.md` when
  this review began.
- `tracker/items/WI-0004/journal.md` — **read in full**, all thirteen entries. Eleven correspond
  one-to-one with the eleven history rows; the two extra are declared non-transition entries and
  say so in their `**Trigger:**` (the first review's correction at 01:28:17Z, and `implement`'s
  opening entry at 01:32:04Z on the send-back resumption). More entries than rows is legal; fewer
  would be the `journal.execution.missing` finding.
- `tracker/items/WI-0004/questions/Q-001.md` — `status: answered`, `addressed-to: human`,
  `answered-by: human`, with `## Consequences` naming `refinement-qa.md` and `item.md`; both
  exist and both carry the answer.
- `tracker/items/WI-0004/artifacts/plan.md` (`## Approach`, all eleven steps, the AC mapping, the
  four assumptions, `## Decisions and ADRs`, `## Risks`), `impl-report.md` (rounds 1 and 2),
  `verify-report.md` (this round's, and the first as its appendix).
- **The diff, hunk by hunk, not a description of it**: `git diff main..wi/WI-0004 -- expenses/`
  read in full; `-- tests/` read as its class and method list plus the single deleted line;
  `-- README.md` read as its complete +/- set.
- `docs/architecture/overview.md` v5, `docs/product/vision.md`,
  `docs/architecture/adr/ADR-0006-…md`, `ADR-0007-…md`, `tracker/project.yaml`,
  `tracker/items/EP-001/questions/Q-001.md`.
- A **detached** trial merge (`git worktree add --detach /tmp/trial5 main`) with the suite run on
  the merge result — see D9 and finding F4.

### The D12 claim audit — what I opened for each claim

Every claim below was decided by opening the thing it cites and reading that. Where the previous
review had audited the same claim, it was re-opened rather than carried over: re-quoting an
earlier verdict is the exact failure D12 exists to catch, and this item has already produced one
instance of it.

| claim | cited | what I opened | verdict |
|-------|-------|---------------|---------|
| `overview.md` v5: "WI-0004 added three module-level functions here — `naming_expenses`, `delete_person` and `delete_expense`" | `expenses/store.py` | `grep -n "^def " expenses/store.py` → eleven functions, of which those three are at 126, 145 and 162; `git diff main..wi/WI-0004 -- expenses/store.py` adds exactly them | **true** |
| `overview.md` v5: `naming_expenses` "reports every stored expense that names a given person, as `paid_by`, in `shared_by`, or as a key of `shares_minor`" | `expenses/store.py` | `store.py:135-141` — the three-way `or` over `enumerate(data["expenses"], start=1)` | **true** |
| `overview.md` v5: `delete_person` "refuses while any expense still names the person and says how many do" | `ADR-0007`, `WI-0004 AC3` | `store.py:151-155`, and AC3's text in `item.md` | **true** |
| `overview.md` v5: "Nothing was added to `load`" | `ADR-0007` | ADR-0007's `## Decision` says it; then `git diff main..wi/WI-0004 -- expenses/store.py`, which is a single hunk at `@@ -121,3 +121,47 @@` with **zero** deleted lines — `load` is at line 33 and untouched | **true** |
| `overview.md` v5: "`VERSION` is still 1" | `ADR-0006`, `expenses/store.py` | `expenses/store.py:15` → `VERSION = 1`; ADR-0006's Decision says the shape does not change | **true** |
| `overview.md` v5: "Each noun has three actions: `add`, `list` and `delete`" | `expenses/cli.py` | `cli.py:32,34,35` (person add/list/delete) and `:42,53,54` (expense add/list/delete), plus the four `HANDLERS` keys under those two nouns | **true** |
| `overview.md` v5: "`expense list` prints that position as its leading column" and "after a deletion the remaining expenses renumber" | `ADR-0006`, `WI-0004 AC2` | `cli.py:139-147` — `"%d  %s  %s  paid by %s  shared by %s" % (position, …)` over `enumerate(recorded, start=1)`; and `store.py:162-166` — `recorded.pop(number - 1)` on the stored list, which the listing re-enumerates each time | **true** |
| `overview.md` v5, `## What is coming`: WI-0003 "is parked until the stakeholder supplies a sample of their bank's format" | `tracker/items/EP-001/questions/Q-001.md` | that file: `status: answered`, the answer being *"I'll send you a sample later."* No sample is in the workspace and WI-0003 is `blocked` | **true** |
| ADR-0006 Decision: "`expense list` prints that position as its first whitespace-separated field" | `WI-0004 AC2` | `cli.py:139-147` again, and this review's own run of `expense list` through `awk '{print $1}'` → `1 2` | **true** |
| ADR-0007 Decision: the invariant is every name in a stored expense being in `data["people"]`, enforced at `add_expense` and `delete_person`, with `settle.positions()` unchanged and nothing added to `store.load` | `expenses/store.py`, `expenses/settle.py`, `WI-0004 AC3` | `git diff main..wi/WI-0004 -- expenses/settle.py` → **empty**; `add_expense`'s existing refusal; `delete_person`'s new one | **true** |
| `docs/product/vision.md`: "A record made by mistake can be **deleted** … It cannot be edited in place" | `WI-0001/Q-003`, WI-0004 | `vision.md:38-39`; `HANDLERS` in `cli.py`, which has `delete` under both nouns and no `edit` anywhere | **true** |
| `overview.md` (unchanged since v3): the one-way layering, "nothing below `cli.py` imports `cli.py`" | `expenses/settle.py`, `expenses/store.py` | `git diff main..wi/WI-0004 -- expenses/ \| grep -E "^\+import\|^\+from"` → **no import added by this item** | **true, still** |

Twelve claims, twelve true. The one that was false last time — "two new functions in `store.py`"
— no longer appears anywhere: `grep -c "two new functions" docs/architecture/overview.md` → 0.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | Every acceptance criterion ticked | **pass** | `grep -c "^- \[x\] AC" tracker/items/WI-0004/item.md` → 8; `grep -c "^- \[ \] AC"` → 0 |
| D2 | Every ticked criterion cites evidence in `verify-report.md` | **pass** | its Criteria table gives, for each of AC1–AC8, a command the second verification ran and its actual output — `od -c` byte dumps for the exact-output criteria, `md5sum` brackets for the refusals, `wc -c` for "prints nothing to stdout", a one-process/fresh-process comparison for AC5. No row cites `impl-report.md`, and none cites the appendix holding the first verification |
| D3 | All declared gates passed on the final state of the code | **pass** | `implement` ran the suite on `e2a0b3d`; `verify` re-ran it on `beb522e`; this review ran it on the trial-merge result. `lint-clean` is recorded as **skipped**, citing ADR-0004, at every stage and by every skill — never as a pass |
| D4 | No open blocking question | **pass** | `tracker/items/WI-0004/questions/Q-001.md` is `status: answered`; it is the only question on the item, and no question anywhere in the workspace is `open` |
| D5 | A journal entry per execution; `history.md` chains without a gap | **pass** | eleven rows, `— → draft → awaiting-answer → draft → ready → planned → in-progress → verifying → in-review → in-progress → verifying → in-review`, each `from` matching the previous `to`, the last matching `item.md`. Thirteen journal entries: eleven matching the rows by timestamp and actor, two declared non-transition entries |
| D6 | Design decisions in ADRs, cited from the plan or journal | **pass** | ADR-0006 and ADR-0007, both `status: current`, both cited by name from `plan.md`'s `## Decisions and ADRs` with route `decided`. The third decision — refusals through `ExpensesError` rather than argparse's `type=` — is route `documented` in `## Approach` with its reasoning, which is right: it decides a code path, not the system. Round 2 added, amended and superseded **no** ADR, which is correct, because it changed no design |
| D7 | Documents the change invalidated have been updated, with a version bump and a change-log row | **pass** | **this was the send-back, and it is now closed.** `docs/architecture/overview.md` is at `version: 5`, `updated-by: implement`, `updated-for: WI-0004`, with change-log row 5 naming the item. The deletion commands are described in `## The pieces, and why each exists` under `expenses/store.py` and `expenses/cli.py`; `## What is coming` holds WI-0003 alone, which is still coming. `README.md` was updated with the item (plan step 10) and `docs/product/vision.md` needed no change — its deletion sentence was written forward-looking and is now simply true |
| D8 | Every commit references the item ID | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → exit 0, `all 8 commit(s) on main..wi/WI-0004 name WI-0004` |
| D9 | Merged into the trunk | **pass** | trial-merged first into a **detached** worktree (`git worktree add --detach /tmp/trial5 main`), which left `git rev-parse --short main` at `441a9b0` throughout; merge clean, 13 files changed; `python3 -m unittest discover -s tests -t .` on the merge result → `Ran 120 tests in 1.215s`, `OK`. The trial was then removed, the item closed while the branch was still unmerged, and only then was the branch merged into `main` for real. See F4 |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0004 wi/WI-0004` → exit 0: `verified at beb522ed; wi/WI-0004 has moved to 2c96f8ea but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code`. Compared by the script. Independently: `git diff --stat beb522e..2c96f8e -- expenses/ tests/ README.md` is empty |
| D11 | `review.md` exists and says what was examined | **pass** | this file; `## What I examined` is first, and names the artifacts, the diff ranges, the twelve claims audited and what was opened for each |
| D12 | Claims in `docs/` about the behaviour this item touched are still true; absolute claims carry a resolvable citation | **pass** | the twelve-row audit above, each verdict reached by opening the citation. `lint-claims --changed-since main` → exit 0, `checked 1 document(s)`, `0 errors, 0 warnings` — that is the half a program can check; the audit is the half it cannot |

## Findings

**F1 — the send-back is fixed, and fixed at the root rather than at the symptom.** `implement`
did not merely delete the false sentence: it opened `expenses/store.py`, counted the functions,
and recorded in `impl-report.md` `## Round 2` a claim-by-claim table of what it checked against
what. It also struck rather than deleted the round-1 bullet that had declared the missing document
as though declaring it made it acceptable, and noted that the same bullet contained the same
miscount. That is the propagation path D12 describes, made visible in the item's own record.
No action.

**F2 — `expense delete` refuses a positive whole number written with leading zeros.**
Non-blocking; recorded, not to be acted on here. `cli.POSITION_RE` is `^[1-9]\d*$`, so
`expense delete 01` produces `expense '01' is not a positive whole number` — a sentence that is
true of the form the tool accepts and false of the value `01` denotes. The plan's `## Approach`
says the handler raises "on anything that is not [a positive whole number]", which `01` arguably
is. Nothing turns on it: `expense list` never prints a leading-zero number, no criterion covers
the case, and it fails safe with the tool's ordinary refusal and exit 2. It is recorded in
`item.md`'s `## Notes` so that a later reader meets it as a known choice rather than as a bug.

**F3 — `naming_expenses` still returns positions no caller reads.** Non-blocking, carried from
the first review's F2 unchanged. `delete_person` uses only `len()`. The `(position, expense)`
shape is the architect's, fixed in `plan.md`, and is what a future message naming *which*
expenses stand in the way would need. Now recorded in `item.md`'s `## Notes` too, since a finding
that lives only in a review is exactly what stops being read once an item is `done`.

**F4 — the trial merge was isolated this time, and the previous failure is worth keeping visible.**
The first review used `git worktree add /tmp/trial4 main`, which checks out the *real* `main`
branch rather than copying it, and the merge fast-forwarded the actual ref; `check-commit-refs`
caught it within the minute and it was rewound to `441a9b0`. This review used
`git worktree add --detach /tmp/trial5 main` and verified after the merge that
`git rev-parse --short main` was still `441a9b0`. The correction is in the first review's
appendix and in this item's journal, deliberately not tidied away. **The rule for this project:
a trial merge uses a detached checkout or a copy; `git worktree add <path> <trunk>` is not one.**

**F5 — nothing in the diff contradicts an ADR, and there is no unrequested scope.** Read hunk by
hunk. `expenses/cli.py`: `POSITION_RE` and `parse_position` → plan steps 4–5; the two subparsers,
their arguments and the two `HANDLERS` entries → step 4; `person_delete` and `expense_delete`
handlers → step 5; the `enumerate` in `expense_list` → step 6. `expenses/store.py`:
`naming_expenses`, `delete_person`, `delete_expense` → steps 1–3. `tests/`: one deleted line
(`line.split()[1]` → `[2]`) → step 7, which is ADR-0006's named repair and the only change made
to another item's evidence; `test_store.py`'s four classes → step 8; `test_cli.py`'s eight
`WI0004AC*` classes → step 9. `README.md` → step 10. `docs/architecture/overview.md` → Definition
of Done D7 and this review's own first-round finding, which is the item's one declared deviation
from the plan and is declared as such in `impl-report.md`. Two behaviours no criterion names are
both recorded in the plan rather than smuggled in: `naming_expenses` also checking
`shares_minor`'s keys (assumption 2 — it can only refuse more), and `parse_position` stripping
whitespace, which `parse_date` and `add_person` already do.

**F6 — the code is one I would be comfortable maintaining.** Specifics, since vague comfort is
not a review finding: every refusal is raised before any mutation, so "a refusal changes nothing
on disk" is a property of the layering rather than a promise each handler keeps; `save()` is
called by the handler only after the store function has returned; `expense_delete` parses its
argument *before* loading the store, which is why AC7's empty-store cases create no file; and the
two comments that exist (`POSITION_RE`'s and the `type=int` note on the subparser) explain a
choice rather than restate the code. The one thing a future reader could get wrong is F3, and it
now has a note in two places.

## Accepted gaps

Six, all now written into `item.md`'s `## Notes` — which is the point of accepting them. In
brief: `lint-clean` checked nothing on this project (ADR-0004, project-wide); AC8(c) and AC8(d)
are verified by reading only, so deleting either README sentence would leave the suite green; no
criterion pins any refusal message string; `expense delete 01` is refused (F2); `naming_expenses`
returns positions nobody reads (F3); and nothing was tested on another platform, against an older
dataset, or under concurrent use — no older dataset exists and the product is one person at one
terminal [src: docs/product/vision.md].

None of these justified a send-back: each is a limit on what was checked or a consequence of a
decision already recorded, and none is a claim in the record that is untrue.

## Verdict

**Accepted — merged and closed, `outcome: delivered`.** Twelve of twelve Definition of Done
criteria pass, including the two that failed last time. The change is eight criteria met with
evidence gathered twice, independently, by commands rather than by reading reports; a diff that
maps hunk-for-hunk onto the plan with one declared deviation; no ADR contradicted; a clean
detached trial merge with 120 tests passing on the merge result; and a `docs/` that now says what
the code does, checked claim by claim against the code rather than against itself.

---

# Appendix — the first review, at `e50dc4f`, which rejected this item

Kept verbatim, including its own correction. Its verdict was **Rejected** on D7 and D12; the
fix for it is what round 2 of `impl-report.md` describes and what D7 and D12 above record as
closed.


### What I examined

- `tracker/items/WI-0004/item.md` — the eight criteria and their tick state.
- `tracker/items/WI-0004/history.md` — all eight rows, checked for gaps and against `item.md`.
- `tracker/items/WI-0004/journal.md` — read in full; eight entries, one per history row.
- `tracker/items/WI-0004/questions/Q-001.md` — `status: answered`, `## Consequences` naming two
  files that exist and that carry the answer.
- `tracker/items/WI-0004/artifacts/plan.md`, `impl-report.md`, `verify-report.md`.
- **The diff, hunk by hunk**: `git diff main..wi/WI-0004 -- expenses/store.py`,
  `-- expenses/cli.py`, `-- README.md`, `-- tests/`. Not the reports about it.
- `docs/architecture/overview.md` v4, `docs/product/vision.md`,
  `docs/architecture/adr/ADR-0006-…md` and `ADR-0007-…md`.
- A trial merge of `wi/WI-0004` into a throwaway worktree of `main`, with the test suite run on
  the merge result.

### The D12 claim audit — what I opened for each claim

Each row is a claim in `docs/` about behaviour this item touched. The verdict comes from opening
the thing the claim cites and reading it, not from the sentence or from a neighbouring document.

| claim | cited | what I opened | verdict |
|-------|-------|---------------|---------|
| ADR-0006 Decision: "`expense list` prints that position as its first whitespace-separated field" | `WI-0004 AC2` | `expenses/cli.py:139-149` — `"%d  %s  %s  paid by %s  shared by %s" % (position, …)` over `enumerate(recorded, start=1)` | **true** |
| ADR-0006 Decision: "The stored record shape does not change, and `VERSION` stays 1" | `expenses/store.py` | `expenses/store.py:15` (`VERSION = 1`) and the whole `store.py` diff — 44 added lines, **zero** removed | **true** |
| ADR-0006 Consequences: "`store.expenses(data)` already returns the list in recorded order, so the position is an index" | `expenses/store.py` | `store.expenses` → `list(data["expenses"])`; `add_expense` appends | **true** |
| ADR-0007 Decision: the invariant is every name in a stored expense — `paid_by`, `shared_by`, or a key of `shares_minor` — being in `data["people"]` | `expenses/store.py`, `WI-0004 AC3` | `store.naming_expenses` checks exactly those three routes; `store.delete_person` refuses when it returns non-empty | **true** |
| ADR-0007 Decision: "Nothing is added to `store.load`, and `settle.positions()` is not changed" | `expenses/settle.py` | `git diff main..wi/WI-0004 -- expenses/settle.py` → empty; `store.load` unchanged in the diff | **true** |
| `docs/product/vision.md`: "A record made by mistake can be **deleted**… It cannot be edited in place" | `WI-0001/Q-003`, WI-0004 | `WI-0001/Q-003`'s `## Answer`, and the delivered commands | **true** — and now true in the present tense, which it was not before this item |
| `docs/architecture/overview.md` §"What is coming": "WI-0004 adds deletion … as two more handlers in `cli.py` over **two new functions** in `store.py`" | `tracker/items/WI-0004/artifacts/plan.md` | the plan's `## Approach` block (which says `delete_person()` and `delete_expense()`) **and then `expenses/store.py` itself** | **false** — see finding F1 |

The last row is the one this audit exists for. The plan's *Approach* summary says two functions;
the plan's *Steps* add three, because step 1 adds `naming_expenses`. `docs/architecture/overview.md`
re-quoted the summary rather than the steps, and nothing since had re-checked it against the code.
`grep -n "^def " expenses/store.py` on the branch head returns `naming_expenses` (126),
`delete_person` (145) and `delete_expense` (162) — three.

### Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | Every acceptance criterion ticked | **pass** | `grep -c "^- \[x\] AC" tracker/items/WI-0004/item.md` → 8; no `- [ ] AC` remains |
| D2 | Every ticked criterion cites evidence in `verify-report.md` | **pass** | its Criteria table gives, for each of AC1–AC8, a command and its actual output — byte dumps for the exact-output criteria, md5 comparisons for the refusals, a `cmp` for AC5. No row cites `impl-report.md` |
| D3 | All declared gates passed on the final state of the code | **pass** | `implement`'s closing entry records the suite run on `ff28637`'s tree; `verify` re-ran it on `f4e8319`; this review re-ran it on the trial merge result. `lint-clean` is recorded as **skipped** with ADR-0004 as the reason at every stage, never as passed |
| D4 | No open blocking question | **pass** | `tracker/items/WI-0004/questions/Q-001.md` is `status: answered`; it is the only question on the item |
| D5 | A journal entry per execution; `history.md` chains without a gap | **pass** | eight history rows, `— → draft → awaiting-answer → draft → ready → planned → in-progress → verifying → in-review`, each `from` matching the previous `to`; the last row's `to` matches `item.md`'s `status`. Eight journal entries, one per row, actors matching |
| D6 | Design decisions in ADRs, cited from the plan or journal | **pass** | ADR-0006 and ADR-0007 exist, both `status: current`, both cited by name from `plan.md`'s `## Decisions and ADRs` with their route (`decided`). The third decision — refusals through `ExpensesError` rather than `argparse`'s `type=` — is recorded in the plan as `documented` with its reasoning, which is the right route: it decides a code path, not the system |
| D7 | Documents the change invalidated have been updated, with a version bump and a change-log row | **FAIL** | `docs/architecture/overview.md` is still at version 4, whose `## What is coming` section describes this item's work as forthcoming. It is delivered. See finding **F1** |
| D8 | Every commit references the item ID | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → exit 0, `all 4 commit(s) on main..wi/WI-0004 name WI-0004` |
| D9 | Merged into the trunk | **not reached** | the item is rejected; the branch is left intact and unmerged. The trial merge was clean and is recorded below, so this is the only thing standing between the item and D9 |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0004 wi/WI-0004` → exit 0: `verified at f4e8319c; wi/WI-0004 has moved to e50dc4fc but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code`. Compared by the script, not by eye |
| D11 | `review.md` exists and says what was examined | **pass** | this file; `## What I examined` is first and lists the artifacts, the diff ranges and the claim audit |
| D12 | Claims in `docs/` about the behaviour this item touched are still true; absolute claims carry a resolvable citation | **FAIL** | six of the seven claims audited above are true against the code. The seventh — `overview.md`'s "two new functions in `store.py`" — is false: there are three. `lint-claims --changed-since main` → exit 0, so every citation *resolves*; this is the half a program cannot check. See finding **F1** |

### Findings

**F1 — `docs/architecture/overview.md` is out of date in two ways, and one of them is a wrong
claim about named code.** Blocking. This is the send-back.

1. Its `## What is coming` section still presents `person delete` and `expense delete` as
   forthcoming. They are delivered and tested on this branch. The document's own change log
   shows the expected remedy: row 3, *"`expenses/settle.py` and the `settle` command exist, so
   they move from 'What is coming' into the diagram, the layering rule and a piece of their
   own"* — made by `implement`, for WI-0002, on delivery. The same move is due here.
2. The sentence *"as two more handlers in `cli.py` over **two new functions** in `store.py`"* is
   false. `store.py` gains three: `naming_expenses`, `delete_person` and `delete_expense`.
   `naming_expenses` is not an implementation detail hidden inside another function — it is
   module-level, it is plan step 1, and it is the function that makes ADR-0007's invariant
   checkable. This is a D12 failure of exactly the kind D12 was written for: the claim came from
   the plan's `## Approach` summary, which also says two, and was never re-checked against the
   steps below it or the code.

   What is needed, concretely: bump `docs/architecture/overview.md` to version 5 with a
   change-log row naming WI-0004; move the deletion paragraph out of `## What is coming` into the
   body — the `expenses/store.py` and `expenses/cli.py` entries under `## The pieces, and why
   each exists`; state the count correctly or drop the count; and state ADR-0007's invariant in
   the `store.py` piece, since it is now a property of the delivered code rather than a plan.
   `WI-0003` should stay under `## What is coming`; it is still coming.

**F2 — `naming_expenses` returns positions that no caller reads.** Non-blocking; recorded, not to
be acted on. `delete_person` uses only `len()` of the result. The `(position, expense)` shape is
the architect's, fixed in `plan.md`'s `## Approach` block, and it is what a future message naming
*which* expenses stand in the way would need. Flagged so that a later reader does not mistake it
for an oversight and quietly narrow the return type. Do **not** change it as part of the fix for
F1 — that would be scope this item's criteria do not cover.

**F3 — the four deviations `impl-report.md` declares are all sound.** Checked, not taken on
trust. The AC8 test class pins only AC8(a)'s two literals, AC1's and AC2's exact output lines and
AC8(b)'s numbered sample, so it does not pin the prose the plan's assumption wanted left open —
the deviation is well argued and the reasoning is in the report. The empty-name refusal
(`'' is not in the group`) and `delete_expense`'s message (`there is no expense <n>`) are strings
no criterion constrains. And the report is right that AC7 enumerates seven vectors plus two
empty-store cases, not the plan's "nine". None of these is a finding; they are recorded here so
that the next reader can see they were examined rather than skipped.

**F4 — nothing in the diff contradicts an ADR, and there is no unrequested scope.** Every hunk
maps to a plan step: `store.py` → steps 1–3, `cli.py` → steps 4–6, `tests/test_cli.py` →
steps 7 and 9, `tests/test_store.py` → step 8, `README.md` → step 10. Two behaviours exist that
no criterion names, both recorded in the plan rather than smuggled in: `naming_expenses` also
checking `shares_minor`'s keys (assumption 2 — it can only refuse more), and `parse_position`
stripping whitespace, which is what `parse_date` and `add_person` already do. The one WI-0001
test touched (`line.split()[1]` → `[2]`) is the repair ADR-0006 named in advance, and it is the
only change made to another item's evidence.

**F5 — the trial merge is clean.** `git worktree add /tmp/trial4 main` then
`git merge --no-edit wi/WI-0004` → no conflicts, 11 files changed. `python3 -m unittest discover`
on the merge result → `Ran 120 tests in 1.232s`, `OK`. Recorded so that the next `implement`
knows F1 is the only thing in the way.

**Correction, made after this file was first written.** The sentence here originally said the
merge "was never published". That was wrong, and the error was this review's. `git worktree add
/tmp/trial4 main` checks out the **real** `main` branch in a second working directory; it does
not make a throwaway copy of it. The merge therefore fast-forwarded the actual `main` ref to
`e50dc4f`, and removing the worktree did not undo that. It was caught immediately, by
`check-commit-refs` reporting `wi/WI-0004 is already merged into main, so main..wi/WI-0004 is
empty`, in the gate run of the very transition that rejected this item. `main` was rewound with
`git branch -f main 441a9b0` — the commit it was at before, from `git reflog show main` — and
`check-commit-refs WI-0004 wi/WI-0004` then returned to exit 0, `all 4 commit(s) on
main..wi/WI-0004 name WI-0004`. Nothing was lost: the merge was a fast-forward, so no commit was
created and none was orphaned, the branch still carries all four commits, and this repository has
no remote, so nothing left it. The trial merge's result — clean, 120 tests passing — stands; only
the claim about how it was isolated was false. A trial merge in this project must use a detached
checkout or a copy, never `git worktree add <path> <trunk>`.

### Accepted gaps

None accepted, because the item is not being closed. The two gaps `verify-report.md` declares
that would have needed recording in `item.md`'s `## Notes` before a close are named here so they
are not lost in the round trip:

- **`lint-clean` checks nothing on this project.** `commands.lint` is `null`; nothing in this
  diff was checked for style, unused imports or dead code by any tool. ADR-0004 is the standing
  decision, so this is known and project-wide rather than new to this item.
- **AC8(c) and AC8(d) are verified by reading only.** The test class covers AC8(a) and (b). A
  future edit removing the refusal sentence or the renumbering sentence from `README.md` would
  not be caught by the suite. That is what AC8 asks for — it is a criterion "checked by reading
  the file" — but it should be written into `## Notes` when this item is next closed.

### Verdict

**Rejected — back to `in-progress`.** The change itself is good: eight criteria met with real
evidence, a clean diff that maps hunk-for-hunk onto the plan, no ADR contradicted, no unrequested
scope, and a clean trial merge. What fails is the record of it in `docs/`, on two Definition of
Done criteria:

- **D7** — `docs/architecture/overview.md` still describes this item's work as coming.
- **D12** — and while describing it, states a fact about `expenses/store.py` that the delivered
  code contradicts.

F1 is the whole of the send-back and it is one document. F2 through F5 are recorded observations
and require no action. When `overview.md` is at version 5 with the deletion commands in its body
and the function count right, this item should come back through verification and close.
