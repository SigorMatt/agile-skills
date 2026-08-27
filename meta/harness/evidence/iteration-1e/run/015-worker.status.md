# Harness status — turn 15

Three skills ran, in this order: `review-close` on BUG-0002, `plan` on BUG-0001, `implement` on
BUG-0001. The turn ended on the budget, not on a stopping point — nothing is blocked, nothing is
waiting on the stakeholder, and BUG-0001 sits at `verifying` for the next turn to pick up.

- **Consumed answers first, as amendment B requires.** Every question in the workspace was already
  `status: answered` when this turn began; none was left open, so nothing needed
  `answer-questions` and `next` did not stop.
- **BUG-0002 closed, `outcome: delivered`, merged into `main` at `c84b2d3`.** Twelve of twelve
  Definition of Done criteria pass, recorded criterion by criterion, with a fourteen-row D12 claim
  audit in which every verdict came from opening the cited source. The trial merge was detached
  (`git worktree add --detach`), clean, and green at 123 tests; the item was closed before the
  real merge, because `check-commit-refs` reads the commits not yet on the trunk.
- **`verify`'s one non-blocking finding on BUG-0002 was opened and did not hold.** It reported
  that the change made `tests/test_cli.py`'s module docstring ("each test starts from a store that
  does not exist yet") inaccurate. Seven pre-existing test classes already record data in their
  own `setUp` through a helper that writes the file, so the sentence has been inaccurate under the
  strict reading since WI-0001 — and under the reading that makes it true of those seven it is
  true of the new class too. Not a defect this diff introduced, so not a send-back and not a bug.
  Recorded as F1 in `review.md` and in the item's `## Notes`, with two further precision findings
  (F2, F3) and seven accepted gaps.
- **BUG-0001 planned and implemented.** The visible fix is two citation markers and a version
  bump. The decision that was actually open was which skill may make it — see the toolkit note
  below — and it is recorded as **ADR-0009** against three alternatives. `docs/product/vision.md`
  is now at version 4, `lint-claims --all` exits 0 over the whole tree for the first time, and
  each marker was removed in turn to prove the linter still examines both paragraphs rather than
  having fallen silent.
- **Nothing was filed.** No question, no new bug, no ADR superseded.

## For the owner — three things about the toolkit

1. **`spec/doc-header.md` §5 and the Definition of Done pull in opposite directions, and a
   document-only defect is where it becomes unavoidable.** §5 says `implement` and `verify` do not
   write to `docs/`, and lists `refine` and `answer-questions` as the updaters of
   `product/vision.md`. BUG-0001's acceptance criteria *are* criteria about that file, so read
   flatly no skill the pipeline dispatches on `planned` or `in-progress` may fix it. Meanwhile D7
   makes the delivering item responsible for leaving `docs/` true, and in this project `implement`
   has already written versions 5 and 7 of `docs/architecture/overview.md` — both reviewed and
   accepted — because at plan time the code a document describes does not exist yet. ADR-0009
   resolves it for this project by reading §5's prohibition as its stated reason describes (a
   skill may not edit `docs/` on a conclusion it reached itself mid-execution), and it says so
   loudly rather than quietly. This is a real gap in the methodology, not a project quirk: it
   deserves either an exception in §5 for items whose criteria are about a document, or a
   dispatchable owner for such items.
2. **`review-close`'s SKILL.md says the transition writes the `**Status:**` bullet itself; the
   script rejects a body without one.** "let the tool stamp the heading … the transition … writes
   the `**Status:**` bullet itself from the move it actually made" — but
   `scripts/transition --journal-body-file` exits 1 with *"the journal body is not a legal entry —
   missing the '**Status:**' bullet"*. The template printed by `journal-entry --template` includes
   the bullet, so the template and the script agree and only the prose is wrong. Cost this turn:
   one failed transition and a re-run. The same paragraph appears in `plan`'s and `implement`'s
   SKILL.md.
3. **`check-commit-refs` reports a branch with no commits of its own as "already merged".** During
   `implement`'s opening transition — branch just created, zero commits ahead of trunk — the gate
   failed with *"`wi/BUG-0001` is already merged into `main`, so `main..wi/BUG-0001` is empty"* and
   advice to rewind a merge that never happened. It is non-blocking there (the gates do not block
   an intermediate move) and it goes green as soon as the branch carries work, but the message
   sends a resuming worker looking for a merge to undo. An empty range on a freshly branched item
   is a different condition from an already-merged one, and the script can tell them apart.

Two smaller notes: `lint-claims --all` reads the whole tree, so a citation written into an item's
own plan or report is part of that item's acceptance criterion — this turn produced an instance of
it, when ADR-0009 cited a plan file before the plan existed. And every contracted
`claims-are-sourced` gate is trunk-scoped, which is exactly why three skills passed over BUG-0001's
defect before `verify` found it with the whole-tree run.

```json
{
  "stop_reason": "turn-budget-exhausted",
  "skills_run": ["review-close", "plan", "implement"],
  "open_human_questions": [],
  "items_touched": ["BUG-0002", "BUG-0001"],
  "last_action": "implement moved BUG-0001 to verifying on wi/BUG-0001; vision.md is at version 4 and lint-claims --all exits 0 over the whole tree",
  "notes": "Nothing is blocked and nothing waits on the stakeholder. BUG-0002 is done and merged into main; BUG-0001 is at verifying on branch wi/BUG-0001, unmerged, with its record committed. WI-0003 stays blocked awaiting the bank CSV sample the stakeholder deferred (EP-001/Q-001). EP-001 is not yet at rest, because BUG-0001 is not terminal; once it is, next's step 6 should dispatch review-close on the epic for sign-off. Three toolkit findings are written up above: spec/doc-header.md section 5 leaves a document-only defect with no skill allowed to fix it (ADR-0009 records this project's resolution); review-close/plan/implement SKILL.md prose contradicts scripts/transition about who writes the Status bullet; and check-commit-refs misreports a freshly created branch as already merged."
}
```
