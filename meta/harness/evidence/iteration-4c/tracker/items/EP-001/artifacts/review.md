# Review — EP-001

The ending of the engagement, not the review of a change. There is no branch, no diff and no
merge here: `EP-001` is an epic, its three children were each reviewed and merged on their own
close, and what is judged now is the engagement as a whole against the epic Definition of Done
(`spec/dor-dod.md` §4) and the stakeholder's answer to the sign-off.

## What I examined

**The tracker.**

- `tracker/items/EP-001/item.md` — the goal, the eight success measures, the scope and out-of-scope
  lists, and the notes as they stand after `answer-questions` took the acceptance into them
- `tracker/items/EP-001/history.md` and `journal.md` — the whole chain, five rows, from `intake`
  creating the epic to the acceptance being consumed
- `tracker/items/EP-001/questions/Q-001.md` … `Q-006.md` — all six, including `Q-004`, the
  `elicitation` question, and `Q-006`, the sign-off with the stakeholder's reply
- `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md` — status and outcome on
  each, and the acceptance criteria their reviews closed over
- `tracker/items/WI-000{1,2,3}/artifacts/verify-report.md` — each verdict and, in each, the
  `## Not verified, and why` section, which is where a gap this ending has to carry would be
- `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `tracker/items/WI-0003/questions/Q-001.md`,
  `Q-002.md` — the four refinement answers, read for the cross-answer check

**The code, in full.** Not a summary of it: `recall/store.py` (162 lines), `recall/schedule.py`
(55), `recall/cli.py` (245), `recall/__main__.py`, and the five test modules. This is what the
claims audit below is decided from.

**The tool, run.** Ten commands against a scratch deck at `/tmp/epicend/cards.txt`, each a
separate process, exercising every success measure that can be exercised without rebooting a
machine. Quoted under DE3 below.

**The documents, claim by claim, from their citations.** `docs/product/vision.md` (v7),
`docs/architecture/overview.md` (v5, as it stood at the start of this execution), and all nine
ADRs. What was opened for each claim, and what came of it, is under DE6.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| DE1 | Every child terminal, and every undelivered child named | **pass** | `WI-0001`, `WI-0002`, `WI-0003` are all `status: done` — read from each `item.md`, and `scripts/engagement-state EP-001` reports `at-rest: every child has stopped, no question is open, no request is open`. There is no undelivered child to name; all three are named anyway, by ID, in `EP-001/Q-006`'s `## Question`, which `check-epic-signoff` confirms ("names all 3 child item(s)"). No bug item was ever filed in this engagement, so no unfixed defect is hiding behind an unnamed child. |
| DE2 | Every child's outcome recorded; dropped items say why | **pass** | `outcome: delivered` on each of the three `item.md` files. Nothing was dropped, so the second clause is vacuous rather than skipped. |
| DE3 | Every success measure addressed — met, or explicitly not met with the reason | **pass, with one measure met in part** | Eight measures, walked one by one below the table. Seven are met and demonstrated by commands run in this execution; the eighth — the data survives a **reboot of the machine** — is met as to the file and untested as to the reboot, which is stated here, in `EP-001/item.md`, and was stated to the stakeholder before they accepted. |
| DE4 | `docs/product/` reflects what was built, not what was proposed | **pass** | `docs/product/vision.md` v7 read against the code. Its three action bullets describe `add`, `review` and `delete` as `recall/cli.py` implements them, including the duplicate-front warning, the count before the first card, the stop-part-way exit, and the confirmation before a deletion. Its exclusions describe absences that are real: no edit command, no list command, no undo, no second user — `_parser()` registers exactly three subcommands. Its `## Open with the stakeholder` now records the sign-off round and its answer. |
| DE5 | Open questions across all children closed, or re-filed | **pass** | Ten questions exist in the engagement — six on `EP-001`, two on `WI-0001`, two on `WI-0003`. Every one is `status: answered`; none is `open` and none is `deferred`. `validate-workspace` agrees, and `engagement-state` reads the same fact. |
| DE6 | Every claim in `docs/` about behaviour this epic delivered checked against the code during this epic; every citation resolves | **pass, one defect found and repaired** | The audit is below. `scripts/lint-claims --context epic` reports its own scope as "the whole document set rather than anything --changed-since could name; absolute claims: every document under docs; citations: every markdown file in the workspace" and exits 0 — but that is the mechanical half, and it is not what found the defect. Reading `docs/architecture/overview.md` §How it is checked against `tests/test_add.py` did. |
| DE7 | The stakeholder was asked whether they accept, after rest, and answered | **pass** | `EP-001/Q-006`, `kind: sign-off`, filed 2026-08-30T13:31:00Z, after rest was reached at 2026-08-30T13:26:28Z. `check-epic-signoff EP-001`: "carries the stakeholder's reply, names all 3 child item(s), and was filed after the engagement reached rest". Their reply: *"A — accept as complete."* |
| DE8 | The stakeholder was asked at least one open question that was not about the team's agenda, and it was answered | **pass** | `EP-001/Q-004`, `kind: elicitation`, filed by `intake` at 2026-08-30T11:06:26Z — at the **start** of the engagement, which is where it is worth something, not alongside the sign-off as the fallback route allows. It earned its place: their answer to it is what put deletion in scope as `WI-0003`, contradicting an exclusion the team had inferred. `check-epic-signoff` confirms: "DE8 satisfied by tracker/items/EP-001/questions/Q-004.md". |

