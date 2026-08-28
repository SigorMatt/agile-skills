# Review — WI-0001

## What I examined

**The record, in full.** `item.md` (fifteen criteria, all ticked); `history.md` (eight rows,
`— → draft → ready → planned → in-progress → awaiting-answer → in-progress → verifying →
in-review`, chaining without a gap, last row matching the frontmatter); `journal.md` end to end
(eight entries — `intake`, `refine`, `plan`, `implement` ×2 for its first execution's open and
close, `answer-questions`, `implement`, `verify`); `plan.md` including its criteria-to-test
mapping, six assumptions and four risks; `impl-report.md` including its six declared deviations;
`verify-report.md` including its `## Not verified, and why`; and both questions, Q-001 and Q-002,
each `answered` with `## Consequences` naming files that exist.

**The diff, hunk by hunk — `main..wi/WI-0001`, twelve files, 951 lines of code and tests.** Not
the reports about it. Every hunk was mapped to a plan step and a criterion:

| file | plan step | serves |
|------|-----------|--------|
| `tidy/rules.py` | 1 | AC5 — `DEFAULT_RULES` and `folder_for` over a flattened index; `extension_of` lowercases |
| `tidy/planner.py` | 2, 3 | AC4, AC6, AC9, AC10, AC11, AC13 and the Q-002 case — the scan, the four-way classification, `_free_destination`, `_is_taken` |
| `tidy/apply.py` | 4 | AC7, AC9 — `os.makedirs`, `os.link`, `os.unlink`, and `_move_without_a_link` |
| `tidy/cli.py` | 5 | AC1, AC2, AC3, AC10, AC14, AC15 — the parser, `render`, the exit codes |
| `tidy/__main__.py` | 6 | AC1 — three lines |
| `README.md` | 7 | AC5's "a file in the repository a user can read" |
| `tests/` ×6 | 8 | the `demonstrated by` column, plus 21 tests beyond the sixteen named |

Nothing in the diff serves neither a plan step nor a criterion. There is no age handling, no rule
loading, no unrelated fix, and no third-party import — the five modules import only `os`, `shutil`,
`argparse`, `sys`, `dataclasses` and `typing`, so ADR-0001 holds.

**The claims in `docs/`, from their citations rather than from the prose (D12).** Each of these was
decided by opening the cited file and reading it, not by reading the sentence:

| claim | cites | opened | verdict |
|-------|-------|--------|---------|
| "Every destination is decided in `planner.py` and nowhere else" | ADR-0002, `tidy/planner.py` | `tidy/planner.py` **and** `tidy/apply.py` | **true** — `apply_plan` joins `action.destination` to the folder and never computes one, including on the fallback path |
| The module table's "may write to disk" column | — | all five modules | **true** — `cli` writes only to the two streams, `planner` calls `os.scandir` and `os.path.lexists`, `rules` calls `os.path.splitext`; only `apply` calls `os.makedirs`/`os.link`/`os.unlink`/`shutil.move` |
| "no dependency outside the Python standard library" | ADR-0001 | every import in `tidy/` | **true** |
| never-overwrite "is enforced by the kernel rather than by a check a future call site has to remember" | ADR-0003, EP-001/Q-002 | `tidy/apply.py` | **misleading — corrected.** True of the `os.link` path; `_move_without_a_link` is a check-then-act. See Finding 1 |
| `Action`'s kind is "`move`, `leave`, or `skip`" (ADR-0002 `## Decision` 1) | — | `tidy/planner.py` | **false — corrected.** No `skip` is ever emitted. See Finding 2 |
| "`tests/` contains only an empty package marker, so … reports `NO TESTS RAN` and exits **5**" (ADR-0004) | `[src: run: …]` | ran the command | **false — corrected.** 37 tests, exit 0. See Finding 3 |
| "it moves the incoming one under a suffixed name and says so, in the preview and again in the real run" (vision.md) | EP-001/Q-002, WI-0001 AC9 | `verify-report.md` AC9/AC10 rows, and the code | **true** |
| ADR-0002's "AC8 and AC10 become properties of the structure" | WI-0001 AC8, AC10 | `tidy/cli.py` | **true** structurally — apply renders and executes the same list. See Finding 4 for what that cost the AC8 *test* |

