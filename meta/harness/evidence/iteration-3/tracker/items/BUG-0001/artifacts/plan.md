# Plan — BUG-0001 Two documents claim a column's width does not depend on its marker; it does

## Problem

Three places in this project say, as an absolute, that a column's width is independent of the
alignment marker in its delimiter cell: `docs/architecture/overview.md`'s *"Where a cell's content
sits in its field"* bullet, `ADR-0007`'s `## Decision` item 4, and — found while planning, not at
filing — the docstring of `WidthIndependenceTest` in `tests/test_units.py`. All three are false.
`_column_widths` in `mdtab/table.py` raises a column's width so that its delimiter cell can still
be written, and how wide that cell must be is one dash plus one column per `:` the marker carries;
a column narrow enough for that floor to bind is wider with `:-:` than with `---` from identical
content. The change is to the words, for a developer reading them, under a hard constraint: **no
file under `mdtab/` may change** (AC6). The tool is correct. The floor is what `WI-0001 AC6`
forces, `tests/fixtures/align-empty-cell` already pins it as expected output, and deleting it —
the fix the false sentence invites — would stop `mdtab | mdtab` being a fixed point for a
degenerate column.

## Approach

Three moves, in this order, because each supplies what the next needs.

**First, pin the behaviour.** A new test in `tests/test_units.py` asserts what the corrected
sentences will say: the same run laid out twice, once with `---` on the narrow column and once
with `:-:`, and the second is exactly one display column wider. It goes in `WidthIndependenceTest`,
beside the existing test rather than in a class of its own, because the two together are the whole
truth about that class's subject: markers do not move a column that has room, and do widen one
that does not. Writing it first means the corrected prose is describing something that runs.

**Second, correct the three statements**, each to say the true and narrower thing rather than
merely dropping the false one. Deleting the clause would leave the overview's list silent about a
question a reader arrives with, and silence is what let the wrong answer stand for two items. Each
corrected sentence distinguishes the two things the false one conflated:

- a column's width does not depend on the **alignment** the marker declares — this is
  `WI-0002 AC6`, it is true, and it is what the existing `WidthIndependenceTest` test proves;
- a column's width *can* depend on the **marker's colons**, through the floor in the
  "How wide a column is" bullet, which is `WI-0001 AC12` as amended by `WI-0001/Q-005`.

**Third, make the correction to `ADR-0007` legal.** `spec/doc-header.md` §4 says an ADR is never
edited to change its decision. ADR-0007's decision is not changing — only a false clause of its
justification — and there was no rule for that case, so this plan records one: `ADR-0009`, written
by this execution, permits an in-place correction under four conditions and requires the removed
sentence to be quoted verbatim in the change log. Superseding ADR-0007 was the alternative and is
rejected there, at length: its decision is still in force, and marking it `superseded` would send
every reader of the several `[src: ADR-0007]` citations looking for a change to the system that
never happened.

**What `implement` must not do**, stated here because the false sentence is an argument for doing
it: do not remove `needed` or the `max(...)` from `_column_widths` to make the old wording true.
AC6 forbids touching `mdtab/`, and `tests/fixtures/align-empty-cell.out.md` would fail if you did.

**A note on where the documents are edited.** `ADR-0009` is committed by this execution, on
`main`, before any branch exists — so `lint-claims --changed-since main`, which is
`claims-are-sourced` for every skill after this one, will not see it. That is a known toolkit
defect, recorded in `WI-0003`'s `## Notes` and again in `EP-001/artifacts/review.md` Finding 2.
The three corrections in steps 2–4 are deliberately left for `implement` to make **on the branch**,
where the gate does see them, rather than being made here as a tidy-up. Run
`lint-claims --all` as well; `--changed-since main` reporting `checked no documents` is not a pass.

## Steps

1. **Add the regression test.** In `tests/test_units.py`, class `WidthIndependenceTest`, add a
   test beside `test_the_pipes_land_in_the_same_places_under_all_four_markers`. It calls `lay_out`
   twice on a four-line run whose middle column's cells are all empty — the shape of
   `tests/fixtures/align-empty-cell.in.md` — once with `---` for that column's delimiter cell and
   once with `:-:`, everything else identical. It asserts the middle column's field is 2 display
   columns wide in the first and 3 in the second, using the module's existing `pipe_columns`
   helper so the measurement is display width and not `len` (`ADR-0002`). Afterwards
   `python3 -m unittest discover -s tests -t .` reports 72 tests and exits 0.

2. **Correct `tests/test_units.py`'s `WidthIndependenceTest` docstring.** It reads *"AC6 — a
   column's width is the same whatever its marker says"*, which is the same false sentence in a
   third place, and it now sits directly above a test proving the opposite. Replace it with one
   naming both facts and both criteria: the width is the same whatever **alignment** the marker
   declares (`WI-0002 AC6`), and it is not always the same whatever the marker **is**, because of
   the floor (`WI-0001 AC12`). Rename neither test; the existing name is accurate about what it
   checks. Afterwards the class's docstring and its two tests agree.

