# Review — WI-0004

## What I examined

- **The diff, hunk by hunk**, over `main..wi/WI-0004` — 4 non-tracker files, +310/−5. Every hunk
  was mapped to an acceptance criterion, a plan step, or one of the three deviations
  `impl-report.md` declares:
  - `recall.py` — the module docstring (three commands → four), `USAGE`/`USAGE_DELETE`
    (plan step 1), `delete_card` (step 2), `_card_number` and `cmd_delete` (step 3), the `main`
    registration (step 4).
  - `tests/test_delete.py` — ten cases (steps 5 and 6).
  - `README.md` — the `### recall delete <card number>` entry, the exit-code row for `1`, and the
    number-reuse paragraph (step 7's three edits).
  - `tests/test_docs.py` — four cases (step 8, and step 7's second half).
  Nothing in the diff serves neither a criterion nor a plan step.
- **The record's mechanics.** `history.md` chains without a gap across eight rows —
  `— → draft → awaiting-answer → draft → ready → planned → in-progress → verifying → in-review` —
  and its last row matches `item.md`'s status. `journal.md` carries eight entries whose
  timestamps and actors correspond one-to-one with those rows. All ten criteria are ticked. The
  item's one question, `Q-001`, is `answered` with `## Consequences` naming files that exist.
- **The reports' declared gaps** — `verify-report.md` `## Not verified, and why` and
  `impl-report.md` `## What I did not do`. Each is judged below under `## Accepted gaps`.
- **The claims audit (D12), from the citations rather than from the prose.** Each absolute claim
  in `docs/` about behaviour this item touched was checked by running the code it points at, not
  by reading the sentence or a neighbouring document:
  - *"`delete` removes one card by its number, immediately and with no confirmation prompt,
    printing what it removed"* [`docs/architecture/overview.md` §2, citing WI-0004 AC2 and
    WI-0004/Q-001] — **true**. Opened `cmd_delete`: nothing reads stdin on any path.
    `verify-report.md` records the run with stdin held open for 30 seconds returning 0.
  - *"surviving cards keep the numbers they had"* [overview, citing WI-0004 AC3 and ADR-0008] —
    **true**. Opened `delete_card`: one `cards.pop(position)` and no write to any other card.
  - *"The next number is still one more than the largest stored, so deleting the highest-numbered
    card frees its number for the next card added"* [overview, citing ADR-0004 and ADR-0008] —
    **true**, and run rather than reasoned: on a three-card store, `recall delete 3` then
    `recall add "die Maus" "the mouse"` printed `Added card 3.` and `recall list` showed
    `3\tdie Maus\tthe mouse`.
  - *"Nothing in the tool does today; there is no history and no second copy of a card"*
    [overview, citing ADR-0004] — **true**. The store written by that run has top-level keys
    `['cards', 'version']` and each card has `['answer', 'due', 'interval', 'number', 'question',
    'result']`. No history, no duplicate.
  - *"a card number naming no card is the other [instance of exit 1]"* [overview §1, citing
    ADR-0005 and ADR-0009] — **true**. `recall delete 9` exited 1.
  - *"Risk: low; nothing in the epic deletes a card"* [`ADR-0004` `## Options considered`,
    option F] — **no longer true**; see finding R1.
- **`README.md`'s worked example, executed verbatim.** `verify` did this and I repeated the
  reasoning against the diff: the example's three blocks match what the tool prints, including
  the deliberate `der Hunt` typo, which is the mistyped card the example is about deleting.
- **The trial merge and its test run** — see D3 and D9.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | Every acceptance criterion checkbox is ticked | **pass** | `grep -c "^- \[x\] AC"` → `10`; `grep -c "^- \[ \] AC"` → `0` |
| D2 | Every ticked criterion cites its evidence in `verify-report.md` | **pass** | `## Criteria` has a row per AC1–AC10, each with the command `verify` ran and its actual output. No row cites `impl-report.md`. Spot-checked three against the reports' own quoted output: AC5's md5 `6fffae2e262d9995c29bdf5a1ac36616` before and after, AC8's four exit-2 runs, AC9's `it is not JSON` message naming the path |
| D3 | All declared gates passed on the **final** state of the code, not an earlier one | **pass** | `implement`'s six gates ran on `0a26e4ae`; `verify`'s six ran on the same commit; the code has not changed since — `check-verify-freshness` reports the branch moved to `5dfc6eb2` but "only the record changed (5 file(s) under tracker/ or docs/)". This review then ran `python3 -m unittest discover -s tests -t .` on the **merge result**, not on the branch: `Ran 101 tests in 7.399s` / `OK`, exit 0 |
| D4 | No open blocking question remains | **pass** | `grep -l "^status: open" tracker/items/*/questions/*.md` → nothing. `Q-001` is `answered`, `answered-by: human` |
| D5 | A journal entry for every execution, and a history chain without a gap | **pass** | eight history rows and eight journal entries, matching in order and timestamp: `answer-questions`, `refine`, `answer-questions`, `refine`, `plan`, `implement`, `implement`, `verify`. `validate-workspace` → `0 errors, 0 warnings` |
| D6 | Every decision that changed the design is in an ADR, cited from the plan or journal | **pass** | the three questions `refine` routed to `plan` are settled in `ADR-0008` (numbers may be reused; schema and `STORE_VERSION` unchanged) and `ADR-0009` (exit `1` widened). Both are named in `plan.md`'s `## Decisions and ADRs` table and in the `plan` journal entry. The three smaller choices `implement` made are declared as deviations rather than smuggled in |
| D7 | Documents the change invalidated have been updated, with a version bump and a change-log row | **pass, with finding R1** | `docs/architecture/overview.md` is at `version: 4`, `updated-for: WI-0004`, with a change-log row for `delete` and the widened exit code. `README.md`'s exit-code row and store section were corrected by this item. The one document not updated is `ADR-0004` — deliberately, and R1 records why that is defensible and where it still bites |
| D8 | Every commit on the branch references the item ID | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → exit 0, `all 7 commit(s) on main..wi/WI-0004 name WI-0004` |
| D9 | The change is merged into the trunk | **pass — as the action immediately following this review's transition** | The procedure requires closing *before* merging, because `commits-reference-the-item` inspects `main..wi/WI-0004` and merging first empties that range. The merge was proved safe first: a detached trial worktree at `main`, `git merge --no-ff wi/WI-0004` → clean, tests green on the result, worktree removed, and `git rev-parse main` confirmed still `6e9e5cc` — the trial moved nothing |
| D10 | `verify` ran **after** the last code change | **pass** | `check-verify-freshness WI-0004 wi/WI-0004` → exit 0. Run, not judged by eye: the report's `Verified-commit: 0a26e4ae...` is behind the branch head, and the gate itself established that every commit since touches only `tracker/` |
| D11 | The review record exists and states what was examined | **pass** | this file; `## What I examined` precedes the verdict and names the diff range, the claims opened, and the commands run |
| D12 | Every claim in `docs/` about the behaviour this item touched is still true; absolute claims carry resolvable citations | **pass, with finding R1** | the six claims listed under `## What I examined` were each checked by opening what they cite and running the code. Five are true; the sixth is R1. `lint-claims --changed-since main` → exit 0 (and it refused this item once already, on four unresolvable citations in `impl-report.md`, which were fixed in `1b1c674` — the gate did its job) |

## Findings

### R1 — `ADR-0004` still says "nothing in the epic deletes a card", and nothing points forward

`ADR-0004` `## Options considered`, option F, reads:

> **F — derive it from the cards present: one more than the largest number stored.** Cost: if
> someone hand-deletes the last card from the file, the next card added reuses its number.
> Risk: low; nothing in the epic deletes a card [src: WI-0001].

The epic now deletes a card, and the reuse it calls a hand-editing curiosity is reachable from
the command line — which this review demonstrated above. `ADR-0004` is `status: current`,
`version: 1`, and carries no pointer to `ADR-0008`.

**Not a send-back, and not an error by `plan`.** This was decided, not overlooked: `WI-0004`'s
`## Notes` says *"`ADR-0004` is left as written — an ADR records what was believed when it was
decided"*, and `ADR-0008` exists precisely to re-weigh option F against the premise this item
removes, and keeps it. Within the ADR genre `## Options considered` is a record of the reasoning
at the time, so the sentence is history rather than a live claim, and `ADR-0008` cites `ADR-0004`.

**What remains, and it is real:** the link runs one way. A reader who lands on `ADR-0004` — a
document marked `current` — reads a false present-tense risk assessment with nothing telling them
it was revisited. That is D12's failure shape exactly: a stale sentence that survives because
each document assumes another one handles it. The cheap fix is a forward pointer in `ADR-0004`
with a version bump and a change-log row, which is what its header is built for. Amending an ADR
is the architect's call and not this skill's, so it is recorded as an accepted gap rather than
performed here.

### R2 — `impl-report.md` overstates what its mutation runs showed (raised by `verify` as F1)

`impl-report.md` attributes its mutation A to AC5 and lists AC5 among the tests its mutations
turned red. `verify` re-ran that exact mutation and the only test that failed was AC6's. I did
not take this from `verify`'s report — `verify-report.md` quotes the run, and the claim is
checkable against `impl-report.md`'s own text, which I read.

The delivered behaviour is correct: AC5 was demonstrated directly, twice, by `verify` and again
in the D2 spot-check. So the defect is in the report's evidence section, not in the code. It does
not fail D3, which asks whether the gates passed on the final code, nor D2, which asks about
`verify-report.md`. It is recorded because an overstated evidence claim in a closed item is
exactly the kind of sentence that gets re-quoted later.

### R3 — AC5's test cannot tell a correct implementation from a crashing one (raised by `verify` as F2)

`test_a_number_that_names_no_card_is_refused_and_changes_nothing` passes against an
implementation that raises `TypeError`, because each of its four assertions holds accidentally:
a traceback exits non-zero, the crash precedes the stdout write, a spurious `save` of an
unmodified document is byte-identical, and `assertIn("9", stderr)` is satisfied by the traceback's
line numbers. `verify` established this by mutation and quoted the traceback.

This is the most useful thing the run produced, and it is worth being plain that it is a real
weakness rather than a curiosity: it is why R2's misattribution could be written without anyone
noticing. The criterion is sound and the code satisfies it, so there is nothing to send back —
but the test protecting AC5 will not protect it against a future change.

**Judged as a maintenance point, not a defect.** I would be comfortable maintaining this code;
I would not be comfortable relying on that one test. The narrow fix — assert `there is no card 9`
rather than the substring `9`, or assert `Traceback` is absent — is recorded in the item's
`## Notes` so it survives the close.

## Accepted gaps

Each of these is written into `item.md`'s `## Notes` by this review, so that it survives the item
being closed. A gap that lives only in a report nobody reopens is not recorded.

1. **AC3 is exercised only on a two-survivor store.** Declared by the plan under `## Risks`, by
   `impl-report.md` under `## What I did not do`, and by `verify-report.md` under `## Not
   verified, and why`. `delete_card` pops by index so position is irrelevant, but that is an
   argument from the code. Accepted: AC3 is worded against that store, and the criterion is met
   as written.
2. **Argument shapes no criterion names** — `01`, `+1`, `" 1"`, `1.0`, and digits from other
   scripts. The plan declared these as a reversible assumption; `verify` exercised only what AC8
   names. Accepted: the plan reasoned about them explicitly, `_card_number` implements what it
   said, and reversing costs one predicate.
3. **R1** — `ADR-0004`'s stale risk line and the one-way link to `ADR-0008`.
4. **R2** — the misattributed mutation claim in `impl-report.md`.
5. **R3** — the weak AC5 test, with the narrow fix named.
6. **Concurrency, interrupted writes, and a filesystem failing mid-write** are unverified.
   `ADR-0004`'s write protocol is inherited unchanged and no criterion of this item touches it.
   Accepted as pre-existing rather than introduced here.

## Verdict

**Accept, and close as `delivered`.**

The change does what all ten criteria ask, verified by commands rather than by assertion, and it
does it in the shape the rest of `recall.py` already has: a pure function over the document beside
`add_card`, a command function beside `cmd_list`, and the same ordering discipline — validate,
load, decide, write — that makes "changes nothing on disk" a property of the structure rather than
of care. The three deviations from the plan are declared, small, and all "how" rather than "what",
and the one that adds behaviour no criterion covers (catching a failing `save`) makes `delete`
consistent with `add` and `review` rather than novel.

Three findings are recorded rather than sent back. None is a failure of this item's criteria:
R1 is a documentation link, R2 is a sentence in a report, R3 is a test that is weaker than the
criterion it guards. All three are written into `## Notes`, which is what makes accepting them
honest rather than convenient.
