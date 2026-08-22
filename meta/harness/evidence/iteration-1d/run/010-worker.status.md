# Harness status — turn 10

The stakeholder had answered all three outstanding questions between turns, so this turn began by
consuming them and ended with the pipeline moving again.

- **`answer-questions` on WI-0002.** They chose **option A, the pairwise debt report**, over
  `refine`'s recommendation of a minimised settlement, because "if the number ever gets questioned
  I want it to trace straight back to what those two people actually shared". Recorded as
  `ADR-0006` — five computation steps, and an explicit statement that a printed circle of debts is
  correct output rather than a defect. AC1 amended; the two R10 rows that hung on the choice
  settled. Item returned to `draft`, its recorded `resume-to`.
- **`answer-questions` on WI-0003.** Two replies, only one of them an answer. `Q-002` was answered
  properly — **option B**: the payer, the sharers and a date range are given when the import runs.
  That is now `ADR-0007`, which also settles the two things their answer left open (the range is
  optional; a row outside it is skipped silently rather than reported as a failure), and AC1 says
  so. `Q-001`, the bank CSV sample, came back **"I'll send you a sample later" for the second
  time** — the same sentence as on `EP-001/Q-002`. It is marked answered because that is what they
  said and it has a consequence; nothing about the file's shape was guessed. The item went back to
  `draft` rather than to `blocked`: `blocked` is terminal and needs a human, and this item is not
  due (it `depends-on` WI-0002), so `draft` is inert and self-healing — the `refine` execution
  eventually dispatched will file a fresh question if the sample still has not arrived. **No third
  request for the sample was filed this turn**, deliberately: they have been asked twice, no skill
  could use the answer yet, and a third question would have stopped the loop on the one item that
  was actually runnable.
- **`next`** then dispatched `refine` on WI-0002 (priority `high` beats BUG-0001 at `medium`;
  WI-0003 not runnable).
- **`refine` on WI-0002 → `ready`, no override.** Asked the stakeholder nothing — everything left
  was arithmetic following from the ADRs or presentation `refine` may decide. The six inherited
  criteria became **eleven**, six of them carrying a complete ledger and the exact stdout it must
  produce. One inherited criterion turned out to be **wrong**, and the pairwise answer is what
  exposed it: old AC3 announced "nobody owes anybody" when every person's net position is zero,
  which is true of a *circle* of debts that must still print three lines. AC4 now triggers on "no
  pair has a non-zero balance" and AC8 pins the circle down with a worked example.

Nothing is blocked, no question is open, and BUG-0001 and WI-0002 are both waiting at `ready`.
Next turn `next` will dispatch `plan` on WI-0002.

Two things for the toolkit owner, both minor and both worked around:

1. `transition --journal-body-file` **made the status move and then refused the journal entry**
   (my body was missing the `**Commands:**` bullet). The history row existed and the entry did
   not, which is exactly the split state `spec/skill-contract.md` §2.3 calls the transition a
   checkpoint to prevent. The tool said so clearly and `scripts/journal-entry` repaired it, but the
   validation of the body should probably happen before the row is written.
2. A journal entry that **quotes** an unresolvable citation form fails `claim.citation.unresolved`
   on the journal itself — so an entry cannot record *which* malformed citation the validator
   rejected without tripping the same check. I described the offending forms in prose instead.

```json
{
  "stop_reason": "turn-budget-exhausted",
  "skills_run": ["answer-questions", "answer-questions", "refine"],
  "open_human_questions": [],
  "items_touched": ["WI-0002", "WI-0003"],
  "last_action": "refine took WI-0002 from draft to ready with eleven observable criteria and no DoR override",
  "notes": "All three stakeholder answers consumed. WI-0003's CSV sample was deferred a second time, so that item sits at draft unrefined with the instruction to re-ask recorded at the point where the answer is needed; no third question was filed, to avoid stopping the loop on the runnable item. Two toolkit observations above: transition can write the history row and then reject the journal body, and a journal cannot quote a malformed citation without failing the citation gate itself."
}
```
