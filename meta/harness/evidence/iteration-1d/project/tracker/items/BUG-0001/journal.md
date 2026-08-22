# Journal — BUG-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-22T02:28:45Z — verify v0.1.2 — qa-engineer

- **Item:** BUG-0001
- **Trigger:** filed by `verify` while verifying WI-0001 at branch head
  `49dd2a0cffdabf33fd4976f9d93bfc62edbc591f`. Not dispatched — this is the item's creation.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — to establish that no criterion of WI-0001 covers this
  - `expenses/cli.py` on `wi/WI-0001` — `main` saves after the handler has already printed
  - `.claude/agile-skills/spec/work-item.md` §3 — the required body for a bug
- **Decisions:**
  - **Filed as a bug rather than sent back to WI-0001.** `verify`'s rule: a send-back is for a
    failure of the item's own acceptance criteria. WI-0001 defines "refused" as a stderr message,
    a non-zero exit code, and no change to the recorded data; all three hold. No criterion of
    WI-0001 constrains stdout on a failed write, so WI-0001 is not failing and this is unspecified
    behaviour that needs its own item.
  - **One bug, not three.** `add-person`, `add-expense` and `repay` all show it, but they share
    one root cause — the handler prints and then `main` saves — and one fix. Splitting them would
    give three reproductions of the same line of code.
  - **Priority `medium`.** No data is lost or corrupted and the exit code is correct, so a careful
    caller is not misled; a person reading the terminal, or a script reading stdout, is.
  - **Filed at `ready`, not `draft`.** `pipeline.yaml` allows `verify` to create a bug directly at
    `ready`, on the grounds that a bug with reproduction steps already satisfies the bug
    Definition of Ready. Both acceptance criteria are decidable from a terminal.
- **Questions raised:** none
- **Commands:**
  - `python3 -m expenses --file $V/l.json add-person Cara` (with `$V` at mode 500) → exit 1,
    stderr `error: cannot write the ledger at …: [Errno 13] Permission denied: …`, stdout
    `Added Cara.`
  - the same with `add-expense --payer Ana --amount 10 --description x` → exit 1, stdout
    `Recorded 10.00 paid by Ana for x.`
  - the same with `repay --from Ana --to Ben --amount 5` → exit 1, stdout
    `Recorded Ana repaying 5.00 to Ben.`
  - `python3 -m expenses --file $V/l.json people` after restoring mode 700 → exit 0, prints
    `Ana` and `Ben` only, confirming nothing was recorded
  - `.claude/agile-skills/scripts/new-item --id BUG-0001 --type bug … --found-in WI-0001` → exit 0
- **Gates:** not applicable — this entry records the creation of an item, not an execution against
  one. `verify`'s own gates are recorded in WI-0001's journal entry for this execution.
- **Artifacts:**
  - `tracker/items/BUG-0001/item.md` — summary, six reproduction steps, expected and actual
    behaviour with verbatim output, and two acceptance criteria
- **Status:** `—` → `ready`
- **Result:** Filed against WI-0001's delivered behaviour: all three recording commands print
  their success line before the save is attempted, so a failed write reports success on stdout and
  failure on stderr in the same run. The data is genuinely unchanged, which is why WI-0001's own
  criteria do not catch it.

## 2026-08-22T03:44:14Z — plan v0.2.0 — architect

