# Implementation report — BUG-0001

Branch `wi/BUG-0001`, from `main` at `5db7845`; head `d6d2ecb`.

**Third pass.** `review-close` rejected the item at `4025111` (`artifacts/review.md`) on one
finding, about where the AC4 test keeps its two documents. Nothing in `docs/` changed on this
pass and no acceptance criterion moved. Read `## Third pass — the fixture-rule send-back` first,
then `## Second pass`, then the first-pass sections; each says what it changed and what it left
standing.

## Third pass — the fixture-rule send-back

**What was wrong.** The AC4 test built its two documents from Python string literals inside
`tests/test_units.py`:

```python
dashes = filtered("a | | b\n---|---|---\nc | | d\n")
colons = filtered("a | | b\n---|:-:|---\nc | | d\n")
```

`ADR-0005` `## Decision` says *"Fixtures are the only place a test may express a document; a test
may not build one from a Python literal"*, and `tests/test_units.py`'s module docstring says the
same locally — *"These test fragments — a width, a row, a prefix — not documents; whole documents
live in `tests/fixtures/` and are exercised by `test_fixtures.py`"*. The second pass declared the
tension in `## Deviations from the plan` 1 and left it for a reviewer; the reviewer's answer is
that the record had already ruled, in `WI-0001/Q-004`, which weighed and rejected option D,
*"keep the literal, declare the deviation"*.

**What was done.** Four files and no change to `docs/`:

1. **Two fixture pairs**, `tests/fixtures/width-marker-dashes.{in,out}.md` and
   `tests/fixtures/width-marker-colons.{in,out}.md` — the two documents of `## Steps to
   reproduce`, byte for byte. The expected outputs were **derived by hand from the rules and then
   compared against the tool**, in that order, which is what `test_fixtures.py`'s docstring
   requires of a fixture: for the dashes document, column 0 is `2 + 1 = 3` wide and renders as 2
   because the missing leading pipe drops a guard space, the middle column is `max(2 + 0, 1) = 2`,
   and column 2 is `3` rendering as 2 — giving `a |  | b`; for the colons document the middle
   column's marker makes the floor `1 + 2 = 3`, so `max(2, 3) = 3` and the row is `a |   | b`.
   Both hand-derivations match the bytes the tool produces.
2. **Both pairs registered in `ALIGNED`** in `tests/test_fixtures.py`, which is what puts them
   through the eight document-level tests that walk that map — round-trip, AC6 idempotence, the
   equal-row-width and pipe-alignment checks, and the untouched-lines check — rather than only
   through the one test written for them.
3. **The assertion moved to `ProcessTest`**, which already exists for the tests stated over
   `python3 -m mdtab` rather than over a call, and whose docstring is widened from *"AC1 — the
   one test that needs the process boundary"* to name both reasons. AC4 asks for the two
   *commands*, so the test still runs them; it now reads its input from the fixtures and derives
   the width with `pipe_columns` and `contents`, both already in that module.
4. **`tests/test_units.py` returns to what it was**, plus the docstring correction that plan step
   2 requires: the `os`, `subprocess` and `sys` imports, the `ROOT` constant and the `filtered()`
   helper are gone, and `WidthIndependenceTest`'s docstring still names both facts and both
   criteria — it now points at the test in `test_fixtures.py` for the half stated over documents
   instead of at a sibling method. The class keeps the test that is genuinely a fragment test.

**Nothing else moved.** `docs/architecture/overview.md` stays at v7 and `ADR-0007` at v2, so AC1,
AC2 and AC3 are unaffected and their evidence below still stands. Nothing under `mdtab/` (AC6);
the four new files are under `tests/fixtures/`.

