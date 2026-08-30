# Review — WI-0001

## What I examined

**The record, in full.** `item.md` (nine criteria, all ticked, plus the out-of-scope list and the
notes); `history.md` (six rows, chaining without a gap, last row matching the status);
`journal.md` (all eight entries, read end to end — `intake`, `answer-questions`, `refine`, `plan`
twice, `implement` twice, `verify`); `plan.md`; `impl-report.md`; `verify-report.md`. The item has
no `questions/` directory contents, so there was nothing to check for open questions.

**The diff, hunk by hunk — not the reports about it.** `main..wi/WI-0001`, ten code and document
files. Every hunk was traced:

| file | serves | verdict |
|------|--------|---------|
| `recall/deck.py` | plan step 2; AC9 (`Deck.add` appends unconditionally) | clean. No filesystem reference, which is the rule `overview.md` gives it — checked by `grep`, not assumed |
| `recall/store.py` | plan step 3; AC4, AC5, AC7, AC8 | clean, with one finding below. The `os.replace` write and the raising `load` are the two clauses the plan called load-bearing, and both are present as designed |
| `recall/cli.py` | plan step 4; AC1, AC2, AC3, AC6, AC8 | clean, with one finding below. The blank check genuinely precedes `store.deck_path()`, so AC2's "byte-identical" holds by construction rather than by luck |
| `bin/recall`, `recall/__main__.py` | plan step 5; ADR-0005 §1 and §3 | clean. No logic in either, as ADR-0005 requires |
| `tests/support.py`, `test_add.py`, `test_list.py`, `test_storage.py` | plan steps 1 and 6 | clean. Nine acceptance tests via subprocess, five unit tests with the path passed explicitly |
| `docs/process/using-recall.md` | plan step 7; AC7(a) | one citation repaired during this review — see `## Findings` |

Four functions exist that `plan.md` does not name — `build_parser`, `_report_unreadable`,
`_card_from`, `_card_to_entry`. Each implements a contract the plan does state. **No unrequested
scope was found.**

**No contradiction with any ADR.** Checked against all five: `ADR-0001` (one executable,
subcommands, `add` taking options, exit codes carrying the outcome), `ADR-0002` (`rung` and `due`
written, no ease factor), `ADR-0003` (standard library only — no third-party import appears
anywhere in `recall/`), `ADR-0004` (path, JSON shape, `version` from the first write, atomic
write, refuse-do-not-repair, absent ≠ unreadable), `ADR-0005` (`bin/recall`, no install step).

**The claims audit (D12), done from the citations rather than from the prose.** Each absolute
claim in the documents this item touched was checked by opening what it cites and, where the
claim is about behaviour, by running the behaviour:

| claim | cites | how I checked it | verdict |
|-------|-------|------------------|---------|
| "works from a checkout with nothing installed but Python 3" | `ADR-0003` | opened ADR-0003 §1; ran the whole suite and both gate commands with no third-party package | true |
| "no install step, no virtual environment, no package to fetch" | `ADR-0005` | opened ADR-0005 decision A; ran `recall` with only `PATH` exported | true |
| "`python3 -m recall` takes the same subcommands" | `ADR-0005` | opened §3; ran `python3 -m recall list` → exit 0 | true |
| "both sides required, neither blank, exits non-zero" | `WI-0001 AC2` | opened AC2; ran all six refusal cases | true |
| "the same question may be added twice" | `WI-0001 AC9` | opened AC9; added a duplicate question | true |
| "one line per card, in the order added, each side exactly as typed; empty deck says so at exit 0" | `WI-0001 AC6` **only** | opened AC6 — it supports the last clause and none of the first three | **citation insufficient; claim true.** Repaired, see `## Findings` |
| "one file, under your home directory" / "not under `/tmp`…, still there after a reboot" | `ADR-0004`, `WI-0001 AC7` | opened both; computed `deck_path()` against the ambient home; `find`ed the created files | true |
| "no flag, no environment variable, no configuration file" | `ADR-0004` | opened §1; `grep`ed `store.py` for `environ`/`getenv`/`XDG`/`argv` — no code match | true |
| "will not repair it and will not replace it… bytes left exactly as they were" | `ADR-0004`, `WI-0001 AC8` | opened §5 and AC8; ran six damage kinds × two subcommands | true |
| the quoted example error message | — | reproduced it: wrote `{` into a deck and ran `recall list`. Output matches the documented text character for character, modulo the path | true |
| "writes go through a temporary file and an atomic rename" | `ADR-0004` | opened §4; read `save` in `store.py` — `tempfile.mkstemp` in the destination directory, then `os.replace` | true |
| "`add` already records what the scheduler will need" | `ADR-0002` | opened ADR-0002; read the stored JSON — `rung: 0` and an ISO `due` are present | true |
| `overview.md`: "`store.py` never prints" | `ADR-0004` etc. | `grep`ed `store.py` for `print`/`sys.stdout`/`sys.stderr` — only a docstring match | true |
| `overview.md`: "`deck.py` never touches the filesystem" | — | `grep`ed `deck.py` for `open`/`pathlib`/`os.`/`Path` — no match | true |
| `overview.md`'s file tree | — | `ls`ed all five paths | true |

