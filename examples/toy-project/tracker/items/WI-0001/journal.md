# Journal — WI-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-16T21:15:23Z — intake v0.1.0 — product-analyst

- **Item:** WI-0001
- **Trigger:** invoked directly; created by the same `intake` execution that opened EP-001
- **Inputs read:** the human's answers in session (recorded verbatim in
  `tracker/items/EP-001/journal.md`); `tracker/project.yaml`; `tracker/items/` (empty)
- **Decisions:**
  - This item carries the whole tool the human described — listing, sorting, the total, and the
    behaviour on subdirectories, empty files, unreadable folders and non-text files — because
    none of those parts is independently useful to him. Unsorted output is what `wc -l *`
    already gives him, and he named "a stack trace instead of a number" as a failure condition,
    so an item without the awkward-case behaviour would ship something he has already rejected.
  - AC8 states only the observable guarantee (a complete listing, exit 0, no traceback), not how
    it is achieved. The human delegated the mechanism ("you decide, I don't really care"), and
    an invented mechanism recorded as a requirement would be indistinguishable from one he
    asked for.
  - `--top N` is excluded from this item at the human's explicit instruction; it is WI-0002.
- **Questions raised:** none filed as artifacts — the human was present and answered directly.
  Five open points are recorded in this item's `## Notes` for `refine`: the sort tie-break, the
  treatment of non-text files, the exact output shape, an empty folder, and the exit code for
  the unreadable-path case.
- **Commands:** `python3 .claude/agile-skills/scripts/new-item --id WI-0001 --type work-item
  --epic EP-001 --title "Count lines per file in a folder and print them largest first"
  --priority high --status draft --actor intake --reason "created from idea intake for EP-001"`
  → exit 0
- **Gates:** all four are recorded once, on EP-001's journal entry for this execution, since one
  `intake` execution created the epic and both items. `workspace-valid` → **pass**;
  `epic-has-success-measures` → **pass**; `items-are-separable` → **pass** (this item depends on
  nothing and is built first); `no-solution-in-the-problem` → **pass with a note** (the strings
  `python3 linecount.py <folder>` and the stdlib constraint are the human's own words from his
  answers to Q7 and Q8, not design added here).
- **Artifacts:** `tracker/items/WI-0001/item.md`, `journal.md`, `history.md` (all new)
- **Status:** `—` → `draft`
- **Result:** Created at `draft` with nine acceptance criteria drawn from the human's answers,
  and five open points left honestly open for `refine` rather than filled in.

## 2026-08-16T21:24:10Z — refine v0.1.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`; invoked directly by the human ("do Step 3 for both draft items,
  starting with WI-0001"), not dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0001/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — did not exist before this execution
  - `tracker/items/EP-001/journal.md` — the human's eight intake answers, verbatim; read first
    so that nothing already answered was re-asked
  - `tracker/items/EP-001/item.md` (success measures), `tracker/items/WI-0002/item.md` (sibling
    scope: `--top N` and the total-line question that belongs to it, not here)
  - `docs/product/vision.md` (v1), `tracker/project.yaml`
  - `.claude/agile-skills/spec/dor-dod.md`, `work-item.md`, `journal-and-history.md`
- **Decisions:**
  - **Nine criteria became thirteen.** Every rewrite is below with what changed about its
    meaning:
    - *AC1* — was "each row showing a line count and the file's name", which two implementations
      could satisfy with different output. Now fixes column order, right-alignment to the width
      of the widest number printed, a two-space separator, the bare filename, and a worked
      three-line example. The format mirrors `wc -l` on the human's authority ("that's what my
      eye already expects"), which also matters because `wc -l *` is the tool being replaced.
    - *AC2* — gained the tie-break (filename ascending, byte order) it never had, and gained the
      human's real requirement, which was not the rule but the stability behind it: two runs on
      an unchanged folder must `diff` clean.
    - *AC3* — the total row is now specified to appear **only when at least one file is listed**.
      The human redefined it himself when rejecting `0  total` for an empty folder.
    - *AC4* — unchanged in substance; "no content at all" tightened to "zero bytes", and it now
      says the row keeps its sorted position rather than being appended somewhere.
    - *AC5* — was "a final line with text but no trailing newline is included". Now states the
      whole counting rule (newline bytes, plus one if the file is non-empty and its last byte is
      not a newline) with three worked examples. Promoted from an edge case to the general rule
      because, after the answer to Q3, it governs every file including non-text ones.
    - *AC6* — unchanged in substance; "no error is printed about it" split into stdout **and**
      stderr, so it is checkable on both streams.
    - *AC7, AC8* — new. Symlinks and dotfiles were unstated ways for "one row per file directly
      in the folder" to mean two different things. Proposed by me, confirmed by the human.
    - *AC9* — was "a file that is not text" with an undefined subject and an ambiguous
      "complete listing": if such a file were skipped, was the listing still complete? Now the
      mechanism is settled (same byte rule as every file, one row each), so "complete" has a
      count, and `Traceback` absence is stated for both streams.
    - *AC10* — new. A folder with no files was listed as undiscussed at intake and had no
      criterion at all.
    - *AC11* — gained the stream (stderr), the empty stdout, and the exit code (2). "Non-zero"
      alone could not be checked by a command.
    - *AC12* — new, and the one thing here the human has not seen. See the assumption below.
    - *AC13* — was AC9, "a test framework that ships with Python 3, requiring no installation",
      a property with no observation attached. Now names the command and the exit code, at the
      human's own request that "the tests run" be shown rather than told.
  - **Assumptions recorded, and why each is safe.**
    - *Symlinks (AC7) and dotfiles (AC8)* — proposed by me, confirmed verbatim ("Yes to both as
      you proposed"). Safe because both follow from a rule he did state — subdirectories are
      ignored silently, and he asked for no ignore patterns — rather than adding a new one.
    - *AC12 (a path that is a regular file; no argument at all)* — **not put to the human at
      all**, and flagged as such in `## Notes` and in the Q&A. Safe to assume because it cannot
      produce a wrong count, only a wrong message on an invocation that is already wrong; it
      matches `argparse`'s default exit code of 2; and reversing it later is a one-line change.
      Holding the item at `draft` for a second round on it would have cost more than that.
    - *The `wc -l`-style format itself* is the human's confirmed choice, not an assumption.
  - **Deliberately left open for `plan`:** the exact wording of the stderr messages in AC11 and
    AC12. The criteria constrain the stream, the exit code, and that the message names the path
    and the problem. Fixing the exact string here would be inventing a requirement, and would
    make `verify` fail an implementation that is correct in every way the human cares about.
  - **Scope excluded, and on whose authority.** Two entries added to `## Out of scope`: detecting
    or reporting that a file is not text (the human's authority — he chose the no-special-case
    option in Q3), and counting through a symlink that points at a directory or reporting broken
    symlinks (his authority too — "ignore it exactly like a real subdirectory", "don't error").
  - **Nothing was moved between items.** WI-0002's open question about what the total means when
    the output is limited stays on WI-0002; it is not answerable here because there is nothing
    to limit yet.
  - **No conflict with the vision or the epic.** Checked each of EP-001's six success measures
    against the rewritten criteria: measures 1–2 → AC1/AC2/AC6, 3 → AC1/AC2, 4 → AC9, 5 → AC11,
    6 → AC13. AC10's `no files` output is new since the vision was written and does not
    contradict it, so no update to `docs/product/vision.md` was needed and none was made.
- **Questions raised:** six, all asked in one batch, all answered; recorded verbatim in
  `tracker/items/WI-0001/artifacts/refinement-qa.md`. None left `[unresolved]`. No question
  artifact was filed — the human was present and answered directly. One item in that file was
  never put to him (AC12) and is marked as the analyst's own extension there and in `## Notes`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 1 warning
    (`project.commands.test-null`, a `plan` responsibility, not a DoR criterion)
  - `python3 .claude/agile-skills/scripts/run-gate --skill refine --item WI-0001 --all` → exit 0
    (run before and after the rewrite; `workspace-valid` PASS, the other three reported MANUAL)
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0, "board already current; not
    rewriting the timestamp" (no status had changed yet at that point; re-run after the
    transition)
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to ready --actor refine --reason
    "Definition of Ready passed criterion by criterion; 6 questions answered, 13 criteria now
    decidable"` → exit 0
