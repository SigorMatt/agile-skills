# Harness status — turn 8

Consumed no answers this turn — every question in the workspace was already `answered` when the
turn started, so the amendment-B sweep found nothing to propagate. The turn was three pipeline
actions and it ends waiting on the stakeholder again.

- **WI-0001 accepted, merged and closed** at its third review, `outcome: delivered`. Definition of
  Done applied D1–D12: eleven pass, D6 passes with a recorded caveat, none fails. I read the diff
  hunk by hunk and ran the tool myself on 20 hand-written stores rather than re-reading `verify`'s
  sweep — including the class of input that caused both earlier rejections (a store that passes
  `store.load()` and breaks above it) and the write-path `OSError` that `verify` had declared
  untriggered. No new AC violation. Trial-merged into a throwaway worktree at `main` first, 23
  tests green on the merge result, item closed while the branch was still unmerged, then merged.
- **Four declared gaps decided rather than left in a report**, all written into `item.md`
  `## Accepted gaps`: a hand-edited bad name is listed verbatim (F5); the `expenses` list's
  elements are still unvalidated and WI-0002 now inherits that as a criterion (F6); AC8's
  "one-line message" against argparse's two-line failures, with the reading stated (F7); and the
  catch-all backstop being recorded in `overview.md` v2 rather than in an ADR (F8). Two gaps
  carried by the previous review were struck as **closed** rather than re-carried.
- **`plan.md`'s superseded AC8 paragraph** — handed to this skill by name in `impl-report.md` —
  was corrected by an **appended** `## Correction` section, not by editing the paragraph. That
  file is not one of `review-close`'s declared outputs; the step outside the list is flagged in
  `review.md`, in the journal and here rather than done quietly.
- **WI-0002 refined and suspended** on three questions to the human. Seven further gaps were
  decided by `refine` itself and marked as such in the criteria; the item went from eight criteria
  to eleven and from four failing DoR criteria to two-and-a-bit.
- **WI-0003 refined to `ready`** with **no** questions filed — every gap was derivable. It found a
  real contradiction between AC2 and AC5 that would have reached `verify`, and recorded
  `depends-on: WI-0002` in frontmatter so the orchestrator holds it back until there is an expense
  record to design against. It is Ready and deliberately not runnable.
- Nothing refused to pass. Two `validate-workspace` failures occurred and both were transients
  this turn caused and fixed: a stale board after `depends-on` changed, and
  `question.blocking.not-suspended` in the moment between writing WI-0002's questions and moving
  its status. Both are recorded in the journals rather than smoothed over.

## Note on the amendments

Amendment A ("file every question you have, across every item you can legitimately reach") and
`next`'s step 2 ("a human-addressed question stops the loop") pull in opposite directions. I
followed A: after suspending WI-0002 I ran `refine` on WI-0003 in the same turn rather than
stopping, because stopping would have cost a whole turn to learn that WI-0003 needed nothing from
the stakeholder. This is recorded in WI-0003's journal under `**Trigger:**` so the deviation from
the strict one-action cadence is visible in the tracker and not only here.

```json
{
  "stop_reason": "human-question-open",
  "open_human_questions": ["WI-0002/Q-004", "WI-0002/Q-005", "WI-0002/Q-006"],
  "items_touched": ["WI-0001", "WI-0002", "WI-0003", "EP-001"],
  "last_action": "refine took WI-0003 to ready with no questions; the loop then stopped on WI-0002's three open human questions",
  "notes": "WI-0001 is delivered and merged; the tool now has add-person and people, a per-user JSON store, and 23 tests green on main. EP-001 stays open with two children left, and the reason is recorded in review.md rather than skipped. Toolkit friction worth knowing: (1) the Bash hook protecting the append-only transition record and the generated board matches on the command *text*, so a journal entry that merely quotes one of those paths inside a heredoc is blocked - it fired twice on me, once while I was writing this very file, and both times the write was aimed somewhere else entirely; I had to reword prose to get past it, which is a false positive that pushes skills toward vaguer journals; (2) the transition script's tests-pass-on-the-merge-result gate runs commands.test in the working tree, not on a merge result, so review-close must perform the real trial merge itself - I did, in a detached worktree, and the gate as written would pass for a change that breaks on merge; (3) refine's precondition 2 assumes the human is present and its failure path is the only route available here, which means the skill can never reach its own completion transition for an item that genuinely needs the stakeholder, and WI-0002 has now spent two passes there; (4) nothing in spec/dor-dod.md or the verify/review-close contracts says who may *clear* an acceptance-criterion tick - the previous review flagged this and it is still true."
}
```