3. **Correct `docs/architecture/overview.md`.** In `## Rules that live in exactly one place`,
   bullet *"Where a cell's content sits in its field"*, replace the final clause *"and no column's
   width depends on its marker"* with the narrower true statement and a pointer to the
   "How wide a column is" bullet four lines below, so the two bullets read as one answer instead
   of two. Its citations must support what the new sentence says: `WI-0002 AC6` for the alignment
   half, and `WI-0001 AC12` or `ADR-0009` for the pointer. Bump the frontmatter to version 6, set
   `updated`, `updated-by: implement`, `updated-for: BUG-0001`, and add a change-log row quoting
   the removed clause. Afterwards a reader of the two bullets can predict the output of both
   commands in the item's `## Steps to reproduce`.

4. **Correct `ADR-0007`**, under `ADR-0009`'s four conditions. In `## Decision` item 4, keep
   *"`_column_widths` is not touched"* — it is true and it is item 4's substance — and replace
   *"A column's width does not depend on its marker [src: WI-0002 AC6]"* with what `WI-0002 AC6`
   actually says, noting that the marker's colons do reach the width through the floor and that
   WI-0002 changed neither. `status` stays `accepted`; version becomes 2; `updated-by: implement`,
   `updated-for: BUG-0001`; the change-log row **quotes the removed sentence in full** and cites
   `ADR-0009` as the rule permitting the in-place edit. Afterwards ADR-0007 contains no false
   statement and no `[src: ADR-0007]` citation elsewhere has moved.

5. **Run the gates and record them.** `python3 -m unittest discover -s tests -t .` → exit 0;
   `python3 -W error -m compileall -q mdtab tests` → exit 0;
   `.claude/agile-skills/scripts/lint-claims --all` → exit 0 (and run `--changed-since main` too,
   for the contract, knowing what its verdict is worth); `git diff --stat main` shows no path
   under `mdtab/`.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — the overview bullet no longer asserts it, does not contradict the "How wide a column is" bullet, cites something that supports it, and lets a reader predict both commands | 3 | Read the two bullets, then run both commands from `## Steps to reproduce` and check the prediction holds: `---` gives a 2-wide middle column, `:-:` gives 3. `lint-claims --all` exits 0, so whatever absolute the new sentence carries has a citation that resolves; that the citation *supports* it is `verify`'s read, against `WI-0002 AC6` and `WI-0001 AC12`. |
| AC2 — ADR-0007 decision 4 no longer asserts it; the ADR keeps `status: accepted` and records the correction rather than being superseded | 4 | `grep -n "does not depend on its marker" docs/architecture/adr/ADR-0007-*.md` returns nothing; `grep -n "^- \*\*Status:\*\*" ` on the same file still reads `accepted`; its change log's top row quotes the removed sentence verbatim and cites `ADR-0009`, whose four conditions can be checked one by one against the diff of that file. |
| AC3 — both documents carry a version bump and a change-log row naming this item | 3, 4 | `docs/architecture/overview.md` frontmatter `version: 6` with a v6 row naming BUG-0001; `ADR-0007` frontmatter `version: 2` with a v2 row naming BUG-0001. In both, the top change-log row's version equals the frontmatter version (`spec/doc-header.md` §3), which `validate-workspace` also checks. |
| AC4 — a test runs both cases and asserts 2 columns and 3; it fails if the floor is removed | 1, 2 | `python3 -m unittest discover -s tests -t .` → 72 tests, exit 0. Sensitivity, run by `verify` and not assumed: delete `needed` from `_column_widths`' `max(...)` in a scratch copy, re-run, and the new test fails; restore. Step 2 is mapped here because AC4 asks the test to pin *the behaviour the corrected sentences describe*, and a class docstring asserting the opposite two lines above it un-pins exactly that. |
| AC5 — the test suite and `lint-claims --all` both exit 0 | 5 | The two commands, with their exit codes quoted in `impl-report.md`. |
| AC6 — no file under `mdtab/` changes | constraint on 1–5 | `git diff --name-only main` on the branch lists only `tests/test_units.py`, `docs/architecture/overview.md`, `docs/architecture/adr/ADR-0007-*.md` and files under `tracker/`. Nothing under `mdtab/`. |

## Assumptions

- **The corrected sentences will be judged on whether they are true, not on their wording.** This
  plan fixes what each must stop saying and what it must let a reader predict, and leaves the
  phrasing to `implement`. Reversing this costs one round trip: if `verify` finds a corrected
  sentence still misleading, the item comes back with the specific sentence quoted. Nothing else
  depends on the wording, so reversal is one file and no interface.
