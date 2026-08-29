# Verification report — BUG-0001

Verified-commit: 4d8f6306d69c7b0ebb35d9e5f02c4e775a02a741

**Third verification, written from scratch.** The second one (at `7a83da9`) passed all six
criteria and `review-close` then rejected the item on finding 1 of `artifacts/review.md` — the
AC4 test built two whole documents from Python literals. `implement`'s third pass moved them into
`tests/fixtures/` (`d6d2ecb`) and touched nothing in `docs/` and nothing under `mdtab/`. This
report re-derives all six verdicts from the criteria against this head rather than carrying any
of them over: every command below was run in this execution, and no row cites `impl-report.md`.

It also fixes what `review.md` finding 2 asked the next report to fix — the bare-table sweep
below names which quantity it measured, and gives both.

## Verdict

**Pass — all six criteria.** `verifying → in-review`.

One finding is recorded in `## Defects found` that no criterion covers and that is therefore not
a send-back: `tests/test_units.py` lost one blank line above `parsed()` on this pass, which no
plan step and no criterion accounts for.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | (a) `sed -n '58,95p' docs/architecture/overview.md` — read the corrected bullet and the "How wide a column is" bullet below it; (b) the two reproduce commands `printf 'a \| \| b\n---\|---\|---\nc \| \| d\n' \| python3 -m mdtab \| cat -A` and the same with `---\|:-:\|---`; (c) interior marker sweep `for m in '---' '--:' ':--' ':-:'; do printf 'a \| \| b\n---\|%s\|---\nc \| \| d\n' "$m" \| python3 -m mdtab \| sed -n '1p' \| cat -A; done`; (d) the same sweep on a bare table `printf ' \|a\|b\n%s\|---\|---\n \|c\|d\n'`; (e) `sed -n '145,205p' mdtab/table.py` — `_column_widths` and `_render_cell` read, not described; (f) `python3 -c` calling `_column_widths` directly on both sweeps | (b) `a \|  \| b$` / `--\|--\|--$` / `c \|  \| d$`, exit 0; and `a \|   \| b$` / `--\|:-:\|--$` / `c \|   \| d$`, exit 0. (c) `a \|  \| b$`, `a \|  \| b$`, `a \|  \| b$`, `a \|   \| b$`. (d) ` \| a \| b$`, `  \| a \| b$`, `  \| a \| b$`, `   \| a \| b$`. (f) interior middle column `[2, 2, 2, 3]`; bare first column `[2, 3, 3, 4]`. (e) `needed = 1 + marker.startswith(":") + marker.endswith(":")`, `widths.append(max(width, needed + omitted))`; `_render_cell` computes `padding = width - 2 - display_width(text)` and adds the guard spaces outside it | Taken clause by clause. **No longer asserts the old absolute** — the bullet's last sentence about widths now reads *"a column's width does not depend on the *alignment* its marker declares"*, and (a) shows no live bullet carries the unqualified form. **True of the code as it stands**, each claim separately: guard spaces outside the field and immobile — `_render_cell` adds them outside `padding`; width independent of *alignment* — `_column_widths` never calls `column_alignments`, and the discriminating pair is `---` and `:--`, which declare the **same** alignment and give **different** widths (2 and 3, sweep (f) bare), while `--:` and `:--` declare **different** alignments and give the **same** width (3); floor exists and counts the colons — `max(width, needed + omitted)` with `needed` counting `:`; *"can* come out wider under one marker than another" — hedged, and (c)+(d) show it. **Does not contradict "How wide a column is"** — it defers to that bullet instead of restating it, which is what v6 got wrong; the floor stated there reproduces every number in (f). **Cites something that supports it** — `WI-0002 AC6` says *alignment* verbatim for the first half; `WI-0001 AC12` and `WI-0001/Q-005` state the floor and its worked example for the second. **A reader of the two bullets can predict both commands** — the bullet states the pair literally (2 under `---`, 3 under `:-:`) and the floor rule below regenerates it. See `## Not verified, and why` for the reading of "predict the output" this rests on |
| AC2 | **pass** | `sed -n '/^## Decision/,/^## Consequences/p' docs/architecture/adr/ADR-0007-*.md \| grep -c "does not depend on its marker"`; `grep -n '^- \*\*Status:\*\*' docs/architecture/adr/ADR-0007-*.md`; `sed -n '1,10p'` for the frontmatter; the v2 change-log row read in full and compared against `git show main:docs/architecture/adr/ADR-0007-*.md` | `0`; `12:- **Status:** accepted`; `version: 2`, `status: current`, `updated-for: BUG-0001`; the v2 row carries the removed sentence between `*"` and `"*` in full — *"A column's width does not depend on its marker [src: WI-0002 AC6], so the two rules idempotence forces stay exactly where `docs/architecture/overview.md` says they are [src: WI-0001/Q-005]."* — and cites `[src: ADR-0009]` | The ADR did not change on this pass; the check was re-run, not carried over. Item 4 keeps *"`_column_widths` is not touched"* — true, and confirmed by AC6's diff — and its replacement clause was checked for truth rather than only for absence of the old: *"they already reached the width before WI-0002"* holds, since `max(width, needed + omitted)` predates it, and *"a column too narrow to hold its own marker is wider with `:-:` than with `---`"* names those two markers rather than generalising, so the one-colon case that killed v6 of the overview does not touch it. `ADR-0009`'s four conditions: (1) decision unchanged; (2) removed text demonstrably false, by (b) above; (3) quoted in full; (4) `status: accepted` kept, `version: 2`. Not superseded, and `**Supersedes:** —` is unchanged |
| AC3 | **pass** | `sed -n '1,8p' docs/architecture/overview.md`; `sed -n '/^## Change log/,$p' docs/architecture/overview.md`; the same two on `ADR-0007`; `python3 .claude/agile-skills/scripts/validate-workspace .` | overview `version: 7` with top row `\| 7 \| … \| implement \| BUG-0001 \| …` and a v6 row also naming BUG-0001; ADR-0007 `version: 2` with top row `\| 2 \| … \| implement \| BUG-0001 \| …`. Validator → exit 0, `checked 5 item(s), 11 document(s)`, `0 errors, 0 warnings` | In both documents the top change-log row's version equals the frontmatter version, which is `spec/doc-header.md` §3 and which the validator also checks mechanically. Both rows quote the text they removed |
| AC4 | **pass** | `git diff main -- tests/test_fixtures.py tests/test_units.py`; `cat -A tests/fixtures/width-marker-*.md`; `python3 -m unittest discover -s tests -t .`; mutation of `mdtab/table.py` line 175 to `widths.append(width)` then `python3 -m unittest tests.test_fixtures.ProcessTest.test_a_marker_with_colons_widens_a_column_too_narrow_to_hold_it`; and a second, independent mutation of `tests/fixtures/width-marker-colons.out.md` | The four fixture bytes are exactly the two documents of `## Steps to reproduce` and exactly what the two commands print — `width-marker-dashes.in.md` is `a \| \| b$ / ---\|---\|---$ / c \| \| d$` and its `.out.md` is `a \|  \| b$ / --\|--\|--$ / c \|  \| d$`, and the colons pair likewise with a 3-wide middle column. Suite → exit 0, `Ran 72 tests in 0.140s`, `OK`. Under the floor mutation the named test fails with `AssertionError: 2 != 3` and the full suite reports `FAILED (failures=5)`; restored, `Ran 72 tests … OK`, `git status --short` empty | The test is `ProcessTest.test_a_marker_with_colons_widens_a_column_too_narrow_to_hold_it` in `tests/test_fixtures.py`. It runs both **commands** — `sys.executable -m mdtab` with the fixture bytes on stdin — which is AC4's wording, asserts the middle field is 2 in the first and 3 in the second, and derives the width from `pipe_columns` so it is a display width and not a `len` (ADR-0002). It also requires all three lines of each output to agree on the width, so a delimiter row that alone happened to be right would not pass it. The `review.md` finding 1 route is taken exactly: the two documents are fixture pairs under `tests/fixtures/`, registered in `ALIGNED`, and `test_units.py` holds no document and imports no `subprocess` |
| AC5 | **pass** | `python3 -m unittest discover -s tests -t .`; `python3 .claude/agile-skills/scripts/lint-claims --all` | `Ran 72 tests in 0.140s`, `OK`, exit 0; `lint-claims: checked the whole tree under /home/msi/agile-skills-throwaway/mdtab`, `0 errors, 0 warnings`, exit 0 | Both run at the head being verified, with the tree clean |
| AC6 | **pass** | `git diff --name-only main`; `git diff --name-only main \| grep -c '^mdtab/'` | Fifteen paths: `docs/architecture/adr/ADR-0007-…md`, `docs/architecture/overview.md`, the four `tests/fixtures/width-marker-*` files, `tests/test_fixtures.py`, `tests/test_units.py`, and seven under `tracker/`. `grep -c '^mdtab/'` → `0` | Nothing under `mdtab/` is on the branch. The floor the false sentence invited deleting is intact — confirmed twice over, since the mutation run for AC4 had to be introduced by hand and was reverted |

