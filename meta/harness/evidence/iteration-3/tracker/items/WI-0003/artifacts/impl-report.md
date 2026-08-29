# Implementation report — WI-0003

Branch `wi/WI-0003`. Two `implement` executions have run against it and this report covers both.

- **The code**, built up to `f74d201`, is `## What was built` through `## What I did not do` below.
  Nothing in those sections changed in the second execution; `git diff 5672ac2..HEAD -- mdtab/` is
  empty, and the suite is the same 71 tests.
- **The documents**, at `2c39bc4`, are `## Second execution — the D7/D12 send-back` at the end.
  Every gate reported in that section was run on `2c39bc4`, the current branch head.

This report also replaces the partial one written when the item suspended on `Q-002`; that
execution's own record is in `journal.md`.

## What was built

`mdtab/scan.py` gained `shared_prefix(contents) -> str | None`: the longest common prefix, byte
for byte, of a run's `line_prefix` values, returned only when what every line carries past it is
space characters and nothing else. `lay_out`'s rule 2 in `mdtab/table.py` calls it and strips the
run's shared prefix instead of requiring every line to repeat one. That is the whole behaviour
change — one new function and two lines.

Nothing downstream needed to know, as the plan predicted. `is_delimiter_row` already strips its
cells, so a delimiter row that is the deepest-indented line is still recognised;
`has_leading_pipe` reads the body it is handed, so a row with extra spaces before its `|` has no
leading pipe while its neighbours do and rule 4 refuses that run; `_render_cell` trims each cell,
so the spaces that are now part of a first cell are removed like any other cell padding.

The commits: `a502bc8` the function and its unit tests, `f32d681` the rule, the fixtures and the
two tests plan steps 5 and 6 name, `f74d201` the correction `Q-002` produced, and two tracker
commits carrying the record.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `shared_prefix` is the relaxed rule, in one function, called from one place | `tests/test_units.py::SharedPrefixTest`, six tests: the five values plan step 1 names (including the tab and `>` refusals), the "prefixes, not raw lines" case, and the empty run |
| AC2 | mdtab recognises the bare right-aligned table it lays out itself | fixture `refeed-bare-first-column`; `PaddingPlacementTest::test_ac10_…`'s final assertion, now `assertEqual(lay_out(laid_out), laid_out)`; `printf '   a \| bbbbb\n----:\|--\nxxxx \| y\n' \| python3 -m mdtab` → `   a \| bbbbb` / `----:\|------` / `xxxx \| y    `, the trailing spaces confirmed with `cat -A` |
| AC3 | the same after a `>` and after an indent | fixtures `refeed-blockquote-first-column`, `refeed-list-indent-first-column`; both of AC3's two-step transcripts run, and both steps produce the criterion's bytes |
| AC4 | idempotence, on every document this item touches | `FixtureRoundTripTest::test_ac6_running_the_tool_on_its_own_output_changes_nothing` over all 40 pairs; and `python3 -m mdtab` twice with `diff` on each of the six laid-out inputs — six fixed points, no diff |
| AC5 | uneven leading spaces are tidied to the shared prefix | fixtures `uneven-leading-spaces` (`  a \| b`/`---\|---`/`  ccc \| d` → `a   \| b`/`----\|--`/`ccc \| d`), `uneven-delimiter-deepest`, `uneven-blockquote-space`; all three of AC5's documents, all three matching byte for byte |
| AC6 | a tab or a `>` still refuses the run | fixtures `quote-depth` (new) and `tab-prefix` (existing, unedited), both returned byte-for-byte; `SharedPrefixTest::test_a_tab_one_line_has_and_another_does_not_is_no_shared_indent` and `…test_a_difference_in_quote_depth_is_no_shared_indent` |
| AC7 | outer-bar tables unaffected, refused by rule 4 rather than rule 2 | `ragged-prefix` still returned unchanged (it is in `UNTOUCHED`); the extra-space assertion now in `test_rule_4_a_run_whose_rows_disagree_about_their_outer_pipes`; `outer-pipes`, `blockquote-table`, `list-indent-table`, `mixed-pipes` all pass unedited |
| AC8 | no shipped document changed | `git diff --name-status main..wi/WI-0003 -- tests/fixtures/` → 14 files, every one status `A`; no `.out` of the 33 shipped pairs modified. `python3 -m unittest tests.test_fixtures` passes |
| AC9 | the suite passes with exactly the two tests AC9 names changed | `python3 -m unittest discover -s tests -t .` → `Ran 71 tests`, `OK`. `git diff main..wi/WI-0003 -- tests/` shows changed assertions in `test_ac10_…` (one line) and `test_ac11_…` (its two comparison expressions) and nowhere else; the seven other changed assertion lines are the new `SharedPrefixTest`, and `test_rule_2_…`'s extra-space assertion is relocated to `test_rule_4_…` character-for-character |
| AC10 | silent, exit 0 | each of the seven new fixture inputs through `python3 -m mdtab` with stderr captured: `exit=0 stderr=<empty>`, seven for seven; `ProcessTest`'s two tests |

## Deviations from the plan