- **Gates:**
  - `workspace-valid` (hard) → **pass** — `validate-workspace` exits 0 (1 warning, unrelated to
    this item: `commands.test` is null and belongs to `plan`).
  - `definition-of-ready` (hard) → **pass**, criterion by criterion per `spec/dor-dod.md` §1:
    - *R1* **pass** — frontmatter complete; `type: work-item`, `epic: EP-001`, `priority: high`;
      `validate-workspace` [auto] exits 0.
    - *R2* **pass** — `## Story` names the role ("someone who has just opened a folder of mixed
      notes and code"), the capability ("one command that lists each file … biggest first") and
      the outcome ("so that I can see which two or three files hold most of the material without
      opening any of them"). Unchanged by this execution; it was already sound.
    - *R3* **pass** — AC1–AC13, each a labelled checkbox [auto].
    - *R4* **fail on entry → pass after rewrite.** Six of the nine original criteria were not
      decidable: AC1 (row format unfixed, and "a file directly in the folder" silent on dotfiles
      and symlinks), AC2 (no tie-break), AC3 (total's label and format unfixed), AC7 (stream and
      exit code unfixed), AC8 ("a file that is not text" undefined and "complete listing"
      ambiguous while the mechanism was delegated), AC9 (a property with no command attached).
      A boundary case was also missing entirely: a folder with no files. All six were rewritten
      from the human's answers; AC10 and AC12 were added. No criterion now contains an
      unmeasurable adjective — checked by scanning the rewritten list for "appropriate",
      "reasonable", "clean", "properly", "sensible", "graceful": none occurs.
    - *R5* **pass** — `## Out of scope` has seven entries, including `--top N` and recursion,
      which a reader would most plausibly assume are in.
    - *R6* **pass** — no open question on this item [auto]; `validate-workspace` exits 0.
    - *R7* **pass** — no `depends-on`; WI-0002 depends on this item, not the reverse, so it is
      independently deliverable and is sequenced first [auto].
    - *R8* **fail on entry → pass** — `artifacts/refinement-qa.md` did not exist; it now holds
      the whole exchange with every answer tagged.
    - *R9* **pass** — one `linecount.py` plus its tests, one coherent change. Reassessed after
      the rewrite, because thirteen criteria could suggest a split: they are thirteen properties
      of one command's output, not thirteen deliverables, and intake's reasoning (unsorted
      output is what `wc -l *` already gives him; a listing without the awkward-case behaviour
      is a failure he has already named) still holds unchanged.
  - `criteria-are-decidable` (hard) → **pass** — the command or observation that settles each,
    with the verdict that follows. Fixtures below are ordinary folders a verifier can build:
    - *AC1* — build a folder with `notes.md` (128 lines) and `a.py` (7); run
      `python3 linecount.py <folder>`; compare stdout to the three lines quoted in AC1. Any
      difference in column width, separator, or name form → fail.
    - *AC2* — a folder with `A.md` and `a.md` at the same count plus one larger file; the order
      must be larger-first then `A.md` then `a.md`. Then `cmd > a; cmd > b; diff a b` → must be
      empty, exit 0.
    - *AC3* — take AC1's output; the last line must be the sum, same column, two spaces,
      `total`. On AC10's fixture, no such line may appear.
    - *AC4* — `: > empty.txt` in the fixture; a row `0  empty.txt` must appear in sorted
      position.
    - *AC5* — three files written with `printf 'a\nb\n'`, `printf 'a\nb'`, `printf '\n'`;
      expected counts 2, 2, 1.
    - *AC6* — `mkdir sub` inside the fixture; `sub` must not appear in stdout, stderr must be
      empty, exit 0.
    - *AC7* — `ln -s notes.md link.md`, `ln -s sub dirlink`, `ln -s nowhere broken`; expect a row
      named `link.md` with `notes.md`'s count, no row for `dirlink` or `broken`, empty stderr,
      exit 0.
    - *AC8* — add `.gitignore`; a row for it must appear.
    - *AC9* — copy any PNG in; row count must equal the number of files plus the total row,
      stderr empty, exit 0, and `grep -c Traceback` on both streams → 0.
    - *AC10* — an empty folder, and a folder containing only `sub/`; stdout exactly `no files`,
      stderr empty, exit 0.
    - *AC11* — `python3 linecount.py /nonexistent` → empty stdout, one stderr line naming the
      path, `echo $?` → 2. Then `mkdir noread && chmod 000 noread` as a non-root user → same
      shape.
    - *AC12* — `python3 linecount.py README.md` and `python3 linecount.py` → empty stdout, a
      stderr message, `echo $?` → 2 in both cases.
    - *AC13* — `python3 -m unittest discover` from the repository root, on a machine with only
      Python 3 → exit 0, no installation step performed.
  - `qa-recorded-verbatim` (hard) → **pass** — `artifacts/refinement-qa.md` holds all six
    questions as asked and all six answers as given, in order. Q3's answer keeps its hesitation
    ("You decide, honestly. If you're making me pick: the first one") rather than being tidied
    into a decision, and the file explains why it is tagged as the human's answer even so.
    Q5's answer is tagged `[assumed]` because I proposed both behaviours and he confirmed them.
    The unasked AC12 is recorded in its own section as not put to him. Every human tag reads
    `[human — simulated by the builder]`, because this run is a methodology test and the record
    must not claim a real person said these things.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0001/item.md` (rewritten: criteria, out-of-scope, notes; `updated` bumped)
  - `tracker/items/WI-0001/journal.md` (this entry), `history.md` (one row)
  - `tracker/board.md` (regenerated)
  - commit on `main` covering `tracker/` and `docs/`, referencing WI-0001
- **Status:** `draft` → `ready`
- **Result:** WI-0001 is Ready with thirteen criteria, each settled by a named command or
  observation. All five open points intake left are closed on the human's word; two behaviours
  (symlinks, dotfiles) are recorded as assumptions he confirmed, and one criterion (AC12) is
  recorded as the analyst's own extension that he has not seen.

## 2026-08-16T21:36:40Z — plan v0.1.1 — architect

- **Item:** WI-0001
- **Trigger:** status `ready`, dispatched by `next` (highest-ranked runnable item; WI-0002
  rejected because its `depends-on: WI-0001` is not `done`)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (13 criteria, `## Out of scope`, `## Notes`)
  - `tracker/items/WI-0001/history.md`
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` (Q1–Q6; the `[assumed]` tags on Q5 and on
    the unasked AC12)
  - `tracker/items/WI-0002/item.md` — read for its criteria only, to know what this design must
    not foreclose; it is not planned here
  - `tracker/items/EP-001/item.md` (scope and out-of-scope)
  - `docs/product/vision.md` (v1)
  - `tracker/project.yaml`
  - `docs/architecture/overview.md` — did not exist; this execution created it
  - `docs/architecture/adr/` — empty; ADR-0001, ADR-0002 and ADR-0003 are the first three
  - the project's source code: there is none. `README.md` is one line, and no `.py` file exists
- **Decisions:**
  - **argparse, not hand-rolled parsing** (ADR-0001). Rationale: AC11, AC12 and WI-0002's AC7
    and AC8 all pin the failure shape to "nothing on stdout, a message on stderr, exit 2", which
    is argparse's default behaviour; hand-rolling it would mean writing and testing that shape
    ourselves for no criterion's benefit. Branch: **decided here**, with option B costed in the
    ADR.
  - **A file that cannot be read is skipped, named on stderr, and the run still exits 0**
    (ADR-0002). Rationale: no criterion rules on it, but the code must do something, and the two
    silent options make the total quietly wrong while the fatal option destroys the answer for
    every other file in the folder. Branch: **decided here** — the documents are genuinely
    silent, and the decision is reversible in one `except` branch, so it did not go to the human.
  - **`commands.test: python3 -m unittest discover`; `commands.lint` and `commands.build` stay
    null** (ADR-0003). Rationale: AC13 fixes the test command; no linter ships with CPython and
    `ruff`, `flake8`, `pyflakes` and `pylint` are all absent here, while EP-001 and the vision
    forbid depending on an installed tool. A stand-in such as `compileall` would report a green
    `lint-clean` for a check the test command already subsumes, which is exactly the dishonest
    pass the gate exists to prevent. Branch: **documented** (the constraint) plus **decided
    here** (which of the three options follows from it).
  - **`count_lines` and `format_report` hold no I/O and no argv** (`docs/architecture/overview.md`
    v1). Rationale: AC5 (the newline rule) and AC1 (the column width) are arithmetic, and keeping
    them out of `main` is what lets a test assert them without building a directory.
  - **Symlink handling is one call, `entry.is_file(follow_symlinks=True)`.** Rationale: it gives
    AC6 and all three cases of AC7 from a single predicate, so there is no second place where
    "what counts as a file here" could drift. Branch: **documented** — the behaviour is AC7's;
    only the mechanism is chosen here.
  - **The sort key is `(-count, os.fsencode(name))`.** Rationale: AC2 says byte order, and plain
    string comparison is code-point order, which differs for non-ASCII names. Branch:
    **documented** (AC2), mechanism chosen here.
  - **Four recorded assumptions** rather than four questions: `tests/` as a package, the 1 MiB
    read chunk, the stderr wording, and `no files` when every file in a folder fails to read.
    Each is one file or one line to reverse, and each is written under `## Assumptions` in
    plan.md with its reversal cost. Branch: **assumed**.
  - **Nothing in this plan anticipates `--top`.** Rationale: `format_report` computes the total
    from the rows it is given; WI-0002 needs a total over *all* files and a different label, and
    will change that signature under its own criteria. Designing for it now would ship an
    interface no criterion here tests.
- **Questions raised:** none. Nothing required the human: every open point was answered from the
  documents or recorded as a reversible assumption, and the one genuinely undecided case (an
  unreadable file inside a readable folder) is reversible in a single branch, so ADR-0002 took it
  rather than escalating.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
    (the `commands.test-null` warning present before this execution is gone)
  - `python3 -c "importlib.util.find_spec(...)"` for `ruff`, `flake8`, `pyflakes`, `pylint` →
    all four absent; evidence for ADR-0003
  - `python3 -V` → Python 3.12.3
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` (hard) → **pass** — `validate-workspace` exit 0, 0 errors, 0 warnings
  - `every-criterion-is-addressed` (hard) → **pass** — the `## Acceptance criteria mapping` table
    in `artifacts/plan.md` has one row per criterion AC1–AC13, each naming the plan step that
    satisfies it and the named test or command that demonstrates it. Two plan items map to no
    AC and are declared as such immediately below the table (the `.gitignore`, and ADR-0002's
    branch), rather than being left for a reader to notice
  - `project-commands-resolved` (hard) → **pass** — `commands.test` is `python3 -m unittest
    discover`, the command AC13 names; `commands.lint` and `commands.build` are null with
    ADR-0003 recording why, so `lint-clean` will be reported as skipped rather than passed. The
    test command is not yet runnable (there are no tests until `implement` writes them), which is
    the expected state at `planned`
  - `decisions-recorded` (hard) → **pass** — every choice this plan makes is in the `## Decisions
    and ADRs` table of plan.md, each pointing at ADR-0001, ADR-0002, ADR-0003, an existing
    document, or an entry under `## Assumptions` with its reversal cost
  - `plan-is-executable-without-you` (advisory) → **pass** — step 2 names each function, its
    signature, its behaviour and its observable result; step 3 names the test files and the
    tests. The judgement left to `implement` is how to write the tests' fixtures, not what the
    program should do
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/plan.md` (new)
  - `docs/architecture/overview.md` (new, v1)
  - `docs/architecture/adr/ADR-0001-argparse-for-the-command-line.md` (new, v1)
  - `docs/architecture/adr/ADR-0002-a-file-that-cannot-be-read.md` (new, v1)
  - `docs/architecture/adr/ADR-0003-no-lint-command.md` (new, v1)
  - `tracker/project.yaml` (`commands.test` filled in; the null lint/build now carry ADR-0003 as
    their reason)
  - `tracker/items/WI-0001/journal.md` (this entry), `history.md` (one row)
  - `tracker/board.md` (regenerated)
  - commit on `main` covering `tracker/` and `docs/`, referencing WI-0001
- **Status:** `ready` → `planned`
- **Result:** WI-0001 has a plan of four steps, an architecture overview, and three ADRs. Every
  one of the thirteen criteria maps to a step and to a named test; the two design questions the
  criteria do not answer — how the command line is parsed, and what happens to a file that
  cannot be read — are decided and recorded rather than left for `implement` to guess. No
  question was put to the human.

## 2026-08-16T21:41:30Z — implement v0.1.0 — developer

- **Item:** WI-0001
- **Trigger:** status `planned`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (AC1–AC13, `## Out of scope`, `## Notes`)
  - `tracker/items/WI-0001/artifacts/plan.md` (steps 1–4, the AC mapping, `## Assumptions`)
  - `tracker/items/WI-0001/history.md` — no send-back; this is a first implementation
  - `tracker/items/WI-0001/questions/` — empty
  - `docs/architecture/overview.md` (v1), `docs/architecture/adr/ADR-0001`, `ADR-0002`, `ADR-0003`
  - `tracker/project.yaml` (`commands.test`, `conventions.branch-prefix`, `commit-subject`)
  - the branch: `wi/WI-0001` did not exist at the start; `git log main..wi/WI-0001` was empty.
    The repository held no Python file, so there was no existing code to reconcile with
- **Decisions:** (all inside the plan's latitude — no interface, ADR or criterion was re-decided)
  - **Committed the first slice before moving the item to `in-progress`, rather than after.**
    `scripts/transition` runs every `implement` hard gate on every transition, and `tests-pass`
    (`NO TESTS RAN`, exit 5) and `commits-reference-the-item` (`no commits on
    main..wi/WI-0001`) cannot pass on an empty branch, so the transition the procedure asks for
    first was refused. Rationale for not using `--force`: it stamps `[gates forced]` on the
    history row permanently, which would tell every later reader that this item's gates were
    overridden when in fact they all pass. The refused attempt had already written
    `branch: wi/WI-0001` into `item.md`, so a run resuming inside that one-commit window would
    have found the branch instead of starting again. Recorded as deviation 1 in the
    implementation report.
  - **One test file, three classes** (`CountLinesTest`, `FormatReportTest`, `EndToEndTest`)
    rather than one file per layer. Rationale: 27 tests over one 117-line module; splitting them
    would spread the AC-to-test map across files without making any criterion easier to find.
  - **`SCRIPT` is derived from `__file__`, not from the working directory.** Rationale: AC13
    runs the suite from the repository root, but a test that only passes from one directory is a
    trap for the next person, and the criterion is about the tool, not about `cwd`.
  - **The PNG for AC9 is generated in-test with `zlib` and `struct`** rather than committed as a
    binary fixture. Rationale: it keeps the repository text-only and the fixture verifiable by
    reading it; the criterion asks for a PNG, not for a file on disk that happens to be one.
  - **Four extra tests** beyond the ones the plan names (`test_ac1_name_is_bare_not_a_path`,
    `test_ac1_column_is_as_wide_as_the_widest_number_printed`,
    `test_ac5_trailing_byte_after_a_chunk_boundary`, `test_ac9_bytes_are_never_decoded`).
    Rationale: each pins a clause of a criterion that the plan's single test asserted only
    incidentally — the bare name, the total setting the column width, the chunk-boundary case
    with a trailing partial line, and that no decoding happens. No new behaviour came with them.
  - **Decided *not* to decide:** nothing. No case arose that the plan and the ADRs did not
    already settle, so no question was filed. The one case the criteria do not cover — an
    unreadable file inside a readable folder — was already decided by ADR-0002 at planning time,
    and is implemented and tested exactly as that ADR states.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0001` → exit 0
  - `scripts/transition WI-0001 --to in-progress --actor implement --branch wi/WI-0001` (first
    attempt, before any code) → **exit 1, refused**: `tests-pass` FAIL (`python3 -m unittest
    discover` exited 5, `NO TESTS RAN`), `commits-reference-the-item` FAIL (`no commits on
    main..wi/WI-0001; nothing was delivered`). No status change was made
  - `python3 -m unittest discover` (after the first slice) → exit 0, 8 tests
  - `git commit` → `5adc619 linecount: count lines per file and print them largest first (refs
    WI-0001)`
  - `scripts/transition WI-0001 --to in-progress --actor implement --branch wi/WI-0001` (second
    attempt) → exit 1 **after applying the transition**: all hard gates passed, but
    `validate-workspace` then reported `journal.execution.missing` — `implement` was in
    `history.md` with no journal entry yet. That is this entry, and it is written before the next
    transition, which is the order `spec/journal-and-history.md` §2 implies (one entry per
    execution, appended when the execution finishes)
  - `python3 -m unittest discover -v` (branch head) → exit 0, `Ran 27 tests in 0.765s`, `OK`;
    the two root-guarded tests ran rather than skipping
  - `git commit` → `86f4384 tests: end-to-end coverage of every acceptance criterion (refs
    WI-0001)`
  - `python3 linecount.py /tmp/demo` (128-line `notes.md`, 7-line `a.py`, a subdirectory) →
    `128  notes.md` / `  7  a.py` / `135  total`, exit 0; `python3 linecount.py /tmp/demo | head -1`
    → `128  notes.md`; `python3 linecount.py /nope/nope` → `linecount: /nope/nope: No such file or
    directory` on stderr, exit 2
- **Gates:** (evidence in full in `artifacts/impl-report.md` `## Gates`)
  - `tests-pass` (hard) → **pass** — `python3 -m unittest discover`, exit 0, 27 tests, on branch
    head `86f4384`
  - `lint-clean` (hard) → **skipped** — `{{commands.lint}}` is null in `tracker/project.yaml`; the
    gate runner reported `SKIP` with "there is nothing to run; this gate checked nothing".
    ADR-0003 records why the project has no linter. Not a pass
  - `workspace-valid` (hard) → **pass** — `scripts/validate-workspace` exit 0, 0 errors, 0
    warnings (re-run after this entry was written)
  - `every-criterion-has-a-test` (hard) → **pass** — `impl-report.md` maps AC1–AC13 to named test
    functions with the exact bytes or exit codes they assert; no criterion is evidenced by
    reading the code
  - `commits-reference-the-item` (hard) → **pass** — `scripts/check-commit-refs WI-0001
    wi/WI-0001` exit 0; both commits carry the ID
  - `no-unplanned-scope` (advisory) → **pass** — the branch adds `.gitignore`, `linecount.py`,
    `tests/__init__.py`, `tests/test_linecount.py` and modifies nothing else. Every function is
    one plan step 2 names; there is no flag, option or code path no criterion or ADR asks for
- **Artifacts:**
  - `linecount.py` (new), `tests/__init__.py` (new), `tests/test_linecount.py` (new),
    `.gitignore` (new)
  - `tracker/items/WI-0001/artifacts/impl-report.md` (new)
  - branch `wi/WI-0001`, commits `5adc619..86f4384` (2 commits), plus this execution's tracker
    commit
  - `tracker/items/WI-0001/journal.md` (this entry), `history.md` (two rows: `planned →
    in-progress`, `in-progress → verifying`)
- **Status:** `planned` → `in-progress` → `verifying`
- **Result:** `linecount.py` and 27 tests are on `wi/WI-0001`; every criterion has a named test
  that asserts exact bytes, an exit code, or both, and the whole suite passes from the repository
  root with nothing installed. One deviation of consequence — the `in-progress` transition came
  one commit later than the procedure asks, because the gate runner refuses that transition on an
  empty branch and forcing it would have misreported the gates.

## 2026-08-16T21:45:10Z — verify v0.1.1 — qa-engineer

- **Item:** WI-0001
- **Trigger:** status `verifying`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — read **first**, before the implementation report, so that
    what would settle each criterion was derived from the criterion
  - `tracker/items/WI-0001/history.md`, `artifacts/plan.md`, `artifacts/refinement-qa.md`
  - `tracker/items/WI-0001/artifacts/impl-report.md` — read after the criteria, and treated as
    claims to check rather than as evidence
  - `docs/architecture/adr/ADR-0001`, `ADR-0002`, `ADR-0003`; `tracker/project.yaml`
  - the code on `wi/WI-0001` at commit `7d86345d6395330a40424832798e6d6362c0a3a7` (last code
    commit `86f4384`): `linecount.py`, `tests/test_linecount.py`, `.gitignore`, and
    `git diff --stat main..wi/WI-0001`
- **Decisions:**
  - **Built every fixture fresh under `/tmp/verify-wi0001-XgZc/` and drove the tool from the
    shell**, rather than reading the suite's fixtures. Rationale: the suite is the developer's
    account of the criteria; running the criterion's own commands is the only thing that
    distinguishes "the tests pass" from "the tool does what was asked".
  - **Used a real system PNG for AC9** (`/usr/share/pixmaps/hplj1020_icon.png`, confirmed with
    `file`) instead of the `png_bytes()` helper the tests use. Rationale: if the helper produced
    something that was not really a PNG, the test and the verification would share the mistake.
  - **Verified AC13 in a fresh `git clone` of the branch**, not in the working tree. Rationale:
    the criterion is about a machine with only Python 3 and no installation step; the working
    tree also contains `.claude/`, which a clone of the repository does not, so only the clone
    actually tests the claim.
  - **AC12's second case passes with a two-line stderr.** argparse prints a usage line above its
    message. Judged `pass`, not `ambiguous`: AC12 requires "prints a message on stderr" and fixes
    the stream and the exit code, and unlike AC11 it does not say "one line". Recorded in the
    report so the reading is visible rather than implied.
  - **Classification: nothing to route.** No criterion failed, so there is no send-back; no
    behaviour delivered by another item was touched — this is the first code in the repository —
    so there is no bug item. The one thing the mutation testing surfaced (AC6's test would not
    notice a regression affecting entries that are neither files nor directories) is not a defect
    against any criterion, and is recorded as an observation instead of filed.
  - **Nothing judged `ambiguous`**, so no question was filed.
- **Questions raised:** none
- **Commands:** (all run from the repository root or against fixtures under `/tmp/verify-wi0001-XgZc/`)
  - `git rev-parse HEAD` → `7d86345d6395330a40424832798e6d6362c0a3a7`; `git status --porcelain` →
    only the untracked `.claude/` and `CONSUMER-PROMPT.md`, no modified tracked file
  - `python3 -m unittest discover` → exit 0, `Ran 27 tests in 0.653s`, `OK`
  - AC1: `python3 linecount.py $F | cat -A` → `128  notes.md$` / `  7  a.py$` / `135  total$`, exit 0
  - AC2: same, on a four-file folder → ` 9  big.md$` / ` 3  A.md$` / ` 3  Z.md$` / ` 3  a.md$` /
    `18  total$`; then `python3 linecount.py $F > a.out; python3 linecount.py $F > b.out;
    diff a.out b.out` → no output, exit 0
  - AC3: `python3 linecount.py $F | tail -1 | cat -A` → `18  total$`
  - AC4: `python3 linecount.py $F | cat -A` → `5  full.txt$` / `0  empty.txt$` / `5  total$`, exit 0
  - AC5: a folder holding `a\nb\n`, `a\nb`, `\n` and an empty file → `2`, `2`, `1`, `0`, total `5`
  - AC6: → stdout `4  a.txt` / `4  total`, stderr 0 bytes, exit 0 (the 99-line file in `sub/` is
    absent from the total)
  - AC7: → ` 6  link.txt` / ` 6  target.txt` / ` 2  plain.txt` / `14  total`, stderr 0 bytes, exit 0
  - AC8: → `5  a.txt` / `2  .gitignore` / `7  total`, exit 0
  - AC9: `cp /usr/share/pixmaps/hplj1020_icon.png $F/image.png; file $F/image.png` → `PNG image
    data, 45 x 45`; `python3 linecount.py $F` → `13  image.png` / ` 5  a.txt` / ` 3  b.txt` /
    `21  total`, 4 lines, stderr 0 bytes, exit 0; `grep -c Traceback` on both streams → `0`
  - AC10: empty folder and a folder of two subdirectories → stdout exactly `no files`, stderr 0
    bytes, exit 0, both
  - AC11: `python3 linecount.py $W/does-not-exist` → stdout 0 bytes, stderr 1 line `linecount:
    …/does-not-exist: No such file or directory`, exit 2; `chmod 000 noread` then
    `python3 linecount.py …/noread` as `id -u` = 1000 → stdout 0 bytes, stderr 1 line `linecount:
    …/noread: Permission denied`, exit 2
  - AC12: `python3 linecount.py README.md` → stdout 0 bytes, stderr `linecount: …/README.md: Not a
    directory`, exit 2; `python3 linecount.py` → stdout 0 bytes, stderr `usage: linecount [-h]
    folder` + `linecount: error: the following arguments are required: folder`, exit 2
  - AC13: `git clone -q --branch wi/WI-0001 . /tmp/…/clone && cd /tmp/…/clone &&
    python3 -m unittest discover` → exit 0, `Ran 27 tests in 0.626s`, `OK`, in a tree with no
    `.claude/` and no install step; `grep` of the imports → stdlib only
  - ADR-0002: a `chmod 000` file beside a readable one → stdout `5  a.txt` / `5  total`, stderr
    `linecount: secret.txt: Permission denied`, exit 0
  - EP-001 pipe measure: 200-file folder, `python3 linecount.py $F | head -3` → the three largest,
    first command exit 0, no `BrokenPipeError`
  - sensitivity: `python3 /tmp/verify-wi0001-XgZc/sensitivity.py` (13 mutations) → exit 0,
    "mutations that the suite did not catch: 0"; plus a fourteenth mutation run by hand (`if True:`
    in `list_files`) → 4 tests failed. `git checkout -- linecount.py` after each; `git status`
    clean afterwards
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
- **Gates:**
  - `tests-pass` (hard) → **pass** — run here on the branch head, exit 0, 27 tests; and again in
    the fresh clone, exit 0
  - `lint-clean` (hard) → **skipped** — `{{commands.lint}}` is null (ADR-0003); the gate checked
    nothing and is not recorded as a pass. What it leaves unchecked is in `## Not verified, and
    why`
  - `workspace-valid` (hard) → **pass** — `validate-workspace` exit 0, 0 errors, 0 warnings
  - `every-criterion-independently-checked` (hard) → **pass** — thirteen rows in
    `verify-report.md`, each a command run here with its actual output quoted; none cites the
    implementation report
  - `negative-cases-exercised` (hard) → **pass** — nine failure and boundary conditions triggered
    on a real filesystem, plus ADR-0002's case and the `head` pipe
  - `tests-would-fail-without-the-change` (advisory) → **pass** — 14 mutations, 14 caught, listed
    with the tests that broke
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/verify-report.md` (new), carrying
    `Verified-commit: 7d86345d6395330a40424832798e6d6362c0a3a7`
  - `tracker/items/WI-0001/item.md` — all thirteen criteria ticked, each against evidence in the
    report; none was ticked without a command run here
  - no bug items filed
  - `tracker/items/WI-0001/journal.md` (this entry), `history.md` (one row)
- **Status:** `verifying` → `in-review`
- **Result:** All thirteen criteria pass on `7d86345`, decided by commands run here against
  fixtures built here — including a real system PNG and a fresh clone, both chosen so the check
  did not share the implementation's assumptions. Fourteen mutations of the delivered behaviour
  were all caught by the suite. Nothing was sent back and no bug was filed; the honest gaps are
  lint (there is none), non-UTF-8 filenames, and scale beyond a couple of hundred files.

## 2026-08-16T21:52:00Z — review-close v0.1.1 — reviewer

- **Item:** WI-0001
- **Trigger:** status `in-review`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0001/item.md`, `history.md` (six rows, checked against `pipeline.yaml`),
    `journal.md` (all five entries, in full)
  - `artifacts/plan.md`, `artifacts/impl-report.md`, `artifacts/verify-report.md`,
    `artifacts/refinement-qa.md`; `questions/` (empty)
  - `docs/architecture/overview.md` (v1), `ADR-0001`, `ADR-0002`, `ADR-0003`;
    `docs/product/vision.md` (v1)
  - the diff `main..wi/WI-0001` for `.gitignore`, `linecount.py`, `tests/` — read hunk by hunk,
    not the reports about it — plus `git log --format="%h %s" main..wi/WI-0001` and
    `git diff --name-only 7d86345..wi/WI-0001`
- **Decisions:**
  - **Accepted the change on substance.** Every hunk maps to a criterion or a plan step (the table
    is in `review.md` `## What I examined`); nothing contradicts an ADR; nothing anticipates
    WI-0002. Definition of Done D1–D8 and D11 pass with the evidence recorded per criterion.
  - **D10 passes on substance and fails as a gate, and I did not close over the difference.** The
    only commit after the verified sha is `4635eb9`, `verify`'s own tracker-only record;
    `git diff --name-only 7d86345..wi/WI-0001` lists nothing outside `tracker/`. So the
    verification does apply to the code that would be merged — but `check-verify-freshness`
    compares the recorded sha with the branch head and exits 1, and it is a **hard** gate.
  - **Did not merge.** D9 is recorded as not met. Merging is part of the accept action whose
    close is refused; putting the code on `main` for an item that cannot be closed would also
    pre-empt whichever resolution is chosen for D10.
  - **Did not send the item back.** A rejection would ask `implement` to fix something it did not
    do wrong. `in-review → verifying` is not a transition `pipeline.yaml` offers at all, so the
    gate's declared `on_failure: verifying` has no legal route from here; and re-verifying would
    not converge, since each `verify` execution must commit a record that moves the branch head
    past the sha it just recorded.
  - **Did not force the transition.** `--force` stamps `[gates forced]` on the history row
    permanently. Overriding a hard gate is not the reviewer's decision to take alone, and this
    item's gates are otherwise clean — a forced row would misdescribe it to every later reader.
  - **Could not file a question either.** A blocking question requires moving the item to
    `awaiting-answer`, and `scripts/transition` runs this skill's gates on that transition too.
    Verified by dry run: `--to awaiting-answer --actor review-close --resume-to in-review
    --dry-run` → the same single failure, `verification-postdates-the-code`. All four exits from
    `in-review` are therefore closed, and the item stays where it is. That is the impasse this
    entry records.
  - **Filed no bug item.** The defect is in the methodology's own gate tooling, not in this
    project's product; a `bug` under EP-001 would describe something the linecount tracker does
    not own. `review.md` `## Verdict` names the three resolutions and who each belongs to.
  - **Findings recorded rather than sent back:** the inert `from __future__ import annotations`,
    the `*.pyc` superset in `.gitignore`, and the intermediate list in `format_report`'s width
    calculation. None changes behaviour or touches a criterion; the first is the first concrete
    cost of having no linter (ADR-0003), which is why it is written down.
- **Questions raised:** none — not because none was needed, but because filing one requires a
  transition this skill's own gates refuse (see `## Decisions`). The question this execution would
  have filed is stated in `review.md` `## Verdict`: which of the three resolutions to D10's gate
  failure the project should take.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0001 wi/WI-0001` → **exit 1**,
    "was verified at 7d86345… but wi/WI-0001 is now at 4635eb9a"
  - `git diff --name-only 7d86345d6395330a40424832798e6d6362c0a3a7..wi/WI-0001` → `tracker/board.md`,
    `tracker/items/WI-0001/artifacts/verify-report.md`, `history.md`, `item.md`, `journal.md` —
    nothing outside `tracker/`
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, "all 4
    commit(s) on main..wi/WI-0001 name WI-0001"
  - `python3 -m unittest discover` → exit 0, 27 tests
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `grep -c "^- \[x\] AC" item.md` → 13; `grep -c "^- \[ \]" item.md` → 0
  - `git log --format="%h %s" main..wi/WI-0001` → 4 commits
  - `python3 … transition WI-0001 --to awaiting-answer --actor review-close --resume-to in-review
    --reason "…" --dry-run` → exit 1, refused, single failure `verification-postdates-the-code`;
    nothing written (history unchanged, tree clean)
- **Gates:**
  - `definition-of-done` (hard) → **fail** — D1–D8 and D11 pass with per-criterion evidence in
    `review.md`; **D9 not met** (not merged, because the close is refused) and **D10 fails as a
    gate** while passing on the facts. The per-criterion table is in `review.md`
    `## Definition of Done`
  - `verification-postdates-the-code` (hard) → **fail** — `check-verify-freshness` exit 1; the
    only intervening commit is `verify`'s own tracker record, and no code file differs
  - `commits-reference-the-item` (hard) → **pass** — `check-commit-refs` exit 0, 4 of 4 commits
  - `tests-pass-on-the-merge-result` (hard) → **pass on the branch, not on a merge result** —
    `python3 -m unittest discover` exits 0 at the branch head, but no merge has been performed, so
    what the gate command actually measured is the branch. Recorded as it is rather than as a pass
    for something that did not happen
  - `workspace-valid` (hard) → **pass** — `validate-workspace` exit 0, 0 errors, 0 warnings
  - `record-is-reconstructible` (hard) → **pass** — from `tracker/`, `docs/` and `git log` alone a
    reader can answer all four questions: *what was built and why* (`item.md`, `plan.md`,
    `docs/product/vision.md`, the four commits); *which skill decided what* (five journal entries,
    each with `**Decisions:**` and its persona; `history.md`'s `actor` column); *what questions
    arose and how they were resolved* (six at refinement, verbatim in `refinement-qa.md`; none
    filed as artifacts afterwards; the two the criteria left open are ADR-0001 and ADR-0002); and
    *what verification found* (`verify-report.md`: thirteen criteria with quoted output, 14
    mutations, five declared gaps). This entry is what keeps that true for this execution
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/review.md` (new) — what was examined, the full DoD table, the
    findings, the accepted gaps, and the verdict
  - `tracker/items/WI-0001/journal.md` (this entry)
  - no merge commit, no epic closure, no history row: the item did not transition
- **Status:** `in-review` → `in-review` (unchanged; no legal transition passes this skill's gates)
- **Result:** The change is accepted on substance — thirteen criteria met and independently
  demonstrated, a complete and reconstructible record, a diff with no unrequested scope. It could
  not be closed: `verification-postdates-the-code` reads `verify`'s own mandatory tracker commit
  as "the code changed after verification", and because that gate runs on every transition out of
  `in-review`, the item can be neither closed, rejected, suspended nor blocked without an
  authorised `--force`. The pipeline stops here, at `in-review`, awaiting a decision that is the
  human's to make.

## 2026-08-17T00:00:40Z — review-close v0.1.1 — reviewer

- **Item:** WI-0001
- **Trigger:** status `in-review`, dispatched by `next` — a **second** execution of this skill on
  this item. The first (entry above, 2026-08-16T21:52:00Z) reached the same verdict on substance
  and could not act on it, because `verification-postdates-the-code` compared shas and read
  `verify`'s own tracker commit as a code change, and because `scripts/transition` refused *every*
  transition whose actor had a failing hard gate. Both were fixed in the methodology's tooling
  between the two executions. That first entry stands as written: the refusal was real when it
  was recorded.
- **Inputs read:**
  - `tracker/items/WI-0001/artifacts/review.md` — my own first-execution record, re-checked
    against the branch rather than re-derived: the examination, the diff-to-criteria table, the
    findings and the accepted gaps are unchanged and still true, because nothing on the branch
    changed between the executions (`git diff --name-only d41a046..wi/WI-0001` → empty)
  - `tracker/items/WI-0001/item.md`, `history.md`, `journal.md` (including my first entry),
    `artifacts/plan.md`, `impl-report.md`, `verify-report.md`; `questions/` (still empty)
  - `.claude/agile-skills/scripts/check-verify-freshness` and `check-commit-refs` — read to
    establish what the repaired gates now assert, rather than assuming the fix did what was
    announced
  - `tracker/project.yaml`, `pipeline.yaml` (the legal transitions out of `in-review`)
- **Decisions:**
  - **Did not re-review the change.** The branch is byte-identical to the state the first
    execution examined, so re-reading the diff would have produced the same table and disguised
    which execution actually did the work. What I re-ran instead were the **gates**, which are the
    only things whose result could have changed.
  - **Updated `review.md` rather than writing a second review file.** A skill re-run overwrites its
    own artifact (`spec/workspace-layout.md` §1.2); the history of attempts belongs in this
    journal. Two rows changed — D9 (now merged) and D10 (now a passing gate) — plus the verdict.
    The D10 row keeps the first execution's finding in it, so the record does not quietly become
    "it always passed".
  - **Proved the merge result before touching the trunk.** `main` was at `f09a938`, which is also
    `git merge-base main wi/WI-0001`, so the merge could only be a fast-forward — but rather than
    argue that, I merged into a throwaway branch off `main`, confirmed `git diff --stat
    wi/WI-0001 HEAD` was empty, ran the suite there (27 tests, exit 0), and deleted the branch.
    That makes `tests-pass-on-the-merge-result` evidence about a merge result rather than about
    the branch, which is the honest reading of that gate and the thing my first execution had to
    record as unmeasured.
  - **Closed first, merged second.** `check-commit-refs` counts commits on `main..wi/WI-0001` and
    fails an empty range as "nothing was delivered", so merging before the transition would have
    made that gate fail for a change that had just been delivered correctly. The close therefore
    runs while the range is still populated, and the fast-forward follows immediately — with the
    merge result already proved, so nothing rests on the order.
  - **Carried the five accepted gaps into `item.md`'s `## Notes`.** They were listed in
    `review.md`, and nobody re-reads the reports of a closed item. No acceptance criterion was
    touched — the addition is a `## Notes` paragraph.
  - **Left `EP-001` open.** `WI-0002` is still `ready`, so epic DE1 fails and the epic Definition
    of Done is not applied yet. No epic journal entry, because no execution acted on the epic.
  - **No `--force`, at any point, in either execution.** Every gate that passed, passed on its own
    terms.
- **Questions raised:** none. The question the first execution would have filed — which of three
  resolutions to take for the freshness gate — was answered by the tooling fix, so there is
  nothing left to ask.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0001 wi/WI-0001` → **exit 0**:
    "WI-0001 verified at 7d86345d; wi/WI-0001 has moved to d41a046b but only the record changed
    (6 file(s) under tracker/ or docs/), so the verification still covers the code"
  - `git branch tmp/merge-check main; git checkout tmp/merge-check; git merge --no-ff wi/WI-0001`
    → merge commit `6263990`; `git diff --stat wi/WI-0001 HEAD` → empty (tree-identical);
    `python3 -m unittest discover` → exit 0, `Ran 27 tests in 0.644s`, `OK`;
    `git checkout wi/WI-0001; git branch -D tmp/merge-check`
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 … transition WI-0001 --to done --actor review-close --outcome delivered` → applied,
    with every hard gate passing
  - `git checkout main && git merge --ff-only wi/WI-0001` → fast-forward;
    `python3 -m unittest discover` on `main` → exit 0, 27 tests; `python3 linecount.py <folder>`
    on `main` → the expected report, exit 0
- **Gates:**
  - `definition-of-done` (hard) → **pass** — D1–D11 each with its own result and evidence in
    `review.md` `## Definition of Done`. D9 and D10, the two the first execution could not pass,
    are now evidenced by the merge and by the repaired freshness gate respectively
  - `verification-postdates-the-code` (hard) → **pass** — exit 0, quoted above; the gate now
    compares changed paths, and every path that moved after the verified sha is under `tracker/`
  - `commits-reference-the-item` (hard) → **pass** — all 5 commits on `main..wi/WI-0001` name
    WI-0001 (4 at the first execution, plus that execution's own record commit)
  - `tests-pass-on-the-merge-result` (hard) → **pass** — and this time on a real merge result:
    27 tests, exit 0, on `tmp/merge-check` before the trunk moved, and again on `main` after the
    fast-forward
  - `workspace-valid` (hard) → **pass** — `validate-workspace` exit 0, 0 errors, 0 warnings
  - `record-is-reconstructible` (hard) → **pass** — the four questions are answerable from
    `tracker/`, `docs/` and `git log` alone; this second entry is what keeps that true across the
    two executions, since a reader of the first entry alone would think the item is still stuck
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/review.md` (updated: D9, D10, the verdict, and the note that
    the accepted gaps now live in `item.md`)
  - `tracker/items/WI-0001/item.md` — `status: done`, `outcome: delivered`, and the five accepted
    gaps added to `## Notes`
  - `tracker/items/WI-0001/journal.md` (this entry), `history.md` (one row: `in-review → done`)
  - `main` fast-forwarded from `f09a938` to the branch head; `tracker/board.md` regenerated
  - no bug item, no epic closure, no ADR
- **Status:** `in-review` → `done` (outcome `delivered`)
- **Result:** WI-0001 is delivered and merged into `main`: `linecount.py` and 27 tests, thirteen
  criteria met and independently demonstrated, three ADRs, and a record that now covers both a
  refusal and its resolution. The two gate defects the first execution hit were fixed in the
  tooling, not worked around in this item, and nothing was forced. `EP-001` stays open behind
  `WI-0002`.

## 2026-08-17T01:30:00Z — verify v0.1.1 — qa-engineer

- **Item:** WI-0001
- **Trigger:** not a dispatched execution. The item is `done` and merged; this is an independent
  regression pass over the merged trunk, judging what is on `main` against this item's criteria.
  No status was changed and no history row was appended.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the thirteen criteria, read in full **before** any report,
    and the accepted gaps in `## Notes`
  - `tracker/items/WI-0002/item.md` — the eleven criteria of the item that changed this code last
  - `tracker/items/EP-001/item.md` — `## Goal`, `## Success measures`, `## Scope`
  - `docs/architecture/adr/ADR-0001` … `ADR-0005`, `docs/architecture/overview.md` v2,
    `docs/product/vision.md` v1
  - `tracker/project.yaml` — `commands.test`, `commands.lint`
  - the code on `main` at `6d1e437b4293571296809b322c47fb0dc83d1ad6`: `linecount.py` and
    `tests/test_linecount.py`; and `git show 5adc619:linecount.py`, the build this item shipped
  - `artifacts/impl-report.md`, `artifacts/verify-report.md`, `artifacts/review.md` and
    `artifacts/plan.md` — read **after** the criteria and after the fixtures were built, and used
    only to see which gaps had already been declared. None of them is cited as evidence for any
    verdict.
- **Decisions:**
  - **Built fixtures from the criteria, not from the tests.** Each criterion was turned into a
    folder on disk before `linecount.py` was read, so that what was checked is what was asked
    for rather than what was built. That is what turned up BUG-0001: AC7 names three symlink
    cases and the suite has one test each, so a loop and an unstattable target — both "resolves
    to nothing" — were never reached by anything derived from the tests.
  - **All three defects filed as bugs, not send-backs.** `verify`'s test is "does an acceptance
    criterion of *this* item say the behaviour should be different?" For BUG-0001 the answer is
    yes (AC7), which would normally be a send-back — but a send-back needs an item in flight, and
    both work items are `done` and merged. Each defect was additionally reproduced against
    `git show 5adc619:linecount.py`, the build this item shipped, so `found-in: WI-0001` is an
    observation rather than an inference, and none of them is WI-0002's.
  - **BUG-0001's two triggers kept in one item.** A symlink loop and a symlink into an
    unreadable directory are one uncaught `OSError` class from one call with two ways to reach
    it; they share a reproduction and will share a fix. Splitting them would create two items
    that cannot be closed independently.
  - **The `(all M files)` count was judged not a defect.** `--top` on a folder with a skipped
    file prints `total (all 1 files)` for two files. WI-0002 AC3 defines M twice in one sentence
    and the two halves disagree here; the implementation follows the operative gloss ("the number
    of rows the same command would print without `--top`"), so the record settles it and no
    question was filed. Recorded in `BUG-0002` `## Notes` instead.
  - **No bug filed for `BrokenPipeError`.** WI-0001 `## Notes` invited "an actual sighting". One
    exists at 5000 files, which the item's own stated envelope excludes ("never thousands"); at
    200, 250, 300 and 320 files — the last past the pipe buffer at 68 491 bytes — it did not
    reproduce. Filing a defect only reachable outside the stated size would be inventing one. The
    measured boundary is in the report instead.
  - **The report was written to `tracker/items/EP-001/artifacts/regression-verify-report.md`,
    not to this item's `verify-report.md`.** Overwriting a closed item's verification report
    would destroy the evidence `review-close` cited for D2 and D10, and this pass spans two items
    and an epic rather than one item.
  - **No checkbox was ticked or unticked.** Every criterion here was already ticked by the
    original verification, and this pass reproduced twelve of the thirteen independently; AC7 now
    has a demonstrated counter-example, but unticking a closed item's box would contradict D1 and
    is `answer-questions`' or `refine`'s call, not this pass's. The failure is carried by
    BUG-0001, which is the mechanism the record has for it.
- **Questions raised:** `EP-001/Q-001` (non-blocking, to architect) — filing a bug under a closed
  epic makes `validate-workspace` fail `epic.closed-with-open-children`, and `ids-and-statuses.md`
  §4 gives an epic no transition out of `done` while `journal-and-history.md` §1 forbids a row
  after one whose `to` is `done`. Three options set out; no recommendation, because the answer
  changes what "done" means for every epic in every project using this pipeline.
- **Commands:** (every command this pass ran that produced a verdict; full output in the report)
  - `git rev-parse HEAD` → `6d1e437b4293571296809b322c47fb0dc83d1ad6`; `git status --short` → no
    tracked file modified
  - `python3 -m unittest discover` (repo root) → exit 0, `Ran 46 tests in 1.155s`, `OK`
  - AC1: `python3 linecount.py /tmp/qa-lc/A | cat -A` → `128  notes.md$` / `  7  a.py$` /
    `135  total$`, exit 0
  - AC2: `python3 linecount.py /tmp/qa-lc7/tie` → `2  A.md` / `2  B.md` / `2  a.md` / `2  b.md` /
    `1  zz.md` / `9  total`; `cmd > a; cmd > b; diff a b` → exit 0, empty
  - AC4/AC5: `python3 linecount.py /tmp/qa-lc7/count` → `2  no_trailing.txt` / `2  two_nl.txt` /
    `1  just_nl.txt` / `1  one_noeol.txt` / `0  empty.txt` / `6  total`, exit 0
  - AC6/AC7/AC8: `python3 linecount.py /tmp/qa-lc7/mixed` → `3  link-to-file` / `3  real.txt` /
    `1  .gitignore` / `7  total`, stderr empty, exit 0
  - AC9: `python3 linecount.py /tmp/qa-lc7/bin` → `13  img.png` / ` 3  notes.txt` / `16  total`,
    exit 0; `grep -c Traceback` → 0 on stdout, 0 on stderr
  - AC10: `python3 linecount.py /tmp/qa-lc7/empty | cat -A` → `no files$`, stderr empty, exit 0;
    same for a folder of only subdirectories
  - AC11: `python3 linecount.py /tmp/qa-lc8/does-not-exist` → exit 2,
    `linecount: /tmp/qa-lc8/does-not-exist: No such file or directory`, stdout empty;
    `chmod 000` directory as uid 1000 → exit 2, `linecount: /tmp/qa-lc6/d000: Permission denied`
  - AC12: regular file → exit 2, `linecount: /tmp/qa-lc8/plainfile.txt: Not a directory`; no
    argument → exit 2, `usage: linecount [-h] [--top N] folder` + `linecount: error: the
    following arguments are required: folder`; stdout empty in both
  - **BUG-0001:** `python3 linecount.py /tmp/bug1a` (two-link loop) → exit 2,
    `linecount: /tmp/bug1a: Too many levels of symbolic links`, stdout empty;
    `/tmp/bug1d` (self-referential) → identical; `/tmp/bug1b/folder` (symlink into a `chmod 000`
    directory) → exit 2, `linecount: /tmp/bug1b/folder: Permission denied`; control
    `/tmp/bug1c` (plain broken symlink) → exit 0, `1  ok.txt` / `1  total`
  - **BUG-0002:** `python3 linecount.py /tmp/bug2a` (both files `chmod 000`) → exit 0, two
    `Permission denied` lines on stderr, `no files` on stdout; `2>/dev/null` → `no files` alone,
    byte-identical to the empty control folder; `/tmp/bug2b` (folder `chmod 444`) → same
  - **BUG-0003:** `python3 linecount.py /tmp/bug3` (folder holding `bad\xff.txt`) → exit 1,
    `UnicodeEncodeError: 'utf-8' codec can't encode character '\udcff' in position 6: surrogates
    not allowed` under a traceback, stdout empty; `wc -l *` on the same folder → exit 0, 3 rows
  - byte-identity of the WI-0001 build vs trunk: `git show 5adc619:linecount.py` run beside
    `linecount.py` on 8 folders and 2 error paths → `IDENTICAL` on all ten, including the three
    bug fixtures
  - 13 mutations of `linecount.py` in a scratch tree, `python3 -m unittest discover` after each →
    all 13 FAILED (failures 1 to 22); scratch tree discarded
  - `python3 linecount.py /tmp/qa-lc4/f5000 | head -1` → `BrokenPipeError: [Errno 32] Broken
    pipe`, first stage exit 1; the same at 200/250/300/320 files → exit 0, no error
  - `.claude/agile-skills/scripts/new-item` ×3 → exit 0, BUG-0001/0002/0003 created at `ready`
  - `.claude/agile-skills/scripts/board-gen` → exit 0
  - `.claude/agile-skills/scripts/validate-workspace` → exit 1, one error remaining
    (`epic.closed-with-open-children`); seven other errors this pass created were fixed
- **Gates:**
  - `tests-pass` (hard) → **pass** — `python3 -m unittest discover`, exit 0, 46 tests
  - `lint-clean` (hard) → **skipped** — `commands.lint` is `null` by ADR-0003; there is no command
    to run. Recorded as skipped, never as passed. What it leaves unchecked is in the report's
    `## Not verified, and why`
  - `workspace-valid` (hard) → **fail** — exit 1,
    `tracker/items/EP-001/item.md: ERROR [epic.closed-with-open-children] the epic is done but
    BUG-0001, BUG-0002, BUG-0003 are not`. Caused by filing the bugs, which this skill is
    required to do; no legal transition clears it. Filed as `EP-001/Q-001`
  - `every-criterion-independently-checked` (hard) → **pass** — all thirteen criteria of this
    item have a command and quoted output in the report, none citing `impl-report.md`
  - `negative-cases-exercised` (hard) → **pass** — every error, empty-input and boundary
    criterion triggered on disk; the list is in the report
  - `tests-would-fail-without-the-change` (advisory) → **pass** — 13 mutations, 13 suite failures
- **Artifacts:**
  - `tracker/items/EP-001/artifacts/regression-verify-report.md` (new)
  - `tracker/items/BUG-0001/`, `BUG-0002/`, `BUG-0003/` (new, at `ready`, `found-in: WI-0001`)
  - `tracker/items/EP-001/questions/Q-001.md` (new, open, non-blocking, to architect)
  - `tracker/board.md` regenerated; `journal.md` (this entry). No history row, no code change
- **Status:** `done` → `done` (unchanged — an independent regression pass changes no status)
- **Result:** Twelve of thirteen criteria reproduced independently on the merged trunk. AC7 has a
  demonstrated counter-example — a symlink that cannot be stat'ed aborts the whole listing and
  blames the folder — and two further defects sit in the seams between ADR-0002, ADR-0005 and
  AC10, and between `os.scandir`'s decoded names and the overview's "no file can raise a decoding
  error". Filed as BUG-0001, BUG-0002, BUG-0003. The tests that exist are sensitive; what they
  miss is the cases the criteria named but the fixtures never reached.