- **Item:** BUG-0001
- **Trigger:** status `ready`, dispatched by `next` — the only runnable item on the board.
  WI-0003 is `blocked` and the two work items are `done`.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — the summary, the six reproduction steps, the verbatim
    actual output, AC1 and AC2, and the `## Notes` reasoning for why this is a bug item rather
    than a send-back to WI-0001
  - `tracker/items/BUG-0001/history.md` — one row; filed at `ready` by `verify` during WI-0001.
    Not a re-plan, so there is no rejection record to read first
  - no `artifacts/refinement-qa.md` exists — a bug enters at `ready` and `verify` applied the bug
    Definition of Ready at filing time (`spec/dor-dod.md` §2), so there was no refinement round
  - `docs/architecture/overview.md` (v6) — the four modules and what each is allowed to know, the
    exit-code table, and the statement that `cli.py` is the only module that writes to stdout
  - `docs/architecture/adr/` — all ten existing ADRs scanned; `ADR-0003` (the ledger file and its
    precedence), `ADR-0005` (no third-party dependencies, hence `unittest` and `compileall`) and
    `ADR-0010`/`ADR-0007` (what WI-0003's import command will be) read in full
  - `tracker/items/WI-0001/artifacts/plan.md` — for the "every command is the same skeleton"
    property this fix has to preserve
  - `tracker/project.yaml` — `commands.test` and `commands.lint`, both already set
  - the code: `expenses/cli.py` in full, `expenses/store.py` in full,
    `tests/cli_harness.py` in full, and `tests/test_persistence.py` (the `run` helper, the two
    permission tests and their root guard)
- **Decisions:**
  - **The handler contract changes, rather than three `print` calls moving. Route: decided, and
    recorded as `ADR-0011`.** Moving the prints into `main` command by command would fix today's
    three commands and leave the ordering as something each future command must remember —
    including `WI-0003`'s importer, which is a fourth mutating command. Making the handler return
    its success line puts the ordering in `main` once, which is the same argument that put the save
    in `main` in the first place. Three alternatives were worth naming and are in the ADR:
    returning `(changed, line)`, buffering stdout in `main`, and saving before the handler runs.
  - **The read-only handlers keep printing their own rows and return `None`.** Route: decided, in
    `ADR-0011`. The return value is *the success line*, not *the command's output*. Routing the
    listings through it is option C, which was rejected because it stops `expenses` streaming and
    makes the ordering a property of a buffer rather than of readable code. Stating this explicitly
    matters more than it looks: the asymmetry reads like an oversight, and the next person to
    "tidy" it would reintroduce the rejected option.
  - **Nothing outside `cli.py` changes. Route: answered from the code, not assumed.** The tempting
    assumption was that no caller depends on the handler's `bool`. It was checked instead —
    `grep` over `tests/` and `expenses/` for `handler`, `-> bool` and `changed` returns only two
    unrelated test names — so `## Assumptions` in the plan is empty rather than carrying a
    plausible-sounding guess.
  - **The success wording stays byte-identical. Route: answered from the document.** `BUG-0001`
    quotes all three lines as the actual behaviour and asks only for their timing. Rewording them
    would be a change nobody asked for that `verify` would have to judge against a criterion that
    does not mention it.
  - **The regression test lives in `tests/test_persistence.py` and uses real processes.** Route:
    decided. That file is the end-to-end-through-real-processes file, it already has the `run`
    helper and the `@unittest.skipIf(os.geteuid() == 0, ...)` guard the permission tests need, and
    the defect is about what a real run writes to stdout. The in-process harness would also capture
    stdout, but the bug was found and reported against real processes and the regression should be
    reproducible by the same six steps.
  - **The test must lock the directory *after* the people are recorded.** Route: answered from the
    code. `add-expense` and `repay` name people, and an unknown person is refused with exit 2
    before any save is attempted, so locking an empty directory would produce a passing test that
    never exercises the defect. This is written into the plan step rather than left to be
    rediscovered, because it is exactly the shortcut a hurried implementation would take.
  - **The plan asserts the test fails before the fix.** Route: decided. A regression test that was
    never observed failing against the unfixed code is not evidence, and the fix is invisible on
    the success path, so there is nothing else a reviewer could look at.
  - **`docs/architecture/overview.md` is updated by `implement`, at step 6, not by this
    execution.** Its header says it describes code that exists, and the handler contract does not
    exist yet. Recording it as a plan step keeps the D12 obligation visible without putting a claim
    about unwritten code into the document — the same sequencing WI-0002 used, where `plan` wrote
    v4 in advance and `implement` corrected it at v5. The difference here is that this change is
    one bullet, so describing it in advance would buy nothing.
  - **One improvement was found and deliberately left out of scope:** strengthening
    `CliTestCase.assertRefused` to assert empty stdout, which would pass today and would guard
    every existing refusal test in future. It maps to no criterion of this item. It is written into
    `## Out of scope for this item` so it is a visible opportunity rather than a lost thought.
- **Questions raised:** none. Nothing here is irreversible — `ADR-0011` is one file, no data
  migration, no change to any command's arguments or output on the success path — and nothing
  depends on intent no document records: `BUG-0001` states the expected behaviour and cites what it
  contradicts. `spec/question.md` §1 puts asking the human third for `plan`, behind answering from
  the documents and making a reversible recorded decision, and this fell to the first two.
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, 115 tests, OK (the recorded
    `commands.test`, run in this project by this execution)
  - `python3 -m compileall -q expenses tests` → exit 0 (the recorded `commands.lint`)
  - `python3 .claude/agile-skills/scripts/lint-claims <ADR-0011>` and `<plan.md>` → exit 0, 0
    errors 0 warnings, over the whole tree
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors 0 warnings
  - `grep -rn "handler\|-> bool\|changed" tests/ expenses/` → only two unrelated test names
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-08-22T03:41:30Z`
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors 0 warnings)
  - `every-criterion-is-addressed` → **pass**. Both criteria have a row in the plan's mapping
    table with a specific demonstration, not "tests": AC1 → steps 1, 2 and 3, demonstrated by the
    new test run for all three commands and by `BUG-0001`'s own six steps, whose step 4 must stop
    printing `Added Cara.` while the stderr line and exit 1 remain; AC2 → step 5, demonstrated by
    `python3 -m unittest discover -s tests -t . -q` passing on the fixed code and the same command
    failing the new test against the pre-fix code. No AC is unmapped and no step is unmapped —
    steps 4, 6 and 7 are the docstring, the overview and the gate run, which the mapping's
    "demonstrated by" column and D7/D12 require rather than an AC.
  - `project-commands-resolved` → **pass**. `commands.test` and `commands.lint` were already set
    for WI-0001 and both were run by this execution, green, against the current code.
    `commands.build` is `null` and stays so: nothing is built, the tool runs from the checkout
    (`ADR-0005`).
  - `decisions-recorded` → **pass**. The one decision with alternatives worth naming is
    `ADR-0011`, with four options, their costs and risks, the decision, and reversibility stated
    explicitly. Everything else in the plan is either answered from a document with the citation
    in place or recorded above with its route. No ADR was written for a choice with no alternative
    worth naming.
  - `claims-are-sourced` → **pass** (`lint-claims`, exit 0, 0 errors 0 warnings over the whole
    tree, run after both `ADR-0011` and `plan.md` were written).
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/plan.md` (new) — problem, approach, seven steps, the AC
    mapping table, an empty `## Assumptions` with the reason it is empty, decisions, four risks,
    and four things out of scope
  - `docs/architecture/adr/ADR-0011-a-command-handler-returns-its-success-line-rather-than-printing-it.md`
    (new, v1)
  - `docs/architecture/overview.md` — **not** updated by this execution; step 6 of the plan assigns
    it to `implement`, with the reason recorded above
- **Result:** BUG-0001 is planned. The defect is one line of ordering, but the fix is a contract:
  a handler returns its success line and `main` prints it after `store.save` returns, so the
  ordering is stated once in `main` instead of remembered in every command — including the import
  command WI-0003 will add. Seven steps, both criteria mapped, and a regression test that follows
  the bug's own reproduction in real processes and must be seen failing before the fix.
- **Status:** `ready` → `planned`

## 2026-08-22T03:44:54Z — plan v0.2.0 — architect

- **Item:** BUG-0001
- **Trigger:** a correction to the record this same `plan` execution had just written, appended
  under `spec/journal-and-history.md`'s rule that a wrong entry is corrected by a later entry that
  says what was wrong — never by rewriting one.
- **Inputs read:** `tracker/items/BUG-0001/history.md` (the row appended at
  2026-08-22T03:44:14Z), `.claude/agile-skills/spec/journal-and-history.md` §1
- **Decisions:**
  - **What went wrong.** The `--reason` passed to `scripts/transition` contained the literal text
    `str|None`. `history.md` is a markdown table, so the pipe was written through verbatim and
    split the reason across two cells: the row came out with 7 columns instead of 6, and
    `validate-workspace` then reported three consequent errors — `history.columns`,
    `history.tail-mismatch` (the malformed row's `to` no longer read as `planned`), and
    `journal.status.unmatched` (the journal entry claimed a move the history appeared not to
    record). The transition itself **was** applied; `item.md` says `planned` and the journal entry
    at 2026-08-22T03:44:14Z is correct as written.
  - **What was changed, exactly.** The four characters `str|None` in that row's `reason` cell were
    replaced with `str-or-None`. Nothing else in the row, and nothing else in either file, was
    touched: the timestamp, the `from`, the `to`, the `actor` and the `resume-to` are as the tool
    stamped them, and the reason's meaning is unchanged. This is a repair of a cell the tool
    mangled while writing text it was given, not a revision of what happened — but it is still an
    edit to an append-only file, which is why it is recorded here rather than done quietly.
  - **The toolkit defect this is evidence of.** `scripts/transition` interpolates `--reason` into
    a markdown table row without escaping `|`. Any reason mentioning a union type, a shell pipe or
    an alternation produces a workspace that fails validation immediately after a transition the
    tool reports as successful — and the failure surfaces as three errors about the history and
    the journal disagreeing, none of which names the actual cause. Escaping the pipe (or rejecting
    a reason containing one, with a message) would cost a line. Worth fixing in the toolkit: the
    tool's own output was what corrupted the record, and the diagnosis cost more than the fix
    would.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 before the repair, with
    `history.columns`, `history.tail-mismatch` and `journal.status.unmatched`; exit 0 after it,
    0 errors 0 warnings
- **Gates:** none apply — this entry accompanies no status change and runs no gate of its own. The
  five `plan` gates are recorded in the 2026-08-22T03:44:14Z entry and are unaffected: the repair
  changed six characters of prose in a history reason and no artifact any gate examines.
- **Artifacts:** `tracker/items/BUG-0001/history.md` — the reason cell of the
  2026-08-22T03:44:14Z row, `str|None` → `str-or-None`
- **Status:** `planned` → `planned` (unchanged — this entry accompanies no transition; the move it
  corrects the record of was made at 2026-08-22T03:44:14Z)
- **Result:** The record is truthful again and the workspace validates. BUG-0001 is `planned`, as
  the previous entry says; only the wording of that row's reason changed, and the change is
  described above so a reader can see exactly what was edited and why an append-only file was
  touched at all.

## 2026-08-22T03:48:14Z — implement v0.2.1 — developer

- **Item:** BUG-0001
- **Trigger:** status `planned`, dispatched by `next` as the only runnable item on the board (EP-001 `open`, WI-0001 and WI-0002 `done`, WI-0003 `blocked` — all four statuses have `owner: null`).
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — the two acceptance criteria, the six reproduction steps, and the verbatim actual output
  - `tracker/items/BUG-0001/artifacts/plan.md` — the seven steps, the AC mapping, the risks, and the four things declared out of scope
  - `tracker/items/BUG-0001/history.md` — two rows, `ready` then `planned`; no send-back, so this is a fresh execution and not a resumption
  - `tracker/items/BUG-0001/journal.md` — including the correction entry recording that the `planned` row's reason cell was repaired by hand
  - `tracker/items/BUG-0001/questions/` — empty; no question has ever been filed on this item
  - `docs/architecture/adr/ADR-0011-a-command-handler-returns-its-success-line-rather-than-printing-it.md` — the handler contract this item executes, and its rejection of buffering the listings
  - `docs/architecture/overview.md` v6 — the `cli.py` bullet that step 6 extends
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, `conventions.branch-prefix`, `conventions.commit-subject`
  - `expenses/cli.py` — all seven handlers, `main`, and the module docstring
  - `tests/test_persistence.py` — the `run` helper, `PersistenceTestCase`, and the two existing `skipIf(os.geteuid() == 0)` permission tests step 5 copies
  - `tests/cli_harness.py` — `assertRefused`, to confirm the out-of-scope note about widening it is about code that exists
- **Decisions:**
  - **This is a fresh start, not a resumption.** No `wi/BUG-0001` branch existed (`git branch -a` listed `main`, `wi/WI-0001`, `wi/WI-0002`), the history's last row is `ready → planned` rather than a send-back from `verifying` or `in-review`, and `item.md` carries no `branch` field. So there is no partial work to reconcile with, and the branch was created from `main` at `17ca1fa`.
  - **The test will be written before the fix, and run against the unfixed code**, because the plan's AC2 evidence column requires a recorded run showing the regression test failing on the pre-fix code — a regression test that never failed against the defect is not evidence that it covers it. The failing output goes in `impl-report.md`.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/BUG-0001 main` → exit 0, branch created at `17ca1fa`
- **Gates:**
  - `tests-pass` → **not yet run** (no change has been made; this entry opens the execution)
  - `lint-clean` → **not yet run**
  - `workspace-valid` → **not yet run**
  - `every-criterion-has-a-test` → **not yet run**
  - `commits-reference-the-item` → **not yet run** (no commit exists on the branch)
  - `no-unplanned-scope` → **not yet run** (advisory; no diff exists)
  - `claims-are-sourced` → **not yet run**
- **Artifacts:**
  - branch `wi/BUG-0001`, created from `main` at `17ca1fa`, no commits yet
- **Result:** Implementation of BUG-0001 has started on `wi/BUG-0001`. Nothing is built yet; the closing entry reports the work and runs the gates.
- **Status:** `planned` → `in-progress`

## 2026-08-22T03:51:18Z — implement v0.2.1 — developer

- **Item:** BUG-0001
- **Trigger:** status `in-progress`, continuing this skill's own execution opened at 2026-08-22T03:48:14Z; the plan's seven steps are done.
- **Inputs read:**
  - `tracker/items/BUG-0001/artifacts/plan.md` — the seven steps, worked in order
  - `tracker/items/BUG-0001/item.md` — AC1 and AC2, and the six reproduction steps
  - `docs/architecture/adr/ADR-0011-a-command-handler-returns-its-success-line-rather-than-printing-it.md` — the contract, including its rejection of buffering the listings
  - `.claude/agile-skills/spec/work-item.md` — the `## Acceptance criteria` rules, read to settle who ticks a box
  - `expenses/cli.py`, `tests/test_persistence.py`, `tests/cli_harness.py`, `docs/architecture/overview.md` — the files changed and the two consulted
- **Decisions:**
  - **The regression test was written and run first, against the unfixed code.** AC2 asks for a test that "fails if the success line is moved back before the save", and the only honest evidence for that is a recorded run in which it did fail. It failed three times — once per `subTest` — with `'Added Cara.\n' != ''`, `'Recorded 10.00 paid by Ana for x.\n' != ''` and `'Recorded Ana repaying 5.00 to Ben.\n' != ''`, which are the three lines `item.md` quotes as the actual behaviour. A regression test that never failed against the defect demonstrates nothing, and this one now cannot be weakened without the failure reappearing.
  - **Step 7's "tick both criteria in `item.md`" was not carried out, and this is the one deviation that changes who does something.** `spec/work-item.md` says a box is ticked by `verify`, "only when it has evidence for it, and cites that evidence in `verify-report.md`". A box ticked by `implement` would assert to `verify` that an independent party had already confirmed the criterion — the single thing the separation of these two skills exists to prevent. The evidence step 7 wanted recorded is in `impl-report.md`'s criteria table instead, which is what `verify` reads. Recorded as deviation 1 in the report; no code and no criterion is affected.
  - **The `people` assertion was made stronger than the plan's wording.** The plan asks the test to assert `Cara` is absent after the permissions are restored; the test asserts the listing is exactly `["Ana", "Ben"]`. That entails the absence and additionally catches a ledger that lost or reordered what was already there. Inside the plan's latitude — same step, stricter assertion.
  - **The docstring addition is a paragraph, not the single sentence step 4 names.** It states the contract, cites `ADR-0011`, and says why the four listings return `None` after printing their own rows. `ADR-0011` names exactly that misreading — mistaking "the success line" for "everything this command prints" — as option A's own risk, and the docstring is where a person adding a command will be looking.
  - **Not decided here, and not needed:** whether `assertRefused` should also assert empty stdout. The plan puts it under "out of scope"; it maps to no criterion of this item, and widening a shared assertion inside a bug fix would make both changes harder to review. Left where the plan left it, as a visible opportunity.
- **Questions raised:** none — the plan answered everything the code needed, and the one conflict encountered (step 7 against `spec/work-item.md`) is resolved by the spec rather than by a decision that was mine to make.
- **Commands:**
  - `git checkout -b wi/BUG-0001 main` → exit 0
  - `python3 -m unittest tests.test_persistence.TestAFailedWriteSaysNothingOnStdout -v` on the unfixed tree → exit 1, `FAILED (failures=3)`, one per command
  - `python3 -m unittest discover -s tests -t . -q` on the branch head → exit 0, `Ran 116 tests in 3.002s / OK`
  - `python3 -m compileall -q expenses tests` → exit 0
  - BUG-0001's six reproduction steps by hand, stdout and stderr captured separately → all three commands `stdout=[] exit=1` with `error: cannot write the ledger at …: [Errno 13] Permission denied: '….tmp'` on stderr; step 6's `people` printed `Ana` and `Ben`
  - `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0001 wi/BUG-0001` → exit 0, all 3 commits name the item
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 5 items, 13 documents, 0 errors 0 warnings
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → used to stamp `overview.md` v7; the first value written was ahead of the clock and was corrected before committing
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` exit 0, 116 tests, on branch head `d727aba` before the report commit and unaffected by it)
  - `lint-clean` → **pass** (`python3 -m compileall -q expenses tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, 0 errors 0 warnings)
  - `every-criterion-has-a-test` → **pass** (AC1 → `TestAFailedWriteSaysNothingOnStdout.test_every_recording_command_prints_nothing_when_the_save_fails`, asserting empty stdout for all three commands, plus the by-hand reproduction; AC2 → the recorded pre-fix run of that test, `FAILED (failures=3)`. Neither rests on reading the code)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 3 of 3 commits)
  - `no-unplanned-scope` → **pass** (advisory; `git diff main..HEAD` is three files and every hunk maps to a numbered plan step — docstring to 4, seven signatures and three returns to 1–2, `main` to 3, the test class to 5, the overview bullet to 6)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0)
