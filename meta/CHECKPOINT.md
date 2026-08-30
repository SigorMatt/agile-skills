# CHECKPOINT

## Phase IV is complete. There is no next unit in this session.

Builder session three (`meta/BUILDER-3-PROMPT.md`) is done: META-119 through META-131, all
committed and pushed. `./scripts/check` is green across **28 steps**.

**The verdict:** all three ROADMAP §2 conditions read positive. **The kernel is proven.** The
gated tracks — the retro skill, the Codex adapter, the content packs — are the owner's to open.
The reasoning, the qualifications and the evidence line for each condition are in
`meta/FINAL-REPORT-3.md` §6 and in the 2026-08-30 addendum in `meta/findings/FINDINGS.md`.

## What the owner does next

The report names one thing as the next session's first unit, and it is not a fix:

**A regression run against the kernel as it now stands.** 4b ran on the kernel *after* 3b's four
fixes and *before* F-073's and META-131's five. Nothing in those six touches a skill contract and
every gate is green — but the last run tested a kernel one commit behind this one, and that is the
one gap in the proof. `iteration-3c` or `iteration-4c`, same configs, one run, read for nothing
but whether those six changes hold.

Then the two classes META-128's triage deferred, each an ADR-0006-shaped derivation rather than a
patch: the **half-written record** (F-036, F-043, F-051, F-053) and **document-as-deliverable**
(F-057, F-058). And **H-015** early, because it constrains every future session: the simulated
human's skill directory is one global path rewritten at the start of every sim turn, so two
iterations cannot run at once and nothing refuses them — this session ran 3b and 4b in series for
that reason alone.

Findings, of 87 filed: **72 fixed**, 11 deferred behind a named gate (4 in the *half-written
record* class, 2 in *document-as-deliverable*, 5 individually gated), **2 open** — F-061, the
conditional-acceptance observation held open deliberately, and H-015, filed this session and not
fixed because it touches `harness/` — 1 rejected, 1 a pointer to another entry (F-042 → F-029).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** `~/agile-skills-throwaway/mdtab-3b` and `recall-4b` hold the
  two completed engagements; both trails are banked under `meta/harness/evidence/`.
