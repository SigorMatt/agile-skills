# Harness status — turn 16

No stakeholder answers were waiting: all twelve human-addressed questions across the workspace
were already `answered`, so `answer-questions` had nothing to consume and the turn went straight
into the loop. BUG-0001 was `planned` and was the only runnable item on the board; this turn took
it all the way to `done` and merged it.

**What happened, in order.**

1. **`implement` on BUG-0001** — executed the plan's seven steps on `wi/BUG-0001`. `ADR-0011`'s
   handler contract: `cmd_add_person`, `cmd_add_expense` and `cmd_repay` now return their success
   line instead of printing it, the four listings return `None` after printing their own rows, and
   `main` saves first and prints the line only on the path where `store.save` returned. The
   regression test was written and run **before** the fix, so its failure against the unfixed code
   is on the record: `FAILED (failures=3)` quoting the three lines BUG-0001 names as the actual
   behaviour. `docs/architecture/overview.md` went to v7.
2. **`verify` on BUG-0001** — both criteria pass on evidence gathered independently, not from
   `impl-report.md`. The six reproduction steps were run here (empty stdout, `Permission denied` on
   stderr, exit 1, nothing recorded), and "prints nothing" was re-checked byte-exactly with
   `wc -c` because a shell `$(...)` capture would have shown a lone newline as empty. AC2's
   sensitivity was demonstrated the way AC2 words it — `print(line)` moved back above the save,
   test fails, restore. Both boxes ticked. Five boundary cases exercised.
3. **`review-close` on BUG-0001** — accepted, closed as `delivered`, merged into `main` at
   `0fb7ac2`. All twelve Definition of Done criteria recorded individually with evidence. Tests
   green on the merge result (116) and again on `main` after the real merge.

**Things worth knowing.**

- **`verify` found a stale documentation claim and routed it correctly.** `overview.md`'s lede
  still said "this version is step 5 of WI-0002's plan" after `implement` wrote v7 for BUG-0001.
  It is not a send-back (no criterion of this item covers the overview) and not a bug (not another
  item's behaviour) — it is D12, so it went to `review-close`, which corrected it as v8 and
  rewrote the sentence into a form that does not go stale on the next edit.
- **Four gaps were accepted at review and written into `item.md`'s `## Notes`**, so they outlive
  the closed item: neither criterion is verified under `root` (the test skips itself there, which
  is the honest option); `ADR-0011`'s central argument that WI-0003's importer inherits the
  ordering cannot be checked until WI-0003 exists; `CliTestCase.assertRefused` still does not
  assert empty stdout; and a ledger at mode 400 in a writable directory is still overwritten,
  because atomic replace renames over the target and POSIX `rename` needs permission on the
  directory, not the file.
- **WI-0003 is still `blocked` and only the stakeholder can move it.** It needs 3–5 lines of their
  bank's CSV export at `tracker/items/WI-0003/artifacts/bank-sample.csv`. Three questions have
  been asked and answered on it and `ADR-0010` forbids a fourth; once the file exists, any skill
  may return the item to `draft`.
- **EP-001 stays `open`**, correctly: DE1 fails while WI-0003 is `blocked`, so the DE7 stakeholder
  sign-off question is not yet due. `check-epic-signoff` passed only because BUG-0001 is a bug, not
  an epic — that pass should not be read as the epic having been cleared.

**What refused to pass, and what got in the way:**

1. **A toolkit defect, hit at the worst possible moment.** `spec/workspace-layout.md` §1.1 requires
   `<item>/questions/` to exist even when empty, and git does not track empty directories.
   BUG-0001 is the first item in this project that never had a question, so its `questions/` was an
   untracked empty directory — and the **trial merge that `review-close`'s own procedure mandates**
   switches branches, which deleted it. `validate-workspace` then failed with `questions.missing`
   on an item that had done nothing wrong, at the moment of closing. Worked around by recreating
   the directory with a `.gitkeep` that explains why it is there. The real fix belongs upstream:
   `scripts/new-item` should create the keep file, or the validator should not require a directory
   version control cannot carry. Any future item with no questions will hit this identically.
2. **A self-inflicted one, caught and corrected.** The closing `implement` journal entry gave the
   commit range as `ad961d7..b0fa7c2` — `b0fa7c2` was predicted before `git commit` reported the
   real hash, and is not a commit in this repository. Corrected to the three hashes listed
   individually, with a journal entry saying exactly what was changed and why. `scripts/transition`
   did nothing wrong here; the lesson is to read hashes back from `git log`, never from the commit
   you are about to make.
3. **A conflict between the plan and the spec, resolved in the spec's favour.** BUG-0001's plan
   step 7 told `implement` to tick both acceptance criteria. `spec/work-item.md` gives ticking to
   `verify`, "only when it has evidence for it". `implement` declined, declared it as deviation 1,
   and put the evidence in `impl-report.md` instead; `verify` ticked the boxes. Review agreed this
   was the correct reading — a box ticked by the developer would tell the verifier that something
   had already been independently confirmed, which is what separating those two skills prevents.
   Worth flagging as a `plan` defect: the skill wrote a step that instructs another skill to
   violate a spec rule.

Nothing is blocked that a skill could resolve, and no question is open. The next turn's `next`
will find only WI-0003 (`blocked`, owner `null`) and EP-001 (`open`, owner `null`), and will
report `nothing runnable` — unless the stakeholder has dropped the CSV sample by then, which is the
one thing that restarts this epic.

```json
{
  "stop_reason": "turn-budget-exhausted",
  "skills_run": ["implement", "verify", "review-close"],
  "open_human_questions": [],
  "items_touched": ["BUG-0001"],
  "last_action": "review-close closed BUG-0001 as delivered and merged wi/BUG-0001 into main at 0fb7ac2",
  "notes": "Three skills, one item, start to finish. Toolkit defect worth fixing: an item with no questions has an empty questions/ directory that git cannot track, so the trial merge review-close is required to perform deletes it and validate-workspace fails with questions.missing at the moment of closing — worked around with a .gitkeep; new-item should create it. Second finding: BUG-0001's plan step 7 instructed implement to tick the acceptance criteria, which spec/work-item.md reserves for verify; implement declined and declared it, and review agreed — but plan should not be writing steps that tell a downstream skill to break a spec rule. WI-0003 remains blocked on a CSV sample only the stakeholder can supply (tracker/items/WI-0003/artifacts/bank-sample.csv); EP-001 correctly stays open because DE1 fails, so the DE7 sign-off question is not yet due. Next turn will report nothing-runnable unless that file appears."
}
```
