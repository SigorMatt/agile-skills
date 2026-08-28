# Review — BUG-0005

Two rounds. Round 1 suspended the item on D12 and filed `Q-001`; round 2, below, resumes after
`answer-questions` corrected `ADR-0012` to v2. **Round 2's verdict is accept and merge.** Round 1's
sections are left exactly as they were written — they are what the reviewer believed at the time,
and round 2 says what changed.

## What I examined

- **The record's mechanics.** `history.md` — five rows, chaining `— → ready → planned →
  in-progress → verifying → in-review` with no gap, and the last row matching `item.md`'s status.
  `journal.md` — five entries, one per history row, with matching actors and versions
  (`review-close v0.5.0` filing it, `plan v0.3.1`, `implement v0.2.2` twice, `verify v0.1.4`).
  All three acceptance criteria ticked; `grep -c "^- \[ \]" item.md` → `0`. No question existed on
  the item before this review.
- **The diff, hunk by hunk**, at `git diff main..wi/BUG-0005`: three hunks.
  1. `README.md:38-40`, the exit-status paragraph's third clause → AC1, plan step 2. Checked
     against the plan's verbatim replacement text: identical.
  2. `tests/test_cli.py:1-5`, the module docstring gaining `and BUG-0005 AC3` → declared as
     deviation 2 in `impl-report.md`; it keeps the module's own list of covered criteria true.
  3. `tests/test_cli.py:485-534`, `AllMovesFailExitStatusTests` → AC3, plan step 3. Read line by
     line: `addCleanup(os.chmod, band, 0o700)` is registered **before** `os.chmod(band, 0o500)`,
     so a failing assertion cannot leave an undeletable tree; the probe guard removes its probe
     before skipping; the assertions cover the status, both files still at the top level, neither
     destination folder created, and exactly two failure lines with one naming each file.
     `assertEqual(len(failures), 2)` is an exact count, so a stray failure line would fail the
     test rather than pass it silently.
  Nothing under `tidy/` is in the diff. `git diff main..wi/BUG-0005 --stat` → `README.md | 5`,
  `tests/test_cli.py | 52`.
- **The ADRs the change could contradict.** ADR-0006 (three exit statuses, the CLI boundary),
  ADR-0007 (`"failed"` versus `"fell-back"`), ADR-0009 (a `leave` is not a failure), ADR-0003
  (the fallback), and ADR-0012 (this item's own). The change contradicts none of them: it states
  in prose the predicate ADR-0007 fixed and ADR-0012 chose to keep.
- **The declared gaps** — `verify-report.md` `## Not verified, and why` (five entries) and
  `impl-report.md` `## What I did not do` (six entries). Judged individually below.