**The gates, run rather than read**, and the trial merge (below).

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every checkbox ticked | **pass** | `grep -c '^- \[x\] AC' tracker/items/WI-0001/item.md` → 15; `grep '^- \[ \]'` → none |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | the report's `## Criteria` table has a row per AC1–AC15, each naming a command run in that execution and quoting its output. Spot-checked three against the artifacts they claim: AC5's 59-row check (table typed from `item.md`, not imported), AC14's four `exit 2` runs, AC15's eight runs across four fixtures |
| D3 | gates passed on the **final** state of the code | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 37 tests … OK`, and `python3 -m compileall -q tidy tests` → exit 0, both re-run in this execution **and** on the trial merge result `9286fe3`. No code file has changed since `f6254de`; everything after it is `tracker/` and `docs/` |
| D4 | no open blocking question | **pass** | Q-001 and Q-002 both `status: answered`, `answered-by: answer-questions`, with `## Consequences` naming `item.md` and `plan.md`; `validate-workspace` → 0 errors |
| D5 | an entry per execution; history chains | **pass** | eight history rows, eight journal entries; the two `implement` entries at 16:09:55 and 16:13:02 are that execution's open and close, as `implement`'s procedure prescribes. `impl-report.md` deviation 6 explains why the second `implement` execution has one entry and not two, and the explanation holds — `answer-questions` had already returned the item to `in-progress`, so there was no move to hang an opening entry on |
| D6 | design decisions in ADRs, cited from the plan or journal | **pass** | ADR-0002, ADR-0003 and ADR-0004 were minted by `plan` and are cited in `plan.md` `## Decisions and ADRs`; ADR-0001 predates the item and is cited too. The two decisions taken later — the AC6/AC15 overlap and the taken-destination-name case — were correctly *not* made ADRs: `answer-questions` recorded why in Q-001 and Q-002, and they decide nothing ADR-0002 had not |
| D7 | documents the change invalidated have been updated, with a version bump and a change-log row | **pass — after this execution fixed three of them.** `overview.md` → v2, `ADR-0002` → v2, `ADR-0004` → v2, each with a change-log row naming this item and this skill. See Findings 1–3 |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → `all 8 commit(s) on main..wi/WI-0001 name WI-0001`, exit 0 |
| D9 | merged into the trunk | **pass** | the trial merge into a **detached** worktree of `main` succeeded with no conflict (`9286fe3`), the suite and the lint both passed on the merge result, and `git rev-parse main` was `d46b852` before and after the trial. The real merge follows this close, in the order SKILL.md step 8 mandates: `commits-reference-the-item` inspects `main..branch`, which merging first would empty |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0001 wi/WI-0001` → exit 0: "verified at `6b187316`; `wi/WI-0001` has moved to … but only the record changed (15 file(s) under `tracker/` or `docs/`), so the verification still covers the code". Compared, not assumed |
| D11 | `review.md` exists and states what was examined | **pass** | this file; `## What I examined` is first and names the diff range, the eight claims audited and what was opened for each |
| D12 | claims in `docs/` about the behaviour this item touched are still true | **pass — after three corrections.** The audit table above; each verdict was reached by opening the cited file. Three claims failed and were fixed rather than waved through. `lint-claims --changed-since main` → `checked 3 document(s)`, 0 errors |

## Findings

**1. `overview.md` read as though never-overwrite were always kernel-enforced. Corrected.**
The paragraph said the guarantee "is enforced by the kernel rather than by a check a future call
site has to remember", citing ADR-0003 — but ADR-0003 itself provides `_move_without_a_link`, a
check-then-act fallback, and the overview did not mention it. A reader of the overview alone would
have believed the strong guarantee held everywhere. Fixed in `overview.md` v2, which now names the
fallback, what it costs, and BUG-0002. Not a send-back: the code is what ADR-0003 decided, and the
document is what was wrong.

