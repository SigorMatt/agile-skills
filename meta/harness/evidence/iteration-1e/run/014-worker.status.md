# Harness status — turn 14

No stakeholder answers were waiting — every question in the workspace is `status: answered`, and
none is open — so this turn went straight into the loop. All three skill executions went to
BUG-0002, the traceback-instead-of-a-message defect `review-close` filed against WI-0001. It came
in at `ready` and leaves at `in-review`, verified, with the merge and the close still to do.

- **`plan` on BUG-0002.** Reproduced the bug on trunk first (`chmod 500` on a directory, `person
  add Ana` → exit 1 and an eleven-line traceback) rather than planning against the item's account
  of it. The decision that was actually open was not "remove the traceback" — the criteria already
  demand that — but **where an operating-system error stops being an exception and becomes a
  refusal**, because `store.load` and `store.save` had settled it in opposite directions by
  accident and nothing recorded either. That is **ADR-0008**, decided against three named
  alternatives (catch in `cli.main`; catch per handler; leave it), and it answers the item's own
  open note about `mkdir` explicitly. `plan.md` has nine steps, a five-row criteria mapping, three
  reversible assumptions with what reversal costs, four risks and four things out of scope.
  `docs/architecture/overview.md` went to version 6, recording under "What is coming" that the
  refusal claim in its `expenses/cli.py` piece did **not** yet hold on the write path — `plan` and
  `answer-questions` are the only skills `spec/doc-header.md` §5 lets write that document, so
  leaving the false absolute unmarked until the fix landed was not an option. Commit `37e57f0`.
- **`implement` on BUG-0002.** Branch `wi/BUG-0002` from `main` at `37e57f0`. The fix is one
  wrapper: `save`'s whole body, the `mkdir` included, inside `try` with
  `except OSError → ExpensesError("cannot write %s: %s")`, and the existing temporary-file cleanup
  left *nested inside* it so it still runs before the translation — which is what AC3 turns on.
  Three regression tests in `tests/test_cli.py` run the tool in a real subprocess against a
  mode-500 directory, behind a write probe that skips them where mode 500 does not bind. Two
  deviations from the plan, both recorded: the fixture records `Zoe` rather than `Ana` (with `Ana`
  already in the group, AC1's literal command would have been refused by `add_person` and passed
  for the wrong reason), and the AC3 test does not restore permissions before asserting.
  `overview.md` → version 7, ADR-0008's rule moved into the body. 123 tests green; commits
  `db45f4f`, `f23bfda`, `d8b4c4e`.
- **`verify` on BUG-0002 — pass, `verifying → in-review`.** Every criterion decided from its own
  text with my own fixtures, designed before `impl-report.md` was opened: `wc -c` on stdout,
  `wc -l` and two `grep -c` on stderr, `md5sum` brackets around *two* refusals, and
  `ls -a | grep -c '^\.expenses-'`. AC1 was run twice — against a directory holding a dataset and
  against the empty one the bug's own reproduction uses. AC4 was checked in three parts, including
  both directions of the sensitivity check: the handling reverted → `FAILED (failures=3)`, and the
  probe forced by making the directory writable → `OK (skipped=3)`, which is the root case
  reproduced by construction rather than by becoming root. Tree restored and `md5sum -c`'d after
  each injection; `git status` empty and `HEAD` still `d8b4c4e` afterwards. Four boundary cases
  beyond the criteria, including the `mkdir` clause of ADR-0008 and a check that an ordinary
  refusal (`Ana is already in the group`) is *not* re-wrapped. Commit `a332c73`.

## What the next turn should know

- **`next` will dispatch `review-close` on BUG-0002** (`in-review`, medium) ahead of BUG-0001
  (`ready`, low). `check-verify-freshness BUG-0002 wi/BUG-0002` already reports exit 0 —
  "verified at `d8b4c4e8`; `wi/BUG-0002` has moved to `a332c738` but only the record changed", so
  D10 is satisfied and does not need re-verification.
- **One non-blocking finding is waiting for the reviewer**, in `verify-report.md` under
  `## Defects found`: `tests/test_cli.py`'s module docstring still says "each test starts from a
  store that does not exist yet", which this diff made false for three tests. It fails no
  criterion, so it was neither a send-back nor a bug item — it is the reviewer's call.
- **The trial merge must use `git worktree add --detach`.** Turn 12 lost `main` to a plain
  `git worktree add <path> main`; the rule is in `review.md` F4 and in WI-0004's journal.
- **The repository is left on branch `wi/BUG-0002`**, working tree clean, `main` at `37e57f0`.
- After BUG-0002 closes, only BUG-0001 remains before EP-001 reaches rest and needs its sign-off
  question to the stakeholder. WI-0003 stays `blocked` on the bank CSV sample, already asked and
  answered with a deferral.

## Notes for the owner

- **The `**Artifacts:**` requirement bit again, exactly as turn 13 predicted.** `implement`'s
  opening journal entry — the short one that records the branch before any work exists — was
  refused by `transition` for a missing `**Artifacts:**` bullet, which is awkward precisely
  because that entry has no artifacts yet. The entry now says so in words. The error message is
  good and the template is the answer; the friction is that `SKILL.md` describes the opening entry
  as "short and honest" without mentioning that four bullets are structurally mandatory.
- **`check-commit-refs` fails informatively but confusingly on a branch with no commits yet.** At
  the `planned → in-progress` move the branch tip equals `main`, so the gate reports "`wi/BUG-0002`
  is already merged into main … Rewind the merge, close, then merge" — advice for a completely
  different situation. It is non-blocking on that move, so nothing was harmed, but a reader of the
  transcript would reasonably think something had gone wrong.
- **`plan` commits to the trunk, `implement` branches from it.** That is per the skill contracts
  and works, but it means `lint-claims --changed-since main` saw only one document during
  `implement`, because ADR-0008 was already on `main`. Worth knowing when reading the gate output.
- **Nothing is waiting on the stakeholder.** No question is open and none was filed — none was
  real.

```json
{
  "stop_reason": "turn-budget-exhausted",
  "skills_run": ["plan", "implement", "verify"],
  "open_human_questions": [],
  "items_touched": ["BUG-0002"],
  "last_action": "verify passed BUG-0002 on all five criteria against d8b4c4e and moved it to in-review, recording one non-blocking finding for the reviewer",
  "notes": "Three skill executions, the full budget, all on BUG-0002: ready -> planned -> in-progress -> verifying -> in-review. The fix is one wrapper in expenses/store.py so an OSError leaves as ExpensesError('cannot write <path>: <error>'), with the temporary-file cleanup left nested inside it; ADR-0008 records where that boundary belongs and answers the item's open question about mkdir. Verification ran every check itself and did the sensitivity check in both directions (handling reverted -> 3 failures; probe forced -> OK (skipped=3)), restoring and checksumming the tree each time. Next turn: review-close on BUG-0002, whose verify-freshness gate already passes; then BUG-0001, then EP-001 reaches rest and needs a stakeholder sign-off question. Toolkit findings: implement's mandatory **Artifacts:** bullet is hardest to satisfy on the opening entry that has none; and check-commit-refs on a branch with no commits yet reports 'already merged into main - rewind the merge', advice for an unrelated situation."
}
```
