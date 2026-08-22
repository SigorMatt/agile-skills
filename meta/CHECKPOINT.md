# CHECKPOINT

## Current unit: META-084b — F-017 adoption: every skill journals through the tool

META-084 built the mechanism (`scripts/journal-entry`, `transition --journal-body-file`,
`spec/journal-and-history.md` §0). This unit makes the skills use it.

Steps:
1. Each skill's `## Journaling` section gains the same short "how to write it" block: the body
   is written to a file, the entry is appended by `journal-entry`, and an entry that accompanies
   a status change goes through `transition --journal-body-file`. `next` is exempt (it journals
   nothing).
2. `intake`'s "then append `— → open` to history.md" instruction is replaced by the tool.
3. Patch-bump every skill whose `process.md` changed; re-render.
4. `./scripts/check` green; FINDINGS F-017 note updated with the adoption commit; journal;
   commit; push.

Done when: check green and no skill still describes writing a journal heading by hand.

Next unit: **META-085** — F-018 (the write guard matches the target, not the command string).

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