**Gates re-run at `d6d2ecb`:** `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 72
tests`, `OK` (the count is unchanged: one test left `test_units.py` and one arrived in
`test_fixtures.py`); `python3 -W error -m compileall -q mdtab tests` → exit 0;
`validate-workspace` → exit 0; `lint-claims --changed-since main` → exit 0, `checked 2
document(s)`; `lint-claims --all` → exit 0; `check-commit-refs BUG-0001 wi/BUG-0001` → exit 0,
`all 11 commit(s) … name BUG-0001`; `git diff --name-only main | grep -c '^mdtab/'` → `0`.

**AC4's sensitivity, re-run against the moved test:** with line 175 of `mdtab/table.py` changed
from `widths.append(max(width, needed + omitted))` to `widths.append(width)`,
`ProcessTest.test_a_marker_with_colons_widens_a_column_too_narrow_to_hold_it` fails with
`AssertionError: 2 != 3` and the suite reports `FAILED (failures=5)` — one more than the second
pass's four, because the new `width-marker-colons` fixture pair also fails its round-trip. The
mutation was reverted from a backup copy; line 175 is the original, the suite is back to `Ran 72
tests … OK` and `git status --short` is clean.

**Second pass.** Verification sent the item back on AC1 at `64012f3`
(`artifacts/verify-report.md`), and everything below the next heading was written on the first
pass and still holds except where `## Second pass — the AC1 send-back` says otherwise.

## Second pass — the AC1 send-back

**What was wrong.** The v6 clause written to replace BUG-0001's false absolute contained a new
one: *"so a column too narrow to hold its own marker comes out one column wider for each `:` the
marker carries"*. It restates the minimum-width rule as an increment, and it is false in **both**
directions:

- **An interior column with one colon is not widened at all.**
  `for m in '---' '--:' ':--' ':-:'; do printf 'a | | b\n---|%s|---\nc | | d\n' "$m" | python3 -m mdtab | sed -n '1p' | cat -A; done`
  → `a |  | b$`, `a |  | b$`, `a |  | b$`, `a |   | b$` — widths 2, 2, 2, 3. Only the second
  colon binds, because an empty column's `2 + max(content)` is already 2 and a one-colon marker's
  minimum is also 2. This is the case `verify` found.
- **And the first column of a bare table *is* widened by a single colon** — which the send-back
  did not name and which was found while fixing it. The floor is `needed + omitted`, and a row
  with no leading pipe drops one guard space, so `omitted` is 1 there:
  `for m in '---' '--:' ':--' ':-:'; do printf ' |a|b\n%s|---|---\n |c|d\n' "$m" | python3 -m mdtab | sed -n '1p' | cat -A; done`
  → ` | a | b$`, `  | a | b$`, `  | a | b$`, `   | a | b$` — widths 1, 2, 2, 3. So no per-marker
  increment rule of any kind is true; the width depends on the marker, the content **and** the
  row's outer-pipe style together.

**What was done.** `docs/architecture/overview.md` v7. The bullet keeps the alignment half
unchanged and, for the colons, names the rule and hands the arithmetic to the *"How wide a column
is"* bullet immediately below, which already states it correctly including the outer-pipe clause.
It keeps exactly one concrete pair, which is what AC1 requires a reader to be able to predict:

> The marker's colons are a separate question, and the bullet below answers it rather than this
> one: a column is never narrower than its delimiter cell can be written, and how wide that cell
> must be counts the `:` it carries. So a column whose content leaves it at that minimum can come
> out wider under one marker than under another — the middle column of `a | | b` is 2 columns
> wide under `---` and 3 under `:-:` [src: WI-0001 AC12; src: WI-0001/Q-005].

Restating a rule one bullet from where it lives was the mistake, in the section whose subject is
rules that live in exactly one place. Deferring is not evasion here: it is the section's own
convention, and it is the only form of the sentence that stays true for interior and outer columns
alike without duplicating three clauses.

**Every claim in the new sentence, checked against the code rather than against the old one:**

