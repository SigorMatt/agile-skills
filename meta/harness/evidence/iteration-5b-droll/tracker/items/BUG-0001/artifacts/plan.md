# Plan — BUG-0001 A stray file named 'planned' is tracked at the repository root

## Problem

A 3289-byte file named `planned`, holding captured `run-gate` output, is tracked at the
repository root. It entered at `6788e55` when an unquoted `--resolving WI-0001:ready->planned`
was read by the shell as a redirect: the argument was truncated at `ready-` and the gate output a
person was meant to read went into a new file named after the truncated half
[src: BUG-0001]. Nothing about droll depends on it — the tool, its tests, its lint and its
documents are all independent of it, and `validate-workspace` passes with it present. What is
wrong is the record: the repository carries an artifact nobody declared, and
`spec/workspace-layout.md` §1 says a workspace root holds `tracker/`, `docs/` and the project's
own source. The change is one deletion, on a branch, merged to the trunk, with a commit that
names the item so `git log --grep BUG-0001` reconstructs it. The constraint that shapes the rest
of this plan is that **nothing observable about droll may change**: the fix is to the repository,
not to the program.

## Approach

Delete the file with `git rm` on a branch, and let the ordinary close merge that deletion into
the trunk. No droll source file, no test and no document is edited.

Three things follow from the problem being a repository artifact rather than a program defect,
and each is a decision rather than an omission:

- **No `unittest` regression test.** `tests/` holds `unittest.TestCase` classes about the dice
  roller [src: ADR-0002], and a test asserting the absence of a file at the repository root is
  not about the dice roller. The item says so itself and provides `AC3` as the regression check
  instead: re-run the command that caused the file, with the quoting that prevents it, and
  observe both that its output reaches the terminal and that no file appears
  [src: BUG-0001 AC3 "writes its output to the terminal and creates no file"].
- **No `.gitignore` entry.** Adding `planned` to `.gitignore` would hide the symptom rather than
  remove it, and would silently ignore a legitimately-named file if the project ever grew one.
  No acceptance criterion asks for it. Recorded under `## Out of scope for this item`.
- **No document is named by this plan**, and that is deliberate rather than an oversight —
  see `## Decisions and ADRs` D2, because naming one would have a mechanical consequence this
  item does not deserve.

## Steps

1. **Create the branch.** `git checkout -b wi/BUG-0001 main`, from the trunk at the tip that
   carries `WI-0001`'s merge. Afterwards: `git rev-parse --abbrev-ref HEAD` prints
   `wi/BUG-0001`, and `ls planned` still finds the file, because nothing has been removed yet.

2. **Delete the file and commit.** `git rm planned`, then one commit whose subject follows
   `tracker/project.yaml`'s `conventions.commit-subject` and names the item — for example
   `repo: delete the stray captured gate output at the root (refs BUG-0001)`. Change no other
   path: `git show --stat HEAD` must list exactly one file, `planned`, as a deletion.
   Afterwards: `ls planned` reports no such file; `git ls-files | grep -vE
   '^(droll|tests|docs|tracker|\.claude)/'` returns `.gitignore`, `CONSUMER-PROMPT.md`,
   `IDEA.md` and `SIMULATION-NOTICE.md`, and not `planned`; and `git log --oneline --all --
   planned` shows `6788e55` **and** this new commit, because a deletion adds history rather than
   rewriting it.

3. **Run the regression check `AC3` names, verbatim and with the argument quoted.**
   `python3 .claude/agile-skills/scripts/run-gate --skill plan --item WI-0001 --all --resolving
   'WI-0001:ready->planned'`. Afterwards: the gate verdicts appear on the terminal,
   `git status --short` prints nothing, and `ls planned` still reports no such file. The single
   quotes are the whole of the fix being demonstrated — without them the shell reads `> planned`
   as a redirect and recreates the bug.

4. **Run the project's declared commands, to show that nothing about droll moved.**
   `python3 -m unittest discover -s tests -t .` and `python3 -m compileall -q droll tests`.
   Afterwards: both exit 0, and the test count is whatever the suite holds — this plan states no
   number, because a number here is one somebody would have to amend
   (`spec/dor-dod.md` R11). `git diff main..HEAD --name-only` lists `planned` and nothing else,
   which is the evidence that the suite passing is not a claim about an unchanged suite but about
   an untouched one.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `git ls-files \| grep -vE '^(droll\|tests\|docs\|tracker\|\.claude)/'` no longer lists `planned`, on the trunk, and `ls planned` reports no such file | 2 | Both commands, run at the branch head, where the deletion is. **"On the trunk" is settled in two stages and neither is a re-reading of the criterion.** `verify` runs before the merge, so what it can observe is the branch head plus the fact that the branch's tree is what the trunk receives; `review-close`'s trial merge into a detached worktree of `main` is where the commands can be run against the actual merge result, before the close, and the same two commands on `main` after the merge settle it finally. This is the same shape as `WI-0001`'s D9 and for the same reason: the close must precede the merge |
