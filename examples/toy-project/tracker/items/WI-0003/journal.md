# Journal — WI-0003

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-16T23:50:12Z — intake v0.1.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** invoked directly by the human with a new request against the delivered tool; this
  execution created the item
- **Inputs read:** the human's request and his six answers, in this session; `EP-001/item.md` and
  `history.md`; `WI-0001/item.md` and `WI-0002/item.md` (the delivered order, the `--top`
  precedent and its `-t` rejection); `linecount.py`; `docs/product/vision.md` (v1)
- **Decisions:** see EP-001's entry of the same timestamp for why the work was not split and why
  it sits under the reopened epic. Local to this item: six criteria were written from answers the
  human gave in as many words, and three points he did not settle were left out of the criteria
  and written into `## Notes` as open — the `--top` interaction he declined to decide, the
  failure shape of a bad or missing `--sort` value, and whether the test-command criterion
  applies. `priority: medium` is the analyst's, not his; there is only one open item, so nothing
  is ordered by it.
- **Questions raised:** none filed as artifacts — the human was present and answered directly.
  His six answers are verbatim in `EP-001/journal.md` under this timestamp. Three points remain
  open for `refine`, listed in this item's `## Notes`.
- **Commands:** `new-item --id WI-0003 --type work-item --title … --epic EP-001 --priority medium
  --status draft --actor intake` → exit 0
- **Gates:** `workspace-valid` → **pass** (`validate-workspace .` exits 0 once this entry exists;
  it reported `journal.execution.missing` on this file until then). `epic-has-success-measures` →
  **pass**, evidence on EP-001. `items-are-separable` (advisory) → **pass**: nothing in
  `depends-on`, both prior items `done`, buildable now. `no-solution-in-the-problem` (advisory) →
  **pass**: `--sort`, `name`, `count` and byte order are all the human's words.
- **Artifacts:** `tracker/items/WI-0003/item.md`, `journal.md`, `history.md` (all new)
- **Status:** `—` → `draft`
- **Result:** Drafted with what he actually said and with three named gaps. Not Ready: `refine`
  owns those three, and `verify` will have to decide them from this item alone.

