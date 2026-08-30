# Workspace layout

The **workspace** is the tracker and documentation that the methodology creates *inside the
consumer's own project*. It sits alongside the project's source code, in the same git
repository, and is committed with it. That co-location is deliberate: a tracker in a different
system drifts from the code within a week, and `git log --grep WI-0007` only reconstructs an
item's history if the item and the code share a history.

---

## 1. The tree

```
<project root>/
├── tracker/
│   ├── project.yaml              # machine-readable project config (§3)
│   ├── board.md                  # GENERATED — never hand-edited (§4)
│   ├── requests/                 # the stakeholder writes here, unprompted (spec/request.md)
│   │   └── R-001.md
│   └── items/
│       ├── EP-001/
│       │   ├── item.md
│       │   ├── journal.md
│       │   ├── history.md
│       │   ├── questions/
│       │   └── artifacts/
│       ├── WI-0001/
│       │   ├── item.md
│       │   ├── journal.md
│       │   ├── history.md
│       │   ├── questions/
│       │   │   └── Q-001.md
│       │   └── artifacts/
│       │       ├── refinement-qa.md
│       │       ├── plan.md
│       │       ├── impl-report.md
│       │       ├── verify-report.md
│       │       └── review.md
│       └── BUG-0001/
│           └── … same shape …
├── docs/
│   ├── product/
│   │   ├── vision.md
│   │   └── prd.md
│   ├── architecture/
│   │   ├── overview.md
│   │   └── adr/
│   │       └── ADR-0001-<slug>.md
│   └── process/
│       └── ways-of-working.md
└── <the project's own source code>
```

### 1.1 What MUST exist

| Path | When |
|------|------|
| `tracker/project.yaml` | from workspace initialisation |
| `tracker/items/` | from workspace initialisation |
| `tracker/requests/` | from workspace initialisation; may be empty, and usually is |
| `tracker/board.md` | after the first item exists |
| `<item>/item.md`, `journal.md`, `history.md` | for every item directory, from creation |
| `<item>/questions/`, `<item>/artifacts/` | directories may be empty, but MUST exist |
| `docs/product/vision.md` | once an epic exists |
| `docs/architecture/overview.md` | once any item has reached `planned` |

An item directory missing `journal.md` or `history.md` is an error even if it has never been
worked on. The files are created with their headers at the moment the item is created, so
"empty" and "lost" are distinguishable.

### 1.2 Artifact names are fixed

| Artifact | Written by | Contains |
|----------|-----------|----------|
| `artifacts/refinement-qa.md` | `refine` | the full Q&A verbatim, each answer marked as `human` or `assumed`. MUST open with frontmatter carrying `status: agenda` or `status: recorded` — see §1.3 |
| `artifacts/plan.md` | `plan` | design, steps, assumptions, ADR references, gate commands |
| `artifacts/impl-report.md` | `implement` | what was built, AC → evidence map, deviations from the plan |
| `artifacts/verify-report.md` | `verify` | per-AC verdict with evidence, gates run, defects found. MUST contain a line `Verified-commit: <sha>` naming the commit that was verified — a verification that does not say what it verified cannot be shown to be current, and Definition of Done D10 turns on exactly that |
| `artifacts/review.md` | `review-close` | what was examined, DoD result per criterion, verdict |
| `artifacts/retro.md` | `retro` | on an **epic** only, after the engagement has ended: what the record shows about how the work went, and the toolkit findings it proposes upstream. Schema in [`retro.md`](retro.md) |

Fixed names, not free choice. A skill looking for the previous stage's output must find it
without searching, and a validator must be able to say "this item reached `verifying` but has
no `impl-report.md`" — which is a real failure mode, not a hypothetical one.

Re-running a skill **overwrites** its own artifact and appends a journal entry. It does not
create `plan-2.md`. The journal is where the history of attempts lives; the artifact always
holds the current answer.

### 1.3 `refinement-qa.md` says whether the conversation happened

```yaml
---
status: recorded
---
```

`status: agenda` means the questions are written down and the conversation has **not** happened
— which is the honest thing for `refine` to leave behind when it is interrupted before reaching
the human. `status: recorded` means the exchange in this file is what was actually said.

Definition of Ready **R8** is satisfied only by `recorded`, and `validate-workspace` reports
`artifact.refinement-qa.not-recorded` on an item that has reached `ready` without it.

The field exists because R8 was an `[auto]` check on a **filename**. A worker interrupted mid
refinement did the right thing — wrote the agenda down for the next session — and then noticed
that the file it had just created would read to an automated check as R8 satisfied, and
mitigated it with a banner nothing reads (F-031). A mechanical gate that checks the wrong thing
is worse than a manual one, because it is trusted: nobody re-reads a criterion marked `[auto]`.

---

## 2. Initialisation

`scripts/workspace-init <project-root>` creates the tree, writes `tracker/project.yaml` with
placeholders, and creates the `docs/` directories. It is idempotent: running it on an existing
workspace makes no changes and exits 0.

It MUST NOT create empty placeholder documents under `docs/`. An empty `vision.md` reads to a
later skill as "the vision is empty", not as "nobody has written it yet".

---

## 3. `tracker/project.yaml`

The machine-readable facts about the project that gates need and that no methodology file can
know in advance.

```yaml
project:
  name: wc-tool
  trunk-branch: main
  description: A command-line utility that summarises text files in a directory.

commands:
  test: python3 -m pytest -q
  lint: python3 -m ruff check .
  build: null

conventions:
  branch-prefix: wi/
  commit-subject: "<scope>: <summary> (refs <ITEM-ID>)"
```

