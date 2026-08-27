# Builder micro-session 2.6 — iteration-2 preconditions

Location when adopted: meta/BUILDER-2.6-PROMPT.md. Paste everything below the line into Claude
Code at the repository root.

---

You are a deliberately small fix session. FINAL-REPORT-2.5 §9 gave iteration 2 a GO on two
conditions; your mission is exactly those conditions and nothing else. Standing discipline
applies (checkpoint, small pushed commits, findings statuses, version bumps, must-fail
fixtures for enforcement changes, META-### continues). Read FINAL-REPORT-2.5 §7/§9 and the
three findings before starting. Scope is closed: if you find something new, file it and leave
it open — this session fixes three findings.

1. **F-050 — an epic-level question cannot legally be deferred.** 1e's evidence already names
   the answer: a deferred sign-off is E3, and E3 belongs to review-close. Fix per ADR-0006's
   own method — and close the class on itself: extend the pipeline-invariant injection step
   (or add a lint) so that every rule naming a status is mechanically checked against both
   item types (`applies_to` completeness becomes a gate, not a thing a person remembers).
   Must-fail fixture: the exact contradiction 1e's architect would have hit on the other
   branch.

2. **F-049 — SKILL.md files claim the tool writes the **Status:** bullet; the tool refuses a
   body without one.** Six failed transitions a run, five files, one-word class of fix.
   Decide which side is right (tool or docs), fix all occurrences, and add the render check
   that keeps prose and tool behavior from disagreeing on this again if cheap; otherwise
   just fix and note.

3. **F-055 — review-close's "throwaway copy of the trunk" advanced the real trunk.** The
   procedure told a skill to do something dangerous without saying how. Name the mechanism
   (--detach or equivalent) in the contract, and add the must-fail case: the old procedure
   attempted, the damage now impossible or loudly refused.

Acceptance: ./scripts/check green (including the new fixtures); the three findings
`fixed (commit …)` with citations that resolve; affected versions bumped; one short closing
note appended to meta/FINAL-REPORT-2.5.md ("§11 — preconditions met, <date>, commits …")
rather than a new report. Then stop — do not run iteration 2; the owner launches it.

