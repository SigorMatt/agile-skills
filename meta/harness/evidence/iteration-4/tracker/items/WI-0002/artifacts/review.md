# Review — WI-0002

Reviewed at branch head `73b33091`, against trunk `41eb102d`. Trial merge `2ba79c37`.

## What I examined

**The record, in full.** `item.md` including all ten criteria and the `## Notes` that record what
`refine` settled in each round; `history.md`'s eight rows; `journal.md`'s eight entries end to end
— `intake`, `refine`, `answer-questions`, `refine` again, `plan`, `implement` twice, `verify`;
`plan.md`; `impl-report.md`; `verify-report.md`; and `questions/Q-001.md`, the one question on
this item, answered by the stakeholder.

**The diff, hunk by hunk, not the reports about it.** `git diff main -- recall.py` in full, and
the diffs of `README.md`, `tests/support.py`, `tests/test_store.py`, `tests/test_docs.py` and the
two new test modules. Each hunk was mapped to a plan step or a criterion; the mapping is in
`## Findings`.

**The claims in `docs/`, from their citations (D12).** Twelve absolute claims that this item's
behaviour touches, each decided by opening the thing it cites rather than by reading the
sentence:

| claim | in | what I opened | holds |
|-------|----|---------------|-------|
| exit 0 success, 2 a wrong command line, 1 a store that could not be used `[src: ADR-0005]` | overview §2 | `cmd_review` and my own runs: `--deck german` → 2, a version-3 store → 1, a session → 0 | yes |
| `review` walks the due cards one at a time and records a result for each `[src: WI-0002 AC1; AC2]` | overview §2 | AC1 and AC2 in `item.md`; the `for card in cards:` loop and `record_result` | yes |
| `review` does not decide when a card comes back; it writes a placeholder WI-0003 replaces `[src: ADR-0006; WI-0003 AC2]` | overview §2 | ADR-0006's `## Decision`; WI-0003's AC2, which is the 1/3/7/30 ladder; `record_result`, which writes `when + 1 day` | yes |
| the path is `RECALL_FILE` when set and non-empty, else `~/.recall.json` `[src: ADR-0002]` | overview §3 | `store_path()`, unchanged by this branch | yes |
| the per-card review state and the version-2 shape are ADR-0006's `[src: ADR-0004; ADR-0006]` | overview §3 | ADR-0006's schema block against `STORE_VERSION = 2`, `READABLE_VERSIONS = (1, 2)` and the card `add` writes | yes |
| the store is the only state — no cache, no index, no second copy `[src: ADR-0004]` | overview | every `open(`, `NamedTemporaryFile` and `os.replace` in `recall.py`: one read path, one write-by-rename, no other persistence | yes |
| the session reads standard input a line at a time and a whole session can be driven from a pipe `[src: WI-0002 AC9]` | overview §"reads a stream" | `read_line`'s use of `stream.readline()`; every session in this review was a pipe | yes |
| there is no raw keypress mode, no screen clearing, no cursor control `[src: WI-0002]` | overview §"reads a stream" | `grep` for `termios`, `tty`, `curses`, `getch` and escape sequences in `recall.py` — none present | yes |
| the end of standard input ends a session exactly as `q` does, keeping what was recorded `[src: WI-0002 AC9]` | overview §"reads a stream" | `_await_key` returning `None` for both; and my own runs, which produce identical stores either way | yes |
| dependencies are the standard library only `[src: ADR-0003]` | overview §"why" | the five imports: `datetime`, `json`, `os`, `sys`, `tempfile` | yes |
| the store layer is already separated within the file by the contracts WI-0001 fixed `[src: recall.py]` | overview §"why" | the module: `store_path`, `load`, `save`, `add_card`, `due_cards`, `record_result` sit above the `# --- the commands ---` divider and none of them touches `sys.stdout` or `sys.argv` | yes |
| **"with `review` added the module is roughly 280 lines" `[src: recall.py]`** | overview §"why" | `wc -l recall.py` → **342**; non-blank lines → **274**; statement lines only → 211 | **under one reading, not the other — F1 below** |