1. **Three extra citation corrections in `mdtab/table.py`.** Step 2 authorised updating rule 2's
   own comment to cite ADR-0008. `has_leading_pipe`'s docstring ("a line with its AC15 prefix
   already stripped"), `_outer_style`'s "(AC14, ADR-0003 rule 4)" and `lay_out`'s docstring were
   corrected too: each describes a rule this change reverses or restates, and
   `has_leading_pipe`'s is the sentence AC7's whole argument rests on.
2. **`tests/test_fixtures.py`'s hand-written maps had to change.** Step 3 said pairs are
   discovered by name so no test code changes. True of `FixtureRoundTripTest`, but `ALIGNED` and
   `UNTOUCHED` are written by hand and a laid-out fixture missing from `ALIGNED` is checked
   against the wrong rule. The six laid-out pairs went into `ALIGNED` and `quote-depth` into
   `UNTOUCHED`. `answer-questions` corrected step 3 to say so.
3. **A step 7 that did not exist when the plan was written.** `test_ac11_…` failed on
   `uneven-blockquote-space`, which neither the plan nor AC9 expected. That was `Q-002`, answered
   by `answer-questions`: the test compares a raw line's fields and so counts a `>` prefix as part
   of the first cell, which was exact only under the rule this item reverses. The plan gained
   step 7 and AC9 gained a second named test; the gates step became step 8.

## Gates

| gate | result |
|---|---|
| `tests-pass` | pass — `python3 -m unittest discover -s tests -t .` → `Ran 71 tests`, `OK`, exit 0 |
| `lint-clean` | pass — `python3 -W error -m compileall -q mdtab tests` exit 0 |
| `workspace-valid` | pass — `validate-workspace` 0 errors, 0 warnings |
| `every-criterion-has-a-test` | pass — all ten rows above name a test function or an exact command with its output |
| `commits-reference-the-item` | pass — `check-commit-refs WI-0003 wi/WI-0003`: all 5 commits name WI-0003 |
| `no-unplanned-scope` | pass (advisory) — every hunk traces to a plan step; the three deviations above are recorded rather than silent |
| `claims-are-sourced` | pass — `lint-claims --changed-since main` 0 errors, 0 warnings |

All seven were run on the branch head, after the last change.

## What I did not do

- **I did not tick any acceptance criterion in `item.md`.** They are `verify`'s to tick.
- **I did not touch AC9 or any other criterion myself.** AC9's checking clause was amended by
  `answer-questions` answering `Q-002`, which is one of the two skills permitted to; the
  amendment and its basis are in `questions/Q-002.md` and in this item's journal.
- **I did not repair anything else the change made stale.** ADR-0003 is still cited in
  `tests/test_units.py`'s module docstring ("Each rejection rule of ADR-0003 gets its own test
  here") and in `tests/test_fixtures.py`'s `align-unrecognised` comment. Both sentences are still
  true of the rules they describe — rules 1, 3 and 4 are reproduced unchanged in ADR-0008 — and
  correcting citations beyond the ones this item's own change falsified would be tidying, not
  this item's work.
- **One thing a reader should know about the corrected test.** `without_indent` removes each
  line's *own* leading run of space, tab and `>`, not the run's shared prefix, which a
  document-level test cannot know. It is therefore a superset strip, and it was checked not to
  have become a tautology: mutating `_render_cell` to drop the last character of every cell makes
  `test_ac11_…` fail on 24 fixtures.


---

## Second execution — the D7/D12 send-back

`review-close` rejected the item to `in-progress` at 2026-08-28T22:02:29Z. It accepted the change —
every hunk mapped to a plan step, no ADR contradicted, the trial merge at `3ea3147` green — and
failed it on **D7** (documents the change invalidated have been updated, with a version bump and a
change-log row) and **D12** (every claim in `docs/` about the behaviour this item touched is still
true). `review.md` `## Verdict` lists three edits that clear it. Those three, and nothing else, are
what this execution did.

### What was built

Nothing under `mdtab/`. `git diff 5672ac2..HEAD -- mdtab/` is empty and the suite is unchanged at
71 tests, which is the point: the send-back was about what the documents say, not about what the
code does.

| # | file | what changed | which finding |
|---|------|--------------|---------------|
| 1 | `docs/architecture/overview.md` | §"A property the tool lost and **is getting back**" → "…and **got back**", rewritten in the past tense against the merged behaviour. The sentence `review.md` quotes against it — *"the code lands with [src: WI-0003], and until it does, the paragraph above still describes what the tool does"* — is gone, and so is line 111's "left alone today". The section now states the rule as implemented, cites `mdtab/scan.py` for it, and gains a sentence the old text never had: a run whose lines differ by a **tab** or by a `>` is still not a table. `version: 5`, change-log row | F1 |
| 2 | `docs/architecture/overview.md` | the pipeline diagram's `[ADR-0003]` at line 30 and the copy-through paragraph's `[src: ADR-0003]` at line 41 → `ADR-0008` | F2 |
| 3 | `docs/product/vision.md` | "*one whose rows disagree … or about how far they are indented*" → "*or about their indentation in a way it cannot make sense of*", plus a new paragraph saying where the line now falls — spaces tidied, tabs and `>` refused — quoting the stakeholder's own words from `Q-001` rather than paraphrasing. Line 44's `[src: ADR-0003]` → `ADR-0008`. `version: 5`, change-log row | F3 |
| 4 | `docs/product/vision.md` | "## Open at the time of writing" rewritten: it carried the indentation question as one that *might need asking*, when it was asked as `Q-001` and answered on 2026-08-28 **against its own premise**. The section now records the answer and states that nothing is waiting to be asked | F3 |
| 5 | `tests/test_units.py:5` | module docstring "*Each rejection rule of ADR-0003…*" → ADR-0008, which is what `RejectionTest`'s own docstring in the same file has said since `f32d681` | F4 |

