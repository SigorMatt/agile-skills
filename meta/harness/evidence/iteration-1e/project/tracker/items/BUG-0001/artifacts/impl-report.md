# Implementation report — BUG-0001

## What was built

Two citation markers and a version bump. No code, no tests, one file.

`docs/product/vision.md` went from version 3 to **4**. The paragraph that says the product
deliberately has no per-person amounts and no weights now ends its sentence with a marker naming
`WI-0001/Q-001` and `expenses/store.py`; the paragraph that says a mistaken record cannot be
edited in place now ends its sentence with a marker naming `WI-0001/Q-003` and
`expenses/cli.py`. Each pair is deliberate: the question says why the product is that way, the
file shows that it is [src: tracker/items/BUG-0001/artifacts/plan.md].

Nothing else about either paragraph changed. The bracketed question references the paragraphs
already carried — `(`WI-0001/Q-001`)`, `(`WI-0001/Q-002`)`, `(`WI-0001/Q-003`, WI-0004)` — are
still there, which the plan asks for and which step 5's check is about: removing one would take
away the backticked name the paragraph makes its absolute claim *about*, so the linter would stop
examining the paragraph rather than accept it as sourced [src: BUG-0001].

The front matter records `version: 4`, `updated-by: implement`, `updated-for: BUG-0001`, and the
change log gained the matching top row. `updated-by: implement` is a recorded departure from the
methodology's writer table, decided before this execution began and not by it [src: ADR-0009].

Branch `wi/BUG-0001`, from `main` at `7f5ac6c` — the commit carrying the plan and ADR-0009. One
commit: `1235e19`.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — `lint-claims --all` exits 0 with 0 errors and 0 warnings | both flagged paragraphs now carry a citation that resolves | `python3 .claude/agile-skills/scripts/lint-claims --all` → `lint-claims: checked the whole tree under /home/msi/agile-skills-throwaway/expenses-1e`, `lint-claims: 0 errors, 0 warnings`, `exit=0`. Run again after the two injections below, on the restored tree, with the same result |
| AC2 — the document still says the same two things, in the same two paragraphs; nothing removed or softened | the edit is additive inside each paragraph, plus a line rewrap in the first one | `git diff main..wi/BUG-0001 -- docs/product/vision.md`: 9 insertions, 8 deletions, in three hunks — the front matter, the two paragraphs, and the new change-log row. **Not one line of prose is deleted without being re-added**: the second paragraph's deletion is `re-record.` returning as `re-record <marker>.`, and the first paragraph's three deleted lines return as three lines with the same words in the same order, rewrapped because the marker made one line too long for this document's width. Both sentences, quoted from the file afterwards: *"The product deliberately has no per-person amounts and no weights: an uneven bill is two entries, not one complicated one"* and *"It cannot be edited in place: the stakeholder was offered both and chose deletion, so a correction is a delete and a re-record"* |
| AC3 — front matter at `version: 4` with a matching change-log row | plan step 3 | the front matter reads `version: 4`, `status: current`, `updated: 2026-08-27T02:17:05Z`, `updated-by: implement`, `updated-for: BUG-0001`; the change log's top row begins `\| 4 \| 2026-08-27T02:17:05Z \| implement \| BUG-0001 \|` and describes the change in terms a reader can act on. The `4` in the row and the `4` in the header are the same number, which is what the rule asks |
| AC4 — `validate-workspace .` exits 0 with 0 errors | every marker this item wrote resolves, in `vision.md` and in this item's own artifacts | `python3 .claude/agile-skills/scripts/validate-workspace .` → `checked 7 item(s), 11 document(s)`, `0 errors, 0 warnings`, `exit=0` |

### The check that AC1 did not pass by the linter falling silent

Plan step 5, done twice — once per marker — with the file restored and checksummed each time.
This is the one way this fix could look right while sourcing nothing, so it is evidence rather
than a note. The linter's `hint:` lines are elided below because they contain the marker syntax
with a placeholder inside it, which does not resolve and would fail AC1 if quoted here — the same
trap `## Notes` warns about and the same one this item's own plan hit while being written.

