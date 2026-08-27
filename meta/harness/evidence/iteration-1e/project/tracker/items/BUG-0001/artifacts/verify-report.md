# Verification report — BUG-0001

Verified-commit: 76e62a6458b4b2d03dd45ee396110f91d74104a3

## Verdict

**Pass.** All four acceptance criteria are met, each decided by a command run in this session
against the head of `wi/BUG-0001` and quoted below. The criteria were read from `item.md` and the
checks designed from them before `impl-report.md` was opened.

The one way this fix could look right while sourcing nothing is if an edit had stopped the linter
from examining either paragraph, so AC1 would go green with nothing cited. That was checked by
removing each of the two citation markers in turn and watching the matching error come back, then
restoring the file and confirming the restore by checksum — twice, once per marker, by this skill.
Both markers are load-bearing on their own lines.

A third injection, not in the plan, establishes that this report itself is inside the scope AC1
is measured over: a scratch document added under `docs/product/` was flagged by the whole-tree
linter within the same run and then removed. AC1 and AC4 were therefore re-run after this report
was written, and both of those final runs are the evidence recorded here.

No defect was found. Nothing is sent back and no bug is filed.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 — `lint-claims --all` exits 0 and reports 0 errors and 0 warnings | **pass** | `python3 .claude/agile-skills/scripts/lint-claims --all` | `lint-claims: checked the whole tree under /home/msi/agile-skills-throwaway/expenses-1e`, `lint-claims: 0 errors, 0 warnings`, `exit=0` | run three times by this skill: on the branch head as committed; after each injection was restored; and finally with this report present in the tree. The injections below are what stop this row from being a tautology |
| AC2 — the document still says the same two things, in the same two paragraphs; the fix adds citations and removes or softens nothing | **pass** | `git diff main -- docs/product/vision.md`, then `sed -n '25,42p' docs/product/vision.md` to read the result | the diff is three hunks: the front matter, the two paragraphs, and one new change-log row. `9 insertions(+), 8 deletions(-)`. Every deleted line of prose returns: the second paragraph's `re-record.` comes back as `re-record` plus a marker plus the full stop, and the first paragraph's three deleted lines come back as three lines carrying the same words in the same order, rewrapped. Read back from the file, the claims stand as *"The product deliberately has no per-person amounts and no weights: an uneven bill is two entries, not one complicated one"* and *"It cannot be edited in place: the stakeholder was offered both and chose deletion, so a correction is a delete and a re-record"* | both paragraphs are still present and neither absolute is hedged. The bracketed question references the paragraphs already carried are all still there, which matters for AC1 for the reason the injections show |
| AC3 — front matter at `version: 4` with a matching `## Change log` row | **pass** | `sed -n '1,12p' docs/product/vision.md`, then `sed -n '/## Change log/,/^| 3 /p' docs/product/vision.md` | front matter: `version: 4`, `status: current`, `updated: 2026-08-27T02:17:05Z`, `updated-by: implement`, `updated-for: BUG-0001`. Top change-log row: `4`, `2026-08-27T02:17:05Z`, `implement`, `BUG-0001`, describing the two claims gaining resolvable citations and stating that neither claim changed | the version, timestamp, actor and item agree across the header and the row — a row that named a different version or a different item would satisfy "a row exists" and not "a matching row" |
| AC4 — `validate-workspace .` exits 0 with 0 errors | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` | `validate-workspace: checked 7 item(s), 11 document(s)`, `validate-workspace: 0 errors, 0 warnings`, `exit=0` | re-run after this report was written, so the count includes this item's verification artifacts |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → `Ran 123 tests in 1.517s`, `OK`, `exit=0`, run by this skill on `76e62a6`. Unchanged from the trunk, which is what this item predicts: nothing under `expenses/` or `tests/` is in its diff |
| `lint-clean` | **skipped** | `tracker/project.yaml` records `lint: null`; ADR-0004 is the decision, and it is that this project installs nothing and the standard library ships no linter. Nothing ran, so nothing is claimed — see `## Not verified, and why` |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 7 items, 11 documents, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | every row above names a command this skill ran and quotes its actual output; no row rests on `impl-report.md`. The claims linter, the validator, the diff and the file itself were each read here |
| `negative-cases-exercised` | **pass** | AC1's failure condition was produced three times by construction — two marker removals and one injected document — and each produced the expected error and exit 1. Listed in the next section |
| `tests-would-fail-without-the-change` (advisory) | **pass** | there is no unit test and the item records why: the check *is* the claims linter, and this project's test command has no reach into `docs/`. The equivalent was run instead — each citation removed in turn, the linter's error returning for that exact line, the file restored and checksummed |

## Negative and boundary cases exercised