- **Artifacts:**
  - `expenses/cli.py` — the handler contract, the three returns, the four `None`s, `main`'s ordering, the docstring paragraph
  - `tests/test_persistence.py` — `TestAFailedWriteSaysNothingOnStdout`, one test over three commands
  - `docs/architecture/overview.md` — v7, the `cli.py` bullet and a change-log row
  - `tracker/items/BUG-0001/artifacts/impl-report.md` — new
  - branch `wi/BUG-0001`, commits `ad961d7`, `d727aba`, `29f526b` (3), all naming BUG-0001
- **Result:** All three recording commands now print nothing on stdout when the save fails, and the fix lives in `main` rather than in each command, so `WI-0003`'s importer inherits it. Both criteria have evidence in `impl-report.md` and both boxes are left unticked for `verify`, which is the one place this execution departed from the plan.
- **Status:** `in-progress` → `verifying`

## 2026-08-22T03:51:55Z — implement v0.2.1 — developer

- **Item:** BUG-0001
- **Trigger:** a correction to the entry at 2026-08-22T03:51:18Z, made immediately after it was written. No status change and no work on the item.
- **Inputs read:**
  - `tracker/items/BUG-0001/journal.md` — the entry just appended
  - `git log --oneline main..wi/BUG-0001` — the three commits, read rather than assumed