## 2026-08-16T23:58:00Z — refine v0.1.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`; invoked directly by the human in the same session as intake, not
  dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0003/item.md`, `history.md` (one row, `— → draft`: a fresh draft, not an
    item sent back from a later stage), `journal.md` (intake's entry and its three open points)
  - `tracker/items/EP-001/journal.md` — the six intake answers, verbatim, so none was re-asked
  - `tracker/items/WI-0002/item.md` and `artifacts/refinement-qa.md` — the `--top` precedents for
    the failure shape, the flag position, the `-t` rejection and the analyst-derived test
    criterion; `WI-0001/item.md` for the row format, the sort key and the empty-folder answer
  - `docs/architecture/adr/ADR-0004-rejecting-a-bad-top-value.md` — why `--top`'s value is
    hand-checked rather than left to argparse, which is the precedent AC7 follows
  - `docs/product/vision.md` (v2) — checked for conflict; none. The vision already describes
    `--sort` as being added and not delivered
  - `linecount.py` — `parse_args`, `parse_top`, the sort key and `format_report`'s `label`, so the
    criteria describe the tool that exists
  - `tests/test_linecount.py` — checked whether any of the 60 tests asserts the usage or help
    text, because AC4 claims they pass unmodified. None does; the claim holds
  - `.claude/agile-skills/spec/dor-dod.md` §1, `work-item.md`, `journal-and-history.md`
- **Decisions:**
  - **AC2 rewritten from a feeling into a procedure.** Intake's version ended "can be compared row
    for row by eye", which `verify` cannot decide. It now names two folders, three filenames, the
    required order and the fact that the counts differ between them. The human confirmed it is the
    same measure: "it's the same thing, just written so someone else can run it."
  - **The absent-file case is an exclusion, not a feature.** He said a missing row is the signal
    and "don't add anything special for it", so it is written into `## Out of scope` — a later
    reader could otherwise reasonably assume the tool should mark or pad the gap.
  - **AC7 split in two, on his instruction.** A bad *value* gets our one-line message (ADR-0004's
    reasoning, and WI-0002 AC7's exact failure shape); a *missing* value stays argparse's usage
    block. The split keeps the message we control to one line without re-implementing what
    argparse already does correctly.
  - **AC4 carries its own exception.** The usage and help text will change, exactly as `--top`
    changed it; WI-0002 discovered that at review and recorded it as an accepted gap. Putting it
    in the criterion before any code exists is the cheap version of the same honesty. He agreed in
    those terms: "I'd rather the criterion be true than tidy."
  - **AC9 written, and written to decide nothing.** The human refused to settle what
    `--top N --sort name` selects *and* refused to have an assumption recorded in his name. Both
    readings nevertheless agree on the shape of the output — at most N rows, exit 0, WI-0002 AC3's
    labelled total — so AC9 fixes that and only that. It passes under either reading, so it takes
    nothing away from "leave it genuinely open", and it stops the one combination nobody has
    specified from shipping as a traceback. Flagged as analyst-derived in its own text, in
    `## Notes`, and in the Q&A; he was not asked, because he had just asked not to be held up.
  - **No override recorded, though he offered one.** Reasoning in full in the Q&A's closing
    section and summarised under the DoR gate below. In short: nothing in §1 is unmet, the override
    record requires naming the criteria that were not met, and naming one would be false.
  - **The undefined combination was written as instructions to the downstream skills**, not just
    as a note. `## Notes` tells `plan` and `implement` not to file a question about it — he was
    asked and chose to leave it unconstrained, so escalating to the architect would get it decided
    by someone other than him — and tells `verify` that its own observation of the behaviour is
    not a contract. Without that, the most likely outcome is a question artifact that routes the
    decision around him, which is the specific thing he objected to.
- **Questions raised:** six, asked in one batch, all answered. Five settled; Q2 recorded
  `[unresolved]` and carried into `## Notes` as a risk. A seventh point (AC9) was not asked and is
  tagged `[assumed]`. Full text, verbatim and tagged, in `artifacts/refinement-qa.md`. No question
  artifact was filed — the human was present throughout.
- **Commands:**
  - `grep -n "usage\|--help" tests/test_linecount.py` → no matches; 60 tests, none asserting the
    usage or help text (evidence for AC4's "pass unmodified")
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to ready --actor refine …` → see
    Status
- **Gates:**
  - `workspace-valid` (hard) → **pass** — `validate-workspace .` exits 0 (7 items, 10 documents,
    0 errors, 0 warnings) with the refined item, the Q&A artifact and this entry in place.
  - `definition-of-ready` (hard) → **pass**, criterion by criterion against `spec/dor-dod.md` §1:
    - **R1 pass** [auto] — `id`, `type: work-item`, `title`, `status`, `priority: medium`,
      `epic: EP-001`, `created`, `updated` all present and valid; `validate-workspace` exits 0.
    - **R2 pass** [skill] — role "someone who keeps two folders that are meant to hold the same
      set of notes", capability "list a folder's files in filename order instead of largest-first",
      outcome "so that the two listings come out in the same order and I can see by eye whether
      the same files are present in both". The outcome is his, from intake Q1.
    - **R3 pass** [auto] — ten criteria, `AC1`–`AC10`, each an unticked markdown checkbox.
    - **R4 pass** [skill] — every criterion names a command and an observable result; the evidence
      per criterion is under `criteria-are-decidable` below. No unmeasurable adjective survives:
      "by eye" was removed from AC2 at this refinement, and the only judgement words left ("not a
      regression" in AC4, "deliberately not decided" in AC9) are scoping statements about what the
      criterion does *not* require, not thresholds a verifier has to guess.
    - **R5 pass** [skill] — `## Out of scope` names nine exclusions, of which at least three are
      things a reader could reasonably assume were included: a descending name order, marking a
      filename absent from the other folder, and deciding the `--top` interaction.
    - **R6 pass** [auto] — `questions/` is empty; no open question of any kind on this item, so
      none is blocking.
    - **R7 pass** [auto] — no `depends-on`; WI-0001 and WI-0002 are both `done`, so nothing
      unfinished is depended on and the item can be built immediately.
    - **R8 pass** [auto] — `artifacts/refinement-qa.md` holds all six questions and all six
      answers verbatim, plus the unasked seventh, each tagged `[human — simulated by the builder]`,
      `[assumed]` or `[unresolved]`.
    - **R9 pass** [skill] — one flag, one code path, one coherent change to `linecount.py` plus its
      tests. Nothing here is separable: a `--sort` accepting `name` but not `count` would be half
      an interface and would deliver nothing observable on its own.
    - **On the override he offered:** since R1–R9 all pass, there is nothing to override. The
      override procedure in §1 requires naming the unmet criteria; no criterion is unmet, so a
      `DoR overridden:` history row would assert something false and would devalue every genuine
      override in this repository. What he was protecting against — an analyst's guess recorded as
      his decision — was honoured instead by leaving the combination genuinely undecided. The
      history reason for this transition therefore does **not** begin `DoR overridden:`, and the
      Q&A carries his offer verbatim so a reader can check that judgement rather than take it.
  - `criteria-are-decidable` (hard) → **pass**. Per criterion, the observation and the verdict:
    - **AC1** — build the three-file folder named in the criterion, run
      `python3 linecount.py --sort name <folder>`; the three rows must appear as `Zebra.md`,
      `apple.md`, `notes.md`, then the `total` row; exit 0. Any other order fails it.
    - **AC2** — build folders `A` and `B` as named, run the two commands, compare the filename
      column of each; both must read `ideas.md`, `notes.md`, `todo.md`.
    - **AC3** — run `--sort count <folder>` and `<folder>` on the same folder, diff stdout, stderr
      and the exit codes; any byte of difference fails it.
    - **AC4** — run the WI-0001/WI-0002/BUG-000* suites unmodified (`python3 -m unittest
      discover`) and diff today's binary against the new one on the same folder for an invocation
      that names a folder; the usage/help text is excluded by the criterion's own words.
    - **AC5** — `python3 linecount.py -s name <folder>`: stdout empty, stderr non-empty, exit 2.
    - **AC6** — an empty folder with each of `--sort name` and `--sort count`: stdout exactly
      `no files\n`, stderr empty, exit 0.
    - **AC7** — `--sort size <folder>`: stdout empty, stderr exactly one line starting
      `linecount: --sort: `, exit 2. `--sort` with the value missing: stdout empty, stderr carries
      argparse's usage block, exit 2.
    - **AC8** — run the three spellings, diff their stdout, stderr and exit codes pairwise.
    - **AC9** — a folder of at least three files with `--top 2 --sort name`: exit 0, at most two
      file rows, last row matching `total (all M files)`. The verdict does not depend on which two
      files appear, which is the point.
    - **AC10** — `python3 -m unittest discover` from the repository root: exit 0, and the new
      tests are present in `tests/`.
  - `qa-recorded-verbatim` (hard) → **pass** — `artifacts/refinement-qa.md` reproduces every
    question as it was asked and every answer as it was given, including the answer that refuses
    the analyst's proposal (Q2) and the one that corrects it (Q1). Nothing was paraphrased into
    agreement; Q2's answer is recorded as a refusal of both the question and the fallback, which is
    what it was.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0003/item.md` — AC1–AC6 rewritten and AC7–AC10 added; three exclusions added
    to `## Out of scope`; `## Notes` rewritten around what was settled, what is deliberately
    undefined, and why no override was recorded
  - `tracker/board.md` regenerated by the transition
  - commit `tracker: the refined item and its Q&A record (refs WI-0003)`
- **Status:** `draft` → `ready`
- **Result:** Ready, with ten criteria a stranger with a terminal could settle and one flag
  combination deliberately left unspecified at the human's explicit instruction — recorded as
  unresolved, not as an assumption in his name, and carried in `## Notes` with instructions for
  every skill that will meet it. `plan` is next.

## 2026-08-17T00:06:00Z — plan v0.1.1 — architect

- **Item:** WI-0003
- **Trigger:** status `ready`, dispatched by `next` (the only runnable item; every other item is
  `done`)
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — AC1–AC10, `## Out of scope`, `## Notes`
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — in particular Q2 `[unresolved]` and Q7
    `[assumed]`, which are this design's soft ground, and Q3 for the failure shape
  - `tracker/items/WI-0003/history.md` — two rows, `— → draft → ready`; a first plan, not a re-plan
  - `docs/architecture/overview.md` v4 — the function table and the three-`OSError` boundary
  - `docs/architecture/adr/`: **ADR-0001** (argparse owns the command line), **ADR-0003** (no lint
    command exists or may be added), **ADR-0004** (hand-validate a flag value so the message is one
    line), **ADR-0005** (`format_report` keeps its signature), **ADR-0008** (the report is written
    as bytes). ADR-0002, ADR-0006 and ADR-0007 were read for the `OSError` boundaries and are
    untouched by this change
  - `tracker/project.yaml` — `commands.test` already set, `commands.lint` null with ADR-0003
  - `linecount.py` in full — `parse_args`, `parse_top`, `list_files`, `count_lines`,
    `format_report`, `main`, and specifically the single `rows.sort(...)` call and the `rows[:top]`
    slice this change lives next to
  - `tests/test_linecount.py` — the two-layer style, the `run(*args)` and `write(...)` helpers, the
    `test_ac<n>_*` naming, and the class-per-item convention. Also grepped for `usage` and
    `--help`: no matches, which is the evidence AC4's exception is safe
- **Decisions:** by the preference order in the procedure — documented first, then reversible
  assumption, and the human not asked at all.
  - **Hand-validate `--sort`'s value; no `choices=`. [documented]** ADR-0004 decided this exact
    question for `--top`: argparse's rejection is a usage block plus a message, which is two lines,
    and AC7 asks for one. No new ADR — the decision exists, its reasoning transfers unchanged, and
    a second ADR restating the first devalues the trail (`spec/doc-header.md` §4: do not write an
    ADR for a choice with no alternative worth naming *here*).
  - **`default="count"` rather than `None`. [assumed, trivial]** It removes the `None` branch from
    `main`, which is what makes AC3 (spelling out the default is byte-identical) fall out of the
    design instead of being special-cased.
  - **A new `sort_rows(rows, order)` rather than a key expression inline in `main`. [documented]**
    The overview's stated shape is a pipeline of pure-ish steps behind a thin `main`, with the
    arithmetic isolated for unit testing; the tie-break is arithmetic of exactly that kind. It also
    puts "count descending, then name ascending" in one place rather than two.
  - **Names compare as `os.fsencode`d bytes in both orders. [documented]** ADR-0008 made the output
    side byte-oriented so an undecodable name cannot abort the report; ordering is the same choice
    applied to comparison, and AC1 states it as a criterion.
  - **The `--top` slice is not touched, and the combination stays unspecified. [ADR-0009]** The
    item's `## Notes` forbid escalating this, and that instruction is the human's recorded choice,
    so no question was filed. The design adds no code to make the combination come out either way;
    ADR-0009 records the four options, the fact that today's code therefore selects the
    alphabetically-first N as a *consequence* rather than a decision, and that reaching the other
    reading later is one line.
  - **Four reversible assumptions recorded in the plan** rather than escalated: case sensitivity of
    the value, which message wins when `--top` and `--sort` are both invalid, the exact rejection
    wording, and `sort_rows` returning a new list. Each names what reversing it costs; none touches
    an interface a test asserts.
  - **`project.yaml` unchanged.** `commands.test` is `python3 -m unittest discover`, which step 8
    of the plan runs; `commands.lint` stays null because ADR-0003 records why the project has no
    linter. That is the "or an ADR records why the project has none" branch of the gate, not a
    silent omission.
- **Questions raised:** none. No decision here was irreversible or turned on intent no document
  records — the two candidates were both already decided (ADR-0004, ADR-0008), and the one genuine
  unknown is under a standing instruction from the human not to ask about it. No human was present
  in this run in any case; had a question been needed it would have been filed as an artifact, not
  asked.
- **Commands:**
  - `grep -n "^class \|^    def test" tests/test_linecount.py` → 60 tests, class-per-item layout
  - `grep -n "usage\|--help" tests/test_linecount.py` → no matches (evidence for AC4's exception)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
- **Gates:**
  - `workspace-valid` (hard) → **pass** — `validate-workspace .` exits 0 with the plan, ADR-0009,
    the overview at v5 and this entry in place.
  - `every-criterion-is-addressed` (hard) → **pass** — the `## Acceptance criteria mapping` table
    in `plan.md` carries one row per criterion, AC1 through AC10, each naming the plan step that
    satisfies it and the specific named test that will demonstrate it. No AC is without a step; no
    step exists that no AC maps to (the mechanical check the procedure prescribes: deleting any
    step would break a mapping row).
  - `project-commands-resolved` (hard) → **pass** — `commands.test: python3 -m unittest discover`
    is a real command in this repository and is the one the plan runs at step 8; `commands.lint` is
    null and **ADR-0003** records why the project has and may have no linter, which is the branch
    this gate explicitly allows. The `lint-clean` gate downstream will therefore report `skipped`,
    honestly, rather than a pass for a command nobody runs.
  - `decisions-recorded` (hard) → **pass** — every choice this plan makes appears in
    `## Decisions and ADRs` pointing at ADR-0001, ADR-0003, ADR-0004, ADR-0008 or the new ADR-0009,
    or in `## Assumptions` with the cost of reversing it stated. Four assumptions, four reversal
    procedures, each one file.
  - `plan-is-executable-without-you` (advisory) → **pass** — the eight steps name the function, the
    file, the position in the file and what is true afterwards. The one place a reader could go
    wrong is step 5's position relative to the `if not rows:` branch, which is called out in
    `## Risks` precisely because it would pass a casual reading and fail AC1.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/plan.md` (new)
  - `docs/architecture/adr/ADR-0009-the-top-and-sort-combination-is-left-unspecified.md` (new)
  - `docs/architecture/overview.md` v4 → v5
  - commit `tracker: the plan, ADR-0009, and overview v5 (refs WI-0003)`
- **Status:** `ready` → `planned`
- **Result:** Designed as two new pure functions and one changed line in `main`, with the
  `--top` slice deliberately untouched. Everything the design had to decide came from an existing
  ADR or is a recorded reversible assumption; the one thing nobody may decide has an ADR saying so
  and why. `implement` can execute this without asking anything.

## 2026-08-17T00:12:00Z — implement v0.1.0 — developer

- **Item:** WI-0003
- **Trigger:** status `planned`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — AC1–AC10 and `## Notes`, including the standing instruction
    not to escalate the `--top` interaction
  - `tracker/items/WI-0003/artifacts/plan.md` — all eight steps, the mapping table, the four
    assumptions and the risks
  - `tracker/items/WI-0003/history.md` — `— → draft → ready → planned`; a fresh start, no
    send-back, no branch to reconcile with
  - `tracker/items/WI-0003/questions/` — empty
  - `docs/architecture/adr/ADR-0004` and `ADR-0008` (the two the plan leans on), `ADR-0009` (the
    unspecified combination), `ADR-0003` (why there is no lint command)
  - `tracker/project.yaml` — `branch-prefix: wi/`, `commit-subject`, `commands.test`
  - `linecount.py` and `tests/test_linecount.py` in full, for the shape to match
- **Decisions:** all inside the plan's latitude.
  - **Where the `--sort` validation goes in `main`:** after the `--top` block, which the plan's
    Assumption 2 already fixed. The comment there names the assumption so the ordering is not
    mistaken for a requirement.
  - **`row_names(stdout)` helper in the tests**, using `lstrip()` before splitting on two spaces.
    Without the `lstrip`, a narrow count in a wide column starts the line with the same two spaces
    that separate the columns, and the helper would return the count. It is used by the AC2 test,
    where the two folders have different column widths — which is exactly the case that would have
    caught it.
  - **AC2's test asserts the two stdouts differ** as well as that the name order matches.
    Otherwise the test would still pass if the tool ignored the contents entirely, and the
    criterion is about two folders whose counts differ.
  - **A five-line comment above `rows[:top]`** pointing at ADR-0009, which the plan did not name.
    ADR-0009 itself says the cost of leaving the combination unspecified falls on a reader who has
    only the code; this is the pointer that pays it. Declared under Deviations.
  - **Not updating argparse's `description` string** ("largest first"), which is now less than the
    whole truth about the interface. No criterion covers it and widening the diff for it is the
    scope creep this skill is warned about; it is in `## What I did not do` for the reviewer.
  - **Not escalating the `--top N --sort name` selection.** The item forbids it and the reason is
    the human's own. The behaviour that fell out — the N alphabetically first — is recorded as an
    observation in the report, not as a decision, and attributed to nobody.
- **Questions raised:** none.
- **Commands:**
  - `git checkout -b wi/WI-0003 main` → exit 0
  - `python3 -m unittest discover` (after each step, and last on the branch head) → exit 0,
    `Ran 77 tests in 2.305s`, `OK`
  - `git diff -U0 tests/test_linecount.py | grep -c "^-"` → `1`, the diff header alone: no line of
    the existing 60 tests was removed or changed
  - manual demonstration on a throwaway AC1 folder: default order, `--sort name`,
    `--top 2 --sort name`, `--sort size` (exit 2), `--help` — output quoted in the report
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
- **Gates:** all six, on branch head `214dc3d`:
  - `tests-pass` (hard) → **pass** — `python3 -m unittest discover`, exit 0, 77 tests.
  - `lint-clean` (hard) → **skipped**, not passed — `commands.lint` is null in `project.yaml` and
    ADR-0003 records why the project has no linter. The 63 changed lines of `linecount.py` and 172
    of tests were read by a person and by no tool. `run-gate` reported the same skip.
  - `workspace-valid` (hard) → **pass** — `validate-workspace .`, exit 0, 0 errors, 0 warnings.
  - `every-criterion-has-a-test` (hard) → **pass** — the report's table names a test function for
    each of AC1–AC10; none is demonstrated by reading code. AC4 additionally rests on the 60
    unmodified tests still passing.
  - `commits-reference-the-item` (hard) → **pass** — `check-commit-refs`: all 1 commit on
    `main..wi/WI-0003` names WI-0003.
  - `no-unplanned-scope` (advisory) → **pass** — every hunk traces to a plan step; the two that do
    not are declared under Deviations (the ADR-0009 comment and the `parse_args` docstring).
- **Artifacts:**
  - `linecount.py` (+63 lines), `tests/test_linecount.py` (+172 lines)
  - `tracker/items/WI-0003/artifacts/impl-report.md` (new)
  - branch `wi/WI-0003`, commit range `main..wi/WI-0003` = `214dc3d`
- **Status:** `planned` → `in-progress` → `verifying`
- **Result:** Built as planned, 17 tests added and none changed. Two things are handed over rather
  than hidden: the combination's incidental behaviour (the N alphabetically first, nobody's
  decision) and argparse's now-partial `description` string.

## 2026-08-17T00:20:00Z — verify v0.1.1 — qa-engineer

- **Item:** WI-0003
- **Trigger:** status `verifying`, dispatched by `next`
- **Inputs read:** in this order, deliberately — `tracker/items/WI-0003/item.md` (AC1–AC10, the
  only standard here) **before** `artifacts/impl-report.md`; then `artifacts/plan.md` (the mapping
  table and the four assumptions), `history.md`, `artifacts/refinement-qa.md` (for AC9's wording
  and the standing instruction about the combination), `docs/architecture/adr/ADR-0009` and
  `ADR-0004`, `tracker/project.yaml`, and the code on branch `wi/WI-0003` at
  **`8792e410bb27c9256e466bc77895fb7a85598131`** — the branch head, which is the state every
  verdict below refers to
- **Decisions:**
  - **No send-back and no bug.** Every criterion of this item passed, and nothing delivered by an
    earlier item was found broken. The two candidates were weighed rather than waved past: the
    `--top N --sort name` selection (no criterion fixes it, and the item forbids raising a defect
    over which reading it is — so it is an observation, recorded, not a finding) and argparse's
    `description` string still saying "largest first" (already incomplete after WI-0002, so
    pre-existing and unchanged by this item; no criterion covers it; AC4 excepts help text).
  - **AC4 was checked against the previous binary, not against the test suite alone.**
    `git show main:linecount.py` gives the tool as it was before this item, and running both on
    the same folder is the only evidence that answers the criterion's actual words. The suite
    passing proves the tests still pass; it does not by itself prove the *output* is unchanged.
  - **AC2 was given a counter-check.** Asserting that two folders come out in the same name order
    proves little unless the count order would have differed, so I ran the same two folders
    without `--sort` and confirmed `diff` exits 1. Without that, a tool that ignored the flag
    entirely could have passed my check on a badly chosen fixture.
  - **AC9 verified as shape only, on purpose**, and its observed selection written into the report
    as an observation with an explicit note that nothing may cite it as settled. Ticking AC9 while
    recording what the code actually does is exactly what the criterion asks for; judging the
    selection would have been me deciding what the human declined to decide.
  - **AC1's byte-order clause was exercised end to end** with a name that is not valid UTF-8, even
    though the item only requires the uppercase/lowercase demonstration. The unit test covers the
    rule; the criterion says "compared as bytes", and BUG-0003 is what happens when that claim is
    only checked at the unit layer.
- **Questions raised:** none. No criterion was ambiguous: AC9 is unusual in fixing a shape rather
  than a content, but it is unambiguous about what it fixes.
- **Commands:** all run against `8792e41`:
  - `git rev-parse HEAD` → `8792e410bb27c9256e466bc77895fb7a85598131`
  - `python3 -m unittest discover` → exit 0, `Ran 77 tests in 2.428s`, `OK`
  - AC1: `python3 linecount.py --sort name $F` → ` 2  Zebra.md/ 7  apple.md/ 5  notes.md/14  total`,
    exit 0, stderr 0 bytes; and the same on a folder holding `Aaa.txt`, `bad.txt`, `bad\xff.txt`
    → byte order, exit 0
  - AC2: the flag on folders `A` and `B` → identical filename columns; counter-check without the
    flag → `diff` exit 1
  - AC3: `--sort count $F` vs `$F` → `cmp` reports both streams identical
  - AC4: `git show main:linecount.py > /tmp/old_linecount.py`; old vs new on the same folder →
    `cmp` identical, both exit 0; `git diff --numstat main..HEAD -- tests/test_linecount.py` →
    `172 0`; usage lines compared old vs new → `[--top N] folder` vs `[--top N] [--sort KEY] folder`
  - AC5: `-s name $F` → exit 2, stdout 0 bytes
  - AC6: `--sort name` and `--sort count` on an empty folder → `no files\n`, stderr 0 bytes, exit 0
  - AC7: `--sort size $F` → exit 2, one line on stderr; `$F --sort` and `--sort $F` → exit 2,
    argparse's usage block, stdout 0 bytes
  - AC8: three spellings → `cmp` identical pairwise, all exit 0
  - AC9: `--top 2 --sort name $F` → exit 0, two file rows, `14  total (all 3 files)`; also
    `--top 0` and `--top 99` with `--sort name` → exit 0
  - sensitivity: three breakages applied and reverted (`sort_rows` ignoring the order → 3 failures;
    `parse_sort` never raising → 7 failures; `choices=` instead of our check → 1 failure), each
    followed by restoring the file and re-running the suite to `OK`; `git status` clean afterwards
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
- **Gates:**
  - `tests-pass` (hard) → **pass** — run here, on the branch head, exit 0, 77 tests.
  - `lint-clean` (hard) → **skipped** — `commands.lint` is null; ADR-0003 records why. Recorded in
    the report's `## Not verified, and why` as what that leaves unchecked. Never treated as a pass.
  - `workspace-valid` (hard) → **pass** — `validate-workspace .`, exit 0, 0 errors, 0 warnings.
  - `every-criterion-independently-checked` (hard) → **pass** — the report's table names, for each
    of AC1–AC10, a command this execution ran and quotes its actual output. `impl-report.md` is
    cited as evidence for nothing.
  - `negative-cases-exercised` (hard) → **pass** — six error and boundary conditions triggered:
    the rejected short form, a bad value, both missing-value spellings, the empty folder under both
    orders, `--top 0`/`--top 99` with `--sort name`, and an undecodable filename.
  - `tests-would-fail-without-the-change` (advisory) → **pass** — three breakages, each producing
    named failures, listed in the report. The `choices=` break is the one worth keeping: it means a
    future "tidy-up" that discards ADR-0004's decision fails the suite instead of shipping.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/verify-report.md` (new), carrying
    `Verified-commit: 8792e410bb27c9256e466bc77895fb7a85598131`
  - `tracker/items/WI-0003/item.md` — AC1 through AC10 ticked, each against evidence in that report
  - no bug items filed
- **Status:** `verifying` → `in-review`
- **Result:** Pass on all ten criteria, every one demonstrated by a command run here rather than
  read about. Two things are handed to review as observations rather than defects: the
  combination's incidental selection, and the `description` string that predates this item.

## 2026-08-17T00:20:01Z — review-close v0.1.1 — reviewer

- **Item:** WI-0003
- **Trigger:** status `in-review`, dispatched by `next`
- **Clock note:** this execution ran at 2026-08-17T00:15:13Z by this machine's clock, which is
  what `Q-001`'s `created` and the history row carry. The preceding journal entry is stamped
  00:20:00Z — `verify` wrote its heading from a value ahead of the real clock — and entries must be
  non-decreasing, so this heading is clamped to 00:20:01Z rather than rewriting an append-only
  entry that belongs to another execution. Recorded because a clamp that is not announced looks
  like a gap in the timeline.
- **Inputs read:** `item.md` (ten criteria, all ticked), `history.md` (six rows), `journal.md` in
  full (five entries), `artifacts/plan.md`, `artifacts/impl-report.md`,
  `artifacts/verify-report.md`, `artifacts/refinement-qa.md`, `questions/` (empty at the time of
  reading), `docs/architecture/adr/ADR-0001`, `ADR-0003`, `ADR-0004`, `ADR-0005`, `ADR-0008`,
  `ADR-0009`, `docs/architecture/overview.md` v5, `docs/product/vision.md` v2, and the diff
  `main..wi/WI-0003` for `linecount.py` and `tests/test_linecount.py`, hunk by hunk
- **Decisions:**
  - **The record's mechanics pass.** `history.md` chains without a gap and its last row matches
    `item.md`; five skill executions in the history have five journal entries (`implement`'s two
    rows are one execution and correctly carry one entry); all ten boxes are ticked and every tick
    has a command and quoted output behind it in `verify-report.md`; no question existed on the
    item at that point; every commit on the branch names WI-0003.
  - **The verification is not stale**, checked rather than assumed: `check-verify-freshness` reports
    the verified commit `8792e410` against branch head `b6c7414a` and finds only five files under
    `tracker/`/`docs/` changed since — the record, not the code. D10 holds.
  - **The diff is accounted for, hunk by hunk.** Module docstring (plan step 6), `sort_rows` (3),
    `parse_sort` (1), the `--sort` declaration (2), the validation block in `main` (4), the single
    changed sort line (5), and the tests (7). The two hunks not in the plan — the ADR-0009 comment
    above the slice and the `parse_args` docstring — were both declared under
    `## Deviations from the plan` and both are improvements to the record rather than to behaviour.
    Nothing contradicts an ADR: ADR-0004's shape is followed exactly, ADR-0005's signature is
    untouched, ADR-0008's byte-orientation is extended consistently to the comparison, and ADR-0009
    is followed to the letter — `rows[:top]` is byte-for-byte what WI-0002 left.
  - **One maintainability finding, not blocking.** `sort_rows`'s `else` branch means any `order`
    that is not `"name"` silently means "count": a typo like `sort_rows(rows, "nmae")` would return
    the count order rather than raise. It is unreachable today because `parse_sort` gates the only
    call site and `ParseSortTest` proves it rejects everything else, and `verify` demonstrated the
    sensitivity of that test. Recorded in `review.md` as a finding to be aware of if a second call
    site is ever added, not as a defect of this item.
  - **The two declared gaps were judged, not waved through.** The `--top N --sort name` selection
    is unspecified by design (ADR-0009) and the item forbids treating it as a defect — accepted.
    Argparse's `description` still reading "largest first" is pre-existing (it was already partial
    after WI-0002), covered by no criterion, and excepted by AC4 — accepted, and to be written into
    the item's `## Notes` at closing so it survives the report nobody re-reads.
  - **D7 fails, and the fix is not mine to make.** `docs/product/vision.md` v2 records `--sort` as
    "(being added, WI-0003; not delivered at the time of writing)". Merging this branch makes that
    stale, which is exactly what D7 and the epic's DE4 test for. `spec/doc-header.md` §5 allocates
    `product/vision.md` to `intake`, `refine` and `answer-questions`; `review-close` is not an
    updater of it, and the section's own reasoning applies to me directly — I would be editing the
    document and then certifying D7 and DE4 against my own edit. Recording it as an accepted gap
    was rejected as an option: that is precisely what happened to `--top` at this epic's first
    closure, and the human's response on returning was "nobody ever added `--top` to that vision
    either, so put that in too". Filed `Q-001` to the architect rather than editing, guessing, or
    closing over it. `doc-header.md` §3's "fixing a typo is a content change, the rule has no
    exceptions" is what rules out treating this as too small to matter.
  - **No merge was performed.** The merge is step 8, after the accept decision, and the accept
    decision turns on D7. Merging first and asking afterwards would have made the question academic
    and the trunk the thing under discussion.
- **Questions raised:** `Q-001` (blocking, to architect) — whether `answer-questions` should update
  `vision.md` to record `--sort` as delivered so D7 and DE4 can pass, with three options and a
  recommendation. Not escalated to the human: none of `spec/question.md` §4's four conditions
  applies — the record fully determines the answer.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0003 wi/WI-0003` → exit 0,
    "only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers
    the code"
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → exit 0, all 3
    commits name WI-0003
  - `git diff main..wi/WI-0003 -- linecount.py` and `-- tests/test_linecount.py` → read in full;
    `git diff --numstat` on the tests → `172 0`
  - `grep -c "^- \[x\] AC"` / `"^- \[ \] AC"` on `item.md` → `10` and `0`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
- **Gates:**
  - `definition-of-done` (hard) → **fail at D7**, walked criterion by criterion:
    **D1 pass** (10/10 ticked) · **D2 pass** (each tick cites a command and its output in
    `verify-report.md`) · **D3 pass** (the gates were run on `8792e41`, the last code commit;
    `tests-pass` re-run here would be on the merge result, which this execution never reached) ·
    **D4 pass** at the time of the walk — `Q-001` was filed by this execution afterwards and is now
    the open blocking question · **D5 pass** (five executions, five journal entries, history chains
    to the current status) · **D6 pass** (ADR-0009 is the only design decision this change made, and
    it is cited from `plan.md`, this journal, `item.md` `## Notes`, `overview.md` v5 and a comment
    in the code) · **D7 fail** — `docs/product/vision.md` still describes `--sort` as not delivered;
    `overview.md` was properly bumped v4 → v5 with a change-log row, so the architecture side of D7
    is satisfied and the product side is not · **D8 pass** (`check-commit-refs`) · **D9 not yet** —
    the branch is unmerged because this execution stopped before step 8 · **D10 pass**
    (`check-verify-freshness`) · **D11 pass** — `review.md` is not yet written, because the review
    concluded in a question rather than a verdict; this journal entry carries what was examined
    and will be lifted into `review.md` when the item resumes.
  - `verification-postdates-the-code` (hard) → **pass** — `check-verify-freshness`, exit 0.
  - `commits-reference-the-item` (hard) → **pass** — `check-commit-refs`, exit 0, 3 commits.
  - `tests-pass-on-the-merge-result` (hard) → **not run** — there is no merge result to run them
    against. Not a pass and not a skip: the step that would produce the artefact was not reached.
  - `workspace-valid` (hard) → **pass** — `validate-workspace .`, exit 0.
  - `record-is-reconstructible` (hard) → **pass** — from the tracker, `docs/` and `git log --grep
    WI-0003` alone: what was built and why (the human's two-folder comparison, `item.md` and
    `EP-001/journal.md`), which skill decided what (five journal entries, each with its gates),
    what questions arose (Q2 at refinement, left `[unresolved]` on his instruction; `Q-001` here),
    and what verification found (ten criteria with commands and output, plus three sensitivity
    breakages). The one thing a reader cannot learn is what `--top N --sort name` *should* select —
    and the record says plainly that nobody decided it, which is the honest answer rather than a
    hole.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md` (new, blocking, to architect)
  - no merge, no `review.md`, no change to `item.md`'s status beyond the suspension
- **Status:** `in-review` → `awaiting-answer` (`resume-to: in-review`)
- **Result:** The change is sound and the record is complete — every mechanical check passes, the
  diff maps to the plan, and the two declared gaps are acceptable. It cannot be closed yet: the
  product vision still says this feature is not delivered, and updating that document belongs to
  `answer-questions`, not to me. Everything examined here is recorded so the resumed execution does
  not repeat it.

## 2026-08-17T00:20:02Z — answer-questions v0.1.1 — architect

- **Item:** WI-0003
- **Trigger:** status `awaiting-answer` with an open blocking question addressed to `architect`;
  dispatched by `next` (orchestrator step 3)
- **Inputs read:**
  - `tracker/items/WI-0003/questions/Q-001.md` — the only question on the item, blocking, to
    architect. No non-blocking questions were open, so there was no backlog to sweep up
  - `tracker/items/WI-0003/item.md` (ten criteria, all ticked), `history.md` (the suspending row
    records `resume-to: in-review`), `journal.md` (six entries, including `review-close`'s
    per-criterion Definition of Done walk)
  - `tracker/items/WI-0003/artifacts/verify-report.md` (the verdict and AC1's quoted output),
    `impl-report.md` (what was built, and the two declared gaps), `plan.md`,
    `refinement-qa.md` (Q2, to confirm the answer does not touch it)
  - `docs/product/vision.md` **v2** — the document in question, read in full to establish that the
    stale parenthetical was the *only* thing merging invalidated
  - `docs/architecture/adr/` — **ADR-0009** in full (to confirm nothing here disturbs it),
    ADR-0004 and ADR-0008 checked for contradiction; `docs/architecture/overview.md` v5
  - `.claude/agile-skills/spec/doc-header.md` §3 and §5, `spec/question.md` §4,
    `spec/dor-dod.md` §3 and §4
- **Decisions:**
  - **Answered by route 1 — from an existing document — not by deciding.** The question asks
    whether a documentation fact should be recorded, and three artifacts already establish the
    fact: ten ticked criteria in `item.md`, `verify-report.md`'s "Pass" against
    `8792e410bb27c9256e466bc77895fb7a85598131`, and commit `214dc3d` on the branch. No ADR was
    written, because no alternative was being chosen: writing one would pad the trail with a
    non-decision, which `spec/doc-header.md` §4 warns against.
  - **Option A, as the asker recommended.** B was rejected on the asker's own reasoning
    (`doc-header.md` §5 exists so a reviewer cannot certify D7/DE4 against their own edit) and C
    on the record's precedent — the same gap, left open for `--top` at this epic's first closure,
    is the one the human returned and asked to have fixed.
  - **The minimum edit.** Only the parenthetical changed. The bullet's description of what
    `--sort` does was written by `intake` from the refined criteria and matches what shipped, so
    rewriting it would have been an unrequested edit to a product document made under cover of
    answering a question. Nothing was added about byte order or the `--top` interaction: neither is
    what was asked, and the vision is not a manual.
  - **The ordering caveat is stated in the answer, not hidden.** The word "delivered" is written
    one step before the merge that makes it literally true. If `review-close` rejects instead of
    merging, this consequence must be reverted with the item's status; that is named in
    `## Answer` so a reader does not have to notice it themselves.
  - **Not escalated.** None of `spec/question.md` §4's four conditions holds, and the human's
    intent is on the record in his own words from intake: "I'd rather the vision described what the
    tool actually does."
  - **No epic-journal entry.** The answer changed a documentation fact, not the shape of the work,
    so per the skill's journaling rule it belongs on the item alone. EP-001's own entry comes when
    `review-close` closes it.