| AC2 — the deletion is a commit on the trunk referencing `BUG-0001`, and `git log --oneline --all -- planned` still shows `6788e55` | 2 | `git log --grep BUG-0001 --oneline` returns step 2's commit; `git show --stat` on it shows exactly one deleted path. `git log --oneline --all -- planned` returns two lines, `6788e55` among them, which is the observation that no history was rewritten. `check-commit-refs BUG-0001 wi/BUG-0001` is the gate that reads the same thing mechanically |
| AC3 — the quoted `run-gate` command writes to the terminal and creates no file; `git status --short` is empty afterwards and `ls planned` still reports no such file | 3 | The command run verbatim, its output read from the terminal rather than from a file, then `git status --short` and `ls planned`. Already exercised once by this planning execution on the pre-fix tree: the command printed eight gate lines, exited 0, and `git status --short` was empty [src: run: python3 .claude/agile-skills/scripts/run-gate --skill plan --item WI-0001 --all --resolving 'WI-0001:ready->planned' → exit 0, git status --short empty]. That is evidence the criterion is demonstrable, not evidence it is met — it is met when step 3 is run after step 2 and `ls planned` reports nothing |

## Assumptions

- **A1 — the file has no reader.** Nothing in `droll/`, `tests/`, `docs/`, `tracker/` or
  `.claude/` opens, imports or names a path called `planned`; the only occurrences of the word in
  the workspace are this item's own prose and the status name `planned` in the pipeline's status
  graph, which is not a path. **Reversing it** costs one `git revert` of step 2's commit, which
  restores the file byte for byte because the deletion does not rewrite history — the cheapest
  kind of reversal there is. No delegation licensed this and none was needed: it is a reading of
  the repository, not of the stakeholder's intent.
- **A2 — the commit scope prefix is `repo:`.** `conventions.commit-subject` is
  `<scope>: <summary> (refs <ITEM-ID>)` and fixes the shape but not the vocabulary; the branch so
  far uses `droll:` for source and `tracker:` for the record, and this commit is neither.
  **Reversing it** costs nothing that matters — no gate reads the scope word, only that the
  subject names the item — so `implement` may choose differently without filing anything.

## Decisions and ADRs

Both decisions below came from **branch 1 of the preference order**: they were answered from
documents already in the repository, and are cited rather than re-decided. No ADR is written,
because neither introduces a commitment a future execution would need to read in order to know
whether it may revisit something — and an ADR trail padded with non-decisions is one the real
decisions hide in.

- **D1 — the regression check is `AC3`, not a `unittest` case.** Answered from `ADR-0002`, which
  scopes `tests/` to `unittest.TestCase` classes exercising droll, and from the item's own
  `## Notes`. The alternative — a test that shells out and asserts a file's absence — would put a
  claim about the repository inside the dice roller's suite, where the next person to read it
  would have no idea why it is there.
- **D2 — this plan names no document, and the `## Invalidation set` is `none`.** Answered from
  `ADR-0004` point 4a, which records that `--plan-documents` widens `implement`'s
  `claims-are-sourced` window to **every document the plan names**, whatever the change did to
  it. `docs/product/vision.md` carries an unsourced absolute inside its `## Engagement state`
  section that no skill may repair before the engagement ends, and `ADR-0004` says in terms that
  a later item meeting that shape *"gets its own decision, not this one"* [src: ADR-0004]. Naming
  `vision.md` here defensively would drag that sentence into this item's gate window and buy
  `BUG-0001` — a one-line deletion — a forced hard gate and a third override decision. It is not
  named because **it is not at risk**: deleting a stray file at the repository root cannot make
  a sentence about the engagement true or false. The alternative was considered and rejected on
  exactly those grounds, which is why this is a decision and not a blank.

## Invalidation set