### DE3, measure by measure

Every command below was run in this execution from the repository root, against a scratch deck at
`/tmp/epicend/cards.txt` set through `RECALL_CARD_FILE`, on 2026-08-30. Each command is a separate
process, so anything surviving between two of them survived a restart of the tool.

1. **Add a card from a terminal, restart, review the next day, and it is offered — with no
   re-entry.** *Met, in part by substitution.* `python3 -m recall add "bonjour" "hello"` → `Added:
   bonjour`, and a second process reading the file back shows `front: bonjour / back: hello /
   rung: 0 / due: 2026-08-30`. The next-day half was checked by WI-0002's verification with a
   controlled clock; the restart half is a restart of the **tool**, which every command here
   demonstrates. A restart of the **machine** is the gap in measure 8.
2. **On a day when some are due and others are not, a session offers exactly those due today or
   earlier, checkable against the file by hand.** *Met.* After answering both cards they became
   `due: 2026-08-31`; the immediately following `python3 -m recall review` printed `Nothing is
   due.` and exited 0. A third card added afterwards was `due: 2026-08-30` and the next review
   printed `1 card due.` — the set matches the file, read by eye.
3. **Wrong → due tomorrow; right → 1, 3, 7 or 30 days by rung; both visible in the file.** *Met.*
   Both cards at rung 0 answered in one session moved to `rung: 1 / due: 2026-08-31` — one day on,
   which is rung 1's interval. The four intervals and the wrong-answer reset are `INTERVALS = {1:
   1, 2: 3, 3: 7, 4: 30}` and `FIRST_RUNG = 1` in `recall/schedule.py`, and WI-0002's verification
   demonstrated every rung transition with a fixed date.
4. **A session started again the same day offers only what is still due, and no card already
   answered that day.** *Met.* The second `review` in the same minute printed `Nothing is due.`
5. **Every due card is offered, none withheld, and the count is stated before the first one.**
   *Met.* `2 cards due.` printed before `[1/2] bonjour`, and `1 card due.` before `[1/1] au
   revoir`. No cap exists in `recall/cli.py`: `review` iterates the whole of `due_positions`.
6. **Stopping part-way is supported, and killing the tool part-way loses no answer already
   given.** *Met.* `q` at the first prompt printed `Stopped. 0 cards answered; the rest are still
   due.` and exited 0. The no-loss half is structural and was verified on WI-0002: `store.save` is
   called after each card, before the next is printed (`recall/cli.py`, `review`).
7. **A card can be deleted and stops being offered.** *Met, demonstrated in both directions.*
   `review` offered `au revoir`; `delete "au revoir"` showed all four of its fields and removed it
   on `y`; the next `review` printed `Nothing is due.` A front matching nothing (`delete "nope"`)
   removed nothing and exited 1.
8. **The whole of the data lives in a file on the person's own machine and survives a reboot of
   it.** *Met as to the file; the reboot itself is untested.* The file is at the path the person
   controls, is plain UTF-8 text, and holds both the cards and their scheduling state — printed in
   full above. No machine was rebooted in this engagement. WI-0001's verification did better than
   read the code: it traced the syscalls `save` makes and confirmed the write is flushed and
   renamed before the command exits, which is what a reboot would need. That is strong evidence
   and it is not the measure. The stakeholder was told this in the sign-off before answering.

### DE6 — the claims audit, from the citations

Each claim below was decided by opening what it cites and reading that, not by reading the
sentence or a neighbouring document that repeats it.

- `overview.md` §How it is run, on `review` — offers every card due today or earlier, earliest
  first with ties in card-file order, count before the first card, back revealed only on Enter,
  `y`/`n`, written before the next card, `q` and end-of-stream stop without loss. **True**, read
  against `recall/cli.py`'s `review` and `recall/schedule.py`'s `due_positions` — `sorted()` on
  the due date is stable, so ties keep file order, and `_ask` returns `None` at EOF, which the
  caller treats as `q`.
- `overview.md` §How it is run, on `delete` — names the card by its front side, prints all four
  fields, removes only on `y`, exits 0 on a decline leaving the file byte-identical, exits non-zero
  on no match, lists numbered matches when a front is shared. **True**, read against `delete`,
  `_confirmed` and `_chosen_among`. The byte-identical claim holds because no `save` is reached on
  any declining path.
- `overview.md` §How it is run, "confirmations go to standard output; warnings and refusals go to
  standard error". **True** across all three subcommands, including `main`'s handler for a
  malformed card file.
- `overview.md` §Where the cards live — the two environment variables, each read as set **and
  non-empty**, and the directory created on first use. **True**, against `card_file_path()` and
  `save`'s `os.makedirs(directory, exist_ok=True)`.
- `overview.md` §What the card file looks like — the header, one block of four labelled lines per
  card, blocks separated by a blank line, a value being everything after the first `: ` verbatim,
  `rung` 0 for never answered and 1–4 otherwise, `due` as `YYYY-MM-DD`. **True**, against
  `_render`, `_parse`, `_value` and `_card`, and against the deck printed under DE3.
- `overview.md` §The pieces, the store bullet — "no append and no remove: `load` and `save` are the
  only two operations it offers". **True**, against `recall/store.py`'s public surface. This
  sentence was false from v1 to v4 and was repaired at WI-0003's close; re-read here from the
  module rather than trusted because it was recently repaired.
- `overview.md` §The pieces, the schedule bullet — pure functions, no file, no environment, no
  printing, the day passed in. **True**: `recall/schedule.py` imports `datetime` and `store` and
  nothing else, and every function takes `today` as an argument.
- `overview.md` §How it is checked — **FALSE, and repaired.** It said *"every test that runs the
  tool sets `RECALL_CARD_FILE` to a path inside a temporary directory and clears `XDG_DATA_HOME`
  from the child's environment"*. `tests/test_add.py` falsifies it twice:
  `test_default_path_is_the_documented_one` runs the tool with `RECALL_CARD_FILE` **unset** and
  `XDG_DATA_HOME` **set**, and `test_default_path_without_a_data_directory_is_under_home` runs it
  with `RECALL_CARD_FILE` unset and `HOME` redirected. Both must do this — the default path is
  precisely what they check, and it cannot be checked through the override. The property the
  sentence was reaching for, that no test run touches a real deck, is **true**: both redirect into
  the same per-test temporary directory, by a different route. See `## Findings`.
