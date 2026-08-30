# Verification report — WI-0003

Verified-commit: 1ebf08efef963568d2f61eb1e8b1b1806958ea55

Branch `wi/WI-0003`, working tree clean at that commit before and after this execution.

## Verdict

**Pass.** All nine acceptance criteria were checked against commands this skill ran itself, and
all nine hold. No criterion was ambiguous, no defect belonging to this item was found, and no
bug item was filed. The item goes to `in-review`.

The criteria were read in full before `impl-report.md` was opened, and every command in the
table below was derived from the criterion's own sentence rather than from the report. The
report was read afterwards and agrees with what was found; nothing in this verdict rests on it.

One thing `review-close` must act on, which is not a defect in the code: `docs/architecture/overview.md`
v4 says `delete` is *"not yet started"* and *"named here so a reader can see where it will
attach"*. Those two sentences become false the moment this branch merges. `implement` declared
the obligation and correctly did not fix it — `spec/doc-header.md` §5 forbids it writing to
`docs/`. It is recorded in `## Defects found` below as a documentation obligation, not as a
send-back, because no acceptance criterion of this item is about the overview.

## Criteria

Card files were seeded by writing `ADR-0007`'s format directly (never by the tool), pointed at
with `RECALL_CARD_FILE`, and compared byte-for-byte with `cmp`/`md5sum -c` where a criterion
says "byte-identical". Every run below was a real invocation of `python3 -m recall`.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 — one argument, `y`, card removed, confirmation names the front, exit 0 | **pass** | seeded two cards; `printf 'y\n' \| RECALL_CARD_FILE=$F python3 -m recall delete "capital of France"` | prompt shown, then `Deleted: capital of France`; `EXIT=0`; file afterwards held only `front: capital of Spain / back: Madrid / rung: 0 / due: 2026-08-30` | the confirmation names the front side; the other card's four fields are untouched |
| AC2 — the card and its schedule shown first, `y`/`n` stated, `n` writes nothing and exits 0 | **pass** | `printf 'n\n' \| … delete "capital of France"` against a rung-3 card due 2026-09-04; and a second run against a rung-0 card | prompt read `About to delete:` / `front: capital of France` / `back:  Paris` / `rung:  3 of 4` / `due:   2026-09-04` / `Delete it? y to delete, n to keep.`; then `Nothing was deleted.`, `EXIT=0`, `cmp` reported the file **IDENTICAL**. The rung-0 card printed `rung:  0 of 4 (never answered)` | the four values are the record's own: `due` is the stored `YYYY-MM-DD` verbatim, and `rung` shows the stored integer inside `N of 4`. The rendering adds the ladder height; it does not transform the stored value, which is what the criterion's *"as that card's record holds it"* is guarding |
| AC3 — never offered again; count one lower; every other card unchanged | **pass** | seeded `alpha`/`beta`/`gamma` all due on or before today; ran `review` on a copy (`q` at the first card) to get the before-count; deleted `beta` with `y`; ran `review` on the result, walking both cards | before: `3 cards due.` — after: `2 cards due.`, offering `[1/2] alpha` and `[2/2] gamma`. `beta` appears **nowhere** in the post-deletion session output. The card file after the deletion held `alpha` at `rung: 1 / due: 2026-08-28` and `gamma` at `rung: 0 / due: 2026-08-30` — the seeded values | `beta`'s stored due date was 2026-08-29 and today is 2026-08-30, so the session was started on a date after it, which is the condition the criterion names |
| AC4 — the deletion is in the stored file; an emptied file still works | **pass** | deleted the only card, then `grep -c '^front:' $F`; then `python3 -m recall review`; then `python3 -m recall add "new front" "new back"` against the same file | `grep -c` printed `0` and `grep 'only card'` exited 1 (absent). `review` printed `Nothing is due.`, `EXIT=0`. `add` printed `Added: new front`, `EXIT=0`, and the file then held that one card | the file left behind is the two header lines and nothing else — still the tool's own format, read back by two later processes |
| AC5 — no match: no prompt, a message naming the front, non-zero exit, byte-identical | **pass** | three runs: a populated file with no such front; a file holding no cards; no file at all | each printed `No card has the front '<front>'.` and `Nothing was deleted.` to stderr with `EXIT=1`; `md5sum -c` reported **OK** for the two files that existed and the absent file was **still absent**; `grep -c "About to delete"` over stdout+stderr returned `0` for all three | the front side is quoted back in the message in every case |
| AC6 — several matches listed, numbered from 1 in card-file order, one chosen; `n` keeps all | **pass** | seeded `dup`/`other`/`dup`/`dup` — the non-matching card **interleaved** on purpose — then `printf '2\n' \| … delete "dup"`; and a second seeding answered `n` | the prompt printed `3 cards have the front 'dup'.`, then `[1]`,`[2]`,`[3]` each with `front`/`back`/`rung`/`due`, then `Which one? 1, 2, 3 to delete that card, n to keep them all.` Answering `2` printed `Deleted: dup`, `EXIT=0`, and the file afterwards held `dup/first back/1/2026-08-01`, `other/unrelated/3/2026-09-09` and `dup/third back/4/2026-08-03` — exactly the second match gone and every other record intact. Answering `n` gave `Nothing was deleted.`, `EXIT=0`, `cmp` **BYTES_IDENTICAL** | the interleaved `other` card is the point of the case: it proves the number is an index into the *matches* and the removal an index into the *file*, which is the one place a wrong mapping would destroy a card the person was not shown |
| AC7 — unrecognised input re-asks with the card reprinted; the stream ending deletes nothing | **pass** | `printf 'maybe\nn\n'` at the single prompt; `printf 'maybe\ny\n'`; `printf '0\n9\nyes\nn\n'` at the several-match prompt; and both prompts run with `< /dev/null` | `maybe` produced `Not one of the answers. This prompt takes: y, n.` and then the whole `About to delete:` block again — `grep -c 'front: solo'` counted the block **twice** — and the file was `BYTES_IDENTICAL`. `maybe` then `y` still **deleted** (so it was not counted as a no) and `maybe` then `n` still kept it (so it was not counted as a yes). At the listing prompt, `0`, `9` and `yes` were each refused with `This prompt takes: 1, 2, n.` and the full numbered listing reprinted — 4 listings for 3 refusals. Closed stdin at the single prompt and at the listing prompt both printed `Nothing was deleted.`, `EXIT=0`, `cmp` **BYTES_IDENTICAL** | `0` and an out-of-range `9` are refused like any other unrecognised text, which is the boundary the criterion's *"anything other than what that prompt has just said it takes"* covers |
| AC8 — an unparseable card file stops before any card is shown and any prompt | **pass** | seeded a file whose second card had `rung: not-a-number` on line 11, then `delete "alpha"` — a front that **does** exist in that file; and a second file with a mislabelled `bak:` line | `.qa-scratch/ac8/cards.txt: line 11: 'rung: not-a-number' is not a whole number`, `EXIT=1`, `grep -c "About to delete"` returned `0`, `cmp` **BYTES_IDENTICAL**. The second: `line 5: expected a line starting 'back: ', found 'bak: y'`, `EXIT=1` | the message names the file and the line; line 11 is the corrupt line. This is the same refusal `add` and `review` make (`WI-0002` AC14) |
| AC9 — wrong argument count is a usage message; an empty argument is AC5's no-match | **pass** | `delete` with no argument; `delete alpha extra`; `delete ""`; `delete "   "`; plus `add "" B` and `add "   " B` to confirm no card can hold such a front | no argument: `usage: recall delete [-h] front` / `recall delete: error: the following arguments are required: front`, `EXIT=2`. Two arguments: `usage: recall [-h] {add,review,delete} ...` / `recall: error: unrecognized arguments: extra`, `EXIT=2`. `""` and `"   "`: `No card has the front '<arg>'.` + `Nothing was deleted.` on stderr, `EXIT=1`. Both files `BYTES_IDENTICAL` in all four runs. `add` refused both empty fronts with `The front side is empty.` and exit 1 | recorded so a reader can judge it: the two cases name `delete` **differently**. The no-argument message is the `delete` subparser's own usage. The two-argument message is the top-level usage, where `delete` appears inside the choice list `{add,review,delete}` and the error line names the surplus argument rather than the subcommand. The criterion asks that the usage message name the `delete` subcommand; the token is present in both, so both pass on the criterion as written — but the second is weaker than the first, and if that distinction matters it is a wording change to AC9, not a defect in this code |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → `Ran 90 tests in 4.502s` / `OK`, exit 0, run on the branch head before any local change and again after every mutation was reverted |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → no output, exit 0 |
| `workspace-valid` | **pass** | `.claude/agile-skills/scripts/validate-workspace .` → `checked 4 item(s), 11 document(s)` / `0 errors, 0 warnings`, exit 0 |
| `every-criterion-independently-checked` | **pass** | every row of `## Criteria` names a command this execution ran and quotes its real output. The acceptance criteria were read before `impl-report.md` was opened; the report is cited nowhere as evidence |
| `negative-cases-exercised` | **pass** | see `## Negative and boundary cases exercised` — thirteen conditions triggered, not read about |
| `a-criterion-about-criteria-is-read` | **not applicable, and the underlying read was done anyway** | no criterion of WI-0003 has other criteria as its subject: AC1–AC9 each describe behaviour directly, and the citations to `WI-0001` AC2/AC6/AC7 and `WI-0002` AC13/AC14 are provenance for a decision, not a subject. The item's `## Out of scope` does make a claim of that shape in prose — *"`WI-0002`'s criteria all still read true against the session after this item ships"* — so it was read out rather than assumed; see `## The claim about WI-0002's criteria` below |
| `tests-would-fail-without-the-change` (advisory) | **pass** | nine mutations, each independently reverted; see `## Test sensitivity check` |

