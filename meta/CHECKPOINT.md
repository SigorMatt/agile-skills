# CHECKPOINT

## The mission is complete.

Every unit in [`plan.md`](plan.md) is ticked, every box in `seed/03-ACCEPTANCE.md` carries an
evidence pointer, and [`FINAL-REPORT.md`](FINAL-REPORT.md) is written. `./scripts/check` passes
with no skipped steps. The working tree is clean and `main` is pushed to `origin`.

There is no next unit. If you are a fresh session picking this up, read
[`FINAL-REPORT.md`](FINAL-REPORT.md) first — its §5 lists the recommended next iterations, in
order, with the reasoning for that order.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** Instructed by the human on
  2026-08-16; `origin` is `git@github.com:SigorMatt/agile-skills.git` and `main` tracks it.

## If you are starting the next iteration

The recommended first piece of work is `validate-claims` — a script that resolves every commit
sha cited in an artifact, checks line-count claims against `git diff --numstat`, and flags a
sentence repeated across documents whose wording has diverged. Four of the six findings in
`examples/toy-project/AUDIT.md` are in that class and none of them needed judgement. The two
checklist criteria added in response to the audit (`D12`, `DE6` in `spec/dor-dod.md`) are
**unexercised**, which is the argument for making the class mechanical rather than trusting
another checklist item.

## Where the toy run lives

It was executed in a standalone repository outside this one and imported without `.git`
(ADR-0004). That scratch repository is disposable — `examples/toy-project/` plus `IDEA.md` and
`HUMAN-SCRIPT.md` contain everything needed to reproduce the run from scratch, and
`import.sh` re-imports a fresh one.