**ADR-0004's forward-looking sentence**, because it is the one place a recorded decision could be
contradicted. Line 85 reads "`version` is an integer, `1` for the shape this item delivers.
WI-0003 adds per-card scheduling fields to each card object and bumps it." WI-0002 bumped it
instead. I opened ADR-0006's `## Context`, which meets this head on: ADR-0004 decided that
`version` is the seam through which per-card scheduling state arrives, and this uses that seam
exactly as designed; what was overtaken is a prediction about *which item* would reach it first,
made before WI-0002 was refined to require persisted results. That reasoning is recorded where a
later reader will meet it, so no question was filed and no supersession was needed. Recorded as
an accepted gap below rather than passed over silently.

**The declared gaps**, both lists: `## Not verified, and why` in the verification report (five
entries) and `## What I did not do` in the implementation report (four deliberate omissions and
two things a reader might expect). Each is dispositioned in `## Accepted gaps`.

**The merge**, on a throwaway detached worktree of `main`, with the suite and a smoke run of the
tool on the merge result — not on the branch.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `grep -c '^- \[x\] AC'` → 10; `grep -c '^- \[ \] AC'` → 0 |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | the report's `## Criteria` table has a row per AC naming a command `verify` ran and quoting its actual output. Spot-checked three against the code rather than taking the table's word: AC7's exit 2 with empty stdout, AC8's `das Pferd`/`die Katze`/`der Hund` order, AC10's doubled prompts. No row's evidence is a test name or a line of `impl-report.md` |
| D3 | the declared gates passed on the **final** state of the code | **pass** | `implement` ran all seven on `075e339`, the last code commit. `verify` re-ran tests, lint and the validator itself on `e397490`. Every commit after `075e339` touches only `tracker/` — confirmed by `check-verify-freshness`, which reports "only the record changed (5 file(s) under tracker/ or docs/)" |
| D4 | no open blocking question | **pass** | `questions/Q-001.md` is `status: answered`, `answered-by: human`; no other question exists on the item |
| D5 | a journal entry per execution, history chains without a gap | **pass** | eight history rows — `— → draft → awaiting-answer → draft → ready → planned → in-progress → verifying → in-review` — and eight journal entries whose timestamps and actors match them row for row. The last row's `to` is `in-review`, which is `item.md`'s status |
| D6 | every design decision is in an ADR, cited from the plan or journal | **pass** | ADR-0006 records the `due`/`result` fields, version 2, the read rule for version 1, the day-after placeholder and saving after each card. Cited 12 times in `plan.md` and 16 in `journal.md`. The seven reversible assumptions are in the plan's `## Assumptions` with their reversal cost, which is where assumptions belong rather than in an ADR |
| D7 | documents the change invalidated are updated, with a version bump and a change-log row | **pass, with F1 recorded** | `docs/architecture/overview.md` is at v2 with a change-log row naming WI-0002, and ADR-0006 is at v1 — both written by `plan` before the code existed. I re-checked all twelve of their claims against the delivered code (table above); eleven hold outright and the twelfth is a figure that holds under one reading of "lines" and not another. `README.md` — not under `docs/`, but the only user-facing document — gained the `review` section, the key map, the card-field table and a corrected store example, and its "Not yet built" now names only the ladder |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → `all 9 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0 |
| D9 | merged into the trunk | **pass** | trial merge `2ba79c37` on a detached worktree, suite green on the merge result, trial discarded, `main` confirmed unmoved at `41eb102d`; then the real merge, **`f916a37`**, after the item was closed. The suite was re-run on the merged trunk: `Ran 55 tests`, `OK` |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0002 wi/WI-0002` → exit 0: verified at `e3974907`, branch has moved to `73b33091` but only the record changed. The comparison was run, not judged by how the last commit looked |
| D11 | `review.md` exists and states what was examined | **pass** | this file; `## What I examined` is first and names the artifacts, the diff, the twelve claims and what was opened for each |
| D12 | claims in `docs/` about the behaviour this item touched are still true, checked against the code | **pass, with F1 recorded** | the twelve-row table above. Each was decided by opening the cited thing — the code, the ADR, or the criterion — and not by reading the sentence or a neighbouring document. `lint-claims --changed-since main` → `checked no documents changed since main`, 0 errors: no file under `docs/` changed on this branch, so the automatable half had nothing to check here and the hand audit is the whole of D12 for this item |

