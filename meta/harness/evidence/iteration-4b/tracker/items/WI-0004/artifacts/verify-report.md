# Verification report — WI-0004

Verified-commit: ffef942134b0c6e3304a417e51bacfc43ddb2b15

That commit is the head of branch `wi/WI-0004` as verification ran. (The branch name was on
the `Verified-commit:` line itself until review; `check-verify-freshness` matches the sha to
end of line, so the parenthetical made the gate report the line as missing. Only the format
changed — the sha, and everything verified against it, is untouched.)

Every command below was run by this skill against that commit, with `PATH` set to the checkout's
`bin/` and `HOME` set to a fresh empty temporary directory per case, so each case starts with no
deck. Nothing here is taken from `impl-report.md`; the report was read afterwards, to compare.

## Verdict

**Pass.** All twelve acceptance criteria hold, each demonstrated by a command run here with its
output quoted below. No criterion of this item failed, so there is no send-back. One defect was
observed that is **not** this item's — `delete` inherits BUG-0001, which is already filed — and it
is recorded under `## Defects found` rather than as a new bug.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | three cards added with `recall add`, then `printf 'y\n' \| recall delete --question "der Hund"`, then `recall list` | `der Hund` / `  the dog` / `delete this card? [y/n] Deleted. The deck now holds 2 card(s).` → exit 0; the listing then gives `die Katze \| the cat` and `das Pferd \| the horse` | both sides printed **before** the prompt; the deleted question does not appear in the listing and the other two are unchanged |
| AC2 | **pass** | the `recall list` above is a separate process from the delete; `recall list \| grep -c "der Hund"` | `0` (grep exit 1), and the other two cards present | the listing process shares nothing with the deleting one but the deck file, so what it shows came off disk |
| AC3 | **pass** | deck file written directly with X due today, Y due today+7, Z due today; `delete X`, `delete Y`, each with `y`; then `recall review` driven by a here-document supplying an empty line and `y` | `Z question` / `  [press return to see the answer]   Z answer` / `  did you get it right? [y/n]   next review: 2026-08-31 (in 1 day)` → exit 0 | neither `X question` nor `Y question` appears anywhere; Y was **not** due (seven days out) and was still deletable |
| AC4 | **pass** | two-card deck; `printf 'y\n' \| recall delete --question "die Katzen"` | exit **2**; stderr `recall delete: refusing -- no card has the question 'die Katzen'. Type it exactly as recall list shows it. Nothing has been removed.`; stdout empty | sha256 of the deck file identical before and after; no `[y/n]` and neither answer side on stdout |
| AC5 | **pass** | two cards added with the same question side (`der See`); `printf 'y\n' \| recall delete --question "der See"` | exit **2**; stderr `recall delete: refusing -- 2 cards have the question 'der See', and recall cannot tell which one you mean. Nothing has been removed.` | the count is in the message; sha256 identical before and after; `recall list` still shows both cards. Also checked with **three** duplicates: the message says `3 cards`, so the count is real and not a hard-coded 2 |
| AC6 | **pass** | two-card deck; four runs of `recall delete --question "der Hund"` with stdin `n`, `maybe`, an empty line, and `< /dev/null` | each: exit **0**, stdout `… delete this card? [y/n] Not deleted. The deck is exactly as it was.`, `[y/n]` occurring **once**, stderr empty (no `Traceback`), sha256 identical | the prompt is not re-asked on `maybe`, which is the clause that separates this from `review`; `recall list` afterwards still shows both cards |
| AC7 | **pass** | one-card deck; `recall delete` with `--question` omitted, `""`, `"   "`, and `" \t "` — then the same four against an empty `HOME` | each: exit **2**, stderr `recall delete: refusing -- --question must be given and must not be blank. The deck was not touched.`, no `[y/n]` on stdout, sha256 identical | with no deck, `find $HOME -type f` gives `0` files afterwards: nothing was created |
| AC8 | **pass** | deck file written as `not json at all`, then as a truncated `{"version": 1, "cards": [{"question": "a"`; `printf 'y\n' \| recall delete --question …` on each | exit **3** both times; stderr names the file: `recall: cannot read the deck file /tmp/…/deck.json -- it is not valid JSON (Expecting value, line 1). Nothing has been written…` | both the malformed and the truncated case; sha256 identical before and after; no prompt issued |
| AC9 | **pass** | empty `HOME`; `printf 'y\n' \| recall delete --question "anything"` | exit **2**; stderr `… no card has the question 'anything' …` | deck file absent, its parent directory absent, `$HOME/.local` absent, `find $HOME -type f` → `0`; no prompt |
| AC10 | **pass** | one-card deck; delete with `y`; then `recall list`; then `recall add`; then `recall list` | `Deleted. The deck now holds 0 card(s).` (exit 0); `The deck is empty. Add a card with: recall add --question "..." --answer "..."` (exit 0); `Added. The deck now holds 1 card(s).` (exit 0); `der Hund \| the dog` | the deck file on disk is `{"version": 1, "cards": []}` — empty and valid, not unreadable |
| AC11 | **pass** | deck file written with rungs 0/2/3 and due dates −2/+5/+30 days; delete the middle card with `y`; compare the JSON before and after | `version same: True`, `count: 2`, `entries identical (question/answer/rung/due, in order): True`, `order: ['first', 'third']`, `any grade key added: False` | the comparison is of the parsed entries as whole dicts, so an added or changed key would show |
| AC12 | **pass** | see `## The criterion whose subject is other criteria` below | — | read, with tests as evidence |

