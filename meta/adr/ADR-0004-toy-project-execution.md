# ADR-0004 — How the toy project is executed and imported

- **Status:** accepted
- **Date:** 2026-08-17
- **Unit:** META-060

## Context

Acceptance C requires a small real project driven from idea to done **using only the rendered
skills**, executed by context-free subagents, and committed into this repository with its
complete paper trail. Acceptance C6 then requires a fresh subagent to reconstruct the run from
"the toy project's tracker + docs + git log".

Two of those requirements pull against each other. The pipeline needs a git repository: items
work on branches, `check-commit-refs` reads `git log`, `review-close` merges, and Definition of
Done D8 is "`git log --grep <ID>` reconstructs the item's code history". But a git repository
cannot simply live inside this repository — git will either treat it as a submodule gitlink,
recording a commit hash and none of the content, or refuse to track the `.git` directory
usefully. Either way the history would be present at run time and absent for a reader.

## Decision

1. **The run happens in a standalone git repository outside this one**, at
   `$CLAUDE_JOB_DIR/tmp/toy/linecount`. It is a real repository: real branches, real commits,
   real merges. Nothing about the run is simulated.

2. **The result is imported into `examples/toy-project/` without `.git`.** Source code, the
   whole `tracker/`, the whole `docs/`, and the installed-skill footprint that the run actually
   used.

3. **The git evidence is preserved as text**, generated from the real repository at import time:
   - `examples/toy-project/GIT-LOG.md` — `git log --all --stat --graph --date-order` with full
     subjects, so every commit, its item ID, its branch and its files are visible;
   - `examples/toy-project/GIT-BRANCHES.md` — the branch list and, per item, the output of
     `git log --grep <ITEM-ID> --oneline`, which is the exact command D8 names.

4. **The audit subagent (C6) is given `tracker/`, `docs/`, `GIT-LOG.md` and
   `GIT-BRANCHES.md`** and nothing else. That is "the tracker + docs + git log" in the only form
   that can be committed here.

5. **`examples/toy-project/README.md` states plainly that `.git` was not imported**, so a reader
   never mistakes the absence of a `.git` directory for the run not having used git.

## Alternatives considered

- **Make `examples/toy-project/` a git submodule.** Preserves history perfectly and fails the
  actual requirement: a reader cloning this repository gets an empty directory unless they
  initialise the submodule, and the acceptance checklist wants the paper trail *committed here*.
- **Run the pipeline directly in this repository, on a branch.** Rejected: the toy project's
  commits and this build's commits would share a history, `git log --grep WI-0001` would return
  results from both, and the item-history property being demonstrated would be the first
  casualty.
- **Rename `.git` to `dot-git` and commit it.** Technically possible, unreadable in practice,
  and it invites someone to restore it into a repository whose remotes and config are wrong.
- **Bundle the repository** (`git bundle`) and commit the binary. Preserves everything, but a
  binary blob is not a paper trail: the point of C6 is that a reader — human or agent — can read
  the history. Text wins.

## Consequences

- The example is auditable by reading, which is what it is for.
- The example cannot be `git checkout`-ed to an intermediate state. Accepted: the tracker's
  `history.md` and `journal.md` already record the sequence, and they are the artifacts under
  test.
- Import is a scripted step (`examples/toy-project/import.sh`), so it can be re-run if the toy
  project is re-executed after a skill fix — which the iterate-and-deepen loop expects to
  happen.
