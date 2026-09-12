---
id: BUG-0001
type: bug
title: A stray file named 'planned' is tracked at the repository root
status: planned
priority: low
epic: EP-001
created: "2026-09-11T22:47:26Z"
updated: "2026-09-11T23:18:10Z"
found-in: WI-0001
---

## Summary

A file named `planned`, 3289 bytes, sits at the repository root and is tracked by git. It holds
captured `run-gate` output and is not part of droll, of the tracker, or of the documentation. It
was found by `verify` while enumerating what `git ls-files` returns outside the declared
directories, checking a different claim in `WI-0001`'s invalidation set. It entered at commit
`6788e55`, *"tracker: the plan, the two ADRs and the architecture overview (refs WI-0001)"*, which
is `main`'s tip and the base of `wi/WI-0001` — so it is not in that branch's `main..HEAD` diff and
no gate on `WI-0001` ever had it in scope.

Its own first line records how it was made: `--resolving WI-0001:ready-` and `exited 2`, with
`validate-workspace: --resolving takes ITEM-ID:from->to[+journal]`. The argument
`WI-0001:ready->planned` was written unquoted, the shell took `> planned` as a redirect, truncated
the argument at `ready-`, and created the file it was named after. The gate output a person was
meant to read went into the file instead of onto the terminal, which is why nobody noticed.

Nothing about droll is affected: the tool's behaviour, its tests, its lint and its documents are
all independent of this file. What is affected is the record — the repository carries an artifact
nobody declared, and `git ls-files` is one of the things a later execution enumerates.

## Steps to reproduce

1. `cd` to the repository root and run `git ls-files | grep -vE '^(droll|tests|docs|tracker|\.claude)/'`.
2. Read the file: `head -2 planned`.
3. Confirm it is tracked rather than a local leftover: `git log --oneline --all -- planned`.

## Expected behaviour

Step 1 returns only files the project or the methodology declares. `spec/workspace-layout.md` §1
gives the tree a workspace root holds — `tracker/`, `docs/`, and the project's own source code —
and a file of captured gate output is none of the three. `tracker/project.yaml` declares droll's
source as `droll` and `tests`. Step 2 should find no such file.

## Actual behaviour

Step 1, verbatim:

```
.gitignore
CONSUMER-PROMPT.md
IDEA.md
SIMULATION-NOTICE.md
planned
```

Step 2, verbatim:

```
FAIL   workspace-valid  (hard)
       `/usr/bin/python3 /home/msi/agile-skills-throwaway/droll/.claude/agile-skills/scripts/validate-workspace --root /home/msi/agile-skills-throwaway/droll --resolving WI-0001:ready-` exited 2
```

Step 3, verbatim:

```
6788e55 tracker: the plan, the two ADRs and the architecture overview (refs WI-0001)
```

`ls -la planned` reports 3289 bytes.

## Acceptance criteria

- [ ] AC1 — `git ls-files | grep -vE '^(droll|tests|docs|tracker|\.claude)/'` no longer lists
      `planned`, on the trunk, and `ls planned` reports no such file.
- [ ] AC2 — the deletion is a commit on the trunk referencing `BUG-0001`, so
      `git log --grep BUG-0001` reconstructs it; and `git log --oneline --all -- planned` still
      shows `6788e55`, because the file's history is not rewritten.
- [ ] AC3 — running the command that produced it with the argument quoted —
      `python3 .claude/agile-skills/scripts/run-gate --skill plan --item WI-0001 --all --resolving 'WI-0001:ready->planned'` —
      writes its output to the terminal and creates no file: `git status --short` is empty
      afterwards and `ls planned` still reports no such file.

## Notes

**On AC3 and the Definition of Ready RB5.** A regression test in droll's own suite would be the
wrong instrument: this is not droll's behaviour, and `tests/` exists to hold `unittest.TestCase`
classes about the dice roller [src: ADR-0002]. AC3 is the regression check instead — it re-runs the
command that caused the file, with the quoting that prevents it, and asserts the absence rather
than asserting it once by hand. It fails against the original mistake and passes against the fix,
which is what RB5 asks a regression case to do.

**The general defect is in how a `run-gate` invocation is typed, not in `run-gate`.** The
`--resolving` argument contains a literal `>` and must be quoted; the toolkit's own skill
procedures show it quoted. The failure mode is silent in both directions at once — the file is
created, and the output the caller wanted to read disappears into it — and the truncated argument
then produced an `exited 2` that reads like a tool defect rather than a typing one. Worth sending
upstream: any argument carrying `>` has this shape, and the exit-2 message names the syntax
without hinting that the shell may have eaten half of it.

**Priority `low`, deliberately.** Nothing depends on the file, `validate-workspace` passes with it
present, and droll is unaffected. It is filed rather than fixed here because `verify` repairs
nothing it judges, and filed rather than sent back to `WI-0001` because no acceptance criterion of
that item reaches the contents of the repository root.
