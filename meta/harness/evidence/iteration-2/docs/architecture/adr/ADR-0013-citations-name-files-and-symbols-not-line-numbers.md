---
title: Citations in docs/ name files and symbols, never line numbers
version: 1
status: current
updated: 2026-08-28T13:51:07Z
updated-by: plan
updated-for: BUG-0006
---

# ADR-0013 — Citations in `docs/` name files and symbols, never line numbers

- **Status:** accepted
- **Date:** 2026-08-28
- **Decided by:** plan (architect), for BUG-0006
- **Supersedes:** —

## Context

Three `[src: path:line]` citations survive in `docs/`, and **all three now point at lines that do
not support the sentences they are attached to** [src: BUG-0006; src: ADR-0008; src: ADR-0009;
src: run: grep -rn "\.py:" docs/architecture/adr/ADR-0008-help-text-is-prose-guarded-by-a-test.md
docs/architecture/adr/ADR-0009-one-entry-that-cannot-be-examined-is-a-leave.md → exit 0, four hits:
the three citations, at ADR-0008 line 48 and ADR-0009 lines 23 and 106, every one of them
`tidy/cli.py`, plus one prose mention of the form in ADR-0009's change log. This record's own
`## Context` table quotes all three, so a sweep of the whole of `docs/` also returns those quotes].

| citation | what its sentence means | where that is today | what is at the cited line today |
|---|---|---|---|
| `ADR-0008:48` → `tidy/cli.py:52` | `build_parser` runs before `parse_args` has said where the rules came from | `tidy/cli.py:62`, `args = build_parser().parse_args(argv)` | a docstring inside `render` |
| `ADR-0009:23` → `tidy/cli.py:67` | `cli.py`'s `except OSError`, ADR-0006's target-folder handler | `tidy/cli.py:88-90` | a comment about the `--rules` file |
| `ADR-0009:106` → `tidy/cli.py:93` | only a `"failed"` outcome makes the process exit non-zero | `tidy/cli.py:114`, the module's last statement | a blank line |

Every one of the three claims is still **true**; only the pointers are wrong
[src: tidy/cli.py; src: BUG-0006].

Two facts make this a decision rather than an edit.

**The first is that the drift already recurred, on the citations that were meant to be immune.**
BUG-0004/Q-002 made ADR-0009's six `tidy/planner.py:NN` citations file-level and deliberately left
its two `tidy/cli.py:NN` ones alone because they were exact; BUG-0006 AC2, written the same day,
records them as "exact and must stay so" [src: BUG-0004/Q-002; src: BUG-0006 AC2]. They were exact
then and they are not now, and the thing that moved them is the next item's merge — WI-0003 adding
the `--rules` block to `cli.py`, twenty-one lines above both
[src: run: git show cea3b907:tidy/cli.py | grep -n "" | sed -n "67p;93p" → exit 0, `except OSError
as error:` and the `return 1 if any(...)` statement, both exactly as cited;
src: run: git show 82a7d26:tidy/cli.py | grep -n "" | sed -n "67p;93p" → exit 0, a `--rules`
comment line and a blank line]. So the premise under "must stay so" had already failed, before any
work on this item began, in under two hours of project time.

**The second is that no gate can catch it.** `spec/doc-header.md` §4a makes `path` and `path:line`
one citation form with one test — that the file exists — so `scripts/lint-claims` passes on all
three [src: .claude/agile-skills/spec/doc-header.md; src: BUG-0006]. What fails is a person: D12 tells a reviewer to
open what a sentence cites and decide from what is there, and a reviewer who does that lands on a
docstring, a comment and a blank line [src: .claude/agile-skills/spec/dor-dod.md].

This project has already chosen a rule for the case, in ADR-0009 v2's `## Consequences`: "an ADR
about a change to a file cites that file, and the change is what moves its own line numbers", with
the named symbols in the prose carrying the precision [src: ADR-0009]. What has not been decided is
whether that rule is the general one for `docs/` or a remedy applied once, and BUG-0006 leaves the
choice here in terms [src: BUG-0006].

## Options considered

- **A — Repoint each citation at its current line: `:52` → `:62`, `:67` → `:88`, `:93` → `:114`.**
  Cost: three numbers, and the two ADR-0009 citations keep the exactness BUG-0006 AC2 asks them to
  keep, which is the reading that honours the criterion's parenthetical literally. Risk, and the
  decisive one: this is the remedy whose failure the context above measures. The same two citations
  were repointed-by-hand-equivalent — left exact — nineteen hours ago and drifted again on the very
  next merge, with no gate to notice and no criterion in any item to catch it. Choosing A is
  choosing to schedule the same defect again, and BUG-0006's own `## Notes` says so: "after this
  item, nothing prevents the next code edit from re-breaking any `path:line` citation that
  survives" [src: BUG-0006].
