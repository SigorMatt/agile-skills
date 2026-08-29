# Review — BUG-0001

Second review of this item. The first (at `4025111`, on the third-pass branch's predecessor)
rejected it on one finding — the AC4 test built two whole documents from Python literals — and
that section of the earlier review is superseded by this file. Its finding 2, a note asking the
next verification report to name which quantity its bare-table sweep measured, was carried out.

## What I examined

- `item.md` (all six criteria and their ticks), `history.md` (ten rows), `journal.md` (all ten
  entries, read in full), `artifacts/plan.md`, `artifacts/impl-report.md` (all three passes),
  `artifacts/verify-report.md` (the third pass, rewritten from scratch), and the previous
  `artifacts/review.md`, which this file replaces. `tracker/items/BUG-0001/questions/` does not
  exist; no question was ever filed on this item.
- The diff `main..wi/BUG-0001`, hunk by hunk: `git diff main -- docs/`, `git diff main --
  tests/test_fixtures.py tests/test_units.py`, `cat -A` on the four new fixture files, and the
  full changed-path list `git diff --name-only main` — fifteen paths, two documents, six test
  files, seven under `tracker/`.
- The code the corrected sentences are about, read rather than described: `mdtab/table.py`
  `_column_widths` (149–176), `_render_cell` (179–205) and `_spaces_omitted`.
- `docs/architecture/adr/ADR-0009-…md` `## Decision` — the four conditions ADR-0007's in-place
  edit had to meet — and `docs/architecture/adr/ADR-0007-…md` `## Decision` item 4 with its change
  log, compared against `git show main:<adr>` by string comparison rather than by eye.
- `docs/architecture/adr/ADR-0005-…md` `## Decision`, `tests/test_fixtures.py` in full
  (`ALIGNED`, the discovery helpers, `ProcessTest`), and `tests/test_units.py`'s module docstring
  — the rule the previous rejection rested on, and whether the fix satisfies it.
- `tracker/items/WI-0001/questions/Q-004.md`, the precedent the previous rejection cited.
- The tool itself: the two commands of `## Steps to reproduce`, three four-marker sweeps, and
  `_column_widths` called directly on both sweep tables.

**Claims audited from their citations (D12).** Each verdict below was reached by opening the cited
artifact, not by reading the sentence or a neighbouring document that repeats it.

| claim | where | cites | what I opened | verdict |
|---|---|---|---|---|
| a column's width does not depend on the *alignment* its marker declares | overview "Where a cell's content sits in its field"; ADR-0007 item 4 | `ADR-0007`; `WI-0002 AC6` | `WI-0002/item.md` AC6 — *"a column's width does not depend on its alignment. Every column is `2 + max(display width of its header and body cells)` wide, with WI-0001 AC12's two qualifying clauses unchanged"* — and `_column_widths`, which never calls `column_alignments` | **supported.** Independently discriminated: `---` and `:--` declare the same alignment and give different widths (2 and 3 on a bare table's first column, `_column_widths` called directly), while `--:` and `:--` declare different alignments and give the same width (3). A width is not a function of an alignment |
| the guard spaces are outside the field and do not move | overview, same bullet | `ADR-0007`; `WI-0002 AC6` | `_render_cell`: `padding = width - 2 - display_width(text)`, and the two guard spaces added outside `before`/`after` | **supported** |
| a column is never narrower than its delimiter cell can be written | overview, same bullet, deferring to the bullet below | `WI-0001 AC12`; `WI-0001/Q-005` | AC12's amended text — *"a column is never narrower than its delimiter cell can be written … must hold at least one `-`, plus one character for a leading `:` and one for a trailing `:`"* — and Q-005's `## Answer`, which put that clause there | **supported**, and phrased word-for-word as the "How wide a column is" bullet phrases it, so the two cannot drift |
| how wide that cell must be counts the `:` it carries | overview, same bullet | `WI-0001 AC12` | `_column_widths`: `needed = 1 + marker.startswith(":") + marker.endswith(":")` | **supported** |
| the middle column of `a \| \| b` is 2 columns wide under `---` and 3 under `:-:` | overview, same bullet | `WI-0001 AC12`; `WI-0001/Q-005` | AC12's own worked example — *"with marker `:---:` such a column is 3 wide rather than 2, and with `---` or `:---` it is 2"* | **supported exactly**, and reproduced: `_column_widths` on that table returns `[3,2,3]`, `[3,2,3]`, `[3,2,3]`, `[3,3,3]` for the four markers |
| ADR-0007 item 4: *"they already reached the width before WI-0002"* | ADR-0007 item 4 | `WI-0001 AC12` | `git show main:mdtab/table.py` — `max(width, needed + omitted)` is there, and no `mdtab/` path is on this branch | **supported** |
| the "How wide a column is" bullet's floor, including *"plus whichever surrounding spaces the row's outer-pipe style drops"* | overview | `WI-0001 AC12`; `WI-0001 AC6`; `WI-0001/Q-005` | `_column_widths`' `max(width, needed + omitted)` and `_spaces_omitted`; and the bare-table sweep, where a missing leading pipe makes `omitted` 1 | **supported** |

No claim in `docs/` about the behaviour this item touched was found to be false. The one sentence
that started this item is absent from every live claim in the tree; the only remaining occurrences
are the change-log rows that are *required* to quote what they removed and `ADR-0009`'s own text,
which quotes it in order to rule on it.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `grep -n "^- \[.\] AC" tracker/items/BUG-0001/item.md` → all six `[x]` |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | Six rows, each naming commands run in the third verification with their real output; no row cites `impl-report.md`. The report was rewritten from scratch for this pass rather than inheriting the second pass's rows, which is what makes D2 true of *this* head |
| D3 | the declared gates passed on the **final** state of the code | **pass** | Re-run here at `67b2957`: `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 72 tests in 0.140s`, `OK`; `python3 -W error -m compileall -q mdtab tests` → exit 0. And on the trial merge result — see D9 |
| D4 | no open blocking question on the item | **pass** | `tracker/items/BUG-0001/questions/` does not exist; no question was filed on this item at any point |
| D5 | a journal entry per execution; `history.md` chains without a gap | **pass** | Ten history rows — `— → ready → planned → in-progress → verifying → in-progress → verifying → in-review → in-progress → verifying → in-review` — and ten journal entries at the same ten timestamps. Each row's `to` equals the next row's `from`, and the last row's `to` matched `item.md`'s `status: in-review` when this review began |
| D6 | every design-changing decision is in an ADR, cited from the plan or journal | **pass** | One decision about the project's rules was made by this item — *correct ADR-0007 in place rather than supersede it* — and it is `ADR-0009`, written by `plan`, cited from `plan.md`'s `## Decisions and ADRs` table, from `plan`'s journal entry, and from ADR-0007's own v2 change-log row. The third pass made no design decision: it relocated a test to satisfy an existing ADR |
| D7 | documents the change invalidated are updated, with a version bump and a change-log row | **pass** | `docs/architecture/overview.md` 5 → 7 with v6 and v7 rows; `ADR-0007` 1 → 2 with a v2 row. In both, the top row's version equals the frontmatter version, and both rows quote in full the sentence they removed. The third pass changed no document, correctly: re-editing a passed document would have invalidated three ticks to fix none of them |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs BUG-0001 wi/BUG-0001` → exit 0, `all 13 commit(s) on main..wi/BUG-0001 name BUG-0001` |
| D9 | merged into the trunk | **pass** | Trial merge first, in a **detached** worktree: `git worktree add --detach /tmp/mdtab-trial-bug1 main`, `git merge --no-ff wi/BUG-0001` → clean, merge commit `2480754`; `python3 -m unittest discover -s tests -t .` on the merge result → exit 0, `Ran 72 tests`, `OK`; `compileall` → exit 0; worktree removed. `git rev-parse main` returned `5db7845902546b7e38cba59af51f5095ec6a965e` both before and after the trial, so the trial moved nothing. The real merge follows this review, after the item is closed |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness BUG-0001 wi/BUG-0001` → exit 0, *"verified at 4d8f6306; wi/BUG-0001 has moved to 67b2957f but only the record changed (5 file(s) under tracker/ or docs/)"*. The last change to code was `d6d2ecb`; the verification is at `4d8f630`, which is after it |
| D11 | `review.md` exists and states what was examined | **pass** | this file |
| D12 | every claim in `docs/` about the behaviour this item touched is still true, checked from its citation; absolutes carry a resolvable citation | **pass** | The seven-row audit table in `## What I examined`, each verdict reached by opening the cited artifact and the code; plus `lint-claims --changed-since main` → exit 0, `checked 2 document(s)`, and `lint-claims --all` → exit 0, for the mechanical half |

Twelve of twelve pass.

## Findings

**1. Not blocking. `tests/test_units.py` lost a blank line, and no plan step or criterion accounts
for it.** `git diff main -- tests/test_units.py` has two hunks and the first is only this:

```
 from mdtab.width import display_width
 
-
 def parsed(bodies):
```

`parsed()` is now one blank line below the import block where every other top-level `def` and
`class` in that file has two — `pipe_columns` (30), `cell_content_end` (43), `DisplayWidthTest`
(66), and so on down the module. It was introduced by the third pass, `d6d2ecb`, when the `os`,
`subprocess` and `sys` imports were removed and the removal overshot by one line;
`impl-report.md`'s third-pass section says the file *"returns to what it was"*, which is one line
short of true. `verify` found it and recorded it rather than sending the item back, which was the
right routing: no criterion of this item is about it, so it is not a send-back's business, and
nothing another item delivered is wrong, so it is not a bug item's.

**It is accepted rather than rejected, deliberately, and the reasoning is recorded so the next
reviewer can disagree with a sentence rather than with a silence.** The project has no style
gate — `commands.lint` is `python3 -W error -m compileall`, which compiles and does not lint — so
the standard being missed is the file's own internal consistency and nothing enforceable. Against
that, a rejection costs a full `implement` → `verify` → `review-close` cycle for one whitespace
character that changes no behaviour, no output and no document. Sending it back would be
proportionate to nothing. It is recorded in the item's `## Notes` under `## Accepted gaps` below,
so it survives this item rather than living only in a report nobody reads again.

**Nothing else.** Every hunk in `main..wi/BUG-0001` maps to a criterion or a plan step:
ADR-0007's frontmatter, item 4 and v2 row to plan step 4 (AC2, AC3); the overview's frontmatter,
bullet and v6/v7 rows to plan step 3 and the AC1 send-back (AC1, AC3); the four
`tests/fixtures/width-marker-*` files, the two `ALIGNED` entries, `ProcessTest`'s widened
docstring and the new test to AC4 by the route the previous review named; `WidthIndependenceTest`'s
docstring to plan step 2; and the `tracker/` paths to this item's own record. Nothing under
`mdtab/` (AC6), which the trial merge's clean test run independently confirms.

**The previous rejection is satisfied in the terms it was written in.** It required the two
documents to live in `tests/fixtures/` and not in a string literal, and left the placement and
the fate of `WidthIndependenceTest`'s docstring to `implement`. Both documents are now hand-derived
fixture pairs whose expected halves were derived from the rules before being compared with the
tool — the order `test_fixtures.py`'s own docstring requires — the assertion runs both commands
from `ProcessTest`, which is where this project already keeps tests stated over `python3 -m mdtab`,
and the pairs went into `ALIGNED`, so they are also walked by the eight document-level tests. That
last part was not asked for and is a genuine improvement: `verify` confirmed it by corrupting
`width-marker-colons.out.md` and watching a test fail. `ADR-0005` is satisfied and no criterion and
no ADR had to move, which is what the rejection predicted.

## Accepted gaps

Recorded here and written into `item.md`'s `## Notes`, because a gap that lives only in a report
is a gap nobody will find.

1. **The lost blank line above `parsed()` in `tests/test_units.py`** — finding 1 above. Accepted
   as cosmetic, with no style gate in the project to have caught it; a one-line fix for anyone who
   next touches that file.
2. **AC1's *"someone reading only the two bullets can predict the output of both commands"* is
   passed on a stated reading.** The two bullets give the quantity the two outputs differ in — a
   2-column middle field against a 3-column one — and the rule that produces it, but not the whole
   rendering arithmetic, so a reader could not reconstruct the two outputs byte for byte from them
   alone. Both this review and the previous one agree the stricter reading is satisfiable by no
   pair of bullets in a rules-live-in-one-place list, so it cannot be what AC1 intends. Declared
   in `verify-report.md` `## Not verified, and why` on two consecutive passes rather than assumed.
3. **`tracker/items/WI-0002/artifacts/review.md` line 64 holds a wrong verification record on a
   closed item** — it reports having checked this very sentence against the code and found that it
   held, having checked the guard-space half and the four-marker layout, neither of which reaches
   the width floor. It is history, not a live claim: nothing reads that line as a statement about
   the tool, `lint-claims` does not read `tracker/`, and correcting a closed item's evidence is
   forbidden by this item's `## Out of scope`. Accepted, named for the third time in this item's
   record, and **not** filed as a follow-up item — filing one would put a corrected paragraph of a
   closed item's history in front of the stakeholder at sign-off as an undelivered child, which is
   worse than the thing it fixes.
4. **A fifth restatement of the false sentence in wording the sweep's three phrasings do not
   match** would not have been found. The systematic check is the fifteen-claim audit in
   `EP-001/artifacts/review.md`, which this item's `## Out of scope` says not to repeat, and which
   DE6 will apply again when the engagement next reaches rest — which is now.

## Verdict

**Accepted — `in-review` → `done`, `outcome: delivered`.**

Three copies of a false absolute are gone from live text; what replaced them survives being
checked against `mdtab/table.py` claim by claim and against three four-marker sweeps that killed
the first replacement; ADR-0007 was corrected in place under all four of `ADR-0009`'s conditions
with the removed sentence quoted verbatim, which a string comparison against `main` confirms; the
behaviour the corrected sentences describe is pinned by a test that fails `2 != 3` when the width
floor is deleted, and by two fixture pairs that fail their round-trips as well; and nothing under
`mdtab/` is on the branch, so the tool the documents were wrong about is exactly as it was. The
trial merge is clean and its test run is green. One cosmetic finding is accepted and recorded.
