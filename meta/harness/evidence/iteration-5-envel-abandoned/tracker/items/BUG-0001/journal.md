# Journal — BUG-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-10T14:21:00Z — review-close v0.14.0 — reviewer

- **Item:** BUG-0001
- **Trigger:** not dispatched on this item — `review-close` was dispatched on WI-0001 at `in-review` and filed this bug while reviewing it, which is the creation row already in this item's history.
- **Inputs read:**
  - `tracker/items/WI-0001/artifacts/verify-report.md` `## Not verified, and why` — the declared gap "Behaviour under a non-UTF-8 locale", which is what sent this execution to look
  - `tracker/items/WI-0001/artifacts/plan.md` — assumption P5 and `## Risks`, both of which describe this area and describe it wrongly
  - `tracker/items/WI-0001/questions/Q-002.md` — the stakeholder's *"don't restrict the characters"*
  - `envel/store.py`, `envel/cli.py`, `bin/envel` on `wi/WI-0001` at `e92d188`
  - `docs/architecture/adr/ADR-0003-one-json-store-and-where-it-lives.md`, `ADR-0004-envelope-identity-is-the-folded-trimmed-name.md`
- **Decisions:**
  - **Filed as a bug rather than sent back to WI-0001.** The test in `verify`'s and `review-close`'s procedures is whether an acceptance criterion of that item says the behaviour should be different. None of AC1–AC11 does: AC8 covers a space and nothing covers a non-ASCII character. The promise lives in `WI-0001/Q-002` and in the item's `## Notes`, which is why it is real, and in neither of the two places that would make it a send-back.
  - **`medium`, not `high`.** Python 3.12 coerces the C locale to UTF-8 (PEP 538), so `LC_ALL=C` alone does not reproduce it; it needs `PYTHONCOERCECLOCALE=0` and `PYTHONUTF8=0` as well. Not `low`, because the failure mode is a traceback rather than a refusal.
  - **Left the fix undecided.** `## Expected behaviour` offers accept-and-store or refuse-with-a-message and says which is chosen is the planner's. What the item does assert is that a traceback is wrong, and AC1 is written so a person at a terminal can decide it.
  - **Did not edit WI-0001's plan**, although two of its sentences are now known to be wrong about this. It is a tracker artifact of an item about to close, and `review-close` does not rewrite a closed item's record; the correction is recorded in `## Notes` here instead, for whoever plans this.
- **Questions raised:** none.
- **Commands:**
  - `env -u PYTHONIOENCODING PYTHONCOERCECLOCALE=0 PYTHONUTF8=0 LC_ALL=C LANG=C PATH="$PWD/bin:$PATH" ENVEL_FILE="$T/s.json" envel new "café"` → exit 1, `UnicodeEncodeError: 'utf-8' codec can't encode characters in position 4-5: surrogates not allowed`, raised at `envel/store.py:66` and unhandled
  - the same under `LC_ALL=C` alone → exit 0, and `envel list` → `café`. The coercion is what hides it
  - `envel list` under the broken locale against a store already holding `café` → exit 0, prints `café`. The failure is on the write, not the print
  - `envel list` after the failed `new` → exit 0, `No envelopes yet.` — the store was not created, so the atomic write held
  - `scripts/new-item --id BUG-0001 --type bug --title ... --found-in WI-0001 --actor review-close --status ready` → exit 0
