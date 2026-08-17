# Review — WI-0003

Reviewed by `review-close` v0.1.1 (reviewer) across two executions: 2026-08-17T00:15:13Z, which
stopped at D7 and filed `Q-001`, and 2026-08-17T00:21:54Z, which resumed after that answer and
closed the item. `main` fast-forwarded to the branch tip, as every earlier item in this epic did.

## What I examined

- **The record's mechanics.** `history.md` — eight rows, chaining without a gap, the last matching
  `item.md`. `journal.md` — seven entries for seven skill executions (`implement`'s two rows are
  one execution and carry one entry; `review-close` has two, one per execution). `questions/` —
  one question, `Q-001`, answered, with four files named under `## Consequences` and each opened
  and checked.
- **The diff**, `main..wi/WI-0003`, hunk by hunk: 63 lines of `linecount.py` and 172 of
  `tests/test_linecount.py`. `git diff --numstat` on the test file reports `172 0` — no existing
  test was touched, which is what AC4 rests on.
- **The reports**: `plan.md` (eight steps, the mapping table, four assumptions),
  `impl-report.md` (two declared deviations, four declarations of what was not done),
  `verify-report.md` (ten criteria with commands and quoted output, six negative cases, three
  sensitivity breakages).
- **The ADRs** the change touches or claims to follow: ADR-0001, ADR-0003, ADR-0004, ADR-0005,
  ADR-0008 and the new ADR-0009. `overview.md` v5 and `vision.md` v3.
- **The merge result**: produced first as a trial `--no-ff` merge (`0dbd81a`) and tested there —
  `Ran 77 tests`, `OK` — then, after that merge turned out to make `commits-reference-the-item`
  unsatisfiable, rewound and redone as a fast-forward *after* closing. See `## Findings` 3. All
  seven of EP-001's success measures were re-run against the merged trunk (recorded in EP-001's
  journal).

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every criterion ticked | **pass** | `grep -c "^- \[x\] AC"` → 10; `"^- \[ \] AC"` → 0 |
| D2 | every tick cites evidence | **pass** | `verify-report.md`'s table gives, per criterion, the command `verify` ran and its actual output — including AC4 checked against `git show main:linecount.py`, not against the suite alone |
| D3 | gates passed on the final code | **pass** | `implement`'s gates ran on `214dc3d`, the last code commit; `verify` re-ran the suite itself on `8792e41`; this execution re-ran it on the merged tree → `Ran 77 tests`, `OK`. No code changed after any of them — every later commit touches only `tracker/` and `docs/` |
| D4 | no open blocking question | **pass** | `Q-001` is `answered`, `answered-by: answer-questions`, with its consequences propagated and verified file by file |
| D5 | journal per execution, history chains | **pass** | seven executions, seven entries; `validate-workspace` → 0 errors, 0 warnings |
| D6 | design decisions in ADRs, cited | **pass** | ADR-0009 is the only design decision this change made, and it is cited from `plan.md`, this item's `## Notes`, `overview.md` v5, both `review-close` journal entries and a comment in `main` itself. Everything else cites ADR-0001/0004/0005/0008 rather than re-deciding |
| D7 | invalidated documents updated | **pass, after a round trip** | `overview.md` v4 → v5 (the function table gained `parse_sort` and `sort_rows`). `vision.md` v2 → v3 — this was **failing** at the first review: v2 said `--sort` was "being added … not delivered at the time of writing", which merging makes stale. `review-close` may not edit `product/vision.md` (`doc-header.md` §5), so it filed `Q-001` rather than editing and certifying its own edit; `answer-questions` made the change with a change-log row |
| D8 | commits reference the item | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → all 5 commits name WI-0003, exit 0 |
| D9 | merged into the trunk | **pass** | `main` fast-forwarded to the branch tip after closing, so `main` and `wi/WI-0003` name the same commit and the branch's work is not left only on the branch. The merge result was proved green *before* closing (trial merge `0dbd81a`, 77 tests `OK`) and the suite was run again on the trunk afterwards |
| D10 | verification postdates the code | **pass** | `check-verify-freshness` → verified at `8792e410`; everything after it changed only `tracker/`/`docs/`, so the verification still covers the code. Run, not judged by how the last commit looked |
| D11 | review record states what was examined | **pass** | this file, `## What I examined` first |

