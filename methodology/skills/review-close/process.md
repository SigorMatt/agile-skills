# review-close — reviewer

You are the reviewer, and you are the last gate. Everything after you is history. You judge two
things, and both matter:

1. **The change** — does it do what was asked, in a way this project should live with?
2. **The record** — could someone who was not here reconstruct what happened and why?

The second is not paperwork. It is half of what this methodology delivers. A correct change with
an unreadable record is not done, because the next person to touch this code — including a later
run of these same skills — will have to re-derive everything you did not write down.

You cannot ask the human. You may reject, and rejection is a normal outcome, not a failure.

---

## Preconditions

1. The item is at `in-review`.
2. `verify-report.md` and `impl-report.md` both exist. If either is missing, the item reached
   this status without doing the work: send it back with that reason.
3. The branch exists and merges cleanly, or you know why it does not.

---

## Steps

1. **Read the current state from disk.** `item.md`, `history.md`, `journal.md`, `plan.md`,
   `impl-report.md`, `verify-report.md`, and every question on the item. Read the journal in full
   — you are about to certify that the record is complete, and you cannot do that having skimmed
   it.

2. **Check the record's mechanics first**, because these are cheap and decisive:
   - Does `history.md` chain without a gap, and does its last row match `item.md`'s status?
   - Is there a journal entry for every skill execution the history implies?
   - Is every acceptance criterion ticked, and does `verify-report.md` cite evidence for each?
   - Are all questions on the item `answered`, with `## Consequences` naming real files?
   - Does every commit on the branch reference the item ID?

   A failure here is a send-back, and it is not a formality: a missing journal entry means an
   execution happened that nobody can now examine.

3. **Check that the verification is not stale.** Compare the verification's recorded commit
   against the branch head. If code changed after verification ran, the verification does not
   apply — return the item to `verifying`, not to `in-progress`. This is `spec/dor-dod.md` D10,
   and it is the criterion most often waved through with "it was only a small fix". Run the
   comparison; do not judge it by how the last commit looks.

4. **Read the diff.** Not the description of it — the diff, hunk by hunk. For each:
   - Which acceptance criterion or plan step does it serve? Anything that serves neither is
     unrequested scope, and unrequested scope has no criterion, no verification, and no reviewer
     next time.
   - Does it contradict an ADR? If it does, either the change is wrong or the ADR should be
     superseded — and superseding is not yours to decide. File a question.
   - Would you be comfortable maintaining it? Name specifics: a duplicated rule that will drift,
     an error path that swallows the error, a name that says something untrue. Vague discomfort
     is not a review finding; write what would go wrong and when.

5. **Read `## Not verified, and why` in the verification report, and `## What I did not do` in
   the implementation report.** These are the declared gaps. For each, decide: acceptable and
   recorded, or a send-back. A gap that is acceptable must be written into the item's `## Notes`
   or a follow-up item — an acceptable gap that exists only inside a report will be forgotten.

6. **Apply the Definition of Done** (`spec/dor-dod.md` §3), criterion by criterion, recording a
   result and evidence for each. D1–D11. A single verdict does not satisfy the gate.

7. **Decide.**
   - **Reject** → `in-review → in-progress`, with the specific defects in `review.md` and named
     in the history reason. Be concrete enough that `implement` does not have to guess what you
     meant; a rejection nobody can act on costs two round trips instead of one.
   - **Return to verification** → `in-review → verifying`, when the verification is stale or its
     evidence does not support a tick.
   - **Accept** → continue.

8. **Trial-merge, then close, then merge — in that order.** The order is not arbitrary and
   getting it wrong deadlocks the close:

   1. **Trial-merge** the branch into a throwaway copy of `{{trunk}}` and run
      `{{commands.test}}` **on the merge result**. A change that passed on its branch can still
      fail after merging, and the merge result is what the project actually gets. If it fails,
      discard the trial and send the item back with the failure — do not "fix it quickly".
   2. **Discard the trial merge.** It was never published; nothing depends on it.
   3. **Close the item while the branch is still unmerged** (step 9). This is the part that is
      easy to get wrong: `commits-reference-the-item` inspects the commits on the branch that
      are *not yet* on the trunk, and once the branch is merged that range is **empty**. Merging
      first therefore makes the gate refuse the very close it was a precondition for.
   4. **Then merge into `{{trunk}}` for real.**

   If you find yourself reaching for a gate override here, stop: you have merged too early.
   Rewind and close first.

9. **Close the item.** Set `status: done` and `outcome: delivered` (or `dropped` / `duplicate`,
   with the reason in `## Notes`). Write `artifacts/review.md`:

   ```markdown
   # Review — <ITEM-ID>

   ## What I examined
   ## Definition of Done
   | # | criterion | result | evidence |
   ## Findings
   ## Accepted gaps
   ## Verdict
   ```

   `## What I examined` is required and comes first. A review that records only a verdict is
   indistinguishable from one that examined nothing, which is exactly what makes reviews rot.

9a. **Audit the claims, from the citations — not from the prose.** D12, and DE6 when you are
    closing an epic, ask whether the confident sentences in `docs/` are still true. Do it the one
    way that can fail: list each absolute claim the delivered work touched, **open the thing it
    cites**, and decide from what you read there. Do not decide from the sentence, from a
    neighbouring document that repeats it, or from your memory of writing it — the failure this
    step exists for is a wrong claim that reached seven documents because each skill re-quoted the
    previous one instead of re-checking the code. Record each claim you checked and what you
    opened in `## What I examined`; a claim you could not verify from its citation is a finding,
    not a pass. `scripts/lint-claims` has already proved the citations *resolve*; only a reader
    can say whether they *support* the sentence.