All six boxes in `item.md` are ticked and were re-demonstrated in this execution; none is carried
over from the second verification.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 72 tests in 0.140s`, `OK`, at `4d8f630` with a clean tree |
| `lint-clean` | **pass** | `python3 -W error -m compileall -q mdtab tests` → exit 0 |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 5 item(s), 11 document(s)`, `0 errors, 0 warnings` |
| `every-criterion-independently-checked` | **pass** | Every row above names commands run in this execution and quotes their real output. No row's evidence is `impl-report.md`; the report was read after the criteria and is not cited as evidence anywhere |
| `negative-cases-exercised` | **pass** | See `## Negative and boundary cases exercised` — the one-colon interior column (the case that falsified v6), the bare-table outer-pipe case, the content-exceeds-the-minimum case, the width-floor mutation, and a corrupted fixture |
| `tests-would-fail-without-the-change` (advisory) | **pass** | Two independent mutations, both run and both reverted: the floor in `_column_widths`, and the expected bytes of `width-marker-colons.out.md` |

## Negative and boundary cases exercised

1. **The one-colon interior column** — the boundary the v6 wording died on, and the reason AC1
   needs more than the two reproduce commands.
   `for m in '---' '--:' ':--' ':-:'; do printf 'a | | b\n---|%s|---\nc | | d\n' "$m" | python3 -m mdtab | sed -n '1p' | cat -A; done`
   → `a |  | b$`, `a |  | b$`, `a |  | b$`, `a |   | b$`. `_column_widths` for the middle column,
   called directly: `[2, 2, 2, 3]`. A one-colon marker widens it by **nothing**, because the
   floor `1 + 1 = 2` does not exceed `2 + max(content) = 2`. The v7 sentence asserts nothing about
   this case; it says a column at the minimum *can* come out wider, and defers the arithmetic.
