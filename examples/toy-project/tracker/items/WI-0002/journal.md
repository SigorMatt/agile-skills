# Journal — WI-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-16T21:15:23Z — intake v0.1.0 — product-analyst

- **Item:** WI-0002
- **Trigger:** invoked directly; created by the same `intake` execution that opened EP-001
- **Inputs read:** the human's answers in session (recorded verbatim in
  `tracker/items/EP-001/journal.md`); `tracker/project.yaml`; `tracker/items/` (empty)
- **Decisions:**
  - Created as a separate item at the human's explicit instruction: "One thing I do want, but as
    a *second* piece of work after the basic thing works … Don't build it into the first item."
    Left to my own judgement I would have folded a flag this small into WI-0001, so the reason it
    stands alone is recorded here to stop a later reader treating the split as an oversight.
  - `depends-on: WI-0001` — there is no listing to limit until WI-0001 exists. This also encodes
    the human's stated build order in a form the orchestrator enforces.
  - `priority: medium` — the epic is coherent without this flag. The human called it "genuinely
    useful" but sequenced it second, and `medium` behind WI-0001's `high` is what makes the
    orchestrator honour that ordering.
  - AC4 (a bad `--top` value fails loudly and non-zero) is derived from his rule about a missing
    folder, not stated by him about this flag. Marked as derived in `## Notes` so `refine`
    confirms it rather than inheriting it as settled.
- **Questions raised:** none filed as artifacts — the human was present. Three open points are
  recorded in this item's `## Notes` for `refine`: whether the total covers all files or only
  the rows shown, whether AC4 reflects the human's intent, and flag position relative to the
  folder argument.
- **Commands:** `python3 .claude/agile-skills/scripts/new-item --id WI-0002 --type work-item
  --epic EP-001 --title "Add --top N to show only the N largest files" --priority medium
  --status draft --actor intake --reason "created from idea intake for EP-001; human deferred it
  behind WI-0001"` → exit 0