- **The D12 claim audit, from the citations rather than from the prose.** ADR-0012 is
  `status: current`, `version: 1`, `updated-for: BUG-0005`, so its absolute claims about exit
  statuses are squarely in D12's scope. Each was checked by opening what it cites:

  | claim in ADR-0012 | what I opened | verdict |
  |---|---|---|
  | "`cli.main` ends with `return 1 if any(outcome.kind == "failed" for outcome in outcomes) else 0`" `[src: tidy/cli.py]` | `sed -n 105,120p tidy/cli.py` | **true** — it is line 114 and it is the function's last statement |
  | "every status the module returns is one of 0, 1 and 2" `[src: run: grep -n "return " tidy/cli.py → exit 0, nine hits: …]` | ran that grep | **true** — nine hits, numeric returns `2, 2, 2, 0, 0` and the final 1-or-0, plus `parser`, `line` and a rendered string, exactly as cited |
  | "a move carried by ADR-0003's fallback is a success that says so" `[src: ADR-0007]` | `tidy/apply.py:72-89` — `_move_without_a_link` returns `Outcome("fell-back", …)` on success | **true** |
  | "a file that was never going to move gets a `leave` line and does not affect the status" `[src: ADR-0009]` | `tidy/apply.py:38-39` skips `action.kind != "move"`; a run with `notes.xyz` exits 0 | **true** |
  | "2 still covers the four ways a run cannot start, including the `--rules` file" `[src: ADR-0006; src: WI-0003 AC12]` | all four triggered during verification, each `EXIT: 2` | **true** |
  | "a script … must count the `could not be moved` lines on stderr" (`## Consequences`, and again in option B's risk) | `grep -c "could not be moved" tidy/apply.py` → `1` of 5 `Outcome("failed", …)` messages; then the all-fail run itself | **FALSE** — see Findings |
- **`docs/architecture/overview.md`**, deliberately not updated by this item. Its exit-status
  sentences (lines 51, 57-61, 67, 133) are about the fallback and the two error boundaries; none
  describes `README.md`'s exit-status paragraph, and `only a "failed" outcome makes the process
  exit non-zero` is still true. D7 holds without a version bump, which is what `plan` predicted.
- **The gate scripts**, run rather than assumed: `check-verify-freshness`, `check-commit-refs`,
  `lint-claims --changed-since main`, `check-epic-signoff`, `validate-workspace`.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `grep -c "^- \[ \]" tracker/items/BUG-0005/item.md` → `0`; AC1, AC2, AC3 all `- [x]` |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | Three rows, each naming a command run by `verify` and quoting its output: AC1 the item's reproduction (`EXIT: 1`, `find` showing both files at the top level), AC2 a word-diff plus seven runs of the tool, AC3 the test under three conditions (`ok`, `skipped`, `FAILED`). No row cites `impl-report.md` |
| D3 | the item's declared gates passed on the final state of the code | **pass** | The branch's only code commit is `05be040`; `implement` ran all seven of its gates there, and `verify` ran its six at `4835edf`, which differs from `05be040` only by tracker files. Nothing has touched `tidy/`, `tests/` or `README.md` since |
| D4 | no open blocking question remains | **fail** | `tracker/items/BUG-0005/questions/Q-001.md`, `blocking: true`, `status: open`, filed by **this execution** against D12 below. It is the mechanism working, not a pre-existing defect: before this review the item had no `questions/` directory at all |
| D5 | a journal entry per execution, and `history.md` chains to the current status | **pass** | 5 history rows, 5 journal entries, actors matching row for row; the last row's `to` is `in-review`, which is `item.md`'s status |
| D6 | every decision that changed the design is in an ADR, cited from the plan or journal | **pass** | The one design decision — keep three exit statuses rather than add a fourth — is ADR-0012, cited from `plan.md` line 24 (`[src: ADR-0012]`), line 119 (`## Decisions and ADRs`) and line 155 (`## Out of scope`), and from `plan`'s journal entry. The three remaining choices are recorded as reversible assumptions A1-A3 with their reversal costs |
| D7 | documents the change invalidated updated, with a version bump and a change-log row | **pass** | The change invalidated none. ADR-0012 was written *for* this item and remains at v1 with its change-log row; `docs/architecture/overview.md` describes modules and boundaries, which this item did not move, and its exit-status sentences were re-read against the code and are still true. A version bump with nothing behind it would devalue every other one |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs BUG-0005 wi/BUG-0005` → exit 0, `all 4 commit(s) on main..wi/BUG-0005 name BUG-0005` |
| D9 | merged into the trunk | **not reached** | Step 7 decided against acceptance before step 8's trial merge, which is the correct order — a failed gate must not be merged over. `main` is unmoved at `5dc1799`, and the branch is intact |
| D10 | `verify` ran **after** the last code change | **pass** | `check-verify-freshness BUG-0005 wi/BUG-0005` → exit 0: *"verified at 4835edfc; wi/BUG-0005 has moved to dd49e595 but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"*. Run, not judged by how the last commit looked |
| D11 | `review.md` exists and states what was examined | **pass** | This file; `## What I examined` is its first section and lists the diff hunks, the ADRs, the claim audit and the scripts |
| D12 | every claim in `docs/` about the behaviour this item touched is still true, checked against the code | **fail** | ADR-0012 (`status: current`, `updated-for: BUG-0005`) tells a reader twice to count `could not be moved` lines on stderr to tell an all-fail run from a partial one. In the all-fail run the ADR is about there are none. Detail in Findings; the six other absolute claims in the same ADR were audited from their citations and all hold |

Eleven criteria examined, ten pass, D9 not reached, **D4 and D12 fail** — D4 as a direct
consequence of the question D12 required.

## Findings

**F1 — ADR-0012 twice recommends counting a stderr line that the run it describes never prints.**
*Blocking. Escalated as `Q-001` to the architect.*

`## Consequences`: "A script that wants to distinguish 'nothing moved' from 'some moved' must
count the `could not be moved` lines on stderr rather than read the exit status." And in
`## Options considered`, inside the rejection of option B: "a script that cares can count the
`could not be moved` lines on stderr".

`tidy/apply.py` appends five distinct `Outcome("failed", …)` messages and only one of them
contains that string — the `shutil.move` failure at line 86. `grep -c "could not be moved"
tidy/apply.py` → `1`. The all-fail run fails at `os.makedirs` (line 46) and emits
`could not create the folder for …; <file> was left where it is` instead. Run during this review:

```
$ python3 -m tidy .harness/rv/allfail --apply 2>err.txt; echo "EXIT: $?"
EXIT: 1
$ grep -c "could not be moved" err.txt
0
```

Exit 1, nothing moved, and zero matching lines — so the advice returns the inverse of the truth in
exactly the scenario the ADR exists to describe. The second occurrence is load-bearing: it is part
of why option B (a fourth exit status) was rejected, so the recorded case for decision A rests on
a workaround that does not exist as written.

Not repaired here. Correcting a factual clause of a `status: current` ADR in place is established
practice (BUG-0002/Q-002), but the second occurrence sits inside a rejected option's rationale,
and reweighing that touches the reasoning behind the decision — which is the architect's. The
decision itself is not in question, and BUG-0005's delivered README clause is unaffected: it says
nothing about stderr.

**F2 — the new test class's docstring quotes the README clause verbatim, and nothing makes it
drift-proof.** *Non-blocking. Accepted; recorded below.*

`AllMovesFailExitStatusTests`'s docstring reproduces "whether that is one of them, some of them, or
all of them". If the paragraph is reworded again the docstring silently goes stale. This project
has already been bitten by a stale description once (BUG-0003) and answered it in
`test_help_says_age_chooses_the_band_and_names_every_band` by deriving the expectation from the
table the tool routes by rather than copying it. That pattern does not transfer here — the test
asserts behaviour, not prose, and deriving a docstring from `README.md` would be worse than the
problem. The cost of the gap is a comment a future reader may find out of date, not a test that
passes wrongly.

**F3 — `README.md`'s 0 clause and a failing run share the phrase "left where they are".**
*Non-blocking. Examined and not filed; recorded below.*

Raised by `verify` in `verify-report.md` `## Defects found` and re-checked here. I reach the same
conclusion: the 0 clause is governed by "on success", its "including" items elaborate what success
is, and nothing in it is false. It is also not fixable by this item — AC2 and `plan.md` step 2 both
forbid touching that clause, because BUG-0001 AC2 and WI-0003 AC12 are verified against it.

## Accepted gaps

Recorded here and, on close, in the item's `## Notes`, so that they survive the report.

1. **The clause's readability, including its internal em dash** (`impl-report.md`
   `## Deviations`). The delivered sentence separates its three top-level clauses with em dashes
   and the new third clause contains a fourth. It resolves — "whether" cannot open an exit-code
   clause — and it is the architect's chosen wording, delivered verbatim as the plan required. AC1
   asks only that a reader can predict the code, which they can.
