# Journal — WI-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-27T15:46:52Z — intake v0.2.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** invoked directly by the caller on the stakeholder's stated idea; no status, the item did not exist yet
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement
  - `tracker/project.yaml`
  - `tracker/items/` (empty — this is a new workspace, no existing items to overlap with)
- **Decisions:**
  - Created as the thin end-to-end slice: scan a folder, choose a destination per file, report the
    plan, carry it out. Rationale: a preview with nothing to preview delivers nothing, and moving
    files without a preview is the thing the stakeholder explicitly asked not to have — so the
    preview and the moving belong in one item, not two. See EP-001's entry for how the whole idea
    was split.
  - Acceptance criteria left deliberately rough, with a note saying so. Rationale: intake's own
    guidance is that an honestly rough criterion beats a polished unfalsifiable one, and AC1/AC5/AC6
    cannot be made decidable until EP-001/Q-001 (target environment) and EP-001/Q-003 (recursion)
    are answered. `refine` owns sharpening them.
  - Priority set to `medium`, the same as its siblings. Rationale: the stakeholder stated no
    ordering, and equal priorities record that fact rather than a guess. EP-001/Q-004 asks them for
    the ordering.
  - No technology named anywhere in the story, title or criteria — "the tool", not "the Python
    script". Rationale: the stakeholder named none, and choosing one here would be designing rather
    than analysing. EP-001/Q-001 asks them.
- **Questions raised:** none on this item; four on EP-001 (`EP-001/Q-001`–`Q-004`), all open and
  addressed to the human, two of which (Q-001, Q-003) bear directly on this item's criteria
- **Commands:**
  - `scripts/new-item --id WI-0001 --type work-item --epic EP-001 --priority medium --status draft --actor intake` → exit 0, created at `draft`
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, exit 0 — see EP-001's entry; this
    item's journal entry is one of the things that had to exist for it to pass)
  - `epic-has-success-measures` → **pass** (an epic-level gate; evidence recorded on EP-001)
  - `items-are-separable` (advisory) → **pass** — this item is buildable first and depends on
    nothing; WI-0002 and WI-0003 both declare `depends-on: WI-0001`
  - `no-solution-in-the-problem` (advisory) → **pass** — title and story name no language, no file
    format and no data structure; nothing had to be removed
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` (new)
  - `tracker/items/WI-0001/history.md`, `journal.md` (new, headers written by `scripts/new-item`)
- **Status:** `—` → `draft`
- **Result:** WI-0001 exists at `draft` as the first of three items under EP-001 — sort a folder's
  files by type, with a preview that changes nothing. Its criteria are rough by design and two of
  them wait on open questions to EP-001.

## 2026-08-27T16:01:32Z — refine v0.2.2 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, dispatched by `next` (step 5; the only runnable candidate — WI-0002
  and WI-0003 both `depends-on: WI-0001`, which is not `done`)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the draft, as amended by `answer-questions` earlier today
  - `tracker/items/WI-0001/history.md` — one row only, `— → draft` by `intake`. **This is a fresh
    draft, not a send-back**, so the whole item was in scope rather than a specific defect
  - `tracker/items/WI-0001/journal.md` — `intake` v0.2.1's entry, which records that the criteria
    were left rough on purpose and that no technology was to be named until EP-001/Q-001 landed
  - `tracker/items/WI-0001/artifacts/` — empty; no earlier `refinement-qa.md` to continue
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-004.md` — the stakeholder's four answers,
    verbatim; the source of every standing deferral relied on below
  - `tracker/items/EP-001/item.md` — success measures and out-of-scope list
  - `tracker/items/WI-0002/item.md`, `WI-0003/item.md` — checked for scope this item must not
    swallow: age routing and user-supplied rules respectively
  - `docs/product/vision.md` (v2) — the never-overwrite promise and "does not go looking inside
    subfolders"; nothing written here contradicts it
  - `docs/architecture/adr/ADR-0001-python-3-stdlib-cli.md` (v1) — Python 3, stdlib only, one CLI
    entry point
  - `.claude/agile-skills/spec/dor-dod.md` §1, `work-item.md`
- **Decisions:**
  - **No question was put to the stakeholder this round, and this was a routing decision under
    `refine` step 3, not an omission.** Two of their four answers are standing deferrals over a
    whole category — *"Whatever's easiest for you to build and test — you know this better than
    me"* (EP-001/Q-001) and *"whichever's easier for you"* (EP-001/Q-004) — and step 3's third
    bullet says a category deferral is a real answer that applies to the category. Every gap found
    was either inside that category (invocation, naming, output wording, exit codes, the default
    mapping) or had a conservative answer following directly from the safety emphasis they *did*
    state. Each was decided, tagged `[assumed]` in `refinement-qa.md` naming the deferral relied
    on, and carried into `## Notes` so `plan`, `implement` and `verify` inherit it as an
    assumption rather than as a stakeholder decision. The counterweight considered was F-023, a
    stakeholder who received four questions on one item and found three of them things a team
    should have decided; the risk accepted in return is that five assumptions are now load-bearing
    and unconfirmed, which is why they are listed in one block in `## Notes` rather than scattered.
  - **PREVIEW is the default; APPLY requires a flag** (AC1, AC2). The deferral covers the flag's
    *spelling*, not the direction, and the direction is not a coin flip: the stakeholder led their
    idea with the dry run and called never-overwrite the one thing they actually care about, so a
    tool whose bare invocation moves files would put the dangerous behaviour behind the shortest
    command. Choosing the safe side of a safety decision needs no confirmation.
  - **The default extension table was written out in full** (AC5), replacing "files are grouped by
    kind of file" — a criterion two implementations could both satisfy while disagreeing about
    every file. Seven folders, matched on the final extension case-insensitively, because EP-001
    forbids reading contents to classify. Decided rather than asked because it is the most
    reversible thing in the item: WI-0003 exists to hand the mapping to the user.
  - **Unrecognised files are left where they are and reported, not swept into a catch-all**
    (AC6), replacing AC5's old "has a stated, observable outcome", which was a criterion that
    could not fail. Rationale: the vision says the tool moves files and does nothing else, and
    moving a file the tool admits it does not understand is the move most likely to surprise; a
    user who wants them swept can add a rule in WI-0003, whereas recovering files from `other/` is
    manual work. The cost is accepted and written into `## Notes`: a folder of unrecognised
    extensions is reported and left untidied, so a correct run can move nothing.
  - **Hidden files are skipped entirely** (AC13), a case nothing in the item, the epic or the
    vision had addressed. Someone pointing this at their home directory and finding `.bashrc` in
    `code/` would reasonably call it broken; dotfiles are configuration rather than clutter.
  - **`## Notes` names two things as deliberately unconstrained rather than pretending they are
    decided**, per R10, with `refine` named as who left them so: the exact form of the collision
    suffix (the stakeholder left it open themselves — *"or whatever you want to call it"*), and
    what happens if a destination folder name is already taken by a *file* at the top level. The
    second was considered for a criterion and rejected: nothing else depends on it, and pinning it
    would be inventing a requirement rather than recording one.
  - **Three open design questions were routed to `plan` rather than to a person** — the command's
    name and the apply flag's spelling, the exact text of each kind of output line, and where the
    AC5 table is written down for a user to read. Each would have the same answer whoever the
    stakeholder was, which is step 3's test for an implementation-only choice. The criteria are
    written so a verifier can still decide them: AC1 requires `--help` to reveal the invocation, so
    `TOOL`, `PREVIEW` and `APPLY` resolve from the tool itself.
  - **Criteria were renumbered, and every live pointer at the old numbers was repointed.** The six
    criteria `intake` and `answer-questions` left became fifteen. `docs/product/vision.md` cited
    `WI-0001 AC7` for never-overwrite, which now means something else; it is v3 and cites AC9.
    `WI-0002` AC5 cited `WI-0001 AC3` for preview/real agreement; it now cites AC8. The
    `## Consequences` sections of `EP-001/Q-002` and `Q-003` now give both the number they filed
    and the current one. `EP-001/journal.md` still names the old numbers and was **not** edited —
    it is append-only and was true when written; this bullet is the correction that record points
    forward to.
  - **Nothing was left `[unresolved]`, and no Definition of Ready override was needed or taken.**
