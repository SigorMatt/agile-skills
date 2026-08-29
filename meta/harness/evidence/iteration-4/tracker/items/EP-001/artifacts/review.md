# Review — EP-001

The ending of the engagement, not the review of a change. There is no branch and no diff: an
epic's children carry the code, and each of `WI-0001`..`WI-0004` was reviewed and merged under
its own `review.md`. What is judged here is whether the engagement as a whole delivered what was
asked, whether the record says so truthfully, and whether the person who asked for it agreed —
against `spec/dor-dod.md` §4.

## What I examined

**The engagement's own state.**

- `scripts/engagement-state EP-001` → `at-rest`, rest reached `2026-08-29T13:58:30Z` — every
  child stopped, no question open anywhere, no request open.
- `tracker/items/EP-001/item.md` — `## Goal`, `## Success measures` SM1–SM5, `## Scope` (now
  final), `## Out of scope`.
- `tracker/items/EP-001/history.md` — nine rows, chaining without a gap, last row `→ open`
  matching `item.md`. Eight journal entries in `journal.md`, one for every row after creation.
- All seven questions on the epic (`Q-001`..`Q-007`) and the one on each of `WI-0001`
  (`Q-001`, `Q-002`), `WI-0002`, `WI-0003`, `WI-0004` — all `answered`, each with
  `## Consequences` naming files that exist.
- `Q-006` in full: the stakeholder's reply, *"A — accept as complete… close it out"*.

**The behaviour, re-run by me rather than read about.** A scratch store under
`RECALL_FILE=/tmp/smcheck/store.json`, driving the `recall` executable as a user would. This is
the second time these measures have been run at an ending, deliberately: the first run's evidence
is a claim like any other, and DE3 is not satisfied by re-reading it.

- SM1 — `recall add "bonjour" "hello"` in one process, `recall list` in another printed
  `1	bonjour	hello`. Present in the next run, no import step.
- SM2 — the same card was offered by `recall review` on the day it was added; its stored `due`
  was `2026-08-29`, the day of the run.
- SM3 — answered right (`\ny\n`), then a second `recall review` in a fresh process on the same
  day printed `Nothing is due today.`
- SM4 — a five-step ladder walk, resetting `due` to today between steps (the documented way to
  move a card, `ADR-0007`): `interval` 1 → 3 → 7 → 30 → 30, `due` 2026-08-30 → 09-01 → 09-05 →
  09-28 → 09-28. Two rights in a row put the card at 2026-09-01 against 2026-08-30 after one —
  strictly later, which is what SM4 asks. A wrong answer then returned it to `interval` 1,
  `due` 2026-08-30, the day after the review and the shortest rung, not the rung it had reached.
- SM5 — `cat` of the store showed pretty-printed JSON with `number`, `question`, `answer`,
  `due`, `result`, `interval` per card. Every one of SM1–SM4 above was confirmed from that file's
  contents, without the tool.

**The test suite**, on the trunk as the project actually has it: `python3 -m unittest discover -s
tests -t .` → `Ran 101 tests… OK`.

**The claims, from their citations** (DE6 — each opened, not re-read from the prose):

- `docs/architecture/overview.md` *"491 lines, of which roughly 260 are code"*
  `[src: run: wc -l recall.py → 491]` — ran `wc -l recall.py` → **491**; an AST split gives 260
  code lines against 90 blank, 24 comment and 118 docstring. Both halves hold. This is the claim
  that failed DE6 at the previous ending (it said *"roughly 280"*), so it is the one checked
  hardest.
- *"20 functions and one exception class"* `[src: recall.py]` — parsed the module: 20 top-level
  functions, one class, `StoreError`.
- *"`load` and `save` are the only functions that touch the disk at all"* `[src: recall.py]` —
  grepped every `open(`, `os.replace`, `tempfile`, `.write(`: lines 112, 184, 191, 194, all
  inside `load` (104–173) and `save` (174–202). `add_card`, `delete_card`, `due_cards`,
  `next_interval`, `record_result` (212–284) contain none. The seam the design decision rests on
  is real.
- *"`delete` removes one card by its number, immediately and with no confirmation prompt,
  printing what it removed"* `[src: WI-0004 AC2]` — `recall delete 2` printed
  `Deleted card 2	merci	thank you` with no prompt; `recall delete 1 3` refused with
  `usage: recall delete <card number>`, exit 2.
- *"surviving cards keep the numbers they had"* and *"deleting the highest-numbered card frees
  its number"* `[src: ADR-0008]` — after deleting 2 from {1,2,3}, `list` gave 1 and 3; after
  deleting 3, the next `add` was numbered **2**. Both halves hold.
- `ADR-0009`'s exit code — `recall delete 9` against a store with no card 9 printed
  `recall delete: there is no card 9` and exited **1**, not 2.
- `docs/product/vision.md` v4 — the ladder, the binary result, a new card due the day it is
  added, 30 staying at 30, wrong coming back the next day and not the same day: each confirmed by
  the SM3/SM4 runs above. *"`recall delete <n>` removes one card at once"* confirmed as above.
  *"Not a card editor"* — no `edit` command exists; `recall` with no argument prints
  `usage: recall <add|list|review|delete>`.
