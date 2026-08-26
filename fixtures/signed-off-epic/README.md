# An epic the stakeholder actually accepted

The counterpart of `../broken-workspace`'s EP-001. `scripts/check-epic-signoff EP-001` must pass
here and fail there, which is what proves DE7 is a gate rather than a wish.

Captured from a real scratch run rather than hand-authored, so the timestamps and history rows
are ones the tools produced: the child WI-0001 reached `done`, and only then was the sign-off
filed, answered "accept with the import as a follow-up", and recorded. Move the sign-off's
`created` earlier than the child's close and the gate refuses it — that case is exercised in
`meta/journal.md` under META-088.

**Edited once, on purpose (2026-08-27, META-105b).** The termination gate now requires the
statement to **name every child item by ID**, so that a child nobody remembered is in front of
the stakeholder rather than implied by its absence (F-046). The captured `## Question` described
what was delivered in prose and named nothing, so it would have failed the rule it is supposed to
demonstrate. The `## Question` section — and only that section — was rewritten to name `WI-0001`.
Everything else here is still what the tools produced.