## Findings

**Every hunk traces to a plan step or a criterion**, with one exception, which `verify` had
already found:

| file | hunk | serves |
|------|------|--------|
| `recall.py` | `STORE_VERSION` 2, `READABLE_VERSIONS`, the version check and the `due`/`result` validation in `load`, version stamping in `save` | plan step 1, ADR-0006 |
| `recall.py` | `today()`, `add_card`'s two new fields and its new `when` parameter | plan step 2 |
| `recall.py` | `due_cards`, `record_result`, `read_line` | plan step 3, plan step 4 |
| `recall.py` | `cmd_review`, `_await_key`, the `review` dispatch in `main`, `USAGE`/`USAGE_REVIEW`/`NOTHING_DUE`/the key and prompt constants | plan step 5, AC1–AC10 |
| `README.md` | the `review` section, key map, worked example, card-field table, version rule, version-2 store example, revised "Not yet built" | plan step 6, AC2, AC8 |
| `tests/support.py` | `HOME` always replaced; `stdin=` | plan step 7 |
| `tests/test_review.py` | 14 cases | plan step 8 |
| `tests/test_session_parts.py` | 10 unit cases | plan steps 3 and 4 — the plan states unit-level "Afterwards" checks for both and names no file; declared as deviation 2 |
| `tests/test_store.py`, `tests/test_docs.py` | version rule, new fields, README claims | plan steps 1, 2, 7, 9 |

**F1 — "roughly 280 lines" is right under one reading of "lines" and wrong under another.**
`docs/architecture/overview.md` says "with `review` added the module is roughly 280 lines", and
that sentence is the stated reason the store layer stays in `recall.py` rather than moving to a
second module. `wc -l recall.py` is **342**. Non-blank lines are **274**, which is "roughly 280"
to within two percent; statement lines alone are 211. So the figure is accurate under the
non-blank reading and wrong under the raw one, and the document does not say which it means.

I checked this rather than assuming it in either direction, and it changed the outcome: on the
`wc -l` reading alone this would have been a false claim in `docs/` about code this item wrote,
which is a D12 failure and a rejection. It is not one. Under either reading the decision the
sentence supports is untouched — 342 lines is still a module one reader holds — so this is
imprecision, not falsity, and it is recorded rather than sent back. Written into the item's
`## Notes` so it survives the item, because WI-0003 adds the ladder to this same module and will
meet the sentence again with a larger file.

**F2 — `cmd_review`'s `input_stream` parameter is unreachable.** `cmd_review(arguments,
input_stream=None)` widens the signature the plan's interface table fixed. `grep -rn
"input_stream"` finds exactly two hits, both inside the function's own definition: `main` passes
one argument and every test drives the real executable through a real pipe. So it is delivered
code that no criterion covers, no test exercises and no reviewer will look at again. `implement`
declared it (deviation 4) and `verify` recorded it, which is why it is a finding rather than a
defect — the fault would have been leaving it undeclared.

Accepted rather than sent back: it is one keyword argument with a default, it changes no
behaviour, and it makes the session testable in-process, which is a plausible need for WI-0003.
Recorded in the item's `## Notes` with the removal cost, so that if WI-0003 does not use it, it
can be deleted knowingly rather than inherited by default.

**F3 — a `due` that is a string but not a date silently removes a card from every review.**
`verify` reproduced it: a card with `"due": "tomorrow"` is accepted by `load`, sorts above every
`YYYY-MM-DD` value in `due_cards`, and is therefore never due again — while `recall list` still
shows it, so it does not look lost. I confirmed the mechanism in the code rather than taking the
report's word: `load` checks only `isinstance(card["due"], str)`, and `due_cards` compares
strings.

This is reachable through a path the criteria endorse, not a hypothetical: AC8 requires a checker
to hand-edit `due` in the store file, and WI-0001 AC5 exists so that a person can open and edit
it. `verify` was right not to file it as a bug — RB3 requires the expected behaviour to cite
something it contradicts, and ADR-0006 states the `YYYY-MM-DD` format without requiring `load` to
enforce it, so there is nothing to cite. It is also correctly not a send-back: no acceptance
criterion of this item says otherwise.