- **Marker 1 removed** (the equal-split paragraph): `lint-claims --all` → `exit=1`,
  `docs/product/vision.md:31: ERROR [claim.unsourced] an absolute claim ('no') about
  'WI-0001/Q-001' with no citation`, `1 error, 0 warnings`. Restored from a copy taken
  beforehand; `md5sum -c` → `docs/product/vision.md: OK`.
- **Marker 2 removed** (the deletion paragraph): `lint-claims --all` → `exit=1`,
  `docs/product/vision.md:38: ERROR [claim.unsourced] an absolute claim ('cannot') about
  'WI-0001/Q-003' with no citation`, `1 error, 0 warnings`. Restored; `md5sum -c` → `OK`.
- **Restored tree:** `lint-claims --all` → `0 errors, 0 warnings`, `exit=0`.

Each marker is therefore load-bearing on its own line, and neither paragraph slipped out of the
linter's attention.

## Deviations from the plan

- **Plan step 1 says to change no other word of the paragraph. Three lines of it were
  rewrapped.** Adding the marker made the line 141 characters long in a document that wraps at
  about 98, so the sentence boundaries moved across lines 34 to 36. No word was added, removed or
  reordered — the diff's three deleted lines and three added lines contain the same prose — and
  the paragraph reads as it did. Recorded because "change no other word" is literally true and
  "change no other line" is not.
- Nothing else. The eight steps were executed in order, as written.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 123 tests in 1.499s`, `OK`, run on the branch head. Unchanged from `main`, which is the expected result: this item touches nothing under `expenses/` or `tests/` |
| `lint-clean` | **skipped** | `commands.lint` is null in `tracker/project.yaml`; ADR-0004 records that this project installs nothing and the standard library ships no linter. The gate checked nothing and is not reported as a pass |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 7 items, 11 documents, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | AC1 and AC4 each name a command and its output above; AC1 additionally names the two injections that make it fail and the restore that makes it pass again, which is this item's equivalent of a test that fails without the change. AC2 names the diff and quotes both sentences; AC3 names the front matter and the change-log row. No criterion rests on reading the code. There is no unit test and none is possible: the check *is* `scripts/lint-claims`, and this project's test command has no reach into `docs/` [src: BUG-0001] |
| `commits-reference-the-item` | **pass** | `check-commit-refs BUG-0001 wi/BUG-0001` → exit 0, `all 1 commit(s) on main..wi/BUG-0001 name BUG-0001` |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0, `checked 1 document(s)`, 0 errors, 0 warnings. And the stronger form this item exists for: `lint-claims --all` → exit 0 over the whole tree |
| `no-unplanned-scope` (advisory) | **pass** | the diff against `main` is **one** file, `docs/product/vision.md`, in three hunks: the front matter (step 3), the two paragraphs (steps 1 and 2), and the change-log row (step 3). Nothing under `expenses/`, `tests/` or `README.md` is touched. This item's own tracker files are the only other thing this execution writes |

## What I did not do

- **The other absolutes in `vision.md` are still unsourced, deliberately.** "no accounts, no
  sync, no sharing of the dataset" and "No network access, no hosted service, no bank connection"
  are absolute claims, but they name nothing as code or as a path, so the rule does not reach
  them and the linter does not flag them. The plan lists them under `## Out of scope for this
  item`, and sourcing them would be work with no criterion behind it.
- **Nothing was done about the scoping that let this defect through three contracted gates.**
  Every skill's `claims-are-sourced` gate reads what changed since the trunk, which is why `plan`,
  `implement` and `review-close` all passed over `vision.md` while the whole-tree run failed. That
  is a property of the toolkit rather than of this project, and the plan records it as out of
  scope [src: tracker/items/BUG-0001/artifacts/plan.md].
- **`docs/architecture/overview.md` is untouched**, as the plan requires: this item alters nothing
  about the shape of the system, and a version bump with no substantive change devalues every
  other one.
- **No question was filed, and none was needed.** ADR-0009 had already decided the one thing that
  was genuinely open — whether this skill may edit this document — before this execution began. If
  it had not, this execution would have stopped rather than decided it, which is what ADR-0009 §1
  says of an `implement` execution that reaches such a judgement itself.
