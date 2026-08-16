# Review — WI-0002

## What I examined

- `tracker/items/WI-0002/item.md` — the eleven criteria as they now stand, including AC10 after
  Q-001 corrected it, `## Out of scope`, and `## Notes` with its "Amended after `ready`" paragraph
- `history.md` — six rows, each checked against `pipeline.yaml`'s legal transitions
- `journal.md` — all six entries in full: `intake`, `refine`, `plan`, `implement`,
  `answer-questions`, `verify`
- `artifacts/plan.md`, `impl-report.md`, `verify-report.md`, `refinement-qa.md`,
  `questions/Q-001.md` (answered, with `## Consequences` naming three files)
- `docs/architecture/overview.md` v2, ADR-0004 and ADR-0005 (both created for this item),
  ADR-0001 … ADR-0003 (to check nothing here contradicts them), `docs/product/vision.md` v1
- **the diff itself**, hunk by hunk: `git diff main..wi/WI-0002 -- linecount.py tests/` —
  `linecount.py` +69/−11, `tests/test_linecount.py` +180/−0
- `git log --format="%h %s" main..wi/WI-0002` (four commits) and
  `git diff --name-only b2d851c..wi/WI-0002` (tracker only)

Every hunk of the code diff maps to a plan step and a criterion:

| hunk | serves |
|------|--------|
| the docstring's usage line `[--top N]` | plan deviation 3 — declared, one line, no behaviour |
| `format_report(rows, total=None, label="total")` and its two new branches | AC3, AC5, AC6, AC10 via ADR-0005; the `total is None` default is what keeps AC4 true |
| `parse_top` | AC7 via ADR-0004 — the one-line failure argparse cannot produce |
| `parser.add_argument("--top", metavar="N", …)` with no `type=` | AC8, and ADR-0004's premise |
| the `top` resolution block in `main` | AC7 — it returns 2 before the filesystem is touched |
| the `if top is None or not rows` report choice | AC1, AC3, AC4, AC6, AC9 |
| three appended test classes | AC1–AC11, and AC4's "unmodified" evidence |

Nothing implements a second flag, a short form, a threshold selector, or any other thing this
item's `## Out of scope` excludes. ADR-0004 and ADR-0005 are both honoured by the code that cites
them.

## Definition of Done

`spec/dor-dod.md` §3, criterion by criterion.

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | 11 of 11 `- [x]`, none left `- [ ]`; `validate-workspace` exit 0 |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | eleven rows, each with the command `verify` ran and its quoted output. Two were checked by routes the implementation could not have supplied: AC4 against the binary WI-0001 shipped (`git show 461e37f:linecount.py`), AC11 in a fresh clone |
| D3 | the gates passed on the **final** state of the code | **pass** | the last code commit is `abc7c66`; `verify` ran the suite at `b2d851c`, whose code tree is identical (`git diff --name-only b2d851c..wi/WI-0002` lists only `tracker/`), and I re-ran it myself at the branch head: 46 tests, exit 0 |
| D4 | no open blocking question | **pass** | `Q-001` is `status: answered`, and was filed `blocking: false` — the item was never suspended. Its `## Consequences` names three files, and I opened all three: AC10 is amended in `item.md`, the `## Notes` paragraph is there, and the plan's AC10 mapping row is rewritten |
| D5 | a journal entry per execution; history chains | **pass** | six history rows chaining `— → draft → ready → planned → in-progress → verifying → in-review`, the last matching `item.md`; six journal entries, one per execution — including `answer-questions`, which correctly has an entry and **no** history row, because it changed no status |
| D6 | every design decision is an ADR, cited | **pass** | ADR-0004 (reject a bad `--top` in our own code) and ADR-0005 (`format_report` keeps its signature) — both cited by number in `plan.md`'s decision table, in the `plan` journal entry, and in the docstrings of the code they govern |
| D7 | documents the change invalidated were updated, with a bump and a change-log row | **pass** | `docs/architecture/overview.md` v1 → v2, `updated-for: WI-0002`, change-log row present, and its function table now lists `parse_top` and `format_report`'s new parameters. `plan` made that change, as it must — `implement` and `verify` may not write to `docs/`. See `## Accepted gaps` for what `docs/product/` does **not** say |
| D8 | every commit references the item ID | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → exit 0, "all 4 commit(s) … name WI-0002" |
| D9 | merged into the trunk | **pass** | `main` was at `4825e16`, which is also `git merge-base main wi/WI-0002`, so the merge is a fast-forward. Proved before the trunk moved by merging into a throwaway branch: `git diff --stat wi/WI-0002 HEAD` empty, 46 tests pass there. Then `git checkout main && git merge --ff-only wi/WI-0002`, with the suite re-run on `main` |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0002 wi/WI-0002` → exit 0: "verified at `b2d851c6`; … has moved to `37a93244` but only the record changed (5 file(s) under `tracker/` or `docs/`)" |
| D11 | `artifacts/review.md` exists and says what was examined | **pass** | this file |

## Findings

1. **The no-argument usage line changed, and that is a real behaviour difference.** WI-0001
   printed `usage: linecount [-h] folder`; the tool now prints `usage: linecount [-h] [--top N]
   folder`. `verify` found it by running the old binary beside the new one, and recorded it
   rather than passing over it — which is exactly what I want a verifier to do. I accept it:
   AC4's byte-identity is stated "on the same folder" and this invocation has none; WI-0001 AC12
   requires only "a message on stderr" and exit 2, both of which hold; and no implementation of
   `--top` can leave that line unchanged without lying about the interface. It is written into
   `item.md`'s `## Notes` so it survives this item.