- **Gates:** all four are recorded once, on EP-001's journal entry for this execution, since one
  `intake` execution created the epic and both items. `workspace-valid` → **pass**;
  `epic-has-success-measures` → **pass**; `items-are-separable` → **pass** (declares
  `depends-on: WI-0001`, built second); `no-solution-in-the-problem` → **pass** (`--top N` is
  the human's own phrasing from his answer to Q7).
- **Artifacts:** `tracker/items/WI-0002/item.md`, `journal.md`, `history.md` (all new)
- **Status:** `—` → `draft`
- **Result:** Created at `draft`, sequenced behind WI-0001, with the total-line ambiguity flagged
  for `refine` rather than guessed at.

## 2026-08-16T21:27:40Z — refine v0.1.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`; invoked directly by the human, immediately after WI-0001 was
  refined in the same session, not dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — did not exist before this execution
  - `tracker/items/EP-001/journal.md` — the human's intake answers, verbatim, Q7 in particular
  - `tracker/items/WI-0001/item.md` (now `ready`, the thirteen criteria this item builds on) and
    `tracker/items/WI-0001/artifacts/refinement-qa.md`
  - `tracker/items/EP-001/item.md`, `docs/product/vision.md` (v1), `tracker/project.yaml`
  - `.claude/agile-skills/spec/dor-dod.md`, `work-item.md`, `journal-and-history.md`
- **Decisions:**
  - **Four criteria became eleven.** Each rewrite, and what changed about its meaning:
    - *AC1* — was "prints file rows for at most three files, and they are the three with the
      highest line counts", silent on whether a total row still appears and on what it counts.
      Now inherits WI-0001 AC1's row format and AC2's order by reference, and says the total row
      follows.
    - *AC2* — new, and it is the substance the old AC1 lacked: the limit is applied **after**
      sorting, so a tie at the cut line is broken by filename rather than by chance. Fixture
      (9, 5, 5, 5) written into the criterion.
    - *AC3* — the total's meaning, the one question intake flagged as unanswerable here. It is
      the sum of every file in the folder, and the label says so: `total (all M files)`. M is
      spelled out as "the number of rows the same command would print without `--top`" because
      the criterion already uses N for the flag's argument.
    - *AC4* — was "the same output as it did before this item", checkable only by reference to a
      version that no longer exists. Now two observations: the plain `total` label is kept when
      the flag is absent, and WI-0001's tests pass unmodified.
    - *AC5* — was AC3 (N larger than the file count). Substance unchanged; gained the ruling that
      the label still says `(all M files)` because the flag was given, which is the case a reader
      would otherwise guess at.
    - *AC6* — new. `--top 0` is not an error: no file rows, total row still printed, exit 0.
    - *AC7* — was AC4, "an unusable value … prints a message naming the problem and exits with a
      non-zero status", with zero folded in as unusable and the stream unstated. Zero is now
      explicitly legal (AC6), and the failure shape is pinned to WI-0001 AC11: empty stdout, one
      stderr line, exit 2.
    - *AC8* — new. Flag position either side of the folder argument, and `-t` must actively fail.
    - *AC9* — new. The empty folder keeps WI-0001 AC10's behaviour whatever N is.
    - *AC10* — new. Column width is sized to the widest number printed, the total included; this
      only became a question once AC3 allowed the total to exceed every visible row.
    - *AC11* — new, analyst-derived: `python3 -m unittest discover` still exits 0.
  - **The analyst's own proposal was rejected on the biggest question, and that is recorded.**
    I proposed the unlabelled all-files total (option a); the human chose the labelled variant
    (option c) and gave the reason — he would wonder why the column does not add up. The Q&A
    keeps my proposal and his rejection rather than presenting (c) as the plan all along.
  - **WI-0001 was deliberately not edited.** AC6 here prints a total row when no file row is
    listed, which sits outside WI-0001 AC3's condition ("when at least one file is listed")
    rather than contradicting it, and AC9 keeps WI-0001 AC10 whole. WI-0001 is past `ready`,
    where `spec/work-item.md` §2 allows criteria to change only through `answer-questions` or a
    send-back to `refine`. Loosening a neighbouring item's criterion to make this one fit is the
    exact failure that rule exists to prevent, so the interaction is written into this item's
    `## Notes` instead.
  - **Intake's derived AC4 is no longer derived.** The human confirmed it in as many words, so it
    moves out of the assumptions list and into the settled list.
  - **Assumptions recorded, and why each is safe.**
    - *Flag position and the absence of `-t` (AC8)*, and *the empty folder with `--top` (AC9)* —
      proposed by me, confirmed verbatim. Safe: both follow rules he did state (no flags to
      remember; WI-0001's empty-folder behaviour) rather than adding new ones.
    - *AC11 (the test command)* — proposed with its label and accepted with it: "Mark it as your
      own if that's the honest label."
    - *The plural inside `(all M files)`* — **never put to him**. A one-file folder yields
      `(all 1 files)`. Safe because it is cosmetic, cannot change a count, and reversing it is a
      one-line change; special-casing it would add a rule every verifier then has to check.
  - **Deliberately left to `plan`:** the wording of the stderr messages in AC7 and AC8, exactly
    as for WI-0001; and whether `--top` is implemented with `argparse` or by hand. The criteria
    constrain the observable behaviour, not the mechanism.
  - **No conflict with the vision or the epic.** EP-001 names `--top N` in `## Scope` as a later,
    separate addition, which is what this item is. The vision's "no flags for the common case"
    is unaffected: the common case remains `python3 linecount.py <folder>`, and AC4 pins it to
    WI-0001's behaviour byte for byte. No update to `docs/product/vision.md` was needed.
- **Questions raised:** six, asked in one batch, all answered, plus one addendum put to the human
  before it was written into a criterion. Recorded verbatim in
  `tracker/items/WI-0002/artifacts/refinement-qa.md`. None left `[unresolved]`. No question
  artifact was filed — the human was present. One decision (the plural in the total label) was
  never put to him and is marked as the analyst's own there and in `## Notes`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/run-gate --skill refine --item WI-0002 --all` → exit 0
    (`workspace-valid` PASS; the other three reported MANUAL and are recorded below)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 1 warning
    (`project.commands.test-null`, a `plan` responsibility)
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to ready --actor refine --reason
    "Definition of Ready passed criterion by criterion; 6 questions answered, 11 criteria now
    decidable"` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` (hard) → **pass** — `validate-workspace` exits 0; the single warning is
    about `commands.test` being null, which belongs to `plan`.
  - `definition-of-ready` (hard) → **pass**, criterion by criterion per `spec/dor-dod.md` §1:
    - *R1* **pass** — frontmatter complete; `type: work-item`, `epic: EP-001`,
      `priority: medium`, `depends-on: [WI-0001]` resolves [auto].
    - *R2* **pass** — role ("someone scanning a folder that holds a couple of hundred files"),
      capability ("ask for only the N largest"), outcome ("without piping the output through
      another command"). Unchanged by this execution.
    - *R3* **pass** — AC1–AC11, each a labelled checkbox [auto].
    - *R4* **fail on entry → pass after rewrite.** All four original criteria had a hole: AC1 was
      silent on the total row and on ties at the cut; AC2 defined itself against a version of the
      tool that would no longer exist; AC3 inherited the same total ambiguity; AC4 fixed neither
      the stream nor the exit code and wrongly folded `--top 0` in with negative and non-numeric
      values. Three cases were missing entirely: flag position, the empty folder under `--top`,
      and the column width once the total can exceed every visible row. Scanned the rewritten
      list for unmeasurable adjectives ("reasonable", "sensible", "clean", "properly",
      "appropriate", "gracefully"): none occurs.
    - *R5* **pass** — `## Out of scope` has six entries; `-t` and "select by threshold rather
      than rank" are both things a reader could reasonably assume are included.
    - *R6* **pass** — no open question on this item [auto].
    - *R7* **pass** — `depends-on: WI-0001` is unfinished, which R7 permits provided the
      dependency is recorded and the item is sequenced after it: it is, in frontmatter and on the
      board (`blocked by WI-0001 (ready)`), and `priority: medium` behind WI-0001's `high` makes
      `next` honour the order [auto].
    - *R8* **fail on entry → pass** — `artifacts/refinement-qa.md` did not exist; it now holds
      the whole exchange, tagged.
    - *R9* **pass** — one flag on one existing script plus its tests. Reassessed after the
      rewrite: eleven criteria describe one flag's behaviour in eleven situations, not eleven
      deliverables, and the item cannot be split further without producing a flag that parses but
      does not limit.
  - `criteria-are-decidable` (hard) → **pass** — the command or observation that settles each,
    and the verdict that follows. `F` below is a fixture folder built with ordinary shell
    commands:
    - *AC1* — `F` with four files; `python3 linecount.py --top 3 F` → exactly three file rows in
      WI-0001 AC1's format, then the total row. A fourth file row → fail.
    - *AC2* — `F` = `big.txt` (9 lines), `a.md`, `b.md`, `c.md` (5 each); `--top 3` → rows
      `big.txt`, `a.md`, `b.md`, and `grep -c c.md` on stdout → 0.
    - *AC3* — `F` of 27 files summing 1204; `--top 3` → last line exactly
      `1204  total (all 27 files)`.
    - *AC4* — `python3 linecount.py F` → last line is `1204  total`, with no parenthesis; and
      `python3 -m unittest discover` runs WI-0001's own tests unmodified → exit 0.
    - *AC5* — `F` of 4 files; `--top 99` → four file rows and the labelled total; `echo $?` → 0.
    - *AC6* — `--top 0` on `F` → no file row on stdout, the labelled total row present,
      `echo $?` → 0.
    - *AC7* — `--top -1 F` and `--top abc F` → empty stdout, one stderr line, `echo $?` → 2.
    - *AC8* — `--top 3 F > a` and `F --top 3 > b`; `diff a b` empty and exit 0; then `-t 3 F` →
      empty stdout, stderr non-empty, `echo $?` → 2.
    - *AC9* — an empty folder and a folder holding only `sub/`, each with `--top 0`, `--top 3`,
      `--top 99` → stdout exactly `no files`, stderr empty, exit 0, no total row.
    - *AC10* — `F` of 27 files summing 1204 whose two largest are 9 and 7; `--top 2` → the three
      lines quoted in AC10, space for space.
    - *AC11* — `python3 -m unittest discover` from the repository root → exit 0, and `tests/`
      contains tests naming `--top`.
  - `qa-recorded-verbatim` (hard) → **pass** — `artifacts/refinement-qa.md` holds all six
    questions as asked, plus the addendum, and every answer as given, in order. Q1 keeps my
    rejected proposal and his reason for rejecting it. Q4, Q5 and the addendum are tagged
    `[assumed]` because I proposed them and he confirmed. The unasked plural decision has its own
    section as not put to him. Every human tag reads `[human — simulated by the builder]`,
    because this run is a methodology test and the record must not claim a real person said
    these things.
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0002/item.md` (rewritten: criteria, out-of-scope, notes; `updated` bumped)
  - `tracker/items/WI-0002/journal.md` (this entry), `history.md` (one row)
  - `tracker/board.md` (regenerated)
  - commit on `main` covering `tracker/`, referencing WI-0002
- **Status:** `draft` → `ready`
- **Result:** WI-0002 is Ready with eleven criteria, each settled by a named command or
  observation. The total-line ambiguity intake flagged is closed in the human's own words, with
  the label he asked for; three behaviours are recorded as assumptions he confirmed, and one
  cosmetic decision is recorded as the analyst's own. No epic item remains at `draft`.

## 2026-08-17T00:06:20Z — plan v0.1.1 — architect

- **Item:** WI-0002
- **Trigger:** status `ready`, dispatched by `next` — runnable for the first time, because its
  `depends-on: WI-0001` reached `done`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` (AC1–AC11, `## Out of scope`, `## Notes`)
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — all six answers, including Q1 where the
    human rejected the analyst's own proposal in favour of the labelled total
  - `tracker/items/WI-0001/item.md` — read as a **constraint**, not for context: its AC1, AC2,
    AC3 and AC10 are what "byte-identical" in this item's AC4 means
  - `tracker/items/WI-0001/artifacts/review.md` and `verify-report.md` — the accepted gaps and
    what was never verified, so this plan does not assume more coverage than exists
  - `docs/architecture/overview.md` (v1 at the time), `ADR-0001`, `ADR-0002`, `ADR-0003`,
    `docs/product/vision.md` (v1), `tracker/project.yaml`
  - the code on `main` at `461e37f`: `linecount.py` (117 lines) and `tests/test_linecount.py`
    (271 lines, 27 tests) — read in full, because this change edits four of its five functions
- **Decisions:**
  - **`--top` is validated by our own `parse_top`, not by argparse's `type=int`** (ADR-0004).
    Rationale: AC7 wants **one** line on stderr and argparse writes two (a `usage:` block, then
    the message). The tidier alternative — overriding `ArgumentParser.error` — would change the
    message for WI-0001's no-argument case as well, which is exactly what AC4's byte-identity
    clause is least clear about, and it buys nothing because AC12 never asked for one line.
    Branch: **decided here**.
  - **`format_report` grows `total=None, label="total"` rather than changing shape** (ADR-0005).
    Rationale: AC4 requires WI-0001's tests to pass **unmodified**, and those tests call the
    one-argument form with exact expected strings, including `format_report([]) == "no files\n"`.
    Optional parameters keep every one of them true by construction; a second renderer would
    duplicate the column arithmetic that two items' criteria state to the space character.
    Branch: **decided here**.
  - **`main` decides emptiness before it decides the limit** — `if top is None or not rows`.
    Rationale: AC9 says a folder with no files prints `no files` whatever N is, and AC6 says
    `--top 0` on a folder that *has* files still prints the total row. Ordering the two tests this
    way makes both fall out of one expression. Branch: **documented** (both are criteria).
  - **`--top` slices an already-sorted list.** Rationale: AC2's tie at the cut line then comes
    from WI-0001's comparator rather than from a second rule that could disagree with it.
    Branch: **documented** (AC2, refinement Q3).
  - **Four recorded assumptions instead of four questions**: what `int()` accepts (`3_0` → 30),
    the un-pluralised `(all 1 files)` label the item already carries, that M counts the files the
    tool listed (so an ADR-0002 skip is in neither M nor the total), and the wording of the new
    stderr line. Each is one function or one string to reverse; each is under `## Assumptions`
    with that cost. Branch: **assumed**.
  - **Updated `docs/architecture/overview.md` to v2 myself.** Rationale: the function table
    changes, and `implement` and `verify` may not write to `docs/` (`spec/doc-header.md` §5), so
    an overview left at v1 would be wrong the moment the code lands.
  - **Asked the human nothing.** Every open point was already settled in refinement, answerable
    from WI-0001's criteria, or reversible enough to record as an assumption.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
    (7 documents now: two new ADRs)
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `git log --oneline -3` / `git branch --show-current` → `main` at `461e37f`, WI-0001 merged
- **Gates:**
  - `workspace-valid` (hard) → **pass** — `validate-workspace` exit 0, 0 errors, 0 warnings
  - `every-criterion-is-addressed` (hard) → **pass** — the `## Acceptance criteria mapping` table
    in `artifacts/plan.md` carries one row per criterion AC1–AC11, each naming the step that
    satisfies it and the named test that will demonstrate it. Three criteria (AC2, AC3, AC10) are
    demonstrated with the item's own worked fixtures, so the verifier does not have to invent one
  - `project-commands-resolved` (hard) → **pass** — `commands.test` is `python3 -m unittest
    discover`, unchanged and demonstrably runnable (27 tests pass on `main` today);
    `commands.lint` and `commands.build` stay null with ADR-0003 recording why, so `lint-clean`
    will again be reported as skipped rather than passed
  - `decisions-recorded` (hard) → **pass** — `## Decisions and ADRs` lists eight choices: two
    point at ADR-0004 and ADR-0005, four at criteria or refinement answers that already settled
    them, and the assumptions at `## Assumptions` with their reversal costs
  - `plan-is-executable-without-you` (advisory) → **pass** — steps 1–4 give the function
    signatures, the two rejection messages, the exact `main` wiring and the observable result of
    each; step 5 names every test to add and forbids editing an existing one. What is left to the
    developer is fixture construction, not behaviour
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/plan.md` (new)
  - `docs/architecture/adr/ADR-0004-rejecting-a-bad-top-value.md` (new, v1)
  - `docs/architecture/adr/ADR-0005-format-report-keeps-its-old-signature.md` (new, v1)
  - `docs/architecture/overview.md` (v1 → v2, with a change-log row)
  - `tracker/items/WI-0002/journal.md` (this entry), `history.md` (one row)
  - `tracker/board.md` (regenerated); commit on `main` covering `tracker/` and `docs/`
- **Status:** `ready` → `planned`
- **Result:** WI-0002 has a six-step plan that touches four functions in one file, with all eleven
  criteria mapped to a step and a named test. The two decisions the criteria force — how a bad
  `--top` value is rejected, and how the renderer prints a total it cannot derive — are ADR-0004
  and ADR-0005. The criterion most likely to break silently is AC4 (nothing changes without the
  flag), and the plan makes its evidence mechanical: no deleted line in the test file, and
  WI-0001's 27 tests still in the passing set.

## 2026-08-17T00:18:40Z — implement v0.1.0 — developer

- **Item:** WI-0002
- **Trigger:** status `planned`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` (AC1–AC11, `## Out of scope`, `## Notes`),
    `artifacts/plan.md` (steps 1–6 and the mapping table), `history.md` (no send-back — a first
    implementation), `questions/` (empty at the start; this execution filed Q-001)
  - `docs/architecture/adr/ADR-0001` … `ADR-0005`, `docs/architecture/overview.md` (v2)
  - `tracker/project.yaml`; `tracker/items/WI-0001/item.md` for the criteria AC4 makes binding
  - the code on `main` at `461e37f`: `linecount.py` (117 lines) and `tests/test_linecount.py`
    (271 lines), both read in full before changing either
  - the branch: `wi/WI-0002` did not exist; `git log main..wi/WI-0002` was empty
- **Decisions:**
  - **Moved the item to `in-progress` before writing any code**, as the procedure asks. The
    tooling now reports the gates on that move without refusing it — `commits-reference-the-item`
    failed there, correctly and harmlessly, because nothing had been committed yet. That is the
    friction the WI-0001 run recorded and worked around; it no longer exists.
  - **Filed `Q-001` about AC10 instead of quietly choosing a fixture.** The criterion's example
    folder cannot exist: 27 files whose two largest hold 9 and 7 lines sum to at most 243, not
    1204. I implemented the rule (the column covers the widest number printed, total included),
    demonstrated the criterion's exact three lines at the renderer, and split the end-to-end
    evidence into two buildable folders — one keeping the 27 files and the 1204 total, one
    keeping the "two largest hold 9 and 7". Editing AC10 to fit is precisely what a developer may
    not do.
  - **Filed it `blocking: false`.** The honest test is whether I could proceed, and I could:
    nothing about the delivered behaviour turns on the answer, only the wording of an
    illustration. A blocking question would have suspended an item that was not stuck and stopped
    the run for a correction `answer-questions` can make from the record.
  - **New test classes rather than new methods in WI-0001's classes.** `ParseTopTest`,
    `TopFormatTest` and `TopTest` are additions; WI-0001's three classes are untouched. Rationale:
    AC4's "the tests written for WI-0001 pass unmodified" then has mechanical evidence —
    `git diff main -- tests/test_linecount.py | grep -c "^-[^-]"` → 0 — instead of resting on my
    word. This differs from the plan, which named two of the tests as members of
    `FormatReportTest`; same tests, better evidence.
  - **Updated the module docstring's usage line** to `[--top N] <folder>`. One line, no
    behaviour, not in the plan; a docstring that omitted the flag would have been wrong on
    delivery.
  - **Left every WI-0001 failure path exactly as it was**, including argparse's two-line usage
    block for a missing argument. AC7 asks for one line only for a bad `--top` value, and
    ADR-0004 already rejected unifying them because that is what would put AC4 at risk.
  - **Did not test `--top` against an unreadable file** (ADR-0002's skip). No criterion covers the
    interaction; it is declared in the implementation report's `## What I did not do` rather than
    left for `verify` to notice.
- **Questions raised:** `Q-001` (non-blocking, to architect) — AC10's worked example describes a
  folder that cannot exist; three options and a recommendation are in the file. The item was **not**
  suspended, because the question is not blocking.
- **Commands:**
  - `git checkout -b wi/WI-0002` → exit 0
  - `scripts/transition WI-0002 --to in-progress --actor implement --branch wi/WI-0002` → applied;
    gates reported, not blocking ("'implement' only gates its completion transition (to
    'verifying')")
  - `python3 -m unittest discover` after the code change, before the new tests → exit 0, 27 tests
    — the first check that AC4 held
  - `python3 -m unittest discover` on the branch head → exit 0, `Ran 46 tests in 1.154s`, `OK`
  - `git diff main -- tests/test_linecount.py | grep -c "^-[^-]"` → `0` (no deleted line)
  - `git commit` → `abc7c66 linecount: add --top N, limiting the rows but not the total (refs
    WI-0002)`
  - `scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, 1 of 1
  - manual: `python3 linecount.py $D` → the plain report and `139  total`;
    `--top 2 $D` and `$D --top 2` → identical, `139  total (all 4 files)`;
    `--top 0 $D` → `139  total (all 4 files)` alone; `--top abc $D` → `linecount: --top: 'abc' is
    not a whole number`, exit 2; `--top -1 $D` → `linecount: --top: -1 is negative`, exit 2;
    `-t 2 $D` → argparse's usage block, exit 2
  - `scripts/board-gen .` → rewrote the board with the new open question
  - `scripts/validate-workspace .` → exit 0 after the board was regenerated
- **Gates:** (full evidence in `artifacts/impl-report.md` `## Gates`)
  - `tests-pass` (hard) → **pass** — 46 tests, exit 0, on branch head `abc7c66`
  - `lint-clean` (hard) → **skipped** — `{{commands.lint}}` is null; ADR-0003 says why. Not a pass
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors
  - `every-criterion-has-a-test` (hard) → **pass** — AC1–AC11 each map to a named test asserting
    exact bytes or an exit code; AC10's end-to-end half uses two buildable folders instead of the
    criterion's impossible one, which is Q-001's subject
  - `commits-reference-the-item` (hard) → **pass** — 1 of 1 commit names WI-0002
  - `no-unplanned-scope` (advisory) → **pass** — two files touched: one new function, one new
    argument, two optional parameters, the `main` wiring, one docstring line, and three appended
    test classes. Nothing WI-0001 delivered was refactored
- **Artifacts:**
  - `linecount.py` (117 → 164 lines), `tests/test_linecount.py` (271 → 451 lines, 27 → 46 tests)
  - `tracker/items/WI-0002/artifacts/impl-report.md` (new)
  - `tracker/items/WI-0002/questions/Q-001.md` (new, open, non-blocking)
  - branch `wi/WI-0002`, commit `abc7c66`, plus this execution's tracker commit
  - `tracker/items/WI-0002/journal.md` (this entry), `history.md` (two rows), `tracker/board.md`
- **Status:** `planned` → `in-progress` → `verifying`
- **Result:** `--top N` is delivered on `wi/WI-0002`: 19 new tests, 46 in total, all passing, with
  WI-0001's 27 untouched and provably so. One criterion — AC10 — turned out to describe a folder
  that cannot exist; the rule behind it is implemented and demonstrated, and Q-001 asks the
  architect how the wording should be corrected rather than quietly correcting it.

## 2026-08-17T00:24:10Z — answer-questions v0.1.1 — architect

- **Item:** WI-0002
- **Trigger:** `Q-001` open and addressed to `architect`; dispatched by `next` at step 3, ahead of
  any status owner. The item was **not** at `awaiting-answer` — the question is non-blocking, so
  it sits at `verifying` throughout
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-001.md` — the only question on this item, and the only
    open question in the workspace
  - `tracker/items/WI-0002/item.md` (AC1–AC11 and `## Notes`), `artifacts/plan.md`,
    `artifacts/impl-report.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — **Q6 in particular**, which is where the
    answer came from: the human confirmed the alignment rule in the words AC10's first sentence
    now carries
  - `tracker/items/WI-0001/item.md` (AC1, AC2, AC3, AC10 — the criteria WI-0002 AC4 makes binding)
  - `docs/architecture/overview.md` (v2), `ADR-0001` … `ADR-0005`, `docs/product/vision.md` (v1)
    — checked for anything that would contradict the correction; none does
- **Decisions:**
  - **Answered Q-001 with option A: correct the example, leave the rule alone.** Route:
    **recorded intent** (`spec/question.md` §1 step 2), not my own judgement. Refinement Q6 put
    the rule to the human as "size the column to the widest number actually printed, total
    included, so everything lines up", and he confirmed it verbatim; that sentence is what AC10
    exists to state and it is untouched. The illustration beside it was arithmetically impossible
    — 27 files whose largest holds 9 lines reach 243, never 1204 — so it was replaced with a
    folder that exists: 26 files of 46 lines and one of 8, still 27 files and still 1204 lines.
  - **Amended an acceptance criterion, which is a thing only this skill and `refine` may do, and
    recorded it in three places** — inline in AC10, in the item's `## Notes` under "Amended after
    `ready`", and in Q-001's `## Consequences`. The test that this is not the failure mode the
    procedure warns about ("amending a criterion to match what was built") is whether the
    criterion still describes what the human asked for: it does, in his own words, and the
    delivered code was written against the rule rather than against the example — the *original*
    expected output is still produced exactly, by `TopFormatTest.
    test_ac10_width_covers_an_explicit_total`. Only the folder that demonstrates it changed.
  - **Rejected option B** (keep the impossible example, explain it in a footnote): it leaves a
    criterion no verifier can check end to end, and every future reader has to rediscover the
    contradiction. **Rejected option C** (split AC10 in two): disproportionate — it turns one
    criterion the human recognises into two he never saw, over a slip in an illustration.
  - **Did not escalate to the human.** None of the four conditions in `spec/question.md` §4
    holds: the intent is recorded verbatim, the change is reversible in one paragraph, it
    contradicts no ADR or product document, and it is not a coin flip. Escalating would have
    spent his attention on the arithmetic of his own example.
  - **Left `impl-report.md` alone.** It is another skill's record of its own execution and was
    true when written; rewriting it would erase the evidence that the defect was caught during
    implementation rather than at review. Left `tests/test_linecount.py` alone too: this skill
    writes no code, and both `test_ac10_*` tests keep their assertions — one of them *is* the
    corrected example, the other is now extra coverage.
  - **No status change.** Step 7 applies only to an item suspended by a blocking question; this
    one never was, so there is no `resume-to` to honour and WI-0002 stays at `verifying` for
    `verify` to pick up with the corrected criterion in hand.
  - **No ADR written.** The answer decides nothing about the system — it repairs an illustration.
    An ADR here would pad the trail that ADR-0001 … ADR-0005 have to stay readable in.
- **Questions raised:** none. Nothing was re-addressed to the human.
- **Commands:**
  - `python3 -c "print(27*9)"` → `243`, the arithmetic that settles the contradiction
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → rewrote the board; `## Open questions`
    is `_None._` again
  - `python3 -m unittest discover` → exit 0, `Ran 46 tests`, `OK` — confirming the correction
    needed no code change
- **Gates:**
  - `answer-is-propagated` (hard) → **pass** — every file named in `## Consequences` was opened
    and changed: `item.md` (AC10's example rewritten; a `## Notes` paragraph added),
    `artifacts/plan.md` (the AC10 row of the mapping table rewritten to the corrected fixture and
    all three tests), `questions/Q-001.md` (answer, basis, rejected options, consequences). The
    two files listed as deliberately unchanged are named as such, with the reason
  - `answered-from-the-record` (hard) → **pass** — the answer quotes refinement Q6 and the
    human's confirmation of it, plus the arithmetic that makes the old example impossible. No
    part of it rests on preference
  - `escalation-is-justified` (hard) → **pass, vacuously** — nothing was escalated, and the entry
    above states which of the four conditions were tested and why none applies
  - `workspace-valid` (hard) → **pass** — `validate-workspace` exit 0 after the board was
    regenerated
  - `item-resumed-correctly` (hard) → **pass** — not applicable and recorded as such: the
    question was non-blocking, the item was never suspended, no history row carries a `resume-to`
    for it, and WI-0002 stays at `verifying`
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md` — `status: answered`, `answered-by:
    answer-questions`, with `## Answer` and `## Consequences` filled in
  - `tracker/items/WI-0002/item.md` — AC10's worked example corrected; `## Notes` records the
    amendment and its basis
  - `tracker/items/WI-0002/artifacts/plan.md` — the AC10 mapping row rewritten
  - `tracker/board.md` regenerated; `tracker/items/WI-0002/journal.md` (this entry)
  - no ADR, no document version bump, no history row, no code change
- **Status:** `verifying` → `verifying` (unchanged, and correctly so)
- **Result:** Q-001 is answered from the human's own recorded words: AC10's rule stands, its
  impossible worked example is replaced by a folder that exists, and the correction is written
  into the criterion, the item's notes and the plan rather than left inside the question. WI-0002
  continues at `verifying` with a criterion a verifier can now actually build.

## 2026-08-17T00:32:00Z — verify v0.1.1 — qa-engineer

- **Item:** WI-0002
- **Trigger:** status `verifying`, dispatched by `next` — after `answer-questions` closed Q-001,
  so AC10 was read in its corrected form
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the eleven criteria, read **first** and used to derive what
    would settle each one before the implementation report was opened
  - `history.md`, `artifacts/plan.md`, `artifacts/refinement-qa.md`, `questions/Q-001.md`
    (answered), then `artifacts/impl-report.md` — read last, and treated as claims to check
  - `tracker/items/WI-0001/item.md` (AC1, AC2, AC3, AC10 — what AC4 makes binding) and the code
    WI-0001 shipped, extracted with `git show 461e37f:linecount.py`
  - `docs/architecture/adr/ADR-0001` … `ADR-0005`, `docs/architecture/overview.md` (v2)
  - the code on `wi/WI-0002` at `b2d851c` (last code commit `abc7c66`) and
    `git diff main..wi/WI-0002`
- **Decisions:**
  - **Checked AC4 against the binary WI-0001 delivered, not against today's tests.** "Byte-
    identical to what WI-0001 delivered" is a claim about two programs, so I ran both over the
    same four folders and three failure paths and compared with `cmp`. A test asserting today's
    bytes would have proved nothing about the past, and the implementation report could not have
    supplied this evidence.
  - **Recorded the one divergence AC4 does not cover, rather than passing it silently.** With no
    argument at all, stderr changed: `usage: linecount [-h] folder` → `usage: linecount [-h]
    [--top N] folder`. AC4's byte-identity is stated "on the same folder", and this invocation
    has none; WI-0001 AC12 requires only "a message on stderr" and exit 2, both of which hold;
    and any implementation of this item changes that line, since a usage string that hid the new
    flag would be wrong. So: **pass**, with the divergence named in the report's AC4 row and
    again under `## Not verified, and why`, because it is the one observable difference in
    behaviour WI-0001 delivered and `review-close` should see it without hunting.
  - **Used the corrected AC10 example and checked its arithmetic before building it** (26×46+8 =
    1204 over 27 files). The criterion is now buildable, which was the point of Q-001; the
    fixture produced the stated three lines byte for byte.
  - **Exercised two failure values no criterion names** — `--top 3.5` and `--top ""` — because
    AC7's "not a whole number" is a class, not two examples. Both behave exactly as `abc` does.
  - **Exercised the `--top`/ADR-0002 interaction the implementation report declared untested**: a
    `chmod 000` file inside the folder is in neither M nor the total, and the run still exits 0
    with the stderr line. That matches the plan's assumption 3 and AC3's own definition of M, so
    it is an observation, not a defect — recorded rather than filed.
  - **Classification: nothing to route.** No criterion failed, so no send-back; no behaviour
    delivered by another item is broken — WI-0001's output is byte-identical on every folder
    tested — so no bug item.
  - **Nothing judged `ambiguous`**, and no question filed. The one criterion that was ambiguous in
    the earlier sense — AC10 — had already been corrected through Q-001 before this execution
    began, which is the protocol working as intended.
- **Questions raised:** none
- **Commands:** (fixtures under `/tmp/verify-wi0002-fJiq/`, built by this execution)
  - `git rev-parse HEAD` → `b2d851c665e3ee33b1df3cb559e0a43b325870b5`; `git status --porcelain` →
    no modified tracked file
  - `python3 -m unittest discover` → exit 0, `Ran 46 tests in 1.146s`, `OK`
  - AC1: `--top 3` on five files → ` 9  a.txt` / ` 7  b.txt` / ` 5  c.txt` / `25  total (all 5
    files)`, stderr 0 bytes, exit 0
  - AC2: the criterion's fixture → ` 9  big.txt` / ` 5  a.md` / ` 5  b.md` / `24  total (all 4
    files)`; `grep -c c.md` → 0
  - AC3: 27 files summing 1204 → last line `1204  total (all 27 files)`; the same folder without
    the flag prints 28 lines and `1204  total`
  - AC4: `git show 461e37f:linecount.py` then old-vs-new over four folders → stdout, stderr and
    exit codes identical in every case; missing path and regular-file paths identical, exit 2/2;
    no-argument case **DIFFERENT** (the usage line), exit 2/2
  - AC5: `--top 99` on three files → all three rows, `9  total (all 3 files)`, exit 0
  - AC6: `--top 0` on two files → stdout exactly `8  total (all 2 files)`, stderr 0 bytes, exit 0
  - AC7: `--top -1`, `abc`, `3.5`, `""` → each stdout 0 bytes, stderr exactly 1 line, exit 2
  - AC8: `--top 1 $F` vs `$F --top 1` → `cmp` identical on stdout and stderr, exits 0/0; `-t 1` →
    stdout 0 bytes, argparse's message, exit 2
  - AC9: empty folder with N = 0, 3, 99 and a folder of only subdirectories → `no files`, stderr
    0 bytes, exit 0 every time
  - AC10: the corrected fixture → `  46  f00.txt` / `  46  f01.txt` / `1204  total (all 27 files)`
  - AC11: `git clone -q --branch wi/WI-0002 . …/clone` then `python3 -m unittest discover` in the
    clone → exit 0, 46 tests
  - ADR-0002 interaction: `chmod 000` file + `--top 1` → `5  a.txt` / `9  total (all 2 files)`,
    stderr `linecount: secret.txt: Permission denied`, exit 0
  - AC4 mechanics: `git diff main..wi/WI-0002 -- tests/test_linecount.py | grep -c "^-[^-]"` → 0;
    `comm` of the old and new `def test_` names → none missing; 27 → 46 tests
  - sensitivity: `python3 /tmp/verify-wi0002-fJiq/sensitivity.py` (12 mutations) → exit 0,
    "mutations the suite did not catch: 0"; plus a thirteenth by hand (adding a `-t` alias) →
    caught by `test_ac8_no_short_form`. `git status` clean afterwards
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
- **Gates:**
  - `tests-pass` (hard) → **pass** — 46 tests, exit 0, run here on the branch head and again in a
    fresh clone
  - `lint-clean` (hard) → **skipped** — `{{commands.lint}}` is null (ADR-0003); checked nothing,
    not a pass, and what it leaves unchecked is in the report
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors, 0 warnings
  - `every-criterion-independently-checked` (hard) → **pass** — eleven rows, each a command run
    here with quoted output; AC4 checked against the previously shipped binary
  - `negative-cases-exercised` (hard) → **pass** — eight conditions triggered, two beyond the
    criteria, plus the ADR-0002 interaction
  - `tests-would-fail-without-the-change` (advisory) → **pass** — 13 mutations, 13 caught
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md` (new), carrying
    `Verified-commit: b2d851c665e3ee33b1df3cb559e0a43b325870b5`
  - `tracker/items/WI-0002/item.md` — all eleven criteria ticked, none without a command run here
  - no bug items; `journal.md` (this entry), `history.md` (one row)
- **Status:** `verifying` → `in-review`
- **Result:** All eleven criteria pass on `b2d851c`, decided by commands run here — including
  AC4 against the binary WI-0001 actually shipped, and AC10 against the example Q-001 made
  buildable. Thirteen mutations of the new behaviour were all caught. One divergence is recorded
  for the reviewer: the usage line now advertises `[--top N]`, so the no-argument message is not
  byte-identical to WI-0001's — outside AC4's scope, unavoidable, and named rather than smoothed.

## 2026-08-17T00:40:30Z — review-close v0.1.1 — reviewer

- **Item:** WI-0002
- **Trigger:** status `in-review`, dispatched by `next`
- **Inputs read:**
  - `item.md` (eleven criteria, `## Out of scope`, `## Notes`), `history.md` (six rows, checked
    against `pipeline.yaml`), `journal.md` (all six entries, in full)
  - `artifacts/plan.md`, `impl-report.md`, `verify-report.md`, `refinement-qa.md`,
    `questions/Q-001.md` — and the three files its `## Consequences` names, opened to confirm the
    changes are actually in them
  - `docs/architecture/overview.md` v2, `ADR-0004`, `ADR-0005`, `ADR-0001` … `ADR-0003`,
    `docs/product/vision.md` v1
  - the diff `main..wi/WI-0002` for `linecount.py` and `tests/`, hunk by hunk, plus
    `git log main..wi/WI-0002` and `git diff --name-only b2d851c..wi/WI-0002`
- **Decisions:**
  - **Accepted.** Every hunk maps to a plan step and a criterion (the table is in `review.md`);
    no ADR is contradicted; nothing from `## Out of scope` appears in the code.
  - **Accepted the usage-line divergence as a recorded gap, not a defect.** `verify` found that
    the no-argument stderr changed from `usage: linecount [-h] folder` to `usage: linecount [-h]
    [--top N] folder`. AC4's byte-identity is stated "on the same folder"; WI-0001 AC12 asks only
    for a message on stderr and exit 2, both of which hold; and no implementation of `--top`
    could leave that line unchanged without misdescribing the interface. Sending the item back
    would have asked for something impossible. It is now in `item.md`'s `## Notes`, because a gap
    that lives only in a verification report is invisible the moment the item closes.
  - **Did not send back for findings 2–4** (the `None` sentinel's two meanings, two error styles
    on stderr, `int()`'s permissiveness). Each is recorded in an ADR or an assumption, each is
    reversible in one function, and none contradicts a criterion.
  - **Closed before merging, then fast-forwarded.** `check-commit-refs` counts commits on
    `main..wi/WI-0002` and fails an empty range as "nothing was delivered", so merging first
    would have made that gate fail for a change that had just been delivered correctly. The merge
    result was proved beforehand on a throwaway branch — tree-identical to the branch head, 46
    tests green — so nothing rests on the order.
  - **Closed `EP-001` in the same execution**, this being its last child not `done`. The epic
    Definition of Done is applied criterion by criterion in the **epic's** journal entry, where a
    reader looking at the epic will find it, with one gap named: `docs/product/vision.md` never
    mentions `--top`, and this skill may not edit it.
  - **Filed no bug item and no question.** Nothing found belongs to another item, and nothing
    required a decision that was not already recorded.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002` → exit 0,
    "verified at b2d851c6; … only the record changed (5 file(s) under tracker/ or docs/)"
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, 4 of 4
  - `git branch tmp/merge-check main; git merge --no-ff wi/WI-0002` → `git diff --stat
    wi/WI-0002 HEAD` empty; `python3 -m unittest discover` → exit 0, 46 tests; branch deleted
  - `git diff main..wi/WI-0002 --stat -- linecount.py tests/` → +69/−11 and +180/−0
  - `python3 -m unittest discover` → exit 0, `Ran 46 tests`, `OK`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 … transition WI-0002 --to done --actor review-close --outcome delivered` → applied
  - `git checkout main && git merge --ff-only wi/WI-0002`; `python3 -m unittest discover` on
    `main` → exit 0, 46 tests
- **Gates:**
  - `definition-of-done` (hard) → **pass** — D1–D11 each with its own result and evidence in
    `review.md` `## Definition of Done`
  - `verification-postdates-the-code` (hard) → **pass** — exit 0; the commits after the verified
    sha touch only `tracker/`
  - `commits-reference-the-item` (hard) → **pass** — 4 of 4
  - `tests-pass-on-the-merge-result` (hard) → **pass** — 46 tests, exit 0, on the proved merge
    result before the trunk moved, and again on `main` after the fast-forward
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors, 0 warnings
  - `record-is-reconstructible` (hard) → **pass** — from `tracker/`, `docs/` and `git log` alone:
    *what was built and why* (`item.md`, `plan.md`, four commits); *which skill decided what*
    (six journal entries with personas, and `history.md`'s actor column); *what questions arose
    and how they were resolved* (six at refinement verbatim, then `Q-001` with its answer, its
    basis in refinement Q6 and its three propagated files); *what verification found* (eleven
    criteria with quoted output, thirteen mutations, the usage-line divergence, five declared
    gaps)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/review.md` (new)
  - `tracker/items/WI-0002/item.md` — `status: done`, `outcome: delivered`, five accepted gaps
    added to `## Notes`
  - `main` fast-forwarded from `4825e16` to the branch head; `tracker/board.md` regenerated
  - `tracker/items/EP-001/item.md` — closed, and `tracker/items/EP-001/journal.md` — the epic
    closure entry with the epic Definition of Done
  - `journal.md` (this entry), `history.md` (one row: `in-review → done`)
- **Status:** `in-review` → `done` (outcome `delivered`)
- **Result:** `--top N` is delivered and merged. Eleven criteria independently demonstrated, two
  ADRs for the decisions the criteria forced, one question raised and answered inside the record,
  and one honest behaviour difference — the usage line — accepted and written into the item
  rather than left in a report. EP-001 closes with it.

## 2026-08-17T01:30:00Z — verify v0.1.1 — qa-engineer

- **Item:** WI-0002
- **Trigger:** not a dispatched execution. The item is `done` and merged; this is an independent
  regression pass over the merged trunk, judging what is on `main` against this item's criteria.
  No status was changed and no history row was appended.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the eleven criteria, read in full **before** any report,
    including AC10 as corrected by `answer-questions` for `Q-001`, and the five accepted gaps
  - `tracker/items/WI-0001/item.md` — the thirteen criteria AC4 promises to leave alone
  - `tracker/items/EP-001/item.md` — `## Success measures`
  - `docs/architecture/adr/ADR-0004`, `ADR-0005`, and `ADR-0001` to `ADR-0003`;
    `docs/architecture/overview.md` v2; `docs/product/vision.md` v1
  - `tracker/project.yaml`
  - the code on `main` at `6d1e437b4293571296809b322c47fb0dc83d1ad6`, and
    `git show 5adc619:linecount.py` — the WI-0001 build, used as the reference for AC4
  - `artifacts/plan.md`, `artifacts/impl-report.md`, `artifacts/verify-report.md`,
    `artifacts/review.md`, `questions/Q-001.md` — read **after** the criteria and after the
    fixtures were built, and cited as evidence for nothing
- **Decisions:**
  - **AC4 checked by running both binaries, not by reading the diff.** `git show
    5adc619:linecount.py` was extracted and run beside `linecount.py` on eight folders — the
    tie folder, the counting-rule folder, the symlink/dotfile folder, the PNG folder, an empty
    folder, the 27-file folder and both unreadable-file folders — plus the missing-path and
    regular-file error paths. All ten byte-identical on stdout, stderr and exit code. The usage
    line with no argument differs, which the item already records as an accepted gap; this pass
    confirms it and finds nothing else.
  - **AC10 verified against the corrected example, and the correction re-derived.** The 27-file
    folder of `Q-001` (26 files of 46 lines plus `small.txt` of 8) sums to 1204, and `--top 2`
    prints `··46··f00.txt`, `··46··f01.txt`, `1204··total (all 27 files)`. The arithmetic of the
    superseded example was checked independently: 27 files whose two largest hold 9 and 7 lines
    cannot sum to 1204, so the correction was necessary and the rule it preserved is intact.
  - **No defect attributed to this item.** All three defects filed by this pass reproduce
    identically against the WI-0001 build at `5adc619`, so `--top` neither caused nor worsened
    any of them. `main`'s `if top is None or not rows` short-circuit inherits BUG-0002's
    behaviour rather than creating it, which is why `found-in` names WI-0001.
  - **The `(all M files)` count is an observation, not a defect.** With one file skipped under
    ADR-0002, `--top 5` on a two-file folder prints `3  total (all 1 files)`. AC3 defines M twice
    in one sentence — "the number of files in the folder — that is, the number of rows the same
    command would print without `--top`" — and a skipped file makes the halves disagree. The
    implementation follows the second, which is the operative gloss, so the record settles it;
    no question filed. Recorded in `BUG-0002` `## Notes` so whoever fixes the skip behaviour sees
    that it moves M.
  - **ADR-0004's and ADR-0001's stated consequences were exercised rather than assumed.**
    `--top 3_0` → 30, `--top ' 3 '` → 3, `--top +2` → two rows, `--top=2` and the abbreviation
    `--to 2` both accepted. Each is predicted by its ADR and forbidden by no criterion, so each
    is recorded as a pass of the ADR rather than as a finding.
- **Questions raised:** `EP-001/Q-001` (non-blocking, to architect) — filed once for this pass;
  see the WI-0001 entry of the same timestamp. Nothing about this item's criteria is ambiguous.
- **Commands:**
  - `python3 -m unittest discover` (repo root) → exit 0, `Ran 46 tests`, `OK`
  - AC1: `python3 linecount.py --top 3 /tmp/qa-lc9/f27` → `  46  f00.txt` / `  46  f01.txt` /
    `  46  f02.txt` / `1204  total (all 27 files)`, exit 0
  - AC2: `python3 linecount.py --top 3 /tmp/qa-lc9/tie` (`big.txt` 9; `a.md`,`b.md`,`c.md` 5) →
    ` 9  big.txt` / ` 5  a.md` / ` 5  b.md` / `24  total (all 4 files)` — no row for `c.md`
  - AC4: `git show 5adc619:linecount.py > /tmp/qa-lc10/lc_wi1.py`, then both run on 8 folders and
    2 error paths, `diff` on stdout and stderr and the exit codes compared → `IDENTICAL` ×10
  - AC5: `python3 linecount.py --top 99 /tmp/qa-lc9/tie` → all four rows +
    `24  total (all 4 files)`, exit 0
  - AC6: `python3 linecount.py --top 0 /tmp/qa-lc9/tie` → `24  total (all 4 files)` alone, exit 0
  - AC7: `--top -1` → `linecount: --top: -1 is negative`; `--top abc` → `linecount: --top: 'abc'
    is not a whole number`; `--top 3.5` and `--top ''` likewise — one line each, stdout empty,
    exit 2
  - AC8: `--top 3 <folder>` vs `<folder> --top 3` → `diff` empty on both streams, exits 0/0;
    `-t 3 <folder>` → `usage: linecount [-h] [--top N] folder` + `linecount: error: unrecognized
    arguments: -t /tmp/qa-lc7/tie`, stdout empty, exit 2
  - AC9: empty folder with `--top 0`, `--top 3`, `--top 99` → `no files$` (via `cat -A`), stderr
    empty, exit 0, all three
  - AC10: `python3 linecount.py --top 2 /tmp/qa-lc9/f27 | cat -A` → `  46  f00.txt$` /
    `  46  f01.txt$` / `1204  total (all 27 files)$`
  - AC3 singular label: `python3 linecount.py --top 1 /tmp/qa-lc9/one` → `3  total (all 1 files)`,
    as this item's own assumption predicts
  - ADR consequences: `--top 3_0`, `--top ' 3 '`, `--top +2`, `--top=2`, `--to 2`,
    `--top 100000000000000000000` → each exit 0 with the predicted output
  - 13 mutations of `linecount.py`, `python3 -m unittest discover` after each → all 13 FAILED;
    the four aimed at this item (`--top` negative check removed, the `(all M files)` label
    reduced to `total`, the `rows[:top]` slice ignored, the column width computed without the
    total) failed with 2, 8, 7 and 9 failures
  - `.claude/agile-skills/scripts/validate-workspace` → exit 1, one error remaining
- **Gates:**
  - `tests-pass` (hard) → **pass** — exit 0, 46 tests
  - `lint-clean` (hard) → **skipped** — `commands.lint` is `null` by ADR-0003; no command exists.
    Never recorded as passed
  - `workspace-valid` (hard) → **fail** — exit 1, `epic.closed-with-open-children` on EP-001,
    caused by filing the bugs this skill is required to file; `EP-001/Q-001` raised
  - `every-criterion-independently-checked` (hard) → **pass** — all eleven criteria have a
    command and quoted output in `EP-001/artifacts/regression-verify-report.md`
  - `negative-cases-exercised` (hard) → **pass** — AC6 (`--top 0`), AC7 (four bad values plus
    `--top` with no value), AC8 (`-t`), AC9 (empty folder × three N) all triggered on disk
  - `tests-would-fail-without-the-change` (advisory) → **pass** — 13 mutations, 13 suite failures
- **Artifacts:**
  - `tracker/items/EP-001/artifacts/regression-verify-report.md` (new)
  - `tracker/items/BUG-0001/`, `BUG-0002/`, `BUG-0003/` (new; none `found-in: WI-0002`)
  - `tracker/items/EP-001/questions/Q-001.md` (new)
  - `tracker/board.md` regenerated; `journal.md` (this entry). No history row, no code change
- **Status:** `done` → `done` (unchanged — an independent regression pass changes no status)
- **Result:** All eleven criteria reproduced independently on the merged trunk, including AC4's
  byte-identity against the binary WI-0001 shipped and AC10's corrected worked example. Nothing
  found in this pass is `--top`'s: the three defects filed all predate it and reproduce against
  `5adc619`.
