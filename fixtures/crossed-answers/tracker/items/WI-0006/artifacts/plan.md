---
status: recorded
---

# Plan — WI-0006

Fixture. A delegation spent in an engagement that has filed neither a sign-off nor an ending
statement. There is nowhere yet to surface it, so this gate says so on stdout and reports
nothing: an ending with no ask at all is `check-epic-signoff`'s to refuse.

## Assumptions

- Requests are read in the order they were filed.
  **Under delegation:** `R-001` — how the stakeholder's own notes are queued.
