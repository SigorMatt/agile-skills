# Journal — BUG-0001

## 2026-08-16T12:00:00Z — verify v0.1.0 — qa-engineer

- **Item:** BUG-0001
- **Trigger:** defect found while verifying WI-0001
- **Inputs read:** WI-0001 item.md
- **Decisions:** filed as a bug because no AC of WI-0001 covers this behaviour
- **Questions raised:** none
- **Commands:** none
- **Gates:** workspace-valid → pass
- **Artifacts:** BUG-0001
- **Status:** `—` → `ready`
- **Result:** Bug filed.

## 2026-08-16T12:25:00Z — implement v0.1.0 — developer

- **Item:** BUG-0001
- **Trigger:** status `in-progress`, dispatched by `next`
- **Inputs read:** BUG-0001 item.md
- **Decisions:** none
- **Questions raised:** none
- **Commands:** none
- **Gates:** workspace-valid → pass
- **Artifacts:** commit 234f170
- **Status:** `in-progress` → `verifying`
- **Result:** F-019 in one entry — the transition was journalled and committed, and the
  `transition` call that was chained after a failed `cd` never ran, so history.md has no such
  row and the item never left `in-progress`.