The stakeholder quotation added to `vision.md` was copied from `questions/Q-001.md` `## Answer` and
checked word for word against it, not retyped from the summary in `item.md` `## Notes`.

### Acceptance criteria evidence

Unchanged. This execution changed no behaviour, so the evidence in `## Acceptance criteria evidence`
above stands as written, and `verify` re-confirmed all ten of it at `0129b1d` — a commit this
execution has not moved past in any file under `mdtab/` or `tests/fixtures/`.

Two of the ten are worth restating because this execution touched a file they name:

| AC | still satisfied by | re-checked how |
|----|--------------------|----------------|
| AC1 | `tests/test_units.py::SharedPrefixTest`, six tests | the file's module **docstring** changed; no test, name or assertion did. `git diff 5672ac2..HEAD -- tests/test_units.py` is five lines, all inside the docstring |
| AC9 | `python3 -m unittest discover -s tests -t .` → `Ran 71 tests`, `OK` | re-run on `2c39bc4`. The two pre-existing tests AC9 names are untouched by this execution, and no third one changed |

### Deviations from the plan

**One, and it is the finding itself.** `plan.md`'s eight steps contain no step for updating
`docs/`. That is what `review.md` identifies as where this went missing — `overview.md`'s own
change-log row 4 recorded the document as describing a tool "*and that the code has not landed
yet*", and nobody scheduled the edit for when it did.

So the authority for this execution's diff is not a plan step. It is `review.md`'s send-back list,
which `SKILL.md` step 1 makes authoritative for a resumed run — *"If the history's last row shows a
send-back … your job is that defect, not the whole item."* The `no-unplanned-scope` gate below is
recorded against that list rather than against the plan, and each of the five changes above names
the finding it answers.

`plan.md` was **not** amended to add a ninth step. Editing the plan is `plan`'s or
`answer-questions`', not this skill's, and nothing here needed a decision — the review named the
files, the lines and the required content.

### Gates

Every gate re-run on `2c39bc4`, the branch head, after the last change.

| gate | result |
|---|---|
| `tests-pass` | **pass** — `python3 -m unittest discover -s tests -t .` → `Ran 71 tests in 0.087s`, `OK`, exit 0 |
| `lint-clean` | **pass** — `python3 -W error -m compileall -q mdtab tests` → exit 0 |
| `workspace-valid` | **pass** — `validate-workspace .` → `4 item(s), 10 document(s)`, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** — all ten rows of `## Acceptance criteria evidence` still name a test function or an exact command with its output; this execution invalidated none of them and moved no file they depend on |
| `commits-reference-the-item` | **pass** — `check-commit-refs WI-0003 wi/WI-0003` → `all 9 commit(s) on main..wi/WI-0003 name WI-0003`, exit 0 |
| `no-unplanned-scope` | **pass** (advisory) — five changes, each traced above to one of `review.md`'s four findings; nothing else in the diff. See the deviation above for why the trace is to the review rather than to a plan step |
| `claims-are-sourced` | **pass** — `lint-claims --changed-since main` → `checked 2 document(s) changed since main`, 0 errors, 0 warnings. Note that this gate had **nothing to check** on the previous execution (`checked no documents changed since main`), because `plan` committed ADR-0008 and the overview edits on the trunk before the branch was cut. It is only non-vacuous now because this execution is the first to change a document *on the branch* — which is exactly the hole `review.md` had to audit by hand |

### What I did not do

- **I did not touch `mdtab/`,** and the review said not to: *"No code change is required and none
  should be made."*
- **I did not amend `plan.md`** to add the documentation step it is missing. It is not this skill's
  artifact. Whether the plan template should carry a "update the documents this change invalidates"
  step by default is a real question about the toolkit and it is raised in the journal rather than
  acted on here.
- **I did not touch `vision.md`'s historical change-log rows**, which still cite ADR-0003. Row 3
  records what `answer-questions` concluded in WI-0001, when ADR-0003 was current; rewriting it
  would falsify a record of what was believed at the time, which is the same rule that made
  ADR-0003 superseded rather than edited (`spec/doc-header.md` §4).
- **I did not re-verify the ten acceptance criteria.** That is `verify`'s, and it is cheap here:
  `check-verify-freshness` treats `docs/` as record, so the code verification at `0129b1d` should
  still stand.