| claim | true? | how |
|-------|-------|-----|
| a column's width does not depend on the *alignment* its marker declares | yes | `WI-0002 AC6`, unchanged from the first pass, and its own test `test_the_pipes_land_in_the_same_places_under_all_four_markers` |
| a column is never narrower than its delimiter cell can be written | yes | `_column_widths`: `max(width, needed + omitted)`. Phrased word-for-word as the next bullet phrases it, deliberately — same rule, one owner |
| how wide that cell must be counts the `:` it carries | yes | `needed = 1 + marker.startswith(":") + marker.endswith(":")` |
| a column whose content leaves it at that minimum **can** come out wider under one marker than under another | yes | hedged, and demonstrated by both sweeps above; nothing is asserted about columns whose content already exceeds the minimum, where the marker is irrelevant (`X \| q \| Y` under all four markers) |
| the middle column of `a \| \| b` is 2 columns wide under `---` and 3 under `:-:` | yes | the two reproduce commands, exit 0 both, output quoted above |

**What was not changed on this pass.** `ADR-0007` is untouched and stays at v2 — `verify` passed
AC2 against it, its wording names the two markers rather than generalising, and re-editing a
passed criterion would invalidate its tick for nothing. `tests/test_units.py` is untouched: AC4
passed, and the sentence's one concrete claim is the pair that test already pins. No file under
`mdtab/` (AC6). AC3 needed re-satisfying and was: `docs/architecture/overview.md` is now
`version: 7` with a v7 row naming BUG-0001 and quoting the removed clause in full.

**Gates re-run at `07a8966`:** `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 72
tests`, `OK`; `python3 -W error -m compileall -q mdtab tests` → exit 0;
`validate-workspace` → exit 0, `0 errors, 0 warnings`; `lint-claims --all` → exit 0;
`lint-claims --changed-since main` → exit 0; `check-commit-refs BUG-0001 wi/BUG-0001` → exit 0,
`all 6 commit(s) … name BUG-0001`; `git diff --name-only main | grep -c '^mdtab/'` → `0`.

**A note for whoever verifies this.** `lint-claims --all` passed over the false v6 sentence, and
passes over this one. It checks that an absolute carries a citation that *resolves*, not that the
citation *supports* the sentence — `WI-0001 AC12` was cited by the false clause too. The only
thing that caught v6 was running the markers, and that is what should decide v7.

## First pass

## What was built

Nothing under `mdtab/`. This item is a defect in what three documents *say*, and the tool they
describe is correct, so the whole change is one test and two document corrections.

**The test.** `WidthIndependenceTest.test_a_marker_with_colons_widens_a_column_too_narrow_to_hold_it`
in `tests/test_units.py` runs the two commands from the item's `## Steps to reproduce` through
`python3 -m mdtab` — the same three-line document twice, differing only in the middle column's
delimiter cell — and asserts the middle column is 2 display columns wide with `---` and 3 with
`:-:`. It measures with the module's existing `pipe_columns` helper, so the measurement is
display width and not `len` (ADR-0002), and it checks every line of each output agrees on the
width rather than only the delimiter row.

**The docstring above it.** `WidthIndependenceTest`'s docstring read *"AC6 — a column's width is
the same whatever its marker says"*: the same false sentence in a third place, found while
planning, and it would now have sat directly above a test proving the opposite. It now names both
facts and both criteria — the width does not depend on the *alignment* a marker declares
(`WI-0002 AC6`), and it is not always the same whatever the marker *is*, because a delimiter cell
must stay writable (`WI-0001 AC12`, `WI-0001/Q-005`).

