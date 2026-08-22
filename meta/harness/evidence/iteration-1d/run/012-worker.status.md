# Harness status — turn 12

No stakeholder answers were pending — all eleven questions on disk were already `answered` and
propagated — so `answer-questions` did not run and the turn went straight into the loop. Two
skills ran, WI-0002 closed, and the loop then stopped on a question addressed to the stakeholder.

- **`review-close`** merged WI-0002 and closed it as `delivered`. The Definition of Done was
  walked criterion by criterion; D1–D11 pass. **D12 failed on one claim of the eight audited**,
  and that is the substance of this turn. `ADR-0008` wrote that `debts.py` "raises nothing —
  every ledger the store can load has a debt report", `implement` copied the sentence into
  `docs/architecture/overview.md` v5 and into the module's own docstring, and it is false:
  `Ledger.from_dict` checks that the keys are present and not what their values hold, so a
  hand-edited ledger whose `amount_minor` is the JSON string `"3000"` loads without a `StoreError`
  and then raises `TypeError` out of the share division. It was found by opening the cited code
  rather than by re-reading the sentence, which is exactly the failure mode D12 exists for — one
  claim that reached three documents because each skill re-quoted the previous one.

  The overview is corrected to v6 with a change-log row. `ADR-0008` and the module docstring were
  left as written and recorded as accepted gaps in the item's `## Notes`: amending a recorded
  decision is not the reviewer's to do, and editing source after verification would send the item
  back to `verifying` under D10 for one sentence. Everything else passed on its own evidence —
  `check-verify-freshness`, `check-commit-refs`, `lint-claims` and `check-epic-signoff` all exit
  0, and the trial merge into a throwaway copy of `main` ran 115 tests green before the item was
  closed and the real merge made.

- **`refine`** reached WI-0003 — runnable for the first time, now that both its dependencies are
  `done` — and suspended it on `Q-003` rather than refining it. The bank CSV sample has been asked
  for twice and deferred twice with the same sentence. Rather than ask a third time, this
  execution filed the choice underneath the missing fact: should the importer learn the file's
  shape from **a sample sent now**, from **a fixed format the stakeholder converts their export
  into**, or from **the column mapping given as options at import time**? Only the first needs the
  sample; the third takes it off the critical path entirely, and is the recommendation. No
  acceptance criterion was rewritten — two of the three options change what the command's
  arguments are — and no Definition of Ready verdict was claimed.

Nothing refused to pass, nothing is `blocked`, and the working tree is on `main` and clean.

**Two things the owner should know about the toolkit.**

1. **`review-close` is told to file bug items and the pipeline will not let it.** Its SKILL.md
   says "a defect belongs to another item: file a bug item with reproduction steps and
   `found-in`, and continue reviewing this one". `pipeline.yaml`'s only `null → ready` transition
   names `verify` as its actor and the only `null → draft` names `intake`, and
   `validate-workspace`'s `transition_is_legal` enforces the actor, so a bug filed by
   `review-close` fails validation as an illegal transition. This bit for real this turn: the
   behaviour behind the false claim above *is* a defect — the same hand-edited ledger crashes the
   `expenses` and `repayments` listings through `format_amount`, and `store.py` documents refusing
   a mis-shaped file, so value types slipping past `Ledger.from_dict` is a WI-0001 defect that
   wants a bug item. It has no bug item. It is recorded in `WI-0002/artifacts/review.md` as
   finding F2 and in WI-0002's `## Notes` as accepted gap 3, which is the best this skill could
   legally do. Either the contract or the transition table should give way.

2. **`transition` rejects an `outcome` set before the move and requires one after it.** Setting
   `outcome: delivered` in `item.md` before running the transition fails validation with
   `item.outcome.premature`; leaving it out means the transition itself succeeds and then reports
   the workspace invalid with `item.outcome.missing`, exit 1, with the move already applied. The
   only working order is transition, then edit `item.md`, then re-validate — which is a hard gate
   failing on a state the tool itself created. `transition` already accepts `--outcome`; passing
   it would be the obvious fix, and the skill's SKILL.md does not mention the flag.

Also worth carrying forward from turn 11 and confirmed again: clear `expenses/__pycache__` and
`tests/__pycache__` before trusting a test run that follows a same-second file swap.

```json
{
  "stop_reason": "human-question-open",
  "skills_run": ["review-close", "refine"],
  "open_human_questions": ["WI-0003/Q-003"],
  "items_touched": ["WI-0002", "WI-0003"],
  "last_action": "refine filed Q-003 on WI-0003 and suspended it at awaiting-answer with resume-to draft",
  "notes": "WI-0002 is done and merged into main; the tree is on main and clean. review-close's D12 audit caught a false claim that had reached three documents (debts.py 'raises nothing'), corrected the overview to v6, and recorded the ADR and the module docstring as accepted gaps in the item's Notes. The defect underneath it belongs to WI-0001 and has no bug item, because pipeline.yaml lets only verify create an item at ready and only intake at draft, while review-close's SKILL.md instructs it to file one — contract and pipeline disagree. Second toolkit friction: transition refuses an outcome set before the move and then reports the workspace invalid for the missing outcome after it, so the only working order is transition, edit item.md, re-validate; --outcome exists as a flag but the skill never mentions it. WI-0003 stopped the loop: after two deferrals of the CSV sample, refine stopped asking for the file and asked the choice underneath it instead, recommending that the column mapping become run-time options so the sample leaves the critical path. BUG-0001 is ready and is the only runnable item once Q-003 is answered."
}
```
