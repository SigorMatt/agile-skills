# Harness status — turn 16

No stakeholder answers were waiting: all seven previously escalated questions were already
`answered` and consumed in earlier turns, so `answer-questions` had nothing to do and the turn went
straight to the loop.

Three skills ran, and the engagement reached its end:

1. **`verify` on BUG-0001** → `verifying → in-review`. All four criteria pass, each decided by a
   command run in this session against `76e62a6`. The check that mattered was the sensitivity one:
   each of the two citation markers was removed from `docs/product/vision.md` in turn, the linter
   re-run, the matching error watched coming back, and the file restored and checksummed — so AC1
   is green because the claims are sourced, not because the linter stopped looking at those
   paragraphs. A third injection (a scratch document under `docs/`, flagged then deleted) proved
   the whole-tree run reaches artifacts added *after* implementation, which is what makes an AC1
   measured with the verification report in the tree a live result. `verify-report.md` written; no
   defect found, no bug filed.
2. **`review-close` on BUG-0001** → `in-review → done`, `outcome: delivered`, merged to `main` at
   `778af48`. All twelve Definition of Done criteria recorded with their own evidence. D12 was
   decided by opening what the two citations name — `WI-0001/Q-001` and `expenses/store.py`,
   `WI-0001/Q-003` and `expenses/cli.py` — rather than by re-reading the sentences; both claims are
   true and both citations support them.
3. **`review-close` on EP-001** → `open → awaiting-answer`, `resume-to: open`. `next` step 6 fired:
   nothing was runnable and `engagement-state EP-001` reported `at-rest`. **EP-001/Q-004** was filed
   — `kind: sign-off`, addressed to the human, blocking — restating the goal in the stakeholder's
   own words, naming all six children with what became of each, and offering four endings. The
   epic is suspended and the loop stops there.

**What refused to pass, and why it was right to.** The first attempt at closing BUG-0001 failed on
two hard gates. `commits-reference-the-item` reported `main..wi/BUG-0001` empty and told me to
rewind: my trial merge had been made in a `git worktree` checked out on `main`, and a worktree
shares the repository's refs, so the merge fast-forwarded the real trunk rather than a copy —
removing the worktree did not undo it. `main` was reset to `7f5ac6c`, the gate went green, and
nothing had been published. The gate did exactly the job it exists for. (BUG-0002's review used a
*detached* trial merge, which is the technique that avoids this.) `workspace-valid` failed at the
same time on `item.outcome.premature`; see note 1 below.

Everything is committed. `main` carries the merge, the suite is green at 123 tests, and
`lint-claims --all` exits 0 over the whole tree — the first time that has been true since BUG-0001
was filed, which was the point of the item.

The stop is a real one, not the budget: with Q-004 open, `next` step 3 stops the loop regardless of
how much budget remained. The 3-skill budget also happens to be exhausted.

**Notes for the owner, all about the toolkit rather than the project:**

1. **`outcome` cannot be written before the transition, and must be written after it — but nothing
   says so.** `review-close`'s SKILL.md step 9 says "Set `status: done` and `outcome: delivered`",
   which reads as one edit before the move. Doing that makes `validate-workspace` fail with
   `item.outcome.premature` ("outcome is set to 'delivered' but the item is not done"), and the
   transition's own `--resolving` hint does not exempt it. Omitting it makes the *post*-transition
   validation fail with `item.outcome.missing`. So the only working order is: transition, then
   write the outcome, then validate — and the transition necessarily reports a validation error on
   the way through. Cost this turn: one failed transition and one confusing error. Step 9 should
   say the outcome is written immediately after the move.
2. **`check-verify-freshness` counts `docs/` as record, not as deliverable.** Its message here was
   *"only the record changed (5 file(s) under `tracker/` or `docs/`), so the verification still
   covers the code"*. That is sound for every item whose deliverable is under `expenses/`, and
   wrong in principle for a document-only item like BUG-0001, whose deliverable **is** a file under
   `docs/`: an edit to `docs/product/vision.md` made after verification would have been classified
   as a record change and D10 would have passed over it. It did not happen — I checked
   `git diff --name-only 76e62a6..HEAD -- docs/` directly and it is empty — and the review records
   the finding, but the script cannot tell a document deliverable from a document record.
3. **The `Status:` bullet contradiction is still there, and cost a failed transition again.**
   `review-close`'s (and `plan`'s and `implement`'s) SKILL.md says the transition "writes the
   `**Status:**` bullet itself"; `scripts/transition --journal-body-file` exits 1 with *"the journal
   body is not a legal entry — missing the '**Status:**' bullet"*. The template printed by
   `journal-entry --template` includes the bullet, so only the prose is wrong. This was reported
   last turn and is unchanged.
4. **`verify`'s SKILL.md lists five hard gates at the top and its contract lists six**, and the
   contract's `every-criterion-has-a-test` does not appear in `verify`'s gate list at all — it is
   `implement`'s. Minor, but a worker reconciling the two spends time on it.

```json
{
  "stop_reason": "human-question-open",
  "skills_run": ["verify", "review-close", "review-close"],
  "open_human_questions": ["EP-001/Q-004"],
  "items_touched": ["BUG-0001", "EP-001"],
  "last_action": "review-close filed EP-001/Q-004, the sign-off question, and suspended the epic to awaiting-answer with resume-to open",
  "notes": "BUG-0001 is done, delivered and merged into main at 778af48; lint-claims --all now exits 0 over the whole tree, which was the defect's whole point. The engagement is at rest with five of six children delivered — WI-0003, the bank CSV import, is still blocked on the sample the stakeholder deferred in EP-001/Q-001 — and Q-004 puts all six items to them by name with four endings to choose from. Nothing further can run until they answer. Four toolkit findings above: the outcome-before-transition trap in review-close step 9 (cost a failed transition), check-verify-freshness treating docs/ as record even when a document is the deliverable, the still-unfixed Status-bullet contradiction in three SKILL.md files, and a gate-list mismatch between verify's SKILL.md and its contract. Also worth recording as a near miss: a trial merge made in a git worktree checked out on main advanced the real trunk ref; check-commit-refs caught it and its error message named the exact fix."
}
```