2. **The bare-table first column** — the same sweep with the outer pipe missing, where the floor
   picks up the dropped guard space.
   `for m in …; do printf ' |a|b\n%s|---|---\n |c|d\n' "$m" | python3 -m mdtab | sed -n '1p' | cat -A; done`
   → ` | a | b$`, `  | a | b$`, `  | a | b$`, `   | a | b$`. **Naming the quantity, which
   `review.md` finding 2 asked for:** those are the *rendered leading fields* — what is printed
   before the first `|` — and they are 1, 2, 2, 3. The *column widths* `_column_widths` returns for
   the same table are **2, 3, 3, 4**; the difference is the one guard space the missing outer pipe
   drops (`_spaces_omitted` → `omitted = 1`). Both were computed, not inferred: the printed form by
   the sweep, the widths by calling `_column_widths(rows, leading=False, trailing=True)` directly.
   The inference AC1 rests on is unaffected and holds in both measures — `---` and `:--` declare
   the same alignment (`left`) and give different widths, so a width is not a function of an
   alignment.
3. **The marker is irrelevant once the content exceeds the minimum** — the other side of AC1's
   hedge. `for m in '---' '--:' ':--' ':-:'; do printf 'a | q | b\n---|%s|---\nc | r | d\n' "$m" | python3 -m mdtab | sed -n '1p'; done`
   → `a | q | b` four times. The hedge in the overview's *"can come out wider"* is doing real work.
4. **The width floor removed** — AC4's stated failure mode, run rather than assumed. See
   `## Test sensitivity check`.
5. **The expected bytes corrupted** — proof the two new fixture pairs are actually exercised by
   the document-level tests and not merely present on disk. See the same section.
6. **No fourth copy of the false sentence in live text.** `plan.md`'s last risk asks verify to
   sweep before ticking AC1:
   `grep -rn "width does not depend on its marker\|width is the same whatever its marker\|no column's width depends on its marker" --include='*.md' --include='*.py' .`
   → no hit under `mdtab/` or `tests/` at all. In `docs/` the only hits are the change-log rows of
   `overview.md` v6 and `ADR-0007` v2, which are *required* to quote what they removed
   (`ADR-0009` condition 3), and `ADR-0009`'s own `## Context` and `## Decision`, which quote the
   sentence in order to rule on it. Every other hit is under `tracker/` and is record, not claim.

