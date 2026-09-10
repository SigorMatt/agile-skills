# Journal — WI-0005

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-10T13:29:37Z — answer-questions v0.6.2 — architect

- **Item:** WI-0005
- **Trigger:** created by `answer-questions` while consuming the stakeholder's answer to `EP-001/Q-005`; not dispatched by `next`
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-005.md` (the answer that implied this work)
  - `tracker/items/EP-001/item.md` (scope, to check no existing item already covered it)
  - `tracker/items/WI-0002/item.md`, `tracker/items/WI-0003/item.md`
  - `.claude/agile-skills/spec/ids-and-statuses.md` §5 (creation authority)
- **Decisions:**
  - Filed as its own work item, for the same reason as WI-0004.
  - AC1 is deliberately loose: nothing in the record says how a person identifies the spend they mean — an index in a listing, a generated identifier, or a match on envelope, amount and date. Guessing here would have put a decision the stakeholder has never seen into an acceptance criterion; `refine` must pin it with them.
  - Scoped to correcting a *spend*, which is what they asked for. Whether income and transfers need the same treatment is left as a question for `refine` rather than assumed either way.
  - Recorded in `## Notes` that this answer replaced a line in `EP-001`, so a reader of this item alone can see that editing a transaction was once out of scope and on whose reading.
- **Questions raised:** none
- **Commands:**
  - `scripts/new-item --id WI-0005 --type work-item --epic EP-001 --status draft --actor answer-questions --arose-from EP-001/Q-005` → exit 0
- **Gates:**
  - `answer-is-propagated` → **pass** (this item *is* part of the propagation of `EP-001/Q-005`; it is named in that question's `## Consequences` and it exists)
  - `answered-from-the-record` → **pass** (the basis is the stakeholder's own words in `EP-001/Q-005`, quoted in `## Notes`)
  - `escalation-is-justified` → **skipped** (nothing was escalated from this item)
  - `propagated-claims-carry-their-obligation` → **pass** (`lint-documents --rule propagated-claims-carry-their-obligation --item EP-001 --uncommitted` → exit 0; this execution wrote no quantified sentence into `docs/`)
  - `engagement-state-is-left-to-the-ending` → **pass** (`lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0)
  - `cross-answer-consistency` → **pass** (`lint-answers --item EP-001` → exit 0; the checks live on the EP-001 questions)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0 after this entry)
  - `item-resumed-correctly` → **skipped** (this item was created, not resumed; the resumption gate applies to EP-001, which this execution returned to `open`)
  - `a-deferral-is-not-an-answer` → **skipped** (no reply on EP-001 deferred; all five were answered)
- **Artifacts:**
  - `tracker/items/WI-0005/item.md` (new — story, five acceptance criteria, out of scope, notes)
  - `tracker/items/WI-0005/history.md`, `tracker/items/WI-0005/journal.md` (new)
- **Status:** `—` → `draft`
- **Result:** WI-0005 exists at `draft`. Its hardest criterion — how a person names the spend they mean — is marked as unresolved rather than invented, and is what `refine` must settle first.