2. **F2**, the docstring quote that can drift.
3. **F3**, the "left where they are" phrase shared between the 0 clause and a failing run's
   stderr. Provenance if anyone does file it: the phrase entered at `1156654` (BUG-0004), the
   message at `49be3d7` (WI-0001), so it belongs to neither alone.
4. **Everything under `## Not verified, and why` in `verify-report.md`** — behaviour under root or
   on a filesystem that does not enforce mode `0o500` (which the criteria themselves make
   conditional), and the declaration that implementation and verification ran in the same session.
   The second is a property of how this pipeline is driven, not a choice made by any skill here,
   and it is right that it is written down rather than left to be assumed.

None of these four is a reason to reject. All four are reasons to write something down, which is
what this section is.

## Verdict

**Suspended, not rejected and not accepted.** The change is good and I would merge it; the ADR it
produced is not yet true. `Q-001` is open to the architect, the item is at `awaiting-answer` with
`resume-to: in-review`, and `main` is unmoved at `5dc1799`.

Deliberately **not** done: no trial merge (step 8 follows an acceptance, and D12 failed at step
7), no edit to ADR-0012, and no send-back to `in-progress` — `implement` does not own ADRs, and
there is nothing wrong with the code or the README clause it delivered.

When `Q-001` is answered and its consequence has reached ADR-0012, this review resumes at step 8:
trial-merge into a detached worktree, confirm `main` unmoved, close, then merge. D1-D3, D5-D8,
D10 and D11 are established at `dd49e595` and need only re-confirming for anything the answer
changes.

