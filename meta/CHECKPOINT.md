# CHECKPOINT

## Builder session six is RUNNING. Mission: `meta/BUILDER-6-PROMPT.md`; plan: `meta/plan.md` Phase VII.

**META-167 is DONE** (commit `cd00504`, pushed): one masking rule for every citation surface —
`citations_in()` / `carries_citation()` in `scripts/lib/claims.py`, four unmasked sites converted,
the surface table in the module docstring, `lint-retro`'s own F-054 bug fixed on the way,
`selftest.py` 357 → 369.

**Current unit: META-168 — severity follows knowledge.**

Steps:
1. `CitationResolver` classifies a problem instead of only describing it: a marker whose body
   matches a **known form** and does not resolve is one thing; a marker matching **no form at
   all** is another, because the gate cannot tell a mention from a typo. `problems_in()` carries
   the classification to its three callers (`validate-workspace.check_claim_citations`,
   `lint-claims` rule 1, `lint-retro.check_citations`).
2. Recognised-and-unresolvable stays an ERROR under `claim.citation.unresolved`. Matching no form
   becomes a WARNING under its own code, whose message teaches both escapes: backtick it if it is
   a mention, and here are the forms if it is a citation.
3. The mention convention (backticked = mention) moves out of the `problems_in()` source comment
   into `spec/doc-header.md` §4a's citation forms table, with the cost of the warning said plainly
   rather than left to be discovered.
4. The proof-case, over a scratch COPY of `meta/harness/evidence/iteration-5-envel-abandoned/`
   (read-only source): zero errors from the mention at `tracker/items/WI-0002/history.md:14`, and
   a planted genuinely-bad citation in the same copy still failing. Both outputs recorded.
5. F-113 and F-075 statuses updated together, each saying they are one class.

Done when: `./scripts/check` green, the new cases mutation-checked non-vacuous, committed AND
pushed.

**Next unit: META-169** — the toolkit-path ruling (ADR-0013): `[src: .claude/agile-skills/...]`
is refused, and a `toolkit:` quote-and-attribute form replaces it.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten — and **the LAST status bullet is the current one** (F-112; step 17c).
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5r is staged in META-173 and is NOT run here; its
  probe is NOT read.