- **Questions raised:** none. Nothing was re-addressed to the human.
- **Commands:**
  - `date -u` → `2026-08-17T00:18:40Z`; `tail -1 tracker/items/WI-0003/history.md` →
    `resume-to: in-review`, read rather than inferred from which skill asked
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to in-review --actor
    answer-questions …` → see Status
- **Gates:**
  - `answer-is-propagated` (hard) → **pass** — every file named under `## Consequences` was opened
    and the change confirmed present: `docs/product/vision.md` carries `version: 3`,
    `updated-by: answer-questions`, `updated-for: WI-0003`, the bullet now reading "(delivered,
    WI-0003)", and a v3 change-log row; `Q-001.md` carries `status: answered`, `answered-at` and
    `answered-by`; this journal entry and the history row exist. The section names four files, not
    intentions.
  - `answered-from-the-record` (hard) → **pass** — the answer cites `item.md`'s ticked criteria,
    `verify-report.md`'s verdict and verified commit, and `impl-report.md`/commit `214dc3d`. The
    record was not silent, so no ADR was required.
  - `escalation-is-justified` (hard) → **not applicable, recorded rather than omitted** — nothing
    was escalated. The four conditions were checked one by one against `spec/question.md` §4 and
    none applies; the check is written into `## Answer`.
  - `workspace-valid` (hard) → **pass** — `validate-workspace .`, exit 0.
  - `item-resumed-correctly` (hard) → **pass** — the suspending row of 00:16:31Z records
    `resume-to: in-review`, and this execution's row targets `in-review`. They match. Read from the
    history rather than inferred: a `review-close` question and a `verify` question both look like
    "it was being checked", and inferring would have discarded a completed review.
  - `definition-of-ready` / other skills' gates → not run; not this skill's.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md` — answered, with the answer, the four consequences,
    and the ordering caveat
  - `docs/product/vision.md` — v2 → v3, one parenthetical and one change-log row
  - no ADR created, none superseded; **ADR-0009 untouched**; no acceptance criterion amended and no
    plan step rewritten
- **Status:** `awaiting-answer` → `in-review` (the recorded `resume-to`)
- **Result:** D7's blocker is cleared by a documentation fact the record already contained, edited
  by the skill entitled to edit it. `review-close` resumes with the same review it had already
  completed and one criterion now satisfiable.

## 2026-08-17T00:21:54Z — review-close v0.1.1 — reviewer

- **Item:** WI-0003
- **Trigger:** status `in-review`, dispatched by `next` after `answer-questions` resumed the item
  at its recorded `resume-to`. This is the second execution of this skill on this item; the first
  (00:20:01Z entry) did the reading and stopped at D7
- **Inputs read:** `questions/Q-001.md` in full, including `## Answer` and `## Consequences`;
  `docs/product/vision.md` **v3** (the file the answer named, opened to confirm the change is
  actually there); `item.md`, `history.md` and `journal.md` again, for the two rows and the entry
  added since; `artifacts/verify-report.md` and `impl-report.md` for the gaps being accepted; the
  diff `main..wi/WI-0003` once more before merging; `tracker/items/EP-001/item.md` — goal, all
  seven success measures, scope and out-of-scope — for the epic Definition of Done