---

# Round 2 — resumed after `Q-001` was answered

`Q-001` was answered by `answer-questions` at 2026-08-28T13:41:30Z and `ADR-0012` is at **v2**.
This round re-does what the answer touched, re-runs every gate on the current head
(`eb4a32b`), and takes the decision round 1 deferred.

## What I examined — round 2

- **The answer itself**, `questions/Q-001.md` `## Answer` and `## Consequences`. It did not take
  the wording round 1 recommended, and said why: the review's own proposed replacement — "count
  the failure lines `tidy` prints on stderr" — is false in a second way round 1 did not test. That
  is a correction to this review and it is accepted; the evidence is below, gathered here rather
  than read from the answer.
- **`ADR-0012` v2, both corrected sentences, audited from their citations** — the same way round 1
  audited v1, and against the code rather than against the answer that produced them:

  | claim in ADR-0012 v2 | what I opened or ran | verdict |
  |---|---|---|
  | "No phrase runs through all five of `apply_plan`'s failure messages — `was left where it is` is in three of them and `could not` in three, and the two sets are not the same three" | `grep -n` for both phrases in `tidy/apply.py`: `was left where it is` at `:46, :55, :80`; `could not` at `:46, :67, :86`; the five `Outcome("failed", …)` messages read in full | **true** — three and three, sharing only line 46, and no phrase occurs in all five |
  | "the failure lines arrive interleaved with the banner and with ADR-0003's fall-back line, which reports a *success*" | forced the mixed case here — `recent/documents` at mode `0500` and `os.link` monkeypatched to raise `OSError(18)` | **true** — three `tidy: ` lines for a run in which *one of two* files moved: the banner, `doc.pdf could not be moved to …`, and `photo.jpg was moved … without a hard link`. A line count returns 3 for a half-successful run, which is why round 1's own suggestion had to be rejected |
  | "stdout carries one `move` line per intended move, printed before anything is attempted" | `tidy/cli.py` — the `for action in actions` write loop precedes the `apply_plan` call; confirmed on both runs below | **true** |
  | "every source named in a `move` line that is still where it was is a file the run did not move away, and if that is all of them, nothing moved" `[src: run: … mode 0500 → exit 1 …]` | rebuilt the all-fail run: `python3 -m tidy .harness/rv2/allfail --apply` | **true** — exit 1, two `move` lines on stdout, `doc.pdf` and `photo.jpg` both still at the top level, and `recent/` still empty. The cited run reproduces exactly as cited |
  | "The one case that reading does not distinguish is the failure in which a copy reached the destination and the original could not be removed" | `tidy/apply.py:60-68` — the `os.unlink` failure, `Outcome("failed", "%s was copied to %s but the original could not be removed: %s")` | **true**, and it is the honest caveat: that file is still where it was and a copy did arrive |
  | option B's risk: "the same growth ADR-0006 declined for the unusable-target case — 'the contract grows faster than the tool'" | `docs/architecture/adr/ADR-0006-…md:51-52` | **true** — quoted word for word from option B's risk line there |
  | option B's risk: a workaround exists but "is dearer than reading a status: it compares stdout's `move` lines with the filesystem afterwards" | the two runs above | **true**, and it is the same observable `## Consequences` sets out, so the two sections now agree |

  The six claims round 1 audited in v1 are untouched by the edit and were re-read to confirm that:
  the `cli.main` last-statement quote, the `grep -n "return "` citation, the fall-back claim, the
  `leave` claim, and the four-ways-to-exit-2 claim all still stand as round 1 recorded them.