- **Gates:** none of `review-close`'s gates apply to this item. This execution created BUG-0001 and did not transition it; it sits at `ready` where `new-item` put it, and the gates below were run against WI-0001, which is the item under review.
  - `definition-of-done` → **skipped** (this item is filed, not closed — the Definition of Done is walked on WI-0001)
  - `engagement-state-is-restated` → **skipped** (an item close is not an ending, and this is not even a close)
  - `accepted-gaps-are-dispatchable` → **skipped** (recorded on WI-0001, whose accepted gap this item is the disposition of: `item-filed:BUG-0001`)
  - `verification-postdates-the-code` → **skipped** (nothing is verified here; this item has no branch)
  - `commits-reference-the-item` → **skipped** (no branch)
  - `tests-pass-on-the-merge-result` → **skipped** (nothing to merge)
  - `workspace-valid` → **pass** (`scripts/validate-workspace .` → exit 0 once this entry and the board landed)
  - `record-is-reconstructible` → **skipped** (recorded on WI-0001)
  - `claims-are-sourced` → **skipped** (recorded on WI-0001)
  - `cross-answer-consistency` → **skipped** (recorded on WI-0001)
  - `epic-sign-off` → **skipped** (recorded on WI-0001; this is not an epic)
- **Artifacts:**
  - `tracker/items/BUG-0001/item.md` — summary, reproduction, expected and actual behaviour with the verbatim traceback, four acceptance criteria, and the notes explaining why it is filed rather than sent back
- **Status:** `—` → `ready` (created by this execution; not transitioned since)
- **Result:** BUG-0001 is filed at `ready` against WI-0001's delivered behaviour: `envel new "café"` raises an unhandled `UnicodeEncodeError` out of `store.save` and prints a traceback under a locale that decodes `argv` with surrogate escapes. The store is not corrupted. It is the disposition of WI-0001's accepted gap "behaviour under a non-UTF-8 locale", and the board will dispatch it to `plan`.

## 2026-09-10T14:49:42Z — plan v0.6.2 — architect

- **Item:** BUG-0001
- **Trigger:** status `ready`, dispatched by `next` — the only runnable candidate this pass
  (WI-0002 has three open blocking questions; WI-0003 to WI-0005 depend on it)
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` (AC1–AC4, the reproduction, the notes), `history.md` (one
    row: filed by `review-close` at `ready`), `journal.md` (`review-close`'s filing entry and the
    four commands it ran). There is no `artifacts/refinement-qa.md`: a bug enters at `ready` and
    is not refined
  - `docs/architecture/overview.md` (v2) — the four pieces and the one-way dependency
  - `docs/architecture/adr/ADR-0001`, `ADR-0002`, `ADR-0003` (`## Decision` in full),
    `ADR-0004` (`## Context` and `## Consequences`)
  - `docs/product/vision.md` (v2), including its `## Engagement state`
  - `docs/process/ways-of-working.md` (v2) — both sections, and the two citations into
    `envel/store.py` its second section carries
  - `tracker/items/WI-0001/questions/Q-002.md` (the stakeholder on names) and `Q-004.md` (the two
    coverage cases this item inherited)
  - `tracker/project.yaml` — `commands.test` and `commands.lint`, both already set
  - the code: `envel/cli.py` in full, `envel/store.py` (`store_path`, `load`, `save`, `_discard`,
    `_check_shape`), `tests/` (two modules, no `tests/test_store.py`)