**The two documents.** `docs/architecture/overview.md`'s *"Where a cell's content sits in its
field"* bullet and `ADR-0007`'s `## Decision` item 4 each kept the true half of what they said
and handed the false half to the rule that actually owns it. Neither sentence was deleted: AC1
requires a reader of the overview's two bullets to be able to predict both commands, and silence
is what let the wrong answer stand for two items.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — the overview bullet no longer asserts it, does not contradict the "How wide a column is" bullet, cites something that supports it, and lets a reader predict both commands | The clause *"and no column's width depends on its marker"* is replaced by two sentences: the width does not depend on the *alignment* the marker declares `[src: ADR-0007; src: WI-0002 AC6]`, and the marker's colons reach the width through the minimum a delimiter cell must have, so `:-:` gives a 3-column field where `---` gives 2 `[src: WI-0001 AC12; src: WI-0001/Q-005]`. That second sentence points at the very next bullet rather than restating it, so the two read as one answer. | `sed -n '77,92p' docs/architecture/overview.md` shows the corrected bullet immediately above the unchanged "How wide a column is" bullet. The prediction holds against the tool: `printf 'a \| \| b\n---\|---\|---\nc \| \| d\n' \| python3 -m mdtab \| cat -A` → exit 0, `a \|  \| b$` (middle column 2); with `---\|:-:\|---` → exit 0, `a \|   \| b$` (middle column 3). The citations are `WI-0002 AC6` for the alignment half and `WI-0001 AC12` + `WI-0001/Q-005` for the floor half — the same two the corrected ADR cites. |
| AC2 — ADR-0007 decision 4 no longer asserts it; `status: accepted` is kept and the correction is recorded rather than the ADR superseded | Item 4 keeps *"`_column_widths` is not touched"*, which is its substance and is true. The clause after it now says what `WI-0002 AC6` says, and adds that the marker's colons already reached the width before WI-0002, through `WI-0001 AC12`, and that WI-0002 changed neither rule. `ADR-0009`'s four conditions all hold: (1) the decision is unchanged — no code conforming to v1 needs to move; (2) the removed text was false against `_column_widths`, demonstrably, by the command above; (3) the change-log row quotes the removed sentence in full; (4) `status` stays `accepted` and `version` is 2. | `sed -n '/^## Decision/,/^## Consequences/p' docs/architecture/adr/ADR-0007-*.md \| grep -c "does not depend on its marker"` → `0`. `grep -n '^- \*\*Status:\*\*' docs/architecture/adr/ADR-0007-*.md` → `12:- **Status:** accepted`. The v2 change-log row contains the removed sentence between `*"` and `"*` and cites `[src: ADR-0009]`. |
| AC3 — both documents carry a version bump and a change-log row naming this item | `docs/architecture/overview.md` frontmatter `version: 6`, top change-log row `\| 6 \| … \| implement \| BUG-0001 \| …`. `ADR-0007` frontmatter `version: 2`, top row `\| 2 \| … \| implement \| BUG-0001 \| …`. In both, the top row's version equals the frontmatter version, which `spec/doc-header.md` §3 requires. | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 5 item(s), 11 document(s)`, `0 errors, 0 warnings` — it is the validator that checks the version/change-log agreement. |
| AC4 — a test runs both commands and asserts 2 and 3; it fails if the floor is removed | **Superseded by the third pass**: the test is now `tests/test_fixtures.py`, `ProcessTest.test_a_marker_with_colons_widens_a_column_too_narrow_to_hold_it`, reading `width-marker-dashes` and `width-marker-colons` from `tests/fixtures/`. What follows described the second pass's version, whose assertions are unchanged. `tests/test_units.py`, `WidthIndependenceTest.test_a_marker_with_colons_widens_a_column_too_narrow_to_hold_it`. It asserts `middle_width(dashes) == 2` and `middle_width(colons) == 3`, where `middle_width` re-derives the width from `pipe_columns` on every line and fails if the lines disagree. | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 72 tests`, `OK`. **Sensitivity, run rather than assumed:** with line 175 of `mdtab/table.py` temporarily changed from `widths.append(max(width, needed + omitted))` to `widths.append(width)`, the suite reported `FAILED (failures=4)` and this test failed with `AssertionError: 2 != 3`. The mutation was reverted with `git checkout -- mdtab/table.py` and the suite returned to `Ran 72 tests … OK`; `git diff --name-only main` confirms nothing under `mdtab/` is on the branch. |
| AC5 — the test suite and `lint-claims --all` both exit 0 | Both run at the branch head, after the last commit. | `python3 -m unittest discover -s tests -t .` → exit 0 (`Ran 72 tests`, `OK`). `python3 .claude/agile-skills/scripts/lint-claims --all` → exit 0 (`checked the whole tree`, `0 errors, 0 warnings`). |
| AC6 — no file under `mdtab/` changes | The only source file touched is `tests/test_units.py`. | `git diff --name-only main` → `docs/architecture/adr/ADR-0007-alignment-is-placed-inside-the-cells-field.md`, `docs/architecture/overview.md`, `tests/test_units.py`, and four paths under `tracker/`. Filtering that list through `grep '^mdtab/'` matches nothing. |