1. **First citation removed.** The marker at the end of the equal-split sentence was deleted from
   a working copy of the document. `lint-claims --all` → `exit=1`,
   `docs/product/vision.md:31: ERROR [claim.unsourced] an absolute claim ('no') about
   'WI-0001/Q-001' with no citation`, `1 error, 0 warnings`. Restored from a copy taken first;
   `md5sum -c` → `docs/product/vision.md: OK`.
2. **Second citation removed.** Same, for the deletion sentence. `lint-claims --all` → `exit=1`,
   `docs/product/vision.md:38: ERROR [claim.unsourced] an absolute claim ('cannot') about
   'WI-0001/Q-003' with no citation`, `1 error, 0 warnings`. Restored; `md5sum -c` → `OK`.
3. **A new document with an unsourced claim, added and then removed.** A scratch file was written
   to `docs/product/zz-probe.md` containing one absolute claim about a path that does not exist.
   `lint-claims --all` → `exit=1`, one error against `zz-probe.md:12`, `1 error, 0 warnings`. The
   file was deleted immediately and `git status --short` was empty afterwards. This is the
   boundary that decides whether AC1 means anything once this report exists: the whole-tree run
   reaches documents added after the implementation, so a green AC1 measured with this report in
   the tree is a live result and not a stale one.
4. **The restored tree, after all three.** `git status --short` empty, `git rev-parse HEAD` =
   `76e62a6458b4b2d03dd45ee396110f91d74104a3`, `lint-claims --all` → 0 errors, 0 warnings,
   `exit=0`. Every check above was made against the branch head and left it as it found it.

## Test sensitivity check

Cases 1 and 2 above are this item's sensitivity check, and they are the reason AC1 is a pass
rather than a coincidence. Each marker was removed on its own, and each time exactly one error
returned, naming the line the marker had been on and the absolute word in that sentence — `'no'`
at line 31, `'cannot'` at line 38. Neither paragraph fell silent when the other's marker went,
which is what would have happened had a paragraph stopped being examined instead of being sourced.

The project's own suite was also run against the branch head and is unchanged at 123 tests
passing. It has no bearing on any criterion here; it is recorded because a document-only change
that moved a test count would be a finding in itself.

## What the citations resolve to

The linter decides that a citation exists. Whether it resolves to something that supports the
claim is a separate question, and it was checked here because a citation naming an unrelated file
would satisfy AC1 while making the document worse.

- The equal-split marker names `WI-0001/Q-001` and `expenses/store.py`. Both exist. `add_expense`
  at `expenses/store.py:109` takes an amount, a payer, a list of sharers, a date and a
  description — there is no weight and no per-person amount in its signature
  [src: expenses/store.py].
- The deletion marker names `WI-0001/Q-003` and `expenses/cli.py`. Both exist. The parser builds
  `add`, `list` and `delete` under each of `person` and `expense`, and no `edit` subcommand is
  registered anywhere in the file [src: expenses/cli.py].

## Diff against the plan

The change touches one file outside this item's own tracker directory — `docs/product/vision.md`
— which is exactly what the plan's steps 1 to 3 describe [src: tracker/items/BUG-0001/artifacts/plan.md].
Nothing under `expenses/`, `tests/` or `README.md` is in the diff, and
`docs/architecture/overview.md` is untouched, both as the plan requires.

One deviation is declared in `impl-report.md` and is confirmed here: plan step 1 says to change no
other word of the paragraph, and three of its lines were rewrapped because the added marker made a
line too long. The diff shows the same words in the same order across those three lines, so no
word was changed; the plan's literal wording holds and its wording about lines does not. It fails
no criterion — AC2 is about what the paragraph says — and it is recorded rather than waved past.

## Defects found

None. No criterion of this item failed, and no behaviour delivered by another item was found to be
wrong while checking this one.

## Not verified, and why

- **`lint-clean`.** The project has no lint command, by a recorded decision (ADR-0004). Nothing
  was run and nothing is claimed. What this leaves unchecked is style and static analysis across
  the whole tree — for this item, which adds no code, that is nothing at all.
- **The other absolute claims in `vision.md`.** "no accounts, no sync, no sharing of the dataset"
  and "No network access, no hosted service, no bank connection" are unsourced, and the linter
  does not flag them because they name nothing as code or as a path. This item's criteria do not
  reach them and the plan lists them as out of scope, so no verdict is offered on whether they
  ought to be sourced one day.
- **Whether the whole-tree scoping should be a contracted gate.** Three skills passed over this
  defect because every contracted `claims-are-sourced` gate reads only what changed since the
  trunk. That is a property of the toolkit, the plan puts it out of scope, and nothing here tests
  it. It stays true after this item closes: the next document defect written outside an item's own
  diff will be found the same way this one was, by someone running the whole-tree form by hand.
- **Anything about the tool's runtime behaviour.** This item changed a document. The suite was run
  to show the tree did not move, not as evidence about any criterion.