- `WI-0001` AC5's documented location — `README.md:146-150` names `~/.recall.json` and the
  `RECALL_FILE` override, matching `store_path()`.

**The record's reachability** — `git log --grep` returns 8 commits for `EP-001`, 14 for
`WI-0001`, 19 for `WI-0002`, 18 for `WI-0003`, 15 for `WI-0004`. Nine ADRs under
`docs/architecture/adr/`.

## Definition of Done

Epic Definition of Done, `spec/dor-dod.md` §4.

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| DE1 | every child terminal, every undelivered child named | **pass** | `WI-0001`, `WI-0002`, `WI-0003`, `WI-0004` all `status: done`; none undelivered, so there is nothing the outcome must qualify. `check-epic-signoff EP-001` confirms `Q-006` names all 4 children |
| DE2 | every child's `outcome` recorded; dropped items say why | **pass** | all four carry `outcome: delivered` in `item.md`; no child was dropped, so the `## Notes` obligation does not arise |
| DE3 | every success measure addressed — met, or not met with the reason | **pass** | SM1–SM5 each re-run by me against the trunk in a scratch store, transcripts under *What I examined*. All five met; none needs a not-met reason |
| DE4 | `docs/product/` reflects what was built, not what was proposed | **pass** | `vision.md` v4: `## Where this stands` records the tool as finished and accepted; `recall delete` recorded as built (it is); editing, decks, statistics and a schedule command recorded as out (no such commands exist — `usage: recall <add\|list\|review\|delete>`) |
| DE5 | open questions closed or re-filed against a follow-up | **pass** | all 12 questions across the epic and its four children are `status: answered`; `engagement-state` reports none open |
| DE6 | claims in `docs/` about delivered behaviour checked against the code **during this epic**; every citation resolves | **pass** | the eight claim checks above, each decided by opening the cited source. `lint-claims --changed-since main` → 0 errors, 0 warnings. One accepted gap below |
| DE7 | the stakeholder was asked after rest, and answered | **pass** | `check-epic-signoff EP-001` → PASS: `Q-006` carries the reply, names all 4 children, and was filed after rest was reached at 2026-08-29T13:58:30Z |

## Findings

None that send anything back. Two observations that belong in the record:

1. **The DE6 failure from the previous ending is genuinely fixed, not merely edited.**
   `overview.md` v5 no longer leads with a size, and the sentence that now carries the
   store-stays-in-one-module decision names the seam function by function. I checked the seam
   itself rather than the sentence about it: `load` and `save` are the only disk-touching
   functions in the module, so the decision rests on something a reader can re-check in one
   grep. The re-ask trigger is stated as *something other than a command needs the store*, which
   cannot go stale the way a line count did.

2. **Two of the review-close hard gates cannot apply to an epic ending, and say so themselves.**
   `check-commit-refs EP-001 main` exits 1 with *"main is already merged into main, so main..main
   is empty"*, and `check-verify-freshness EP-001 main` exits 1 with *"EP-001 has no
   verify-report.md"*. Both are correct: an epic has no branch and no verification of its own,
   and `SKILL.md`'s own precondition 4 says so — *"There is no code to review and no branch to
   merge."* They are recorded as **skipped, with the reason**, not forced. This is a toolkit
   observation rather than a defect in this engagement.

## Accepted gaps

1. **`ADR-0002` carries three unsourced absolute claims that no skill may fix.**
   `lint-claims --all` reports `claim.unsourced` at `ADR-0002:72`, `:97` and `:102` — *"used
   exactly as given"* about `RECALL_FILE`, *"every criterion in EP-001"*, and *"exactly one pile
   per user account"*. I checked all three against the code and they are **true**: `store_path()`
   returns the override unmodified with no `expanduser`, every measure in this review was in fact
   run against a temporary store via that variable, and the default resolves to one path per home
   directory. What is missing is provenance, not correctness. It cannot be repaired: `spec/
   doc-header.md` §5 makes an ADR superseded-only, and adding a citation is an edit rather than a
   supersession, so no legal move clears it. Accepted, recorded here and in `EP-001/Q-007`, and
   left in place rather than fixed out of contract.

2. **The contracted form of the claims gate is blind on this path.** `claims-are-sourced` runs
   `lint-claims --changed-since main`, and at an epic ending there is no branch, so the diff
   against the trunk is empty and the gate reports *"checked no documents"* and exits 0. It
   passed here, but it would have passed over anything. I therefore also ran `--all`, and the
   three errors above are what that found. The gate's verdict is recorded as the contract
   defines it; the real audit is the claim-by-claim work under *What I examined*.

3. **The store accepts the JSON number `1.0` where `1` is expected.** Carried forward from
   `WI-0003`'s review, disclosed to the stakeholder at sign-off and waved off — *"that `1.0`
   thing in the store file doesn't bother me"* (`Q-005`). It is recorded in the epic's
   `## Out of scope` so that it survives this closing, and no item covers it, deliberately.

## Verdict

**Accept — ending E1, delivered.** Every child is `done` with `outcome: delivered`, all seven
epic Definition of Done criteria pass, and the stakeholder was asked after the engagement reached
rest and accepted it unconditionally (`Q-006`, option A). `EP-001` closes `open → done` with
`outcome: delivered`.