- `vision.md` §What it is for — the three action bullets and the persistence promise. **True**
  against `recall/cli.py`; the duplicate-front warning is `add`'s `any(card.front == front ...)`
  branch, which warns on stderr and adds the card regardless.
- `vision.md` §The spacing rule — a day, then three, then a week, then a month; wrong goes back to
  the start; due when the date is today or earlier. **True** against `INTERVALS`, `after_wrong`
  and `is_due`.
- `vision.md` §What it deliberately is not — no editor, no list, no undo, no second user, no
  browser. **True**: `_parser()` registers `add`, `review` and `delete` and nothing else, and no
  code path restores a deleted card.
- ADR-0006 §Decision — standard library only, package at the repository root, the two gate
  commands and what lint does not catch. **True**: no import outside the standard library in
  `recall/`, and both commands run clean here.
- ADR-0008 §Decision — the resolution order, set-but-empty treated as unset, the directory created,
  every save written through a temporary file and renamed, the whole file rewritten. **True**
  against `card_file_path()` and `save`, including the `fsync` of the file and of the directory.
  Its two `## Corrections` errata, which narrowed "set" to "set to a non-empty value", still match
  the code.
- ADR-0002, ADR-0004, ADR-0005, ADR-0007, ADR-0009 — the ladder, the file being the tool's to
  write, deletion by front side with a confirmation, the block format, the schedule living in its
  own module. **True**, each read against the module it names. `ADR-0005`'s v2 erratum about
  `depends-on` is a tracker fact, re-checked against `WI-0003/item.md`.