## Negative and boundary cases exercised

Each of these was *triggered* by a command in this execution, and its output is quoted in the
criteria table above.

1. A front side that matches no card, against a populated file — AC5.
2. A front side that matches no card, against a file holding a header and no cards — AC5.
3. A front side that matches no card, against a card file that **does not exist** — AC5; the file was still absent afterwards, so nothing created it.
4. An unrecognised answer (`maybe`) at the single-match prompt, followed by `n` — AC7.
5. The same unrecognised answer followed by `y`, to prove it was not silently counted as a no — AC7.
6. `0` at the several-match prompt — the boundary below the first number — AC7.
7. `9` at the several-match prompt — a number past the last match — AC7.
8. `yes` at the several-match prompt — text that begins with an accepted letter of the *other* prompt — AC7.
9. Closed stdin at the single-match prompt — AC7.
10. Closed stdin at the several-match prompt — AC7.
11. A card file with an unparseable `rung:` value, and a second with a mislabelled field line — AC8.
12. `delete` with no argument and `delete` with two arguments — AC9.
13. `delete ""` and `delete "   "` — AC9, and `add` was run with the same two values to confirm the criterion's premise that no stored card can hold such a front.

Two boundary cases beyond the criteria were exercised because they are where a positional mix-up
would hide: **the non-matching card interleaved among the matches** (AC6, the `other` card between
`dup` #1 and `dup` #2), and **deleting the last card in the file** (AC4), after which two further
processes read and wrote the file successfully.

## Test sensitivity check

Nine mutations were applied to `recall/cli.py`, one at a time, each followed by the full suite and
then a byte-for-byte restore from a copy taken before the first one (`cmp` confirmed the restore
each time, and `git status` was clean afterwards). Every mutation turned the suite red, so no
criterion is covered only by a test that passes against an absent implementation.

| # | mutation | AC it attacks | result |
|---|----------|---------------|--------|
| M1 | `store.save(path, cards)` deleted from `delete()` — the removal is never written | AC1, AC3, AC4 | `FAILED (failures=9)` |
| M2 | `_confirmed` returns the position without asking at all | AC2 | `FAILED (failures=8)` |
| M3 | the no-match path returns `EXIT_OK` instead of `EXIT_REFUSED` | AC5 | `FAILED (failures=9)` |
| M4 | `_chosen_among` returns `positions[0]` whatever number was typed | AC6 | `FAILED (failures=2)` |
| M5 | `_confirmed` treats anything but `n` as a yes, so a closed stream deletes | AC7 | `FAILED (failures=2)` |
| M6 | `_ask` prints the prompt once instead of on every re-ask, so the card is not reprinted | AC7 | `FAILED (failures=3)`, naming `test_an_unrecognised_answer_re_asks_with_the_card_reprinted`, `test_an_unrecognised_answer_re_asks_the_whole_listing` and `tests.test_review`'s equivalent |
| M7 | `main()`'s `CardFileError` handler returns `EXIT_OK` | AC8 | `FAILED (failures=3)` |
| M8 | the `delete` subparser's `front` becomes `nargs="?"`, so no argument is legal | AC9 | `FAILED (failures=1)` |
| M9 | `_described` drops the `rung` and `due` lines from the prompt | AC2 | `FAILED (failures=3)` |

Every criterion is attacked by at least one mutation: AC1/AC3/AC4 by M1, AC2 by M2 and M9, AC5 by
M3, AC6 by M4, AC7 by M5 and M6, AC8 by M7, AC9 by M8.

## The claim about WI-0002's criteria

WI-0003's `## Out of scope` claims that `review` is untouched and that all fourteen of WI-0002's
criteria still read true. That is not an acceptance criterion of this item, so it is not ticked
anywhere — but it is a claim, so it was read rather than assumed.

`git diff main...HEAD -- recall/cli.py` shows `review()`, `_stopped()`, `_ask()`, `add()` and
`_side_error()` **unchanged, byte for byte**. `recall/schedule.py` and `recall/store.py` are not in
the diff at all. The only edits touching existing code are `_parser()` gaining a `delete`
subparser and `main()` becoming one explicit branch per subcommand — a rewrite that preserves the
`add` and `review` dispatch and removes a fall-through.

So each of WI-0002 AC1–AC14 describes code this change did not modify, and each sentence remains
true for that reason. **Non-intersection does not apply here**: things executable do exercise the
old criteria together with the new behaviour. `tests/test_review.py`'s 60-test suite runs green on
this branch head; `tests/test_delete.py`'s `NeverOfferedAgainTests` runs a real `review` session
after a real deletion; `OtherSubcommandsTests.test_add_and_review_still_dispatch_to_themselves`
exercises the rewritten `main()` for the two older subcommands; and this execution independently
ran `review` twice against a deleted-from file (AC3 above), seeing the count fall from 3 to 2 with
the survivors' order and state intact — which is WI-0002 AC2, AC10 and AC12 read against WI-0003's
behaviour in one command.

## Defects found

**None against this item's acceptance criteria.** No send-back, and no bug item filed.

One **documentation obligation** is carried forward to `review-close`, recorded here so it cannot
be lost:

- `docs/architecture/overview.md` v4 line 12 — *"`delete` not [yet started]"* — and lines 35–36 —
  *"`delete` is named here so a reader can see where it will attach"* — are true of `main` and
  false of this branch. They become false in the trunk at the merge. `implement` declared this as
  a D7/D12 obligation and did not fix it, which is correct: `spec/doc-header.md` §5 names
  `implement` as a skill that does not write to `docs/`, and the same restriction applies to this
  skill. `review-close` owns the repair, at the same version bump that records the merge.

No unrequested behaviour was found. The diff is `recall/cli.py` (+97 lines, all of them accounted
for by plan steps 2–6), `tests/test_delete.py` (new, plan step 7), and tracker files. Nothing in
the code is unaccounted for by a criterion and a plan step.

## Not verified, and why

1. **The card file's default location.** Every run in this report set `RECALL_CARD_FILE`, so
   `delete` was never exercised against `$XDG_DATA_HOME/recall/cards.txt` or the `$HOME` fallback.
   That path is `ADR-0008`'s and `WI-0001`'s, `delete` calls the same `store.card_file_path()` as
   `add` and `review`, and writing to a real home directory from a verification run would leave
   state behind. It is covered by `tests/test_store.py`, unchanged on this branch.
2. **A concurrent second writer.** `delete` reads, waits at a prompt for as long as the person
   likes, then rewrites the whole file. Another `recall` process writing in between would be lost.
   The plan names this and WI-0002's close already accepted it for the whole tool; no criterion of
   this item covers it, and it was not exercised. It remains an open property of the store, not a
   defect of this item.
3. **Non-ASCII and unusual front sides.** Matching is exact equality on the stored string, so a
   front differing only by case, by surrounding whitespace or by unicode normalisation does not
   match. `NoMatchTests.test_a_near_miss_is_not_a_match` covers the near miss and this execution
   confirmed exact matching on ordinary text, but no normalisation case was constructed. This is
   `plan.md` assumption 2, deliberate and recorded there.
4. **Interactive use at a real terminal.** Every run drove the tool with piped stdin or
   `/dev/null`. `Ctrl-D` at a tty was not pressed by a person; the closed-stream case stands in
   for it, which is the same evidence `WI-0002` AC11 rests on.
5. **The prompt as seen on a narrow terminal.** `_described` does not wrap, so a long side runs
   past the edge. No criterion constrains the width and none was checked.