- **Decisions:**
  - **What was wrong.** The `**Artifacts:**` bullet of the 03:51:18Z entry gave the commit range as `ad961d7..b0fa7c2`. `ad961d7` is real; `b0fa7c2` is not a commit in this repository. It was written before `git commit` had reported the report commit's hash, so it is a predicted value rather than an observed one — the one class of thing a record must never contain, because a reader has no way to tell a guessed hash from a read one.
  - **What was changed, exactly.** That bullet now lists the three hashes individually — `ad961d7`, `d727aba`, `29f526b` — as `git log --oneline main..wi/BUG-0001` reports them. Nothing else in that entry or any other was touched, and the number of commits (3) and the claim that all three name the item are unchanged and were already independently confirmed by `check-commit-refs`. Listing them rather than writing a range also removes the ambiguity that `A..B` excludes `A`.
  - **Why an append-only file was edited rather than only annotated.** Leaving a hash that resolves to nothing would send the next reader — most immediately `verify` — looking for a commit that does not exist. The wrong value is replaced and this entry says what it was, so nothing is hidden.
  - **Worth noting about the toolkit:** nothing here is a tool defect. `scripts/transition` wrote exactly the body it was given. The lesson is mine: read hashes back from `git log` before putting them in a journal body, never from the commit you are about to make.