All twelve boxes are now ticked in `item.md`.

## The criterion whose subject is other criteria

**AC12 covers `WI-0001` AC3 and `WI-0001` AC6 by ID.** Per `spec/dor-dod.md`, each is read against
this item's behaviour and given its own verdict; the tests are evidence for the reading, not its
definition.

- **`WI-0001` AC3** — *"After `recall add` twice with different cards, `recall list` writes both
  cards to stdout and exits 0. Each card's question side and answer side are both shown, and each
  is shown exactly as it was given — no trimming beyond the blank check in AC2, no case change, no
  truncation."* **Still true.** Read against the new behaviour: `delete` adds no field to the deck
  file, and `cmd_list` is not in the diff. Demonstrated on a deck containing a card with a leading
  capital and an internal double space, after a deletion — `recall list | cat -A` gives
  `Der  Bahnhof | The  Station$` and `das Pferd | the horse$`, exit 0. Both sides, verbatim, no
  number, no code, no extra column, no trailing whitespace.
- **`WI-0001` AC6** — *"`recall list` with no cards in the deck writes a line to stdout saying the
  deck is empty and exits 0. It is not an error and it does not print an empty page with no
  explanation."* **Still true.** Read against the new behaviour: the new way to reach an empty deck
  is to delete every card, and the empty deck that leaves is the same value an unstarted deck has.
  Demonstrated by deleting all three cards and running `recall list`:
  `The deck is empty. Add a card with: recall add --question "..." --answer "..."`, exit 0.

**Non-intersection: none.** Two executable cases exercise `recall delete` and the listing's shape
together, so this criterion does not have to be waived and nothing is being laundered by a coverage
gap: `tests/test_delete.py::DeleteTests::test_listing_is_unchanged_by_a_deletion` asserts the exact
lines and their shape after a deletion, and `…::test_deleting_the_last_card_leaves_an_empty_deck`
asserts the empty-deck message and exit 0 on a deck emptied by deleting. Both were run on their own
here: `python3 -m unittest tests.test_delete.DeleteTests.test_listing_is_unchanged_by_a_deletion
tests.test_delete.DeleteTests.test_deleting_the_last_card_leaves_an_empty_deck -v` → `Ran 2 tests …
OK`. The tests are the evidence; the two paragraphs above are the assessment.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 55 tests in 8.427s / OK`, run by this skill on `ffef942` |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → `checked 6 item(s), 12 document(s) / 0 errors, 0 warnings` |
| `every-criterion-independently-checked` | **pass** | the table above records, for each of AC1–AC12, a command this skill ran and its actual output. No row cites `impl-report.md` |
| `negative-cases-exercised` | **pass** | see `## Negative and boundary cases exercised` — every error, empty-input and boundary clause was triggered, not read about |
| `a-criterion-about-criteria-is-read` | **pass** | AC12's covered criteria named by ID, each with its own verdict read from its sentence; non-intersection stated (there is none) with the two covering cases named |
| `tests-would-fail-without-the-change` (advisory) | **pass** | three mutations, run by this skill — see `## Test sensitivity check` |

## Negative and boundary cases exercised

Each was produced here, not inferred:

- **No card matches** (AC4) — exit 2, message on stderr, deck byte-identical, no prompt.
- **Two cards match** (AC5) — exit 2, `2 cards` in the message, both cards still listed. **Three
  cards match**, beyond the criterion — the message says `3 cards`, so the count is computed.