- **Questions raised:** none — six agenda items, all closed in
  `artifacts/refinement-qa.md` as `[assumed]` under a recorded standing deferral; no question file
  filed, nothing `[unresolved]`
- **Commands:**
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-08-27T15:58:15Z`, the clock reading this execution's
    artifacts are stamped with
  - `scripts/validate-workspace .` → run twice during the rewrite, exit 0 both times (one expected
    warning, `project.commands.test-null`, which is `plan`'s to clear)
  - `grep -rn "WI-0001 AC" docs/ tracker/` → located the three stale cross-references repaired above
  - `scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** — `scripts/validate-workspace`, run by `scripts/transition`
    against the state this move produces, exit 0.
  - `definition-of-ready` → **pass**, criterion by criterion:
    - **R1 pass** [auto] — `id`, `type: work-item`, `title`, `status`, `priority: high`,
      `epic: EP-001`, `created`, `updated` all present; validator reports no frontmatter error.
    - **R2 pass** [skill] — role *"someone with a folder full of unsorted files"*, capability
      *"be shown exactly where every file would be moved to and then have it done"*, outcome
      *"so that the folder gets organised … without me having to trust the tool before I have seen
      what it intends to do"*. Unchanged from `intake`; it was already complete.
    - **R3 pass** [auto] — fifteen criteria, `AC1`…`AC15`, each an unticked checkbox.
    - **R4 fail on entry → pass after rewrite.** Six criteria were failing. AC1 said "in preview
      mode" without saying how a user selects it; AC4 said kinds are "stated somewhere a user can
      read" without stating them; AC5 said an unrecognised file has "a stated, observable outcome"
      without stating one; AC6 said "an error a user can act on" with no exit status or stream
      named; AC7/AC8 (collisions) named no observation; AC10 asserted idempotence without saying
      what would be compared. All six were rewritten and are listed under `criteria-are-decidable`
      below. No criterion now contains an unmeasurable adjective: the words "appropriate",
      "reasonable", "clean", "properly" and "graceful" appear nowhere in the criteria.
    - **R5 pass** [skill] — six entries, including two a reader would reasonably assume are
      included: classifying by file *contents* rather than extension, and moving subfolders.
    - **R6 pass** [auto] — `tracker/items/WI-0001/questions/` is empty; no question, blocking or
      otherwise.
    - **R7 pass** [auto] — no `depends-on`. WI-0002 and WI-0003 depend on this item, not the
      reverse, so it is independently deliverable and is first in the recorded delivery order.
    - **R8 pass** [auto] — `artifacts/refinement-qa.md` exists and declares `status: recorded`.
      It is `recorded` rather than `agenda` because every item on the agenda is closed and none is
      pending a reply; its opening section states plainly that no question was put to the
      stakeholder this round and why, so the file does not imply a conversation that did not
      happen.
    - **R9 pass** [skill] — one coherent change: list a folder, choose a destination per file,
      print the plan, carry it out. No split needed. The two things that would have made it
      compound are already separate items — age routing is WI-0002, user rules WI-0003 — and both
      are on this item's out-of-scope list so the boundary is visible from here.
    - **R10 pass** [skill] — the behaviours this item introduces are two modes crossed with six
      classes of input. Every cell has a criterion: PREVIEW and APPLY × recognised (AC3, AC7),
      unrecognised (AC6), collision (AC10, AC9), hidden (AC13), nothing-to-do (AC15), bad target
      (AC14); plus subfolders under both modes (AC11), the second APPLY (AC12), and the agreement
      between the two modes (AC8). Two combinations are deliberately unconstrained and named as
      such in `## Notes` with `refine` recorded as who left them so.
  - `criteria-are-decidable` → **pass**. For each criterion, the observation that settles it:
    AC1 run `TOOL --help`, read stdout, check exit 0. AC2 run `TOOL <folder>` bare, then compare a
    recursive listing before and after. AC3 run PREVIEW over a fixture with one recognised file and
    count move lines against files. AC4 `find` listing with sizes and paths, diffed before against
    after. AC5 one fixture file per extension in the table, run PREVIEW, compare each destination
    against its row, including `PHOTO.JPG` for the case-insensitivity clause. AC6 a `.xyz` file and
    an extensionless file: read the output lines, then confirm the paths are unchanged after APPLY.
    AC7 compare the multiset of (basename, size) under the folder before and after APPLY. AC8
    capture PREVIEW's (file, destination) pairs, run APPLY, compare the resulting pairs. AC9 place
    two different `report.pdf` files, run APPLY, checksum the pre-existing one. AC10 the same
    fixture, read the PREVIEW line for the suffixed name. AC11 a pre-existing subfolder with a file
    in it: diff its recursive listing before against after, and grep the output for its contents.
    AC12 run APPLY twice, diff the listing after each, then run PREVIEW and count move lines.
    AC13 place `.bashrc` and `.hidden.jpg`, grep both modes' output for them, check the paths after
    APPLY. AC14 run against `/nonexistent` and against a regular file: check stderr contains the
    path, stdout is empty, exit status is 2, and nothing changed. AC15 run both modes over an empty
    folder and over one holding only a subfolder: one line, no move lines, exit 0.
  - `qa-recorded-verbatim` → **pass**. `artifacts/refinement-qa.md` quotes all four of the
    stakeholder's EP-001 answers verbatim, in their words, with the `[human]` tag and the question
    they came from. Every one of the six agenda items is recorded with why it was asked, the answer,
    and the `[assumed]` tag naming the deferral it rests on. Nothing is tagged `[human]` that a
    person did not say, and nothing is tagged `[assumed]` without the reasoning that produced it.
    No answer was paraphrased into agreement — there is no answer to paraphrase, because no
    question was put, and the file says so in its first sentence rather than implying otherwise.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` (new) — `status: recorded`; the routing
    rationale, the four verbatim stakeholder quotes, six agenda items with their answers
  - `tracker/items/WI-0001/item.md` — criteria rewritten from six rough to fifteen decidable;
    `## Out of scope` extended to six entries; `## Notes` rewritten with the five assumptions, the
    two deliberately unconstrained points, and the three questions routed to `plan`
  - `docs/product/vision.md` (v2 → v3) — never-overwrite citation repointed to `WI-0001 AC9`
  - `tracker/items/WI-0002/item.md` — AC5's cross-reference repointed to `WI-0001 AC8`
  - `tracker/items/EP-001/questions/Q-002.md`, `Q-003.md` — `## Consequences` now give both the
    criterion numbers filed and the current ones
  - `tracker/board.md` (regenerated)
- **Status:** `draft` → `ready`
- **Result:** WI-0001 is Ready. Fifteen criteria, each with a named observation that settles it,
  covering both modes against recognised, unrecognised, colliding, hidden, absent and invalid
  input. Five decisions were taken under the stakeholder's standing deferral rather than referred
  to them, and all five are listed in one block in `## Notes` so that whoever reads this item next
  inherits them as assumptions rather than discovering them. `plan` is next, with three named
  design questions waiting for it.

## 2026-08-27T16:07:58Z — plan v0.3.1 — architect

- **Item:** WI-0001
- **Trigger:** status `ready`, dispatched by `next` (step 5; the only runnable candidate, WI-0002
  and WI-0003 both depending on it)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the fifteen criteria, which are this design's contract, and
    the `## Notes` block listing `refine`'s five assumptions and the three design questions routed
    here
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — six agenda items, all `[assumed]`, none
    `[unresolved]`; the soft ground this design stands on
  - `tracker/items/WI-0001/history.md` — two rows, `— → draft → ready`. Not a re-plan; there is no
    review or verification record to read
  - `tracker/items/EP-001/item.md` and `questions/Q-001.md` … `Q-004.md` — the stakeholder's own
    words on collisions, recursion and the delegation
  - `docs/architecture/adr/ADR-0001-python-3-stdlib-cli.md` (v1) — the only ADR that predates this
    execution; Python 3.9+, one CLI entry point, standard library only
  - `docs/architecture/overview.md` — **did not exist**; this is the first planned item in the
    project, so creating it is part of this job
  - `docs/product/vision.md` (v3) — the preview as the product's central promise
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, `commands.build` all `null`
  - `tracker/items/WI-0002/item.md`, `WI-0003/item.md` — to know what this design must leave room
    for and must not build
  - **the project's source code: there is none.** `ls` at the root shows `tracker/`, `docs/`,
    `.claude/` and the harness files only. Nothing was read because nothing exists; this is a
    greenfield item, which is why an architecture overview had to be written before the plan
