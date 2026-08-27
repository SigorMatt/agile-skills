# Harness status — turn 13

No stakeholder answers were waiting — every question in the workspace is `status: answered` — so
this turn went straight into the loop. All three skill executions went to WI-0004, which came in
`in-progress` under a Definition-of-Done rejection and leaves `done`, merged into `main`.

- **`implement` on WI-0004 (round 2).** Reconciled with the branch first: all eleven plan steps
  were already executed on `wi/WI-0004`, so nothing was rebuilt. The outstanding work was review
  finding F1 alone — `docs/architecture/overview.md` at version 5: the deletion paragraph moved
  out of `## What is coming` into the `expenses/store.py` and `expenses/cli.py` pieces, the
  function count corrected from two to three, ADR-0007's invariant stated where the enforcing code
  is described, `## What is coming` reduced to WI-0003, header fields and a change-log row. Every
  sentence was checked against `grep -n "^def "` and the diff rather than against the plan's
  summary, which is where the false claim came from. One commit, `e2a0b3d`; `impl-report.md`
  gained a `## Round 2` section with an eight-row claim-audit table, and round 1's stale
  "`overview.md` was not updated" bullet was struck with the correction stated beside it rather
  than deleted. Gates green on the branch head; `lint-clean` skipped per ADR-0004.
- **`verify` on WI-0004 (second verification).** All eight criteria re-derived from their own text
  and re-demonstrated with commands run in this session — `od -c` byte dumps, `md5sum` brackets
  either side of every refusal, `wc -c` on stdout, and a deliberate one-process-then-fresh-process
  comparison for AC5. Nothing was inherited: the boxes were already ticked, and each was
  re-demonstrated before it was left ticked. Five sensitivity probes, all failing as expected,
  tree restored and re-verified clean. It was established (not assumed) that
  `git diff --stat f4e8319..HEAD -- expenses/ tests/ README.md` is empty, so the code was
  byte-identical to the previously verified state. `overview.md` v5 was inspected but explicitly
  **not judged** — no criterion covers it, and D7/D12 belong to the reviewer.
- **`review-close` on WI-0004 — accepted, merged, closed `outcome: delivered`.** Twelve of twelve
  Definition of Done criteria pass, including D7 and D12. The D12 audit was re-done from the
  citations rather than carried over from the first review: twelve claims, each decided by opening
  the cited file — twelve true, and `grep -c "two new functions"` → 0. Six accepted gaps were
  written into `item.md`'s `## Notes` so they outlive the reports that declared them. Two
  non-blocking findings recorded, not acted on (`expense delete 01` refused with a message true of
  the form and false of the value; `naming_expenses` returning positions nobody reads). Merge
  commit `3fa80d4`, `--no-ff`; 120 tests pass on `main` after it.

## What went right that went wrong last turn

The trial merge used **`git worktree add --detach /tmp/trial5 main`**, and `git rev-parse main`
was checked immediately after the merge: still `441a9b0`. Last turn's `git worktree add <path>
main` checked out the real branch and fast-forwarded `main`. The rule is now written into
`review.md` F4 and into WI-0004's journal, so the next execution meets it in the record rather
than rediscovering it.

## Notes for the owner

- **The `**Status:**` friction is real and hit again.** `verify`'s SKILL.md, like `implement`'s,
  says the transition "writes the `**Status:**` bullet itself"; `scripts/transition` in fact
  **requires** it and then rewrites it. The verify transition was refused on the first attempt for
  exactly this. Turn 12 reported it against `implement`; the wording is identical in `verify` and
  `review-close`, so the one-word fix ("rewrites") belongs in all three. `journal-entry --template`
  shows the bullet, so following the template works.
- **A second, smaller instance of the same class:** `journal-entry` also requires
  `**Artifacts:**`, which is easy to omit on a short correction entry. The error message is good;
  the template is the answer both times.
- **The closing entry can never name the merge commit.** The procedure's order is trial-merge →
  discard → close → merge, so `review-close`'s `**Artifacts:**` bullet promises a merge commit
  that does not exist yet. WI-0004 now carries a short addendum entry naming `3fa80d4`; if that is
  worth doing every time, the procedure could say so, since otherwise a reader reconstructing the
  item from `git log --grep` has to infer which commit was the merge.
- **Nothing is waiting on the stakeholder.** No question is open and none was filed — none was
  real. WI-0003 stays `blocked` on the bank CSV sample, already asked and answered with a deferral
  (*"I'll send you a sample later."*).
- **Next turn:** `engagement-state EP-001` → `active`, still in flight BUG-0001 and BUG-0002. The
  selection key picks **BUG-0002** (`ready`, medium, created 2026-08-27T00:16:35Z) ahead of
  BUG-0001 (`ready`, low), so `next` will dispatch `plan` on BUG-0002. Two bugs and then the epic
  reaches rest and needs a sign-off question.

```json
{
  "stop_reason": "turn-budget-exhausted",
  "skills_run": ["implement", "verify", "review-close"],
  "open_human_questions": [],
  "items_touched": ["WI-0004"],
  "last_action": "review-close accepted WI-0004 on all twelve Definition of Done criteria, merged wi/WI-0004 into main as 3fa80d4 (--no-ff, 120 tests green on main), closed it outcome: delivered, and recorded six accepted gaps in item.md's Notes",
  "notes": "Three skill executions, the full budget, all on WI-0004, which is now delivered, merged and closed. The D7/D12 send-back was fixed at the root: docs/architecture/overview.md v5 and a claim-by-claim audit done by opening each citation rather than re-quoting the previous verdicts. This turn's trial merge used `git worktree add --detach`, and main was verified unmoved afterwards — the fix for last turn's finding. Toolkit findings: verify's and review-close's SKILL.md carry the same misleading sentence turn 12 reported for implement, that the transition 'writes' the **Status:** bullet when the script requires it present (the verify transition was refused for exactly this); journal-entry likewise requires **Artifacts:**; and review-close's step ordering means the closing journal entry can never name the merge commit, which was handled here with an addendum entry naming 3fa80d4. Nothing is blocked on the stakeholder; next turn's next dispatches plan on BUG-0002."
}
```