- **Questions raised:** none
- **Commands:**
  - `git log --oneline main..wi/BUG-0001` → exit 0, three commits: `29f526b`, `d727aba`, `ad961d7`
- **Gates:** none apply — this entry accompanies no status change and runs no gate of its own. The seven `implement` gates are recorded in the 03:51:18Z entry and are unaffected: the correction changes one line of prose in a journal bullet and no artifact any gate examines.
- **Artifacts:**
  - `tracker/items/BUG-0001/journal.md` — the `**Artifacts:**` bullet of the 2026-08-22T03:51:18Z entry, `ad961d7..b0fa7c2` → the three hashes listed
- **Status:** `verifying` → `verifying` (unchanged — this entry accompanies no transition; it corrects the record of the move made at 2026-08-22T03:51:18Z)
- **Result:** The commit list in the closing entry is now what `git log` reports. BUG-0001 remains `verifying`, as that entry says.

## 2026-08-22T03:55:59Z — verify v0.1.2 — qa-engineer

- **Item:** BUG-0001
- **Trigger:** status `verifying`, dispatched by `next` — the only runnable item on the board; EP-001 is `open`, WI-0001 and WI-0002 are `done`, WI-0003 is `blocked`, and all four of those statuses have `owner: null`.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — **first**, before the implementation report: AC1 and AC2, the six reproduction steps, and the three success lines quoted as the pre-fix actual behaviour. What would settle each criterion was derived from the criterion's own wording before anything the developer wrote was opened
  - `tracker/items/BUG-0001/history.md` — three rows; `ready → planned → in-progress → verifying`, no send-back, so this is a first verification
  - `tracker/items/BUG-0001/artifacts/plan.md` — the seven steps and the AC mapping, read for step 6's diff check and to see what the plan claimed would not change
  - `tracker/items/BUG-0001/artifacts/impl-report.md` — read after the criteria, and treated as a claim to check rather than as evidence. No row of my criteria table cites it
  - no `artifacts/refinement-qa.md` exists for this item — a bug enters at `ready` and neither criterion's wording turned out to be contested
  - `.claude/agile-skills/spec/dor-dod.md` — D12, to settle where the documentation finding belongs
  - the code at branch head `758c0af9b29cdf769943c42f3a98a3f179f82523` on `wi/BUG-0001`: `expenses/cli.py` in full, `tests/test_persistence.py`'s new class, and `git diff main..HEAD` across all three changed files
  - `tracker/project.yaml` — `commands.test` and `commands.lint`