- **Decisions:**
  - **Separate planning from applying, and decide every destination in one place** (ADR-0002,
    new). Three of the fifteen criteria are about the *relationship* between the two modes — AC8
    (they agree), AC10 (a rename is visible before it happens), AC12 (the second apply is a no-op).
    The naive `dry_run` boolean satisfies each mode separately and makes their agreement a
    coincidence, which is precisely the shape that produces a preview that is right about simple
    moves and wrong about collisions. Preference-order branch: **decided**, because the record was
    silent and the choice shapes the module boundary that WI-0002 and WI-0003 will both extend.
    Two alternatives named and costed in the ADR, including previewing against a copy of the
    folder, which was rejected as unusable at any size.
  - **Move with `os.link` then `os.unlink`** (ADR-0003, new). The stakeholder's one hard constraint
    is that nothing is overwritten, and the obvious implementation makes that a check-then-act with
    a window, resting on every future call site remembering the check — while the underlying
    primitive, `os.rename`, silently replaces on POSIX. `os.link` fails with `FileExistsError` when
    the destination exists, so the kernel enforces the guarantee in one operation. Source and
    destination are always on the same filesystem here, because the tool never leaves the folder it
    was given. Branch: **decided**. The fallback for filesystems that refuse hard links is in the
    ADR, and its weakness is recorded as a risk rather than hidden.
  - **`commands.test` and `commands.lint` filled in, `commands.build` left `null`** (ADR-0004,
    new). `python3 -m unittest discover -s tests -t . -q` and `python3 -m compileall -q tidy tests`.
    Branch: **decided**, since ADR-0001 had already ruled out third-party packages, which rules out
    every style linter. Two things are recorded loudly rather than smoothed over: the lint command
    is a *syntax* check and a passing lint gate on this project must not be read as a style
    verdict; and the test command exits **5**, not 0, today, because there are no tests yet.
    Recording that honestly is the point — a project claiming a test command with no tests should
    not report success — and it becomes a passing gate the moment `implement` writes the first
    test. `build` stays `null` because a package run with `python3 -m` has no build step, and
    inventing one would make a gate report a pass for work nobody does.
  - **`python3 -m tidy <folder>`, with `--apply` for the real run.** A package rather than a loose
    script because `tests/` must import it and because `python3 -m tidy` is a real terminal command
    needing no install [src: ADR-0001]. Branch: **decided** — `refine` routed the spelling here
    explicitly, having settled the direction (preview by default) itself.
  - **stdout carries per-file lines only; the mode banner and every error go to stderr.** This was
    the one genuine ambiguity in the criteria: AC3 says stdout contains "exactly one line per file
    that would be moved", AC6 requires unrecognised files to be reported on a line too, and AC14
    requires stdout to be empty on a usage error. Splitting the streams and defining a move line as
    one whose first field is `move` makes all three literally checkable — AC3 by counting lines
    matching `^move `. This is a *reading* of the criteria, recorded as such in the plan; no
    criterion was amended, and `plan` has no authority to amend one.
  - **The collision suffix goes before the extension** — `report (2).pdf`, not `report.pdf (2)`.
    Branch: **assumed** (plan `## Assumptions` 1), with the reversal cost stated. The reasoning is
    not aesthetic: this tool classifies by extension, so `report.pdf (2)` has the extension
    `.pdf (2)` and the tool could not recognise its own output. The stakeholder explicitly left the
    form open — *"or whatever you want to call it"* [src: EP-001/Q-002].
  - **Four smaller assumptions, each recorded with what reversing it costs**: sorting the scan for
    stable output; treating a destination reserved earlier in the same plan as taken (which cannot
    fire today but closes a hole WI-0003 would open); `README.md` as the file AC5 requires; and
    exit 1 reserved for a partial apply failure, so a run in which three files moved and one did
    not does not exit 0.
  - **The second thing `refine` left deliberately unconstrained was left unconstrained.** A
    destination folder name already taken by a *file* at the top level is not decided here and is
    not in the mapping table. Deciding it would be inventing a requirement; it is named in the
    item's `## Notes` and is a candidate bug item if it ever matters.
  - **Nothing was asked of the human, and nothing needed to be.** Branch 3 of the preference order
    applies only to an irreversible decision or to intent no document records. Every decision above
    is one file's worth of change to reverse, and the three that carry product weight — never
    overwrite, top level only, delivery order — were answered by the stakeholder this morning and
    are cited rather than re-opened.
  - **Two things were deliberately not designed**, per the "designing past the item" check: no
    timestamp branch anywhere in `planner.py`, and no argument or file-loading path for rules. Both
    are the next two items, and the overview records where each will land so the next `plan`
    execution does not have to re-derive it.
- **Questions raised:** none
- **Commands:**
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-08-27T16:03:05Z`
  - `python3 -VV` → `Python 3.12.3`, which satisfies ADR-0001's 3.9 floor
  - `ls -la` at the repository root → no source code exists; `tracker/`, `docs/`, `.claude/` and
    harness files only
  - `python3 -m unittest discover -s tests -t . -q` → **exit 5**, `NO TESTS RAN` — run before
    recording it, and recorded in ADR-0004 with that exit code
  - `python3 -m compileall -q tidy tests` → exit 0
  - `.claude/agile-skills/scripts/lint-claims --all` → first run **9 errors**
    (`claim.unsourced` across the three new ADRs); citations added to all nine paragraphs; re-run
    exit 0, 0 errors
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 4 documents checked
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, **0 warnings** — the
    `project.commands.test-null` warning that had stood since `intake` is now cleared
  - `.claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** — `scripts/validate-workspace`, run by `scripts/transition`
    against the state this move produces, exit 0, and for the first time in this project with zero
    warnings as well as zero errors.
  - `every-criterion-is-addressed` → **pass** — `plan.md`'s `## Acceptance criteria mapping` has
    one row per criterion, AC1 through AC15, fifteen rows for fifteen criteria. Each row names the
    plan step that satisfies it and a *specific* named test with what it asserts — not "tests". The
    hardest three were written to be demonstrable rather than plausible: AC7 is a multiset of
    (basename, size) taken recursively before and after; AC8 parses the (file, destination) pairs
    out of the preview's own output and compares them with the apply's; AC9 checksums the
    pre-existing file. Checked in the other direction too: every step 1–6 appears in the table,
    step 7 is required by AC5's "a file in the repository a user can read", and step 8 is the
    column itself — so no step exists that no criterion needs.
  - `project-commands-resolved` → **pass**, with one thing stated plainly. `commands.test` and
    `commands.lint` are now real commands, both executed in this repository during this execution
    rather than expected to work. `commands.test` exits 5 today because no test exists yet, which
    is the honest result and not a vacuous pass — the gate's own failure condition is a command
    that "exits zero without checking anything", and this one does the opposite. `commands.build`
    remains `null` under ADR-0004, which is the escape the gate allows: an ADR recording why the
    project has none.
  - `decisions-recorded` → **pass** — `plan.md`'s `## Decisions and ADRs` table lists every choice
    this plan makes and points each at either an ADR (ADR-0001 read; ADR-0002, ADR-0003, ADR-0004
    written) or a numbered entry under `## Assumptions` that states what reversing it would cost.
    Five assumptions, five reversal costs, all of them one file. Nothing contradicts an existing
    ADR: ADR-0001 was the only one in the tree and no third-party package appears anywhere in this
    design.
  - `claims-are-sourced` → **pass** — `scripts/lint-claims --changed-since main`, exit 0. It failed
    first with nine `claim.unsourced` errors across the three new ADRs, each an absolute about a
    named code object; every one now carries a citation that resolves, and `--all` over the whole
    tree is also clean.
  - `plan-is-executable-without-you` (advisory) → **pass** — read back cold. Every step names the
    file it touches, the function it adds, and what is true afterwards; the interfaces block fixes
    the signatures so step 4 does not have to guess what step 2 returned; and the output contract
    fixes the three things `refine` left to this skill, so no step requires a decision the plan
    does not make. The check applied was the mechanical one: no step survives that no criterion
    maps to. What is deliberately *not* specified is how each function is written — the plan
    contains no implementation, and the only files created outside `tracker/` and `docs/` are two
    empty package markers.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/plan.md` (new) — problem, approach with the fixed interfaces
    and the output contract, eight steps, a fifteen-row criteria mapping, five assumptions, the
    decisions table, scaffolding, four risks, and what is out of scope
  - `docs/architecture/overview.md` (new, v1) — the three-layer shape, the module table, the two
    architectural commitments, and where WI-0002 and WI-0003 will touch it
  - `docs/architecture/adr/ADR-0002-separate-planning-from-applying.md` (new, v1)
  - `docs/architecture/adr/ADR-0003-move-with-os-link.md` (new, v1)
  - `docs/architecture/adr/ADR-0004-test-and-lint-commands.md` (new, v1)
  - `tracker/project.yaml` — `commands.test` and `commands.lint` set; `commands.build` left `null`
    under ADR-0004
  - `tidy/__init__.py`, `tests/__init__.py` (new, empty) — scaffolding, listed in `plan.md`
    `## Scaffolding`, created so the two declared gate commands can execute at all
  - `tracker/board.md` (regenerated)