| document | what | kind | why | disposition |
|----------|------|------|-----|-------------|
| none | This change deletes one untracked-by-any-document file at the repository root and edits no source, no test and no document. `docs/` was read rather than recalled — all six documents: `docs/product/vision.md`, `docs/architecture/overview.md` and `ADR-0001` to `ADR-0004`. The only sentence anywhere in `docs/` that mentions the repository root is `ADR-0002`'s *"Tests are `unittest.TestCase` classes under `tests/`, discovered from the repository root"*, which is about where discovery starts and is unaffected by which stray files are beside it; `grep -rn 'ls-files\|repository root\|planned' docs/` returns that one line and nothing else. No document describes the behaviour this item's criteria name, because the criteria are about git state rather than about droll | cited-fact | — | — |

`implement` closes every row and may add rows; if executing this plan turns out to falsify a
document, the row belongs here rather than in a journal entry.

## Deliverable documents

`none`. No acceptance criterion of this item has a document as its subject: `AC1` and `AC2` are
about git state and `AC3` is about a command's side effects. `implement` is therefore permitted
to write no document at all on this item, which is the correct permission for a change that
should touch nothing but one deletion.

## Binding ADRs

- **ADR-0002 — standard library only, including the tooling.** Binds step 4, which runs the two
  commands this ADR fixed as the project's test and lint commands, and binds D1: its scoping of
  `tests/` to `unittest.TestCase` classes about droll is what rules out a regression test for a
  repository-level defect. It also forbids reaching for any third-party tool in steps 1-3, which
  matters only in that nothing here needs one.
- **ADR-0004 — a gate that nobody is permitted to clear is overridden once, visibly, and named.**
  Binds D2. Point 4a states how `--plan-documents` widens `implement`'s `claims-are-sourced`
  window, and the ADR states that a later item meeting the same shape gets its own decision;
  together those are what make naming a document in this plan a choice with a cost rather than a
  free precaution. No override is sought for this item and none should be needed — the branch
  edits nothing under `docs/`, so `review-close`'s `--changed-since` window will contain no
  document at all.

- **ADR-0001 — the accepted dice expression grammar** and **ADR-0003 — rejection messages go to
  stdout at the prompt.** Listed, and **not engaged**: this change alters no line of droll and
  therefore neither what is accepted nor what is printed. They are in the list on purpose. The
  project has exactly four ADRs, so naming all four lets `verify` record a verdict for each —
  `not-engaged` is one of the three verdicts it may give — and lets `review-close`'s D13
  completeness question, *did the plan name every ADR this change engages?*, be answered by
  reading this list against the index rather than by re-deriving which ADRs exist. The two above
  are the two that constrain the design; these two are the two that were read and found not to.

## Scaffolding

`none`. This plan creates no file outside `tracker/` and `docs/`; both declared gate commands
already run in this project, unchanged, and step 4 runs them to show that they still do.

## Risks

- **`AC1` says "on the trunk" and `verify` runs before the merge.** This is the one place the
  plan could be executed correctly and still produce an argument. The mapping row above states
  which observation settles the criterion at each stage — branch head for `verify`, the detached
  trial merge for `review-close`, and `main` itself after the merge — so that nobody has to
  invent a reading. If `verify` judges the branch-head observation insufficient, the honest move
  is a question to the architect, not a loosened criterion.
- **Step 3 recreates the bug if the quoting is dropped.** The command in `AC3` contains a literal
  `>`. Run without the single quotes, the shell truncates the argument and creates the file
  again, which would fail `AC1` in the same execution that was demonstrating `AC3`. The step
  writes the command in full for that reason, and `git status --short` immediately afterwards is
  what catches it if it happens.
- **A deletion is invisible in a suite run.** Steps 1-3 produce no test signal at all — the suite
  passes before and after — so `git diff main..HEAD --name-only` listing exactly one path is the
  only evidence that this change is what it claims to be. Step 4 asks for it explicitly rather
  than leaving `verify` to think of it.

## Out of scope for this item

- **Adding `planned`, or any pattern, to `.gitignore`.** It would hide a recurrence rather than
  prevent one, and would silently ignore a legitimately-named file later. No criterion asks for
  it.
- **Any change to `run-gate`, `validate-workspace` or any toolkit script.** The item's `## Notes`
  is right that the general defect is in how an invocation is typed and that the `exited 2`
  message could hint that a shell may have eaten half an argument — but `.claude/` is the
  installed toolkit, not this project's source, and a finding about it travels upstream in the
  retrospective rather than in a droll work item.
- **Auditing the repository root for other undeclared files.** `git ls-files` currently returns
  four other root files — `.gitignore`, `CONSUMER-PROMPT.md`, `IDEA.md`, `SIMULATION-NOTICE.md` —
  and all four are the harness's or the project's own. `AC1` names `planned` and only `planned`;
  a wider sweep is a different item.