- **Decisions:**
  - **AC1: pass, on the six steps run here rather than on the report's account of them.** All three recording commands under `chmod 500` gave `exit=1`, empty stdout and the `Permission denied` line on stderr, and step 6 confirmed neither `Cara` nor the expense nor the repayment was recorded.
  - **"Prints nothing" was checked byte-exactly.** My first pass captured stdout with `$(...)`, which strips trailing newlines and would report a lone `\n` as empty — a `print()` of an empty string would have slipped through. The check was redone with redirection and `wc -c`: `stdout_bytes=0` for all three. Small, but it is the difference between demonstrating the criterion and demonstrating something that looks like it.
  - **AC2: pass, and the sensitivity check was done the way AC2 words it.** The criterion says the test must fail "if the success line is moved back before the save", so `print(line)` was moved back above the `try: store.save(...)` block in `main` and the test re-run: `FAILED (failures=3)`, quoting the three pre-fix lines. `git checkout -- expenses/cli.py` restored it and the suite is green again.
  - **Recorded rather than passed over: the new test is the only guard among 116.** Against the sabotage the full suite reported `FAILED (failures=3)` and the other 115 tests passed. That is not reassurance, it is the fact that this criterion has exactly one test holding it up — which is why AC2 demands the test be demonstrably sensitive, and why the demonstration is in the report rather than summarised as "confirmed".
  - **The test was confirmed to have run, not skipped.** `id -u` → `1000`, so `skipIf(os.geteuid() == 0)` is inactive here, and the full-suite line is a bare `OK` with no skip count. Under root AC2's evidence would have been vacuous, and a passing suite would have looked identical.
  - **Boundary case 2 is not a defect, and no bug was filed for it.** With the ledger *file* at mode 400 but its directory writable, `add-person` succeeds and records. `store.save` writes a temporary file and renames over the target, and POSIX `rename` needs write permission on the directory, not on the file. The location genuinely can be written, so AC1 is not contradicted and neither is WI-0001 AC9. Filing a bug for designed atomic-replace semantics would misroute the work; it is recorded as an exercised boundary with its outcome, because a reader could reasonably expect mode 400 to protect a ledger and it does not.
  - **The documentation finding is routed to `review-close`, not sent back and not filed as a bug.** `overview.md`'s opening paragraph still says "this version is step 5 of WI-0002's plan"; "this version" is now v7, written for BUG-0001. Applying the classification test in the procedure: no acceptance criterion of this item says anything about the overview, so it is not a send-back; and it is not behaviour delivered by another item, so it is not a bug. It is a stale claim in a document this item touched, which is exactly D12, and D12 is `review-close`'s. It is in `## Defects found` where that audit will read it.
  - **Both boxes ticked, both on commands I ran.** Neither tick rests on `impl-report.md`.