**2. ADR-0002 named an `Action` kind that was never built. Corrected.**
`## Decision` 1 specified `move`, `leave` **or `skip`**; `build_plan` emits no action at all for a
hidden file or a subfolder. This is an undeclared deviation — `impl-report.md` lists six and this
is not among them — but it is a deviation in the right direction: AC13 requires a hidden file to
appear in neither mode's output, and an entry that produces no `Action` cannot be rendered by
mistake, whereas a `skip` action would have depended on `render` remembering to suppress it.
Recorded in ADR-0002 v2. The decision itself is untouched; superseding is not this skill's to do.

**3. ADR-0004's note about the test command had become false. Corrected.**
"`tests/` contains only an empty package marker, so … reports `NO TESTS RAN` and exits **5**" is
no longer this repository — the command runs 37 tests and exits 0. The note predicted its own
expiry ("It becomes a passing gate the moment `implement` writes the first test") and nothing came
back to close the loop, which is exactly the shape D12 exists to catch. Marked superseded by fact
in ADR-0004 v2, with the real outcome cited; the reasoning is kept because it is the part worth
having.

**4. The AC8 test is weaker than AC8, and ADR-0002's confidence is why.**
`verify` found this and it survives review as a real observation.
`test_cli.ApplyTests.test_apply_matches_the_preview_it_printed` compares two rendered stdouts, both
produced by the same loop in `cli.main` *before* `apply_plan` is called, so an apply that silently
moved nothing would pass it — demonstrated by `verify`'s mutation `apply_plan(folder, actions[:1])`,
which broke AC7's test and left AC8's green. The criterion is genuinely met: `verify` checked the
previewed pairs against disk state. The lesson is that "AC8 becomes a property of the structure"
(ADR-0002 `## Consequences`) made the test that names AC8 into a test of the structure rather than
of the outcome. Accepted as a gap and written into `item.md` `## Notes` 2, because WI-0002 and
WI-0003 both extend this path.

**5. `test_nothing_to_do_cases` calls `self.setUp()` inside the test body.**
It re-enters the fixture between `subTest` cases to get a fresh temporary folder. It is correct —
`addCleanup` stacks, so every folder is still removed — and it passes, but it is an unusual idiom
that will read as a mistake to the next person. Not a defect and not a send-back; noted because
WI-0002 will extend this class.

**No finding rose to a rejection.** Nothing in the diff contradicts an ADR, nothing is unrequested
scope, and no error path swallows an error: `apply_plan` returns a message per action that did not
complete and `cli.main` prints every one to stderr. The two genuine defects this change carries
were found by `verify`, are outside this item's criteria, and are open as BUG-0001 and BUG-0002.

## Accepted gaps

Five, each declared upstream and each now written into `item.md` `## Notes` so that it survives the
close — a gap recorded only in a verification report is a gap nobody reads again:

1. ADR-0003's fallback is unexercised on a real filesystem that refuses hard links; on one, AC9
   rests on a check-then-act. Also now in `overview.md` v2.
2. AC8's coverage in the suite rests on AC7's test (Finding 4).
3. Symlinks at the top level are unspecified; a moved relative symlink breaks. `impl-report.md`
   describes this incorrectly and `verify` corrected it from a run.
4. `python3 -m tidy` runs only from the repository root — what ADR-0001 chose, not a defect.
5. Verified on Linux/ext4 only; a case-insensitive filesystem is untested against AC9's suffix rule.

Accepting a gap is not the same as accepting a defect. The two things that *are* defects —
BUG-0001 and BUG-0002 — are items, not notes, and both are `ready` under EP-001.

## Verdict

**Accept.** All fifteen acceptance criteria are ticked and each tick is backed by a command
`verify` ran against the branch head, with its output quoted. The Definition of Done passes D1–D12,
three of them only after this review corrected documents that had stopped being true. The trial
merge is clean and the suite and lint pass on the merge result. WI-0001 closes as
`outcome: delivered`, and the branch merges into `main` after the close.

The engagement is **not** over: `scripts/engagement-state EP-001` reports `active`, with WI-0002,
WI-0003, BUG-0001 and BUG-0002 still in flight. No sign-off question is due, and filing one now
would be asking the stakeholder to sign off work that has not been done.