## Test sensitivity check

**The width floor.** `mdtab/table.py` line 175 changed from
`widths.append(max(width, needed + omitted))` to `widths.append(width)` by an in-place edit over a
backup copy. `python3 -m unittest tests.test_fixtures.ProcessTest.test_a_marker_with_colons_widens_a_column_too_narrow_to_hold_it`
→ `AssertionError: 2 != 3`, `FAILED (failures=1)`. Full suite → `FAILED (failures=5)`, the extra
four being the fixture round-trips the floor also pins. `mdtab/table.py` restored from the backup;
`git status --short` empty and the suite back to `Ran 72 tests … OK`.

**The fixtures are wired in, not merely written.** `tests/fixtures/width-marker-colons.out.md` was
replaced with a version one column too wide. Full suite → `FAILED (failures=1)`. Restored;
`git status --short` empty. So the two new pairs really are walked by the `ALIGNED` map's
document-level tests — round-trip, idempotence, equal row widths, pipe alignment — and not only by
the one test written for them.

Both mutations were introduced by hand in this execution and both were reverted in it. The tree is
clean at the verified commit.

## Defects found

**1. Not blocking, and no criterion covers it — for `review-close`.** `tests/test_units.py` lost
one blank line on this pass. `git diff main -- tests/test_units.py` has two hunks, and the first is:

```
 from mdtab.width import display_width
 
-
 def parsed(bodies):
```

`parsed()` is now separated from the import block by one blank line where every other top-level
`def` and `class` in that file has two (`pipe_columns` at 30, `cell_content_end` at 43,
`DisplayWidthTest` at 66, and so on). No plan step and no acceptance criterion accounts for the
hunk, and `impl-report.md`'s third-pass section says the file *"returns to what it was"* plus the
docstring correction, which is one line short of true. It is cosmetic — `compileall` does not care
and no test reads it — so it is neither a send-back (no criterion of this item is about it) nor a
bug item (nothing another item delivered is wrong). It is one line in one file, and it is recorded
here so `review-close` can decide whether to have it fixed before the merge.

**Nothing else.** Every other hunk in `main..wi/BUG-0001` maps to a plan step or a criterion: the
ADR-0007 frontmatter, item 4 and v2 row to plan step 4 (AC2, AC3); the overview frontmatter, bullet
and v6/v7 rows to plan step 3 and the AC1 send-back (AC1, AC3); the four fixture files, the
`ALIGNED` entries, the `ProcessTest` docstring and the new test to AC4 by way of `review.md`
finding 1; `WidthIndependenceTest`'s docstring to plan step 2. Nothing under `mdtab/` (AC6).

## Not verified, and why

- **AC1's "someone reading only the two bullets can predict the output of both commands", on the
  strict reading.** The two bullets give the quantity the two outputs differ in — a 2-column
  middle field against a 3-column one — and the rule that produces it. They do not give the whole
  rendering (the guard spaces, the delimiter row's own fill, the outer-pipe drop), so a reader
  could not reconstruct the two outputs byte for byte from those bullets alone. AC1 is passed on
  the reading that "predict the output" means predict what the commands are contrasted *for*,
  which is the width. The second verification recorded the same reading and `review.md`'s
  `## Accepted gaps` reviewed and agreed with it — *"the stricter reading is satisfiable by no pair
  of bullets in a rules-live-in-one-place list"*. It is restated here rather than dropped, because
  this report is written from scratch and an undeclared gap reads as a clean pass.
- **Whether a fifth or sixth restatement of the false sentence exists in wording the grep did not
  match.** The sweep in case 6 above uses the three phrasings the record knows about. A paraphrase
  in words none of them share would not be found by it. The termination review's fifteen-claim
  audit (`EP-001/artifacts/review.md`) is the systematic check, and it is not repeated here —
  `plan.md` `## Out of scope` puts it outside this item.
- **`tracker/items/WI-0002/artifacts/review.md` line 64**, which records a verification of this
  very sentence that concluded it "holds". It is a wrong record on a closed item. It is history
  rather than a live claim, correcting it would mean rewriting a closed item's evidence, and this
  item's `## Out of scope` forbids that. Not verified, not corrected, and named here for the third
  time in this item's record so it is not lost.
- **Anything about `mdtab/`'s behaviour beyond the width floor and the guard spaces.** This item's
  criteria are about what three documents say; the tool's behaviour was exercised only where a
  corrected sentence makes a claim about it.
