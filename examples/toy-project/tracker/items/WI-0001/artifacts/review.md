# Review — WI-0001

## What I examined

- `tracker/items/WI-0001/item.md` — all thirteen criteria, `## Out of scope`, `## Notes`
- `history.md` — six rows, read row by row against `pipeline.yaml`'s legal transitions
- `journal.md` — all five entries in full (`intake`, `refine`, `plan`, `implement`, `verify`),
  not skimmed
- `artifacts/plan.md`, `artifacts/impl-report.md`, `artifacts/verify-report.md`,
  `artifacts/refinement-qa.md`
- `docs/architecture/overview.md` v1 and ADR-0001, ADR-0002, ADR-0003
- `questions/` — empty; no question was ever filed on this item
- **the diff itself**, hunk by hunk: `git diff main..wi/WI-0001 -- .gitignore linecount.py tests/`
  — 117 lines of `linecount.py`, 271 of `tests/test_linecount.py`, 2 of `.gitignore`, and an
  empty `tests/__init__.py`. Nothing that existed before was modified
- `git log --format="%h %s" main..wi/WI-0001` — four commits, and
  `git diff --name-only 7d86345..wi/WI-0001` to establish exactly what changed after verification

Every hunk of the code diff maps to a plan step and to a criterion:

| hunk | serves |
|------|--------|
| `.gitignore` (`__pycache__/`, `*.pyc`) | plan step 1 — keeps the tree clean after the AC13 command |
| `count_lines` | AC5, and AC9 by reading bytes so nothing can be decoded |
| `list_files` | AC6, AC7 (all three cases), AC8 — one predicate, `is_file(follow_symlinks=True)` |
| `format_report` | AC1 (column width over counts *and* total), AC3, AC10 |
| `parse_args` | AC12's no-argument case, ADR-0001 |
| `main` | AC2 (the sort key), AC11 and AC12 (the folder-error branch, exit 2), ADR-0002 (the per-file branch) |
| `tests/__init__.py`, `tests/test_linecount.py` | AC13 and the evidence for AC1–AC12 |

No hunk contradicts an ADR. No hunk implements `--top`, an ignore rule, recursion, or any other
thing EP-001 puts out of scope; `format_report` derives the total from the rows it is given, so it
has not been pre-shaped for WI-0002.

## Definition of Done

`spec/dor-dod.md` §3, criterion by criterion.

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `grep -c "^- \[x\] AC"` → 13; `grep -c "^- \[ \]"` → 0; `validate-workspace` exit 0 |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | thirteen rows in the report's `## Criteria`, each naming the command run and quoting actual output. Two of them (AC9 with a system PNG, AC13 in a fresh `git clone`) were checked by a route the implementation did not use, which is what makes them independent rather than a second reading of the tests |
| D3 | the gates passed on the **final** state of the code | **pass** | the last code commit is `86f4384`; `implement`'s gates ran on it, and `verify` ran its own `python3 -m unittest discover` (27 tests, exit 0) at `7d86345`, whose code tree is identical — `git diff --name-only 7d86345..wi/WI-0001` lists only `tracker/` files. I re-ran the suite myself at the branch head: exit 0 |
| D4 | no open blocking question | **pass** | `tracker/items/WI-0001/questions/` is empty |
| D5 | a journal entry per execution; history chains without a gap | **pass** | history: `— → draft` (intake), `draft → ready` (refine), `ready → planned` (plan), `planned → in-progress` and `in-progress → verifying` (implement), `verifying → in-review` (verify) — each row's `from` equals the previous row's `to`, and the last row matches `item.md`'s status. Journal: five entries, one per execution, `implement`'s covering both of its transitions as one execution. `validate-workspace` agrees (0 errors) |
| D6 | every design decision is in an ADR, cited from a plan or journal | **pass** | ADR-0001 (argparse), ADR-0002 (a file that cannot be read), ADR-0003 (no lint command) — all three cited by number in `plan.md`'s `## Decisions and ADRs` and in the `plan` journal entry; ADR-0002 is cited again in `linecount.py`'s comment at the branch it governs, and ADR-0003 is the reason recorded for every skipped `lint-clean` |
| D7 | documents the change invalidated were updated, with a version bump and change-log row | **pass** | `docs/architecture/overview.md` was created at v1 by `plan` with a change-log row; `docs/product/vision.md` v1 needed no change — nothing delivered here contradicts it (single file, stdlib only, no flags for the common case, a number rather than a stack trace) |
| D8 | every commit references the item ID | **pass** | `scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, "all 4 commit(s) on main..wi/WI-0001 name WI-0001" |
| D9 | merged into the trunk | **pass** | `main` was at `f09a938`, which is also `git merge-base main wi/WI-0001`, so the merge is a fast-forward and the merge result is tree-identical to the branch head — proved before the trunk was touched by merging into a throwaway branch (`tmp/merge-check`) and running `git diff --stat wi/WI-0001 HEAD` → empty. `git checkout main && git merge --ff-only wi/WI-0001` then moved the trunk, and `python3 -m unittest discover` on `main` → exit 0, 27 tests |
| D10 | `verify` ran after the last code change | **pass** | `scripts/check-verify-freshness WI-0001 wi/WI-0001` → exit 0: "verified at `7d86345d`; `wi/WI-0001` has moved to `d41a046b` but only the record changed (6 file(s) under `tracker/` or `docs/`), so the verification still covers the code". The commits after the verified sha are `verify`'s and this review's own tracker records; `git diff --name-only 7d86345..wi/WI-0001` lists no file outside `tracker/`. **First execution of this review recorded this as a gate failure** — the gate then compared shas rather than paths and could not see the distinction. It was fixed in the methodology's tooling between the two executions; the substance of the finding did not change, and no `--force` was used |
| D11 | `artifacts/review.md` exists and says what was examined | **pass** | this file; `## What I examined` is first and lists the artifacts, the diff range, and the commands run |