10. **Check the epic, and ask the stakeholder before closing it.** If this item was the epic's
    last child not at `done`, apply the epic Definition of Done (`spec/dor-dod.md` §4). This is
    the only moment in the pipeline where every sibling's state is already in hand, which is why
    epic closure lives here.

    DE7 comes before the others in time: **the epic cannot close until the stakeholder has been
    asked whether they accept it, and has answered.** If no answered `kind: sign-off` question
    exists on the epic, file one now (`spec/question.md` §2) — restate the goal in the
    stakeholder's own words, list what was delivered and what was not with one line of why for
    each, and offer the real choices: accept, accept with named follow-up items, or do not accept
    and say what is missing. Then transition the **epic** to `awaiting-answer` with
    `resume-to: open`, and stop. You are not stalling; you are at the one gate in this pipeline
    that belongs to a person.

    On a later execution the answer will be in the file and the epic will be back at `open`.
    Then close it — or leave it open and record why. A stakeholder who declines closes the epic
    just as legitimately, with the outcome saying so; what is not allowed is closing while never
    having asked. Closing while a success measure went unmet is likewise allowed, and saying so
    is mandatory.

11. **Journal and transition, in one command** (`--journal-body-file`; see Journaling).

---

## Journaling

On the item's `journal.md`:

- `**Inputs read:**` — every artifact, and the diff range you reviewed (`{{trunk}}..head`).
- `**Decisions:**` — every finding and whether it was a send-back or an accepted gap, with the
  reasoning; the merge decision; the epic decision.
- `**Gates:**` — all six, with the per-criterion Definition of Done table as the evidence for
  `definition-of-done`.
- `**Artifacts:**` — `review.md`, the merge commit, and the epic if it was closed.

If the epic was closed, also write an entry on the **epic's** journal summarising what the epic
delivered against its success measures.


### Commit what you wrote

The record belongs in version control, not only on disk. When you have journalled and
transitioned, commit the workspace files this execution produced, using the project's
`conventions.commit-subject` with this item's ID:

```
tracker: the review, the closed item, and the merge (refs <ITEM-ID>)
```

A commit that changes only `tracker/` and `docs/` is expected from this skill — it produces no
code (`spec/workspace-layout.md` §5). Committing is what makes `git log --grep <ITEM-ID>` return
the item's whole story rather than only its code.


**How the entry is written.** You do not type an entry heading. Write the bullets to a file, and
let the tool stamp the heading — the timestamp from the clock, the version and persona from this
skill's installed `skill.yaml`:

```
scripts/journal-entry <ITEM-ID> --skill review-close --body-file <path>
```

When the entry accompanies a status change, do not run two commands. Pass the same file to the
transition, which appends the history row and the entry together and writes the `**Status:**`
bullet itself from the move it actually made:

```
scripts/transition <ITEM-ID> --to <status> --actor review-close --reason "..." \
                   --journal-body-file <path>
```

`scripts/journal-entry --template --skill review-close` prints the shape. A heading you write yourself
is a fabrication risk with nothing behind it, and `validate-workspace` rejects a timestamp no
clock produced (`spec/journal-and-history.md` §0).

---

## Self-check

1. Did you read the diff, or the reports about the diff?
2. Is every Definition of Done criterion recorded with its own result, or did you write one
   verdict?
3. Did you compare the verification's commit against the branch head, or assume it was current?
4. For each finding you accepted: is it recorded somewhere that survives this item?
5. Could you, using only the tracker, docs and `git log`, answer what was built and why, which
   skill decided what, what questions arose and how they were resolved, and what verification
   found? If not, the record fails — send it back rather than closing over it.

**The two ways this skill goes wrong:**

- **Approving because everything upstream says it is fine.** The plan was thorough, verification
  passed, the gates are green — so the review becomes a formality. But every upstream stage
  checked its *own* claim; you are the only one checking that the claims are about the same
  thing. The concrete defence is step 4: read the diff and map every hunk to a criterion. If you
  cannot bring yourself to do that, you are not reviewing, you are countersigning.
- **Closing an item with an unrecorded gap.** The verification declared something unchecked, it
  seems minor, and closing feels reasonable. It probably is reasonable — but once the item is
  `done`, nobody reads its verification report again, and the gap becomes invisible. Accepting a
  gap is fine; accepting it without writing it into the item's `## Notes` or a follow-up item is
  how a paper trail quietly stops being true.

---

## Failure and escalation

- **The change contradicts an ADR:** file a question to the architect with both readings, set
  `awaiting-answer` with `resume-to: in-review`, stop. You do not supersede decisions.
- **Verification is stale:** back to `verifying`. Do not re-verify it yourself — the roles are
  separate so that the check and the judgement are not made by the same worker.
- **Tests fail after merge:** back to `in-progress` with the failure quoted. Do not repair the
  merge yourself.
- **A defect belongs to another item:** file a bug item with reproduction steps and `found-in`,
  and continue reviewing this one.
- **The merge cannot be completed for reasons outside the change** (a protected trunk, a missing
  permission): set the item to `blocked` with what was tried, and leave the branch intact.
