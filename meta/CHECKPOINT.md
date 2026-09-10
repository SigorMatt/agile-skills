# CHECKPOINT

## Builder session six is RUNNING. Mission: `meta/BUILDER-6-PROMPT.md`; plan: `meta/plan.md` Phase VII.

**Done so far.** META-167 (`cd00504`) — one masking rule for every citation surface.
META-168 (`656b6c5`) — severity follows knowledge: a marker matching no form is a WARNING under
`claim.citation.unrecognised`, a recognised one that fails stays an ERROR; the mention convention
is in `spec/doc-header.md` §4a; `scripts/check` step 6a is the proof-case over a copy of the
banked iteration-5 evidence. 46 steps, 109 fixture codes, 386 selftest cases.

**Current unit: META-169 — the toolkit-path ruling (ADR-0013).**

Steps:
1. ADR-0013: are `[src: .claude/agile-skills/...]` installed-toolkit paths a legal citation form?
   The ruling is **illegal-as-a-path, legal-as-a-quote** — derivation in the brief and in the ADR.
2. `spec/doc-header.md` §4a's forms table gains the `toolkit:` quote-and-attribute form and the
   refusal of the path form.
3. `scripts/lib/claims.py` enforces both; the refusal is an ERROR with its own code, because the
   gate knows exactly what is wrong and what to write instead.
4. A fixture proves both directions. The twelve citations in the banked evidence stay untouched —
   evidence is read-only and the ruling governs future writing.

Done when: `./scripts/check` green, mutation-checked non-vacuous, committed AND pushed.

**Next unit: META-170** — placement: the authoring skills state or point at the citation forms
table, and F-114's status is updated.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten — and **the LAST status bullet is the current one** (F-112; step 17c).
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5r is staged in META-173 and is NOT run here; its
  probe is NOT read.
