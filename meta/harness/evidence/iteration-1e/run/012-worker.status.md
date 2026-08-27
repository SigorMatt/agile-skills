# Harness status — turn 12

No stakeholder answers were waiting — every question in the workspace was already
`status: answered` — so this turn went straight into the loop and spent its whole budget on
WI-0004, carrying it from `planned` through implementation, verification and review.

- **`implement` on WI-0004** — branch `wi/WI-0004` off `main`, the plan's eleven steps in order:
  `naming_expenses`, `delete_person` and `delete_expense` in `expenses/store.py`; the
  `person delete` / `expense delete` subparsers and handlers in `expenses/cli.py`; the leading
  position column in `expense list`; the one WI-0001 test that column breaks, repaired; new test
  classes in both suites; and the README. Four commits, all naming the item. All hard gates green
  on the branch head (`lint-clean` skipped — `commands.lint` is `null` per ADR-0004).
  `impl-report.md` declares four deviations from the plan, one of them against a plan assumption.
- **`verify` on WI-0004** — all eight criteria checked with commands run in this session, not by
  reading the implementation report: `od -c` byte dumps for the exact-output criteria, `md5sum`
  either side of every refusal, and a deliberate one-process-then-fresh-process `cmp` for AC5
  (comparing two shell runs would not have tested persistence at all). Six test-sensitivity
  probes; five failed as expected and one is recorded as a behaviour-preserving move rather than
  an insensitive test, with the probe that does remove the behaviour named beside it. No defects,
  no bugs filed, criteria ticked.
- **`review-close` on WI-0004 — rejected, back to `in-progress`.** The code is sound: every hunk
  maps to a plan step, no ADR is contradicted, the trial merge is clean and 120 tests pass on the
  merge result. What fails is **D7 and D12**: `docs/architecture/overview.md` is still at
  version 4, whose `## What is coming` section describes this item's delivered work as
  forthcoming — and in the same sentence says `store.py` gains "two new functions" when it gains
  three (`naming_expenses`, `delete_person`, `delete_expense`). The claim was re-quoted from the
  plan's `## Approach` summary, which also says two, and never checked against the plan's own
  steps or the code. That is the failure mode D12 exists for, so it was sent back rather than
  accepted as a gap. `review.md` names the fix concretely enough to act on without guessing.

## What went wrong, and was repaired

The review's trial merge **accidentally advanced the real `main`**. The skill says to trial-merge
into "a throwaway copy of the trunk"; `git worktree add /tmp/trial4 main` checks out the actual
`main` branch in a second directory rather than copying it, so the merge fast-forwarded the real
ref, and removing the worktree did not move it back.

`check-commit-refs` caught it within the minute — in the gate run of the transition that rejected
the item — reporting exactly the case its own error message warns about. `main` was rewound with
`git branch -f main 441a9b0` (the target read from `git reflog show main`), and the gate then
returned to exit 0. **Nothing was lost:** the merge was a fast-forward so no commit was created or
orphaned, `wi/WI-0004` still carries all four commits, and this repository has no remote. The
mistake, the detection and the repair are all in WI-0004's journal as a correction entry, and
`review.md`'s finding F5 was corrected in place with the correction stated rather than the false
sentence quietly removed.

## Notes for the owner

- **A toolkit friction worth fixing:** `implement`'s SKILL.md says the transition "writes the
  `**Status:**` bullet itself from the move it actually made", which reads as *you need not write
  one*. `scripts/transition` in fact **requires** the bullet to be present and then replaces it —
  the first attempt failed with `the journal body is not a legal entry — missing the '**Status:**'
  bullet`. The script is right and the prose is misleading; `journal-entry --template` does show
  the bullet, so following the template works. Worth one word in the SKILL.md ("rewrites" rather
  than "writes").
- **A trap worth naming in `review-close`'s step 8.** "Trial-merge into a throwaway copy of the
  trunk" does not tell a worker that `git worktree add <path> <trunk>` is not one. A detached
  checkout (`git worktree add --detach <path> <trunk>`) is, and would have made this turn's
  mistake impossible. The gate caught it, which is the system working — but the cheaper fix is one
  clause in the procedure.
- **WI-0004 is one document away from closing.** Next turn's `next` will dispatch `implement` on
  it (`in-progress`, medium, created 2026-08-26T23:42:32Z — still ahead of BUG-0002 on `created`
  and BUG-0001 on priority-rank). The work is `docs/architecture/overview.md` v5 and nothing else;
  `review.md`'s F1 specifies it. After that it must pass through `verify` again before it can
  close.
- **Nothing is waiting on the stakeholder.** No question is open, and no question was filed this
  turn — none was real. WI-0003 remains `blocked` on the bank CSV sample, which is a question
  that was already asked and answered with a deferral.

```json
{
  "stop_reason": "turn-budget-exhausted",
  "skills_run": ["implement", "verify", "review-close"],
  "open_human_questions": [],
  "items_touched": ["WI-0004"],
  "last_action": "review-close rejected WI-0004 back to in-progress on Definition of Done D7 and D12 — docs/architecture/overview.md still describes the delivered work as coming and miscounts store.py's new functions — and recorded a correction for a trial merge that briefly fast-forwarded the real main before being rewound",
  "notes": "Three skill executions, the full budget, all on WI-0004. Two toolkit findings: implement's SKILL.md says transition 'writes' the **Status:** bullet when the script requires it present and rewrites it (the first transition attempt was refused for exactly this); and review-close's step 8 says to trial-merge into 'a throwaway copy of the trunk' without warning that `git worktree add <path> <trunk>` checks out the real branch rather than copying it — this turn hit that and advanced main, which check-commit-refs caught immediately and which was rewound with no loss. Suggest `git worktree add --detach` in the procedure. WI-0004 needs only docs/architecture/overview.md v5, then re-verification, to close."
}
```
