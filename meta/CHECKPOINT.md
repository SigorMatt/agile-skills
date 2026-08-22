# CHECKPOINT

## Current unit: META-085 — F-018: the write guard decides on the target, not the sentence

F-018: `guard-workspace-writes.py` denies a Bash command when the command *string* contains a
guarded path and any redirect-ish character, so printing, grepping, or naming `tracker/board.md`
in a commit message is refused as though it were a write. A guard that fires on mentions trains
the agent to phrase around it.

Steps:
1. Rewrite the Bash branch to resolve **write targets**: redirections (`>`, `>>`, fd-prefixed,
   attached forms, heredoc destinations), and the argument positions of the mutating commands
   the guard knows (`tee`, `sed -i`, `dd of=`, `cp`/`mv`/`install`, `rm`/`truncate`/`shred`,
   `patch`). Anything unparseable is still allowed — the documented policy.
2. `adapters/claude-code/hooks/test_guard.py` — a table of commands that MUST be denied and
   commands that MUST be allowed, the allowed side seeded with the exact shapes F-018 names.
3. Wire it into `./scripts/check` as its own step.
4. Check green; FINDINGS; journal; commit; push.

Done when: the mention cases pass, the write cases are denied, and the new step is in `check`.

Next unit: **META-086** — F-001 (claim-provenance lint).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** `origin` is
  `git@github.com:SigorMatt/agile-skills.git`; `main` tracks it.
- This session MAY modify `methodology/`, `spec/`, `scripts/`, `adapters/`, `harness/`.
  It may NOT touch `meta/harness/evidence/**` (read-only history) and may not rewrite filed
  finding text (append corrections instead).
- Every change traces to an F-### or H-###. Anything unfiled gets filed first.
- Behavioural skill change ⇒ version bump in `skill.yaml`. Spec change ⇒ append to that spec
  file's `## Revisions` section. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture proving the old failure is now blocked.
- Toolkit commits and harness commits stay separate (two ledgers, two prefixes).
