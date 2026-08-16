# Review — BUG-0003

## What I examined

- `item.md` — the six criteria, the reproduction script, `## Expected behaviour` with its five
  quotations (overview v2's bytes boundary, the exit-code contract, the vision's "a number, not a
  stack trace", WI-0001's `## Notes`, EP-001's `## Why now`), and `## Notes`
- `history.md` — five rows; `journal.md` — all **six** entries in full, including the
  `answer-questions` entry that corrected an ADR
- `artifacts/plan.md` (with its corrected `## Approach`), `impl-report.md`, `verify-report.md`,
  `questions/Q-001.md` (`answered`, with both files named in its `## Consequences` opened and
  checked)
- `docs/architecture/adr/ADR-0008` **v2**, `ADR-0002`, `ADR-0006`, `ADR-0007`,
  `docs/architecture/overview.md` v4, `docs/product/vision.md` v1
- **the diff**, hunk by hunk: `git diff main..wi/BUG-0003 -- linecount.py tests/` — `linecount.py`
  +9/−3, `tests/test_linecount.py` +55/−0

Two code hunks, both from plan steps 1–2:

| hunk | serves |
|------|--------|
| the module docstring gains one sentence: names are bytes too, citing ADR-0008 | plan step 2 — no behaviour |
| `print(text, end="")` → `sys.stdout.buffer.write(os.fsencode(text))` + `flush()`, with the comment explaining why | AC1–AC5 |

Everything that builds `text` is byte-identical to `main`: `count_lines`, `list_files`,
`format_report`, `parse_top`, `parse_args`, the sort key, `main`'s branch structure and every
stderr `print`. The change is at the boundary and nowhere else, which is what makes AC5 — "existing
output is unchanged" — checkable rather than hopeful.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | 6 of 6 `- [x]`; `validate-workspace` exit 0 |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | six rows, each with the command and the **captured bytes** quoted as `repr` — the only honest way to evidence a byte no terminal renders. Fixtures were built under `/tmp/vbug3-nC1s/` with bytes paths, not the item's own `/tmp/bug3` |
| D3 | the gates passed on the **final** state of the code | **pass** | last code commit `8634781`; `verify` ran the suite at `21d583d`, code-identical; I re-ran it on the merge result: 60 tests, exit 0 |
| D4 | no open blocking question | **pass** | `Q-001` is `answered` and was never blocking. Both files its `## Consequences` names were opened: ADR-0008 is at v2 with the correction block and the change-log row, and `plan.md`'s `## Approach` carries the corrected example |
| D5 | a journal entry per execution; history chains | **pass** | five rows chaining `— → ready → planned → in-progress → verifying → in-review`, the last matching `item.md`; six journal entries — the `verify` filing, `plan`, `implement`, `verify`, `answer-questions`, and this review |
| D6 | every design decision is an ADR, cited | **pass** | ADR-0008 v2, cited in `plan.md`'s decision table, in the `plan` and `answer-questions` journal entries, and in the code comment at the line it governs. Four options costed; reversibility stated |
| D7 | documents the change invalidated were updated | **pass** | `docs/architecture/overview.md` v3 → v4 by `plan`, extending "bytes, not text" from contents to names and recording the single-write constraint. ADR-0008 v1 → v2 by `answer-questions`. Both carry change-log rows; `vision.md` needed none — this fix makes its "a number, not a stack trace" claim true where it was false |
| D8 | every commit references the item ID | **pass** | `check-commit-refs` → exit 0, "all 4 commit(s) … name BUG-0003" |
| D9 | merged into the trunk | **pass** | `main` was at `f1b7524` = the merge base, so a fast-forward. Proved on a throwaway branch first: `git diff --stat wi/BUG-0003 HEAD` empty, 60 tests green. Then `git merge --ff-only`, suite re-run on `main` |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness` → exit 0: "verified at `21d583df`; … only the record changed (8 file(s) under `tracker/` or `docs/`)" |
| D11 | `artifacts/review.md` exists and says what was examined | **pass** | this file |

## Findings

1. **The verification did the thing this methodology is for.** It did not stop at "the criteria
   pass"; it measured the ADR's *reasoning* and found the rejected option's example did not
   reproduce — then measured further and found a setting where it does, which strengthens the
   decision rather than undermining it. That is the difference between checking work and
   confirming it, and it is worth naming in the record.
2. **The correction was routed correctly.** `verify` does not write to `docs/`, so it filed a
   question; `answer-questions` amended ADR-0008 in place at v2, kept the wrong claim visible
   because `doc-header.md` §4 exists to preserve what was believed, and changed no code. Had the
   ADR been edited by the skill that found the problem, nobody would have reviewed the edit.
3. **The single-write constraint is real and is recorded.** stdout is now one buffered byte write
   at the end of `main`; anything later that `print`s to stdout would interleave. ADR-0008's
   consequences and overview v4 both say so. I checked that nothing prints to stdout today, and
   nothing does.
4. **`test_ac3` passing against the old code was declared, not hidden.** Two runs of a
   consistently crashing tool are byte-identical, so AC3's test alone would not have caught this
   bug. `implement` said so unprompted and `verify` confirmed it; AC6 does not list that test,
   which is right. This is the kind of honesty that makes the rest of the report believable.
5. **Nothing else.** No duplicated rule, no swallowed error, no unrequested scope.

## Accepted gaps

Each is declared in `verify-report.md` `## Not verified, and why` or `impl-report.md` `## What I
did not do`, and each is carried into `item.md`'s `## Notes`:

1. **stderr's encoding is untouched** — a file both undecodable *and* unreadable could still raise
   while composing `linecount: <name>: <problem>`. Outside this item's criteria; a separate defect
   if it is ever observed.
2. **Non-POSIX platforms** — the new test class is `skipUnless(os.name == "posix")`.
3. **No lint** (ADR-0003).
4. **Interleaving is untestable today** — nothing else writes to stdout, so the constraint in
   finding 3 is a rule for future changes rather than something a test can hold.
5. **Only small reports were exercised** — the write is a single buffered call.

## Epic

`EP-001` is closed by this execution: BUG-0003 was its last child not `done`. The epic Definition
of Done is applied criterion by criterion in the epic's own journal entry, with its six success
measures re-run against the merged trunk — including the two the three bugs bore on, which now
behave as the epic always claimed they would.

## Verdict

**Accepted, merged into `main`, and closed with outcome `delivered`.**

Six criteria, each demonstrated on captured bytes; a two-hunk diff at exactly one boundary; an ADR
whose reasoning was tested, found partly wrong in its illustration, and corrected without changing
its decision. The tool now prints the folder that used to make it crash, and prints it the way
`ls -b` and `wc` do.
