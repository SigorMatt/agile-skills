# CHECKPOINT

## Builder session six is RUNNING. Mission: `meta/BUILDER-6-PROMPT.md`; plan: `meta/plan.md` Phase VII.

**Done so far.** META-167 (`cd00504`) one mask for every citation surface · META-168 (`656b6c5`)
severity follows knowledge, plus `scripts/check` step 6a, the proof-case over a copy of the banked
iteration-5 evidence · META-169 (`c8f69b3`) ADR-0013, *a toolkit source is quoted and attributed,
not pointed at*: `claim.citation.outside-the-record` refuses a citation into any pruned directory,
`[src: toolkit: <document> <section> "<words>"]` replaces it. 46 steps, 110 fixture codes, 419
selftest cases.

**Current unit: META-170 — the grammar goes where the writer writes (F-114's placement half).**

Steps:
1. Derive, from the contracts rather than by hand, the set of skills whose obligations require
   "a citation that resolves".
2. Each of them states or directly points at the **citation forms table** by name — which forms
   exist, what makes one well-formed, workspace-relativity, the mention convention from META-168,
   and the toolkit ruling from META-169. Short in the skills; `spec/doc-header.md` §4a stays the
   single source.
3. A `./scripts/check` step derives that set the same way and asserts each one's procedure names
   the table, so the pointer cannot rot the next time a contract gains the obligation.
4. Re-render `adapters/claude-code/dist/`; bump whatever the repository's version discipline
   requires. F-114's placement half updated — the finding is then fixed in both halves.

Done when: F-114's own grep (`grep -rniE "workspace-relative|citation forms|forms table"` over the
installed skills, which returned nothing in the abandoned workspace) returns hits;
`./scripts/check` green; committed AND pushed.

**Next unit: META-171** — H-022: the bounded self-repair allowance in the driver. Harness commit,
separate as always.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten — and **the LAST status bullet is the current one** (F-112; step 17c).
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5r is staged in META-173 and is NOT run here; its
  probe is NOT read.