- **Questions raised:** none — neither criterion was ambiguous. AC1 names its own reproduction and AC2 names its own falsification, which is why both could be settled without asking anyone.
- **Commands:**
  - `git rev-parse HEAD` → `758c0af9b29cdf769943c42f3a98a3f179f82523`
  - `id -u` → `1000` (not root; the regression test's skip guard is inactive)
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 116 tests in 2.993s / OK`
  - `python3 -m compileall -q expenses tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors 0 warnings
  - BUG-0001's six reproduction steps in a fresh `mktemp -d`, stdout and stderr to separate files → all three recording commands `exit=1`, `stdout=<<>>`, stderr `error: cannot write the ledger at …: [Errno 13] Permission denied: '….tmp'`; step 6 `people` → `Ana`, `Ben`
  - the same three commands re-run with `>/tmp/o 2>/tmp/e` and `wc -c` → `stdout_bytes=0`, `stderr_bytes=134`, exit 1 for each
  - `python3 -m unittest tests.test_persistence.TestAFailedWriteSaysNothingOnStdout -v` → exit 0, `Ran 1 test … ok`
  - `print(line)` moved above `store.save` in `main`, then the same test → exit 1, `FAILED (failures=3)`, `'Added Cara.\n' != ''`, `'Recorded 10.00 paid by Ana for x.\n' != ''`, `'Recorded Ana repaying 5.00 to Ben.\n' != ''`
  - `python3 -m unittest discover -s tests -t . -q` against that sabotage → exit 1, `Ran 116 tests`, `FAILED (failures=3)` — only the new test
  - `git checkout -- expenses/cli.py`; `git diff` → no change to it; `python3 -m unittest discover -s tests -t . -q` → exit 0, `OK`
  - boundary: `chmod 400` the ledger file with the directory writable, `add-person Cara` → exit 0, `Added Cara.`, and `people` afterwards lists `Ana`, `Ben`, `Cara`
  - boundary: `add-person Ana` when Ana exists → exit 2, `stdout_bytes=0`, stderr `error: 'Ana' is already recorded as 'Ana'; …`
  - boundary: `chmod 000` the ledger, `add-person Dee` → exit 1, `stdout_bytes=0`, stderr `error: cannot read the ledger at …: [Errno 13] Permission denied`
  - success path: the three success lines compared with `[ "$a" = "…" ]` against the strings `item.md` quotes → all three matched exactly; `people`, `expenses`, `repayments`, `debts` all exit 0 and still print their rows
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 0 errors 0 warnings
- **Gates:**
  - `tests-pass` → **pass** (`unittest discover` exit 0, 116 tests, run here at `758c0af` before anything was touched)
  - `lint-clean` → **pass** (`compileall` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, 0 errors 0 warnings)
  - `every-criterion-independently-checked` → **pass** (AC1 → the six steps plus the byte-exact re-run; AC2 → reading the test body, running it, and sabotaging `main` to make it fail. `impl-report.md` is cited nowhere as evidence)
  - `negative-cases-exercised` → **pass** (AC1 is wholly a negative criterion and every part of it was triggered; four further error and boundary paths were exercised — read-only ledger file, duplicate name, unreadable ledger, and the unchanged success path)
  - `tests-would-fail-without-the-change` → **pass** (advisory; the sabotage produced `FAILED (failures=3)` and the finding that 115 other tests are indifferent to this behaviour)
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/verify-report.md` — new, with `Verified-commit: 758c0af9b29cdf769943c42f3a98a3f179f82523`
  - `tracker/items/BUG-0001/item.md` — AC1 and AC2 ticked
  - no bug item filed; one documentation finding recorded for `review-close`'s D12 audit
- **Result:** BUG-0001 passes. A failed ledger write now says nothing on stdout for all three recording commands, the fix is in `main` so no command can get the ordering wrong on its own, and the regression test is demonstrably the thing that would catch its return. One stale sentence in `overview.md`'s lede is left for `review-close` to settle under D12.
- **Status:** `verifying` → `in-review`

## 2026-08-22T04:00:22Z — review-close v0.3.1 — reviewer

- **Item:** BUG-0001
- **Trigger:** status `in-review`, dispatched by `next` — the only runnable item; EP-001 is `open`, WI-0001 and WI-0002 are `done`, WI-0003 is `blocked`, and all four statuses have `owner: null`.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — both criteria, their tick state, and the `## Notes` reasoning for filing this as a bug rather than sending WI-0001 back
  - `tracker/items/BUG-0001/history.md` — five rows, chaining without a gap, the last matching the item's status
  - `tracker/items/BUG-0001/journal.md` — **in full**, all seven entries, since the Definition of Done includes the completeness of this record and it cannot be certified from a skim
  - `tracker/items/BUG-0001/artifacts/plan.md`, `impl-report.md`, `verify-report.md`
  - `tracker/items/BUG-0001/questions/` — empty; no question was filed at any stage
  - the diff `main..wi/BUG-0001`, hunk by hunk — three files under `expenses/`, `tests/` and `docs/`, 82 insertions and 28 deletions
  - `docs/architecture/adr/` — all eleven listed; `ADR-0011` in full, and `ADR-0007` and `ADR-0010` because they govern the import command `ADR-0011` argues will inherit this contract
  - `docs/architecture/overview.md` v7, and the code it makes claims about
  - `.claude/agile-skills/spec/dor-dod.md` §3 and §4, and `spec/workspace-layout.md` §1.1
- **Decisions:**
  - **Accepted, merged, closed as `delivered`.** All twelve Definition of Done criteria pass, each recorded with its own evidence in `review.md`'s table rather than under a single verdict.
  - **The diff was read against the plan rather than against the reports.** Every hunk maps to a numbered plan step — docstring to 4, seven signatures and four `return None`s to 1–2, three `print`-to-`return` conversions to 1, `main` to 3, the test class to 5, the overview bullet to 6. No unrequested scope.
  - **D12 found one claim that had stopped being true, and I corrected it (`overview.md` v8).** The lede still read "this version is step 5 of WI-0002's plan"; true at v6, false once `implement` wrote v7 for BUG-0001. `verify` found it and routed it here rather than filing a bug or sending the item back — the right call, since no criterion of this item covers the overview and it is not another item's behaviour. It is now rewritten to describe the document and defer to the change log for which item wrote which version, which is the form that does not go stale on the next edit. Header bumped, change-log row added.
  - **The audit was done from the citations, not from the prose.** Three absolute claims about behaviour this item touched were each checked by opening what they cite: "`cli.py` is the only module that writes to stdout or stderr" (grepped the other modules — no matches), `ADR-0011`'s "the handler is reached only through `set_defaults` and the single call in `main`, and no test reads its return value" (grepped `expenses/` and `tests/` — seven `set_defaults` lines, one call at `cli.py:129`, nothing in `tests/`), and "`main` prints the line only after `store.save` has returned" (read `main`). All three hold, and the second is worth having re-checked rather than re-quoted, because the change is exactly what could have falsified it.
  - **`impl-report.md`'s deviation 1 is accepted and was right.** `implement` refused plan step 7's instruction to tick the criteria, on the grounds that `spec/work-item.md` gives ticking to `verify`. That is the correct reading, and it is declared rather than done quietly, which is what made it reviewable. Deviations 2 and 3 are inside the plan's latitude.
  - **Four gaps accepted, and all four written into `item.md`'s `## Notes`.** Neither criterion is verified under root; `ADR-0011`'s "the importer inherits the ordering" claim is unverifiable until WI-0003 exists; `assertRefused` still does not assert empty stdout; and a ledger at mode 400 in a writable directory is still overwritten by the atomic rename. Accepting a gap is fine — leaving it only in a verification report nobody reads after closure is not, which is why each one is now on the item.
  - **One thing noticed and deliberately not filed as a bug:** `PersistenceTestCase.setUp` calls `tempfile.mkdtemp()` with no cleanup, so every test in that file leaves a directory behind. It predates this item, the new test inherits it rather than introducing it, and it is test hygiene rather than delivered behaviour — so it fails the test that would make it a bug item. Recorded in `review.md` so the judgement is visible instead of silent.
  - **The epic is not closed and no sign-off question is due.** `EP-001` still has `WI-0003` at `blocked`, so DE1 fails and DE7's stakeholder question is premature. `check-epic-signoff BUG-0001` passes, but for the unrelated reason that a bug is not an epic — worth stating so the pass is not mistaken for the epic having been cleared.
  - **A toolkit defect, hit and worked around.** `spec/workspace-layout.md` §1.1 requires `<item>/questions/` to exist even when empty; git does not track empty directories. BUG-0001 is the first item in this project that never had a question, so its `questions/` was an untracked empty directory — and the trial merge that *this skill's own procedure mandates* switches branches, which deleted it. `validate-workspace` then failed with `questions.missing` on an item that had done nothing wrong, at the moment of closing. I recreated the directory and added a `.gitkeep` explaining why it is there, so the next branch switch does not repeat it. The general fix belongs in the toolkit: `scripts/new-item` should create the keep file, or the validator should not require a directory version control cannot carry.
- **Questions raised:** none — nothing in the change contradicted an ADR, and no criterion was ambiguous.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness BUG-0001 wi/BUG-0001` → exit 0, "verified at `758c0af9`; `wi/BUG-0001` has moved to `ac5ff050` but only the record changed (5 file(s) under `tracker/` or `docs/`)"
  - `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0001 wi/BUG-0001` → exit 0, all 5 commits name the item
  - `python3 .claude/agile-skills/scripts/check-epic-signoff BUG-0001` → exit 0, "BUG-0001 is a 'bug', not an epic … PASS"
  - `grep -n "print(\|sys.stdout\|sys.stderr" expenses/*.py` excluding `cli.py` → no matches (D12)
  - `grep -rn "handler" expenses/ tests/` → seven `set_defaults(handler=…)`, one `line = args.handler(args, ledger)` at `cli.py:129`, one docstring line; nothing under `tests/` (D12)
  - `grep -n -i "print\|summar\|stdout\|output" docs/architecture/adr/ADR-0007*.md ADR-0010*.md` → no output; neither ADR constrains the import command's printing, so `ADR-0011` contradicts neither
  - `git branch trial/BUG-0001 main`; `git merge --no-ff wi/BUG-0001` → exit 0, no conflict, 9 files changed
  - `python3 -m unittest discover -s tests -t . -q` **on the merge result** → exit 0, `Ran 116 tests in 3.000s / OK`
  - `python3 -m compileall -q expenses tests` on the merge result → exit 0
  - `git checkout wi/BUG-0001`; `git branch -D trial/BUG-0001` → trial discarded, never published
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1, `questions.missing`, caused by the branch switch above; after recreating the directory with a `.gitkeep`, exit 0, 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 0 errors 0 warnings
- **Gates:**
  - `definition-of-done` → **pass** (D1–D12 each recorded with its own result and evidence in `review.md`'s table; D12 passes after the correction described above, and no criterion is covered by a blanket verdict)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0; run, not judged by how the last commits looked — the two commits after verification touch only `tracker/` and `docs/`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 5 of 5; run before the merge, while `main..wi/BUG-0001` is still non-empty)
  - `tests-pass-on-the-merge-result` → **pass** (116 tests, exit 0, on the trial merge of `wi/BUG-0001` into a throwaway copy of `main` — not on the branch alone)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0 after the `questions/` directory the trial merge deleted was restored; the failure and its cause are described above)
  - `record-is-reconstructible` → **pass** (answered from the tracker, `docs/` and `git log --grep BUG-0001` alone: *what and why* — `item.md`'s reproduction and `plan.md`'s problem statement; *which skill decided what* — `ADR-0011` by `plan`, the contract executed by `implement` with three declared deviations, both criteria ticked by `verify`; *what questions arose* — none on this item, and the journal says so explicitly rather than by omission; *what verification found* — `verify-report.md`'s criteria table, five boundary cases and the sensitivity check. The two self-declared correction entries in the journal mean even the record's own repairs are visible)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0)
  - `epic-sign-off` → **pass** (`check-epic-signoff` exit 0 — because this is a bug, not an epic. `EP-001` remains `open` with `WI-0003` at `blocked`, so DE1 fails and DE7 is not yet due)
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/review.md` — new: what was examined, the D12 claim audit table, D1–D12, five findings, four accepted gaps, the verdict
  - `tracker/items/BUG-0001/item.md` — `done`, `outcome: delivered`, and four accepted gaps added under `## Notes`
  - `docs/architecture/overview.md` — v8, the D12 correction to the opening paragraph, with a change-log row
  - `tracker/items/BUG-0001/questions/.gitkeep` — new, so the directory survives the branch switches this pipeline performs
  - the merge of `wi/BUG-0001` into `main`, made immediately after this close
  - `EP-001` unchanged — not closed, and not eligible to be
- **Result:** BUG-0001 is delivered and merged. A run that records nothing now says nothing on stdout, for all three recording commands at once, because the ordering lives in `main` rather than in each command — which is what makes it hold for the next mutating command too. Twelve Definition of Done criteria pass, one after I corrected a stale sentence in `overview.md` that `verify` had flagged, and the four gaps nobody checked are on the item rather than buried in a report.
- **Status:** `in-review` → `done`