| Field | Required | Rules |
|-------|----------|-------|
| `project.name` | yes | short slug |
| `project.trunk-branch` | yes | the branch items merge into |
| `project.description` | yes | one or two sentences |
| `commands.test` | yes, may be `null` | resolved into `{{commands.test}}` |
| `commands.lint` | yes, may be `null` | resolved into `{{commands.lint}}` |
| `commands.build` | yes, may be `null` | resolved into `{{commands.build}}` |
| `conventions.branch-prefix` | yes | default `wi/` |
| `conventions.commit-subject` | yes | MUST contain `<ITEM-ID>`; this is what makes D8 checkable |

A `null` command is honest — it means the project has none yet. It makes the corresponding gate
**skipped**, and `plan`'s exit criteria require either filling it in or recording an ADR that
says why the project has none. What is forbidden is a command that does not exist, or one that
exits 0 without doing anything: both report a passing gate for work nobody checked.

---

## 4. `tracker/board.md` is generated

`scripts/board-gen` regenerates it from item state. It carries a header saying so.

```markdown
<!-- GENERATED by board-gen. Do not edit; run scripts/board-gen. -->
# Board — generated 2026-08-16T11:47:52Z

## EP-001 — Summarise a directory of text files  (open)

| id | title | type | status | priority | blocked by |
|----|-------|------|--------|----------|------------|
| WI-0001 | Count lines per file | work-item | done | high | — |
| WI-0002 | Sort the summary | work-item | verifying | high | — |
| BUG-0001 | Empty directory crashes | bug | in-progress | critical | — |
| WI-0003 | Recurse into subdirectories | work-item | awaiting-answer | medium | Q-001 |

## Open questions

| item | question | to | blocking | created |
|------|----------|----|----------|---------|
| WI-0003 | Q-001 — should symlinked directories be followed? | human | yes | 2026-08-16T11:32:10Z |

## Summary

- 4 items: 1 done, 1 verifying, 1 in-progress, 1 awaiting-answer
- 1 open question, 1 addressed to the human
```

Rules:

- `board.md` is derived state. `validate-workspace` reports `board.stale` when regenerating it
  would produce different content, so a board that disagrees with the tracker is caught rather
  than believed. The comparison ignores the `# Board — generated <timestamp>` line and nothing
  else: every other byte must be a function of tracker state, which is why the questions table
  carries each question's `created` timestamp rather than its age.
- The **Open questions** section MUST come before the summary, and questions addressed to the
  human MUST be listed first. When the loop stops, this is the thing a returning human reads.

---

## 5. Relationship to the project's git history

- Item work happens on `<conventions.branch-prefix><ITEM-ID>`, e.g. `wi/WI-0007`.
- Every commit on that branch MUST match `conventions.commit-subject`, which MUST contain the
  item ID. `git log --grep WI-0007` therefore reconstructs the item's code history (R4.4), and
  `validate-workspace` can check it mechanically.
- Workspace changes (tracker and docs) are committed **with** the code change that caused them,
  not separately. A commit that changes only the tracker is legitimate for `intake`, `refine`
  and `answer-questions`, which produce no code.
- **`plan` produces no code, with one carve-out: scaffolding a declared gate command needs in
  order to execute at all.** `plan`'s own contract requires it to have *run* the commands it
  records, and a test command cannot run against a package that has no `__init__.py` — it errors
  rather than failing. So `plan` MAY create a file outside `tracker/` and `docs/` when all of:
  the command cannot execute without it; the file contains **no behaviour** (an empty package
  marker, an empty test module, the minimum a tool needs to recognise the project); it is listed
  in the plan under `## Scaffolding` with the command that needed it; and no acceptance criterion
  depends on it. A stub function with a `pass` body is **not** scaffolding — that is an interface
  decision, and it belongs in the plan where a reviewer can argue with it. See
  `meta/adr/ADR-0007` for why this beats letting `plan` record a command it never ran (F-034).
- **An epic-level record commit belongs on the trunk**, not on whichever item branch happens to
  be checked out. An epic is not a branch-scoped unit of work: it has no branch of its own, it
  outlives every item under it, and its record — `tracker/items/EP-###/` — is changed by
  executions that are not about any one child. A skill writing an epic's record while an item
  branch is checked out MUST commit it on the trunk (check out the trunk, commit, return),
  before or after the item's own commits but never inside them.

  This is a rule because breaking it fails a gate for an item that did nothing wrong: an
  epic-level commit sitting on `wi/WI-0003` names `EP-001`, and `check-commit-refs WI-0003`
  reports it as a commit on the item's branch that does not name the item. The worker that hit
  it had no way to know where the commit should have gone, because nothing said (F-016).
- `review-close` merges the branch into `{{trunk}}`. The workspace never depends on a remote
  existing: everything here works in a purely local repository.

---

## Revisions

| # | Date | Change |
|---|------|--------|
| 1 | 2026-08-17 | Initial. |
| 2 | 2026-08-22 | `tracker/requests/` added — the stakeholder-initiated channel (F-021, `spec/request.md`). |
| 3 | 2026-08-22 | §5: an epic-level record commit is made on the trunk, not on the item branch that happens to be checked out (F-016). |
| 4 | 2026-08-27 | §5: `plan` may create behaviour-free scaffolding a declared gate command needs in order to execute, listed under `## Scaffolding` (F-034, ADR-0007). §1.2/§1.3: `refinement-qa.md` declares `status: agenda` or `recorded`, and Definition of Ready R8 reads that field rather than the filename (F-031). |