## Deviations from the plan

1. **The regression test runs the two commands as a subprocess instead of calling `lay_out`.**
   **Resolved on the third pass** — the ADR-0005 tension this paragraph flagged was the review's
   finding 1, and the test now reads two fixture pairs from `tests/fixtures/` in
   `tests/test_fixtures.py`. The deviation from plan step 1 stands (the test runs the commands
   rather than calling `lay_out`, because that is AC4's wording); its cost does not. The rest of
   this paragraph is kept as it was written.
   Plan step 1 said to call `lay_out` twice on a four-line run shaped like
   `tests/fixtures/align-empty-cell.in.md`. AC4 says the test *"runs both commands from
   `## Steps to reproduce`"*, and those commands are `printf … | python3 -m mdtab` on a **bare**
   three-line table, not a piped four-line one. A criterion cannot be waived by a plan and cannot
   be amended by this skill, so the test was written to satisfy AC4's wording: it invokes
   `python3 -m mdtab` with exactly the item's two inputs. Everything else about step 1 is kept —
   the placement in `WidthIndependenceTest` beside the existing test, and the measurement through
   `pipe_columns` so ADR-0002 is honoured. The numbers are unaffected: 2 and 3 either way.
   Cost of the deviation: `test_units.py` gains `os`/`subprocess`/`sys` imports and a four-line
   `filtered()` helper, and one test in that file now exercises the process boundary, which its
   module docstring reserves for `tests/fixtures/` and `test_fixtures.py` (ADR-0005). That
   tension is real and is flagged here rather than resolved unilaterally; the alternative —
   putting the test in `test_fixtures.py`, whose own docstring says every document in it comes
   from `tests/fixtures/` — trades the same friction the other way and would separate the test
   from the docstring plan step 2 corrects.

2. **Plan steps 1 and 2 landed in one commit** (`fa9f067`) rather than two. The docstring is a
   description of the test directly beneath it; splitting them would have left one commit in
   which the class docstring contradicts its own contents.

Nothing else departed from the plan. Steps 3, 4 and 5 were executed as written, in order, and the
document corrections were made on the branch rather than on the trunk exactly as
`## Approach`'s last paragraph directs — which worked: `lint-claims --changed-since main` reported
`checked 2 document(s)` rather than the `checked no documents` the plan warned about.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 72 tests in 0.137s`, `OK`, at `44dde4d` |
| `lint-clean` | **pass** | `python3 -W error -m compileall -q mdtab tests` → exit 0 |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 5 item(s), 11 document(s)`, `0 errors, 0 warnings` |
| `every-criterion-has-a-test` | **pass** | Every row of the table above names a test function or an exact command with its output. AC1 and AC2 are document criteria and are demonstrated by commands over the documents plus the two `python3 -m mdtab` runs whose output AC1 requires a reader to be able to predict; AC4's sensitivity was demonstrated by mutation, not asserted. |
| `commits-reference-the-item` | **pass** | `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0001 wi/BUG-0001` → exit 0, `all 2 commit(s) on main..wi/BUG-0001 name BUG-0001` |
| `no-unplanned-scope` (advisory) | **pass** | Seven files change. `tests/test_units.py` is plan steps 1–2; `docs/architecture/overview.md` is step 3; `ADR-0007` is step 4; the four `tracker/` paths are this item's own record and the board. Every hunk traces to a plan step. |
| `claims-are-sourced` | **pass** | `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, `checked 2 document(s) changed since main`; and `--all` → exit 0, `0 errors, 0 warnings` |

## What I did not do

**On the third pass, specifically:**

- **I did not touch `docs/`.** The review's finding 1 is about a test file; AC1, AC2 and AC3 were
  passed by `verify` against `overview.md` v7 and `ADR-0007` v2, and re-editing a passed document
  would invalidate those ticks for nothing.
- **I did not correct `verify-report.md`'s bare-table sweep numbers**, which the review's finding
  2 records: it calls the printed leading-field widths *"widths 1, 2, 2, 3"* where
  `_column_widths` computes 2, 3, 3 and 4 for that table, the difference being the guard space
  the missing outer pipe drops. That report belongs to `verify` and the next verification will
  write it; the finding is in `review.md` so it reaches whoever does.
- **I did not rename `ProcessTest`.** Its docstring now names both reasons a test lands there,
  which is what stops the class from claiming to hold one test while holding two; renaming it
  would touch the AC1 tests, which no criterion here covers.
- **I did not add the fixture pairs to `UNTOUCHED`.** They contain a table mdtab lays out, so
  `ALIGNED` is where they belong, and putting a laid-out fixture in `UNTOUCHED` would assert its
  two halves are identical, which they are not.

**From the earlier passes, still true:**

- **I did not tick any acceptance criterion.** `spec/work-item.md` §95 gives that to `verify`,
  which must demonstrate each one itself. All six boxes in `item.md` are unticked.
- **I did not touch `mdtab/` on the branch** — AC6 — including not deleting `_column_widths`'
  floor, which is the "fix" the false sentence invites and which the mutation above shows would
  break four tests.
- **I did not amend `WI-0002 AC6` or reopen any closed item.** It says *alignment*, it is
  correctly ticked, and every corrected sentence narrows to it.
- **I did not audit the rest of `docs/` again.** `tracker/items/EP-001/artifacts/review.md`
  records the fifteen-claim audit that produced this item.
- **I did not correct the two remaining live-ish restatements outside `docs/`, because they are
  history rather than claims.** The plan's last risk asks for a tree-wide sweep for a fourth copy
  of the sentence. It was run:
  `grep -rn "width does not depend on its marker\|width is the same whatever its marker\|no column's width depends on its marker" --include='*.md' --include='*.py' .`
  Every remaining hit is one of: the verbatim quotes the two change-log rows are *required* to
  carry (`ADR-0009` condition 3); `ADR-0009`'s own `## Context` and `## Decision`, which quote the
  sentence in order to rule on it; this item's `item.md`, `plan.md` and `journal.md`; `EP-001`'s
  `journal.md` and `review.md`, which record finding it; and
  `tracker/items/WI-0002/artifacts/review.md` line 64, which records that `verify` checked the
  sentence against the code and judged it to hold. That last one is a **wrong verification record
  on a closed item** — it checked the guard-space half and the four-marker layout, neither of
  which reaches the width floor. Correcting it would mean rewriting a closed item's evidence,
  which this item's `## Out of scope` forbids and which no criterion here covers, so it is left
  alone and named here instead. Nothing under `mdtab/` restates the sentence.
- **I did not resolve the placement tension recorded as deviation 1.** If `verify` or
  `review-close` judges that a process-level test does not belong in `test_units.py`, moving it to
  `test_fixtures.py` is a one-hunk change and nothing else depends on where it lives.