## Findings

1. **`sort_rows`'s `else` branch silently means "count".** Any `order` that is not exactly
   `"name"` returns the count order instead of raising, so `sort_rows(rows, "nmae")` would look
   like it worked. Unreachable today: `parse_sort` gates the only call site, `ParseSortTest` proves
   it rejects `"size"`, `"Name"`, `"COUNT"`, `""`, `"1"` and `"names"`, and `verify` demonstrated
   that test fails when `parse_sort` stops raising. Not a defect of this item — no criterion is
   violated and the behaviour cannot be reached — but recorded in `## Notes` because the guarantee
   is "one validated call site", and that is a property of today's call graph rather than of the
   function.
2. **Nothing else in the change.** Every hunk maps to a plan step or to a declared deviation; no
   ADR is contradicted; the `rows[:top]` slice is byte-for-byte what WI-0002 left, as ADR-0009
   requires.
3. **A finding against the pipeline's own tooling, not against this item.** `review-close`'s
   procedure merges at step 8 and closes at step 9, but its `commits-reference-the-item` gate runs
   `check-commit-refs <item> <branch>`, which inspects `{{trunk}}..{{branch}}` — an empty range
   once the branch is merged. Merging first therefore makes the gate unsatisfiable, and it refuses
   the very transition the merge was a precondition for. This execution hit it: the trial merge
   `0dbd81a` was green, and the close was then refused with "no commits on `main..wi/WI-0003`;
   nothing was delivered". The five items closed earlier in this epic all avoided it the same way —
   WI-0001's history row says so in as many words: *"closing before the fast-forward so
   commits-reference-the-item still has a range"* — so the trial merge was rewound (local, never
   published, nothing else referencing it), the item closed, and `main` fast-forwarded afterwards.
   No `--force` was used and no gate was overridden. The defect belongs to the methodology's gate
   tooling, not to this project, so no bug item was filed under EP-001; it is recorded here and in
   the journal so the next reviewer meets it as a known ordering constraint rather than a surprise.

## Accepted gaps

All three are written into the item's `## Notes`, not only here, because a closed item's reports
are not re-read.

1. **`--top N --sort name` selects the N alphabetically first** — observed under AC9, decided by
   nobody, bounded in shape by that criterion, explained by ADR-0009. Accepted: the human declined
   to specify it and forbade anyone else specifying it in his name.
2. **Argparse's `description` still says "largest first"** — pre-existing since `--top` shipped,
   covered by no criterion, excepted by AC4. Accepted.
3. **Nothing lints this project** (ADR-0003) — the 63 changed lines of `linecount.py` and 172 of
   tests were read by two people-shaped roles and by no tool. Accepted, unchanged from every item
   in this epic, and recorded in `verify-report.md`'s `## Not verified, and why`.

Also unchanged and not re-litigated here: only POSIX was exercised, and a one-file folder still
prints `total (all 1 files)` (WI-0002's own accepted gap).

## Verdict

**Accept.** `main` fast-forwarded to the branch tip; `python3 -m unittest discover` passes on the
merge result, both on the trial merge before closing and on the trunk afterwards. WI-0003 is
`done` with outcome `delivered`.

The item is worth one closing note. Its most valuable artifact is not the flag — it is that a
question the human refused to answer stayed unanswered all the way through plan, implementation,
verification and review, without anyone quietly deciding it on his behalf, and that the one
document rule this pipeline could have bent for convenience (a reviewer editing the product vision
he then certifies) was escalated instead.