- **Four cancelling replies** (AC6) — `n`, `maybe`, an empty line, closed standard input. All exit
  0, all print `Not deleted.`, none re-asks, none writes.
- **Missing and blank `--question`** (AC7) — omitted, `""`, spaces, tabs; and each of the four
  again with no deck present, confirming nothing is created.
- **Unreadable deck** (AC8) — both a wholly malformed file and a truncated one; exit 3 each,
  file untouched.
- **Absent deck and absent parent directory** (AC9) — exit 2, and the home directory still holds
  zero files afterwards.
- **The empty deck a deletion leaves** (AC10) — `recall list` and `recall add` both still work
  against it; the file on disk is `{"version": 1, "cards": []}`.
- **A card that is not due** (AC3) — Y, due in seven days, deleted successfully; deletion is not
  restricted to due cards.
- **Reply forms around the accepted one**, checking `plan.md` `## Assumptions` 1 and the sentence
  `docs/process/using-recall.md` now prints: ` Y ` (capital, surrounded by spaces) **deletes**,
  and `yes` **does not** — it cancels with exit 0. The documentation's claim that "capital letters
  and surrounding spaces are fine" is therefore true as written.

## Test sensitivity check

Three mutations were applied to the branch by this skill, each run, each reverted; the working
tree was confirmed clean afterwards (`git status --short recall/` → empty) and the full suite
re-run green (`Ran 55 tests … OK`).

| mutation | result | which criterion it protects |
|----------|--------|------------------------------|
| `positions_matching` compares with `in` instead of `==` (substring matching) | `FAIL: test_no_such_card_is_refused` | AC4 — a near-miss string must not match a card |
| `cmd_delete`'s confirmation branch replaced with `if False:` (every deletion goes through) | `FAIL: test_anything_but_yes_cancels` ×4 (`n`, unrecognised word, empty line, closed input) | AC6 — the guard the stakeholder asked for |
| `Deck.remove` reverses the survivors after deleting | `FAIL: test_survivors_keep_their_schedules` ×3 and `FAIL: test_listing_is_unchanged_by_a_deletion` | AC11, AC12 — order is preserved, not merely the set |

No test passed against removed behaviour. The remaining criteria are exercised through `bin/recall`
against a subcommand that does not exist on `main`, so removing it fails them on exit code.

## Defects found

**None of this item's own.** One pre-existing defect was confirmed to extend to the new subcommand,
and it is **not** a WI-0004 criterion failure and not a new bug:

- `recall delete` inherits **BUG-0001**. With the deck path existing as a *directory*
  (`mkdir -p $HOME/.local/share/recall/deck.json`), `printf 'y\n' | recall delete --question "x"`
  exits **1** with `IsADirectoryError: [Errno 21] Is a directory: /tmp/…/deck.json` and a Python
  traceback on stderr. AC8 is not violated: AC8 governs a deck file that "cannot be read **as a
  deck**", which is `store.DeckUnreadable`, and that path was verified above. This is the class
  BUG-0001 already describes — *"`recall/cli.py` catches `store.DeckUnreadable` and nothing else,
  so any other filesystem error … escapes `main`"* — so no new bug is filed. Whoever plans
  BUG-0001 should know that the fix now has four subcommands to cover rather than three; that is
  recorded here rather than by editing BUG-0001, which is another item's artifact.

## Not verified, and why

- **AC7's tab case is delivered by the shell, not by a literal tab in the criterion.** The four
  blank forms were sent as `""`, `"   "` and `" \t "` via `printf`-quoted shell arguments. A tab
  typed into an interactive terminal with readline may be intercepted before it reaches the
  process; that is a property of the terminal, not of `recall`, and it is out of this item's
  scope.
- **"Survives a reboot" is not re-verified here.** It is `WI-0001` AC7 and was verified there.
  AC2's requirement — surviving the *process* ending — was verified, which is what AC2 asks.
- **Concurrency is not verified.** Two `recall delete` runs racing over one deck file is specified
  nowhere in this item and nothing here exercises it. `ADR-0004`'s atomic rename bounds the damage
  to "one of the two writes wins", but that is an argument, not a measurement.
- **Message wording is checked only where a criterion names it.** No criterion fixes a sentence,
  so the assertions above are on exit codes, the presence of the option name, the count, the file
  path, and the substrings `Not deleted` and `deck is empty`. The full sentences were read against
  `docs/process/using-recall.md` v6 and agree with it, but that agreement is a documentation check,
  not a criterion.