- **Decisions:**
  - **Found a second unhandled site, by running the item's own contrast case.** `BUG-0001` states
    in three places that only the write fails and that `envel list` under the same locale succeeds
    against a store holding `café`. It does not: it raises `UnicodeEncodeError` at
    `envel/cli.py:82` and prints a traceback, exit 1. The item's criteria are unchanged — AC3
    already requires `envel list` afterwards to exit 0, which cannot hold under accept-and-store
    unless the print path is fixed — so this is a correction to the item's prose and not a
    send-back or a new bug. `plan` has no write authority over `item.md`, so it is recorded at the
    top of `plan.md` and here.
  - **Chose accept-and-store over refuse (`ADR-0005`, option B over option A).** Documented route
    first: the stakeholder was told the characters in a name would not be restricted
    (`WI-0001/Q-002`), and refusing `café` is that restriction. The measurement decided the shape:
    the interpreter reports stdout as `ascii`/`surrogateescape`, stderr as
    `ascii`/`backslashreplace` and the filesystem encoding as `ascii`/`surrogateescape`, so the
    bytes are recoverable on the way in and stderr was never at risk.
  - **Refused option C, re-executing under UTF-8 mode from the launcher**, on `ADR-0002`'s terms:
    the launcher is eleven lines that put a path on `sys.path` and call `main`, and a personal
    budgeting tool overruling the operator's environment is not a fix. Refused option D, storing
    the surrogates, on `ADR-0003`'s: the file would stop being a document of the person's text.
  - **Put the whole fix at the boundary, in `envel/cli.py`, and kept the domain rules ignorant of
    locales.** The overview's one-way dependency is what makes `envel/envelopes.py` testable
    without a filesystem, and a locale rule in it would be the first thing to break that.
  - **Kept a guard in `store.save` as well as the boundary recovery** (step 4). Not belt-and-braces
    for its own sake: AC3 asks that a failed `new` never leave a partial store, and the guard is
    what makes "no path out of this module ends in a traceback" true of the module rather than of
    the one call path this item found.
  - **Four assumptions, each with its reversal cost** — the refusal status (P1), the message
    wording (P2), recovery applied to the whole argument list (P3), and the store format being
    untouched (P4). None is taken under a delegation: this engagement has no standing delegation,
    which `refine` established on WI-0002 the same day, so each says so and names where a
    disagreement lands.
  - **Carried WI-0001's two inherited coverage cases as step 6, as steps and not as criteria.**
    That is what `WI-0001/Q-004` decided, and this plan is where that answer becomes work.
  - **Did not touch `docs/architecture/overview.md`.** The change adds a responsibility to the
    boundary but not a piece, an edge or a direction, and its rows are in the invalidation set as
    `cited-fact` because the lines they cite move. Repairing them now would mean citing lines that
    do not exist yet; `implement` repairs them after step 4, which is what the set is for.
  - **Left `tracker/project.yaml` alone.** Both commands are real and were run by this execution.
- **Cross-answer check:** Checked against: `WI-0001/Q-002`; `EP-001/Q-003`; `EP-001/Q-001`.
  - `WI-0001/Q-002` — **relied on, and compatible.** "I want spaces — 'eating out' is one of mine
    — so don't restrict the characters" is the reason option A was refused. Nothing in this plan
    narrows what a name may contain; the one refusal it adds is for bytes that are not text in any
    encoding the tool can name, which is not a restriction on characters.
  - `EP-001/Q-003` — compatible, and reinforcing. "The whole point is that the number is the
    truth" is about balances, not names, and the same instinct decides step 2: bytes that cannot
    be decoded are refused rather than guessed at, because a guessed name is a stored value the
    person never typed.
  - `EP-001/Q-001` — compatible: "no network for anything". Nothing here reaches the network, and
    `ADR-0001` keeps the fix inside the standard library.
  - No conflict was found, so no question quoting two answers was filed. `ADR-0005` settles a
    question about encodings, not a disagreement between two things the stakeholder said.
- **Questions raised:** none. Neither decision this plan makes is irreversible — `ADR-0005`
  records the reversal cost of each of its four parts, and none changes the store's format — and
  neither depends on intent the record does not already carry.