- **`docs/architecture/overview.md`**, re-read rather than assumed unchanged since round 1: its
  exit-status sentences (`:57-61`, `:67`, `:133`) are about the two error boundaries and about
  `"failed"` versus `"fell-back"`, and `only a "failed" outcome makes the process exit non-zero`
  is still exactly what `tidy/cli.py`'s last statement does. No version bump is owed.
- **One further claim, found by the architect while answering and handed to this round in
  writing** — `ADR-0006:26-29`. Examined and **not** filed; see finding F4.
- **The diff again at the current head**, `git diff main...wi/BUG-0005`: the three code hunks round
  1 read are byte-identical, and the only new content is `docs/architecture/adr/ADR-0012-…md`
  (v1 → v2) plus tracker files. Nothing under `tidy/` in the diff.
- **The gate scripts, re-run on `eb4a32b` rather than trusted from round 1** —
  `check-verify-freshness`, `check-commit-refs`, `lint-claims --changed-since main`,
  `check-epic-signoff`, `validate-workspace`, and the suite on the trial merge result.

## Definition of Done — round 2

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `grep -c "^- \[ \]" tracker/items/BUG-0005/item.md` → `0`; AC1, AC2, AC3 all `- [x]`. Unchanged since round 1 and re-checked |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | Three rows, each naming a command `verify` ran and quoting its output. Unchanged since round 1 and re-checked |
| D3 | the item's declared gates passed on the final state of the code | **pass** | The branch's only code commit is still `05be040`; nothing has touched `tidy/`, `tests/` or `README.md` since. The three commits added after round 1 (`de18164`, `eb4a32b` and this round's) are tracker and `docs/` only, and the suite was re-run on the merge result — 158 tests, `OK` |
| D4 | no open blocking question remains | **pass** | `Q-001` is `status: answered`, `answered-by: answer-questions`, `answered-at: 2026-08-28T13:41:30Z`, with a `## Consequences` naming three files, each opened and confirmed. It is the only question on the item. Round 1's fail is closed |
| D5 | a journal entry per execution, and `history.md` chains to the current status | **pass** | 7 history rows and 7 journal entries after this execution, actors matching row for row; before it, 6 and 6, with `answer-questions v0.3.1` added at 2026-08-28T13:43:06Z |
| D6 | every decision that changed the design is in an ADR, cited from the plan or journal | **pass** | ADR-0012, cited from `plan.md` lines 24, 119 and 155 and from `plan`'s journal entry. The v2 correction changed no decision — its change-log row says so, and option B stays rejected |
| D7 | documents the change invalidated updated, with a version bump and a change-log row | **pass** | `ADR-0012` v1 → **v2**, `updated-by: answer-questions`, `updated: 2026-08-28T13:39:28Z`, change-log row 2 present and specific about what was wrong. `overview.md` re-read and owed nothing |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs BUG-0005 wi/BUG-0005` → exit 0, `all 6 commit(s) on main..wi/BUG-0005 name BUG-0005`; run before the merge, while that range was still non-empty |
| D9 | merged into the trunk | **pass** | Trial-merged into a detached worktree at `main` (`5dc1799`): merge result `730f2c00`, suite green there. `main` confirmed still `5dc17990` after the trial worktree was removed. The real merge follows this close, in step 8's order, and its sha is recorded in the journal entry |
| D10 | `verify` ran **after** the last code change | **pass** | `check-verify-freshness BUG-0005 wi/BUG-0005` → exit 0: *"verified at 4835edfc; wi/BUG-0005 has moved to eb4a32bf but only the record changed (8 file(s) under tracker/ or docs/), so the verification still covers the code"*. Run on this round's head, not carried over from round 1 |
| D11 | `review.md` exists and states what was examined | **pass** | This file, both rounds; `## What I examined — round 2` precedes this table |
| D12 | every claim in `docs/` about the behaviour this item touched is still true, checked against the code | **pass** | The seven-row audit above, each row decided by opening the cited code or by running the cited command. Round 1's F1 is closed against a corrected document that was checked rather than taken on trust — including rejecting round 1's own proposed replacement. F4 below is the one remaining candidate and is judged not a defect, with the reasoning recorded |

Twelve criteria, twelve passes.

## Findings — round 2

**F1 — closed.** ADR-0012 v2 no longer tells anyone to count a line that is not printed. The
correction is not the one this review recommended, and the reason is a finding against round 1:
"count the failure lines `tidy` prints on stderr" is also false, because no phrase runs through
all five failure messages and the failure lines share stderr with the banner and with ADR-0003's
fall-back line — which reports a **success**. Round 1 checked that its target string was absent
and did not check that its proposed replacement was present. The mixed run above is the
demonstration: three `tidy: ` lines for a run in which one of two files moved.

**F4 — `ADR-0006:26-29` paraphrases `README.md`'s exit-status contract in words `README.md` no
longer uses.** *Non-blocking. Examined and not filed; recorded below.*

Found by `answer-questions` while auditing ADR-0012 and handed to this round in `Q-001`'s
`## Consequences` with both readings, rather than edited on the architect's own judgement. The
sentence: "`README.md` states the exit-status contract — 0 on success including nothing to do, 2
when the named folder does not exist or is not a folder, 1 when some file could not be moved while
others were `[src: README.md]`". Neither half matches `README.md` today — the exit-2 half stopped
matching when BUG-0001 rewrote that clause, the exit-1 half when this item rewrote its own.

It is not a defect, and the paragraph settles it itself. The sentence does not end there: it
continues "— and the current exit 1 contradicts it, because no file failed to move; nothing was
even planned", which is the BUG-0001 defect that ADR-0006's own decision removed. A reader cannot
take the paragraph as a description of today, because its conclusion is a defect this ADR fixed;
it is `## Context` narrating the world as it stood when the decision was taken, which is what
`spec/doc-header.md` §4 preserves and what an ADR's context is for. The citation names the
document that was being quoted, and that document still exists. Compare BUG-0004/Q-002, which
corrected ADR-0009's citations precisely because they were *pointers a reader follows*, not a
record of a past belief.

What would change this verdict is a project convention that ADR contexts be written in the past
tense. That is a `ways-of-working` question, not one item's, and no such document exists yet.

## Accepted gaps — round 2

Round 1's four stand, and are written into the item's `## Notes` on close along with this fifth:

5. **F4** — `ADR-0006:26-29`'s paraphrase of a `README.md` clause this item reworded. Judged
   historical context rather than a live claim, for the reason above. Provenance if anyone
   disagrees: the exit-2 half went stale at `068cecd` (BUG-0001), the exit-1 half at `05be040`
   (this item).

## Verdict — round 2

**Accepted and merged.** Twelve of twelve Definition of Done criteria pass on the final state.
The change is still what round 1 approved — one clause of `README.md` and one regression test,
nothing under `tidy/` — and the artifact that failed round 1 is corrected, re-audited from the
code, and now says something a reader can act on. The trial merge was detached, produced
`730f2c00` with 158 tests green, and `main` was confirmed unmoved at `5dc17990` before this close.
The real merge is `10db1f64`, made after it; the suite was re-run on the merged trunk — exit 0,
`Ran 158 tests`, `OK` — and `compileall` exits 0 there. (This paragraph's last two sentences were
completed after the merge; nothing else in the round-2 sections changed.)
