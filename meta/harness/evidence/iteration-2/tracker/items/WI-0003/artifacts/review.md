# Review — WI-0003

Two rounds. **Round 1** reviewed the change at branch head `22e7313` and accepted everything
except D12, which failed on one document this merge invalidates and that `review-close` may not
edit; it escalated WI-0003/Q-003 and deliberately did not merge. **Round 2** — this one — resumes
at head `ccf4ece`, after `answer-questions` amended ADR-0008 to v2. The code is unchanged between
the two heads: `d870cb1` is still the last commit touching `tidy/` or `tests/`, and the six
commits after it touch only `tracker/` and `docs/`.

## What I examined

### Round 2 (at `ccf4ece`)

- **The record's mechanics, re-counted.** `history.md` now has ten rows and `journal.md` ten
  entries, one per execution — the eight of round 1 plus `review-close` (round 1's escalation) and
  `answer-questions` (Q-003). The chain runs `— → draft → awaiting-answer → draft → ready →
  planned → in-progress → verifying → in-review → awaiting-answer → in-review` without a gap, and
  its last row matches `item.md`'s `status: in-review`. Twelve criteria ticked, none unticked. All
  **three** questions are `answered`, and I opened Q-003's `## Consequences`: it names four paths
  and each contains what it says.
- **The diff since round 1 read it**, `22e7313..ccf4ece`, hunk by hunk. Two commits, no code:
  `8d47a5f` is round 1's own record, and `ccf4ece` is the answer to Q-003 — ADR-0008 v1 → v2,
  Q-003's answer, and one paragraph of `item.md`'s review notes. I read the ADR diff rather than
  the answer's description of it: both `## Decision` citations are replaced by the anchored form,
  "that same `grep`" becomes "that same anchored `grep`", a `## Consequences` bullet is added, and
  the frontmatter and change log are both updated. Nothing in `## Context`, `## Options
  considered` or the decision itself moved, which is what makes this a correction rather than a
  supersession.
- **The full code diff, again, hunk by hunk** — `main..ccf4ece` over `tidy/`: `cli.py` (the
  `--rules` argument, the epilog sentence, and the loader call placed before `os.path.isdir`),
  `planner.py` (`build_plan(folder, ruleset=None)` resolving in the body, the two lookups called
  on the ruleset, and nothing else moved), `rules.py` (`Ruleset`, `BUILT_IN`, `merge`, the two
  lookups carried onto the class verbatim, `DEFAULT_RULES` and `DEFAULT_BANDS` untouched), and
  `ruleset_file.py` (new, the whole of the validation). Every hunk traces to a plan step and an
  acceptance criterion; I found one hunk-level behaviour no criterion covers, which is Finding 2.
  `git diff main..ccf4ece -- tidy/apply.py` is empty, as ADR-0011 forecast.
- **The trial merge, re-done.** `git rev-parse main` → `0a56b7a1…` before;
  `git worktree add --detach /tmp/trial-wi3 main`; `git -C /tmp/trial-wi3 merge --no-ff
  wi/WI-0003` → merge commit `459323d`; **inside the trial**, `python3 -m unittest discover -s
  tests -t . -q` → `Ran 157 tests in 0.159s / OK`, exit 0, and `python3 -m compileall -q tidy
  tests` → exit 0. `git worktree remove --force`; `git rev-parse main` → `0a56b7a1…` again, and
  `git worktree list` shows only the primary. The trunk did not move (F-055).
- **The D12 claims audit, re-run from the citations.** Round 1's table is below and its verdicts
  stand — the code it opened has not changed — but the two rows that this round's edit touches
  were re-decided by running the commands, not by reading the amended sentences:

  | claim | what I opened | verdict |
  |-------|---------------|---------|
  | ADR-0008 `## Decision`: "`tidy/cli.py` imports nothing from `tidy/rules.py`", now cited as `run: grep -nE "^(from\|import).*\brules\b" tidy/cli.py → exit 1, no output` | ran the citation as written | **true, and now reproducible** — exit 1, no output. A reader performing D12's procedure gets what the citation records, and gets it from a check that decides the sentence rather than from a listing of a file that keeps changing |
  | ADR-0008 `## Consequences`, Reversibility: `run: grep -rn "epilog\|description=" tidy tests --include=*.py → exit 0, two hits, both tidy/cli.py` | ran it | true — two hits, `tidy/cli.py:23` and `tidy/cli.py:25`. Untouched by the amendment, and correctly so |
  | ADR-0008's new `## Consequences` bullet: that the amendment was made and why | the ADR's own diff and `tidy/cli.py`'s six import lines | true; and see Finding 3 for one blemish in the change-log row that describes it |
  | ADR-0010: `[bands]` has three fixed keys, so a third band is unrepresentable | `tidy/ruleset_file.py` `BAND_KEYS` (line 22) and `_read_bands` | true |
  | ADR-0010: `optionxform` is `str`, so a destination `Photos` stays `Photos` | `tidy/ruleset_file.py:42` | true |
  | ADR-0010: a rejected rule file exits 2 before the target folder is examined | `tidy/cli.py` `main`, the `load_rules` block above the `os.path.isdir` check | true; and I ran it — a missing `--rules` path over a real folder gives one stderr line and exit 2 |
  | ADR-0011: `build_plan`'s default is `None`, so `cli.py` need not import a table | `tidy/planner.py:27`, and the anchored grep | true |
  | ADR-0011: `apply.py` is not touched | `git diff main..ccf4ece -- tidy/apply.py` → 0 lines | true |
  | `overview.md` v9: "WI-0003 left the guard green because it did not change `DEFAULT_BANDS`" | the `rules.py` diff, and `tests/test_cli.py:15` importing `DEFAULT_BANDS`; `python3 -m tidy --help` still prints "recent or old" | true — the only diff lines naming the two constants are a moved loop line and the new `BUILT_IN` construction |

### Round 1 (at `22e7313`), kept because its evidence is still the evidence

- **The record's mechanics.** Eight history rows, eight journal entries, one per skill execution
  (`intake`, `refine`, `answer-questions`, `refine`, `plan`, `implement` ×2, `verify`). Q-001 and
  Q-002 `answered`, their `## Consequences` naming `item.md` and `artifacts/refinement-qa.md`,
  both of which carry the paragraphs described. Q-002 additionally records a *negative*
  consequence — that ADR-0005 and `README.md` needed no change — which round 1 checked and agreed
  with.
- **The diff, hunk by hunk**, `main..22e7313`: four files under `tidy/` (249 insertions), four
  test files, `README.md` and `docs/architecture/overview.md`.
  - `tidy/rules.py` — `Ruleset`, `BUILT_IN`, `merge`, and the two lookups moved onto the class.
    `DEFAULT_RULES` and `DEFAULT_BANDS` are untouched by the diff, and both lookup bodies are
    carried across verbatim. Plan steps 1–2, ADR-0011.
  - `tidy/ruleset_file.py` — new, plan step 4, ADR-0010. Validation runs in the order the plan
    fixed, and every path raises `RuleFileError` with a collapsed one-line message.
  - `tidy/planner.py` — `build_plan(folder, ruleset=None)` resolving in the body, and the two
    lookups called on the ruleset. Plan step 3. Nothing else in the function moved: the collision
    handling, the `leave` reasons, the per-entry `OSError` boundary and the single clock read are
    byte-identical, which is what keeps ADR-0002, ADR-0005 and ADR-0009 intact.
  - `tidy/cli.py` — three edits: the `--rules` argument, the epilog sentence, and the loader call
    placed before the `os.path.isdir` check. Plan step 5, ADR-0006 and ADR-0010.
  - `tidy/apply.py` — **not touched**; `git diff main..HEAD -- tidy/apply.py` is empty, as
    ADR-0011 predicted.
- **The ADRs the change touches**: ADR-0002, ADR-0005, ADR-0006, ADR-0008, ADR-0009, ADR-0010,
  ADR-0011. Nothing contradicts one.
- **The declared gaps**, both reports: `impl-report.md` `## What I did not do` (four items) and
  `verify-report.md` `## Not verified, and why` (five). Each is judged in §Accepted gaps.
- **The rest of round 1's D12 audit**, unchanged and still true at this head:
  `[types]` values are one path component and keys are lowercased on load (`_read_types`,
  `_has_separator`); `folder_for`/`band_for` carry the same bodies; ADR-0005 §Consequences'
  forecast held, with ADR-0011 carrying the one correction (the lookups becoming methods);
  `overview.md` v9's new paragraphs check out against each cited file, with its version bump and
  change-log row present; and `README.md`'s "Your own rules" section was checked by extracting its
  own `ini` block and **running it**, which produced the redirect and the band rename its prose
  claims, with its quoted error line character-identical to the real one.

## Definition of Done

Round 2's results. Where round 1 differed, the row says so.

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every checkbox ticked | **pass** | `grep -c "^- \[x\] AC" item.md` → 12; `grep -c "^- \[ \] AC"` → 0 |
| D2 | every tick cites evidence in `verify-report.md` | **pass** | all twelve rows name a command `verify` ran and quote its output; the sample folder and rule files were built from the item's preamble, not from `tests/`, so no row cites `impl-report.md` |
| D3 | gates passed on the final state | **pass** | `verify` ran at `d870cb1`, the last code commit; I re-ran `unittest` (157, `OK`) and `compileall` (exit 0) on the merge result `459323d` |
| D4 | no open blocking question | **pass** | all three questions are `answered`. Round 1 recorded this as "pass at the time of the audit, now superseded", because the question it filed was open; Q-003 was answered at `2026-08-27T22:09:33Z` and the item resumed at `in-review` |
| D5 | a journal entry per execution, history chains | **pass** | ten rows, ten entries, listed in §What I examined; the chain has no gap and its last row matches the item's status |
| D6 | design decisions in ADRs, cited from plan or journal | **pass** | ADR-0010 and ADR-0011, both cited in `plan.md`'s "Decisions and ADRs" table and in the `plan` journal entry. Assumptions A1 (`old/old/report.pdf`) and A2 (fractional boundary) are recorded as plan assumptions with their reversal cost, which is the right home for a decision `refine` deliberately left unconstrained |
| D7 | invalidated documents updated, with version bump and change-log row | **pass** | `docs/architecture/overview.md` v8 → v9 (`implement`, WI-0003) and `docs/architecture/adr/ADR-0008…md` v1 → v2 (`answer-questions`, WI-0003). Both carry a change-log row whose top version matches the frontmatter; `README.md` updated for AC12 |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → `all 12 commit(s) on main..wi/WI-0003 name WI-0003`, exit 0 |
| D9 | merged into the trunk | **pass** | trial merge `459323d` clean and green; the item is closed while the branch is still unmerged, and the real `--no-ff` merge follows immediately (§Verdict records the sha). Round 1 recorded this as "not reached" |
| D10 | verification postdates the last code change | **pass** | `check-verify-freshness WI-0003 wi/WI-0003` → exit 0: "verified at `d870cb1`; `wi/WI-0003` has moved to `ccf4ece` but only the record changed (8 file(s) under `tracker/` or `docs/`)". I ran the comparison rather than judging it by how the commits looked |
| D11 | `review.md` exists and says what was examined | **pass** | this document; `## What I examined` is first and covers both rounds — the diff, the record, the trial merge and the claims audit |
| D12 | claims in `docs/` about the touched behaviour are still true | **pass** | the round 2 audit table above, decided by running each citation. Round 1 recorded this as **fail** on ADR-0008's two `run:` citations; that is Finding 1, now closed against the amended ADR and re-checked by running the amended command rather than by reading the amendment |

`claims-are-sourced` was run as well: `lint-claims --changed-since main` → `checked 2 document(s)
/ 0 errors, 0 warnings`.

## Findings

**Finding 1 — ADR-0008's evidence was made unreproducible by this merge. Raised in round 1,
escalated as WI-0003/Q-003, closed in round 2.**

ADR-0008 supported "`tidy/cli.py` imports nothing from `tidy/rules.py`" with a recorded command
and its output, twice: `grep -n "^from\|^import" tidy/cli.py → exit 0, five imports: argparse,
os, sys, .apply, .planner`. This item adds a sixth import, `from .ruleset_file import
RuleFileError, load as load_rules`, whose module name begins with the five letters `rules`. The
claim stayed true and its evidence stopped being reproducible, which `lint-claims` cannot see —
it proves a citation resolves, not that it supports its sentence.

`answer-questions` decided option A and amended both citations in place to
`grep -nE "^(from|import).*\brules\b" tidy/cli.py → exit 1, no output`, bumping ADR-0008 to v2
with a change-log row naming this item. I closed the finding by running the new citation, not by
reading the answer: exit 1, no output. The remedy is better than a repair — the citation is now a
check that fails exactly when someone imports the rule table, which is the event ADR-0008 exists
to prevent, rather than a listing that decays whenever `cli.py` gains an unrelated import.

**Finding 2 — `--rules ""` is silently a no-rules run. New in round 2; accepted, not a
send-back.**

`tidy/cli.py` guards the loader with `if args.rules:`, so an empty string reaches neither
`ruleset_file.load` nor an error path:

```
$ python3 -m tidy /tmp/emptyrules/S --rules ""
tidy: preview only - nothing will be moved. Re-run with --apply to move.
move   budget.csv -> recent/spreadsheets/budget.csv        (exit 0)

$ python3 -m tidy /tmp/emptyrules/S --rules /tmp/emptyrules/absent.ini
tidy: /tmp/emptyrules/absent.ini cannot be used: No such file or directory   (exit 2)
```

What would go wrong, and when: `--rules "$RULES"` with `RULES` unset expands to exactly this, and
the run then sorts by the built-in tables while the user believes their own rules applied. Every
neighbouring mistake — a missing file, a directory, an unparseable file — is a one-line exit 2, so
this is the one input in the feature's vocabulary that fails quietly.

It is **not** a criterion failure, and I checked rather than assumed: AC8's six classes are
properties of a rule *file*, and an empty path names no file; AC1's "no rules" case is about a run
with none supplied, and `tests.test_cli.…test_a_rules_flag_naming_nothing_is_a_no_rules_run`
exercises an empty rule *file*, not an empty path. `plan` did not specify it either way. So it is
an accepted gap rather than a send-back, and it is written into the item's `## Notes` so it
survives this close — the fix, if a later item wants it, is to test `args.rules is not None` and
let `load` report the empty path in the ordinary way.

**Finding 3 — ADR-0008's new change-log row over-escapes the regex it quotes. Cosmetic;
accepted.**

Row 2 describes the amendment as the anchored `grep -nE "^(from|import).*\\brules\\b"` check,
with doubled backslashes, while the two citations it describes carry the single-backslash form.
Nothing downstream reads that cell, and the doubled form is still the same command when pasted
into a shell — `"\\b"` is `\b` after quote removal — so no reader is misled into running something
different. It is recorded rather than repaired because `review-close` may not edit an ADR
(`spec/doc-header.md` §5), and re-suspending a finished item to correct a change-log cell would
cost a full question round trip for a blemish that changes nothing a reader does. If a later
execution edits ADR-0008 for any other reason, this is worth carrying in the same edit.

**No other finding.** I looked for the usual things and did not find them: no duplicated rule that
will drift (the extension index is built once and merged by copy), no error path that swallows its
error (`RuleFileError` carries the operating system's or the parser's own words), no name that
says something untrue, and no hunk serving neither a criterion nor a plan step.

## Accepted gaps

Each is acceptable **and** is recorded in the item's `## Notes`, which this review has extended. A
gap recorded only in a report is one nobody reads again.

1. **`Ruleset` is frozen but its `by_extension` dict is not.** `BUILT_IN.by_extension is
   _BY_EXTENSION` → `True`, and `BUILT_IN.by_extension['.zzz'] = 'x'` succeeds, changing the
   built-in table for the whole process; only rebinding a *field* raises `FrozenInstanceError`.
   Nothing in the codebase does this, and `merge` copies before it updates, so no behaviour is
   wrong today and no criterion is violated. What would go wrong, and when: a future item that
   wants to add a rule "in place" — the obvious way to write it — would silently corrupt every
   subsequent lookup in the same process, which is precisely the global-state failure ADR-0011
   chose option B to avoid. The fix (a `MappingProxyType`, or a `frozenset` of pairs) is a design
   change belonging to `plan`.
2. **`boundary-days = inf` is accepted**, giving one band for everything. AC8 requires rejecting a
   boundary that is "not a positive number of days", and `inf` is a positive number, so this is
   inside the criterion. Declared by `implement`, reproduced by `verify`.
3. **A well-formed but meaningless entry is accepted** — `.csv = .csv` files under a folder called
   `.csv`. `plan`'s Risks section predicted it and called it "odd, not wrong"; the preview shows
   it before anything moves.
4. **An inline `#` is part of a value, not a comment.** `README.md` says so and tells the user to
   put the note on the line above; both modes still agree on the resulting path.
5. **Unexercised: `os.altsep`, and a rule file the process may not read.** `verify` declared both.
   Linux has `os.altsep = None`, and the permission case takes the same `OSError` branch as the
   missing-file and is-a-directory cases, which were exercised. No criterion asks for either.
6. **`tests/test_rules.py` differs from `main`.** AC1 asks that no test be edited to accommodate
   this item. Every removed line there is paired with the identical assertion prefixed `BUILT_IN.`;
   no expected value changed, and the other four pre-existing test files have zero removed lines.
   That is the rename ADR-0011 predicted and `plan` Risk 1 told a reviewer to distinguish from a
   changed assertion. Round 1 checked it line by line and it is a rename.
7. **`--rules ""` is a silent no-rules run** — Finding 2, new in round 2.
8. **ADR-0008's change-log row over-escapes its regex** — Finding 3, new in round 2. Not in the
   item's `## Notes`: it is a blemish in a document, not a property of this item's delivery, and
   the ADR itself carries the correct form in both citations.

## Verdict

**Accepted, closed and merged.** Twelve of twelve Definition of Done criteria pass. The diff maps
hunk-for-hunk onto `plan.md`'s eleven steps and every hunk to a criterion; verification is fresh
against the last code change; the trial merge was detached, clean, and green on the merge result;
`main` was confirmed unmoved before the real merge; and the item was closed while the branch was
still unmerged, so `commits-reference-the-item` had a non-empty range to inspect.

Round 1's single failure, D12 on ADR-0008, is closed against the amended ADR and re-checked by
running the amended command. Two new findings — a quiet `--rules ""` and an over-escaped
change-log cell — are accepted with their consequences written down rather than repaired here:
neither violates a criterion, and neither is `review-close`'s to fix.

Merged into `main` as `82a7d264`, a `--no-ff` merge made immediately after this close; `main`
moved `0a56b7a1` → `82a7d264`. Outcome: **delivered**.