I am accepting it and recording it, and naming where it should be decided: **WI-0003's refinement
owns this**, because that item writes the same field on the same ladder and inherits the gap.
Written into WI-0002's `## Notes` and into WI-0003's, so that the item that will meet it has it
in front of them rather than in a closed item's review.

**Maintainability, read as someone who will have to keep this working.** Nothing rises to a
defect. Three observations:

- `_await_key` is the right shape. AC5, AC9 and AC10 are three criteria describing one behaviour,
  and putting `q`, end-of-input and an unrecognised line in one loop is why they cannot drift
  apart. The alternative — a check per call site — is the version that eventually disagrees with
  itself.
- `save` mutating its argument (`document["version"] = STORE_VERSION`) is a side effect on a
  parameter, which is usually worth objecting to. Here it is what makes "a version-1 store is
  upgraded in place by the next write" true with no migration, ADR-0006 says exactly that, and
  the only caller discards the document afterwards. Accepted deliberately rather than by not
  noticing.
- The `load` version check runs *after* the `cards` check, so a version-3 document that also
  lacks a `cards` array reports the missing array rather than the version. Both are exit 1 with
  the file untouched, so no behaviour a criterion names is affected. Not filed.

## Accepted gaps

Each is copied into the item's `## Notes`, because a gap recorded only in a report stops being
read the moment the item closes.

1. **Nothing was verified at a real terminal.** Every check, in implementation and in
   verification, drove the session through a pipe. That is the item's own design — AC9 requires
   pipe-drivability and `## Out of scope` excludes anything requiring a terminal — but it means
   no one has confirmed the tool is usable with a person at the keyboard. The mitigation (prompts
   on their own lines, nothing depending on partial-line flushing) is implemented and was read,
   not exercised.
2. **A card answered right comes back tomorrow.** ADR-0006's declared placeholder until WI-0003
   lands. The most likely thing to be reported as a defect by anyone meeting the tool in between;
   `README.md`'s "Not yet built" says so in the user's own terms.
3. **`due` is a bare local date, and a session crossing local midnight sees the date it started
   with.** Recorded in ADR-0006 and the plan's `## Risks`; no criterion asks and nothing defends
   against it.
4. **The write protocol was not re-tested under interruption.** Inherited unchanged from WI-0001
   and re-checked only through its visible effects — a refused store is byte-identical afterwards.
   The same gap was accepted when WI-0001 closed.
5. **ADR-0004's prediction that WI-0003 would bump the store version is overtaken.** Its decision
   — that `version` is the seam — is followed exactly. ADR-0006's `## Context` records this in the
   place a reader will meet it, so no supersession was raised.
6. **F1's imprecise line count, F2's unreachable parameter and F3's non-date `due`**, as above.

## Verdict

**Accepted, merged and closed `delivered`.**

Ten criteria, each demonstrated by a command run against the code rather than by a passing test;
nine negative and boundary conditions triggered, including the cross-item one that mattered most,
where a version-1 store written by WI-0001 is read, reviewed and upgraded in place; twelve mutants
confirming the suite would notice each behaviour going missing. All twelve Definition of Done
criteria pass. Three findings and six gaps are accepted and written into the item's `## Notes`,
and two of them — F3 and the placeholder next-due rule — are also written into WI-0003's, which is
the item that will meet them.

The trial merge into a detached worktree of `main` produced `2ba79c37`, the suite was green on the
merge result and the tool ran on it, the trial was discarded and `main` was confirmed still at
`41eb102d`. The item was closed before the real merge, because `check-commit-refs` reads the
commits not yet on the trunk and merging first would empty that range — `check-commit-refs` was
run once more immediately before the merge and reported all ten commits naming WI-0002.

**The merge is `f916a37`.** The suite was re-run on the merged trunk (`Ran 55 tests`, `OK`) and
the workspace validates there with 0 errors and 0 warnings. This sha is recorded here in a
separate trunk commit, because the close necessarily precedes the merge and so the closing journal
entry cannot name the commit that follows it.