- **Step 2 belongs to this item.** The test docstring was not named in BUG-0001 because nobody had
  read it when the bug was filed; it is the same false sentence in a third place, and it would sit
  directly above the new test contradicting it. The judgement is that correcting it is part of AC4
  rather than new scope — a criterion cannot be amended by this skill, so it is recorded here as a
  judgement rather than as a new AC. Reversing it costs one line in one file, and if a reviewer
  disagrees the docstring can be restored and filed separately.
- **`WI-0002 AC6` is correct as written and is not amended.** It says *alignment*, its tick is
  supported, and `WidthIndependenceTest`'s existing test is its evidence. Every corrected sentence
  narrows to it rather than around it. Reversal would mean re-opening a closed, verified item,
  which is not cheap — which is precisely why this plan does not touch it.

## Decisions and ADRs

| decision | route | where |
|----------|-------|-------|
| Correct ADR-0007 in place rather than superseding it, keeping `status: accepted`, under four stated conditions | decided (option 3 of the preference order was not needed: the record was silent, the choice is reversible, and it forces no change to any code) | `ADR-0009` — created by this execution, with options A/B/C, their costs and risks, and reversibility |
| Correct the three sentences rather than deleting the clause | documented | `spec/dor-dod.md` DE6 requires claims in `docs/` to be *true*, not absent; the overview's list exists to answer where each rule lives, and BUG-0001's `## Summary` records that the silence is what let the wrong answer stand. Recorded under `## Approach`, not as an ADR: no alternative is worth naming beyond deletion, which the AC1 wording already excludes by requiring a reader to be able to predict both commands. |
| Write the regression test before the prose | documented | `spec/dor-dod.md` RB5 and AC4. Recorded here; not an ADR, because ordering two steps of one item is not an architectural commitment. |
| Leave the three document corrections to `implement`, on the branch | decided | `## Approach`, last paragraph — so `lint-claims --changed-since main` has something to read. Reversible at zero cost: if `implement` prefers, nothing breaks by the corrections arriving in a different commit, as long as they arrive on the branch. |
| Do not touch `mdtab/` | documented | AC6, and `WI-0001 AC6` with `tests/fixtures/align-empty-cell.out.md` as the standing evidence that the floor is intended behaviour. |

## Scaffolding

None. This execution created no file outside `tracker/` and `docs/`.

## Risks

- **`implement` reads the false sentence as a specification and "fixes" the code.** It is a
  plausible reading — two documents and a test docstring all say the width should not depend on
  the marker — and the result would be a green suite except for
  `tests/fixtures/align-empty-cell`, plus a broken idempotence property nobody would notice until
  a degenerate column appeared. Guarded three ways: AC6 forbids a diff under `mdtab/`, step 5
  checks it mechanically, and `## Approach` names the temptation.
- **The correction is made to the overview and not to ADR-0007, or vice versa.** Then the two
  disagree, which is worse than today, where they agree and are both wrong. AC1 and AC2 are
  separate criteria for this reason, and step 4 is not optional.
- **The change-log row for ADR-0007 says "corrected a wrong sentence" without quoting it.**
  Condition 3 of `ADR-0009` exists precisely because this is the shortcut under time pressure, and
  taking it destroys the evidence the whole approach relies on. AC2's demonstration checks the
  quote is there.
- **The new test is written so loosely that it passes with the floor removed** — for instance by
  asserting only that the two outputs differ. AC4's demonstration requires the mutation to be run,
  not assumed, so this is caught by `verify` rather than by hope.
- **A fourth copy of the sentence exists somewhere nobody has looked.** The termination review
  audited fifteen absolute claims across `docs/` and found three copies of this one; it did not
  audit `tests/` or `tracker/`, and a copy in a closed item's artifacts would be history rather
  than a live claim. `verify` should grep the tree for the phrase before ticking AC1.

## Out of scope for this item

- **Changing `_column_widths`, or anything else under `mdtab/`.** AC6.
- **Amending `WI-0002 AC6`,** or re-opening any closed item. See `## Assumptions`.
- **Auditing the rest of `docs/` again.** `tracker/items/EP-001/artifacts/review.md` records the
  fifteen-claim audit that produced this item; repeating it here would duplicate work that is
  already written down, and DE6 will be applied again when the engagement next reaches rest.
- **Fixing `lint-claims`' vacuous `--changed-since` pass, or the `plan`-commits-on-the-trunk
  ordering that causes it.** Both are defects in the toolkit, not in mdtab. They are recorded in
  `EP-001/artifacts/review.md` Findings 2 and in `WI-0003`'s `## Notes`; this plan works around
  them by running `--all` and by leaving the document edits to the branch.
- **The five caveats the stakeholder declined at sign-off.** No README, no `--help`, no
  diagnostics, multi-codepoint emoji, large documents, older interpreters — all refused in terms,
  recorded in `docs/product/vision.md` v6, and none of them is this item.
