# CHECKPOINT

## Builder session six is RUNNING. Mission: `meta/BUILDER-6-PROMPT.md`; plan: `meta/plan.md` Phase VII.

**Current unit: META-167 — one masking rule for every citation surface.**

Steps:
1. Enumerate every site that scrapes the citation vocabulary (`CITATION_RE`, `problems_in`)
   across `scripts/` — resolution checks and *presence* checks alike — and name the record
   surface each one reads (history rows, journal bodies, question files, item files, documents,
   retro reports). `scripts/lib/record.py` is the record model; the list should come from it.
2. Fix the scraping once at the shared layer in `scripts/lib/claims.py`: a presence check must
   read masked text, so a backticked example can no longer satisfy a rule that wants a real
   citation, and a backticked example can no longer be refused as a broken one.
3. A fixture per surface, both directions: the mention that used to trip (or used to pass
   falsely), and a real unresolved citation on the same surface.

Done when: `./scripts/check` is green, the new fixtures are mutation-checked non-vacuous, and
the unit is committed AND pushed.

**Next unit: META-168** — severity follows knowledge (unrecognised form is a WARNING, recognised
and unresolvable stays an ERROR), the mention convention into the forms table, F-113 + F-075
statuses, and the proof-case over a scratch copy of the banked iteration-5 workspace.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten — and **the LAST status bullet is the current one** (F-112; step 17c).
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5r is staged in META-173 and is NOT run here; its
  probe is NOT read.
