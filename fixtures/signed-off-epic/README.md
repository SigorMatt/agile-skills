# An epic the stakeholder actually accepted

The counterpart of `../broken-workspace`'s EP-001. `scripts/check-epic-signoff EP-001` must pass
here and fail there, which is what proves DE7 is a gate rather than a wish.

Captured from a real scratch run rather than hand-authored, so the timestamps and history rows
are ones the tools produced: the child WI-0001 reached `done`, and only then was the sign-off
filed, answered "accept with the import as a follow-up", and recorded. Move the sign-off's
`created` earlier than the child's close and the gate refuses it — that case is exercised in
`meta/journal.md` under META-088.