## Findings

**One, in `docs/architecture/overview.md`, and it is a documentation defect rather than a defect
in the code.** The sentence quoted under DE6 was a universal claim — *every* test that runs the
tool — supported by three citations, none of which was the file that contradicts it.
`tests/test_add.py` was the one test module the old sentence did not cite, and it is the one that
falsifies it. That is the D12 failure mode exactly: a citation that resolves is not a citation
that supports the sentence, and `lint-claims` exits 0 on both.

Nothing about the tests is wrong; the two path tests are right to do what they do, and the
property that matters — no test writes outside its own temporary directory — holds. Repaired in
place, `overview.md` v5 → v6, with the two routes distinguished and `tests/test_add.py` cited.
No code changed and no test changed, so nothing needed re-verifying.

**No finding against the code.** The diff of this engagement was reviewed hunk by hunk at each of
the three item closes; this execution re-read all three modules whole and found nothing to send
back. No bug item was filed by this execution, and none exists in the engagement.

## Accepted gaps

1. **A reboot was never performed.** Success measure 8 says the data survives a reboot of the
   machine; every piece of evidence stops at a restart of the tool, with WI-0001's syscall trace
   as the strongest substitute. Recorded in `EP-001/item.md` `## Notes` so it survives this
   review, and disclosed to the stakeholder in `EP-001/Q-006` before they accepted.
2. **The tool assumes it is the only writer of the card file.** Two concurrent sessions would end
   with the second to finish overwriting the first. Accepted deliberately in `ADR-0008` for a
   single-user local tool, and disclosed in the sign-off.
3. **No test exercises a card file that another process changes mid-session.** The gap follows
   from gap 2 and is recorded in WI-0002's verification.

None of the three is a defect in what was asked for; all three are limits of the evidence or of
the design, and all three are now written somewhere that outlives this document.

## Verdict

**Accept, and end the engagement as E1 — delivered.**

Every criterion of the epic Definition of Done passes. All three children are `done` with
`outcome: delivered`, every question in the engagement is answered, the documents were audited
from their citations with one false sentence found and repaired, and the stakeholder was asked at
rest and answered: *"A — accept as complete. This is what I asked for and it works."* They named
no follow-up work, so nothing is carried forward and no item is left behind. `EP-001` closes with
`outcome: delivered`.
