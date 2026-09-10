# Journal — WI-0004

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-10T13:29:37Z — answer-questions v0.6.2 — architect

- **Item:** WI-0004
- **Trigger:** created by `answer-questions` while consuming the stakeholder's answer to `EP-001/Q-005`; not dispatched by `next`
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-005.md` (the answer that implied this work)
  - `tracker/items/EP-001/item.md` (scope, to check no existing item already covered it)
  - `tracker/items/WI-0002/item.md`, `tracker/items/WI-0003/item.md`
  - `.claude/agile-skills/spec/ids-and-statuses.md` §5 (creation authority)
- **Decisions:**
  - Filed as its own work item rather than as extra criteria on WI-0002. Widening an existing item to swallow new work hides the scope change from the board and from the person who asked for it (`spec/ids-and-statuses.md` §5, F-029); a new item at `draft` puts it where `refine` will reach it.
  - `depends-on: WI-0002`, not WI-0001. A move changes two balances, and balances are WI-0002's; without them there is nothing observable for AC2 to assert.
  - Left the command word, argument order and amount format unpinned. They must match WI-0002's, and WI-0002 has not fixed them either — `refine` pins both together rather than this item guessing first.
- **Questions raised:** none
- **Commands:**
  - `scripts/new-item --id WI-0004 --type work-item --epic EP-001 --status draft --actor answer-questions --arose-from EP-001/Q-005` → exit 0
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
  - `tracker/items/WI-0004/item.md` (new — story, five acceptance criteria, out of scope, notes)
  - `tracker/items/WI-0004/history.md`, `tracker/items/WI-0004/journal.md` (new)
- **Status:** `—` → `draft`
- **Result:** WI-0004 exists at `draft` and carries the stakeholder's own reason for wanting it. It is the counterpart to WI-0002 AC6: refusing an overspend is only workable because this command exists.