- **Status:** `ready` → `planned`
- **Result:** WI-0001 is planned. Eight steps across four modules, a README and four test modules,
  with every one of the fifteen criteria mapped to a named test and what it asserts. Three ADRs
  record the decisions that carry weight: the plan/apply split that makes the preview trustworthy,
  `os.link` so the kernel rather than a code convention enforces never-overwrite, and the project's
  test and lint commands. The project now has an architecture overview, a real test command, and no
  outstanding validator warning. `implement` is next and needs nothing from anyone.

## 2026-08-27T16:09:55Z — implement v0.2.2 — developer

- **Item:** WI-0001
- **Trigger:** status `planned`; dispatched by `next` as the only runnable item (WI-0002 and WI-0003 both depend on it and it is not `done`).
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the fifteen acceptance criteria, the five inherited assumptions, and the three design questions `refine` routed to `plan`
  - `tracker/items/WI-0001/artifacts/plan.md` — eight steps across four modules, the interface contracts, the output contract, and the AC-to-test mapping table
  - `tracker/items/WI-0001/history.md` — three rows, ending `ready -> planned`; no send-back, so this is a fresh execution and not a resumption
  - `tracker/items/WI-0001/questions/` — empty; no question has ever been filed on this item
  - `docs/architecture/adr/ADR-0003-move-with-os-link.md` — the move primitive and its fallback, which step 4 executes rather than re-decides
  - `tracker/project.yaml` — branch prefix `wi/`, commit subject convention, `commands.test` and `commands.lint` (both non-null, so neither gate will be skipped)
- **Decisions:**
  - Treating this as a fresh start rather than a resumption: `git branch` showed only `main`, `wi/WI-0001` did not exist, and `tidy/` and `tests/` hold nothing but the two empty `__init__.py` markers `plan` created as scaffolding. Nothing on disk needs reconciling.
  - Branched from `main` at d46b852, the commit that carries the plan, so the branch's first parent is the state the plan was written against.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0001 main` → 0 (branch created)
- **Gates:**
  - `tests-pass` → **not yet run** — no code has been written; it runs on the branch head at step 7
  - `lint-clean` → **not yet run** — same
  - `workspace-valid` → **not yet run** as a completion gate; the transition accompanying this entry runs it
  - `every-criterion-has-a-test` → **not yet run** — no test exists yet
  - `commits-reference-the-item` → **not yet run** — the branch has no commits of its own yet
  - `claims-are-sourced` → **not yet run** — nothing has changed since `main`
- **Artifacts:**
  - branch `wi/WI-0001`, created at d46b852; no commit on it yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0001 has started on `wi/WI-0001`. The plan is executable as written — its preconditions all hold and nothing in it needs a decision that is not already recorded — so the next entry will be the closing report at step 9.

## 2026-08-27T16:13:02Z — implement v0.2.2 — developer

- **Item:** WI-0001
- **Trigger:** status `in-progress`; continuation of the execution opened at 2026-08-27T16:09:55Z, suspended at SKILL.md step 6 before any code was written.
- **Inputs read:**
  - `tracker/items/WI-0001/artifacts/plan.md` — step 5's CLI output rule, step 4's error handling, `## Assumptions` 1–5, `## Risks`
  - `tracker/items/WI-0001/item.md` — AC6, AC8, AC15, and the `## Notes` list of what `refine` deliberately left unconstrained and routed to `plan`
  - `.claude/agile-skills/spec/question.md` — §1 (this skill may never ask a human), §2 (file format, one decision per question, the one-ask framing), §3 rule 1 (a blocking question suspends the item)
  - `docs/architecture/adr/ADR-0002-separate-planning-from-applying.md` and `ADR-0003-move-with-os-link.md` — read to check whether either already settles the two gaps; neither does
- **Decisions:**
  - **Stop before writing code rather than after.** Both gaps land in `tidy/cli.py` and one of them may move a check into `tidy/planner.py`, which are two of the four modules the plan defines. Writing the other modules first would have produced a branch whose shape presumes an answer.
  - **Two questions, not one.** `spec/question.md` §2 forbids folding two decisions into one file. They share a round, so each `## Context` opens with the same frame and Q-002 says it is the last.
  - **Addressed to `architect`, not `human`.** Neither turns on stakeholder intent: Q-001 is a contradiction between two criteria the stakeholder never saw in this form, and Q-002 is a decision the item explicitly routed to `plan`, which did not take it. Both are reversible and neither contradicts an ADR, so none of `spec/question.md` §4's four escalation conditions applies. The loop therefore does not stop; `next` will dispatch `answer-questions`.
  - **Not escalated, decided as mine:** three further under-determined points, recorded here so `verify` is not the one to find them. (a) A symlink at the top level — `os.scandir` + `entry.is_dir()` is what plan step 2 names, so a symlink to a directory is omitted and a symlink to a file is treated as a file; that is the plan's own mechanism, not a new decision. (b) An unreadable target directory — no criterion covers it, AC14 covers only "missing" and "not a directory"; it will be listed under `## What I did not do` rather than guessed at. (c) The exact wording of the banner and the failure messages — plan step 5 fixes what they must contain, not how they read.
