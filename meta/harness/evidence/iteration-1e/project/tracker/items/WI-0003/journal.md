# Journal — WI-0003

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-26T23:24:58Z — intake v0.2.0 — product-analyst

- **Item:** WI-0003
- **Trigger:** invoked directly on the stakeholder's opening statement (`IDEA.md`); no prior workspace state existed
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement
  - `tracker/project.yaml`
  - `tracker/items/EP-001/item.md` (written by this same execution)
- **Decisions:**
  - See EP-001's entry for this execution for how the work was split and why.
  - Wrote no CSV column layout into the criteria. A bank export has no standard shape, so an invented one would pass verification and fail on the stakeholder's real file; EP-001/Q-001 asks for it instead.
- **Questions raised:** none on this item; `EP-001/Q-001`, `EP-001/Q-002` and `EP-001/Q-003` are filed on the epic and affect this item
- **Commands:**
  - `scripts/new-item --id WI-0003 --type work-item --status draft --actor intake` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace` reported 0 errors at the end of this execution)
  - `epic-has-success-measures` → **pass** (assessed on EP-001; see its entry)
  - `items-are-separable` (advisory) → **pass** (see EP-001's entry for the order and dependencies of all three items)
  - `no-solution-in-the-problem` (advisory) → **pass** (see EP-001's entry)
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` (new)
- **Status:** `—` → `draft`
- **Result:** Created at draft. It cannot be refined or planned until EP-001/Q-001 supplies the bank's CSV layout.

## 2026-08-26T23:32:30Z — answer-questions v0.2.0 — architect

- **Item:** WI-0003
- **Trigger:** no status of its own — this item is parked as a consequence of EP-001/Q-001, on which the stakeholder replied but did not answer. `answer-questions` was run on EP-001.
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-001.md` (the stakeholder's reply: "I'll send you a sample later.")
  - `tracker/items/EP-001/questions/Q-003.md` (their refusal to drop this item)
  - `tracker/items/WI-0003/item.md` (AC1 and AC2, and intake's note that neither can be made decidable without the layout)
  - `tracker/items/EP-001/item.md`, `tracker/items/EP-001/journal.md`
  - `docs/product/vision.md` (v1, before this execution bumped it)
  - `docs/architecture/adr/` — empty
  - `.claude/agile-skills/spec/question.md` §2 and §3, `spec/ids-and-statuses.md` §4 and §6
- **Decisions:**
  - Parked this item at `blocked` with `resume-to: draft` rather than leaving it at `draft`. Rationale: `spec/question.md` §2 says a deferral that leaves no decision takeable parks the item with what would unblock it recorded. Left at `draft`, the orchestrator would dispatch `refine` on it, and `refine` could only either file a fresh question re-asking for the sample the stakeholder just said they would send, or invent a layout — which is option B of Q-001, the failure that question exists to prevent.
  - Recorded **what unblocks it** as a single concrete thing in `## Notes`: a sample of the export, or its header row plus two or three example rows naming the amount, date and description columns. A park with no stated exit is indistinguishable from abandonment.
  - Raised `priority` from `medium` to `high`. Rationale: the stakeholder said "the import's part of what I asked for too", which under `spec/ids-and-statuses.md` §6 is the definition of `high` ("required for the epic's stated outcome") rather than `medium` ("the epic is coherent without it"). Checked that this does not disturb the delivery order decided under Q-003: the orchestrator's selection key breaks a priority tie on `created` ascending, and WI-0002 was created at 23:22:38 against this item's 23:22:40, so WI-0002 is still selected first.
  - Did **not** close this item as `dropped`. The stakeholder explicitly refused to drop it.
  - Did **not** touch AC1 or AC2. Neither can be made decidable without the layout, and rewriting them to something decidable would mean choosing a layout.
  - Left the second unknown Q-001 raised — that a bank row says who was charged but not who shared — untouched and still recorded as refinement's, since it is a consequence of the layout.
  - Noted the consequence for the engagement rather than hiding it: with this item at `blocked`, EP-001 cannot end as fully delivered, and at rest the termination question will name it as not delivered and put the choice back to the stakeholder.
- **Questions raised:** none. Re-asking for the sample would repeat a question the stakeholder has already replied to, and effort is not an escalation condition.
- **Commands:**
  - `scripts/transition WI-0003 --to blocked --actor answer-questions --resume-to draft` → this entry
- **Gates:**
  - `answer-is-propagated` → **pass** — Q-001's `## Consequences` names this item's `## Notes`, its priority and its history row; all three are present. Q-003's names the priority change and the not-dropped note; both present.
  - `answered-from-the-record` → **pass** — the park follows from the stakeholder's own reply, quoted verbatim in `## Notes` and in Q-001's `## Answer`. No ADR: the record is not silent, and no architectural choice was made — the layout is exactly what was *not* decided.
  - `escalation-is-justified` → **skipped** — nothing was escalated from this item.
  - `workspace-valid` → **pass** — run by this transition.
  - `item-resumed-correctly` → **skipped** — this item was not at `awaiting-answer` and had no `resume-to` to honour; it is being suspended, and the `resume-to: draft` it now carries is the status it is leaving.
  - `a-deferral-is-not-an-answer` → **pass** — Q-001's reply was a deferral. Of the two moves in `spec/question.md` §2 this execution took the first (decide under the deferral) at the epic level and expressed it here as the park: the reply settled the *choice* Q-001 offered — option A, not B and not C — but not the *layout*, so nothing anywhere claims the layout is known and the item that needs it is at `blocked` with its exit condition written down. See EP-001's journal entry for why the question itself could not be marked `deferred`.
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` — `priority` `medium` → `high`; `## Notes` rewritten with the park, its exit condition, and the effect on the epic's ending
- **Status:** `draft` → `blocked`
- **Result:** WI-0003 is parked at `blocked`, waiting on one thing and saying so. Nothing about the bank's CSV format has been invented, and the item was not dropped.