- **B — Make all three file-level, and let the symbols already named in the prose carry the
  precision.** `[src: tidy/cli.py]` in each of the three places; no prose is rewritten, because each
  sentence already names its target in backticks — `build_parser` and `parse_args` for the first,
  `except OSError` for the second, `apply_plan` and `"failed"` for the third — and each is a search
  term that lands a reader on the statement in one `grep`
  [src: run: grep -c "parse_args" tidy/cli.py → exit 0, 1; src: run: grep -c "except OSError"
  tidy/cli.py → exit 0, 1; src: run: grep -c "apply_plan" tidy/cli.py → exit 0, 2 — the import and
  the call, with the return statement the sentence is about five lines below the call]. Cost: a reader gets a file and a symbol instead of a line, so following a
  citation is a `grep` rather than a `sed -n`. It also does not honour BUG-0006 AC2's "must stay
  so" in its literal form — though it satisfies AC2's own normative sentence, which is that no
  `path:line` citation points at a line that does not support its sentence, and satisfies it
  permanently rather than until the next merge. Risk: a sentence whose subject is *not* named in
  the prose would lose its precision entirely under this rule; none of the three is such a
  sentence, and the rule as stated requires the symbol.
- **C — Keep the line numbers and add a gate that checks them.** A script that reads each
  `path:line` citation, opens the line, and fails when it is blank or does not contain the symbol
  the sentence names. Cost: the gate lives in `.claude/agile-skills/scripts/`, which is the toolkit
  running this project and not part of `EP-001`; BUG-0006's `## Notes` rules it out on exactly that
  ground [src: BUG-0006]. Risk: even inside the toolkit it is the harder thing to get right — "does
  this line support this sentence" is the human read D12 exists for, and a mechanical proxy for it
  would pass on a line that merely contains the right word.
- **D — Leave it.** Cost: none today. Risk: three `status: current` ADRs keep citations a reviewer
  cannot follow, which is the failure D12 exists to catch and the reason this item was filed.

## Decision

**B, as a rule for the whole of `docs/` and not only for these three sentences.** A citation under
`docs/` names a **file**, and the sentence names the **symbol** — a function, a method, a statement
form, or a literal string — so that a reader gets from the sentence to the evidence in one `grep`
that survives every edit above it. Line numbers do not appear in a `src` citation
[src: ADR-0009; src: BUG-0006].

Checkable against the repository as: the citation sweep in BUG-0006 AC2 returns no citation
carrying a line number, and each of the three sentences this item touches still names its subject
in backticks [src: BUG-0006 AC2; src: tidy/cli.py].

Two things this decision does **not** disturb:

1. **`run:` citations keep their commands and outcomes.** They are not paths and the drift this ADR
   is about cannot reach them; ADR-0008 v2 already records why a `run:` citation states an outcome
   rather than a snapshot [src: ADR-0008].
2. **Citations to items, criteria, questions and ADRs are unaffected.** `BUG-0004 AC3` and
   `WI-0003/Q-002` name things whose identity does not move [src: .claude/agile-skills/spec/doc-header.md].

## Consequences

- A reviewer performing D12 on any document in `docs/` can follow every citation and land on
  something, which is the property BUG-0006 was filed to restore
  [src: BUG-0006 AC1; src: .claude/agile-skills/spec/dor-dod.md]. What they land on is a file, and
  the sentence tells them what to look for in it.
- **The exactness BUG-0006 AC2 asks ADR-0009's two citations to keep is not kept, and the record
  says so rather than quietly dropping it.** AC2's normative sentence — no `path:line` citation
  points at a line that does not support its sentence — is satisfied, and by construction: after
  this item there are no `path:line` citations at all, so the grep it prescribes returns nothing.
  The parenthetical asking those two to stay exact rested on their being exact, and they had
  stopped being so before this plan was written. `verify` should decide AC2 against its first
  sentence and against this consequence, with the git evidence in `## Context` in front of it.
- **Nothing enforces this rule.** `lint-claims` cannot tell a file citation from a line citation —
  §4a makes them one form — so a future document may reintroduce `path:line` and no gate will
  object. The enforcement is that this ADR exists to be cited, and that `plan` and
  `answer-questions` are the two skills that write citations. That is weaker than a gate and it is
  the honest state; option C is what a gate would look like and why it is not this project's to
  build.
- **Reversibility: cheap.** Three citations in two files, one commit, no code, no interface, no
  data. Reversing to A means putting three numbers back and accepting that they go stale; reversing
  to C means work in a repository this project does not own.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-28T13:51:07Z | plan | BUG-0006 | First version: citations under `docs/` name a file and the prose names the symbol, generalising the rule ADR-0009 v2 recorded for one document, after all three surviving `path:line` citations were found pointing at lines that do not support their sentences |