**The merge result, not just the branch.** Trial-merged into a **detached** worktree of `main` and
ran both project commands there.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `grep -c "^- \[x\] AC"` → 9; `grep -c "^- \[ \] AC"` → 0 |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | its Criteria table has nine rows (AC7 split into three), each naming a command and quoting actual output. No row cites `impl-report.md` and no row's evidence is "a test passes" — which is the failure mode this criterion exists for |
| D3 | declared gates passed on the **final** state | **pass** | `implement` ran its eight on the branch head; `verify` re-ran `tests-pass` and `lint-clean` itself on `7c552ef`; this review ran both again on the **merge result** (`Ran 16 tests ... OK`, exit 0; `compileall` exit 0). Three independent runs, the last on what the project actually gets |
| D4 | no open blocking question | **pass** | `tracker/items/WI-0001/questions/` is empty — no question was ever filed on this item |
| D5 | a journal entry per execution; history chains | **pass** | six history rows (`intake`, `refine`, `plan`, `implement`, `implement`, `verify`), last row `verifying → in-review` matching `status: in-review`. Eight journal entries — the two extras are `answer-questions`, which propagated an epic answer without a status change, and `plan`'s own append-only correction recording a gate it had omitted. Every history actor has an entry |
| D6 | design decisions in ADRs, cited from plan or journal | **pass** | `ADR-0003`, `ADR-0004`, `ADR-0005` written by `plan` and cited in `plan.md` `## Decisions and ADRs` with the route for each; `ADR-0001` and `ADR-0002` read, not revisited, and said so. No decision in the diff is absent from an ADR |
| D7 | invalidated documents updated, with a version bump and change-log row | **pass** | `docs/process/using-recall.md` v1 → **v2** in this review, with a change-log row, for the citation repair below. `docs/architecture/overview.md` v1 was checked against the code and **not** invalidated — its two behavioural rules were verified by `grep` and its file tree by `ls`. No other document makes a claim this item's behaviour touches |
| D8 | every commit references the item ID | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, `all 8 commit(s) on main..wi/WI-0001 name WI-0001` |
| D9 | merged into the trunk | **pass** | trial merge into a detached worktree of `main` produced `a24ded8`, clean, with both commands green on it. `main` was `5e92294` before the trial and `5e92294` after — the trial published nothing. The real merge is performed immediately after this close, in the order the procedure requires: `commits-reference-the-item` reads `main..branch`, which merging empties, so closing must come first. The merge commit's sha is recorded in this item's journal |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0001 wi/WI-0001` → exit 0: *"verified at 7c552ef6; wi/WI-0001 has moved to 45671364 but only the record changed (10 file(s) under tracker/ or docs/), so the verification still covers the code"*. Run, not eyeballed — the code has not moved since verification and the commits since are `tracker/` and `docs/` only |
| D11 | `review.md` exists and says what was examined | **pass** | this document; `## What I examined` is first and lists the artifacts, the diff files, the five ADRs, the fifteen claims and what was opened for each |
| D12 | claims in `docs/` about the touched behaviour are still true; new absolutes carry a resolvable citation | **pass, after one repair** | the fifteen-row table above — every claim checked by opening its citation and, where behavioural, by running it. Fourteen true and correctly sourced; one true but under-cited, repaired in place. `lint-claims --context work-item --changed-since main` → exit 0 over a scope that could see something: *"1 document(s) in 1 path(s) differ from main"* |

## Findings

**1. A sentence in `docs/process/using-recall.md` made four claims and cited the source for one.**
*Repaired, not sent back.* The `## Reading the deck back` paragraph read "One line per card, in
the order they were added, each side shown exactly as you typed it. With no cards yet, it says the
deck is empty and exits successfully — that is not an error `[src: WI-0001 AC6]`." AC6 supports
only the final clause. A reader following the citation to check "in the order they were added"
would not find it there.