## Findings

1. **`from __future__ import annotations` in `linecount.py` (line 17) does nothing.** No
   annotation in the file is evaluated, so the import is noise. Not a send-back: it changes no
   behaviour and no criterion. It is the kind of thing a linter would have removed, and there is
   no linter (ADR-0003) — recorded here so the cost of that ADR is visible in a concrete case
   rather than in the abstract.
2. **`.gitignore` carries `*.pyc` as well as the planned `__pycache__/`.** A harmless superset of
   plan step 1; no criterion touches it.
3. **`format_report`'s width calculation builds an intermediate list** (`[count for count, _ in
   rows] + [total]`). Correct and readable at these sizes; noted only because it is the one place
   in the file that allocates proportionally to the folder, and the plan's `## Risks` already
   bounds the folder at a couple of hundred files.
4. **Nothing else.** No duplicated rule, no swallowed error (both `except OSError` branches print
   the error before continuing, and the one that means "no answer at all" returns 2), no name that
   says something untrue. I would be comfortable maintaining this file.

## Accepted gaps

Each of these is declared in `verify-report.md` `## Not verified, and why` or in `impl-report.md`
`## What I did not do`, and is accepted rather than sent back. All five are also written into
`item.md`'s `## Notes`, because a gap that lives only in a report of a closed item is a gap
nobody will read again:

1. **No lint of any kind, on this item or any future one** (ADR-0003). Finding 1 above is the
   first concrete instance. Accepted: the ADR states the constraint and its reversal cost.
2. **Filenames that are not valid UTF-8 are untested.** `os.fsencode` in the sort key exists
   precisely for them, and AC2's own example is verified. Accepted: no criterion asks for one, and
   the code path is shared with the tested case.
3. **Scale beyond ~200 files, and files beyond 3 MiB, are untested.** The item and the plan bound
   the tool at "a few dozen, occasionally a couple of hundred". Accepted as bounded by the item.
4. **Non-POSIX platforms are untested.** AC7 and AC11 are written in terms of symlinks and Unix
   permissions; nothing asks for Windows. Accepted.
5. **`BrokenPipeError` is unhandled.** The `head` case was exercised by verification on a 200-file
   folder and did not reach it. Accepted, with the plan's instruction that an actual sighting is a
   bug item.

## Verdict

**Accepted, merged into `main`, and closed with outcome `delivered`.**

Every criterion is met and independently demonstrated, the record is complete and
reconstructible, the diff is entirely traceable to criteria and plan steps, and the two decisions
the criteria left open are recorded as ADRs rather than buried in code. All eleven Definition of
Done criteria pass, each with its own evidence above.

This review was executed twice, and the second execution changed no finding about the change
itself. The first execution reached the same verdict on substance but could not act on it: the
`verification-postdates-the-code` gate compared the verified sha with the branch head, so it read
`verify`'s own mandatory tracker commit as "the code changed after verification". Because
`scripts/transition` then ran a skill's hard gates on *every* transition, all four exits from
`in-review` were closed — `done`, `in-progress` (reject), `awaiting-answer` (file a question about
the gate) and `blocked` — and the item stopped there rather than being forced through.

Both causes were fixed in the methodology's own tooling between the two executions, along the
lines this review's first execution recorded: `check-verify-freshness` now compares the **paths**
that changed rather than the shas, and passes when everything that moved is under `tracker/` or
`docs/`; and hard gates now refuse only a skill's completion transition, so a skill can always
file a question about the gate that is blocking it. This second execution re-ran every gate on the
unchanged branch and they passed on their own terms. **No `--force` was used at any point**, and
this item's history carries no `[gates forced]` row.

The epic `EP-001` stays `open`: `WI-0002` (`--top N`) is still `ready`, so DE1 — every child item
`done` — is not met. Nothing else about the epic was pre-judged here.