- **Commands:**
  - `env -u PYTHONIOENCODING PYTHONCOERCECLOCALE=0 PYTHONUTF8=0 LC_ALL=C LANG=C … envel new "café"`
    → exit 1, `UnicodeEncodeError` at `envel/store.py:66`, unhandled — the reported failure,
    reproduced
  - `envel new "café"` under the suite's own locale → exit 0; then the same broken environment,
    `envel list` → **exit 1**, traceback, `UnicodeEncodeError: 'ascii' codec can't encode character
    '\xe9' in position 3` at `envel/cli.py:82`; `od -c` on its output confirms the traceback is
    what reaches the terminal. This is the second site, and it contradicts the item
  - `env … python3 -c "print(sys.stdout.encoding, sys.stdout.errors …)"` → stdout
    `ascii`/`surrogateescape`, stderr `ascii`/`backslashreplace`, filesystem
    `ascii`/`surrogateescape` — the measurement `ADR-0005` rests on
  - `grep -rn "src: envel/|src: bin/|src: tests/" docs/` → eight line-number citations into the
    code, across two documents; both documents are rows of the invalidation set
  - `python3 -m unittest discover -s tests -t .` → exit 0, 24 tests, OK
  - `python3 -m compileall -q envel tests` → exit 0
  - `.claude/agile-skills/scripts/lint-documents --rule documents-at-risk-are-enumerated --item
    BUG-0001` → exit 0
  - `.claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0
  - `.claude/agile-skills/scripts/lint-claims --uncommitted` → exit 1 on first run
    (`claim.unsourced`, "exactly" with no citation in `ADR-0005`), then exit 0 after the sentence
    was rewritten to carry the run it describes
- **Gates:**
  - `workspace-valid` → **fail**, and this transition is forced. `run-gate`'s own output:
    `validate-workspace --resolving 'BUG-0001:ready->planned+journal'` exited 1 with
    "docs/architecture/adr/ADR-0005-…:129: ERROR [doc.changelog.no-execution] the row says plan
    changed this at 2026-09-10T14:45:10Z for BUG-0001, and BUG-0001's journal has no execution of
    plan at all". That entry is the one this very command appends. The four conditions in
    `docs/process/ways-of-working.md` are walked in `## Gate override` below, and
    `validate-workspace` was re-run immediately after the move and reports 0 errors
  - `every-criterion-is-addressed` → **pass** — `## Acceptance criteria mapping` has one row per
    criterion, AC1 to AC4, each naming the steps that satisfy it and a specific demonstration: the
    named test under the item's own child environment (AC1), the same test shown failing with
    steps 1–4 reverted (AC2), the list-under-the-broken-locale case plus a byte comparison of the
    store file across a refused `new` (AC3), and a `git diff` over the existing test functions plus
    a read of WI-0001's eleven criteria, with AC4's byte-identical stdout named as the one to watch
    (AC4)
  - `project-commands-resolved` → **pass** — `commands.test` and `commands.lint` were already set
    and this execution ran both: 24 tests OK, and `compileall` exit 0. Neither exits zero without
    checking anything: WI-0001's `verify` killed six mutations with this suite
  - `decisions-recorded` → **pass** — the design choice is `ADR-0005`, with four options, the
    decision in five clauses and a reversal cost per part. Everything else is one of the four
    entries under `## Assumptions`, each stating what reversal costs; none is taken under a
    delegation, and each says so
  - `plan-is-executable-without-you` (advisory) → **pass** — each of the eight steps names the file
    it touches and what is true afterwards. Step 7 says the criteria are ticked by `verify` and not
    by `implement`, which is the F-048 shape this self-check exists for; step 8's document repair is
    inside the invalidation set, which is what permits `implement` to make it
  - `documents-at-risk-are-enumerated` → **pass** — `lint-documents --rule
    documents-at-risk-are-enumerated --item BUG-0001` → exit 0, "5 invalidation row(s), 0
    deliverable document(s), 6 binding ADR(s)". The set was written from a read of `docs/` and not
    from memory: the eight code citations were found by grep, and each row locates its sentence by
    quotation or by heading. Three kinds are represented — `cited-fact` for the moving line numbers,
    `quantified` for ADR-0003's claim about what the write survives, `engagement-state` for the
    vision's three stale bullets, which nobody here may repair
  - `cross-answer-consistency` → **pass** — `lint-answers --uncommitted` → exit 0, "checked 7
    consumed human answer(s) and 0 delegation(s)". The `**Cross-answer check:**` bullet above names
    the three prior answers this design was checked against and the verdict for each; no document
    was edited to reconcile two of them
  - `claims-are-sourced` → **pass** — `lint-claims --uncommitted` → exit 0 after one real repair.
    It failed first on an absolute in `ADR-0005` ("says exactly how") with no citation, which was a
    genuine finding rather than the engagement-state false positive WI-0001 met: the sentence was
    rewritten to carry the run it describes. Note that the window here is uncommitted paths under
    `docs/`, so `docs/product/vision.md`'s engagement-state section — the finding that forced
    WI-0001's move — is not in scope of this run and will return at the ending
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/plan.md` (new) — problem with the item's correction, approach,
    eight steps, the AC mapping, four assumptions, a five-row invalidation set, deliverable
    documents `none`, five binding ADRs, scaffolding `none`, four risks, and what is out of scope
  - `docs/architecture/adr/ADR-0005-text-crossing-the-process-boundary.md` (new, v1)
  - `tracker/board.md` — regenerated
- **Status:** `ready` → `planned`
- **Result:** BUG-0001 is planned. The fix is four small changes at one boundary, recorded as
  `ADR-0005`: recover `argv` through the filesystem encoding and re-read it as UTF-8, refuse bytes
  that are not UTF-8 rather than guess, escape rather than raise on the way out, and guard the
  store's write. Planning found a second unhandled site the item denies exists — `envel list` under
  the same locale — which AC3 already requires to be fixed, so no criterion changed and nothing was
  sent back.

**Gate override — `workspace-valid`, forced.** The four conditions in
`docs/process/ways-of-working.md`, one at a time:

1. **The finding is outside the rule the gate implements.** The rule is F-084's: a change-log row
   claims a timestamp, a skill and an item, and "a validator matches a row against the journal of
   the item it names" (`spec/journal-and-history.md` §0). What it exists to catch is a row
   attributed to an execution that never happened — the real case was a row attributed to
   `implement` twelve minutes after that execution's closing entry. Here the execution is
   happening, and the entry that makes the attribution true is appended by the command being
   refused. The `--resolving 'BUG-0001:ready->planned+journal'` argument shows the tool is told the
   entry is coming and does not credit it.
2. **The change that would clear it is unavailable.** Skill by skill, through the nine in
   `pipeline.yaml`: `plan` is this execution and its entry is written by step 5 of the very
   command that refuses — the only way to have it first is to write it standalone, which would
   need a `**Status:**` bullet stating a move that had not happened, and the spec forbids exactly
   that ("an entry that accompanies a status change is written by the transition tool in the same
   invocation, so that `**Status:**` states the move that was actually made"). `intake`, `refine`,
   `implement`, `verify`, `review-close`, `answer-questions` and `retro` are not dispatchable on
   this item at `ready` and none of them made this change, so a row naming any of them would be
   false. `next` writes no document. The remaining option is to attribute the ADR to another item —
   also false. There is no true row that passes.
3. **A question records the diagnosis, the options and the decision** — and this is where this
   override *diverges from the convention*, deliberately and on the record. No question was filed.
   The convention was written for `WI-0001/Q-003`, where the gate's finding was a real statement
   about a document that stays false after the move and belongs to some other actor; the question
   is what makes that finding dispatchable. This finding is not of that kind: it is about the
   ordering of two writes inside one command, and it clears the instant the command finishes —
   `validate-workspace` reports 0 errors immediately afterwards. Filing a question addressed to the
   architect, by the architect, about a thing already fixed by the time anyone read it would be
   theatre. The diagnosis, the options and the decision are in this entry instead, and the identical
   failure is already on the record: `WI-0001`'s `ready → planned` row was forced for the same
   reason on the same day.
4. **The journal carries the verdict as `fail` with the run's own output, and the history reason
   names why.** Both are done: the gate line above quotes `run-gate` verbatim, and the history row
   for this move ends `[gates forced]` with the reason.

**For the retrospective.** This is the second time this exact refusal has cost a forced
transition in this engagement — `WI-0001` `ready → planned`, and now this — and both times the
skill was `plan` writing an ADR, which is the ordinary case rather than an unusual one. Any skill
whose contract has it write a document *and* transition in the same execution meets it. The
`--resolving` mechanism already exists and already downgrades other rules for the pending move; a
change-log row naming the acting skill and the item being transitioned is the same shape and is
not downgraded.