2. **`format_report`'s `None` sentinel carries two meanings** — "derive the total" and, with no
   rows, "there were no files". ADR-0005 names this and the risk it creates for a future third
   caller; `main` is the only caller today and both branches are pinned by tests
   (`test_ac6_top_zero_prints_only_the_total`, `test_ac9_empty_folder_whatever_n_is`). Accepted
   as recorded, not as unnoticed.
3. **Two error styles now reach stderr on purpose** — our one-line `linecount: --top: …` and
   argparse's usage block. ADR-0004 explains why unifying them was rejected (it would have put
   AC4 at risk). A later reader who finds this untidy should read that ADR before "fixing" it.
4. **`parse_top` accepts what `int()` accepts**, so `--top 3_0` means 30. Declared as the plan's
   assumption 1 and as an ADR-0004 consequence; untested, cosmetic, and it cannot produce a wrong
   count — only an unexpected N.
5. **Nothing else.** The code reads as one file with one job; the new function is four lines of
   logic and a docstring that explains why it exists at all. I would be comfortable maintaining
   it.

## Accepted gaps

Each is declared in `verify-report.md` `## Not verified, and why` or in `impl-report.md`
`## What I did not do`, and each is written into `item.md`'s `## Notes` so it outlives the reports:

1. **The usage-line divergence** (finding 1) — accepted, and now recorded in the item.
2. **No lint, on this item or any other** (ADR-0003) — 69 changed lines of `linecount.py` were
   read at review and by no tool.
3. **`int()`'s permissiveness** (`3_0`, `+3`, `" 3 "`) — untested; assumption 1.
4. **The singular label** — `(all 1 files)` on a one-file folder was never run; the item's own
   recorded assumption, cosmetic and cheap to reverse.
5. **Non-POSIX platforms**, unchanged from WI-0001.

The `--top`/ADR-0002 interaction (a `chmod 000` file is in neither M nor the total) is **not** in
this list: `verify` exercised it and it matches the plan's assumption 3 and AC3's own definition
of M. It is verified behaviour, not a gap.

## Epic

`EP-001` is closed by this execution — this was its last child not `done`. The Definition of Done
for epics (`spec/dor-dod.md` §4) is applied in the epic's own journal entry, criterion by
criterion, with one gap named there: `docs/product/vision.md` v1 never mentions `--top`, and
`review-close` may not edit it (`spec/doc-header.md` §5 gives that to `refine` and
`answer-questions`). Nothing in the vision is made false by this item.

## Verdict

**Accepted, merged into `main`, and closed with outcome `delivered`.**

Eleven criteria, each independently demonstrated; a diff with no unrequested scope; two ADRs for
the two decisions the criteria forced; and a question filed, answered from the human's own
recorded words, and propagated into the criterion it corrected — all visible in the record
without asking anyone what happened. No gate was forced, at any point, on this item or the last.
