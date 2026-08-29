# CHECKPOINT

## Current unit: META-127 — the dual regression gate, launched

**Session:** builder 3. Phase IV of `meta/plan.md`. META-119..126 done and pushed.

**Intent.** Two runs, detached, against the fixed kernel. Their configs differ from the
originals only in `id`, `project` and `max-turns`; the personas and probe scripts are byte-for-
byte the ones that produced F-062..F-067.

- **3b** — `iteration-3b-mdtab`, project `mdtab-3b`, persona `contradictory-stakeholder`, probe
  `iteration-3-mdtab` **including P-signoff-extension**. The pass condition is the sim saying its
  reserved line: the planted contradiction is escalated — a question quoting both stakeholder
  answers by ID — the scripted reconciliation *"the multiline case wins; I over-spoke before"* is
  elicited and recorded, and the engagement ends through the gate.
- **4b** — `iteration-4b-recall`, project `recall-4b`, persona `cooperative-pm`, probe
  `iteration-4-recall`. The pass condition is the boring run again, and this time an ending whose
  own audit signs with **zero new findings**: the claims gate examines a real scope, nothing is
  legally unfixable, and the driver labels the completed engagement `epic-done`.

Both projects are provisioned and the installed toolkit carries `lint-answers` and `scope.py`.
`--max-turns 30`.

**While they run:** META-128 — cluster 5, the triage of every remaining open finding. Do not
touch `harness/` or anything outside `meta/` while a run is in flight: the W4 contamination rule
fires on a repository that changes mid-turn, and `meta/` and `harness/` are the exempt paths —
so `meta/` only.

**When they stop:** their trails are read-only evidence from that moment (META-129), then
`meta/FINAL-REPORT-3.md` (META-130).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **A harness run is in flight.** Touch nothing outside `meta/`.