All four claims were verified true against the code during this review — one line per card and
insertion order by running `recall list` after three adds, verbatim text with `cat -A`, the empty
case against a fresh home. So this is the case `spec/doc-header.md` §4b and step 9b describe: a
true claim whose source is wrong, which has a repair rather than being a defect or an accepted
gap. The citation was split — `plan.md` for the line format, `ADR-0004` for the order, `AC3` for
the verbatim text, `AC6` for the empty case — the sentence itself was left alone, and the document
went to v2 with a change-log row. No decision changed, so nothing is superseded. This is a
document this item created, not a standing ADR, so no `## Corrections` section applies.

**2. A third reproduction of `BUG-0001`, found in the diff and the only one that fails quietly.**
*Added to the existing bug; not a send-back.* `store.load` catches `NotADirectoryError` alongside
`FileNotFoundError` and returns an empty `Deck` for both. They are not the same condition. With a
*file* where `~/.local/share/recall` should be, `recall list` reports an empty deck and **exits
0**; the following `recall add` raises `FileExistsError` from `mkdir`. `ADR-0004` §6 draws exactly
the line this blurs — "absent is not the same as unreadable" — and this is the one place in the
code that crosses it.

It was added to `BUG-0001` as reproduction C rather than filed as `BUG-0002`, because it shares
`BUG-0001`'s root cause: the `OSError` family is unhandled at the `cli.py` boundary. One fix
closes all three and one verification covers them. It was given its own acceptance criterion on
that bug, because a fix that merely quietens `add`'s traceback would leave C's actual failure —
a person being told they have no cards — in place.

**Not a send-back of WI-0001**, by the same test `verify` applied: AC8 requires the deck *file* to
exist, and here it does not; AC5 describes an absent parent, and here the parent is present and is
the wrong kind of thing; AC6 is arguably satisfied, since there are no cards and the tool says so.
No criterion of this item says any of it should be different.

**3. Nothing else.** No hunk contradicts an ADR. No error path swallows an error — the one that
could, `store.save`'s `except BaseException`, unlinks the temporary file and re-raises, and the
deck is only ever reached through the rename, so the comment claiming the deck is untouched is
accurate. No name says something untrue. The `try/except DeckUnreadable` block appears twice, in
`cmd_add` and `cmd_list`, which is duplication I looked at and accepted: `plan.md` specifies it
("caught in exactly one place, at the top of each `cmd_*`"), two call sites is where the
alternative costs more than it saves, and `BUG-0001`'s fix will touch both anyway.

## Accepted gaps

Each was declared in `verify-report.md` `## Not verified, and why` and judged acceptable here.
**All three that could otherwise be forgotten are now written into `item.md` `## Notes`**, because
nobody reads a verification report after an item closes.

| gap | decision | where it now lives |
|-----|----------|--------------------|
| `python3 -m recall` works but no criterion covers it and no test exercises it | accept — adding a criterion is `refine`'s work, adding an unrequested test is scope | `item.md` `## Notes` |
| `bin/recall` is outside `commands.lint`'s two directories | accept — every acceptance check executes it, so a syntax error fails loudly; the gate simply does not see it | `item.md` `## Notes` |
| concurrency never exercised | accept — unspecified and out of scope; `os.replace` is about interrupted writes, not simultaneous ones | `item.md` `## Notes` |
| `commands.lint` is a syntax check and proves little | accept — already recorded in `ADR-0003` §3 consequences, which says so plainly | `ADR-0003`, no new record needed |
| AC7 not tested by rebooting | accept — AC7 was deliberately written to be decidable without one, and was decided the three ways it specifies | the criterion itself |
| `rung` and `due` not read back | accept — by design; nothing in this item consumes them | `item.md` `## Notes`, already there from refinement |

`$TMPDIR` being unset on this machine made one clause of AC7(c)'s check vacuous. Recorded rather
than accepted as a gap: the `/tmp` and `/var/tmp` clauses were not vacuous, and the criterion's
substance — the path is under the home directory — was checked directly.

## Verdict

**Accept.** All twelve Definition of Done criteria pass, one after a repair made here. The change
does what the nine criteria asked, in a way this project should live with: the two decisions the
plan identified as load-bearing are present as designed, the module boundaries `overview.md`
declares are real and were checked rather than assumed, and no hunk exists that a criterion or a
plan step does not account for.

The item closes as `delivered` with `BUG-0001` open against its behaviour. That is not a
contradiction: no acceptance criterion of WI-0001 covers any of that bug's three reproductions,
and the item is judged against its criteria. The bug is named in `item.md` `## Notes` so that the
relationship is visible from the item rather than only from the bug.