- **Decisions:**
  - **The answer was checked, not taken on trust.** `Q-001`'s `## Consequences` names four files;
    each was opened. `vision.md` is at `version: 3` with `updated-by: answer-questions`,
    `updated-for: WI-0003`, the bullet reading "(delivered, WI-0003)" and a v3 change-log row.
    That is `answer-is-propagated` verified from the consuming side, which is the only side that
    matters.
  - **The answer's ordering caveat was honoured.** It noted that "delivered" was written one step
    before the merge that makes it true, and that rejecting instead of merging would require
    reverting it. I merged, so the caveat discharges; nothing needed reverting.
  - **Accept — and the merge had to be redone in the other order.** I merged first, as the
    procedure's step 8 says, with `--no-ff` (trial merge `0dbd81a`, 77 tests green on it). The
    close was then **refused**: `commits-reference-the-item` runs `check-commit-refs` over
    `main..wi/WI-0003`, which is empty once the branch is merged, so it reported "nothing was
    delivered". The gate is unsatisfiable after the merge that D9 requires. Rather than
    `--force` — which would stamp `[gates forced]` on a row whose gates are otherwise clean, and
    which is not the reviewer's override to take alone — I checked how the five earlier items in
    this epic closed, and WI-0001's history row states the answer outright: *"closing before the
    fast-forward so commits-reference-the-item still has a range"*. So the trial merge was rewound
    (`git reset --hard` to the pre-merge commit; local, never published, and nothing outside this
    execution's uncommitted drafts referenced it), the item was closed on the branch with the gate
    passing on a real range, and `main` was fast-forwarded afterwards — which is also the shape
    every other item in this repository has, with no merge commits on `main`. Recorded rather than
    quietly re-done: an unpublished rewind is cheap, but a rewind nobody mentions is not.
  - **The defect is the tooling's, so no bug item was filed.** `review-close`'s step order (merge
    at 8, close at 9) contradicts its own gate's range. A `bug` under EP-001 would describe
    something the linecount tracker does not own; `review.md` `## Findings` 3 records it where the
    next reviewer of this project will meet it.
  - **Three gaps accepted and written into `item.md` `## Notes`**, not left in the reports: the
    `--top N --sort name` selection, argparse's now-partial `description`, and `sort_rows`'s
    `else` branch. The third is my own finding rather than an inherited one — the branch is
    unreachable today only because `parse_sort` gates the single call site, which is a property of
    the call graph and not of the function. None is a defect: no criterion is violated by any of
    them, so sending the item back would have been rejecting it for something nobody asked for.
  - **EP-001 closes.** WI-0003 was its last child not `done`, so the epic Definition of Done was
    applied here — the only point in the pipeline where every sibling's state is already in hand —
    and all seven success measures were re-run against the merged trunk rather than assumed from
    the earlier closures. The epic's own journal entry carries the measure-by-measure results.
- **Questions raised:** none. `Q-001`, filed by this skill's previous execution, is `answered`.
- **Commands:**
  - `git checkout main && git merge --no-ff wi/WI-0003` → trial merge `0dbd81a`, 10 files,
    +934/−26
  - `python3 -m unittest discover` **on that merge result** → exit 0, `Ran 77 tests in 2.254s`,
    `OK`
  - `transition WI-0003 --to done …` → **refused**: `run-gate: 1 hard gate(s) failed:
    commits-reference-the-item`; `check-commit-refs WI-0003 wi/WI-0003` → exit 1, "no commits on
    `main..wi/WI-0003`; nothing was delivered"
  - `grep "| done |" tracker/items/*/history.md` → the five earlier items' closing rows, including
    WI-0001's "closing before the fast-forward so commits-reference-the-item still has a range"
  - `git reset --hard 4b02d9b` (rewinding the trial merge) and `git checkout wi/WI-0003`
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → exit 0, 5 commits
    naming WI-0003, on a range that exists again
  - after closing: `git checkout main && git merge --ff-only wi/WI-0003`, then
    `python3 -m unittest discover` on the trunk → exit 0, 77 tests
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0003 wi/WI-0003` → exit 0
  - the seven epic success measures, each run against the merged trunk — commands and output in
    EP-001's journal entry of the same timestamp
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
- **Gates:**
  - `definition-of-done` (hard) → **pass**, D1–D11 individually, with the evidence in
    `artifacts/review.md`'s table. D7 is the one that changed since the first execution: `vision.md`
    v3 now records `--sort` as delivered, so both halves of D7 — architecture (`overview.md` v5)
    and product (`vision.md` v3) — hold.
  - `verification-postdates-the-code` (hard) → **pass** — `check-verify-freshness`, exit 0; every
    commit after the verified one touches only `tracker/` and `docs/`.
  - `commits-reference-the-item` (hard) → **pass** — `check-commit-refs`, exit 0, all 5.
  - `tests-pass-on-the-merge-result` (hard) → **pass** — 77 tests, exit 0, run twice: on the trial
    merge `0dbd81a` before closing, and on `main` after the fast-forward. This is the gate the
    first execution could not run at all, and it is recorded as run here rather than inherited from
    the branch.
  - `commits-reference-the-item` (hard) → **pass on the second attempt, and the first failure is
    recorded rather than hidden** — exit 1 while the trial merge stood ("no commits on
    `main..wi/WI-0003`"), exit 0 with all 5 commits once the merge was rewound. See `## Decisions`
    and `review.md` `## Findings` 3.
  - `workspace-valid` (hard) → **pass** — `validate-workspace .`, exit 0, 0 errors, 0 warnings.
  - `record-is-reconstructible` (hard) → **pass** — from `tracker/`, `docs/` and
    `git log --grep WI-0003` alone a reader can answer all four questions: what was built and why
    (the two-folder comparison, in the human's words in `EP-001/journal.md`), which skill decided
    what (seven journal entries with their gates), what questions arose and how they resolved
    (Q2 at refinement, left `[unresolved]` on his instruction; `Q-001` here, answered from the
    record and propagated), and what verification found (ten criteria, six negative cases, three
    sensitivity breakages). What the record does *not* answer — what `--top N --sort name` should
    select — it says plainly that nobody decided, which is an answer rather than a hole.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/review.md` (new)
  - `tracker/items/WI-0003/item.md` — three accepted gaps added to `## Notes`; `status: done`,
    `outcome: delivered`
  - `main` fast-forwarded to the branch tip after closing (the trial merge `0dbd81a` was
    rewound; see Decisions)
  - `tracker/items/EP-001/item.md` — `status: done`, `outcome: delivered`; and an entry on
    `EP-001/journal.md` with the seven success measures re-run
- **Status:** `in-review` → `done` (`outcome: delivered`)
- **Result:** Accepted and merged. The flag ships; the one question the human refused to answer is
  still unanswered, on purpose and in writing; and the document rule that would have been easiest
  to bend was escalated instead of bent. EP-001 closes with it.
