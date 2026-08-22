# CHECKPOINT

## Current unit: META-084 — F-017: a journal header no skill can invent

F-017 + its two addenda: skills write *plausible* timestamps instead of reading a clock (run 1c
stamped eleven entries across a next-morning half-day for work done in minutes), and they invent
version strings too (run 1b's "review-close v0.1.0" against an installed 0.1.2). The class fix is
that no self-reported header field is authored by the model.

Steps:
1. `scripts/journal-entry` — the only sanctioned writer of a `journal.md` entry. It stamps the
   heading itself: clock for the timestamp, the installed `skill.yaml` for version and persona.
   The caller supplies only the bullets. Monotonic clamp announced, as `transition` does.
   `--restamp-last` is the journal's counterpart of the history repair.
2. `scripts/transition --journal-body-file` — history row and journal entry from **one** clock
   read, with the `**Status:**` bullet written by the script from the move it just made.
3. `spec/journal-and-history.md` — a timestamp is read from a clock and never estimated; header
   fields come from a mechanical source; the restamp exception now covers `journal.md`.
4. `scripts/validate-workspace` — `journal.timestamp.future`, `history.timestamp.future`,
   `journal.timestamp.outside-activity`, `history.timestamp.outside-activity`,
   `journal.version.impossible`.
5. Must-fail fixture cases for each; EXPECTED-CODES updated.
6. Ship the new script in the adapter; re-render; `./scripts/check` green; FINDINGS, journal,
   commit, push.

Done when: check green, and a demonstration that an entry stamped in 1c's shape is rejected.

Next unit: **META-084b** — every skill's `## Journaling` section adopts the script; version bumps.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** `origin` is
  `git@github.com:SigorMatt/agile-skills.git`; `main` tracks it.
- This session MAY modify `methodology/`, `spec/`, `scripts/`, `adapters/`, `harness/`.
  It may NOT touch `meta/harness/evidence/**` (read-only history) and may not rewrite filed
  finding text (append corrections instead).
- Every change traces to an F-### or H-###. Anything unfiled gets filed first.
- Behavioural skill change ⇒ version bump in `skill.yaml` (patch for a fix, minor for a contract
  change). Spec change ⇒ append to that spec file's `## Revisions` section. Re-render after any
  of it.
- Every enforcement fix ships a must-fail fixture proving the old failure is now blocked.
- Toolkit commits and harness commits stay separate (two ledgers, two prefixes).