- **Questions raised:** Q-001 (blocking), Q-002 (blocking)
- **Commands:**
  - `grep -n "Nothing to do\|no \`move\` action" tracker/items/WI-0001/artifacts/plan.md` → 0 (three hits, confirming step 5's literal rule)
  - `grep -n "already taken\|taken by a\|a file literally called" tracker/items/WI-0001/artifacts/plan.md` → 1 (no match; the case the item routed to `plan` is absent from the plan)
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → 0
- **Gates:**
  - `tests-pass` → **not run** — no code was written this execution, so there is nothing for it to judge; it runs on the branch head before the move to `verifying`
  - `lint-clean` → **not run** — same reason
  - `workspace-valid` → **pass** — run by the transition accompanying this entry, resolving `WI-0001:in-progress->awaiting-answer`
  - `every-criterion-has-a-test` → **not run** — no test exists yet; AC6 and AC15 cannot be given tests until Q-001 settles which of them constrains the shared case
  - `commits-reference-the-item` → **fail, not blocking** — the branch carried no commits of its own when the gate ran, so `main..wi/WI-0001` was empty; the question artifacts are committed immediately after this entry, which fills that range
  - `claims-are-sourced` → **pass** — `lint-claims --changed-since main` exit 0
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-001.md` — created; the AC6/AC15 contradiction in plan step 5's output rule
  - `tracker/items/WI-0001/questions/Q-002.md` — created; the destination-folder-name-taken-by-a-file case the item routed to `plan` and `plan` did not decide
  - branch `wi/WI-0001` — no source file created; `tidy/` and `tests/` are unchanged from `main`
- **Status:** `in-progress` → `awaiting-answer`
- **Result:** Implementation stopped at plan step 5 without writing code. Plan step 5's rule "no `move` action → print only the single Nothing-to-do line" contradicts AC6 for a folder holding only unrecognised files, which is the fixture AC6 itself names; and the plan never decided the case `refine` explicitly routed to it, where an AC5 destination name is already taken by a top-level file, which today would end APPLY in an uncaught `FileExistsError` from `os.makedirs`. Both are user-visible and neither is this skill's to choose, so both are filed to the architect and the item is suspended at `awaiting-answer` with `resume-to: in-progress`.

## 2026-08-27T16:16:56Z — answer-questions v0.3.1 — architect

- **Item:** WI-0001
- **Trigger:** status `awaiting-answer`; dispatched by `next` step 4 as the item owning the oldest open architect-addressed question (Q-001, created 2026-08-27T16:11:38Z).
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-001.md` and `Q-002.md` — both open, both `addressed-to: architect`, both blocking, filed by `implement` before any code was written
  - `tracker/items/WI-0001/item.md` — AC3, AC6, AC8, AC15, and the `## Notes` list of what `refine` left deliberately unconstrained
  - `tracker/items/WI-0001/artifacts/plan.md` — step 2's ordering of tests, step 3's collision resolution, step 4's error handling, step 5's output rule, `## Assumptions` 1–5
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — Q3 (the origin of AC6) and Q5 (the origin of AC15), including the "why asked" and the rationale recorded for each
  - `tracker/items/WI-0001/history.md` — the suspending row of 2026-08-27T16:13:02Z, carrying `resume-to: in-progress`
  - `docs/architecture/adr/ADR-0002-separate-planning-from-applying.md` v1 — `## Decision` and `## Consequences`; the decision Q-002 has to fit inside
  - `docs/architecture/adr/ADR-0003-move-with-os-link.md` v1 — checked for whether it already covers the `os.makedirs` failure path; it does not, it covers `os.link` only
  - `docs/architecture/adr/ADR-0001-python-3-stdlib-cli.md` v1 and `ADR-0004-test-and-lint-commands.md` v1 — checked for conflict; neither bears on either question
  - `docs/product/vision.md` v3 — the "shows its work before it does it" promise, cited in Q-002's rejection of option C
  - `tracker/items/EP-001/questions/Q-001.md` — the standing deferral the item's assumptions rest on, checked for whether it reaches either question; it does not
- **Decisions:**
  - **Q-001 — answered from recorded intent (route 2), option A.** `refinement-qa.md` Q3 states AC6's reporting unconditionally — *"It is left exactly where it is, and both modes report it on a distinct line saying so"* — and Q5 states AC15's purpose as anti-silence — *"a line rather than silence because silence is indistinguishable from a crash"* — over a scope it names as *"the empty and no-op cases"*. So the two criteria never conflicted; **`plan` step 5 manufactured the conflict** by turning "print a line when there would otherwise be none" into "print only that line". Option A satisfies both intents and leaves all four of AC15's named fixtures emitting exactly one stdout line, because none of them produces a `leave` action either.
  - **AC15 amended, deliberately and on the record.** I am one of two skills permitted to change a criterion, so this is stated rather than buried: AC15 gained a clause scoping "a single line" to the four cases it enumerates and stating that AC6 governs the overlap. It adds no behaviour and changes no target — it records which of two criteria governs a fixture both could be read as claiming, from the refinement record, **before any code existed**. This is the opposite of reshaping a criterion around what was built; nothing has been built.
  - **Q-002 — answered from an existing document (route 1), option B.** ADR-0002 `## Decision` gives `planner.py` the job of describing "what would happen" for every entry and gives `apply.py` a layer that "computes nothing"; its `## Consequences` records that this is what makes AC8 structural. Option A would put a decision inside `apply.py` and make AC8 true only with an exception, so ADR-0002 selects option B. The filesystem read it needs is the same kind plan step 3 already sanctions — ADR-0002 forbids the planner *writing*, not reading.
  - **No ADR minted for Q-002.** It decides nothing ADR-0002 had not decided; it applies ADR-0002 to a case the plan overlooked. Recording it as an ADR would imply a new architectural commitment where there is none. It is recorded in `plan.md` `## Assumptions` 6 with its reversal cost, per `spec/question.md` §1's preference order.
  - **No acceptance criterion added for Q-002's case.** `refine` recorded that "pinning it now would be inventing a requirement", and nothing since has changed that. The behaviour is in the plan with a named test and stays out of the criteria; the item's `## Notes` now says so.
  - **No scope widened, so no item filed under step 3b.** Both answers land inside WI-0001; neither implies work no item records.
  - **A `plan` defect, recorded rather than swallowed.** `refine` routed the AC5-destination-name-taken decision to `plan` explicitly in the item's `## Notes`, and `plan` did not take it — `grep` over `plan.md` for the case returns nothing across `## Approach`, all eight steps, `## Assumptions` and `## Risks`. Nothing in the toolkit catches a plan that silently declines a decision an item routed to it: `plan`'s gates check that every AC has a mapped test, and this case has no AC by design, so it fell through the one check that would have seen it. Worth fixing in the `plan` skill.
- **Questions raised:** none — neither question was re-addressed to the human, because neither meets any of `spec/question.md` §4's four conditions: both are reversible, neither turns on intent no document records, neither contradicts an ADR, and the record was not silent on either.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → 0 (no document under `docs/` changed this execution)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 1 before the move, reporting exactly the two conditions this transition resolves — `board.stale` and `question.awaiting.none-open` on WI-0001
  - `grep -n -A6 "AC15 — Over a folder" tracker/items/WI-0001/item.md` → 0 (propagation check)
  - `grep -n "unconditionally, because AC6" tracker/items/WI-0001/artifacts/plan.md` → 0 (propagation check)
  - `grep -n "is not a folder" tracker/items/WI-0001/artifacts/plan.md` → 0 (propagation check)
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → 0
- **Gates:**
  - `answer-is-propagated` → **pass** — every file named in a `## Consequences` section was opened and the change confirmed present: `item.md` AC15 at line 89 carries the new clause and `[src: WI-0001/Q-001]`; `item.md` `## Notes` line 145 records Q-002's decision; `plan.md` line 130 carries step 5's rewritten rule; `plan.md` line 100 carries step 2's new test; `plan.md` line 200 is `## Assumptions` 6; `plan.md` line 219 is the new `## Decisions and ADRs` row; the AC6 mapping row names `test_cli.test_leave_lines_are_printed_when_nothing_moves`. No `## Consequences` section names an intention rather than a file.
  - `answered-from-the-record` → **pass** — Q-001 cites `artifacts/refinement-qa.md` Q3 and Q5 by their recorded rationale; Q-002 cites ADR-0002 `## Decision` and `## Consequences`. Neither answer required the record to be declared silent, so neither needed a new ADR.
  - `escalation-is-justified` → **skipped, with the reason** — nothing was escalated. No question was re-addressed to `human`, so the gate has no subject.
  - `workspace-valid` → **pass** — run by the transition accompanying this entry, resolving `WI-0001:awaiting-answer->in-progress`
  - `item-resumed-correctly` → **pass** — the suspending row of 2026-08-27T16:13:02Z records `resume-to: in-progress`, read from `history.md` rather than inferred from which skill asked, and this move targets `in-progress`
  - `a-deferral-is-not-an-answer` → **skipped, with the reason** — neither reply deferred. Both questions were answered by this skill from the record; no reply of the "not yet" kind arrived, so step 3a's two moves do not apply and no item was parked at `blocked`.
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-001.md` — answered; `status: answered`, `answered-by: answer-questions`, `answered-at: 2026-08-27T16:15:23Z`; `## Answer` and `## Consequences` written
  - `tracker/items/WI-0001/questions/Q-002.md` — answered; same stamps; `## Answer` and `## Consequences` written
  - `tracker/items/WI-0001/item.md` — AC15 amended; the `## Notes` "deliberately unconstrained" entry updated to record Q-002's decision and that it stays out of the criteria
  - `tracker/items/WI-0001/artifacts/plan.md` — step 5's output rule rewritten; step 2 gained a fourth test in its ordering; `## Assumptions` gained entry 6; `## Decisions and ADRs` gained a row; the AC6 mapping row gained a test
  - no ADR created, and no document under `docs/` changed, so no version was bumped
- **Status:** `awaiting-answer` → `in-progress`
- **Result:** Both blocking questions on WI-0001 are answered from the record and propagated. Q-001 was a conflict `plan` step 5 introduced rather than one between the criteria, and is resolved in favour of what `refinement-qa.md` says each criterion was for; AC15 now says which criterion governs the overlap. Q-002 is settled by ADR-0002, which permits only the plan-time answer if AC8 is to stay structural. The item returns to `in-progress`, its recorded `resume-to`, with no source file yet written and the plan now executable as it stands.

## 2026-08-27T16:23:59Z — implement v0.2.2 — developer

- **Item:** WI-0001
- **Trigger:** status `in-progress`; dispatched by `next` step 5 as the only runnable item, resuming the execution `answer-questions` returned to `in-progress` at 2026-08-27T16:16:56Z.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — AC1–AC15 as they now stand, including AC15's clause from Q-001
  - `tracker/items/WI-0001/artifacts/plan.md` — steps 1–8, the interface contracts, the output contract, `## Assumptions` 1–6, `## Risks`, and the AC-to-test mapping table
  - `tracker/items/WI-0001/questions/Q-001.md` and `Q-002.md` — read to confirm both are `answered`; the decisions were taken from `plan.md` and `item.md`, which is where `answer-questions` propagated them, not from the question files
  - `tracker/items/WI-0001/history.md` — six rows; the last is the resumption, so this is a continuation and not a send-back
  - `docs/architecture/adr/ADR-0001..ADR-0004` — the interpreter floor and stdlib-only constraint, the two-layer split, the move primitive and its fallback, and the test and lint commands
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, the branch prefix and the commit subject convention
  - the branch itself: `git log main..wi/WI-0001` showed two tracker commits and no source file, so nothing needed reconciling before building
- **Decisions:**
  - **No opening journal entry, deliberately.** SKILL.md step 3 binds it to the move to `in-progress`, and the item was already there. There was no transition to carry an entry, and a free-standing one asserting a move would have been false. Recorded as deviation 6 in the report so the absence is explained rather than noticed.
  - **`os.path.lexists` rather than `os.path.exists`** for both the collision check and the destination-parent check, so a broken symlink counts as an occupied name. Within the plan's latitude and in the direction AC9 points; `os.link` would have refused it anyway, but as an apply-time failure rather than a planned rename.
  - **`no extension` as the leave reason for an extensionless file**, where the plan's template would have rendered `no rule for ''`. The item routes line wording to the developer and AC6 constrains content, not phrasing.
  - **A hyphen rather than an em dash in the preview banner.** The plan gave the text as an example; a hyphen does not depend on the terminal's encoding for a line printed on every run.
  - **Two test helper modules** (`tests/support.py`, `tests/cli_support.py`) holding fixtures and output parsing. `unittest discover`'s `test*.py` pattern does not collect them, so they add no test and no gate surface.
  - **Plan step 4's fallback message goes in the failure list, as written**, even though that makes a fully successful run on a filesystem without hard links exit 1. Following the plan literally and reporting the consequence was the right move; changing it would have been re-litigating a decision this skill does not own. Flagged for `verify` under `## What I did not do`.
  - **Not fixed, filed as knowledge instead:** an unreadable target folder raises `PermissionError` out of `build_plan` with no AC covering it, and top-level symlink handling is unspecified. Both are named in the report rather than guessed at; inventing an exit code and a message for either would be inventing a requirement.
  - **The tests were mutation-checked, not just run.** Five behaviours were removed one at a time — the hidden-file skip, the subfolder skip, collision resolution, the `--apply` guard, and Q-001's unconditional action lines — and the suite re-run each time. Every one produced failures; the suite is green again after restoring each. That is the evidence for `every-criterion-has-a-test`, because a suite that passes against a hollowed-out implementation demonstrates nothing.
  - **One test rewritten during the run.** `test_apply.test_every_move_lands_and_the_source_is_gone` was first written with a tautological sha256 assertion that could not fail. It was replaced with a check that each destination holds the moved file's actual contents.
- **Questions raised:** none this execution — Q-001 and Q-002 were raised earlier and are answered
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → 0 (`Ran 37 tests … OK`) on the branch head
  - `python3 -m compileall -q tidy tests` → 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → 0 (`all 6 commit(s) on main..wi/WI-0001 name WI-0001`)
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0
  - `python3 -m tidy --help` → 0; and a manual end-to-end run over a fixture folder exercising preview, apply, a collision, a subfolder, dotfiles, a re-run, a missing path and an empty folder
  - five mutation runs of `python3 -m unittest discover -s tests -t .` → each FAILED, as intended; the sixth, after restoring, → 0
  - `git commit` ×4 → 0
- **Gates:**
  - `tests-pass` → **pass** — `python3 -m unittest discover -s tests -t . -q` exit 0, 37 tests, run after the last commit
  - `lint-clean` → **pass** — `python3 -m compileall -q tidy tests` exit 0
  - `workspace-valid` → **pass** — `validate-workspace` 0 errors, 0 warnings, and re-run by the transition accompanying this entry
  - `every-criterion-has-a-test` → **pass** — `impl-report.md` `## Acceptance criteria evidence` names a test function for each of AC1–AC15; none is demonstrated by reading code; the mutation table in the same file shows five of them failing when the behaviour is removed
  - `commits-reference-the-item` → **pass** — `check-commit-refs` exit 0 over all six commits in `main..wi/WI-0001`
  - `no-unplanned-scope` → **pass** (advisory) — the diff against `main` is `tidy/rules.py`, `tidy/planner.py`, `tidy/apply.py`, `tidy/cli.py`, `tidy/__main__.py`, six files under `tests/`, and `README.md`. Every one is a numbered plan step. No age routing, no rule loading, no unrelated fix.
  - `claims-are-sourced` → **pass** — `lint-claims --changed-since main` exit 0; no document under `docs/` changed this execution
- **Artifacts:**
  - `tidy/rules.py`, `tidy/planner.py`, `tidy/apply.py`, `tidy/cli.py`, `tidy/__main__.py` — created
  - `tests/support.py`, `tests/cli_support.py`, `tests/test_rules.py`, `tests/test_planner.py`, `tests/test_apply.py`, `tests/test_cli.py` — created; 37 tests
  - `README.md` — created; the AC5 table as a user-readable file, plus both modes, the collision rule and what the tool will not do
  - `tracker/items/WI-0001/artifacts/impl-report.md` — created
  - branch `wi/WI-0001`, commits `4e9b697..f6254de` — four implementation commits (49be3d7 rules+README, 7b7bb58 planner, abe75b6 apply, f6254de cli), each carrying its own tests
- **Status:** `in-progress` → `verifying`
- **Result:** WI-0001 is implemented and every gate passes on the branch head. All fifteen criteria have named tests, and five of the behaviours behind them were removed one at a time to prove the tests fail without them. Three things are handed to `verify` rather than left to be found: ADR-0003's hard-link fallback is unreachable from the test suite and, followed literally, makes a wholly successful run on such a filesystem exit 1; an unreadable target folder raises out of `build_plan` with no criterion covering it; and top-level symlink handling is unspecified.

## 2026-08-27T16:35:22Z — verify v0.1.4 — qa-engineer

- **Item:** WI-0001
- **Trigger:** Status `verifying` — `implement` reported itself complete at 2026-08-27T16:23:59Z; dispatched by `next` as the only runnable candidate (EP-001 has a null owner, WI-0002 and WI-0003 depend on WI-0001, which is not `done`).
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the fifteen acceptance criteria, read **before** the implementation report so the checks were derived from what was asked for rather than from what was built
  - `tracker/items/WI-0001/history.md`
  - `tracker/items/WI-0001/artifacts/plan.md` — the steps, the AC-to-test mapping table, `## Assumptions` 1–6 and `## Risks`
  - `tracker/items/WI-0001/artifacts/impl-report.md` — read after the criteria; treated as claims to check, not as evidence
  - `docs/architecture/adr/ADR-0003-move-with-os-link.md` — what a non-`FileExistsError` `OSError` is supposed to mean
  - `tracker/project.yaml` — `commands.test` and `commands.lint`
  - `README.md` — the file AC5 requires the rule table to be readable in, and the documented exit-status contract
  - the code on `wi/WI-0001` at `6b1873161b148392d8ee5cb6ff5824a4ab404289`: `tidy/rules.py`, `tidy/planner.py`, `tidy/apply.py`, `tidy/cli.py`, `tidy/__main__.py`
  - `.claude/agile-skills/spec/dor-dod.md` §2 and `spec/ids-and-statuses.md` §5 — the bug Definition of Ready and the provenance rule applied to the two bugs filed
- **Decisions:**
  - **Every criterion was checked against a fixture folder built for it, not against the test suite.** AC5 in particular was checked by typing AC5's table by hand from `item.md` into the check script rather than importing `tidy/rules.py`, so a wrong table could not agree with itself. All 59 extension rows and `PHOTO.JPG` were checked, and `README.md`'s table was parsed row by row against the same hand-typed copy.
  - **AC8 was checked against disk state, not only against two printed outputs.** The mutation `apply_plan(folder, actions[:1])` — an apply that silently moves only one file — leaves AC8's own named test green, because that test compares two `render` outputs produced before `apply_plan` is ever called. Preview's printed pairs were therefore checked against what actually landed. The criterion is met; the observation about the suite's coverage of it is in the report.
  - **BUG-0001 and BUG-0002 are bugs, not send-backs.** SKILL.md step 7's test is whether an acceptance criterion of *this* item says the behaviour should be different. For the unreadable folder, AC14 names "a target path that does not exist, or one that is a regular file rather than a folder" and stops there. For the exit status of a successful apply, no criterion speaks at all — AC3's "exit status is 0" is PREVIEW and AC15's is the nothing-to-do case. Sending the item back for either would be verifying against criteria nobody wrote; both were filed at `ready` with `found-in: WI-0001`.
  - **They were filed as two items, not one.** They are unrelated faults in different modules (`planner.build_plan` and `apply.apply_plan`) and each needs its own reproduction and its own later verification.
  - **Three findings were recorded rather than filed.** `impl-report.md`'s symlink claim is wrong in detail — the symlink is moved as a symlink, not replaced by a hard link — but the behaviour matches `mv` and no criterion mentions symlinks. AC8's named test being weaker than AC8 is a coverage observation, not a product defect. `python3 -m tidy` running only from the repository root is exactly what ADR-0001 chose. None is a criterion failure and none justifies an item on its own.
  - **No criterion was judged `ambiguous`, so no question was raised.** AC6-versus-AC15 was the one candidate, and WI-0001/Q-001 had already settled it inside `item.md`; the amended wording was checked directly against the fixture Q-001 named.
- **Questions raised:** none
- **Commands:**
  - `git rev-parse HEAD` → `6b1873161b148392d8ee5cb6ff5824a4ab404289`, branch `wi/WI-0001`
  - `python3 -m unittest discover -s tests -t . -q` → 0 (`Ran 37 tests in 0.037s`, `OK`)
  - `python3 -m compileall -q tidy tests` → 0
  - `python3 -m tidy --help` → 0 (AC1)
  - `python3 -m tidy .harness/f1` → 0, 3 move lines + 2 leave lines; recursive `(path, size, sha256)` listing identical before and after (AC2, AC3, AC4)
  - `python3 -m tidy .harness/f5` over 59 one-per-extension files + `PHOTO.JPG` → 0, `MISMATCHES: none` against the hand-typed AC5 table (AC5)
  - README table parsed against the same table → `DISCREPANCIES: none` (AC5)
  - `python3 -m tidy .harness/f1 --apply` → 0; `(basename, size)` multiset and per-basename sha256 identical before and after (AC6, AC7)
  - preview vs apply over two identical fixtures → `AC8: SETS IDENTICAL`; preview's pairs vs disk after apply → `DISCREPANCIES: none` (AC8)
  - collision fixture, apply → pre-existing `documents/report.pdf` unchanged (`eeeee`, sha `5057ae10c213`), incoming at `documents/report (2).pdf`; both modes print the suffixed name (AC9, AC10)
  - double-collision fixture → incoming became `report (3).pdf`, both existing files unchanged (boundary, beyond any criterion)
  - subfolder fixture, both modes → only `move   photo.jpg -> images/photo.jpg`; `holiday/` listing identical after apply (AC11)
  - `python3 -m tidy .harness/f12 --apply` twice → 0 and 0, listings identical; following preview → 0 move lines, exit 0 (AC12)
  - hidden-file fixture, both modes → dotfiles in neither output, both still at their original paths after apply (AC13)
  - `python3 -m tidy .harness/does-not-exist-xyz` / `.harness/regular.txt`, each × both modes → exit 2, `stdout bytes: 0`, path named on stderr (AC14)
  - four nothing-to-do fixtures × both modes → all eight `exit=0 stdout-lines=1 move-lines=0` (AC15)
  - folder holding only `notes.xyz` and `README`, both modes → two `leave` lines then the nothing-to-do line, 0 move lines, exit 0 (AC15's amendment clause, the WI-0001/Q-001 fixture)
  - folder with a regular file named `images`, both modes → `leave  photo.jpg   ['images' exists and is not a folder]`, nothing moved (plan `## Assumptions` 6)
  - `chmod 000` folder, both modes → **exit 1 with a `PermissionError` traceback** → BUG-0001
  - `os.link` patched to raise `OSError(18)`, apply → both files moved, **exit 1** → BUG-0002
  - symlink fixture, apply → file symlink moved as a symlink, directory symlink skipped, outside target untouched
  - 13 mutations applied one at a time, suite re-run, `git checkout --` after each → 12 of 13 FAILED as intended; the 13th was a badly-formed mutation of mine (dead code after a `continue`), replaced by the subfolder-skip mutation which covers AC11 and AC12
  - `scripts/new-item --id BUG-0001 …` → 0; `scripts/new-item --id BUG-0002 …` → 0
  - `scripts/journal-entry BUG-0001 --skill verify --body-file …` → 0; same for BUG-0002 → 0
  - `scripts/lint-claims --changed-since main` → 0 (`checked no documents changed since main`)
  - `scripts/validate-workspace .` → 0 errors, 0 warnings
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` on `6b18731` → exit 0, `Ran 37 tests … OK`)
  - `lint-clean` → **pass** (`python3 -m compileall -q tidy tests` → exit 0)
  - `workspace-valid` → **pass** (`scripts/validate-workspace .` → `checked 6 item(s), 6 document(s)`, 0 errors, 0 warnings)
  - `every-criterion-independently-checked` → **pass** (every row of the report's `## Criteria` names a command run in this execution and quotes its output; no row cites `impl-report.md`; AC5's expected table was typed from `item.md` rather than imported)
  - `negative-cases-exercised` → **pass** (15 negative and boundary cases triggered, listed in the report — every error, empty-input and boundary case any criterion names, plus four beyond them)
  - `tests-would-fail-without-the-change` (advisory) → **pass** (13 mutations, at least one per criterion, each restored; the table is in the report; `git status` clean and the suite green afterwards)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/verify-report.md` — created, with `Verified-commit: 6b1873161b148392d8ee5cb6ff5824a4ab404289`
  - `tracker/items/WI-0001/item.md` — all fifteen criteria ticked, each against a command in this execution
  - `tracker/items/BUG-0001/` — new bug at `ready`, `found-in: WI-0001`
  - `tracker/items/BUG-0002/` — new bug at `ready`, `found-in: WI-0001`
  - `tracker/board.md` — regenerated
  - commit `tracker: the verification report, the ticked criteria, and any bug items you filed (refs WI-0001)`
- **Status:** `verifying` → `in-review`
- **Result:** All fifteen acceptance criteria pass, each demonstrated by a command run in this execution against `6b18731` rather than by the implementation report. Two defects outside this item's criteria were found by exercising the edges `plan` and `implement` had flagged, and were filed as BUG-0001 and BUG-0002 at `ready` rather than sent back. WI-0001 moves to `in-review`.

## 2026-08-27T16:40:26Z — review-close v0.5.0 — reviewer

- **Item:** WI-0001
- **Trigger:** Status `in-review` — `verify` passed all fifteen criteria at 2026-08-27T16:35:22Z; dispatched by `next` as the highest-ranked runnable item (priority high, rank 2, ahead of BUG-0001 and BUG-0002 at medium).
- **Inputs read:**
  - `tracker/items/WI-0001/item.md`, `history.md` (8 rows), `journal.md` (8 entries, read end to end)
  - `tracker/items/WI-0001/artifacts/plan.md`, `impl-report.md`, `verify-report.md`
  - `tracker/items/WI-0001/questions/Q-001.md` and `Q-002.md`, both `answered`, `## Consequences` checked against the files they name
  - **the diff `main..wi/WI-0001`** — twelve files, 951 lines, read hunk by hunk: `tidy/rules.py`, `tidy/planner.py`, `tidy/apply.py`, `tidy/cli.py`, `tidy/__main__.py`, `README.md`, and all six files under `tests/` including the two helper modules
  - `docs/architecture/overview.md`, `docs/product/vision.md`, `docs/architecture/adr/ADR-0001..ADR-0004` — for D12, each audited claim decided by opening what it cites
  - `.claude/agile-skills/spec/dor-dod.md` §3 (D1–D12), `spec/doc-header.md` §4a, `spec/work-item.md` §`outcome`
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, `trunk-branch`
- **Decisions:**
  - **Accept, not reject.** Every hunk in the diff maps to a plan step and a criterion; nothing is unrequested scope; no import leaves the standard library, so ADR-0001 holds; no error path swallows an error. The mapping table is in `review.md` `## What I examined`.
  - **Three documents were corrected rather than waved through (D12), each with a version bump and a change-log row.** (a) `overview.md` v2 — the never-overwrite paragraph read as though the guarantee were always kernel-enforced; ADR-0003's `_move_without_a_link` is a check-then-act, and the overview did not say so. (b) `ADR-0002` v2 — `## Decision` 1 named an `Action` kind `skip` that `build_plan` never emits; the implementation omits hidden files and subfolders entirely, which is stronger than what the ADR asked for. (c) `ADR-0004` v2 — its "`tests/` contains only an empty package marker … `NO TESTS RAN` … exits 5" note had become false; the command now runs 37 tests and exits 0. In all three the *decision* is untouched: correcting a fact is not superseding, and superseding is not this skill's to do.
  - **The `skip` deviation is a finding, not a send-back.** It is an undeclared deviation — `impl-report.md` lists six and this is not among them — but it is a deviation toward the criterion: AC13 requires a hidden file to appear in neither mode's output, and an entry producing no `Action` cannot be rendered by mistake, where a `skip` action would have depended on `render` suppressing it.
  - **Five gaps accepted, and all five written into `item.md` `## Notes`** rather than left in the verification report: the untested hard-link fallback, AC8's suite coverage resting on AC7's test, unspecified symlink handling (with `impl-report.md`'s incorrect account of it corrected from a run), `python3 -m tidy` running only from the repository root, and Linux/ext4-only verification. An accepted gap that lives only in a report of a closed item is a paper trail that has quietly stopped being true.
  - **No bug filed by this execution.** The two defects in play were found by `verify` and already exist as BUG-0001 and BUG-0002. Findings 4 and 5 in `review.md` — the weak AC8 test and the `setUp()`-inside-`subTest` idiom — are test-quality observations, not defects in delivered behaviour, and were recorded rather than turned into items.
  - **No question filed.** Nothing in the change contradicts an ADR once the three documents are corrected, so there was nothing for the architect to arbitrate.
  - **Close, then merge — in that order**, per SKILL.md step 8: `check-commit-refs` inspects `main..wi/WI-0001`, which merging first would empty.
  - **The engagement is not over and no sign-off is due.** `scripts/engagement-state EP-001` → `active`, four children still in flight. Filing a sign-off question now would ask the stakeholder to accept work nobody has done.
- **Questions raised:** none
- **Commands:**
  - `check-verify-freshness WI-0001 wi/WI-0001` → 0 — "verified at `6b187316`; `wi/WI-0001` has moved to `e710724d` but only the record changed (15 file(s) under `tracker/` or `docs/`), so the verification still covers the code" (D10, compared rather than assumed)
  - `check-commit-refs WI-0001 wi/WI-0001` → 0 — "all 8 commit(s) on main..wi/WI-0001 name WI-0001" (D8)
  - `git rev-parse main` before the trial → `d46b85263d17218fc1896e49b740e55ca6f2b1e1`
  - `git worktree add --detach .harness/trial-WI-0001 main` → 0 (detached, per F-055)
  - `git -C .harness/trial-WI-0001 merge --no-ff wi/WI-0001` → 0, no conflict, merge commit `9286fe35d249ea55dc3ee4378e7c2bb861f5e2cf`
  - `python3 -m unittest discover -s tests -t . -q` **inside the trial worktree** → 0, `Ran 37 tests in 0.035s`, `OK`
  - `python3 -m compileall -q .harness/trial-WI-0001/tidy .harness/trial-WI-0001/tests` → 0
  - `git worktree remove --force .harness/trial-WI-0001` → 0; `git rev-parse main` after → `d46b85263d17218fc1896e49b740e55ca6f2b1e1`, unchanged
  - `python3 -m unittest discover -s tests -t . -q` on the branch → 0, `Ran 37 tests … OK`
  - `python3 -m compileall -q tidy tests` → 0
  - `lint-claims --changed-since main` → 0, "checked 3 document(s) changed since main", 0 errors
  - `validate-workspace .` → 0 errors, 0 warnings
  - `engagement-state EP-001` → "EP-001 active — still in flight: BUG-0001, BUG-0002, WI-0001, WI-0002, WI-0003"
- **Gates:**
  - `definition-of-done` → **pass** (D1–D12 walked one at a time with per-criterion evidence; the table is in `review.md` `## Definition of Done`. D7 and D12 passed only after this execution corrected `overview.md`, `ADR-0002` and `ADR-0004`)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` → exit 0, quoted above)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` → exit 0, 8 of 8)
  - `tests-pass-on-the-merge-result` → **pass** (`Ran 37 tests … OK`, exit 0, run **inside the trial worktree at `9286fe3`**, not on the branch; lint also 0 there)
  - `workspace-valid` → **pass** (`validate-workspace .` → 0 errors, 0 warnings)
  - `record-is-reconstructible` → **pass** — answered from the tracker, `docs/` and `git log` alone: *what was built and why* — `item.md` `## Story` and the epic goal, delivered as five modules and a README across four layered commits; *which skill decided what* — `refine` turned six rough criteria into fifteen decidable ones under the stakeholder's standing deferral on EP-001/Q-001, `plan` minted ADR-0002/0003/0004 and chose `python3 -m tidy`, `--apply` and the line forms, `answer-questions` settled the AC6/AC15 overlap and the taken-destination-name case, `implement` built it, `verify` checked it and filed two bugs, this review corrected three documents; *what questions arose and how they were resolved* — Q-001 and Q-002, both answered from the record with `## Consequences` naming the artifacts they changed, plus EP-001/Q-001..Q-004 answered by the stakeholder; *what verification found* — fifteen passes with quoted output, fifteen negative and boundary cases, thirteen mutations, two defects outside the criteria
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` → 0 errors over the 3 documents this execution changed; every absolute sentence added carries a resolvable `[src: ...]`)
  - `epic-sign-off` → **not applicable, and checked rather than assumed** — this is a work-item close, not an engagement ending. `engagement-state EP-001` reports `active` with four children in flight, so no sign-off question is due and none was filed
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/review.md` — created; `## What I examined` names the diff range, the eight audited claims and what was opened for each
  - `tracker/items/WI-0001/item.md` — `## Notes` extended with the five accepted gaps; `status: done`, `outcome: delivered`
  - `docs/architecture/overview.md` → v2, `docs/architecture/adr/ADR-0002-separate-planning-from-applying.md` → v2, `docs/architecture/adr/ADR-0004-test-and-lint-commands.md` → v2, each with a change-log row
  - commit `docs: the D12 audit's three corrections, and WI-0001's accepted gaps (refs WI-0001)` (`8fdbb3d`)
  - `tracker/board.md` — regenerated
  - the merge of `wi/WI-0001` into `main`, made after this close
- **Status:** `in-review` → `done`
- **Result:** Accepted and closed as `delivered`. Definition of Done D1–D12 all pass, three of them only after this review corrected documents that had stopped being true — the never-overwrite guarantee described as unconditional, an `Action` kind that was never built, and a test-command note that predicted its own expiry and was never revisited. The trial merge into a detached worktree of `main` was clean and the suite and lint passed on the merge result; `main` did not move. Five gaps were accepted into `item.md` `## Notes`; the two real defects remain open as BUG-0001 and BUG-0002. The engagement stays `open` — `engagement-state` reports four children still in flight.
