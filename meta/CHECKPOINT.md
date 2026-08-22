# CHECKPOINT

## Current unit: META-086 — F-001: claim provenance, mechanized

F-001 is the thesis finding: every machine-decidable gate held in the toy run, every gate resting
on a human-style read did not, and a wrong justification propagated to a seventh document. D12
and DE6 were the response and are `[skill]` checks — the kind that does not hold. This unit turns
the class into a program.

Steps:
1. `spec/doc-header.md` — the citation convention: `[src: ...]` with a closed set of **resolvable**
   forms (a workspace path, an item ID, an item's AC, a question, an ADR number, a commit sha, a
   command with its recorded outcome).
2. `scripts/lint-claims` — two rules. (a) every `[src: ...]` must resolve. (b) a paragraph in
   `docs/**` that makes an **absolute** claim about a named code object (`no`/`never`/`only`/
   `every`/`cannot`… together with a backticked identifier or a path) must carry at least one
   citation. `--changed-since <ref>` scopes rule (b) to what this execution actually touched,
   the same scoping D7 and D12 already use.
3. `validate-workspace` — `claim.citation.unresolved` over the whole workspace (rule (a) only;
   rule (b) belongs to the gate, not to the resting state of a historical record).
4. New hard gate `claims-are-sourced` on `plan`, `implement`, `review-close`; minor bumps.
   A hard gate makes `transition` refuse the completion move, which is what "unskippable" means
   here — `--force` remains, and remains recorded forever.
5. `spec/dor-dod.md` — D12 and DE6 gain the mechanical half.
6. Must-fail fixture: an unresolvable citation, and an unsourced absolute claim.
7. Re-render; `./scripts/check` green; FINDINGS; journal; commit; push.

Done when: check green, and both new rules demonstrated firing and passing.

Next unit: **META-087** — F-013 (an epic becomes suspendable).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** `origin` is
  `git@github.com:SigorMatt/agile-skills.git`; `main` tracks it.
- This session MAY modify `methodology/`, `spec/`, `scripts/`, `adapters/`, `harness/`.
  It may NOT touch `meta/harness/evidence/**` and may not rewrite filed finding text.
- Every change traces to an F-### or H-###. Anything unfiled gets filed first.
- Behavioural skill change ⇒ version bump in `skill.yaml`. Spec change ⇒ append to that spec
  file's `## Revisions` section. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture proving the old failure is now blocked.
- Toolkit commits and harness commits stay separate (two ledgers, two prefixes).
